#!/usr/bin/env python3
"""Check redacted runtime evidence; an asset-free fixture alone does not prove play."""
import argparse
import json
import re
from pathlib import Path

REQUIRED = (
    'hud=1 open=1 page=root',
    'hud=1 open=1 page=weapons',
    'hud=1 open=1 page=give_weapons',
    'hud=1 open=1 page=snipers',
    'owns_intervention=1 holds_intervention=1',
    'hud=1 open=0 page=root',
    'shot menu_open=0',
)
INHERITED_STATISTICS = ('maps/mp/_matchdata:10:3 in init: setmatchdatadef: unavailable: '
                        'IW4 definition schemas are not supported by the local match-data store')


def failures(report, baseline):
    messages = report.get('sourceDiagnostics', [])
    errors = []
    build = report.get('binarySha256', '')
    if (report.get('launched') is not True or report.get('synergyEnabled') is not True
            or not re.fullmatch(r'[0-9a-f]{64}', str(build))
            or not report.get('orderedStream')):
        errors.append('Missing enabled-menu build/launch/ordered-stream provenance')
    position = 0
    for required in REQUIRED:
        match = next((index for index in range(position, len(messages))
                      if required in messages[index]), None)
        if match is None:
            errors.append('Missing or out-of-order observation: ' + required)
        else:
            position = match + 1
    if any('shot menu_open=1' in message for message in messages):
        errors.append('Gameplay shot leaked while Synergy was open')
    baseline_messages = baseline.get('sourceDiagnostics', [])
    valid_baseline = (baseline.get('launched') is True
                      and baseline.get('synergyEnabled') is False
                      and baseline.get('binarySha256') == build
                      and baseline.get('exitCode') == 0
                      and not baseline.get('stoppedByDiagnostic', False)
                      and bool(baseline.get('orderedStream')))
    for message in messages:
        if message.startswith('SYNERGY_PROBE '):
            continue
        if valid_baseline and message == INHERITED_STATISTICS and message in baseline_messages:
            continue
        errors.append('New or unclassified script fault: ' + message)
    if report.get('exitCode') != 0 or report.get('stoppedByDiagnostic', False):
        errors.append('Diagnostic did not exit normally with code 0')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--baseline', type=Path, required=True)
    args = parser.parse_args()
    report, baseline = (json.loads(p.read_text(encoding='utf-8-sig'))
                        for p in (args.report, args.baseline))
    errors = failures(report, baseline)
    for error in errors:
        print('FAIL: ' + error)
    if not errors:
        print('PASS: actual Synergy hierarchy, Intervention held, no observed menu-open shot, post-close shot, normal exit')
        if INHERITED_STATISTICS in report.get('sourceDiagnostics', []):
            print('INHERITED DEBT: statistics error also observed with Synergy disabled')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
