"""Structural acceptance only; independent reviews judge evidence and source quality."""
import json
from pathlib import Path
import re
import sys


def validate(path):
    root = Path.cwd()
    candidate = root / path
    if Path(path).is_absolute() or '..' in Path(path).parts:
        raise ValueError('Report must be a scoped relative path')
    for parent in (candidate, *candidate.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError('Report path must not follow symlinks')
    if not candidate.is_file() or candidate.stat().st_size > 65536:
        raise ValueError('Report missing or exceeds 64 KiB')
    text = candidate.read_text(encoding='utf-8')
    matches = re.findall(r'<research>(.*?)</research>', text, re.S)
    if len(matches) != 1:
        raise ValueError('Report needs exactly one evidence verdict')
    record = json.loads(matches[0])
    if record.get('verdict') not in ('source-feasible', 'requires-local-proof', 'blocked') or record.get('runtimeVerified') is not False:
        raise ValueError('Source research cannot establish runtime verification')
    for field in ('unknowns', 'inaccessibleSources'):
        if not isinstance(record.get(field), list) or not all(isinstance(item, str) and item.strip() for item in record[field]):
            raise ValueError('Unknowns and inaccessible sources must be explicit lists')
    sources = record.get('sources')
    if not isinstance(sources, list) or not 1 <= len(sources) <= 40:
        raise ValueError('Report needs bounded immutable source references')
    prose = re.sub(r'<research>.*?</research>', '', text, flags=re.S)
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError('Invalid source')
        revision, url = source.get('revision'), source.get('url')
        if not isinstance(revision, str) or not re.fullmatch(r'[0-9a-f]{40}', revision):
            raise ValueError('Source revision must be a complete commit')
        if not isinstance(url, str) or not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/blob/' + revision + r'/[^\s<>"?#]+', url):
            raise ValueError('Source URL must identify its immutable public file')
        if f']({url})' not in prose:
            raise ValueError('Source needs a citation in the report prose')
    for heading in ('Verified source facts', 'Source inference', 'Unknowns', 'Next local proof'):
        if not re.search(r'^## ' + re.escape(heading) + r'\s*$', prose, re.M):
            raise ValueError('Report must distinguish facts, inference, unknowns and next proof')
    return record


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('Expected one host-selected report path')
        verdict = validate(sys.argv[1])['verdict']
        print('PASS: structurally valid source report; evidence verdict=' + verdict)
    except (ValueError, OSError, UnicodeError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
