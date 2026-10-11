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
