# F03 — Mundo autoritativo, conocimiento y persistencia

**Auditoría y desarrollo documental:** 2026-10-11. **Estado de trabajo:** CINCO PASOS DOCUMENTADOS / VALIDACIÓN DE REFERENCIA EN CI / **INTEGRACIÓN CORE BLOQUEADA**. **Estado global en `main`: PLANIFICADA**, pendiente de gobierno F01/F02; **F03 no se declara CERRADA**. **Madurez objetivo:** `CORE_INTEGRADO`.

## Objetivo

Reconciliar una realidad de campaña existente antes de observarla, información adquirida con límites de acceso, acontecimientos causales incluso fuera de escena y guardados compatibles sin duplicación de identidades. No crear un segundo Core RPG en este repositorio.

## Cinco pasos, entregables e interpretación exacta

| Paso | Trabajo realizado en rama F03 | Evidencia / límite |
|---|---|---|
| **F03-P01** | [Cronología, semillas, identidad, materialización y ciclo LOD](CONTRATO_IDENTIDAD_MATERIALIZACION_P01.md) | Diseño y fuentes auditadas. Generación real **NO_EJECUTADA** |
| **F03-P02** | [Verdad, percepción/observación, conocimiento y privacidad](VERDAD_PERCEPCION_CONOCIMIENTO_P02.md) | Política de campos, canales y rechazo. Core Knowledge **NO_EJECUTADO** |
| **F03-P03** | [Tiempo, eventos, agendas y causalidad fuera de escena](CAUSALIDAD_TIEMPO_OFFSCREEN_P03.md) | Invariantes y escenarios. Core Simulation/Actions **NO_EJECUTADOS** |
| **F03-P04** | [Guardado, carga, migraciones y operaciones pendientes](GUARDADO_CARGA_MIGRACION_P04.md) | Protocolo de seguridad. Core Persistence **NO_EJECUTADO** |
| **F03-P05** | [Validador, fixture, batería de pruebas y bloqueo técnico](VALIDACION_Y_BLOQUEOS_P05.md) | [Código de QA](../../../../../tools/validation/validate_f03_reference.py), [tests](../../../../../tools/validation/test_f03_reference.py), [fixture](../../../../../validation/fixtures/f03/continuity_reference_v0.1.json), [workflow](../../../../../.github/workflows/f03-reference-contracts.yml) |

### Fuentes reutilizadas sin mover

`universe/chronology/`, `universe/generation/`, `gameplay/persistence/`, `gameplay/ship_operations/sensor_resolution/`, `gameplay/ship_operations/operational_event_log/`, `gameplay/ship_operations/ship_memory/`, `ai/memory/`, `validation/fixtures/` y `docs/decisions/universal_stardate_system.md`.

**F02** se ha desarrollado en [PR #3](https://github.com/robdor80/Videojuego_StarTrek/pull/3) (P01–P05 documentales), **F01** sigue en [PR #2](https://github.com/robdor80/Videojuego_StarTrek/pull/2) por DEC-0001. Ambas están pendientes de fusión. La F03 usa el traspaso **INT-02…INT-06** sin asumir que `main` contenga los nuevos archivos F02; su rama deriva independientemente de `main`.

### Restricciones y puerta de cierre

- **CoreRPG main** comprobado en `dcfcb83c9853e005b5450bd39e0ba693cb91e257`; 4.5 permanece en rama `feat/generic-world-state@2a3da891`; las 4.7, 4.9, 4.10 no están disponibles como interfaces validadas de producción.
- Ni JSON, ni CI estática, ni test Python, ni ejemplo del log acreditan persistencia/simulación verdadera o una versión UE5 jugable.
- `ESTADO_GLOBAL.json` no se toca desde F03 antes de integrar F01 y F02: se evita anunciar una fase principal concurrente sin resolución de decisiones.
- Para cerrar al nivel `CORE_INTEGRADO` se exigen SHA/versión real, contratos validados con responsables, pruebas positivas/negativas de Core contra el fixture, guardado/carga y ciclos fuera de escena, evidencias de ejecución y revisión/merge.
- Elegir Galaxy, Sovereign u Odyssey como base Imperator **sigue reservado al autor** y no condiciona esta auditoría.

La rama documenta **todos los P01–P05**; la fase permanece **EN_REVISION / BLOQUEADA_CORE** en su madurez objetivo. Continuar hacia F04 solo para diseño independiente mientras se resuelven dependencias.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md), [estado global](../../ESTADO_GLOBAL.json) y [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).
