# Sala de la supercomputadora — Enterprise-G, clase Valhalla

Fecha: 1 de noviembre de 2026. **Estado V04D: prototipos locales PARCIALES; último modelo válido V04B.** Se entregan candidatos de unión para P01 y T01, sin extenderlos al resto de sectores. Se recomienda A adaptado y tapa continua para revisión, con holguras reales y límites explícitos. V04B conserva sus archivos y su estado anterior. No existe una V04D definitiva; faltan aprobación de diseño y pruebas en UE5. Los apartados V03, V04, V04B y V04C conservan el registro histórico.

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
- Los **101 materiales** de la V03 conservan colores, alpha, entradas y conexiones de nodos; los **dos bloques de imagen de archivo** presentes conservan tamaño y bytes empaquetados. El recuento anterior de tres bloques se corrige tras la inspección V04B, descrita más adelante. Cero bibliotecas externas y ninguna ruta de imagen hacia el área experimental.
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

## V04B — puertas, encuentros constructivos y preparación funcional

**Entrega local nueva: `Sala_Supercomputadora_Valhalla_Puertas_V04B.blend`. Estado: PARCIAL.** Se parte exactamente de la V04 verificada. Se conservan los archivos originales y todos los entregables existentes. La modificación válida de esta fase es una preparación geométrica y animada de la puerta exterior; no se declara terminada la sala ni implementado su funcionamiento en UE5.

### Puerta exterior: impedimento original y mecanismo elegido

Las hojas son `Component#130` y `Component#131`, instanciadas por `Component_435035` y `Component_435936`. Los revestimientos del hueco son dos instancias de `Component#120`, `Component_431089` y `Component_431089.001`. Se inspeccionaron las posiciones originales, los materiales, las secciones y poses intermedias de apertura.

La posición original **ya tiene 0,330000 m entre las hojas**, por lo que es una referencia parcialmente abierta, no un cierre estanco. Cada hoja tiene aproximadamente 46,029 mm de espesor. Entre los planos exteriores del revestimiento hay 401,181 mm de profundidad y espacio lateral modelado para alojar las hojas. Sin embargo, las caras del revestimiento cierran el acceso a ese espacio atravesando la trayectoria de las hojas. Se detectan cruces con `#120` en la propia posición original y durante el desplazamiento; una pose final sin cruces no demuestra un barrido libre.

Se eligió **deslizamiento lateral opuesto, paralelo al eje Y del modelo**, por la forma de las dos hojas, el hueco y la cavidad existente. Para hacerlo compatible con las superficies modeladas se introdujo una ranura medida únicamente en una **copia privada del revestimiento**. No se ensanchó el hueco de paso del personaje ni se retiraron las hojas, paredes, marcos exteriores o detalles.

| Medida | Resultado |
| --- | ---: |
| Hueco entre jambas | 1,799236 m |
| Altura central del hueco sobre Z=0,37 m | 2,035446 m |
| Espesor máximo de las hojas | 0,046029 m |
| Ranura local en X | 31,190818–31,240846 m |
| Ancho de ranura | 0,050029 m |
| Holguras laterales medidas tras guardar | 2,000809 mm y 2,000306 mm |
| Retirada completa detrás de cada jamba | 10 mm |
| Carrera de cada hoja, cierre de diagnóstico → apertura | 0,907618 m |
| Separación central en el cierre de diagnóstico | 4,000 mm |

El nuevo bloque `V04B_Revestimiento_Puerta_Ranura` conserva materiales y orientación de las caras supervivientes. La ranura retira el 12,4707 % del área superficial del revestimiento, manteniendo las dos bandas exteriores. Es una abertura para una hoja de 46 mm dentro de un revestimiento de 401 mm de profundidad; no es una abertura de 0,70 m para forzar el paso del personaje. El objeto y la malla originales `Component#120` permanecen conservados. Solo las dos instancias del revestimiento utilizan la colección privada nueva `V04B_Revestimiento_Ranurado`.

Sin esta corrección local, el deslizamiento atraviesa el revestimiento original y no se acepta como cinemática libre. Como alternativas, una puerta elevada necesitaría un alojamiento vertical adicional no modelado; una separación perpendicular seguida de deslizamiento requeriría revisar los recubrimientos y un mecanismo nuevo; una articulación o plegado exige bisagras y cambios de diseño que no están justificados por la fuente. No se ejecutaron esas alternativas ni se las presenta como movimientos certificados.

La cavidad comprobada es el espacio libre de las superficies del modelo. No se han diseñado carriles, actuadores, rodamientos, soportes o refuerzos ni se realiza aquí una aprobación estructural del revestimiento ranurado.

### Estados conservados y apertura realmente modelada

La V04B se guarda en el fotograma 1. Las instancias de las dos hojas reciben claves lineales de posición y marcadores explícitos:

| Fotograma | Estado | Desplazamiento Y de `#130` desde la referencia | Desplazamiento Y de `#131` |
| --- | --- | ---: | ---: |
| 1 | Referencia original, separación 0,33 m | 0 | 0 |
| 20 | Cierre de diagnóstico, junta central 4 mm | -0,128955 m | +0,197045 m |
| 60 | Apertura completa de diagnóstico | +0,778663 m | -0,710573 m |

Las carreras desde el cierre son simétricas, ±0,907618 m. Todas las matrices originales se conservan exactamente en el fotograma 1; los datos de malla de ambas hojas no cambian. Las claves usan interpolación lineal, sin sobrepasar los extremos. El cierre deja una junta deliberada de 4 mm: no se declara sellado hermético ni se añaden juntas ficticias.

Se guardaron además copias locales independientes de los estados cerrado y abierto. Las vistas comparan la referencia original, el cierre y la apertura, en frontal, isométrica y secciones a Z=1,50 m. Las hojas permanecen presentes, dentro de las cavidades laterales, en el estado abierto. No se ocultan ni se excluyen del cálculo de paso.

### Barrido continuo y cápsula provisional

Se comprobó el movimiento completo, no solo varios fotogramas. Un control continuo por ejes separadores calculó intervalos de posible contacto para cada pareja candidata de triángulos bajo traslación. En la geometría original confirma cruces con `Component#120`; con la copia ranurada no quedan parejas candidatas ni triángulos degenerados pendientes en el subsistema móvil.

El script reutilizable incorpora además una condición conservadora suficiente: las cajas de cada triángulo barrido durante toda la carrera no solapan las de los triángulos fijos. En la entrega resulta **cero parejas potencialmente solapadas**; si hubiera una, el script rechazaría guardar para pedir revisión geométrica. Las dos hojas se separan monótonamente y su distancia mínima entre extremos en Y es la junta de 4 mm del cierre. Las caras enteramente bajo la base, con tolerancia de 0,010 mm, se tratan como apoyo al suelo.

Se verificaron seis casos analíticos del control continuo, incluido un cruce transitorio con ambos extremos libres, un cruce de planos en mitad del movimiento, separación de planos y conservación del resultado tras giro y traslación. El barrido cubre las posiciones intermedias de la animación: la referencia original también está dentro de la carrera entre cierre y apertura.

