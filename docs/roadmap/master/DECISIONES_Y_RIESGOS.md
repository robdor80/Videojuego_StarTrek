# Registro de decisiones y riesgos — base 11-10-2026; actualizado 13-10-2026

## Decisiones de autor y de arquitectura (no tomar por la IA sin permiso)

| ID | Estado | Decisión / frontera | Etapa | Observación |
|---|---|---|---|---|
| DEC-0001 | **APROBADA 2026-10-13** | Galaxy/Enterprise-D como base artística para la **nueva Clase Valhalla**; deja de usarse «Imperator» como nombre vigente | F01-P03 | Clase propia, evolución exterior reconocible; **fecha de servicio pendiente**. Acta: `fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md` |
| DEC-0002 | **APROBADA 2026-10-11** | v0.0.1 = prototipo interno exclusivamente de guardia de Sensores, antes del lanzamiento; prototipos sucesivos pueden ensayar Academia | F01-P04 | Política en `docs/decisions/prototype_validation_and_release_policy.md`; números FPS/VRAM pendientes de medición F07/F08, y los ensayos no son partes obligatorias del juego final |
| DEC-0003 | **PENDIENTE_TECNICA** | Escoger puente piloto 3D según viabilidad y licencias | F07-P03 | No equivale a elegir Dama final; criterios de prototipo |
| DEC-0004 | **FIJADA_PREVIAMENTE** | RPG Star Trek en 3D para PC y NPC persistentes fuera de escena | F01-P01 / F12 | No reabrir sin solicitud expresa |
| DEC-0005 | **FIJADA_PREVIAMENTE** | Carrera profesional opcional, sin capitanía automática de alférez ni final obligatorio Valhalla | F11 | «Imperator» es nombre histórico de trabajo. Rutas científica, táctica/operativa y exploración/mando |
| DEC-0006 | **FIJADA_PREVIAMENTE** | Tres épocas jugables definidas en repositorio | F01-P02 | Revisar decisiones ya escritas, no extender con épocas nuevas por iniciativa propia |
| DEC-0007 | **FIJADA_PREVIAMENTE** | Star Trek canon/rules ≠ Core RPG genérico ≠ UE5 presentación; IA remota no autoritativa | F02–F05 | No mover reglas Star Trek al Core |
| DEC-0008 | **POR_VERIFICAR_EXTERNO** | Adaptadores reales, versiones y responsabilidades concretas Core/UE5 | F02 | Necesita lectura del estado externo; no fijar API hipotética |
| DEC-0009 | **POR_VERIFICAR_EXTERNO** | Licencias y reutilización de mallas de terceros / pipeline Rob3D–UE5 | F07 | Sin incorporar originales a ciegas |
| DEC-0010 | **APROBADA 2026-10-13** | Valhalla: separación de platillo regulada, dos secciones autónomas con hangares híbridos, defensa avanzada, mando NPC independiente y reacoplamiento asistido | F01; F04–F07/F11 | Detalles en acta Valhalla; sistemas sin implementar todavía |
| DEC-0011 | **APROBADA 2026-10-13** | Libertad de continuidad propia: permitir cambios explícitos de cronología/eventos del canon de TV sin añadir época jugable nueva automáticamente | F01-P02 / F11 | Fecha de servicio Valhalla **no fijada**; registrar GAME_ADDITION y reglas de disponibilidad por campaña |
| DEC-0012 | **APROBADA 2026-10-13** | Valhalla incluirá blindaje ablativo desplegable y torpedos transfásicos inspirados en Endgame | F01/F07/F09/F14 | Viabilidad geométrica, visual, balance, reglas y runtime pendientes |

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
| R-011 | MEDIO | Ideas nuevas salten fases y provoquen retrabajo | Entrada `ideas/` obligatoria y decisión/planificación antes de trabajo (F00) |

## Control de cambios

Cada nueva decisión: `DEC-XXXX` con fecha, alternativas, fundamento, autor/aprobación y archivos afectados. Cada riesgo: actualizar evaluación, plan de mitigación y evidencia de cierre. Los acuerdos ya canonizados **no** se convierten en pendientes por el mero hecho de crear un plan nuevo.

F00 no resolvió DEC-0001/0002. El autor aprobó **DEC-0002** (prueba interna Sensores) el 11-10-2026 y **DEC-0001** (Galaxy como referencia de la nueva Clase Valhalla) el 12–13-10-2026. La fecha de servicio sigue sin fijar. El expediente original conserva «Imperator» solo en su nombre de archivo histórico.

## Seguimiento F01 (11-10-2026)

F01-P01…P05 revisados en [acta de cierre documental de 13-10-2026](fases/F01/ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md). DEC-0001/0002 aprobadas; PR #2 **fusionada**. **F01 CERRADA / DISENO_VALIDADO** únicamente en diseño. Odyssey sigue fuera del catálogo vigente hasta decisión explícita. Tecnologías y naves nuevas requieren GAME_ADDITION y reglas temporales; la autorización conceptual no implica Valhalla disponible en 2372, ni para Pike/Kirk. **El desarrollo real Core/UE5 está pendiente**.
