# Sala de la supercomputadora — Enterprise-G, clase Valhalla

Fecha: 1 de noviembre de 2026. **Estado: PARCIAL.** Entrega de construcción conservadora para revisión independiente, pendiente de resolver contactos con la estructura y de validar colisiones y navegación en Unreal Engine 5.

## Resumen ejecutivo

Se han reconstruido e integrado **dos conjuntos circulares de bancos**, cada uno con cuatro sectores y sus pasos radiales abiertos. Escala de integración **1:1**, sin estirar consolas ni pantallas. Los originales Blender y SketchUp permanecen intactos. Se han recuperado los colores de sombreado y tres imágenes originales desde SketchUp, sin materiales PBR inventados.

La integración abre correctamente, conserva los 1.407 objetos originales y añade 15.392 objetos de banco con mallas compartidas. Las 136 mallas originales conservan exactamente sus coordenadas, índices de vértices de los polígonos, asignación material por polígono y UV. No se ha recortado ni eliminado arquitectura para ocultar conflictos. Las secciones muestran contactos pendientes: esta entrega **no acredita ausencia de interpenetraciones**, estanqueidad de todas las mallas ni jugabilidad completa.

## Fuentes y protección

Directorio local de fuentes y entregables, relativo a la raíz del repositorio:

`PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/`

| Original | SHA-256, verificado tras la entrega |
| --- | --- |
| `Sala computadora completa (con circulos vacios).blend` | `97723d2b98a919ab051ff39a74f31c6a547c2147c91731d737938ddbc6ba7ea9` |
| `Sala computadora completa (con circulos vacios).skp` | `4d9d6566d40be21cc8aa5908d20d434ae452e90d84dad316ecaf12529112e815` |
| `Semicirculo_computadora.blend` | `07819bf5a08bc57c0286daf6c4471431fae37dbc3db0d14f4c716658ebcda71d` |
| `Semicirculo_computadora.skp` | `3c58332d4aad3d369f807292bf2faa84a1ded1f5cc04eef3794e5257083cc9b5` |

Se trabajó mediante lecturas de las fuentes y copias nuevas. No se sobrescribieron los originales, proyectos UE, texturas base ni respaldos. No se borró material anterior.

Blender utilizado: **5.2.2 LTS**, compilación `d13f752e3b9c`. Ambos modelos utilizan unidades métricas, `scale_length = 1`; las medidas siguientes son metros y consideran `matrix_world` de las instancias evaluadas. Las mallas de definición, excluidas de la vista, no son posiciones ensambladas. No hay modificadores en las fuentes.

| Inventario Blender | Sala original | Semicírculo original |
| --- | ---: | ---: |
| Objetos de escena | 1.407 | 4.139 |
| Mallas de definición | 136 | 38 |
| Empties / instancias organizativas | 1.269 | 4.099 |
| Colocaciones evaluadas con caras | 920 | 3.855 |
| Vértices evaluados, incluyendo repeticiones de instancia | 622.293 | 4.231.682 |
| Materiales | 75 | 36 |
| Mallas con UV | 90 | 26 |

Las colecciones originales `ROOT_MODEL`, `Layer0`, `Component#…`, fuentes geométricas y `DECK 00 DOOR 00` se mantienen. Las fuentes contienen una cámara y una luz cada una. Se preservan las relaciones originales de instanciación de la sala; los bancos nuevos usan objetos de malla con datos compartidos, separados por recinto y mitad.

## Referencia aportada: cubierta 11 de la NCC-1701-D

Archivo original local:

`PROYECTO VALHALLA/Blueprints/NCC1701D/star-trek-the-next-generation-enterprise-sheet-8.jpg`

La lámina 8 contiene la cubierta 10 a la izquierda y la cubierta 11 a la derecha. Se inspeccionó la **mitad derecha**, incluida la región central y la llamada `MAIN COMPUTER CORE (P/S)`. La organización de los dos recintos circulares, sus sectores radiales, la zona intermedia y las conexiones hacia los corredores aporta una referencia topológica coherente con la sala 3D.

La comparación visual justifica conservar los pasos radiales y el bloque de conexión: completar los bancos no significa cerrar esos pasos con un anillo macizo. Los círculos pequeños del modelo cumplen una función de vestíbulo y no se rellenaron con bancos. La orientación «superior/inferior» de este informe describe la vista del modelo, sin fijar todavía ejes navales para la Valhalla.

