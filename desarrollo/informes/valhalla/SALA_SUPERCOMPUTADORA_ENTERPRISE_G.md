# Sala de la supercomputadora — Enterprise-G, clase Valhalla

Fecha: 1 de noviembre de 2026. **Estado V04: PARCIAL.** Ocho montantes ajustados y verificados; quedan 128 interpenetraciones superficiales, la funcionalidad de las puertas y la validación en Unreal Engine 5. Véase la continuación V04 al final. Los apartados anteriores a esa continuación conservan el registro de la entrega V03.

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

## Continuación V04 — ajuste local y validación del 1 de noviembre de 2026

**Resultado: mejora geométrica parcial, sin aprobación de toda la sala.** Se entrega un archivo nuevo, `Sala_Supercomputadora_Valhalla_Geometria_V04.blend`, en el mismo directorio local de la sala indicado en «Fuentes y protección». La V03, el hito `FINAL`, los otros entregables, los cuatro originales y el blueprint conservan sus hashes anteriores. La PR #79 permanece en borrador y no se fusiona.

### Revisión de las incidencias y corrección del plan

Se leyeron los siete JSON existentes y los cinco scripts de diagnóstico. Se reutilizaron las 16.312 colocaciones y las 174 mallas utilizadas en el diagnóstico; no se reconstruyeron los bancos. Las 434 incidencias iniciales tienen una decisión individual registrada: ocho ajustes, 128 cruces pendientes, 271 contactos límite conservados, 15 coincidencias conservadas para revisión y 12 falsos positivos que no requieren intervención.

Las 136 incidencias de cruce corresponden a **28 colocaciones de origen, repetidas cuatro veces** mediante los dos recintos y sus mitades reflejadas; algunas piezas cruzan dos instancias arquitectónicas. La equivalencia se comprobó con todos los vértices de las cuatro colocaciones de cada grupo: discrepancia máxima **0,000003541 m**, sin deducir equivalencia únicamente del nombre.

Para investigar la herencia se abrió el semicírculo original y se comprobaron los cruces de las mismas piezas contra sus superficies arquitectónicas originales. En los 136 casos ya existe un cruce correspondiente en la fuente. Se transformaron además los puntos medios de cada cruce triangular al sistema original y se midió su distancia a la arquitectura de la fuente: máximo **0,001750 m**, dentro del umbral declarado de 2 mm. Esta correspondencia próxima no significa identidad exacta de ambas arquitecturas ni convierte las penetraciones heredadas en uniones admisibles.

El plan anterior omitía 96 de las 136 incidencias de cruce. Sus 16 traslaciones de consola a cero metros procedían de un error del planificador: el filtro `normal · radial > 0,5` descartaba todos los planos útiles; `max(..., default=0)` devolvía cero ante la lista vacía. **No se ejecutó ninguna como corrección.**

Se evaluaron también restricciones de separación por planos para identificar límites de esa alternativa. Las consolas requerirían traslaciones candidatas de aproximadamente 0,219–0,239 m y algunas tapas producirían soluciones de más de 8 m o restricciones inviables. Estos resultados describen el problema de utilizar planos infinitos para superficies finitas; **se rechazaron**, no se interpretaron como movimientos válidos.

Los contactos límite sin cruce propio se conservan como contactos superficiales compatibles con apoyos y juntas; no se declara positivo el volumen libre por ello. Las 15 coincidencias siguen necesitando interpretación constructiva. No se cerraron superficies abiertas ni se eliminaron caras originales para reducir el contador.

### Correcciones aplicadas en dos grupos

Se ajustaron exclusivamente los ocho montantes `Component#34` con índices de origen `0477` y `3480`: cada índice aparece en `C01/C02` y en `A_Original/B_Espejo`.

| Grupo | Objetos | Ajuste medido |
| --- | ---: | --- |
| `0477` | 4 | Dos planos originales de pared por montante; recortes de aproximadamente 0,516–0,520 mm y 2,409–2,411 mm |
| `3480` | 4 | Un plano original de pared por montante; recorte de aproximadamente 2,309–2,311 mm |

