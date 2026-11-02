# CATÁLOGO OFICIAL — Biblioteca modular Voyager → USS Enterprise-G (clase Valhalla)

> **Versión:** 1.0 · **Fecha de inventario:** 2 de noviembre de 2026 · **Ámbito:** biblioteca 3D local de corredores, accesos y mantenimiento.
> **Fuente:** árbol `tree /F` proporcionado por el propietario y clasificación visual realizada conjuntamente en Blender. Este documento **no** supone una auditoría automática del interior de los `.blend`.

## 1. Ubicación y alcance

**Carpeta raíz exacta en el MSI:**

```text
C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\PROYECTO VALHALLA\Cubiertas Enterprise G\Biblioteca modular de corredores
```

**Archivo maestro:** `Biblioteca_Voyager_Valhalla_MASTER.blend` (en esa raíz). Conservarlo como referencia; usar copias o los módulos individuales para montar la nave.

**Inventario comprobado por nombres de archivo:**

| Concepto | Cantidad |
|---|---:|
| Familias/carpetas presentes | 9 |
| Módulos individuales `.blend` | 58 |
| Archivo maestro `.blend` adicional | 1 |
| Copias automáticas `.blend1` | 7 |
| Archivos listados en total | 66 |

**Importante:** se respeta exactamente el árbol real: existen las carpetas 01, 02, 03, 07, 08, 09, 10, 11 y 12; las numeraciones 04–06 **no aparecen** y no se inventan. Las piezas pueden tener alias funcionales en las búsquedas, pero **sus archivos no se renombran** a partir de este catálogo.

## 2. Cómo usar este catálogo

1. Buscar una **necesidad en lenguaje natural** (p. ej., «escalera que salga por la izquierda» o «acceso de carga»).
2. Localizar el **identificador y archivo exactos** en el índice de funciones (sección 3) o en el inventario (sección 4).
3. Formar la ruta como `RAÍZ\CARPETA\ARCHIVO.blend` sin modificar caracteres, espacios ni guiones.
4. Abrir/copiar el `.blend` correspondiente e importarlo a un archivo de construcción; **no modificar el MASTER ni los originales**.
5. Verificar siempre escala, posición/orientación, geometría de unión, colisiones y transitabilidad; el catálogo refleja la identificación visual, no una certificación de encaje.

**Ejemplo de ruta real y literal:**

```text
C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\PROYECTO VALHALLA\Cubiertas Enterprise G\Biblioteca modular de corredores\09_Conductos_Jefferies\VY_JEF_008_Recto_Largo.blend
```

## 3. Índice práctico: qué pieza pedir según la necesidad

