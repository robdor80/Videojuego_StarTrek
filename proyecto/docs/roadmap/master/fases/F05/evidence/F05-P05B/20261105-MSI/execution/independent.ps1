$ErrorActionPreference='Stop'
$base='C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\laboratorios\f05\p05b\20261105'
Set-Location "$base\w"
Start-Transcript "$base\independent-checks.log"
try {
 & 'C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
 $output="$base\w\laboratorios\f05\p05b\r1\clean-1"
 & ./desarrollo/integration/f05/run_f05.ps1 -Stage Native -Suite All -CoreSource "$base\c" -BuildRoot $output -Generator 'Visual Studio 18 2026'
 foreach($stage in @('Stage','Unreal','TestUnreal')) {
  & ./desarrollo/integration/f05/run_f05.ps1 -Stage $stage -Suite All -CoreSource "$base\c" -BuildRoot $output -EngineRoot 'C:\Program Files\Epic Games\UE_5.8'
 }
 & ./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite All -RealRHI -CoreSource "$base\c" -BuildRoot $output -EngineRoot 'C:\Program Files\Epic Games\UE_5.8'
} finally {Stop-Transcript}
