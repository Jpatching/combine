param(
 [Parameter(Mandatory=$true)][string]$Session,
 [Parameter(Mandatory=$true)][string]$StatusModule,
 [Parameter(Mandatory=$true)][string]$Output,
 [ValidateSet('preflight','mount-diagnostic','ground-query','offline-menus','checkpoint')][string]$Scenario='preflight',
 [string]$MenuImage
)
$ErrorActionPreference='Stop'
$result=@{verdict='refused';boundary='preflight';reason='prerequisites-unavailable';cleanup='not-needed';runtime_identity='unverified'}
$acted=$false;$mounted=$false

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
  if($Scenario -eq 'checkpoint' -and ($m.checkpoint_token -cnotmatch '^[0-9a-f]{32}$' -or 'checkpoint_script' -notin $m.artifacts.role)){throw 'checkpoint-unprepared'}
  $offsets=@{};$tails=@{}
  if(@($m.log_paths).Count -lt 1 -or @($m.log_paths).Count -gt 4){throw 'log-boundary'}
  foreach($path in $m.log_paths){$offsets[$path]=(Get-Item -LiteralPath $path).Length;$tails[$path]=''}
  if($Scenario -eq 'checkpoint'){Invoke-CombineTrialPulse 65}else{Invoke-CombineTrialPulse}
  $result.cleanup='unknown';$result.boundary=if($Scenario -eq 'checkpoint'){'checkpoint'}else{'mount'};$result.verdict='unavailable'
  $result.reason=if($Scenario -eq 'checkpoint'){'checkpoint-observer-timeout'}else{'mount-observer-timeout'}
  $timer=[Diagnostics.Stopwatch]::StartNew();$observed=$false
  while($timer.Elapsed.TotalSeconds -lt 65 -and !$observed){
   $s=Get-CombineTrialSnapshot $false ($Scenario -eq 'offline-menus')
   if($Scenario -ne 'checkpoint' -and $s.Report.Adapter -eq 'ready, mounted'){$mounted=$true;$result.verdict='passed';$result.reason='mount-observed';$observed=$true;break}
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
     }elseif($line -match 'COMBINE_SKATE native-exception'){
      $result.verdict='failed';$result.reason='native-exception';$observed=$true
     }
    }
   }
   Start-Sleep -Milliseconds 100
  }
 }
}catch{
 $result.verdict='refused';$result.reason='native-prerequisite-or-observer-refused'
 if($_.Exception.Message -in @('process-identity','foreground','windowed','fresh-gameplay','runtime-inventory',
  'runtime-identity','input-refused','input-release','stale-menu-image','unknown-offline-menu','log-boundary')){
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
   if($result.reason -in @('mount-observer-timeout','checkpoint-observer-timeout','checkpoint-recovery-unverified')){throw 'pending-preparation-unverified'}
   if($s.Report.Adapter -eq 'ready, mounted'){Invoke-CombineTrialPulse;Start-Sleep -Milliseconds 800}
   $null=Get-CombineTrialSnapshot $true ($Scenario -eq 'offline-menus');Test-CombineTrialInventory;$result.cleanup='verified'
  }catch{$result.verdict='unavailable';$result.boundary='recovery';$result.reason='recovery-unverified'}
 }
 $result | ConvertTo-Json -Compress | Set-Content -LiteralPath $Output -Encoding UTF8
}
if($result.cleanup -eq 'unknown'){exit 3}
if($result.verdict -eq 'passed'){exit 0}else{exit 2}
