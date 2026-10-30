# F03 — Mundo autoritativo, conocimiento y persistencia

> **CIERRE FORMAL — 30-10-2026:** F03-P01–P05 **CERRADAS al nivel `CORE_INTEGRADO`** en su corte vertical verificable. [CoreRPG PR #12](https://github.com/robdor80/CoreRPG/pull/12) y [Star Trek PR #62](https://github.com/robdor80/Videojuego_StarTrek/pull/62) fusionadas mediante commits de merge `c147d81ed069da2e09149613ab02cbc3ebe95a4a` y `fe6460c4e037fffa1e4f5ded9b2617af1fe846e2`. El Core fijado `9c53a33787de13d91eb2abe4da07033ee0fa1dc1` permanece accesible en el historial de `main`. Ver [informe de ejecución](INFORME_EJECUCION_2026-10-30.md), [auditoría](AUDITORIA_TECNICA_2026-10-30.md) y [evidencias](evidencias_20261030/results.json).
>
> **Límites:** únicamente fixture sintético de identidad, conocimiento autorizado, agenda/reloj y persistencia; Unreal validado en `-NullRHI`. **No** significa `UE5_JUGABLE`, sensores completos, simulación galáctica, migraciones generales ni validez del año 2372 para la cronología narrativa. Siguiente fase principal: F04, pendiente de su propia reauditoría de integración.

## Antecedentes históricos (11–30 de octubre, superados por el cierre)

Los párrafos y etiquetas de estado que siguen registran el trabajo anterior a las fusiones; las menciones a PR «Draft», F03 «EN_CURSO/EN_REVISION/BLOQUEADA» o integración «pendiente» se conservan únicamente como antecedentes y **no representan el estado vigente**. Para el estado oficial consultar `../../ESTADO_GLOBAL.json`.

**Auditoría y desarrollo documental:** 2026-10-11; **sincronización de PR anteriores:** 2026-10-13. **Estado de trabajo:** CINCO PASOS DOCUMENTADOS / VALIDACIÓN DE REFERENCIA EN CI / **INTEGRACIÓN CORE PENDIENTE**. El estado global de F03 es ahora **`EN_REVISION`**, por pruebas de referencia superadas, con P01–P04 **BLOQUEADAS** en ejecución Core y P05 cerrada solo como QA de fixture. **F03 no se declara CERRADA**. **Madurez objetivo:** `CORE_INTEGRADO`.

## Objetivo

Reconciliar una realidad de campaña existente antes de observarla, información adquirida con límites de acceso, acontecimientos causales incluso fuera de escena y guardados compatibles sin duplicación de identidades. No crear un segundo Core RPG en este repositorio.

## Cinco pasos, entregables e interpretación exacta

| Paso | Trabajo realizado en rama F03 | Evidencia / límite |
|---|---|---|
| **F03-P01** | [Cronología, semillas, identidad, materialización y ciclo LOD](CONTRATO_IDENTIDAD_MATERIALIZACION_P01.md) | Diseño y fuentes auditadas. Generación real **NO_EJECUTADA** |
| **F03-P02** | [Verdad, percepción/observación, conocimiento y privacidad](VERDAD_PERCEPCION_CONOCIMIENTO_P02.md) | Política de campos, canales y rechazo. Core Knowledge **NO_EJECUTADO** |
| **F03-P03** | [Tiempo, eventos, agendas y causalidad fuera de escena](CAUSALIDAD_TIEMPO_OFFSCREEN_P03.md) | Invariantes y escenarios. Core Simulation/Actions **NO_EJECUTADOS** |
| **F03-P04** | [Guardado, carga, migraciones y operaciones pendientes](GUARDADO_CARGA_MIGRACION_P04.md) | Protocolo de seguridad. Core Persistence **NO_EJECUTADO** |
| **F03-P05** | [Validador, fixture, batería de pruebas y bloqueo técnico](VALIDACION_Y_BLOQUEOS_P05.md) | [Código de QA](../../../../../../desarrollo/tools/validation/validate_f03_reference.py), [tests](../../../../../../desarrollo/tools/validation/test_f03_reference.py), [fixture](../../../../../../desarrollo/validation/fixtures/f03/continuity_reference_v0.1.json), [workflow](../../../../../../.github/workflows/f03-reference-contracts.yml) |

### Fuentes reutilizadas sin mover

`sistemas/universe/chronology/`, `sistemas/universe/generation/`, `sistemas/gameplay/persistence/`, `sistemas/gameplay/ship_operations/sensor_resolution/`, `sistemas/gameplay/ship_operations/operational_event_log/`, `sistemas/gameplay/ship_operations/ship_memory/`, `sistemas/ai/memory/`, `desarrollo/validation/fixtures/` y `proyecto/docs/decisions/universal_stardate_system.md`.

**Actualización 2026-10-13:** [F01 PR #2](https://github.com/robdor80/Videojuego_StarTrek/pull/2) y [F02 PR #3](https://github.com/robdor80/Videojuego_StarTrek/pull/3) **ya están fusionadas en `main`**. DEC-0001 se resolvió: Galaxy/Enterprise-D inspira la nueva **Clase Valhalla**, distinta de Galaxy; su fecha de servicio queda pendiente. La F03 utiliza el traspaso documental **INT-02…INT-06** de F02, sin confundirlo con contratos Core/UE5 validados ni con cierre formal de F01/F02.

### Restricciones y puerta de cierre

- **CoreRPG main** comprobado en `dcfcb83c9853e005b5450bd39e0ba693cb91e257`; 4.5 permanece en rama `feat/generic-world-state@2a3da891`; las 4.7, 4.9, 4.10 no están disponibles como interfaces validadas de producción.
- Ni JSON, ni CI estática, ni test Python, ni ejemplo del log acreditan persistencia/simulación verdadera o una versión UE5 jugable.
- Tras las PR #2–#7 fusionadas, `ESTADO_GLOBAL.json` ha quedado reconciliado: F01 CERRADA en diseño, F02 fase principal, F03 EN_REVISION. **No** confundir QA estática con persistencia/simulación en Core. Véase [acta](../../ACTA_RECONCILIACION_F00_F06_2026-10-13.md).
- Para cerrar al nivel `CORE_INTEGRADO` se exigen SHA/versión real, contratos validados con responsables, pruebas positivas/negativas de Core contra el fixture, guardado/carga y ciclos fuera de escena, evidencias de ejecución y revisión/merge.
- **DEC-0001 está resuelta:** Galaxy/Enterprise-D es la referencia creativa de la **nueva Clase Valhalla**; la decisión no impone el puente de la v0.0.1, ni resuelve su año de servicio.

La rama documenta **todos los P01–P05**; la fase permanece **EN_REVISION / BLOQUEADA_CORE** en su madurez objetivo. Continuar hacia F04 solo para diseño independiente mientras se resuelven dependencias.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md), [estado global](../../ESTADO_GLOBAL.json) y [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).
