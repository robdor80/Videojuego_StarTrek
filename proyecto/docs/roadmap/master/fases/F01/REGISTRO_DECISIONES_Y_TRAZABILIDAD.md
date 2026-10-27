> **Actualización autoral 2026-10-23:** La primera fila de esta matriz, que considera **vigentes tres épocas jugables**, refleja exclusivamente la decisión F01 anterior. Prevalece desde esta fecha **TNG/DS9/Voyager como única época jugable** (véase `proyecto/docs/decisions/playable_eras.md`). Los antecedentes Pike/Kirk no se eliminan.

# F01-P05 — Matriz de decisiones, procedencia y alcance

**Fecha base:** 2026-10-11 · **Cierre de gobierno:** 2026-10-13 · **Estado:** CERRADA en diseño F01-P05; DEC-0001/0002 aprobadas y QA de expediente verificada. [Acta de cierre](ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md).

## Aprobadas previamente (sin reinterpretación)

| Decisión | Estado | Documento fuente | Consecuencia |
|---|---|---|---|
| Tres épocas: Pike, Kirk, TNG/DS9/Voyager | VIGENTE | `proyecto/docs/decisions/playable_eras.md` | F01-P02, F03, F11; no cuarta época tácita |
| Canon hasta fecha D, luego historia emergente | VIGENTE | `proyecto/docs/decisions/campaign_continuity.md` | Los episodios no son guion obligatorio |
| Castellano es-ES al jugador | VIGENTE | `proyecto/docs/decisions/player_facing_language.md` | Menús, diálogos, mensajes |
| Simulación autoritativa previa a observación | VIGENTE | `proyecto/docs/decisions/authoritative_observable_universe.md` | Core y Sensores, F03/F06 |
| Academia jugable y formación real | VIGENTE | `proyecto/docs/decisions/academy_playable_hub.md`, `sistemas/gameplay/careers/academy_path/academy_career_v0_2.md` | Cuatro años, especializaciones, graduación |
| Crecimiento sin barra de XP genérico | VIGENTE | `proyecto/docs/decisions/character_growth_without_xp.md` | Evaluación profesional por evidencia |
| Objetivos del personaje no garantizan acontecimientos | VIGENTE | `proyecto/docs/decisions/player_objectives.md` | Ascenso a mando de Valhalla opcional; «Imperator» es el nombre histórico provisional |
| Separar rango, puesto, destino y consola | VIGENTE | `proyecto/docs/decisions/personnel_model.md` | Mando no derivado solo de rango |
| Clase, rol y nave individual diferentes | VIGENTE | `proyecto/docs/decisions/starship_identity_model.md` | La nueva Clase Valhalla tendrá identidad propia distinta de la Enterprise-D |
| Lore para reglas jugables, no enciclopedia | VIGENTE | `proyecto/docs/decisions/lore_to_game_rule.md` | Contratos en siguientes fases |
| Fuentes y añadidos etiquetados | VIGENTE | `mundo/sources/canon_policy.md`, `mundo/sources/provenance_policy.md` | Conflictos se registran; no canon artificial |
| Primer corte **interno** v0.0.1, solo guardia Sensores | APROBADO para pruebas, no lanzamiento | `proyecto/docs/decisions/prototype_validation_and_release_policy.md`, `proyecto/docs/roadmap/ship_console_vertical_slice_v0_0_1.md` | F06–F08; código reutilizable, datos de laboratorio descartables |
| RPG 3D en PC, carrera opcional, universo persistente | VIGENTE como decisión de producto | `proyecto/docs/roadmap/master/PLAN_MAESTRO.md`, `proyecto/docs/vision/VISION_PRODUCTO_RPG_3D_v0.1.md` | F01-P01 y sucesivas |
| Prioridad Core genérico / Trek específico / UE5 visual | VIGENTE | `proyecto/docs/roadmap/game_design_readiness_v0_2.md` | No duplicar runtime |

## Decisiones del autor y pendientes técnicos

| ID | Cuestión | Alternativas / material | Estado |
|---|---|---|---|
| DEC-0001 | Base e identidad de Clase Valhalla (antes «Imperator») | **Galaxy/Enterprise-D seleccionada** como inspiración de clase nueva, modernización exterior reconocible | **APROBADA 2026-10-13** |
| DEC-0002 | Alcance primer prototipo interno | v0.0.1 guardia de Sensores, exclusivamente para validación; no forma parte automáticamente de campaña final; `PROPUESTA_MVP_Y_PRESUPUESTO.md` | APROBADA, 2026-10-11 |
| DEC-0003 | Puente piloto / licencia | Selección técnica y licencias en F07; **no** viene determinada por Galaxy/Valhalla | PENDIENTE_TECNICA |
| DEC-0010 | Operativa Valhalla | Dos secciones con mando autónomo, separación/reacoplamiento, hangares y dotaciones | APROBADA, diseño; runtime pendiente |
| DEC-0011 | Cronología propia | El autor puede alterar canon televisivo expresamente; **fecha servicio Valhalla no fijada** | APROBADA como política, fecha pendiente |
| DEC-0012 | Tecnología avanzada Valhalla | Blindaje ablativo desplegable y torpedos transfásicos | APROBADA, diseño; viabilidad 3D pendiente |

## No aprobadas / límites

- **La base creativa sí ha sido elegida: Galaxy**. No se ha aprobado Odyssey como clase disponible en 2372 ni la fecha de entrada en servicio de Valhalla.
- Los prototipos `v0.0.x` **no son lanzamientos** ni las misiones y datos de laboratorio se incorporan automáticamente al juego definitivo. La posible `v0.0.2` de Academia está planteada, no comprometida.
- No se ha aprobado un número concreto de FPS, de tripulantes simultáneos renderizados ni un rendimiento UE5 garantizado.
- No se ha decidido un final obligatorio en Valhalla (antes Imperator), ni capitanía automática al graduarse.
- Se admite **continuidad de juego propia** y alteración temporal expresa de acontecimientos como la tecnología de «Endgame»; eso **no** equivale a desplegar tecnología futura en todas las épocas o a introducir Odyssey en 2372 automáticamente.
- No se ha aprobado sustituir el estado autoritativo por resultados generados libremente por IA.

## Evidencias / límites

Comparación de los documentos citados contra `main@0f989948c028792c2f8802996161ca98b26ec572` y rama de F01; no se han ejecutado suites, UE5 ni benchmarks. **DEC-0001 está resuelta**. Cierre de fase pendiente de QA documental, validaciones de gobierno y acta de cierre; la fusión de PR #2 es un paso de integración documental independiente, sin afirmar UE5/Core integrados.

**Registro de resolución:** Galaxy → nueva Clase Valhalla; quedan pendientes la fecha de servicio y los resultados técnicos. Véase [acta creativa completa](ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md). Actualizar estado global sin fingir cierre, mantener QA documental y seguir el orden de fusión de PR previamente acordado. El merge por sí solo no modifica la madurez técnica.
