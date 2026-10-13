# F07 — Pipeline 3D, Rob3D y puente piloto

**13-10-2026 · EN_REVISION / preparación paralela autorizada.** F02 permanece como única fase principal activa; F08 continúa pausada. **F07 NO es todavía UE5_JUGABLE.**

## DEC-0003 — nueva elección expresa del autor
El puente para el prototipo interno **v0.0.1 de Sensores** será **USS Sutherland**, archivo auditado star_trek_sutherland_bridge.glb. El nombre «Sunderland» mencionado oralmente corresponde provisionalmente a Sutherland; no crear otro asset sin evidencia. Selección de puente aprobada, **viabilidad técnica y derechos pendientes**.

El **puente Kelvin queda EXCLUIDO de v0.0.1**, reservado para estudiar adaptación futura a Sovereign u Odyssey; no usarlo como sustituto automático. El puente piloto no define la nueva Clase Valhalla, inspirada en Galaxy.

## Pasos y evidencias
| Paso | Estado | Entrega de la rama | Falta |
|---|---|---|---|
| P01 | EN_REVISION | [Inventario y procedencia](P01_AUDITORIA_INVENTARIO.md), catálogo, generador local | Listado MSI, licencias y hashes derivados |
| P02 | CERRADA SOLO REFERENCIA GLB/UV/PBR | [Pipeline Blender/Rob3D/UE5, UV-PBR y blindaje](P02_PIPELINE_PBR_BLINDAJE.md) | Materiales aplicados a Sutherland/Valhalla y visualización en UE5 pendientes |
| P03 | CERRADA SOLO ELECCIÓN | [Sutherland elegido](P03_PUENTE_PILOTO_SUTHERLAND.md) | Tránsito, colisiones, interacción y derechos |
| P04 | EN_REVISION | [Guion UE5 primera persona y consola](P04_PLAN_PRUEBA_UE5.md) | Montaje y recorrido real en MSI |
| P05 | BLOQUEADA | [QA, rendimiento, build](P05_CONTROL_RENDIMIENTO_BUILD.md) | Ejecutar UE5/packaging/telemetría |

[Registro de ensayos no ejecutados](EVIDENCIA_Y_PENDIENTES.json).

## Reutilización y puerta de cierre
Se conserva el GLB fuente y la auditoría estática de F02 (170 mallas, 19.501 triángulos, 25 materiales unlit, 17 imágenes), así como los directorios originales assets/ships/, assets/scenes/, art_direction/visual_bibles/, presentation/, ui/bridge/, ui/lcars/. No mover ni renombrar originales. El inventario del MSI queda pendiente hasta que el autor tenga acceso: no bloquea trabajo documental ni scripts.

**F07 solo podrá cerrarse con un mapa UE5 realmente transitable e interactivo, pruebas verificadas en MSI, build/telemetría reproducibles y revisión de procedencia.** Un test Python o fixture no prueba juego, Core ni UE5.

## Implementación de referencia posterior a la PR inicial

Scripts: `tools/assets/f07_pbr_plate.py` (genera GLB de placa técnica PBR+UV), `tools/assets/f07_gltf_audit.py` (inspector estático y SHA) y `tools/validation/test_f07_pbr_pipeline.py` (calidad reproducible). CI: `.github/workflows/f07-pbr-reference.yml`. **Solo el ejemplo procedural queda probado por automatización**; los originales del MSI, el Sutherland y las placas definitivas siguen sin ejecutar en UE5. El autor no tiene que facilitar hoy el inventario local.
