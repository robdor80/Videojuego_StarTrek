# F01-P05 — Matriz de decisiones, procedencia y alcance

**Fecha:** 2026-10-11 · **Estado:** EN_REVISION — DEC-0002 aprobada; falta únicamente DEC-0001 y el acta de cierre.

## Aprobadas previamente (sin reinterpretación)

| Decisión | Estado | Documento fuente | Consecuencia |
|---|---|---|---|
| Tres épocas: Pike, Kirk, TNG/DS9/Voyager | VIGENTE | `docs/decisions/playable_eras.md` | F01-P02, F03, F11; no cuarta época tácita |
| Canon hasta fecha D, luego historia emergente | VIGENTE | `docs/decisions/campaign_continuity.md` | Los episodios no son guion obligatorio |
| Castellano es-ES al jugador | VIGENTE | `docs/decisions/player_facing_language.md` | Menús, diálogos, mensajes |
| Simulación autoritativa previa a observación | VIGENTE | `docs/decisions/authoritative_observable_universe.md` | Core y Sensores, F03/F06 |
| Academia jugable y formación real | VIGENTE | `docs/decisions/academy_playable_hub.md`, `gameplay/careers/academy_path/academy_career_v0_2.md` | Cuatro años, especializaciones, graduación |
| Crecimiento sin barra de XP genérico | VIGENTE | `docs/decisions/character_growth_without_xp.md` | Evaluación profesional por evidencia |
| Objetivos del personaje no garantizan acontecimientos | VIGENTE | `docs/decisions/player_objectives.md` | Ascenso/Imperator opcionales |
| Separar rango, puesto, destino y consola | VIGENTE | `docs/decisions/personnel_model.md` | Mando no derivado solo de rango |
| Clase, rol y nave individual diferentes | VIGENTE | `docs/decisions/starship_identity_model.md` | Imperator requiere identidad propia |
| Lore para reglas jugables, no enciclopedia | VIGENTE | `docs/decisions/lore_to_game_rule.md` | Contratos en siguientes fases |
| Fuentes y añadidos etiquetados | VIGENTE | `sources/canon_policy.md`, `sources/provenance_policy.md` | Conflictos se registran; no canon artificial |
| Primer corte **interno** v0.0.1, solo guardia Sensores | APROBADO para pruebas, no lanzamiento | `docs/decisions/prototype_validation_and_release_policy.md`, `docs/roadmap/ship_console_vertical_slice_v0_0_1.md` | F06–F08; código reutilizable, datos de laboratorio descartables |
| RPG 3D en PC, carrera opcional, universo persistente | VIGENTE como decisión de producto | `docs/roadmap/master/PLAN_MAESTRO.md`, `docs/vision/VISION_PRODUCTO_RPG_3D_v0.1.md` | F01-P01 y sucesivas |
| Prioridad Core genérico / Trek específico / UE5 visual | VIGENTE | `docs/roadmap/game_design_readiness_v0_2.md` | No duplicar runtime |

## Pendientes expresas de autor

| ID | Cuestión | Alternativas / material | Estado |
|---|---|---|---|
| DEC-0001 | Base de Clase Imperator | Galaxy / Sovereign / Odyssey; el autor considera E por ahora pero espera Codex | NECESITA_AUTOR; SIN ELEGIR |
| DEC-0002 | Alcance primer prototipo interno | v0.0.1 guardia de Sensores, exclusivamente para validación; no forma parte automáticamente de campaña final; `PROPUESTA_MVP_Y_PRESUPUESTO.md` | APROBADA, 2026-10-11 |
| DEC-0003 | Puente piloto / licencia | Selección técnica y licencias en F07, **no** resolver en F01 | PENDIENTE_TECNICA |

## No aprobadas / límites

- No se ha aprobado Odyssey como clase disponible en 2372; tampoco se ha elegido una Dama.
- Los prototipos `v0.0.x` **no son lanzamientos** ni las misiones y datos de laboratorio se incorporan automáticamente al juego definitivo. La posible `v0.0.2` de Academia está planteada, no comprometida.
- No se ha aprobado un número concreto de FPS, de tripulantes simultáneos renderizados ni un rendimiento UE5 garantizado.
- No se ha decidido un final obligatorio en Imperator, ni capitanía automática al graduarse.
- No se ha aprobado ampliar cronología por asumir una nave futura ni reescribir conflictos de fuente.
- No se ha aprobado sustituir el estado autoritativo por resultados generados libremente por IA.

## Evidencias / límites

Comparación de los documentos citados contra `main@0f989948c028792c2f8802996161ca98b26ec572` y rama de F01; no se han ejecutado suites, UE5 ni benchmarks. Cierre de fase supeditado a DEC-0001, validaciones documentales y PR fusionada.

**Proceso al terminar Codex y decidir el autor:** registrar fecha, Dama, época aplicable y justificación en `DECISIONES_Y_RIESGOS.md`; actualizar `ANALISIS_DAMAS_IMPERATOR.md`, esta matriz y estado global; después cumplir puerta de cierre F01.