La imagen contiene escala gráfica, pero no se realizó calibración métrica, registro de píxeles contra el 3D ni verificación individual de cada símbolo de puerta. Por tanto, la lámina no se utilizó para redimensionar la Valhalla ni se declara equivalencia exacta entre ambas naves. Su función en esta entrega es revisar estructura y conectividad; la comprobación dimensional sigue sustentada en los modelos.

SHA-256 del blueprint, conservado intacto: `9389ef8e391fbbb5548f71324cf4388d4a49be0eda141415fb4cc4a602a2d0d1`.

## Inventario de emplazamientos y dimensiones

Se identificaron **dos recintos grandes**, del mismo tamaño de implantación, y **dos vestíbulos circulares pequeños** conectados con el bloque central. Se integró un conjunto en cada recinto grande; no se duplicaron bancos en los vestíbulos, corredores ni en el bloque rectangular.

Los siguientes centros son los del maestro normalizado por la envolvente de los bancos; no se tomaron los orígenes arbitrarios de los objetos como centros de círculo.

| Elemento | Centro X | Centro Y | Cota de apoyo Z | Escala adicional |
| --- | ---: | ---: | ---: | ---: |
| Banco circular superior | 22,684833 | 14,314360 | 0,370000 | 1,000000 |
| Banco circular inferior | 22,684834 | -19,261851 | 0,370002 | 1,000000 |

| Medida del maestro reconstruido | Valor |
| --- | ---: |
| Envolvente exterior X | 19,556940 m |
| Envolvente exterior Y | 19,510550 m |
| Altura de los bancos | 3,316350 m |
| Cota inferior integrada | 0,370000 m |
| Cota superior integrada | 3,686354 m |
| Diámetro de envolvente radial exterior máximo | 19,716455 m |
| Diámetro de exclusión radial interior mínimo | 4,931834 m |

Los diámetros radiales describen extremos de vértices respecto al centro de referencia; no son un ajuste analítico de una circunferencia lisa. Las medidas X/Y difieren 46,390 mm, alrededor del 0,24 %. Se conserva la poligonización y el diseño ligeramente irregular de la fuente; no se ha aplicado una deformación anisótropa para fingir igualdad de diámetros. La adecuación de esa irregularidad a una circunferencia matemática perfecta queda pendiente de revisión geométrica.

El techo original contiene geometría entre Z=3,49635 y 3,69635 m y las tapas de banco alcanzan Z=3,68635 m. Esa superposición de rangos exige revisar el encuentro tapa/techo cara por cara. No se acredita una holgura positiva de techo por comparar solamente cotas máximas.

## Reconstrucción, simetría y alineación

Se identificaron **3.848 colocaciones de banco** por semicírculo. Se excluyeron de la extracción `ROOT_MODEL`, `Component#200`, `Component#58`, `Component#202` e `Image`: corresponden a arquitectura, cubierta, conexión y referencia plana. Esos elementos permanecen en las copias recuperadas de las fuentes; no se insertaron otra vez sobre la sala.

El plano de reconstrucción es **X=11,870779991 m** en el semicírculo de origen. Se conserva una mitad y se obtiene la otra mediante `x' = 2·11,870779991 - x`. El origen editable del maestro es `(11,870779991; 16,047512054; 0,370000005)` antes de normalizarlo a `(0;0;0)`.

Se conservan las cuatro aberturas radiales y la zona central. No se soldaron a través de pasos funcionales ni se unieron indiscriminadamente las mallas. Cada círculo contiene **7.696 objetos**, con datos de malla reutilizados. No se detectaron colocaciones de origen exactamente duplicadas según malla y matriz redondeada a siete decimales.

Para las reflexiones se genera una variante de malla reflejada y se invierte el orden de sus caras; la transformación de objeto resultante tiene determinante positivo. La validación independiente encontró **cero transformaciones negativas** entre los bancos integrados. Esto verifica la compensación del espejo, pero no acredita que todas las normales heredadas de SketchUp sean correctas ni que las superficies sean cerradas.

La implantación se calcula por consenso de desplazamientos entre vértices arquitectónicos de la cubierta (`Component#58` de la fuente y `Component#194` de la sala), seguido de refinamiento mediante correspondencias próximas.

