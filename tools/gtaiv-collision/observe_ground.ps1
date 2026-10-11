param(
    [Parameter(Mandatory=$true)][string]$Session,
    [Parameter(Mandatory=$true)][string]$Output
)
# Read-only observation plus one bounded F8 pulse. Never focus or launch GTA.
$ErrorActionPreference='Stop'
$observerStartedMs=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$events=Join-Path $Output 'events-private.jsonl'
$m=Get-Content -LiteralPath $Session -Raw | ConvertFrom-Json
Import-Module (Join-Path $PSScriptRoot '../gtaiv-skate/game-status.psm1') -Force
Add-Type @'
using System; using System.Runtime.InteropServices;
public static class GroundCollectorWindow {
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint p);
 [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
 [DllImport("user32.dll")] public static extern short GetAsyncKeyState(int key);
 [StructLayout(LayoutKind.Sequential)] public struct Mouse {public int dx,dy;public uint data,flags,time;public UIntPtr extra;}
 [StructLayout(LayoutKind.Sequential)] public struct Key {public ushort vk,scan;public uint flags,time;public UIntPtr extra;}
 [StructLayout(LayoutKind.Explicit)] public struct Union {[FieldOffset(0)] public Mouse mouse;[FieldOffset(0)] public Key key;}
 [StructLayout(LayoutKind.Sequential)] public struct Input {public uint type;public Union data;}
 [DllImport("user32.dll")] public static extern uint SendInput(uint n,Input[] d,int size);
 public static uint F8(bool up) {Input i=new Input();i.type=1;i.data.key.scan=0x42;i.data.key.flags=(uint)(8|(up?2:0));return SendInput(1,new Input[]{i},Marshal.SizeOf(typeof(Input)));}
 public static uint GuardedDown(uint expected) {
  uint owner;IntPtr window=GetForegroundWindow();GetWindowThreadProcessId(window,out owner);
  if(expected==0 || owner!=expected || IsIconic(window) || (GetAsyncKeyState(0x77)&0x8000)!=0)return 0;
  return F8(false);
 }
}
'@
function Verify-Artifacts {
 $exe=Get-Item -LiteralPath $m.executable
 if($exe.VersionInfo.FileVersion -ne '1.2.0.59' -or (Get-AuthenticodeSignature -LiteralPath $exe.FullName).Status -ne 'Valid'){throw 'artifact-mismatch'}
 $hashes=@()
 foreach($artifact in $m.artifacts){
  $hash=(Get-FileHash -LiteralPath $artifact.path -Algorithm SHA256).Hash.ToLowerInvariant()
  if($hash -cne $artifact.sha256){throw 'artifact-mismatch'}
  $modified=[DateTimeOffset](Get-Item -LiteralPath $artifact.path).LastWriteTimeUtc
  if($modified.ToUnixTimeMilliseconds() -gt $m.process.start_ms){throw 'artifact-mismatch'}
  $hashes+=$hash
 }
 return ,$hashes
}
function Snapshot {
 # Expensive identity work precedes the fresh process/status/focus sample.
 $hashes=Verify-Artifacts
 $games=@(Get-Process GTAIV -ErrorAction SilentlyContinue)
 if($games.Count -ne 1){throw 'stale-process-status'}
 $g=$games[0];$start=[DateTimeOffset]$g.StartTime.ToUniversalTime()
 if($g.Id -ne $m.process.pid -or $start.ToUnixTimeMilliseconds() -ne $m.process.start_ms -or $g.Path -ine $m.executable){throw 'stale-process-status'}
 $statusFile=Get-Item -LiteralPath $m.state_path
 if($statusFile.Length -gt 8192 -or ($statusFile.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'stale-process-status'}
 $state=[IO.File]::ReadAllText($statusFile.FullName) | ConvertFrom-Json
 $now=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
 $report=ConvertTo-CombineGameReport -Snapshot $state -ExpectedProcessId $g.Id -ExpectedStartTime $start -NowMs $now
 [uint32]$foregroundId=0;$window=[GroundCollectorWindow]::GetForegroundWindow()
 [void][GroundCollectorWindow]::GetWindowThreadProcessId($window,[ref]$foregroundId)
 if($now-$state.updated_ms -gt 2000 -or $state.updated_ms-$now -gt 1000){throw 'stale-process-status'}
 if(!$report.CanTest -or $report.Adapter -ne 'ready, unmounted' -or $report.PlayerControl -ne 'enabled'){throw 'not-ready'}
 if(!$g.Responding -or $g.MainWindowHandle -eq 0 -or $window -ne $g.MainWindowHandle -or
    $foregroundId -ne $g.Id -or [GroundCollectorWindow]::IsIconic($window)){throw 'foreground-lost'}
 return @{pid=$g.Id;start_ms=$m.process.start_ms;now_ms=$now;updated_ms=$state.updated_ms;
  foreground=$true;minimized=$false;responding=$true;scene='gameplay';player_control=$true;
  on_foot=$true;adapter_ready=$true;mounted=$false;artifacts=$hashes}
}
function Event($event) {
 $json=$event | ConvertTo-Json -Depth 20 -Compress
 [IO.File]::AppendAllText($events,$json+"`n",[Text.UTF8Encoding]::new($false))
}
try {
 if($m.token -cnotmatch '^[0-9a-f]{32}$' -or @($m.log_paths).Count -lt 1 -or @($m.log_paths).Count -gt 2){throw 'Session schema'}
 $before=Snapshot
 # Reuse the reviewed current-run reader's byte boundaries and quoted-log handling.
 $offsets=@{};$pending=@{}
 foreach($path in $m.log_paths){$offsets[$path]=if(Test-Path -LiteralPath $path){(Get-Item -LiteralPath $path).Length}else{0};$pending[$path]=''}
 $before=Snapshot
 Event @{kind='ready';snapshot=$before;setup_ms=([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-$observerStartedMs)}
 $collectionStartedMs=[DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
 $down=0;$up=0;$pressed=$false
 try {
  # Recheck the actual foreground inside the same native call as key-down.
  $down=[GroundCollectorWindow]::GuardedDown($m.process.pid)
  $pressed=$down -eq 1
  if($pressed){Start-Sleep -Milliseconds 100}
 } finally {if($pressed){$up=[GroundCollectorWindow]::F8($true)}}
 if($down -ne 1 -or $up -ne 1){throw 'Input refused'}
 $timer=[Diagnostics.Stopwatch]::StartNew();$attempt=$null;$activeLog=$null;$done=$false;$count=0
 $prefix='COMBINE_GROUND_COLLECT '+$m.token+' PRIVATE '
 while(!$done -and $timer.Elapsed.TotalSeconds -lt 35){
  $snapshot=Snapshot
  foreach($path in $m.log_paths){
   if(!(Test-Path -LiteralPath $path)){continue}
   $file=Get-Item -LiteralPath $path
   if($file.Length -lt $offsets[$path] -or $file.Length-$offsets[$path] -gt 1048576){throw 'Log boundary changed'}
   $stream=[IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
   try {
    $null=$stream.Seek($offsets[$path],[IO.SeekOrigin]::Begin)
    $bytes=[byte[]]::new(1048577);$read=$stream.Read($bytes,0,$bytes.Length)
    if($read -gt 1048576){throw 'Log bound'}
    $offsets[$path]+=$read
   } finally {$stream.Dispose()}
   $text=$pending[$path]+[Text.Encoding]::UTF8.GetString($bytes,0,$read)
   $lines=$text.Split([char]10);$pending[$path]=$lines[-1]
   if($pending[$path].Length -gt 65536){throw 'Line bound'}
   foreach($line in @($lines | Select-Object -SkipLast 1)){
    $index=$line.IndexOf($prefix,[StringComparison]::Ordinal)
    if($index -lt 0){continue}
    if($activeLog -and $activeLog -cne $path){throw 'Ambiguous diagnostic log'};$activeLog=$path
    $raw=$line.Substring($index+$prefix.Length).Trim()
    if($raw.EndsWith('"')){$raw=$raw.Substring(0,$raw.Length-1)}
    try {$row=$raw | ConvertFrom-Json} catch {$raw=('"'+$raw+'"') | ConvertFrom-Json;$row=$raw | ConvertFrom-Json}
    if($row.kind -eq 'start'){
     if($null -ne $attempt){throw 'Duplicate start'};$attempt=$row.attempt;continue
    }
    if($null -eq $attempt -or $row.attempt -ne $attempt -or ++$count -gt 97){throw 'Diagnostic sequence'}
    if($row.kind -notin @('reading','complete')){throw 'Diagnostic refused'}
    $row | Add-Member -NotePropertyName snapshot -NotePropertyValue $snapshot
    if($row.kind -eq 'complete'){$row | Add-Member -NotePropertyName collection_ms -NotePropertyValue ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()-$collectionStartedMs)}
    Event $row
    if($row.kind -eq 'complete'){$done=$true}
   }
  }
  $null=Snapshot
  if(!$done){Start-Sleep -Milliseconds 50}
 }
 if(!$done){throw 'Collection deadline'}
 exit 0
} catch {
 $_ | Out-String | Set-Content -LiteralPath (Join-Path $Output 'observer-error-private.txt')
 $reason=$_.Exception.Message
 if($reason -notin @('stale-process-status','not-ready','foreground-lost','artifact-mismatch')){$reason='observer-refused'}
 Event @{kind='refused';reason=$reason}
 exit 2
}
