# F12 — Vida a bordo, NPC y relaciones

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

Simular tripulación persistente sin necesidad de cargar simultáneamente todos los actores 3D.

## Pasos y entregables

- [ ] **F12-P01** — Reutilizar identidad, horarios, bienestar, hábitos, personalidad, memoria y relaciones.
- [ ] **F12-P02** — Resolver exclusividad temporal, lugares, relevos, visitas, descanso y obligaciones fuera de servicio.
- [ ] **F12-P03** — Integrar iniciativa social NPC↔NPC, consecuencias, privacidad y límites de conocimiento.
- [ ] **F12-P04** — Aplicar LOD de simulación, actualización fuera de escena y representación 3D bajo demanda.
- [ ] **F12-P05** — Validar meses de continuidad, cambios de nave/destino y relaciones que evolucionan por causas auténticas.

## Material ya creado que no se mueve

- `gameplay/social/`
- `gameplay/relationships/`
- `gameplay/characters/`
- `gameplay/personality/`
- `ai/memory/`
- `ai/personality/`
- `docs/roadmap/academy_life_final_closure_v1.0.md`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F03–F05, F07 y F10; relación adulta y límites existentes deben respetarse.

## Puerta de cierre

Prueba de continuidad social fuera de escena, privacidad y separación simulación/renderizado. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).


## Avance autónomo de referencia — 14-10-2026

Preparación **P01–P05** con cribado de agenda y actividad, eventos sociales causales, proyección de conocimiento privado por NPC, selección visual LOD A/B/C y reproducción determinista de meses y traslados **solo offline**. Ver [acta de evidencias y bloqueos](ACTA_P01_P05_REFERENCIA_2026-10-14.md).

- Ejecutor sin autoridad Core: `tools/validation/f12_shipboard_reference.py`.
- **45 escenarios** de prueba: `validation/fixtures/f12/f12_shipboard_scenarios_v0.1.json`.
- Pruebas unitarias: `tools/validation/test_f12_shipboard_reference.py`.
- CI: `.github/workflows/f12-shipboard-reference.yml`.

**Esta preparación no altera los contratos canónicos ni concede consentimiento, disponibilidad, amistad, ascensos, conocimientos o traslados en el juego.** La fase global continúa `PLANIFICADA` y los cinco pasos originales permanecen sin cerrar mientras falten integración Core/Host, continuidad social con save/load, NPC persistentes UE5 y aceptación en MSI.
