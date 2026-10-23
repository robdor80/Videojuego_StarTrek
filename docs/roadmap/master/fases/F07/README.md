# F07 — Pipeline 3D, Rob3D y puente piloto

**23-10-2026 · EN_REVISION / reconciliación de pruebas locales comunicadas.** F02 continúa como fase principal de gobierno, F08 sigue pausada respecto a ejecución E2E y **F07 NO está certificada como UE5_JUGABLE**.

La documentación preparatoria del **13-10-2026** fue correcta en su fecha, pero quedó desactualizada tras los ensayos de Sutherland en el MSI. Véase el [acta de reconciliación 23-10-2026](RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md). Los informes, logs, vídeos, escenas y hashes locales siguen pendientes de incorporación: **avance reportado no equivale a prueba oficial aprobada**.

## DEC-0003 — selección del puente piloto

Para el prototipo interno **v0.0.1 de Sensores** está elegida la **USS Sutherland**, `star_trek_sutherland_bridge.glb`. Se conserva el nombre correcto Sutherland y el hash original de la auditoría F02.

El **Enterprise A New Bridge (Kelvin)** continúa **excluido del piloto Sutherland**. Su estudio posterior como candidato arquitectónico para la **Clase Valhalla** es un trabajo separado; no se intercambian escenas ni se sustituyen activos sin decisión expresa.

## Pasos F07 y estado comprobable

| Paso | Estado de gobierno | Lo ya disponible | Lo pendiente |
|---|---|---|---|
| P01 | EN_REVISION | [Auditoría estática](P01_AUDITORIA_INVENTARIO.md) y fuente GLB identificada; el MSI ha sido utilizado para ensayos de puente reportados. | Inventario/hashes completos locales, procedencia y trazabilidad de derivados. |
| P02 | CERRADA **solo como referencia reproducible** | [Pipeline GLB UV/PBR](P02_PIPELINE_PBR_BLINDAJE.md) y CI; también edición artística PBR local de Sutherland **reportada** en copia Blender. | Verificación de copias, exportación e inspección de materiales en UE5; placa real Valhalla no acreditada. |
| P03 | CERRADA **solo elección** | [Selección Sutherland](P03_PUENTE_PILOTO_SUTHERLAND.md); recorridos e importación UE5 **reportados**, y laboratorios de puertas/sillas. | Evidencia primaria y aceptación integral de puente, consola y procedencia. |
| P04 | EN_REVISION | [Plan UE5](P04_PLAN_PRUEBA_UE5.md); importación/recorridos/colisiones **reportados** (UE07-01 a UE07-04 con matices). | Logs/mapas/hashes; ruta oficial completa; interacción Sensores, retorno, IA, visual y reinicios UE07-05…09. |
| P05 | BLOQUEADA para **cierre de QA** | [Protocolo de QA](P05_CONTROL_RENDIMIENTO_BUILD.md); actividad UE5 y pruebas locales reportadas. | Telemetría numérica, packaged build, aceptación y trazabilidad. |

[Registro de evidencias y pendientes actualizado](EVIDENCIA_Y_PENDIENTES.json) — diferencia explícitamente `REPORTADO_*_PENDIENTE_COTEJO` de `NO_EJECUTADO` y de un hipotético `PASS`.

## Laboratorios relacionados (evidencia externa todavía no cotejada)

- **Puertas y circulación Sutherland:** el seguimiento comunicó **50/50** ensayos de puertas y **44/44** de colisiones/circulación, pero no tenemos aquí sus logs originales.
- **F07-CHAIR-02:** seis mecanismos de base/silla, retranqueo 27 cm, avance 57 cm en 1,9 s y **59/59** comprobaciones comunicadas; aceptación del mecanismo en el laboratorio, **no del sentado**.
- **F07-SEAT-01:** sentado **NO APROBADO**; once poses con intersección muslos/asiento según informe comunicado.
- **PBR artístico:** cambios en copia Blender de suelo, puertas, techo, iluminación, tapicería y otros acabados, con validación UE5 todavía no acreditada.
- **F07-CHAIR-SELECT:** encargo para examinar cuatro GLB alternativos; no hay una silla ganadora certificada en este expediente.

Todos los datos anteriores proceden de seguimiento de las pruebas locales. Su constatación primaria, rutas definitivas y versiones se integrarán en `Documents\StarTrek3D` y se referenciarán aquí **cuando se recuperen realmente**, sin inventar vínculos.

## Reutilización y puerta de cierre

Se conservan las fuentes y la auditoría estática F02 (170 mallas, 19.501 triángulos, 25 materiales unlit, 17 imágenes), sin mover ni renombrar originales ni repositorios de escenas.

**F07 solo podrá cerrarse** cuando exista mapa UE5 transitable **e interactivo** bajo los criterios UE07-01…09, evidencia MSI cotejada, materiales/colisiones validados, telemetría y build reproducibles, y control documental de procedencia. Se distinguirán las pruebas ya reportadas de los requisitos todavía abiertos.

## Implementación de referencia P02

`tools/assets/f07_pbr_plate.py` genera un ejemplo GLB PBR/UV; `tools/assets/f07_gltf_audit.py` lo audita, `tools/validation/test_f07_pbr_pipeline.py` ejerce regresiones y `.github/workflows/f07-pbr-reference.yml` corre la CI.

**Esa CI sigue probando únicamente la referencia procedural; no prueba escenas UE5, materiales de Sutherland, animaciones, ni blindaje de Valhalla.** La edición PBR local reportada queda diferenciada de la referencia CI.
