param([Parameter(Mandatory=$true)][string]$Script)
$ErrorActionPreference='Stop'
$project=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'UnrealEditor*' -and $_.CommandLine -like "*$project*" }) {
    throw 'El proyecto ya esta abierto: no se permite escritura concurrente.'
}
$scriptPath=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot $Script)).Path
$log=Join-Path $project ('Saved\F07_Sutherland_Audit\Codex_Full_Bridge\'+[IO.Path]::GetFileNameWithoutExtension($Script)+'.log')
$arguments=@('"'+$project+'\f07sutherland.uproject"','/Game/maps/L_F07_Sutherland_Test','-ExecutePythonScript="'+$scriptPath+'"','-EnablePlugins=PythonScriptPlugin,GeometryScripting,ProceduralMeshComponent','-unattended','-nop4','-nosplash','-nullrhi','-NoSound','-abslog="'+$log+'"')
$process=Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $arguments -WindowStyle Hidden -PassThru
$process.WaitForExit()
Write-Output "UE exit=$($process.ExitCode); log=$log"