| Recinto | Operación sobre coordenadas originales de la fuente | Coincidencias | Error máximo de las coincidencias |
| --- | --- | ---: | ---: |
| Superior | `(x+10,814052582; y-1,733152390; z)` | 125/128 | 0,000002133 m |
| Inferior | `(x+10,814053535; -y-3,214339018; z+0,000001907)` | 125/128 | 0,000002959 m |

Los tres puntos no coincidentes pertenecen al borde del corte de la cubierta del semicírculo, excluida de los bancos insertados. Su discrepancia máxima es aproximadamente 0,311 m; no se ha ocultado ese resultado ni se ha deformado la sala para ajustarlos. La transformación inferior necesita reflexión Y para orientar la conexión hacia el bloque central. Todas las escalas adicionales son uniformes e iguales a 1; no se generaron variantes de tamaño innecesarias.

Colecciones nuevas: `VALHALLA_BANCOS_MAESTRO`, `Semicirculo_A_Original`, `Semicirculo_B_Espejo`, `VALHALLA_BANCOS_INTEGRADOS`, `Banco_Circular_01` y `Banco_Circular_02`.

## Puertas, accesos e interferencias

Los **1.407 objetos originales** están presentes con sus transformaciones originales, incluidos puertas, componentes de puerta, estructura y conexiones. Se compararon hashes de las **136 mallas originales**, incluyendo coordenadas, índices de cara, materiales por cara y UV: cero diferencias. No se borró geometría original ni se dejó una copia adicional de la arquitectura del semicírculo superpuesta.

Se cortaron las superficies trianguladas mediante planos horizontales Z=0,80; 1,50 y 2,70 m. Las alturas sobre el suelo de apoyo son aproximadamente 0,43; 1,13 y 2,33 m. Se midieron las intersecciones de las secciones y se verificaron franjas rectangulares en los pasos centrales.

| Z global | Segmentos de banco | Segmentos de arquitectura | Puntos de intersección entre secciones |
| --- | ---: | ---: | ---: |
| 0.8 m | 47872 | 19482 | 138 |
| 1.5 m | 45920 | 19176 | 138 |
| 2.7 m | 37728 | 15550 | 78 |

En ambos recintos, a las tres alturas, la franja entre bancos alrededor del eje vertical de planta mide al menos **1,04760 m** y alrededor del eje horizontal **1,04114 m**. No hay segmentos de banco dentro de las franjas ensayadas de 0,80 m y 0,40 m respectivamente, extendidas 19,6 m a lo largo de los ejes. Son medidas de separación **entre bancos**: no equivalen al ancho útil de cada puerta, pues la arquitectura original también limita el paso. No se ha validado el barrido de apertura de todas las hojas ni la envolvente de un personaje por todas las rutas.

Las intersecciones se concentran en encuentros de paneles, soportes y consolas con `Component#200` y `Component#202`. A Z=1,50 m intervienen `Component#206`, `#34`, `#13`, `#41`, `#15` y `#20` de los bancos. La fuente sin modificar ya produce **36 puntos** de intersección en esa sección. De los 138 puntos de la sala integrada, 115 están a menos de 5 mm de contactos de la fuente trasladados/reflejados; los otros 23 no quedan explicados por esa comparación. Esta tolerancia compara localizaciones de contacto, no profundidad de penetración.

**Pendiente:** clasificar y resolver cada contacto, distinguir apoyo previsto de penetración, revisar especialmente el sector reflejado y el encuentro de tapas con techo. No se aplicaron booleanos generales sobre superficies trianguladas del original: falta determinar una corrección local segura que conserve estructura, materiales y pasos. La longitud común de las secciones es cero y sus cruces son puntos; eso **no significa volumen de interpenetración cero**.

Se generaron vistas superiores de la sala, vistas isométricas, detalle del círculo y vista sin tapas, además de un diagrama de sección a Z=1,50 m (estructura oscura, bancos azules, contactos rojos). También se renderizó el semicírculo en Eevee antes/después de recuperar materiales. Las ocultaciones y cámaras de diagnóstico no se guardaron en los entregables.

## AUDITORÍA DE MATERIALES, COLORES Y TEXTURAS

### Hallazgo y causa de las superficies blancas

La sala contiene **75 materiales** y el semicírculo **36**. Todos tienen un Principled BSDF conectado a Material Output. En los originales **no hay nodos Image Texture** ni imágenes de archivo registradas; las dos entradas de imagen por archivo son `Render Result` y `Viewer Node`, que son buffers de Blender, no texturas externas ni imágenes empaquetadas.

