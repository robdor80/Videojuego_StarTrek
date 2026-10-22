# Inventario y procedencia

Se inspeccionó la biblioteca `BIBLIOTECA_3D` (1.321 archivos enumerados; no se recorrió `.git`). La ruta histórica existe. La ruta facilitada es la ubicación actual normalizada de la colección; las fichas antiguas conservan una ubicación anterior que ya no existe. Se consultaron metadatos de `StarTrek_3D_Library/03_METADATA`, que señalaron la carpeta concreta del Escritorio; no se escaneó todo el disco.

## Modelos, fuentes y derivados reales

| Ruta | Formato | Bytes | SHA-256 |
|---|---|---|---|
| `star-trek-voyager-collection.zip` (fuente local: `BIBLIOTECA_3D/assets/otros/corridor/Star Trek Voyager Collection/voyager/coleccion_de_pasillos_voyager/star-trek-voyager-collection.zip`) | .zip | 7876154 | e9da08c7b504892ddc6d17fd8542f365aedf67daaccab33050b125ca9ffcc28d |
| `star_trek_voyager_collection.glb` (fuente local: `BIBLIOTECA_3D/assets/otros/corridor/Star Trek Voyager Collection/voyager/coleccion_de_pasillos_voyager/star_trek_voyager_collection.glb`) | .glb | 4262160 | d1bbe6dabb81327eae77bfdb3d8f170773086f137177d03ef5e7d3a5e87fcbb8 |
| `StarTrekVoyagerCollection.blend` (fuente local: `BIBLIOTECA_3D/assets/otros/corridor/Star Trek Voyager Collection/voyager/coleccion_de_pasillos_voyager/star-trek-voyager-collection/source/StarTrekVoyagerCollection.blend`) | .blend | 7875980 | 22a5744ee57f74a02e43798d5d9e8841cca00dbdde3660befde6cf25ccb88992 |
| `Voyager Bridge Max2011.max` (fuente local: `FUENTE_MAX/Voyager Bridge Max2011.max`) | .max | 19895548 | 4b06036b6b5fc48d2a0c4859f322065c24275aea2b774917853981928e35a867 |
| `Voyager Bridge.mc6` (fuente local: `FUENTE_MAX/Voyager Bridge.mc6`) | .mc6 | 941261 | dadf3052ad4c530ba8e815ad4e6455ca383585b401e5e08fc4087092959e7b84 |
| `Voyager_Bridge_MAX_Trabajo.blend` (fuente local: `FUENTE_MAX/Voyager_Bridge_MAX_Trabajo.blend`) | .blend | 15591461 | 912ee7f0b7ffb15517a8fc5b7d5c08b439c1b4ae733e263fd257cd79fffc51ac |
| `Voyager Bridge.obj` (fuente local: `FUENTE_OBJ/Voyager Bridge.obj`) | .obj | 37746664 | 5e2df918e3837fbb30b70efbdedeb423cac8d29dcd9d6c33ac77cc304351581d |
| `VoyagerB.Mtl` (fuente local: `FUENTE_OBJ/VoyagerB.Mtl`) | .mtl | 17437 | 0ab640506a753a678419110d4d9e1f6b0f0e3cb8461f5cdea47f52d16d2a2325 |
| `VoyagerB_original.Mtl` (fuente local: `FUENTE_OBJ/VoyagerB_original.Mtl`) | .mtl | 14246 | 278205f875f51ca73596583ac4f01b79ef83f07cba66d0251800349d74b1c3b7 |
| `Voyager_Bridge_MAX_Trabajo.blend` (fuente local: `FUENTE_OBJ/Voyager_Bridge_MAX_Trabajo.blend`) | .blend | 15591461 | 912ee7f0b7ffb15517a8fc5b7d5c08b439c1b4ae733e263fd257cd79fffc51ac |
| `Voyager_Bridge_Trabajo.blend` (fuente local: `FUENTE_OBJ/Voyager_Bridge_Trabajo.blend`) | .blend | 9728783 | 668989aa67fbbdc40e0b4e8e197be429a504009360086cc23a8fd24b323b8ac1 |
| `Voyager_Bridge_Trabajo.glb` (fuente local: `FUENTE_OBJ/Voyager_Bridge_Trabajo.glb`) | .glb | 24583620 | b35de63e03d7a719558b316889acae35b64c947b2566f6bfe944b9f02d171e96 |

La copia MAX editable del Escritorio y la de `Voyager_Bridge_Recovery/originales` tienen **el mismo SHA-256**. El ZIP de la colección contiene únicamente `source/StarTrekVoyagerCollection.blend`; su hash coincide con el `.blend` extraído. No son versiones adicionales independientes.

## Materiales y dependencias

- Colección: `.glb`, `.blend`, ZIP, README y metadata.json; no aparecen imágenes en esa carpeta ni dependencias de imagen en ambos modelos.
- Puente detallado del Escritorio: OBJ, MTL vigente, MTL anterior, informe de reparación, dos BLEND y GLB; **102 archivos de imagen** externos, todos decodificados. El OBJ declara `mtllib VoyagerB.Mtl`.
- Recovery: MAX de 2011, MC6, BLEND de conversión y **104 imágenes**, todas decodificadas. Hay candidatos por nombre para las 49 imágenes declaradas en el BLEND, pero las rutas originales de ese BLEND apuntan a `VOYBRIDGETEX-1/Textures`, carpeta inexistente dentro de Recovery. Sus imágenes actuales están en `VoyagerBridge`.
- En los dos directorios hay 206 imágenes externas contadas como archivos físicos, no 206 diseños únicos. El GLB detallado embebe 49 imágenes y crea 50 referencias de textura.

[DATOS/inventario_archivos.csv](DATOS/inventario_archivos.csv) publica metadatos de 221 archivos Voyager. La auditoría local incluyó 230 entradas; los metadatos de archivos Sutherland se excluyen de esta publicación por ser ajenos a su alcance documental. [DATOS/texturas_externas.csv](DATOS/texturas_externas.csv) enumera tamaños, resoluciones, hashes y decodificación. No se encontraron otras versiones Voyager en la biblioteca histórica por nombre/ruta y fichas consultadas; no se afirma que no existan bajo otros nombres en ubicaciones ajenas al alcance.

## Referencias históricas que no equivalen a recursos actuales

Los JSON de `StarTrek_3D_Library/03_METADATA` mencionan descargas `star_trek_-_intrepid_type`, `uss_voyager_4k_textures_star_trek_intrepid` y `voyager_ncc_74656` en Downloads; esas rutas exactas no existen. Son referencias de nave exterior o de identidad no comprobada, no puentes adicionales auditados. Las carpetas `01_BLENDER` y `02_GAME_READY` consultadas no aportaron modelos Voyager físicos.

El GLB de colección declara internamente autor `scrimshawsean`, título `Star Trek Voyager Collection`, generador `Sketchfab-12.68.0` y licencia CC-BY-4.0. Son **metadatos declarados en el archivo**, no una verificación externa de licencia ni de derechos de franquicia. La familia OBJ/MAX no se atribuye al autor de la colección.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
