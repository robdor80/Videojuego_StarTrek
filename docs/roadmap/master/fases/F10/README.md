# F10 — Academia jugable e integración de academiaflota

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

Transformar los currículos y la vida académica existentes en experiencia jugable con continuidad.

## Pasos y entregables

- [ ] **F10-P01** — Verificar 4 años, 3 trimestres, 60 asignaturas principales, 7 especializaciones, guías, web y estados de estudio.
- [ ] **F10-P02** — Delimitar competencias de la web academiaflota frente a la partida real en Core RPG/UE5.
- [ ] **F10-P03** — Integrar cadetes persistentes, turnos, profesores, vida social, clases y evaluaciones según contratos ya cerrados.
- [ ] **F10-P04** — Crear prácticas con consolas reales, simulaciones, Kobayashi Maru y ceremonia/graduación.
- [ ] **F10-P05** — Validar trayectoria y guardado: aspirante→cadete→graduado→alférez, conservando historia y vínculos.

## Material ya creado que no se mueve

- `gameplay/careers/academy_path/`
- `docs/roadmap/academy_life_final_closure_v1.0.md`
- `docs/roadmap/game_design_readiness_v0_2.md`
- `tools/generation/run_academy_life_suite.py`
- `validation/fixtures/academy_life/`
- `ui/academy/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F02–F05, F08 y F09 según práctica; repo externo academiaflota.

## Puerta de cierre

Prueba académica reproducible y transición real al servicio; 20/20 life design no sustituye integración UE5. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
