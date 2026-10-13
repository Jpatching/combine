param([Parameter(Mandatory=$true)][string]$StatusModule)
$ErrorActionPreference='Stop'
try {
 Import-Module $StatusModule -Force
 Add-Type @'
using System;using System.Runtime.InteropServices;
public static class CombineStatusWindow {
 [DllImport("user32.dll")]public static extern int GetWindowLong(IntPtr h,int i);
 [DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")]public static extern bool IsIconic(IntPtr h);
}
'@
 $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
 $windowed=$false;$foreground=$false;$responding=$false
 if($games.Count -eq 1){
  $g=$games[0];$h=$g.MainWindowHandle
  $responding=$g.Responding
  $windowed=$h -ne [IntPtr]::Zero -and ([CombineStatusWindow]::GetWindowLong($h,-16) -band 0x00C00000) -eq 0x00C00000
  $foreground=$h -ne [IntPtr]::Zero -and ![CombineStatusWindow]::IsIconic($h) -and [CombineStatusWindow]::GetForegroundWindow() -eq $h
 }
 $report=Get-CombineGameReport
 @{process_count=$games.Count;responding=$responding;windowed=$windowed;foreground=$foreground;game=$report} | ConvertTo-Json -Depth 4 -Compress
 if(!$responding -or !$windowed -or !$foreground -or !$report.CanTest){exit 2}
}catch{Write-Output 'UNAVAILABLE: status-observation';exit 2}
