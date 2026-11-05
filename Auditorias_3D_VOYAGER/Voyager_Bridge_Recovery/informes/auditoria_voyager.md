# Auditoría técnica de la USS Voyager — Misión 1

Fecha: 09/10/2026 02:40 (Europe/Madrid). Auditoría de solo lectura del BLEND de trabajo, MAX 2011, MC6 y texturas suministradas.

## Diagnóstico principal

Se ha recuperado un conjunto separable de **631 mallas MAX y 11 empties**, pero su apariencia no está restaurada: los **90 materiales usados por esas piezas no tienen nodos de textura y todos tienen Emission Strength=0**. Las 49 imágenes de archivo del BLEND tienen rutas rotas y ningún contenido empaquetado. Los **104 archivos de textura disponibles se decodifican correctamente** en Blender, por lo que gran parte del trabajo visual es recuperable a partir de los recursos locales.

Hay además problemas de superficie y ensamblaje que impiden declarar la geometría completa: `floorfront` conserva 606 vértices pero sólo una cara minúscula, `Mesh1497` tiene 531 vértices sin cara, y dos mallas están muy alejadas del puente. La comparación del MAX es parcial y no certifica equivalencia geométrica ni visual completa.

**Mesh468 son 35 paneles planos del suelo**, no el suelo completo. Sus caras miran hacia −Z; la cubierta `Mesh1206` está 8,017 mm encima, comparte la planta de los paneles y actualmente tiene un material opaco. Activar emisión en Mesh468, por sí solo, no resuelve este conjunto.

## Integridad, alcance y reproducción

Se calcularon tamaño, fecha de modificación en nanosegundos y SHA-256 de los **107 archivos de originales**, antes y después. Resultado: **sin cambios**. El JSON conserva ambos manifiestos. No se guardó el BLEND, no se exportaron GLB/FBX, no se eliminaron ni fusionaron objetos y no se editaron materiales, colores ni repositorios externos.

Blender verificado: `5.2.2 LTS`, build `d13f752e3b9c`. Ejecución background con `--factory-startup --disable-autoexec`; apertura mediante `open_mainfile(use_scripts=False, load_ui=False)`. La preferencia de ejecución automática observada fue `False`. Los scripts de diagnóstico calculan cachés de triangulación y cargan imágenes temporales para comprobar decodificación, sin alterar los datablocks originales de imagen. Las vistas usan una escena/cámara temporal Workbench y un modo de visualización monocromo; no prueban los colores ni el render del modelo original.

