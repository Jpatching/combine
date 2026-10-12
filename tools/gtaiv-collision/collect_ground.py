"""Bounded ground collection; raw observations and identities stay in one private bundle."""
import argparse
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from compare_ground import LABELS, compare, number, position, unique_object

ROOT = Path(__file__).resolve().parents[2]


class Refusal(Exception):
    """Only fixed, source-safe reasons cross the command boundary."""


def read_json(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > 1048576:
        raise Refusal('invalid-input')
    return json.loads(path.read_text(encoding='utf-8-sig'),
                      parse_float=Decimal, object_pairs_hook=unique_object)


def write_json(path, value):
    # Keep exact decimal coordinates as JSON numbers, including in the bundle.
    path.write_text(json_exact(value) + '\n', encoding='utf-8')


def artifact_hashes(items, verify=False):
    if not isinstance(items, list) or not items or len(items) > 32:
        raise Refusal('invalid-input')
    result = []
    seen = set()
    for item in items:
        path = local_path(item['path'])
        digest = item['sha256']
        if not path.is_absolute() or str(path) in seen or not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise Refusal('invalid-input')
        seen.add(str(path))
        if verify:
            try:
                with path.open('rb') as stream:
                    hasher = hashlib.sha256()
                    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                        hasher.update(chunk)
                    actual = hasher.hexdigest()
            except OSError:
                raise Refusal('artifact-mismatch') from None
            if actual != digest:
                raise Refusal('artifact-mismatch')
        result.append(digest)
    return result


def local_path(value):
    if os.name != 'nt' and re.match(r'^[A-Za-z]:\\', value):
        return Path('/mnt/' + value[0].lower() + '/' + value[3:].replace('\\', '/'))
    return Path(value)


def windows_path(value):
    if os.name == 'nt':
        return str(value)
    result = subprocess.run(['wslpath', '-w', str(value)], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def powershell():
    return 'powershell' if os.name == 'nt' else 'powershell.exe'


def probe_source(document, token):
    points, _ = validate_points(document)
    if not isinstance(token, str) or not re.fullmatch('[0-9a-f]{32}', token):
        raise Refusal('invalid-input')
    if any(p['qualified'] is not True or not p.get('surface_evidence') or not p.get('layer_evidence') for p in points.values()):
        raise Refusal('unconfirmed-checkpoints')
    config = {'token': token, 'checkpoints': [
        {key: point[key] for key in ('label', 'position', 'query_z_m')} for point in points.values()]}
    # Serialize exact point data as a literal, never as executable input.
    holder = Path(__file__).with_name('ground_probe.js').read_text(encoding='utf-8')
    return holder.replace('__CONFIG__', json_exact(config))


def json_exact(value):
    if isinstance(value, Decimal):
        if not value.is_finite():
            return 'null'
        return str(value)
    if isinstance(value, dict):
        return '{' + ','.join(json.dumps(k) + ':' + json_exact(x) for k, x in value.items()) + '}'
    if isinstance(value, list):
        return '[' + ','.join(json_exact(x) for x in value) + ']'
    return json.dumps(value, allow_nan=False)


class WindowsObservation:
    """Adapter over the retained current-run reader and reviewed native buffer."""
    def __init__(self, session_path, session, output, timeout_seconds):
        self.session_path, self.session, self.output = session_path, session, output
        self.timeout_seconds = timeout_seconds
        self.process = None
        self.restarts = 0

    def __iter__(self):
        command = [powershell(), '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File',
                   windows_path(Path(__file__).with_name('observe_ground.ps1')),
                   '-Session', windows_path(Path(self.session_path).resolve()),
                   '-Output', windows_path(self.output.resolve())]
        with (self.output / 'observer-private.log').open('w') as log:
            process = self.process = subprocess.Popen(command, stdout=log, stderr=log)
            try:
                status = process.wait(timeout=self.timeout_seconds)
            except subprocess.TimeoutExpired:
                # The observer owns its key-up and has its own 35-second deadline.
                # Retain a timed-out child; never terminate it between down/up.
                raise Refusal('observer-timeout') from None
        path = self.output / 'events-private.jsonl'
        if not path.is_file() or path.stat().st_size > 1048576:
            raise Refusal('collection-interrupted')
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            event = json.loads(line, parse_float=Decimal, object_pairs_hook=unique_object)
            if event.get('kind') == 'reading':
                witness = self.session.get('witnesses', {}).get(event.get('label'), {})
                for key in ('ground_loaded', 'intended_surface', 'loading_evidence', 'layer_evidence'):
                    event['reading'][key] = witness.get(key)
            yield event
        if status != 0:
            raise Refusal('observer-refused')

    def restore(self):
        if self.process is not None and self.process.poll() is None:
            # Neither restoration nor new input may race a retained observer.
            raise Refusal('observer-still-running')
        if self.process is not None:
            try:
                keys = read_json(self.output / 'input-cleanup-private.json')
                if type(keys.get('owned')) is not bool or keys.get('released') is not True:
                    raise Refusal('input-release-unverified')
            except (OSError, ValueError, KeyError, TypeError):
                raise Refusal('input-release-unverified') from None
        recovery_session = dict(self.session)
        restoration = self.session.get('restore_script')
        if restoration:
            artifact_hashes([restoration], verify=True)
            self.restarts = None
            with (self.output / 'restoration-private.log').open('w') as log:
                process = subprocess.Popen([powershell(), '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File',
                    windows_path(local_path(restoration['path'])), '-Mode', 'Restore'], stdout=log, stderr=log)
                try:
                    status = process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    raise Refusal('restoration-failed') from None
            if status != 0:
                raise Refusal('restoration-failed')
            # Successful byte restoration is not evidence of a restart. Observe
            # the actual run identity; missing/ambiguous identity stays unknown.
            script = "$g=@(Get-Process GTAIV -ErrorAction SilentlyContinue);if($g.Count -ne 1){exit 2};$s=[DateTimeOffset]$g[0].StartTime.ToUniversalTime();[pscustomobject]@{pid=$g[0].Id;start_ms=$s.ToUnixTimeMilliseconds();executable=$g[0].Path}|ConvertTo-Json -Compress"
            try:
                observed = subprocess.run([powershell(), '-NoProfile', '-NonInteractive', '-Command', script],
                                          capture_output=True, text=True, timeout=10)
                (self.output / 'restoration-run-private.log').write_text(observed.stdout + observed.stderr)
                identity = json.loads(observed.stdout, object_pairs_hook=unique_object)
                owner = self.session['process']
                if observed.returncode == 0 and type(identity.get('pid')) is int and type(identity.get('start_ms')) is int and identity.get('executable', '').casefold() == self.session['executable'].casefold():
                    self.restarts = int((identity['pid'], identity['start_ms']) != (owner['pid'], owner['start_ms']))
                    recovery_session['process'] = {key: identity[key] for key in ('pid', 'start_ms')}
            except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError, RecursionError):
                pass
        artifact_hashes(self.session['retained_artifacts'], verify=True)
        recovery_session['artifacts'] = self.session['retained_artifacts']
        recovery_path = self.output / 'recovery-session-private.json'
        write_json(recovery_path, recovery_session)
        gate = ROOT / 'tools/workbench/trial.ps1'
        result_path = self.output / 'recovery-readiness-private.json'
        with (self.output / 'recovery-readiness-private.log').open('w') as log:
            checked = subprocess.run([powershell(), '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                '-File', windows_path(gate), '-Session', windows_path(recovery_path),
                '-StatusModule', windows_path(ROOT / 'tools/gtaiv-skate/game-status.psm1'),
                '-Output', windows_path(result_path), '-Scenario', 'preflight'],
                stdout=log, stderr=log, timeout=20)
        readiness = read_json(result_path)
        if checked.returncode != 0 or readiness.get('verdict') != 'passed':
            raise Refusal('recovery-readiness-unverified')
        return 'verified'


def validate_points(document):
    values = document.get('checkpoints')
    if type(document.get('schema_version')) is not int or document['schema_version'] != 1 or not isinstance(values, list) or not 4 <= len(values) <= 32:
        raise Refusal('invalid-input')
    points = {}
    for point in values:
        label = point.get('label')
        if not isinstance(label, str) or not label.isascii() or not label.replace('_', '').isalnum() or not 1 <= len(label) <= 32 or label in points:
            raise Refusal('invalid-input')
        position(point.get('position'))
        number(point.get('mesh_height_m'))
        number(point.get('query_z_m'))
        if type(point.get('qualified')) is not bool:
            raise Refusal('invalid-input')
        points[label] = point
    if not set(LABELS) <= points.keys():
        raise Refusal('missing-points')
    # The existing comparator validates the identity and the unchanged frozen set.
    frozen = dict(document, checkpoints=[points[label] for label in LABELS])
    compare(frozen, dict(frozen, checkpoints=[]))
    return points, frozen


def ready(snapshot, session):
    owner = session['process']
    for field in ('pid', 'start_ms', 'now_ms', 'updated_ms'):
        if type(snapshot.get(field)) is not int:
            raise Refusal('stale-process-status')
    if snapshot['pid'] != owner['pid'] or snapshot['start_ms'] != owner['start_ms'] or snapshot['pid'] <= 0:
        raise Refusal('stale-process-status')
    age = snapshot['now_ms'] - snapshot['updated_ms']
    if snapshot['updated_ms'] < owner['start_ms'] or not -1000 <= age <= 2000:
        raise Refusal('stale-process-status')
    if snapshot.get('foreground') is not True or snapshot.get('minimized') is not False or snapshot.get('responding') is not True:
        raise Refusal('foreground-lost')
    if snapshot.get('scene') != 'gameplay' or any(snapshot.get(f) is not True for f in ('player_control', 'on_foot', 'adapter_ready')) or snapshot.get('mounted') is not False:
        raise Refusal('not-ready')
    if snapshot.get('artifacts') != artifact_hashes(session['artifacts']):
        raise Refusal('artifact-mismatch')


def validate_session(session):
    if type(session.get('schema_version')) is not int or session['schema_version'] != 1:
        raise Refusal('invalid-input')
    owner = session.get('process', {})
    if any(type(owner.get(k)) is not int or owner[k] <= 0 for k in ('pid', 'start_ms')):
        raise Refusal('stale-process-status')


def collect(points_document, session, events, output, mode, cleanup=None):
    started = time.monotonic()
    report = {'mode': mode, 'verdict': 'inconclusive', 'reason': 'collection-interrupted',
              'restoration': 'unverified'}
    observations = {'schema_version': 1, 'selected_sha256': points_document.get('selected_sha256'), 'checkpoints': []}
    private = {'mode': mode, 'observations': observations, 'events': [], 'timing': {}}
    readings = {}
    complete = False
    verified = False
    try:
        points, frozen = validate_points(points_document)
        validate_session(session)
        artifact_hashes(session['artifacts'], verify=True)
        artifact_hashes(session['retained_artifacts'])
        if session.get('restore_script'):
            artifact_hashes([session['restore_script']], verify=True)
        verified = True
        private['timing']['setup_seconds'] = time.monotonic() - started
        collection_started = time.monotonic()
        first = True
        for event in events:
            if len(private['events']) >= 100 or time.monotonic() - started > 120:
                raise Refusal('collection-interrupted')
            private['events'].append(event)
            kind = event.get('kind')
            if kind == 'refused':
                reason = event.get('reason')
                allowed = ('stale-process-status', 'foreground-lost', 'artifact-mismatch',
                           'not-ready', 'collection-interrupted', 'observer-refused')
                raise Refusal(reason if reason in allowed else 'observer-refused')
            if kind == 'restored':
                if event.get('snapshot', {}).get('artifacts') != artifact_hashes(session['retained_artifacts']):
                    raise Refusal('restoration-failed')
                report['restoration'] = 'verified'
                break
            ready(event.get('snapshot', {}), session)
            if first:
                if kind != 'ready':
                    raise Refusal('late-collection')
                if type(event.get('setup_ms')) is int and 0 <= event['setup_ms'] <= 120000:
                    private['timing']['observer_setup_seconds'] = Decimal(event['setup_ms']) / 1000
                first = False
                continue
            if kind == 'complete':
                if complete:
                    raise Refusal('invalid-observation')
                complete = True
                if type(event.get('collection_ms')) is int and 0 <= event['collection_ms'] <= 120000:
                    private['timing']['observer_collection_seconds'] = Decimal(event['collection_ms']) / 1000
                continue
            if kind != 'reading' or complete:
                raise Refusal('invalid-observation')
            label, batch = event.get('label'), event.get('batch')
            if label not in points or type(batch) is not int or batch != len(readings.get(label, [])) or batch >= 3:
                raise Refusal('invalid-observation')
            reading = dict(event['reading'])
            if reading.get('buffer_intact') is not True:
                reading['query_success'] = False
            # Independent witness references are mandatory; physical flags and
            # height success are deliberately never promoted into these flags.
            for flag, evidence in (('ground_loaded', 'loading_evidence'), ('intended_surface', 'layer_evidence')):
                if not isinstance(reading.get(evidence), str) or not reading[evidence].strip():
                    reading[flag] = None
            if not points[label].get('surface_evidence') or not points[label].get('layer_evidence'):
                reading['intended_surface'] = None
            readings.setdefault(label, []).append(reading)
        private['timing']['collection_seconds'] = time.monotonic() - collection_started
        observations['checkpoints'] = [{'label': label, 'readings': rows} for label, rows in readings.items()]
        if complete:
            result = compare(frozen, dict(observations, checkpoints=[p for p in observations['checkpoints'] if p['label'] in LABELS]))
            report.update(result)
            report.pop('reason', None)
            if any(len(readings.get(label, [])) != 3 for label in points):
                report.update(verdict='inconclusive', reason='collection-incomplete')
        if cleanup is None and report['restoration'] != 'verified':
            raise Refusal('restoration-failed')
    except Refusal as error:
        report.update(verdict='inconclusive', reason=str(error))
        if str(error) == 'restoration-failed':
            report['restoration'] = 'failed'
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError, RecursionError):
        report.update(verdict='inconclusive', reason='invalid-input')
    finally:
        if cleanup is not None and verified:
            try:
                report['restoration'] = cleanup()
            except Refusal as error:
                reason = str(error)
                if reason == 'observer-still-running':
                    report.update(verdict='inconclusive', reason=reason, restoration='required')
                else:
                    report.update(verdict='inconclusive', reason='restoration-failed', restoration='failed')
            except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
                report.update(verdict='inconclusive', reason='restoration-failed', restoration='failed')
        observations['checkpoints'] = [{'label': label, 'readings': rows} for label, rows in readings.items()]
        private['report'] = report
        private['timing']['total_seconds'] = time.monotonic() - started
        write_json(output / 'result-private.json', private)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoints', required=True)
    parser.add_argument('--session', required=True)
    parser.add_argument('--output', required=True, help='New private bundle directory')
    parser.add_argument('--authored-events', help='Authored test observations; never live evidence')
    parser.add_argument('--prepare-probe', action='store_true', help='Write a private script for reviewed staging; do not execute')
    parser.add_argument('--timeout-seconds', type=int, choices=range(1, 51), default=50,
                        metavar='1..50', help='Observer deadline; default 50 seconds')
    args = parser.parse_args(argv)
    report = {'mode': 'authored' if args.authored_events else 'live', 'verdict': 'inconclusive', 'reason': 'invalid-input', 'restoration': 'unverified'}
    output = None
    created_output = False
    try:
        output = Path(args.output)
        output.mkdir(mode=0o700, parents=False, exist_ok=False)
        created_output = True
        points_document, session = read_json(args.checkpoints), read_json(args.session)
        if args.prepare_probe:
            source = probe_source(points_document, session.get('token'))
            (output / 'diagnostic-script.js').write_text(source, encoding='utf-8')
            write_json(output / 'probe-config-private.json', {
                'token': session['token'],
                'checkpoints_sha256': hashlib.sha256(Path(args.checkpoints).read_bytes()).hexdigest(),
                'script_sha256': hashlib.sha256(source.encode()).hexdigest()})
            print(json.dumps({'mode': 'preparation', 'verdict': 'prepared', 'execution': 'none'}))
            return 0
        live = None
        if args.authored_events:
            events = read_json(args.authored_events)
        else:
            source = probe_source(points_document, session.get('token'))
            digest = hashlib.sha256(source.encode()).hexdigest()
            contract = read_json(Path(__file__).resolve().parents[1] / 'workbench/runtime-roles.json')
            required_roles = set(contract['required'])
            allowed_roles = required_roles | set(contract['optional'])
            artifacts = session.get('artifacts', [])
            observed_roles = {item.get('role') for item in artifacts}
            if len(artifacts) != len(observed_roles) or not required_roles <= observed_roles <= allowed_roles:
                raise Refusal('runtime-inventory-incomplete')
            by_role = {item['role']: item for item in artifacts}
            if by_role['executable']['path'] != session.get('executable') or by_role['script']['sha256'] != digest or session.get('checkpoints_sha256') != hashlib.sha256(Path(args.checkpoints).read_bytes()).hexdigest():
                raise Refusal('artifact-mismatch')
            if {item['path'] for item in artifacts} != {item['path'] for item in session.get('retained_artifacts', [])}:
                raise Refusal('runtime-inventory-incomplete')
            if not (os.name == 'nt' or os.environ.get('WSL_DISTRO_NAME')):
                raise Refusal('live-runner-unavailable')
            live = WindowsObservation(args.session, session, output, args.timeout_seconds)
            events = live
        report = collect(points_document, session, iter(events), output, report['mode'],
                         cleanup=live.restore if live else None)
        if live:
            # Counts observed before/after replacements, not restoration exits.
            write_json(output / 'restart-count-private.json', {'verified_process_replacements': live.restarts})
    except Refusal as error:
        report['reason'] = str(error)
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError, RecursionError, subprocess.SubprocessError):
        pass
    if created_output and not (output / 'result-private.json').exists():
        try:
            write_json(output / 'result-private.json', {'report': report, 'observations': [], 'timing': {}})
        except OSError:
            report.update(verdict='inconclusive', reason='bundle-unavailable')
    print(json.dumps(report))
    return {'agreement': 0, 'disagreement': 1, 'inconclusive': 2}[report['verdict']]


if __name__ == '__main__':
    sys.exit(main())
