# H05 — Resultados verificables del ciclo M0

Fecha: 2026-11-13. Implementación `5ee7b169e87ab24aa141cd3c4f81c3bec6c37803`,
base `cf8fffe755ba04cf66ed09042858ec923d7b100b`. CoreRPG limpio
`76a7b7b485616d8c4994f384a90f123bf333591d`; jsoncons histórico
`bcb44594c50c495ee1e690602cdd71455942ad0e`. Ver las decisiones e inventario en
[informe de implementación](H05_INFORME_IMPLEMENTACION_2026-11-13.md).

## Ejecuciones y clasificación inicial

Esta publicación inicial conserva los resultados locales y deja CI explícitamente
pendiente. Se actualizará con los runs y sus SHA antes de entregar la PR.

| Entorno/suite | PASS | FAIL | SKIP/NOT_RUN | Estado |
|---|---:|---:|---:|---|
| Linux GCC 14.2, M0 nativo | 25 | 0 | 0 | PASS; ciclo real completado y pendiente entre procesos |
| Linux GCC, H02–H05/F04/F05 en build limpio nuevo | — | — | — | RUNNING |
| Linux Release OFF, carga y símbolos | 1 | 0 | 0 | PASS; se repetirá sobre el SHA final de código |
| Linux F11 aislada | 17 | 0 | 0 | PASS; fuentes F11 no vinculadas a TrekHost |
| H01 documental | 11 | 0 | 0 | PASS |
| CI Linux GCC / Windows MSVC / Clang ASan-UBSan | — | — | NOT_RUN | Pendiente de abrir PR y Actions |
| CI productos Release OFF Linux/Windows | — | — | NOT_RUN | Pendiente |
| MSI/UE/D3D12/NullRHI/corte eléctrico físico | 0 | 0 | NOT_RUN | Fuera de H05 |

## Matriz de 28 escenarios

Los nombres de ensayo siguientes llevan el prefijo `host.m0.` salvo indicación.
PASS de esta tabla se refiere a Linux local; CI y plataformas se registrarán arriba.

| ID | Caso/evidencia | Resultado y alcance |
|---|---|---|
| HM-01 | `inspect_product.py`, Release OFF | PASS Linux; Windows pendiente CI. |
| HM-02 | `bound`, escritor `process` | PASS; H03 BOUND y PERSON Core 3. |
| HM-03 | `readonly`, `submit` | PASS; bytes Core, RNG, tick y revisión iguales tras lectura. |
| HM-04 | `submit`, `process` | PASS; F05_ISSUED sin task/result. |
| HM-05 | `execute`, `recipient`, `concurrent` | PASS; receptor real, 4 eventos causales y resultado RNG real. |
| HM-06 | `process` completado y pendiente | PASS; escritor/lector nuevos, H04 y bytes Core iguales. |
| HM-07 | `process`, `recover`, `pending` | PASS; reconsulta y renovación de generación en LOAD. |
| HM-08 | `replay`, `concurrent`, `process` | PASS; misma key/payload, correlación distinta, sin otro evento/intento/RNG. |
| HM-09 | `conflict` | PASS; IDEMPOTENCY_CONFLICT y bytes idénticos. |
| HM-10 | `stale` | PASS; REVISION_STALE, REFUSED auditado F05, sin acción/RNG. |
| HM-11 | `unbound`; H03 `hi09_close_during_bind` | PASS; salidas vacías, sin auto-bind. RESOLVING conserva el cierre H03. |
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
| HM-23 | H04 `import`, `identity`, `wrong_binding`, `foreign_core`, `absent_binding` | PASS en regresión local previa; se repiten en build limpio/CI. |
| HM-24 | H02/H03/H04/F04/F05 + F11 aislada | Regresiones completas limpias/CI pendientes; no se relajan oráculos históricos. |
| HM-25 | `process` / `measurements.json` | PASS; 4 generaciones por campaña, tamaños y hashes reales. |
| HM-26 | Compilación negativa + exports/dependencias | PASS Linux; sin F04Session*/actor ni receptor público en SessionOwner; Windows pendiente CI. |
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

Primera muestra: SAVE completada v1/v2/v3 = 32 153/27 110/24 965 µs;
RESTORE = 12 669 µs. Pendiente = 30 236/27 310/25 962 µs; RESTORE = 37 986 µs.
Son observaciones, sin percentiles ni garantía de rendimiento. Los runs CI
proporcionarán muestras independientes. No se elimina ni deduplica ningún archivo.

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
  Se preservó la salida y se prepara un build nuevo; no se elimina el laboratorio
  anterior ni se cambia la expectativa histórica.
- El entorno carecía de CMake/Ninja/Clang. Se instalaron CMake/Ninja en un venv
  local del laboratorio. Clang local: NOT_RUN; su ejecución corresponde a CI.

Hito parcial: no certifica H13, Unreal, MSI, F06 ni emisor institucional F11.
