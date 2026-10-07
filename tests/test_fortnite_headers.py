"""Synthetic format probes; no game bytes, keys or logs."""
import importlib.util
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    'fortnite_headers', Path(__file__).resolve().parents[1] /
    'tools/fortnite-export/check_headers.py')
headers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(headers)


def footer(flag=0, version=4, offset=0, size=16, magic=0x5A6F12E1):
    return bytes([flag]) + struct.pack('<IIqq', magic, version, offset, size) + bytes(20)


class HeaderTests(unittest.TestCase):
    def test_v4_has_no_guid_and_index_can_end_at_45_byte_footer(self):
        report = headers.parse_footer(footer(), 61)
        self.assertTrue(report['indexInBounds'])
        self.assertTrue(report['indexEndsAtFooter'])
        self.assertFalse(report['encryptedIndexFlag'])

    def test_encrypted_flag_is_metadata_only(self):
        self.assertTrue(headers.parse_footer(footer(flag=1), 61)['encryptedIndexFlag'])

    def test_bad_magic_version_flag_and_truncation(self):
        for data in [footer(magic=0), footer(version=7), footer(flag=2), footer()[:-1]]:
            with self.subTest(data_length=len(data)), self.assertRaises(ValueError):
                headers.parse_footer(data, 61)

    def test_negative_and_overrun_ranges(self):
        for offset, size in [(-1, 16), (0, -1), (17, 0), (1, 16), (2**63-1, 16)]:
            with self.subTest(offset=offset, size=size), self.assertRaises(ValueError):
                headers.parse_footer(footer(offset=offset, size=size), 61)

    def test_short_file_rejected_even_with_full_buffer(self):
        with self.assertRaises(ValueError):
            headers.parse_footer(footer(), 44)

    def test_cli_preserves_input_and_existing_report(self):
        private = Path(__file__).resolve().parents[1] / '.private'
        private.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=private) as folder:
            root = Path(folder)
            source = root / 'input'
            source.mkdir()
            data = bytes(16) + footer(flag=1)
            (source / 'fixture.pak').write_bytes(data)
            output = root / 'report.json'
            command = [sys.executable, headers.__file__, str(source), str(output)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_bytes()
            self.assertEqual((source / 'fixture.pak').read_bytes(), data)
            self.assertNotIn(str(root), result.stdout + result.stderr)
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
            self.assertEqual(output.read_bytes(), report)
            output.unlink()
            (source / 'fixture.pak').write_bytes(b'truncated')
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())
            self.assertNotIn(str(root), result.stdout + result.stderr)

    def test_cli_rejects_container_symlink(self):
        private = Path(__file__).resolve().parents[1] / '.private'
        private.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=private) as folder:
            root = Path(folder)
            source = root / 'input'
            source.mkdir()
            target = root / 'target.pak'
            target.write_bytes(bytes(16) + footer())
            (source / 'linked.pak').symlink_to(target)
            output = root / 'report.json'
            result = subprocess.run([sys.executable, headers.__file__, str(source), str(output)],
                                    capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
