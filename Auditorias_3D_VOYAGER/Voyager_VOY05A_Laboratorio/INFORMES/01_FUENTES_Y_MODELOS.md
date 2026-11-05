# VOY-05A — Fuentes y modelos

Las rutas indicadas en el encargo existen. Se copiaron físicamente al laboratorio; `VERIFICACION/originales_antes.json` registra **221 archivos** (modelos, materiales, texturas, ZIP y auxiliares). Las copias utilizadas están en `FUENTES/PUENTE`, `FUENTES/COLECCION` y `FUENTES/RECOVERY`. El `.max` original se conserva y se identifica, pero no se abrió con 3ds Max: se inspeccionó su conversión Blender disponible. Ese límite se mantiene expresamente.

| Recurso analizado | Mallas | Triángulos | Sistema | scale_length |
| --- | --- | --- | --- | --- |
| coleccion | 83 | 71738 | METRIC | 1.0 |
| coleccion_glb | 317 | 67548 | METRIC | 1.0 |
| puente_blend | 1 | 271705 | METRIC | 1.0 |
| puente_glb | 1 | 271705 | METRIC | 1.0 |
| puente_max | 631 | 533138 | METRIC | 1.0 |
| puente_max_desktop | 631 | 533138 | METRIC | 1.0 |
| puente_obj | 630 | 271705 | METRIC | 1.0 |

El nativo de colección es `star-trek-voyager-collection/source/StarTrekVoyagerCollection.blend`, localizado dentro de la ruta orientativa. GLB y nativo son vistas de la misma colección, con diferencias que se cuantifican en `DATOS/contraste_formatos_actual.json`; las particiones GLB se tratan como materiales, no habitaciones nuevas. El puente OBJ conserva 630 mallas; el Blend de trabajo y el GLB del escritorio reducen el conjunto a una. Se usa OBJ para trazabilidad de hojas.

MAX y OBJ no se declaran copias geométricas perfectas: tienen diferencias reales de conversión, colocación o contenido. La afinidad histórica MAX≈OBJ×1,50813535+traslación se vuelve a comprobar como hipótesis, no calibración física. Véase `DATOS/max_residuos_por_objeto.json`. No se suman automáticamente accesos del MAX como instancias adicionales; los seis grupos de hojas se contrastan mediante nombres, posición y el mapa VOY-02.

Se consultaron informes originales VOY-01/02/03/04 y los informes Sutherland de puertas F07-P02/P03C/P03D/P03E/P03F/P03G disponibles. Sus copias están en `REFERENCIAS`; los hashes de los documentos leídos están en `VERIFICACION/referencias_antes.json`. Las escenas antiguas y los proyectos Unreal no se abrieron ni se guardaron. Los resultados de movimiento de VOY-02 y Sutherland se atribuyen a sus informes; no son pruebas nuevas de VOY-05A.

Disponibilidad: rectos, curva 90°, desvíos T y cuatro vías, Y Mesh2, conectores quebrados Mesh52/80, cabina Mesh17, accesos Mesh37/42/94, envolventes de habitaciones y salas, conductos y mantenimiento. No se acredita una biblioteca de camarotes terminados, zonas técnicas equipadas completas ni mecanismos de puerta. La asignación canónica de cada sala queda pendiente. En `14_CATALOGO_COBERTURA.md` se documentan las 83 piezas, incluidas las que no aportan un acceso aceptado.
