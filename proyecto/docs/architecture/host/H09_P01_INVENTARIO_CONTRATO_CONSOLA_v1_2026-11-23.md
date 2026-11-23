# H09-P01 — Inventario operativo, permisos y contrato de consola limpia v1

**Fecha:** 2026-11-23 · **Responsable:** ChatGPT · **Estado:** DISEÑADO / NO IMPLEMENTADO EN RUNTIME / NO CERTIFICADO.
**Subfase:** H09-P01 [C] del Plan Maestro HOST v1.2. Entrega documental de arquitectura y contrato lógico; **no** crea ABI C, plugins UE5, barridos reales, rutas ejecutadas, eventos ni permisos nuevos.

Registro verificable: `H09_P01_REGISTRO_CONSOLAS_v1.json`. Las pruebas estáticas de esta subfase validan fuentes y coherencia, **no** la integración Core/Unreal. Las operaciones enumeradas son **objetivos de adaptación**, nunca endpoints que se afirmen disponibles.

## 1. Autoridad y límites

- **CoreRPG**: único estado del universo, tiempo de campaña, conocimiento, validación de recursos/efectos, cronología, persistencia y resultado final de acciones.
- **F04/F05**: dotación, puesto y guardia, autoridad de ejecución de órdenes y transiciones de la cadena de mando. **F11**, exclusivamente en el proyecto principal, conserva las atribuciones institucionales; HOST no genera nombramientos, delegaciones ni ascensos.
- **F06**: reglas y contrato sensorial del videojuego. La implementación de referencia Python de F06 es **no autoritativa**, incluso si supera sus pruebas. Solo una adaptación real al Core puede crear una observación confirmada y visible en la partida.
- **F09**: catálogo de **16 familias funcionales** y contratos de las consolas; una familia **no equivale** a una estación física. Sensores, Ciencia, CONN, Navegación y Operaciones forman el primer corredor.
- **HOST H02–H08**: autentica sesión/campaña/personaje, coordina una única secuencia de operaciones en el propietario del Core, ejecuta lecturas autorizadas y entrega proyecciones filtradas; H08 transporta avisos de hechos confirmados y usa el reloj de Core sin duplicarlo.
- **Unreal Engine 5**: muestra LCARS y controles, nunca decide si el capitán, operador o NPC tiene permisos ni reconstruye información oculta. **IA**: explica datos ya autorizados; ni ejecuta la mutación ni amplía las observaciones.

**Advertencia sobre una coincidencia de nombres:** la ABI C existente `TREK_HOST_SUBMIT_SCAN` y `TrekHostScan` remiten al circuito de órdenes/acciones F04-F05 del HOST; **no demuestran** la existencia de un escáner F06, de una proyección de detecciones o de un servicio de sensores en Unreal. En H09-P02 debe establecerse un adaptador explícito, sin reaprovechar semánticamente aquella operación solo por llamarse SCAN.

## 2. Inventario reutilizable verificado en main