Se repitió la comprobación continua del recorrido completo desde el bloque central hasta el extremo del corredor exterior, de X=22,684833 a X=55,5 m, a Y=-2,473749 m. Se utiliza la misma cápsula **provisional para Valhalla**, de diámetro 0,70 m y altura 1,80 m, con base Z=0,37 m, y la cota de distancia por intervalos utilizada en V04.

| Estado real de la V04B | Resultado del recorrido |
| --- | --- |
| Fotograma 1, referencia original | Bloqueado por las hojas |
| Fotograma 20, cierre de diagnóstico | Bloqueado por las hojas |
| Fotograma 60, apertura completa | **Libre en los 329 intervalos certificados**, sin intervalos indeterminados |

Las hojas y el revestimiento modificado intervienen en las tres pruebas; no se utiliza la omisión de hojas de la V04. Las once rutas interiores ya verificadas quedan fuera de la región de barrido y no reciben geometría nueva. Se acredita separación geométrica de superficies en el movimiento y el recorrido abierto, no el comportamiento de un controlador ni la seguridad de cierre con un personaje en el hueco.

### Clasificación de las 128 incidencias: significado e impacto

Se conservaron los 128 cruces banco/arquitectura y se revisaron individualmente por familia, materiales afectados, cotas y visibilidad. Se trazaron **7.680 rayos**: cinco puntos de cruce por incidencia desde doce posiciones de observación a Z=1,65 m, elegidas sobre rutas interiores previamente comprobadas. Es una prueba de ocultación desde esas posiciones, no una garantía desde cualquier cámara ni con todos los materiales posibles de UE5.

| Familia | Incidencias | Clasificación de impacto | Decisión |
| --- | ---: | --- | --- |
| `Component#206` | 32 | Interferencia visual o funcional que necesita corrección | Prioridad de revisión de implantación: son módulos completos de paneles/hojas acristalados casi superpuestos, no consolas identificadas. No mover ni eliminar una variante sin resolver su función. |
| `Component#50` | 20 | Requiere revisión manual del remate superior | Cruces desde Z=2,994498 m, por encima de la cápsula, ocultos en 1.200/1.200 rayos interiores. Falta validar vistas altas, unión con paredes y acabado del remate. No se recortan tapas globalmente. |
| `Component#41` | 4 | Encuentro constructivo admisible provisionalmente | Solape del bastidor con pared, excursión superficial máxima ~1,635 mm, oculto en 240/240 rayos. Se conserva como unión local; no es aprobación estructural ni prueba de volumen. |
| `Component#29` | 8 | Interpenetración oculta compatible condicionalmente con futura colisión simplificada | Solape posterior ~2,21–2,58 mm; oculto en 480/480 rayos. Conservar el panel y usar una envolvente de colisión coherente de pared/bastidor. |
| `Component#13` | 32 | Misma compatibilidad condicional | Travesaños posteriores, ~2,21–2,57 mm; ocultos en 1.920/1.920 rayos. No separar los detalles de su soporte. |
| `Component#7` | 32 | Misma compatibilidad condicional | Módulos de panel, ~2,21–2,60 mm; ocultos en 1.920/1.920 rayos. Conservar detalles y revisar la envolvente en UE5. |

El reparto es **32 incidencias prioritarias de interferencia, 20 de revisión manual, cuatro encuentros constructivos provisionales y 72 solapes ocultos de compatibilidad condicional**. Ninguno se registra como cruce geométricamente eliminado por esta clasificación. Las «excursiones» son la medida del clasificador triangular anterior; no se reinterpretan como una profundidad volumétrica exacta de penetración.

Para `#206`, 48 de los 1.920 rayos no encontraron una ocultación previa de al menos 2 mm. Además, las vistas de cada objeto aislado muestran que **cada colocación ya contiene el módulo de dos paneles acristalados**. Por tanto, el aspecto de dos hojas en conjunto no justifica considerar dos colocaciones superpuestas como hojas complementarias.

Se comprobaron ocho parejas de módulos `#206`: índices de fuente `0840/1921` y `3002/3843`, repetidos en las cuatro mitades de los dos recintos. Sus centros están separados aproximadamente **8,171–8,172 mm** y sus planos difieren **2,89545–2,89547°**. Presentan 628–632 parejas de triángulos con cruce propio por pareja de módulos. Los dos casos de fuente también se cruzan al abrir el semicírculo original: el problema es heredado. Estas **ocho parejas banco/banco son adicionales** al contador de 128 banco/arquitectura; no se mezclan ambos universos.

Resolverlas exige decidir la implantación y el papel de esos módulos: una copia única compartida, un acceso de mantenimiento u otra composición deben justificarse contra los marcos y el diseño. No se elige arbitrariamente un ángulo, no se desplazan 22–24 cm y no se borran módulos para bajar el contador. Las tapas tampoco se deforman: sus cruces altos no bloquean las rutas ensayadas, pero permanecen pendientes como remate visual/constructivo.

### Auditoría de regresiones y conservación

Se realizó una auditoría incremental completa del subsistema modificado. Las firmas de todas las mallas y matrices de bancos permanecen iguales a la V04. Ninguna de las 15.392 colocaciones de banco tiene siquiera solape de cajas con la región completa de movimiento de las hojas y los revestimientos modificados. Por ello, las **430 incidencias banco/arquitectura** de referencia conservan exactamente su clasificación: **128 cruces, 275 contactos límite, 15 coincidencias y 12 falsos positivos**. No se declara una nueva ejecución integral innecesaria del clasificador sobre bancos que no han cambiado; el barrido continuo y la comprobación de regiones cubren los cambios locales.

La entrega final fue reabierta desde la carpeta local de la sala y comparada con la candidata validada:

- Se conservan los **228 bloques de malla** de la V04 y se añade uno privado para el revestimiento. Se conservan los **16.799 objetos** previos y se añade un objeto de revestimiento. Las 16.312 colocaciones geométricas evaluadas no cambian en número.
- Todas las matrices originales coinciden en el fotograma 1. Los únicos vínculos originales modificados son las dos referencias de colección de los revestimientos; las únicas animaciones añadidas afectan a las dos instancias de hoja.
- Los **101 materiales** conservan colores, alpha, nodos y conexiones. No se sustituyen materiales o texturas para esconder encuentros.
- Se corrige expresamente el recuento anterior de imágenes: la **V04 ya contiene dos bloques `FILE` empaquetados**, `Fencing_Diamond_Mesh.png` y `Wood_Cherry_Original.jpg`. Ambos conservan exactamente tamaño, rutas relativas y SHA-256 en la V04B. No se ha eliminado una tercera imagen durante esta fase; el anterior recuento de tres bloques no era correcto.
- Todas las UV originales permanecen en sus bloques originales. En el revestimiento privado se comprobaron **224 coordenadas de bucle UV** contra interpolaciones de aristas originales, con error máximo **0,000013755 unidades UV**; sus 64 caras conservan material y orientación de una cara original correspondiente. No se añaden caras de cierre para fingir una topología estanca.
- Las claves de las dos hojas se reabren en los fotogramas 1, 20 y 60 y conservan interpolación lineal. Cero bibliotecas externas, imágenes empaquetadas y ninguna dependencia de rutas experimentales.
- Los **12 archivos protegidos** al inicio, incluidos la V04, los diez archivos anteriores y el blueprint, conservan sus hashes. No se sobrescribió ni eliminó ningún entregable existente.

