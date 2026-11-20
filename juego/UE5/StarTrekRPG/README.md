# StarTrekRPG

Proyecto principal C++ Win64 para Unreal Engine **5.8.4** (asociación `5.8`). El mapa mínimo de H06 muestra el panel HOST. El panel usa una sesión por GameInstance y muestra exclusivamente la proyección autorizada del jugador. OPEN técnico queda `PRINCIPAL_UNBOUND`; la creación productiva de cadete sigue pendiente.

## Reconstruir desde Git

Requisitos: UE 5.8.4, toolchain Win64 reconocido por UBT, CMake, Python y un checkout limpio de CoreRPG en `76a7b7b485616d8c4994f384a90f123bf333591d`. Usar el checkout Core existente. El script comprueba el pin mediante el CMake de HOST y prepara el header C y las dos DLLs de Release. No cambiar el pin ni la arquitectura para abrir el editor. Git conserva el descriptor, configuración, fuentes y commandlet que genera el mapa; los binarios y recursos Unreal generados no están versionados.

Desde la raíz del repositorio en PowerShell, definir `$engine` como el directorio de instalación de UE (en este equipo `C:/Program Files/Epic Games/UE_5.8`), `$core` como el checkout limpio y `$work` como una ruta absoluta de salida de la ejecución conforme a `AGENTS.md`. Para ensayos usar una copia aislada del proyecto y hacer que `$project` apunte a esa copia. Invocar siempre el script del proyecto del repositorio: su ubicación determina dónde encontrar las fuentes HOST.

```powershell
$project = (Resolve-Path 'juego/UE5/StarTrekRPG/StarTrekRPG.uproject').Path
$projectDir = Split-Path -Parent $project
$version = Get-Content "$engine/Engine/Build/Build.version" -Raw | ConvertFrom-Json
if ("$($version.MajorVersion).$($version.MinorVersion).$($version.PatchVersion)" -ne '5.8.4') {
    throw 'Seleccionar la instalación UE 5.8.4.'
}
New-Item -ItemType Directory -Force "$work/tmp", "$work/user" | Out-Null
$env:TEMP = "$work/tmp"
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
[Environment]::SetEnvironmentVariable('UE-LocalDataCachePath', "$work/ddc", 'Process')

& juego/UE5/StarTrekRPG/Build/Prepare-Host.ps1 -CoreSource $core -BuildRoot "$work/native" -ProjectDir $projectDir
& "$engine/Engine/Build/BatchFiles/Build.bat" StarTrekRPGEditor Win64 Development "-Project=$project" -WaitMutex -NoHotReload -NoUBA -NoXGE -MaxParallelActions=3 "-Log=$work/ubt-editor.log"
if ($LASTEXITCODE) { throw 'Editor build failed.' }
& "$engine/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" $project -run=HostDiagnosticMap -nullrhi -unattended -nop4 -NoZenAutoLaunch -ddc=NoZenLocalFallback "-UserDir=$work/user" "-AbsLog=$work/map.log"
if ($LASTEXITCODE) { throw 'Diagnostic map generation failed.' }
& "$engine/Engine/Build/BatchFiles/Build.bat" StarTrekRPG Win64 Development "-Project=$project" -WaitMutex -NoHotReload -NoUBA -NoXGE -MaxParallelActions=3 "-Log=$work/ubt-game.log"
if ($LASTEXITCODE) { throw 'Game build failed.' }
```

Antes de UBT deben existir `Binaries/Host/include/trek/host/host_abi.h`, `Binaries/Host/TrekHost.dll` y `Binaries/Host/TrekF04Bridge.dll` en **el mismo proyecto que se va a abrir**. Una copia creada por la conversión de Unreal puede omitir `Binaries`; volver a ejecutar la preparación con `-ProjectDir` dirigido a esa copia. No copiar DLLs sueltas de procedencia desconocida. El header y los DLLs deben corresponder a la misma composición Release; ABI esperada: 1, x64. Las herramientas existentes `desarrollo/integration/host/tests/inspect_product.py` e `inspect_abi.py` validan la salida nativa con tests OFF.

El commandlet crea `Content/Diagnostics/HostDiagnostic.umap` si falta, sin sobrescribir uno existente. El mapa tiene un punto de entrada y usa el GameMode configurado. El mapa se regenera con Unreal y queda cubierto por la exclusión general de `*.umap`. UBT prepara las DLLs en `Binaries/Win64`; el empaquetado las conserva como NonUFS. La instalación del motor y las fuentes Core siguen fuera del proyecto.

## Abrir el editor para crear contenido

Cerrar antes las sesiones del proyecto si se va a recompilar. Para trabajar en la copia principal comprobar que `$project` termina en `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`, sin el sufijo de conversión `StarTrekRPG 5.8`.

```powershell
& "$engine/Engine/Binaries/Win64/UnrealEditor.exe" $project -d3d12 -windowed
```

Este comando abre el **editor**. El comando con `-game` de la sección siguiente ejecuta el juego de diagnóstico. No ofrece herramientas de creación de contenido.

