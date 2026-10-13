$ErrorActionPreference='Stop'
# Evaluate the actual status observation expression against synthetic window facts.
# No windows are focused and no game input is sent.
Add-Type @'
using System;
public static class CombineStatusWindow {
 public static IntPtr Foreground=new IntPtr(1);
 public static bool Minimized=false;
 public static bool IsIconic(IntPtr h){return Minimized;}
 public static IntPtr GetForegroundWindow(){return Foreground;}
}
'@
$line=@(Get-Content (Join-Path $PSScriptRoot 'status.ps1') | Where-Object {$_ -match '^\s*\$foreground='})
if($line.Count -ne 1){throw 'Expected one foreground observation'}
$expression=[scriptblock]::Create($line[0])
foreach($case in @(
 @{name='focused captionless';windowed=$false;handle=1;active=1;minimized=$false;expected=$true},
 @{name='focused captioned';windowed=$true;handle=1;active=1;minimized=$false;expected=$true},
 @{name='other foreground';windowed=$false;handle=1;active=2;minimized=$false;expected=$false},
 @{name='minimized';windowed=$false;handle=1;active=1;minimized=$true;expected=$false},
 @{name='missing window';windowed=$false;handle=0;active=0;minimized=$false;expected=$false}
)){
 $h=[IntPtr]$case.handle;$windowed=$case.windowed
 [CombineStatusWindow]::Foreground=[IntPtr]$case.active
 [CombineStatusWindow]::Minimized=$case.minimized
 . $expression
 if($foreground -ne $case.expected){throw ('Foreground regression: '+$case.name)}
}
Write-Output 'PASS: status reports actual focus independently of caption style; missing/minimized/other windows refuse'
