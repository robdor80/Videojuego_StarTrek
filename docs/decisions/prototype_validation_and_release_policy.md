# Política aprobada — prototipos internos y lanzamiento Star Trek RPG

**Estado:** APROBADA (DEC-0002, delimitación de producto) · **Fecha:** 2026-10-11 · **Fase:** F01-P04 · **Autor:** Roberto, por conversación de coordinación.

## Dos sistemas de progreso distintos

- Las **fases F00–F15** del plan maestro gobiernan preparación, desarrollo, integración y aceptación de las capacidades del videojuego.
- Las **versiones v0.0.x** son *builds de validación internos*, pensados para probar una funcionalidad concreta; no son expansiones publicadas, temporadas jugables ni episodios obligatorios del juego final.
- El **producto integrado** aspirará a una versión de lanzamiento 1.0, precedida por cuantas pruebas alfa/beta resulten necesarias. La numeración no garantiza fecha de entrega ni finalización de una fase.

## Primer prototipo aprobado — v0.0.1

Una **guardia de Sensores** en un puente 3D: recibir orden, manejar una consola real, resolver escaneo con estado autoritativo y límites de conocimiento, informar, registrar, evaluar y persistir la prueba según contratos reales de Core/UE5. El fixture actual 2372-03-14 es material reproducible de aceptación; la elección concreta del puente de prueba es independiente de la Dama/Imperator final.

No necesita incluir los cuatro años jugables de Academia, todas las naves, NPC completos ni el resto de consolas. No se publicará como experiencia final por sí misma.

## Posibles pruebas siguientes (solo ejemplos)

- **v0.0.2 (idea no cerrada):** Academia 3D; clase con instructor, una práctica real de Sensores y evaluación.
- **v0.0.3 (idea no cerrada):** horarios, vida social y persistencia de cadetes.
- **v0.0.4 (idea no cerrada):** guardias a bordo, interacción y otras consolas.

Su orden, contenido, número y ejecución **no están aprobados todavía como entregas**, y no sustituyen el camino crítico por fases.

## Reutilización vs descartes

- **A conservar/reutilizar cuando funcionen:** operaciones y contratos, componentes UI, consolas, sistemas Core, NPC/identidad, escenarios modulares, assets utilizables legalmente, pruebas regresivas, optimizaciones.
- **Descartables sin pérdida de canon:** misiones guiadas de evaluación, NPC ficticios de test, datos/semillas de fixture, telemetría y guardados de laboratorio. No se insertarán automáticamente en el juego final.
- **Regla de independencia:** los datos de cada ensayo viven en un entorno/guardado aislado del historial persistente de una futura campaña jugable.
- **Regla de aceptación:** cada prototipo se cierra contra pruebas reproducibles del componente, no por su nombre de versión ni por mostrar una captura 3D.

## Límites de responsabilidad

El prototipo no autoriza implantar un motor Star Trek paralelo a Core RPG. IA remota interpreta pero no muta World State. El puente piloto es selección técnica posterior (`DEC-0003`); la Dama base Imperator sigue pendiente de decisión de autor (`DEC-0001`).

**Enlaces:** `docs/roadmap/master/fases/F01/PROPUESTA_MVP_Y_PRESUPUESTO.md`, `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`, `docs/roadmap/master/PLAN_MAESTRO.md`, `docs/roadmap/master/CRITERIOS_DE_CIERRE.md`.