| Necesidad durante la construcción | Buscar primero | Observación |
|---|---|---|
| Corredor recto corto / medio / largo | `VY_REC_001` / `VY_REC_002` / `VY_REC_003` | `01_Rectos` |
| Curva de corredor grande / mediana / pequeña | `VY_CUR_001` / `002` / `003` | `02_Curvas` |
| Esquina de corredor a 90° | `VY_CUR_004` | Aunque su ID es CUR, vive en `03_Intersecciones` |
| Cruce de cuatro direcciones | `VY_INT_001` | `03_Intersecciones` |
| Cruce en T o bifurcación Y | `VY_INT_002` / `003` / `004` / `005` | Comparar variantes antes de elegir |
| Distribuidor general con isla o abierto | `VY_INT_006` / `VY_INT_007` | **No son exclusivos de holocubiertas** |
| Acceso lateral / doble acceso / vestíbulo sin salida | `VY_ACC_001` / `002` / `003` | Variantes Recessed |
| Vestíbulo con una o dos salidas Jefferies | `VY_ACC_004` / `005` / `006` | `006` incorpora controles |
| Pantalla / panel de información potencial | `VY_ACC_007` | Superficie rectangular; uso funcional pendiente |
| Acceso Jefferies integrado en pasillo principal | `VY_ACC_008` | Abertura lateral visible |
| Corredor etiquetado JT pero sin hueco de tubo visible | `VY_ACC_009` | **NO asumir que permite entrar en Jefferies** |
| Entradas de camarotes | `VY_HAB_001` / `002` | Asimétrica / simétrica |
| Puerta aislada, de turboascensor o de carga | `VY_PUE_001` / `002` / `003` / `004` | Comprobar hoja móvil antes de animar |
| Zona de controles técnicos de 6 o 4 paneles | `VY_TEC_001` / `002` | `08_Modulos_Tecnicos` |
| Tubo Jefferies recto corto / medio / largo | `VY_JEF_006` / `007` / `008` | `09_Conductos_Jefferies` |
| Tubo Jefferies tipo Slant 4° / giro 90° / T | `VY_JEF_001`–`005` | Confirmar dimensiones del tipo Slant |
| Marco de salida/entrada de tubo Jefferies | `VY_JEF_009` | Marco abierto, **sin hoja de puerta visible** |
| Escalera de mano entre cubiertas | `VY_VER_001` / `002` / `003` / `005` / `006` | Diferentes orientaciones de salida |
| Escalera compuesta de dos niveles | `VY_VER_004` / `007` | Inspeccionar unión de peldaños y cotas |
| Mantenimiento, giro 90° | `VY_MAN_001` / `008` | Dos variantes |
| Mantenimiento, unión en T | `VY_MAN_002` / `VY_MNT_006` | El segundo conserva prefijo MNT real |
| Pasillo técnico recto | `VY_MAN_003` / `004` / `007` | Dos variantes estándar y una larga |
| Marco/junta candidata de mantenimiento | `VY_MAN_005` | **Compatibilidad pendiente de comprobar** |
| Vestíbulo de turboascensor ancho / estrecho | `VY_TUR_001` / `002` | Small = más estrecho, no necesariamente menos largo |
| Cabina de turboascensor | `VY_TUR_003` | Funcionalidad de cabina y puertas pendiente |

## 4. Inventario exhaustivo por carpeta

Las columnas «Original identificado» y «Uso/observación» se basan en nombres e inspecciones manuales de la sesión de catalogación. Si figura **pendiente**, el dato no se verificó examinando internamente los archivos.

### 01_Rectos — 3 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_REC_001 — Recto Corto.blend` | `Hallway_Strait_Small1_89` | Corredor recto corto; ajuste fino de recorridos. |
| `VY_REC_002_Recto_Medio.blend` | `Hallway_Medium_Single1_73` | Corredor recto de longitud intermedia. |
| `VY_REC_003_Recto_Largo.blend` | `Hallway_Strait_large1_87` | Corredor recto largo para ejes principales. |

**Ruta de esta familia:** `01_Rectos\` (relativa a la raíz indicada en §1).

### 02_Curvas — 3 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_CUR_001_Curva_Grande.blend` | `Hallway_4__Degree_Circlar_Large1_53` | Curva amplia de corredor; referencia original a 4 grados. |
| `VY_CUR_002_Curva_Mediana.blend` | `Hallway_4__Degree_Circlar_Medium1_57` | Curva mediana de corredor; referencia original a 4 grados. |
| `VY_CUR_003_Curva_Pequeña.blend` | `Hallway_4__Degree_Circlar_Small1_61` | Curva corta de corredor; referencia original a 4 grados. |

**Ruta de esta familia:** `02_Curvas\` (relativa a la raíz indicada en §1).

### 03_Intersecciones — 8 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_CUR_004_Esquina_90.blend` | `Hallway_90__Degree_Turn1_65` | Codo de corredor a 90°. Conserva prefijo CUR, pero reside aquí. |
| `VY_INT_001_Cruce_4_Direcciones.blend` | `Hallway_4_Way_Junction1_63` | Cruce principal de cuatro direcciones. |
| `VY_INT_002_Cruce_T.blend` | `Hallway_T_Junction1_91` | Cruce de tres ramales en T. |
| `VY_INT_003_Cruce_T_Con_Puerta.blend` | `Sin origen original confirmado` | Variante en T con zona de puerta/panel; funcionalidad de puerta sin verificar. |
| `VY_INT_004_Seccion_T_1x2.blend` | `T__Section_Hallway___1x2_1_171` | Sección de distribución en T, variante 1×2. |
| `VY_INT_005_Bifurcacion_Y.blend` | `Group2_19 (Mesh2_18)` | Bifurcación de tipo Y; identificación del conjunto en el Outliner. |
| `VY_INT_006_Distribuidor_Isla.blend` | `Hallway_Primary_Secondary_Location___island___EG__Holodeck_1_75` | Distribuidor con disposición «isla», dos accesos laterales y paso central. Uso GENERAL; Holodeck solo figura como ejemplo en el original. |
| `VY_INT_007_Distribuidor_Abierto_Con_Pasillo.blend` | `Hallway_Primary_Secondary_Location___open___EG__Holodeck_1_77` | Variante abierta del distribuidor; circulación con paso de corredor. Uso GENERAL, no exclusivo de holocubiertas. |

