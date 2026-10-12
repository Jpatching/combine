param(
    [string]$StatePath=(Join-Path $env:LOCALAPPDATA 'Combine\gtaiv-status\state.json'),
    [switch]$WaitPlayable,
    [switch]$Watch,
    [ValidateRange(1,3600)][int]$TimeoutSeconds=60,
    [switch]$Json
)
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot 'game-status.psm1') -Force
if($WaitPlayable -and $Watch){throw 'Choose WaitPlayable or Watch'}
$timer=[Diagnostics.Stopwatch]::StartNew();$previous=''
do {
    $report=Get-CombineGameReport -StatePath $StatePath
    $key=$report | ConvertTo-Json -Compress
    if($key -ne $previous) {
        if($Json){Write-Output $key}
        else {Write-Output ("Scene: {0}`nPlayer control: {1}`nController: {2}`nAdapter: {3}`nCurrent test: {4}" -f $report.Scene,$report.PlayerControl,$report.Controller,$report.Adapter,$report.CurrentTest)}
        $previous=$key
    }
    if($WaitPlayable -and $report.CanTest){exit 0}
    if(!$WaitPlayable -and !$Watch){exit 0}
    if($timer.Elapsed.TotalSeconds -ge $TimeoutSeconds){if($WaitPlayable){exit 2}else{exit 0}}
    Start-Sleep -Milliseconds 250
} while($true)
