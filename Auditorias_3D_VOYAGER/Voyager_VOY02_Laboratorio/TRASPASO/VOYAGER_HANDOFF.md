# Voyager VOY-02 — traspaso exhaustivo desde parada controlada

**Estado: detenido por orden del usuario el 21/10/2026. VOY-02 NO está terminado.** El archivo Blender, los datos, los scripts y las capturas actuales están guardados. La orden de esta sesión es conservarlos y esperar; este documento no activa por sí solo nuevas operaciones.

Leer primero [entorno compartido](UE5_ENTORNO_COMPARTIDO.md), [Sutherland](SUTHERLAND_ESTADO_FINAL.md) y este documento. [VOYAGER_NUEVO_HILO.md](VOYAGER_NUEVO_HILO.md) contiene el encargo listo para una nueva conversación. No es necesario reconstruir el historial de chat para localizar el punto de continuidad.

## 1. Último punto seguro y orden vigente

La última operación de trabajo Voyager terminada fue `SCRIPTS/12_capturas.py`: abrió el `.blend` guardado, generó **33 PNG**, escribió `DATOS/capturas_manifest.json` y terminó con `CAPTURAS_COMPLETADAS 33` / `Blender quit`. El guardado de ocho escenas se había completado mediante `11_construir_escenas.py`, con 49 imágenes empaquetadas. Los dos logs se conservan.

Al inspeccionar las imágenes se detectó que el encuadre de algunas vistas superiores recorta el conjunto: especialmente `G02_conjunto_planta.png` y `D02_planta_camarote.png`. **La parada llegó antes de editar las cámaras, los maniquíes, el script de capturas o reconstruir escenas.** No hay una corrección de encuadre ya aplicada que deba buscarse. El script `12_capturas.py` sigue con su encuadre original.

Durante el traspaso solo se inspeccionaron archivos, procesos y documentación existente, se comprobaron hashes/legibilidad y se escribieron documentos e inventarios en `TRASPASO`. No se ejecutaron nuevas mediciones geométricas, renders, scripts de fabricación, restauraciones, importaciones Unreal o modificaciones de Voyager/Sutherland.

No se encontró ningún proceso Blender/Python de laboratorio/UnrealEditor/UnrealBuildTool pendiente. No se interrumpió un proceso activo ni fue necesario recuperar un guardado parcial. No hay trabajo propio conocido que dependa de una aplicación abierta o de un buffer sin guardar. La inspección de procesos es una instantánea, no una garantía contra actividad futura del usuario.

## 2. Objetivo original y decisiones aprobadas

Proyecto Videojuego Star Trek RPG, repositorio `robdor80/Videojuego_StarTrek`; USS Voyager clase Intrepid. Motor final previsto UE 5.8.2. Herramienta de laboratorio Blender 5.2.2 LTS en MSI Raider Windows 11.

Voyager debe aspirar a un puente excelente, pocos pasillos creíbles, acceso a turbolift y un camarote funcional, con futuras consolas, sillas, puertas y NPC. La Enterprise Valhalla será la nave insignia más extensa. No se pretende reproducir todas las cubiertas ni convertir todos los recursos disponibles en contenido jugable.

VOY-02 investiga mediante pruebas reales si esos interiores pueden construirse con los recursos existentes; no entrega una Voyager terminada ni restaura artísticamente el puente. La primera auditoría VOY-01 se acepta como base: ampliar lo necesario, sin repetir indiscriminadamente el inventario completo.

Autorización VOY-02: copias físicas independientes, escenas `.blend` experimentales, separación/agrupación/transformación de geometría copiada, pivotes provisionales, conectores/adaptadores, maniquíes y cápsulas, pruebas geométricas, capturas/renders/animaciones técnicas, scripts y exportaciones de diagnóstico útiles. No instalar dependencias si las existentes resuelven el trabajo. Autonomía para ensayos en esas copias sin confirmación por cada paso.

Límites aprobados: no modificar originales, Sutherland, Unreal ni activos de producción; no restauración artística definitiva ni integración UE. No presentar un experimento como activo final. No copiar parámetros de movimiento Sutherland sin validación Voyager. No inventar FPS ni coste real de Unreal. No ocultar defectos para aparentar una conexión válida.

La orden posterior de **parada** suspende nuevas operaciones en esta sesión. La reanudación corresponde a la nueva sesión que el usuario inicie con el prompt de continuidad. No se crean restricciones visuales nuevas: las capturas del laboratorio y el ZIP local solicitado siguen formando parte de la misión. La limitación de publicación de imágenes de VOY-01 procede de aquella auditoría y no equivale a prohibir evidencias locales VOY-02.

## 3. Raíces y archivos de entrada

Raíz VOY-02: `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio`.

| Recurso | Ruta exacta |
|---|---|
| Auditoría anterior | `C:\Users\andro\Documents\Auditorias_3D\Voyager_Puente_2026-10-21` |
| OBJ original detallado | `C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ\Voyager Bridge.obj` |
| MTL original | Misma carpeta: `VoyagerB.Mtl` |
| Texturas originales OBJ | Misma carpeta: `VOYBRIDGETEX-1\Textures` |
| Colección nativa original | `C:\Users\andro\Documents\GitHub\3D Star Trek\assets\otros\corridor\Star Trek Voyager Collection\voyager\coleccion_de_pasillos_voyager\star-trek-voyager-collection\source\StarTrekVoyagerCollection.blend` |
| GLB de colección indicado inicialmente por el usuario | `C:\Users\andro\Documents\GitHub\3D Star Trek\assets\otros\corridor\Star Trek Voyager Collection\voyager\coleccion_de_pasillos_voyager\star_trek_voyager_collection.glb` |
| Conversión MAX de referencia | `C:\Users\andro\Documents\Voyager_Bridge_Recovery\originales\Voyager_Bridge_MAX_Trabajo.blend` |
| Copia OBJ de trabajo | `FUENTES\OBJ\Voyager Bridge.obj` bajo la raíz VOY-02 |
| Cache importada OBJ | `FUENTES\OBJ\puente_base_importado.blend` |
| Copia colección | `FUENTES\COLECCION\coleccion_original.blend` |
| Copia conversión MAX | `FUENTES\MAX\puente_max_conversion.blend` |
| Archivo principal entregado parcialmente | `ESCENAS\VOY02_Laboratorio.blend` |

