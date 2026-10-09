"""Authored synthetic fixtures; no game data."""
import importlib.util
from pathlib import Path
import json
import os
import subprocess
import tempfile
import struct
import sys
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('collision_inspector', ROOT / 'tools/gtaiv-collision/inspect_resource.py')
inspector = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inspector
SPEC.loader.exec_module(inspector)


def geometry():
    data = bytearray(512)
    struct.pack_into('<I', data, 8, 0x50000020)
    data[0x24] = 4
    struct.pack_into('<I', data, 0x20 + 0x8c, 0x50000120)
    struct.pack_into('<3f', data, 0x20 + 0x90, 1, 1, 1)
    struct.pack_into('<3f', data, 0x20 + 0xa0, 1, 2, 3)
    struct.pack_into('<I', data, 0x20 + 0xb0, 0x50000100)
    struct.pack_into('<2i', data, 0x20 + 0xc8, 3, 1)
    struct.pack_into('<9h', data, 0x100, 0,0,0, 2,0,0, 0,2,0)
    struct.pack_into('<4f8H', data, 0x120, 0,0,1, 2, 0,1,2,0, 0xffff,0xffff,0xffff,0xffff)
    return data


def resource(data):
    return struct.pack('<III', 0x05435352, 0x20, 2) + zlib.compress(data, level=9)


class CollisionTests(unittest.TestCase):
    def test_command_rejects_invalid_zlib_framing(self):
        raw = resource(geometry())
        cases = [
            ('missing-checksum', raw[:-4]),
            ('truncated-checksum', raw[:-1]),
            ('corrupt-checksum', raw[:-1] + bytes([raw[-1] ^ 1])),
            ('trailing-data', raw + b'extra'),
            ('concatenated-stream', raw + zlib.compress(b'extra', level=9)),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'private-resource.wbn'
            command = [sys.executable, str(ROOT / 'tools/gtaiv-collision/inspect_resource.py'), str(path)]
            for case, payload in cases:
                with self.subTest(case=case):
                    path.write_bytes(payload)
                    result = subprocess.run(command, capture_output=True, text=True, timeout=3)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(json.loads(result.stdout), {'verdict':'invalid', 'reason':'decompression-error'})
                    self.assertEqual(result.stderr, '')

    def test_rejects_truncation_and_bad_indices(self):
        data = geometry()
        struct.pack_into('<H', data, 0x130, 9)
        for raw, reason in [(b'RSC', 'truncated-header'), (resource(data), 'invalid-index'), (resource(geometry())[:-1], 'decompression-error')]:
            with self.subTest(reason=reason):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(raw)
                self.assertEqual(raised.exception.reason, reason)

    def test_caps_and_unsupported_layouts_refuse_explicitly(self):
        for change, reason, verdict in [
            ((0x24, '<B', 12), 'unsupported-root', 'unsupported'),
            ((0x24, '<B', 0), 'unsupported-root', 'unsupported'),
            ((0x136, '<H', 1), 'unsupported-quad', 'unsupported'),
            ((0xe8, '<i', 40000), 'count-cap', 'invalid'),
        ]:
            data = geometry()
            struct.pack_into(change[1], data, change[0], change[2])
            with self.subTest(reason=reason):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data))
                self.assertEqual((raised.exception.reason, raised.exception.verdict), (reason, verdict))
        raw = struct.pack('<IIIH', 0x05435352, 0x20, 2047 | (15 << 11), 0xda78)
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(raw)
        self.assertEqual(raised.exception.reason, 'decompressed-cap')

    def test_invalid_faces_coordinates_and_pointer_tags_refuse(self):
        cases = [(0x20 + 0x90, '<f', float('nan'), 'nonfinite-coordinate'),
                 (0x132, '<H', 0, 'invalid-face'),
                 (8, '<I', 0x60000020, 'invalid-pointer'),
                 (0x20 + 0xb0, '<I', 0x500001ff, 'invalid-span')]
        for offset, fmt, value, reason in cases:
            data = geometry()
            struct.pack_into(fmt, data, offset, value)
            with self.subTest(reason=reason):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data))
                self.assertEqual(raised.exception.reason, reason)

    def test_command_emits_only_source_safe_verdict_and_refuses_nonfiles(self):
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory) / 'private-asset-name.wbn'
            private.write_bytes(resource(geometry()))
            command = [sys.executable, str(ROOT / 'tools/gtaiv-collision/inspect_resource.py')]
            result = subprocess.run(command + [str(private)], capture_output=True, text=True, timeout=3)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout), {'verdict':'structurally-decoded', 'reason':'validated-geometry'})
            self.assertEqual(result.stderr, '')
            for args in [[str(private)+'-missing'], [str(private), 'private-extra'], [directory], ['--private-option']]:
                result = subprocess.run(command + args, capture_output=True, text=True, timeout=3)
                self.assertEqual(json.loads(result.stdout)['verdict'], 'invalid')
                self.assertNotIn('private', result.stdout + result.stderr)
            if hasattr(os, 'mkfifo'):
                fifo = Path(directory) / 'private-fifo'
                os.mkfifo(fifo)
                result = subprocess.run(command + [str(fifo)], capture_output=True, text=True, timeout=3)
                self.assertEqual(json.loads(result.stdout)['reason'], 'not-regular-file')

    def test_header_payload_limits_and_invalid_faces_are_bounded(self):
        original = resource(geometry())
        bomb = resource(b'x' * 513)
        cases = [(bytes(inspector.INPUT_CAP + 1), 'input-cap'),
                 (bomb, 'decompressed-size'),
                 (original + b'extra', 'decompression-error')]
        for offset, fmt, value, reason in [
            (0x130, '<H', 0x8000, 'unsupported-index-flags'),
            (0xac, '<I', 0x50000100, 'overlapping-spans'),
            (0x100, '<9h', (0,0,0, 1,0,0, 2,0,0), 'invalid-face'),
            (0x120, '<f', float('inf'), 'invalid-face'),
        ]:
            data = geometry()
            struct.pack_into(fmt, data, offset, *(value if isinstance(value, tuple) else (value,)))
            cases.append((resource(data), reason))
        for raw, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(raw)
                self.assertEqual(raised.exception.reason, reason)

    def test_short_primitive_header_reports_unsupported_before_geometry_span(self):
        data = geometry()
        struct.pack_into('<I', data, 8, 0x500001f0)
        data[0x1f4] = 1
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(data))
        self.assertEqual((raised.exception.verdict, raised.exception.reason), ('unsupported', 'unsupported-root'))

    def test_known_triangle_is_decoded_in_rage_coordinates(self):
        result = inspector.decode_resource(resource(geometry()))
        self.assertEqual(result.vertices, ((1.0,2.0,3.0), (3.0,2.0,3.0), (1.0,4.0,3.0)))
        self.assertEqual(result.faces, ((0,1,2),))

if __name__ == '__main__':
    unittest.main()
