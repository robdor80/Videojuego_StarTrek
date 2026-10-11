# F06 — Consola de Sensores

**Estado de fase global:** PLANIFICADA; **trabajo de rama:** referencia verificable preparada. **Madurez demostrada:** REFERENCIA_PROBADA para los barridos y el paquete de coordinación; **meta de fase:** operaciones integradas reales con Core/UE5 (PENDIENTE).

## Entregables de los cinco puntos

- [ ] **F06-P01** — [Auditoría de diez ramas, alcance v0.0.1 y manual](REVISION_ARBOL_MANUAL_P01.md). Árbol y contratos revisados; el PDF está localizado pero su revisión visual queda pendiente.
- [x] **F06-P02 — referencia** — [Detección, filtros, interferencia, conocimiento y resultado parcial](DETECCION_CONOCIMIENTO_P02.md). Reutiliza el motor original; verificado sin efectos autoritativos.
- [x] **F06-P03 — referencia** — [Memoria de nave, transferencias a Ciencia y eventos](MEMORIA_CIENCIA_EVENTOS_P03.md). Propuestas de dossiers, handoff y eventos; persistencia y envío reales pendientes.
- [x] **F06-P04 — contrato** — [Matriz de operación, recursos, puestos, rechazo y demora](OPERACIONES_RECURSOS_ORDENES_P04.md). No introduce economía o permisos falsos en el canon.
- [x] **F06-P05 — suite independiente** — [Pruebas y acuerdo semántico para UE5](PRUEBAS_UE5_Y_CIERRE_P05.md), [evidencia JSON](EVIDENCIA_P05.json). **26/26 pruebas verificadas**, [Actions 38179039670](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38179039670): 8 del motor anterior + 18 F06.

**Los checks indican preparación de entregables de referencia, no cierre de la fase completa.** P01 queda abierto por revisión del PDF.

## Código y CI

- tools/simulation/resolve_sensor_scan.py — motor original **sin modificaciones**.
- tools/simulation/f06_reference.py — orquestación de prueba sin escribir World State.
- tools/simulation/test_f06_reference.py — 18 pruebas automáticas.
- .github/workflows/f06-sensors-reference.yml — compilación y suites del motor + F06.

La implementación devuelve snapshots, candidaturas de dossier y cadenas de eventos; `authoritative=false`, `effects_applied=0` y `reservation_applied=false`. No confirma resultados en campaña.

## Dependencias y límite de la autonomía

PR #2–#6 de F01–F05 todavía pendientes; la interfaz de Core RPG 4.7/4.9/4.10/4.12, tick/persistencia, órdenes realmente entregadas, permisos, transferencia real a Ciencia, presentación UE5 y aceptación de una guardia en MSI **no se han ejecutado**. Tampoco se ha decidido aquí la Dama base de Imperator. No modificar `ESTADO_GLOBAL.json` ni declarar F06 CERRADA hasta cumplir los criterios del plan maestro.

## Fuente original conservada

- gameplay/ship_operations/consoles/sensors/
- gameplay/ship_operations/sensor_resolution/
- gameplay/ship_operations/interconsole/
- gameplay/ship_operations/ship_memory/
- gameplay/ship_operations/operational_event_log/
- docs/manuals/sensors/
- validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json

[Criterios de cierre](../../CRITERIOS_DE_CIERRE.md) · [Plan maestro](../../PLAN_MAESTRO.md) · [Estado global](../../ESTADO_GLOBAL.json).
