# F03 — Mundo autoritativo, conocimiento y persistencia

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO o INTEGRACION_PROBADA según cada paso.

## Objetivo

Construir la continuidad mínima de un universo observable, incluso fuera de escena.

## Pasos y entregables

- [ ] **F03-P01** — Reconciliar cronología, semillas, identidad estable y materialización antes de observación.
- [ ] **F03-P02** — Definir verdad del mundo frente a percepción/conocimiento por personaje, nave y consola.
- [ ] **F03-P03** — Conectar simulación causal, tiempo, eventos, agendas y operaciones fuera de escena.
- [ ] **F03-P04** — Resolver guardado, carga, migraciones y continuidad de datos y órdenes pendientes.
- [ ] **F03-P05** — Validar determinismo, límites de conocimiento, consistencia de identidad y ausencia de duplicación.

## Material del repositorio que se aprovecha sin moverlo

- `universe/generation/`
- `universe/chronology/`
- `gameplay/ship_operations/sensor_resolution/`
- `gameplay/ship_operations/operational_event_log/`
- `gameplay/ship_operations/ship_memory/`
- `validation/fixtures/`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F02; Generic World State/CoreRPG 4.5 y fases posteriores aún deben contrastarse.

## Puerta de cierre

Pruebas de continuidad y conocimiento sobre estado autoritativo efectivamente integrado, no solo contratos. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
