# Datos de diagnóstico publicados

Todos son metadatos o resultados numéricos de solo lectura. No contienen modelos, imágenes, coordenadas por vértice, índices de malla ni píxeles. Los alias de origen se explican en el [README](../README.md#alias-de-origen). Las áreas y cajas no sustituyen las pruebas de cápsula. Para la interpretación y umbrales, consultar [geometría](../03_GEOMETRIA.md), [materiales](../04_MATERIALES_TEXTURAS.md) y [método](../09_METODO_FUENTES_LIMITACIONES.md).

| Archivo | Contenido |
|---|---|
| [aprovechamiento.csv](aprovechamiento.csv) | Matriz A–E por componente |
| [archivos_zip.json](archivos_zip.json) | Archivo del ZIP y hash para demostrar copia idéntica |
| [capturas_solo_local.csv](capturas_solo_local.csv) | 55 capturas: nombre, hash, resolución y motivo de retención |
| [capturas_solo_local.json](capturas_solo_local.json) | 55 capturas: nombre, hash, resolución y motivo de retención |
| [componentes_blend.csv](componentes_blend.csv) | 83 piezas del nativo de colección: áreas, envolventes, materiales y conteos |
| [componentes_obj_split.csv](componentes_obj_split.csv) | 630 grupos recuperados del OBJ: áreas, cotas, UV descritas en informe |
| [componentes_obj_work.csv](componentes_obj_work.csv) | OBJ fusionado de trabajo |
| [componentes_recovery.csv](componentes_recovery.csv) | Conversión MAX + OBJ heredado; no sumar como un único puente |
| [conteos_validacion_importacion.json](conteos_validacion_importacion.json) | Diferencias crudo/importado explicadas por tripletas duplicadas |
| [deep_blend.json](deep_blend.json) | Áreas, rayos de pasillo, piezas conectadas y resumen de coincidencias |
| [deep_obj_split.json](deep_obj_split.json) | Metadatos por grupo separado y resumen de coincidencias |
| [deep_obj_work.json](deep_obj_work.json) | Metadatos del objeto fusionado y resumen de coincidencias |
| [deep_recovery.json](deep_recovery.json) | Áreas, suelos y resumen de coincidencias; sin triángulos originales |
| [fuentes_documentales.json](fuentes_documentales.json) | Fuentes leídas y hashes, con rutas lógicas |
| [gltf_validacion_numerica.json](gltf_validacion_numerica.json) | Accesores: resultados de índices, áreas, UV y normales, sin su contenido geométrico |
| [hallazgos.csv](hallazgos.csv) | Problema, evidencia, gravedad, consecuencia, solución propuesta y grado |
| [hallazgos.json](hallazgos.json) | Problema, evidencia, gravedad, consecuencia, solución propuesta y grado |
| [integridad_final.json](integridad_final.json) | Relectura original: 230 entradas; detalle Voyager con rutas lógicas |
| [inventario_archivos.csv](inventario_archivos.csv) | Archivos Voyager con tamaño, mtime y hash; fuentes lógicas |
| [inventario_archivos.json](inventario_archivos.json) | Archivos Voyager con tamaño, mtime y hash; fuentes lógicas |
| [materiales_auditoria.json](materiales_auditoria.json) | Imágenes externas: metadatos/decodificación; referencias MTL y factores glTF |
| [materiales_gltf.csv](materiales_gltf.csv) | Factores y canales de los materiales, sin mapas de píxeles |
| [obj_estructura.json](obj_estructura.json) | Grupos, materiales, envolvente y conteos del OBJ, sin vértices |
| [recovery_candidatos_imagen.csv](recovery_candidatos_imagen.csv) | Coincidencias nominales; no certifica asignación semántica |
| [resumen_modelos.json](resumen_modelos.json) | Recuentos de las seis variantes inspeccionadas |
| [texturas_externas.csv](texturas_externas.csv) | Dimensiones, hash y resultado de decodificación; no contiene texturas |
| [verificacion_entrega.json](verificacion_entrega.json) | QA de la auditoría local, no prueba de imágenes publicadas |