| Área | Fuente real en repositorio | Madurez comprobada para H09 |
| --- | --- | --- |
| Plan HOST | `PLAN_MAESTRO_HOST_v1.2_2026-11-11.md` | H09-P01 definida como inventario/contrato |
| Ciclo, identidad y entrada C | `desarrollo/integration/host/include/trek/host/session_owner.h`, `host_abi.h` | Interfaces HOST reales; **no** operaciones F06 nativas |
| Puesto/dotación | `desarrollo/integration/f04/include/f04_bridge.h` | API F04 existente; evaluar permisos con F04/Core |
| Órdenes | `desarrollo/integration/f05/include/f05_orders.h` | API F05 existente; ejecutar una orden no implica una lectura F06 |
| F06 petición/resultado | `sistemas/gameplay/ship_operations/sensor_resolution/sensor_scan_request_contract.json`, `sensor_result_contract.json` | Contratos v0.1; extensión de resultado Enterprise-D declarada **no implementada** |
| F06 referencia | `desarrollo/tools/simulation/f06_reference.py`, `resolve_sensor_scan.py` | Pruebas de referencia; **sin** estado autoritativo ni reservas |
| Consola Sensores | `sistemas/gameplay/ship_operations/consoles/sensors/sensor_console_interaction_model.json` | UX lógica aprobada: navegación, trabajo, estado persistente |
| Contacto/navegación | `sistemas/gameplay/ship_operations/sensor_resolution/contact_navigation_solution_v0.1.json` | Solución observador-relativa; `vector` legado no equivale a rumbo |
| Navegación | `sistemas/gameplay/navigation/navigation_order_contract.json`, `navigation_state.json` | Intenciones, validación y modelo de estado; no equivale a movimiento Core probado |
| Interconsolas | `sistemas/gameplay/ship_operations/interconsole/interconsole_data_package_contract.json` | Protocolo de **datos conocidos**, no transporte de ejecución instalado |
| Ciencia y OPS | `.../consoles/science/incoming_analysis_task_contract.json`, `.../interconsole/sensor_to_operations_power_request.json` | Contratos de entrada/solicitud; recepción no concede recursos |
| Mando | `sistemas/gameplay/chain_of_command/README.md`; `sistemas/gameplay/orders/starship_order_pipeline.md` | Intención ≠ orden ≠ compromiso ≠ resultado; rango por sí solo no basta |
| Comunicaciones | `sistemas/gameplay/communications/subspace_communication_contract.json` | Modelo de canales, destinatarios y latencia, no endpoint HOST operativo |
| F09 | `sistemas/gameplay/ship_operations/consoles/f09_reference_matrix_v0.1.json` | Inventario de 16 familias **reference_only_not_runtime** |
| Enterprise-D refit | `sistemas/gameplay/ship_operations/sensor_resolution/enterprise_d_valhalla_sensor_superiority_v0.1.json` | Diseño aprobado para configuración **galaxy_refit_a2**, activación condicionada y runtime pendiente |
| Astrometría | `sistemas/gameplay/ship_operations/interconsole/s11_astrometrics_to_navigation_route_proposal_v0.1.json` | Ruta **propuesta**, no maniobra |

El README general F06 en `proyecto/docs/roadmap/master/fases/F06/README.md` conserva evidencias históricas de **referencia**, no prueba F06 integrado al Core/UE. El desarrollo paralelo de F06 debe reconciliar su contrato y estado real **antes** de H09-P02: no congelar aquí decisiones de ejecución aún abiertas.

## 3. Matriz funcional priorizada

La tabla siguiente documenta **capacidad objetivo** y propietario de ejecución, no APIs existentes:

| Ruta / intención | Operación lógica | Propietario de hechos o decisión | Cierre posterior |
| --- | --- | --- | --- |
| Sensores: estado | `SENSOR_STATUS_READ` | Core/F06, vista por observador | H09-P02 |
| Sensores: contactos | `SENSOR_CONTACTS_READ` | Core/F06, conocimiento por nave | H09-P02 |
| Sensores: barrido | `SENSOR_SCAN_REQUEST` | F05 autoriza intención; Core/F06 calcula y confirma | H09-P02 |
| Sensores: informe | `SENSOR_RESULT_READ` | Proyección de Core/F06, sin verdad oculta | H09-P02 |
| Sensores → Ciencia | `SENSOR_TO_SCIENCE_HANDOFF` | Core/transferencia persistente autorizada | H09-P05 |
| Ciencia: análisis | `SCIENCE_ANALYSIS_REQUEST` | Ciencia recibe y interpreta datos observados | H09-P05 |
| Navegación: ruta | `NAVIGATION_ROUTE_PROPOSE` | Navegación/Core valida una solución; solo propone | H09-P03 |
| CONN: timón/warp | `CONN_MANEUVER_ORDER` | F05 + motor de movimiento Core, con efecto real | H09-P03 |
| Operaciones: potencia | `OPS_POWER_REQUEST` | OPS/Core decide y reserva; solicitar no reasigna | H09-P04 |
| Ingeniería: soporte | `ENGINEERING_SUPPORT_REQUEST` | Ingeniería/F05/Core, con cola y acuse propio | H09-P04 |
| Nave: estado operativo | `SHIP_STATUS_READ` | Core, filtrado por puesto | H09-P04 |
| Comunicaciones: abrir canal | `COMMUNICATIONS_HAIL_REQUEST` | Comunicaciones/Core; el receptor puede no contestar | H09-P04/P05 |
| Táctica: análisis derivado | `TACTICAL_ASSESSMENT_READ` | Sensores/Core + Táctica; sin fijación ni disparo | H09-P05 |

