# Prepare an isolated local trial; no downloads, game-file edits or forced exits.
param(
    [Parameter(Mandatory=$true)][string]$Source,
    [Parameter(Mandatory=$true)][string]$Binary,
    [Parameter(Mandatory=$true)][string]$Destination,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-fA-F]{64}$')][string]$ExpectedSha256,
    [string]$ReviewDirectory,
    [string]$EvidenceFile,
    [string]$ChecklistFile,
    [string]$WorkflowDirectory,
    [switch]$Synergy,
    [switch]$Launch
)
$ErrorActionPreference = 'Stop'
if ($ReviewDirectory) {
    if (!$EvidenceFile -or !$ChecklistFile -or !$WorkflowDirectory) { throw 'Review preparation requires evidence, checklist and shared workflow directory.' }
    if (Test-Path -LiteralPath $ReviewDirectory) { throw 'Review destination exists; refusing to overwrite.' }
    foreach ($path in @($EvidenceFile, $ChecklistFile, (Join-Path $WorkflowDirectory 'review-bundle.ps1'), (Join-Path $WorkflowDirectory 'review-launch.ps1'))) {
        if (!(Test-Path -LiteralPath $path -PathType Leaf)) { throw 'Required review input missing.' }
    }
}
if ($Launch -and !$ReviewDirectory) { throw 'Launch requires a verified review bundle.' }
$Source = (Resolve-Path -LiteralPath $Source).Path.TrimEnd('\')
$Binary = (Resolve-Path -LiteralPath $Binary).Path
$Destination = [IO.Path]::GetFullPath($Destination).TrimEnd('\')
if (Test-Path -LiteralPath $Destination) { throw 'Destination exists; refusing to overwrite a trial.' }
if ($Destination.StartsWith($Source + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Destination must be outside the source.' }
if (!(Test-Path -LiteralPath (Join-Path $Source 'iw4l.exe'))) { throw 'Source is not a prepared runtime.' }
if (!(Test-Path -LiteralPath (Join-Path $Source '.env'))) { throw 'Prepared source settings missing.' }
if ((Get-FileHash -LiteralPath $Binary -Algorithm SHA256).Hash -ne $ExpectedSha256) { throw 'Build hash mismatch.' }
if ($Launch -and (Get-Process iw4l -ErrorAction SilentlyContinue)) { throw 'Close the existing game before launching another trial.' }
$originalHash = (Get-FileHash -LiteralPath (Join-Path $Source 'iw4l.exe') -Algorithm SHA256).Hash
New-Item -ItemType Directory -Path $Destination | Out-Null
# Exclude recordings and diagnostic artifacts; all copied settings stay local.
& robocopy $Source $Destination /E /XJ /XD iw4l-artifacts recordings OBS /XF *.log *.mp4 *.mkv *.iw4ldemo /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -gt 7) { throw "Runtime copy failed: $LASTEXITCODE. Incomplete trial retained." }
Copy-Item -LiteralPath $Binary -Destination (Join-Path $Destination 'iw4l.exe') -Force
$settingsPath = Join-Path $Destination '.env'
$settings = Get-Content -LiteralPath $settingsPath -Raw
$settings = $settings.Replace($Source.Replace('\','/'), $Destination.Replace('\','/')).Replace($Source, $Destination)
if ($settings.Contains($Source) -or $settings.Contains($Source.Replace('\','/'))) { throw 'Old runtime path remains.' }
if ($Synergy) {
    # Remove inherited automation settings. Explicit zero avoids dotenv fallback.
    $settings = [regex]::Replace($settings, '(?m)^\s*(?:export\s+)?(?:COMBINE_SYNERGY_GSC|COMBINE_SYNERGY_GSC_PROBE|IW4L_CMDS|IW4L_CONSOLE_STDIN)\s*=.*(?:\r?\n|$)', '')
    $settings += "`r`nCOMBINE_SYNERGY_GSC=1`r`nCOMBINE_SYNERGY_GSC_PROBE=0`r`nIW4L_CMDS=`r`nIW4L_CONSOLE_STDIN=0`r`n"
}
[IO.File]::WriteAllText($settingsPath, $settings, (New-Object Text.UTF8Encoding($false)))
if ((Get-FileHash -LiteralPath (Join-Path $Source 'iw4l.exe') -Algorithm SHA256).Hash -ne $originalHash) { throw 'Source executable changed.' }
if ((Get-FileHash -LiteralPath (Join-Path $Destination 'iw4l.exe') -Algorithm SHA256).Hash -ne $ExpectedSha256) { throw 'Deployed hash mismatch.' }
if ($ReviewDirectory) {
    . (Join-Path $WorkflowDirectory 'review-bundle.ps1')
    New-ReviewBundle -Destination $ReviewDirectory -Executable (Join-Path $Destination 'iw4l.exe') `
        -ExpectedSha256 $ExpectedSha256 -EvidenceFile $EvidenceFile -ChecklistFile $ChecklistFile `
        -LaunchLabel $(if ($Synergy) { 'Test Synergy' } else { 'Test Intervention' }) -Arguments @('map','mp_rust') | Out-Null
    if ($Synergy) {
        Move-Item -LiteralPath (Join-Path $ReviewDirectory 'launch.ps1') -Destination (Join-Path $ReviewDirectory 'verified-launch.ps1')
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'launch-synergy-trial.ps1') -Destination (Join-Path $ReviewDirectory 'launch.ps1')
    }
}
if ($Launch) { & (Join-Path $ReviewDirectory 'launch.ps1') }
[PSCustomObject]@{ state='prepared'; sha256=$ExpectedSha256.ToLowerInvariant(); sourceExecutableUnchanged=$true; acceptance='unaccepted' } | ConvertTo-Json
