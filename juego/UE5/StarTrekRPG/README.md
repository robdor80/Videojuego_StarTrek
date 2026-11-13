# StarTrekRPG

Proyecto principal C++ Win64 aprobado para Unreal Engine **5.8.2**. El mapa mínimo de H06 muestra el panel HOST. El panel usa una sesión por GameInstance y muestra exclusivamente la proyección autorizada del jugador. OPEN técnico queda `PRINCIPAL_UNBOUND`; la creación productiva de cadete sigue pendiente.

## Reconstruir desde Git

Requisitos: UE 5.8.2, toolchain Win64 reconocido por UBT, CMake, Python y un checkout limpio de CoreRPG en `76a7b7b485616d8c4994f384a90f123bf333591d`. Usar el checkout Core existente. El script comprueba el pin mediante el CMake de HOST y prepara el header C y las dos DLLs de Release. Git conserva el descriptor, configuración, fuentes y commandlet que genera el mapa.

Desde la raíz del repositorio en PowerShell, definir `$engine` como el directorio de instalación de UE, `$core` como el checkout limpio y `$work` como una ruta absoluta de salida de la ejecución. El workflow local usa un directorio temporal conforme a AGENTS.

```powershell
$project = (Resolve-Path 'juego/UE5/StarTrekRPG/StarTrekRPG.uproject').Path
New-Item -ItemType Directory -Force "$work/tmp", "$work/user" | Out-Null
$env:TEMP = "$work/tmp"
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
[Environment]::SetEnvironmentVariable('UE-LocalDataCachePath', "$work/ddc", 'Process')

& juego/UE5/StarTrekRPG/Build/Prepare-Host.ps1 -CoreSource $core -BuildRoot "$work/native"
& "$engine/Engine/Build/BatchFiles/Build.bat" StarTrekRPGEditor Win64 Development "-Project=$project" -WaitMutex -NoHotReload -NoUBA -NoXGE -MaxParallelActions=3 "-Log=$work/ubt-editor.log"
& "$engine/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" $project -run=HostDiagnosticMap -nullrhi -unattended -nop4 -NoZenAutoLaunch -ddc=NoZenLocalFallback "-UserDir=$work/user" "-AbsLog=$work/map.log"
& "$engine/Engine/Build/BatchFiles/Build.bat" StarTrekRPG Win64 Development "-Project=$project" -WaitMutex -NoHotReload -NoUBA -NoXGE -MaxParallelActions=3 "-Log=$work/ubt-game.log"
```

El commandlet crea `Content/Diagnostics/HostDiagnostic.umap` si falta. El mapa tiene un punto de entrada y usa el GameMode configurado. El mapa se regenera con Unreal y queda cubierto por la exclusión general de `*.umap`. UBT prepara las DLLs en `Binaries/Win64`; el empaquetado las conserva como NonUFS. La instalación del motor y las fuentes Core siguen fuera del proyecto.

## Abrir el diagnóstico

```powershell
& "$engine/Engine/Binaries/Win64/UnrealEditor.exe" $project -game -d3d12 -windowed
```

Abrir sesión técnica, consultar y cerrar desde el panel. Para recuperar, introducir el ID técnico de una campaña conocida por H04 y la ranura local. La raíz predeterminada se toma del directorio de aplicaciones del usuario y se puede aislar durante ensayos con `-UserDir`. H04 valida la dirección, el registro local y el vínculo persistido. SAVE requiere ese vínculo. El panel muestra el resultado de H04 cuando termina la operación y mantiene F11 como `SERVICE_UNAVAILABLE`.

La [matriz y los comandos de verificación H06](../../../proyecto/docs/architecture/host/H06_RESULTADOS_2026-11-13.md) documentan la automatización de interfaz, mundos, persistencia y RHI. Los proyectos de laboratorio y los recursos artísticos tienen sus propias rutas y su migración futura se controla por separado.
