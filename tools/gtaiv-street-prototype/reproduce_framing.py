# SPDX-License-Identifier: GPL-3.0-only
"""Throwaway framing experiment; does not qualify geometry or touch GTA."""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import zlib


ROOT = Path(__file__).resolve().parents[2]
INSPECTOR_REVISION = 'fcb4acc0c643d7244a8cae1db83c9e08b1a07887'
INSPECTOR_PATH = 'tools/gtaiv-collision/inspect_resource.py'


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verdict(module, raw):
    try:
        module.decode_resource(raw)
        return {'verdict': 'structurally-decoded', 'reason': 'validated-geometry'}
    except module.Refusal as error:
        return {'verdict': error.verdict, 'reason': error.reason}


def experiment(resource=None):
    source = subprocess.run(
        ['git', 'show', f'{INSPECTOR_REVISION}:{INSPECTOR_PATH}'],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    replacements = [
        ('zlib.decompressobj(-15)', 'zlib.decompressobj()'),
        ('inflater.decompress(raw[14:], total_size + 1)',
         'inflater.decompress(raw[12:], total_size + 1)'),
    ]
    corrected = source
    for old, new in replacements:
        if corrected.count(old) != 1:
            raise ValueError('unexpected-inspector-source')
        corrected = corrected.replace(old, new)

    with tempfile.TemporaryDirectory(prefix='combine-framing-') as directory:
        before_path = Path(directory) / 'before.py'
        after_path = Path(directory) / 'after.py'
        before_path.write_text(source)
        after_path.write_text(corrected)
        before = load_module(before_path, 'framing_before')
        after = load_module(after_path, 'framing_after')

        # Authored composite marker, no proprietary bytes or geometry.
        data = bytearray(512)
        struct.pack_into('<I', data, 8, 0x50000020)
        data[0x24] = 12
        raw = struct.pack('<III', 0x05435352, 0x20, 2) + zlib.compress(data, 9)
        expected_before = {'verdict': 'invalid', 'reason': 'decompression-error'}
        expected_after = {'verdict': 'unsupported', 'reason': 'unsupported-root'}
        if verdict(before, raw) != expected_before or verdict(after, raw) != expected_after:
            raise ValueError('framing-reproduction-changed')
        # The correction must validate the checksum and reject missing/trailing data.
        corrupt = raw[:-1] + bytes([raw[-1] ^ 1])
        for invalid in (corrupt, raw[:-1], raw + b'X', raw[:-4]):
            if verdict(after, invalid) != expected_before:
                raise ValueError('invalid-framing-accepted')

        report = {'authored_framing_checks': 'passed', 'runtime_tested': False}
        if resource is not None:
            # Reuse the bounded file reader; neither result exposes asset contents.
            report['baseline'] = before.inspect_file(resource)
            report['temporary_correction'] = after.inspect_file(resource)
        return report


def main():
    if len(sys.argv) > 2:
        print('{"verdict":"unavailable","reason":"expected-zero-or-one-local-file"}')
        return 2
    try:
        report = experiment(sys.argv[1] if len(sys.argv) == 2 else None)
    except (OSError, ValueError, subprocess.SubprocessError):
        print('{"verdict":"unavailable","reason":"experiment-prerequisite-or-check-failed"}')
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