La holgura nominal de corte es **0,100 mm** respecto a los planos medidos, por encima de la tolerancia de clasificación de 0,010 mm. Cada montante utiliza una copia privada de su malla. Se conserva su transformación y su material; se recorta la porción posterior/lateral que atraviesa la pared y se cierra solamente ese sólido originalmente cerrado. La fracción de volumen retirada es del **2,44–2,97 %** por montante. Las costuras de vértices se soldaron únicamente en estas ocho copias para permitir el corte; las mallas originales permanecen conservadas.

No se deformaron pantallas, consolas ni detalles decorativos. Las UV de las caras supervivientes se interpolan al cortar; las caras nuevas de cierre reciben proyección plana y el mismo material del montante. No se alteraron la arquitectura, los círculos completos, sus escalas ni los demás objetos de banco.

Después del primer grupo se comprobaron los cuatro montantes frente a arquitectura y bancos próximos; después del segundo, los ocho. Ambos controles terminaron sin nuevos pares de cruce ni cruces restantes entre los montantes ajustados y la arquitectura. No fue necesario revertir un grupo.

### Auditoría tridimensional antes y después

Se repitió la clasificación de todas las parejas banco/arquitectura con el mismo criterio superficial del diagnóstico inicial. Las parejas se compararon por objeto de banco e instancia arquitectónica, porque los identificadores secuenciales posteriores cambian.

| Clasificación | V03 / inicio V04 | V04 entregada |
| --- | ---: | ---: |
| Interpenetraciones superficiales | 136 | **128** |
| Contactos límite | 271 | 275 |
| Superficies coincidentes | 15 | 15 |
| Falsos positivos por tolerancia | 12 | 12 |
| Total de incidencias | 434 | 430 |
| Nuevas parejas de contacto | — | **0** |

Cuatro incidencias dejan de existir (`I00026`, `I00141`, `I00286`, `I00359` del diagnóstico inicial). Otras cuatro pasan de cruce a contacto límite (`I00118`, `I00258`, `I00337`, `I00414`); los apoyos superficiales restantes se conservan. **Ocho cruces corregidos, cero cruces nuevos.** La reducción del total no es el criterio de aceptación: se mantienen los contactos de ensamblaje y las dudas documentadas.

| Familia pendiente | Incidencias | Motivo de conservación y siguiente trabajo |
| --- | ---: | --- |
| `Component#206` | 32 | Consolas abiertas entre dos superficies; falta una solución conjunta de implantación y apoyos. No ejecutar desplazamientos radiales nulos ni candidatos de 22–24 cm. |
| `Component#50` | 20 | Tapas superiores con cruces heredados contra paredes `#200/#202`; requieren resolver el encuentro finito por sector conservando el diseño. No aplicar recortes globales sobre mallas abiertas/no manifold. |
| `Component#41` | 4 | Laterales estructurales del bastidor con topología heredada; mover una pieza aisladamente unos 38,76 mm puede romper la unión del conjunto. Revisar el bastidor completo. |
| `Component#29` | 8 | Paneles inferiores: una traslación candidata de 2,31–2,68 mm no acredita por sí sola que todos los apoyos y detalles asociados sigan ensamblados. |
| `Component#13` | 32 | Travesaños finos: resolver con el bastidor y sus apoyos, sin recortar ni separar detalles individualmente. |
| `Component#7` | 32 | Módulos repetidos de panel: pendiente ajuste rígido del subconjunto completo, sin deformar su geometría. |
| **Total abierto** | **128** | **No se acredita ausencia total de interpenetraciones.** |

### Puerta exterior, blueprint y recorridos continuos

`Component#130`, instancia `Component_435035`, es una **hoja de puerta modelada con espesor y borde superior redondeado**. La hoja complementaria es `Component#131`, instancia `Component_435936`. Su forma se revisó en vistas frontal e isométrica junto con los marcos; no son superficies auxiliares. La hoja `#130` tiene espesor aproximado **0,046029 m** y altura **2,035446 m**. Ambas existen en la sala original y se conservan sin cambios; no tienen animación configurada.

