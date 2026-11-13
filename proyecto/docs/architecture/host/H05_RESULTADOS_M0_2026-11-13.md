# H05 — Resultados verificables del ciclo M0

Fecha: 2026-11-13. Código final `0b022b1188b0a3490441af0769fffcefdc6f8ce0`,
base `cf8fffe755ba04cf66ed09042858ec923d7b100b`. CoreRPG limpio
`76a7b7b485616d8c4994f384a90f123bf333591d`; jsoncons histórico
`bcb44594c50c495ee1e690602cdd71455942ad0e`. Ver las decisiones e inventario en
[informe de implementación](H05_INFORME_IMPLEMENTACION_2026-11-13.md).

## Ejecuciones y clasificación

Código final en [PR #139 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/139).
CI de código: [HOST H02–H05, run 43467528745](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745),
sobre `0b022b1188b0a3490441af0769fffcefdc6f8ce0`;
[H01 independiente](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528739).
La publicación final de estos informes solo modifica Markdown; los SHA ensayados
se identifican por fila, sin atribuirles el SHA futuro de su propia documentación.

| Entorno/suite | PASS | FAIL | SKIP/NOT_RUN | Estado |
|---|---:|---:|---:|---|
| Linux GCC 14.2, M0 nativo final (`0b022b11`) | 26 | 0 | 0 | PASS; ciclo real completado y pendiente entre procesos |
| Linux GCC, H02–H05/F04/F05 limpio (`5ee7b169`) | 235 | 0 | 0 | PASS; 80 HOST, 134 F05, 21 F04; 31,07 s |
| Linux GCC, HOST tras añadir RESOLVING (`0f753ad1`) | 81 | 0 | 0 | PASS; 26 M0 + 55 históricos; 5,96 s |
| Linux Release OFF, carga y símbolos | 1 | 0 | 0 | PASS sobre `0b022b11`; carga, exports, dependencias y pin |
| Linux F11 aislada | 17 | 0 | 0 | PASS; fuentes F11 no vinculadas a TrekHost |
| H01 documental | 11 | 0 | 0 | PASS |
| CI Ubuntu 26.04.1 / GCC 15.2 (`0b022b11`) | 236 | 0 | 0 | PASS; 81 HOST, 134 F05, 21 F04; 13,32 s |
| CI Windows 10.0.26100 / MSVC 19.51.36260.0 (`0b022b11`) | 236 | 0 | 0 | PASS; 81 HOST, 134 F05, 21 F04; 23,88 s |
| CI Ubuntu / Clang 21.1.8 ASan+UBSan (`0b022b11`) | 81 | 0 | 0 | PASS; HOST completo, sin diagnóstico sanitizador; 13,63 s |
| CI Linux Release OFF (`0b022b11`) | 1 | 0 | 0 | PASS; carga/exports/dependencias y pin |
| CI Windows Release OFF (`0b022b11`) | 1 | 0 | 0 | PASS; carga/exports/dependencias y pin |
| CI F11 Linux aislada (`0b022b11`) | 17 | 0 | 0 | PASS |
| CI F11 Windows aislada (`0b022b11`) | 17 | 0 | 0 | PASS |
| CI H01 Linux y Windows (`0b022b11`) | 11 + 11 | 0 | 0 | PASS |
| MSI/UE/D3D12/NullRHI/corte eléctrico físico | 0 | 0 | NOT_RUN | Fuera de H05 |

Los pasos H01/F11 del job de sanitizadores están SKIP por diseño: se ejecutan
en los dos jobs nativos. Ninguna prueba CTest de la ejecución final se omite.
Clang local es NOT_RUN; Clang CI es PASS. Los productos no ejecutan CTest: su
unidad de validación es la compilación Release OFF y la carga/inspección real.

## Enlaces de CI y artefactos

Todos estos jobs ensayan `0b022b1188b0a3490441af0769fffcefdc6f8ce0`:

| Job | Estado | Artefacto |
|---|---|---|
| [GCC Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/job/132030519353) | PASS | [host-h05-ubuntu-latest-native](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/artifacts/14058103599) |
| [MSVC Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/job/132030519432) | PASS | [host-h05-windows-latest-native](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/artifacts/14058799395) |
| [Clang ASan/UBSan](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/job/132030519853) | PASS | [host-h05-ubuntu-latest-asan-ubsan](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/artifacts/14058733948) |
| [Producto Linux OFF](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/job/132030518973) | PASS | [host-h05-product-linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/artifacts/14058808258) |
| [Producto Windows OFF](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/job/132030519421) | PASS | [host-h05-product-windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745/artifacts/14059651678) |

Los artefactos nativos incluyen `native.xml`, `tests.log`, revisiones, compilador,
CMakeCache, LastTest.log, `f11/tests.xml`, `f11/run.json`, logs de proceso,
`measurements.json` y `processes.json`. El job ASan incluye el JUnit HOST;
H01/F11 se omiten únicamente en ese job. Los dos productos incluyen los logs
reales de carga y símbolos. Los artefactos tienen la retención de Actions
(expiración declarada: 2027-02-11); estos informes permanentes conservan las
conclusiones, recuentos, incidencias, SHA y medidas aunque los ZIP expiren.

Los resúmenes CI se contrastaron con los logs de jobs por API; JUnit local se
leyó y contó por nombre de prueba. La descarga directa local de ZIP fue denegada
por la política de red del runner de trabajo; los ZIP están publicados en Actions
con los enlaces anteriores. No se presenta esa descarga fallida como un fallo
funcional ni se afirma haber analizado localmente su XML remoto.

## Matriz de 28 escenarios

Los nombres de ensayo siguientes llevan el prefijo `host.m0.` salvo indicación.
PASS de los ensayos nativos se acredita en Linux; las ejecuciones por plataforma
y el subconjunto de sanitizadores están desglosados arriba.
**M0 PROBADO nativo; NO CERTIFICADO; NO FUSIONADO**. No queda un bloqueo
reproducido de M0. Auditoría independiente, aceptación y fusión siguen pendientes. Los escenarios de
regresión H04/F04/F05 conservan sus oráculos y fuentes originales.

| ID | Caso/evidencia | Resultado y alcance |
|---|---|---|
| HM-01 | `inspect_product.py`, Release OFF | PASS Linux y Windows Release OFF. |
| HM-02 | `bound`, escritor `process` | PASS; H03 BOUND y PERSON Core 3. |
| HM-03 | `readonly`, `submit` | PASS; bytes Core, RNG, tick y revisión iguales tras lectura. |
| HM-04 | `submit`, `process` | PASS; F05_ISSUED sin task/result. |
| HM-05 | `execute`, `recipient`, `concurrent` | PASS; receptor real, 4 eventos causales y resultado RNG real. |
| HM-06 | `process` completado y pendiente | PASS; escritor/lector nuevos, H04 y bytes Core iguales. |
| HM-07 | `process`, `recover`, `pending` | PASS; reconsulta y renovación de generación en LOAD. |
| HM-08 | `replay`, `concurrent`, `process` | PASS; misma key/payload, correlación distinta, sin otro evento/intento/RNG. |
| HM-09 | `conflict` | PASS; IDEMPOTENCY_CONFLICT y bytes idénticos. |
| HM-10 | `stale` | PASS; REVISION_STALE, REFUSED auditado F05, sin acción/RNG. |
| HM-11 | `unbound`, `resolving`; H03 `hi09_close_during_bind` | PASS; despacho durante RESOLVING devuelve PRINCIPAL_UNBOUND vacío sin esperar al bind; cierre H03 conservado. |
| HM-12 | `scope`, aserciones de compilación | PASS; sin campo actor/issuer/scope; estación ajena rechazada sin cambios. |
| HM-13 | `authority` | PASS; F04_DENIED/F05_REFUSED real, sin task/intento/resultado/RNG; no se afirma rechazo atómico. |
| HM-14 | `recipient` | PASS; capitán emisor no puede recibir/ejecutar para otro PERSON. |
| HM-15 | `unsupported` | PASS; F05_UNSUPPORTED y REFUSED, sin motor alternativo. |
| HM-16 | `expired`, `process`, `recover` | PASS; generación vieja no lee ni muta tras CLOSE/LOAD. |
| HM-17 | `saving`, `loading` | PASS; pausas reales H04, BUSY_STATE y sin Core concurrente. |
| HM-18 | `save_order` | PASS; SAVE espera al despacho confirmado; LOAD recupera la orden completa ISSUED. |
| HM-19 | `close_order` | PASS; pausa tras commit real, cierre invalida cola y respuesta tardía. |
| HM-20 | `unknown` | PASS; inyección complementaria 49151, diagnóstico privado original, DOMAIN_REJECTED vacío. |
| HM-21 | `observer` | PASS; jugador ajeno no ve orden y no puede cambiar vínculo. |
| HM-22 | `institutional`, inspección de producto | PASS; SERVICE_UNAVAILABLE, bytes iguales, sin F11 trial. |
| HM-23 | H04 `import`, `identity`, `wrong_binding`, `foreign_core`, `absent_binding` | PASS en build local limpio; se repiten en CI. |
| HM-24 | H02/H03/H04/F04/F05 + F11 aislada | PASS local limpio; resultado CI por plataforma arriba; no se relajan oráculos históricos. |
| HM-25 | `process` / `measurements.json` | PASS; 4 generaciones por campaña, tamaños y hashes reales. |
| HM-26 | Compilación negativa + exports/dependencias | PASS de inspección Linux/Windows; sin F04Session*/actor ni receptor público en SessionOwner. |
| HM-27 | `recover` | PASS; LOAD de ranura ausente falla PATH_REJECTED, conserva bytes, ciclo explícito posterior completo. |
| HM-28 | `pending`, `process` pendiente | PASS; recupera ISSUED, luego recibe y ejecuta con F05 real. |

## Comandos reproducibles

Ejecutar desde el checkout del repositorio. Elegir siempre un build y raíz de
temporales NUEVOS: las suites F05 históricas exigen no reutilizar su salida.
Todos los valores `$build`, `$temp`, `$report`, `$product` y `$core` deben estar
bajo la raíz temporal autorizada `laboratorios/host/h05/`; no incluirla en Git.

```sh
export TMPDIR="$temp" TEMP="$temp" TMP="$temp" F04_TEST_TEMP_ROOT="$temp"
cmake -S desarrollo/integration/host -B "$build" \
  -DCORERPG_SOURCE_DIR="$core" -DTREK_HOST_TESTS=ON -DCMAKE_BUILD_TYPE=Release
cmake --build "$build" --config Release --parallel 3 --target \
  host_native_tests host_fault_tests host_persistence_tests host_m0_tests \
  f04_tests f04_population_tests f04_history_faults f05_tests \
  f05_delegation_tests f05_initiative_tests f05_ai_tests f05_integration_audit_tests
ctest --test-dir "$build" -C Release -j 3 \
  -R '^(host\.|f05\.|f04\.(history_faults|thread|scope|identity|class|buffers|determinism|population_.*|process_save|process_load)$)' \
  --no-tests=error --output-on-failure --output-junit "$report"
```

La ejecución local limpia usó Debian 13, GCC 14.2.0, CMake 4.4.4, generador
Ninja, build `gcc-clean`, `--parallel 4` y CTest `-j 3`. La dependencia jsoncons
se reutilizó desde el checkout descargado por CMake mediante
`FETCHCONTENT_SOURCE_DIR_JSONCONS`; su pin histórico no cambió. Los ensayos
finales incrementales se limitaron a HOST/M0 tras los cambios en hooks de test;
CI recompiló y repitió la selección completa de 236 casos sobre el código final.

El workflow versionado `host-h02-native.yml` contiene los comandos PowerShell
exactos de Windows y Clang. MSVC usa `-A x64` y `--config Release`. Clang añade
`-fsanitize=address,undefined -fno-omit-frame-pointer`, ASAN_OPTIONS y UBSAN_OPTIONS
con halt_on_error, y selecciona `^host\.`. F11 se construye por separado mediante
`desarrollo/integration/f11_host/run_native.py` (17 pruebas) y H01 mediante
`desarrollo/tools/validation/test_host_h01_contracts.py` (11 pruebas).

```sh
cmake -S desarrollo/integration/host -B "$product" \
  -DCORERPG_SOURCE_DIR="$core" -DTREK_HOST_TESTS=OFF -DCMAKE_BUILD_TYPE=Release
cmake --build "$product" --config Release --parallel 3 --target TrekHost
python3 desarrollo/integration/host/tests/inspect_product.py "$product"
ctest --test-dir "$build" -C Release -R '^host.m0.process$' --output-on-failure
```

Muestra final local: procesos 4777/4780 para write/read y 4785/4796 para
write_pending/read_pending, todos con exit 0, dataset
`0b5dcd4203e34d448aa1980a63b03765`. Orden Core 375, intento 379, resultado 381,
evento terminal 382, revisión 5178, stream 984065, tirada 99, consumed_random=1.

El ensayo de proceso ejecuta write/read y write_pending/read_pending mediante
subprocesos independientes. Registra PIDs, comandos, códigos de salida, logs y
mediciones. El diagnóstico binario `expected-active` solo sirve como oráculo;
RESTORE abre exclusivamente la ranura H04. Compara estado, identidad, revisión,
reloj, stream RNG y hechos completos; en el lector reconsulta, repite la key,
restaura otra vez y rechaza la generación anterior. Ninguna generación opaca de
C++ se serializa como credencial entre procesos.

## Medición real inicial Linux/GCC

Bytes lógicos de todos los archivos por versión (sobre H04 e historial), sin
atribuirlos a bloques físicos asignados. Objetos son archivos `.obj` Core;
repetición se calcula por SHA256 de contenido respecto a generaciones anteriores
de la misma campaña, nunca por parecido de nombres.

| Campaña/versión | Bytes totales | Objetos | Bytes objetos | Objetos repetidos | Bytes repetidos |
|---|---:|---:|---:|---:|---:|
| Completada v1 nueva | 96 289 | 2 | 96 015 | 0 | 0 |
| Completada v2 con orden | 98 619 | 2 | 98 345 | 0 | 0 |
| Completada v3 sin cambios | 98 619 | 2 | 98 345 | 2 | 98 345 |
| Completada v4 tras LOAD | 98 967 | 3 | 98 693 | 2 | 98 345 |
| Pendiente v1 nueva | 96 289 | 2 | 96 015 | 0 | 0 |
| Pendiente v2 ISSUED | 97 029 | 2 | 96 755 | 0 | 0 |
| Pendiente v3 sin cambios | 97 029 | 2 | 96 755 | 2 | 96 755 |
| Pendiente v4 tras LOAD y ejecución | 195 374 | 4 | 195 100 | 2 | 96 755 |

Muestra final `0b022b11`: SAVE completada v1/v2/v3 = 84 267/90 906/80 146 µs;
RESTORE = 63 234 µs. Pendiente = 85 343/70 293/89 123 µs; RESTORE = 13 566 µs.
Se midió durante compilaciones concurrentes; es latencia observada, no benchmark
aislado. La muestra limpia anterior (`5ee7b169`) obtuvo 35 250/26 333/28 198 µs
y RESTORE 20 156 µs; pendiente 36 183/25 818/31 657 µs y RESTORE 11 832 µs.
Son observaciones, sin percentiles ni garantía de rendimiento. Los artefactos de los runs CI
contienen sus propias muestras independientes. No se elimina ni deduplica ningún archivo.

## Incidencias conservadas

- Primer oráculo H05: FAIL al exportar historial antes de migrarlo. Corregido
  el diagnóstico: `f04_save` monolítico / `f04_history_export_active` segmentado.
  Ninguna recuperación usa esos bytes.
- El oráculo nuevo exigía incremento de revisión en la tirada; Core conserva
  esa revisión y consume RNG, mientras F05 aumenta la revisión al auditar.
  Corregido contra las cabeceras y el oráculo histórico F05, sin modificar este.
- La ranura inexistente devuelve PATH_REJECTED por el recorrido seguro H04;
  el test nuevo se ajustó a ese contrato y comprueba la conservación del Core.
- Repetir toda la suite en un build ya usado produjo FAIL
  `f05.p05a_I_process_save: fresh history output required` y NOT_RUN de su lector.
  Se preservó la salida y el build nuevo pasó 235/235; no se elimina el laboratorio
  anterior ni se cambia la expectativa histórica.
- El entorno carecía de CMake/Ninja/Clang. Se instalaron CMake/Ninja en un venv
  local del laboratorio. Clang local: NOT_RUN; su ejecución corresponde a CI.
- CI Windows inicial: FAIL de enlace del ejecutable M0 (declaración del hook
  dentro de función, resuelta con distinto ámbito por MSVC). El producto Release
  OFF pasó. Corregido en `0b022b11` con declaraciones de namespace, sin cambios
  al producto ni a expectativas históricas. La ejecución final se registra arriba.
  Evidencia previa: [run 43466768691](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43466768691)
  sobre `d530d9fbb6758cb1fa6755262297e81b84e7a885`: GCC 235/235, sanitizadores
  80/80, productos y F11 17/17 por SO PASS; M0 Windows NOT_RUN por el enlace.
  El run intermedio `43467402612` quedó superado por la corrección final; no se
  usa para acreditar M0. Ningún FAIL previo se oculta como PASS.

Hito parcial: no certifica H13, Unreal, MSI, F06 ni emisor institucional F11.
