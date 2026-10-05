# Redact one chronological runtime stream; never include raw error arguments.
function ConvertTo-SynergyDiagnostics {
    param([string[]]$Lines)
    $messages = @()
    $statistics = 'maps/mp/_matchdata:10:3 in init: setmatchdatadef: unavailable: IW4 definition schemas are not supported by the local match-data store'
    foreach ($line in $Lines) {
        if ($line -match '(SYNERGY_PROBE [a-z_0-9= ]+)') { $messages += $Matches[1] }
        elseif ($line.Contains($statistics)) { $messages += $statistics }
        elseif ($line -match '([a-zA-Z0-9_./]+:\d+:\d+ in [a-zA-Z0-9_]+):') {
            # Keep source location, discard potentially private error arguments.
            $messages += ($Matches[1] + ': script fault (details retained privately)')
        }
        elseif ($line -match 'unresolved (?:method or unknown builtin|function or unknown builtin|function|thread function)') {
            $messages += 'unresolved script symbol (details retained privately)'
        }
        elseif ($line -match 'gsc: script runtime error|gsc.*refused') {
            $messages += 'unclassified script failure (details retained privately)'
        }
    }
    return $messages
}
