# HOST H09-P03 — Auditoría, arquitectura y plan de Navegación / CONN

**Fecha:** 27-11-2026. **Responsable:** ChatGPT (preparación) / Codex Cloud (implementación compleja futura).  
**Estado:** PLANIFICADO + DISEÑO DOCUMENTAL; **no implementado, probado en Core, certificado ni jugable en UE5**.  
**Baseline auditada:** `main@1242f7852f435e59a80ae0eddab9edf968052dc1`.  
**Alcance:** exclusivamente H09-P03. No desbloquea H09-P02, no valida F06, no inicia H09-P04 y no requiere MSI.

## 1. Alcance vigente y evidencias reales

El [Plan Maestro HOST v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md) especifica **H09-P03 [X]: «Navegación, órdenes de timón y cronología de viaje según fase general correspondiente»**, con dependencia general de H06/H08 y contratos F06/F09. Esta preparación separa las partes que **no** requieren observaciones F06 del trabajo que **sí** las necesita; el plan no debe leerse como obligación de ejecutar P02 antes de cualquier análisis de P03.

**Inspección en `main` a 27-11-2026:**

| Área | Artefacto verificado | Evidencia / madurez |
| --- | --- | --- |
| Core fijo | `desarrollo/integration/host/CMakeLists.txt` | Fija Core SHA `76a7b7b485616d8c4994f384a90f123bf333591d` y exige checkout limpio. **No cambiar el pin**. No se auditó aquí el árbol externo completo de Core. |
| HOST real | `desarrollo/integration/host/include/trek/host/session_owner.h`, `src/native_session.h` y `src/gateway.h` | SessionOwner, vista de campaña, cola propietaria y guardado/carga; operaciones nativas de vista, orden F05, reloj H08. **No consta una API nativa de ruta ni de desplazamiento naval** en las superficies inspeccionadas. |
| F04 | `desarrollo/integration/f04/include/f04_bridge.h` | Existe `F04_ST_HELM`, `F04_Q_HELM`, `F04_Q_ASTROMETRY` y `F04_MOVE`. **El nombre `F04_MOVE` no acredita mover una nave espacial**; corresponde al dominio de acciones F04 y exige auditoría semántica en Core. |
| F05 | `desarrollo/integration/f05/include/f05_orders.h` | `F05OrderRequest` indica expresamente **P01 soporta solo `F04_SCAN`, sin parámetros**. `f05_submit/receive/execute_order` no permiten afirmar timón, destino, warp, impulso ni ruta. |
| H08 | `H08_P03_RELOJ_ACTIVIDADES_CORE_2026-11-23.md`, `session_owner.h` | Existe avance explícito acotado por `f04_advance` a través de HOST. El tick/agenda Core son autoritativos; **avanzar el reloj no demuestra movimiento de naves**. |
| UE5 | `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`, `Source/StarTrekRPG/Private/HostSessionSubsystem.h` | Proyecto 5.8.4 real y subsistema de sesión, Academy y consultas. **No aparece API de navegación/CONN** en la interfaz inspeccionada. MSI no disponible para verificación presencial. |
| F09 | `sistemas/gameplay/ship_operations/consoles/f09_reference_matrix_v0.1.json` | `navigation` y `conn` son dos familias lógicas de las 16. `navigation → conn` es ruta de datos permitida de referencia, no ejecución. |
| H09-P01 | `H09_P01_REGISTRO_CONSOLAS_v1.json` | Identifica exactamente `NAVIGATION_ROUTE_PROPOSE` (propuesta) y `CONN_MANEUVER_ORDER` (intención de mutación), ambas indisponibles en runtime. PR #211 y #225 fusionadas. |
| Navegación Fxx | `sistemas/gameplay/navigation/README.md`, `navigation_order_contract.json`, `navigation_state.json` | Bucle, ocho intenciones y estado objetivo descritos; **no motor Core probado**. |
| Cartografía | `anchor_route_graph.json`, `navigation_distance_edge_model.json`, `route_cost_model.json`, `route_context_model.json`, `astrography_location_model.json` | Semilla de nodos/rutas, perfiles y fuentes de distancias; **referencia, no ubicación mutable ni solver ejecutable**. Enlaces de distancia nula no producen ETA cuantificada. |
| Astrometría S11 | `sistemas/gameplay/astrometrics/s11_projection_contract_v0.1.json`, `sistemas/gameplay/ship_operations/interconsole/s11_astrometrics_to_navigation_route_proposal_v0.1.json` | Handoff de propuesta aprobado en diseño; `runtime_implemented=false`. Astrometría no ejecuta movimientos. |
| Estado de nave | `sistemas/gameplay/ship_operations/starship_state_model.json` | `current_location` es esquema de autoría, **no campo verificado de WorldState Core**. |
| Órdenes nave | `sistemas/gameplay/orders/starship_order_pipeline.md` | Intención ≠ validación ≠ ejecución ≠ consecuencia; un recibo F05 ISSUED no autoriza anunciar movimiento. |
| Sensores F06 | referencia F06, PR Draft #213 y #215 al 27-11-2026 | Jugabilidad pendiente de aceptación presencial del propietario; H09-P02 **BLOQUEADA**. No asumir observaciones vivas de F06. |