Las rutas relativas de las tablas posteriores parten de la raíz VOY-02. Los scripts resuelven esa raíz desde su propio archivo. Algunos también leen JSON de VOY-01: conservar esa carpeta en su ubicación actual. `11_construir_escenas.py` usa matrices del inventario `Voyager_Puente_2026-10-21\DATOS\blender_blend.json` para reconstruir transformaciones nativas. Los informes de materiales de referencia leen `gltf_Voyager_Bridge_Trabajo.json` y `gltf_validacion_numerica.json` de VOY-01. No trasladar carpetas durante recuperación sin revisar esas dependencias.

## 4. VOY-01 y GitHub: terminado antes de este laboratorio

Se leyeron los nueve Markdown locales de VOY-01 (ocho informes y anexo metodológico), se consultaron metadatos y el índice de la PR #32. Hay copias de los Markdown en `REFERENCIAS`, además de `REFERENCIAS/PR32.json`.

- PR documental: <https://github.com/robdor80/Videojuego_StarTrek/pull/32>.
- Rama: `docs/voyager-3d-audit`.
- Head documentado: `c3a5a0885f39ecdc0d6acaaf7057b6817282efe4`.
- Último estado remoto consultado: abierta, Draft, sin fusionar. No se vuelve a consultar GitHub durante la parada.
- VOY-01 produjo nueve Markdown, inventarios CSV/JSON y **55 capturas locales**. Las imágenes no se publicaron por falta de comprobación suficiente de sus licencias. No se subieron modelos ni texturas.
- El checkout local de `Videojuego_StarTrek` se comprobó limpio en `main`, HEAD `3479faefb9aa56980265c5b03aeab3ba3ddd083f`, durante el traspaso. No se hizo fetch ni se modifica `main`.

La autorización Git anterior era para documentación VOY-01. **VOY-02 no ha creado una rama, commit, PR o publicación.** La entrega pendiente de esta fase es local, incluidos sus documentos y ZIP. No asumir que la PR #32 contiene las nuevas pruebas o escenas.

Base VOY-01 reutilizada: OBJ 630 objetos, 271.705 triángulos validados, UV0 en los 630, 102 materiales y 49 imágenes utilizables. Dimensiones numéricas del puente 13,150 × 13,011 × 3,840; el OBJ no define por sí solo metros físicos. Pasillos blancos con geometría pero sin texturas: ancho exterior típico 3,693, alto exterior 3,114 y altura central interior aproximada 2,816. Pivotes, normales/UV, coincidentes y materiales PBR requieren trabajo futuro; no se han reparado por esta misión.

## 5. Conservación al detener

La comprobación de conservación relee y calcula SHA-256, no reutiliza únicamente tamaño/fecha:

- **115 entradas originales registradas al inicio**: 106 recursos copiados + nueve informes VOY-01; todos sus SHA-256 y metadatos coinciden con `DATOS/entradas_antes.json`.
- Las **106 copias** registradas también coinciden con sus fuentes.
- **207 archivos preexistentes VOY-02** inventariados con ruta relativa/absoluta, tamaño, mtime_ns y SHA-256. Se excluye `TRASPASO`, creada para conservar el estado.
- **59 archivos** de `DATOS` y `CAPTURAS` comprobados: JSON legibles, archivos NPZ con CRC ZIP correcto y PNG verificables mediante Pillow, sin errores.
- Cero procesos relevantes pendientes después de excluir el propio registrador.

Evidencias: [ESTADO_PARADA.json](ESTADO_PARADA.json), [COMPROBACION_ENTRADAS.json](COMPROBACION_ENTRADAS.json), [INVENTARIO_ARCHIVOS.csv](INVENTARIO_ARCHIVOS.csv), [registrar_estado.py](registrar_estado.py).

La legibilidad de JSON/PNG/NPZ no valida las conclusiones físicas. El `.blend` tiene 24.191.156 bytes, comprobados durante el traspaso, y abrió correctamente para las capturas, pero sigue pendiente comparar numéricamente su geometría transformada con la que se usó en las pruebas NPZ. No se abre Blender durante esta parada para completar esa tarea. Los hashes no certifican todo el ordenador o todo Sutherland.

## 6. Qué hay guardado

| Carpeta | Archivos previos al traspaso | Contenido |
|---|---:|---|
| `CAPTURAS` | 33 | PNG reales Workbench; encuadres parcialmente pendientes |
| `DATOS` | 26 | Resultados numéricos JSON y cuatro NPZ de geometría |
| `ESCENAS` | 1 | Un `.blend` con ocho escenas, evitando duplicaciones grandes |
| `FUENTES/COLECCION` | 1 | Copia nativa |
| `FUENTES/MAX` | 1 | Copia conversión MAX |
| `FUENTES/OBJ` | 3 + 102 texturas | OBJ, MTL, cache importada y texturas copiadas |
| `LOGS` | 15 | Ejecuciones, incluido fallo inicial conservado y reintento correcto |
| `REFERENCIAS` | 10 | Nueve Markdown VOY-01 y referencia PR32 |
| `SCRIPTS` | 14 + 1 cache | Scripts `00`–`12` y `geom.py`; cache Python incidental conservada |
| `PAQUETE` | 0 | ZIP todavía no preparado |

No hay todavía nueve informes finales VOY-02, índice README, tablas diagnósticas CSV finales o ZIP compartible. El CSV de inventario en `TRASPASO` es una evidencia de conservación y no sustituye esos entregables.

## 7. Scripts, resultados y ejecución ya realizada

