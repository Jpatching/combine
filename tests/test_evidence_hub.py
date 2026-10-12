"""The public HTTP/command boundaries use authored evidence, never game assets."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
COMMAND = ROOT / 'scripts/evidence_hub.py'


class EvidenceHubTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = Path(self.temp.name) / 'state'

    def cli(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(COMMAND), '--state', str(self.state), *args],
                           text=True, capture_output=True, timeout=15)
        if ok:
            self.assertEqual(p.returncode, 0, p.stderr)
        return p

    def start(self):
        p = subprocess.Popen([sys.executable, str(COMMAND), '--state', str(self.state),
                              'serve', '--port', '0'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: (p.terminate(), p.communicate(timeout=10)))
        line = p.stdout.readline()
        self.assertTrue(line.startswith('http://127.0.0.1:'), line)
        self.url = line.strip()
        return self.get('/api/state')

    def get(self, path, headers=None):
        with urllib.request.urlopen(urllib.request.Request(self.url + path, headers=headers or {})) as r:
            return json.loads(r.read())

    def post(self, path, body, token, origin=None):
        headers = {'Content-Type': 'application/json', 'X-Combine-Token': token,
                   'Origin': origin or self.url}
        req = urllib.request.Request(self.url + path, json.dumps(body).encode(), headers, method='POST')
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())

    def test_persistent_candidate_and_idempotent_test_request(self):
        first = self.start()
        request = {'id': str(uuid.uuid4()), 'scenario': 'mount-diagnostic', 'attempts': 10}
        batch = self.post('/api/requests', request, first['token'])
        self.assertEqual(self.post('/api/requests', request, first['token']), batch)
        self.assertEqual(len(self.get('/api/state')['batches']), 1)
        snapshot = json.loads(self.cli('status').stdout)
        self.assertEqual(snapshot['batches'][0]['requested'], 10)
        self.assertEqual(snapshot['candidate']['owner_acceptance'], 'pending')

    def test_requests_cannot_supply_commands_or_cross_origin(self):
        token = self.start()['token']
        valid = {'id': str(uuid.uuid4()), 'scenario': 'preflight', 'attempts': 1}
        for body, origin, expected in [(dict(valid, command='touch bad'), None, 400),
                                       (dict(valid, attempts=True), None, 400),
                                       (dict(valid, scenario='shell'), None, 400),
                                       (valid, 'https://evil.example', 403)]:
            with self.subTest(body=body), self.assertRaises(urllib.error.HTTPError) as error:
                self.post('/api/requests', body, token, origin)
            self.assertEqual(error.exception.code, expected)

    def test_only_registered_unchanged_media_is_served_with_ranges(self):
        clip = Path(self.temp.name) / 'authored.mp4'
        clip.write_bytes(b'0123456789')
        record = Path(self.temp.name) / 'record.json'
        record.write_text(json.dumps({'scenario': 'mount-diagnostic', 'verdict': 'failed',
            'boundary': 'ground-query', 'reason': 'non-finite', 'changed_variable': 'authored fixture',
            'cleanup': 'verified', 'source_revision': 'a' * 40, 'runtime_identity': 'authored',
            'media': [str(clip)]}))
        self.cli('import', str(record))
        snapshot = self.start()
        artifact = snapshot['attempts'][0]['media'][0]['id']
        with urllib.request.urlopen(urllib.request.Request(self.url + '/media/' + artifact,
                                                          headers={'Range': 'bytes=2-5'})) as r:
            self.assertEqual(r.status, 206)
            self.assertEqual(r.read(), b'2345')
        for route in ['/media/../../etc/passwd', '/media/unregistered', '/config.json']:
            with self.assertRaises(urllib.error.HTTPError):
                urllib.request.urlopen(self.url + route)
        clip.write_bytes(b'changed')
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(self.url + '/media/' + artifact)
        self.assertEqual(error.exception.code, 409)

    def test_missing_runtime_configuration_records_refusal_without_input(self):
        token = self.start()['token']
        self.post('/api/requests', {'id': str(uuid.uuid4()), 'scenario': 'mount-diagnostic',
                                  'attempts': 10}, token)
        self.cli('work', '--once')
        snapshot = self.get('/api/state')
        self.assertEqual(len(snapshot['attempts']), 1)
        self.assertEqual(snapshot['attempts'][0]['verdict'], 'refused')
        self.assertEqual(snapshot['attempts'][0]['boundary'], 'configuration')
        self.assertEqual(snapshot['batches'][0]['status'], 'stopped')

    def test_stop_pending_batch_survives_reconnect(self):
        token = self.start()['token']
        batch = self.post('/api/requests', {'id': str(uuid.uuid4()), 'scenario': 'preflight',
                                         'attempts': 10}, token)
        self.post('/api/stop', {'id': batch['id']}, token)
        self.assertEqual(self.get('/api/state')['batches'][0]['status'], 'stopped')
        self.cli('work', '--once')
        self.assertEqual(self.get('/api/state')['attempts'], [])

    def test_two_unchanged_failures_stop_and_remain_authored(self):
        token = self.start()['token']
        self.post('/api/requests', {'id': str(uuid.uuid4()), 'scenario': 'mount-diagnostic',
                                  'attempts': 10}, token)
        fixtures = Path(self.temp.name) / 'fixtures.json'
        fixtures.write_text(json.dumps([{'verdict': 'failed', 'boundary': 'ground-query',
            'reason': 'non-finite', 'changed_variable': 'same fixture', 'cleanup': 'verified'}] * 10))
        self.cli('work', '--once', '--authored-results', str(fixtures))
        state = self.get('/api/state')
        self.assertEqual(len(state['attempts']), 2)
        self.assertEqual(state['batches'][0]['reason'], 'unchanged-failure-needs-new-experiment')
        self.assertTrue(all(a['mode'] == 'authored' for a in state['attempts']))

    def test_unverified_recovery_blocks_all_further_requests_from_execution(self):
        token = self.start()['token']
        for _ in range(2):
            self.post('/api/requests', {'id': str(uuid.uuid4()), 'scenario': 'mount-diagnostic',
                                      'attempts': 10}, token)
        fixtures = Path(self.temp.name) / 'fixtures.json'
        fixtures.write_text(json.dumps([{'verdict': 'unavailable', 'boundary': 'recovery',
            'reason': 'owned-child-pending', 'changed_variable': 'fixture', 'cleanup': 'unknown'}]))
        for _ in range(2): self.cli('work', '--once', '--authored-results', str(fixtures))
        state = self.get('/api/state')
        self.assertEqual(len(state['attempts']), 1)
        self.assertIn('blocked-recovery', [b['status'] for b in state['batches']])

    def test_unchanged_experiment_cannot_restart_in_another_batch(self):
        token = self.start()['token']
        fixtures = Path(self.temp.name) / 'fixtures.json'
        fixtures.write_text(json.dumps([{'verdict': 'failed', 'boundary': 'ground-query',
            'reason': 'non-finite', 'changed_variable': 'same fixture', 'cleanup': 'verified'}] * 10))
        for _ in range(2):
            self.post('/api/requests', {'id': str(uuid.uuid4()), 'scenario': 'mount-diagnostic',
                                      'attempts': 10}, token)
            self.cli('work', '--once', '--authored-results', str(fixtures))
        self.assertEqual(len(self.get('/api/state')['attempts']), 2)
        fixtures.write_text(json.dumps([{'verdict': 'passed', 'boundary': 'ground-query',
            'reason': 'query-observed', 'changed_variable': 'different fixture', 'cleanup': 'verified'}] * 10))
        self.post('/api/requests', {'id': str(uuid.uuid4()), 'scenario': 'mount-diagnostic',
                                  'attempts': 1}, token)
        self.cli('work', '--once', '--authored-results', str(fixtures))
        self.assertEqual(len(self.get('/api/state')['attempts']), 3)


if __name__ == '__main__':
    unittest.main()
