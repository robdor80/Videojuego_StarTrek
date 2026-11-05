$ErrorActionPreference='Stop'
$base='C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\laboratorios\f05\p05b\20261105'
$RunnerDir="$base\w\desarrollo\integration\f05"
$Output="$base\w\laboratorios\f05\p05b\r1\clean-1"
$Pin='76a7b7b485616d8c4994f384a90f123bf333591d'
& 'C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
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

  $Dll=Join-Path $Output 'native/f04/Release/TrekF04Bridge.dll'
  & dumpbin /EXPORTS $Dll | Set-Content (Join-Path $Output 'logs/dll-exports.txt')
  if($LASTEXITCODE){throw 'dumpbin exports failed'}
  & dumpbin /DEPENDENTS $Dll | Set-Content (Join-Path $Output 'logs/dll-dependents.txt')
  if($LASTEXITCODE){throw 'dumpbin dependents failed'}
  $Headers=@((Join-Path $RunnerDir '../f04/include/f04_bridge.h'))+@(Get-ChildItem (Join-Path $RunnerDir 'include/f05_*.h') | ForEach-Object FullName)
  $Exports=@($Headers | ForEach-Object {[regex]::Matches((Get-Content $_ -Raw),'F04_API\s+(?:const\s+)?\w+(?:\s*\*)?\s+(f0[45]_\w+)\s*\(')} | ForEach-Object {$_.Groups[1].Value} | Sort-Object -Unique)
  if($Exports.Count -lt 30){throw 'Incomplete ABI export inventory'}
  $LoadedSha=[F05DllProbe]::Verify($Dll,$Exports)
  if($LoadedSha -ne $Pin){throw "Loaded DLL has wrong Core: $LoadedSha"}
  @{core=$LoadedSha;exports=$Exports;dll_sha256=(Get-FileHash $Dll -Algorithm SHA256).Hash} | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $Output 'logs/dll-load.json')

