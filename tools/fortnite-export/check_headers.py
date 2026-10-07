"""Read-only version-4 Pak footer diagnostic; never reads/decrypts package payloads.

Usage: python3 tools/fortnite-export/check_headers.py PRIVATE_INPUT NEW_PRIVATE_REPORT
Both paths must be beneath this checkout's ignored .private directory.
"""
import json
from pathlib import Path
import struct
import sys


def parse_footer(footer: bytes, file_size: int) -> dict:
    # v4 has one flag + magic/version + two int64s + SHA-1: 45 bytes.
    # The encryption GUID was added in v7; assuming 61 bytes gives false bounds.
    if len(footer) != 45 or file_size < 45:
        raise ValueError("Truncated version-4 footer")
    flag = footer[0]
    magic, version, offset, size = struct.unpack_from('<IIqq', footer, 1)
    if magic != 0x5A6F12E1 or version != 4:
        raise ValueError("Only standard version-4 Pak footers are supported")
    if flag not in (0, 1):
        raise ValueError("Invalid encrypted-index flag")
    end = file_size - 45
    if not (0 <= offset <= end and 0 <= size <= end - offset):
        raise ValueError("Index range outside container payload")
    return {"version": version, "encryptedIndexFlag": bool(flag),
            "indexInBounds": True, "indexEndsAtFooter": offset + size == end}


def private_path(value: str) -> Path:
    path = Path(value).absolute()
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError("Links are unsupported")
    path = path.resolve()
    private = Path(__file__).resolve().parents[2] / '.private'
    if not path.is_relative_to(private):
        raise ValueError("Use this checkout's ignored private directory")
    return path


def main(args: list[str]) -> int:
    if len(args) != 2:
        print("Usage: check_headers.py PRIVATE_INPUT NEW_PRIVATE_REPORT", file=sys.stderr)
        return 2
    try:
        source, output = map(private_path, args)
        if not source.is_dir() or output.exists() or output.is_relative_to(source):
            raise ValueError("Require input directory and separate new report")
        containers = sorted(p for p in source.iterdir() if p.suffix.lower() == '.pak')
        if not containers:
            raise ValueError("No containers supplied")
        rows = []
        for number, path in enumerate(containers):
            if path.is_symlink() or not path.is_file():
                raise ValueError("Require ordinary container files")
            with path.open('rb') as stream:
                size = stream.seek(0, 2)
                stream.seek(max(0, size - 45))
                row = parse_footer(stream.read(45), size)
            rows.append({"container": number, **row})
        # Exclusive creation preserves previous diagnostics, even after a race.
        with output.open('x') as stream:
            json.dump({"containers": rows, "payloadEncryptionEstablished": False,
                       "completeIsland": False, "collisionQualified": False}, stream, indent=2)
        flags = sum(row['encryptedIndexFlag'] for row in rows)
        print(f"PASS: {len(rows)} valid v4 headers; {flags} encrypted-index flags; payload untested")
        return 0
    except (OSError, ValueError):
        print("FAIL: invalid header or private report roots; no payload decoding", file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
