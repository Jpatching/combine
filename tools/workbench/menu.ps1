param([string]$Image,[string]$Text)
$ErrorActionPreference='Stop'
function Get-CombineOfflineMenuCategory([string]$InputText) {
 $text=$InputText.ToUpperInvariant()
 $category='unknown'
 if($text -match '\b(ONLINE|MULTIPLAYER|SIGN IN|LOG IN|LOGIN)\b'){$category='login'}
 elseif($text -match '\bLOADING\b'){$category='loading'}
 elseif($text -match '\bSTART\b' -and $text -match '\bOPTIONS\b' -and $text -match '\bBACK\b' -and $text -match '\bSOCIAL\b' -and $text -notmatch '\bEPISODES\b'){$category='single-player-start-menu'}
 elseif($text -match '\bQUIT\b' -and ($text -replace '[^A-Z0-9]','') -match 'EPISODESFROMLIBERTYCITY' -and
     $text -notmatch '\b(START|OPTIONS|BACK|SOCIAL|LOADING)\b'){$category='offline-title-selector'}
 return $category
}
if($PSBoundParameters.ContainsKey('Text')){Write-Output ('MENU_CLASSIFICATION='+ (Get-CombineOfflineMenuCategory $Text));exit 0}
if(!$Image){throw 'Image required'}
trap {$_ | Out-String | Set-Content ($Image+'.error-private.txt');Write-Output 'MENU_CLASSIFICATION=unavailable';exit 2}
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Storage.FileAccessMode,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrEngine,Windows.Media.Ocr,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrResult,Windows.Media.Ocr,ContentType=WindowsRuntime]
$method=[System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {$_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetGenericArguments().Count -eq 1 -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'} | Select-Object -First 1
function Await($operation,[Type]$type){
 $task=$method.MakeGenericMethod($type).Invoke($null,@($operation))
 if(-not $task.Wait(10000)){throw 'Bounded OCR timeout'}
 return $task.Result
}
$file=Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Image)) ([Windows.Storage.StorageFile])
$stream=Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
try{
 $decoder=Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
 $bitmap=Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
 try{
  $engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
  if($null -eq $engine){throw 'No local OCR language'}
  $result=Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
  $result.Text | Set-Content ($Image+'.ocr-private.txt') -Encoding UTF8
  $category=Get-CombineOfflineMenuCategory $result.Text
  Write-Output ('MENU_CLASSIFICATION='+$category)
 }finally{if($null -ne $bitmap){$bitmap.Dispose()}}
}finally{$stream.Dispose()}
