"""Bounded runner over reviewed native diagnostic interfaces; never a shell queue."""
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import time
import uuid

from evidence_store import digest, now

ROOT = Path(__file__).resolve().parents[1]


def attempt(store, scenario, config_path):
    result = {'scenario': scenario, 'verdict': 'refused', 'boundary': 'configuration',
              'reason': 'runtime-configuration-unavailable', 'cleanup': 'not-needed',
              'started_at': now(), 'source_revision': 'unverified', 'runtime_identity': 'unverified',
              'changed_variable': 'same-session diagnostic', 'limitations': 'No ground qualification or riding acceptance',
              'mode': 'live', 'media': []}
    folder = store.root / 'runs' / str(uuid.uuid4())
    folder.mkdir(parents=True, mode=0o700)
    process = None
    capture = None
    try:
        config = json.loads(Path(config_path).read_text()) if config_path else {}
        checkout = Path(config['source_checkout'])
        source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
        if source != config['source_revision'] or subprocess.check_output(['git', 'status', '--porcelain'], cwd=checkout, text=True).strip():
            raise ValueError('source-mismatch')
        result['source_revision'] = source
        result['controller_revision'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        session = Path(config['session'])
        if digest(session) != config['session_sha256']: raise ValueError('session-mismatch')
        runtime = json.loads(session.read_text(encoding='utf-8-sig'))
        build = runtime['recorded_build_revision']
        if not isinstance(build, str) or not re.fullmatch(r'[0-9a-f]{40}', build): raise ValueError('build-provenance-unavailable')
        changed = subprocess.check_output(['git', 'diff', '--name-only', build, source, '--', 'tools/gtaiv-skate'], cwd=checkout, text=True).splitlines()
        if any('/tests/' not in name and not name.endswith('/README.md') and not name.endswith('/check.py') for name in changed):
            raise ValueError('runtime-source-relationship-unverified')
        identity = 'build=' + build + '; session-sha256=' + config['session_sha256']
        result['changed_variable'] = config.get('changed_variable', 'same-session diagnostic')
        if not (os.name == 'nt' or os.environ.get('WSL_DISTRO_NAME')):
            result.update(boundary='preflight', reason='windows-runtime-unavailable'); return result
        ps = 'powershell.exe' if os.name != 'nt' else 'powershell'
        def win(path):
            if os.name == 'nt': return str(path)
            return subprocess.check_output(['wslpath', '-w', str(Path(path).resolve())], text=True).strip()
        driver = ROOT / 'tools/workbench/trial.ps1'
        command = [ps, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', win(driver),
                   '-Session', win(session), '-StatusModule', win(checkout / 'tools/gtaiv-skate/game-status.psm1'),
                   '-Output', win(folder / 'native-result.json'), '-Scenario', scenario]
        if scenario == 'ground-query':
            command = [sys.executable, str(ROOT / 'tools/gtaiv-collision/collect_ground.py'),
                       '--checkpoints', config['checkpoints'], '--session', str(session),
                       '--output', str(folder / 'collection')]
        result.update(boundary='preflight', reason='native-runner-unavailable', cleanup='unknown')
        if scenario in {'mount-diagnostic', 'offline-menus', 'checkpoint'}:
            # Capture must start before the native driver can send input.
            from gta_capture import Capture
            capture = Capture(folder)
            capture.start()
        if scenario == 'offline-menus':
            from gta_capture import screenshot
            screenshot(folder / 'menu-private.png')
            command.extend(['-MenuImage', win(folder / 'menu-private.png')])
        with (folder / 'runner-private.log').open('w') as log:
            process = subprocess.Popen(command, stdout=log, stderr=log, text=True)
            try: process.wait(timeout=100)
            except subprocess.TimeoutExpired:
                # Never terminate a child that may own a key or race its recovery.
                (folder / 'pending-child-private.json').write_text(json.dumps({'pid': process.pid, 'started_at': now()}))
                result.update(verdict='unavailable', boundary='recovery', reason='owned-child-pending', cleanup='unknown')
                return result
        if scenario == 'ground-query':
            report = json.loads((folder / 'collection/result-private.json').read_text())['report']
            result.update(verdict={'agreement': 'passed', 'disagreement': 'failed'}.get(report['verdict'], 'inconclusive'),
                          boundary='ground-query', reason=report.get('reason', report['verdict']),
                          cleanup=report['restoration'], runtime_identity=identity)
        else:
            native = json.loads((folder / 'native-result.json').read_text(encoding='utf-8-sig'))
            result.update({k: native[k] for k in ('verdict', 'boundary', 'reason', 'cleanup', 'runtime_identity')})
            if 'diagnostic' in native:
                result['diagnostic'] = native['diagnostic']
            result['runtime_identity'] = identity + '; ' + native['runtime_identity']
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        # Full diagnostics remain private; the browser receives fixed labels only.
        if process is None:
            result.update(boundary='configuration', reason='runtime-configuration-unavailable', cleanup='not-needed')
    finally:
        if capture:
            try:
                video = capture.stop()
                result['media'] = [str(video)]
            except (OSError, ValueError, subprocess.SubprocessError, RuntimeError, SystemExit):
                result['limitations'] += '; video verification unavailable'
                if result['verdict'] == 'passed': result['verdict'] = 'inconclusive'
        result['finished_at'] = now()
        (folder / 'result-private.json').write_text(json.dumps(result, indent=2))
    return result


def work(store, config_path=None, once=False, authored=None):
    fixtures = iter(authored) if authored is not None else None
    while True:
        batch = store.claim()
        if batch:
            previous = None; duplicates = 0; status = 'completed'; reason = 'bounded-batch-complete'
            try:
                for _ in range(batch['requested']):
                    if store.stopped(batch): status, reason = 'stopped', 'owner-stop'; break
                    try: experiment = digest(config_path) if config_path else 'missing-configuration'
                    except OSError: experiment = 'configuration-unavailable'
                    if fixtures is not None: experiment = 'authored:' + json.dumps(authored, sort_keys=True)
                    if store.scenario_stopped(batch['scenario'], experiment):
                        status, reason = 'stopped', 'unchanged-failure-needs-new-experiment'; break
                    if fixtures is None:
                        result = attempt(store, batch['scenario'], config_path)
                    else:
                        result = dict(next(fixtures))
                        result.update(scenario=batch['scenario'], mode='authored',
                                      limitations='Authored runner fixture; no runtime evidence', media=[])
                    result['experiment'] = experiment
                    store.add_attempt(result, batch)
                    signature = (result['verdict'], result['boundary'], result['reason'], result['changed_variable'])
                    duplicates = duplicates + 1 if signature == previous else 1
                    previous = signature
                    if result['cleanup'] not in {'verified', 'not-needed'}:
                        status, reason = 'blocked-recovery', 'recovery-unverified'; break
                    if result['boundary'] == 'configuration' or result['verdict'] == 'refused':
                        status, reason = 'stopped', result['reason']; break
                    if result['verdict'] != 'passed' and duplicates >= 2:
                        status, reason = 'stopped', 'unchanged-failure-needs-new-experiment'; break
            except BaseException:
                status, reason = 'blocked-recovery', 'runner-interrupted'
                raise
            finally:
                store.finish(batch, status, reason)
        if once: return
        time.sleep(1)
