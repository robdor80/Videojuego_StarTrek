# Auditoría técnica GLB — USS Sutherland Bridge
**Fecha:** 2026-10-12  
**Alcance:** inspección directa del archivo original `star_trek_sutherland_bridge.glb` entregado por el autor; análisis de glTF 2.0 y geometría vía Python/trimesh/Pillow. No se ha abierto este archivo en Unreal Engine y no es una validación de licencia de la franquicia.

## Identidad verificable del archivo recibido
- Archivo: `star_trek_sutherland_bridge.glb`.
- Tamaño: **13.429.416 bytes** (12,81 MiB).
- **SHA-256:** `53ac9b52fe9fb4b19c5488d7265f6f7471383ae89071204fd3fc62232ca3889b`.
- Formato: **glTF 2.0 binario válido**, generador `Sketchfab-12.67.0`, una escena.
- Metadatos internos `asset.extras`: `author=Andrew Perdzock (https://sketchfab.com/AndrewPerdzock)`, `license=CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)`, `title=Star Trek: Sutherland Bridge`; fuente `https://sketchfab.com/3d-models/star-trek-sutherland-bridge-7dcbb60473164f36a0a4f39df11b34c1`. **La licencia está declarada dentro del fichero original**, no verificada independientemente en la página de Sketchfab (acceso automatizado restringido); los derechos de Star Trek como franquicia son independientes y deben evaluarse antes de redistribuir.
- El fichero recibido **no se debe confundir automáticamente** con el `..._Validado_ae9e06...glb` mostrado en Rob3D: no se ha comparado el contenido de esa exportación y su nombre puede reflejar un proceso de conversión.

## Estructura geométrica
| Métrica | Resultado |
|---|---:|
| Mallas/objetos `mesh` | **170** |
| Nodos jerárquicos glTF | **343** |
| Primitivas | **170** (modo TRIANGLES) |
| Triángulos | **19.501** |
| Vértices indexados reportados por trimesh | **39.523** |
| Materiales | **25** |
| Texturas/imágenes incluidas | **17/17**, integradas en el BIN; sin rutas externas |
| Animaciones / armatures / skins | **0 / 0 / 0** |
| Bounds mundo según trimesh | **19,879 × 7,446 × 16,133 m (X,Y,Z)**; comprobar dimensiones y up-axis en UE5 |
| Triángulos de área casi nula detectados | **0** a umbral 1e-10 unidades locales cuadradas |
| Mallas cerradas (watertight) | **0 de 170**; frecuente para escenarios de superficies abiertas, no equivale a mallas defectuosas |
| Vértices NaN/Inf | **0** |
| UV | **165/170 mallas** con al menos `TEXCOORD_0`; las otras 5 no usan textura UV y deben examinarse si se retocan |

**Rendimiento:** 19,5 mil triángulos es una carga geométrica baja para un puente; los 170 elementos y 25 materiales sí merecen comprobar batches/draw calls al importarlo. No afirmar FPS sin medición MSI. Evitar fusionar puertas, asientos o pantallas que luego necesiten interacción; optimizar objetos decorativos estáticos por material cuando se demuestre útil.

## Hallazgo visual principal — NO son materiales PBR
- **Los 25/25 materiales llevan `KHR_materials_unlit`**; no hay `normalTexture`, `occlusionTexture` ni texturas de roughness/metallic configuradas como mapas normales del glTF.
- Por tanto, las paredes, techo, suelo y LCARS reciben tratamiento `unlit` en el archivo exportado. Esto puede explicar en gran medida la apariencia plana al verlo en Rob3D frente a la escena configurada en Sketchfab (que podría añadir efectos de visor/postprocesado). **No es evidencia de texturas faltantes**.
- **Propuesta sin alterar el original:** convertir selectivamente suelo, muros, pilares, asientos y techo a materiales **Default Lit / PBR** en UE5 o Blender, conservando texturas base. Mantener pantallas LCARS y luminarias como **emissive** cuando resulte apropiado y ajustar su intensidad. Añadir iluminación y ambient occlusion reales. Controlar espacios de color sRGB / linear, normales, especular y roughness.
- La mayor imagen es un PNG **4096×2048, ~9,1 MB comprimidos**, enlazado al material `plaque`. Si no hay lectura de la placa en primer plano, conviene ensayar una resolución más baja, **sin sobrescribir el original**.
- Las texturas suman aproximadamente **73 MiB de memoria RGBA8 base** si todas se decodifican sin compresión GPU, o **97 MiB con cadena completa de mipmaps** como estimación teórica, no medición real de VRAM UE5. El empaquetado/comprensión de UE5 cambia el resultado.

## Puertas, asientos y consolas
- Existen **cuatro meshes** que usan el material `door` y **dos** con `turbolcar`; esto **no demuestra** que las puertas sean piezas independientes en una animación funcional ni que admitan movimiento sin retoque.
- Existen puestos laterales y pantallas; las imágenes LCARS son **estáticas**; habrá que definir un punto interactivo y una superficie de salida dinámica en UE5.
- No hay animaciones ni rig. Asientos utilizables, puertas con apertura y NPC sentados/reacciones deben integrarse después. Las colisiones no están certificadas; glTF normal no incluye las colisiones gameplay de UE5.

## Recomendación para v0.0.1
**Apto como candidato técnico prioritario; NO validado aún como puente jugable.** Es posible que requiera poco modelado base; todavía falta la prueba de UE5. Proceso sugerido:
1. Preservar el GLB recibido e identificar igualmente el `Validado` de Rob3D con SHA propia.
2. Importar **una copia** a un nivel aislado UE5, sin sustituir el puente Kelvin existente.
3. Confirmar tamaño humano, orientación de eje, suelo, pilares y acceso a todas las estaciones.
4. Crear colisiones simples por grupos: suelo, escalones/plataforma, paredes, mesas, sillas y barandillas; comprobar que ni techo ni objetos invisibles bloqueen el recorrido.
5. Hacer una prueba *walkthrough* real con primera persona en MSI, desde acceso/turboascensor hasta estación de Sensores elegida.
6. Ajustar PBR para elementos arquitectónicos; mantener LCARS emisivos y sustituir una pantalla por superficie interactiva/Widget Component/Render Target.
7. Registrar el resultado del import, asset path, UE5 version, capturas, draw calls/FPS y defectos pendientes.
8. Verificar licencia efectiva y atribuciones antes de distribuir o publicar derivados.

**Condición de selección:** supera la prueba de transitabilidad e interacción sin bloqueantes y no presenta problemas de procedencia. Solo entonces elegir entre Sutherland y Kelvin para la v0.0.1. El desarrollo de la clase Galaxy definitiva continúa separado y F07/F08 no se reactivan por esta auditoría.

**Estado de hallazgo:** INSPECCIÓN_ESTÁTICA_COMPLETA / IMPORTACIÓN_UE5_PENDIENTE / LICENCIA_DECLARADA_CC_BY_4_0_NO_AUDITADA_FRENTE_A_DERECHOS_FRANQUICIA.