**Ruta de esta familia:** `03_Intersecciones\` (relativa a la raíz indicada en §1).

### 07_Accesos_y_Camarotes — 15 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_ACC_001_Vestibulo_Grande_Salida_Lateral.blend` | `Recessed_Large___Single_Exit1_157` | Vestíbulo grande con una salida/puerta lateral. |
| `VY_ACC_002_Vestibulo_Grande_Doble_Salida.blend` | `Recessed_Large___Double_Exits1_141` | Vestíbulo grande con dos salidas laterales. |
| `VY_ACC_003_Vestibulo_Grande_Sin_Salidas.blend` | `Recessed_Large___No_Exits1_153` | Vestíbulo o remate sin salidas laterales. |
| `VY_ACC_004_Vestibulo_Acceso_Jefferies.blend` | `Recessed_Large___Single_JT_Exit1_159` | Vestíbulo con una abertura lateral pequeña tipo tubo Jefferies. |
| `VY_ACC_005_Vestibulo_Doble_Acceso_Jefferies.blend` | `Recessed_Large___Double_JT_Exit1_143` | Vestíbulo con dos accesos laterales tipo Jefferies. |
| `VY_ACC_006_Vestibulo_Doble_Jefferies_Controles.blend` | `Recessed_Large___Double_JT_Exit___Controls1_151` | Doble acceso a Jefferies y cuatro controles en pared. |
| `VY_ACC_007_Vestibulo_Sin_Salidas_Panel_Superior.blend` | `Recessed_Large___No_Exits___Top_Details1_155` | Vestíbulo sin salidas con zona rectangular superior susceptible de pantalla informativa; la función de pantalla no está acreditada. |
| `VY_ACC_008_Pasillo_Acceso_Jefferies.blend` | `Hallway_J_tube_Access_Single1_67` | Tramo de corredor normal con pequeña abertura lateral tipo Jefferies. |
| `VY_ACC_009_Acceso_JT_Cerrado_Grande.blend` | `Corridor___JT_Access___Large1_5` | Módulo de corredor etiquetado JT Access, PERO en inspección visual no se encontró abertura Jefferies visible. No asumir acceso practicable. |
| `VY_HAB_001_Acceso_Camarotes_Asimetrico.blend` | `Hallway_Residential_Quarters_Asymetrical1_79` | Variante de acceso/corredor de camarotes asimétrica. |
| `VY_HAB_002_Acceso_Camarotes_Simetrico.blend` | `Hallway_Residential_Quarters_Symetrical1_81` | Variante de acceso/corredor de camarotes simétrica. |
| `VY_PUE_001_Puerta_Rebajada_Grande.blend` | `Recessed_large_Door_Edge1_165` | Panel/puerta independiente de la familia Recessed; movimiento de hoja por comprobar. |
| `VY_PUE_002_Puerta_Carga_Grande.blend` | `Recessed_Large_Cargo_Type_Door1_161` | Módulo grande de acceso de carga con puerta aparente. |
| `VY_PUE_003_Puerta_Turboascensor.blend` | `Recessed_Large_Turbolift_Door_Edge1_167` | Panel aislado con puerta de tipo turboascensor; determinar posteriormente qué malla sería hoja móvil. |
| `VY_PUE_004_Puerta_Carga.blend` | `Recessed_Large_Cargo_Type_Door_Edge1_163` | Panel aislado de puerta de carga; no confundir con el módulo completo VY_PUE_002. |

