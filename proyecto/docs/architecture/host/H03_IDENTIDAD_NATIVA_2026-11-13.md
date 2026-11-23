# H03 — Identidad local en TrekHost

Implementación de H03-P02/P03 y trazabilidad H03-P04. Base Star Trek
`316ee3e95d2559239600190d37bddf83592f8d1c` (H02, [PR #132](https://github.com/robdor80/Videojuego_StarTrek/pull/132)).
Contrato y matriz de diseño tomados de la [PR #133](https://github.com/robdor80/Videojuego_StarTrek/pull/133)
en `b28d22d11487fbf399fa27f36002d4f5210c961e`.

## Alta de identidad

1. `SessionOwner::open` activa el Core y emite la generación H02. El propietario representa al único principal local. Cada apertura crea un marcador efímero de campaña de HOST que distingue activaciones incluso si coinciden los datos de población, el ID de nave, la revisión y los IDs de persona.
2. El flujo nativo de creación autorizado llama a `PlayerBootstrap::prepare` con la generación y la persona resultante de ese flujo. `player_bootstrap.h` es una cabecera privada de C++ para la composición de confianza. Una elección de interfaz debe pasar por el flujo de creación antes de llegar a este punto. La prueba utiliza personas materializadas por F04 en una población controlada. La creación del cadete de la Academia sigue pendiente.
3. El trabajador H02 comprueba la persona con `f04_person` y el observador de bootstrap de `f04_handles`. Obtiene el ámbito del Core abierto y la revisión de `f04_stats`. Solo el propietario construye `PlayerSelection`, ligada al marcador de campaña por una referencia débil. La elegibilidad para iniciativa es decisión de F05, cuyo observador debe ser PERSON de la dotación activa.
4. `PlayerBootstrap::bind` verifica la campaña y despacha `f05_bind_player` en el mismo trabajador y con la revisión esperada. El primer éxito de F05 publica el vínculo. El propietario conserva el `F04Ref` operativo y publica solo una copia de la generación y del ID de persona a través de `current_player`. El ID sirve para proyección. H05 debe resolver el actor en el propietario al ejecutar cada operación autorizada.

El estado de identidad es privado. Una sesión Core `ACTIVE` comienza `UNBOUND`.
Durante la primera llamada F05 el vínculo queda `RESOLVING` y las consultas devuelven
`PRINCIPAL_UNBOUND`. Un éxito válido publica `BOUND` bajo el mutex de admisión.
Un conflicto Core previo al primer vínculo deja el estado `INVALID` y cierra el acceso
de jugador para esa activación. Otros rechazos iniciales mantienen `UNBOUND`, con
reconsulta y reintento explícitos. Un intento posterior de sustituir al sujeto legítimo
conserva el vínculo previo.

## Concurrencia, revisión y errores

- Preparación, vinculación y comprobaciones H02 comparten la cola FIFO de hasta 32 solicitudes pendientes. El mutex queda libre durante Core. La lectura de la proyección se linealiza bajo el mutex y los consumidores deben comprobar la generación al usar una copia después de otra transición.
- La admisión de cierre o el fallo de la comprobación de vida H02 invalidan generación, campaña, vínculo y solicitudes pendientes bajo el mismo mutex. Si F05 ya fue despachado, puede confirmar en Core antes de volver. El trabajador descarta el resultado operativo de esa generación y solo entonces destruye la sesión. La mutación confirmada pertenece a la campaña que se está cerrando.
- F05 valida el observador y el vínculo preexistente antes de comprobar la revisión inicial. Un replay del mismo sujeto admite la revisión anterior y conserva la revisión Core. Un sujeto distinto devuelve el conflicto original. HOST pasa la revisión esperada a F05 y cada preparación lee la revisión vigente. Un primer `F04_STALE` exige refrescar y solicitar el intento explícitamente.
- El bootstrap interno conserva el código original de F04/F05. `F04_SCOPE` se mapea a `SCOPE_INVALID`, `F04_DENIED` a `ACCESS_DENIED`, `F04_STALE` y `F04_REVIEW` a `REVISION_STALE` y `F05_IDEMPOTENCY_CONFLICT` al error homónimo. Argumento, hilo, capacidad e interno conservan su mapeo H02. Los demás rechazos se devuelven como `DOMAIN_REJECTED`. Los rechazos por campaña o generación de HOST se deciden antes de F05 y carecen de código Core. En caso de denegación, la selección o proyección sale vacía.

## Matriz H03-P04

Los nombres nativos tienen prefijo CTest `host.native.`; los de inyección,
`host.fault.`. Resultados locales de Windows x64, Release, MSVC
19.51.36256.0, SDK 10.0.26100.0 y CMake 4.4.3. Los artefactos de GitHub
Actions documentan la revisión exacta ejecutada por plataforma.

| Caso | Prueba o evidencia | Resultado |
|---|---|---|
| HI-01 | `hi01_first_bind`, alta PERSON y proyección en la generación activa | PASS |
| HI-02 | `hi02_unbound`, Core activo, proyección vacía y revisión intacta | PASS |
| HI-03 | `hi03_client_boundary`, compilación de la superficie de consulta y resolución desde el vínculo | PASS nativo. Adaptadores H05/H06/H10 PENDIENTES |
| HI-04 | `hi04_replay`, replay con revisión anterior, sin nuevo hecho | PASS |
| HI-05 | `hi05_conflict`, otro sujeto, código F05 original, revisión y personaje conservados | PASS |
| HI-06 | `hi06_foreign_campaign`, selección de otra activación con mismos IDs y revisión | PASS |
| HI-07 | `hi07_expired`, cierre y reapertura, salidas vacías y revisión intacta | PASS |
| HI-08 | `hi08_concurrent`, dos productores, un solo vínculo confirmado | PASS |
| HI-09 | `hi09_close_during_bind` (inyección), pausa después del commit, invalidación inmediata de llamadas en cola y del resultado tardío | PASS |
| HI-10 | `hi10_stale`, rechazo real F05 con `F04_STALE`, revisión intacta y recuperación explícita | PASS |
| HI-11 | `hi11_invalid_person` y `hi11_bind_failure` (inyección), rechazo real de no PERSON y de residente, fallos de ámbito, interno y de dominio | PASS |
| HI-12 | `hi12_revision`, reconsulta comparada con un bind Core independiente que añade un único registro | PASS |
| HI-13 | `hi13_reopen`, campaña nueva con ID de PERSON repetido, sin herencia | PASS |
| HI-14 | `product_boundary` (H02), inspección de símbolos del puente cargado y composición CMake sin emisor de ensayo | PASS de frontera. Operación institucional H07 PENDIENTE |
| HI-15 | Restore legítimo con scope y generación renovados | PENDIENTE H04 |
| HI-16 | Restore con persona ausente o vínculo F05 incompatible | PENDIENTE H04 |
| HI-17 | Importación que afirma identidad profesional | PENDIENTE H04/H07 |
| HI-18 | Callback de UI/IA posterior a LOAD | PENDIENTE H04/H10 |
| HI-19 | `hi19_validation` y `hi19_incompatible_core_binding` (inyección), campaña sana y rechazo sin publicar sujeto incorrecto | PASS |

## Reproducción

CoreRPG limpio en `76a7b7b485616d8c4994f384a90f123bf333591d`, ABI de creación
F04 1. Composición H02 con `F05_ENABLE_ORDERS=ON`, `F04_ENABLE_HISTORY=ON`,
`F11_ENABLE_PROMOTIONS=OFF`, `CORERPG_BUILD_CONTENT_JSON=OFF` y
`F04_HISTORY_TESTING=1` heredado del puente. jsoncons queda fijado por F05
en `bcb44594c50c495ee1e690602cdd71455942ad0e`.

El workflow [HOST H02 native](../../../../.github/workflows/host-h02-native.yml)
recoge los nuevos casos por el prefijo `host.`. Incluye Windows y Linux en
Release con regresiones H02/F04/F05, Linux con ASan/UBSan, verificación de
producto Linux con tests desactivados y regresiones aisladas H01/F11.

```powershell
cmake -S desarrollo/integration/host -B $build -DCORERPG_SOURCE_DIR="$core" -DTREK_HOST_TESTS=ON -DCMAKE_BUILD_TYPE=Release
cmake --build $build --config Release --target host_native_tests host_fault_tests f04_tests f04_population_tests f05_tests f05_delegation_tests f05_initiative_tests f05_ai_tests f05_integration_audit_tests
ctest --test-dir $build -C Release -R '^(host\.|f05\.|f04\.(thread|scope|identity|class|buffers|determinism|population_.*|process_save|process_load)$)' --no-tests=error --output-on-failure --output-junit "$report"
```

Para repetir en MSVC x64, añadir el generador Visual Studio disponible y
`-A x64`. Usar un build limpio y un directorio temporal por ejecución para
los casos históricos F04/F05 que escriben archivos. El JUnit conserva la
salida por prueba, incluidas las comprobaciones de revisión de H03.

## Dependencias de H04 y alcance

La identidad durable de campaña y la procedencia de ranura corresponden a
H04. Antes de activar jugador tras LOAD, H04 necesita contrastar campaña
y persona persistentes con el estado autoritativo, reconstruir el ámbito
y emitir una generación nueva. La ABI pública F05 del pin inspeccionado
carece de lector de `f05_player`; coordinar con F05 una consulta de solo
lectura para distinguir ausencia, coincidencia y conflicto. `f05_bind_player`
puede mutar un Core sin vínculo, por lo que la restauración debe permanecer
cerrada mientras falte esa verificación. H03 implementa aperturas nuevas.
Los rangos, comisiones, destinos y permisos institucionales siguen en F11.

## Inventario

| Archivo en `desarrollo/integration/host` | Cambio |
|---|---|
| `include/trek/host/session_owner.h` | Proyección de identidad y errores H03. |
| `src/player_bootstrap.h` | Selección opaca de campaña y entrada de creación de confianza. |
| `src/session_owner.cpp` | Admisión, publicación y revocación del vínculo con la generación H02. |
| `src/native_session.h`, `src/native_session.cpp` | Operaciones de identidad en el propietario y normalización. |
| `src/f04_session_bridge.cpp` | Validación PERSON, revisión y llamada F05 por ABI pública. |
| `tests/player_native_tests.cpp`, `tests/native_tests.cpp`, `tests/test_support.h` | Escenarios de identidad con puente real y ejecución nativa. |
| `tests/fault_tests.cpp` | Fallos y carrera de cierre reproducibles. |
| `CMakeLists.txt` | Registro de pruebas H03 bajo `TREK_HOST_TESTS`. |

Este informe se añade en `proyecto/docs/architecture/host`.
