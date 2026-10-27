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

- `sistemas/universe/`
- `sistemas/gameplay/first_contact/`
- `sistemas/gameplay/conflict/`
- `sistemas/gameplay/diplomacy/`
- `sistemas/gameplay/exploration/`
- `proyecto/docs/roadmap/procedural_layers_master_plan_v0.1.md`
- `proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`
- `sistemas/narrative/`
- `desarrollo/validation/fixtures/procedural_first_contact/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F03–F05 y Core runtime; respetar bloque 4 antes del 5 en adelante sin duplicar subsistemas.

## Puerta de cierre

Mundo con eventos reproducibles, vida persistente y misiones derivadas de estados existentes. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).


## Avance autónomo de referencia — 14-10-2026

Preparación **P01–P05** con auditoría de capas 001–120, puerta estricta de bloques dinámicos 4→10, economía/tráfico/recursos/disrupciones, Primera Directriz y primer contacto, derivación de misiones desde necesidades preexistentes y replay causal determinista **solo offline**. Ver [acta de evidencias y bloqueos](ACTA_P01_P05_REFERENCIA_2026-10-14.md).

- Ejecutor sin autoridad Core: `desarrollo/tools/validation/f13_dynamic_universe_reference.py`.
- **44 escenarios** sintéticos y no canónicos: `desarrollo/validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json`.
- Pruebas unitarias: `desarrollo/tools/validation/test_f13_dynamic_universe_reference.py`.
- CI: `.github/workflows/f13-dynamic-universe-reference.yml`.

La preparación conserva 001–118 en su madurez declarada, 119 `PARTIAL`, 120 `BLOCKED_RUNTIME` y el **bloque 4 como siguiente bloque real**. No cierra el bloque 4 ni implementa 5–10; el uso del contrato de misión emergente solo valida la frontera causal y no adelanta el bloque 9.

**No hay mutaciones de World State, integración CoreRPG, save/load real ni ejecución UE5/MSI.** F13 continúa globalmente `PLANIFICADA` y F02 sigue siendo la única fase principal `EN_CURSO`.