### Archivo, reproducción y evidencias locales

| Archivo local nuevo | Tamaño | SHA-256 |
| --- | ---: | --- |
| `Sala_Supercomputadora_Valhalla_Puertas_V04B.blend` | 3.895.466 bytes | `bb18697813040754122f5595f1d13d7eb93705828438e75a497cf460b251babd` |

El [script reutilizable V04B](../../tools/blender/valhalla_supercomputadora_v04b.py) exige el hash de la V04 revisada, rechaza salidas existentes, crea el revestimiento privado, conserva datos originales y comprueba el barrido conservador antes de guardar. Utiliza el módulo de firmas del script V04 situado a su lado; ambos son archivos permanentes versionados. No depende de los datos ni scripts desechables del diagnóstico.

```text
blender --background --factory-startup --python-exit-code 1 --python desarrollo/tools/blender/valhalla_supercomputadora_v04b.py -- --input V04.blend --output NUEVA_V04B.blend --evidence-dir EVIDENCIA_TEMPORAL_AUTORIZADA
```

Las evidencias brutas y los modelos de diagnóstico se conservan localmente. Sus referencias por nombre y hash permiten identificar la ejecución sin crear dependencias permanentes de rutas experimentales:

| Evidencia | Resultado registrado | SHA-256 |
| --- | --- | --- |
| `integridad_v04b.json` | Reapertura, datos originales, UV, materiales, claves y hashes protegidos | `eb05100c7225dfcd935ccee412f114a12fd5b7df99f111d40383cb4259ed4768` |
| `clasificacion_128_v04b_final.json` | Decisión individual por impacto de las 128 incidencias | `032fe0013baf096167a0b89132d5a77d17d5426139afe8910c3916d7027fe249` |
| `visibilidad_128_v04b.json` | 7.680 rayos de visibilidad con puntos, obstáculos y márgenes | `48f17aebf5f83cc40ed176352f3f62e93d07460987213e7077448ecb22fa3527` |
| `barridos_puertas.json` | Comparación continua antes/después del revestimiento | `30844b0cffaf524cbc184936d0915a2e934991650e8e9c2002cf9fe51a862150` |
| `paso_capsula_v04b.json` | Ruta exterior con hojas realmente presentes, estados 1/20/60 | `8127575e52d37098b14a64ae88dfc0357c244d0b1858b38ad965a2dfe230b0eb` |
| `auditoria_incremental_v04b.json` | Ausencia de regiones de banco afectadas, contador conservado y holguras | `a370adc6f6e428ecf68edc2f94e7cb3d846c5c25433c4fa9089e1b23a4e9fdd4` |

Se conservan también `familias_detalle.json`, `paneles_fuente_original.json`, los seis casos analíticos de `regresiones_barrido.json`, `resumen_v04b.json`, las copias de puerta cerrada/abierta y las vistas comparativas de puerta, módulos acristalados, tapas y bastidores. Los renders y secciones de diagnóstico no alteran las cámaras, visibilidad ni materiales guardados en la entrega. El área experimental es prescindible para abrir o reproducir la V04B y no se ha eliminado.

### Separación de Blender y UE5

**Realizado en Blender:** modificación local medida del revestimiento, poses lineales conservando la referencia, barridos geométricos continuos, hueco útil, recorrido exterior abierto con cápsula provisional, clasificación de encuentros, vistas y comprobación de integridad.

**Pendiente en Unreal Engine 5:** separación funcional de actores/componentes y pivotes, colisiones simples de paredes/bancos/hojas, controlador y tiempos de apertura, enclavamientos y detección de personaje durante el cierre, navegación actualizable, soporte y movilidad del personaje, validación de materiales e iluminación, rendimiento y revisión de las incidencias priorizadas. Los fotogramas de diagnóstico no equivalen a tiempos de una puerta implementada.

**La sala sigue PARCIAL.** La puerta exterior dispone de una solución geométrica local y verificable en copia; no se declara un sistema funcional completo ni se aprueban automáticamente los solapes conservados. La PR #79 continúa como borrador y no se fusiona.


## Continuación V04C — Módulos acristalados y remates superiores

**Resultado: diagnóstico entregado; ninguna corrección geométrica aprobada.** La base de esta fase es `Sala_Supercomputadora_Valhalla_Puertas_V04B.blend`, SHA-256 `bb18697813040754122f5595f1d13d7eb93705828438e75a497cf460b251babd`. Permanece intacta y sigue siendo el último estado válido, todavía PARCIAL. No se ha creado `Sala_Supercomputadora_Valhalla_Modulos_V04C.blend`: escoger una lateralidad o recortar los encuentros actuales sin resolver su referencia constructiva sería una decisión de diseño no demostrada.

### Origen y función de Component#206

Se compararon las ocho parejas de la entrega y las cuatro colocaciones del semicírculo fuente, incluyendo su árbol original de SketchUp:

- Las cuatro proceden del mismo nodo `Component_20769`, definición `Component#206`, recurso geométrico `mesh_20`. Cada uno contiene el módulo completo con sus dos paneles acristalados, **1.130 vértices y 728 polígonos**. No son dos hojas complementarias ni consolas identificadas.
- Las matrices locales de hijo son iguales; cambian las transformaciones de los sectores `Component_1442`, instancias de `Component#51`. Al componer la cadena original y convertir Y vertical a Z vertical se reproducen las cuatro matrices Blender con error máximo **4,322 × 10⁻⁷** por coeficiente. La separación y el giro ya existen en SketchUp; no se introdujeron en V03/V04 ni en la animación de puerta.
- La separación entre centros es **8,171–8,172 mm** y el ángulo entre planos **2,89545–2,89547°**. Una colocación tiene lateralidad reflejada respecto a su pareja. Tras reflejar el eje tangencial, la discrepancia máxima de las nubes canónicas en los dos casos de fuente ensayados es **1,193 × 10⁻⁷ m**. Las diferencias de hash de una canonización sin esta reflexión no prueban que sean diseños distintos.
- Se conservan el recurso original, los materiales y las UV. La escala local X=1,15 de la definición ya está en la cadena SKP y no es un estiramiento añadido en esta revisión. La integración general continúa a escala 1:1.
- Las cuatro fuentes están en `Layer0`; sus propiedades y diccionarios de atributos leídos están vacíos. No aparece metadato que justifique capas constructivas o funciones diferentes. **La evidencia es compatible con redundancia de un módulo compartido al repetir sectores; la intención de diseño no queda demostrada por la geometría.**

Las anclas de los objetos caen hacia extremos opuestos del mismo encuentro. En el primer caso, la cuerda entre anclas mide 1,013813 m frente a un ancho proyectado del módulo de 1,006614 m. Sus vértices de arquitectura más cercanos están a unos 15,6–18 mm: no se puede usar el origen del objeto como si fuera una cara exacta de jamba. Las ocho parejas banco/banco se relacionan así con las 32 incidencias banco/arquitectura de V04B:

| Pareja visual | Colocación y fuentes | Incidencias banco/arquitectura de referencia |
| --- | --- | --- |
| P01 | `C01_Banco_A_0840_1921` | `I00045`, `I00046`, `I00097`, `I00098` |
| P02 | `C01_Banco_A_3002_3843` | `I00113`, `I00114`, `I00131`, `I00132` |
| P03 | `C01_Banco_B_0840_1921` | `I00155`, `I00156`, `I00178`, `I00179` |
| P04 | `C01_Banco_B_3002_3843` | `I00229`, `I00230`, `I00276`, `I00277` |
| P05 | `C02_Banco_A_0840_1921` | `I00297`, `I00298`, `I00314`, `I00315` |
| P06 | `C02_Banco_A_3002_3843` | `I00330`, `I00331`, `I00348`, `I00349` |
| P07 | `C02_Banco_B_0840_1921` | `I00369`, `I00370`, `I00390`, `I00391` |
| P08 | `C02_Banco_B_3002_3843` | `I00406`, `I00407`, `I00424`, `I00425` |

Cada pareja reúne cuatro incidencias de referencia, dos por cada módulo completo. Las ocho parejas banco/banco son un segundo universo y siguen separadas del contador de 128.

### Alternativas independientes y reversibles

Se generaron tres archivos **de diagnóstico, no aprobados** desde lecturas independientes de la V04B intacta:

| Variante | Implantación activa en cada pareja | Resultado |
| --- | --- | --- |
| A | Mantener 0840/3002 exactamente en su posición original | Ocho módulos activos; 16 cruces con arquitectura; no quedan parejas activas #206/#206 |
| B | Mantener 1921/3843 exactamente en su posición original | Ocho módulos activos; 16 cruces con arquitectura; no quedan parejas activas #206/#206 |
| C | Un módulo con la lateralidad de A, centro geométrico y normal medios de la pareja | Giro de ~1,4477° y traslación del centro de ~4,086 mm respecto a A; siguen 16 cruces con arquitectura |

En A/B se conservan los ocho objetos no activos; en C se conservan los 16 originales y se añaden ocho propuestas que comparten sus mallas. Los originales pasan a `V04C_REFERENCIA_206_NO_ACTIVA`, desactivada en vista y render, **sin borrar ni modificar sus mallas, matrices o UV**. La propiedad `V04C_colecciones_previas` conserva las colecciones de origen. Para revertir la variante basta restituir esos vínculos y desactivar la colección de propuestas C; también se mantiene la V04B intacta como referencia independiente.

Las tres alternativas tienen **112 cruces activos banco/arquitectura: 16 de #206 y los otros 96 exactamente conservados**. Es el contador de una alternativa que desactiva colocaciones, no un nuevo resultado aprobado de la sala. V04B sigue teniendo 128. No hay nuevas relaciones de cruce con arquitectura ni cruces propios entre los módulos activos y otros bancos. Las excursiones máximas del clasificador para #206 son 9,816 mm en A, 10,791 mm en B y 6,839 mm en C; son medidas entre triángulos, no profundidades volumétricas exactas. Ninguna de estas cifras acredita un encaje resuelto.

También se ensayaron **328 poses restringidas** en dos casos representativos: dos lateralidades, dos referencias de orientación (media de centros o cuerda de jambas cercanas) y 41 desplazamientos normales entre −40 y +40 mm. Ninguna quedó libre de cruces en ese conjunto de pruebas. Los mejores casos todavía cruzan un objeto y desplazan el centro unos 66–68 mm; **no se han trasladado al modelo ni se consideran soluciones justificadas**. El ensayo acota estas alternativas, no demuestra la imposibilidad de cualquier rediseño.

Las vistas aisladas y las secciones permiten leer bordes desdoblados, diferencias de junta y lateralidad. Se comparó además P01 con EEVEE y nodos originales. La apariencia más limpia de un módulo aislado no resuelve la unión con bastidores, paredes y remates. Falta fijar una referencia común de jambas y elegir la lateralidad conforme al diseño, o justificar una revisión local del marco. No se ha supuesto que #206 sea otra puerta funcional ni se le ha inventado una apertura.

### Las 20 incidencias de Component#50

Se revisaron **16 tapas físicas que agrupan 20 encuentros**, con vista superior y lateral de cada una y cuatro muestras adicionales en EEVEE. El catálogo siguiente enlaza los identificadores de lámina con cada incidencia:

| Lámina | Objeto de tapa | Incidencias |
| --- | --- | --- |
| T01 | `C01_Banco_A_Original_3844_Component#50` | `I00133` |
| T02 | `C01_Banco_A_Original_3845_Component#50` | `I00134` |
| T03 | `C01_Banco_A_Original_3846_Component#50` | `I00135` |
| T04 | `C01_Banco_A_Original_3847_Component#50` | `I00136`, `I00137` |
| T05 | `C01_Banco_B_Espejo_3844_Component#50` | `I00278` |
| T06 | `C01_Banco_B_Espejo_3845_Component#50` | `I00279` |
| T07 | `C01_Banco_B_Espejo_3846_Component#50` | `I00280` |
| T08 | `C01_Banco_B_Espejo_3847_Component#50` | `I00281`, `I00282` |
| T09 | `C02_Banco_A_Original_3844_Component#50` | `I00350` |
| T10 | `C02_Banco_A_Original_3845_Component#50` | `I00351` |
| T11 | `C02_Banco_A_Original_3846_Component#50` | `I00352` |
| T12 | `C02_Banco_A_Original_3847_Component#50` | `I00353`, `I00354` |
| T13 | `C02_Banco_B_Espejo_3844_Component#50` | `I00426` |
| T14 | `C02_Banco_B_Espejo_3845_Component#50` | `I00427` |
| T15 | `C02_Banco_B_Espejo_3846_Component#50` | `I00428` |
| T16 | `C02_Banco_B_Espejo_3847_Component#50` | `I00429`, `I00430` |

Se trazaron 300 rayos elevados, cinco puntos por incidencia desde tres vistas. **68 rayos no tienen una ocultación previa de al menos 2 mm y las 20 incidencias tienen algún punto potencialmente expuesto.** El resultado complementa los rayos a altura de personaje de V04B; no los contradice. Los encuentros empiezan aproximadamente en Z=2,994498 m, por encima de la cápsula ensayada.

Se detectan además solapes proyectados de triángulos casi horizontales cuya separación vertical local es inferior a **0,1 mm**. Su suma de áreas proyectadas es 0,346969 m², con máximo por incidencia de 0,034149 m². Esa suma incluye dobles caras y solapes entre triángulos: **no es un área de unión ni una cantidad de material que deba eliminarse**. Las imágenes muestran encuentros y transparencias de referencia; no se ha probado parpadeo temporal ni se interpreta la transparencia de Workbench como el acabado final de UE5.

