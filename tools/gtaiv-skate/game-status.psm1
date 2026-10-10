# Only fixed state labels cross this interface. Never return private file contents.
function New-UnknownReport {
    [pscustomobject]@{Scene='unknown';PlayerControl='unknown';Controller='unknown';Adapter='unknown';CurrentTest='waiting for verified game state';OnFoot=$null;CanTest=$false}
}
function ConvertTo-CombineGameReport {
    param($Snapshot,[long]$ExpectedProcessId,[DateTimeOffset]$ExpectedStartTime,[long]$NowMs)
    $unknown=New-UnknownReport
    $ExpectedStartMs=$ExpectedStartTime.ToUnixTimeMilliseconds()
    if($null -eq $Snapshot){return $unknown}
    $names=@('schema','pid','process_start_ms','updated_ms','scene','player_control','on_foot','adapter_ready','mounted','controller')
    $actual=@($Snapshot.PSObject.Properties.Name)
    if($actual.Count -ne $names.Count -or @($names | Where-Object {$_ -notin $actual}).Count){return $unknown}
    foreach($name in @('schema','pid','process_start_ms','updated_ms')) {
        $value=$Snapshot.$name
        if($value -isnot [int] -and $value -isnot [long]){return $unknown}
    }
    foreach($name in @('player_control','on_foot','adapter_ready','mounted','controller')) {
        if($Snapshot.$name -isnot [bool]){return $unknown}
    }
    if($Snapshot.scene -isnot [string] -or $Snapshot.scene -notin @('unknown','gameplay','cutscene','paused','unavailable')){return $unknown}
    if($Snapshot.schema -ne 1 -or $Snapshot.pid -ne $ExpectedProcessId -or $ExpectedProcessId -le 0 -or
        $Snapshot.process_start_ms -ne $ExpectedStartMs -or $Snapshot.updated_ms -lt $ExpectedStartMs -or
        $NowMs-$Snapshot.updated_ms -gt 2000 -or $Snapshot.updated_ms-$NowMs -gt 1000){return $unknown}
    $allowed=$Snapshot.scene -eq 'gameplay' -and $Snapshot.adapter_ready -and $Snapshot.controller -and $Snapshot.on_foot
    $allowed=$allowed -and ($Snapshot.player_control -or $Snapshot.mounted)
    $task='waiting for controllable gameplay'
    if($allowed){$task=if($Snapshot.mounted){'ready for riding test'}else{'ready for mount test'}}
    elseif($Snapshot.scene -eq 'gameplay' -and ($Snapshot.player_control -or $Snapshot.mounted)) {
        $task=if(!$Snapshot.on_foot){'waiting for on-foot gameplay'}elseif(!$Snapshot.controller){'waiting for controller slot 0'}else{'waiting for adapter readiness'}
    }
    [pscustomobject]@{
        Scene=$Snapshot.scene
        PlayerControl=$(if($Snapshot.player_control){'enabled'}else{'disabled'})
        Controller=$(if($Snapshot.controller){'connected, slot 0'}else{'disconnected, slot 0'})
        Adapter=$(if(!$Snapshot.adapter_ready){'not ready'}elseif($Snapshot.mounted){'ready, mounted'}else{'ready, unmounted'})
        CurrentTest=$task;OnFoot=$Snapshot.on_foot;CanTest=[bool]$allowed
    }
}
function Get-CombineGameReport {
    param([string]$StatePath=(Join-Path $env:LOCALAPPDATA 'Combine\gtaiv-status\state.json'))
    $unknown=New-UnknownReport
    try {
        $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
        if($games.Count -eq 0){$unknown.Scene='closed';$unknown.CurrentTest='waiting for game launch';return $unknown}
        if($games.Count -ne 1){return $unknown}
        $file=Get-Item -LiteralPath $StatePath -ErrorAction Stop
        if($file.Length -gt 8192 -or $file.PSIsContainer -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)){return $unknown}
        $snapshot=[IO.File]::ReadAllText($file.FullName) | ConvertFrom-Json -ErrorAction Stop
        $start=[DateTimeOffset]$games[0].StartTime.ToUniversalTime()
        $now=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
        ConvertTo-CombineGameReport -Snapshot $snapshot -ExpectedProcessId $games[0].Id -ExpectedStartTime $start -NowMs $now
    } catch {return $unknown}
}
Export-ModuleMember -Function ConvertTo-CombineGameReport,Get-CombineGameReport