El modo Sólido está configurado mayoritariamente con `color_type = MATERIAL`, y muestra `material.diffuse_color`. Los nodos Principled originales conservan **Base Color=(0,8;0,8;0,8;1)** y Alpha=1, independientemente del color/alpha de visualización. Esa divergencia explica que la previsualización de materiales y el render aparezcan casi blancos. No es prueba de ausencia de color ni de texturas blancas reales. Los colores de objeto no son la fuente que utiliza esa configuración de Sólido: las 136 mallas de la sala y las 38 del semicírculo tienen `object.color=(1;1;1;1)`.

La inspección del importador OpenSKP instalado muestra que busca el nodo por el nombre inglés `Principled BSDF`, mientras los archivos contienen el nombre localizado `BSDF Principista`. Esto permite que se guarde el color de visualización y se omita la asignación al shader y la creación del nodo de imagen. Es un mecanismo compatible con los datos observados; no hay registro de la importación histórica para atribuirle de forma concluyente cada pérdida. La recuperación busca el nodo por su **tipo**, independiente del idioma.

### Clasificación y recuperación

| Categoría | Sala original | Semicírculo original | Resultado |
| --- | --- | --- | --- |
| Grafo Principled → Output existente | 75 | 36 | Conservado |
| Colores básicos sin imagen según SKP | 73 materiales resueltos + `Material` | 32 materiales resueltos + `Material` | Conservados; color/alpha trasladados al shader |
| Materiales con imagen recuperable | `openskp_material_33` | `openskp_material_21`, `_22`, `_34` | Reconectados a imágenes originales |
| Nodos Image Texture en los `.blend` originales | 0 | 0 | Restaurados en las copias |
| Imágenes de archivo ausentes tras recuperar | 0 | 0 | Imágenes empaquetadas |
| Materiales con apariencia de shader incompleta en la importación | Colores/alpha distintos del shader por defecto | Colores/alpha distintos del shader por defecto | Corregida la divergencia mínima |

Se comprobaron todos los índices de material resuelto y los cuatro valores RGBA contra el SKP: coincidencia dentro de 0,00001 antes de cualquier corrección. Se preservan nombres, ranuras y asignaciones por cara, rugosidad y metálico existentes; no se reemplaza la biblioteca por materiales genéricos. El material estándar `Material` permanece como material de reserva. Se conserva la transparencia original, con método Dithered cuando corresponde.

| Imagen original | Fuente | Materiales | Dimensiones | Destino |
| --- | --- | --- | --- | --- |
| `Wood_Cherry_Original.jpg` | SKP de la sala | `_33`, `Component#30` | 256×256 | Empaquetada en copia recuperada y sala integrada |
| `Fencing_Diamond_Mesh.png` | SKP del semicírculo | `_21`, `_22`, `Component#17` | 117×56 | Empaquetada en maestro y sala integrada |
| `núcleo.png` | SKP del semicírculo | `_34`, `Image` | 2262×1555 | Empaquetada en la copia de fuente; referencia plana excluida de los bancos |

El SKP conserva para la última imagen una ruta antigua de otro equipo, `C:\Users\user\Desktop\núcleo.png`; no se necesita ese archivo externo porque los bytes se recuperaron del propio SKP. Se buscó también en las carpetas locales: existe una copia de `Wood_Cherry_Original.jpg` bajo los recursos de Two Forward y su SHA-256 coincide con la imagen extraída (`6e3bbe69e0d99af013000cba499f3fc33098f7ad69748e44ce7769132838d98c`). No se inventaron las imágenes restantes.

Las 90 mallas con UV de la sala y las 26 del semicírculo contienen coordenadas finitas y más de dos valores distintos. Los tres objetos que necesitan imagen tienen UV utilizables. `Image` tiene UV 0…1; `Component#17` conserva valores de repetición muy amplios, hasta aproximadamente 6.608,71. Tener UV no prueba que sean adecuados para lightmaps o PBR: esa densidad y repetición necesitan revisión artística y técnica posterior.

Los `.blend` finales no tienen bibliotecas externas enlazadas. Todas sus imágenes de archivo están empaquetadas y las rutas son `//nombre_de_imagen`, sin depender de archivos de evidencia. La sala integrada contiene **101 datablocks de material** y dos imágenes funcionales; la imagen plana de referencia y materiales sin uso en los bancos siguen conservados en la copia de fuente, no se añadieron como decoración a la sala.