Las 20 incidencias continúan como **revisión manual de remate con posible interferencia visual desde arriba**. Propuesta local: decidir primero si la tapa pasa por encima de la pared o termina en el revestimiento y qué pieza aporta la cara visible; después ajustar únicamente el borde o la cara interior redundante de ese encuentro en una copia. No se ha ejecutado un recorte porque falta esa decisión constructiva. No se cierran globalmente mallas abiertas ni se retiran tapas para despejar un contador.

### Conservación y ausencia de regresiones en las alternativas

Las tres variantes se reabrieron desde disco y se compararon independientemente con V04B:

- **229 bloques de malla idénticos**, incluyendo vértices, aristas, polígonos, suavizado, asignación material y UV. Se mantienen los **16.800 objetos** de V04B; A/B no añaden objetos y C añade ocho propuestas. Todos los objetos originales conservan matrices, parentesco y datos; solo cambian los vínculos a colecciones de los #206 archivados.
- **101 materiales** iguales en colores, alpha, nodos, valores de entrada, enlaces e imágenes. Los dos bloques `FILE` empaquetados, sus rutas, dimensiones y hashes son iguales. Cero bibliotecas externas y ninguna referencia a rutas experimentales para abrir los modelos.
- Las matrices de las dos hojas y los revestimientos coinciden en **1, 20 y 60**; las seis curvas conservan claves y valores con interpolación lineal. Se repitió en cada variante el barrido conservador continuo del movimiento completo, con **cero parejas potencialmente solapadas de cajas de triángulos**.
- Se mantienen **once rutas interiores y la ruta exterior abierta** para la cápsula provisional de diámetro 0,70 m y altura 1,80 m, base Z=0,37 m. La prueba de regresión utiliza la igualdad exacta del entorno restante: A/B solo desactivan módulos; en C los ocho módulos nuevos ni siquiera solapan las cajas de las 12 rutas ampliadas por la cápsula. Por tanto se conserva, sin omitir hojas, el certificado V04B de los 329 intervalos exteriores abiertos. No se declara una nueva simulación completa de personaje ni se presenta un muestreo de poses como prueba continua.
- La auditoría de contactos recalcula los ocho módulos activos frente a **toda la arquitectura y los vecinos de banco candidatos** de cada variante, incluidos cruces banco/banco. Se preservan por igualdad de geometría las restantes 96 relaciones de cruce; no se ha fingido una nueva ejecución integral sobre componentes sin cambios. No se detectan nuevas relaciones de cruce propias en el subsistema estudiado.
- Los **72 solapes ocultos condicionales**, los cuatro encuentros #41 y las 20 incidencias #50 conservan exactamente geometría y colocación. No se amplía su aprobación ni se modifica su clasificación silenciosamente.
- **13 archivos protegidos** al inicio conservan tamaño y SHA-256: fuentes, entregables anteriores incluida V04B y blueprint. No se sobrescribe ni elimina material anterior.

### Láminas, archivos y reproducción

El cuaderno local `Revision_visual_Enterprise_G_V04C_02.pdf` contiene **14 láminas A3 apaisadas y 90 imágenes seleccionadas**: sala completa y planta completa de ambos círculos; perfiles de las ocho parejas; comparación base/A/B/C para cada una; vistas superiores y laterales de las 16 tapas con sus 20 IDs; muestras EEVEE; puerta cerrada y abierta; interiores y secciones técnicas. Los PNG de detalle son de 2.400 × 1.800 píxeles, los generales de 3.200 × 2.400 y las muestras EEVEE de 1.800 × 1.350. El PDF se renderizó con Poppler y sus páginas se revisaron visualmente.

Las secciones Z=2,80 m, el azul/naranja de los perfiles y las cámaras o luces de diagnóstico solo existen en escenas transitorias de render. No se guardan como sustituciones de materiales o arquitectura en V04B ni en las alternativas. Workbench muestra materiales de referencia; las ocho muestras EEVEE usan los nodos originales. Se conserva el primer montaje PDF como borrador y se identifica la revisión `_02` como entrega visual por incluir la planta sin recortar. Los ensayos de encuadre sin información útil no se incluyen en la selección.

| Modelo local de diagnóstico | Bytes | SHA-256 |
| --- | ---: | --- |
| `V04C_DIAG_A.blend` | 3898972 | `4636bedd3780ba979c30921b4f2f1ef7961607b51d9eeb1b926274174d92ae12` |
| `V04C_DIAG_B.blend` | 3898031 | `f4cfe48dd24a747ea2607b3dc53d3552374c36433ee203bafa25ce45108ec652` |
| `V04C_DIAG_C.blend` | 3897101 | `de70c845101378e08cf9cffb4913916fd09685673b9a95dc4bbd07679ddc13fe` |

El [generador reutilizable de variantes V04C](../../tools/blender/valhalla_supercomputadora_v04c_variantes.py) valida el hash de entrada, exige directorios nuevos o vacíos, conserva originales, verifica sus estados y firmas y escribe archivos con el prefijo explícito `DIAG`. Usa únicamente el módulo permanente V04 situado a su lado; no depende de scripts ni datos experimentales. No produce una V04C aprobada.

```text
blender --background --factory-startup --python-exit-code 1 --python desarrollo/tools/blender/valhalla_supercomputadora_v04c_variantes.py -- --input V04B.blend --output-dir NUEVO_DIRECTORIO_LOCAL --evidence-dir NUEVA_EVIDENCIA_TEMPORAL_AUTORIZADA
```

| Evidencia local | Contenido | SHA-256 |
| --- | --- | --- |
| `cadena_skp_206.json` | Origen SKP y correspondencia de matrices | `90b0c8f8c99767dc971cd1b64555e7a6ead53d0b43cf52dea79cbfd1eacd88e6` |
| `parejas_206_estudio.json` | Geometría, implantación y vínculo con las 32 incidencias | `827fa23676933560a5d3c7bc545334a00cb1a98988396b905cea6758e4f67a6d` |
| `ajustes_206_diagnostico.json` | 328 poses restringidas ensayadas, ninguna aprobada | `2ff1de575d7cc0dafb0482f8b09ce658b87886b701f92f9aa4f572f9fb6a7fc9` |
| `remates_20_revision.json` | 20 encuentros, rayos elevados y solapes proyectados | `4487f02aeaf182150c82079e2bdfba476750a98b315cc8f3d3900cf1a0460a34` |
| `auditoria_variantes_v04c.json` | Reapertura, conservación, barridos, rutas y cruces activos | `91adf3d3456ef7c68e00cae85ce60dd6bc086ae065844749b13fc81b4f020f6c` |
| `integridad_originales_final.json` | 13 archivos originales protegidos sin cambios | `bfca7dff9e0c5257fac88e6c54be7253e8782ad926783f54bfacb83dd4edd33a` |
| `catalogo_imagenes.json` | Catálogo de renders, motores, cortes y resolución | `a481b63632cdd69af4d191e4ea2d63a7fe8bca5c5b0a1807315946b680416c42` |
| `Revision_visual_Enterprise_G_V04C_02.pdf` | 14 láminas A3, 90 imágenes seleccionadas | `74df230887ef02938e4b554294c25504560e3f664782ab24121d55ddfc4944a5` |

