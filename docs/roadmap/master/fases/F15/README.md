# F15 — QA integral, rendimiento, distribución y beta

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** ACEPTACION_SUPERADA / BUILD_DISTRIBUIBLE.

## Objetivo

Cerrar producto jugable con pruebas, recuperación de estado y publicación reproducible.

## Pasos y entregables

- [ ] **F15-P01** — Unificar QA de dominio, CI de referencia, integración Core y pruebas automatizadas UE5.
- [ ] **F15-P02** — Ejecutar recorrido Academia→destino→misión→ascensos/decisiones→guardado/carga.
- [ ] **F15-P03** — Perfilar VRAM/RAM/CPU/FPS, fallos de proveedor remoto y sesiones largas en MSI.
- [ ] **F15-P04** — Validar castellano, controles, accesibilidad, UX, registros, migraciones y errores recuperables.
- [ ] **F15-P05** — Definir versiones, distribución, actualizaciones, criterios beta y publicación verificable.

## Material ya creado que no se mueve

- `validation/`
- `tools/validation/`
- `tools/generation/`
- `localization/`
- `ui/`
- `docs/roadmap/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

Todas las fases; QA y optimización son también condiciones transversales desde F00.

## Puerta de cierre

Aceptación E2E, CI y build distribuible realmente ejecutados; no basta con validaciones documentales. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
