# Exercise the public trial command with authored native state and logs. No game input.
$ErrorActionPreference='Stop'
$fixture=Join-Path ([IO.Path]::GetTempPath()) ('combine-trial-'+[guid]::NewGuid().ToString('N'))
$null=New-Item -ItemType Directory -Path $fixture
try {
 Copy-Item (Join-Path $PSScriptRoot 'trial.ps1') (Join-Path $fixture 'trial.ps1')
 @'
function Initialize-CombineTrial($Session,$StatusModule) {
 $script:session=Get-Content $Session -Raw|ConvertFrom-Json
 $script:acted=$false;$script:cleanup=$false;$script:observations=0;$script:mounted=$false
}
function Get-CombineTrialSnapshot([bool]$RequireUnmounted=$true,[bool]$Menu=$false) {
 $script:observations++
 if($script:session.test_case -eq 'timeout' -and $script:observations -gt 2 -and !$script:cleanup){throw 'fixture-terminal-event-missed'}
 if($script:session.test_case -eq 'failed-recovery' -and $script:cleanup){throw 'fresh-gameplay'}
 return @{Report=@{Adapter=$(if($script:mounted){'ready, mounted'}else{'ready, unmounted'})}}
}
function Invoke-CombineTrialPulse {
 $script:acted=$true
 if($script:session.test_case -eq 'mounted'){$script:mounted=!$script:mounted;return}
 $message=if($script:session.test_case -eq 'timeout'){'COMBINE_SKATE Skate: preparation timed out - GTA retained'}else{'COMBINE_SKATE native-exception'}
 Add-Content -LiteralPath $script:session.log_paths[0] -Value $message
}
function Get-CombineTrialInputOwned {return $script:acted}
function Test-CombineTrialInputReleased {$script:cleanup=$true;return $true}
function Test-CombineTrialInventory {}
Export-ModuleMember -Function *
'@ | Set-Content (Join-Path $fixture 'runtime.psm1') -Encoding UTF8
 foreach($case in @('failed-recovery','timeout','mounted')) {
  $log=Join-Path $fixture ($case+'.log');[IO.File]::WriteAllText($log,'')
  $session=Join-Path $fixture ($case+'-session.json');$output=Join-Path $fixture ($case+'-result.json')
  @{test_case=$case;log_paths=@($log)}|ConvertTo-Json|Set-Content $session -Encoding UTF8
  $messages=@(& (Join-Path $PSHOME 'powershell.exe') -NoProfile -NonInteractive -ExecutionPolicy Bypass -File (Join-Path $fixture 'trial.ps1') -Session $session -StatusModule 'authored' -Output $output -Scenario mount-diagnostic)
  $code=$LASTEXITCODE;$actual=Get-Content $output -Raw|ConvertFrom-Json
  switch($case) {
   'failed-recovery' {
    if($code -ne 3 -or $actual.reason -ne 'recovery-unverified' -or $actual.cleanup -ne 'unknown' -or
       $actual.diagnostic.verdict -ne 'failed' -or $actual.diagnostic.boundary -ne 'mount' -or
       $actual.diagnostic.reason -ne 'native-exception'){throw 'Cleanup failure must retain the original diagnostic'}
   }
   'timeout' {
    if($code -ne 2 -or $actual.verdict -ne 'failed' -or $actual.boundary -ne 'preparation' -or
       $actual.reason -ne 'preparation-timeout' -or $actual.cleanup -ne 'verified'){throw 'Preparation timeout must be observed with verified cleanup'}
   }
   'mounted' {
    if($code -ne 0 -or $actual.reason -ne 'mount-observed' -or $actual.cleanup -ne 'verified'){throw 'Observed mount must dismount and verify recovery'}
   }
  }
 }
 Write-Output 'PASS: trial command retains first failure, observes preparation timeout and verifies mounted recovery; authored fixtures only'
}finally{Remove-Item -LiteralPath $fixture -Recurse -Force}