**Ruta de esta familia:** `07_Accesos_y_Camarotes\` (relativa a la raíz indicada en §1).

### 08_Modulos_Tecnicos — 2 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_TEC_001_Control_Grande.blend` | `Recessed_ControlArea___Large1_133` | Alcoba/vestíbulo técnico grande con seis controles (3×2). |
| `VY_TEC_002_Control_Mediano.blend` | `Recessed_ControlArea___Medium1_139` | Alcoba/vestíbulo técnico mediano con cuatro controles (2×2). |

**Ruta de esta familia:** `08_Modulos_Tecnicos\` (relativa a la raíz indicada en §1).

### 09_Conductos_Jefferies — 9 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_JEF_001_Curva_4Grados_Larga.blend` | `J_tube_4__Degree_Slant_Long1_95` | Tramo largo marcado Slant 4° por la fuente; comprobar curva/inclinación y conexiones con medidas. |
| `VY_JEF_002_Curva_4Grados_Mediana.blend` | `J_tube_4__Degree_Slant_Medium1_97` | Tramo mediano marcado Slant 4°; geometría exacta por medir. |
| `VY_JEF_003_Curva_4Grados_Corta.blend` | `J_tube_4__Degree_Slant_Short1_99` | Tramo corto marcado Slant 4°; geometría exacta por medir. |
| `VY_JEF_004_Codo_90.blend` | `J_tube_90__Turn1_101` | Codo de Jefferies a 90°. |
| `VY_JEF_005_Interseccion_T.blend` | `J_tube_T__Section_Turn1_111` | Derivación de tres ramales, tipo T. |
| `VY_JEF_006_Recto_Corto.blend` | `J_Tube_Short1_109` | Conducto Jefferies recto corto. |
| `VY_JEF_007_Recto_Mediano.blend` | `J_Tube_Medium1_107` | Conducto Jefferies recto mediano. |
| `VY_JEF_008_Recto_Largo.blend` | `J_Tube_Long1_105` | Conducto Jefferies recto largo. |
| `VY_JEF_009_Marco_Acceso_Jefferies.blend` | `J_Tube_Access_hatch1_103` | Marco terminal poligonal ABIERTO, sin hoja de cierre visible; no clasificarlo como escotilla animada. |

**Ruta de esta familia:** `09_Conductos_Jefferies\` (relativa a la raíz indicada en §1).

### 10_Conexiones_Verticales — 7 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_VER_001_Conexion_Vertical_Subida_Bajada.blend` | `G_2_Way_Up_Dn_Junction1_11` | Nodo vertical con escalera de mano; subida y bajada. |
| `VY_VER_002_Conexion_Vertical_4_Direcciones.blend` | `G_4_Way_Up_Dn_Lt_Rt_Junction___With_Hallway_access1_13` | Nodo vertical con escalera y conexiones laterales; el original indica arriba/abajo/izquierda/derecha y acceso de pasillo. |
| `VY_VER_003_Mantenimiento_Vertical_Doble_Acceso.blend` | `Vertical_Maintenance_Double1_175` | Módulo vertical con escalera y dos accesos peatonales. |
| `VY_VER_004_Escalera_Vertical_Dos_Niveles.blend` | `Compuesto: Vertical_Maintenance_TSEC_2_1_181 + Vertical_Maintenance_TSEC_3_2_187` | Conjunto de dos piezas apiladas, dos niveles y continuidad aparente de escalera. Se propuso conservar las piezas separadas dentro del mismo .blend; encaje por medir. |
| `VY_VER_005_Escalera_Doble_Acceso_90.blend` | `Vertical_Maintenance_TSEC_1_1_179` | Módulo vertical con escalera y accesos peatonales en paredes a 90°. |
| `VY_VER_006_Escalera_Accesos_Opuestos.blend` | `Vertical_Maintenance_Double2_177` | Módulo vertical con escalera y accesos peatonales enfrentados. |
| `VY_VER_007_Escalera_Dos_Niveles_Salida_Lateral.blend` | `Compuesto: Vertical_Maintenance_TSEC_3_1_185 + Vertical_Maintenance_TSEC_2_2_183` | Dos módulos apilados: escalera inferior y continuación superior con salida lateral. Geometría y navegación entre alturas por verificar. |