| Script | Ejecución y resultado guardado | Estado |
|---|---|---|
| `00_preparar.py` | Copias físicas y hashes; `entradas_antes.json`, referencias | Completado. **No repetir sobre la entrega:** vuelve a escribir el baseline |
| `01_sondeo.py` | Importación OBJ, lectura colección/MAX; `obj_*`, `modulos_*`, `max_*`, cache `.blend` | Completado tras corregir manejo de malla vacía en MAX; reintento `-- max` correcto |
| `02_mediciones_iniciales.py` | `planos_horizontales_obj.json`, `candidatos_accesos_y_muebles.json`, `modulos_sondeo.json`, `comparacion_escala_max_obj.json` | Sondeos iniciales; no usar extremos de bbox como interfaces finales |
| `geom.py` | Rayos, secciones, distancias segmento-triángulo, cápsulas y soporte; cinco casos analíticos de control superados durante el trabajo | Helper numérico; conservar método y límites |
| `03_interfaces.py` | `interfaces_modulos.json`, 83 mallas clasificadas geométricamente | Completado; puertos candidatos no equivalen a certificación artística de cada módulo |
| `04_ergonomia.py` | `ergonomia_inicial.json` | Incompleto como ergonomía global; puertas inicialmente mal agrupadas, sustituido por 06 |
| `05_correspondencias.py` | `correspondencias_max_obj.json` | Completado para correspondencia medida; requiere Blender/KDTree |
| `06_puertas_escala.py` | `puertas_medidas.json` | Grupos completos de hojas, medidas y pruebas en escalas múltiples |
| `07_ensamblajes.py` | `ensamblajes_pruebas.json` | Siete ensamblajes y sus recorridos ensayados |
| `08_transitos_puente.py` | `transitos_puente.json`, variantes `_1p0`, `_1p15`, `_1p2` | Muestreo de rutas parcial; no certifica circulación completa |
| `09_prototipo.py` | `prototipo_conjunto.json`, `prototipo_geometria.npz` | Dos rutas conectadas pasan ensayos geométricos seleccionados |
| `10_funcional.py` | `preparacion_funcional.json` | Contactos discretos de puertas/sillas y candidatos de pantallas |
| `11_construir_escenas.py` | `ESCENAS/VOY02_Laboratorio.blend`, `escenas_manifest.json` | Guardado terminado, 49 imágenes empaquetadas; falta contraste numérico final |
| `12_capturas.py` | 33 PNG, `capturas_manifest.json` | Terminó; QA visual incompleta y encuadre por corregir |

`habitaciones_sondeo.json` contiene un sondeo adicional de 49 muestras por habitación guardado durante la investigación. Su reconstrucción como script dedicado y documentación del método están pendientes; no perder ese JSON por no verlo asociado a un número de script.

El primer `01_sondeo.log` conserva el fallo de forma de array en una malla MAX vacía. Se corrigió con forma `(-1,3)` y se ejecutó de nuevo únicamente MAX. `01_sondeo_max.log` acredita terminación. No interpretar ese fallo histórico como proceso actualmente abierto ni descartar el resultado correcto posterior.

Los scripts numéricos usan el Python con NumPy de Blender. `01`, `05`, `10`, `11`, `12` usan APIs de Blender y se ejecutaron con Blender en background. Revisar los imports antes de repetir un script. La ruta de `geom.py` se añade explícitamente con `sys.path.insert(0, str(Path(__file__).resolve().parent))` cuando hace falta.

## 8. Métodos y significado de «verificado»

Geometría fuente exportada a NPZ en coordenadas de mundo: `vertices`, `triangles`, `object_ids`, `cross_normals`; metadata por objeto con bbox de superficie usada, origen, escala, materiales y conteos. Las pruebas no usan solo bounding boxes como criterio final de paso.

La cápsula es un segmento vertical con radio 0,35 m; alturas 1,60/1,75/1,90 m según prueba. Se calcula distancia segmento–triángulo con control de intersección y distancias a bordes, tras filtrado espacial. El paso se muestrea cada ≤0,025 m y, en ensamblajes/prototipo, se añade margen de 0,0125 m. El soporte se comprueba aparte cada 0,05 m con cinco rayos de huella (centro y desplazamientos ±0,20 m en X/Y), tolerancia vertical de 0,01 m. Consultar valores concretos de cada JSON: la búsqueda de puente usa otra rejilla/margen.

Límites: son superficies triangulares, no volúmenes sólidos certificados; contacto con superficies puede bloquear, y estar dentro de un volumen sin cruzar su superficie puede escapar a un ensayo superficial. Cápsulas discretas y rayos no son CharacterMovement, NavMesh, animación humana, dinámica de escalones ni certificación de toda la planta. Un `minimum_clearance: null` con cero candidatos significa ausencia de obstáculos en el vecindario examinado; no una holgura infinita medida.

Puertas/sillas: BVH como filtro + SAT de triángulos en 17 ejes, tolerancia de separación 1 µm. Se cuentan contactos e intersecciones, comparando con pose cerrada/original. **No hay solver de barrido continuo** en VOY-02. No confundirlo con el SAT continuo y las pruebas físicas Unreal de Sutherland.

Criterios del usuario para los futuros informes: A verificado y compatible; B compatible con ajustes menores; C viable con adaptación importante; D reconstrucción recomendada; E no demostrado/pendiente. Un ancla alineada y una cápsula que pasa no convierten por sí solas un perfil completo en grado A.

## 9. Escala del puente: hallazgos y pendientes

### Evidencia existente

Se midieron tres accesos con las **hojas completas**, incluidos adornos que el primer sondeo había omitido. Identificaciones y vectores exactos están en `puertas_medidas.json` y `correspondencias_max_obj.json`.

| Acceso | Centro OBJ numérico (x,y,z) | Normal exterior | Carrera por hoja, unidades OBJ |
|---|---|---|---:|
| `D_IZQ` | (−6,303851; 0,183815; 0,021205) | (−0,878742; 0,477298; 0) | 0,4186214 |
| `D_DER` | (6,316095; 0,184453; 0,021205) | (0,878739; 0,477302; 0) | 0,4186216 |
| `D_POST` | (1,191131; 6,382051; 0,712296) | (0; 1; 0) | 0,418619 |

La puerta derecha abierta da aproximadamente 0,757 m de ancho en varias alturas (0,756 a 1,70 m), y rayo vertical central de 1,775576 unidades de altura libre. La posterior da 0,8383 de ancho y rayo central de altura 2,023154, pero molduras desplazadas impiden que ese único rayo certifique todo el volumen de una persona alta. La izquierda da aproximadamente 0,8383 de ancho; el rayo de altura central no encuentra un dintel equivalente y no debe inventarse un rectángulo libre con ese dato.

