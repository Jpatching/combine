param([Parameter(Mandatory=$true)][string]$Plan,[Parameter(Mandatory=$true)][string]$Output)
# One reviewed GTA IV bundle only. Closed-game replacement; originals backed up.
$ErrorActionPreference='Stop'
$written=@();$complete=$false;$rollback='not-needed'
function Hash([string]$Path){(Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Closed {if(@(Get-Process GTAIV -ErrorAction SilentlyContinue).Count){throw 'game-must-be-closed'}}
function Safe-Directory([string]$Path){
 $current=[IO.Path]::GetFullPath($Path);$volume=[IO.Path]::GetPathRoot($current).TrimEnd('\')
 while($current){
  $entry=Get-Item -LiteralPath $current
  if(!$entry.PSIsContainer -or ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'unsafe-directory'}
  if($current.TrimEnd('\') -ieq $volume){break}
  $current=[IO.Path]::GetDirectoryName($current.TrimEnd('\'))
 }
}
function Relative([string]$Value){
 if(!$Value -or [IO.Path]::IsPathRooted($Value) -or $Value -match '(^|[\\/])\.{1,2}([\\/]|$)|:'){throw 'bundle-invalid'}
 return $Value.Replace('/','\')
}
try {
 Closed
 if(Test-Path -LiteralPath $Output){throw 'existing-bundle-preserved'}
 $planData=Get-Content -LiteralPath $Plan -Raw|ConvertFrom-Json
 $inspection=Get-Content -LiteralPath $planData.inspection -Raw|ConvertFrom-Json
 $window=Get-Content -LiteralPath $planData.window_mode -Raw|ConvertFrom-Json
 $root=Split-Path -Parent $inspection.Executable
 Safe-Directory $root
 Safe-Directory (Split-Path -Parent $Output)
 $roles=@{plugin='CLEO\CLEO_PLUGINS\combine_skate.cleo';worker='CLEO\CLEO_PLUGINS\combine_skate_worker.exe';
  definitions='CLEO\.config\gta_iv.json';script='CLEO\combine_skate.js';watchdog='CLEO\combine_skate_watchdog.js';
  status_script='CLEO\combine_game_status.js';checkpoint_script='CLEO\combine_checkpoint.js';evaluation_script='CLEO\combine_evaluation.js'}
 if($planData.source_revision -cnotmatch '^[0-9a-f]{40}$' -or @($planData.items).Count -ne 8 -or
  @($planData.items.role|Select-Object -Unique).Count -ne 8){throw 'bundle-invalid'}
 $seen=@{}
 foreach($item in $planData.items){
  if($item.role -notin $roles.Keys -or $seen.ContainsKey([string]$item.role)){throw 'bundle-invalid'}
  $seen[[string]$item.role]=$true
 }
 if(@($roles.Keys|Where-Object {$_ -notin $seen.Keys}).Count){throw 'bundle-invalid'}
 $exe=Get-Item -LiteralPath $inspection.Executable
 if($exe.Name -ine 'GTAIV.exe' -or $exe.VersionInfo.FileVersion -ne '1.2.0.59' -or
  (Get-AuthenticodeSignature $exe.FullName).Status -ne 'Valid' -or (Hash $exe.FullName) -ine $window.ExecutableSha256 -or
  [Convert]::ToBase64String([IO.File]::ReadAllBytes($window.Target)) -cne $window.CandidateBase64){throw 'baseline-mismatch'}
 $hashes=@{'GTAIV.exe'=(Hash $exe.FullName)};$retained=@('GTAIV.exe')
 foreach($entry in $planData.baseline.PSObject.Properties){
  $relative=Relative $entry.Name
  if($relative -in $roles.Values -or $entry.Value -cnotmatch '^[0-9a-fA-F]{64}$'){throw 'bundle-invalid'}
  if((Hash (Join-Path $root $relative)) -ine $entry.Value){throw 'baseline-mismatch'}
  $hashes[$relative]=$entry.Value.ToLowerInvariant();$retained+=$relative
 }
 $backup=$Output+'.backups'
 if(Test-Path -LiteralPath $backup){throw 'existing-bundle-preserved'}
 $null=New-Item -ItemType Directory -Path $backup
 $items=@()
 foreach($item in $planData.items){
  if($item.role -notin $roles.Keys -or $item.sha256 -cnotmatch '^[0-9a-f]{64}$'){throw 'bundle-invalid'}
  $source=Get-Item -LiteralPath $item.source
  if($source.PSIsContainer -or ($source.Attributes -band [IO.FileAttributes]::ReparsePoint) -or (Hash $source.FullName) -cne $item.sha256){throw 'bundle-source-mismatch'}
  $relative=$roles[$item.role];$target=Join-Path $root $relative
  Safe-Directory (Split-Path -Parent $target)
  $before=Join-Path $backup $item.role;$existed=Test-Path -LiteralPath $target
  $oldHash=$null
  if($existed){
   if((Get-Item $target).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'bundle-invalid'}
   $oldHash=Hash $target;[IO.File]::WriteAllBytes($before,[IO.File]::ReadAllBytes($target))
   if((Hash $before) -cne $oldHash){throw 'backup-unverified'}
  }
  $items+=@{Relative=$relative;Source=$source.FullName;SourceHash=$item.sha256;ExpectedOld=$oldHash;Before=$before;Existed=$existed;Target=$target}
 }
 $recovery=@{Root=$root;Revision=$planData.source_revision;Items=$items;Hashes=$hashes;Retained=@($retained|Select-Object -Unique)}
 if($planData.checkpoint_token -cnotmatch '^[0-9a-f]{32}$'){throw 'bundle-invalid'}
 $recovery.CheckpointToken=$planData.checkpoint_token
 $recovery|ConvertTo-Json -Depth 10|Set-Content -LiteralPath ($Output+'.recovery-private.json') -Encoding UTF8
 foreach($item in $items){
  Closed
  Safe-Directory (Split-Path -Parent $item.Target)
  if($item.Existed -and (Hash $item.Target) -cne $item.ExpectedOld){throw 'independent-target-change'}
  if(!$item.Existed -and (Test-Path -LiteralPath $item.Target)){throw 'independent-target-change'}
  if((Hash $item.Source) -cne $item.SourceHash){throw 'bundle-source-mismatch'}
  $temporary=$item.Target+'.combine-new-'+[guid]::NewGuid().ToString('N')
  [IO.File]::WriteAllBytes($temporary,[IO.File]::ReadAllBytes($item.Source))
  if((Hash $temporary) -cne $item.SourceHash){throw 'bundle-source-mismatch'}
  Closed
  if($item.Existed){[IO.File]::Replace($temporary,$item.Target,$null)}else{[IO.File]::Move($temporary,$item.Target)}
  $written+=$item
  if((Hash $item.Target) -cne $item.SourceHash){throw 'installed-bundle-mismatch'}
 }
 Closed
 foreach($relative in $hashes.Keys){if((Hash (Join-Path $root $relative)) -cne $hashes[$relative]){throw 'baseline-mismatch'}}
 $recovery.Items=@($items|ForEach-Object {@{Relative=$_.Relative;Source=$_.Source;SourceHash=$_.SourceHash}})
 $recovery|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $Output -Encoding UTF8
 $complete=$true
 Write-Output 'PASS: reviewed closed-game bundle installed and hash verified; backups retained; gameplay untested'
}catch{
 if($written.Count -and !$complete){
  $rollback='unverified'
  try {
   Closed
   foreach($item in $written){
    Safe-Directory (Split-Path -Parent $item.Target)
    if((Hash $item.Target) -cne $item.SourceHash){throw 'independent-target-change'}
    if($item.Existed){
     if((Hash $item.Before) -cne $item.ExpectedOld){throw 'backup-unverified'}
     $temporary=$item.Target+'.combine-rollback-'+[guid]::NewGuid().ToString('N')
     [IO.File]::WriteAllBytes($temporary,[IO.File]::ReadAllBytes($item.Before))
     if((Hash $temporary) -cne $item.ExpectedOld){throw 'backup-unverified'}
     Closed
     if((Hash $item.Target) -cne $item.SourceHash){throw 'independent-target-change'}
     [IO.File]::Replace($temporary,$item.Target,$null)
     if((Hash $item.Target) -cne $item.ExpectedOld){throw 'rollback-unverified'}
    }else{[IO.File]::Delete($item.Target)}
   }
   $rollback='verified'
  }catch{}
 }
 $_|Out-String|Set-Content -LiteralPath ($Output+'.error-private.txt')
 $reason=$_.Exception.Message
 if($reason -cnotmatch '^(game-must-be-closed|existing-bundle-preserved|bundle-invalid|baseline-mismatch|bundle-source-mismatch|backup-unverified|independent-target-change|installed-bundle-mismatch|unsafe-directory)$'){$reason='bundle-stage-unavailable'}
 Write-Output ('UNAVAILABLE: '+$reason+'; rollback='+$rollback+'; preserve private backups; game not launched');exit 2
}
