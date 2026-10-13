# F07-P05 — Telemetría, build y QA en MSI

**BLOQUEADA: no se ha ejecutado UE5 ni compilado un paquete en el MSI.**

Objetivo hardware: MSI Windows 11, i9-14900HX, 32 GB RAM, RTX 4070 portátil 8 GB. No estimar FPS ni VRAM real por triángulos.

Tras abrir el mapa Sutherland, anotar driver, versión concreta de UE5/proyecto, resolución 2560×1600 o configuración usada, escalado, calidad, nivel, commit, hash del GLB. Medir FPS, frame time GPU/CPU, RAM, VRAM y draw calls mediante herramientas de UE compatibles (stat fps, stat unit, stat gpu, stat rhi). Repetir recorrido spawn→Sensores→modo consola→salida; comparar PIE con build privado Development, incluido inicio fuera del editor.

En empaquetado registrar tiempo/procedimiento, warnings, hash del ejecutable, si abre sin editor, assets realmente incluidos y derechos verificados. **No publicar binarios o texturas de terceros sin comprobación de permisos y atribuciones**, independientemente de la prueba personal.

Para cerrar F07: completar UE07-01…09 con evidencia real en MSI, sin bloqueantes de navegación/interacción, material/colisión probado y telemetría/build trazables. Para F08 se exigirá adicionalmente **integración real** Core↔UE5, orden, detección, eventos y save/load. Un catálogo JSON/CI verde no basta.