Desde el directorio de trabajo, ejecutar en PowerShell:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python 'scripts\auditoria_voyager.py'
```

`scripts/informe_auditoria.py` genera la síntesis Markdown y enriquece el JSON. `scripts/vistas_diagnostico.py` genera sólo PNG de diagnóstico; `scripts/resumir_auditoria.py` facilita consultas al inventario. No hay que ejecutar los scripts incrustados del BLEND.

## Inventario y separación del OBJ

| Dato | Escena global | Conjunto MAX | OBJ antiguo |
|---|---:|---:|---:|
| Objetos | 643 | 642 | 1 |
| Mallas | 632 | 631 | 1 |
| Empties | 11 | 11 | 0 |
| Vértices | 438,967 | 184,697 | 254,270 |
| Polígonos | 483,852 | 212,147 | 271,705 |
| Triángulos de Blender | 533,138 | 261,433 | 271,705 |

Se encontraron **171 materiales**, frente a los aproximadamente 172 indicados previamente; es el recuento real de este archivo. Hay 51 datablocks de imagen: 49 de archivo más `Render Result` y `Viewer Node`. Hay una escena, una colección (`Collection`), ningún enlace de biblioteca y ningún modificador en las 631 mallas MAX. El inventario JSON conserva también jerarquías, visibilidad, propiedades personalizadas, atributos, UV y asignaciones de material por cara.

La malla OBJ se identifica inequívocamente como el objeto exacto **`Voyager Bridge`**, separado en todas las estadísticas, búsqueda de piezas y pruebas de rayos. Tiene 102 slots de material y dimensiones aproximadas 13,150 × 13,011 × 3,840 m. No se usó su geometría como fuente para localizar las piezas MAX.

El lector parcial del MAX encuentra 640 nombres de objetos Blender exactamente. Los otros dos son `ChamferBox001.001` y `hallwaysupports01.001`: existen dos nodos MAX con cada nombre base. El sufijo distingue duplicados nominales, no prueba duplicación geométrica. No se puede identificar cuál de los dos nodos fuente corresponde a cada instancia sólo por el nombre. El registro `provenance` conserva esta limitación.

**22 materiales tienen caras asignadas tanto al OBJ como al conjunto MAX**. Una restauración posterior deberá aislar esa dependencia antes de editar. La antigua malla tiene `hide_viewport=False`, `hide_render=False` y aparece visible al cargar este BLEND en el proceso de auditoría. Esto no informa sobre un ocultamiento temporal/local en una sesión interactiva; la exclusión de exportación debe hacerse por identidad explícita y no depender de la visibilidad.

## Piezas localizadas y prioridad

Las identificaciones físicas se contrastaron con cotas, asignaciones y vistas de geometría aislada. Las etiquetas de estación concreta (seguridad, ciencia, ingeniería, etc.) siguen pendientes cuando sólo hay nombres `Mesh/Plane/Object`.

| Familia | Objetos | Evidencia y alcance |
|---|---|---|
| Suelo central y escalones | `Mesh1500`, `Mesh1715`, `Mesh566` | verificado por geometría y vista aislada. Planos horizontales y bastidor central; materiales Voygray y Brushed_Aluminium. |
| Suelo de pasillos/plataforma exterior | `Mesh1497`, `floorfront`, `hallwayfloor` | parcial. hallwayfloor tiene superficie de 16 m²; floorfront y Mesh1497 conservan muchos vértices sin cara y requieren investigación de contornos. |
| Paneles del suelo y cubierta | `Mesh1206`, `Mesh468` | geometría verificada; función óptica de cubierta pendiente. 35 paneles del suelo; Mesh1206 cubre todos los centroides a 8,017 mm. Material #122 opaco actual. |
| Paneles azules de techo | `Object028`, `Object029`, `Object030`, `Object031`, `Object032`, `Object033`, `Object034`, `Object035`, `Object036`, `Object037`, `Object038`, `Object039`, `Object040`, `Object041`, `Object042`, `Object043`, `Object044`, `Object045`, `Object046`, `Object047`, `Object048`, `Object049` | verificado. Material light blue glow; Z entre 4,1566 y 4,4741 m; anillo perimetral en vista aislada. |
| Elementos glow inferiores | `Mesh1006`, `Mesh1019`, `Mesh1022`, `Mesh1025`, `Mesh1029`, `Mesh1036`, `Mesh1037`, `Mesh994`, `Mesh999`, `Object027`, `Object050`, `Object051`, `Object052`, `Object053`, `Object054`, `Object055`, `Object056` | geometría y asignación verificadas; función individual parcial. 17 objetos distribuidos en bases, frentes y consolas; alturas distintas. No son todos paneles de techo. |
| Techo y luminarias centrales | `Centerpiece`, `Mainroof`, `Mesh86`, `blackinset`, `centerinset`, `centerlight`, `centerlights01`, `lightring03`, `lightringback`, `lightsring02`, `lightssupport` | verificado. Techo, anillos y domo por nombres, cotas y vistas; Mesh86 es plano superior con Window. |
| Barandillas y soportes centrales | `Mesh1324`, `Mesh1325`, `Mesh1326`, `Mesh1327`, `Mesh1328`, `Mesh1329`, `Mesh1330`, `Mesh1331`, `Mesh1332`, `Mesh1372`, `Mesh1373`, `Mesh1374`, `Mesh1375`, `Mesh1376`, `Mesh1387`, `Mesh1388`, `Mesh1389`, `Mesh1390`, `Mesh1391`, `Mesh1392`, `Mesh1393`, `Mesh1394`, `Mesh1395`, `Mesh1396`, `Mesh1397`, `Mesh1398`, `Mesh1399`, `Mesh1400`, `Mesh1401`, `Mesh1402`, `Mesh1403` | verificado por vista aislada. 31 piezas; cinco pasamanos y soportes de Brushed_Aluminium. Otros usuarios del material no son necesariamente barandillas. |
| Carcasas de consolas | `Mesh1114`, `Mesh1119`, `Mesh1127`, `Mesh1133`, `Mesh1340`, `Mesh1717`, `Plane083`, `Plane084` | verificado por grupo aislado; nombres de estaciones pendientes. Carcasas con DimGray; superficies de pantalla inventariadas por material en anexo. |
| Sillones centrales | `Armrest01`, `Armrest02`, `Armrest03`, `Armrest04`, `Box001`, `Box003`, `Box004`, `Box005` | verificado por vista aislada. Dos sillones centrales con cuero Leather2 y cuatro apoyabrazos. |
| Asientos de estaciones | `ChamferBox`, `ChamferBox001.001`, `ChamferBox002`, `Layer:0`, `Layer:001`, `Layer:002` | verificado por geometría y parentesco. Tres grupos de sillas Group009, Group008, Group003; componentes MSB y Object asociados a estos padres. |
| Puertas y hojas | `Mesh1310`, `Mesh1311`, `Mesh1312`, `Mesh1313`, `Mesh1314`, `Mesh1315`, `Mesh1316`, `Mesh1317`, `Mesh1318`, `Mesh1319`, `Mesh1320`, `Mesh1321`, `Mesh1502`, `Mesh1524`, `Mesh1533`, `Mesh1547`, `Mesh1556`, `Mesh1564`, `Mesh1569`, `Mesh1586`, `Mesh1608`, `Mesh1625`, `Mesh1640`, `Mesh1649`, `Mesh1650`, `Mesh178`, `Mesh179`, `Mesh180`, `Mesh181`, `Mesh182`, `Mesh183`, `Mesh88`, `Mesh89`, `Mesh90`, `Mesh91`, `Mesh92`, `Mesh93`, `Mesh94`, `Mesh95`, `Mesh96`, `Mesh97`, `Mesh98`, `Mesh986`, `Mesh988`, `Mesh989`, `Mesh99`, `Mesh990`, `Mesh991`, `door01` | verificado por jerarquía; ensamblaje completo pendiente. Grupos door3, door4, door04–door07 y sus hijos; Doorpanel01–04 son controles pequeños. |
| Controles de puertas | `Doorpanel01`, `Doorpanel02`, `Doorpanel03`, `Doorpanel04` | verificado. Material Doorpanel01_DP_01 y dimensiones pequeñas; no confundir con hojas. |

Vistas: [corte inferior](vistas/max_corte_inferior.png), [suelo y estructura](vistas/suelo_estructura.png), [barandillas](vistas/barandillas.png), [consolas DimGray](vistas/gris_dimgray.png), [sillones y tapizado](vistas/sillones_materiales.png), [exterior y piezas alejadas](vistas/max_exterior.png). El corte selecciona piezas cuya cota máxima es inferior a 2,5 m; una pieza ausente de esa imagen puede existir en la escena completa.

## Mesh468: geometría, material y cubierta

| Propiedad | Valor verificado |
|---|---|
| Origen del objeto | (2,847747; −3,199653; −0,025731) |
| Rotación / escala | (0, 0, 0) / (0,320695877; 0,320695877; 0,320695877) |
| Caja mundial de geometría | X −4,723806 a 4,515859; Y −4,567110 a 1,100726; Z −0,025746882 |
| Dimensiones mundiales | 9,239665 × 5,667836 × 0 m |
| Centro de la caja | (−0,103974; −1,733192; −0,025747), distinto del origen del objeto |
| Geometría | 2.242 vértices; 4.379 aristas; 2.172 caras triangulares |
| Componentes conectados | 35, sin vértices sueltos |
| Área sumada de superficie | 8,192385 m² |
| Material | Un slot; nombre exacto JSON `\u001clight floor\u0003`; 2.172 caras asignadas |
| Normales | 2.172 caras hacia −Z; determinante de transformación positivo |
| Topología | 2.242 aristas de borde; 0 aristas con más de dos caras; 0 caras degeneradas |
| UVMap | U −2871,443 a −1737,140; V 1833,406 a 2529,215; valores finitos |

La planta aislada confirma paneles con esquinas redondeadas, triángulos y trapecios, dispuestos en arco con dos ramales. La superficie no tiene espesor. Las UV están muy fuera de 0–1: no impiden un material uniforme, pero una nueva textura requerirá validar su escala y repetición.

![Mesh468: planta geométrica](vistas/mesh468_planta.png)

La pieza superior **Mesh1206** tiene 2.270 vértices, 2.207 triángulos y 35 componentes; prácticamente la misma planta y área. Z ≈ −0,0177298 m. Los rayos hacia +Z desde **los 2.172 centroides de triángulo** de Mesh468 encuentran Mesh1206 a 0,00801723–0,00801730 m, dentro de un alcance de 5 cm. Es un muestreo de cobertura geométrica, no una intersección exacta ni un render de transmisión.

Su único material es el nombre exacto ` Material #122\u0003`: Base Color blanco, Alpha=1, Transmission Weight=0 y Emission Strength=0. Sus caras también apuntan hacia −Z. Es **hipótesis fuerte** que sea una cubierta de los paneles; no se ha demostrado su material óptico original. `Glass_Floor_Light` del MC6 ofrece una referencia candidata (transparencia 0,9), pero la igualdad de pieza/material entre formatos no está probada. En Blender el culling del material está desactivado; la futura exportación debe resolver tanto normales como cubierta y transparencia.

## Suelos y defectos geométricos reales

`floorfront` no debe considerarse un suelo recuperado por su nombre ni por su caja de vértices: de 606 vértices, **593 no participan en ninguna cara**. Su única cara usa 13 vértices y suma sólo **0,000133254 m²** según la triangulación de Blender. La caja de todos los vértices mide 19,831 × 9,868 m, pero la caja de su superficie es sólo 0,411 × 0,046 m. El JSON distingue `bounds_world` y `bounds_surface_world`.

`Mesh1497` conserva 633 vértices, 14 caras y **531 vértices sin cara**. Su caja de vértices tampoco certifica una plataforma rellena. `hallwayfloor` sí contiene una cara de 363 vértices (361 triángulos, ≈16 m²); esa gran cara requiere comprobar triangulación y colisión. `Mesh1500` es un plano central de ≈28,458 m² a Z≈0,190723 m, con 372 de 373 caras orientadas hacia −Z. `Mesh1715` es un plano inferior de ≈10,235 m² a Z≈−0,434634 m. `Mesh566` aporta bastidor y escalones.

El conjunto MAX presenta **1,523 vértices sin cara, 639 caras de área local inferior a 1e−12 y 795 aristas usadas por más de dos caras**. Hay 95,022 aristas de borde; muchas pertenecen a planos abiertos deliberados y no son defectos por sí mismas. Los recuentos no constituyen una certificación de manifold: no se examinan todas las autointersecciones, winding ni solapamientos exactos. No se aplicó `mesh.validate()` a ninguna malla de la escena.

