# Geometría, arquitectura y escala

## Recuentos reproducidos

| Archivo/método | Objetos | Mallas | Vértices almacenados | Triángulos Blender | Materiales datablock | Mallas con UV |
|---|---|---|---|---|---|---|
| Colección GLB importada | 488 | 317 | 99615 | 67548 | 8 | 317/317 |
| Colección BLEND nativo | 189 | 83 | 90891 | 71738 | 9 | 83/83 |
| OBJ original separado | 630 | 630 | 254270 | 271705 | 102 | 630/630 |
| OBJ BLEND fusionado | 1 | 1 | 254270 | 271705 | 103 | 1/1 |
| Puente GLB texturizado | 1 | 1 | 255754 | 271705 | 102 | 1/1 |
| BLEND Recovery completo (MAX + OBJ) | 643 | 632 | 438967 | 533138 | 171 | 591/632 |

La colección contiene **488 nodos / 317 mallas / 317 primitivas glTF**, **99.615 vértices por suma de primitivas** y **67.563 triángulos almacenados**. Blender valida 15 caras duplicadas de índices y conserva 67.548. Son diferencias de método, no elementos desaparecidos. El `.blend` nativo contiene 189 objetos, 83 mallas y 71.738 triángulos calculados desde polígonos; su triangulación no es idéntica a la exportación glTF. No se certifica equivalencia cara por cara.

El OBJ crudo tiene 254.270 posiciones, otras tantas UV/normales, 630 grupos y **271.911 caras triangulares**. Hay 206 tripletas duplicadas dentro de su mismo grupo; la importación temporal validada conserva 271.705. El BLEND fusionado tiene el mismo recuento de triángulos; el GLB texturizado tiene **1 nodo, 1 malla y 102 primitivas**, con 255.754 vértices por particiones de material/atributos. No son 102 objetos interactivos.

En Recovery no deben sumarse las dos versiones como si fueran una estancia: **631 mallas MAX, 184.697 vértices, 212.147 caras y 261.433 triángulos**, más el antiguo OBJ de 271.705 triángulos. La escena completa da 533.138 porque superpone ambas familias. Tiene 11 empties. Se verificó que el OBJ heredado está visible en el archivo cargado.

## Arquitectura del puente de colección

El grupo fuente `Group_52_1` contiene **8 objetos de malla**, con **3.213 triángulos Blender** frente a **3.183 almacenados en su subárbol GLB**. Siete piezas son principales y una es un residuo diminuto.

| Pieza fuente | Triángulos | Interpretación contrastada |
|---|---|---|
| Mesh103 | 1950 | Carcasa fusionada: planta, niveles, muros, volúmenes de consola y accesos |
| Mesh104 | 764 | Techo/domo, con nervios geométricos |
| Mesh98 | 184 | Barandilla central |
| Mesh99 / Mesh100 | 80 / 80 | Barandillas laterales |
| Mesh101 / Mesh102 | 77 / 77 | Barandillas y soportes |
| Mesh105 | 1 | Residuo de 1,3 × 1,9 mm, lejos de la carcasa |

La carcasa mide **18,017 × 18,241 × 3,780 m**; el techo, **13,935 × 13,935 × 0,979 m**. Es una envolvente reconocible, con suelo y techo reales, escalones/barandillas y accesos representados. Se observan volúmenes simples para puestos y pantalla frontal, pero no pantallas LCARS, controles detallados ni sillas. No se pueden asignar estaciones científicas/tácticas concretas por estos bloques blancos. Los cortes diagnósticos omiten caras por encima de Z=2,50 m; no confundir la falta de paredes altas en ellos con una ausencia original.

La arquitectura no es un sólido cerrado certificado: `Mesh103` se vuelve una sola isla conectada tras soldadura diagnóstica y no ofrece separación funcional entre puertas, suelos y carcasas. Cinco barandillas sí son objetos propios. La ausencia de un sólido watertight no implica por sí sola un defecto en un escenario de superficies abiertas.

## Arquitectura del puente detallado

Las vistas y las asignaciones confirman suelo, plataforma de mando, escalones, cerramiento curvo, techo, luminarias modeladas, pantalla principal, banco posterior de consolas, puestos laterales, puesto frontal, dos sillones centrales y tres asientos de estaciones. Hay puertas, controles de acceso y cabina circular. Los gráficos LCARS son **imágenes sobre superficies**, no botones o circuitos modelados uno a uno. Las carcasas, muebles, barandillas y geometría de luminarias sí existen.

En el OBJ hay separación recuperable por 630 grupos; en los derivados fusionados esa estructura no está presente como objetos. Se comprobó directamente `floorfront_1`: **613 triángulos y 32,829204 m²**, frente a la superficie mínima de la conversión MAX. El techo `Mainroof_1` tiene 14.452 triángulos. No se declara una estancia hermética ni sin huecos solo por su render; las uniones de accesos y la continuidad transitable necesitan una comprobación posterior por recorrido.

