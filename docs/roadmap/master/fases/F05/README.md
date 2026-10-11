# F05 — Órdenes, iniciativa y delegación NPC

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO o INTEGRACION_PROBADA según cada paso.

## Objetivo

El capitán y otros oficiales actúan por sí mismos dentro de sus capacidades y límites.

## Pasos y entregables

- [ ] **F05-P01** — Separar formalmente orden, solicitud, tarea/compromiso, acción, resultado y evento.
- [ ] **F05-P02** — Cerrar ciclos de aceptación, aclaración, rechazo, desobediencia, caducidad y revocación de delegaciones.
- [ ] **F05-P03** — Diseñar iniciativa del capitán NPC, oficiales y tareas NPC↔NPC aun cuando el jugador esté ausente.
- [ ] **F05-P04** — Conectar propuestas y diálogo por IA remota sin mutación directa y con degradación ante latencia/caída.
- [ ] **F05-P05** — Preparar pruebas NPC→NPC, NPC→jugador, jugador capitán→NPC y coordinación con Core RPG 4.10+.

## Material del repositorio que se aprovecha sin moverlo

- `gameplay/orders/`
- `gameplay/chain_of_command/`
- `ai/captain_behavior/`
- `ai/npc_behavior/`
- `gameplay/ship_operations/operational_event_log/`
- `gameplay/ship_operations/ship_computer/`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F04 y F02; 4.10+ solo evaluación e integración incremental de mecanismos comunes.

## Puerta de cierre

Cadena de órdenes y consecuencias trazables, autonomía sin omnisciencia, IA incapaz de escribir estado autoritativo. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