La lectura previa a validación aporta una evidencia concreta: `floorfront` tiene en el lector MAX dos caras, una de **604 índices con vértices repetidos** y otra de 13. El BLEND conserva sólo la de 13. Para `Mesh1497`, el lector encuentra 15 caras, incluida una de **553 índices con repeticiones**; Blender conserva 14. `Mesh69` pasa de 235 caras leídas a 233, con dos caras de índices repetidos. Es compatible con el rechazo de contornos que MAX permite representar y Blender no acepta como un polígono simple. La causa exacta no se certifica sin el registro de importación o una prueba posterior autorizada sobre una copia. La información de vértices aún conservada puede ser útil para reconstruir esos contornos; no debe eliminarse.

En 19 objetos con nombre fuente único hay diferencias de caras frente al lector, que suman **190 caras menos en Blender**. Destacan Centerpiece (8.447 → 8.342), centerRA (634 → 605) y Mainroof (14.454 → 14.447); el lector cuenta siete conjuntos de vértices de cara duplicados en Mainroof. La lista completa está en `source_geometry_comparison`. Son diferencias comprobadas con ese lector, no una afirmación de que todas esas caras deban reinstalarse: algunas pueden ser duplicados o contornos incompatibles.

590 mallas tienen una capa UV; 41 no tienen ninguna. No se encontraron UV no finitas. No hay segunda capa UV registrada para lightmaps. `Mesh551` está vacía; `Mesh150`, `Mesh72` y `Mesh73` no tienen slots de material. La ausencia de UV no obliga a corregir una pieza que vaya a usar material uniforme.

`Mesh992` (Group006) tiene centro (−21,360; 3,252; 16,611) m y `Mesh993` (Group007), (−19,024; 5,786; 16,898) m. Son piezas reales presentes, muy fuera del volumen principal. Sus padres y transformaciones se conservan; no se ha demostrado si el desplazamiento procede del MAX, del importador, del ensamblaje o de una edición posterior. **No ajustar toda la escena usando la caja global ni moverlas automáticamente.** Las unidades declaradas son METRIC, scale_length=1, METERS; eso no certifica la escala física del puente ni su equivalencia con el OBJ antiguo.

## Materiales luminosos y demás shaders

Los nombres originales con caracteres de control se conservan íntegros en JSON. Se detectaron ocho nombres con controles. Algunos dejan prefijos imprimibles (`$`, `(`, `6`) tras limpiar los controles: no se renombraron ni se consideraron contenido semántico fiable. El MAX contiene cadenas limpias `light floor`, `light blue glow`, `light blue glow 2` y `light white to blue glow`.

| Material prioritario | Asignación física | Propiedades Blender verificadas |
|---|---|---|
| light floor | Mesh468, 2.172 caras | Base Color (0,7; 0,5; 0,2), Roughness=1, Metallic=0, Alpha=1; emisión negra y fuerza 0 |
| light blue glow | Object028–Object049, 22 paneles del techo | Mismas propiedades y sin texturas |
| light blue glow 2 | 17 piezas inferiores enumeradas en tabla/anexo | Mismas propiedades; no agruparlas como techo |
| light white to blue glow | centerlight, sólo 64 de sus 2.688 caras | Mismas propiedades; no hay nodos que produzcan un gradiente blanco–azul |
| Material #122 | Mesh1206, cubierta de paneles | Blanco, Alpha=1, Transmission Weight=0; emisión 0 |
| lights con controles | centerlights01, lightringback, Mesh03, Mesh499, Mesh513 | Color (0,7; 0,5; 0,2), emisión 0 |
| Lights | 13 piezas: Mesh451–Mesh498 según inventario | Color ≈(1; 0,972549; 0,913726), emisión 0; distinto datablock del anterior |
| light white on to off | lightring03, lightsring02, Object060 | Fuerza de emisión 0; no hay animación de encendido/apagado en objetos auditados |
| Light TL | Mesh20, 108 caras | Color naranja ≈(1; 0,54902; 0), emisión 0 |

Siete materiales MAX repiten el color (0,7; 0,5; 0,2), incluidas luces y `Brushed_Aluminium`; ese valor está verificado en Blender, **no validado como apariencia original**. Los 90 materiales MAX tienen sólo Principled/Output y, en seis casos, un Normal Map cuyo Color no está conectado a una imagen. Son `fabric brown_BURLAP01`, `Leather2_LEATH01`, `Leather_LEATH01`, `Metal_Co_Metal_Co`, `Plaque_VP_col` y `Voygray_Voygray`. No hay recuperación efectiva de esos mapas normales por el mero hecho de existir el nodo.

Las **50 instancias de nodo Image Texture** de la escena están en materiales asociados al OBJ antiguo, no en los shaders usados por MAX. Por tanto, reenlazar las imágenes existentes no basta para restaurar los materiales MAX: hay que reconstruir sus conexiones. No se declara ningún material MAX plenamente recuperado.

## Comparación con Poser MC6

Se analizaron **142 definiciones** mediante lectura de llaves, propiedades y árboles de shader con números de línea. Sus **54 nombres de textura distintos** tienen archivos locales exactos y decodificables. El MC6 es una variante Poser: sus parámetros y nombres sirven de evidencia, pero no sustituyen automáticamente el shading mental ray del MAX.

| Comparación | Coincidencia verificada | Diferencia o incertidumbre |
|---|---|---|
| light floor ↔ Light_Floor (línea 48507) | Nombre funcional compatible; MC6 KdColor blanco, KaColor blanco; sin mapas | Blender es ocre y emisión 0. MC6 Ambient_Value=0: KaColor blanco por sí solo **no demuestra emisión efectiva** ni su intensidad |
| Mesh1206 ↔ Glass_Floor_Light (línea 7785) | MC6 KdColor≈0,054902 y tMin=tMax=0,9 | Candidato por función; material MAX de cubierta original no recuperado ni identificado inequívocamente |
| blue glow ↔ Light_Blue_Center/Aft (líneas 18423/30189) | MC6 declara KdColor blanco y Ambient_Color azul | Ambient_Value=0 en ambos. La relación exacta con los paneles MAX es hipótesis; no trasladar esos valores como emisión activa |
| Mainscreen_MVS ↔ MainScreen (8385) | MVS.jpg está en MC6, metadatos MAX y carpeta local; geometría Object074 | Blender sin textura conectada y color base negro; MC6 KdColor blanco. Correspondencia de recurso, no shader completo |
| scrn1.1_scn1.1 ↔ Scrn1_1 (47615) | Cambio sistemático scn1.1.png → scn1_1.png; MC6 apunta al archivo local | Blender sin imagen conectada y color negro; MC6 mapa en Diffuse_Color. Las variantes _i no están conectadas en MAX importado |
| fabric brown_BURLAP01 ↔ Fabric_Brown (18723) | BURLAP01.JPG nombrado en MC6 y sufijo material MAX | Propiedades y mapas normales requieren reconstrucción; verificar tapizado mediante render |
| Leather/Leather2 ↔ Leather/Leather2 (29743/19169) | LEATH01.JPG disponible y referenciado | Shaders MAX sin imagen; Normal Map con color constante no recupera relieve |
| Plaque_VP_col ↔ Plaque (3447) | VP_col.png/VP_bump.png disponibles y documentados en recursos | MC6 no tiene textureMap en la propiedad principal y usa VP_bump en Bump/Gradient_Bump; no asumir idéntico esquema MAX |
| Brushed_Aluminium ↔ Railing (9) | Geometría de barandillas aislada; MC6 define Railing | Nombres de materiales diferentes y color distinto. Equivalencia funcional candidata, sin mapa de materiales 1:1 probado |
| Window ↔ Glass_Ceiling (10477) | Window asignado a Mesh86, plano de techo; MC6 contiene vidrio de techo | Window Alpha≈0,2 y Transmission=0; MC6 transparencia 0,9. Comparación funcional, no shader equivalente |

