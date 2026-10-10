"""Public comparison command, using authored coordinates and readings only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMMAND = ROOT / 'tools/gtaiv-collision/compare_ground.py'


def authored():
    points = [
        {'label': label, 'position': [index, 7], 'mesh_height_m': 10,
         'qualified': True}
        for index, label in enumerate(('R1', 'P1', 'H1', 'H2'))
    ]
    checkpoint_set = {'schema_version': 1, 'selected_sha256': 'a' * 64,
                      'checkpoints': points}
    readings = {'schema_version': 1, 'selected_sha256': 'a' * 64,
                'checkpoints': [
                    {'label': p['label'], 'readings': [
                        {'position': p['position'], 'height_m': height,
                         'query_success': True, 'ground_loaded': True,
                         'intended_surface': True}
                        for height in (10.03, 10.04, 10.05)]}
                    for p in points]}
    return checkpoint_set, readings


class GroundComparisonTests(unittest.TestCase):
    def run_comparison(self, checkpoint_set, readings):
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / 'private-coordinates.json'
            observed = Path(directory) / 'private-readings.json'
            expected.write_text(json.dumps(checkpoint_set))
            observed.write_text(json.dumps(readings))
            result = subprocess.run([sys.executable, str(COMMAND), str(expected), str(observed)],
                                    capture_output=True, text=True)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout)

    def test_all_four_complete_points_agree_at_inclusive_boundaries(self):
        status, report = self.run_comparison(*authored())
        self.assertEqual(status, 0)
        self.assertEqual(report, {'verdict': 'agreement', 'checkpoints': [
            {'label': label, 'verdict': 'agreement', 'reason': 'within-tolerance'}
            for label in ('R1', 'P1', 'H1', 'H2')]})

    def test_unavailable_point_cannot_become_agreement(self):
        cases = [
            ('query_success', False, 'readings-unavailable'),
            ('ground_loaded', False, 'readings-unavailable'),
            ('intended_surface', False, 'readings-unavailable'),
            ('height_m', float('nan'), 'readings-unavailable'),
            ('height_m', float('inf'), 'readings-unavailable'),
            ('height_m', 10.05001, 'unstable'),
            ('position', [0, 7.001], 'coordinate-mismatch'),
        ]
        for field, value, reason in cases:
            with self.subTest(field=field, value=value):
                checkpoint_set, readings = authored()
                readings['checkpoints'][0]['readings'][2][field] = value
                status, report = self.run_comparison(checkpoint_set, readings)
                self.assertEqual(status, 2)
                self.assertEqual(report['verdict'], 'inconclusive')
                self.assertEqual(report['checkpoints'][0],
                                 {'label': 'R1', 'verdict': 'inconclusive', 'reason': reason})

    def test_incomplete_and_unqualified_points_remain_visible(self):
        for kind in ('missing-point', 'two-readings', 'four-readings', 'unqualified'):
            with self.subTest(kind=kind):
                checkpoint_set, readings = authored()
                if kind == 'missing-point':
                    readings['checkpoints'].pop(0)
                elif kind == 'two-readings':
                    readings['checkpoints'][0]['readings'].pop()
                elif kind == 'four-readings':
                    readings['checkpoints'][0]['readings'].append(
                        copy.deepcopy(readings['checkpoints'][0]['readings'][0]))
                else:
                    checkpoint_set['checkpoints'][0]['qualified'] = False
                status, report = self.run_comparison(checkpoint_set, readings)
                self.assertEqual(status, 2)
                self.assertEqual(len(report['checkpoints']), 4)
                self.assertEqual(report['checkpoints'][0], {
                    'label': 'R1', 'verdict': 'inconclusive',
                    'reason': 'unqualified' if kind == 'unqualified' else 'readings-unavailable'})

    def test_invalid_identity_or_point_set_cannot_silently_replace_fixed_points(self):
        for kind in ('identity', 'schema', 'duplicate-expected', 'duplicate-observed',
                     'unknown-point', 'missing-expected', 'nonfinite-prediction',
                     'boolean-position', 'string-height', 'malformed-document'):
            with self.subTest(kind=kind):
                checkpoint_set, readings = authored()
                if kind == 'identity': readings['selected_sha256'] = 'b' * 64
                elif kind == 'schema': readings['schema_version'] = True
                elif kind == 'duplicate-expected':
                    checkpoint_set['checkpoints'].append(copy.deepcopy(checkpoint_set['checkpoints'][0]))
                elif kind == 'duplicate-observed':
                    readings['checkpoints'].append(copy.deepcopy(readings['checkpoints'][0]))
                elif kind == 'unknown-point': readings['checkpoints'][0]['label'] = 'private-name'
                elif kind == 'missing-expected': checkpoint_set['checkpoints'].pop()
                elif kind == 'nonfinite-prediction': checkpoint_set['checkpoints'][0]['mesh_height_m'] = float('nan')
                elif kind == 'boolean-position': checkpoint_set['checkpoints'][0]['position'][0] = False
                elif kind == 'string-height': checkpoint_set['checkpoints'][0]['mesh_height_m'] = '10'
                else: readings = []
                status, report = self.run_comparison(checkpoint_set, readings)
                self.assertEqual(status, 2)
                self.assertEqual(report, {'verdict': 'inconclusive', 'reason': 'invalid-input'})

    def test_stable_disagreement_takes_precedence_over_unavailable_other_point(self):
        checkpoint_set, readings = authored()
        for reading, height in zip(readings['checkpoints'][0]['readings'], (10.049, 10.05, 10.05001)):
            reading['height_m'] = height
        readings['checkpoints'][1]['readings'][0]['query_success'] = False
        status, report = self.run_comparison(checkpoint_set, readings)
        self.assertEqual(status, 1)
        self.assertEqual(report['verdict'], 'disagreement')
        self.assertEqual(report['checkpoints'][0]['reason'], 'over-tolerance')
        self.assertEqual(report['checkpoints'][1]['verdict'], 'inconclusive')

    def test_ambiguous_json_keys_are_rejected_without_private_output(self):
        checkpoint_set, readings = authored()
        ambiguous = json.dumps(readings).replace('"query_success": true',
                                                '"query_success": false, "query_success": true', 1)
        with tempfile.TemporaryDirectory() as directory:
            expected = Path(directory) / 'private-coordinates.json'
            observed = Path(directory) / 'private-readings.json'
            expected.write_text(json.dumps(checkpoint_set))
            observed.write_text(ambiguous)
            result = subprocess.run([sys.executable, str(COMMAND), str(expected), str(observed)],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, '')
        self.assertEqual(json.loads(result.stdout), {'verdict': 'inconclusive', 'reason': 'invalid-input'})


if __name__ == '__main__':
    unittest.main()
