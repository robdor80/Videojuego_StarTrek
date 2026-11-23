# H06 — Resultados de verificación

Fecha: 2026-11-13. Base `5f12d9c152dd0003a6d971068d693184f45b213e`. Código Unreal y CI ensayado `216e2cecd0dc5c21647e8f2fd33e0862023f333d`. Adaptador nativo `2b68bd16a6200a86b43d5b66d535e97a28c4eb9d`. CoreRPG limpio `76a7b7b485616d8c4994f384a90f123bf333591d`; jsoncons `bcb44594c50c495ee1e690602cdd71455942ad0e`. [PR #142 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/142) · [Implementación](H06_INFORME_IMPLEMENTACION_2026-11-13.md) · [Decisión G0](H06_DECISION_PROYECTO_UE_2026-11-13.md).

## MSI y Unreal

MSI Raider GE78 HX 14VGG, Windows 11 Pro 10.0.26200, MSVC 19.51.36256.0 x64, SDK 10.0.26100.0, CMake 4.4.3. Unreal Engine **5.8.2 CL 56702186**, D3D12 SM6 en NVIDIA GeForce RTX 4070 Laptop, driver 621.14 (32.0.16.2114). UE confirmó el adaptador NVIDIA elegido y la API activa dentro de la prueba. El escenario automatizado invoca botones Slate del viewport mediante `SButton::SimulateClick`; en D3D12 se ejecutó con ventana y render. El segundo UWorld inicia y termina su ciclo real de juego. La prueba de travel llama `UEngine::LoadMap` y verifica un UWorld nuevo con el mismo GameInstance, handle y generación.

El fixture H04 se preparó en otro proceso con el escritor nativo existente de H05. Se usó una raíz privada de ensayo distinta por ejecución. El fixture contiene una campaña local registrada con PERSON 3, nave 1, tick 28800 y orden completada 375/resultado 381. La vista UE compara identidad, nave, tick y revisión tras restaurar; la comparación del recibo y resultado Core se ejecutó en CTest nativo. La variante sin fixture abrió una campaña técnica y comprobó denegaciones de identidad, error de ruta y cierre.

| Ejecución local | Resultado | Evidencia en `laboratorios/host/h06/ue-product/` |
|---|---|---|
| Editor Development Win64, reconstrucción limpia | UBT/UHT PASS, 15,88 s. UHT escribió 8 archivos. | `rebuild-ubt-editor.log`, SHA-256 `2a99f0171b2bc5f8aa083e09ae262b8d387b7e2c948eba0ebf78daf9cf9bab55` |
| Game Development Win64, reconstrucción limpia | UBT/UHT PASS, 15,61 s. UHT escribió 8 archivos. | `rebuild-ubt-game.log`, SHA-256 `ed2d1fe55dd69582969ec11c52b6a993999494dcb30b3dec55ae2e2f622dd590` |
| Generación de mapa | PASS, 8 456 bytes, ruta de mapa predeterminada. Map Check del editor registró cero errores y advertencias. | `rebuild-map.log`, SHA-256 `744104275e23c19223c34065340d080e7448cc48755f344cad96e1044b5a0d04`; `editor-null.log` |
| `UnrealEditor-Cmd -game -nullrhi`, fixture | 1/1 PASS, 0 fallos/advertencias/omitidos, 0,285 s, pico de working set 1 025,3 MiB. | `null-verified-report/index.json`, SHA-256 `44732f9ed43cf401c2f2117befa87dd1bd7260095ded112a211de5dba4a49ec3` |
| `UnrealEditor-Cmd -game -d3d12`, fixture | 1/1 PASS, 0 fallos/advertencias/omitidos, 0,348 s, pico de working set 1 930,9 MiB. | `dx-verified-report/index.json`, SHA-256 `93d20621982adfc8d00834a005e7a0dcdcb726331d615c1c1e0ee02590b32a56` |
| Win64 cocinado y empaquetado, NullRHI, fixture | 1/1 PASS, 0 fallos/advertencias/omitidos, 0,206 s, pico de working set 278,3 MiB. | `pack-null-report/index.json`, SHA-256 `8b211d8deaad77880c2dfd99d468634b0e77fa07df1ab75eef7182d6904cf930` |
| Win64 cocinado y empaquetado, D3D12, fixture | 1/1 PASS, 0 fallos/advertencias/omitidos, 0,288 s, pico de working set 1 552,8 MiB. | `pack-dx-report/index.json`, SHA-256 `8af556a5287cd4f0e2d3449ca10d36553035329c2826febbbebb0ef41bd88886` |
| Juego en NullRHI reconstruido, raíz vacía | 1/1 PASS, 0 fallos/advertencias/omitidos, 0,005 s de test. | `rebuild-unbound-report/index.json`, SHA-256 `497b78d97600a9b22298c0f8fbe2e335a880a5ad6e910cda6a0c1f89792b0ce8` |

Las duraciones de automatización miden el escenario tras iniciar el juego, y las memorias son el pico del proceso. El primer arranque D3D12 con DDC frío empleó 149,09 s de inicialización, con compilación de shaders. El cook local procesó 197 paquetes de proyecto/motor en 184,57 s y el stage IoStore salió con código 0. El recibo UBT y el stage contienen las dos DLL NonUFS. El arranque empaquetado cargó ABI 1 y ejecutó OPEN/RESTORE con el Core fijado. SHA-256 del TrekHost empaquetado `1aba798bcabcc9ee1c85717eec28420b8a20a910b525320872a975aa76198dc0`; TrekF04Bridge `d38a6b103756d831e00f1f1c745c223b7ebd1549db401f74afe1f46ee883bbdd`. Los informes crudos quedan locales; esta tabla conserva las observaciones y hashes en GitHub.

## Regresión nativa

El [run 43495407748](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43495407748) verificó el commit Unreal indicado arriba. Se contrastaron los JUnit y logs de los cinco jobs. `host.abi.lifecycle` comprueba ABI, exclusividad, ausencia de identidad, tickets y CLOSE. `host.abi.roundtrip` comprueba recuperación del fixture, emisión/replay/cancelación, revisión caducada, publicación, ruta, LOAD y resultado Core. F11 y H01 se ejecutan en los dos jobs nativos.

| Entorno | Resultado | Evidencia |
|---|---|---|
| Windows MSVC 19.51.36260.0 | 238/238 PASS, 0 omitidos, 23,41 s | [JUnit y logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43495407748/artifacts/14071312799) |
| Ubuntu GCC 15.2.0 | 238/238 PASS, 0 omitidos, 11,99 s | [JUnit y logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43495407748/artifacts/14071821892) |
| Ubuntu Clang 21.1.8, ASan/UBSan C/C++ | 83/83 PASS, 0 omitidos, 11,37 s | [JUnit y logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43495407748/artifacts/14071877262) |
| Release OFF, Windows y Linux | PASS en ambos. ABI 1 negociada, carga, pin y exports inspeccionados. | [Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43495407748/artifacts/14071487010) · [Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43495407748/artifacts/14071741633) |
| F11 aislado y H01 documental | 17/17 F11 y 11/11 H01 por SO | `f11/tests.xml` y `h01.log` en los artefactos nativos |
| MSI, selección HOST nativa previa al módulo Unreal | 83/83 PASS, 8,67 s, SHA nativo final | JUnit `host-verified.xml`, SHA-256 `4b3c5e59f93b60a65f534f166df37d6c315082e31ec02332f99eb3ca1688e88f` |

## Matriz HU-01–HU-25

| Caso | Estado | Evidencia y alcance |
|---|---|---|
| HU-01 | PASS | Inventario, aprobación G0 y descriptor versionado. |
| HU-02 | PASS | Proyecto nuevo desde fuentes. Diff sin cambios en originales, labs históricos ni assets. |
| HU-03 | PASS | UBT/UHT Editor y Game Development x64 desde salidas apartadas. |
| HU-04 | PASS | Carga Release OFF en juego empaquetado, dos DLL NonUFS, Core pin verificado. |
| HU-05 | PASS | Consumidor C11, UBT C++ y negociación/carga ABI; tamaños fijos, datos copiados. |
| HU-06 | PASS | OPEN con generación activa, un handle de GameInstance compartido entre dos mundos; duplicado/exclusividad en CTest nativo. |
| HU-07 | PASS | Raíz limpia: `PRINCIPAL_UNBOUND` para vista y SAVE, con proyección vacía. |
| HU-08 | BLOCKED | Pendiente el bootstrap productivo de Academia. El fixture únicamente prueba el vínculo persistido recuperado por H04. |
| HU-09 | PASS | Con fixture, vista autorizada en Unreal, identidad y revisión iguales entre mundos. `host.m0.readonly` y `host.m0.observer` verifican invariancia y acceso en nativo. |
| HU-10 | BLOCKED | SUBMIT del jugador requiere G3. Emisión ISSUED real en C ABI con fixture nativo. |
| HU-11 | PASS | UI C++ y cabecera C sin recepción/ejecución, ningún UFUNCTION ni enlace directo a Core. Release OFF sin exports de ensayo. |
| HU-12 | BLOCKED | UI de órdenes pendiente. Stale y falta de competencia verificadas por CTest nativo. |
| HU-13 | PASS | SAVE desde Slate con fixture, confirmación H04 y marcador COMMITTED inspeccionado. |
| HU-14 | PASS | RESTORE desde Slate con fixture, generación nueva y vista preservada; la prueba nativa verifica además recibo y resultado Core. |
| HU-15 | PASS | Se deja una consulta del segundo mundo pendiente de entrega al solicitar LOAD; se invalida y su respuesta queda sin efecto. Generación antigua rechazada en ABI. |
| HU-16 | PASS | CLOSE con consulta pendiente revoca la vista y la generación. Travel destruye la proyección anterior con consulta pendiente; el proceso sale tras cerrar. |
| HU-17 | PASS | Dos UWorld simultáneos, dos proyecciones y una sesión con la misma identidad y revisión. |
| HU-18 | PASS | `UEngine::LoadMap` crea UWorld nuevo, invalida el panel anterior y permite consultar la misma sesión. |
| HU-19 | PASS | RESTORE con traversal devuelve PATH_REJECTED y conserva generación. El nativo comprueba también SAVE inválido y conservación de la ranura. |
| HU-20 | PASS | SERVICE_UNAVAILABLE en estado y panel, sin emisor ni trial F11. |
| HU-21 | PASS | Panel Slate accesible desde el viewport, callbacks en Game Thread y resultados por poll; sin join en `Deinitialize`. |
| HU-22 | PASS | NullRHI real en juego desde el editor y juego Win64 empaquetado. |
| HU-23 | PASS | D3D12 SM6 real en RTX 4070, interacción automatizada con Slate, cierre y recuperación en ambos ejecutables. |
| HU-24 | PASS | 238/238 Windows y Linux, 83/83 ASan/UBSan, Release OFF en ambos y regresiones F11/H01. |
| HU-25 | PASS | Medidas y ubicación en [implementación](H06_INFORME_IMPLEMENTACION_2026-11-13.md). Regeneración del mapa y build sin dependencia de archivos anteriores. |

## Reproducción nativa

Usar un destino nuevo para el CTest completo, porque las pruebas históricas F05 de persistencia exigen salidas nuevas. Ejecutar desde la raíz del repositorio. `$lab` es la ruta temporal autorizada de la ejecución; `$core` apunta al checkout limpio existente. El workflow enlazado conserva el comando de cada runner y la configuración ASan/UBSan.

```powershell
$env:TEMP = "$lab/tmp"
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
$env:F04_TEST_TEMP_ROOT = $env:TEMP
$env:PYTHONDONTWRITEBYTECODE = '1'
New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
cmake -S desarrollo/integration/host -B "$lab/native" -G 'Visual Studio 18 2026' -A x64 "-DCORERPG_SOURCE_DIR=$core" -DTREK_HOST_TESTS=ON
cmake --build "$lab/native" --config Release --parallel 3 --target host_abi_tests host_native_tests host_fault_tests host_persistence_tests host_m0_tests f04_tests f04_population_tests f04_history_faults f05_tests f05_delegation_tests f05_initiative_tests f05_ai_tests f05_integration_audit_tests
ctest --test-dir "$lab/native" -C Release -j 3 -R '^(host\.|f05\.|f04\.(history_faults|thread|scope|identity|class|buffers|determinism|population_.*|process_save|process_load)$)' --no-tests=error --output-on-failure --output-junit "$lab/native.xml"

cmake -S desarrollo/integration/host -B "$lab/product" -G 'Visual Studio 18 2026' -A x64 "-DCORERPG_SOURCE_DIR=$core" -DTREK_HOST_TESTS=OFF
cmake --build "$lab/product" --config Release --parallel 3 --target TrekHost
python desarrollo/integration/host/tests/inspect_product.py "$lab/product"
python desarrollo/integration/host/tests/inspect_abi.py "$lab/product"
```

En el MSI el segundo configure reutilizó `-DFETCHCONTENT_SOURCE_DIR_JSONCONS=$lab/native/_deps/jsoncons-src` tras confirmar el pin. Ambos DLLs están juntos en la salida Release de F04; la import lib de TrekHost queda en el directorio Release de HOST. Los JUnit locales quedan en el laboratorio. El smoke OFF carga y negocia la ABI sin ejecutables de test.

## Reproducción Unreal

Aplicar primero el [procedimiento de reconstrucción del proyecto](../../../../juego/UE5/StarTrekRPG/README.md). Los comandos siguientes usan `$engine` como instalación de UE 5.8.2, `$project` como ruta absoluta al descriptor y `$lab` como destino temporal autorizado. Usar un `$user` nuevo por pasada y conservar las variables TEMP y DDC del README. Para la prueba de apertura sin identidad, usar raíz vacía y omitir el argumento de fixture. Para la prueba positiva, `$writer` es el `host_m0_tests.exe` compilado con el CMake de HOST en modo tests ON.

```powershell
$root = Join-Path $user 'Saved/HostSlots'
New-Item -ItemType Directory -Path $root -Force | Out-Null
& $writer write $root
if ($LASTEXITCODE) { throw 'H04 fixture preparation failed' }
$campaign = Get-Content "$root/campaign-id" -Raw
$common = @('-unattended','-nop4','-nosound','-nosplash','-windowed','-resx=960','-resy=650',
    "-UserDir=$user","-H06FixtureCampaign=$campaign",
    '-ExecCmds=Automation RunTests StarTrek.H06.DiagnosticFlow',
    '-TestExit=Automation Test Queue Empty')
# Elegir -nullrhi o -d3d12 para $rhi, con destino nuevo por ejecución.
& "$engine/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" $project -game $rhi @common -NoZenAutoLaunch -ddc=NoZenLocalFallback "-AbsLog=$lab/game.log" "-ReportExportPath=$lab/game-report"
```

Para cook y stage IoStore, el cooker de 5.8.2 usa el directorio exacto que se le pasa. Se ejecutó primero el cook a disco y después el stage con la estructura por plataforma esperada por UAT. Los comandos equivalentes colocan el cook directamente bajo `Windows`.

```powershell
$uat = "$engine/Engine/Build/BatchFiles/RunUAT.bat"
$env:uebp_LogFolder = "$lab/uat"
& $uat BuildCookRun "-project=$project" -target=StarTrekRPG -platform=Win64 -clientconfig=Development -skipbuild -cook -unattended -nop4 -NoZenAutoLaunch -ddc=NoZenLocalFallback "-CookOutputDir=$lab/cooked/Windows" "-AdditionalCookerOptions=-NoZenAutoLaunch -ddc=NoZenLocalFallback -UserDir=$lab/user-cook"
& $uat BuildCookRun "-project=$project" -target=StarTrekRPG -platform=Win64 -clientconfig=Development -skipbuild -skipcook -stage -pak -iostore -nodebuginfo -unattended -nop4 -NoZenAutoLaunch "-CookOutputDir=$lab/cooked" "-stagingdirectory=$lab/staged"
$exe = "$lab/staged/Windows/StarTrekRPG/Binaries/Win64/StarTrekRPG.exe"
# Preparar $common con un $user nuevo y su fixture para cada modo.
& $exe $rhi @common "-AbsLog=$lab/packaged.log" "-ReportExportPath=$lab/packaged-report"
```

Comprobar que cada `index.json` contiene exactamente `StarTrek.H06.DiagnosticFlow`, estado Success, `succeeded=1`, `failed=0` y `notRun=0`. El proceso puede salir con código cero incluso si falla una aserción de Automation. La primera pasada se clasificó por el JSON y el log.

## Incidencias y límites

- ABI nativa inicial: se corrigió la aserción de layout por terminador y padding. En el primer CTest el nuevo oráculo de revisión comparaba instantes distintos. Se fijó la comparación en el instante de SAVE y se conservó el oráculo del resultado Core. Los 236 casos históricos pasaron en esa ejecución. El [run nativo anterior al módulo](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758) documenta la repetición.
- UBT exigió BuildSettings V7 en 5.8.2. Se corrigieron dependencias de includes, el guardado del mapa con flags `RF_Public | RF_Standalone` y la declaración reflejada del commandlet para Game. La primera recuperación desde UE falló por separadores de ruta: el adaptador UE convierte la raíz al formato nativo antes de entregarla a H04. H04 conserva su implementación y política.
- El cook inicial intentó usar Zen Store por defecto. Se configuró `bUseZenStore=False`; el segundo cook terminó correctamente y el stage separado exigió ubicar su salida bajo `Windows`. Se trasladó esa salida dentro de H06 y se obtuvo un solo paquete final. El editor standalone cargó el mapa y completó Map Check; el comando `Quit` no cerró ese primer smoke desatendido y se detuvo el proceso propio. Los cinco flujos de Automation de arriba exportaron resultados y cerraron.
- Los resultados UE positivos de persistencia y vista usan fixture explícito. Las órdenes del jugador productivo y los rechazos desde su UI siguen bloqueados por H03/Academia. Las pruebas automatizadas de D3D12 actuaron sobre los widgets reales, sin sesión de aceptación manual. H06 queda pendiente de auditoría independiente y M1 permanece parcial.