El anexo enumera los 90 materiales MAX con sus candidatos MC6, propiedades verificadas y objetos usuarios. La coincidencia numérica de Kd no acredita recuperación completa: no se ha validado equivalencia entre espacios de color, exponentes de brillo Poser y roughness PBR, reflexión, refracción ni render.

## Texturas: enlaces, empaquetado, candidatos y ausencias

| Estado | Cantidad | Interpretación |
|---|---:|---|
| Archivos locales de textura | 104 | Todos decodificados en imágenes temporales de Blender; tamaño, profundidad y hash en JSON |
| Imágenes FILE registradas en BLEND | 49 | Todas sin datos de píxeles y rutas inexistentes `//VOYBRIDGETEX-1\Textures\...` |
| Imágenes correctamente enlazadas y decodificadas | 0 | No hay enlace de archivo válido en el BLEND auditado |
| Imágenes empaquetadas | 0 | No hay copia recuperable dentro del BLEND |
| Candidatos locales de igual nombre para imágenes BLEND | 10 | alumb_t, BURLAP01, DP_01, LEATH01, Metal_Co, n011, scn8, scn9, Voygray, VP_col |
| Candidatos con punto cambiado a guion bajo | 39 | scn1.1 → scn1_1, scn10.1 → scn10_1, etc.; no son una ausencia real de archivo |
| Buffers de render/compositor | 2 | Render Result y Viewer Node; no contarlos como texturas faltantes |
| Nombres únicos bitmap en metadatos MAX | 105 | 22 con igual basename y 78 candidatos renombrados; 5 sin candidato |

Los candidatos renombrados se apoyan también en referencias del MC6 al nombre con guion bajo. Se ha verificado existencia y decodificación, **no identidad byte a byte con el bitmap original del MAX**: el MAX referencia rutas, no aporta un checksum original utilizable para esta comparación. Los archivos `_i`, BM_NRM.tif, BM_DISP.tif, VP_bump.png, BNC.png, MVS.jpg, XYT.jpg y otros están disponibles aunque no aparezcan como imagen conectada en el conjunto MAX.

Los cinco recursos sin candidato en `originales` son:

- `glare_streaks_star_camera_filter.tif`.
- `scn1.5_ilum.png`.
- `scn10.1.1.jpg`.
- `scn10.2.1.jpg`.
- `scn10.6.1.jpg`.

Están referenciados en `FileAssetMetaData2`; su ausencia local es real dentro del paquete auditado, pero **no se ha probado que todos estén activos en el render original**. El filtro glare corresponde por nombre a un efecto de cámara; los JPG alternativos no deben sustituirse por pantallas PNG sin comprobación. Los recursos locales adicionales respecto a esos basenames son `alumin.JPG`, `Map__2_Gradient.tga`, `Metal_Al.jpg` y `VP_Spec.png`. Son candidatos útiles para investigación, no mapas ya asignados.

## Qué permite afirmar el MAX y qué limita el importador

El MAX es un contenedor CFB/OLE con diez streams. Se inspeccionaron nombres, tamaños, hashes y cadenas legibles; se recorrieron parcialmente nodos, clases y referencias con el **importador instalado io_scene_max 1.9.2**, hash de código `1b786ebe82d2a1c0df273514af449e8b91430672abafde3de4ee634f2432320d`. No se llamó a `load`, `read`, `make_scene`, `create_shape` ni otras rutinas que construyen una escena. El JSON conserva posibles errores del lector (en esta ejecución: 0).

Metadatos del MAX:

- `3ds Max Version: 13,00`.
- `Vertices: 188929`.
- `Faces: 221871`.
- `Objects: 635`.
- `Shapes: 0`.
- `Lights: 8`.
- `Cameras: 17`.

El lector encuentra **671 nodos con nombre**: 631 entradas geométricas/principales (incluidas 89 envolturas 0x2032), 11 dummies, 17 cámaras, cuatro targets de cámara y ocho luces. Los targets tienen super_id 0x10 y GUID 0x1020; no deben contarse como mallas. Las 17 cámaras más targets y ocho luces explican 29 nodos fuente ausentes, junto con los dos duplicados nominales diferenciados por Blender.

Las luces originales identificadas son: `mr Area Omni001`, `Fspot001`, `Fspot002`, `Fspot003`, `Omni002`, `Omni003`, `Omni004`, `Omni005`. No se recuperaron intensidades, unidades, sombras, render shaders ni equivalencia óptica. Las cámaras conservadas sólo como evidencia de nombres/clases incluyen estaciones, turbolift y vista frontal; no están en Blender.

La comparación 188.929 vértices / 221.871 caras / 635 objetos del resumen MAX frente a 184.697 / 212.147 / 631 mallas de Blender tiene diferencias de 4.232 vértices, 9.724 caras y cuatro objetos. **Son indicadores para investigar, no prueba de cuatro mallas concretas perdidas**: los resúmenes pueden incluir evaluación de modificadores o conteos con convenciones distintas, y no se ha certificado que sus cifras sean actuales. El conteo de triángulos Blender no debe compararse directamente con “Faces” sin saber qué cuenta MAX.

Limitaciones verificadas en el código local `import_max.py`:

1. `SKIPPABLE` (líneas 82–100) incluye cámaras, targets, Omni y Free Direct. `create_mesh` (2156–2191) sólo crea tipos soportados y omite otros; no crea luces/cámaras. La ausencia de esos elementos en Blender no demuestra que faltaran en el MAX.
2. `get_arch_material` (1579–1587) sólo extrae diffuse/specular/shinines. No convierte mapas, emisión, falloff o árboles completos de Arch & Design. El lector encuentra Arch & Design en Mesh468, centerlight, barandillas y otros objetos; los materiales luminosos no han recuperado su comportamiento.
3. `adjust_material` (1671–1712) construye Principled, carga algunos bitmaps, normal y transparencia; asigna emission_color pero **no emission_strength**. Usa además `blend_method='HASHED'`, una ruta que debe contrastarse con la API actual antes de una nueva importación. No se conservan logs de la importación original para demostrar qué errores ocurrieron entonces.
4. `create_shape` (1865–1885) ejecuta `mesh.validate()` antes de asignar índices de material. Si elimina caras, las longitudes de asignaciones pueden divergir; el código imprime errores de longitud. El caso de contornos/suelos requiere investigación específica. La auditoría no ejecuta esa validación en la escena de trabajo.
5. Las conversiones de UV, índices, primitivas, matrices y pivotes son parciales. El código permite errores por objeto y continúa (`make_scene`, 2223–2228); puede producir una escena aparentemente completa aunque algunos elementos fallen.

`VideoPostQueue` contiene **Lens Effects Glow**, con nombres Floorglow, Blueglow, Redglow, orangeglow y Turbolift Lights. La biblioteca y los metadatos identifican mental ray Renderer. Son referencias verificadas a shaders/postprocesado original: no certifican sus parámetros ni que todos estuvieran habilitados, y no se han recreado en Blender.

