$ErrorActionPreference='Stop'
$root=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
foreach($file in @('tools/workbench/trial.ps1','tools/workbench/runtime.psm1','tools/workbench/menu.ps1',
                  'tools/workbench/prepare-session.ps1','tools/workbench/open.ps1','tools/workbench/status.ps1',
                  'tools/workbench/stage.ps1','tools/gtaiv-collision/observe_ground.ps1')){
 $tokens=$null;$errors=$null
 $null=[System.Management.Automation.Language.Parser]::ParseFile((Join-Path $root $file),[ref]$tokens,[ref]$errors)
 if($errors.Count){throw ('PowerShell parser failure: '+$file)}
}
Import-Module (Join-Path $PSScriptRoot 'runtime.psm1') -Force
if([CombineTrialWindow]::GuardedDown([IntPtr]::Zero,0,0,64) -ne 0){throw 'Invalid owner accepted'}
$cases=@(
 @('Quit Episodes from Liberty City','offline-title-selector'),
 @('Quit Episodes from Liberty City SIGN IN','login'),
 @('START OPTIONS BACK SOCIAL CLUB','single-player-start-menu'),
 @('START OPTIONS BACK SOCIAL MULTIPLAYER','login'),
 @('Episodes from Liberty City','unknown'),
 @('LOADING','loading'),
 @('START OPTIONS BACK SOCIAL CLUB LOADING','loading'),
 @('Quit Episodes from Liberty City ONLINE','login'),
 @('Quit Episodes from Liberty City OPTIONS','unknown')
)
foreach($case in $cases){
 $actual=& (Join-Path $PSScriptRoot 'menu.ps1') -Text $case[0]
 if($actual -cne ('MENU_CLASSIFICATION='+$case[1])){throw 'Menu regression'}
}
Write-Output 'PASS: Windows helper syntax, compiled invalid-owner refusal and nine menu fixtures; no game input'
$fixture=Join-Path ([IO.Path]::GetTempPath()) ('combine-inventory-'+[guid]::NewGuid().ToString('N'))
$null=New-Item -ItemType Directory -Path $fixture
try {
 $roles=@('GTAIV.exe','CLEO\CLEO_PLUGINS\combine_skate.cleo','CLEO\CLEO_PLUGINS\combine_skate_worker.exe',
  'CLEO\.config\gta_iv.json','CLEO\combine_skate.js','CLEO\combine_skate_watchdog.js','CLEO\combine_game_status.js')
 $hashes=@{}
 foreach($relative in $roles){
  $target=Join-Path $fixture $relative
  $null=New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force
  [IO.File]::WriteAllText($target,'before')
  $hashes[$relative]=(Get-FileHash $target -Algorithm SHA256).Hash.ToLowerInvariant()
 }
 $changed='CLEO\combine_skate.js';$target=Join-Path $fixture $changed
 [IO.File]::WriteAllText($target,'reviewed-after')
 $source=Join-Path $fixture 'reviewed-source.js';[IO.File]::WriteAllText($source,'reviewed-after')
 $newHash=(Get-FileHash $source -Algorithm SHA256).Hash.ToLowerInvariant()
 $manifest=Join-Path $fixture 'manifest.json';$output=Join-Path $fixture 'inventory.json'
 $value=@{Root=$fixture;Revision=('a'*40);Hashes=$hashes;Retained=@($roles|Where-Object {$_ -ne $changed});
  Items=@(@{Relative=$changed;Source=$source;SourceHash=$newHash;ExpectedOld=$hashes[$changed]})}
 $value|ConvertTo-Json -Depth 8|Set-Content $manifest -Encoding UTF8
 $runner=Join-Path $PSHOME 'powershell.exe'
 $messages=@(& $runner -NoProfile -NonInteractive -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'prepare-session.ps1') -Manifest $manifest -Output $output -InventoryOnly)
 if($LASTEXITCODE -ne 0){throw 'Reviewed staged bytes must qualify instead of obsolete rollback hashes'}
 $actual=Get-Content $output -Raw|ConvertFrom-Json
 if(($actual.artifacts|Where-Object {$_.role -eq 'script'}).sha256 -cne $newHash){throw 'Session must pin reviewed staged bytes'}
 [IO.File]::WriteAllText($target,'independent-change')
 $messages=@(& $runner -NoProfile -NonInteractive -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'prepare-session.ps1') -Manifest $manifest -Output (Join-Path $fixture 'refused.json') -InventoryOnly)
 if($LASTEXITCODE -eq 0){throw 'Independent installed changes must refuse'}
 Write-Output 'PASS: reviewed staged inventory overrides rollback hashes; independent changes refuse'
}finally{
 # Only this newly authored temporary fixture is removed.
 Remove-Item -LiteralPath $fixture -Recurse -Force
}