Con radio humano real 0,35 m y hojas completas desplazadas, alturas 1,60 y 1,75 pasan el tramo ensayado a factor 1,00; **1,90 falla en las tres puertas a factor 1,00**. A **1,10 y superiores probados** pasan las tres alturas. Factores ensayados: 1 / 1,10 / 1,15 / 1,20 / 1,25 / 1,30 / 1,508135. Tramo local a ambos lados del plano de puerta, no recorrido completo de puente.

Se escogió **1,10 como escala de trabajo experimental**, mínimo factor de la serie probada que admite 1,90 m en esos accesos. No es escala final canónica. La altura derecha a ese factor sería aproximadamente 1,953 m: margen pequeño para una referencia de 1,90. El conjunto exterior a 1,10 sería aproximadamente 14,465 × 14,312 × 4,224 m, pero una envolvente no acredita alturas útiles.

Suelo encontrado por sondeo en unidades OBJ: navegación 0,021205; frontal/laterales 0,297639; zona central 0,435856; posterior 0,712296. Son niveles locales, no una medición terminada de cada escalón. El primer impacto sobre Z en la zona posterior era una consola (~0,4684 sobre el suelo), **no el techo**. No trasladar ese resultado a una tabla de altura de techo. Las zonas laterales son estrechas o bajas localmente; falta caracterización completa.

### Lo que sigue pendiente

La escala global aún necesita referencias independientes medidas: asiento, suelo de pies, mesa/LCARS, altura de techo por zona, vanos completos, peldaños y huellas, pasos entre consolas y distancia entre sillones. Hay candidatos de cojines y niveles en `candidatos_accesos_y_muebles.json` y `planos_horizontales_obj.json`, pero no una validación antropométrica terminada. No presentar una bbox de asiento o un primer impacto de rayo como altura ergonómica definitiva.

La elección 1,10 tiene evidencia arquitectónica parcial y no resuelve por sí sola problemas locales de sillas o circulación. El informe debe separar confianza de escala global, ergonomía sentada y fidelidad canónica. No aumentar todo hasta 1,508 para forzar un resultado.

### Familia MAX

Transformación empírica medida: **MAX ≈ OBJ × 1,50813535 + (−0,11236; 1,875563; −0,466607)**. Nueve parejas arquitectónicas independientes coinciden tras esa similitud con error máximo ≤8,80×10⁻⁶ m, según vecinos de vértices; RMS de pocos micrómetros. Los pares incluyen Mainroof, hallwayfloor, centerlight, centerlights01/centerlights, blackinset, centerinset, lightssupport, hallwaypanels y hallwaysubframe.

518/630 mallas MAX encuentran correspondencia de bbox OBJ a <2 mm. **No son equivalentes todos los objetos**: `strudextends` falla con RMS ~0,443 m y máximo ~1,018 m, y hay diferencias en muebles/sillas. El factor no demuestra una conversión estándar de unidades ni la intención del autor; su causa técnica original no está establecida. No mezclar piezas tras normalizar solo una pieza de referencia.

## 10. Pasillos: inventario funcional e interfaces

`interfaces_modulos.json` normaliza cada módulo por centro XY y suelo candidato; contiene bbox local, puertos cardinales, posición, normal de salida, suelo/techo, anchuras a Z=0,4 / 1,0 / 1,7 / 2,2, rayos de bloqueo y segmentos de sección 2 mm dentro del extremo. El predicado evita llamar «puerto» a cualquier extremo decorativo: necesita anchura ≥0,65 m en alturas de prueba, suelo compatible y ausencia de bloqueo central. No acredita acabado completo o todas las orientaciones posibles de las 83 piezas.

| Pieza | Uso identificado | Puertos útiles encontrados |
|---|---|---|
| Mesh12 | Recto corto | Y± |
| Mesh13 | Recto largo | Y± |
| Mesh18 | Recto medio | Y± |
| Mesh41 | Curva | Y−, X+ |
| Mesh40 | T | Y±, X+ |
| Mesh38 | Cuatro vías | X±, Y± |
| Mesh14 | Recto con puertas laterales | Y±; hojas laterales cerradas, no se demostró su tránsito |
| Mesh37 | Acceso de turbolift | Y− ancho, Y+ más estrecho |
| Mesh17 | Cabina de turbolift | Y− |
| Mesh57 | Acceso residencial | Y±; no equivale a habitación completa |
| Mesh4 / Group4 | Envolvente de habitación aprovechada | X− |
| Mesh1 | Otra envolvente aprovechable | Y− |
| Mesh5 / Mesh6 | Envolventes con cambios de nivel | Sin puerto alineado confirmado |
| Mesh81 | Recurso sanitario parcial | Sin puerto confirmado |

Conductos Jefferies, mantenimiento y otros recursos están en inventarios anteriores y de sondeo; su clasificación funcional exhaustiva y sus conexiones transitables no se han completado aquí. No llamar habitación a un acceso residencial o un nicho.

### Ensamblajes realmente probados

Se alinearon anclas, suelo y normales opuestas con matrices registradas. Residual de ancla prácticamente cero numérico no significa perfiles idénticos. La diferencia de sección es Hausdorff aproximada sobre segmentos muestreados a 10 mm.

| Caso | Unión | Grado preliminar por unión | Diferencias relevantes |
|---|---|---|---|
| B01_CORTO_LARGO | 12 Y+ → 13 Y− | B | Ancho igual; sección ~82 mm |
| B02_DOS_RECTOS_CURVA | 13 → 41 → 18 | C / C | Diferencia ancho ~366 mm; secciones ~95 / 41 mm |
| B03_RECTA_T | 18 → 40 → ramal18 | C / C | Diferencia ancho ~366 mm; secciones ~95 / 82 mm |
| B04_CUATRO_VIAS | 18 → 38 → ramal18 | C / C | Diferencia ancho ~366 mm; sección ~39 mm |
| B05_MODULO_PUERTAS | 18 → 14 | B | Diferencia ancho ~220 mm; sección ~82 mm |
| B06_TURBOLIFT | 18 → 37 → 17 | B / C | Diferencias ancho ~146 / 422 mm; sección ~82 / 376 mm |
| B07_RESIDENCIAL | 18 → 57 | B | Diferencia ancho ~220 mm; sección ~82 mm |

