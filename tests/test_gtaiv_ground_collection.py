"""Authored observations through the public collection command; no GTA claims."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMMAND = ROOT / 'tools/gtaiv-collision/collect_ground.py'
LABELS = ('R1', 'P1', 'H1', 'H2')


def authored(directory):
    artifact = directory / 'authored-plugin.bin'
    artifact.write_bytes(b'authored diagnostic plugin')
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    points = {'schema_version': 1, 'selected_sha256': 'a' * 64, 'checkpoints': [
        {'label': label, 'position': [i, 7], 'mesh_height_m': 10,
         'query_z_m': 12, 'qualified': True, 'surface_evidence': 'authored-scene',
         'layer_evidence': 'authored-layer'} for i, label in enumerate(LABELS)]}
    session = {'schema_version': 1, 'process': {'pid': 100, 'start_ms': 1000},
               'artifacts': [{'path': str(artifact), 'sha256': digest}],
               'retained_artifacts': [{'path': str(artifact), 'sha256': digest}]}
    def snapshot(now):
        return {'pid': 100, 'start_ms': 1000, 'now_ms': now, 'updated_ms': now,
                'foreground': True, 'minimized': False, 'responding': True,
                'scene': 'gameplay', 'player_control': True, 'on_foot': True,
                'adapter_ready': True, 'mounted': False, 'artifacts': [digest]}
    events = [{'kind': 'ready', 'snapshot': snapshot(2000)}]
    for p in points['checkpoints']:
        for batch, height in enumerate((10.03, 10.04, 10.05)):
            events.append({'kind': 'reading', 'snapshot': snapshot(2100 + len(events)),
                'label': p['label'], 'batch': batch, 'reading': {
                    'position': p['position'], 'height_m': height, 'query_success': True,
                    'buffer_intact': True, 'ground_loaded': True, 'intended_surface': True,
                    'loading_evidence': 'authored-independent-support',
                    'layer_evidence': 'authored-independent-layer'}})
    events.append({'kind': 'complete', 'snapshot': snapshot(3000)})
    events.append({'kind': 'restored', 'snapshot': snapshot(3100)})
    return points, session, events


class GroundCollectionTests(unittest.TestCase):
    def run_collection(self, change=None, live=False, prepare=False):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            points, session, events = authored(folder)
            if change:
                change(points, session, events)
            for name, value in (('points', points), ('session', session), ('events', events)):
                (folder / (name + '.json')).write_text(json.dumps(value))
            command = [sys.executable, str(COMMAND),
                '--checkpoints', str(folder / 'points.json'),
                '--session', str(folder / 'session.json'),
                '--output', str(folder / 'bundle')]
            if prepare:
                command.append('--prepare-probe')
            elif not live:
                command.extend(['--authored-events', str(folder / 'events.json')])
            result = subprocess.run(command, text=True, capture_output=True)
            bundle = folder / 'bundle/result-private.json'
            private = json.loads(bundle.read_text()) if bundle.exists() else None
            self.assertEqual(result.stderr, '')
            return result.returncode, json.loads(result.stdout), private

    def test_complete_collection_uses_frozen_gate_and_retains_private_bundle(self):
        status, report, private = self.run_collection()
        self.assertEqual(status, 0)
        self.assertEqual(report['verdict'], 'agreement')
        self.assertEqual(report['mode'], 'authored')
        self.assertEqual(report['restoration'], 'verified')
        self.assertEqual([p['label'] for p in report['checkpoints']], list(LABELS))
        self.assertEqual(len(private['observations']['checkpoints']), 4)
        self.assertIn('collection_seconds', private['timing'])
        self.assertNotIn('height_m', json.dumps(report))

    def test_missing_readings_and_unavailable_queries_remain_inconclusive(self):
        changes = [
            lambda p, s, e: e.__delitem__(slice(1, 4)),
            lambda p, s, e: e[1]['reading'].update(query_success=False),
            lambda p, s, e: e[1]['reading'].update(position=[99, 7]),
            lambda p, s, e: e[1]['reading'].update(ground_loaded=None),
            lambda p, s, e: e[1]['reading'].update(intended_surface=False),
            lambda p, s, e: e[1]['reading'].pop('loading_evidence'),
            lambda p, s, e: p['checkpoints'][0].pop('layer_evidence'),
        ]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                status, report, private = self.run_collection(change)
                self.assertEqual(status, 2)
                self.assertEqual(report['verdict'], 'inconclusive')
                self.assertEqual(report['checkpoints'][0]['verdict'], 'inconclusive')

    def test_stale_status_lost_focus_and_interruption_refuse_collection(self):
        cases = [
            ('stale-process-status', lambda e: e[1]['snapshot'].update(pid=101)),
            ('stale-process-status', lambda e: e[1]['snapshot'].update(start_ms=999)),
            ('stale-process-status', lambda e: e[1]['snapshot'].update(updated_ms=1000, now_ms=4001)),
            ('foreground-lost', lambda e: e[1]['snapshot'].update(foreground=False)),
            ('foreground-lost', lambda e: e[1]['snapshot'].update(minimized=True)),
            ('collection-interrupted', lambda e: e.pop(-2)),
        ]
        for reason, change in cases:
            with self.subTest(reason=reason):
                status, report, private = self.run_collection(lambda p, s, e: change(e))
                self.assertEqual(status, 2)
                self.assertEqual(report['reason'], reason)
                self.assertIsNotNone(private)

    def test_artifact_mismatch_refuses_before_observation_execution(self):
        def change(p, session, events):
            Path(session['artifacts'][0]['path']).write_bytes(b'wrong artifact')
        status, report, private = self.run_collection(change)
        self.assertEqual(status, 2)
        self.assertEqual(report['reason'], 'artifact-mismatch')
        self.assertEqual(private['events'], [])

    def test_restoration_failure_is_visible_even_after_matching_heights(self):
        status, report, private = self.run_collection(
            lambda p, s, e: e[-1]['snapshot'].update(artifacts=['b' * 64]))
        self.assertEqual(status, 2)
        self.assertEqual(report['reason'], 'restoration-failed')
        self.assertEqual(report['restoration'], 'failed')

    def test_extra_named_points_do_not_change_the_four_point_verdict(self):
        def change(points, session, events):
            points['checkpoints'].append(dict(points['checkpoints'][0], label='EXTRA'))
            for batch in range(3):
                row = json.loads(json.dumps(events[batch + 1]))
                row.update(label='EXTRA')
                row['reading']['height_m'] = 100
                events.insert(-2, row)
        status, report, private = self.run_collection(change)
        self.assertEqual(status, 0)
        self.assertEqual(report['verdict'], 'agreement')
        self.assertEqual([p['label'] for p in report['checkpoints']], list(LABELS))
        self.assertEqual(len(private['observations']['checkpoints']), 5)

    def test_additional_points_cannot_be_silently_omitted_from_collection(self):
        for count in (0, 1, 2):
            def change(points, session, events):
                points['checkpoints'].append(dict(points['checkpoints'][0], label='EXTRA'))
                for batch in range(count):
                    row = json.loads(json.dumps(events[batch + 1]))
                    row.update(label='EXTRA')
                    events.insert(-2, row)
            with self.subTest(count=count):
                status, report, private = self.run_collection(change)
                self.assertEqual(status, 2)
                self.assertEqual(report['reason'], 'collection-incomplete')
                self.assertTrue(all(p['verdict'] == 'agreement' for p in report['checkpoints']))

    def test_retained_measurements_preserve_decimal_coordinates_as_numbers(self):
        status, report, private = self.run_collection(
            lambda p, s, e: e[1]['reading'].update(height_m=10.031))
        self.assertEqual(status, 0)
        self.assertEqual(private['observations']['checkpoints'][0]['readings'][0]['height_m'], 10.031)

    def test_live_collection_refuses_unconfirmed_surface_before_execution(self):
        def change(p, s, e):
            s['token'] = 'c' * 32
            p['checkpoints'][0]['qualified'] = False
        status, report, private = self.run_collection(change, live=True)
        self.assertEqual(status, 2)
        self.assertEqual(report['reason'], 'unconfirmed-checkpoints')
        self.assertEqual(private['observations'], [])

    def test_preparation_writes_strict_private_script_without_execution(self):
        status, report, private = self.run_collection(
            lambda p, s, e: s.update(token='c' * 32), prepare=True)
        self.assertEqual(status, 0)
        self.assertEqual(report, {'mode': 'preparation', 'verdict': 'prepared', 'execution': 'none'})

    def test_existing_bundle_is_preserved_even_when_it_has_no_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'existing'
            output.mkdir()
            sentinel = output / 'unrelated.txt'
            sentinel.write_text('preserve this')
            result = subprocess.run([sys.executable, str(COMMAND), '--checkpoints', 'absent',
                '--session', 'absent', '--output', str(output)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual([p.name for p in output.iterdir()], ['unrelated.txt'])

    @unittest.skipIf(os.name == 'nt', 'Authored executable adapter uses POSIX scripts')
    def test_retained_observer_blocks_restoration_until_confirmed_exit(self):
        # Substitute only the external process adapter, through the real CLI.
        # The authored child sends no input and touches only this temporary folder.
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            points, session, events = authored(folder)
            session['token'] = 'c' * 32
            points_path = folder / 'points.json'
            points_path.write_text(json.dumps(points))
            session_path = folder / 'session.json'
            session_path.write_text(json.dumps(session))
            preparation = folder / 'preparation'
            prepared = subprocess.run([sys.executable, str(COMMAND), '--prepare-probe',
                '--checkpoints', str(points_path), '--session', str(session_path),
                '--output', str(preparation)], capture_output=True, text=True)
            self.assertEqual(prepared.returncode, 0)
            metadata = json.loads((preparation / 'probe-config-private.json').read_text())
            artifacts = []
            for role in ('executable', 'plugin', 'worker', 'definitions', 'script', 'watchdog', 'status_script', 'manifest'):
                path = folder / role
                path.write_bytes((preparation / 'diagnostic-script.js').read_bytes() if role == 'script' else role.encode())
                artifacts.append({'role': role, 'path': str(path),
                                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            restoration = folder / 'reviewed-restoration.ps1'
            restoration.write_text('authored restoration fixture')
            session.update(executable=str(folder / 'executable'),
                checkpoints_sha256=metadata['checkpoints_sha256'], artifacts=artifacts,
                retained_artifacts=artifacts, restore_script={'path': str(restoration),
                    'sha256': hashlib.sha256(restoration.read_bytes()).hexdigest()})
            session_path.write_text(json.dumps(session))
            shim = folder / 'powershell.exe'
            shim.write_text('#!/usr/bin/python3\nimport sys,time\nfrom pathlib import Path\n'
                'if "-Mode" in sys.argv:\n Path(__file__).with_name("restoration-ran").touch()\n'
                'else:\n time.sleep(2)\n')
            shim.chmod(0o755)
            mapper = folder / 'wslpath'
            mapper.write_text('#!/usr/bin/python3\nimport sys\nprint(sys.argv[-1])\n')
            mapper.chmod(0o755)
            env = dict(os.environ, PATH=str(folder) + os.pathsep + os.environ.get('PATH', ''),
                       WSL_DISTRO_NAME='authored-adapter')
            result = subprocess.run([sys.executable, str(COMMAND), '--checkpoints', str(points_path),
                '--session', str(session_path), '--output', str(folder / 'bundle'),
                '--timeout-seconds', '1'], capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 2)
            report = json.loads(result.stdout)
            self.assertEqual(report['reason'], 'observer-still-running')
            self.assertEqual(report['restoration'], 'required')
            self.assertFalse((folder / 'restoration-ran').exists())
            time.sleep(1.2)  # Let the harmless authored child exit before folder cleanup.
            # Now let the authored observer finish and restoration return zero,
            # while the external process identity remains unchanged.
            for event in events:
                event['snapshot']['artifacts'] = [a['sha256'] for a in artifacts]
            session['witnesses'] = {label: {key: events[1]['reading'][key] for key in
                ('ground_loaded', 'intended_surface', 'loading_evidence', 'layer_evidence')}
                for label in LABELS}
            session_path.write_text(json.dumps(session))
            (folder / 'events-fixture.jsonl').write_text('\n'.join(json.dumps(e) for e in events[:-1]))
            (folder / 'identity-fixture.json').write_text(json.dumps(
                {'pid': 100, 'start_ms': 1000, 'executable': session['executable']}))
            shim.write_text('#!/usr/bin/python3\nimport sys\nfrom pathlib import Path\n'
                'root=Path(__file__).parent\n'
                'if "-Mode" in sys.argv:\n (root/"restoration-ran").touch()\n'
                'elif "-Command" in sys.argv:\n print((root/"identity-fixture.json").read_text())\n'
                'elif any(a.endswith("trial.ps1") for a in sys.argv):\n'
                ' Path(sys.argv[sys.argv.index("-Output")+1]).write_text("{\\"verdict\\":\\"passed\\"}")\n'
                'else:\n output=Path(sys.argv[sys.argv.index("-Output")+1])\n'
                ' (output/"input-cleanup-private.json").write_text("{\\"owned\\":true,\\"released\\":true}")\n'
                ' (output/"events-private.jsonl").write_text((root/"events-fixture.jsonl").read_text())\n')
            second = subprocess.run([sys.executable, str(COMMAND), '--checkpoints', str(points_path),
                '--session', str(session_path), '--output', str(folder / 'second-bundle')],
                capture_output=True, text=True, env=env)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            metric = json.loads((folder / 'second-bundle/restart-count-private.json').read_text())
            self.assertEqual(metric, {'verified_process_replacements': 0})
            self.assertTrue((folder / 'restoration-ran').exists())
            good_shim = shim.read_text()
            (folder / 'restoration-ran').unlink()
            shim.write_text(good_shim.replace('released\\\":true', 'released\\\":false'))
            failed_release = subprocess.run([sys.executable, str(COMMAND), '--checkpoints', str(points_path),
                '--session', str(session_path), '--output', str(folder / 'failed-release-bundle')],
                capture_output=True, text=True, env=env)
            self.assertEqual(failed_release.returncode, 2)
            self.assertEqual(json.loads(failed_release.stdout)['restoration'], 'failed')
            self.assertFalse((folder / 'restoration-ran').exists())
            shim.write_text(good_shim)
            shim.write_text(shim.read_text().replace('(root/"restoration-ran").touch()',
                'sys.exit(2)'))
            third = subprocess.run([sys.executable, str(COMMAND), '--checkpoints', str(points_path),
                '--session', str(session_path), '--output', str(folder / 'third-bundle')],
                capture_output=True, text=True, env=env)
            self.assertEqual(third.returncode, 2)
            self.assertEqual(json.loads(third.stdout)['restoration'], 'failed')
            metric = json.loads((folder / 'third-bundle/restart-count-private.json').read_text())
            self.assertEqual(metric, {'verified_process_replacements': None})


if __name__ == '__main__':
    unittest.main()
