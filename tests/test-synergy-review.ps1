# Synthetic adapter checks only. Does not launch a game or require game data.
param([Parameter(Mandatory=$true)][string]$WorkflowDirectory)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$root = Join-Path $env:TEMP ('synergy-review-test-' + [Guid]::NewGuid().ToString('N'))
$source = Join-Path $root 'source'
New-Item -ItemType Directory -Path $source | Out-Null
$binary = Join-Path $source 'iw4l.exe'
Copy-Item (Join-Path $env:SystemRoot 'System32/whoami.exe') $binary
$hash = (Get-FileHash $binary -Algorithm SHA256).Hash
$settings = 'PROFILE=' + $source.Replace('\','/') + "/profile`nCOMBINE_SYNERGY_GSC=0`nCOMBINE_SYNERGY_GSC_PROBE=1`nIW4L_CMDS=bad`nIW4L_CONSOLE_STDIN=1`n"
[IO.File]::WriteAllText((Join-Path $source '.env'), $settings)
$evidence = Join-Path $root 'input.json'
@{ sourceCommit=('a'*40); issue='synthetic fixture'; upstreamPins=@{runtime=('b'*40)}; patches=@{test=('c'*64)}; checks=@(@{command='fixture';result='pass'}) } | ConvertTo-Json -Depth 5 | Set-Content $evidence
$trial = Join-Path $root 'trial'; $bundle = Join-Path $root 'bundle'
& (Join-Path $repo 'scripts/prepare-trickshot-trial.ps1') -Source $source -Binary $binary -Destination $trial -ExpectedSha256 $hash -ReviewDirectory $bundle -EvidenceFile $evidence -ChecklistFile (Join-Path $repo 'templates/synergy-checklist.txt') -WorkflowDirectory $WorkflowDirectory -Synergy | Out-Null
$text = Get-Content (Join-Path $trial '.env') -Raw
if ($text.Contains($source.Replace('\','/')) -or !$text.Contains($trial.Replace('\','/') + '/profile')) { throw 'Forward-slash profile escaped isolation.' }
foreach ($expected in @('COMBINE_SYNERGY_GSC=1','COMBINE_SYNERGY_GSC_PROBE=0','IW4L_CONSOLE_STDIN=0')) { if (!$text.Contains($expected)) { throw 'Unsafe trial settings.' } }
if ($text.Contains('IW4L_CMDS=bad')) { throw 'Inherited commands survived.' }
if ((Get-Content (Join-Path $source '.env') -Raw) -ne $settings) { throw 'Source settings modified.' }
if (@(Get-ChildItem $bundle -Filter '*.lnk').Count -ne 3 -or !(Test-Path (Join-Path $bundle 'Test Synergy.lnk'))) { throw 'Synergy shortcuts absent.' }
& (Join-Path $bundle 'launch.ps1') -VerifyOnly
# Observe environment inside the wrapper without executing a process.
@'
param([switch]$VerifyOnly)
if (!$VerifyOnly -or $env:COMBINE_SYNERGY_GSC -ne '1' -or $env:COMBINE_SYNERGY_GSC_PROBE -ne '0' -or $env:IW4L_CMDS -ne ' ' -or $env:IW4L_CONSOLE_STDIN -ne '0') { throw 'Wrapper environment unsafe.' }
'@ | Set-Content (Join-Path $bundle 'verified-launch.ps1')
$old = $env:IW4L_CMDS
try {
    $env:IW4L_CMDS = 'inherited automation'
    & (Join-Path $bundle 'launch.ps1') -VerifyOnly
    if ($env:IW4L_CMDS -ne 'inherited automation') { throw 'Caller environment not restored.' }
} finally { $env:IW4L_CMDS = $old }
Write-Output 'PASS: Synergy isolation, settings sanitation, exact-build verification, shortcuts, wrapper overrides/restoration'
