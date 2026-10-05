# Bounded actual-Synergy diagnostic in a fresh local runtime copy; no owner verdict.
param(
    [Parameter(Mandatory=$true)][string]$Source,
    [Parameter(Mandatory=$true)][string]$Binary,
    [Parameter(Mandatory=$true)][string]$Destination,
    [Parameter(Mandatory=$true)][string]$Report,
    [switch]$Baseline,
    [ValidateSet('1280x720','1920x1080')][string]$Resolution='1280x720'
)
$ErrorActionPreference = 'Stop'
if (Get-Process iw4l -ErrorAction SilentlyContinue) { throw 'A game is already running.' }
if (Test-Path -LiteralPath $Report) { throw 'Report exists; preserve prior evidence.' }
$source = $Source
$dest = $Destination
$binary = $Binary
$hash = (Get-FileHash -LiteralPath $binary -Algorithm SHA256).Hash
& (Join-Path $PSScriptRoot 'prepare-trickshot-trial.ps1') -Source $source -Binary $binary -Destination $dest -ExpectedSha256 $hash
$state = [ordered]@{ kind='integration diagnostic, not owner trial'; binarySha256=$hash.ToLowerInvariant(); synergyEnabled=(!$Baseline); launched=$false; gameplay='not tested'; acceptance='unaccepted' }
$state | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $dest 'SYNERGY-INTEGRATION-CHECK.json')
$old = $env:COMBINE_SYNERGY_GSC
$oldProbe = $env:COMBINE_SYNERGY_GSC_PROBE
$oldCommands = $env:IW4L_CMDS
$oldStdin = $env:IW4L_CONSOLE_STDIN
$process = $null
try {
    $env:COMBINE_SYNERGY_GSC = if ($Baseline) { '0' } else { '1' }
    $env:COMBINE_SYNERGY_GSC_PROBE = '1'
    $env:IW4L_CONSOLE_STDIN = '0'
    # Actual physical-button commands traverse the original GSC input manager.
    $env:IW4L_CMDS = 'wait world; spawn 0; wait spawn; wait 5; set ui_r_displayMode 0; set ui_r_mode 1280x720; wait 1; set ui_r_mode '+$Resolution+'; wait 5; press +speed_throw 0.3; press +melee 0.3; wait 1; screenshot synergy-root; press +attack 0.1; wait 1; press +attack 0.1; wait 1; press +activate 0.1; wait 1; press +activate 0.1; wait 1; press +attack 0.1; wait 1; press +attack 0.1; wait 1; press +attack 0.1; wait 1; press +activate 0.1; wait 1; press +activate 0.1; wait 2; screenshot synergy-intervention; press +attack 0.1; wait 1; press +melee 0.1; wait 1; press +melee 0.1; wait 1; press +melee 0.1; wait 1; press +melee 0.1; wait 1; press +attack 0.2; wait 2; press +speed_throw 0.3; press +melee 0.3; wait 1; screenshot synergy-reopen; press +melee 0.15; wait 1; screenshot synergy-closed; wait 1; finish_run'
    if ($Baseline) { $env:IW4L_CMDS = 'wait world; spawn 0; wait spawn; wait 5; finish_run' }
    $process = Start-Process -FilePath (Join-Path $dest 'iw4l.exe') -ArgumentList @('map','mp_rust') -WorkingDirectory $dest -PassThru -RedirectStandardOutput (Join-Path $dest 'check.stdout.log') -RedirectStandardError (Join-Path $dest 'check.stderr.log')
    [void]$process.Handle
    $state.launched = $true
    $state.pid = $process.Id
    $state.startedUtc = [DateTime]::UtcNow.ToString('o')
    $state | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $dest 'SYNERGY-INTEGRATION-CHECK.json')
    Write-Output ('Diagnostic process started; build ' + $hash.ToLowerInvariant())
    $exited = $process.WaitForExit(180000)
    if (!$exited) {
        [void]$process.CloseMainWindow()
        if (!$process.WaitForExit(5000)) { $process.Kill(); $process.WaitForExit() }
        $state.stoppedByDiagnostic = $true
    }
    $process.WaitForExit()
    $process.Refresh()
    $state.exitCode = $process.ExitCode
    $state.endedUtc = [DateTime]::UtcNow.ToString('o')
    $state | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $dest 'SYNERGY-INTEGRATION-CHECK.json')
    # latest.log is the runtime's ordered stream. Never concatenate mirrored logs.
    $streams = @(Get-ChildItem -LiteralPath (Join-Path $dest 'iw4l-artifacts') -Recurse -File -Filter 'latest.log')
    if ($streams.Count -ne 1) { throw 'Expected one authoritative runtime diagnostic stream.' }
    . (Join-Path $PSScriptRoot 'synergy-diagnostic-log.ps1')
    $messages = @(ConvertTo-SynergyDiagnostics -Lines (Get-Content -LiteralPath $streams[0].FullName))
    $state.orderedStream = 'single runtime latest.log'
    $state.sourceDiagnostics = @($messages)
    $state | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $Report
    $state | ConvertTo-Json -Depth 4
} finally {
    $env:COMBINE_SYNERGY_GSC = $old
    $env:COMBINE_SYNERGY_GSC_PROBE = $oldProbe
    $env:IW4L_CMDS = $oldCommands
    $env:IW4L_CONSOLE_STDIN = $oldStdin
    if ($process -and !$process.HasExited) { $process.Kill(); $process.WaitForExit() }
}
