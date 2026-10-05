# Project adapter around the shared exact-build launcher. No diagnostic inputs.
param([switch]$VerifyOnly)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$values = @{
    COMBINE_SYNERGY_GSC = '1'
    COMBINE_SYNERGY_GSC_PROBE = '0'
    # A nonempty whitespace value blocks inherited .env command fallback.
    IW4L_CMDS = ' '
    IW4L_CONSOLE_STDIN = '0'
}
$previous = @{}
try {
    foreach ($name in $values.Keys) {
        $previous[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
        [Environment]::SetEnvironmentVariable($name, $values[$name], 'Process')
    }
    & (Join-Path $PSScriptRoot 'verified-launch.ps1') -VerifyOnly:$VerifyOnly
} finally {
    foreach ($name in $values.Keys) {
        [Environment]::SetEnvironmentVariable($name, $previous[$name], 'Process')
    }
}
