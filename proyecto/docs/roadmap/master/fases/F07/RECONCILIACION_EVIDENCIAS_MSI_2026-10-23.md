# F07 — Reconciliación de pruebas locales Sutherland (23-10-2026)

**Tipo:** actualización documental de avance comunicado; **no** constituye ejecución de Unreal Engine ni auditoría de los archivos locales por el autor de este documento.  
**Estado de F07:** `EN_REVISION`; **no** alcanza todavía `UE5_JUGABLE`.  
**Fuente inicial:** conversaciones de seguimiento y aprobaciones humanas del proyecto entre el 13 y el 23 de octubre de 2026.  
**Evidencia primaria pendiente:** proyectos UE5, informes de laboratorios Codex, capturas, logs, hashes y resultados de comandos en el MSI. No están depositados en este repositorio.

## Motivo

El expediente de 13-10-2026 describía correctamente una preparación de F07 sin ejecución local entonces. Con posterioridad se efectuaron pruebas y laboratorios en el MSI. El estado antiguo `NO_EJECUTADO` se convirtió en desactualizado para algunas actividades; **no debe transformarse automáticamente en `PASS` ni `CERRADA` sin cotejar su evidencia primaria**.

## Avances reportados, pendientes de cotejo de artefactos

| Actividad | Declaración disponible | Lectura de madurez |
|---|---|---|
| Importación Sutherland UE5 | El puente fue importado y recorrido por el jugador en UE5 en el MSI. | Ejecución comunicada; faltan mapa exacto, configuración, log y prueba del hash del derivado. |
| Locomoción y circulación | Se realizaron recorridos y pruebas de obstáculos/colisiones dentro del Sutherland. | Pruebas parciales comunicadas; no acreditan automáticamente los criterios completos de UE07-02/03/04. |
| Puertas | Se comunicaron pruebas de apertura/cierre y circulación; resumen del laboratorio: 50/50 pruebas de puertas y 44/44 de circulación/colisiones. | Resultados de laboratorio reportados; faltan informes/logs originales y trazabilidad al mapa/commit. |
| Sillas: F07-CHAIR-02 | Seis bases y movimiento probados; retranqueo de 27 cm, recorrido de avance de 57 cm y duración de 1,9 s. Se comunicaron 59/59 pruebas de sillas superadas y aceptación visual humana. | Mecanismo de laboratorio favorable, **no** equivale a sentado funcional ni a cierre F07. |
| Sentado: F07-SEAT-01 | Resultado no aprobado: intersección de muslos y cojín en once poses muestreadas con las animaciones ensayadas. | Incidencia reproducible según informe comunicado, **pendiente de solución**. |
| PBR Sutherland | Edición artística de materiales de suelo, techo, puertas, luces y mobiliario en copia Blender. | Trabajo artístico local reportado; **no** certifica importación/verificación PBR en UE5 ni modifica la prueba CI del GLB procedural. |
| Nueva selección de sillas | Existe un encargo para comparar cuatro GLB en laboratorio independiente. | Encargo/proceso separado: **sin resultado aceptado registrado aquí**. |

**Nota de precaución:** los recuentos 50/50, 44/44 y 59/59 se recogen *como comunicados* en el seguimiento; esta PR documental no ha inspeccionado los logs originales. No asignar fecha exacta, porcentaje de rendimiento UE5, rutas de mapas ni checksums no constatados.

## Matriz oficial UE07 — criterio de reconciliación

- **UE07-01 (importación aislada):** importación real reportada; **pendiente evidencia versionada** de aislamiento/configuración/hash.
- **UE07-02 (escala humana):** locomoción real reportada; **pendiente prueba metrológica** a escala Quinn/cápsula.
- **UE07-03 (tránsito completo):** recorridos reales reportados; **pendiente evidencia del trayecto exacto** turboascensor–Sensores–salida exigido por el plan.
- **UE07-04 (colisiones sólidas):** laboratorios/recorridos reportados; **pendiente matriz final** y comprobación de bloqueantes en mapa de aceptación.
- **UE07-05 (activar consola), UE07-06 (salir/restaurar input), UE07-07 (sin IA remota), UE07-08 (materiales/LCARS en UE5), UE07-09 (reinicios):** **no consta prueba oficial cotejada**; conservar `NO_EJECUTADO` hasta evidencia específica.

El puente **no** debe declararse `UE5_JUGABLE` por los laboratorios de puertas o sillas.

## P05 y riesgos todavía abiertos

- Telemetría real (FPS, frame time CPU/GPU, RAM, VRAM, draw calls) **sin valores cotejados**.
- Build independiente del editor y resultado de packaging **no verificados**.
- Comparación hash/fuente y condiciones de procedencia **pendientes de cierre documental**.
- Sentado/levantado natural **no aprobado**; no bloquear por ello el reconocimiento de ensayos previos del mecanismo.
- Integración de la consola de Sensores en UE5 con entrada/salida, UX, tres reinicios y material legible: **pendiente de evidencia específica**.
- CoreRPG, save/load y escaneo real son límites de F08/Core/F06, no éxitos implícitos de F07.

## Próximo trabajo de recuperación documental en MSI

1. Localizar en el MSI los laboratorios **F07-CHAIR-02**, **F07-SEAT-01** (ruta comunicada: `C:\Users\andro\Documents\StarTrek_3D\F07_SEAT_01_Lab`) y las escenas/ensayos originales del puente y las puertas.
2. Extraer manifiestos, versiones UE5/Blender, mapa, capturas, vídeos, logs, comandos y resultados, sin mover ni sobrescribir originales.
3. Registrar hashes y rutas de artefactos recuperables en el centro documental propuesto `Documents\StarTrek3D`; distinguir archivos locales privados de recursos versionables en el repositorio público.
4. Mapear cada evidencia a un **UE07-XX**, dejando constancia de fecha, responsable, variante de escena, criterio de aceptación y defectos restantes.
5. Solo tras cotejo: promover selectivamente estados a `PASS`, `FAIL` o `EJECUTADO_CON_RESERVAS`, actualizar `ESTADO_GLOBAL.json` y valorar el cierre de P04/P05.
6. Conservar el estado histórico del corte del 13-10-2026; esta acta explica la evolución, **no reescribe lo que era cierto entonces**.

## Límites

No se han accedido ni modificado carpetas del MSI, modelos 3D, proyectos Unreal, Blender o CoreRPG. No se ejecutaron pruebas UE5 desde GitHub. No se han fusionado cambios en `main` por el mero hecho de preparar esta acta.
