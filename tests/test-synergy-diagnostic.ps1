# Synthetic log fixtures only; no runtime/assets needed.
$ErrorActionPreference = 'Stop'
. (Join-Path (Split-Path $PSScriptRoot -Parent) 'scripts/synergy-diagnostic-log.ps1')
$lines = @(
    'SYNERGY_PROBE shot menu_open=0',
    'SYNERGY_PROBE hud=1 open=0 page=root',
    'SYNERGY_PROBE shot menu_open=0',
    'gsc: script runtime error: common_scripts/utility:10:3 in helper: unavailable: C:\Users\Example\private.txt',
    'gsc: script runtime error: non_location private detail',
    'unresolved function or unknown builtin C:\private\secret.txt'
)
$result = @(ConvertTo-SynergyDiagnostics -Lines $lines)
if ($result.Count -ne 6) { throw 'Observation/fault omitted or deduplicated.' }
if ($result[0] -ne $result[2] -or $result[1] -ne 'SYNERGY_PROBE hud=1 open=0 page=root') { throw 'Event order lost.' }
if ($result[3] -ne 'common_scripts/utility:10:3 in helper: script fault (details retained privately)') { throw 'Imported helper fault omitted.' }
if (($result -join ' ').Contains('private.txt') -or ($result -join ' ').Contains('secret.txt') -or ($result -join ' ').Contains('Example')) { throw 'Private diagnostic argument leaked.' }
Write-Output 'PASS: chronological repeated observations, imported and unclassified faults, private-argument redaction'
