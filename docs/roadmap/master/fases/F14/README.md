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
