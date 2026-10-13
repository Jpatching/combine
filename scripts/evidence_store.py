"""Private, durable candidate evidence and bounded requests. No game actions."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import uuid

SCENARIOS = {'preflight': 'Check current windowed gameplay readiness',
             'offline-menus': 'Resume recognized offline menus in the current process',
             'checkpoint': 'Return Niko to the prepared exterior test checkpoint',
             'mount-diagnostic': 'Identify the first mount/refusal boundary',
             'ground-query': 'Collect independently qualified checkpoint readings'}
VERDICTS = {'untested', 'unavailable', 'refused', 'failed', 'passed', 'inconclusive'}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def identifier(value):
    if not isinstance(value, str) or str(uuid.UUID(value)) != value:
        raise ValueError('Invalid request identity')
    return value


class Store:
    def __init__(self, directory):
        self.root = Path(directory).resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = self.root / 'evidence.sqlite'
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS batches (id TEXT PRIMARY KEY, data TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS attempts (id TEXT PRIMARY KEY, data TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS media (id TEXT PRIMARY KEY, path TEXT NOT NULL,
                                                sha256 TEXT NOT NULL, size INTEGER NOT NULL);
            ''')
            candidate = {'title': 'GTA IV riding candidate', 'source_revision': 'unpublished',
                         'source_checks': 'untested', 'owner_acceptance': 'pending',
                         'question': 'Why does the ground query refuse before riding?',
                         'next_experiment': 'Compare query availability at one retained checkpoint',
                         'criteria': [
                             {'text': 'Independent loaded collision and intended layer at four checkpoints', 'status': 'inconclusive'},
                             {'text': 'Three readings per point; spread ≤2 cm, mesh error ≤5 cm', 'status': 'untested'},
                             {'text': 'Mount, push, both steering directions, dismount and ordinary GTA recovery', 'status': 'untested'},
                             {'text': 'Recovery after restart and physical-controller trial', 'status': 'untested'}],
                         'blockers': ['Ground query availability/loading/layer remain unqualified'],
                         'issues': [20, 39, 53, 54]}
            db.execute('INSERT OR IGNORE INTO meta VALUES (?,?)', ('candidate', json.dumps(candidate)))
        os.chmod(self.db, 0o600)

    def connect(self):
        db = sqlite3.connect(self.db, timeout=10)
        db.row_factory = sqlite3.Row
        return db

    def snapshot(self):
        with self.connect() as db:
            return {'candidate': json.loads(db.execute("SELECT value FROM meta WHERE key='candidate'").fetchone()[0]),
                    'scenarios': SCENARIOS,
                    'batches': [json.loads(r[0]) for r in db.execute('SELECT data FROM batches ORDER BY rowid DESC LIMIT 100')],
                    'attempts': [json.loads(r[0]) for r in db.execute('SELECT data FROM attempts ORDER BY rowid DESC LIMIT 200')],
                    'updated_at': now()}

    def set_candidate(self, value):
        if not isinstance(value, dict) or value.get('owner_acceptance', 'pending') != 'pending':
            raise ValueError('Owner approval remains in chat')
        allowed = {'title', 'source_revision', 'source_checks', 'question', 'next_experiment', 'criteria', 'blockers', 'issues'}
        if set(value) - allowed:
            raise ValueError('Unsupported candidate fields')
        with self.connect() as db:
            current = json.loads(db.execute("SELECT value FROM meta WHERE key='candidate'").fetchone()[0])
            current.update(value)
            db.execute("UPDATE meta SET value=? WHERE key='candidate'", (json.dumps(current),))

    def request(self, value):
        if set(value) != {'id', 'scenario', 'attempts'} or value['scenario'] not in SCENARIOS:
            raise ValueError('Choose a predefined scenario')
        request_id = identifier(value['id'])
        if type(value['attempts']) is not int or not 1 <= value['attempts'] <= 10:
            raise ValueError('Choose one to ten attempts')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            existing = db.execute('SELECT data FROM batches WHERE id=?', (request_id,)).fetchone()
            if existing:
                batch = json.loads(existing[0])
                if batch['scenario'] != value['scenario'] or batch['requested'] != value['attempts']:
                    raise ValueError('Request identity already has different contents')
                return batch
            batch = {'id': request_id, 'scenario': value['scenario'], 'requested': value['attempts'],
                     'status': 'pending', 'stop_requested': False, 'created_at': now(), 'completed': 0}
            db.execute('INSERT INTO batches VALUES (?,?)', (request_id, json.dumps(batch)))
            return batch

    def stop(self, request_id):
        identifier(request_id)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT data FROM batches WHERE id=?', (request_id,)).fetchone()
            if not row:
                raise ValueError('Unknown batch')
            batch = json.loads(row[0]); batch['stop_requested'] = True
            if batch['status'] == 'pending':
                batch['status'] = 'stopped'
            db.execute('UPDATE batches SET data=? WHERE id=?', (json.dumps(batch), request_id))
            return batch

    def claim(self):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            batches = [json.loads(r[0]) for r in db.execute('SELECT data FROM batches ORDER BY rowid')]
            operation = db.execute("SELECT value FROM meta WHERE key='runtime_operation'").fetchone()
            if operation and json.loads(operation[0])['status'] in {'running', 'unverified'}:
                return None
            if any(b['status'] in {'running', 'blocked-recovery'} for b in batches):
                return None
            batch = next((b for b in batches if b['status'] == 'pending'), None)
            if batch:
                batch.update(status='running', started_at=now())
                db.execute('UPDATE batches SET data=? WHERE id=?', (json.dumps(batch), batch['id']))
            return batch

    def begin_runtime_operation(self, action):
        if action not in {'open', 'recover'}:
            raise ValueError('Unsupported runtime operation')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            batches = [json.loads(r[0]) for r in db.execute('SELECT data FROM batches')]
            operation = db.execute("SELECT value FROM meta WHERE key='runtime_operation'").fetchone()
            if any(b['status'] in {'running', 'blocked-recovery'} for b in batches) or (
                    operation and json.loads(operation[0])['status'] in {'running', 'unverified'}):
                raise ValueError('recovery-reconciliation-required')
            lease = {'id': str(uuid.uuid4()), 'action': action, 'status': 'running', 'started_at': now()}
            db.execute("INSERT OR REPLACE INTO meta VALUES ('runtime_operation', ?)", (json.dumps(lease),))
            return lease

    def finish_runtime_operation(self, lease, status):
        if status not in {'completed', 'refused', 'unverified'}:
            raise ValueError('Invalid runtime operation outcome')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            current = json.loads(db.execute("SELECT value FROM meta WHERE key='runtime_operation'").fetchone()[0])
            if current['id'] != lease['id'] or current['status'] != 'running':
                raise ValueError('Runtime operation ownership changed')
            current.update(status=status, finished_at=now())
            db.execute("UPDATE meta SET value=? WHERE key='runtime_operation'", (json.dumps(current),))

    def finish(self, batch, status, reason):
        with self.connect() as db:
            batch.update(status=status, reason=reason, finished_at=now())
            # A stop requested from another connection is retained.
            row = json.loads(db.execute('SELECT data FROM batches WHERE id=?', (batch['id'],)).fetchone()[0])
            batch['stop_requested'] = row['stop_requested']
            db.execute('UPDATE batches SET data=? WHERE id=?', (json.dumps(batch), batch['id']))

    def stopped(self, batch):
        with self.connect() as db:
            row = db.execute('SELECT data FROM batches WHERE id=?', (batch['id'],)).fetchone()
            return json.loads(row[0])['stop_requested']

    def add_attempt(self, value, batch=None):
        if value.get('scenario') not in SCENARIOS or value.get('verdict') not in VERDICTS:
            raise ValueError('Invalid attempt scenario/verdict')
        allowed = {'scenario', 'verdict', 'boundary', 'reason', 'changed_variable', 'cleanup',
                   'source_revision', 'controller_revision', 'runtime_identity', 'started_at',
                   'finished_at', 'next_experiment', 'measurements', 'limitations', 'mode', 'media', 'diagnostic'}
        allowed.add('experiment')
        if set(value) - allowed:
            raise ValueError('Unsupported evidence fields')
        value = dict(value)
        value.update(id=str(uuid.uuid4()), recorded_at=now(), owner_acceptance='pending')
        value['media'] = [self.register(path) for path in value.get('media', [])]
        if batch:
            value['batch_id'] = batch['id']
            batch['completed'] += 1
        with self.connect() as db:
            db.execute('INSERT INTO attempts VALUES (?,?)', (value['id'], json.dumps(value)))
            if batch:
                current = json.loads(db.execute('SELECT data FROM batches WHERE id=?', (batch['id'],)).fetchone()[0])
                batch['stop_requested'] = current['stop_requested']
                db.execute('UPDATE batches SET data=? WHERE id=?', (json.dumps(batch), batch['id']))
        return value

    def scenario_stopped(self, scenario, experiment):
        with self.connect() as db:
            failures = 0
            signature = None
            for row in db.execute('SELECT data FROM attempts ORDER BY rowid DESC'):
                attempt = json.loads(row[0])
                if attempt['scenario'] != scenario: continue
                if attempt.get('experiment') != experiment or attempt['verdict'] == 'passed': return False
                observed = (attempt['verdict'], attempt.get('boundary'), attempt.get('reason'))
                if signature is not None and observed != signature: return False
                signature = observed
                failures += 1
                if failures == 2: return True
        return False

    def register(self, filename):
        path = Path(filename).expanduser().resolve(strict=True)
        if not path.is_file() or path.suffix.lower() not in {'.mp4', '.webm', '.png', '.jpg', '.jpeg', '.webp'}:
            raise ValueError('Only browser-viewable evidence media can be registered')
        sha = digest(path); key = str(uuid.uuid4()); size = path.stat().st_size
        with self.connect() as db:
            db.execute('INSERT INTO media VALUES (?,?,?,?)', (key, str(path), sha, size))
        return {'id': key, 'name': path.name, 'sha256': sha, 'size': size}

    def media(self, key):
        identifier(key)
        with self.connect() as db:
            row = db.execute('SELECT * FROM media WHERE id=?', (key,)).fetchone()
        if not row:
            raise FileNotFoundError('Unregistered evidence')
        path = Path(row['path'])
        if path.is_symlink() or not path.is_file() or digest(path) != row['sha256']:
            raise ValueError('Registered media changed')
        return path
