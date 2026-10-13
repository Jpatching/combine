# Return typing focus after an owner-authorised, bounded GTA trial. No keys sent.
$ErrorActionPreference='Stop'
try {
 Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class CombineChatFocus {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr h,int n);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@
 $windows=@(Get-Process ChatGPT -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowHandle -ne [IntPtr]::Zero})
 if($windows.Count -ne 1){throw 'unique-chat-window-unavailable'}
 $chat=$windows[0];$start=$chat.StartTime.ToUniversalTime().Ticks;$handle=$chat.MainWindowHandle
 $current=Get-Process -Id $chat.Id
 if($current.StartTime.ToUniversalTime().Ticks -ne $start -or $current.MainWindowHandle -ne $handle){throw 'chat-window-changed'}
 $null=[CombineChatFocus]::ShowWindowAsync($handle,9)
 $null=[CombineChatFocus]::SetForegroundWindow($handle)
 Start-Sleep -Milliseconds 300
 if([CombineChatFocus]::GetForegroundWindow() -ne $handle){throw 'chat-focus-unverified'}
 Write-Output 'PASS: chat typing focus restored; no game input'
}catch{
 Write-Output 'UNAVAILABLE: chat typing focus could not be verified; no game input'
 exit 2
}