Las evidencias se identifican por nombre y hash sin crear vínculos permanentes a rutas experimentales. Modelos, imágenes, PDF, dependencias del lector y datos brutos permanecen excluidos de Git. La publicación comprende únicamente este informe y el generador reutilizable. El juego y los archivos definitivos no dependen del área de diagnóstico, que no se ha borrado.

### Pendientes y límites

**Para revisión visual del diseño:** elegir lateralidad y referencia de jambas de #206; resolver sus encuentros con arquitectura sin movimientos arbitrarios; definir la continuidad y propiedad de las caras de #50; aprobar cualquier intervención local antes de considerarla la nueva base válida. Las tres alternativas son útiles para esa comparación, no una elección realizada en nombre del usuario.

**Realizado en Blender:** procedencia SKP/Blender, medidas, variantes reversibles, comparación visual, conservación, contactos triangulares y continuidad geométrica de las pruebas de puerta y rutas.

**Pendiente en Unreal Engine 5:** colisiones simples y soporte del personaje, funcionamiento y seguridad de puertas, controladores, navegación, materiales y estabilidad temporal, iluminación y rendimiento. La evidencia Blender no demuestra estas prestaciones.

**La sala continúa PARCIAL. PR #79 en borrador y sin fusionar. V04B se conserva como último estado válido.**


## Continuación V04D — Prototipos constructivos de P01 y T01

**Resultado: cuatro prototipos reversibles, todavía sin aprobar.** Se recomienda para revisión **P01 A adaptado** y **T01 continua sobre el apoyo**. La preferencia combina conservación de la colocación, menor intervención, distancia física y continuidad del acabado; no se basa solo en la vista frontal ni en un contador de cruces. No se genera una sala definitiva V04D y no se modifica el último modelo válido, `Sala_Supercomputadora_Valhalla_Puertas_V04B.blend`, SHA-256 `bb18697813040754122f5595f1d13d7eb93705828438e75a497cf460b251babd`.

### P01: propiedad de la unión y procedencia

P01 corresponde a `C01_Banco_A_0840_1921`, las dos colocaciones completas `C01_Banco_A_Original_0840_Component#206` y `C01_Banco_A_Original_1921_Component#206`. Sus jambas pertenecen a las instancias `Component_464607.001` y `Component_464607.004` de `Component#200`. Se conserva la continuidad de ambas arquitecturas y de sus sectores vecinos.

La cadena de SketchUp estudiada en V04C contiene la misma definición `Component#206`, recurso `mesh_20`, repetida con transformaciones de sector y reflexión. No hay capas ni atributos que demuestren funciones distintas. La separación de unos 8,17 mm y el giro de 2,89545° son heredados. Esto es compatible con redundancia al compartir una frontera; **no demuestra documentalmente que su creación fuese accidental**.

La propuesta asigna la unión a **un único módulo compartido P01, en una colección bajo la raíz**, en vez de conservar un módulo activo por cada sector. La arquitectura conserva la propiedad y posición del hueco; el marco del módulo se adapta a sus retornos y cabecera. El candidato A conserva exactamente la colocación 0840; B conserva la 1921. No se utiliza una pose intermedia ni se desplazan las jambas.

### P01: adaptación del marco y medida real

Conservar solo A o B sin adaptar su geometría deja dos cruces con arquitectura. Los prototipos ajustan su contorno a **45 planos medidos de los retornos y la cabecera**, incluidos contactos que no eran cruces propios. Se mantiene el apoyo inferior y se conserva la matriz de la colocación. La banda de ajuste conserva el borde y se desvanece entre **20 y 45 mm** desde el contorno. No cambia la escala general ni se estiran los paños acristalados.

| Propuesta P01 | Fuente retenida | Vértices de fuente adaptados | Ajuste máximo | Mínimo físico frente a las jambas | Cruces propios del módulo con arquitectura |
| --- | --- | ---: | ---: | ---: | ---: |
| A, preferente para revisión | 0840 | 184 | 10,230285 mm | **1,320705 mm** | 0 |
| B, alternativa con menor margen | 1921 | 178 | 12,807166 mm | **0,888805 mm** | 0 |

Los vidrios con material `openskp_material_25.001` no reciben deformación del ajuste. El marco y pequeños remates superiores con materiales 15/26 acompañan la adaptación, estos últimos hasta unos 2 mm, conservando sus asignaciones y UV. Los dos objetos completos originales permanecen archivados dentro de cada archivo; sus mallas no se editan.

La adaptación requiere cambiar diagonales de triangulación de **tres pares de caras en A y dos en B**. Se limita a vecinos coplanares con el mismo material, suavizado y UV continuas. Se conservan los vértices del contorno y sus coordenadas UV; el error máximo de la comprobación afín es inferior a **0,0000231 unidades UV**. Las mallas reabiertas tienen cero inversiones respecto a sus caras de procedencia, cero triángulos degenerados y cero triángulos coincidentes exactos de superficie positiva dentro del módulo privado.

**Los 2 mm de diseño no son una holgura mínima uniforme.** Son el desplazamiento nominal respecto de los planos de ajuste. La medida final recorre **148 facetas próximas de las dos arquitecturas**, incluidos sus biseles, usando distancias vértice/cara, arista/arista e intersección segmento/cara. Excluye únicamente las superficies enteramente bajo la base Z=0,37 m, con 0,1 mm de tolerancia de selección. La búsqueda de parejas utiliza cajas de triángulos ampliadas 15 mm, que cubren cualquier pareja más próxima que esa distancia.

| Testigo de distancia mínima | Triángulo del módulo privado | Arquitectura | Triángulo de arquitectura |
| --- | ---: | --- | ---: |
| A, 1,320705 mm | 155 | `Component_464607.001` | 730 |
| B, 0,888805 mm | 154 | `Component_464607.004` | 728 |

Los cortes de puntos críticos pasan por los segmentos de distancia mínima y muestran sus extremos 3D. Los cortes horizontales a Z=1,50 m son otra medida: su cota tangencial no se sustituye por el mínimo espacial. Si el plano de cota no atraviesa el borde inclinado de B se indica **sin cruce de cota**, sin inferir una distancia de centenares de milímetros a partir de otro punto del panel.

**Se recomienda A** porque requiere menos cambio y mantiene más separación real. La junta es variable; si se exige un mínimo de 2 mm en todas las facetas, ambos prototipos necesitan todavía un ajuste localizado de los biseles correspondientes. Esta decisión queda visible para aprobación del diseño. Los módulos permanecen estáticos y cerrados: no se inventa un mecanismo de apertura ni se acredita un paso funcional por #206.

En el subsistema P01, las cuatro relaciones de cruce banco/arquitectura `I00045`, `I00046`, `I00097`, `I00098` y la pareja banco/banco superpuesta dejan de estar activas en cualquiera de las copias. No aparecen relaciones nuevas frente a arquitectura o vecinos. Esto no cambia el contador de la V04B intacta ni resuelve las otras siete parejas.

