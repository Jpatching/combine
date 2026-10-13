"""Local GTA workflow over the retained launcher and durable diagnostic queue."""
import json
import os
from pathlib import Path
import subprocess
import time
import uuid

from evidence_store import Store, digest, identifier

ROOT = Path(__file__).resolve().parents[1]


def windows(path):
    path = str(Path(path).resolve())
    if os.name == 'nt':
        return path
    return subprocess.check_output(['wslpath', '-w', path], text=True).strip()


def native(script, *arguments, transaction=None):
    if not (os.name == 'nt' or os.environ.get('WSL_DISTRO_NAME')):
        raise ValueError('windows-runtime-unavailable')
    command = ['powershell' if os.name == 'nt' else 'powershell.exe',
        '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File',
        windows(ROOT / script), *arguments]
    process = subprocess.Popen(command)
    name = Path(script).stem
    pending = transaction / ('pending-' + name + '-private.json') if transaction else None
    try:
        if pending:
            pending.write_text(json.dumps({'pid': process.pid, 'started_at': time.time(), 'script': script}))
        # A timed-out/interrupted helper remains owned and is never killed implicitly.
        code = process.wait(timeout=180)
        if pending:
            pending.replace(transaction / ('completed-' + name + '-private.json'))
    except Exception as error:
        raise RuntimeError('native-helper-unverified') from error
    return subprocess.CompletedProcess(command, code)


