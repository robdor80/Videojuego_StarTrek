# Registro de decisiones y riesgos — 11-10-2026

## Decisiones de autor y de arquitectura (no tomar por la IA sin permiso)

| ID | Estado | Decisión / frontera | Etapa | Observación |
|---|---|---|---|---|
| DEC-0001 | **NECESITA_AUTOR** | Elegir la Dama base entre Galaxy, Sovereign y Odyssey para el diseño de Clase Imperator | F01-P03 | Expediente en `fases/F01/ANALISIS_DAMAS_IMPERATOR.md`; Odyssey no consta en catálogo actual; ninguna elegida |
| DEC-0002 | **NECESITA_AUTOR** | Cerrar alcance exacto de la primera experiencia UE5 y MVP | F01-P04 | Propuesta en `fases/F01/PROPUESTA_MVP_Y_PRESUPUESTO.md`; corte Sensores sin 4 años 3D en v0.0.1, umbrales aún sin aprobar |
| DEC-0003 | **PENDIENTE_TECNICA** | Escoger puente piloto 3D según viabilidad y licencias | F07-P03 | No equivale a elegir Dama final; criterios de prototipo |
| DEC-0004 | **FIJADA_PREVIAMENTE** | RPG Star Trek en 3D para PC y NPC persistentes fuera de escena | F01-P01 / F12 | No reabrir sin solicitud expresa |
| DEC-0005 | **FIJADA_PREVIAMENTE** | Carrera profesional opcional, sin capitanía automática de alférez ni final obligatorio Imperator | F11 | Respetar rutas científica, táctica/operativa y exploración/mando; detalles en fase |
| DEC-0006 | **FIJADA_PREVIAMENTE** | Tres épocas jugables definidas en repositorio | F01-P02 | Revisar decisiones ya escritas, no extender con épocas nuevas por iniciativa propia |
| DEC-0007 | **FIJADA_PREVIAMENTE** | Star Trek canon/rules ≠ Core RPG genérico ≠ UE5 presentación; IA remota no autoritativa | F02–F05 | No mover reglas Star Trek al Core |
| DEC-0008 | **POR_VERIFICAR_EXTERNO** | Adaptadores reales, versiones y responsabilidades concretas Core/UE5 | F02 | Necesita lectura del estado externo; no fijar API hipotética |
| DEC-0009 | **POR_VERIFICAR_EXTERNO** | Licencias y reutilización de mallas de terceros / pipeline Rob3D–UE5 | F07 | Sin incorporar originales a ciegas |

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

F00 no intenta resolver DEC-0001/0002. El usuario autorizó organización y auditoría; **la selección de clase protagonista y el contenido creativo se decidirán en F01**.

## Seguimiento F01 (11-10-2026)

F01-P01 y F01-P02 documentados/auditados; P03 depende de DEC-0001 y P04 de DEC-0002. El riesgo de incluir Odyssey desde material de una cronología fuera del alcance se trata como **pendiente de autorización explícita**; no se modifica el catálogo ni se declara disponibles naves o tecnología fuera de fecha. El expediente de Damas, el de MVP y la matriz de decisiones se encuentran en `docs/roadmap/master/fases/F01/`. La fase permanece EN_CURSO hasta aprobación autoral y validación del PR.