La separación actual entre hojas es **0,330000 m**, insuficiente para la cápsula provisional de 0,70 m de diámetro. Existe un hueco arquitectónico de puerta, y el corredor conecta topológicamente con el bloque central. El blueprint de la cubierta 11 se volvió a consultar para esa organización de recintos, vestíbulos y corredores. No se calibraron medidas sobre la lámina ni se identificó un símbolo concreto como prueba de la cinemática de esta puerta de Valhalla.

La cápsula **sigue siendo una referencia provisional para Valhalla**: diámetro 0,70 m, altura 1,80 m, vertical, base a Z=0,37 m. Su eje central ocupa Z=0,72–1,82 m. Las pruebas se refieren a superficies trianguladas estáticas, no a colisiones cocinadas de UE5.

El nuevo control cubre cada tramo completo mediante distancia segmento/triángulo en su punto medio y una cota conservadora: el desplazamiento máximo del eje hasta un extremo es la mitad de la longitud del tramo. Solo se certifica el tramo libre si la distancia supera el radio más esa semilongitud y la tolerancia; los candidatos geométricos se buscan con esa misma expansión. Se subdividen los intervalos que no admiten esa conclusión. Así se comprueban intervalos completos, no solo posiciones aisladas.

El cálculo de distancia utiliza semiespacios de arista para evitar falsos interiores al invertir una matriz de Gram casi degenerada. Se verificaron seis casos analíticos: pared, techo, cruce del eje, punto degenerado, arista degenerada y tangencia de apoyo al suelo. Se excluyen de bloqueo las caras enteramente por debajo de la base, con 0,010 mm de tolerancia numérica, incluidas las caras laterales inferiores de las losas. Un ensayo preliminar produjo un falso bloqueo en `R2_este`; se descartó tras identificar el problema numérico, sin modificar la arquitectura.

| Recorrido en la V04 | Resultado continuo |
| --- | --- |
| Ocho salidas radiales de los dos recintos | Libres de intersección de cápsula en los tramos definidos |
| Dos conexiones de centro a vestíbulo | Libres |
| Conexión entre vestíbulos y bloque central | Libre |
| Bloque central hacia corredor exterior, estado actual | **Bloqueado por las hojas originales** |
| Mismo recorrido, omitiendo solo ambas hojas en el diagnóstico | Libre; demuestra continuidad del hueco, no apertura animada |

Las once rutas interiores tienen certificación geométrica continua según este criterio, sin intervalos indeterminados; no están bloqueadas por bancos o soportes. El recorrido exterior tiene posiciones de colisión confirmada con `Component#130`. El diagnóstico de puerta abierta omite temporalmente ambas hojas en el cálculo, **sin borrarlas, moverlas ni guardar ese estado en el modelo**. Quedan pendientes la cinemática, los alojamientos laterales, los barridos de las hojas, los controles y la implementación de UE5. Tampoco se certifican aquí el soporte continuo de toda la huella del personaje, peldaños, pendientes ni navegación del motor.

### Encuentro superior y conservación

Las 16 tapas `Component#50` se compararon con las dos instancias del techo `Component#194`. No hay cruces triangulares entre esos elementos. Se comprobó también la proyección XY de sus triángulos para no confundir ausencia de cruce superficial con ausencia de inclusión: **cero pares con área proyectada común**, separación XY mínima **0,104170 m**. La coincidencia de sus rangos de Z, por sí sola, no implica que ocupen el mismo lugar. Este resultado resuelve la duda de esas tapas frente a `#194`; no elimina los 20 cruces de tapa contra paredes `#200/#202`.

La reapertura del archivo final verificó:

- Los **16.799 objetos** conservan sus transformaciones, parentesco y pertenencia a colecciones. Solo ocho referencias a datos de malla cambian a las copias ajustadas.
- Los **1.407 objetos y las 136 mallas de la sala original** coinciden con el original en geometría, índices, asignación material y UV incluidos en las firmas.
- Los **220 bloques de malla de la V03**, incluidos los no utilizados por las colocaciones auditadas, permanecen conservados; se añaden ocho bloques privados. Las 174 mallas del inventario inicial son las utilizadas por sus 16.312 colocaciones, no el total de bloques del archivo.
- Los **101 materiales** de la V03 conservan colores, alpha, entradas y conexiones de nodos; las **tres imágenes de archivo** conservan tamaño y bytes empaquetados. Cero bibliotecas externas y ninguna ruta de imagen hacia el área experimental.
- La geometría y los objetos del archivo final coinciden exactamente con la segunda etapa auditada. Las ocultaciones y cámaras del render de diagnóstico no se guardaron.
- Los diez archivos protegidos del manifiesto inicial y el blueprint conservan sus SHA-256. No se sobrescribieron ni eliminaron originales, entregas anteriores o respaldos.

