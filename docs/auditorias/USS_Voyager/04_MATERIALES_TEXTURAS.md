# Materiales, texturas, UV y diagnóstico del blanco

## Respuesta verificada por archivo

| Familia/archivo | Imágenes | Estado real | Conclusión |
|---|---|---|---|
| Colección GLB | 0 | 8 materiales con factores constantes; no hay references de textura | El blanco está en el activo; no es una descarga fallida de imágenes |
| Colección BLEND | 0 imágenes de archivo | 8 materiales usados + Material sin uso; nodos Normal Map sin imagen de entrada | El original nativo tampoco aporta texturas ocultas |
| OBJ + VoyagerB.Mtl vigente | 49 imágenes referenciadas por 50 mapas | Todas las rutas activas resuelven en ubicación original | Recuperable; conservar dependencias juntas |
| Voyager_Bridge_Trabajo.blend | 49 imágenes de archivo | Rutas relativas válidas EN SU UBICACIÓN ORIGINAL; no empaquetadas | Transportar el BLEND solo rompería dependencias |
| Voyager_Bridge_Trabajo.glb | 49 embebidas / 50 texturas | 49/49 decodificadas; sin referencias externas | Referencia visual autocontenida útil |
| Voyager_Bridge_MAX_Trabajo.blend | 49 declaradas + 2 visores internos | Rutas rotas en Recovery; 90 materiales de piezas MAX sin nodo de imagen | No confundir imágenes del OBJ heredado con materiales MAX texturizados |

La colección tiene `FrontColor` blanco por defecto ([1,1,1,1]), `cTerminal` negro, grises `Airway___Upper_Struts`, `Ground_Skirting___Lighting`, `Upper_Border___Lower_Recess`, rojo oscuro `Light_Detailing`, amarillo `Color_E01` y cian `Color_H04`. Todos declaran metallic=0, roughness=0,552786 y doubleSided=true. No hay COLOR_0, mapa normal, AO, rugosidad, metallic, emisión ni extensión unlit. Son materiales compatibles con el esquema metallic-roughness, pero **sin arte PBR de superficie**. La mayor parte del puente usa exclusivamente FrontColor. Los nombres «Lighting» no convierten esas caras en luz.

## Recuperación de la familia detallada

Las 49 imágenes embebidas del GLB detallado se leyeron desde sus bufferViews BIN y se decodificaron con Pillow. La lámina `CAPTURAS/texturas_embebidas_OBJ.png` muestra sus píxeles reales: LCARS, placa, metal, cuero y tejido. No se generó ni sustituyó ninguna textura. El color magenta observado en algunas superficies tampoco prueba un mapa perdido: existe, por ejemplo, el material constante `wire_138008110` con BaseColor≈(0,541; 0,031; 0,431), sin imagen. Los renders Cycles usan los shaders originales importados, sin reparación.

El GLB detallado tiene 102 materiales y solo mapas **BaseColor** (50 referencias, 49 imágenes). No hay mapas normal/roughness/metallic/AO ni emisión configurada. Incluye `KHR_materials_specular`; el detalle de factores está en [DATOS/materiales_gltf.csv](DATOS/materiales_gltf.csv). Todas las 102 emisiones importadas tienen Strength=0. Por ello el interior cerrado, con luz diagnóstica exterior, aparece oscuro: una imagen LCARS legible no implica un panel luminoso. Se añadió una luz temporal interior exclusivamente para inspección y se guardaron ambas vistas. El ruido de 64 muestras no está suavizado ni ocultado con denoise.

El MTL vigente tiene 102 materiales, 50 mapas activos y **0 rutas activas rotas**. El MTL histórico tiene 58 mapas activos, **48 referencias que no resuelven**. El informe de reparación previo registra sustituciones nominales de pantallas; eso no certifica que sean exactamente el arte original de cada estación. No se aplicó ninguna reparación nueva. Tampoco se interpreta el MTL anterior como una versión de geometría.