Las siete rutas centrales seleccionadas pasan las cápsulas de las tres alturas y los controles de soporte de huella. En la unión a cabina el ensayo amplio de suelo a ±0,9 m falla fuera de la garganta estrecha; el recorrido central de la cápsula sí está soportado. Conservar ambos resultados, no reducir la conclusión a «todo el extremo tiene suelo».

Conclusión parcial defendible: **se pueden formar corredores con rutas coherentes mediante un sistema propio de anclas y ajustes/adaptadores; la biblioteca no queda demostrada como kit de perfiles perfectamente intercambiables**. Ninguna unión obtiene A solo por alineación o por pasar el centro. Falta consolidar inventario funcional, CSV y presentación visual de defectos, sin reclasificar indiscriminadamente todos los módulos.

## 11. Circulación del puente: éxito parcial y negativo importante

`08_transitos_puente.py` busca rutas en una rejilla de 0,15 unidades OBJ, cápsula real H=1,90/r=0,35 inversamente escalada, superficies horizontales Voygray y escalones seleccionados. Desnivel máximo entre vecinos 0,31 m a escala, hipótesis de laboratorio. Los objetivos se ajustan al nodo libre cercano; ese ajuste debe revisarse antes de comparar resultados entre factores.

A factor 1,10 hay 2114 nodos libres muestreados. La ruta `pasarela_al_posterior`, desde aproximadamente (3,6;2,7) a (1,2;6,15) OBJ, longitud 6,15 OBJ, suelo ~0,7143 incluida separación de 2 mm, pasa comprobación de cápsula refinada. Es el origen del prototipo conectado.

`centro_al_posterior` y `navegacion_al_lateral` no encuentran ruta bajo esas condiciones a 1,10. A 1,15/1,20 el resultado sigue parcial. A 1,00 hay una ruta navegación–lateral de 9,45 OBJ, pero con ajuste de objetivo a otro componente cercano; **no deducir que reducir escala mejora físicamente el acceso**. Tampoco concluir inexistencia absoluta de rutas por un fallo de rejilla.

**El conjunto no acredita que se pueda ir desde los sillones centrales o navegación hasta los pasillos.** Acredita una salida desde la pasarela superior posterior hacia el exterior ensamblado. Esta limitación debe aparecer en resumen, capturas y hoja de ruta; no esconderla detrás de la escena G.

## 12. Puente–pasillos y prototipo conjunto

Se eligió el acceso posterior. El puente se escala a 1,10 y traslada para que su umbral posterior sea el origen: `bridge_translation` en el JSON, aproximadamente (−1,310244;−7,020256;−0,783525). La biblioteca permanece a factor 1. Las tres parejas completas de hojas están en pose abierta estática en las pruebas; no se desactiva simplemente su visibilidad.

Instancias guardadas en `prototipo_conjunto.json`:

| Instancia | Fuente | Posición aproximada X,Y (m) | Giro Z |
|---|---|---|---:|
| PASILLO_PRINCIPAL | Mesh13 | 0;3,594560 | 0° |
| CRUCE_CUATRO | Mesh38 | 0;8,209515 | 0° |
| ACCESO_TURBO | Mesh37 | 3,993031;8,209515 | −90° |
| CABINA_TURBO | Mesh17 | 7,982409;8,209515 | −90° |
| PASILLO_CAMAROTE | Mesh18 | 0;11,727188 | 0° |
| CAMAROTE_EXISTENTE | Mesh4 / Group4 | 0;18,538573 | +90° |

Las cotas Z y matrices completas están en los datos; no sustituirlas por esos redondeos al reconstruir.

Seis adaptadores nuevos de diagnóstico, naranjas, con suelo/techo de 6 cm y paredes de 8 cm:

| Adaptador | Longitud m | Ancho libre inicial→final m | Altura libre inicial→final m |
|---|---:|---|---|
| AD_PUENTE | 1,40 | 0,82→3,1808 | 1,95→2,81635 |
| AD_CRUCE | 0,60 | 3,1808→2,9613 | Sección de diagnóstico registrada en JSON |
| AD_RAMAL_TURBO | 0,60 | 2,9613→3,1808 | Ver JSON |
| AD_GARGANTA_TURBO | 0,65 | 1,5715→1,1493 | 2,10→2,10 |
| AD_RAMAL_CAMAROTE | 0,60 | 2,9613→3,1808 | Ver JSON |
| AD_CAMAROTE | 1,40 | 3,1808→1,07979 | 2,81635→2,10 |

No reconstruyen molduras ni resuelven artísticamente diferencias entre familias. Hay superposiciones constructivas de piso y encuentros de perfiles que requieren revisión detallada; no se ha cerrado una tabla de todas las penetraciones. Grado preliminar C para la transición compuesta, no A.

Pruebas sobre **todos los triángulos del puente, los módulos, adaptadores y muebles de prueba**, no sobre cajas sustitutas de arquitectura:

- `PUENTE_AL_TURBOLIFT`: 948 poses por altura; 1,60/1,75/1,90 m, r0,35, todas libres en muestras; soporte de huella correcto.
- `PUENTE_AL_CAMAROTE`: 1110 poses por altura, mismas dimensiones y método; todas libres en muestras; soporte correcto.

Estas rutas empiezan en la pasarela superior verificada, atraviesan el umbral posterior abierto, adaptador, recto y cruce, y terminan dentro de cabina o junto a mobiliario de habitación. No hay ascensor móvil, puerta funcional, NPC o locomoción Unreal. La validación numérica de las transformaciones del `.blend` guardado frente al NPZ de prueba sigue pendiente.

## 13. Camarote: recurso real frente a acceso residencial

