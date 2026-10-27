# F07-P05 — Telemetría, build y QA en MSI

**Actualizado 23-10-2026 · BLOQUEADA para cierre de QA y aceptación, NO por falta de cualquier prueba UE5.**

El documento inicial del 13-10-2026 decía que UE5 no había sido ejecutado en el MSI. **Ese enunciado quedó desactualizado**: desde entonces se ha comunicado importación, circulación y ensayos de puertas/sillas del Sutherland. [Acta de reconciliación](RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md).

**Pero no constan aquí una build empaquetada, medidas reproducibles de rendimiento ni pruebas oficiales UE07 completas.** No atribuir `PASS` por extrapolación.

## Control de evidencias faltantes

| Evidencia de P05 | Estado |
|---|---|
| Ejecución UE5 de Sutherland en MSI | **Reportada, pendiente de cotejo de escena/log** |
| Puertas y circulación en laboratorio | **Resultados favorables reportados; logs pendientes** |
| Movimiento de seis sillas | **Mecanismo favorable reportado; sentado NO aprobado** |
| Registro de FPS y tiempos GPU/CPU | **Sin cifras cotejadas** |
| RAM, VRAM y draw calls | **Sin cifras cotejadas** |
| Comparación PIE frente a build Development privada | **Sin resultados cotejados** |
| Build empaquetada que abre sin editor | **NO_EJECUTADO en expediente** |
| Warnings de empaquetado y hash del ejecutable | **Sin datos cotejados** |
| Materiales PBR Sutherland/LCARS en UE5 | **Sin aceptación documentada** |
| UE07-01…09 y procedencia del material | **Cierre pendiente según matriz P04** |

## Protocolo de medición (sigue vigente)

Equipo objetivo: MSI Windows 11, i9-14900HX, 32 GB RAM, RTX 4070 portátil 8 GB. No inferir FPS ni VRAM de la cantidad de triángulos.

Registrar driver, versión UE5, `.uproject`, mapa, resolución, escalado, perfil de calidad y hash GLB. Medir FPS, frame time CPU/GPU, RAM, VRAM y draw calls con herramientas compatibles de Unreal (por ejemplo `stat fps`, `stat unit`, `stat gpu`, `stat rhi`); repetir recorrido de entrada a Sensores, modo consola y retorno. Comparar PIE con build Development **ejecutada sin editor**.

En el empaquetado documentar pasos, warnings, hash del ejecutable, assets incluidos y las condiciones de procedencia/atribución aplicables a la distribución prevista. Los ensayos privados en MSI y la eventual publicación de recursos en GitHub son contextos distintos.

## Condición de cierre

P05 permanece **BLOQUEADA** para certificación hasta reunir trazas MSI, métricas, build reproducible y resultados UE07 completos. F07 seguirá `EN_REVISION`. La conexión E2E CoreRPG + órdenes + escaneo + persistencia pertenece además a F08.

La CI `f07-pbr-reference.yml` solo acredita el ejemplo GLB/UV/PBR; no mide rendimiento en MSI ni ejecuta Unreal.
