"""Asset-free CLI regression checks. Usage: python3 check_runner.py DOTNET RUNNER_DLL."""
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

runtime, runner = map(lambda p: str(Path(p).resolve()), sys.argv[1:])
checks = 0
private = Path(__file__).resolve().parents[2] / '.private'
private.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='runner-tests-', dir=private) as temporary:
    root = Path(temporary)
    source = root / 'input'
    source.mkdir()

    def run(command, destination, *extra, expected):
        global checks
        result = subprocess.run([runtime, runner, command, str(source), str(destination),
                                 'GAME_UE4_20', *extra], capture_output=True, text=True, timeout=30)
        assert result.returncode == expected, (command, result.returncode, result.stderr)
        assert str(root) not in result.stdout + result.stderr, 'Console exposed private root'
        checks += 1

    run('unknown', root / 'invalid', expected=2)
    assert not (root / 'invalid').exists()
    run('inventory', source / 'overlap', expected=1)
    assert not (source / 'overlap').exists()
    run('inventory', root / 'empty', expected=1)
    assert json.loads((root / 'empty/inventory.json').read_text())['files'] == 0
    # Package-name inventory must never claim this empty synthetic file is real geometry.
    (source / 'fixture.umap').write_bytes(b'')
    run('inventory', root / 'index', expected=0)
    report = json.loads((root / 'index/inventory.json').read_text())
    assert len(report['worlds']) == 1 and report['completeIsland'] is False
    assert report['collisionQualified'] is False
    run('inventory', root / 'index', expected=1)  # Never overwrite an earlier result.
    run('inspect', root / 'traversal', '../fixture.umap', expected=1)
    # Unknown containers must fail even if a loose world name can be indexed.
    (source / 'invalid.pak').write_bytes(b'invalid')
    run('inventory', root / 'bad-container', expected=1)
    (source / 'invalid.pak').unlink()
    # Version-4 footer with encrypted-index flag, no real game data or key.
    (source / 'encrypted.pak').write_bytes(
        b'\0' * 16 + b'\1' + struct.pack('<IIqq', 0x5A6F12E1, 4, 0, 16) + b'\0' * 20)
    run('inventory', root / 'encrypted', expected=1)
    report = json.loads((root / 'encrypted/inventory.json').read_text())
    assert report['encryptedUnmounted'] == 1 and report['mounted'] == 0
    (source / 'encrypted.pak').unlink()
    (source / 'loop').symlink_to(source, target_is_directory=True)
    run('inventory', root / 'linked-input', expected=1)
    assert not (root / 'linked-input').exists()
    (source / 'loop').unlink()
    (root / 'alias').symlink_to(root, target_is_directory=True)
    run('inventory', root / 'alias/new-output', expected=1)
    assert not (root / 'new-output').exists()
print(f'PASS: {checks} runner CLI checks; synthetic data only, no export/gameplay claim')