### Auditoría adicional del CoreRPG fijado y de los laboratorios F02/F03

La auditoría se ha extendido directamente al repositorio preexistente [`robdor80/CoreRPG`](https://github.com/robdor80/CoreRPG) en el **commit exacto `76a7b7b485616d8c4994f384a90f123bf333591d`**, consultado por GitHub en modo lectura. Se examinó el árbol completo de nombres (205 rutas, sin truncamiento) y las interfaces públicas relevantes:

| Fuente en CoreRPG fijado | Capacidad realmente publicada | Límite naval |
| --- | --- | --- |
| [`include/corerpg/world_state.hpp`](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/include/corerpg/world_state.hpp) | `WorldState`, `container_of`, `place_entity`, `remove_containment`, revisiones, relaciones, conocimiento por observador | La contención entre entidades **no es una posición continua, rumbo, velocidad ni trayecto físico de nave** |
| [`include/corerpg/action.hpp`](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/include/corerpg/action.hpp) | `ActionEngine::process`; variantes cerradas **PlaceEntity, RemoveContainment, AddRelation, RemoveRelation, StreamRoll** | **No publica operaciones Warp/Impulse/NavRoute/ShipPosition** |
| [`include/corerpg/timeline.hpp`](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/include/corerpg/timeline.hpp) | `Timeline::schedule`, `advance`, `TimedAction`; eventos genéricos ordenados por tick; agenda limitada a 4.096 registros | El tiempo Core sí es reutilizable, pero **no existe avance automático de segmentos de vuelo** por introducir una `TimedAction` |
| [`docs/phases/f03-authoritative-timeline.md`](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/docs/phases/f03-authoritative-timeline.md) | Persiste `WorldState`, RNG, cronología y acciones de tiempo mediante `CampaignPersistence` | El propio documento excluye explícitamente **galactic simulator/travel model** del alcance de esa fase |
| `desarrollo/integration/f03/include/f03_bridge.h` de Star Trek | `f03_schedule_route` y `f03_marker_state`, en **laboratorio experimental independiente** | Ruta de sectores con llegadas programadas: NO sistema de vuelo warp; no integrarla como motor HOST producto |
| `desarrollo/integration/f02/include/f02_bridge.h` de Star Trek | `f02_place` de un sujeto en contenedor | Ejemplo de contención Core, NO cambio continuo de posición naval |

**Conclusión demostrada para las API públicas del pin inspeccionado:** CoreRPG ofrece primitivas fiables para hechos, contención, conocimiento, acciones, tiempo y persistencia, **pero no expone una API de vuelo naval, solver espacial, velocidad warp o movimiento progresivo**. Esto no descarta código de dominio aún no publicado fuera de esas superficies; a fecha de auditoría no existe prueba que autorice afirmar su disponibilidad. No confundir `f03_schedule_route` sintética ni `F04_MOVE` de acciones F04 con un motor de vuelo.

**Consecuencia técnica:** la primera tarea de Codex no consiste en reexplorar aleatoriamente el repositorio, sino en evaluar si existe una **ampliación mínima de dominio naval** que use el único WorldState/tick Core, respete el pin y su política de cambios, y no introduzca estado paralelo. Si requiere modificar el Core fijado o ampliar ABI, elevar primero la decisión arquitectónica al propietario. No programar warp por aproximación ni fabricar el cambio de localización.


## 2. Frontera de responsabilidad: un solo universo

| Dominio | Responsabilidad exclusiva | Prohibición |
| --- | --- | --- |
| **CoreRPG / navegación autoritativa de dominio (si existe)** | Posición y orientación de naves, avance por segmentos, velocidad efectiva, propulsión, riesgos/encuentros, cronología, consecuencias, persistencia, RNG y resultado final | Ninguna segunda posición de verdad en HOST/UE |
| **F04/F05** | Dotación y puesto, cualificación/guardia, órdenes, aceptación y ejecución **solo de tipos realmente implementados** | No reinterpretar `F04_MOVE` ni `F04_SCAN` como «warp» |
| **F11** | Nombramientos, atribuciones y competencias institucionales confirmadas | No otorgar mando desde un menú ni inferir competencia por un grado visual |
| **HOST** | Sesión única, identidad confiable, validación de generación, despacho al dominio instalado, correlación, relectura, acceso observador y proyección efímera | No solver de ruta, física, temporizador de viaje ni estado paralelo |
| **Navegación** | Cálculo/validación de rutas basadas en cartografía conocida, estado y límites **en el sistema dueño de navegación**, una vez presente en Core | Nunca ejecutar por solo seleccionar ruta |
| **CONN** | Transmitir orden de pilotaje autorizado hacia motor de movimiento Core, observar recibos y progreso | No cambiar `current_location` desde Blueprint |
| **Astrometría S11** | Presentar mapa y **solicitar** propuesta de ruta usando handoff existente | No autoridad para ejecutar maniobra |
| **F06** | Observaciones vivas, contactos, amenazas móviles y datos detectados según conocimiento | No requisito para destinos publicados en cartas; sí para interceptación/seguimiento de contactos |
| **Unreal/LCARS** | Introducción de intención, selección, simulación **visual** y presentación de hechos confirmados | No verdad, permisos, ETA inventada ni confirmación anticipada |
| **IA/voz** | Parseo opcional y expresión de vistas autorizadas | No autoejecutar orden ni revelar datos ocultos |

**Un ejemplo:** «Rumbo a Vulcano, warp 6» se interpreta en solicitud estructurada. Navegación consulta carta conocida y estado auténtico, propone ruta con procedencia y ETA solo si un motor real puede calcularla. El oficial de CONN y la autoridad válida tramitan una **orden diferente**. La nave no llega a Vulcano al pulsar «Aceptar»: Core modifica posición/tiempo únicamente según la mecánica real implementada. Si falta, el HOST devuelve `SERVICE_UNAVAILABLE` y no fabrica desplazamiento.

## 3. Independencia respecto a F06 y dependencias diferidas

**Adelantable sin F06 ni H09-P02:**

1. Modelo lógico de consulta de **posición propia** si Core la publica realmente; carta y destino conocido por procedencia, no por un escaneo ficticio.
2. Preparación de propuestas para destinos con carta autorizada: catálogo de rutas, preferencias ya establecidas (`fastest`, `safest`, `avoid_hostile_space`, `prefer_starbase_support`, `silent_or_low_contact`), incertidumbres/ETA desconocida y límites de clase/refit.
3. Protocolo separado `navigation → conn`: entregar **datos de propuesta**; la recepción no equivale a aceptación de orden.
4. Puertas de sesión, identificación, guardia HELM, autenticación y revalidación al comprometer. SAVE/RESTORE, invalidación de generación y UX negativa.
5. Auditoría técnica del motor Core del pin actual; pruebas de documentación, referencias y denegación.

**Dependiente de fuente sensorial F06 aceptada e integrada o de dominio equivalente realmente verificado:** interceptar/seguir un contacto móvil, corregir trayectoria según amenazas recién detectadas, peligros y colisiones dinámicas no documentados en cartas y mostrar estimaciones de contacto como si fueran observaciones. `target_contact_id` requiere resolver conocimiento por observador. No sustituir con datos de escenario Python ni con `ground_truth`.

**Dependiente de capacidad nativa Core aún no acreditada:** posición espacial, integrador de movimiento, actualización temporal por segmentos, consumo de propulsión, ETA calculada, eventos de viaje, orden CONN ejecutable y recuperación en mitad de trayectoria. Si la capacidad no existe en pin aprobado, **P03 de runtime está bloqueada por dependencia real del dominio**, no se «soluciona» con un simulador paralelo.

## 4. Orden de las subfases internas

| Paso | Tarea | Responsable | Dependencia | Entrega y criterio de cierre |
| --- | --- | --- | --- | --- |
| **P03-A** | Auditoría repositorio, pin, fuentes y puertas | ChatGPT | H09-P01 | Informe con estado real, riesgos y referencias: **documental** |
| **P03-B** | Contratos lógicos, matriz negativa y pruebas estáticas | ChatGPT | A | Registro JSON + contrato + validador CI Linux/Windows: **documental** |
| **P03-C** | Descubrimiento **en Core fijado**: movimiento, rutas, posición, reloj, persistencia, F04/F05 y costuras ABI | **Codex Cloud, Sol 6.2 Medium** | A/B | Informe de factibilidad con símbolos/archivos, prueba reproducible y decisión de puerta. Ningún pin cambiado |
| **P03-D** | Adaptador nativo de **lectura/propuesta** de navegación de destinos conocidos, solo si C acredita API autoritativa; de lo contrario, declarar bloqueo | **Codex** | C + fuente Core real | Tests nativos Linux/Windows, lectura por observador, no mutación, fallos tipados |
| **P03-E** | Orden CONN, efectos de viaje y tick real, solo con motor Core y autoridad F04/F05 adecuada **demostrados** | **Codex** | C/D + capacidad dominio aprobada | Pruebas nativas de segmento, recursos, revocación, idempotencia, restauración sin doble avance. Ningún parche arbitrario Core ni pin |
| **P03-F** | Adaptación UE/LCARS y pruebas de extremo a extremo | **Codex** integración, ChatGPT auditoría, propietario aceptación | D/E + MSI | Ciclo controlado UWorld; pruebas Editor/Game/MSI y observación humana. No ejecutar hoy |
| **P03-G** | Auditoría independiente, actas y cierre H09-P03 | ChatGPT; propietario fusión significativa | D–F según criterio | Evidencias por commit/plataforma; CERTIFICADO solo si corresponde al alcance real |

**Regla de no dependencia artificial:** C y el contrato base de D pueden progresar **sin P02**. Si un caso exige contacto dinámico, queda etiquetado `F06_GATE` y no bloquea rutas de cartas. E exige un motor de movimiento autoritativo, **no se presupone su existencia**. F requiere MSI, no la presente sesión.

## 5. Contrato lógico de un itinerario (NO ABI, NO runtime)

El contrato formal está en [`H09_P03_CONTRATO_NAVEGACION_CONN_v1.json`](H09_P03_CONTRATO_NAVEGACION_CONN_v1.json); conserva las **dos** operaciones H09-P01:

**`NAVIGATION_ROUTE_PROPOSE`**: intención para un destino conocido, preferencias y procedencia; produce `route_proposal`, `clarification_required` o rechazo. La propuesta se calcula exclusivamente por el resolvedor de navegación del dominio real. No cambia estado naval, tick ni recursos. Se requiere distinguir destino homónimo, borde político conocido, ruta sin distancias suficientes (`eta=null`) y dato de carta caducado. `proposal_id` real no se inventa si el motor no ha creado uno.

**`CONN_MANEUVER_ORDER`**: intención posterior, explícita y diferente, con `proposal_ref` vigente o parámetros de maniobra tipados aceptados por el dominio; exige sesión, actor, puesto, autoridad, capacidades, estado de propulsión y revisión Core actual. Su `ACCEPTED` **no** equivale a ejecutar ni avanzar posición; el resultado del dominio debe acreditar progreso y efecto real. Si el adaptador/orden no existe, `SERVICE_UNAVAILABLE`.

**Handoff:** S11 → familia `navigation` y `navigation` → familia `conn`. El `conn_navigation` legado del contrato interconsolas se **desambigua**; no crear tercera familia ni aceptar acciones por recibir un paquete. El tránsito de metadatos tiene procedencia y límites de vista.

**Seguridad temporal:** la referencia de propuesta está ligada al identificador de campaña, generación, revisión de datos y posición propia. Si cambian, revalidar o invalidar; tras `RESTORE` nunca reusar un recibo de sesión como si acreditase el nuevo WorldState. La ejecución progresiva se vincula a tick Core real; un reloj UE o H08 visual no mueve la nave.

**Coordenadas y rendimiento:** no convertir Z desconocido a 0, no asumir la misma escala para galaxia y cámara, no equiparar camino de grafo con trayectoria física exacta. Distancia o velocidad efectivas desconocidas → ETA indeterminada, **no** cero. No imponer fórmula warp universal. Ningún «warp instantáneo».

## 6. Matriz de aceptación proyectada

La referencia estructurada contiene los casos **N3-01…N3-24**. Son requisitos **pendientes**, no pruebas ejecutadas. Clasificación: `INDEPENDENT` para 01–17 y `F06_GATE` para 18–24.

| Casos | Escenario mínimo exigido | Responsable de demostración |
| --- | --- | --- |
| N3-01–N3-03 | destino conocido, homónimo y desconocido sin filtración | P03-D / Codex |
| N3-04–N3-07 | rutas preferidas, ETA nula si faltan datos, origen/coords no falsificados, fronteras conocidas | P03-D |
| N3-08–N3-11 | Handoff S11→Navegación→CONN, propuesta no muta Core, estación sin autorización rechazada | P03-D/E |
| N3-12–N3-14 | revisión caducada, retirada de permiso y error tras RESTORE/CLOSE | P03-D/E |
| N3-15–N3-17 | orden sin ejecución no desplaza, avance parcial persistente, SAVE/LOAD durante viaje | P03-E |
| N3-18–N3-24 | contacto no descubierto, interceptación, riesgo recién detectado, actualización de sensor, datos redacted, cambios de conocimiento y E2E con F06 | Tras aceptación e integración F06 |

N3-01–17 son independientes **de F06**, pero N3-15–17 siguen **condicionados al motor real de movimiento de Core**. Las 24 pruebas **no se consideran PASS hoy**. La CI preparatoria solo comprueba **contratos estáticos**, además de las regresiones compartidas cuando Actions las lance.

## 7. Riesgos, decisiones y prohibiciones

- **R1 — alta:** El pin CoreRPG y las ABI F04/F05 inspeccionadas **no acreditan movimiento naval**. Las API públicas del Core fijado se han auditado y **no publican vuelo naval**; Codex debe proponer la extensión de dominio mínima y dependencias, **sin alterar el Core fijado**.
- **R2 — alta:** Confundir `F04_MOVE` de F04 con traslado de nave, o F05 `F04_SCAN` con una orden de warp. Prohibido.
- **R3 — alta:** Dos posiciones, avance fantasma por tick UE/H08, duplicados de resultado al reintentar, teletransporte en UI. Prohibido.
- **R4 — alta:** Rutas y contactos con verdad no descubierta o permiso fabricado. Respuesta filtrada y revisión siempre desde fuente auténtica.
- **R5 — media:** Métricas y trayectos ausentes o imprecisos. Mostrar incertidumbre; no fabricar `z=0`, ETA, velocidades ni calendario.
- **R6 — media:** Selección de nave y ventajas de la Enterprise-D modernizada. Capacidad efectiva por definición/refit y daño; no globalizar transwarp ni límites.
- **R7 — integración:** MSI no disponible; no afirmar trabajo UE, aceptación visual ni certificación de navegación.
- **R8 — alcance:** P02 sigue BLOQUEADA hasta aprobación F06; no iniciar P04.

**Criterio de cierre de la parte ChatGPT:** documento y registro coherentes con fuentes vivas, validador en Linux/Windows, PR y fusión documental autorizada. **No equivale a cerrar H09-P03**. Primera intervención posterior: Codex Cloud, Sol 6.2 Medium, con trabajo acotado de factibilidad nativa y posible adaptador solo tras prueba de API real.