### Valor técnico de SketchUp

Se utilizó **OpenSKP 1.3.0**, ya suministrado por la extensión local de Blender. No se instaló ni modificó ningún complemento. Las dependencias incluidas se cargaron en un directorio aislado de evidencia; no son necesarias para abrir los entregables.

El SKP de la sala declara versión `{21.0.0}`, 244 definiciones, 4 capas y 68 materiales fuente, que se resuelven en 74 variantes por cara/contexto. El semicírculo declara 34 definiciones, 1 capa y 24 materiales fuente, resueltos en 35 variantes. Blender añade el material estándar en ambos casos. La comparación resuelta de colores/índices es exacta dentro de la tolerancia indicada. Los límites globales del SKP difieren ligeramente de los de Blender (centímetros en algunos extremos); no se acredita conversión geométrica perfecta de todos los componentes.

Los SKP aportan **información adicional decisiva**: las tres imágenes originales y su correspondencia material, además de definiciones y capas. No fueron meras copias redundantes. No se reimportó indiscriminadamente toda la arquitectura sobre la sala ni se modificaron los SKP.

### Materiales pendientes y futura fase PBR

La recuperación mínima de color, alpha e imágenes está realizada. Quedan fuera de esta fase los nuevos mapas PBR, suciedad, desgaste, iluminación definitiva, emisión calibrada de pantallas, detalle normal/roughness/metalness y revisión estética de transparencias. Se recomienda trabajar sobre copias de los materiales existentes, conservar nombres e identidad visual, separar UV de textura y lightmap, revisar densidad texel/repetición de la malla metálica y validar el resultado con iluminación y exposición de UE5. No se han inventado mapas PBR.

### Inventario completo de materiales originales

Cada fila identifica el material por su nombre exacto; RGBA son valores de visualización guardados en Blender, redondeados a cuatro decimales. `—` significa que el material no existe en esa fuente. Los nombres coincidentes entre archivos **no implican colores coincidentes**. Las imágenes asociadas están detalladas arriba.