Los objetivos de la matriz serán **SERVICE_UNAVAILABLE** mientras no exista una ruta real verificada. Es lícito que el menú muestre una opción conceptualmente prevista pero bloqueada y con motivo; no que ejecute scripts de referencia como si fueran Core.

## 4. Contrato de consola limpia (lógico, NO ABI)

### Petición

Sobre H01: `host_contract=1.0`, `session_generation`, `correlation_id`, `operation`. Datos opcionales de intención: `ship_context`, `station_context`, `contact_ref`, `known_result_ref`, `requested_parameters`, `expected_core_revision` e `idempotency_key` según operación.

**El cliente puede elegir lo que intenta hacer, pero nunca demostrar su propia autorización.** `principal`, `observer_id` efectivo, vínculo personaje/nave, facultad de mando, turno/puesto, `F04Ref` y alcance de información se resuelven **dentro de HOST/Core**, no se aceptan de los campos UI. El `contact_ref` solo identifica un contacto **ya conocido por ese observador**; no es acceso a una entidad autoritativa universal. No aceptar `entity_id` verdadero o `ground_truth` desde la interfaz.

Para una mutación: comprobar revisión de Core y clave de idempotencia conforme al dominio real. Si la operación no puede comprometerse atómicamente en el runtime disponible, rechazarla; nunca convertir una propuesta en un éxito por un temporizador o por un acuse de presentación.

### Puertas de admisión en orden

1. Sesión H02 `ACTIVE`, generación actual y hilo propietario, con cancelación/invalidez tras `RESTORE` o `CLOSE`.
2. Identidad H03 vinculada y procedencia de campaña correcta; no confiar en actor suministrado por UI/IA.
3. Nave y estación reales, ocupación de puesto, turno, competencia y delegación vigentes **consultados** a F04/F05/F11 según dominio; el rango no basta.
4. Capacidad de clase/refit efectivamente instalado, estado de matriz/sistema, reservas y recursos disponibles, alcance, destino y prohibiciones físicas.
5. Conocimiento **observador-relativo** y revelación permitida según Core/F06; una nave sin transpondedor puede tener armas detectables, pero identidad no revelada.
6. Antes del compromiso, revalidar autoridad, orden, revisión, recursos, objetivo y plazo para cerrar carreras; solo Core confirma ejecución y consecuencias.
7. Responder estado/recibo y hechos **filtrados**; suscripción H08 para avisos posteriores cuando haya fuente real, sin fabricar `ACTION_COMPLETED`, `REPORT_MADE` ni `DATA_SENT`.

### Respuesta

Sobre H01 más `status`, `generation`, `core_revision`/`core_tick` **si realmente constan**, `authorized_view` o `receipt` **si confirmado**, `pending` cuando corresponda y errores normalizados H01 (`PRINCIPAL_UNBOUND`, `ACCESS_DENIED`, `SCOPE_INVALID`, `REVISION_STALE`, `CAPACITY_LIMIT`, `DOMAIN_REJECTED`, `SERVICE_UNAVAILABLE`).

