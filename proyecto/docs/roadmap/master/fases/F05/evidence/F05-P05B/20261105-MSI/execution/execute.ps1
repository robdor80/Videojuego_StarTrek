$ErrorActionPreference='Stop'
$base='C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\laboratorios\f05\p05b\20261105'
Set-Location "$base\w"
Start-Transcript -Path "$base\execution.log"
try {
 & 'C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
 [ordered]@{utc=[DateTime]::UtcNow.ToString('o');powershell=$PSVersionTable.PSVersion.ToString();computer=$env:COMPUTERNAME;gpu=@(Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion,Status);disks=@(Get-PSDrive -PSProvider FileSystem | Select-Object Name,Free,Used);tools=@(Get-Command cmake,ctest,python,cl,dumpbin | Select-Object Name,Source);sdk=$env:WindowsSDKVersion;msvc=$env:VCToolsVersion} | ConvertTo-Json -Depth 6 | Set-Content "$base\environment.json"
 & cl 2>&1 | Out-Host
 & cmake --version
 & python --version
 & ./desarrollo/integration/f05/run_p05b_msi.ps1 -ExpectedTrekSha 486099abd36c18c5ee69c38cd43a95b95910cc5f -CoreSource "$base\c" -BuildRoot "$base\w\laboratorios\f05\p05b\r1" -EngineRoot 'C:\Program Files\Epic Games\UE_5.8' -Generator 'Visual Studio 18 2026'
} finally { Stop-Transcript }
