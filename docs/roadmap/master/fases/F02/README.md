# F02 — Arquitectura y contratos de integración

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO o INTEGRACION_PROBADA según cada paso.

## Objetivo

Fronteras firmes entre Core RPG, Star Trek, UE5, Academia web, NAP y servicios de IA.

## Pasos y entregables

- [ ] **F02-P01** — Auditar capacidades realmente disponibles de Core RPG frente a su roadmap.
- [ ] **F02-P02** — Inventariar entidades/IDs, tiempo, reglas, acciones, eventos, persistencia, permisos y save/load a intercambiar.
- [ ] **F02-P03** — Especificar adaptadores necesarios sin inventar API o contratos que el Core aún no expone.
- [ ] **F02-P04** — Fijar política de fallos de API remota, pruebas de contratos y migraciones/versiones.
- [ ] **F02-P05** — Crear plan de integración mínimo para el primer corte jugable y validarlo con responsables de cada repositorio.

## Material del repositorio que se aprovecha sin moverlo

- `docs/architecture/`
- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`
- `gameplay/ship_operations/`
- `ai/runtime_orchestration.md`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F01 y disponibilidad progresiva Core RPG 4.5+; 4.10+ para Actions; 4.12 para AI.

## Puerta de cierre

Matriz de responsabilidades y especificación de integración contrastada con versiones reales, sin motor duplicado. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