- Consulta: puede devolver **cero contactos legítimos**, incluso por sector equivocado. Cero contactos no implica ausencia de naves en el mundo.
- Barrido: `trace_detected`, `detected_unclassified`, `partially_resolved`, `resolved`, procedencia, confianza y magnitudes **observadas**; nunca `authoritative_entity_id`, `ground_truth`, censos ocultos, datos no revelados o un arma inventada.
- Orden: separar `submitted`, `accepted`, `executing`, `completed`, `failed`, `refused`, `cancelled` por fuente autoritativa; **`accepted` no es `completed`**.
- Handoff: `package_id`, `payload_refs`, procedencia, destinatario, hora de campaña y estado real de entrega; recibir no equivale a analizar ni a aprobar.
- Navegación: `distanceKm`, `bearingDeg`, `elevationDeg`, curso/velocidad y CPA/TCPA cuando estén **resueltos**; no convertir `vector` legado en rumbo ni fabricar ruta/ETA.

### Entregas y reloj

H08 es transporte de avisos por hechos existentes, **no origen** de observaciones F06 ni segundo planificador. Una consulta no cambia revision, tiempo, RNG, historia ni posición. Una petición de barrido con duración necesita ejecución/reserva real del Core; **no** se usa `f04_advance` por cada refresco LCARS ni se supone que una ventana de animación equivalga a tiempo de campaña. No reintentar mutaciones tras timeout a ciegas. Los acuses visuales nunca sustituyen los acuses F05 o la confirmación de Core.

## 5. Superficie LCARS independiente del casco

La consola funcional mantiene tres áreas: **navegación de función**, **área de tarea/contexto**, **estado persistente** (contactos, matriz, interferencias, tareas, avisos). La interfaz puede mostrar pantallas distintas en Academia y Enterprise-D, pero **reutiliza el mismo contrato**. Cambiar de menú no cancela un trabajo en Core ni activa una acción.

Acciones contextuales: `available` (permiso y capacidad acreditados), `blocked` (explicar sin filtrar datos ocultos) o `irrelevant` (no mostrar). La UI no ofrece «acción óptima» automática ni ejecuta al precargar datos. No se infiere el estado disponible de una regla de color o de un rango visible. Tras `RESTORE`, descartar resultados/tokens de generación anterior y reconstruir la vista consultando al HOST. Dos consolas físicas pueden mostrar la misma familia bajo las restricciones de su puesto; no mantienen copias independientes de la nave.

## 6. Enterprise-D modernizada: perfil sensorial especial, no omnisciencia

El contrato `enterprise_d_valhalla_sensor_superiority_v0.1.json` prevé para `uss_enterprise_ncc_1701_d` con `galaxy_refit_a2` **instalado y operativo** informes completos inmediatos sobre objetivos ordinarios: armamento (tipo, ubicación y estado observable), escudos, propulsión, trayectoria y subsistemas. **No necesita transpondedor para detectar armas que su capacidad real permita observar**. Esto no identifica automáticamente a la nave desconocida ni autoriza revelar información clasificada o físicamente invisible.

El objetivo de respuesta de informe habitual es **1.000 ms**, como **criterio futuro de aceptación**, no medición obtenida. Excepciones extraordinarias necesitan origen tecnológico/narrativo aprobado y trazable; no se inventan fallos aleatorios de barrido para crear suspense. Este perfil **no** se aplica globalmente a cualquier nave ni se convierte en regla autónoma del HOST.

## 7. Transferencia Sensores → Ciencia → Navegación/Mando

1. Sensores entrega un resultado confirmado y filtrado por observador, con `contact_id`, `result_id`, fecha y confianza.
2. El operador inicia un paquete `interconsole_data_package` con **referencias conocidas** y procedencia; la autorización de entrega se comprueba, no se hereda de tener el paquete.
3. Ciencia acepta/rechaza trabajo y genera interpretación con su propia procedencia, o pide más datos. No crea identidades ni datos sensoriales de la nada.
4. Navegación/Astrometría consume la observación permitida y puede **proponer** rumbo; CONN solo mueve la nave al recibir una orden válida que Core compromete.
5. Mando/OPS reciben estados y avisos **filtrados**, no todos los objetos del mundo. H08 presenta transiciones F05 existentes cuando son relevantes.
6. Guardar/cargar debe recuperar la misma verdad y conocimiento. El estado de la pantalla es efímero, los hechos confirmados se conservan en Core, y los acuses/tokens H08 se invalidan con la generación.

