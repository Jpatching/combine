"""Compare private fixed ground checkpoints; emit source-safe verdicts only."""
from decimal import Decimal
import json
from pathlib import Path
import re
import sys


LABELS = ('R1', 'P1', 'H1', 'H2')


def number(value):
    if type(value) not in (int, float, Decimal):
        raise ValueError()
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError()
    return result


def position(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError()
    return [number(coordinate) for coordinate in value]


def points(document):
    if not isinstance(document, dict) or type(document.get('schema_version')) is not int or document['schema_version'] != 1:
        raise ValueError()
    if not isinstance(document.get('selected_sha256'), str) or not re.fullmatch('[0-9a-f]{64}', document['selected_sha256']):
        raise ValueError()
    values = document.get('checkpoints')
    if not isinstance(values, list) or len(values) > 4:
        raise ValueError()
    result = {}
    for value in values:
        if not isinstance(value, dict) or value.get('label') not in LABELS or value['label'] in result:
            raise ValueError()
        result[value['label']] = value
    return result


def compare(checkpoint_set, observations):
    expected = points(checkpoint_set)
    observed = points(observations)
    if set(expected) != set(LABELS) or checkpoint_set['selected_sha256'] != observations['selected_sha256']:
        raise ValueError()
    for point in expected.values():
        position(point.get('position'))
        number(point.get('mesh_height_m'))
        if type(point.get('qualified')) is not bool:
            raise ValueError()
    results = []
    for label in LABELS:
        point = expected[label]
        readings = observed.get(label, {}).get('readings', [])
        if point.get('qualified') is not True or not isinstance(readings, list) or len(readings) != 3:
            results.append({'label': label, 'verdict': 'inconclusive',
                            'reason': 'unqualified' if point.get('qualified') is not True else 'readings-unavailable'})
            continue
        try:
            heights = [number(reading['height_m']) for reading in readings]
            coordinates = [position(reading['position']) for reading in readings]
        except (ValueError, KeyError, TypeError, ArithmeticError):
            results.append({'label': label, 'verdict': 'inconclusive', 'reason': 'readings-unavailable'})
            continue
        prediction = number(point['mesh_height_m'])
        if any(
                reading.get('query_success') is not True or reading.get('ground_loaded') is not True or
                reading.get('intended_surface') is not True for reading in readings):
            verdict, reason = 'inconclusive', 'readings-unavailable'
        elif any(coordinate != position(point['position']) for coordinate in coordinates):
            verdict, reason = 'inconclusive', 'coordinate-mismatch'
        elif max(heights) - min(heights) > Decimal('0.02'):
            verdict, reason = 'inconclusive', 'unstable'
        elif any(abs(height - prediction) > Decimal('0.05') for height in heights):
            verdict, reason = 'disagreement', 'over-tolerance'
        else:
            verdict, reason = 'agreement', 'within-tolerance'
        results.append({'label': label, 'verdict': verdict, 'reason': reason})
    verdict = ('disagreement' if any(r['verdict'] == 'disagreement' for r in results) else
               'inconclusive' if any(r['verdict'] == 'inconclusive' for r in results) else 'agreement')
    return {'verdict': verdict, 'checkpoints': results}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError()
        result[key] = value
    return result


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        if len(argv) != 2:
            raise ValueError()
        documents = []
        for argument in argv:
            path = Path(argument)
            if not path.is_file() or path.stat().st_size > 65536:
                raise ValueError()
            with path.open('r', encoding='utf-8') as stream:
                raw = stream.read(65537)
            if len(raw) > 65536:
                raise ValueError()
            documents.append(json.loads(raw, parse_float=Decimal, object_pairs_hook=unique_object))
        report = compare(*documents)
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError, RecursionError):
        report = {'verdict': 'inconclusive', 'reason': 'invalid-input'}
    print(json.dumps(report))
    return {'agreement': 0, 'disagreement': 1, 'inconclusive': 2}[report['verdict']]


if __name__ == '__main__':
    sys.exit(main())
