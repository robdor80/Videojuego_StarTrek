# F06 — Consola de Sensores

**Estado de fase global reconciliado:** **EN_REVISION**, PR #7 ya **fusionada en `main`**. **Madurez demostrada:** `REFERENCIA_PROBADA` en barridos y cadena F04→F05→F06. P01 continúa EN_REVISION por PDF; P02–P04 siguen BLOQUEADAS para operativa autoritativa; P05 cerrada a nivel de pruebas de referencia. Meta de fase: Core/UE5 real (**PENDIENTE**). [Acta](../../ACTA_RECONCILIACION_F00_F06_2026-10-13.md).

## Entregables de los cinco puntos

- [ ] **F06-P01** — [Auditoría de diez ramas, alcance v0.0.1 y manual](REVISION_ARBOL_MANUAL_P01.md). Árbol y contratos revisados; el PDF está localizado pero su revisión visual queda pendiente.
- [x] **F06-P02 — referencia** — [Detección, filtros, interferencia, conocimiento y resultado parcial](DETECCION_CONOCIMIENTO_P02.md). Reutiliza el motor original; verificado sin efectos autoritativos.
- [x] **F06-P03 — referencia** — [Memoria de nave, transferencias a Ciencia y eventos](MEMORIA_CIENCIA_EVENTOS_P03.md). Propuestas de dossiers, handoff y eventos; persistencia y envío reales pendientes.
- [x] **F06-P04 — contrato** — [Matriz de operación, recursos, puestos, rechazo y demora](OPERACIONES_RECURSOS_ORDENES_P04.md). No introduce economía o permisos falsos en el canon.
- [x] **F06-P05 — suite independiente** — [Pruebas y acuerdo semántico para UE5](PRUEBAS_UE5_Y_CIERRE_P05.md), [evidencia JSON](EVIDENCIA_P05.json). **31/31 pruebas de sensores verificadas en la auditoría del 12-10-2026**, [Actions 38228217392](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38228217392): 8 del motor anterior + 23 F06. En aquel corte, tres casos F04→F05→F06 se omitieron por faltar PR precedentes; **la CI integrada posterior ejecutó y superó los tres** (run 38321712021, 0 skips).

**Los checks indican preparación de entregables de referencia, no cierre de la fase completa.** P01 queda abierto por revisión del PDF.

## Código y CI

- tools/simulation/resolve_sensor_scan.py — motor original reutilizado; cambio mínimo para **no exponer censos internos de entidades o firmas no detectadas** en ningún resultado público.
- tools/simulation/f06_reference.py — orquestación de prueba sin escribir World State.
- tools/simulation/test_f06_reference.py — 23 pruebas automáticas.
- tools/simulation/test_f04_f05_f06_cross_phase.py — 3 casos de contrato F04→F05→F06, **de ejecución obligatoria** ahora que F04/F05 están en `main`. No son Core real.
- .github/workflows/f06-sensors-reference.yml — compilación y suites del motor + F06.

La implementación devuelve snapshots, candidaturas de dossier y **event_candidates**. El campo `events` permanece vacío; **nunca** se generan informes pronunciados, acciones completadas o eventos confirmados a partir de un cálculo. `report_pending=not_reported`, `authoritative=false`, `effects_applied=0` y `reservation_applied=false`. No confirma resultados en campaña.

## Dependencias y límite de la autonomía

**PR #2–#6 ya fusionadas**, con la decisión Galaxy/Enterprise-D → **nueva Clase Valhalla** aprobada (fecha de servicio todavía sin fijar). Esto no implica disponibilidad de esa clase en el fixture de Sensores de 2372, ni que el primer puente de pruebas tenga que ser Galaxy. La interfaz real de Core RPG (versiones y APIs a verificar), tick/persistencia, órdenes entregadas, permisos reales, transferencia auténtica a Ciencia, consola UE5 y aceptación de una guardia en el MSI **no se han ejecutado ni validado en esta PR**. No modificar `ESTADO_GLOBAL.json` ni declarar F06 CERRADA sin cumplir los criterios del plan maestro.

## Fuente original conservada

- gameplay/ship_operations/consoles/sensors/
- gameplay/ship_operations/sensor_resolution/
- gameplay/ship_operations/interconsole/
- gameplay/ship_operations/ship_memory/
- gameplay/ship_operations/operational_event_log/
- docs/manuals/sensors/
- validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json

[Criterios de cierre](../../CRITERIOS_DE_CIERRE.md) · [Plan maestro](../../PLAN_MAESTRO.md) · [Estado global](../../ESTADO_GLOBAL.json).

## Endurecimiento de auditoría — 2026-10-12

- **A-02:** la autorización simulada requiere binding de referencia F05 vinculada a operador, acción `sensor_scan`, puesto, nave, revisión y ventana temporal. Una cadena proporcionada por el Host **no demuestra legitimidad real**; en producción se requiere decisión verificable de Core.
- **A-03:** se eliminan `entities_in_scope` y `signatures_evaluated` de la salida **del propio motor base**, evitando el camino de bypass por acceso directo. Siguen calculándose únicamente los contactos efectivamente observados.
- **A-04:** se rechazan magnitudes no finitas, booleanos usados como números, valores fuera de rango y mundo malformado antes de producir salidas.
- **A-05:** la CI observa también los documentos F06 y los contratos originales de Sensores; incorpora ejecución condicional de las suites F03/F04/F05 y una prueba cruzada **con estado OMITIDA si faltan ramas**.
- **A-06:** el resultado del barrido no genera ningún evento autoritativo y no inventa `REPORT_MADE` ni `ACTION_COMPLETED`. Core debe confirmar por separado inicio, resultado, informe y terminación.
- **A-10:** sigue pendiente la lectura visual del PDF del manual; no declarar F06-P01 cerrada.
- **A-07/A-08:** Core real, save/load, UE5 y E2E siguen pendientes; no inferir `CORE_INTEGRADO` del CI Python.

**CI histórica de referencia (12-10-2026):** [run 38228217392](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38228217392) SUCCESS en `a6ef6895208a448c235c60ffced522560ce86a8a`: **31 casos de sensores** y tres interphase OMITIDOS entonces. **Comprobación posterior, 13-10-2026:** [Actions 38321712021](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38321712021) SUCCESS para la PR integrada: 8+23 Sensores, 3 pruebas cruzadas **ejecutadas**, 26 F03, 17 F04 y 19 F05: **96 tests superados**. Core RPG, guardado real, manual PDF y UE5 siguen pendientes.
