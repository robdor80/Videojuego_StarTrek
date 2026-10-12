# F02 — Arquitectura y contratos de integración

**Estado global del programa (actualización 13-10-2026):** la [PR #2 de F01](https://github.com/robdor80/Videojuego_StarTrek/pull/2) ya fue **fusionada**; F01 permanece `EN_CURSO` en su registro hasta cierre formal documental. **F02: trabajo preparatorio iniciado el 11-10-2026**, en PR #3 separada, todavía **NO CERRADA a nivel `CONTRATO_VALIDADO` ni fusionada** al redactar esta nota. Merge documental ≠ integración Core/UE5.
**Madurez objetivo:** `CONTRATO_VALIDADO` respaldado por Core real, no meramente por documentos.

## Objetivo

Establecer fronteras firmes entre [CoreRPG](https://github.com/robdor80/CoreRPG), Star Trek, UE5, web Academia, NAP y servicios de IA. La autoridad real del mundo corresponde al Core y nunca a UE5, IA o un simulador independiente de Star Trek.

## Pasos y evidencias de esta rama

| Paso | Estado preparatorio 11-10-2026 | Entregable |
|---|---|---|
| **F02-P01** | **CERRADA como AUDITORÍA REMOTA**, sin compilación propia | [Auditoría CoreRPG](AUDITORIA_CORE_RPG_2026-10-11.md): main `dcfcb83`, rama 4.5 `2a3da89`, CI examinada |
| **F02-P02** | **CERRADA COMO INVENTARIO AUDITADO**: 24 fuentes JSON (23 contratos/modelos y 1 fixture), 73 selectores verificados, 5 cabeceras Core/main y decisión de tiempo; **NO** APIs ni integración Core validadas | [Matriz P02](MATRIZ_INTERCAMBIO_Y_PROPIEDAD.md) · [Registro JSON](INVENTARIO_INTERCAMBIO_P02.json) |
| **F02-P03** | **DISEÑO DOCUMENTAL COMPLETO / EN_REVISION-BLOQUEADA_CORE**: 11 adaptadores + 1 frontera externa, 11 gaps cubiertos; **sin API Core futura ni UE5 validados** | [Arquitectura P03](ADAPTADORES_Y_FRONTERAS.md) · [Mapa JSON](MAPA_ADAPTADORES_P03.json) · [Secuencias](SECUENCIAS_Y_CASOS_P03.md) · [Handoff Core/Host](SOLICITUD_COORDINACION_CORE_P03.md) |
| **F02-P04** | **DISEÑO DOCUMENTAL COMPLETO / EN_REVISION-BLOQUEADA_CORE**: 13 fallos, 6 ejes, 10 decisiones, 16 pruebas; **CI F02 success**, comprobación de fuentes real y 9/9 tests aislados OK; **sin tests UE5/Core E2E** | [Política P04](FALLOS_VERSIONES_Y_PRUEBAS.md) · [Registro JSON](REGISTRO_FALLOS_COMPATIBILIDAD_P04.json) · [Validador](../../../../../tools/validation/validate_f02_contracts.py) |
| **F02-P05** | **PLAN DOCUMENTAL COMPLETADO / EN_REVISION-BLOQUEADA_CORE**: 11 paquetes de trabajo F03–F08, 13/13 invariantes trazados y plan de entrada F03-P01; **sin validación formal Core/Host ni integración** | [Plan de integración](PLAN_INTEGRACION_PRIMER_CORTE.md) · [Hoja JSON](HOJA_RUTA_EJECUCION_P05.json) · [Validador](../../../../../tools/validation/validate_f02_p05_plan.py) |

Los estados combinados `EN_REVISION/BLOQUEADA_CORE` indican avance documental con **puerta de validación bloqueada por dependencia externa**, no crean un estado nuevo en el JSON de gobierno.

El cierre de **P02** se limita a **inventario y trazabilidad comprobados**: la existencia de campos en contratos Trek no significa que Core exponga interfaces para ellos. Los **11 gaps P03-G01…G11** tienen ya adaptadores y responsables propuestos en el mapa de P03, pero **no** están resueltos como API/runtime. P03 ha terminado su **especificación documental** y sigue **EN_REVISION/BLOQUEADA_CORE** para el nivel `CONTRATO_VALIDADO` hasta disponer de versiones/API reales y acuerdo Core/Host. La fase global activa registrada sigue siendo F01 mientras se tramita el cierre documental; **DEC-0001 ya está resuelta (Galaxy como inspiración para la nueva Clase Valhalla)**.

## Fuentes originales reutilizadas sin moverlas

- `docs/architecture/` y `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`
- `gameplay/ship_operations/` y `gameplay/orders/`
- `ai/runtime_orchestration.md`
- `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`
- `docs/roadmap/master/DEPENDENCIAS_CORE_RPG.md` y matriz de reutilización

## Restricciones

- La **v0.0.1** es una prueba interna exclusivamente de guardia de Sensores. **DEC-0001 resuelta:** Galaxy/Enterprise-D inspira la **nueva Clase Valhalla** (no un refit ni una Sovereign), sin fecha de servicio fijada. Esta decisión **no** determina el puente piloto del prototipo.
- **Corte auditado el 11–12-10-2026:** CoreRPG/main sólo mostraba WorldState mínimo, Catálogo de Content Packs e infraestructura determinista; 4.5 estaba en otra rama. Antes de integración, **reconsultar el estado vigente** de Core; no asumir versiones o API 4.6–4.12 sin comprobarlas.
- No se modifica código UE5 ni Core por adivinación; no se crea un motor paralelo. Un manual, JSON, CI Core o un motor Python de referencia **no** constituyen v0.0.1 jugable.
- Se conserva el estado global existente sin sobrescribirlo desde esta rama: **F01 ya está en `main` tras la fusión de PR #2**, y F02 debe sincronizarse mediante el procedimiento de cierre y madurez real, sin conflictos de gobierno.

## Puerta de cierre de F02

1. CoreRPG `main` contiene las versiones concretas requeridas para el contrato mínimo y se comprueba con los responsables.
2. Adaptadores contrastados con APIs reales; alcance/versionado/migración explícitos.
3. Evidencia de pruebas adecuada al nivel declarado: no declarar `CORE_INTEGRADO` ni `UE5_JUGABLE` sin pruebas reales.
4. Resolver y registrar decisiones de responsable Core/Host, y dependencia F01 pertinente.
5. PR documentada, revisión/merge y sincronización del estado global cuando proceda.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).

La política P04 diferencia fallos seguros de presentación/IA de los fallos de autoridad del Core. El validador P04 inspecciona trazabilidad y deriva de los contratos, **no ejecuta el videojuego**. Los 9 unit tests sintéticos superados en Python 3.13.5/Linux se repitieron en CI y el checkout completo **sí se validó en GitHub Actions**: [run 38149311936, success](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38149311936). Sigue sin acreditar 4.7/4.9/4.10 ni UE5.

## Traspaso a F03 tras P05

Los cinco pasos **P01–P05** tienen ya entregables documentales inspeccionables en esta rama. **F02 NO se declara cerrada al nivel `CONTRATO_VALIDADO`** porque aún no se han verificado y aceptado las capacidades e interfaces Core/Host UE5 necesarias. El corte Core 4.5 fuera de `main` corresponde a la auditoría del 11–12-10-2026. Se permite iniciar en paralelo **F03-P01 de auditoría y diseño** sobre cronología, seeds y materialización, en **rama/PR independiente**, sin fingir ejecución Core. La elección de Valhalla (DEC-0001) ya está en `main` por PR #2; cualquier actualización de estado global F02 deberá hacerse según madurez y QA propios, **sin declarar integración Core/UE5 ficticia**. Fuente de entrada: [P05](PLAN_INTEGRACION_PRIMER_CORTE.md), hoja INT-00…INT-10 y [F03](../F03/README.md).

## Coordinación y auditoría — 2026-10-12

[Ver matriz de interfaces y bloqueos reales para las PR #2–#7](MATRIZ_SINCRONIZACION_AUDITORIA_2026-10-12.md). Documenta el endurecimiento de referencia F04/F05/F06, el estado efectivo de Core `main` (4.4), sus 4.5/4.6–4.12 pendientes, y las condiciones de la prueba transversal después de fusionar. **No afirma integración Core/UE5 ni modifica el estado global.**

## Decisión D5 — Paralelismo Core RPG / Star Trek 3D (12-10-2026)

[Dirección técnica aprobada y punto de parada obligatorio de Core](DECISION_D5_DESARROLLO_PARALELO_CORE_3D_2026-10-12.md): Core puede avanzar por sus etapas 4.5→4.10 **solo hasta completar la capacidad mínima demostrable de la guardia de Sensores**; Blender/UE5 continúan con assets y pruebas visuales sin duplicar la simulación. Spike Core↔UE5 y comprobación NDK tempranos. F07/F08 siguen formalmente pausadas; PR y Core `main` sin fusión automática.
