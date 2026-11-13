# H06 — Resultados de verificación

Fecha: 2026-11-13. Base `5f12d9c152dd0003a6d971068d693184f45b213e`. Código final `2b68bd16a6200a86b43d5b66d535e97a28c4eb9d`. Configuración CI final `517b5adcb8d99a93dfa7ce81c698a74abfd5d6e2`. CoreRPG limpio `76a7b7b485616d8c4994f384a90f123bf333591d`; jsoncons `bcb44594c50c495ee1e690602cdd71455942ad0e`. [PR #142 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/142) · [Implementación](H06_INFORME_IMPLEMENTACION_2026-11-13.md) · [Decisión G0](H06_DECISION_PROYECTO_UE_2026-11-13.md).

## Ejecuciones

MSI Windows 11 Pro 10.0.26200, MSVC 19.51.36256.0 x64, SDK 10.0.26100.0, CMake 4.4.3, VS 18 2026, Python 3.10.11. Unreal 5.8.2 CL 56702186 instalado. Los resultados siguientes usan el ejecutable C, CTest y el cargador del SO. La ejecución UE, la prueba de memoria dentro del motor y las mediciones RHI siguen pendientes. La RAM física está registrada en el inventario G0.

| Entorno y ejecución | Resultado | Evidencia |
|---|---|---|
| MSI Windows x64, selección HOST final, CTest Release ON | 83/83 PASS, 0 FAIL, 0 omitidos, 8,67 s. SHA de código final. | JUnit local `host-verified.xml`, SHA-256 `4b3c5e59f93b60a65f534f166df37d6c315082e31ec02332f99eb3ca1688e88f`. |
| MSI Windows x64, Release OFF, C ABI y pin cargados | PASS, dos inspecciones. SHA de código final. | `product-inspection.log`, `product-abi.log`. TrekHost.dll 202 240 bytes, SHA-256 `1aba798bcabcc9ee1c85717eec28420b8a20a910b525320872a975aa76198dc0`. TrekF04Bridge.dll 924 160 bytes, SHA-256 `e5a2d58730a14ea49965f547185bc6879261cdaab9d8bd8479a4aeb052b12a63`. |
| Ubuntu 26.04.1, GCC 15.2.0, Release ON | 238/238 PASS, 0 FAIL, 0 omitidos, 15,32 s. | [Job](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/job/132103921311) · [JUnit y logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/artifacts/14069575830) |
| Windows runner 10.0.26100, MSVC 19.51.36260.0, Release ON | 238/238 PASS, 0 FAIL, 0 omitidos, 25,25 s. | [Job](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/job/132103921305) · [JUnit y logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/artifacts/14067978789) |
| Ubuntu 26.04.1, Clang 21.1.8, ASan/UBSan C/C++ | 83/83 PASS, 0 FAIL, 0 omitidos, 14,00 s. Sin diagnóstico sanitizador. | [Job](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/job/132103921137) · [JUnit y logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/artifacts/14068721427) |
| Linux Release OFF, GCC 15.2.0 | PASS, exports, dependencias, pin, carga y negociación C. | [Job](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/job/132103920796) · [Logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/artifacts/14068661332) |
| Windows Release OFF, MSVC 19.51.36260.0 | PASS, exports, dependencias, pin, carga y negociación C. | [Job](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/job/132103921294) · [Logs](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758/artifacts/14068666374) |
| F11 aislado y H01 documental | 17/17 F11 y 11/11 H01 por SO. H01 local 11/11. | `f11/tests.xml`, `f11/run.json` y `h01.log` en los dos artefactos nativos. |

El [run nativo final](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488721758) usa `517b5adcb8d99a93dfa7ce81c698a74abfd5d6e2`, que añade el smoke C al job Windows OFF sin cambiar el código de producto. Se contrastaron artefactos y JUnit. Los 238 casos incluyen 83 HOST, 134 F05 y 21 F04. H01 y F11 se ejecutan en los dos jobs nativos y quedan fuera de la selección de sanitizadores. La memoria por caso queda sin medición. El workflow terminó con cinco jobs correctos. El [run precedente](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43488002379) ya pasó los cinco jobs sobre el SHA de código final.

La evidencia CTest incluye `host.abi.lifecycle` y `host.abi.roundtrip`. En el segundo, `host_m0_tests write` crea una ranura H04 local en proceso independiente. El consumidor enlaza solo TrekHost. Recupera el fixture PERSON 3, campaña tick 28800, orden 375 y resultado Core 381 con tirada 99. Prueba reenvío idempotente, rechazo stale, emisión/cancelación reales, SAVE con marcador COMMITTED, error de ruta, RESTORE con nueva generación, rechazo de mutación antigua y expiración de resultados retenidos tras RESTORE/CLOSE. Los oráculos históricos H05, ejecutados en esta rama, verifican además bytes, competencia, observador y RNG.

## Matriz HU-01–HU-25

La columna estado corresponde al oráculo completo de la matriz H06. Cada evidencia parcial queda acotada al SHA y entorno de la sección de ejecuciones.

| Caso | Estado | Evidencia |
|---|---|---|
| HU-01 | BLOCKED | Inventario remoto/local y README comprobados. Falta la elección aprobada. |
| HU-02 | PASS | Diff acotado a HOST/CI e informes. Descriptores, laboratorios históricos, assets y originales fuera del diff. |
| HU-03 | BLOCKED | Proyecto principal pendiente. UBT/UHT Editor y Game pendientes. |
| HU-04 | BLOCKED | Release OFF y carga nativa de ambas bibliotecas, pin y dependencias comprobados. Falta carga desde staging UE. |
| HU-05 | BLOCKED | C11 y C++20 comprueban layout. PASS nativo de versión/tamaños/ownership/errores y exports C. Compilación UBT pendiente. |
| HU-06 | BLOCKED | `host.abi.lifecycle` comprueba OPEN, duplicado, exclusividad entre dos clientes y reapertura. Falta GameInstance. |
| HU-07 | BLOCKED | `host.abi.lifecycle` comprueba PRINCIPAL_UNBOUND en estado, vista, orden y SAVE; resultados vacíos. Falta arranque UE. |
| HU-08 | BLOCKED | H04 restaura el vínculo H03 del fixture. El bootstrap productivo del cadete sigue pendiente. |
| HU-09 | BLOCKED | `host.abi.roundtrip` copia la vista autorizada; `host.m0.readonly` y `host.m0.observer` pasan oráculos de bytes y acceso en nativo. Falta UE. |
| HU-10 | BLOCKED | Emisión ISSUED y replay/cancelación mediante ABI probados con identidad de fixture. Falta vía de identidad productiva y UE. |
| HU-11 | BLOCKED | La superficie C excluye receptor/ejecutor y el producto OFF carece de hooks HOST y diagnósticos F04 de ensayo. Falta verificación de Blueprint. |
| HU-12 | BLOCKED | REVISION_STALE comprobado por ABI; `host.m0.authority` verifica falta de competencia y REFUSED sin intento/RNG. Falta UI. |
| HU-13 | BLOCKED | CTest roundtrip confirma SAVE tras H04 y verifica COMMITTED. Falta UI. |
| HU-14 | BLOCKED | Roundtrip nativo recupera generación, identidad, revisión, reloj y resultado del fixture. Falta UE. |
| HU-15 | BLOCKED | Ticket de vista retenido hasta después de RESTORE devuelve GENERATION_EXPIRED; la ABI rechaza consulta y mutación con token anterior. Falta callback HUD. |
| HU-16 | BLOCKED | CLOSE admite ranura reservada con todas las observaciones ocupadas; ticket de orden previamente autorizado caduca. Join comprobado en nativo. Falta destrucción de UObject. |
| HU-17 | BLOCKED | Exclusividad nativa comprobada con dos clientes. Falta prueba real con dos UWorld. |
| HU-18 | BLOCKED | Falta map travel del proyecto principal. |
| HU-19 | BLOCKED | CTest roundtrip rechaza traversal y ranura ausente; conserva generación y permite SAVE/RESTORE posterior. Falta prueba UE. |
| HU-20 | PASS | Capacidad SERVICE_UNAVAILABLE observada por C y ctypes; ausencia de emisor y trial de F11 en producto, y `host.m0.institutional` ejecutada. |
| HU-21 | BLOCKED | Panel y despacho al Game Thread pendientes de G0. |
| HU-22 | NOT_RUN | UE 5.8.2 disponible. Falta proyecto autorizado y suite de editor/juego. |
| HU-23 | NOT_RUN | GPU y driver disponibles. Falta proyecto autorizado e interacción D3D12 real. |
| HU-24 | PASS | CTest Windows/Linux/ASan y Release OFF de acuerdo con ejecuciones de arriba. |
| HU-25 | PASS | Medidas y cinco carpetas mayores en informe de implementación. El diff solo versiona entregables permanentes; el laboratorio no es requisito del producto. |

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

## Unreal tras G0

Esquema de comandos para el MSI una vez creados y aprobados el descriptor, los targets, el módulo, el staging y la suite. `$engine` apunta al motor 5.8.2 existente, `$project` al descriptor definitivo, `$lab` a los temporales autorizados y `$map` al mapa de diagnóstico. Definir el prefijo de automatización al implementar el módulo.

```powershell
& "$engine/Engine/Build/BatchFiles/Build.bat" StarTrekRPGEditor Win64 Development "-Project=$project" -WaitMutex
& "$engine/Engine/Build/BatchFiles/Build.bat" StarTrekRPG Win64 Development "-Project=$project" -WaitMutex
& "$engine/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" $project -unattended -nullrhi "-ExecCmds=Automation RunTests $suite" '-TestExit=Automation Test Queue Empty' "-ReportExportPath=$lab/nullrhi" "-AbsLog=$lab/nullrhi.log"
& "$engine/Engine/Binaries/Win64/UnrealEditor.exe" $project $map -game -d3d12 -log "-AbsLog=$lab/d3d12.log"
```

Registrar UBT/UHT, dependencia y carga de DLL del juego empaquetado, entorno RHI, tests de actores/mundos y captura de interacción con el diagnóstico. En D3D12 comprobar cierre y recuperación con una ranura H04 autorizada. La creación de campaña vinculada queda condicionada al bootstrap productivo.

## Incidencias

- Primera compilación local: dos aserciones de layout fallaron por el byte NUL del ID de campaña y la alineación a ocho bytes. El layout v1 publicado se fijó en 120 bytes para la respuesta con payload en offset 72 y se verificó en C y C++.
- Primera suite local, 237/238 en 16,57 s. El nuevo oráculo comparaba la revisión global de la consulta con una tomada antes de emitir y cancelar otras órdenes. F05 devuelve la revisión de campaña actual junto al recibo. Se corrigió la referencia al instante de SAVE y se mantuvo una comprobación independiente de ID y valor de la tirada. Los 236 casos históricos pasaron en esa primera ejecución. La repetición HOST final y CI se detallan arriba.
- La revisión de la composición heredada encontró `f04_history_test_delta` y `f04_history_test_validate_full` en la biblioteca F04 de producto H05. Se conserva la flag para los ensayos históricos y se retira de la composición HOST con tests OFF. Se verificó por carga dinámica. Las fuentes y pruebas F04 siguen intactas.

**M1 parcial y bloqueado.** Falta la decisión sobre el proyecto principal y la integración UE, incluida la evidencia NullRHI/D3D12. La aprobación y auditoría independiente quedan pendientes.
