$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\game-status.psm1') -Force
function Assert($Condition,[string]$Message) {if(!$Condition){throw $Message}}
$snapshot=@{schema=1;pid=42;process_start_ms=10000;updated_ms=20000;scene='cutscene';player_control=$false;on_foot=$false;adapter_ready=$true;mounted=$false;controller=$true}
$report=ConvertTo-CombineGameReport -Snapshot ([pscustomobject]$snapshot) -ExpectedProcessId 42 -ExpectedStartTime ([DateTimeOffset]::FromUnixTimeMilliseconds(10000)) -NowMs 20500
Assert ($report.Scene -eq 'cutscene' -and !$report.CanTest -and $report.PlayerControl -eq 'disabled') 'Cutscene must block gameplay input'
Write-Output 'PASS: cutscene state blocks runtime test input'
$snapshot.scene='gameplay';$snapshot.player_control=$true;$snapshot.on_foot=$true
$report=ConvertTo-CombineGameReport -Snapshot ([pscustomobject]$snapshot) -ExpectedProcessId 42 -ExpectedStartTime ([DateTimeOffset]::FromUnixTimeMilliseconds(10000)) -NowMs 20500
Assert ($report.CanTest -and $report.CurrentTest -eq 'ready for mount test') 'Fresh controllable gameplay must permit the mount test'
$snapshot.mounted=$true;$snapshot.player_control=$false
$report=ConvertTo-CombineGameReport -Snapshot ([pscustomobject]$snapshot) -ExpectedProcessId 42 -ExpectedStartTime ([DateTimeOffset]::FromUnixTimeMilliseconds(10000)) -NowMs 20500
Assert ($report.CanTest -and $report.Adapter -eq 'ready, mounted') 'Skate ownership must not be confused with an uncontrolled cutscene'
Write-Output 'PASS: playable GTA and mounted Skate states permit relevant runtime tests'
foreach($case in @('stale','future','otherProcess','restart','invalidBoolean','privateField','paused','controllerMissing','notOnFoot','unknown','malformedScene')) {
    $test=@{};foreach($entry in $snapshot.GetEnumerator()){$test[$entry.Key]=$entry.Value}
    switch($case) {
        stale {$test.updated_ms=18000}
        future {$test.updated_ms=22000}
        otherProcess {$test.pid=99}
        restart {$test.process_start_ms=9999}
        invalidBoolean {$test.controller='true'}
        privateField {$test.private_log='SYNTHETIC PRIVATE CONTENT MUST NOT ESCAPE'}
        paused {$test.scene='paused'}
        controllerMissing {$test.controller=$false}
        notOnFoot {$test.on_foot=$false}
        unknown {$test.scene='unknown'}
        malformedScene {$test.scene='SYNTHETIC PRIVATE CONTENT MUST NOT ESCAPE'}
    }
    $report=ConvertTo-CombineGameReport -Snapshot ([pscustomobject]$test) -ExpectedProcessId 42 -ExpectedStartTime ([DateTimeOffset]::FromUnixTimeMilliseconds(10000)) -NowMs 20500
    Assert (!$report.CanTest) ($case+' must prevent runtime test input')
    Assert (($report | ConvertTo-Json -Compress) -notmatch 'SYNTHETIC PRIVATE') 'Untrusted payload leaked through report'
}
Write-Output 'PASS: stale, restarted, invalid and unsafe states fail closed without echoing private data'
$cli=Join-Path $PSScriptRoot '..\game-status.ps1'
$missing=Join-Path ([IO.Path]::GetTempPath()) ('combine-status-missing-'+[guid]::NewGuid().ToString('N')+'.json')
$runner=Join-Path $PSHOME 'powershell.exe'
$lines=@(& $runner -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $cli -StatePath $missing -WaitPlayable -TimeoutSeconds 1)
Assert ($LASTEXITCODE -eq 2) 'Missing status must time out with exit 2'
Assert ($lines.Count -eq 5) 'Unchanged waiting state must print only once'
Assert (($lines -join "`n") -notmatch 'combine-status-missing') 'Private path must not appear in output'
Write-Output 'PASS: public wait command blocks missing state, prints changes only and keeps paths private'
$boundary=@{};foreach($entry in $snapshot.GetEnumerator()){$boundary[$entry.Key]=$entry.Value}
$boundary.process_start_ms=[long]1790582400000;$boundary.updated_ms=[long]1790582401000
$start=[DateTimeOffset][DateTime]::FromFileTimeUtc([long]134350560000009999)
$report=ConvertTo-CombineGameReport -Snapshot ([pscustomobject]$boundary) -ExpectedProcessId 42 -ExpectedStartTime $start -NowMs 1790582401500
Assert ($report.CanTest) 'Exact process timestamp near a millisecond boundary must not reject its own snapshot'
Write-Output 'PASS: process identity preserves exact timestamp boundaries'
# The deliberately failing child command must not become the CI runner's exit code.
exit 0
