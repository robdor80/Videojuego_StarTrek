# F08 — Vertical slice jugable v0.0.1

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** UE5_JUGABLE / ACEPTACION_SUPERADA.

## Objetivo

Una guardia completa de Sensores en un puente 3D con órdenes, resultados y continuidad.

## Pasos y entregables

- [ ] **F08-P01** — Preparar nave, guardia, capitán NPC, oficial jugador y contacto preexistente.
- [ ] **F08-P02** — Recibir una orden legítima del capitán NPC sin que el mundo dependa del jugador.
- [ ] **F08-P03** — Ejecutar barrido desde consola 3D; informar resultados y recibir consecuencias.
- [ ] **F08-P04** — Guardar/cargar orden, acciones, conocimiento y eventos; seguir operativo sin IA remota.
- [ ] **F08-P05** — Superar aceptación extremo a extremo y publicar evidencias del build y rendimiento.

## Material del repositorio que se aprovecha sin moverlo

- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`
- `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`
- `gameplay/ship_operations/operational_event_log/`
- `presentation/`
- `ui/bridge/`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F02–F07 y runtime Core RPG necesario; no cerrar por documentación únicamente.

## Puerta de cierre

Build UE5 verificable con guardia reproducible, interacción de consola, historial y guardado real. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