| Material | RGBA sala | RGBA semicírculo |
| --- | --- | --- |
| `Material` | 0.8000, 0.8000, 0.8000, 1.0000 | 0.8000, 0.8000, 0.8000, 1.0000 |
| `openskp_material_0` | 0.1373, 0.1373, 0.1373, 1.0000 | 0.2275, 0.2275, 0.2275, 1.0000 |
| `openskp_material_1` | 0.8353, 0.7529, 0.6392, 1.0000 | 0.6667, 0.6667, 0.6667, 1.0000 |
| `openskp_material_2` | 0.8863, 0.8863, 0.8863, 1.0000 | 0.4471, 0.4471, 0.4471, 1.0000 |
| `openskp_material_3` | 1.0000, 0.3294, 0.3294, 1.0000 | 0.7765, 0.7765, 0.7765, 1.0000 |
| `openskp_material_4` | 1.0000, 0.3294, 0.3294, 1.0000 | 0.7765, 0.7765, 0.7765, 1.0000 |
| `openskp_material_5` | 0.7765, 0.7765, 0.7765, 0.1500 | 0.2275, 0.2275, 0.2275, 1.0000 |
| `openskp_material_6` | 1.0000, 0.9804, 0.9804, 1.0000 | 0.4471, 0.4471, 0.4471, 1.0000 |
| `openskp_material_7` | 0.7765, 0.7765, 0.7765, 0.1500 | 1.0000, 0.3294, 0.3294, 1.0000 |
| `openskp_material_8` | 1.0000, 1.0000, 1.0000, 1.0000 | 0.1412, 0.1843, 0.2588, 1.0000 |
| `openskp_material_9` | 0.8863, 0.8863, 0.8863, 1.0000 | 1.0000, 0.3294, 0.3294, 1.0000 |
| `openskp_material_10` | 1.0000, 1.0000, 1.0000, 1.0000 | 0.1412, 0.1843, 0.2588, 0.6800 |
| `openskp_material_11` | 0.8275, 0.7412, 0.5647, 1.0000 | 0.1176, 0.1176, 0.1176, 1.0000 |
| `openskp_material_12` | 0.1176, 0.1176, 0.1176, 1.0000 | 1.0000, 1.0000, 1.0000, 1.0000 |
| `openskp_material_13` | 0.1373, 0.1373, 0.1373, 1.0000 | 0.7098, 0.5216, 0.7176, 1.0000 |
| `openskp_material_14` | 0.6471, 0.1647, 0.1647, 1.0000 | 0.4039, 0.5098, 0.6902, 1.0000 |
| `openskp_material_15` | 0.6471, 0.1647, 0.1647, 1.0000 | 0.3765, 0.3765, 0.3765, 1.0000 |
| `openskp_material_16` | 0.8000, 0.4784, 0.1569, 1.0000 | 0.4627, 0.4627, 0.4627, 1.0000 |
| `openskp_material_17` | 1.0000, 0.6980, 0.3961, 1.0000 | 1.0000, 0.0000, 0.0000, 1.0000 |
| `openskp_material_18` | 1.0000, 0.6980, 0.3961, 1.0000 | 0.5569, 0.5569, 0.5569, 1.0000 |
| `openskp_material_19` | 0.8000, 0.5569, 0.3176, 1.0000 | 0.3765, 0.3765, 0.3765, 1.0000 |
| `openskp_material_20` | 1.0000, 0.6000, 0.1961, 1.0000 | 0.3176, 0.3176, 0.3176, 1.0000 |
| `openskp_material_21` | 0.8000, 0.7176, 0.6392, 1.0000 | 0.8863, 0.8863, 0.8863, 1.0000 |
| `openskp_material_22` | 0.8196, 0.8196, 0.8196, 1.0000 | 0.8863, 0.8863, 0.8863, 1.0000 |
| `openskp_material_23` | 0.8196, 0.8196, 0.8196, 1.0000 | 0.1176, 0.1176, 0.1176, 1.0000 |
| `openskp_material_24` | 0.3176, 0.3176, 0.3176, 1.0000 | 0.1412, 0.1843, 0.2588, 0.6800 |
| `openskp_material_25` | 0.6627, 0.6627, 0.6627, 1.0000 | 0.3922, 0.5843, 0.9294, 0.1600 |
| `openskp_material_26` | 1.0000, 1.0000, 1.0000, 0.7800 | 0.0275, 0.0118, 0.0078, 1.0000 |
| `openskp_material_27` | 0.4000, 0.3569, 0.3176, 1.0000 | 0.3922, 0.5843, 0.9294, 0.5000 |
| `openskp_material_28` | 1.0000, 0.9804, 0.9804, 1.0000 | 1.0000, 1.0000, 1.0000, 0.5900 |
| `openskp_material_29` | 0.0000, 0.0000, 0.0000, 0.7400 | 0.1373, 0.1373, 0.1373, 1.0000 |
| `openskp_material_30` | 0.0000, 0.0000, 0.0000, 0.7400 | 0.1412, 0.1843, 0.2588, 1.0000 |
| `openskp_material_31` | 0.1176, 0.1176, 0.1176, 1.0000 | 0.3176, 0.3176, 0.3176, 1.0000 |
| `openskp_material_32` | 1.0000, 0.9608, 0.9333, 1.0000 | 0.5020, 0.5020, 0.5020, 0.5000 |
| `openskp_material_33` | 0.5961, 0.3373, 0.1647, 1.0000 | 0.1373, 0.1373, 0.1373, 1.0000 |
| `openskp_material_34` | 0.7765, 0.7765, 0.7765, 1.0000 | 0.4196, 0.4157, 0.3804, 1.0000 |
| `openskp_material_35` | 0.3020, 0.4235, 0.5412, 1.0000 | — |
| `openskp_material_36` | 0.3020, 0.4235, 0.5412, 1.0000 | — |
| `openskp_material_37` | 0.7765, 0.7765, 0.7765, 1.0000 | — |
| `openskp_material_38` | 1.0000, 1.0000, 1.0000, 0.7800 | — |
| `openskp_material_39` | 0.2275, 0.2275, 0.2275, 1.0000 | — |
| `openskp_material_40` | 1.0000, 0.9804, 0.9804, 0.8700 | — |
| `openskp_material_41` | 0.0000, 0.0000, 0.0000, 1.0000 | — |
| `openskp_material_42` | 0.1412, 0.1843, 0.2588, 1.0000 | — |
| `openskp_material_43` | 0.7843, 0.8353, 0.9294, 0.8200 | — |
| `openskp_material_44` | 0.4118, 0.4118, 0.4118, 1.0000 | — |
| `openskp_material_45` | 0.0000, 0.0000, 0.0000, 1.0000 | — |
| `openskp_material_46` | 0.8000, 0.7176, 0.6392, 1.0000 | — |
| `openskp_material_47` | 0.3176, 0.3176, 0.3176, 1.0000 | — |
| `openskp_material_48` | 0.0000, 0.0000, 0.0000, 0.6400 | — |
| `openskp_material_49` | 0.8863, 0.8863, 0.8863, 0.7800 | — |
| `openskp_material_50` | 0.3765, 0.3765, 0.3765, 1.0000 | — |
| `openskp_material_51` | 0.6627, 0.6627, 0.6627, 1.0000 | — |
| `openskp_material_52` | 0.7843, 0.8353, 0.9294, 0.8200 | — |
| `openskp_material_53` | 0.8275, 0.8275, 0.8275, 1.0000 | — |
| `openskp_material_54` | 1.0000, 0.8980, 0.6000, 1.0000 | — |
| `openskp_material_55` | 0.6000, 0.6000, 1.0000, 1.0000 | — |
| `openskp_material_56` | 0.3922, 0.5843, 0.9294, 0.1200 | — |
| `openskp_material_57` | 1.0000, 0.0000, 0.0000, 1.0000 | — |
| `openskp_material_58` | 0.5176, 0.5176, 0.5176, 1.0000 | — |
| `openskp_material_59` | 0.6667, 0.6667, 0.6667, 1.0000 | — |
| `openskp_material_60` | 0.6667, 0.6667, 0.6667, 1.0000 | — |
| `openskp_material_61` | 0.5176, 0.5176, 0.5176, 1.0000 | — |
| `openskp_material_62` | 0.4471, 0.4471, 0.4471, 1.0000 | — |
| `openskp_material_63` | 0.4471, 0.4471, 0.4471, 1.0000 | — |
| `openskp_material_64` | 0.2275, 0.2275, 0.2275, 1.0000 | — |
| `openskp_material_65` | 0.1412, 0.1843, 0.2588, 1.0000 | — |
| `openskp_material_66` | 0.5020, 0.5020, 0.5020, 0.5000 | — |
| `openskp_material_67` | 0.2000, 0.1569, 0.1765, 1.0000 | — |
| `openskp_material_68` | 0.6667, 0.0667, 1.0000, 1.0000 | — |
| `openskp_material_69` | 0.1569, 0.2000, 0.2000, 1.0000 | — |
| `openskp_material_70` | 0.1882, 0.2431, 0.2431, 1.0000 | — |
| `openskp_material_71` | 0.7098, 0.6353, 0.4824, 1.0000 | — |
| `openskp_material_72` | 0.2000, 0.1098, 0.0784, 1.0000 | — |
| `openskp_material_73` | 0.7373, 0.7373, 0.7373, 1.0000 | — |