El descriptor conserva `DisableEnginePluginsByDefault=true` y habilita explícitamente, solo para Editor, `ContentBrowserAssetDataSource`, `ContentBrowserClassDataSource`, `EngineAssetDefinitions`, `PropertyAccessEditor` y `PluginBrowser`. Proporcionan, respectivamente, carpetas y recursos al navegador, clases C++, las definiciones de recursos del motor (incluidos Blueprints y materiales), el soporte de compilación que necesitan UMG/animación y Editar > Complementos. Sin `PropertyAccessEditor` el diseñador de widgets puede cerrar el editor al compilar recursos internos. No desactivar estos plugins para reducir el proyecto mínimo. No se necesitan plugins de scripting para crear Blueprints, materiales o Widget Blueprints desde la interfaz.

En el navegador seleccionar **Contenido / Content** (`/Game`), limpiar búsqueda y filtros, y activar **Mostrar carpetas vacías** si se quieren ver directorios aún sin recursos. La raíz virtual **Todo / All**, las colecciones y las clases C++ no son destinos para crear recursos. Probar Añadir > Nueva carpeta, Clase Blueprint (Actor), Interfaz de usuario > Widget Blueprint y Material. Guardar y volver a abrir para comprobar persistencia.

Las carpetas físicas vacías pueden quedar ocultas; PNG/JPEG/MP3 copiados con Windows son fuentes y necesitan importarse para convertirse en recursos `.uasset`. Su presencia física no demuestra que el navegador tenga recursos registrados. Si incluso `/Game` y Editar > Complementos faltan, comprobar los plugins del descriptor y la ruta realmente abierta antes de reinstalar el motor o borrar cachés.

## Proteger el contenido de Unreal (fuera de Git)

**Importante:** `.gitignore` excluye deliberadamente los `.uasset`, `.umap` y otros binarios. Un commit o una PR no salva esos recursos. El proyecto definitivo se debe respaldar en **otra unidad física**, mediante snapshots de todo su directorio `Content`; no utilizar `laboratorios/` ni la misma unidad como única copia de seguridad.

Antes de empezar o terminar una sesión de importación/edición relevante, **guardar todo y cerrar Unreal Editor** para evitar archivos que cambien durante la copia. Elegir una carpeta en el HDD/SSD de respaldo existente, con espacio suficiente. El ejemplo siguiente emplea `X:` solo como marcador: reemplazarlo por la letra REAL de la unidad de respaldo.

Desde PowerShell en la raíz del repositorio:

```powershell
$projectDir = (Resolve-Path 'juego/UE5/StarTrekRPG').Path
& 'juego/UE5/StarTrekRPG/Build/Backup-Content.ps1' -ProjectDir $projectDir -DestinationRoot 'X:\Copias_StarTrekLegends\Unreal'
```

Cada ejecución crea un **snapshot nuevo** de todo `Content` (incluye mapas, widgets, Blueprints, materiales y recursos importados): `StarTrekRPG-Content-AAAAMMDD-HHMMSS-identificador/Content`, `manifest.json` con tamaño y SHA-256 por archivo y `COMPLETE.json` que certifica el manifiesto. Comprueba el origen antes/después de copiar y el destino. No sobrescribe ni borra snapshots previos. Si hay un fallo, conserva el directorio `.incomplete` y no lo considera respaldo válido. El script rechaza destinos en la misma unidad que el proyecto (separación por unidad; no certifica por sí sola que sean discos físicos distintos) y enlaces simbólicos dentro de `Content`.

Verificación periódica de una copia concreta, sin modificar nada:

```powershell
& 'juego/UE5/StarTrekRPG/Build/Verify-ContentBackup.ps1' -SnapshotDir 'X:\Copias_StarTrekLegends\Unreal\StarTrekRPG-Content-AAAAMMDD-HHMMSS-identificador'
```

**Restauración segura:** verificar primero el snapshot y copiar su `Content` **a una copia aislada del proyecto** para ensayar la apertura en UE; no sobreescribir el `Content` principal sin una revisión explícita de rutas y versiones. Si se recupera en otro equipo, el código y configuración proceden de Git, y las dependencias HOST se preparan de nuevo según este README. Las imágenes/audio originales que todavía estén **fuera** de `Content` requieren respaldo aparte.

**Límites:** las herramientas están versionadas, pero no generan copias hasta que alguien las ejecuta con una unidad de destino válida. No hay tarea programada ni copia automática instalada en el MSI. Antes de empezar la intro definitiva, ejecutar una primera copia después de importar sus recursos; repetirla al finalizar cada sesión importante. Conservar más de un snapshot y comprobar de vez en cuando una recuperación real en una copia aislada.

## Ejecutar el juego de diagnóstico

```powershell
& "$engine/Engine/Binaries/Win64/UnrealEditor.exe" $project -game -d3d12 -windowed
```

Abrir sesión técnica, consultar y cerrar desde el panel. Para recuperar, introducir el ID técnico de una campaña conocida por H04 y la ranura local. La raíz predeterminada se toma del directorio de aplicaciones del usuario y se puede aislar durante ensayos con `-UserDir`. H04 valida la dirección, el registro local y el vínculo persistido. SAVE requiere ese vínculo. El panel muestra el resultado de H04 cuando termina la operación y mantiene F11 como `SERVICE_UNAVAILABLE`.

La [matriz y los comandos de verificación H06](../../../proyecto/docs/architecture/host/H06_RESULTADOS_2026-11-13.md) documentan la automatización de interfaz, mundos, persistencia y RHI. Los proyectos de laboratorio y los recursos artísticos tienen sus propias rutas y su migración futura se controla por separado.