## Propuesta ordenada de restauración visual — pendiente de autorización

1. **Preparar una copia de trabajo** fuera de originales y un conjunto explícito MAX. Conservar identidad del OBJ y aislar los 22 materiales compartidos. Guardar correspondencias nombre fuente ↔ nombre limpio ↔ pieza ↔ slot; no fusionar piezas para simplificar nombres.
2. **Resolver geometría crítica antes del look**: recuperar o verificar contornos de floorfront/Mesh1497 desde el MAX, revisar orientación de suelos, investigar Mesh992/Mesh993 y revisar padres/pivotes de puertas. No borrar los vértices sin cara: pueden contener información necesaria para la recuperación.
3. **Preparar un mapa de recursos** sin renombrar originales: enlaces a los 10 nombres exactos y 39 candidatos renombrados, 54 referencias MC6 y bitmaps adicionales MAX. Buscar los cinco ausentes sólo cuando se demuestre uso activo; conservar alternativas marcadas como tales.
4. **Reconstruir un grupo piloto de suelo**: Mesh468 + Mesh1206 + Mesh566 + Mesh1500. Confirmar cubierta, normales, transparencia y material óptico frente a referencias antes de definir emisión. La fuerza y tono luminosos deben comprobarse visualmente; MC6 Ambient_Value=0 no aporta una intensidad activa fiable.
5. **Restaurar pantallas y luminarias**: usar base color y mapas `_i` sólo donde la función del canal se verifique; reconstruir el gradiente white-to-blue, anillos y elementos del turbolift. Separar emisión de material, luces que iluminan y efectos de resplandor.
6. **Restaurar materiales físicos**: tapizados/cuero, metales/barandillas, plaque, vidrio de techo y puertas. Verificar cada shader mediante render con exposición e iluminación controladas, no por nombre o color de viewport.
7. **Comparar vistas fijas del puente** con referencias del original que se dispongan. Registrar qué propiedades coinciden, qué se han aproximado y qué falta. No declarar fidelidad total sin comprobar luces, transparencia, relieve, brillo y textura sobre su geometría real.

## Preparación para Unreal Engine 5 mediante Rob3D

En el directorio auditado no se suministró Rob3D, su configuración, versión ni contrato de exportación; no se ha inspeccionado ni modificado un repositorio externo. Por tanto, no se afirma que transporte materiales, luces, jerarquías o colisiones automáticamente. Estas son condiciones que deberá cumplir una exportación futura autorizada:

