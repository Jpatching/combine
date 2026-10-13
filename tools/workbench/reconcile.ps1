# Read-only local recovery observation. No override or game input.
param(
 [Parameter(Mandatory=$true)][string]$Session,
 [Parameter(Mandatory=$true)][string]$StatusModule,
 [Parameter(Mandatory=$true)][string]$Output
)
$ErrorActionPreference='Stop'
try {
 Import-Module (Join-Path $PSScriptRoot 'runtime.psm1') -Force
 Initialize-CombineTrial $Session $StatusModule
 $null=Get-CombineTrialSnapshot $true
 Test-CombineTrialNoHeldKeys
 Test-CombineTrialInventory
 $null=Get-CombineTrialSnapshot $true
 Test-CombineTrialNoHeldKeys
 @{observation='fresh-normal-gameplay'} | ConvertTo-Json -Compress | Set-Content -LiteralPath $Output -Encoding UTF8
 exit 0
}catch{
 $_ | Out-String | Set-Content -LiteralPath ($Output+'.error-private.txt')
 Write-Output 'UNAVAILABLE: fresh recovery prerequisites absent; no game input'
 exit 2
}
