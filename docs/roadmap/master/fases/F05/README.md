# F05 — Órdenes, delegación e iniciativa NPC

**Estado global:** PLANIFICADA; **trabajo en rama:** P01–P05 desarrollados a nivel referencia, CI de referencia confirmada; integración pendiente.
**Meta de fase del plan maestro:** CORE_INTEGRADO (**no alcanzada**).

## Puntos
- [x] **P01 diseño** — [Modelo de seis objetos y ownership](MODELO_ORDENES_P01.md), [contrato de referencia](CONTRATOS_P01_P02.json).
- [x] **P02 diseño** — [Estados, negativas, caducidad y delegaciones](CICLOS_REVOCACION_P02.md).
- [x] **P03 diseño** — [Iniciativa NPC, fuera de escena y cadena de mando](INICIATIVA_NPC_P03.md).
- [x] **P04 diseño** — [Propuesta LLM, revalidación y fallback](IA_PROPUESTAS_Y_FALLBACK_P04.md).
- [x] **P05 suite incorporada** — [48 fixtures + 16 tests y plan de integración](PRUEBAS_Y_COORDINACION_P05.md). **GitHub Actions verificada: 16/16 pruebas y 48/48 escenarios (run 38178262402).**

Estos checks se refieren únicamente a los entregables independientes, **no** al cierre de P01–P05 a nivel `CORE_INTEGRADO`.

## Reutilización sin mover rutas
`gameplay/orders/`, `gameplay/chain_of_command/`, `ai/captain_behavior/`, `ai/npc_behavior/`, `gameplay/ship_operations/operational_event_log/`, `gameplay/ship_operations/ship_computer/`, además de F02/F03/F04 (PR #3/#4/#5). Las fuentes aprobadas no se cambian por la propuesta.

## Bloqueos y aceptación
CoreRPG `main@dcfcb83` sigue previo a las capacidades de 4.7, 4.9, 4.10 y 4.12. F01 PR #2 y F02–F04 están abiertas; DEC-0001 y DEC-0002 no se resuelven aquí. **No** se fusiona ni se modifica `ESTADO_GLOBAL.json` hasta los controles previos. La iniciativa debe respetar cargo/guardia, conocimiento, recursos y responsabilidad; la IA no muta World State.

[Plan maestro](../../PLAN_MAESTRO.md) · [Criterios de cierre](../../CRITERIOS_DE_CIERRE.md) · [Estado global](../../ESTADO_GLOBAL.json).


## Endurecimiento de auditoría — 2026-10-12

A-01/A-02: `assess` ya no acepta `{}` como autorización y exige explícitamente
fase, canal, decisión externa, identidad del actor, acción, puesto, revisión,
datos de conocimiento/aptitud y, en ejecución, evidencia de guardia, recursos,
capacidad y conflicto temporal. Un `ALLOW_REFERENCE` requiere un
`authorization_binding` de referencia F04 ligado a actor, acción, puesto,
revisión y plazo; una revocación/cambio invalida la solicitud.

Este binding **solo valida coherencia del fixture**; cualquier Host/IA podría
fabricar el diccionario: por tanto no habilita efectos, y en producción deberá
sustituirse por autorización validada y versionada dentro de Core. Las 48
situaciones de referencia se migraron explícitamente para que sus resultados
sigan siendo auditables, sin utilizar valores permisivos por omisión.

**CI validada:** [Actions 38227559253](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38227559253)
SUCCESS: **19 unit tests / 48 fixtures**. `effects_applied=0` y
`authoritative=false`; fase global y contrato Core siguen pendientes.