### T01: dos soluciones reales de remate

T01 es `C01_Banco_A_Original_3844_Component#50`, incidencia `I00133` con `Component_466088.001`, definición `Component#202`. Se estudian tapa, pared, revestimiento y soportes, incluidas las caras inferiores inclinadas que impiden interpretar toda proyección de cubierta como una columna maciza.

| Solución T01 | Propietario constructivo | Ejecución en copia | Resultado medido |
| --- | --- | --- | --- |
| TERMINA contra revestimiento | La arquitectura define el límite del remate | Tapa separada 2 mm en planta; 38 retornos locales explícitos, triangulados en 76 caras, con material blanco original | Mínimo en planta **1,999850 mm**; superficie superior común con el apoyo **0 m²**; arquitectura intacta |
| CONTINUA sobre apoyo, preferente para revisión | La tapa aporta el acabado superior sobre el apoyo | Se sustraen superficies interiores de tapa y de una copia privada del revestimiento; se conservan sus rebajes inclinados | Superficie superior común entre componentes **0 m²**; no se añaden caras al apoyo ni posiciones artificiales |

Antes del ajuste, la intersección de las proyecciones de las superficies superiores era **0,029532510 m²**. Esta es un área de unión de huellas, distinta de la suma de áreas triangulares con dobles caras de V04C. TERMINA reduce la superficie superior de tapa de 28,925917005 a **28,866036649 m²**, una pérdida local de **0,059880357 m²** incluyendo la junta. Solo se construye el retorno de ese nuevo corte; no se cierran otras aberturas originales.

CONTINUA conserva **28,925916857 m²** frente a 28,925917005 m² de referencia: diferencia numérica de aproximadamente **0,148 mm²**. La distancia mínima entre proyecciones de las superficies superiores adyacentes es **1,536 micras**, un residuo numérico del encuentro y no una junta funcional diseñada. La propiedad del acabado evita dos superficies superiores activas solapadas. Las caras verticales internas se retiran hasta la cubierta; la exención se limita a sus caras superiores horizontales.

El reparto de superficies usa huellas y prismas locales, con condiciones adicionales para las caras inferiores inclinadas del apoyo. Después se comprueba la geometría 3D real. No se interpreta el clasificador de cruces como una prueba de volumen de sólidos cerrados. Para la continuidad, las caras retenidas de tapa y apoyo son **fragmentos de superficies originales**, con UV interpoladas: se verificaron 5.070 vértices de superficie en TERMINA y 4.551 + 6.495 en CONTINUA. Error de pertenencia al triángulo fuente inferior a 9 × 10⁻¹⁵ m y de interpolación UV inferior a 4 × 10⁻¹³ antes de serializar.

CONTINUA cambia solo la referencia de colección de **una instancia** de #202 hacia una copia privada. La definición compartida por otros sectores permanece intacta. La tapa continua respeta mejor el acabado superior de referencia; TERMINA sigue siendo una opción si se prefiere una junta visible. **Se recomienda CONTINUA para revisión**, sin aprobarla ni extenderla al resto de tapas.

### Contactos heredados que no se ocultan con el resultado

Las dos soluciones eliminan el cruce de T01 con arquitectura sin nuevas relaciones de cruce. Se conservan **42 relaciones ya presentes entre tapa y componentes del banco**, principalmente 19 con #34, nueve con #30 y cinco con #36, además de #41 y otros detalles. No se presentan como 42 correcciones ni se mezclan con las 128 incidencias banco/arquitectura. No se emite una aprobación nueva de todos esos encuentros.

La tapa fuente también contiene **75 parejas de triángulos coincidentes con normales opuestas**, siempre con los materiales `openskp_material_27.001` y `openskp_material_28.001`. Sus centros están como mínimo a 0,271 m de la huella del revestimiento. Ambas propuestas conservan esas caras de anverso/reverso. Son una cuestión de representación heredada y separada de la superposición tapa/pared resuelta aquí; su tratamiento de material y colisión en UE5 sigue pendiente. Los contadores triangulares de coincidencia pueden variar al fragmentar la malla del apoyo y no equivalen a nuevos encuentros geométricos.

### Conservación, regresiones y tolerancia numérica

Las cuatro copias seleccionadas se reabrieron desde disco y se compararon con V04B:

- **229 mallas originales y 16.800 objetos previos conservados.** Las modificaciones geométricas están en mallas privadas; los originales de banco se archivan con sus vínculos anteriores. A/B y TERMINA añaden una malla y un objeto; CONTINUA añade dos de cada uno. Las matrices originales se conservan; los cambios de colección son únicamente los necesarios para esas sustituciones reversibles.
- **101 materiales y dos imágenes `FILE` empaquetadas idénticos**, incluidos valores de entrada, nodos, conexiones, colores, rutas y hashes. Se conservan todas las UV de los bloques originales. Las caras retenidas privadas mantienen material y suavizado; el error máximo de serialización UV es inferior a 0,0000153 y de posición respecto al plan es inferior a 0,477 micras. Cero bibliotecas externas.
- **18 archivos protegidos sin cambios de tamaño y SHA-256**, incluyendo fuentes, V04B, entregables anteriores, variantes y PDF de V04C. No se sobrescribe ni borra ninguno de ellos.
- Poses y curvas de las puertas **1/20/60 idénticas**, con interpolación lineal. El barrido continuo se vuelve a comprobar en cada copia, con cero parejas potencialmente solapadas de cajas de triángulos barridos.
- **Doce rutas libres preservadas** para la cápsula provisional de diámetro 0,70 m y altura 1,80 m, base Z=0,37 m. Las regiones de geometría nueva de banco quedan fuera de sus cajas ampliadas; el apoyo privado solo pierde superficies. Se conserva el certificado exterior V04B de 329 intervalos libres con hojas reales. No se afirma una nueva simulación completa de personaje ni soporte de la planta del pie.
- Los componentes de los **72 solapes ocultos condicionales** no se editan. Se vuelven a clasificar las nueve relaciones de esas familias que usan el apoyo privado: **todas conservan su cruce**. Las demás arquitecturas no cambian. Las otras siete parejas #206 y otros 19 encuentros de tapa quedan fuera de la intervención.
- Las mallas privadas serializadas tienen **cero caras invertidas y cero triángulos de área nula** en la auditoría. Se registran y omiten fragmentos con altura menor de **1 micra tras convertir a float32**, para no conservar restos numéricamente inestables. Las áreas omitidas suman aproximadamente 0,257 mm² en A, 0,425 mm² en B, 2,603 mm² en TERMINA y 10,974 mm² entre las dos piezas de CONTINUA. No es un recorte global del modelo ni una pérdida de los originales archivados; tampoco certifica estanqueidad de la topología importada.
- **Once pruebas analíticas aprobadas**: sustracción interior/exterior, área y UV de cortes, propiedad de caras coplanares, altura, invariancia por movimiento rígido, tratamiento de líneas sin volumen, borde interior inmóvil y distancias reales entre triángulos, incluido un cruce por el interior de una cara.

### Comparativa visual y archivos locales

