param(
 [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{40}$')][string]$ExpectedTrekSha,
 [Parameter(Mandatory=$true)][string]$CoreSource,
 [Parameter(Mandatory=$true)][string]$BuildRoot,
 [Parameter(Mandatory=$true)][string]$EngineRoot,
 [string]$Generator='Visual Studio 18 2026'
)
$ErrorActionPreference='Stop'
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
$Allowed=Join-Path $Repo 'laboratorios'
if(!$IsWindows){throw 'P05B requires Windows on the owner MSI'}
if(!$BuildRoot.StartsWith($Allowed+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Choose a new laboratory under the repository'}
if(Test-Path -LiteralPath $BuildRoot){throw 'Choose a NEW directory; do not reuse or delete earlier laboratories'}
if($BuildRoot -match '[^\x00-\x7F]'){throw 'Use an ASCII output path for UBT/MSVC'}
$CoreSource=(Resolve-Path -LiteralPath $CoreSource).Path
$Head=(& git -C $Repo rev-parse HEAD).Trim()
if($LASTEXITCODE -or $Head -ne $ExpectedTrekSha){throw "Expected Star Trek $ExpectedTrekSha, got $Head"}
$Dirty=& git -C $Repo status --porcelain
if($LASTEXITCODE -or $Dirty){throw 'Star Trek checkout must be clean'}
$Pin=(Get-Content (Join-Path $PSScriptRoot 'core-revision.txt') -Raw).Trim()
$Actual=(& git -C $CoreSource rev-parse HEAD).Trim()
if($LASTEXITCODE -or $Actual -ne $Pin){throw "Expected Core $Pin, got $Actual"}
& git -C $CoreSource diff --exit-code HEAD
if($LASTEXITCODE){throw 'Core tracked sources must be clean'}
$Version=Get-Content (Join-Path $EngineRoot 'Engine/Build/Build.version') -Raw | ConvertFrom-Json
if($Version.MajorVersion -ne 5 -or $Version.MinorVersion -ne 8 -or $Version.PatchVersion -ne 2){throw 'Actual UE 5.8.2 is required'}
foreach($Tool in @('cmake','ctest','python','dumpbin')){Get-Command $Tool -ErrorAction Stop | Out-Null}
New-Item -ItemType Directory $BuildRoot | Out-Null
$Record=[ordered]@{result='INCOMPLETE';hardware_rhi_acceptance='PENDIENTE_REVISION_LOGS';final_certification='PENDIENTE_ACTA';utc=[DateTime]::UtcNow.ToString('o');computer=$env:COMPUTERNAME;trek=$Head;core=$Pin;engine=$Version;runs=@()}
$Record | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $BuildRoot 'acceptance.json')
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber | ConvertTo-Json | Set-Content (Join-Path $BuildRoot 'windows.json')

# Actually load the DLL and resolve all public ABI exports, without UE or model API.
if(!('F05DllProbe' -as [type])){
 Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class F05DllProbe {
 [DllImport("kernel32", CharSet=CharSet.Unicode, SetLastError=true)] static extern IntPtr LoadLibraryExW(string p,IntPtr f,uint flags);
 [DllImport("kernel32", CharSet=CharSet.Ansi, ExactSpelling=true)] static extern IntPtr GetProcAddress(IntPtr h,string n);
 [DllImport("kernel32")] static extern bool FreeLibrary(IntPtr h);
 [UnmanagedFunctionPointer(CallingConvention.Cdecl)] delegate IntPtr CoreSha();
 public static string Verify(string p,string[] names) {
  IntPtr h=LoadLibraryExW(p,IntPtr.Zero,8);
  if(h==IntPtr.Zero)throw new Exception("LoadLibraryExW failed: "+Marshal.GetLastWin32Error());
  try {
   foreach(string n in names)if(GetProcAddress(h,n)==IntPtr.Zero)throw new Exception("Missing export: "+n);
   var get=(CoreSha)Marshal.GetDelegateForFunctionPointer(GetProcAddress(h,"f04_core_sha"),typeof(CoreSha));
   return Marshal.PtrToStringAnsi(get());
  } finally {FreeLibrary(h);}
 }
}
'@
}
try {
 foreach($Iteration in 1..2){
  $Output=Join-Path $BuildRoot "clean-$Iteration"
  & python (Join-Path $PSScriptRoot 'run_integration_audit.py') --suite core --core-source $CoreSource --output (Join-Path $BuildRoot "core-$Iteration") --generator $Generator
  if($LASTEXITCODE){throw "Full Core suite failed on run $Iteration"}
  & (Join-Path $PSScriptRoot 'run_f05.ps1') -Stage Native -Suite All -CoreSource $CoreSource -BuildRoot $Output -Generator $Generator
  $NativeReport=@(Get-ChildItem $Output -Filter '*-native.xml')
  if($NativeReport.Count -ne 1){throw 'One complete native JUnit is required in each clean run'}
  [xml]$NativeXml=Get-Content $NativeReport[0].FullName -Raw
  $Cases=@($NativeXml.testsuite.testcase)
  if($Cases.Count -ne 395 -or @($Cases | Where-Object {$_.status -ne 'run' -or $_.failure -or $_.error -or $_.skipped}).Count){throw 'All 395 F04/F05 native tests must actually pass, including 30 P05A cases'}
  $Dll=Join-Path $Output 'native/f04/Release/TrekF04Bridge.dll'
  & dumpbin /EXPORTS $Dll | Set-Content (Join-Path $Output 'logs/dll-exports.txt')
  if($LASTEXITCODE){throw 'dumpbin exports failed'}
  & dumpbin /DEPENDENTS $Dll | Set-Content (Join-Path $Output 'logs/dll-dependents.txt')
  if($LASTEXITCODE){throw 'dumpbin dependents failed'}
  $Headers=@((Join-Path $PSScriptRoot '../f04/include/f04_bridge.h'))+@(Get-ChildItem (Join-Path $PSScriptRoot 'include/f05_*.h') | ForEach-Object FullName)
  $Exports=@($Headers | ForEach-Object {[regex]::Matches((Get-Content $_ -Raw),'F04_API\s+(?:const\s+)?\w+(?:\s*\*)?\s+(f0[45]_\w+)\s*\(')} | ForEach-Object {$_.Groups[1].Value} | Sort-Object -Unique)
  if($Exports.Count -lt 30){throw 'Incomplete ABI export inventory'}
  $LoadedSha=[F05DllProbe]::Verify($Dll,$Exports)
  if($LoadedSha -ne $Pin){throw "Loaded DLL has wrong Core: $LoadedSha"}
  @{core=$LoadedSha;exports=$Exports;dll_sha256=(Get-FileHash $Dll -Algorithm SHA256).Hash} | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $Output 'logs/dll-load.json')
  foreach($Stage in @('Stage','Unreal','TestUnreal')){
   & (Join-Path $PSScriptRoot 'run_f05.ps1') -Stage $Stage -Suite All -CoreSource $CoreSource -BuildRoot $Output -EngineRoot $EngineRoot
  }
  & (Join-Path $PSScriptRoot 'run_f05.ps1') -Stage TestUnreal -Suite All -RealRHI -CoreSource $CoreSource -BuildRoot $Output -EngineRoot $EngineRoot
  $Record.runs+=@{iteration=$Iteration;result='PASS';output="clean-$Iteration";real_rhi=$true}
  $Record | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $BuildRoot 'acceptance.json')
 }
 $Record.result='PASS_AUTOMATED'
} finally {
 $Record | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $BuildRoot 'acceptance.json')
 Get-ChildItem $BuildRoot -Recurse -File | Where-Object {$_.Extension -in @('.log','.xml','.json','.txt') -and $_.FullName -notmatch '[\\/](_deps|CMakeFiles)[\\/]'} |
  Get-FileHash -Algorithm SHA256 | Select-Object Path,Hash | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $BuildRoot 'evidence-sha256.json')
}
