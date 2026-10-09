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
CHILD_CAP = 256
RIGID_TOLERANCE = 1e-5


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
        # The codec bytes are the zlib header; validate its checksum too.
        inflater = zlib.decompressobj()
        data = inflater.decompress(raw[12:], total_size + 1)
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

    ranges = [(0, 12)]

    def reserve(offset, size):
        span(offset, size)
        if any(offset < end and start < offset + size for start, end in ranges):
            raise Refusal('overlapping-spans')
        ranges.append((offset, offset + size))

    def geometry(root, used_vertices=0, used_faces=0):
        span(root, 0xf0 if data[root + 4] == 10 else 0xe0)
        polygon_offset = pointer(root + 0x8c)
        factor = read('<3f', root + 0x90)
        center = read('<3f', root + 0xa0)
        if not all(math.isfinite(value) for value in factor + center):
            raise Refusal('nonfinite-coordinate')
        vertex_offset = pointer(root + 0xb0)
        vertex_count, face_count = read('<2i', root + 0xc8)
        if vertex_count + used_vertices > VERTEX_CAP or face_count + used_faces > FACE_CAP:
            raise Refusal('count-cap')
        if vertex_count < 3 or face_count < 1:
            raise Refusal('invalid-count')
        span(vertex_offset, vertex_count * 6)
        span(polygon_offset, face_count * 32)
        reserve(root, 0xf0 if data[root + 4] == 10 else 0xe0)
        reserve(vertex_offset, vertex_count * 6)
        reserve(polygon_offset, face_count * 32)
        vertices = tuple(tuple(q*s+c for q,s,c in zip(read('<3h', vertex_offset+6*i), factor, center)) for i in range(vertex_count))
        if not all(math.isfinite(value) for vertex in vertices for value in vertex):
            raise Refusal('nonfinite-coordinate')
        faces = []
        for index in range(face_count):
            indices = read('<4H', polygon_offset + 32*index + 16)
            if any(value & 0x8000 for value in indices):
                raise Refusal('unsupported-index-flags', 'unsupported')
            if any(value >= vertex_count for value in indices):
                raise Refusal('invalid-index')
            polygon_faces = (indices[:3],) if indices[3] == 0 else (indices[:3], (indices[2], indices[3], indices[0]))
            if len(faces) + len(polygon_faces) + used_faces > FACE_CAP:
                raise Refusal('count-cap')
            if len(set(indices if indices[3] else indices[:3])) != (4 if indices[3] else 3):
                raise Refusal('invalid-face')
            normal = read('<3f', polygon_offset + 32*index)
            if not all(math.isfinite(value) for value in normal) or not any(normal):
                raise Refusal('invalid-face')
            for face in polygon_faces:
                a,b,c = (vertices[i] for i in face)
                u,v = tuple(b[i]-a[i] for i in range(3)), tuple(c[i]-a[i] for i in range(3))
                cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
                if not all(math.isfinite(value) for value in cross) or not any(cross):
                    raise Refusal('invalid-face')
                faces.append(face)
        return Inspection(vertices, tuple(faces))

    root = pointer(8)
    kind = read('<B', root + 4)[0]
    if kind in (4, 10):
        return geometry(root)
    if kind != 12:
        raise Refusal('unsupported-root', 'unsupported')
    reserve(root, 0xa0)
    count, capacity = read('<2H', root + 0x90)
    if count != capacity:
        raise Refusal('unsupported-child-counts', 'unsupported')
    if not 1 <= count <= CHILD_CAP:
        raise Refusal('child-count-cap')
    children = pointer(root + 0x80)
    matrices = pointer(root + 0x84)
    reserve(children, count * 4)
    reserve(matrices, count * 64)
    boxes = pointer(root + 0x8c)
    reserve(boxes, count * 32)
    internal = read('<I', root + 0x88)[0]
    if internal:
        internal = pointer(root + 0x88)
        if internal != matrices:
            reserve(internal, count * 64)
    vertices, faces = [], []
    for index in range(count):
        lower, upper = read('<3f', boxes + index * 32), read('<3f', boxes + index * 32 + 16)
        if (not all(math.isfinite(value) for value in lower + upper)
                or any(a > b for a, b in zip(lower, upper))):
            raise Refusal('invalid-child-box')
        child = pointer(children + index * 4)
        if read('<B', child + 4)[0] not in (4, 10):
            raise Refusal('unsupported-child', 'unsupported')
        mesh = geometry(child, len(vertices), len(faces))
        matrix = tuple(read('<3f', matrices + index * 64 + row * 16) for row in range(4))
        if not all(math.isfinite(value) for row in matrix for value in row):
            raise Refusal('nonfinite-transform')
        if internal and any(read('<3f', internal + index * 64 + row * 16) != matrix[row]
                            for row in range(4)):
            raise Refusal('unsupported-internal-motion', 'unsupported')
        a, b, c = matrix[:3]
        determinant = (a[0]*(b[1]*c[2]-b[2]*c[1])
                       - a[1]*(b[0]*c[2]-b[2]*c[0])
                       + a[2]*(b[0]*c[1]-b[1]*c[0]))
        if (abs(determinant - 1) > RIGID_TOLERANCE
                or any(abs(sum(matrix[i][axis] * matrix[j][axis] for axis in range(3))
                           - (1 if i == j else 0)) > RIGID_TOLERANCE
                       for i in range(3) for j in range(i, 3))):
            raise Refusal('unsupported-transform', 'unsupported')
        base = len(vertices)
        vertices.extend(tuple(sum(vertex[row] * matrix[row][axis] for row in range(3))
                              + matrix[3][axis] for axis in range(3)) for vertex in mesh.vertices)
        faces.extend(tuple(base + value for value in face) for face in mesh.faces)
    if not all(math.isfinite(value) for vertex in vertices for value in vertex):
        raise Refusal('nonfinite-coordinate')
    for face in faces:
        a, b, c = (vertices[i] for i in face)
        u, v = tuple(b[i]-a[i] for i in range(3)), tuple(c[i]-a[i] for i in range(3))
        cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        if not all(math.isfinite(value) for value in cross) or not any(cross):
            raise Refusal('invalid-transformed-face')
    return Inspection(tuple(vertices), tuple(faces))


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
