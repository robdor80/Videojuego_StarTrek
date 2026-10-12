# F05 — Órdenes, delegación e iniciativa NPC

**Estado global reconciliado:** **EN_REVISION**, con P01–P04 BLOQUEADAS para sus capacidades Core reales y P05 CERRADA solo como suite de referencia. **PR #6 fusionada en `main`**; 19 unit tests y 48 fixtures verificados, y regresión F04→F05→F06 superada en [CI integrada](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38321712021). No equivale a implementación de iniciativa NPC.
**Meta de fase del plan maestro:** CORE_INTEGRADO (**no alcanzada**).

## Puntos
- [x] **P01 diseño** — [Modelo de seis objetos y ownership](MODELO_ORDENES_P01.md), [contrato de referencia](CONTRATOS_P01_P02.json).
- [x] **P02 diseño** — [Estados, negativas, caducidad y delegaciones](CICLOS_REVOCACION_P02.md).
- [x] **P03 diseño** — [Iniciativa NPC, fuera de escena y cadena de mando](INICIATIVA_NPC_P03.md).
- [x] **P04 diseño** — [Propuesta LLM, revalidación y fallback](IA_PROPUESTAS_Y_FALLBACK_P04.md).
- [x] **P05 suite incorporada** — [48 escenarios y 19 pruebas unitarias de referencia](PRUEBAS_Y_COORDINACION_P05.md). **GitHub Actions verificada** tras el endurecimiento A-01/A-02: 19/19 pruebas y 48/48 escenarios (run 38228304099). No equivale a ejecución Core/UE5.

Estos checks se refieren únicamente a los entregables independientes: el diseño de P01–P04 está terminado **en documentos**, pero **su ejecución real continúa BLOQUEADA**; P05 sí está cerrada a nivel de referencia. F05 no está `CORE_INTEGRADO`. Véase [acta](../../ACTA_RECONCILIACION_F00_F06_2026-10-13.md).

## Reutilización sin mover rutas
`gameplay/orders/`, `gameplay/chain_of_command/`, `ai/captain_behavior/`, `ai/npc_behavior/`, `gameplay/ship_operations/operational_event_log/`, `gameplay/ship_operations/ship_computer/`, además de F02/F03/F04 (PR #3/#4/#5). Las fuentes aprobadas no se cambian por la propuesta.

## Bloqueos y aceptación
**Foto de Core auditada el 11–12-10-2026:** `main@dcfcb83` estaba previo a las capacidades requeridas de 4.7, 4.9, 4.10 y 4.12; **reconsultar el SHA y las APIs vigentes** antes de integrar. **Actualización 13-10-2026:** las PR F01 #2, F02 #3, F03 #4 y F04 #5 están **fusionadas**. DEC-0001 = Galaxy → nueva **Clase Valhalla**; DEC-0002 = v0.0.1 interna de Sensores. El estado `ESTADO_GLOBAL.json` no se modifica desde esta PR y F05 no se declara `CORE_INTEGRADO`. La iniciativa debe respetar cargo/guardia, conocimiento, recursos y responsabilidad; la IA nunca muta el World State.

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
