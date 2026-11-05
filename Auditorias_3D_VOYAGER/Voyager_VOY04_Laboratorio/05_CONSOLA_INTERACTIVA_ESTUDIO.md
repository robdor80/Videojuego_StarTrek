# VOY-04 — Estudio de la consola y futura interacción

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Piezas reales

Object_129 es la carcasa principal asociada a navegación; Object_126/127 y remates vecinos completan el contexto. No se incluyeron en el grupo móvil de la silla. Las superficies principales Plane_94 y Plane_95 son objetos de pantalla independientes con `scrn10_3` y `scrn10_4`. Plane_96, Plane_139, Plane_138 y Plane_140 son pantallas laterales vecinas; no se declara alcanzable su superficie completa.

Las botoneras LCARS son gráficos de las texturas originales, no cientos de botones geométricos. Los marcos, carcasa y algunas molduras son geometría independiente. Las zonas luminosas siguen usando sus materiales/nodos de origen. Las 49 imágenes permanecen empaquetadas y las UV/materiales de las copias están verificadas; no se han sustituido gráficos ni creado PBR definitivo.

| Pantalla | Material | Desviación máxima de planitud | Centro local (m) |
| --- | --- | --- | --- |
| Plane_94 | scrn10_3 | 1.94 µm | 0.229, 0.492, 0.273 |
| Plane_95 | scrn10_4 | 2.12 µm | -0.249, 0.483, 0.273 |
| Plane_96 | scrn10_5 | 17.69 µm | -0.740, 0.290, 0.393 |
| Plane_139 | scrn10_2 | 0.85 µm | 0.757, 0.386, 0.272 |
| Plane_138 | scrn10_1 | 248.94 µm | 1.189, 0.203, 0.272 |
| Plane_140 | scrn10_6 | 318.90 µm | -1.193, 0.173, 0.274 |

Las dos pantallas centrales no forman exactamente un único plano. Cada superficie debe conservar su propia normal, contorno y UV. La carcasa es abierta/no manifold en este recurso: no se deduce volumen sólido o hueco útil a partir de una AABB. Los datos de planitud no convierten toda la consola en una pantalla plana.

## Preparación entregada

En cada escena 04 se guardaron anclajes de aproximación, cadera sentada, dos manos y punto de interacción, además de una cámara ampliada. `marcadores_interaccion.json` contiene posiciones locales/mundiales y matrices; `consola_superficies.json` contiene normales y planos. Se comprobó que añadir los anclajes no alteró las mallas. Son referencias geométricas, sin eventos de juego.

Una futura superficie dinámica puede reutilizar cada objeto de pantalla y sus UV0. La prueba de manos utiliza puntos interiores a y=0,405 m y x=±0,16 m del marco diagnóstico, con el extremo de la envolvente a 2 mm de su plano. Los hombros alcanzan esos puntos en las tres tallas. La cámara ampliada se orienta al centro de ambas pantallas; no constituye una cámara final de lectura aprobada ni garantiza que el FOV sea cómodo para todos los jugadores.

El futuro ratón podrá consultar la intersección sobre cada superficie y convertirla a sus UV; mandos y accesibilidad necesitarán una modalidad de foco/selección propia. La función, distribución de controles, Widgets, Render Targets, navegación de UI y enlace CoreRPG no están implementados. No se modificó el proyecto Unreal.

## Rodillas, manos y visión

Tras bajar la silla, la holgura mínima calculada de miembros de pierna frente a las tres carcasas ensayadas es aproximadamente 17,7 / 12,6 / 7,7 cm para 1,60 / 1,75 / 1,90. Esto describe la pose de trabajo concreta y esas carcasas; no es una envolvente universal para animaciones futuras. El canto bloqueó la trayectoria directa de manos y sigue siendo un obstáculo real en la versión final.

Los centros Plane_94/95 son visibles por rayo desde cada ojo estimado; quedan pendientes todo el campo visual, oclusión de manos, tipografía, reflejos, contraste y lectura desde la postura alta. No se cambia la inclinación ni altura de la consola para resolverlo en esta fase.

![LCARS originales, render de inspección](CAPTURAS/D04_LCARS_ORIGINALES.png)
