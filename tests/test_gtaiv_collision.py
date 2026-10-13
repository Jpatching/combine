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
    units, shift = len(data) // 256, 0
    while units > 2047:
        units //= 2
        shift += 1
    return struct.pack('<III', 0x05435352, 0x20, units | (shift << 11)) + zlib.compress(data, level=9)


def composite():
    """Authored IV composite: one BVH triangle, rotated +90 Z then translated."""
    data = bytearray(1024)
    struct.pack_into('<I', data, 8, 0x50000020)
    data[0x24] = 12
    struct.pack_into('<4I2H', data, 0xa0,
                     0x500000c0, 0x500000d0, 0x500000d0, 0x50000110, 1, 1)
    struct.pack_into('<I', data, 0xc0, 0x50000140)
    # Fourth lanes are padding, not homogeneous coordinates.
    struct.pack_into('<16f', data, 0xd0,
                     0,1,0,float('nan'), -1,0,0,float('nan'),
                     0,0,1,float('nan'), 10,20,30,float('nan'))
    struct.pack_into('<4f4f', data, 0x110, 1,2,3,0, 3,4,3,0)
    original = geometry()
    data[0x140:0x210] = original[0x20:0xf0]
    data[0x144] = 10
    struct.pack_into('<I', data, 0x140+0x8c, 0x50000260)
    struct.pack_into('<I', data, 0x140+0xb0, 0x50000240)
    data[0x240:0x252] = original[0x100:0x112]
    data[0x260:0x280] = original[0x120:0x140]
    return data


