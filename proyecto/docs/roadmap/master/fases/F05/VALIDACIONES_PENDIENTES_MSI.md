# Validaciones pendientes en MSI — F05-P01

Preparado en Codex Cloud el 2026-11-02. **No se ha ejecutado Unreal Engine
5.8.2 ni se ha accedido al MSI.** Los resultados nativos Linux/Windows de CI
no certifican Unreal, gráficos ni jugabilidad.

## Requisitos

- MSI encendido, Windows x64, UE **5.8.2** real, su SDK Win64 y toolchain C++
  compatible. Visual Studio 2026 Build Tools (o seleccionar otro generador
  CMake compatible), CMake >=3.25, Python 3, Git y PowerShell.
- Rama Star Trek `codex/f05-p01-orders` publicada y árbol limpio. CoreRPG en
  checkout separado del SHA `76a7b7b485616d8c4994f384a90f123bf333591d`.
  No cambiar directamente `main` ni sobrescribir cambios del propietario.
- Usar únicamente un directorio NUEVO en `laboratorios/f05/p01/` del repositorio
  Star Trek. No reutilizar ni borrar laboratorios anteriores. Estos archivos
  temporales están excluidos de Git y no son dependencia del producto.

## Comandos reproducibles

Ejecutar desde PowerShell en el repositorio Star Trek del propietario:

```powershell
$repo = 'C:/Users/andro/Documents/GitHub/Videojuego_StarTrek'
$core = 'C:/Users/andro/Documents/GitHub/CoreRPG'
$run = Join-Path $repo ('laboratorios/f05/p01/msi-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$corePin = Join-Path $run 'core-source'
New-Item -ItemType Directory -Force $run | Out-Null
# Este marcador identifica SOLO el nuevo directorio creado en estos comandos.
Set-Content (Join-Path $run '.f05-p01-generated') 'F05-P01 disposable generated files only'
git -C $core worktree add --detach $corePin 76a7b7b485616d8c4994f384a90f123bf333591d
if ($LASTEXITCODE) { throw 'No continuar sin checkout Core válido' }
Set-Location $repo
& ./desarrollo/integration/f05/run_f05.ps1 -Stage All -CoreSource $corePin -BuildRoot $run -EngineRoot 'C:/Program Files/Epic Games/UE_5.8'
```

Si la instalación real tiene otra ruta, ajustar `EngineRoot`; el script valida
su `Build.version` como 5.8.2. Si el generador difiere, pasar `-Generator` con el
nombre instalado. No adaptar el código al azar para otro motor.

Proyecto generado: `$run/ue/F05OrdersLab.uproject`. No usa proyectos ni recursos
artísticos del propietario. En caso de fallo, conservar logs y retomar con
`-Stage Native`, `Stage`, `Unreal` o `TestUnreal` sobre ese mismo directorio
marcado, sin repetir las fases ya satisfactorias. `Stage` requiere DLL/lib
nativas en `$run/native/f04/Release/`.

El script ejecuta estos pasos verificables:

```powershell
cmake -S "$repo/desarrollo/integration/f05" -B "$run/native" -G 'Visual Studio 18 2026' -A x64 "-DCORERPG_SOURCE_DIR=$corePin"
cmake --build "$run/native" --config Release --parallel 4
ctest --test-dir "$run/native" -C Release -R '^f05\.' --no-tests=error --output-on-failure
# Tras -Stage Stage:
& 'C:/Program Files/Epic Games/UE_5.8/Engine/Build/BatchFiles/Build.bat' F05OrdersLabEditor Win64 Development "-Project=$run/ue/F05OrdersLab.uproject" -WaitMutex -NoHotReload -MaxParallelActions=4
& 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe' "$run/ue/F05OrdersLab.uproject" -unattended -nop4 -nosplash -NullRHI -nosound -NoLiveCoding '-ExecCmds=Automation RunTests F05.P01' '-TestExit=Automation Test Queue Empty' "-ReportExportPath=$run/ue-report" -stdout -FullStdOutLogOutput
```

## Pendientes y criterio satisfactorio

| Validación pendiente | Por qué falta en Cloud | Resultado exigido |
| --- | --- | --- |
| MSVC y carga DLL en el MSI | CI Windows no reproduce SDK/instalación del propietario | Build Release y todos los CTest P01/regresiones seleccionadas con salida 0; pin Core exacto |
| UBT/UHT/editor UE 5.8.2 | Motor y licencia/instalación no disponibles en Cloud | `F05OrdersLabEditor` compila, carga `TrekF04Bridge.dll`, log `ready=1` y SHA esperado |
| `F05.P01.LifecycleAndRecovery` | Necesita proceso real Unreal | Emitir, recibir, ejecutar, guardar/restaurar y replay; futuro idéntico, tirada real, sin segunda ejecución |
| `F05.P01.Negatives` | Necesita ABI DLL dentro de Unreal | Denegación de autoridad, cualificación y operación no soportada; conflicto sin mutación |
| `F05.P01.WorldAndActorIndependence` | Necesita UWorld y Actor reales | Destruir Actor/UWorld conserva bytes; la orden se completa fuera de escena |
| Reapertura del harness sin caché anterior | No hay proceso UE en Cloud | Repetir en NUEVO `$run`, mismos 3 tests satisfactorios y ningún error de DLL/serialización |

El reporte `index.json` debe mostrar exactamente **3 pruebas F05.P01**
satisfactorias, `failed=0`, `notRun=0`; examinar cualquier advertencia y conservar
sus causas. NullRHI solo valida lógica y embedding, no calidad gráfica.

Abrir el harness con RHI real puede comprobar carga del editor, pero **P01 no
incluye una consola o escena jugable**; una pantalla vacía no demuestra órdenes
por interfaz. El recorrido jugable, diálogo y puente final requieren un encargo
posterior, sin convertir esta deuda en autorización de P02 ni de cambios de arte.

## Entrega de resultados locales

Conservar XML, logs y reportes brutos en el nuevo directorio temporal. Publicar
un resumen permanente de los comandos, versión exacta de motor/toolchain,
SHA Star Trek/Core, resultados y errores en la rama P01 mediante commit y PR
Draft existente. No forzar `laboratorios/` a Git. No modificar los informes
históricos para atribuirles estas ejecuciones nuevas.

El directorio completo es prescindible tras conservar el resumen; no es una
dependencia del juego. El worktree Core temporal debe desregistrarse mediante
`git worktree remove` solo con autorización de limpieza del propietario, sin
borrar ni mover fuentes o recursos preexistentes. **No fusionar PR.**