- Seleccionar las 631 mallas y 11 empties MAX explícitamente; excluir `Voyager Bridge`. Mantener puertas/controles/estaciones separables para interacción y pivotes correctos. La pérdida de animación original significa que su lógica de juego deberá construirse y comprobarse.
- Resolver suelos, normales y transformaciones antes de decidir escala en centímetros UE. Mantener una medida patrón y un mapa de transformaciones; no usar la caja global afectada por las mallas alejadas.
- Preservar UV activas y slots de material por cara. Hay 41 mallas sin UV y ninguna segunda capa UV en MAX; decidir lightmaps sólo si se van a usar. Preparar colisiones caminables y de puertas independientemente de los planos luminosos.
- Transportar texturas con rutas verificadas y una tabla PBR/emisión/cubierta. No asumir que un shader Blender complejo se importará igual. La ruta FBX de Epic conecta automáticamente sólo ciertos canales, como Color y Normal; otros necesitan revisión y conexiones explícitas. [Documentación oficial de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).
- Reconstruir emisión y bloom con parámetros de material y validar iluminación por separado. Epic documenta Emissive Color HDR y modelos Lit/Unlit; la elección debe corresponder al uso de cada panel. [Emissive Material Input](https://dev.epicgames.com/documentation/unreal-engine/using-the-emissive-material-input-in-unreal-engine). Con Lumen, superficies emisivas demasiado pequeñas/intensas pueden producir ruido; planificar luces complementarias tras una prueba visual. [Lumen](https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine).
- Evaluar rendimiento con 631 mallas, 261.433 triángulos y 90 materiales. Esos números describen el contenido, no los draw calls medidos ni una aprobación de rendimiento. Optimizar sólo después de preservar interacción y apariencia, con pruebas en el hardware objetivo.

No se ha realizado ninguna exportación ni iniciado la restauración. La siguiente fase queda pendiente de autorización del usuario.

## Anexo A — Materiales MAX, propiedades y usuarios

Los prefijos imprimibles de nombres dañados se muestran como existen tras quitar sólo controles. El JSON conserva el nombre exacto escapado. “Candidato MC6” describe una comparación; ningún material tiene validación visual completa.

| Material Blender | Base Color RGB / roughness / alpha | Candidato MC6 | Objetos MAX con caras asignadas |
|---|---|---|---|
| BNC | 0.7, 0.5, 0.2 / 0 / 1 | BNC | `BCN2`, `BNC1` |
| lights | 0.7, 0.5, 0.2 / 1 / 1 | Sin coincidencia inequívoca | `centerlights01`, `lightringback`, `Mesh03`, `Mesh499`, `Mesh513` |
| light floor | 0.7, 0.5, 0.2 / 1 / 1 | Light_Floor | `Mesh468` |
| Material #122 | 1, 1, 1 / 0 / 1 | Sin coincidencia inequívoca | `Mesh1206` |
| $light blue glow | 0.7, 0.5, 0.2 / 0.4 / 1 | Light_Blue_Center, Light_Blue_Aft | `Object028`, `Object029`, `Object030`, `Object031`, `Object032`, `Object033`, `Object034`, `Object035`, `Object036`, `Object037`, `Object038`, `Object039`, `Object040`, `Object041`, `Object042`, `Object043`, `Object044`, `Object045`, `Object046`, `Object047`, `Object048`, `Object049` |
| (Brushed_Aluminium | 0.7, 0.5, 0.2 / 0 / 1 | Sin coincidencia inequívoca | `Mesh1118`, `Mesh1310`, `Mesh1311`, `Mesh1312`, `Mesh1313`, `Mesh1314`, `Mesh1315`, `Mesh1316`, `Mesh1317`, `Mesh1322`, `Mesh1323`, `Mesh1324`, `Mesh1325`, `Mesh1326`, `Mesh1327`, `Mesh1328`, `Mesh1329`, `Mesh1330`, `Mesh1331`, `Mesh1332`, `Mesh1333`, `Mesh1334`, `Mesh1336`, `Mesh1338`, `Mesh1344`, `Mesh1345`, `Mesh1346`, `Mesh1347`, `Mesh1348`, `Mesh1349`, `Mesh1350`, `Mesh1351`, `Mesh1352`, `Mesh1353`, `Mesh1354`, `Mesh1355`, `Mesh1356`, `Mesh1357`, `Mesh1358`, `Mesh1359`, `Mesh1360`, `Mesh1361`, `Mesh1362`, `Mesh1363`, `Mesh1364`, `Mesh1365`, `Mesh1366`, `Mesh1367`, `Mesh1368`, `Mesh1369`, `Mesh1372`, `Mesh1373`, `Mesh1374`, `Mesh1375`, `Mesh1376`, `Mesh1377`, `Mesh1378`, `Mesh1379`, `Mesh1380`, `Mesh1381`, `Mesh1382`, `Mesh1383`, `Mesh1386`, `Mesh1387`, `Mesh1388`, `Mesh1389`, `Mesh1390`, `Mesh1391`, `Mesh1392`, `Mesh1393`, `Mesh1394`, `Mesh1395`, `Mesh1396`, `Mesh1397`, `Mesh1398`, `Mesh1399`, `Mesh1400`, `Mesh1401`, `Mesh1402`, `Mesh1403`, `Mesh1404`, `Mesh1405`, `Mesh1406`, `Mesh1407`, `Mesh1427`, `Mesh566`, `MSB30187`, `MSB30189`, `MSB30190` |
| (light blue glow 2 | 0.7, 0.5, 0.2 / 1 / 1 | Light_Blue_Center, Light_Blue_Aft | `Mesh1006`, `Mesh1019`, `Mesh1022`, `Mesh1025`, `Mesh1029`, `Mesh1036`, `Mesh1037`, `Mesh994`, `Mesh999`, `Object027`, `Object050`, `Object051`, `Object052`, `Object053`, `Object054`, `Object055`, `Object056` |
| 6light white to blue glow | 0.7, 0.5, 0.2 / 1 / 1 | Light_Blue_Center, Light_Blue_Aft | `centerlight` |
| Black1 | 0, 0, 0 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh100`, `Mesh101`, `Mesh102`, `Mesh103`, `Mesh88`, `Mesh89`, `Mesh90`, `Mesh91`, `Mesh92`, `Mesh93`, `Mesh94`, `Mesh95`, `Mesh96`, `Mesh97`, `Mesh98`, `Mesh99` |
| black2 | 0, 0, 0 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh142`, `Mesh75` |
| Burnt | 0.027451, 0.011765, 0.0078431 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh154` |
| Chairgray_n011 | 0.58431, 0.58431, 0.58431 / 0.9 / 1 | Chair_Grey | `ChamferBox`, `ChamferBox001.001`, `ChamferBox002`, `Layer:0`, `Layer:001`, `Layer:002` |
| Charcoal | 0.13725, 0.13725, 0.13725 / 0.9 / 1 | Sin coincidencia inequívoca | `blackinset`, `centerinset`, `lightssupport`, `Mesh1111`, `Mesh1112`, `Mesh174`, `Mesh175`, `Mesh176`, `Mesh177`, `Mesh178`, `Mesh179`, `Mesh180`, `Mesh181`, `Mesh182`, `Mesh183`, `Mesh184`, `Mesh200`, `Mesh202`, `Mesh203`, `Mesh204`, `Mesh207`, `Mesh210`, `Mesh211`, `Mesh212`, `Mesh213`, `Mesh214`, `Mesh215`, `Mesh225`, `Mesh227`, `Mesh228`, `Mesh229`, `Mesh230`, `Mesh233`, `Mesh246`, `Mesh248`, `Mesh257`, `Mesh261`, `Mesh262`, `Mesh263`, `Mesh264`, `Mesh265`, `Mesh268`, `Mesh269`, `Mesh274`, `Mesh275`, `Mesh276`, `Mesh277`, `Mesh278`, `Mesh283`, `Mesh288`, `Mesh293`, `Mesh298`, `Mesh306`, `Mesh307`, `Mesh308`, `Mesh309`, `Mesh310`, `Mesh311`, `Mesh312`, `Mesh313`, `Mesh314`, `Mesh315`, `Mesh316`, `Mesh317`, `Mesh318`, `Mesh319`, `Mesh320`, `Mesh321`, `Mesh323`, `Mesh324` |
| Color_00 | 0.22745, 0.22745, 0.22745 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh69`, `Mesh869`, `Mesh870`, `Mesh871`, `Mesh872`, `Mesh873`, `Mesh874`, `Mesh875`, `Mesh876`, `Mesh877`, `Mesh878`, `Mesh879`, `Mesh880`, `Mesh881`, `Mesh882`, `Mesh883`, `Mesh884`, `Mesh885`, `Mesh886`, `Mesh893`, `Mesh895`, `Mesh896`, `Mesh897`, `Mesh900`, `Mesh902`, `Mesh903`, `Mesh904`, `Mesh905`, `Mesh906`, `Mesh907`, `Mesh908`, `Mesh909`, `Mesh910`, `Mesh911`, `Mesh912`, `Mesh913`, `Mesh914`, `Mesh915`, `Mesh916`, `Mesh917`, `Mesh918`, `Mesh919`, `Mesh920`, `Mesh921`, `Mesh922`, `Mesh923`, `strudextends` |
| Color_01 | 1, 1, 1 / 0.9 / 1 | Color_01 | `Plane003` |
| Color_03 | 0.66667, 0.66667, 0.66667 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh1128` |
| Color_04 | 0.11765, 0.11765, 0.11765 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh924`, `Mesh925` |
| Color_05 | 0.55686, 0.55686, 0.55686 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh589`, `Mesh657`, `Mesh728`, `Mesh793`, `Mesh861` |
| Color_06 | 0.33725, 0.33725, 0.33725 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh862`, `Mesh863`, `Mesh864`, `Mesh865`, `Mesh866`, `Mesh867`, `Mesh868` |
| Color_07 | 0.77647, 0.77647, 0.77647 / 0.9 / 1 | Sin coincidencia inequívoca | `Centerpiece` |
| Color_A0 | 0, 0, 0 / 0.9 / 1 | Sin coincidencia inequívoca | `centerRA`, `Mesh148`, `Mesh266`, `Mesh926`, `Mesh927`, `Mesh928`, `Mesh929`, `Mesh930`, `Mesh931`, `Mesh932`, `Mesh933`, `Mesh936`, `Mesh938`, `Mesh939`, `Mesh940`, `Mesh941`, `Mesh942`, `Mesh943`, `Mesh944`, `Mesh945`, `Mesh946`, `Mesh947`, `Mesh948`, `Mesh949`, `Mesh950`, `Mesh951`, `Mesh952`, `Mesh953`, `Mesh954` |
| Color_A1 | 0.4, 0.23922, 0.23922 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh981`, `Object074` |
| Color_C2 | 0.2, 0.15686, 0.11765 / 0.9 / 1 | Sin coincidencia inequívoca | `door01`, `Mesh986`, `Mesh988`, `Mesh989`, `Mesh990`, `Mesh991`, `Mesh992`, `Mesh993` |
| Color_H1 | 0.49804, 0.6, 0.6 / 0.9 / 1 | Sin coincidencia inequívoca | `hallwaypanels`, `hallwaysubframe`, `hallwaysupports01`, `hallwaysupports01.001`, `Mesh1101`, `Mesh1109`, `Mesh575`, `Object012`, `Object014`, `Object016`, `Object017`, `Object018`, `Object020`, `Object023`, `Object024`, `Top ring` |
| DimGray | 0.29412, 0.29412, 0.29412 / 1 / 1 | Sin coincidencia inequívoca | `Mesh1114`, `Mesh1119`, `Mesh1127`, `Mesh1133`, `Mesh1340`, `Mesh1717`, `Mesh354`, `Mesh355`, `Mesh356`, `Mesh357`, `Mesh358`, `Mesh365`, `Mesh366`, `Mesh367`, `Mesh368`, `Mesh369`, `Mesh370`, `Mesh371`, `Object005`, `Object068`, `Object069`, `Object070`, `Object071`, `Object072`, `Object073`, `Plane083`, `Plane084` |
| Doorpanel01_DP_01 | 0, 0, 0 / 0.9 / 1 | DoorPanel | `Doorpanel01`, `Doorpanel02`, `Doorpanel03`, `Doorpanel04` |
| fabric brown_BURLAP01 | 0.52941, 0.36078, 0.26667 / 0.9 / 1 | Fabric_Brown | `ChamferBox001`, `ChamferBox004`, `ChamferBox005`, `ChamferBox006`, `ChamferBox007`, `ChamferBox008`, `ChamferBox009`, `ChamferBox014`, `ChamferBox015`, `ChamferBox016`, `ChamferBox017`, `ChamferBox018`, `ChamferBox019`, `ChamferBox020` |
| Leather2_LEATH01 | 0.031373, 0.015686, 0 / 0.9 / 1 | Leather2 | `Armrest01`, `Armrest02`, `Armrest03`, `Armrest04`, `Box001`, `Box003`, `Box004`, `Box005` |
| Leather_LEATH01 | 0.62745, 0.38039, 0.27059 / 0.9 / 1 | Leather | `Mesh1215`, `Mesh1216`, `Mesh1217`, `Mesh1218`, `Mesh1219`, `Mesh1220`, `Mesh1221` |
| Light TL | 1, 0.54902, 0 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh20` |
| light white on to off | 0.588, 0.588, 0.588 / 0.9 / 1 | Sin coincidencia inequívoca | `lightring03`, `lightsring02`, `Object060` |
| LightGr | 0.66275, 0.66275, 0.66275 / 0.9 / 1 | Sin coincidencia inequívoca | `Mainroof`, `Mesh1170`, `Mesh1171`, `Mesh1223`, `Mesh378`, `Mesh379`, `Mesh382`, `Mesh383`, `Mesh385`, `Mesh386`, `Mesh387`, `Mesh416`, `Mesh419`, `Torus001` |
| Lights | 1, 0.97255, 0.91373 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh451`, `Mesh452`, `Mesh453`, `Mesh454`, `Mesh459`, `Mesh491`, `Mesh492`, `Mesh493`, `Mesh494`, `Mesh495`, `Mesh496`, `Mesh497`, `Mesh498` |
| Mainscreen_MVS | 0, 0, 0 / 0.9 / 1 | MainScreen | `Mesh74` |
| Materi04 | 0.62745, 0.56078, 0.49804 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh1173` |
| Material | 0.8, 0.69412, 0.55294 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh1273` |
| Material #53 | 0.090196, 0.090196, 0.090196 / 0.9 / 1 | Sin coincidencia inequívoca | `MSB0030110`, `MSB0030110.MSB0030111`, `MSB0030110.MSB0030112`, `MSB0030110.MSB0030113`, `MSB0030110.MSB0030114`, `MSB0030110.MSB30115`, `MSB0030110.MSB30116`, `MSB0030110.MSB30117`, `MSB0030110.MSB30118`, `MSB0030115`, `MSB0030116`, `MSB0030116.MSB0030123`, `MSB0030116.MSB0030127`, `MSB0030116.MSB0030134`, `MSB0030116.MSB0030173`, `MSB0030116.MSB30174`, `MSB0030116.MSB30175`, `MSB0030116.MSB30176`, `MSB0030116.MSB30177`, `MSB0030117`, `MSB0030117.MSB0030121`, `MSB0030117.MSB0030124`, `MSB0030117.MSB0030128`, `MSB0030117.MSB0030133`, `MSB0030117.MSB30134`, `MSB0030117.MSB30135`, `MSB0030117.MSB30136`, `MSB0030117.MSB30137`, `MSB0030119`, `MSB0030119.MSB0030118`, `MSB0030119.MSB0030120`, `MSB0030119.MSB0030122`, `MSB0030119.MSB0030126`, `MSB0030119.MSB30127`, `MSB0030119.MSB30128`, `MSB0030119.MSB30129`, `MSB0030119.MSB30130`, `MSB0030125`, `MSB0030129`, `MSB0030130`, `MSB0030131`, `MSB0030132`, `MSB0030174`, `MSB30175`, `MSB30176`, `MSB30177`, `MSB30178`, `MSB30179`, `MSB30180`, `MSB30181`, `MSB30182`, `MSB30183`, `MSB30184`, `MSB30185`, `MSB30188`, `Object001`, `Object002`, `Object003`, `Object004`, `Object006`, `Object007` |
| Metal_Co_Metal_Co | 0.75686, 0.75686, 0.75686 / 0.9 / 1 | Metal_Co | `Mesh1409`, `Mesh1410`, `Mesh1414`, `Mesh1415`, `Mesh1416`, `Mesh1417`, `Mesh1418`, `Mesh1448`, `Object067` |
| Metal_Steelplate_Alumb_t | 0.79216, 0.81961, 0.85882 / 0.9 / 1 | Helm_MetalPlating | `Mesh1318`, `Mesh1319`, `Mesh1320`, `Mesh1321`, `Mesh1337`, `Mesh1343`, `Mesh1384`, `Mesh1385` |
| Plaque_VP_col | 1, 0.84314, 0.22353 / 0.9 / 1 | Plaque | `Mesh143` |
| scrn1.1_scn1.1 | 0, 0, 0 / 0.9 / 1 | Scrn1_1 | `Mesh151` |
| scrn1.2_scn1.2 | 0, 0, 0 / 0.9 / 1 | Scrn1_2 | `Plane066` |
| scrn1.3_scn1.3 | 0, 0, 0 / 0.9 / 1 | Scrn1_3 | `Plane086` |
| scrn1.4_scn1.4 | 0, 0, 0 / 0.9 / 1 | Scrn1_4 | `Mesh125` |
| scrn1.5_scn1.5 | 0, 0, 0 / 0.9 / 1 | Scrn1_5 | `Plane041` |
| scrn1.6_scn1.6 | 0, 0, 0 / 0.9 / 1 | Scrn1_6 | `Plane067` |
| scrn1.7_scn1.7 | 0, 0, 0 / 0.9 / 1 | Scrn1_7 | `Plane085` |
| scrn10.1_scn10.1 | 0, 0, 0 / 0.9 / 1 | Scrn10_1 | `Plane089` |
| scrn10.2_scn10.2 | 0, 0, 0 / 0.9 / 1 | Scrn10_2 | `Plane090` |
| scrn10.3_scn10.3 | 0, 0, 0 / 0.9 / 1 | Scrn10_3 | `Plane020` |
| scrn10.4_scn10.4 | 0, 0, 0 / 0.9 / 1 | Scrn10_4 | `Plane021` |
| scrn10.5_scn10.5 | 0, 0, 0 / 0.9 / 1 | Scrn10_5 | `Plane024` |
| scrn10.6_scn10.6 | 0, 0, 0 / 0.9 / 1 | Scrn10_6 | `Plane091` |
| scrn12red | 0, 0, 0 / 0.9 / 0 | scrn12red | `scn12a`, `scn12b` |
| scrn2.1_scn2.1 | 0, 0, 0 / 0.9 / 1 | Scrn2_1 | `Mesh161` |
| scrn2.2_scn6.8 | 0, 0, 0 / 0.9 / 1 | Scrn2_2 | `Plane079` |
| scrn2.3_scn2.3 | 0, 0, 0 / 0.9 / 1 | Scrn2_3 | `Plane080` |
| scrn2.4_scn6.6 | 0, 0, 0 / 0.9 / 1 | Scrn2_4 | `Plane081` |
| scrn2.5_scn2.5 | 0, 0, 0 / 0.9 / 1 | Scrn2_5 | `Mesh163` |
| scrn2.6_scn6.4 | 0, 0, 0 / 0.9 / 1 | Scrn2_6 | `Plane082` |
| scrn2.7_scn2.7 | 0, 0, 0 / 0.9 / 1 | Scrn2_7 | `Plane019` |
| scrn2.8_scn2.8 | 0, 0, 0 / 0.9 / 1 | Scrn2_8 | `Plane064` |
| scrn3.1 | 0, 0, 0 / 0.9 / 0 | Scrn3_1 | `Plane029`, `Plane030`, `Plane031`, `Plane033` |
| scrn3.2_scn3.2 | 0, 0, 0 / 0.9 / 1 | Scrn3_2 | `Plane034`, `Plane035`, `Plane036`, `Plane037` |
| scrn3.3_scn3.3 | 0, 0, 0 / 0.9 / 1 | Scrn3_3 | `Plane028` |
| scrn3.4_scn3.4 | 0, 0, 0 / 0.9 / 1 | Scrn3_4 | `Plane038`, `Plane039` |
| scrn4.1_scn4.1 | 0, 0, 0 / 0.9 / 1 | Scrn4_1 | `Plane016` |
| scrn4.2_scn4.2 | 0, 0, 0 / 0.9 / 1 | Scrn4_2 | `Mesh140`, `Object025`, `Object026` |
| scrn5.1_scn5.1 | 0, 0, 0 / 0.9 / 1 | Scrn5_1 | `Plane032` |
| scrn6.1_scn6.1 | 0, 0, 0 / 0.9 / 1 | Scrn6_1 | `Plane040` |
| scrn6.2_scn6.2 | 0, 0, 0 / 0.9 / 1 | Scrn6_2 | `Plane065` |
| scrn6.3_scn2.9 | 0, 0, 0 / 0.9 / 1 | Scrn6_3 | `Plane087`, `Plane088` |
| scrn6.4_scn6.4 | 0, 0, 0 / 0.9 / 1 | Scrn6_4 | `Plane077` |
| scrn6.5_scn6.5 | 0, 0, 0 / 0.9 / 1 | Scrn6_5 | `Plane078` |
| scrn6.6_scn6.6 | 0, 0, 0 / 0.9 / 1 | Scrn6_6 | `Plane076` |
| scrn6.7_scn6.7 | 0, 0, 0 / 0.9 / 1 | Scrn6_7 | `Plane074` |
| scrn6.8_scn6.8 | 0, 0, 0 / 0.9 / 1 | Scrn6_8 | `Plane075` |
| scrn6.9_scn6.9 | 0, 0, 0 / 0.9 / 1 | Scrn6_9 | `Mesh168` |
| scrn7.1_scn7.1 | 0, 0, 0 / 0.9 / 1 | Scrn7_1 | `Mesh152` |
| scrn7.2_scn7.2 | 0, 0, 0 / 0.9 / 1 | Scrn7_2 | `Plane068` |
| scrn7.3_scn1.3 | 0, 0, 0 / 0.9 / 1 | Scrn7_3 | `Plane069` |
| scrn7.4_scn7.4 | 0, 0, 0 / 0.9 / 1 | Scrn7_4 | `Mesh130` |
| scrn7.5_scn7.5 | 0, 0, 0 / 0.9 / 1 | Scrn7_5 | `Plane070` |
| scrn7.6_scn7.6 | 0, 0, 0 / 0.9 / 1 | Scrn7_6 | `Plane072` |
| scrn7.7_scn7.7 | 0, 0, 0 / 0.9 / 1 | Scrn7_7 | `Plane073` |
| scrn8_scn8 | 0, 0, 0 / 0.9 / 1 | Scrn8 | `Plane071` |
| scrn9_scn9 | 0, 0, 0 / 0.9 / 1 | Scrn9 | `Mesh132` |
| Voygray_Voygray | 0.56078, 0.54902, 0.57647 / 0.9 / 1 | Floor | `floorfront`, `hallwayfloor`, `Mesh1489`, `Mesh1490`, `Mesh1491`, `Mesh1492`, `Mesh1493`, `Mesh1494`, `Mesh1497`, `Mesh1498`, `Mesh1500`, `Mesh1715`, `Mesh572` |
| White | 1, 1, 1 / 0.9 / 1 | Sin coincidencia inequívoca | `Mesh1502`, `Mesh1524`, `Mesh1533`, `Mesh1547`, `Mesh1556`, `Mesh1564`, `Mesh1569`, `Mesh1586`, `Mesh1608`, `Mesh1625`, `Mesh1640`, `Mesh1649`, `Mesh1650`, `Mesh1673`, `Mesh1674`, `Mesh1676`, `Mesh1677`, `Mesh1679`, `Mesh1680`, `Mesh1681`, `Mesh1683`, `Mesh1684`, `Mesh1686`, `Mesh1689`, `Mesh1691`, `Mesh1694`, `Mesh1696`, `Mesh1703`, `Mesh1727`, `Plane004` |
| Window | 0, 0, 0 / 0.9 / 0.2 | Sin coincidencia inequívoca | `Mesh86` |

## Anexo B — Evidencia binaria y geometría prioritaria

Los conteos siguientes usan únicamente el lector instalado, antes de construir/validar una malla. No constituyen un parser independiente validado del MAX.

| Objeto fuente | Vértices leídos | Caras leídas | Caras con vértices repetidos | Caras con índices inválidos | Caras Blender |
|---|---:|---:|---:|---:|---:|
| Mesh69 | 686 | 235 | 2 | 0 | 233 |
| Mesh551 | 0 | 0 | 0 | 0 | 0 |
| Mesh468 | 2242 | 2172 | 0 | 0 | 2172 |
| Mesh1500 | 369 | 373 | 0 | 0 | 373 |
| Mesh1497 | 633 | 15 | 1 | 0 | 14 |
| floorfront | 606 | 2 | 1 | 0 | 1 |
| Mesh1206 | 2270 | 2207 | 0 | 0 | 2207 |
| Mesh993 | 60 | 86 | 0 | 0 | 86 |
| Mesh992 | 71 | 108 | 0 | 0 | 108 |
| Mainroof | 9322 | 14454 | 0 | 0 | 14447 |

El lector aporta conteos de 630 entradas de malla; la primitiva Torus no se decodificó mediante estas rutinas de malla. Todos los registros, distribuciones de longitud de caras, repeticiones y limitaciones están en `max_partial_reader.nodes` del JSON. El cuadro anterior selecciona los objetos prioritarios.

## Anexo C — Localización de datos detallados

`auditoria_voyager.json` contiene inventario completo, no sólo prioridades:

- `input_manifest`, `integrity`: hashes y prueba de integridad de originales.
- `objects`: cada objeto, su procedencia, jerarquía, transformación, visibilidad, geometría, UV, topología y componentes; `material_faces` aporta número de caras y caja física de cada slot.
- `materials`: propiedades, todos los nodos/sockets, valores, enlaces y alcance del output activo; asignaciones separadas legacy_OBJ/MAX.
- `images` y `texture_files`: enlaces, empaquetado, píxeles, candidatos locales y decodificación de 104 recursos.
- `poser`, `material_comparisons`: 142 materiales con líneas MC6 y comparación explícita de propiedades.
- `max_binary`, `max_partial_reader`: estructura CFB, cadenas, metadatos y clases; errores/limitaciones conservados.
- `source_geometry_comparison`: diferencias de caras por objeto entre el lector MAX y Blender, con alcance limitado explícito.
- `texture_reconciliation`, `mesh468_occlusion`, `piece_roles`, `diagnoses`, `future_export`: conciliación de recursos, prueba de cobertura, piezas y plan de recuperación.

El informe no certifica identificación anatómica de cada una de las 631 mallas, ausencia total de defectos ni reproducción del render mental ray. Sí proporciona el inventario trazable para continuar esa recuperación sin mezclar el OBJ.
