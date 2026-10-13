"""Local public commands retain requests and refuse missing setup without input."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

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

    def test_specific_recovery_reconciliation_holds_runtime_and_retains_history(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from evidence_store import Store
        with tempfile.TemporaryDirectory() as directory:
            store = Store(directory)
            store.request({'id': str(uuid.uuid4()), 'scenario': 'preflight', 'attempts': 1})
            batch = store.claim()
            store.finish(batch, 'blocked-recovery', 'recovery-unverified')
            lease = store.begin_reconciliation(batch['id'])
            self.assertIsNone(store.claim())
            with self.assertRaises(ValueError):
                store.begin_reconciliation(batch['id'])
            store.reconcile_recovery(lease, 'fresh-normal-gameplay')
            original = store.snapshot()['batches'][0]
            self.assertEqual(original['reason'], 'recovery-unverified')
            self.assertEqual(original['status'], 'reconciled-recovery')
            self.assertEqual(original['reconciliation']['observation'], 'fresh-normal-gameplay')
            store.request({'id': str(uuid.uuid4()), 'scenario': 'preflight', 'attempts': 1})
            self.assertIsNotNone(store.claim())

    def test_ride_proof_is_predefined_and_refuses_missing_setup(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            config = folder / 'gta.json'
            config.write_text(json.dumps({'state': str(folder / 'state')}))
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/workbench.py'),
                'gta', 'test', '--config', str(config), '--scenario', 'ride-proof'],
                text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('runtime-configuration-unavailable', result.stdout)

    def test_local_reconcile_requires_specific_batch_and_refuses_pending_helpers(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from evidence_store import Store
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            store = Store(folder / 'state')
            batch_id = str(uuid.uuid4())
            store.request({'id': batch_id, 'scenario': 'preflight', 'attempts': 1})
            store.finish(store.claim(), 'blocked-recovery', 'recovery-unverified')
            pending = store.root / 'runs' / 'retained'
            pending.mkdir(parents=True)
            (pending / 'pending-child-private.json').write_text('{}')
            config = folder / 'gta.json'
            config.write_text(json.dumps({'state': str(store.root), 'runtime_config': str(folder / 'runtime.json')}))
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/workbench.py'),
                'gta', 'reconcile', '--config', str(config), '--request-id', batch_id],
                text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn('owned-helper-pending', result.stdout)
            self.assertEqual(store.snapshot()['batches'][0]['status'], 'blocked-recovery')
            self.assertEqual(store.snapshot()['batches'][0]['reason'], 'recovery-unverified')

    def test_reconciliation_binds_the_immutable_original_attempt_session(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from evidence_store import Store
        with tempfile.TemporaryDirectory() as directory:
            store = Store(directory)
            store.request({'id': str(uuid.uuid4()), 'scenario': 'preflight', 'attempts': 1})
            batch = store.claim()
            store.add_attempt({'scenario': 'preflight', 'verdict': 'unavailable', 'media': [],
                'runtime_identity': 'build=' + 'a' * 40 + '; session-sha256=' + 'b' * 64}, batch)
            store.finish(batch, 'blocked-recovery', 'recovery-unverified')
            lease = store.begin_reconciliation(batch['id'])
            store.validate_recovery_session(lease, 'b' * 64)
            with self.assertRaises(ValueError):
                store.validate_recovery_session(lease, 'c' * 64)

    def test_owner_can_run_native_trial_without_recording_setup(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        import gta_trial
        from evidence_store import Store, digest
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            session = folder / 'session.json'
            session.write_text(json.dumps({'recorded_build_revision': 'a' * 40}))
            config = folder / 'runtime.json'
            config.write_text(json.dumps({'source_checkout': str(folder), 'source_revision': 'a' * 40,
                'session': str(session), 'session_sha256': digest(session), 'record_video': False}))
            def output(command, **kwargs):
                if command[0] == 'wslpath':
                    return command[-1]
                if command[1:3] == ['rev-parse', 'HEAD']:
                    return 'a' * 40
                return ''
            class NativeFixture:
                def __init__(self, command, **kwargs):
                    target = Path(command[command.index('-Output') + 1])
                    target.write_text(json.dumps({'verdict': 'passed', 'boundary': 'ride',
                        'reason': 'ride-proof-observed', 'cleanup': 'verified', 'runtime_identity': 'authored-native-fixture',
                        'mount_observation_ms': 237.5}))
                def wait(self, timeout):
                    return 0
            with patch.dict('os.environ', {'WSL_DISTRO_NAME': 'authored'}), \
                    patch.object(gta_trial.subprocess, 'check_output', side_effect=output), \
                    patch.object(gta_trial.subprocess, 'Popen', NativeFixture):
                result = gta_trial.attempt(Store(folder / 'store'), 'ride-proof', config)
            self.assertEqual(result['verdict'], 'passed')
            self.assertEqual(result['cleanup'], 'verified')
            self.assertEqual(result['mount_observation_ms'], 237.5)
            self.assertEqual(result['media'], [])
            self.assertIn('automated video disabled; owner observation unverified', result['limitations'])
            self.assertNotIn('owner-observed', result['limitations'])

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
