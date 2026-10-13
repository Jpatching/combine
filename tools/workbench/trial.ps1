param(
 [Parameter(Mandatory=$true)][string]$Session,
 [Parameter(Mandatory=$true)][string]$StatusModule,
 [Parameter(Mandatory=$true)][string]$Output,
 [ValidateSet('preflight','mount-diagnostic','ground-query','offline-menus','checkpoint','ride-proof')][string]$Scenario='preflight',
 [string]$MenuImage
)
$ErrorActionPreference='Stop'
$result=@{verdict='refused';boundary='preflight';reason='prerequisites-unavailable';cleanup='not-needed';runtime_identity='unverified'}
$acted=$false;$mounted=$false

function Reset-CombineEvaluation {
 # Bind each observer to bytes written after its own trigger, not the mount offset.
 foreach($path in $m.log_paths){$offsets[$path]=(Get-Item -LiteralPath $path).Length;$tails[$path]=''}
 $script:evaluationLines=[Collections.Generic.List[string]]::new()
}
function Wait-CombineEvaluation([string]$Kind) {
 $timer=[Diagnostics.Stopwatch]::StartNew();$started=$Kind -eq 'restored';$terminal=$null;$settle=$null
 while($timer.Elapsed.TotalSeconds -lt 12){
  $null=Get-CombineTrialSnapshot ($Kind -ne 'ride')
  foreach($path in $m.log_paths){
   $file=Get-Item -LiteralPath $path
   if($file.Length -lt $offsets[$path] -or $file.Length-$offsets[$path] -gt 1048576){throw 'log-boundary'}
   $stream=[IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
   try{$null=$stream.Seek($offsets[$path],[IO.SeekOrigin]::Begin);$reader=[IO.StreamReader]::new($stream);$text=$reader.ReadToEnd();$offsets[$path]=$stream.Position}finally{$stream.Dispose()}
   $lines=($tails[$path]+$text).Split([char]10);$tails[$path]=$lines[-1]
   if($tails[$path].Length -gt 65536){throw 'log-boundary'}
   foreach($line in @($lines | Select-Object -SkipLast 1)){$script:evaluationLines.Add($line)}
  }
  # Consume every complete line; returning never discards the remainder of a read.
  while($script:evaluationLines.Count){
   $line=$script:evaluationLines[0];$script:evaluationLines.RemoveAt(0)
   if($line -notmatch 'COMBINE_EVALUATION '){continue}
   if($line -match 'COMBINE_EVALUATION (attempt|walking-attempt):([0-9]+) started'){
    $expected=if($Kind -eq 'ride'){'attempt'}else{'walking-attempt'}
    if($Kind -eq 'restored' -or $started -or $Matches[1] -ne $expected){throw 'evaluation-conflicting-events'}
    $started=$true;continue
   }
   if($line -match 'COMBINE_EVALUATION (UNAVAILABLE|REFUSED):'){throw 'evaluation-observation-unavailable'}
   $value=$null
   if($Kind -eq 'ride' -and $line -match 'COMBINE_EVALUATION (PASS|FAIL): real-input movement=(true|false), left-heading=(positive|negative|unchanged), right-heading=(positive|negative|unchanged), finite-active-camera-moved=(true|false); scale/orientation acceptance unverified'){
    $value=$Matches[1] -eq 'PASS' -and $Matches[2] -eq 'true' -and $Matches[5] -eq 'true' -and (($Matches[3] -eq 'positive' -and $Matches[4] -eq 'negative') -or ($Matches[3] -eq 'negative' -and $Matches[4] -eq 'positive'))
   }elseif($Kind -eq 'restored' -and $line -match 'COMBINE_EVALUATION (PASS|FAIL): native GTA control and owned camera destruction after ride'){$value=$Matches[1] -eq 'PASS'}
   elseif($Kind -eq 'walking' -and $line -match 'COMBINE_EVALUATION (PASS|FAIL): ordinary walking displacement after restoration'){$value=$Matches[1] -eq 'PASS'}
   elseif($line -match 'COMBINE_EVALUATION (PASS|FAIL):'){throw 'evaluation-conflicting-events'}
   if($null -ne $value){
    if(!$started){throw 'evaluation-uncorrelated-event'}
    if($null -ne $terminal){throw 'evaluation-conflicting-events'}
    $terminal=$value;$settle=[Diagnostics.Stopwatch]::StartNew()
   }
  }
  # Observe a short quiet interval so duplicate/conflicting terminal lines refuse.
  if($null -ne $terminal -and $settle.Elapsed.TotalMilliseconds -ge 250){return $terminal}
  Start-Sleep -Milliseconds 100
 }
 throw 'evaluation-observer-timeout'
}

try {
 Import-Module (Join-Path $PSScriptRoot 'runtime.psm1') -Force
 Initialize-CombineTrial $Session $StatusModule
 $m=Get-Content -LiteralPath $Session -Raw | ConvertFrom-Json
 $s=Get-CombineTrialSnapshot $true ($Scenario -eq 'offline-menus')
 $result.runtime_identity='manifest-matched-before-input'
 if($Scenario -eq 'offline-menus'){
  if(!$MenuImage -or (Get-Item -LiteralPath $MenuImage).LastWriteTimeUtc -lt ([DateTime]::UtcNow).AddSeconds(-15)){throw 'stale-menu-image'}
  $category=& (Join-Path $PSScriptRoot 'menu.ps1') -Image $MenuImage
  if(@($category).Count -ne 1 -or $category -notin @('MENU_CLASSIFICATION=offline-title-selector','MENU_CLASSIFICATION=single-player-start-menu') -or
     (Get-Item -LiteralPath $MenuImage).LastWriteTimeUtc -lt ([DateTime]::UtcNow).AddSeconds(-15)){throw 'unknown-offline-menu'}
  Invoke-CombineTrialPulse 28 $true
  $result.verdict='passed';$result.reason='recognized-offline-menu-input-delivered';$result.boundary='offline-menu'
 }elseif($Scenario -eq 'preflight'){$result.verdict='passed';$result.reason='fresh-windowed-foreground-unmounted-gameplay'}
 else {
  if($Scenario -eq 'ride-proof' -and 'evaluation_script' -notin $m.artifacts.role){throw 'evaluation-unprepared'}
  if($Scenario -eq 'checkpoint' -and ($m.checkpoint_token -cnotmatch '^[0-9a-f]{32}$' -or 'checkpoint_script' -notin $m.artifacts.role)){throw 'checkpoint-unprepared'}
  $offsets=@{};$tails=@{}
  if(@($m.log_paths).Count -lt 1 -or @($m.log_paths).Count -gt 4){throw 'log-boundary'}
  foreach($path in $m.log_paths){$offsets[$path]=(Get-Item -LiteralPath $path).Length;$tails[$path]=''}
  $mountTimer=[Diagnostics.Stopwatch]::StartNew()
  if($Scenario -eq 'checkpoint'){Invoke-CombineTrialPulse 65}else{Invoke-CombineTrialPulse}
  $result.cleanup='unknown';$result.boundary=if($Scenario -eq 'checkpoint'){'checkpoint'}else{'mount'};$result.verdict='unavailable'
  $result.reason=if($Scenario -eq 'checkpoint'){'checkpoint-observer-timeout'}else{'mount-observer-timeout'}
  $timer=[Diagnostics.Stopwatch]::StartNew();$observed=$false
  while($timer.Elapsed.TotalSeconds -lt 65 -and !$observed){
   $s=Get-CombineTrialSnapshot $false ($Scenario -eq 'offline-menus')
   if($Scenario -ne 'checkpoint' -and $s.Report.Adapter -eq 'ready, mounted'){
    # Request-to-observation upper bound: includes F6 delivery and status polling,
    # excludes launch, recording setup and subsequent riding/dismount cleanup.
    $result.mount_observation_ms=[Math]::Round($mountTimer.Elapsed.TotalMilliseconds,1)
    $mounted=$true;$result.verdict='passed';$result.reason='mount-observed';$observed=$true;break
   }
   foreach($path in $m.log_paths){
    $file=Get-Item -LiteralPath $path
    if($file.Length -lt $offsets[$path] -or $file.Length-$offsets[$path] -gt 1048576){throw 'log-boundary'}
    $stream=[IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
    try{$null=$stream.Seek($offsets[$path],[IO.SeekOrigin]::Begin);$reader=[IO.StreamReader]::new($stream);$text=$reader.ReadToEnd();$offsets[$path]=$stream.Position}finally{$stream.Dispose()}
    $lines=($tails[$path]+$text).Split([char]10);$tails[$path]=$lines[-1]
    if($tails[$path].Length -gt 65536){throw 'log-boundary'}
    foreach($line in @($lines | Select-Object -SkipLast 1)){
     if($Scenario -eq 'checkpoint'){
      $prefix='COMBINE_CHECKPOINT '+$m.checkpoint_token+' PRIVATE '
      $index=$line.IndexOf($prefix,[StringComparison]::Ordinal)
      if($index -ge 0){
       $raw=$line.Substring($index+$prefix.Length).Trim()
       if($raw.EndsWith('"')){$raw=$raw.Substring(0,$raw.Length-1)}
       try{$event=$raw | ConvertFrom-Json}catch{$event=('"'+$raw+'"') | ConvertFrom-Json | ConvertFrom-Json}
       if($event.event -eq 'reached'){$result.verdict='passed';$result.reason='checkpoint-position-observed-ground-unqualified'}
       elseif($event.event -in @('restored','refused')){$result.verdict='failed';$result.reason='checkpoint-unavailable'}
       else{$result.verdict='unavailable';$result.reason='checkpoint-recovery-unverified'}
       $observed=$true
      }
      continue
     }
     if($line -match 'COMBINE_SKATE surface-refused:(non-finite|near-zero|over-0.05-metres|vertex-rejection)'){
      $result.verdict='failed';$result.boundary='ground-query';$result.reason=$Matches[1];$observed=$true
     }elseif($line -match 'COMBINE_SKATE Skate: ground unavailable/ambiguous'){
      $result.verdict='inconclusive';$result.boundary='ground-query';$result.reason='centre-ground-unavailable';$observed=$true
     }elseif($line -match 'COMBINE_SKATE Skate: preparation (timed out|failed|cancelled|floor changed)'){
      $reason=@{'timed out'='preparation-timeout';'failed'='preparation-failed';'cancelled'='preparation-cancelled';'floor changed'='preparation-floor-changed'}[$Matches[1]]
      $result.verdict=if($Matches[1] -in @('cancelled','floor changed')){'inconclusive'}else{'failed'}
      $result.boundary='preparation';$result.reason=$reason;$observed=$true
     }elseif($line -match 'COMBINE_SKATE Skate: (initialization/controller unavailable|invalid initial pose|qualified floor unavailable|camera unavailable)'){
      $result.verdict='failed';$result.reason=@{'initialization/controller unavailable'='initialization-unavailable';'invalid initial pose'='invalid-initial-pose';'qualified floor unavailable'='qualified-floor-unavailable';'camera unavailable'='camera-unavailable'}[$Matches[1]];$observed=$true
     }elseif($line -match 'COMBINE_SKATE native-exception'){
      $result.verdict='failed';$result.reason='native-exception';$observed=$true
     }
     if($observed){break}
    }
    if($observed){break}
   }
   Start-Sleep -Milliseconds 100
  }
  if($Scenario -eq 'ride-proof' -and $mounted){
   $result.boundary='ride';$result.verdict='unavailable';$result.reason='ride-observer-unavailable'
   Reset-CombineEvaluation
   Invoke-CombineTrialPulse 66
   $ride=Wait-CombineEvaluation 'ride'
   $result.verdict=if($ride){'passed'}else{'failed'};$result.reason=if($ride){'ride-input-observed'}else{'ride-evaluation-failed'}
   Reset-CombineEvaluation
   Invoke-CombineTrialPulse
   $restored=Wait-CombineEvaluation 'restored'
   if(!$restored){throw 'restoration-observation-failed'}
   $null=Get-CombineTrialSnapshot $true
   Reset-CombineEvaluation
   Invoke-CombineTrialWalking
   $walk=Wait-CombineEvaluation 'walking'
   if(!$walk){throw 'walking-observation-failed'}
   if($ride){$result.reason='ride-proof-observed'}
  }
 }
}catch{
 if($result.reason -eq 'ride-evaluation-failed'){$result.diagnostic=@{verdict=$result.verdict;boundary=$result.boundary;reason=$result.reason}}
 $result.verdict='refused';$result.reason='native-prerequisite-or-observer-refused'
 if($_.Exception.Message -in @('process-identity','foreground','windowed','fresh-gameplay','runtime-inventory',
  'evaluation-unprepared','evaluation-conflicting-events','evaluation-uncorrelated-event','evaluation-observation-unavailable','evaluation-observer-timeout','restoration-observation-failed','walking-observation-failed','runtime-identity','input-refused','input-release','stale-menu-image','unknown-offline-menu','log-boundary')){
  $result.reason=$_.Exception.Message
 }
 $_ | Out-String | Set-Content -LiteralPath ($Output+'.error-private.txt')
}finally{
 if((Get-Command Get-CombineTrialInputOwned -ErrorAction SilentlyContinue) -and (Get-CombineTrialInputOwned)){
  $result.cleanup='unknown'
  try{
   if(!(Test-CombineTrialInputReleased)){throw 'owned-key-release-unverified'}
   $s=Get-CombineTrialSnapshot $false ($Scenario -eq 'offline-menus')
   # Mounted or still preparing must be cancelled through the guarded F6 boundary.
   if($result.reason -in @('mount-observer-timeout','checkpoint-observer-timeout','checkpoint-recovery-unverified','evaluation-observer-timeout','evaluation-observation-unavailable','evaluation-conflicting-events','evaluation-uncorrelated-event','ride-observer-unavailable')){throw 'pending-preparation-unverified'}
   if($s.Report.Adapter -eq 'ready, mounted'){Invoke-CombineTrialPulse;Start-Sleep -Milliseconds 800}
   $null=Get-CombineTrialSnapshot $true ($Scenario -eq 'offline-menus');Test-CombineTrialInventory;$result.cleanup='verified'
  }catch{
   if(!$result.diagnostic){$result.diagnostic=@{verdict=$result.verdict;boundary=$result.boundary;reason=$result.reason}}
   $result.verdict='unavailable';$result.boundary='recovery';$result.reason='recovery-unverified'
  }
 }
 $result | ConvertTo-Json -Compress | Set-Content -LiteralPath $Output -Encoding UTF8
}
if($result.cleanup -eq 'unknown'){exit 3}
if($result.verdict -eq 'passed'){exit 0}else{exit 2}
