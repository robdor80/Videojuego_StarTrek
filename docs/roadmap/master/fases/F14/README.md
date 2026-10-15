# F14 — Producción audiovisual, naves y NAP

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

Convertir reglas visuales en recursos trazables utilizables por UE5 y perfiles por época.

## Pasos y entregables

- [ ] **F14-P01** — Reconciliar biblias visuales, identidades de assets, licencias y contratos con NAP 2.0.
- [ ] **F14-P02** — Producir interiores/exteriores y NPC por prioridades del juego y su escalera de naves.
- [ ] **F14-P03** — Crear voces, ambiente, música, efectos, cámaras, UI/LCARS y variantes por era.
- [ ] **F14-P04** — Aplicar optimización de texturas, geometrías, LOD, streaming e inventario de originales/derivados.
- [ ] **F14-P05** — Validar trazabilidad, recuperación y funcionamiento de recursos en builds y repositorios externos.

## Material ya creado que no se mueve

- `art_direction/`
- `assets/`
- `audio/`
- `presentation/`
- `ui/`
- `nap/`
- `manifests/`
- `validation/fixtures/nap/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F01, F07, F08 y F11; NAP externo y pipeline de conversión.

## Puerta de cierre

Recursos verificables con derechos de uso y manifest/reproducción, no solo fichas o imágenes de referencia. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).

## Avance autónomo de referencia — 14-10-2026

Preparación **P01–P05** con reconciliación de los contratos NAP 2.0 observados, prioridades de assets/presentación, puertas de derechos, separación original/derivado, exigencia de métricas para LOD/streaming y trazabilidad de build/recuperación. Véase [acta de preparación F14](ACTA_P01_P05_REFERENCIA_2026-10-14.md).

- Snapshot NAP 2.0: `nap/profile/F14_NAP2_COMPATIBILITY_SNAPSHOT_v0.1.json`.
- Prioridad de assets: `manifests/assets/f14_asset_priority_manifest_v0.1.json`.
- Presentación: `manifests/presentation/f14_presentation_priority_manifest_v0.1.json`.
- Ejecutor offline sin autoridad NAP/UE5: `tools/validation/f14_audiovisual_reference.py`.
- **43 escenarios**: `validation/fixtures/f14/f14_audiovisual_scenarios_v0.1.json`.
- Pruebas: `tools/validation/test_f14_audiovisual_reference.py`; CI `.github/workflows/f14-audiovisual-reference.yml`.

Este avance **no instala un perfil Star Trek en NAP, no produce mallas/audio de juego, no verifica derechos del Sutherland y no ejecuta UE5**. La Fase 14 continúa globalmente `PLANIFICADA`; P01–P05 permanecen sin marcar hasta disponer de los assets, derechos, ejecución NAP que proceda y validación UE5/MSI exigidas por la puerta de cierre.
