param([Parameter(Mandatory=$true)][string]$Inspection,[Parameter(Mandatory=$true)][string]$WindowMode,
 [Parameter(Mandatory=$true)][string]$Output,[switch]$Focus,[switch]$Restart,[switch]$AllowHungTermination)
$ErrorActionPreference='Stop'
$terminationAttempted=$false;$terminationVerified=$false
try {
 $identity=Get-Content -LiteralPath $Inspection -Raw | ConvertFrom-Json
 $mode=Get-Content -LiteralPath $WindowMode -Raw | ConvertFrom-Json
 if((Get-FileHash -LiteralPath $identity.Executable -Algorithm SHA256).Hash -ine $mode.ExecutableSha256 -or
    [Convert]::ToBase64String([IO.File]::ReadAllBytes($mode.Target)) -cne $mode.CandidateBase64){throw 'Pinned runtime/window setting differs'}
 $exe=Get-Item -LiteralPath $identity.Executable
 if($exe.Name -ine 'GTAIV.exe' -or $exe.VersionInfo.FileVersion -ne '1.2.0.59' -or
    (Get-AuthenticodeSignature -LiteralPath $exe.FullName).Status -ne 'Valid'){throw 'Runtime signature/version differs'}
 $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
 if($AllowHungTermination -and !$Restart){throw 'Hung termination requires explicit recovery'}
 if($games.Count -gt 1 -or ($games.Count -eq 1 -and $games[0].Path -ine $exe.FullName)){throw 'Unexpected game process'}
 if($Restart -and $games.Count -eq 1){
  $old=$games[0];$startTicks=$old.StartTime.ToUniversalTime().Ticks
  $normalClosed=$old.CloseMainWindow() -and $old.WaitForExit(20000)
  if(!$normalClosed){
   if(!$AllowHungTermination){throw 'Normal close refused; preserve process'}
   $current=Get-Process -Id $old.Id
   $null=$current.Handle
   if($current.StartTime.ToUniversalTime().Ticks -ne $startTicks -or $current.Path -ine $exe.FullName -or $current.Responding){throw 'Hung process identity/readiness changed'}
   # Explicit opt-in acts on this held process only, never a name or wildcard.
   @{action='approved-hung-termination';pid=$old.Id;start_ticks=$startTicks;unsaved_progress_may_be_lost=$true} |
    ConvertTo-Json | Set-Content -LiteralPath ($Output+'.recovery-private.json') -Encoding UTF8
   $terminationAttempted=$true;$current.Kill()
   if(!$current.WaitForExit(10000)){throw 'Hung process exit unverified'}
   $terminationVerified=$true
  }
  if(@(Get-Process GTAIV -ErrorAction SilentlyContinue).Count){throw 'Process appeared before relaunch'}
  $games=@()
 }
 $launchedByUs=$games.Count -eq 0;$handoff=$false
 if($launchedByUs){$expected=Start-Process -FilePath $exe.FullName -WorkingDirectory $exe.DirectoryName -ArgumentList '-windowed','-width','1280','-height','720' -PassThru}
 else{$expected=$games[0]}
 $null=$expected.Handle
 $expectedId=$expected.Id;$expectedTicks=$expected.StartTime.ToUniversalTime().Ticks
 @{pid=$expectedId;start_ticks=$expectedTicks;launched_by_workflow=$launchedByUs} | ConvertTo-Json |
  Set-Content -LiteralPath ($Output+'.launch-private.json') -Encoding UTF8
 Add-Type @'
using System;using System.Runtime.InteropServices;
public static class CombineOpenWindow{
 [DllImport("user32.dll")]public static extern int GetWindowLong(IntPtr h,int i);
 [DllImport("user32.dll")]public static extern bool IsIconic(IntPtr h);
 [DllImport("user32.dll")]public static extern bool ShowWindowAsync(IntPtr h,int cmd);
 [DllImport("user32.dll")]public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")]public static extern IntPtr GetForegroundWindow();
}
'@
 $timer=[Diagnostics.Stopwatch]::StartNew();$game=$null;$focusRequested=$false
 while($timer.Elapsed.TotalSeconds -lt 120){
  $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
  if($games.Count -gt 1){throw 'Multiple processes'}
  if($games.Count -eq 1){
   if($games[0].Path -ine $exe.FullName){throw 'Process changed'}
   if($games[0].Id -ne $expectedId -or $games[0].StartTime.ToUniversalTime().Ticks -ne $expectedTicks){
    # The signed GTA executable may hand launch to a replacement game process.
    # Adopt once only after our held starter exits; then freeze the new identity.
    if(!$launchedByUs -or $handoff -or !$expected.HasExited -or $games[0].StartTime.ToUniversalTime().Ticks -le $expectedTicks){throw 'Process changed'}
    $expected=$games[0];$null=$expected.Handle
    $expectedId=$expected.Id;$expectedTicks=$expected.StartTime.ToUniversalTime().Ticks;$handoff=$true
   }
   # Restore/focus the authorized launch once its window exists. Requiring
   # responsiveness first can strand a background startup before this request.
   if($Focus -and !$focusRequested -and $games[0].MainWindowHandle -ne [IntPtr]::Zero){
    if(([CombineOpenWindow]::GetWindowLong($games[0].MainWindowHandle,-16) -band 0x00C00000) -ne 0x00C00000){throw 'Window mode refused'}
    $null=[CombineOpenWindow]::ShowWindowAsync($games[0].MainWindowHandle,9)
    $null=[CombineOpenWindow]::SetForegroundWindow($games[0].MainWindowHandle)
    $focusRequested=$true
   }
   if($games[0].MainWindowHandle -ne [IntPtr]::Zero -and $games[0].Responding){$game=$games[0];break}
  }
  Start-Sleep -Milliseconds 250
 }
 if(!$game){throw 'Normal launch/window not ready'}
 if(([CombineOpenWindow]::GetWindowLong($game.MainWindowHandle,-16) -band 0x00C00000) -ne 0x00C00000){throw 'Window mode refused'}
 if($Focus -and !$focusRequested){
  $null=[CombineOpenWindow]::ShowWindowAsync($game.MainWindowHandle,9)
  Start-Sleep -Milliseconds 300
  $null=[CombineOpenWindow]::SetForegroundWindow($game.MainWindowHandle)
  Start-Sleep -Milliseconds 300
 }
 $current=Get-Process -Id $game.Id
 if($current.StartTime.ToUniversalTime().Ticks -ne $game.StartTime.ToUniversalTime().Ticks -or
    ([CombineOpenWindow]::GetWindowLong($current.MainWindowHandle,-16) -band 0x00C00000) -ne 0x00C00000){throw 'Window owner/mode changed'}
 $foreground=[CombineOpenWindow]::GetForegroundWindow() -eq $current.MainWindowHandle -and ![CombineOpenWindow]::IsIconic($current.MainWindowHandle)
 @{pid=$current.Id;start_ticks=$current.StartTime.ToUniversalTime().Ticks;windowed=$true;foreground=$foreground;launcher_handoff=$handoff;termination_attempted=$terminationAttempted;termination_exit_verified=$terminationVerified} |
  ConvertTo-Json | Set-Content -LiteralPath $Output -Encoding UTF8
 if(!$foreground){Write-Output 'UNAVAILABLE: foreground-unverified; pinned windowed process present; no input';exit 2}
 Write-Output 'PASS: pinned windowed foreground game ready for guarded offline-menu checks; no keys sent'
}catch{
 $reason=switch($_.Exception.Message){
  'Pinned runtime/window setting differs' {'runtime-window-setting-mismatch'}
  'Runtime signature/version differs' {'runtime-signature-version-mismatch'}
  'Unexpected game process' {'unexpected-game-process'}
  'Normal close refused; preserve process' {'normal-close-refused'}
  'Hung termination requires explicit recovery' {'hung-termination-needs-recovery'}
  'Hung process identity/readiness changed' {'hung-process-identity-readiness-changed'}
  'Hung process exit unverified' {'hung-process-exit-unverified'}
  'Process appeared before relaunch' {'unexpected-game-process'}
  'Multiple processes' {'multiple-processes'}
  'Process changed' {'process-changed'}
  'Normal launch/window not ready' {'window-not-ready'}
  'Window mode refused' {'windowed-mode-refused'}
  'Window owner/mode changed' {'window-owner-mode-changed'}
  default {'launch-prerequisites-unavailable'}
 }
 $_ | Out-String | Set-Content -LiteralPath ($Output+'.error-private.txt')
 Write-Output ('UNAVAILABLE: '+$reason+'; no keys sent; termination_attempted='+$terminationAttempted+'; termination_exit_verified='+$terminationVerified);exit 2
}
