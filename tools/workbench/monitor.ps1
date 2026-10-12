param([Parameter(Mandatory=$true)][string]$Inspection,
 [Parameter(Mandatory=$true)][string]$StatusModule,
 [ValidateRange(5,120)][int]$TimeoutSeconds=45)
$ErrorActionPreference='Stop'
try {
 Import-Module $StatusModule -Force
 $identity=Get-Content -LiteralPath $Inspection -Raw | ConvertFrom-Json
 $expected=(Get-Item -LiteralPath $identity.Executable).FullName
 Add-Type @'
using System;using System.Runtime.InteropServices;
public static class CombineMonitorWindow {
 [DllImport("user32.dll")]public static extern int GetWindowLong(IntPtr h,int i);
 [DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")]public static extern bool IsIconic(IntPtr h);
}
'@
 $clock=[Diagnostics.Stopwatch]::StartNew();$last='';$locked=$false;$windowAt=-1
 while($clock.Elapsed.TotalSeconds -lt $TimeoutSeconds){
  $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
  $state='waiting-for-process'
  if($games.Count -gt 1){$state='multiple-processes'}
  elseif($games.Count -eq 1){
   $g=$games[0]
   if($g.Path -ine $expected){$state='process-identity-changed'}
   elseif($locked -and ($g.Id -ne $pidSeen -or $g.StartTime.ToUniversalTime().Ticks -ne $ticksSeen)){$state='process-identity-changed'}
   else {
    $h=$g.MainWindowHandle
    if($h -eq [IntPtr]::Zero){$state='waiting-for-window'}
    elseif(([CombineMonitorWindow]::GetWindowLong($h,-16) -band 0x00C00000) -ne 0x00C00000){$state='windowed-mode-refused'}
    elseif(!$g.Responding){$state='window-not-responding'}
    elseif([CombineMonitorWindow]::IsIconic($h) -or [CombineMonitorWindow]::GetForegroundWindow() -ne $h){$state='foreground-unverified'}
    else {
     $locked=$true;$pidSeen=$g.Id;$ticksSeen=$g.StartTime.ToUniversalTime().Ticks
     if($windowAt -lt 0){$windowAt=$clock.Elapsed.TotalSeconds}
     $report=Get-CombineGameReport
     if($report.Scene -eq 'unknown'){$state='waiting-for-fresh-game-state'}
     elseif($report.CanTest){$state='fresh-gameplay'}
     else {$state='fresh-'+$report.Scene}
    }
   }
  } elseif($locked){$state='process-exited'}
  if($state -ne $last){[Console]::Out.WriteLine('MONITOR: '+$state);[Console]::Out.Flush();$last=$state}
  if($state -in @('multiple-processes','process-identity-changed','process-exited','windowed-mode-refused')){exit 2}
  if($state -eq 'fresh-gameplay'){exit 0}
  if($windowAt -ge 0 -and $clock.Elapsed.TotalSeconds-$windowAt -ge 60 -and $state -eq 'waiting-for-fresh-game-state'){
   [Console]::Out.WriteLine('MONITOR: no-fresh-game-state-after-60s');[Console]::Out.Flush();exit 2
  }
  Start-Sleep -Milliseconds 500
 }
 [Console]::Out.WriteLine('MONITOR: timeout-'+$last);[Console]::Out.Flush();exit 2
} catch {
 Write-Output 'MONITOR: observation-unavailable';exit 2
}
