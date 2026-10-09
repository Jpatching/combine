# SPDX-License-Identifier: GPL-3.0-only
# New bounded implementation referring to GTA4Unity/RageLib format definitions.
# See README.md for provenance and inherited attribution, LICENSE for terms.
"""Read-only structural inspection. No runtime or placement qualification."""
from dataclasses import dataclass
import json
import os
import stat
import sys
import math
import struct
import zlib


INPUT_CAP = 16 * 1024 * 1024
DECOMPRESSED_CAP = 32 * 1024 * 1024
VERTEX_CAP = 32767
FACE_CAP = 100000


@dataclass(frozen=True)
class Inspection:
    vertices: tuple
    faces: tuple


class Refusal(ValueError):
    def __init__(self, reason, verdict='invalid'):
        self.reason, self.verdict = reason, verdict
        super().__init__(reason)


def decode_resource(raw):
    if len(raw) > INPUT_CAP:
        raise Refusal('input-cap')
    if len(raw) < 14:
        raise Refusal('truncated-header')
    magic, kind, flags, codec = struct.unpack_from('<IIIH', raw)
    if magic != 0x05435352:
        raise Refusal('unsupported-resource-version', 'unsupported')
    if kind != 0x20:
        raise Refusal('unsupported-resource-type', 'unsupported')
    if codec != 0xda78:
        raise Refusal('unsupported-codec', 'unsupported')
    system_size = (flags & 0x7ff) << (((flags >> 11) & 15) + 8)
    graphics_size = ((flags >> 15) & 0x7ff) << (((flags >> 26) & 15) + 8)
    total_size = system_size + graphics_size
    if total_size > DECOMPRESSED_CAP:
        raise Refusal('decompressed-cap')
    try:
        inflater = zlib.decompressobj(-15)
        data = inflater.decompress(raw[14:], total_size + 1)
        if len(data) > total_size or inflater.unconsumed_tail:
            raise Refusal('decompressed-size')
        if not inflater.eof or inflater.unused_data:
            raise Refusal('decompression-error')
    except zlib.error:
        raise Refusal('decompression-error') from None

    if len(data) != total_size:
        raise Refusal('decompressed-size')
    data = data[:system_size]

    def span(offset, size):
        if offset < 0 or offset + size > len(data):
            raise Refusal('invalid-span')

    def read(fmt, offset):
        span(offset, struct.calcsize(fmt))
        return struct.unpack_from(fmt, data, offset)

    def pointer(offset):
        value = read('<I', offset)[0]
        if value >> 28 != 5 or (value & 0x0fffffff) == 0:
            raise Refusal('invalid-pointer')
        return value & 0x0fffffff

    root = pointer(8)
    span(root, 5)
    if data[root + 4] != 4:
        raise Refusal('unsupported-root', 'unsupported')
    span(root, 0xd0)
    polygon_offset = pointer(root + 0x8c)
    factor = read('<3f', root + 0x90)
    center = read('<3f', root + 0xa0)
    if not all(math.isfinite(value) for value in factor + center):
        raise Refusal('nonfinite-coordinate')
    vertex_offset = pointer(root + 0xb0)
    vertex_count, face_count = read('<2i', root + 0xc8)
    if vertex_count > VERTEX_CAP or face_count > FACE_CAP:
        raise Refusal('count-cap')
    if vertex_count < 3 or face_count < 1:
        raise Refusal('invalid-count')
    span(vertex_offset, vertex_count * 6)
    span(polygon_offset, face_count * 32)
    ranges = [(0, 12), (root, root+0xd0), (vertex_offset, vertex_offset+vertex_count*6), (polygon_offset, polygon_offset+face_count*32)]
    for i, (start, end) in enumerate(ranges):
        if any(start < other_end and other_start < end for other_start, other_end in ranges[:i]):
            raise Refusal('overlapping-spans')
    vertices = tuple(tuple(q*s+c for q,s,c in zip(read('<3h', vertex_offset+6*i), factor, center)) for i in range(vertex_count))
    if any(read('<H', polygon_offset + 32*i + 22)[0] & 0x7fff for i in range(face_count)):
        raise Refusal('unsupported-quad', 'unsupported')
    if any(value & 0x8000 for i in range(face_count) for value in read('<4H', polygon_offset + 32*i + 16)):
        raise Refusal('unsupported-index-flags', 'unsupported')
    faces = tuple(tuple(index & 0x7fff for index in read('<3H', polygon_offset+32*i+16)) for i in range(face_count))
    if any(index >= vertex_count for face in faces for index in face):
        raise Refusal('invalid-index')
    if not all(math.isfinite(value) for vertex in vertices for value in vertex):
        raise Refusal('nonfinite-coordinate')
    for index, face in enumerate(faces):
        if len(set(face)) != 3:
            raise Refusal('invalid-face')
        a,b,c = (vertices[i] for i in face)
        u,v = tuple(b[i]-a[i] for i in range(3)), tuple(c[i]-a[i] for i in range(3))
        cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        normal = read('<3f', polygon_offset + 32*index)
        if not all(math.isfinite(value) for value in normal) or not any(normal):
            raise Refusal('invalid-face')
        if not all(math.isfinite(value) for value in cross) or not any(cross):
            raise Refusal('invalid-face')
    return Inspection(vertices, faces)


def inspect_file(path):
    """Read one regular local file. Never expose input-derived text."""
    try:
        # Check before opening, then recheck the opened descriptor. NONBLOCK
        # prevents a replacement FIFO from blocking on POSIX systems.
        if not stat.S_ISREG(os.stat(path).st_mode):
            raise Refusal('not-regular-file')
        descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0))
        with os.fdopen(descriptor, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode):
                raise Refusal('not-regular-file')
            if info.st_size > INPUT_CAP:
                raise Refusal('input-cap')
            raw = stream.read(INPUT_CAP + 1)
        decode_resource(raw)
        return {'verdict':'structurally-decoded', 'reason':'validated-geometry'}
    except Refusal as refusal:
        return {'verdict':refusal.verdict, 'reason':refusal.reason}
    except (OSError, ValueError):
        return {'verdict':'invalid', 'reason':'file-unavailable'}


def main(args=None):
    args = sys.argv[1:] if args is None else args
    if len(args) != 1 or args[0].startswith('-'):
        result = {'verdict':'invalid', 'reason':'invalid-arguments'}
    else:
        result = inspect_file(args[0])
    print(json.dumps(result, sort_keys=True))
    return {'structurally-decoded':0, 'unsupported':2, 'invalid':1}[result['verdict']]


if __name__ == '__main__':
    sys.exit(main())
