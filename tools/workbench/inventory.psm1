function Get-CombineRuntimeContract {
 $contract=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'runtime-roles.json') -Raw|ConvertFrom-Json
 if($contract.schema -ne 1){throw 'runtime-inventory'}
 return $contract
}
Export-ModuleMember -Function Get-CombineRuntimeContract