Mesh4, agrupación Group4, es la envolvente aprovechada: bbox 8,628 × 6,676 × 2,763 m. El sondeo 7×7 encontró suelo y techo en 49/49 puntos; suelo fuente Z=1,110166, techo 3,87327, altura central ~2,763 m. Puerto X−: ancho ~1,079792 m a Z0,4/1/1,7; estrecha a ~0,80679 a Z2,2. No equivale a certificar que cada pared sea estanca o cada superficie sea válida para colisión.

Mesh1 también da 49/49 muestras de suelo/techo en bbox 5,741 × 8,078 × 4,021 m, con techo variable. Mesh5/Mesh6 dan 43/49 y dos niveles de suelo separados ~0,5597 m; no son sustitutos directos sin resolver escalón. Mesh9 conferencias 28/49 suelo y 25/49 techo; Mesh81 sanitario 21/49 ambos. Las cifras son muestreos, no porcentajes exactos de superficie completa.

Maqueta D y G: cama verde 1,10 × 2,10 × 0,60 m; escritorio 0,65 × 1,40 × 0,75; armario 0,65 × 1,50 × 2,00. Son volúmenes **nuevos de referencia**, no mobiliario recuperado o propuesta de decoración. Hay paso de la cápsula hacia la zona de cama ensayada con esos obstáculos presentes.

Pendiente redactar comparación explícita A adaptar habitación existente / B fabricar habitación con piezas modulares / C estancia nueva coherente con pasillos. Hipótesis inicial favorable a reutilizar Mesh4 como base espacial para el laboratorio; no hay decisión artística final ni confirmación de que su arquitectura sea un camarote canónico. Tampoco se ha acreditado que una puerta de Mesh57 conduzca a una habitación suministrada.

## 14. Preparación funcional: problemas que no deben perderse

### Puertas

Se identificaron hojas completas mediante correspondencia MAX/OBJ, no solo piezas `door` sueltas. Los nombres exactos de 17–18 fragmentos por pareja y sus vectores están en los JSON. El control de cápsula cerrada confirma bloqueo. Ensayo de carrera en fracciones 0/0,25/0,5/0,75/1:

| Puerta | Contactos nuevos frente a cerrada, por fracción | Obstáculos encontrados |
|---|---|---|
| D_IZQ | 0 / 105 / 125 / 146 / 0 | Mesh_1837, Mesh_1855, Object_81 |
| D_DER | 0 / 165 / 196 / 270 / 0 | Mesh_1858, Object_82 |
| D_POST | 0 / 98 / 98 / 100 / 0 | Mesh_1832, Mesh_1833, hallwayfloor_1 |

Son contactos/intersecciones triangulares discretos, no todos penetraciones volumétricas nuevas. **La carrera no está validada**. Que el extremo abierto no cruce superficies no demuestra cavidad para alojar hojas: una hoja podría acabar dentro de una pared cuyo interior no detecta la prueba superficial. Los adapters de G no solucionan esto. No prometer puertas operativas por verlas abiertas en una captura. Grado C preliminar para adaptación funcional, bolsillos/recorrido pendientes.

### Sillas

Cinco grupos provisionales: NAVEGACION 12 partes, LATERAL_DER 31, LATERAL_IZQ 31, MANDO_IZQ 4, MANDO_DER 4. Agrupación por familias y proximidad, no articulación aprobada ni transferencia ciega de sillas MAX. Las candidatas de base fija se proponen por posición baja; falta validar semánticamente asiento/respaldo/base/apoyabrazos y pivotes.

Los ensayos rígidos del conjunto completo +10° y 0,10 m de traslación generan nuevos contactos en los cinco grupos: navegación 1172/696; lateral derecha 30/12; izquierda 50/9; mando izquierda 2701/2193; derecha 2917/2199. Se movió también geometría que quizá debería permanecer fija; no significa que cualquier articulación sea imposible, pero **no hay una silla funcional demostrada**. No copiar los 30 cm de Sutherland. No hay personaje sentado ni alcance real de controles validado.

### Consolas/pantallas

59 objetos con materiales `scrn`/`Mainscreen`; 57 candidatos planos ya independientes (A para esa separabilidad geométrica) y dos B por curvatura/mezcla o error de planitud. `Mesh_1746` / Mainscreen tiene error máximo de plano ~0,09845 m. Los datos contienen nombre/material/plano/triángulos y normal candidata; leerlos antes de elegir una superficie. UV0 conservado. El grado de una superficie no acredita UI, widget, vista ampliada, interacción o materiales emisivos implementados.

## 15. Materiales y rendimiento: iniciado, no cerrado

VOY-01 ya demuestra recuperación de imágenes de color y carencia de una preparación PBR completa (normal/ORM/emisión). Los módulos blancos no tienen texturas. No se han creado materiales artísticos, reconstruido PBR, remapeado UV, reducido texturas o optimizado producción durante VOY-02. Los colores por módulo y adaptador son únicamente diagnóstico.

Lecturas preliminares de los JSON glTF VOY-01: 102 materiales, 101 OPAQUE y uno BLEND `Window` con alfa 0,2; todos `doubleSided`. No confundir la configuración glTF con la política final que adoptará UE. Falta consolidar tabla y recomendaciones Lumen.

Se detectó riesgo por resolución de imágenes, aunque el archivo guardado sea pequeño: 49 imágenes, cálculo preliminar RGBA8 base ~1881,728 MiB y cadena ideal de mipmaps ×4/3 ~2508,97 MiB. **No es memoria real de Unreal ni VRAM medida**: importación, compresión y streaming cambian el coste. Ejemplos registrados: `scn6.4` 7536×5056; `scn6.7`/`scn2.3` 6546×5056; `scn4.1` 10933×2917. Recalcular desde JSON al elaborar la tabla para verificar redondeos, sin cargar/modificar imágenes gigantes si no hace falta. Las hipótesis de límite 2K/4K y su comparación todavía no se han generado.

Distribución de referencia: Leather2 concentra 68.392 triángulos, ~25,2% de los 271.705 del puente. Hay apoyabrazos de ~1500 triángulos. Prioridad futura: evaluar complejidad localizada, repetición, slots, transparencias/doble cara y resolución de pantallas antes de optimizaciones generales. Nada de esto proporciona FPS o un perfil Lumen real.

