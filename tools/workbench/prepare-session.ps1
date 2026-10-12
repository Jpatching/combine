param([Parameter(Mandatory=$true)][string]$Manifest,[Parameter(Mandatory=$true)][string]$Output,[switch]$InventoryOnly,[string]$Window)
$ErrorActionPreference='Stop'
try {
 $old=Get-Content -LiteralPath $Manifest -Raw | ConvertFrom-Json
 $roles=@{executable='GTAIV.exe';plugin='CLEO\CLEO_PLUGINS\combine_skate.cleo';worker='CLEO\CLEO_PLUGINS\combine_skate_worker.exe';
  definitions='CLEO\.config\gta_iv.json';script='CLEO\combine_skate.js';watchdog='CLEO\combine_skate_watchdog.js';status_script='CLEO\combine_game_status.js'}
 $expected=@{}
 function Add-Expected([string]$Relative,[string]$Hash){
  $Relative=$Relative.Replace('/','\')
  if(!$Relative -or [IO.Path]::IsPathRooted($Relative) -or $Relative -match '(^|[\\/])\.{1,2}([\\/]|$)|:' -or $Hash -cnotmatch '^[0-9a-fA-F]{64}$'){throw 'manifest-invalid'}
  $expected[$Relative]=$Hash.ToLowerInvariant()
 }
 foreach($entry in $old.Hashes.PSObject.Properties){Add-Expected $entry.Name $entry.Value}
 $staged=@{}
 foreach($item in @($old.Items)){
  if($null -eq $item){continue}
  $relative=([string]$item.Relative).Replace('/','\')
  $retained=@($old.Retained|ForEach-Object {([string]$_).Replace('/','\')})
  if($staged.ContainsKey($relative) -or $relative -in $retained){throw 'manifest-invalid'}
  if($item.ExpectedOld -and $expected[$relative] -cne ([string]$item.ExpectedOld).ToLowerInvariant()){throw 'manifest-invalid'}
  Add-Expected $relative $item.SourceHash
  $staged[$relative]=$true
 }
 if($old.Revision -cnotmatch '^[0-9a-f]{40}$'){throw 'manifest-invalid'}
 $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
 if(!$InventoryOnly -and ($games.Count -ne 1 -or $games[0].Path -ine (Join-Path $old.Root 'GTAIV.exe'))){throw 'process-identity'}
 if($Window -and !$InventoryOnly){
  $observed=Get-Content -LiteralPath $Window -Raw|ConvertFrom-Json
  if($observed.pid -ne $games[0].Id -or $observed.start_ticks -ne $games[0].StartTime.ToUniversalTime().Ticks){throw 'process-identity'}
 }
 foreach($relative in @($expected.Keys|Sort-Object)){
  $role=@($roles.Keys|Where-Object {$roles[$_] -ieq $relative})
  $label=if($role.Count -eq 1){$role[0]}else{'retained-artifact'}
  $target=Join-Path $old.Root $relative
  if(!(Test-Path -LiteralPath $target -PathType Leaf)){throw ('inventory-missing-'+$label)}
  if((Get-Item -LiteralPath $target).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'manifest-invalid'}
  if((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -cne $expected[$relative]){throw ('inventory-mismatch-'+$label)}
 }
 $artifacts=@()
 foreach($role in $roles.Keys){
  $relative=$roles[$role];$hash=$expected[$relative]
  if(!$hash){throw 'manifest-invalid'}
  $artifacts+=@{role=$role;path=(Join-Path $old.Root $relative);sha256=$hash.ToLowerInvariant()}
 }
 foreach($optional in @(@{role='checkpoint_script';relative='CLEO\combine_checkpoint.js'},@{role='evaluation_script';relative='CLEO\combine_evaluation.js'})){
  if($expected.ContainsKey($optional.relative)){$artifacts+=@{role=$optional.role;path=(Join-Path $old.Root $optional.relative);sha256=$expected[$optional.relative]}}
 }
 $artifacts+=@{role='manifest';path=$Manifest;sha256=(Get-FileHash -LiteralPath $Manifest -Algorithm SHA256).Hash.ToLowerInvariant()}
 if($InventoryOnly){
  if(Test-Path -LiteralPath $Output){throw 'Preserve existing session'}
  @{scope='file-inventory-only';artifacts=$artifacts} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Output -Encoding UTF8
  Write-Output 'PASS: file inventory matches manifest; loaded provenance/gameplay unverified';exit 0
 }
 $start=[DateTimeOffset]$games[0].StartTime.ToUniversalTime()
 $session=@{schema_version=1;process=@{pid=$games[0].Id;start_ms=$start.ToUnixTimeMilliseconds()};
  executable=$games[0].Path;state_path=(Join-Path $env:LOCALAPPDATA 'Combine\gtaiv-status\state.json');
  log_paths=@((Join-Path $env:APPDATA 'CLEO Redux\cleo_redux.log'));artifacts=$artifacts;retained_artifacts=$artifacts;
  recorded_build_revision=$old.Revision;witnesses=@{}}
 if($old.CheckpointToken){
  if($old.CheckpointToken -cnotmatch '^[0-9a-f]{32}$'){throw 'manifest-invalid'}
  $session.checkpoint_token=$old.CheckpointToken
 }
 if(Test-Path -LiteralPath $Output){throw 'existing-session-preserved'}
 $session | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Output -Encoding UTF8
 Write-Output 'PASS: current process bound to retained inventory; no game files or input changed'
}catch{
 $reason=$_.Exception.Message
 if($reason -cnotmatch '^(manifest-invalid|process-identity|existing-session-preserved|inventory-(missing|mismatch)-(executable|plugin|worker|definitions|script|watchdog|status_script|retained-artifact))$'){$reason='session-preparation-unavailable'}
 $_|Out-String|Set-Content -LiteralPath ($Output+'.error-private.txt')
 Write-Output ('UNAVAILABLE: '+$reason+'; no runtime action');exit 2
}
