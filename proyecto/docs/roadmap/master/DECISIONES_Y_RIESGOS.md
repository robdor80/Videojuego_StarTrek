# Registro de decisiones y riesgos — base 11-10-2026; actualizado 13-10-2026

## Decisiones de autor y de arquitectura (no tomar por la IA sin permiso)

| ID | Estado | Decisión / frontera | Etapa | Observación |
|---|---|---|---|---|
| DEC-0001 | **APROBADA 2026-10-13** | Galaxy/Enterprise-D como base artística para la **nueva Clase Valhalla**; deja de usarse «Imperator» como nombre vigente | F01-P03 | Clase propia, evolución exterior reconocible; **fecha de servicio pendiente**. Acta: `fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md` |
| DEC-0002 | **APROBADA 2026-10-11** | v0.0.1 = prototipo interno exclusivamente de guardia de Sensores, antes del lanzamiento; prototipos sucesivos pueden ensayar Academia | F01-P04 | Política en `proyecto/docs/decisions/prototype_validation_and_release_policy.md`; números FPS/VRAM pendientes de medición F07/F08, y los ensayos no son partes obligatorias del juego final |
| DEC-0003 | **ELECCION_AUTOR_APROBADA / VIABILIDAD_PENDIENTE 2026-10-13** | **USS Sutherland** seleccionado para puente piloto v0.0.1 (Sensores). **Kelvin EXCLUIDO de v0.0.1** y reservado para posibles adaptaciones posteriores Sovereign/Odyssey | F07-P03 | La selección no certifica transitabilidad, materiales ni licencias; no altera Valhalla/Galaxy. Detalle: F07/P03_PUENTE_PILOTO_SUTHERLAND.md |
| DEC-0004 | **FIJADA_PREVIAMENTE** | RPG Star Trek en 3D para PC y NPC persistentes fuera de escena | F01-P01 / F12 | No reabrir sin solicitud expresa |
| DEC-0005 | **FIJADA_PREVIAMENTE** | Carrera profesional opcional, sin capitanía automática de alférez ni final obligatorio Valhalla | F11 | «Imperator» es nombre histórico de trabajo. Rutas científica, táctica/operativa y exploración/mando |
| DEC-0006 | **FIJADA_PREVIAMENTE** | Tres épocas jugables definidas en repositorio | F01-P02 | Revisar decisiones ya escritas, no extender con épocas nuevas por iniciativa propia |
| DEC-0007 | **FIJADA_PREVIAMENTE** | Star Trek canon/rules ≠ Core RPG genérico ≠ UE5 presentación; IA remota no autoritativa | F02–F05 | No mover reglas Star Trek al Core |
| DEC-0008 | **POR_VERIFICAR_EXTERNO** | Adaptadores reales, versiones y responsabilidades concretas Core/UE5 | F02 | Necesita lectura del estado externo; no fijar API hipotética |
| DEC-0009 | **POR_VERIFICAR_EXTERNO** | Licencias y reutilización de mallas de terceros / pipeline Rob3D–UE5 | F07 | Sin incorporar originales a ciegas |
| DEC-0010 | **APROBADA 2026-10-13** | Valhalla: separación de platillo regulada, dos secciones autónomas con hangares híbridos, defensa avanzada, mando NPC independiente y reacoplamiento asistido | F01; F04–F07/F11 | Detalles en acta Valhalla; sistemas sin implementar todavía |
| DEC-0011 | **APROBADA 2026-10-13** | Libertad de continuidad propia: permitir cambios explícitos de cronología/eventos del canon de TV sin añadir época jugable nueva automáticamente | F01-P02 / F11 | Fecha de servicio Valhalla **no fijada**; registrar GAME_ADDITION y reglas de disponibilidad por campaña |
| DEC-0012 | **APROBADA 2026-10-13** | Valhalla incluirá blindaje ablativo desplegable y torpedos transfásicos inspirados en Endgame | F01/F07/F09/F14 | Viabilidad geométrica, visual, balance, reglas y runtime pendientes |
| DEC-0013 | **APROBADA 2026-10-30** | Inicio de la ruta de Academia en **2383**, con cuatro cursos y graduación aproximada en 2387 | F01/F10/F11/LORE-03 | Día/mes abierto; rutas que omiten Academia permanecen válidas. Ver `proyecto/docs/decisions/odyssey_valhalla_program_2383_2387_quantum_slipstream.md` |
| DEC-0014 | **APROBADA 2026-10-30 — GAME_ADDITION** | **Odyssey en servicio y punta de lanza al comenzar Academia (2383)** | F01/F04/LORE-03 | Año aprobado; no implica que Enterprise-F sea automáticamente una nave de 2383. Dotación 1.600 Flota |
| DEC-0015 | **APROBADA 2026-10-30 — GAME_ADDITION** | Programa Valhalla tras Nemesis 2379, **construcción/desarrollo 2380–2387 (7 años)**; primera unidad objetivo 2387 y relevo tecnológico de Odyssey | F01/F04/LORE-03/F11 | **SUSTITUYE** el antiguo objetivo Valhalla 2383. Botadura exacta y coincidencia con graduación abiertas; 1.800 Flota + 400 civiles |
| DEC-0016 | **APROBADA 2026-10-30 — GAME_ADDITION** | Flujo cuántico experimental en Odyssey de ensayos desde 2383; evolución y posible instalación posterior en Valhalla | F04/LORE-02/F05/F11 | **No estándar en todas las Odyssey ni obligatorio en Valhalla en 2387**; permitir misión de pruebas, incidentes, fallos y resultados causales. Detalle en acta DEC-0013–0016 |
| DEC-0017 | **APROBADA 2026-10-31 — GAME_ADDITION** | Proyecto Defiant de Valhalla = **nave de guerra clase Defiant + destacamento de Marines «Hijos de Odín»** | F04/F09/F11/F14 | Los Marines **son soldados**, no un eufemismo de seguridad. Defiant tiene dotación naval especializada distinta. [Acta general](../../decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md) |
| DEC-0018 | **APROBADA 2026-10-31 — GAME_ADDITION** | Federación y Flota conservan exploración/diplomacia y asumen explícitamente disuasión militar y capacidad de ataque contundente, con medios furtivos, militares y posibilidad narrativa de daño extremo | LORE/F09/F11 | Capacidad ≠ autorización ni empleo automático; reglas y consecuencias por diseñar. No implica arma planetaria implementada ni política sin control. [Acta](../../decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md) |
| DEC-0019 | **APROBADA 2026-10-31 — GAME_ADDITION** | Dotaciones Defiant y «Hijos de Odín» **diferenciadas y contenidas en los 1.800 miembros de Flota** de Valhalla | F04/F12/F14 | 60 Marines + 40 dotación naval **solo propuesta numérica no ratificada**; cero personas duplicadas, 400 civiles aparte, mando y turnos específicos. [Acta](../../decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md) |