## Archivos entregados y verificación

Todos los archivos siguientes están **solo en disco local**, en el directorio de trabajo indicado al principio. Ninguno se publica en GitHub.

| Archivo | Tamaño, bytes | SHA-256 |
| --- | ---: | --- |
| `Computadora_Circulo_Ajustado_V02.blend` | 1989501 | `2fba31699e59f8d4546f537539f744affbffc09518bf8b93f5aced829900f641` |
| `Computadora_Circulo_Completo_V01.blend` | 1989949 | `1c881773f2ec64ade0c20b45b9295b1271b9c0e1fd1a4645ce36e66a016a9c90` |
| `Sala_computadora_Materiales_Recuperados.blend` | 1448070 | `67d8c6d61415c368541b7260b0b36357173f99f04e2c343b336848ce51350126` |
| `Sala_Supercomputadora_Enterprise_G_FINAL.blend` | 3890394 | `d4aec4297ade9b9bca8c8df202696ba2200a25c056cba3fb3207fa90a25cd2ab` |
| `Sala_Supercomputadora_Valhalla_Integrada_V03.blend` | 3890394 | `d4aec4297ade9b9bca8c8df202696ba2200a25c056cba3fb3207fa90a25cd2ab` |
| `Semicirculo_computadora_Materiales_Recuperados.blend` | 967525 | `b6b7db144e91168b7e8b38b8618c4b28e47ea65097236c31c428e23af6f0d637` |

Los seis archivos se abrieron de nuevo desde su ubicación definitiva con Blender 5.2.2. Se comprobó que no hay bibliotecas externas y que todas las imágenes de archivo están empaquetadas. El archivo con sufijo `FINAL` es el hito de esta entrega; su propiedad de escena y este informe lo identifican como **PARCIAL**, no como aprobación definitiva.