La entrega visual de referencia es **`Enterprise_G_V04D_Comparativa_Constructiva_r02.pdf`**, con **12 láminas A3, 43 imágenes y 11 cortes vectoriales**. Incluye planta con localizadores P01/T01; frontal, lateral, superior, posición de personaje, detalle de junta, nodos originales en EEVEE y sección de cada estado; cortes a escala y puntos críticos con las distancias físicas reales.

Las vistas no se limitan a módulos aislados: las seis cámaras de cada estado utilizan la **escena arquitectónica completa**. Las secciones cortan temporalmente a Z=1,50 o 3,65 m y conservan el contexto próximo. Las cubiertas y paredes ocultan el detalle desde algunas cámaras reales; esa oclusión se señala y se complementa con cortes, sin fingir que una vista frontal demuestra el encaje. Los renders son de 2.400 × 1.800 píxeles; los cortes del PDF son vectoriales. Se renderizaron y revisaron las páginas con Poppler.

| Modelo experimental seleccionado | Bytes | SHA-256 |
| --- | ---: | --- |
| `V04D_PROTO_P01_A_r07.blend` | 3.921.081 | `dcae1df9d539b3209c793014a820114d7f40933288534e7ab73802cc2503df87` |
| `V04D_PROTO_P01_B_r07.blend` | 3.919.134 | `e4a4ac72895b094e142dd22ddfadeb358d8e9ea38a4f47c27a4ff89f05b56b60` |
| `V04D_PROTO_T01_TERMINA_r03.blend` | 3.970.922 | `d193952b6c3f86da8ee05597f03460bf80a7043286db3f8850a7a72983ce6685` |
| `V04D_PROTO_T01_CONTINUA_r06.blend` | 4.032.368 | `25947162031439e3815c2725f52f62012d3dfa968b3a73143518dbb72c2b2063` |

Todos mantienen el estado de **prototipo no aprobado**. Los originales de banco están en `V04D_ORIGINALES_REFERENCIA_NO_ACTIVA`; `V04D_colecciones_previas` registra sus vínculos para restaurarlos. En CONTINUA, la propiedad `V04D_coleccion_original` de la instancia del apoyo permite recuperar su definición anterior. También se conserva una copia exacta de V04B. Las iteraciones y borradores anteriores permanecen como historial local; el índice identifica exclusivamente los archivos seleccionados y la revisión visual `_r02`.

### Código reutilizable y evidencia

La [biblioteca de geometría constructiva](../../tools/blender/valhalla_constructive_geometry.py) proporciona adaptación de borde, reparación de diagonales con UV continuas, prismas por huella, sustracción de superficies con atributos y distancias reales entre triángulos. Lee datos explícitos y no modifica escenas, rutas, visibilidad o archivos. La selección de propietarios, el alcance y la auditoría siguen siendo responsabilidad del llamador; no es un reparador automático de sólidos arbitrarios.

Las [pruebas analíticas reutilizables](../../tools/blender/tests/test_valhalla_constructive_geometry.py) se ejecutan con NumPy y Shapely ≥2.1; se utilizó Shapely 2.1.2 con Blender 5.2.2. Estos módulos permanentes no dependen de archivos experimentales. Los modelos pueden abrirse sin esos paquetes: contienen sus mallas e imágenes empaquetadas. La separación por huellas emplea las operaciones documentadas de [buffer de Shapely](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.buffer.html); las cotas físicas se calculan sobre las superficies, sin reemplazarlas por los planos de ajuste.

```python
fitted = fit_border(vertices, basis, center, planes,
                    gap=0.002, full_band=0.020, zero_band=0.045)
actual_gaps = triangle_surface_gaps(triangle, neighbouring_triangles)
```

```text
python -B desarrollo/tools/blender/tests/test_valhalla_constructive_geometry.py
```

| Evidencia local | Contenido | SHA-256 |
| --- | --- | --- |
| `prototipos_finales.json` | Selección explícita de cuatro prototipos, archivos y hashes | `f63d329451b7e0a2392400a2135784321ea2e4fb0815b66359d1db497cba2b7e` |
| `auditoria_final.json` | Reapertura de las cuatro soluciones; datos, contactos y regresiones | `3e0810195fc942075c7e58aee3a3d430d8606f590ba6ff9fd552cf0dedb6b646` |
| `holguras_jambas_completas_r07.json` | Distancia física frente a 148 facetas, con testigos | `7c10d8a31a5de7461ee5dd5374d6d1067e40246f1eb70a01ed97b8b61b1384a3` |
| `cortes_criticos.json` | Puntos 3D y planos de los dos cortes de mínima separación | `32d51986bea6609e8f78bd8f9281745031dd3632b248665fda9ba61b699186e4` |
| `conservacion_superficies.json` | Procedencia de superficies/UV y 75 parejas de anverso/reverso | `c5eb1b29b125e9ef20242cc50e8a02a51dd2f23f303559924399c55fb4175e8f` |
| `integridad_final.json` | 18 archivos protegidos sin cambios | `3e42cfab902c3d7a34c6440ef5ee54c667b4314b36552ee16cd5cdae46ccebc5` |
| `pruebas_11_geometria.log` | Once comprobaciones analíticas aprobadas | `35f97ba38d738fc0bc90ee00bd2b233895c6412cebf0f8dd00a56ea72f0e3017` |
| `catalogo_imagenes.json` | Cámaras, motores y resolución de 63 renders de proceso | `e1bca453cc0f82b3e2f90378f8ce10c7d952a73843e23611cb97f8fb4d9e0451` |
| `Enterprise_G_V04D_Comparativa_Constructiva_r02.pdf` | 12 láminas A3, 43 imágenes y 11 cortes vectoriales | `60c1d47b7890af0aea135888ad25256194776a87067addc7c9b10d733a69c974` |

Los nombres y hashes identifican la ejecución sin insertar rutas experimentales como dependencias permanentes. Modelos, PNG, PDF, datos, registros y dependencias de cálculo permanecen ignorados por Git. Se publican únicamente este informe, la biblioteca y sus pruebas. No se ha eliminado material anterior ni se ha creado otro árbol de proyecto.

### Decisiones restantes y separación de Blender / UE5

**Para aprobar una solución de diseño:** elegir lateralidad de P01 y aceptar su junta variable, o exigir una adaptación adicional de los biseles para un mínimo uniforme; elegir tapa continua o remate con junta; revisar la representación de las caras opuestas heredadas antes de exportar. La preferencia A/CONTINUA queda documentada como candidatura, no como aprobación del usuario.

**Comprobado en Blender:** encaje localizado, fuente y propiedad de las uniones, conservación de poses, geometría reversible, vistas con entorno, medidas sobre facetas reales, contactos y regresiones geométricas de puertas y rutas.

**Pendiente en UE5:** colisiones simples, soporte y controlador de personaje, navegación, puertas y enclavamientos, materiales de dos caras, iluminación, estabilidad temporal y rendimiento. No se implementa movimiento de #206 ni se declara terminada la sala.

**La sala sigue PARCIAL. V04B permanece como última base válida; PR #79 abierta, en Draft y sin fusionar.**