## Riesgos y mitigación

| ID | Nivel | Riesgo | Mitigación / fase |
|---|---|---|---|
| R-001 | ALTO | Interpretar 120 capas `COMPLETE` como juego terminado | Doble eje de estados, actas y pruebas por madurez (F00, todas) |
| R-002 | ALTO | Core RPG 4.10 no incluya todavía autoridad/delegación genérica | Diseñar Star Trek sin contratos inventados; verificar versión y coordinar 4.10+ (F02, F05) |
| R-003 | ALTO | Dependencia de IA remota detenga el puente o modifique estado | Fallback determinista; validar respuesta al recibir; Core autoridad única (F05, F08) |
| R-004 | ALTO | Crecer en documentación sin llegar a corte UE5 | F08 primer hito jugable verificable; los subplanes se aprovechan, no se rehacen |
| R-005 | ALTO | Recursos 3D de procedencia dudosa o rotos al importar | Licencia, hash/versión, preservar original, prueba materiales/UV/escala (F07, F14) |
| R-006 | MEDIO | Roadmaps especializados diverjan de estado global | Sincronizar enlace/alcance cuando se cierra paso, no duplicar estados falsos |
| R-007 | ALTO | NPC omniscientes o dos actividades incompatibles | Contratos de conocimiento y agendas con invariantes y pruebas (F03, F04, F12) |
| R-008 | ALTO | Renderizado de toda la tripulación degrade MSI RTX4070 8GB | Separar simulación/render, LOD, streaming y perfiles de calidad (F07, F12, F15) |
| R-009 | MEDIO | Academia web y juego mantengan dos verdades divergentes | Delimitar material de estudio vs progreso de partida y sincronización autorizada (F10) |
| R-010 | ALTO | Persistencia incompleta de órdenes, carrera o NPC | F03+F05 y aceptación save/load E2E en F08/F15 |
| R-011 | MEDIO | Ideas nuevas salten fases y provoquen retrabajo | Entrada `proyecto/ideas/` obligatoria y decisión/planificación antes de trabajo (F00) |