def two_children(vertex_count=3, face_count=1):
    data = composite()
    polygon_start = (0x100 + vertex_count * 6 + 31) // 32 * 32
    stride = polygon_start + face_count * 32
    data.extend(bytes(((0x400 + 2 * stride + 4095) // 4096 * 4096) - len(data)))
    struct.pack_into('<4I2H', data, 0xa0,
                     0x500000c0, 0x500000d0, 0, 0x50000160, 2, 2)
    data[0x110:0x150] = data[0xd0:0x110]
    struct.pack_into('<3f', data, 0x140, 0,0,0)
    for i in range(2):
        root = 0x400 + stride * i
        struct.pack_into('<I', data, 0xc0 + i * 4, 0x50000000 + root)
        struct.pack_into('<4f4f', data, 0x160 + i * 32, 1,2,3,0, 3,4,3,0)
        source = geometry()
        data[root:root+0xd0] = source[0x20:0xf0]
        data[root+4] = 10
        struct.pack_into('<I', data, root+0x8c, 0x50000000+root+polygon_start)
        struct.pack_into('<I', data, root+0xb0, 0x50000000+root+0x100)
        struct.pack_into('<2i', data, root+0xc8, vertex_count, face_count)
        data[root+0x100:root+0x112] = source[0x100:0x112]
        data[root+polygon_start:root+stride] = source[0x120:0x140] * face_count
    return data


def dictionary():
    """Authored NY WBD: two distinct hashes and independently placed meshes."""
    data = bytearray(1024)
    struct.pack_into('<IHH', data, 16, 0x50000020, 2, 2)
    struct.pack_into('<IHH', data, 24, 0x50000028, 2, 2)
    struct.pack_into('<2I', data, 32, 0x01020304, 0x11121314)
    struct.pack_into('<2I', data, 40, 0x50000040, 0x50000200)
    for root, vertices, polygons, center in [(64, 320, 352, (1,2,3)), (512, 768, 800, (10,20,30))]:
        original = geometry()
        data[root:root+0xd0] = original[0x20:0xf0]
        struct.pack_into('<I', data, root+0xb0, 0x50000000+vertices)
        struct.pack_into('<I', data, root+0x8c, 0x50000000+polygons)
        struct.pack_into('<3f', data, root+0xa0, *center)
        data[vertices:vertices+18] = original[0x100:0x112]
        data[polygons:polygons+32] = original[0x120:0x140]
    return data


def dictionary_with_box():
    data = dictionary()
    data.extend(bytes(1024))
    struct.pack_into('<I', data, 40, 0x50000400)
    data[0x404] = 3
    struct.pack_into('<2f', data, 0x408, 5, 5)
    struct.pack_into('<3f', data, 0x410, 4,6,8)
    struct.pack_into('<3f', data, 0x420, 1,2,3)
    struct.pack_into('<3f', data, 0x430, 2.5,4,5.5)
    struct.pack_into('<3f', data, 0x450, 2.5,4,5.5)
    struct.pack_into('<3f', data, 0x470, 0.1,0.1,0.1)
    return data


class CollisionTests(unittest.TestCase):
    def test_dictionary_reports_box_primitive_separately_from_polygon_meshes(self):
        result = inspector.decode_resource(resource(dictionary_with_box()), dictionary=True)
        box = result.entries[0][1]
        self.assertIsInstance(box, inspector.BoxInspection)
        self.assertEqual((box.minimum, box.maximum, box.centroid), ((1,2,3), (4,6,8), (2.5,4,5.5)))
        self.assertFalse(hasattr(box, 'vertices'))
        self.assertEqual(result.entries[1][1].vertices, ((10,20,30),(12,20,30),(10,22,30)))

    def test_dictionary_with_primitive_refuses_complete_polygon_output_and_labels_cli(self):
        result = inspector.decode_resource(resource(dictionary_with_box()), dictionary=True)
        with self.assertRaises(inspector.Refusal) as raised:
            result.polygon_entries()
        self.assertEqual((raised.exception.verdict, raised.exception.reason),
                         ('unsupported', 'unsupported-box-geometry'))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'private-primitive.wbd'
            path.write_bytes(resource(dictionary_with_box()))
            command = [sys.executable, str(ROOT / 'tools/gtaiv-collision/inspect_resource.py'), '--dictionary', str(path)]
            completed = subprocess.run(command, capture_output=True, text=True, timeout=3)
            self.assertEqual((completed.returncode, json.loads(completed.stdout), completed.stderr),
                             (0, {'verdict':'structurally-decoded', 'reason':'validated-dictionary-with-primitives'}, ''))

    def test_dictionary_box_requires_complete_finite_positive_extent_fields(self):
        for offset, value in [(0x410, float('nan')), (0x430, float('inf')),
                              (0x450, float('nan')), (0x470, -0.1),
                              (0x408, -1), (0x420, 4)]:
            data = dictionary_with_box()
            struct.pack_into('<f', data, offset, value)
            with self.subTest(offset=offset):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data), dictionary=True)
                self.assertEqual(raised.exception.reason, 'invalid-box-fields')
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(dictionary_with_box()[:1536]), dictionary=True)
        self.assertEqual(raised.exception.reason, 'invalid-span')


    def test_dictionary_preserves_hashes_and_independent_bound_geometry(self):
        result = inspector.decode_resource(resource(dictionary()), dictionary=True)
        self.assertEqual(tuple(key for key, _ in result.entries), (0x01020304, 0x11121314))
        self.assertEqual(tuple(mesh.vertices for _, mesh in result.entries),
                         (((1,2,3),(3,2,3),(1,4,3)), ((10,20,30),(12,20,30),(10,22,30))))
        self.assertEqual(tuple(mesh.faces for _, mesh in result.entries), (((0,1,2),), ((0,1,2),)))

    def test_dictionary_command_reports_whole_resource_verdict_without_keys_or_geometry(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'private-dictionary.wbd'
            path.write_bytes(resource(dictionary()))
            command = [sys.executable, str(ROOT / 'tools/gtaiv-collision/inspect_resource.py'), '--dictionary', str(path)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=3)
            self.assertEqual((result.returncode, json.loads(result.stdout), result.stderr),
                             (0, {'verdict':'structurally-decoded', 'reason':'validated-dictionary'}, ''))
            data = dictionary()
            data[0x204] = 1
            path.write_bytes(resource(data))
            result = subprocess.run(command, capture_output=True, text=True, timeout=3)
            self.assertEqual((result.returncode, json.loads(result.stdout), result.stderr),
                             (2, {'verdict':'unsupported', 'reason':'unsupported-root'}, ''))

    def test_dictionary_refuses_incomplete_spans_counts_duplicates_and_shared_payloads(self):
        cases = [
            (8, '<I', 0x50000040, 'unsupported-dictionary-parent'),
            (20, '<H', 1, 'unsupported-dictionary-counts'),
            (20, '<HH', (257,257), 'unsupported-dictionary-counts'),
            (24, '<I', 0x60000028, 'invalid-pointer'),
            (16, '<I', 0x500003fc, 'invalid-span'),
            (24, '<I', 0x50000020, 'overlapping-spans'),
            (36, '<I', 0x01020304, 'duplicate-dictionary-key'),
            (44, '<I', 0x50000040, 'overlapping-spans'),
            (44, '<I', 0x50000020, 'unsupported-root'),
            (44, '<I', 0x500003fe, 'invalid-span'),
            (512+0xb0, '<I', 0x50000140, 'overlapping-spans'),
        ]
        for offset, fmt, value, reason in cases:
            data = dictionary()
            struct.pack_into(fmt, data, offset, *(value if isinstance(value, tuple) else (value,)))
            with self.subTest(reason=reason):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data), dictionary=True)
                self.assertEqual(raised.exception.reason, reason)
        for count in (0, 257):
            data = dictionary()
            struct.pack_into('<2H', data, 20, count, count)
            struct.pack_into('<2H', data, 28, count, count)
            with self.assertRaises(inspector.Refusal) as raised:
                inspector.decode_resource(resource(data), dictionary=True)
            self.assertEqual(raised.exception.reason, 'dictionary-count-cap')

    def test_dictionary_caps_aggregate_geometry_before_reading_next_bound(self):
        data = dictionary()
        struct.pack_into('<i', data, 512+0xc8, inspector.VERTEX_CAP)
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(data), dictionary=True)
        self.assertEqual(raised.exception.reason, 'count-cap')

    def test_composite_triangulates_unflagged_quad_without_changing_winding(self):
        data = composite()
        struct.pack_into('<i', data, 0x140+0xc8, 4)
        struct.pack_into('<12h', data, 0x240, 0,0,0, 2,0,0, 2,2,0, 0,2,0)
        struct.pack_into('<4H', data, 0x270, 0,1,2,3)
        result = inspector.decode_resource(resource(data))
        self.assertEqual(result.vertices, ((8,21,33), (8,23,33), (6,23,33), (6,21,33)))
        self.assertEqual(result.faces, ((0,1,2), (2,3,0)))

    def test_composite_combines_children_and_bounds_total_output(self):
        result = inspector.decode_resource(resource(two_children()))
        self.assertEqual(result.vertices, ((8,21,33), (8,23,33), (6,21,33),
                                           (-2,1,3), (-2,3,3), (-4,1,3)))
        self.assertEqual(result.faces, ((0,1,2), (3,4,5)))
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(two_children(vertex_count=17000)))
        self.assertEqual(raised.exception.reason, 'count-cap')

    def test_composite_caps_aggregate_faces_and_rejects_shared_child_buffers(self):
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(two_children(face_count=50001)))
        self.assertEqual(raised.exception.reason, 'count-cap')
        data = two_children()
        first, second = (value & 0x0fffffff for value in struct.unpack_from('<2I', data, 0xc0))
        data[second+0xb0:second+0xb4] = data[first+0xb0:first+0xb4]
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(data))
        self.assertEqual(raised.exception.reason, 'overlapping-spans')

    def test_direct_bvh_root_and_quad_rejections(self):
        data = composite()
        struct.pack_into('<I', data, 8, 0x50000140)
        self.assertEqual(inspector.decode_resource(resource(data)).vertices,
                         ((1,2,3), (3,2,3), (1,4,3)))
        for indices, reason in [((0,1,2,0x8003), 'unsupported-index-flags'),
                                ((0,1,2,3), 'invalid-index'),
                                ((0,1,2,1), 'invalid-face')]:
            struct.pack_into('<4H', data, 0x270, *indices)
            with self.assertRaises(inspector.Refusal) as raised:
                inspector.decode_resource(resource(data))
            self.assertEqual(raised.exception.reason, reason)

    def test_composite_applies_child_rotation_then_translation(self):
        result = inspector.decode_resource(resource(composite()))
        self.assertEqual(result.vertices, ((8,21,33), (8,23,33), (6,21,33)))
        self.assertEqual(result.faces, ((0,1,2),))

    def test_composite_refuses_nonfinite_and_nonrigid_transforms(self):
        for offset, value, reason in [(0xd0, float('nan'), 'nonfinite-transform'),
                                      (0x100, float('inf'), 'nonfinite-transform'),
                                      (0xd4, 2, 'unsupported-transform'),
                                      (0xf8, -1, 'unsupported-transform'),
                                      (0xd4, 0, 'unsupported-transform')]:
            data = composite()
            struct.pack_into('<f', data, offset, value)
            with self.subTest(reason=reason, offset=offset):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data))
                self.assertEqual(raised.exception.reason, reason)

    def test_composite_refuses_different_internal_transform(self):
        data = composite()
        struct.pack_into('<I', data, 0xa8, 0x50000300)
        data[0x300:0x340] = data[0xd0:0x110]
        self.assertEqual(inspector.decode_resource(resource(data)).vertices[0], (8,21,33))
        struct.pack_into('<f', data, 0x330, 11)
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(data))
        self.assertEqual((raised.exception.verdict, raised.exception.reason),
                         ('unsupported', 'unsupported-internal-motion'))

    def test_composite_validates_child_boxes_and_all_referenced_spans(self):
        for offset, fmt, value, reason in [
            (0xac, '<I', 0x500003ff, 'invalid-span'),
            (0xac, '<I', 0x500000d0, 'overlapping-spans'),
            (0x110, '<f', float('nan'), 'invalid-child-box'),
            (0x110, '<f', 4, 'invalid-child-box'),
        ]:
            data = composite()
            struct.pack_into(fmt, data, offset, value)
            with self.subTest(reason=reason, offset=offset):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data))
                self.assertEqual(raised.exception.reason, reason)

    def test_composite_rejects_transformed_triangle_precision_loss(self):
        data = composite()
        struct.pack_into('<3f', data, 0x100, 1e30,1e30,1e30)
        with self.assertRaises(inspector.Refusal) as raised:
            inspector.decode_resource(resource(data))
        self.assertEqual(raised.exception.reason, 'invalid-transformed-face')

    def test_composite_refuses_incomplete_or_unsupported_children(self):
        for offset, fmt, value, reason, verdict in [
            (0xb0, '<H', 0, 'unsupported-child-counts', 'unsupported'),
            (0xb0, '<HH', (257,257), 'child-count-cap', 'invalid'),
            (0xb0, '<HH', (0,0), 'child-count-cap', 'invalid'),
            (0xc0, '<I', 0, 'invalid-pointer', 'invalid'),
            (0xa4, '<I', 0, 'invalid-pointer', 'invalid'),
            (0xa4, '<I', 0x500003f0, 'invalid-span', 'invalid'),
            (0xc0, '<I', 0x50000020, 'unsupported-child', 'unsupported'),
            (0x144, '<B', 1, 'unsupported-child', 'unsupported'),
            (0x144, '<B', 12, 'unsupported-child', 'unsupported'),
            (0x276, '<H', 1, 'invalid-face', 'invalid'),
        ]:
            data = composite()
            struct.pack_into(fmt, data, offset, *(value if isinstance(value, tuple) else (value,)))
            with self.subTest(reason=reason, offset=offset):
                with self.assertRaises(inspector.Refusal) as raised:
                    inspector.decode_resource(resource(data))
                self.assertEqual((raised.exception.reason, raised.exception.verdict), (reason, verdict))

    def test_composite_command_keeps_geometry_private_and_refuses_whole_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'private-composite.wbn'
            command = [sys.executable, str(ROOT / 'tools/gtaiv-collision/inspect_resource.py'), str(path)]
            path.write_bytes(resource(two_children()))
            result = subprocess.run(command, capture_output=True, text=True, timeout=3)
            self.assertEqual((result.returncode, json.loads(result.stdout), result.stderr),
                             (0, {'verdict':'structurally-decoded', 'reason':'validated-geometry'}, ''))
            data = two_children()
            second = struct.unpack_from('<I', data, 0xc4)[0] & 0x0fffffff
            data[second+4] = 1
            path.write_bytes(resource(data))
            result = subprocess.run(command, capture_output=True, text=True, timeout=3)
            self.assertEqual((result.returncode, json.loads(result.stdout), result.stderr),
                             (2, {'verdict':'unsupported', 'reason':'unsupported-child'}, ''))

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
            ((0x24, '<B', 11), 'unsupported-root', 'unsupported'),
            ((0x24, '<B', 0), 'unsupported-root', 'unsupported'),
            ((0x136, '<H', 1), 'invalid-face', 'invalid'),
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
