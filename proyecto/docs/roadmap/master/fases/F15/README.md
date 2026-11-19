# F15 — QA integral, rendimiento e instalación privada

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** `ACEPTACION_SUPERADA`. El marcador histórico `BUILD_DISTRIBUIBLE` se interpreta exclusivamente como **build privada instalable localmente**. El corte R7 migra el validador y los fixtures vigentes sin perder el gate fail-closed.

## Objetivo

Cerrar el videojuego privado con pruebas, recuperación de estado e instalación local reproducible en el MSI.

## Pasos y entregables

- [ ] **F15-P01** — Unificar QA de dominio, CI de referencia, integración Core y pruebas automatizadas UE5.
- [ ] **F15-P02** — Ejecutar recorrido Academia→destino→misión→ascensos/decisiones→guardado/carga.
- [ ] **F15-P03** — Perfilar VRAM/RAM/CPU/FPS, fallos de proveedor remoto y sesiones largas en MSI.
- [ ] **F15-P04** — Validar castellano, controles, accesibilidad, UX, registros, migraciones y errores recuperables.
- [ ] **F15-P05** — Verificar build privada, instalación local, actualizaciones reversibles, mantenimiento, copias, migraciones, rollback y recuperación.

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

Aceptación E2E, CI y build PRIVADA realmente compilada, instalada, actualizada y recuperada en MSI; no bastan validaciones documentales. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).

## Avance autónomo de referencia — 15-10-2026 (semántica histórica de beta)

Preparación **P01–P05**, histórica a 15-10, con un gate fail-closed. Los nombres antiguos `release_*`, `f15_beta_*` y `BUILD_DISTRIBUIBLE` siguen existiendo por compatibilidad de rutas, pero **no autorizan publicación**. Véase [acta de preparación F15](ACTA_P01_P05_REFERENCIA_2026-10-15.md).

- Validador: `desarrollo/tools/validation/f15_release_readiness.py`.
- **38 escenarios**: `desarrollo/validation/fixtures/f15/f15_release_readiness_scenarios_v0.1.json`.
- Plantilla deliberadamente bloqueada: `desarrollo/validation/fixtures/f15/f15_beta_capture_template_v0.1.json`.
- Pruebas: `desarrollo/tools/validation/test_f15_release_readiness.py`.
- CI: `.github/workflows/f15-release-readiness-reference.yml`.

El gate vigente exige los canales `private_local` / `private_candidate`, copia **y restauración** probada, migración y rollback, y rechaza canales públicos (`beta`, `release_candidate`, `steam`). Nunca emite `ACEPTACION_SUPERADA`: como máximo deja una captura completa en `REVIEW_REQUIRED`. La plantilla actual es `NO_EJECUTADO` y debe fallar hasta que existan Core/UE5/MSI, E2E, rendimiento, migración/rollback y aceptación real. F15 continúa globalmente `PLANIFICADA`; P01–P05 permanecen sin marcar.

## Criterio vigente R0/R7 — 19-11-2026

**Uso exclusivamente privado.** No exigir publicación, servidores de terceros, marketing, tienda, licencias comerciales ni circulación de instaladores. Mantener QA, seguridad de guardados, pérdida de red/IA, rendimiento, actualización/rollback y recuperación local. La plantilla `NO_EJECUTADO` sigue bloqueada hasta ejecutar una partida real. R7 corrige el código y amplía las regresiones de los canales privados. **No se han ejecutado** ni empaquetado ni recuperación real del MSI. La antigua acta del 15-10 permanece intacta como prueba histórica, no política vigente.
