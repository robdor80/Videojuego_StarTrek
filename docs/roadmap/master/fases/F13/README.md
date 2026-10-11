# F13 — Universo dinámico, exploración y misiones

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

Ampliar un universo persistente que genera situaciones causales y respeta canon/era.

## Pasos y entregables

- [ ] **F13-P01** — Consolidar estado de capas 001–120 y planes procedurales sin confundir contrato con runtime.
- [ ] **F13-P02** — Retomar, siguiendo el orden interno, bloques dinámicos 4–10 (1–3 cerrados a nivel de referencia).
- [ ] **F13-P03** — Integrar navegación, sistemas, planetas, civilizaciones, estaciones, tráfico, recursos, política y economía.
- [ ] **F13-P04** — Cerrar experiencia de primer contacto, Primera Directriz, diplomacia, exploración y misiones emergentes.
- [ ] **F13-P05** — Ejecutar pruebas de simulación fuera de escena, coherencia galáctica, conflicto y consumo de recursos.

## Material ya creado que no se mueve

- `universe/`
- `gameplay/first_contact/`
- `gameplay/conflict/`
- `gameplay/diplomacy/`
- `gameplay/exploration/`
- `docs/roadmap/procedural_layers_master_plan_v0.1.md`
- `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`
- `narrative/`
- `validation/fixtures/procedural_first_contact/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F03–F05 y Core runtime; respetar bloque 4 antes del 5 en adelante sin duplicar subsistemas.

## Puerta de cierre

Mundo con eventos reproducibles, vida persistente y misiones derivadas de estados existentes. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
