# Exercise the public trial command with authored native state and logs. No game input.
$ErrorActionPreference='Stop'
$fixture=Join-Path ([IO.Path]::GetTempPath()) ('combine-trial-'+[guid]::NewGuid().ToString('N'))
$null=New-Item -ItemType Directory -Path $fixture
try {
 # Run the actual exported recovery-key check against an authored OS sampler.
 $source=Get-Content (Join-Path $PSScriptRoot 'runtime.psm1') -Raw
 $check=[regex]::Match($source,'(?s)function Test-CombineTrialNoHeldKeys \{.*?(?=function Get-CombineTrialInputOwned)').Value
 if(!$check){throw 'Recovery-key public check unavailable'}
 $sampler=Join-Path $fixture 'key-sampler.ps1'
 $body=@'
param([int]$HeldKey)
Add-Type 'public static class CombineTrialWindow { public static int Held; public static short GetAsyncKeyState(int vk) {return vk == Held ? (short)-32768 : (short)0;} }'
[CombineTrialWindow]::Held=$HeldKey
$script:acted=$false;$script:released=$true
'@
 ($body+[Environment]::NewLine+$check+[Environment]::NewLine+'try{Test-CombineTrialNoHeldKeys;exit 0}catch{exit 2}')|Set-Content $sampler -Encoding UTF8
 foreach($held in @(0,0x0D,0x57,0x75,0x76,0x77,0x78)){
  & (Join-Path $PSHOME 'powershell.exe') -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $sampler -HeldKey $held
  if(($held -eq 0 -and $LASTEXITCODE -ne 0) -or ($held -ne 0 -and $LASTEXITCODE -ne 2)){throw 'Every owned key including Enter must refuse reconciliation while held'}
 }
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
function Invoke-CombineTrialPulse([int]$Scan=64) {
 if($Scan -eq 66){if($script:session.test_case -ne 'ride-uncorrelated'){Add-Content $script:session.log_paths[0] 'COMBINE_EVALUATION attempt:1 started'};if($script:session.test_case -eq 'ride-conflicting'){Add-Content $script:session.log_paths[0] 'COMBINE_EVALUATION PASS: real-input movement=true, left-heading=positive, right-heading=negative, finite-active-camera-moved=true; scale/orientation acceptance unverified'};Add-Content $script:session.log_paths[0] $(if($script:session.test_case -eq 'ride-pass'){'COMBINE_EVALUATION PASS: real-input movement=true, left-heading=positive, right-heading=negative, finite-active-camera-moved=true; scale/orientation acceptance unverified'}else{'COMBINE_EVALUATION FAIL: real-input movement=false, left-heading=unchanged, right-heading=unchanged, finite-active-camera-moved=false; scale/orientation acceptance unverified'});return}
 if($Scan -eq 67){Add-Content $script:session.log_paths[0] 'COMBINE_EVALUATION walking-attempt:2 started';Add-Content $script:session.log_paths[0] 'COMBINE_EVALUATION PASS: ordinary walking displacement after restoration';return}
 $script:acted=$true
 if($script:session.test_case -in @('mounted','ride-pass','ride-fail','ride-stale-pass','ride-conflicting','ride-uncorrelated')){$script:mounted=!$script:mounted;if($script:mounted -and $script:session.test_case -eq 'ride-stale-pass'){Add-Content $script:session.log_paths[0] 'COMBINE_EVALUATION PASS: real-input movement=true, left-heading=positive, right-heading=negative, finite-active-camera-moved=true; scale/orientation acceptance unverified'};if(!$script:mounted){Add-Content $script:session.log_paths[0] 'COMBINE_EVALUATION PASS: native GTA control and owned camera destruction after ride'};return}
 $message=if($script:session.test_case -eq 'timeout'){'COMBINE_SKATE Skate: preparation timed out - GTA retained'}else{'COMBINE_SKATE native-exception'}
 Add-Content -LiteralPath $script:session.log_paths[0] -Value $message
}
function Invoke-CombineTrialWalking {Invoke-CombineTrialPulse 67}
function Get-CombineTrialInputOwned {return $script:acted}
function Test-CombineTrialInputReleased {$script:cleanup=$true;return $true}
function Test-CombineTrialInventory {}
Export-ModuleMember -Function *
'@ | Set-Content (Join-Path $fixture 'runtime.psm1') -Encoding UTF8
 foreach($case in @('failed-recovery','timeout','mounted','ride-pass','ride-fail','ride-stale-pass','ride-conflicting','ride-uncorrelated')) {
  $log=Join-Path $fixture ($case+'.log');[IO.File]::WriteAllText($log,'')
  $session=Join-Path $fixture ($case+'-session.json');$output=Join-Path $fixture ($case+'-result.json')
  @{test_case=$case;log_paths=@($log);artifacts=@(@{role='evaluation_script'})}|ConvertTo-Json|Set-Content $session -Encoding UTF8
  $messages=@(& (Join-Path $PSHOME 'powershell.exe') -NoProfile -NonInteractive -ExecutionPolicy Bypass -File (Join-Path $fixture 'trial.ps1') -Session $session -StatusModule 'authored' -Output $output -Scenario $(if($case -like 'ride-*'){'ride-proof'}else{'mount-diagnostic'}))
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
   'ride-pass' {
    if($code -ne 0 -or $actual.reason -ne 'ride-proof-observed' -or $actual.cleanup -ne 'verified'){throw 'Ride proof must verify movement, both steering directions, camera and walking recovery'}
   }
   'ride-conflicting' {
    if($code -ne 3 -or $actual.reason -ne 'recovery-unverified' -or $actual.diagnostic.reason -ne 'evaluation-conflicting-events'){throw 'Conflicting evaluation verdicts must retain a classified refusal and block recovery'}
   }
   'ride-uncorrelated' {
    if($code -ne 3 -or $actual.reason -ne 'recovery-unverified' -or $actual.diagnostic.reason -ne 'evaluation-uncorrelated-event'){throw 'Uncorrelated verdicts must not pass'}
   }
   'ride-stale-pass' {
    if($code -ne 2 -or $actual.reason -ne 'ride-evaluation-failed' -or $actual.cleanup -ne 'verified'){throw 'Old PASS before F8 must not mask current FAIL'}
   }
   'ride-fail' {
    if($code -ne 2 -or $actual.reason -ne 'ride-evaluation-failed' -or $actual.boundary -ne 'ride' -or $actual.cleanup -ne 'verified'){throw 'Ride failure must survive successful recovery'}
   }
   'mounted' {
    if($code -ne 0 -or $actual.reason -ne 'mount-observed' -or $actual.cleanup -ne 'verified'){throw 'Observed mount must dismount and verify recovery'}
   }
  }
 }
 Write-Output 'PASS: trial command observes mount, preparation timeout, complete ride and failed ride with verified recovery; authored fixtures only'
}finally{Remove-Item -LiteralPath $fixture -Recurse -Force}
