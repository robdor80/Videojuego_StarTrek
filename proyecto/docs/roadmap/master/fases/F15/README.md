# F15 — QA integral, rendimiento, distribución y beta

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo oficial:** `ACEPTACION_SUPERADA`. `BUILD_DISTRIBUIBLE` es una condición/artefacto de aceptación de P05, no un nivel de madurez adicional del roadmap.

## Objetivo

Cerrar producto jugable con pruebas, recuperación de estado y publicación reproducible.

## Pasos y entregables

- [ ] **F15-P01** — Unificar QA de dominio, CI de referencia, integración Core y pruebas automatizadas UE5.
- [ ] **F15-P02** — Ejecutar recorrido Academia→destino→misión→ascensos/decisiones→guardado/carga.
- [ ] **F15-P03** — Perfilar VRAM/RAM/CPU/FPS, fallos de proveedor remoto y sesiones largas en MSI.
- [ ] **F15-P04** — Validar castellano, controles, accesibilidad, UX, registros, migraciones y errores recuperables.
- [ ] **F15-P05** — Definir versiones, distribución, actualizaciones, criterios beta y publicación verificable.

## Material ya creado que no se mueve

- `desarrollo/validation/`
- `desarrollo/tools/validation/`
- `desarrollo/tools/generation/`
- `audiovisual/localization/`
- `audiovisual/ui/`
- `proyecto/docs/roadmap/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

Todas las fases; QA y optimización son también condiciones transversales desde F00.

## Puerta de cierre

Aceptación E2E, CI y build distribuible realmente ejecutados; no basta con validaciones documentales. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).

## Avance autónomo de referencia — 15-10-2026

Preparación **P01–P05** con un gate final fail-closed para QA transversal, recorrido E2E, rendimiento MSI, UX/castellano y candidato beta/distribuible. Véase [acta de preparación F15](ACTA_P01_P05_REFERENCIA_2026-10-15.md).

- Validador: `desarrollo/tools/validation/f15_release_readiness.py`.
- **37 escenarios**: `desarrollo/validation/fixtures/f15/f15_release_readiness_scenarios_v0.1.json`.
- Plantilla deliberadamente bloqueada: `desarrollo/validation/fixtures/f15/f15_beta_capture_template_v0.1.json`.
- Pruebas: `desarrollo/tools/validation/test_f15_release_readiness.py`.
- CI: `.github/workflows/f15-release-readiness-reference.yml`.

El gate nunca emite `ACEPTACION_SUPERADA` ni `BUILD_DISTRIBUIBLE`: como máximo deja una captura completa en `REVIEW_REQUIRED`. La plantilla actual es `NO_EJECUTADO` y debe fallar hasta que existan Core/UE5/MSI, E2E, rendimiento, migración/rollback y aceptación real. F15 continúa globalmente `PLANIFICADA`; P01–P05 permanecen sin marcar.
