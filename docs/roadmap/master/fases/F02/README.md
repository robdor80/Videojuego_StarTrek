# F02 — Arquitectura y contratos de integración

**Estado global del programa:** F01 sigue siendo la fase principal activa, con [PR #2](https://github.com/robdor80/Videojuego_StarTrek/pull/2) sin fusionar. **F02: trabajo preparatorio iniciado expresamente por el autor el 11-10-2026**, sobre rama separada. **NO CERRADA ni fusionada en main**. Se evita fijar dos fases globales principales simultáneas.
**Madurez objetivo:** `CONTRATO_VALIDADO` respaldado por Core real, no meramente por documentos.

## Objetivo

Establecer fronteras firmes entre [CoreRPG](https://github.com/robdor80/CoreRPG), Star Trek, UE5, web Academia, NAP y servicios de IA. La autoridad real del mundo corresponde al Core y nunca a UE5, IA o un simulador independiente de Star Trek.

## Pasos y evidencias de esta rama

| Paso | Estado preparatorio 11-10-2026 | Entregable |
|---|---|---|
| **F02-P01** | **CERRADA como AUDITORÍA REMOTA**, sin compilación propia | [Auditoría CoreRPG](AUDITORIA_CORE_RPG_2026-10-11.md): main `dcfcb83`, rama 4.5 `2a3da89`, CI examinada |
| **F02-P02** | **EN_REVISION**: inventario completado, interfaces no confirmadas | [Matriz de intercambio y propiedad](MATRIZ_INTERCAMBIO_Y_PROPIEDAD.md) |
| **F02-P03** | **EN_REVISION/BLOQUEADA_CORE**: adaptadores propuestos; APIs 4.5+ no fijadas | [Adaptadores y fronteras](ADAPTADORES_Y_FRONTERAS.md) |
| **F02-P04** | **EN_REVISION**: política definida; pruebas funcionales pendientes | [Fallos, versiones y pruebas](FALLOS_VERSIONES_Y_PRUEBAS.md) |
| **F02-P05** | **EN_REVISION/BLOQUEADA_CORE**: plan del primer corte, validación externa pendiente | [Plan de integración](PLAN_INTEGRACION_PRIMER_CORTE.md) |

Los estados combinados `EN_REVISION/BLOQUEADA_CORE` indican avance documental con **puerta de validación bloqueada por dependencia externa**, no crean un estado nuevo en el JSON de gobierno.

## Fuentes originales reutilizadas sin moverlas

- `docs/architecture/` y `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`
- `gameplay/ship_operations/` y `gameplay/orders/`
- `ai/runtime_orchestration.md`
- `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`
- `docs/roadmap/master/DEPENDENCIAS_CORE_RPG.md` y matriz de reutilización

## Restricciones

- La **v0.0.1** es una prueba interna exclusivamente de guardia de Sensores. La selección definitiva de Dama/Imperator sigue pendiente de DEC-0001, sin inventar Galaxy/Sovereign/Odyssey como clase elegida.
- CoreRPG/main sólo tiene un WorldState mínimo, Catálogo de Content Packs e infraestructura determinista. 4.5 está en otra rama; no asumir 4.6, 4.7, 4.9, 4.10 o 4.12 integradas.
- No se modifica código UE5 ni Core por adivinación; no se crea un motor paralelo. Un manual, JSON, CI Core o un motor Python de referencia **no** constituyen v0.0.1 jugable.
- Se conserva **F01 como fase global activa** en `ESTADO_GLOBAL.json`, sin tocar el estado de F01 desde esta rama: integrar F01 y reevaluar bloqueos antes de sincronizar el estado global de F02, evitando conflictos de merge.

## Puerta de cierre de F02

1. CoreRPG `main` contiene las versiones concretas requeridas para el contrato mínimo y se comprueba con los responsables.
2. Adaptadores contrastados con APIs reales; alcance/versionado/migración explícitos.
3. Evidencia de pruebas adecuada al nivel declarado: no declarar `CORE_INTEGRADO` ni `UE5_JUGABLE` sin pruebas reales.
4. Resolver y registrar decisiones de responsable Core/Host, y dependencia F01 pertinente.
5. PR documentada, revisión/merge y sincronización del estado global cuando proceda.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
