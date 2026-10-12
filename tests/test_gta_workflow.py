"""Local public commands retain requests and refuse missing setup without input."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[1]


class GtaWorkflowTests(unittest.TestCase):
    def test_recovery_and_diagnostics_cannot_claim_the_runtime_together(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from evidence_store import Store
        with tempfile.TemporaryDirectory() as directory:
            store = Store(directory)
            store.request({'id': str(uuid.uuid4()), 'scenario': 'preflight', 'attempts': 1})
            lease = store.begin_runtime_operation('recover')
            self.assertIsNone(store.claim())
            with self.assertRaises(ValueError):
                store.begin_runtime_operation('open')
            store.finish_runtime_operation(lease, 'completed')
            batch = store.claim()
            self.assertIsNotNone(batch)
            with self.assertRaises(ValueError):
                store.begin_runtime_operation('recover')
            store.finish(batch, 'completed', 'authored')
            lease = store.begin_runtime_operation('open')
            store.finish_runtime_operation(lease, 'unverified')
            self.assertIsNone(store.claim())
            with self.assertRaises(ValueError):
                store.begin_runtime_operation('recover')

    def test_hung_termination_is_only_an_explicit_recovery_option(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'gta.json'
            config.write_text('{}')
            for action in ('open', 'test', 'status'):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/workbench.py'),
                    'gta', action, '--config', str(config), '--allow-hung-termination'], text=True, capture_output=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn('hung-termination-needs-recovery', result.stdout)

    def test_missing_setup_is_named_without_echoing_private_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'PRIVATE-DO-NOT-ECHO.json'
            for action in ('open', 'recover', 'status', 'monitor'):
                result = subprocess.run([sys.executable, str(ROOT / 'scripts/workbench.py'),
                    'gta', action, '--config', str(config)], text=True, capture_output=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('configuration-unavailable', result.stdout)
                self.assertNotIn('PRIVATE-DO-NOT-ECHO', result.stdout + result.stderr)

    def test_monitor_rejects_unbounded_wait_before_touching_windows(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'gta.json'
            config.write_text('{}')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/workbench.py'),
                'gta', 'monitor', '--config', str(config), '--monitor-timeout', '121'],
                text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('monitor-timeout-out-of-range', result.stdout)

    def test_test_request_is_idempotent_and_missing_setup_is_not_a_game_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            config = folder / 'gta.json'
            config.write_text(json.dumps({'state': str(folder / 'state')}))
            request = str(uuid.uuid4())
            command = [sys.executable, str(ROOT / 'scripts/workbench.py'), 'gta', 'test',
                       '--config', str(config), '--request-id', request]
            for _ in range(2):
                result = subprocess.run(command, text=True, capture_output=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn('runtime-configuration-unavailable', result.stdout)
            state = subprocess.run([sys.executable, str(ROOT / 'scripts/evidence_hub.py'),
                '--state', str(folder / 'state'), 'status'], text=True, capture_output=True, check=True)
            snapshot = json.loads(state.stdout)
            self.assertEqual(len(snapshot['batches']), 1)
            self.assertEqual(len(snapshot['attempts']), 1)
            self.assertEqual(snapshot['attempts'][0]['cleanup'], 'not-needed')


if __name__ == '__main__':
    unittest.main()