### Entregable y reproducción

| Archivo local nuevo | Tamaño | SHA-256 |
| --- | ---: | --- |
| `Sala_Supercomputadora_Valhalla_Geometria_V04.blend` | 3.892.491 bytes | `e4dbf7a0b835fe0ad2f51500ca801b5a3c914069816885a2e8f551466fe27568` |

El [script V04](../../tools/blender/valhalla_supercomputadora_v04.py) y su [plan revisado](../../tools/blender/valhalla_supercomputadora_v04.plan.json) permiten reproducir los ocho ajustes a partir de la V03 con hash conocido. Ambos son pequeños archivos versionables; no requieren scripts ni datos temporales para generar el modelo. El plan contiene solo los ocho ajustes seguros, no instrucciones para ejecutar las 128 incidencias abiertas.

```text
blender --background --factory-startup --python-exit-code 1 --python desarrollo/tools/blender/valhalla_supercomputadora_v04.py -- --input V03.blend --plan desarrollo/tools/blender/valhalla_supercomputadora_v04.plan.json --output NUEVO_V04.blend --evidence-dir EVIDENCIA_TEMPORAL_AUTORIZADA
```

El script rechaza un hash de entrada distinto, una salida existente, operaciones repetidas, piezas ajenas a los montantes revisados, superficies originalmente abiertas y recortes fuera del límite de 3 mm. Conserva los datos originales y verifica la integridad antes y después de guardar. Las pruebas de contactos y accesos descritas arriba son validaciones adicionales de esta entrega, no funcionalidades que el script de ajuste afirme sustituir.

Las evidencias locales se identifican por nombre y hash para localizar la ejecución correcta sin introducir dependencias de rutas experimentales en el proyecto permanente:

| Evidencia local | Contenido | SHA-256 |
| --- | --- | --- |
| `plan_ejecutable_y_pendientes.json` | Decisiones de las 434 incidencias y equivalencias de simetría | `8c67252bfaba68014bdec593ea7e8747003a6268952f6281bce58c3c44f39830` |
| `herencia_136.json` | Comparación individual con el semicírculo original | `5e727f1796e7248fb3e2193e1075bd5d260a2734200665079619dce05ff69c43` |
| `contactos_3d.json`, segunda etapa | Auditoría de 430 incidencias posteriores | `7f5c2c4452e800d5e2af4e9b3c26b9ff1a382db00cdfaa94ba0e6c32c448abc9` |
| `accesos_continuos_robustos_v04.json` | Intervalos y obstáculos de las rutas de la V04 | `567d16779716db5c90f8c635ad0cf8f8f19250e64e59e8189996f181d3c64bd0` |
| `techo_regresiones_y_puerta.json` | Proyecciones de techo, casos analíticos y medidas de puerta | `90970dac211e2732d31ce5b42ddb8e76c402179388554acbadc65cde38702213` |
| `integridad_entrega.json` | Reapertura, firmas y conservación de originales | `f2224eeeb51294e63c7158558fa34718adee19046aad523ccd9edf31366ce9cc` |

Se conservan además las dos etapas de modelo, sus controles locales, registros de aplicación, pruebas descartadas, renders y `resumen_v04.json`. El área experimental completa es prescindible para abrir el archivo V04 y reproducir sus ajustes con los archivos versionados; no se ha eliminado. Git publica exclusivamente este informe, el script V04 y su plan revisado. Los modelos y las evidencias voluminosas continúan solo en disco local.

**La V04 sigue PARCIAL:** ocho conflictos locales resueltos y accesos interiores comprobados con referencia provisional; 128 cruces heredados, la funcionalidad de las puertas y la validación de colisiones/navegación en UE5 permanecen abiertos.