**Ruta de esta familia:** `10_Conexiones_Verticales\` (relativa a la raíz indicada en §1).

### 11_Conductos_Mantenimiento — 8 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_MAN_001_Codo_Mantenimiento_90.blend` | `Maintenance_90Degree_113` | Módulo de mantenimiento con giro de 90°, variante A. |
| `VY_MAN_002_T_Mantenimiento.blend` | `Maintenance_T_Section1_125` | Sección de mantenimiento con derivación en T, variante A. |
| `VY_MAN_003_Pasillo_Mantenimiento_Recto_A.blend` | `maintenance_straight1_119` | Tramo recto técnico, variante A. |
| `VY_MAN_004_Pasillo_Mantenimiento_Recto_Largo.blend` | `Maintenance_Straight_Large_121` | Tramo recto técnico largo, detalles superiores amarillos. |
| `VY_MAN_005_Marco_Union_Mantenimiento.blend` | `Group_11_1_33` | Pieza auxiliar con posible función de junta o marco adaptador; encaje con VY_MAN_004 sin confirmar. |
| `VY_MAN_007_Pasillo_Mantenimiento_Recto_B.blend` | `maintenance_straight_117` | Tramo recto técnico, variante B. |
| `VY_MAN_008_Codo_Mantenimiento_90_B.blend` | `Maintenance_90Degree1_115` | Giro de mantenimiento a 90°, variante B. |
| `VY_MNT_006_Empalme_T.blend` | `Maintenance_T_Section_123` | Segunda sección/empalme en T. NOTA: el archivo usa prefijo MNT, distinto del prefijo MAN de esta familia. |