## Control de cambios

Cada nueva decisión: `DEC-XXXX` con fecha, alternativas, fundamento, autor/aprobación y archivos afectados. Cada riesgo: actualizar evaluación, plan de mitigación y evidencia de cierre. Los acuerdos ya canonizados **no** se convierten en pendientes por el mero hecho de crear un plan nuevo.

F00 no resolvió DEC-0001/0002. El autor aprobó **DEC-0002** (prueba interna Sensores) el 11-10-2026 y **DEC-0001** (Galaxy como referencia de la nueva Clase Valhalla) el 12–13-10-2026. La fecha de servicio sigue sin fijar. El expediente original conserva «Imperator» solo en su nombre de archivo histórico.

## Seguimiento F01 (11-10-2026)

F01-P01…P05 revisados en [acta de cierre documental de 13-10-2026](fases/F01/ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md). DEC-0001/0002 aprobadas; PR #2 **fusionada**. **F01 CERRADA / DISENO_VALIDADO** únicamente en diseño. Odyssey sigue fuera del catálogo vigente hasta decisión explícita. Tecnologías y naves nuevas requieren GAME_ADDITION y reglas temporales; la autorización conceptual no implica Valhalla disponible en 2372, ni para Pike/Kirk. **El desarrollo real Core/UE5 está pendiente**.

## Actualización F07 — 13-10-2026

El autor autorizó preparar F07 completa y designó USS Sutherland para el ensayo interno de Sensores; se auditaron documentalmente las fuentes ya existentes. Kelvin queda reservado para una futura adaptación Sovereign/Odyssey, sin usarlo en la v0.0.1. Inventario de modelos del MSI pendiente sin fecha; se generarán alias sin renombrar originales. Procedimiento UV/PBR incorporado para placas de blindaje ablativo Valhalla sin implementar daño ni despliegue. F07 EN_REVISION (solo preparación), F08 pausada y Core/UE5 real sin validar. Véase fases/F07/README.md.

## Actualización vigente 2026-10-30 — precedencia temporal

Las decisiones **DEC-0013–0016** son posteriores a los documentos que proponían Valhalla operativa en 2383 o dejaban sin año Odyssey/Valhalla; prevalecen solo para esos aspectos. El registro histórico anterior se conserva sin interpretarlo como autorización para generar una Valhalla de servicio en 2383. La línea tecnológica completa, las autorizaciones y las limitaciones siguen en [el acta transversal](../../decisions/odyssey_valhalla_program_2383_2387_quantum_slipstream.md). F04 sigue **EN_CURSO**; el diseño no equivale a integración en CoreRPG/UE5.

## Actualización de doctrina aprobada 2026-10-31

**DEC-0017–0019** prevalecen en el concepto militar del Proyecto Defiant: nave de guerra furtiva clase Defiant con tripulación naval **especializada en ese buque** y destacamento de Marines **«Hijos de Odín»** como soldados de Flota Estelar. Se mantienen intactos los totales de Valhalla (1.800 Flota + 400 civiles) y las reglas anteriores de camuflaje, atraque simulado y continuidad CoreRPG. La plantilla exacta de ambas dotaciones sigue pendiente de aprobar en F04; no confundir diseño con implementación. [Acta transversal](../../decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md).