## 16. Ocho escenas guardadas y evidencias actuales

| Escena del `.blend` | Qué contiene y qué no certifica |
|---|---|
| A_ESCALA_HUMANA_110 | Puente a 1,10, referencias 1,60/1,75/1,90 y cápsulas wire ocultas en render; ergonomía completa pendiente |
| A_COMPARACION_ESCALAS | Fragmentos reales del acceso a 1/1,10/1,15/1,508 y humano de 1,90; no son cuatro puentes completos |
| B_PASILLOS_UNIONES | Siete ensayos repartidos en cuadrícula, fuentes con colores de diagnóstico y puntos de anclaje |
| C_UNION_PUENTE_PASILLO | Puente, transición posterior, primer recto y cruce; puertas abiertas estáticas |
| D_CAMAROTE_ENSAYO | Mesh4, acceso, pasillo y muebles verdes de referencia |
| E_PUERTAS_CARRERA_PRUEBA | Tres parejas completas con contexto y animación 1/49/97; los contactos intermedios siguen presentes |
| E_SILLAS_GRUPOS | Cinco agrupaciones propuestas aisladas; no animación final de sentado |
| G_INTERIORES_CONECTADOS | Puente + red + cabina + habitación + seis adaptadores y muebles de diagnóstico |

Se comparten datablocks de geometría fuente para evitar repetir datos grandes. Se empaquetan 49 imágenes existentes. La copia del OBJ conserva shaders/UV de origen; los módulos usan colores de diagnóstico en instancias de trabajo. Hay colecciones por arquitectura, suelo, consola/pantalla, silla, puertas y referencias; su estructura es ensayo, no activo modular final exportado.

El script de captura usa Workbench/colores difusos y cortes temporales BMesh. No prueba el aspecto de las texturas/PBR ni equivale a un render de acabado. Los cortes no se guardan en el maestro. Títulos y notas figuran en `capturas_manifest.json`; aún no se han incorporado rótulos 2D finales.

Capturas: A01–A05 (5), B00 y dos por cada B01–B07 (15), C01–C02 (2), D01–D03 (3), E01–E04 (4), G01–G04 (4): total **33**, distintas de las 55 de VOY-01. Todas permanecen locales. Ninguna nueva publicación en GitHub.

Defectos conocidos de presentación pendientes:

1. `shot()` calcula `ortho_scale=radius*2.08` sin asegurar encuadre con el aspecto de imagen. G02 y D02 recortan extremos verticales. Corregir mediante proyección de bounds sobre ejes right/up de cámara y encuadre dependiente de relación de aspecto; valorar formato vertical para plantas largas. Es una propuesta aún no aplicada.
2. En B, `subset` solo filtra el cálculo de cámara, **no oculta** otros módulos del mosaico. Algunos encuadres pueden mostrar casos vecinos. Si se corrige, ocultar/restaurar temporalmente solo para la captura y documentarlo.
3. Las siluetas sencillas tienen torso y cabeza separados por un hueco visible; no se ha añadido cuello. Mantener alturas y huella correctas si se mejora su legibilidad. No interpretar esos muñecos como rig humano ergonómico.
4. Las cámaras de `12_capturas.py` viven en memoria para render y no se guardan en el maestro. Puede convenir una presentación inicial útil al abrir el `.blend`, sin alterar geometría ni esconder problemas.
5. La vista «planta acotada» actual tiene título con envolvente y referencias, pero todavía **no es una lámina completa de cotas ergonómicas verificadas**. Faltan cotas de pasos/puertas/alturas y leyendas, no solo encuadre.

## 17. Entregables pendientes del encargo VOY-02

Crear en la raíz del laboratorio, cuando se reanude y se cierre la evidencia:

- `00_RESUMEN_EJECUTIVO.md`.
- `01_ESCALAS_ERGONOMIA.md`.
- `02_MODULARIDAD_PASILLOS.md`.
- `03_CONEXION_PUENTE_PASILLOS.md`.
- `04_CAMAROTE_JUGADOR.md`.
- `05_PUERTAS_SILLAS_CONSOLAS.md`.
- `06_MATERIALES_RENDIMIENTO.md`.
- `07_HOJA_DE_RUTA_RECOMENDADA.md`.
- `08_PRUEBAS_Y_LIMITACIONES.md`.

Además: índice navegable; tablas CSV/JSON consolidadas de medidas, clasificación funcional, interfaces, matrices, compatibilidades, incidencias y pruebas; scripts y registros conservados; imágenes revisadas con éxitos **y** defectos visibles; ZIP de informes/tablas/capturas para compartir con ChatGPT. El usuario permite mantener `.blend` fuera del ZIP si resulta grande y exige indicar sus rutas exactas. No hace falta duplicar el mismo archivo Blender por cada escena.

La hoja de ruta debe separar: tareas autónomas Blender, decisiones artísticas del usuario, pruebas UE5, sistemas reutilizables de Sutherland, dependencias de futuros sistemas del juego y trabajos razonables de posponer. Priorizar incertidumbre técnica, no ampliar todas las cubiertas.

## 18. Clasificación del estado por subsistema

| Subsistema | Terminado/comprobado | Pendiente o no demostrado |
|---|---|---|
| A Escala | Puertas completas y comparación de factores; similitud MAX en arquitectura | Ergonomía de asientos/controles/escalones y recomendación global definitiva; circulación integral |
| B Modularidad | Siete ensamblajes con matrices y cápsulas/soporte en recorridos seleccionados | Perfiles completos, catálogo funcional exhaustivo, acabados, galerías/CSV finales |
| C Puente–pasillo | Conexión posterior con adaptador y cápsulas en modelo numérico completo | Contraste del `.blend`, revisión detallada de encuentros; funcionamiento de puertas |
| D Camarote | Envolvente real Mesh4, proxies y recorrido seleccionado | Comparación A/B/C y validación de arquitectura/colisión completa; decisiones artísticas |
| E Funcional | Hojas/grupos/pantallas identificados; defectos de movimiento detectados | Bolsillos y carrera de puertas, articulación silla, postura y UI |
| F Material/rendimiento | Hallazgos iniciales y base VOY-01 | Informe, tablas, propuestas PBR/slots/luces; ninguna medida UE real |
| G Conjunto | Modelo numérico y escena construidos, dos rutas parciales geométricas correctas | QA final de escena/imágenes y acceso desde centro del puente |
| Documentación/paquete | Scripts, logs y JSON; este traspaso | Nueve informes, índice y ZIP VOY-02 aún no realizados |

