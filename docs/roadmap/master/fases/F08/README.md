# F08 — Vertical slice jugable v0.0.1

**Estado de la fase global:** **PLANIFICADA / PAUSADA**, pendiente de reactivación formal. F01 está cerrada a nivel de diseño, F02 es la fase principal, F03–F06 tienen entregables de referencia fusionados pero no integración Core/Host. No convertir la prueba interna `v0.0.1` en un lanzamiento por cambios del plan. [Acta de reconciliación](../../ACTA_RECONCILIACION_F00_F06_2026-10-13.md).
**Nivel objetivo:** UE5_JUGABLE / ACEPTACION_SUPERADA.

## Objetivo

Una guardia completa de Sensores en un puente 3D con órdenes, resultados y continuidad.

## Pasos y entregables

- [ ] **F08-P01** — Preparar nave, guardia, capitán NPC, oficial jugador y contacto preexistente.
- [ ] **F08-P02** — Recibir una orden legítima del capitán NPC sin que el mundo dependa del jugador.
- [ ] **F08-P03** — Ejecutar barrido desde consola 3D; informar resultados y recibir consecuencias.
- [ ] **F08-P04** — Guardar/cargar orden, acciones, conocimiento y eventos; seguir operativo sin IA remota.
- [ ] **F08-P05** — Superar aceptación extremo a extremo y publicar evidencias del build y rendimiento.

## Material del repositorio que se aprovecha sin moverlo

- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`
- `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`
- `gameplay/ship_operations/operational_event_log/`
- `presentation/`
- `ui/bridge/`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).


## Preparación paralela autorizada el 13-10-2026 (sin cierre)

Tras completar los preparativos autónomos posibles de F07 (PR #11 y #12 fusionadas), se ha autorizado **preparar** F08 sin ocultar las puertas de UE5/Core. Entregables de la rama:

- [F08-P01 — escenario de guardia, identidades, orden y límites](P01_ESCENARIO_GUARDIA_PREPARACION.md): documentación de puesta en escena, **sin ejecución**.
- [F08-P02…P05 — plan de pruebas y aceptación](PLAN_DE_ACEPTACION_P02_P05.md): secuencia, casos negativos, 13 invariantes y evidencias requeridas, todas **NO_EJECUTADO**.

La fase permanece **PLANIFICADA / PAUSADA para runtime**, sin alterar el estado global ni señalar P01–P05 como cerrados. F02 conserva su condición de única fase principal EN_CURSO. Para completar F08 hay que integrar Core↔UE5, importar y recorrer Sutherland en el MSI, ejecutar los casos y adjuntar build/logs verificables.

## Dependencias y límites

F02–F07 y runtime Core RPG real siguen siendo dependencias. En particular, la [prueba de referencia integrada de Sensores](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38321712021) **no** acredita save/load real ni un puente UE5 jugable. No cerrar por documentación únicamente.

## Puerta de cierre

Build UE5 verificable con guardia reproducible, interacción de consola, historial y guardado real. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
