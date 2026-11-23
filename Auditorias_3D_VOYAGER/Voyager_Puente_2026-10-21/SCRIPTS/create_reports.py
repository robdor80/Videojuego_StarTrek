import json,csv,collections,hashlib,sys,platform
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'DATOS'
def read(n):return json.loads((D/n).read_text(encoding='utf8'))
def write(n,s):(R/n).write_text(s.strip()+'\n',encoding='utf8')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(c).replace('|','/') for c in row)+' |' for row in rows)
def link(p):return f'[{Path(p).name}](<{p}>)'
LIB=Path(r'C:\Users\andro\Documents\GitHub\3D Star Trek');COL=LIB/r'assets\otros\corridor\Star Trek Voyager Collection\voyager\coleccion_de_pasillos_voyager';OBJ=Path(r'C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ');REC=Path(r'C:\Users\andro\Documents\Voyager_Bridge_Recovery');ST=Path(r'C:\Users\andro\Documents\StarTrek_3D')
PBRPATH=Path(r'C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\docs\roadmap\master\fases\F07\P02_PIPELINE_PBR_BLINDAJE.md')
inv=read('inventario_archivos.json');raw=read('gltf_validacion_numerica.json');coll=read('blender_blend.json');rg=read('blender_recovery.json');osplit=read('blender_obj_split.json');deep=read('deep_obj_split.json');mat=read('materiales_auditoria.json')
issue_rows=[
 ['V01','Puente de colección / superficies','No contiene imágenes ni mapas; FrontColor blanco','JSON glTF, ocho materiales; .blend sin nodos de imagen','Alta artística','No hay LCARS ni acabado de puente recuperables de esta familia','Crear arte en fase futura; conservar colores actuales como referencia','C'],
 ['V02','Puente de colección / puestos','Solo ocho objetos de malla en Group_52_1: carcasa, techo, cinco barandillas y residuo; sin sillas reconocibles','Jerarquía, islas soldadas y vistas de corte','Alta funcional','Necesita mobiliario y estaciones para un puente jugable','Usar puente detallado como base; no dedicar primera fase a completar este esquema','C/D'],
 ['V03','Conversión MAX / floorfront','606 vértices, solo 13 usados; 1 cara, 11 triángulos, área 0,000133254 m²','Área en mundo de caras referenciadas; contraste OBJ floorfront_1','Crítica para tránsito','El bounding box de 19,83 m engaña: los vértices sueltos no sostienen un personaje','Recuperar desde OBJ; no rellenar a ciegas esta conversión','D'],
 ['V04','Conversión MAX / Mesh1497','633 vértices, 531 sueltos; 14 caras, 86 triángulos, 7,8545 m² parciales','Deep geometry en mundo','Alta','No representa una plataforma completa por su envolvente','Comparar con grupos OBJ correspondientes y recuperar superficies','C'],
 ['V05','Conversión MAX / materiales','90 materiales usados con caras sin nodo de imagen; las 49 imágenes del OBJ heredado apuntan a rutas inexistentes aquí','Nodos, asignaciones por cara y resolución de rutas en ubicación ORIGINAL','Alta artística','La biblioteca de imágenes del .blend no demuestra texturizado de las piezas MAX','Reconstruir asignaciones desde MTL/MC6; preferir OBJ ya enlazado','C'],
 ['V06','Conversión MAX / ensamblaje','Incluye OBJ antiguo visible además de 631 mallas MAX; Mesh992/Mesh993 alejadas; 520 mallas MAX con escala no unitaria','Inventario y matrices mundo','Alta','Duplicación visible, exportación accidental y escala/pivotes incoherentes','Excluir por identidad el OBJ heredado en futuros derivados; revisar transformaciones y piezas alejadas','C'],
 ['V07','Paneles MAX Mesh468/Mesh1206','Ambos tienen normales hacia abajo; superficies coincidentes en planta separadas unos 8,017 mm; cubierta actual opaca','Área orientada mundial y cotas Z; informe previo de cobertura como evidencia histórica','Alta visual / media geométrica','Añadir emisión no bastaría para hacer visibles los paneles desde arriba','Resolver intención óptica y capas, normales y espesor en copia futura','C'],
 ['V08','OBJ / GLB detallado / topología','578 triángulos casi nulos; 5.439 coincidencias mundiales adicionales tras importación a cuantización 10 µm','Blender + comparación de triángulos; raw glTF separa duplicados por primitiva','Media; pendiente de revisión localizada','Posible z-fighting y problemas de sombreado; parte puede ser doble superficie intencionada','Revisar candidatos por componente; no borrar automáticamente caras coincidentes','B/C'],
 ['V09','OBJ detallado / UV','630/630 objetos con UV0; 11.919 triángulos UV degenerados en GLB leído en bruto; 11.921 con caché Blender','Accesores y UV por loop','Media/alta para nuevo arte','UV existente útil para colores/LCARS; no es un atlas limpio ni garantiza normal mapping','Conservar UV0 legible; rehacer solo zonas afectadas y añadir canal si se requiere horneado','B/C'],
 ['V10','Puente detallado / materiales PBR','49 imágenes sanas, 50 referencias BaseColor; sin mapas normal/ORM/AO ni emisión','JSON glTF y render Cycles original','Alta artística','Pantallas reflejan luz, no emiten; superficies sin respuesta PBR específica','Restauración selectiva de PBR y emisión; no falta toda la textura','C'],
 ['V11','OBJ separado / pivotes y jerarquía','630 objetos independientes, todos con origen mundial (0,0,0); sin animación ni jerarquía funcional','Importación OBJ con split groups; matrices','Media para interacción','Ser objeto separado no lo convierte en puerta/silla lista para animar','Agrupar componentes por mecanismo y establecer pivotes/raíces medidos','B/C'],
 ['V12','Colección / exportación','15 triángulos de índices duplicados; Blender deja 67.548 frente a 67.563 almacenados','Lectura BIN y caché Blender; tripletas de índices repetidas','Baja localizada','Recuentos difieren sin implicar pérdida de 15 piezas','Usar recuento por método; revisar al preparar exportación','B'],
 ['V13','Colección / residuo puente','Mesh105: triángulo de unos 1,3 × 1,9 mm, a ~39 m de la carcasa','Coordenadas en mundo','Baja','Distorsiona encuadre y envolvente de Group_52_1','Excluir del derivado futuro tras revisión; no se ha eliminado del original','B'],
 ['V14','Módulos / ensamblaje','Rectos comparten sección muestreada; están desplegados en catálogo, no conectados; módulos elevados en Z','Rayos BVH y posiciones originales','Media','No existe red recorrible construida ni conexiones garantizadas en toda la colección','Normalizar anclajes y probar uniones en copia futura','B'],
 ['V15','Escala / variantes','Mainroof MAX es ~1,5081 veces el OBJ en sus tres dimensiones; las fuentes no comparten escala práctica','Comparación de cajas de superficies de Mainroof/Mainroof_1','Alta si se mezclan piezas','Transferir materiales por nombre o superponer modelos no alinea la geometría','Calibrar con asiento, vano y cápsula antes de mezclar; no aplicar escala global en esta auditoría','E/B'],
]
with (D/'hallazgos.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['id','componente','observacion','comprobacion','gravedad','consecuencia','recomendacion','grado']);w.writerows(issue_rows)
(D/'hallazgos.json').write_text(json.dumps([dict(zip(['id','componente','observacion','comprobacion','gravedad','consecuencia','recomendacion','grado'],x)) for x in issue_rows],indent=2,ensure_ascii=False),encoding='utf8')
grade_rows=[['Imágenes embebidas del GLB detallado','A','49/49 decodificadas; datos reutilizables, sin afirmar calidad final PBR'],['OBJ original + MTL vigente','B como fuente / C como puente final','630 grupos recuperables, UV y mapas conservados; requiere saneado y preparación'],['Puente detallado exportado GLB','B como referencia / C para interacción','Una malla con 102 primitivas; materiales legibles; organización fusionada'],['Sillas y consolas OBJ separadas','B/C','Geometría real y piezas independientes; pivotes, agrupación, ergonomía y PBR pendientes'],['Carcasa del puente de colección','C','Muy simplificada y fusionada; sin mobiliario ni arte de estaciones'],['Sillas/LCARS ausentes de la colección','D: crear o tomar de otra fuente','No hay base suficiente en esta familia para esos elementos'],['Pasillos rectos/curvos y cruces','B','Secciones compatibles en muestras; falta ensamblaje, materiales y colisiones'],['Conductos Jefferies / mantenimiento','B','Existen módulos; dimensiones de conducto, no circulación humana de pie'],['MAX convertido: floorfront','D para esta conversión','Recuperación preferible desde OBJ'],['Resto de conversión MAX','C','Más separación que GLB, pero escala, suelo y materiales problemáticos'],['MAX binario original','E','Inventariado; no abierto en 3ds Max ni certificado'],['Transitabilidad, NPC, rendimiento UE5','E','No se abrió Unreal; no hay prueba dinámica en esta misión']]
with (D/'aprovechamiento.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['componente','grado','justificacion']);w.writerows(grade_rows)
write('01_RESUMEN_EJECUTIVO.md',f'''
# Auditoría técnica y artística USS Voyager

Fecha: 21/10/2026 (Europe/Madrid). Diagnóstico exclusivamente. **No se restauró, texturizó, animó, exportó un modelo preparado ni se abrió Unreal.**

## Decisión principal

Tenemos **dos familias distintas**: una colección modular de arquitectura simplificada y un puente detallado procedente de OBJ/MAX. La colección indicada por el usuario **sí incluye una carcasa de puente**, además de pasillos, pero no es la mejor base para un puente protagonista. Su aspecto blanco procede del contenido real: ocho materiales constantes y cero texturas.

La mejor base de recuperación es **{link(OBJ/'Voyager Bridge.obj')}**, junto con **VoyagerB.Mtl** y **VOYBRIDGETEX-1/Textures**. Una importación temporal con separación por grupos recupera **630 objetos**, **271.705 triángulos**, **UV0 en los 630** y **49 imágenes con rutas válidas**. El GLB de trabajo conserva esas imágenes embebidas y sirve como referencia visual portable; su única malla fusionada lo hace menos cómodo como máster de edición.

La conversión `Voyager_Bridge_MAX_Trabajo.blend` contiene 631 mallas MAX separadas más el OBJ heredado, pero no gana por estar más fragmentada: tiene pérdida de superficie de suelo, materiales sin texturas, escala diferente y elementos alejados. Se conserva como fuente secundaria de comparación, no como base automática.

## Qué significa para el proyecto

1. **Puente geométrico:** el detallado contiene arquitectura, techo, suelo/plataformas, escalones, dos sillones de mando, tres asientos de estaciones, consolas, pantallas, barandillas, puertas y cabina. No es un puente jugable validado. La colección es mucho más esquemática; su mobiliario principal no está modelado.
2. **Materiales:** en la colección no hay imágenes que recuperar. En el puente detallado hay 49 imágenes sanas; el GLB las muestra. La conversión MAX no las asigna a sus 90 materiales usados. El blanco tiene, por tanto, causas diferentes según archivo.
3. **Aprovechamiento:** imágenes A; OBJ de origen B como fuente; puente final C por preparación artística y funcional. Pasillos B. El suelo frontal de la conversión MAX es D en esa conversión: es mejor recuperar el del OBJ. MAX original y funcionamiento UE5, E.
4. **Módulos:** rectos, curvas, cruces T/4 vías, accesos, turbolift, conductos, mantenimiento y habitaciones/recesos tienen potencial. Son piezas separadas en una lámina de catálogo, no una nave ensamblada.
5. **Trabajo para Unreal 5.8.2:** agrupar por función, revisar escala humana y vanos, limpiar problemas localizados, conservar UV0 útil, preparar PBR/emisión, independizar mecanismos con pivotes y diseñar colisiones. Después haría falta un laboratorio aislado con pruebas reales de tránsito, puertas, NPC y rendimiento.
6. **Primer trabajo recomendado cuando se autorice:** preparar una copia del OBJ separado con un solo recorrido de prueba —acceso, suelo, consola y silla—, antes de invertir en texturizado de todo el puente. Resolver escala y colisiones del recorrido y comparar materiales con el GLB. No reconstruir desde cero el puente de la colección mientras exista esta fuente más completa.

## Limitaciones que cambian la decisión

La cota del conjunto OBJ es **13,150 × 13,011 × 3,840 m** tras conversión Y-up→Z-up, con unidades interpretadas como metros. No prueba ergonomía. La conversión MAX tiene diferencias de escala de ~1,5081 en una pieza contrastada; no se deben mezclar coordenadas sin calibración. Los recuentos de coincidencias/UV son indicadores numéricos, no una orden de borrado ni una prueba exhaustiva de intersecciones. No se abrió el MAX binario con un lector completo.

## Entrega

Los ocho informes solicitados están en `{R}`. Datos y evidencias: `DATOS/`, scripts reproducibles: `SCRIPTS/`, registros: `LOGS/`, catálogo visual: `CAPTURAS/INDICE.md`. Consultar `09_METODO_FUENTES_LIMITACIONES.md` y `DATOS/hallazgos.csv` para métodos y gravedad. La auditoría termina aquí; no se inicia la siguiente fase.
''')
inventory_rows=[]
for f in inv['files']:
 if f['extension'] in ['.glb','.blend','.max','.obj','.mc6','.mtl','.zip'] and 'Suntherland'not in f['path']:
  inventory_rows.append([link(f['path']),f['extension'],f['bytes'],f['sha256']])
write('02_INVENTARIO.md',f'''
# Inventario y procedencia

Se inspeccionó la biblioteca `C:\\Users\\andro\\Documents\\GitHub\\3D Star Trek` (1.321 archivos enumerados; no se recorrió `.git`). La ruta histórica existe. La ruta facilitada es la ubicación actual normalizada de la colección; las fichas antiguas conservan una ubicación anterior que ya no existe. Se consultaron metadatos de `StarTrek_3D_Library/03_METADATA`, que señalaron la carpeta concreta del Escritorio; no se escaneó todo el disco.

## Modelos, fuentes y derivados reales

{table(['Ruta','Formato','Bytes','SHA-256'],inventory_rows)}

La copia MAX editable del Escritorio y la de `Voyager_Bridge_Recovery/originales` tienen **el mismo SHA-256**. El ZIP de la colección contiene únicamente `source/StarTrekVoyagerCollection.blend`; su hash coincide con el `.blend` extraído. No son versiones adicionales independientes.

## Materiales y dependencias

- Colección: `.glb`, `.blend`, ZIP, README y metadata.json; no aparecen imágenes en esa carpeta ni dependencias de imagen en ambos modelos.
- Puente detallado del Escritorio: OBJ, MTL vigente, MTL anterior, informe de reparación, dos BLEND y GLB; **102 archivos de imagen** externos, todos decodificados. El OBJ declara `mtllib VoyagerB.Mtl`.
- Recovery: MAX de 2011, MC6, BLEND de conversión y **104 imágenes**, todas decodificadas. Hay candidatos por nombre para las 49 imágenes declaradas en el BLEND, pero las rutas originales de ese BLEND apuntan a `VOYBRIDGETEX-1/Textures`, carpeta inexistente dentro de Recovery. Sus imágenes actuales están en `VoyagerBridge`.
- En los dos directorios hay 206 imágenes externas contadas como archivos físicos, no 206 diseños únicos. El GLB detallado embebe 49 imágenes y crea 50 referencias de textura.

`DATOS/inventario_archivos.csv` contiene 230 archivos coincidentes del ámbito localizado, incluidos recursos Sutherland inventariados sin abrirlos. `DATOS/texturas_externas.csv` enumera tamaños, resoluciones, hashes y decodificación. No se encontraron otras versiones Voyager en la biblioteca histórica por nombre/ruta y fichas consultadas; no se afirma que no existan bajo otros nombres en ubicaciones ajenas al alcance.

## Referencias históricas que no equivalen a recursos actuales

Los JSON de `StarTrek_3D_Library/03_METADATA` mencionan descargas `star_trek_-_intrepid_type`, `uss_voyager_4k_textures_star_trek_intrepid` y `voyager_ncc_74656` en Downloads; esas rutas exactas no existen. Son referencias de nave exterior o de identidad no comprobada, no puentes adicionales auditados. Las carpetas `01_BLENDER` y `02_GAME_READY` consultadas no aportaron modelos Voyager físicos.

El GLB de colección declara internamente autor `scrimshawsean`, título `Star Trek Voyager Collection`, generador `Sketchfab-12.68.0` y licencia CC-BY-4.0. Son **metadatos declarados en el archivo**, no una verificación externa de licencia ni de derechos de franquicia. La familia OBJ/MAX no se atribuye al autor de la colección.
''')
metrics=[]
for name,label in [('Colección GLB importada','glb'),('Colección BLEND nativo','blend'),('OBJ original separado','obj_split'),('OBJ BLEND fusionado','obj_work'),('Puente GLB texturizado','obj_export'),('BLEND Recovery completo (MAX + OBJ)','recovery')]:
 j=read(f'blender_{label}.json');ms=j['meshes'];metrics.append([name,len(j['objects']),len(ms),sum(m['vertices'] for m in ms),sum(m['triangles'] for m in ms),len(j['materials']),f"{sum(bool(m['uv']) for m in ms)}/{len(ms)}"])
distribution=collections.Counter()
for o in deep['objects']:distribution.update(o['material_triangles'])
top=distribution.most_common(10)
write('03_GEOMETRIA.md',f'''
# Geometría, arquitectura y escala

## Recuentos reproducidos

{table(['Archivo/método','Objetos','Mallas','Vértices almacenados','Triángulos Blender','Materiales datablock','Mallas con UV'],metrics)}

La colección contiene **488 nodos / 317 mallas / 317 primitivas glTF**, **99.615 vértices por suma de primitivas** y **67.563 triángulos almacenados**. Blender valida 15 caras duplicadas de índices y conserva 67.548. Son diferencias de método, no elementos desaparecidos. El `.blend` nativo contiene 189 objetos, 83 mallas y 71.738 triángulos calculados desde polígonos; su triangulación no es idéntica a la exportación glTF. No se certifica equivalencia cara por cara.

El OBJ crudo tiene 254.270 posiciones, otras tantas UV/normales, 630 grupos y **271.911 caras triangulares**. Hay 206 tripletas duplicadas dentro de su mismo grupo; la importación temporal validada conserva 271.705. El BLEND fusionado tiene el mismo recuento de triángulos; el GLB texturizado tiene **1 nodo, 1 malla y 102 primitivas**, con 255.754 vértices por particiones de material/atributos. No son 102 objetos interactivos.

En Recovery no deben sumarse las dos versiones como si fueran una estancia: **631 mallas MAX, 184.697 vértices, 212.147 caras y 261.433 triángulos**, más el antiguo OBJ de 271.705 triángulos. La escena completa da 533.138 porque superpone ambas familias. Tiene 11 empties. Se verificó que el OBJ heredado está visible en el archivo cargado.

## Arquitectura del puente de colección

El grupo fuente `Group_52_1` contiene **8 objetos de malla**, con **3.213 triángulos Blender** frente a **3.183 almacenados en su subárbol GLB**. Siete piezas son principales y una es un residuo diminuto.

{table(['Pieza fuente','Triángulos','Interpretación contrastada'],[['Mesh103',1950,'Carcasa fusionada: planta, niveles, muros, volúmenes de consola y accesos'],['Mesh104',764,'Techo/domo, con nervios geométricos'],['Mesh98',184,'Barandilla central'],['Mesh99 / Mesh100', '80 / 80','Barandillas laterales'],['Mesh101 / Mesh102','77 / 77','Barandillas y soportes'],['Mesh105',1,'Residuo de 1,3 × 1,9 mm, lejos de la carcasa']])}

La carcasa mide **18,017 × 18,241 × 3,780 m**; el techo, **13,935 × 13,935 × 0,979 m**. Es una envolvente reconocible, con suelo y techo reales, escalones/barandillas y accesos representados. Se observan volúmenes simples para puestos y pantalla frontal, pero no pantallas LCARS, controles detallados ni sillas. No se pueden asignar estaciones científicas/tácticas concretas por estos bloques blancos. Los cortes diagnósticos omiten caras por encima de Z=2,50 m; no confundir la falta de paredes altas en ellos con una ausencia original.

La arquitectura no es un sólido cerrado certificado: `Mesh103` se vuelve una sola isla conectada tras soldadura diagnóstica y no ofrece separación funcional entre puertas, suelos y carcasas. Cinco barandillas sí son objetos propios. La ausencia de un sólido watertight no implica por sí sola un defecto en un escenario de superficies abiertas.

## Arquitectura del puente detallado

Las vistas y las asignaciones confirman suelo, plataforma de mando, escalones, cerramiento curvo, techo, luminarias modeladas, pantalla principal, banco posterior de consolas, puestos laterales, puesto frontal, dos sillones centrales y tres asientos de estaciones. Hay puertas, controles de acceso y cabina circular. Los gráficos LCARS son **imágenes sobre superficies**, no botones o circuitos modelados uno a uno. Las carcasas, muebles, barandillas y geometría de luminarias sí existen.

En el OBJ hay separación recuperable por 630 grupos; en los derivados fusionados esa estructura no está presente como objetos. Se comprobó directamente `floorfront_1`: **613 triángulos y 32,829204 m²**, frente a la superficie mínima de la conversión MAX. El techo `Mainroof_1` tiene 14.452 triángulos. No se declara una estancia hermética ni sin huecos solo por su render; las uniones de accesos y la continuidad transitable necesitan una comprobación posterior por recorrido.

Distribución de triángulos por materiales del OBJ separado (es agrupación de caras, no identificación funcional automática):

{table(['Material','Triángulos'],top)}

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

Casos, gravedad y consecuencias: `DATOS/hallazgos.csv`. Inventarios por objeto con área, vértices usados, materiales y cotas: `DATOS/componentes_*.csv`.
''')
write('04_MATERIALES_TEXTURAS.md',f'''
# Materiales, texturas, UV y diagnóstico del blanco

## Respuesta verificada por archivo

{table(['Familia/archivo','Imágenes','Estado real','Conclusión'],[['Colección GLB','0','8 materiales con factores constantes; no hay references de textura','El blanco está en el activo; no es una descarga fallida de imágenes'],['Colección BLEND','0 imágenes de archivo','8 materiales usados + Material sin uso; nodos Normal Map sin imagen de entrada','El original nativo tampoco aporta texturas ocultas'],['OBJ + VoyagerB.Mtl vigente','49 imágenes referenciadas por 50 mapas','Todas las rutas activas resuelven en ubicación original','Recuperable; conservar dependencias juntas'],['Voyager_Bridge_Trabajo.blend','49 imágenes de archivo','Rutas relativas válidas EN SU UBICACIÓN ORIGINAL; no empaquetadas','Transportar el BLEND solo rompería dependencias'],['Voyager_Bridge_Trabajo.glb','49 embebidas / 50 texturas','49/49 decodificadas; sin referencias externas','Referencia visual autocontenida útil'],['Voyager_Bridge_MAX_Trabajo.blend','49 declaradas + 2 visores internos','Rutas rotas en Recovery; 90 materiales de piezas MAX sin nodo de imagen','No confundir imágenes del OBJ heredado con materiales MAX texturizados']])}

La colección tiene `FrontColor` blanco por defecto ([1,1,1,1]), `cTerminal` negro, grises `Airway___Upper_Struts`, `Ground_Skirting___Lighting`, `Upper_Border___Lower_Recess`, rojo oscuro `Light_Detailing`, amarillo `Color_E01` y cian `Color_H04`. Todos declaran metallic=0, roughness=0,552786 y doubleSided=true. No hay COLOR_0, mapa normal, AO, rugosidad, metallic, emisión ni extensión unlit. Son materiales compatibles con el esquema metallic-roughness, pero **sin arte PBR de superficie**. La mayor parte del puente usa exclusivamente FrontColor. Los nombres «Lighting» no convierten esas caras en luz.

## Recuperación de la familia detallada

Las 49 imágenes embebidas del GLB detallado se leyeron desde sus bufferViews BIN y se decodificaron con Pillow. La lámina `CAPTURAS/texturas_embebidas_OBJ.png` muestra sus píxeles reales: LCARS, placa, metal, cuero y tejido. No se generó ni sustituyó ninguna textura. El color magenta observado en algunas superficies tampoco prueba un mapa perdido: existe, por ejemplo, el material constante `wire_138008110` con BaseColor≈(0,541; 0,031; 0,431), sin imagen. Los renders Cycles usan los shaders originales importados, sin reparación.

El GLB detallado tiene 102 materiales y solo mapas **BaseColor** (50 referencias, 49 imágenes). No hay mapas normal/roughness/metallic/AO ni emisión configurada. Incluye `KHR_materials_specular`; el detalle de factores está en `DATOS/materiales_gltf.csv`. Todas las 102 emisiones importadas tienen Strength=0. Por ello el interior cerrado, con luz diagnóstica exterior, aparece oscuro: una imagen LCARS legible no implica un panel luminoso. Se añadió una luz temporal interior exclusivamente para inspección y se guardaron ambas vistas. El ruido de 64 muestras no está suavizado ni ocultado con denoise.

El MTL vigente tiene 102 materiales, 50 mapas activos y **0 rutas activas rotas**. El MTL histórico tiene 58 mapas activos, **48 referencias que no resuelven**. El informe de reparación previo registra sustituciones nominales de pantallas; eso no certifica que sean exactamente el arte original de cada estación. No se aplicó ninguna reparación nueva. Tampoco se interpreta el MTL anterior como una versión de geometría.

En `Recovery/originales` hay 104 imágenes externas sanas, y en la carpeta del Escritorio 102. Las **206/206** se decodificaron. Hay candidatos locales por nombre normalizado para las 49 imágenes del BLEND Recovery; las diferencias de punto/guion bajo no se deben resolver a ciegas. El CSV de candidatos señala solo semejanza nominal, **no garantiza asignación semántica**. El MC6 y los mapas `VP_col`, `VP_bump`, `VP_Spec`, imágenes `_i`, etc., son fuentes de conciliación, no un material UE5 listo.

El BLEND Recovery contiene 171 materiales totales, pero 90 con caras asignadas a las mallas MAX; todos esos 90 carecen de nodos TEX_IMAGE. Otros materiales/nodos pertenecen al OBJ antiguo que comparte la escena. Las 49 rutas de archivo del BLEND fallan en la ubicación original de Recovery. No se confunden esos fallos con los que provoca copiar un BLEND sin dependencias: para `Voyager_Bridge_Trabajo.blend`, se resolvieron también las rutas contra la carpeta original y allí las 49 existen.

## UV y trabajo artístico real

- Colección GLB: **317/317 primitivas con UV0**; sin otro canal y sin colores de vértice. Todas las mallas importadas tienen coordenadas fuera del cuadrado 0–1: eso puede ser tiling válido, no demuestra UV rota. Hay 183 triángulos UV de área próxima a cero. La colección BLEND tiene 83/83 mallas con un canal UV; sus polígonos se triangulan de otra manera y dan 996 degeneraciones UV por ese método.
- OBJ separado: **630/630 mallas con UV0**. Permite conservar la colocación de las imágenes existentes. La versión fusionada y el GLB no aportan otro UV para lightmap. Raw GLB mide 11.919 UV degeneradas; la triangulación/precisión de Blender da 11.921. No hay certificado de atlas sin solapes o densidad de texel uniforme.
- Recovery: 591/632 mallas con UV; las 41 sin UV pertenecen al conjunto MAX. Ese conjunto tiene 590/631 con UV, y el OBJ heredado añade una más. Los objetos que no tengan UV y requieran imágenes nuevas necesitarán despliegue; para materiales constantes no es obligatorio.
- Los recuentos de triángulos UV repetidos son solo detección de coincidencia exacta; **no se ejecutó un solver exhaustivo de solapes ni una medición de estiramiento/texel density**. Es incorrecto decidir «rehacer todas las UV» o «todas listas» con esta evidencia.

## Clasificación de la evidencia

{table(['Estado solicitado','Resultado'],[['Existentes utilizables','49 imágenes embebidas y 206 externos físicos decodificados; no todos son diseños únicos'],['Presentes mal vinculadas','Imágenes declaradas por el BLEND de Recovery; sus materiales MAX además carecen de enlaces de imagen'],['Dañadas/incompatibles','Ninguna imagen probada falló; compatibilidad artística PBR y de importación no está certificada'],['Materiales que requieren reconstrucción','MAX: 90 materiales de piezas. OBJ/GLB: tratamiento PBR y emisión, no recuperación desde cero de toda textura'],['Superficies sin texturas con UV','Colección 317 primitivas; la existencia de UV no garantiza unwrap artístico aprovechable completo'],['Nuevo unwrap necesario','41 mallas MAX sin UV si se decide texturizarlas; zonas UV degeneradas que deban recibir mapas nuevos']])}

La causa de ver **todo** blanco en un visor particular podría además ser su modo Solid/material override; ese visor no se inspeccionó en vivo. Sí se ha probado que el archivo de colección ya carece de imágenes y que el puente detallado texturizado renderiza con sus mapas en Blender. No se atribuye el problema a Blender ni al importador de Unreal sin una prueba que lo demuestre.

Referencia para defaults de factores y atributos: [especificación glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html). Valores y enlaces concretos: JSON locales y CSV de esta auditoría.
''')
write('05_INTERACTIVIDAD.md',f'''
# Interacción potencial: evaluación, sin implementación

## Puertas y accesos

En el **OBJ original separado** hay geometría de puertas y paneles en grupos propios. La importación devuelve 630 objetos sin parentesco funcional y todos con el origen en cero. Deben identificarse las piezas que forman cada hoja, separar el marco fijo, establecer ejes/pivotes y medir volumen de retirada. Los controles pequeños `Doorpanel_*` no son las hojas. No se ejecutó animación, no hay un mecanismo de puertas entregado en esta auditoría y no se certifica que cada vano admita dos hojas correderas sin intervenir.

En **Recovery MAX** existen grupos `door3`, `door4`, `door04`–`door07` y piezas como `door01`, `Mesh1310`–`Mesh1321`, además de otras. La jerarquía ayuda a localizar piezas, pero su ensamblaje y escala tienen incidencias; no se recomienda copiar una animación de Sutherland sin medir cada caso. En la **colección**, las puertas/recesos se integran mayoritariamente en una malla por módulo (en GLB se separan por material, no por hoja). Un marco independiente sí existe como módulo; eso no implica hojas animables separadas.

Grado: **B/C** en geometría detallada, **C** en puertas fusionadas de colección, funcionamiento **E**. Primera comprobación futura: vano real, suelo/umbral, normal del plano, longitud de cada hoja, profundidad de bolsillo y colisión continua en ida/vuelta. La cabina representada no equivale a un turbolift que transporte personajes.

## Sillas y puestos humanos

El puente detallado contiene dos sillones centrales y tres asientos de estaciones reconocibles en las vistas. El OBJ permite recuperar piezas como `Box_6`–`Box_9`, `Armrest_5`–`Armrest_8`, `Layer__3`–`Layer__5` y componentes ChamferBox/MSB/Object. Los apoyabrazos y respaldos son geometría; el cuero es textura/material. No hay esqueleto, posición de sentarse, espacio de piernas certificado ni animación de ocupante.

Todos los orígenes cero impiden usar directamente las rotaciones locales como giros de asiento. La conversión MAX conserva algo de jerarquía de tres estaciones (`Group009`, `Group008`, `Group003`), pero también transformaciones no uniformes. Debe comprobarse la relación asiento–suelo/plataforma, orientación de rodillas, alcance de consola y paso detrás del respaldo con un personaje real. No reducir la cápsula para que parezca transitable. La colección no incluye sillas reconocibles en su subárbol del puente; habría que incorporarlas desde otra fuente o crearlas.

Grado: **B/C** para piezas del OBJ; **D** para sillas ausentes de la colección; ergonomía **E**.

## Consolas y pantalla principal

Hay carcasas, superficies de pantalla y remates recuperables como objetos OBJ. El GLB fusionado conserva materiales/primitivas pero necesitaría recuperar esa separación desde el original para editar por estación. Las imágenes LCARS prueban contenido visual estático; etiquetas Science, Security, Operations, etc., no prueban una función implementada ni la correspondencia canónica de cada ubicación.

La pantalla principal es una superficie representada, actualmente sin imagen operativa de vistas de nave. Los controles mostrados en LCARS están pintados, no modelados como botones. Para una vista ampliada harían falta superficies/rangos UV bien identificados, zona de activación, cámara/entrada/salida de interacción y contenido dinámico. Si la consola conserva marco y tablero juntos, podría mantenerse agrupada como estática y separar solo la salida de pantalla. No se creó ningún Widget, Render Target ni código.

Grado: **B** como formas editables, **C** para arte y comportamiento final.

## Circulación y NPC

Los rayos de pasillos rectos dan una sección holgada a escala interpretada, pero son mediciones sin radio. No certifican curvas, umbrales, escalones o el recorrido completo del puente. En la conversión MAX está probado un problema real de superficie de suelo; una colisión invisible que lo tape no restauraría el render ni justificaría elegir esa fuente.

Para el puente OBJ no se certifica todavía una ruta acceso→consola→silla→salida. Hacen falta suelo continuo, escalones adecuados, espacio de giro, cápsula del proyecto, barridos de altura y radio y verificación en CharacterMovement. Para NPC habría que definir puntos de aproximación, postura sentada, ocupación de estación, espera ante puerta y navegación/solicitud de apertura; nada de ello está incluido en el modelo.

## Lecciones de Sutherland con evidencia local

{table(['Documento leído','Evidencia documentada','Aplicación conceptual en Voyager'],[[link(ST/'F07_P03FG_DoorLab/Reports/INFORME_FINAL_F07_P03G.md'),'Cuatro puertas, ocho hojas; recorridos, alojamientos físicos, pruebas Chaos y ruta D04 a cabina; otros destinos bloqueados','Reutilizar enfoque de raíz local, permisos/intención, ocupación de umbral y pruebas por puerta; recalcular medidas y bolsillos'],[link(ST/'F07_Chair_AutoLab/Reports/INFORME_FINAL_F07_CHAIR_01.md'),'Seis sillas, 15 piezas móviles + base; avance 30 cm y pruebas de ida/vuelta','Separar base y partes móviles; no copiar 30 cm ni número de piezas al diseño Voyager'],[link(ST/'F07_COLL_01_Lab/Reports/INFORME_FINAL_F07_COLL_01.md'),'330 piezas fijas; colisión simple ajustada, revisión de falsos bloqueos; postura sentada todavía pendiente','Medir pasos con cápsula; las líneas no garantizan paso. Movimiento de silla correcto no certifica que un humano se siente'],[link(PBRPATH),'Especificación de canales/espacios de color y laboratorio PBR procedural; no certifica conversión visual completa de Sutherland','Conservar albedo, definir PBR y emisión selectivamente; verificar materiales del recurso concreto']])}

Estos son **resultados comunicados por informes locales leídos**, no pruebas repetidas ahora ni garantías transferibles. Las medidas Sutherland, sus recorridos de 86,8 cm, el avance de silla de 30 cm, sus convexos y las rutas Recast **no se adoptan como medidas Voyager**. La carpeta `Sutherland_PBR_Lab` consultada solo aportó texturas; el BLEND PBR existente en la biblioteca fue inventariado, no abierto ni validado artísticamente en esta misión. No se cambió ningún recurso Sutherland.
''')
module_rows=[]
om={o['name']:o for o in coll['objects']};mm={m['name']:m for m in coll['meshes']}
for o in coll['objects']:
 if o['type']=='MESH' and o['parent'] and not o['parent'].startswith('Group_'):
  module_rows.append([o['parent'],o['name'],mm[o['data']]['triangles'],' × '.join(f'{x:.3f}' for x in o['bounds']['size'])])
write('06_MODULOS_ADICIONALES.md',f'''
# Arquitectura modular y recursos adicionales

La colección es una biblioteca desplegada en el espacio. El nativo BLEND agrupa cada módulo principalmente en una malla con varios materiales; la exportación GLB la divide por material. **317 mallas GLB no significan 317 módulos**: el nativo tiene 83 mallas, ocho de ellas en el grupo del puente. No se contó un `Recessed_*` como una habitación terminada solo por su nombre.

## Familias identificadas

- Rectos `Hallway_Strait_Small1`, `Hallway_Medium_Single1`, `Hallway_Strait_large1`: suelo, paredes/perfiles y techo representados.
- Curvas 90°, cruces T y cuatro vías, variantes circulares de diferentes radios y tramos con una/dos puertas.
- Accesos residenciales simétricos/asimétricos, nichos/control areas, puertas grandes/cargo y marcos laterales independientes.
- `Turbolift1`, accesos cortos/largos de turbolift, accesos Jefferies; la cabina es geometría estática.
- `J_Tube_*`: rectos corto/medio/largo, codo, T, inclinados, hatch y cruces verticales. Son conductos, no pasillos de pie.
- Mantenimiento horizontal/vertical, codos y cruces con diferencias de cota.
- `ConferenceRoom`, `Room___Head___Single_Restroom1`, bloques Group1–Group10 y volúmenes `Hallway_Primary_Secondary_Location_*`: existen formas de estancias/envolventes; mobiliario y calidad interior no se certifican por su etiqueta.

## Compatibilidad medida, no ensamblaje supuesto

Los tres rectos comparten anchura exterior aproximada **3,693 m**, altura exterior **3,114 m** y longitudes **1,316 / 2,195 / 4,389 m**. Un BVH de sus superficies arroja en el centro y a 10/50/90 % de longitud:

{table(['Altura de muestra Z mundo','Anchura entre primeras superficies laterales'],[['0,10 m','3,5344 m'],['0,90 m','3,3168 m'],['1,70 m','3,3271 m'],['2,20 m','3,1808 m']])}

El suelo central está en Z≈−0,019549 m y el techo interior en Z≈2,796803 m: altura central aproximada **2,81635 m**. Las muestras coinciden en los tres tramos. Esto apoya su uso conjunto y el carácter humano de la escala interpretada; no demuestra igualdad de todas las juntas/vértices ni paso de cápsula en recodos. No se montaron módulos ni se corrigieron sus posiciones.

`J_Tube_Long1` mide aproximadamente **1,175 × 1,829 × 0,914 m**; una sección horizontal a Z=0,9 m da ~1,002 m entre superficies laterales. Esa altura no permite paso normal de pie. El rayo vertical iniciado a Z=1,7 m cae sobre la cara exterior superior del tubo; se registra como tal, **no como suelo interior**.

Los módulos están separados en XY y algunos en Z; sus pivotes conservan el sistema de catálogo, sin sockets verificados. Longitudes no homogéneas con un grid de 1 m. No hay UV/material de continuidad garantizados, colisiones, navegación, luces ni puertas activas. Los marcos/recesos y conductos pueden reutilizarse, pero conectar el puente detallado con ellos exigirá un módulo adaptador y comparar vanos, cota de suelo y normal de conexión: ambos recursos proceden de familias distintas y no se demostró encaje directo.

## Inventario de módulos por nombre fuente

Dimensiones son envolventes mundo de objeto; no son anchos útiles ni aforo. La tabla incluye bloques secundarios no interpretados exhaustivamente.

{table(['Grupo fuente','Malla','Triángulos','Dimensiones m'],module_rows)}

Datos completos, también puente y grupos anónimos: `DATOS/componentes_blend.csv`. Rayos, hits/normales y longitudes: `DATOS/deep_blend.json`. Grado global **B** como kit geométrico; acabado final, interacción y ensamblaje todavía pendientes.
''')
write('07_COMPARATIVA_VERSIONES.md',f'''
# Comparación y selección de base

No hay una única línea de versiones por tamaño. Son dos familias de autoría/procedencia distinta y varios derivados de la familia detallada.

{table(['Variante','Integridad/organización','Arte/UV','Selección'],[['Colección .blend nativo','83 mallas / 189 objetos; módulos con materiales, puente simple de 8 mallas','Sin imágenes; UV0 general con tiling/degeneraciones','Base del kit de pasillos, no del puente protagonista'],['Colección GLB','317 mallas divididas por material; 67.563 triángulos crudos','8 materiales constantes, 0 imágenes','Referencia portable del kit; no es una versión texturizada'],['ZIP colección','Un único BLEND, hash igual al extraído','Exactamente la misma fuente','Respaldo, no nueva versión'],['OBJ + MTL vigente','630 grupos recuperables; 271.705 triángulos tras validar; suelo frontal íntegro en comparación','102 materiales, 49 imágenes activas; UV0 en todos los grupos','BASE PRINCIPAL de recuperación propuesta'],['BLEND de trabajo OBJ','1 objeto fusionado, 271.705 triángulos','49 imágenes externas con rutas originales correctas','Referencia editable limitada por fusión; conserva arte'],['GLB de trabajo OBJ','1 nodo / 1 malla / 102 primitivas','49 imágenes embebidas sanas; albedo sin PBR completo','Referencia visual autocontenida y respaldo de arte'],['BLEND MAX de trabajo','631 mallas MAX + 1 OBJ heredado; escalas diferentes, suelo dañado, dos piezas alejadas','90 materiales MAX usados sin imagen; 41 mallas MAX sin UV','Fuente secundaria; no elegirla por número de objetos'],['MAX 2011 original','Inventariado / 19.895.548 bytes; no abierto con 3ds Max','MC6 y texturas asociados disponibles','Conservar para futura comprobación; E en equivalencia completa']])}

## Evidencia decisiva

- La prueba temporal de separación OBJ **ya se ejecutó**: 630 objetos, sin guardarlos como modelo derivado. Por tanto no es una promesa basada solo en el nombre del archivo.
- `floorfront_1` del OBJ tiene 613 caras triangulares y **32,829204 m²**. En MAX convertido `floorfront` conserva **0,000133254 m²** con 593 vértices sueltos. La mayor dimensión de su bounding box no representa un suelo mejor.
- La separación del OBJ no conserva pivotes originales: todos quedan en cero. Aun así conserva mejor equilibrio de superficies, UV, texturas y editabilidad que iniciar desde el GLB fusionado o la conversión MAX defectuosa.
- El archivo MAX de trabajo del Escritorio y el de Recovery tienen hash idéntico: no son dos recuperaciones distintas.
- El GLB detallado tiene la misma envolvente y triangulación que el BLEND fusionado, con más vértices por atributos. No se ejecutó equivalencia completa de normales/UV cara por cara; coincidencia de conteos no es prueba suficiente de identidad completa.
- El OBJ y el MAX convertido no se pueden mezclar por coordenadas: la pieza de techo contrastada muestra escala relativa ~1,5081 y desplazamientos. No se ha decidido cuál es la escala canónica de rodaje.

## Recomendación concreta

Conservar juntos **OBJ original, MTL vigente, MTL anterior, 102 imágenes del Escritorio, GLB texturizado y MAX/MC6/BLEND originales**. Para una futura copia de trabajo empezar con la importación separada del OBJ, manteniendo el GLB como patrón de aspecto. Conservar el nativo BLEND de la colección para módulos, con su ZIP idéntico como respaldo. No se copiaron materiales entre familias ni se eligió el modelo de más bytes/polígonos.

Comparación visual: `CAPTURAS/comparativa_puentes.png`, vistas completas y cortes por versión en el índice. Las vistas de corte eliminan solo caras altas en sesiones temporales; no deben usarse para inferir ausencia de techo en el archivo original.
''')
write('08_PLAN_FUTURO.md',f'''
# Plan futuro propuesto — no ejecutado

## Viabilidad y alcance real

**Viable como recuperación de complejidad media/alta**, especialmente por disponer de OBJ separado y texturas sanas. La carga de ~272.000 triángulos no es por sí sola un bloqueo demostrado. El coste práctico dependerá de materiales, cantidad de componentes/secciones, transparencias/doble cara, sombras y colisiones; no se ofrecen FPS, draw calls reales ni memoria UE5 medida. Un solo objeto con 102 materiales tampoco equivale a una sola llamada de dibujo.

## Orden recomendado para una futura fase autorizada

1. **Copia trazable del OBJ con MTL y dependencias.** Separar sus 630 grupos en una escena nueva, clasificar por arquitectura, mobiliario, pantallas y mecanismos; preservar UV0/normales. Esta auditoría hizo esa separación solo en memoria para inspección y no entregó un máster restaurado.
2. **Escala y suelo primero.** Probar un maniquí/cápsula del proyecto y medir vanos completos, altura de asiento respecto a su plataforma, escalones y suelos. Contrastar escala OBJ/MAX sin normalizar a ciegas. Revisar coincidencias y normales por componente antes de cualquier limpieza global.
3. **Un recorrido piloto.** Acceso→una estación→retorno, con suelo y límites visibles. Mantener bloqueados destinos sin construir, siguiendo el criterio documentado en Sutherland. El kit modular puede aportar un tramo, pero necesita adaptador de cota/sección al puente.
4. **Organización de Static Meshes.** Mantener por separado suelos por nivel, tramos de muros/techo, carcasas de consolas y barandillas coherentes. Puertas/hojas, marcos, base/silla móvil y superficies de pantalla deben ser independientes. Agrupar remates pequeños estáticos por sector/material solo tras perfilar; no exportar cada tornillo como actor por defecto.
5. **Materiales.** Conservar imágenes BaseColor existentes y reconstruir respuesta PBR por familia. Emisión selectiva para LCARS y luminarias, sin convertir toda arquitectura a unlit. Revisar sRGB/color, mapas lineales y normales; añadir mapas nuevos solo cuando esa fase artística se autorice. Tratar cuero, metal y alfombra según referencias artísticas, no aplicar una rugosidad uniforme a todo.
6. **Colisión.** Primitivas/convexos específicos para suelos, escalones, mamparos con huecos, consolas y bases de sillas. Una caja que cubra un vano sería incorrecta. Las hojas móviles precisan barrido y retorno; probar cápsula completa, no solo rayos. La receta debe comprobarse con render y Chaos, como mostró la discrepancia de convexos en Sutherland.
7. **Interacción/NPC.** Primero una puerta y una consola; después agrupación de silla, postura y ocupación. Reutilizar conceptos de intención, permiso, espera y umbral del laboratorio Sutherland, con medidas propias. NavMesh o SmartLinks y permisos de puerta requieren implementación/pruebas, no están en el activo.
8. **Validación UE5 5.8.2 aislada.** Revisar importación/escala/materiales/normales/tangentes, espacios de paso, iluminación, frame time y memoria en MSI. Registrar versión exacta y opciones. Solo después ampliar al resto del puente e integrar; esta misión no abrió el proyecto ni hizo ese ensayo.

## Iluminación con Lumen

Recomendación teórica basada en [Lumen Technical Details, documentación UE 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine): separar paredes, suelos y techo en piezas razonables para cobertura de Surface Cache. Las mallas cóncavas que contienen una habitación y mobiliario completos no son una organización apropiada para esa cobertura. Comprobar superficies delgadas y caras posteriores; el material double-sided no demuestra un cerramiento volumétrico correcto. Para la ruta de software por campos de distancia, Epic recomienda paredes de al menos 10 cm para reducir fugas; no es una medida certificada de estas paredes ni una garantía universal. No se añadieron espesores.

El uso de Lumen no obliga a fabricar un UV de lightmap únicamente para iluminación dinámica. Si se opta por iluminación horneada, preparar canal independiente sin solapes. UV0 existente para LCARS debe preservarse. No se probó Surface Cache, hardware RT, campos de distancia ni exposición del proyecto.

## Facilidad de los trabajos

{table(['Tipo','Trabajo previsto','Por qué'],[['Ajustes limitados','Recuperar grupos OBJ, nombres/colecciones, pivotes, selección de pantallas','Fuente y superficies ya existen; el agrupado funcional requiere atención'],['Intervención artística','PBR, emisión, limpieza localizada de solapes/normales, UV afectadas, detalle de consola','Texturas existentes no equivalen a acabado final; defectos medidos'],['Reconstrucción/recuperación desde otra fuente','Suelo perdido en conversión MAX; mobiliario ausente del puente de colección; adaptador a pasillos','No compensa rehacer una conversión dañada cuando el OBJ conserva superficie'],['Evaluación todavía necesaria','Van os completos, sentado/NPC, colisiones, rendimiento, fidelidad canónica','No se ejecutó el laboratorio dinámico ni comparación con planos canónicos']])}

No se instala software ni se usa MAX como bloqueo de toda la investigación: se conserva su estado E y se avanza con OBJ/GLB ya comprobados. Para colisiones exportadas, nombres y restricciones se consultarían en [FBX Static Mesh Pipeline de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine). El soporte general de GLB se describe en [glTF Support de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/gltf-file-format-support-in-unreal-engine); soportar el formato no garantiza material idéntico ni colisión gameplay.

## Matriz de aprovechamiento

{table(['Componente','Grado','Evidencia/condición'],grade_rows)}

La estimación no se convierte en un calendario de horas sin definir calidad visual, alcance de interactividad y plataforma objetivo. **Auditoría finalizada; toda actuación descrita aquí es una propuesta para otra fase.**
'''.replace('Van os','Vanos'))
sources=[
 REC/'informes/auditoria_voyager.md',REC/'informes/auditoria_voyager.json',OBJ/'VoyagerB_Informe_reparacion.txt',
 ST/'F07_P03FG_DoorLab/Reports/INFORME_FINAL_F07_P03F.md',ST/'F07_P03FG_DoorLab/Reports/INFORME_FINAL_F07_P03G.md',ST/'F07_Chair_AutoLab/Reports/INFORME_FINAL_F07_CHAIR_01.md',ST/'F07_COLL_01_Lab/Reports/INFORME_FINAL_F07_COLL_01.md',
 Path(r'C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\docs\roadmap\master\fases\F02\AUDITORIA_GLB_USS_SUTHERLAND_2026-10-12.md'),Path(r'C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\docs\roadmap\master\fases\F07\P02_PIPELINE_PBR_BLINDAJE.md'),Path(r'C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\docs\roadmap\master\fases\F07\P04_PLAN_PRUEBA_UE5.md')]
docmanifest=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'read as documentation, results not rerun'} for p in sources if p.exists()]
(D/'fuentes_documentales.json').write_text(json.dumps(docmanifest,indent=2,ensure_ascii=False),encoding='utf8')
write('09_METODO_FUENTES_LIMITACIONES.md',f'''
# Método, pruebas, fuentes y límites

## Herramientas verificadas

- Windows/PowerShell para listados, copias e invocación; Python **{platform.python_version()}** y biblioteca estándar para hashes, cabeceras/BIN/JSON, OBJ, MTL y ZIP; Pillow **12.2.0** para decodificar imágenes y componer láminas de sus píxeles existentes.
- **Blender 5.2.2 LTS**, build d13f752e3b9c, instalado en `C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe`. Background, factory-startup, disable-autoexec. BLEND abierto con `use_scripts=False, load_ui=False`. No se controló ni cerró una sesión Blender del usuario.
- Importador glTF integrado y OBJ integrado (split objects/groups, validate meshes). Workbench con color de material para geometría; Cycles CPU a 64 muestras sin denoise para shaders/texturas originales del GLB detallado.
- No se instaló ninguna dependencia. No se ejecutó Unreal ni se abrieron `.uproject`, mapas o assets del motor. Solo se leyeron informes locales y listados de carpetas relacionadas. No se ejecutaron scripts anteriores del proyecto.

## Procedimiento

Inventario acotado de biblioteca y rutas derivadas de metadatos. Modelos pequeños (4–38 MB) inspeccionados antes de cargar. Copias de los BLEND/GLB bajo `TEMP/`; OBJ original leído en una sesión vacía temporal, sin guardado ni exportación. Cálculo de matrices, bbox, usuarios, materiales/nodos, UV, áreas y conectividad. Accesores de ambos GLB decodificados directamente y comparados con recuentos Blender. Validación de índices y decodificación de imágenes; no se llama «validación Khronos completa» a este inspector propio.

Soldaduras de diagnóstico sobre bmesh desechables y cortes sobre mallas temporales en memoria. Los originales no se guardaron; las capturas no son modelos restaurados. No se utilizó ImageGen ni imagen sintética de IA. Las láminas son montajes de capturas o texturas reales. Workbench no muestra imágenes: se acompaña de renders Cycles reales y del contacto de imágenes embebidas para evitar confusión.

La primera preparación Workbench falló porque el GLB no tenía World; se creó uno temporal y se repitió correctamente. No se necesitó cancelar pruebas por memoria o inestabilidad. El render interior cerrado es oscuro porque las lámparas exteriores no resuelven la ausencia de emisión: se conserva como diagnóstico y se añade una vista con una luz interior temporal de inspección. La iluminación de capturas no es la iluminación original ni una propuesta artística final.

## Fuentes documentales leídas

{chr(10).join('- '+link(p) for p in sources)}

Los informes de Sutherland más recientes documentan laboratorios ejecutados; las especificaciones del repositorio de fechas anteriores aún decían «pendiente». Se distingue la fecha/fuente: no se desechan los informes posteriores ni se afirma haber repetido sus ensayos. El informe Voyager del 09/10 se usó como guía; los recuentos/modelos de esta entrega proceden de nueva inspección. En particular se corrige su resumen de Mesh1497 con 14 caras verificadas ahora.

## Referencias técnicas primarias consultadas el 21/10/2026

- [Especificación glTF 2.0: unidades, atributos, materiales y GLB](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html).
- [Epic: Lumen Technical Details, documentación 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine).
- [Epic: FBX Static Mesh Pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).
- [Epic: glTF Support](https://dev.epicgames.com/documentation/en-us/unreal-engine/gltf-file-format-support-in-unreal-engine).

## Alcance de la evidencia

**Verificado:** cantidades y estructura enumeradas, píxeles decodificados, rutas originales resueltas, áreas/cotas y muestras BVH, recuperación temporal de 630 grupos OBJ, defectos de suelo citados y diferencias de escala de piezas contrastadas.

**Estimado/inferido:** conveniencia de base principal, grado A–E, coste artístico relativo, potencial modular, tamaño humano probable y riesgos teóricos UE5. No se certifica fidelidad canónica con planos/fotogramas externos.

**No evaluado:** MAX binario en 3ds Max (no se abrió ni instaló lector), render mental ray/Poser original, equivalencia cara por cara MAX↔OBJ, todos los empalmes modulares, atlas UV/estiramiento exhaustivos, intersecciones arbitrarias, cápsula/NPC/ergonomía, recorrido físico UE5, Lumen, rendimiento, empaquetado e integración.

Las cotas de objeto incluyen a veces vértices sueltos; `deep_*.json` separa bbox de superficie efectivamente referenciada y área. Los umbrales de área son pruebas numéricas, no una medida universal de defecto visible. Normal opuesta a winding no identifica automáticamente «cara invertida» respecto al interior del puente. Coincidencia triangular cuantizada no clasifica intención de capas. Los rayos no tienen radio y no sustituyen colisiones de cápsula.

## Reproducción y preservación

Scripts en `SCRIPTS/`: `inventory.py`, `blender_inspect.py`, `raw_gltf.py`, `deep_geometry.py`, `material_audit.py`, `render_diagnostics.py`, `render_textured.py`, `create_reports.py`. Las rutas fuente están declaradas en ellos. No ejecutar sobre otra ubicación sin revisar las rutas de salida; se escriben exclusivamente en esta carpeta de auditoría. Los logs guardan importaciones/avisos.

`DATOS/inventario_archivos.json` es la línea base de 230 archivos de modelos y dependencias localizados con SHA-256, bytes y mtime_ns; `DATOS/integridad_final.json` registra la relectura final. El manifiesto documental tiene hashes de referencia, no un snapshot anterior a toda lectura. No se afirma haber rehasheado todos los proyectos/archivos del ordenador. No se realizaron operaciones Git ni cambios de código o ramas/commits/PR.
''')
print('REPORTS_WRITTEN',len(list(R.glob('*.md'))))
