# Sutherland — reparación del hueco superior del turboascensor

29/10/2026. Trabajo exclusivamente local en Blender 5.2.2 LTS.

Resultado: `../../blender/Miranda_Puente_Sutherland_PBR_Manual_01_Seis_Sillas_Hueco_Cerrado_01.blend`.

## Diagnóstico

El marco del lado del puente, `Plane.004_0`, ya tenía su borde superior interior a aproximadamente 300,1 cm. El marco de la cabina, `Plane.039_0`, conservaba ese borde a aproximadamente 388,5 cm. La diferencia dejaba abierto el frente posterior de la zona superior, desde el cual se veía el reverso del otro marco. Las normales de las caras existentes estaban orientadas correctamente: el problema era el desfase de geometría entre ambos marcos.

## Reparación limitada

- Único objeto modificado: **Plane.039_0**. No se han creado objetos ni materiales.
- Se trasladaron en Z mundial 40 de sus 56 vértices, correspondientes al borde interior superior y a sus encuentros achaflanados, **−87,748953 cm**. Se conservaron los límites exteriores y la parte superior original del marco.
- Se mantienen las 28 caras, conectividad, índices, UV, normales personalizadas, asignaciones de material y transformaciones del objeto. La anchura de envolvente presenta únicamente una diferencia numérica de 0,000000834 m por la conversión entre coordenadas locales y mundiales.
- El dintel inferior queda a Z ≈ 3,00773195 m. La parte superior real de las hojas de este archivo está a Z ≈ 3,00723195 m; se conserva una holgura de **0,5 mm**. Las hojas no se desplazan ni se redimensionan. El achaflanado del marco se conserva y el paso libre central no se invade.
- El cierre usa las propias caras del marco: no añade paneles superpuestos. Su asignación existente a `PBR_Mamparos_Gris_Oscuro` permanece intacta, disponible para que el usuario la mantenga o reasigne. No se ha realizado texturizado adicional.

## Verificación independiente

El resultado se abrió en otro proceso de Blender y pasó las comparaciones de `verificacion_reapertura.json`:

- 513 objetos; todas las demás mallas y propiedades de objetos se conservan. Las seis sillas, cilindros, plataformas, consolas, hojas y sus jerarquías permanecen intactos.
- Materiales PBR, imágenes empaquetadas, rutas de imágenes, asignaciones y UV sin cambios. También se conservan colecciones, visibilidad, cámara, luces, mundo y configuración persistente de escena.
- 1.089 rayos desde el puente y 1.089 desde la cabina: 2.178/2.178 interceptan el cierre con la normal exterior correcta.
- Sin caras degeneradas ni inversiones de normales en el marco reparado. Verificación visual de ambos lados con descarte de caras posteriores activado.
- Las vistas `capturas/Antes_Puente.png`, `Antes_Cabina.png`, `Reparado_Puente.png` y `Reparado_Cabina.png` son comprobaciones Workbench. El azul identifica temporalmente el marco de cabina; no es un material guardado en el resultado. Las cámaras y ajustes de esas vistas no se guardan en el .blend.

## Conservación

El original se conserva byte por byte respecto a la copia de trabajo tomada tras su último guardado, `Fuente_Original_Inspeccionada.blend`:

SHA-256 original: `23005faed0016472d2f2f73e4f4c0bda830e2961a4ebdf2e90499b9ee94a96c6`.

SHA-256 resultado: `fd9106aa663e37fc278cc03be7f68c0ca0d179cf6822b260af71c225d7885e18`.

Durante la reapertura se detectó el reajuste automático de rutas relativas al guardar desde la copia de trabajo. Ese primer resultado se conserva como `Resultado_Antes_Conservar_Rutas.blend`; el resultado definitivo se guardó manteniendo las rutas originales y superó la verificación completa. Se conservan manifiestos y registros de los intentos de comprobación.

No se ha intervenido en Unreal Engine, mecanismos de apertura, textos, materiales, sillas ni consolas. No se han ejecutado operaciones Git.

Scripts reproducibles, con protecciones contra sobrescritura: `../scripts/hueco01_inspeccionar.py`, `hueco01_reparar.py`, `hueco01_verificar.py` y `hueco01_vistas.py`. No repetir la reparación sobre el resultado existente.