Un resultado «terminado pero pendiente de validación» importante es el `.blend`: guardado y abierto para render, pero no contrastado numéricamente con NPZ. Las capturas existen y son legibles, pero su presentación no está aprobada. Un resultado «iniciado incompleto» es ergonomía integral y materiales/rendimiento. «Todavía no iniciado» incluye restauración artística, integración Unreal, sistemas definitivos y paquete final.

## 19. Recuperación y siguiente operación exacta

Primero, en la nueva conversación, leer estos documentos y el estado guardado. Comparar `ESCENAS/VOY02_Laboratorio.blend`, scripts, JSON y capturas con `INVENTARIO_ARCHIVOS.csv`. Si hay cambios del usuario desde esta parada, identificarlos antes de repetir una etapa. No sobreescribir el inventario de parada para ocultar diferencias.

Abrir o inspeccionar el `.blend` de laboratorio con `use_scripts=False` si se hace desde Python, sin guardar por defecto. Sus ocho escenas están listadas en `DATOS/escenas_manifest.json`. Un render ya lo abrió correctamente, pero falta la comprobación específica de fuentes y transformaciones. Verificar que los 630 objetos OBJ, las instancias modulares y los adaptadores usados por G corresponden a las posiciones/triángulos probados en `prototipo_conjunto.json`/NPZ, incluida la traslación de hojas completas. Mantener las etiquetas de geometría existente frente a nueva de prueba.

**Siguiente edición pendiente:** función `shot()` de `SCRIPTS/12_capturas.py`, para corregir encuadre y aislamiento de casos. No estaba empezada. Si solo cambian cámaras/cortes temporales, repetir únicamente capturas afectadas o renderer; no importar de nuevo fuentes, rehacer anclas, reconstruir geometría ni repetir todos los ensayos. Si se mejora el maniquí o la presentación guardada mediante `11_construir_escenas.py`, justificar la reconstrucción, conservar el estado anterior con criterio y revalidar cambios relevantes. No hacer copias grandes innecesarias.

Después, completar las medidas ergonómicas que faltan, con referencias independientes y sin forzar una escala. Prioridad original: 1 escala humana/arquitectura; 2 pasillos; 3 conexión puente; 4 camarote; 5 puertas/sillas/consolas; 6 materiales/rendimiento; 7 conjunto; 8 hoja de ruta. Aunque G ya exista, A no está cerrada y sus negativos no desaparecen por haber construido G.

No existe un proceso interrumpido que exija reinicio. Si se perdiera un archivo generado, recuperar **solo esa etapa** desde sus entradas verificadas:

- JSON/NPZ fuente perdido: revisar `01_sondeo.py`; la rama MAX puede repetirse con `-- max`, sin rehacer OBJ si está correcto.
- Ensamblajes: `07_ensamblajes.py` usa interfaces y geometría ya exportadas.
- Prototipo numérico: `09_prototipo.py` usa los resultados previos y produce sus propios JSON/NPZ.
- `.blend` de escenas: `11_construir_escenas.py` usa cache OBJ, copia colección y datos previos. Sobrescribe el laboratorio generado, no originales; no ejecutarlo por mera lectura del handoff.
- Capturas: `12_capturas.py` abre el maestro y guarda PNG/manifest; sus cortes no escriben el maestro. Reparar el encuadre antes de considerarlas finales.

Ejemplo futuro de script puramente numérico:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\5.2\python\bin\python.exe' `
  'C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\SCRIPTS\07_ensamblajes.py'
```

Ejemplo futuro dentro de Blender, solo para la etapa que realmente necesite repetirse:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python `
  'C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\SCRIPTS\11_construir_escenas.py'
```

`00_preparar.py` **no debe repetirse en este laboratorio** porque reescribe `entradas_antes.json`. No borrar logs de fallos o sondeos sustituidos; señalar cuáles son históricos y cuáles autoritativos. Si se repiten cálculos por un cambio real, conservar trazabilidad de ese cambio y la evidencia anterior relevante.

## 20. Riesgos, información no resuelta y alcance de este traspaso

- La orden original VOY-02 recibida termina con una frase truncada («No sacrifiques verifi…»). Se conservan los requisitos explícitos completos conocidos; no se inventa el resto.
- El origen de escala física del OBJ y la causa del factor MAX no están establecidos. 1,10 sigue siendo hipótesis de trabajo con evidencia parcial, no conclusión final.
- Paso desde pasarela posterior sí; conexión jugable desde toda la zona central del puente no. No ocultar esa diferencia al presentar el conjunto.
- Las puertas abiertas estáticas del prototipo no tienen mecanismos certificados y sus carreras tienen contactos. Las sillas no tienen articulación ergonómica validada.
- Las capturas recortadas no sirven como prueba visual completa de extremos fuera del encuadre; se conservan como evidencia de trabajo, no como láminas finales.
- Los informes Sutherland son históricos y su aprobación humana no se deduce de sus tests. Parte de las respuestas antiguas del chat solo se recupera como referencias de contenido no resueltas; los archivos locales son la fuente útil.
- No se ha hecho rehash de todos los modelos del ordenador o todos los laboratorios Sutherland. Sí se preservan y verifican las 115 entradas iniciales de VOY-02; no se escriben sus fuentes.
- No hay capturas nuevas publicadas, ZIP listo, informe final VOY-02 ni aprobación de producción. No se debe decir lo contrario en la siguiente sesión.

**Estado seguro de continuidad:** los resultados existentes están en disco, inventariados y sin procesos propios pendientes. Esta sesión se detiene tras el traspaso y espera al usuario. La próxima sesión puede continuar desde aquí sin reconstruir indiscriminadamente VOY-01 ni los ensayos ya correctos.