**Ruta de esta familia:** `11_Conductos_Mantenimiento\` (relativa a la raíz indicada en §1).

### 12_Accesos_Turbolift — 3 módulo(s)

| Archivo exacto (`.blend`) | Original identificado (catálogo Voyager) | Uso y observaciones |
|---|---|---|
| `VY_TUR_001_Acceso_Turbolift_Grande.blend` | `Corridor___Turbolift_access___Large1_7` | Vestíbulo/acceso ancho a turboascensor con numerosos paneles de pared. |
| `VY_TUR_002_Acceso_Turbolift_Estrecho.blend` | `Corridor___Turbolift_access___Small1_9` | Variante de acceso más ESTRECHA, no necesariamente más corta. |
| `VY_TUR_003_Cabina_Turbolift.blend` | `Turbolift1_173` | Cabina de turboascensor según catalogación; verificar piezas internas, puerta y geometría antes de su integración. |

**Ruta de esta familia:** `12_Accesos_Turbolift\` (relativa a la raíz indicada en §1).

## 5. Notas de identificación y advertencias que no debemos olvidar

- **Las descripciones son funcionales y provisionales.** Los archivos están presentes en el árbol, pero no se ha hecho una auditoría automática de mallas, dimensiones, UV, colisiones o encaje módulo a módulo.
- **`VY_ACC_009`:** aunque su fuente se llama `JT_Access`, durante la inspección se comprobó que **no se veía una abertura a Jefferies**. No recomendarlo como acceso practicable sin editar y validar la geometría.
- **`VY_JEF_009`:** tras observarlo de cerca resultó ser un **marco de acceso abierto**, no una escotilla con hoja móvil identificada.
- **`VY_PUE_003` y `VY_PUE_004`:** son paneles/puertas aislados, pero todavía no se ha determinado qué mallas corresponden a hojas animables.
- **`VY_INT_006` y `VY_INT_007`:** el nombre Voyager menciona Holodeck a modo de ejemplo. Su utilidad es la de distribuidores de **uso general**.
- **`VY_VER_004` y `VY_VER_007`:** proceden de pares de módulos vistos apilados y se guardaron como conjuntos compuestos; no confundir el encaje aparente con una unión validada para el personaje.
- **`VY_MAN_005`:** el supuesto uso de «marco de unión» quedó como hipótesis visual. Medir los extremos antes de acoplarlo al pasillo largo.
- **`VY_CUR_004`:** está físicamente en `03_Intersecciones`, aunque su identificador sea `CUR`.
- **`VY_MNT_006`:** el archivo real se llama `VY_MNT_006_Empalme_T.blend`. No hay `VY_MAN_006_Empalme_T.blend` en el árbol. Podemos unificar la nomenclatura en el futuro, pero mientras tanto usar el nombre REAL.
- **`VY_REC_001`:** contiene un espacio y una raya larga Unicode (`VY_REC_001 — Recto Corto.blend`). **No** sustituirlo por `VY_REC_001_Recto_Corto.blend` al buscar el archivo.
- **`VY_TUR_003`:** el árbol confirma que existe un archivo con ese nombre. La geometría interna de la cabina y su operatividad requieren comprobación independiente.
- **Familias 04, 05, 06:** no presentes en el árbol compartido; respetar numeración original, sin inventar carpetas nuevas.

## 6. Archivos de trabajo y copias `.blend1`

El árbol lista **un maestro** y **siete copias `.blend1`** (respaldos generados por Blender). Las copias no cuentan como módulos independientes:

```text
Biblioteca_Voyager_Valhalla_MASTER.blend   [maestro]
Biblioteca_Voyager_Valhalla_MASTER.blend1   [respaldo]
01_Rectos/VY_REC_003_Recto_Largo.blend1   [respaldo]
02_Curvas/VY_CUR_001_Curva_Grande.blend1   [respaldo]
03_Intersecciones/VY_INT_001_Cruce_4_Direcciones.blend1   [respaldo]
07_Accesos_y_Camarotes/VY_ACC_003_Vestibulo_Grande_Sin_Salidas.blend1   [respaldo]
10_Conexiones_Verticales/VY_VER_001_Conexion_Vertical_Subida_Bajada.blend1   [respaldo]
11_Conductos_Mantenimiento/VY_MAN_001_Codo_Mantenimiento_90.blend1   [respaldo]
```

**Precaución:** no borrar `.blend1` por considerarlos «duplicados» sin revisar antes las copias y confirmar que no guardan una versión útil. Este catálogo solo documenta su presencia.

## 7. Pendiente de auditoría técnica con Codex

Cuando Codex vuelva a trabajar sobre la biblioteca, hacerlo **sin modificar los originales** y entregando los resultados en un laboratorio eliminable dentro del repositorio, excluido de Git:

1. Recorrer los 58 `.blend`, confirmar apertura correcta y guardar inventario de objetos, jerarquías, mallas, materiales e imágenes.
2. Medir dimensiones, pivotes, orientaciones y extremos de conexión de cada módulo en unidades coherentes.
3. Probar ensamblajes entre piezas de una misma familia y entre familias (corredor ↔ vestíbulo, pasillo ↔ Jefferies, Jefferies ↔ escotilla, escalera ↔ plantas, acceso ↔ turboascensor).
4. Identificar puertas animables, huecos realmente practicables y paneles potencialmente interactivos.
5. Analizar escalas de personaje, altura útil, pasos por escaleras y transiciones para Unreal Engine; no dar por válidas las colisiones solo por tener malla visible.
6. Informar de archivos duplicados reales, variantes geométricas y piezas faltantes, sin renombrar ni fusionar fuentes automáticamente.
7. Emitir una **segunda versión de este catálogo** con columnas verificadas de dimensiones, compatibilidad y estado de prueba. Mantener intacta la versión 1.0 como instantánea de referencia.

## 8. Reglas para consultar este documento en futuras conversaciones

- Antes de recomendar una pieza, buscar aquí por **función** y devolver **ID + nombre de archivo exacto + carpeta relativa + ruta raíz**.
- Si dos modelos parecen similares, ofrecer las variantes y explicar la diferencia conocida; no inventar medidas ni compatibilidades.
- Nunca presentar una función no verificada como hecho: «puerta animada», «escotilla operativa», «conexión exacta entre cubiertas» o «acceso abierto» requieren pruebas.
- Tratar las rutas y nombres de este documento como la **fuente de verdad de esta instantánea del 02/11/2026**. Si cambia el árbol de archivos, actualizar el catálogo después de recibir un nuevo inventario.
- Mantener los modelos 3D locales fuera de Git si así lo establece el `.gitignore`; este documento Markdown sí puede versionarse en una ubicación documental apropiada **si el usuario lo decide**.

---

**Fin del inventario v1.0.** Base documental para localizar y reutilizar los módulos Voyager en la construcción de la USS Enterprise-G, clase Valhalla.