Las cadenas con otro observador, otra nave o un rango distinto requieren **nueva autorización real**, incluso aunque el mismo dato hubiera sido visible en la consola de origen.

## 8. Matriz de aceptación para P02–P05

| Caso | Prueba exigida antes de declarar integración | Subfase |
| --- | --- | --- |
| H9-01 | ABI legado `SUBMIT_SCAN` no pasa falsamente por barrido F06 | P02 |
| H9-02 | Puesto no ocupado / actor no vinculado: cero información o efecto | P02 |
| H9-03 | Dos naves/observadores no comparten contacto ni secreto de forma implícita | P02 |
| H9-04 | Nave desconocida sin transpondedor: armas observables sin inventar identidad | P02 |
| H9-05 | Enterprise-D A2 activo informa de sistemas ordinarios sin barridos repetitivos | P02 |
| H9-06 | Firma extraordinaria oculta bajo excepción registrada, sin filtrar verdad | P02 |
| H9-07 | Sector erróneo pero válido puede devolver cero contactos, sin error técnico | P02 |
| H9-08 | Sensor dañado/sin energía: bloqueo cerrado, sin evento ficticio | P02 |
| H9-09 | Orden revocada o autoridad caducada antes de commit: no ejecución | P03 |
| H9-10 | Movimiento real: posición, ruta, reloj y recursos coherentes en Core | P03 |
| H9-11 | SAVE/RESTORE durante barrido o maniobra: sin duplicados ni progreso inventado | P02/P03 |
| H9-12 | Transferencia a Ciencia con procedencia, permisos, resultado independiente | P05 |
| H9-13 | Reasignación de potencia denegada no modifica recursos | P04 |
| H9-14 | LCARS filtra campos y descarta resultados de generación caducada | P05 |
| H9-15 | Escenario interactivo 5–10 minutos **reales**, sin acelerar reloj, apariciones y reacciones verificadas en MSI | P05 |
| H9-16 | Consulta repetida y avisos H08 no alteran estado autoritativo | P02/P05 |
| H9-17 | Ruta astrométrica propuesta no cambia posición hasta orden validada CONN/Core | P03 |
| H9-18 | Cambio de nave/sección y delegación revocada vuelve a comprobar autoridad | P04 |

**Las 18 pruebas son requisitos futuros, no resultados.** Las suites Python de F06/F09 actuales solo cubren referencias. H09 exige pruebas reales Core/F05 y, cuando exista adaptador, automatización y aceptación en UE5/MSI. Registrar commit y entorno por resultado.

## 9. Dependencias, responsables y cierre de P01

- **H09-P01 (ChatGPT)**: inventario, contrato, registro, comprobación estática en CI. No requiere MSI ni cuota de Codex.
- **H09-P02 (Codex)**: adaptar F06 real a Core/HOST, preservar observador, capacidad por nave y semántica de barridos; antes debe reconciliarse con la versión/PR final de F06.
- **H09-P03 (Codex)**: ruta, CONN, tiempo y posición reales; sin motor de movimiento paralelo.
- **H09-P04 (Codex)**: enlaces y autoridad validada entre naves/secciones, OPS/comunicaciones según F09 real.
- **H09-P05 (ChatGPT + Codex)**: contrato/presentación LCARS y E2E Sensores→Ciencia→Mando/CONN. Codex ejecuta la integración delicada y las pruebas MSI cuando proceda.

**Riesgos abiertos:** F06 en desarrollo paralelo, F09 aún referencia, ausencia de barrido/navegación autoritativos en la ABI inspeccionada, dependencia de permisos F04/F05/F11, visibilidad de armas e identidades desconocidas, coste/tiempo y carreras de SAVE/RESTORE. Se rechaza crear un segundo motor para ocultarlos.

**Cierre específico H09-P01:** fuentes y símbolos revisados, registro con 16 familias y matriz de operaciones coherente, casos H9-01…H9-18, pruebas estáticas Ubuntu/Windows aprobadas en PR, revisión y fusión autorizada. **No** implica H09 IMPLEMENTADA ni CERTIFICADA.