def execute(action, config_path, scenario='mount-diagnostic', request_id=None, allow_hung_termination=False,
            monitor_timeout=45):
    lease = None
    outcome = 'refused'
    try:
        config_path = Path(config_path).resolve()
        if allow_hung_termination and action != 'recover':
            raise ValueError('hung-termination-needs-recovery')
        if action == 'monitor' and not 5 <= monitor_timeout <= 120:
            raise ValueError('monitor-timeout-out-of-range')
        config = json.loads(config_path.read_text())
        if not isinstance(config, dict) or set(config) - {'state', 'inspection', 'window_mode', 'manifest', 'runtime_config'}:
            raise ValueError('configuration-unavailable')
        def path(name):
            value = config[name]
            if not isinstance(value, str) or not value:
                raise ValueError('configuration-unavailable')
            return (config_path.parent / value).resolve()
        if action == 'status':
            # Require the same reviewed launch configuration, even for inspection.
            path('inspection')
            return native('tools/workbench/status.ps1', '-StatusModule',
                          windows(ROOT / 'tools/gtaiv-skate/game-status.psm1')).returncode
        if action == 'monitor':
            return native('tools/workbench/monitor.ps1', '-Inspection', windows(path('inspection')),
                          '-StatusModule', windows(ROOT / 'tools/gtaiv-skate/game-status.psm1'),
                          '-TimeoutSeconds', str(monitor_timeout)).returncode
        store = Store(path('state'))
        if action == 'reconcile':
            if request_id is None:
                raise ValueError('specific-recovery-batch-required')
            identifier(request_id)
            lease = store.begin_reconciliation(request_id)
            # Conservatively retain every unresolved child marker; never infer key release.
            def no_pending():
                if any(store.root.glob('runs/**/pending-*-private.json')) or any(
                        store.root.glob('launches/**/pending-*-private.json')):
                    raise ValueError('owned-helper-pending')
            no_pending()
            runtime = json.loads(path('runtime_config').read_text())
            session = Path(runtime['session'])
            if digest(session) != runtime['session_sha256']:
                raise ValueError('session-mismatch')
            store.validate_recovery_session(lease, runtime['session_sha256'])
            folder = store.root / 'launches' / uuid.uuid4().hex
            folder.mkdir(parents=True, mode=0o700)
            output = folder / 'reconciliation-private.json'
            outcome = 'unverified'
            result = native('tools/workbench/reconcile.ps1', '-Session', windows(session),
                            '-StatusModule', windows(ROOT / 'tools/gtaiv-skate/game-status.psm1'),
                            '-Output', windows(output), transaction=folder)
            outcome = 'refused'
            if result.returncode:
                print('UNAVAILABLE: recovery-observation-unavailable; retained failure unchanged')
                return 2
            no_pending()
            if digest(session) != runtime['session_sha256']:
                raise ValueError('original-session-binding-unverified')
            store.validate_recovery_session(lease, runtime['session_sha256'])
            observation = json.loads(output.read_text(encoding='utf-8-sig'))
            if set(observation) != {'observation'} or observation['observation'] not in {'fresh-normal-gameplay', 'original-session-exited'}:
                raise ValueError('recovery-observation-unavailable')
            store.reconcile_recovery(lease, observation['observation'])
            lease = None
            print('PASS: specific recovery batch reconciled; original diagnostic retained; no game input')
            return 0
        if action == 'test':
            from gta_trial import work
            batch = store.request({'id': request_id or str(uuid.uuid4()),
                                   'scenario': scenario, 'attempts': 1})
            if batch['status'] == 'pending':
                runtime = path('runtime_config') if 'runtime_config' in config else None
                work(store, runtime, once=True)
            snapshot = store.snapshot()
            batch = next(b for b in snapshot['batches'] if b['id'] == batch['id'])
            attempt = next((a for a in snapshot['attempts'] if a.get('batch_id') == batch['id']), None)
            print(json.dumps({'request_id': batch['id'], 'status': batch['status'],
                'verdict': attempt['verdict'] if attempt else 'unavailable',
                'reason': attempt['reason'] if attempt else batch.get('reason', 'waiting-for-runner'),
                'cleanup': attempt['cleanup'] if attempt else 'unknown'}))
            return 0 if attempt and attempt['verdict'] == 'passed' and attempt['cleanup'] in {'verified', 'not-needed'} else 2
        inspection, mode = path('inspection'), path('window_mode')
        lease = store.begin_runtime_operation(action)
        folder = store.root / 'launches' / uuid.uuid4().hex
        folder.mkdir(parents=True, mode=0o700)
        output = folder / 'window-private.json'
        arguments = ['-Inspection', windows(inspection), '-WindowMode', windows(mode),
                     '-Output', windows(output), '-Focus']
        if action == 'recover':
            arguments.append('-Restart')
            if allow_hung_termination:
                arguments.append('-AllowHungTermination')
        outcome = 'unverified'
        try:
            result = native('tools/workbench/open.ps1', *arguments, transaction=folder)
        except (OSError, ValueError, subprocess.CalledProcessError):
            outcome = 'refused'
            raise
        if result.returncode:
            outcome = 'refused'
            return result.returncode
        if 'manifest' not in config or 'runtime_config' not in config:
            outcome = 'refused'
            print('UNAVAILABLE: session-configuration-unavailable; game open; no test input')
            return 2
        manifest, runtime = path('manifest'), path('runtime_config')
        seed = json.loads(runtime.read_text())
        session = folder / 'session-private.json'
        outcome = 'unverified'
        result = native('tools/workbench/prepare-session.ps1', '-Manifest', windows(manifest),
                        '-Output', windows(session), '-Window', windows(output), transaction=folder)
        if result.returncode:
            outcome = 'refused'
            return result.returncode
        seed.update(session=str(session), session_sha256=digest(session))
        updated = folder / 'runtime-private.json'
        updated.write_text(json.dumps(seed, indent=2))
        # Every session is immutable; only the local workflow pointer changes.
        config['runtime_config'] = str(updated)
        temporary = config_path.with_name(config_path.name + '.' + uuid.uuid4().hex + '.tmp')
        temporary.write_text(json.dumps(config, indent=2))
        temporary.replace(config_path)
        outcome = 'completed'
        print('PASS: game open; current session prepared; gameplay still requires preflight')
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as error:
        reason = str(error) if str(error) in {'windows-runtime-unavailable', 'recovery-reconciliation-required', 'hung-termination-needs-recovery', 'native-helper-unverified', 'monitor-timeout-out-of-range', 'owned-helper-pending', 'specific-recovery-batch-required', 'recovery-observation-unavailable', 'original-session-binding-unverified'} else 'configuration-unavailable'
        print('UNAVAILABLE: ' + reason + '; no further game input')
        return 2
    finally:
        if lease:
            store.finish_runtime_operation(lease, outcome)