En `Recovery/originales` hay 104 imágenes externas sanas, y en la carpeta del Escritorio 102. Las **206/206** se decodificaron. Hay candidatos locales por nombre normalizado para las 49 imágenes del BLEND Recovery; las diferencias de punto/guion bajo no se deben resolver a ciegas. El CSV de candidatos señala solo semejanza nominal, **no garantiza asignación semántica**. El MC6 y los mapas `VP_col`, `VP_bump`, `VP_Spec`, imágenes `_i`, etc., son fuentes de conciliación, no un material UE5 listo.

El BLEND Recovery contiene 171 materiales totales, pero 90 con caras asignadas a las mallas MAX; todos esos 90 carecen de nodos TEX_IMAGE. Otros materiales/nodos pertenecen al OBJ antiguo que comparte la escena. Las 49 rutas de archivo del BLEND fallan en la ubicación original de Recovery. No se confunden esos fallos con los que provoca copiar un BLEND sin dependencias: para `Voyager_Bridge_Trabajo.blend`, se resolvieron también las rutas contra la carpeta original y allí las 49 existen.

## UV y trabajo artístico real

- Colección GLB: **317/317 primitivas con UV0**; sin otro canal y sin colores de vértice. Todas las mallas importadas tienen coordenadas fuera del cuadrado 0–1: eso puede ser tiling válido, no demuestra UV rota. Hay 183 triángulos UV de área próxima a cero. La colección BLEND tiene 83/83 mallas con un canal UV; sus polígonos se triangulan de otra manera y dan 996 degeneraciones UV por ese método.
- OBJ separado: **630/630 mallas con UV0**. Permite conservar la colocación de las imágenes existentes. La versión fusionada y el GLB no aportan otro UV para lightmap. Raw GLB mide 11.919 UV degeneradas; la triangulación/precisión de Blender da 11.921. No hay certificado de atlas sin solapes o densidad de texel uniforme.
- Recovery: 591/632 mallas con UV; las 41 sin UV pertenecen al conjunto MAX. Ese conjunto tiene 590/631 con UV, y el OBJ heredado añade una más. Los objetos que no tengan UV y requieran imágenes nuevas necesitarán despliegue; para materiales constantes no es obligatorio.
- Los recuentos de triángulos UV repetidos son solo detección de coincidencia exacta; **no se ejecutó un solver exhaustivo de solapes ni una medición de estiramiento/texel density**. Es incorrecto decidir «rehacer todas las UV» o «todas listas» con esta evidencia.

## Clasificación de la evidencia

| Estado solicitado | Resultado |
|---|---|
| Existentes utilizables | 49 imágenes embebidas y 206 externos físicos decodificados; no todos son diseños únicos |
| Presentes mal vinculadas | Imágenes declaradas por el BLEND de Recovery; sus materiales MAX además carecen de enlaces de imagen |
| Dañadas/incompatibles | Ninguna imagen probada falló; compatibilidad artística PBR y de importación no está certificada |
| Materiales que requieren reconstrucción | MAX: 90 materiales de piezas. OBJ/GLB: tratamiento PBR y emisión, no recuperación desde cero de toda textura |
| Superficies sin texturas con UV | Colección 317 primitivas; la existencia de UV no garantiza unwrap artístico aprovechable completo |
| Nuevo unwrap necesario | 41 mallas MAX sin UV si se decide texturizarlas; zonas UV degeneradas que deban recibir mapas nuevos |

La causa de ver **todo** blanco en un visor particular podría además ser su modo Solid/material override; ese visor no se inspeccionó en vivo. Sí se ha probado que el archivo de colección ya carece de imágenes y que el puente detallado texturizado renderiza con sus mapas en Blender. No se atribuye el problema a Blender ni al importador de Unreal sin una prueba que lo demuestre.

Referencia para defaults de factores y atributos: [especificación glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html). Valores y enlaces concretos: JSON locales y CSV de esta auditoría.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
