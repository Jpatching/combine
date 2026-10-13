Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class CombineTrialWindow {
 [StructLayout(LayoutKind.Sequential)] public struct Mouse {public int dx,dy;public uint data,flags,time;public UIntPtr extra;}
 [StructLayout(LayoutKind.Sequential)] public struct Key {public ushort vk,scan;public uint flags,time;public UIntPtr extra;}
 [StructLayout(LayoutKind.Explicit)] public struct Union {[FieldOffset(0)] public Mouse mouse;[FieldOffset(0)] public Key key;}
 [StructLayout(LayoutKind.Sequential)] public struct Input {public uint type;public Union data;}
 [DllImport("user32.dll")] public static extern uint SendInput(uint n,Input[] data,int size);
 [DllImport("user32.dll")] public static extern short GetAsyncKeyState(int vk);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
 [DllImport("user32.dll")] public static extern int GetWindowLong(IntPtr h,int index);
 public static uint KeyUp(ushort scan) {return Send(scan,true);}
 static uint Send(ushort scan,bool up) {Input i=new Input();i.type=1;i.data.key.scan=scan;i.data.key.flags=(uint)(8|(up?2:0));return SendInput(1,new Input[]{i},Marshal.SizeOf(typeof(Input)));}
 public static uint GuardedDown(IntPtr window,int pid,long ticks,ushort scan) {
  try {var p=System.Diagnostics.Process.GetProcessById(pid);if(p.StartTime.ToUniversalTime().Ticks!=ticks || p.MainWindowHandle!=window)return 0;}catch{return 0;}
  if(window==IntPtr.Zero || GetForegroundWindow()!=window || IsIconic(window)
     || (GetWindowLong(window,-16)&0x00C00000)!=0x00C00000 || (GetAsyncKeyState(scan==17?0x57:scan>=64&&scan<=67?scan+0x35:0x0D)&0x8000)!=0)return 0;
  return Send(scan,false);
 }
}
'@
function Get-CombineTrialSnapshot([bool]$RequireUnmounted=$true,[bool]$Menu=$false) {
 $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
 if($games.Count -ne 1){throw 'process-identity'}
 $g=$games[0];$start=[DateTimeOffset]$g.StartTime.ToUniversalTime()
 if($g.Id -ne $m.process.pid -or $start.ToUnixTimeMilliseconds() -ne $m.process.start_ms -or $g.Path -ine $m.executable){throw 'process-identity'}
 if(!$g.Responding -or $g.MainWindowHandle -eq 0 -or ([CombineTrialWindow]::IsIconic($g.MainWindowHandle)) -or
    ([CombineTrialWindow]::GetForegroundWindow()) -ne $g.MainWindowHandle){throw 'foreground'}
 if(([CombineTrialWindow]::GetWindowLong($g.MainWindowHandle,-16) -band 0x00C00000) -ne 0x00C00000){throw 'windowed'}
 $r=Get-CombineGameReport -StatePath $m.state_path
 if(!$Menu -and (!$r.CanTest -or ($RequireUnmounted -and ($r.Adapter -ne 'ready, unmounted' -or $r.PlayerControl -ne 'enabled')))){throw 'fresh-gameplay'}
 return @{Game=$g;Report=$r}
}
function Test-CombineTrialInventory {
 Import-Module (Join-Path $PSScriptRoot 'inventory.psm1') -Force
 $contract=Get-CombineRuntimeContract;$roles=@($contract.required)
 $count=@($m.artifacts).Count
 if($count -lt $roles.Count -or $count -gt ($roles.Count+$contract.optional.Count) -or @($m.artifacts.role | Select-Object -Unique).Count -ne $count -or @($roles | Where-Object {$_ -notin $m.artifacts.role}).Count -or
    @($m.artifacts.role | Where-Object {$_ -notin ($roles+@($contract.optional))}).Count){throw 'runtime-inventory'}
 $exe=Get-Item -LiteralPath $m.executable
 if($exe.VersionInfo.FileVersion -ne '1.2.0.59' -or (Get-AuthenticodeSignature -LiteralPath $m.executable).Status -ne 'Valid'){throw 'runtime-identity'}
 foreach($a in $m.artifacts){
  $file=Get-Item -LiteralPath $a.path
  if($file.PSIsContainer -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
     ([DateTimeOffset]$file.LastWriteTimeUtc).ToUnixTimeMilliseconds() -gt $m.process.start_ms -or
     (Get-FileHash -LiteralPath $a.path -Algorithm SHA256).Hash.ToLowerInvariant() -cne $a.sha256){throw 'runtime-inventory'}
 }
 $exeArtifact=@($m.artifacts | Where-Object {$_.role -eq 'executable'})[0]
 if($exeArtifact.path -ine $m.executable){throw 'runtime-identity'}
}
function Invoke-CombineTrialPulse([int]$Scan=64,[bool]$Menu=$false) {
 if($Scan -notin @(28,64,65,66,67)){throw 'unsupported-key'}
 $s=Get-CombineTrialSnapshot $false $Menu
 $owned=$false
 try {
  $down=[CombineTrialWindow]::GuardedDown($s.Game.MainWindowHandle,$s.Game.Id,$s.Game.StartTime.ToUniversalTime().Ticks,$Scan)
  if($down -ne 1){throw 'input-refused'}
  $owned=$true;$script:acted=$true;$script:released=$false;$script:held[$Scan]=$true;Start-Sleep -Milliseconds 200
 }finally{if($owned){if([CombineTrialWindow]::KeyUp($Scan) -ne 1){throw 'input-release'};$script:held.Remove($Scan);$script:released=$script:held.Count -eq 0}}
}
function Invoke-CombineTrialWalking {
 # Fixed normal walking probe only; caller supplies no key or duration.
 Invoke-CombineTrialPulse 67
 $s=Get-CombineTrialSnapshot $true
 $owned=$false
 try {
  $down=[CombineTrialWindow]::GuardedDown($s.Game.MainWindowHandle,$s.Game.Id,$s.Game.StartTime.ToUniversalTime().Ticks,17)
  if($down -ne 1){throw 'input-refused'}
  $owned=$true;$script:acted=$true;$script:released=$false;$script:held[17]=$true
  # The active F9 observer sees normal W movement; no other key is held.
  for($i=0;$i -lt 5;$i++){Start-Sleep -Milliseconds 100;$null=Get-CombineTrialSnapshot $true}
 }finally{if($owned){if([CombineTrialWindow]::KeyUp(17) -ne 1){throw 'input-release'};$script:held.Remove(17);$script:released=$script:held.Count -eq 0}}
}
function Initialize-CombineTrial([string]$Session,[string]$StatusModule) {
 $script:m=Get-Content -LiteralPath $Session -Raw | ConvertFrom-Json
 $script:acted=$false
 $script:released=$true
 $script:held=@{}
 Import-Module $StatusModule -Force
 Test-CombineTrialInventory
}
function Test-CombineTrialNoHeldKeys {
 foreach($key in @(0x57,0x75,0x76,0x77,0x78)){
  if(([CombineTrialWindow]::GetAsyncKeyState($key) -band 0x8000) -ne 0){throw 'input-held'}
 }
 if($script:acted -or !$script:released){throw 'input-held'}
}
function Get-CombineTrialInputOwned {return $script:acted}
function Test-CombineTrialInputReleased {return $script:released}
Export-ModuleMember -Function Initialize-CombineTrial,Get-CombineTrialSnapshot,Test-CombineTrialInventory,Invoke-CombineTrialPulse,Get-CombineTrialInputOwned,Test-CombineTrialInputReleased,Invoke-CombineTrialWalking,Test-CombineTrialNoHeldKeys
