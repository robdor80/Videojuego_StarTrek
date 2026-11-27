# HOST H09-P03-C01 — Factibilidad nativa de Navegación y CONN

- **27-11-2026.** C01 se detiene por dependencia de dominio.
- **Star Trek revisado y probado** en `a2c1cda46bb440b1543dbb88ef75f55cb051cfcf` (`main`, PR #228).
- **CoreRPG revisado y probado** en un checkout limpio de `76a7b7b485616d8c4994f384a90f123bf333591d`.
- **Entrega documental.** P03-D y P03-E quedan pendientes de capacidad autoritativa y aprobación de su integración.

La campaña naval de producto ya tiene identidad de nave, tripulación, puestos y reloj Core. La contención genérica podría representar una localización discreta si la campaña publicase una relación inequívoca entre nave y lugar. En el pin y composición actuales faltan ese hecho de producto, el catálogo de carta autorizado para el observador y el resolvedor de propuestas. Esa combinación impide incluso el adaptador de lectura/propuesta. Tampoco hay ejecutor naval ni una orden F05 de timón. C01 aplica la parada técnica del [encargo aprobado](H09_P03_C01_ENCARGO_CODEX_CLOUD_2026-11-27.md).

## Evidencia en las costuras de producto

| Costura y símbolos | Capacidad y límite observados |
| --- | --- |
| HOST `CMakeLists.txt`, `TrekF04Bridge`, `f04_host_bridge.cpp` | La composición sustituye una unidad de compilación por la variante de producto e incluye F04, snapshot HOST y vinculación F05. El lector F11 es opcional y privado. La campaña naval vive en el único `Campaign` de la sesión F04. La composición HOST también contiene el modo Academia independiente, fuera de este análisis. El generador de datos F10 demuestra un punto de entrada de autoría explícito y revisado. No hay objetivo naval, registro de dominio ni generador de cartas en esa composición. [HOST CMake](../../../../desarrollo/integration/host/CMakeLists.txt) · [Puente de producto](../../../../desarrollo/integration/f04/src/f04_host_bridge.cpp) |
| `catalog`, `initialize`, `initialize_population`, `f04_handles`, `f04_stats`; `bridge::dispatch` en `GatewayOp::VIEW` | La nave primaria es la entidad Core 1. El catálogo crea definiciones de clase y de operaciones de a bordo. La contención creada por el arranque sitúa personas y puestos en la nave. `CampaignView` expone actor, nave, revisión y tick. No hay definición de lugar de carta ni campo de ubicación de la nave en esa vista. El auxiliar Defiant de Valhalla se registra como entidad vinculada a la nave principal, sin localización astronómica. [F04](../../../../desarrollo/integration/f04/src/f04_bridge.cpp) · [Organización](../../../../desarrollo/integration/f04/src/f04_organization.inc) · [Gateway nativo](../../../../desarrollo/integration/host/src/gateway_bridge.cpp) |
| `perform` en `F04_MOVE`; `f05_origin`, `f05_validate`, `f05_execute_order` | `F04_MOVE` exige un puesto activo (`duty`) y aplica `PlaceEntityAction{persona, puesto}`. La disponibilidad de HELM acredita organización, cualificación y guardia. F05 valida autoridad de mando/sensores y `F04_SCAN`, y ejecuta ese único tipo. F04 incluso registra un evento con la denegación de `f04_execute`, por lo que usarlo para sondear operaciones faltantes incumpliría una denegación de propuesta sin mutación. [F04](../../../../desarrollo/integration/f04/src/f04_bridge.cpp) · [F05](../../../../desarrollo/integration/f05/src/f05_orders.inc) |
| `f04_advance`, `schema`, `f04_host_snapshot.inc` | El avance usa `Campaign::time` en los límites de guardias, funciones de mando y tareas F04. `schema` exige `c.time.records().empty()` y valida un vocabulario cerrado de entidades, campos y referencias. La capa snapshot usa `HistoryPersistence` y el catálogo F04. Introducir registros de viaje en Timeline o nuevas entidades bajo ese esquema exige aprobación de la composición, validación de publicación/recuperación y compatibilidad de guardados. [F04](../../../../desarrollo/integration/f04/src/f04_bridge.cpp) · [Snapshot HOST](../../../../desarrollo/integration/f04/src/f04_host_snapshot.inc) |
| `SessionOwner::Impl::admission`, `execute(Dispatch&)`, `execute(Load&)`; `bridge::dispatch` | Existe cola de hilo dueño con control de generación, vinculación H03 y resolución de `F04Ref` desde servidor. RESTORE publica una generación nueva tras validar y cambiar la campaña. SAVE conserva la generación, de modo que una futura propuesta necesita su propia regla de invalidación en el ciclo de SAVE/RESTORE/CLOSE. La comprobación de membresía F04 sirve para la vista de a bordo. La política de visibilidad de cartas y rutas todavía carece de dueño runtime. [Sesión](../../../../desarrollo/integration/host/src/session_owner.cpp) · [Gateway nativo](../../../../desarrollo/integration/host/src/gateway_bridge.cpp) |
| Core `CoreRPG::CoreRPG`, `CoreRPG::ContentJson`, `ResourceDefinition`, `ContentCatalog` | El objetivo estático contiene las primitivas conocidas. El módulo JSON opcional carga definiciones y referencias con esquema cerrado para `id`, `kind`, `references` y `$schema`. Puede identificar contenido revisado, pero no carga los modelos de cartas Star Trek ni registra operaciones ejecutables. La proyección del ejemplo `authorized_context_host.cpp` es una integración genérica de acceso autorizado. [Composición Core](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/CMakeLists.txt) · [Esquema Core](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/schemas/content/0.1.0/resource-definition.schema.json) · [Ejemplo Core](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/examples/authorized_context_host.cpp) |
| Core `Timeline::advance`, `CampaignPersistence::deserialize`, `Simulation::step` | `advance` despacha al `ActionEngine` las operaciones conocidas. La recuperación del archivo v1 acepta los cinco discriminantes explícitos y rechaza el resto. `Simulation::step` procesa el lote genérico de acciones. En estas rutas no se halló un despachador registrado por plugins, una acción naval tipada o un punto de restauración para un estado naval opaco. [Timeline Core](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/src/timeline.cpp) · [Archivo Core](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/src/campaign_persistence.cpp) · [Simulation Core](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/src/simulation.cpp) |

El grafo, el modelo de distancias, los perfiles de coste, la astrografía, el esquema de estado naval y el handoff S11 se leen como fuentes de autoría en los validadores documentales pertinentes. La búsqueda de rutas e identificadores en integración nativa, herramientas, fuentes UE y workflows devolvió referencias en `test_host_h09_p03_contract.py`, `test_s11_astrometrics_contracts.py` y `validate_lore01_c.py`, sin consumidor de producto de esos artefactos. Los nombres de destino publicados en el repositorio, por sí solos, no establecen conocimiento de campaña. La conclusión cubre las superficies nativas y la composición inspeccionadas, sin reclamar una auditoría exhaustiva de todos los assets de Unreal. [Navegación](../../../../sistemas/gameplay/navigation/README.md) · [Handoff S11](../../../../sistemas/gameplay/ship_operations/interconsole/s11_astrometrics_to_navigation_route_proposal_v0.1.json)

La frontera de error para un futuro adaptador seguirá siendo `SERVICE_UNAVAILABLE` cuando el dominio falte. Ese valor ya existe en HOST. En C01 las dos operaciones conservan su estado lógico de indisponibilidad y no se añadió una ruta ejecutable para devolverlo. [Registro de consolas](H09_P01_REGISTRO_CONSOLAS_v1.json) · [Contrato P03](H09_P03_CONTRATO_NAVEGACION_CONN_v1.json)

## Interfaz mínima a someter a revisión

| Etapa | Operación de dominio propuesta | Condiciones de integración |
| --- | --- | --- |
| D | Leer ubicación propia discreta y carta conocida por observador. | Recibir campaña, nave y observador resueltos en la sesión dueña. Devolver lugar tipado o desconocido, revisión de origen, procedencia y revisión del conocimiento/cartografía. El lugar discreto puede acreditarse con contención de Core si el dueño del dominio define, inicializa y valida esa semántica. |
| D | Resolver y proponer ruta de carta conocida, explícitamente de solo lectura. | Recibir destino, perfil, revisión Core/posición/carta/conocimiento y requisitos de llegada aplicables. Distinguir ambigüedad visible, indisponibilidad, rechazo y obsolescencia sin filtrar verdad oculta. Devolver candidatos y referencia ligada a campaña, generación y revisiones, con distancia/ETA opcionales, procedencia e incertidumbre. Sin posición, tick, RNG, recursos ni archivo modificados. Revalidar las referencias antes de publicar/consumir e invalidarlas al guardar, restaurar o cerrar. |
| E | Validar/ejecutar maniobra separada y consultar su progreso. | F04/F05 deben acreditar identidad, guardia HELM, cualificación, delegación y autoridad vigente, nave y revisión del compromiso. Un dominio único calcula progreso por tramos, recursos, cambios de posición y consecuencias en transacción con el reloj Core. Persistir cursor, estado de maniobra y clave/correlación de compromiso con la campaña. Separar el recibo de aceptación del resultado naval, sin reintentos automáticos ni doble consumo tras restaurar. |

### Opciones y efecto sobre el pin

1. **Extensión de dominio en la composición de producto, con el pin actual.** Evaluar primero D con definiciones de carta versionadas y hechos tipados en el mismo `WorldState`, acceso por observador y un resolvedor de dominio llamado por el puente privado. Requiere aprobación explícita para ampliar catálogo, bootstrap, esquema F04 y validación de `HistoryPersistence`, incluidas campañas antiguas que deben conservar ubicación desconocida si carecen del hecho. Para E, solo sería viable bajo el pin si se acredita un despacho determinista en el avance existente, sobre el mismo tick y transacción, y un cursor durable representable por hechos Core. La restricción de agenda vacía impide tratar `Timeline::schedule` como punto de extensión instalado.
2. **Ampliación en CoreRPG y posterior cambio de pin.** Si la compatibilidad de archivos o el despacho en la composición impiden preservar invariantes, publicar un API nativo de dominio y, para E, despacho/registro persistente de acciones tipadas con compatibilidad del formato. Auditar serialización, restauración, avance acotado y consumidores F04/F05 antes de proponer un SHA nuevo y su adopción. Son decisiones independientes del propietario. D puede evaluarse antes del movimiento progresivo.

La recomendación para el siguiente encargo es decidir la opción 1 y delimitar primero la carta conocida, el origen de la nave y las reglas de lectura. La prueba de salida debe recuperar una campaña antigua y una campaña con carta versionada, resolver un destino autorizado y demostrar identidad, tick, revisión, RNG y archivo invariantes durante propuesta y rechazo. Si la costura exige ampliar Core, registrar el requisito exacto y elevar la opción 2. Una vez demostrada la capacidad nativa, D puede integrar el adaptador privado y el handoff. E queda para una entrega posterior con orden tipada, autoridad y progreso persistente. La integración visual corresponde a P03-F cuando exista MSI.

## Pruebas de aceptación aún pendientes

| Casos del contrato | Puerta y prueba pendiente |
| --- | --- |
| N3-01–N3-07 | D. Origen propio y carta cargados. Destino conocido, homónimos, desconocido/redacción, perfiles, ETA y geometría desconocidas y bordes conocidos. |
| N3-08–N3-10 | D. Handoff S11 y Navegación→CONN como datos. Comparar Core/archivo antes y después de proponer y de rechazar. |
| N3-11–N3-14 | D/E. En el hilo dueño, cubrir generación, SAVE/RESTORE/CLOSE, revisiones, guardia HELM, permisos revocados al ejecutar y rechazo sin efectos de navegación. |
| N3-15–N3-17 | E. Aceptación sin desplazamiento, avance parcial con tick Core y guardado/restauración sin repetir tramos, recursos o eventos. |
| N3-18–N3-24 | Puerta F06. Intercepción, replanteo, conocimiento y proyección autorizada de contactos. El E2E requiere aceptación sensorial e integración MSI. |

Los 24 casos están en estado **SKIP / pendientes** en C01. Los validadores y las regresiones existentes solo acreditan sus propios contratos o primitivas.

## Reproducción de la revisión y validadores

Entorno local Debian 13.6 x86_64, Git 2.52.0, Python 3.12.14, GCC 14.2.0, CMake 3.31.10, Ninja 1.13.2 y libcurl 8.14.1. Usar el SHA de Star Trek indicado arriba y un checkout limpio del SHA Core exacto. Ejecutar las compilaciones con rutas de salida y temporales aisladas conforme a `AGENTS.md`.

```sh
git rev-parse HEAD
git -C "$core" rev-parse HEAD
git -C "$core" status --porcelain --untracked-files=all
git -C "$core" grep -niE 'register.{0,10}(action|event|extension)|domain.{0,10}(hook|extension|plugin)|warp|impulse|starship|navigation|trajectory|pathfind|route' -- include src CMakeLists.txt
git grep -Il -E 'anchor_route_graph|navigation_distance_edge_model|route_cost_model|route_context_model|astrography_location_model|navigation_state\.json|s11_astrometrics_to_navigation_route_proposal|NAVIGATION_ROUTE_PROPOSE|CONN_MANEUVER_ORDER' -- desarrollo/integration desarrollo/tools juego/UE5 .github
export PYTHONDONTWRITEBYTECODE=1
for test in test_host_h09_p03_contract test_host_h09_p01_contract test_host_h01_contracts test_s11_astrometrics_contracts; do
  python3 "desarrollo/tools/validation/${test}.py" || exit
done
```

El primer `grep` termina en código 1 (cero coincidencias en esos directorios). El segundo devuelve tres validadores. Complementar la búsqueda con las costuras y símbolos detallados arriba. La evidencia de las limitaciones proviene del grafo de compilación, el despacho y el esquema de recuperación, además de la búsqueda de nombres.

| Validación | Resultado local |
| --- | --- |
| H09-P03, H09-P01, H01 y S11 | PASS, 53 casos (15 + 11 + 11 + 16). Validación de contratos y límites de integración. |
| CoreRPG nativo (Release, configuración predeterminada sin backend JSON opcional) | PASS, 374/374 en 2,83 s de CTest. Incluye acciones admitidas tras guardar/restaurar, reanudación acotada, aislamiento y revocación del observador, bytes invariantes ante rechazo y validación de metadatos de contenido al restaurar. |
| Adaptador naval, CONN, movimiento, MSI y F06 | SKIP. Dependen de capacidades y autorizaciones pendientes. |

```sh
cmake -S "$core" -B "$build_core" -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build "$build_core" --parallel 4
ctest --test-dir "$build_core" -j4 --output-on-failure
```

Como referencias reproducibles, `TimelineTest.AllOperationTypesPersistAndExecute`, `TimelineTest.BoundedResumeDoesNotAdvancePastUnprocessedActions`, `ActionPersistenceTest.RejectedAndNoOpRequestsLeaveCanonicalSaveBytesUnchanged`, `ContextSecurityTest.ObserverIsolationRevocationAndSurvivingOwnedText` y `ExternalContentRestoreTest.SameDefinitionsDoNotAuthorizeChangedPublication` pasaron en la revisión Core indicada. Los avisos de GCC por inicializadores omitidos en Core y sus pruebas no impidieron compilar.

### Regresión nativa de HOST/F05

```sh
cmake -S desarrollo/integration/host -B "$build_host" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DTREK_HOST_TESTS=ON -DCORERPG_SOURCE_DIR="$core"
cmake --build "$build_host" --parallel 2 --target host_native_tests host_persistence_tests f05_tests
ctest --test-dir "$build_host" -j2 --no-tests=error --output-on-failure \
  -R '^(host\.native\.(hc05_thread_boundary|hi01_first_bind|hi10_stale|hi13_reopen)|host\.persistence\.(roundtrip|queue|late)|f05\.(scenario|authority|recipient|unsupported|scope|stale|reception|duplicate|revalidate|expired|cancel|transition|determinism|corrupt|buffers|population|history|history_fault|process_save|process_load))$'
```

**PASS en la selección reproducible, 27/27 en 0,21 s de CTest.** Los 7 casos HOST cubren hilo dueño, identidad, obsolescencia y persistencia. Los 20 casos F05 incluyen el rechazo de una operación fuera del contrato y sus transiciones existentes. La primera invocación, con filtro demasiado amplio, terminó con código 8 por 114 casos F05 seleccionados cuyos ejecutables no se habían compilado (`Not Run`), con los 27 ejecutados aprobados. El filtro corregido selecciona solo los tres ejecutables compilados. Windows y sanitizadores corresponden a los checks de GitHub Actions de la PR. [Actions de la rama](https://github.com/robdor80/Videojuego_StarTrek/actions?query=branch%3Acodex%2Fh09-p03-c01-factibilidad-core)

## Limpieza

El laboratorio propio `laboratorios/HOST/H09-P03-C01/` contuvo el checkout Core de verificación, herramientas locales, compilaciones y registros regenerables. Ocupación medida antes de limpiar de 236.662.784 bytes en bloques. Después de eliminarlo, la ruta quedó ausente. No se retuvo ningún artefacto del laboratorio. El informe y los comandos de reproducción quedan en el repositorio y las pruebas usan únicamente las fuentes versionadas y las dependencias declaradas.