El informe y el [script reutilizable](../../tools/blender/valhalla_supercomputadora.py) pueden versionarse. El script exige fuentes y carpeta de salida nueva/vacía, verifica hashes de originales, identifica materiales por tipo de nodo, reutiliza mallas y valida cotas de integración con vértices reales. Para ejecutarlo con el Blender y lector compatibles ya disponibles:

```text
blender --background --factory-startup --python desarrollo/tools/blender/valhalla_supercomputadora.py -- --source-dir FUENTES --output-dir SALIDAS_NUEVAS --evidence-dir EVIDENCIA_TEMPORAL_AUTORIZADA
```

La generación no necesita los scripts desechables de auditoría para funcionar. Las dependencias del lector se usan solo al reconstruir desde SKP; los modelos entregados abren de manera autónoma. Las evidencias brutas, renders y ejecuciones fallidas se conservan localmente en el área temporal autorizada y pueden retirarse como una unidad sin afectar a los entregables. No se han borrado.

## Git y publicación

Rama: `codex/valhalla-supercomputadora`, creada desde `main` actualizado en `142f852e5a1abfa373413002be928fd4f437b3bc`.

Se añadió `/PROYECTO VALHALLA/` a `.gitignore`. Las reglas existentes ya cubren modelos por extensión, copias `.blend*`, recursos privados `/_ST/`, `/3D Star Trek/`, biblioteca pesada en `/assets/` y texturas PBR. Se conservaron todas esas reglas. La exclusión completa de Valhalla protege también originales SKP, respaldos SKB, blueprint y futuras salidas del directorio, sin añadir nuevas exclusiones globales.

Se verificó con `git check-ignore -v` la exclusión de los `.blend`, `.skp`, `.blend1`, `.skb`, recursos GLB en assets y Blender en juego, además de los directorios privados existentes. La consulta del índice para `.blend*`, `.skp`, `.skb`, `.fbx`, `.glb`, `.gltf`, `.obj` y `.dae` no devolvió modelos versionados. No se ejecutó `git rm --cached` ni se eliminó ningún archivo local.

La publicación incluye exclusivamente este informe, `.gitignore` y el script reutilizable. La PR se abre como borrador para auditoría independiente, **sin fusionar**.

## Estado de validación y trabajo pendiente

| Comprobación | Resultado |
| --- | --- |
| Originales Blender y SKP intactos por SHA-256 | Verificado |
| Blueprint intacto | Verificado por hash registrado |
| Apertura de las seis copias definitivas | Verificada |
| Dos conjuntos circulares insertados a escala uniforme 1:1 | Verificado |
| Alineación arquitectónica | 125/128 puntos por recinto; discrepancias documentadas |
| Espejos con determinante positivo | Verificado |
| Objetos, geometría y UV originales de la sala conservados | Verificado, sin diferencias |
| Materiales originales recuperables | Colores/alpha e imágenes recuperados en copias |
| Pasos centrales sin bancos a tres alturas | Franjas ensayadas libres |
| Ausencia total de interpenetraciones | **No superada**: contactos pendientes |
| Cierre de toda la topología y orientación de todas las normales heredadas | No acreditado |
| Holgura tapa/techo y todas las puertas animadas | Pendiente |
| Colisiones y navegación dentro de UE5 | No ejecutadas |
| Optimización UE5, rendimiento, LOD/Nanite y lightmaps | Pendiente |
| Protección Git de modelos y archivos pesados | Verificada |

La siguiente intervención debe resolver primero los encuentros panel/estructura y tapa/techo de forma localizada, revisar los 23 contactos no explicados por la comparación de fuente a Z=1,50 m y medir cada puerta con su envolvente de apertura. Después procede validar colisión simplificada, cápsula de personaje, navegación y rendimiento en UE5. Los 15.392 objetos nuevos favorecen la edición y las mallas compartidas ahorran memoria; todavía requieren una estrategia de instancias/agrupación para su uso eficiente en el motor.

**Estado final: PARCIAL.** Se dispone de los dos conjuntos integrados y de una recuperación verificable de los materiales, con originales conservados y evidencia de las limitaciones. La prioridad pendiente es geométrica y funcional; los acabados PBR podrán desarrollarse en una fase independiente.