Distribución de triángulos por materiales del OBJ separado (es agrupación de caras, no identificación funcional automática):

| Material | Triángulos |
|---|---|
| Leather2 | 68392 |
| DimGray | 43330 |
| LightGr | 23136 |
| Material__53 | 19926 |
| wire_057008136 | 18635 |
| Color_H1 | 14379 |
| Color_00 | 11572 |
| Color_07 | 8438 |
| Charcoal | 7303 |
| wire_184228153 | 5528 |

`Leather2` suma **68.392 triángulos** en sillones/apoyabrazos (aprox. 25,2 % del puente). Cuatro apoyabrazos usan 1.500 cada uno. Hay margen de optimización artística; el presupuesto no depende solo del total del puente.

## Defectos y límites numéricos

- GLB de colección crudo: 0 índices fuera de rango, 0 posiciones no finitas en Blender, 1 triángulo de área local menor de 1e-10, 46 triángulos cuya normal media almacenada se opone al winding; no son 46 agujeros demostrados. Sus ocho materiales son double-sided, que puede ocultar orientación incorrecta.
- GLB detallado: 0 índices inválidos, 578 triángulos de área local menor de 1e-10 y 244 desacuerdos normal/winding. Las normales medidas no presentan longitudes alejadas de 1 en más de 0,01. No se aportan tangentes en el GLB; su generación y costuras deben revisarse al preparar normales.
- OBJ separado: **5.439 coincidencias triangulares adicionales** al cuantizar coordenadas mundo a 1e-5 m. La suma local por primitiva GLB es 5.368: el segundo método no ve coincidencias entre materiales. Algunas pueden ser capas/dobles caras intencionadas; no hay una clasificación exhaustiva de todas.
- Recovery MAX: `floorfront` tiene 593 vértices sin caras y área efectiva 0,000133254 m²; `Mesh1497` conserva 14 caras, 531 vértices sueltos y área parcial 7,854547 m². **No tiene cero caras**, corrigiendo la formulación abreviada de la auditoría histórica; sus datos detallados anteriores ya indicaban esas 14.
- `Mesh468` y `Mesh1206` tienen normales mundiales hacia −Z, área de unos 8,192385 m² cada uno y separación vertical de unos 8,017 mm. La cubierta actual opaca debe estudiarse antes de emisión.
- `Mesh992` y `Mesh993` de Recovery están fuera del conjunto principal, a Z≈15,6–18 m. `Mesh551` está vacío. No se borraron.

Los bordes abiertos brutos son muy sensibles a vértices partidos por UV/normales: la colección nativa baja de 90.110 bordes boundary a 4.007 al soldar una **copia bmesh** a 1e-6 unidades locales. Este diagnóstico no se guardó ni se propone como operación automática; soldar realmente podría destruir costuras. Los conteos no equivalen a huecos físicos. No se hizo una búsqueda exhaustiva de todas las intersecciones ni una prueba de malla cerrada navegable.

## Escala, orientación, orígenes e instancias

glTF expresa distancias en metros; Blender convierte el eje vertical Y de glTF a Z. La colección nativa declara sistema métrico, scale_length=1 y conserva un padre `Model` a escala 0,01. Su catálogo ocupa unos **153,253 × 68,010 × 6,422 m**; ese es el despliegue de piezas, no el tamaño de una cubierta ensamblada. Hay módulos de mantenimiento a Z≈3,28 m y un puente desplazado a X≈−43 m.

El OBJ separado mide **13,150 × 13,011 × 3,840 unidades interpretadas como metros**; OBJ no impone unidad física por norma. Sus dimensiones y asientos son compatibles como hipótesis de escala humana, pero no certifican todos los vanos ni alturas útiles. Un objeto de puerta concreto mide solo 1,616 m en Z; no debe usarse aisladamente para medir el vano completo. El ajuste de escala requiere un maniquí y la unión real de sus piezas.

La conversión MAX difiere: `Mainroof` / `Mainroof_1` arroja un cociente de aproximadamente **1,5081** en X/Y/Z; `hallwayfloor` tiene 15,999359 m² frente a 7,034308 en el OBJ. No asumir escalas equivalentes ni modificar una para forzar coincidencia. 520 mallas MAX tienen escala local distinta de uno. En el OBJ separado, los **630 orígenes están en (0,0,0)**: posiciones de geometría útiles, pivotes de animación todavía no.

En la colección, las mallas tienen un usuario de objeto cada una; las repeticiones visuales no son automáticamente instancias enlazadas. El JSON conserva usuarios y hashes de geometría para revisar duplicados. No se detectó rig ni animación utilizable en las variantes inspeccionadas. Un espacio de circulación no queda validado por una caja envolvente: los rayos de pasillo se detallan en el informe 06 y no equivalen a cápsulas.

Casos, gravedad y consecuencias: [DATOS/hallazgos.csv](DATOS/hallazgos.csv). Inventarios por objeto con área, vértices usados, materiales y cotas: [inventarios por componente](DATOS/README.md).

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
