"""Nine final technical reports, generated from measured evidence and explicit limitations."""
import json,csv,collections,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'DATOS'
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def table(headers,rows):return '\n'+'| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows)+'\n'
def save(n,body):
 intro='\n**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**\n\n[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)\n\n'
 (R/n).write_text(body.split('\n',1)[0]+intro+body.split('\n',1)[1],encoding='utf8')
proto=read('prototipo_conjunto.json');erg=read('ergonomia_detallada.json');seated=read('puestos_revision.json');access=read('acceso_central_revision.json');doors=read('puertas_medidas.json');motion=read('carreras_investigacion.json');cases=read('ensamblajes_pruebas.json');contrast=read('contraste_blend.json');materials=read('materiales_rendimiento_revision.json');room=read('accesibilidad_camarote.json');enc=read('encuentros_adaptadores.json')
maxerror=max(x['max_coordinate_or_surface_error_m'] or 0 for x in contrast['objects']);budget=materials['texture_hypotheses']
grades=[('Puente detallado como base de trabajo','C','Recuperable; escala y restauración local, circulación integral sin demostrar.'),('Escala global 1,10','B / confianza media','Hipótesis arquitectónica provisional; no canon ni escala definitiva de todos los muebles.'),('Uniones de pasillos seleccionadas','B / C','Cápsulas y soporte pasan; perfiles discrepan, no hay uniones A.'),('Conexión posterior y red','C','Dos rutas geométricas parciales, adaptadores de diagnóstico y puertas abiertas estáticas.'),('Acceso desde centro/navegación','E','No aparece conexión en la búsqueda refinada; requiere estudio de escalones y obstáculos.'),('Mesh4 como base espacial de camarote','C','Habitable como maqueta; no dormitorio artístico/funcional final.'),('Puertas como mecanismos','C / funcionamiento E','Contactos investigados; bolsillos, barrido continuo y lógica no certificados.'),('Sillas y postura','C / ocupación E','Grupos corregidos y proxies; sin rig ni sentarse/levantarse validados.'),('57 superficies planas independientes','A solo separabilidad','No acredita materiales emisivos, alcance, UI ni interacción.'),('PBR, iluminación y rendimiento UE','C / rendimiento E','Canales y presupuestos estudiados; sin perfil real.'),('Accesibilidad física continua','E','Giros locales no resuelven cambios de nivel ni rutas continuas.')]
save('00_RESUMEN_EJECUTIVO.md',f'''# VOY-02 — Resumen ejecutivo
La evaluación técnica se entrega cerrada con resultados positivos y negativos explícitos. Los recursos permiten plantear **un puente detallado, una red pequeña de pasillos, cabina y un camarote**, con adaptación importante. El prototipo no acredita todavía un puente enteramente transitable ni sistemas funcionales terminados. La prioridad siguiente es resolver circulación y puestos, antes del acabado artístico o la integración.

## Recuperación y conservación
Se leyeron íntegramente el prompt adjunto y los tres documentos de continuidad. El laboratorio real es `{R}`. La comprobación previa confirmó 207/207 archivos iguales al inventario de parada, 115/115 entradas originales intactas, 106/106 copias concordantes y 59 archivos JSON/NPZ/PNG legibles. Las 33 capturas existían. No había procesos de laboratorio pendientes. Las rutas de fuentes y el entorno Blender/Unreal están accesibles; el nuevo chat trabaja sobre el mismo laboratorio. No se repitió `00_preparar.py`, ni se sustituyó el baseline.

La inspección reveló una incidencia que el traspaso dejaba abierta: **el `.blend` había perdido la base de importación del OBJ (+90° X)** al clonar sus objetos. Las superficies ensayadas numéricamente eran correctas, pero su representación guardada no lo era. Se repararon 630 datablocks compartidos exclusivamente en el laboratorio, con respaldo SHA-256 verificable. El contraste final de G abarca 645 componentes —630 OBJ, seis módulos, seis adaptadores y tres volúmenes de mobiliario— frente al NPZ. Error máximo {maxerror*1e6:.3f} µm, tolerancia explícita 20 µm para aritmética float32. Hay ocho escenas útiles y 49 imágenes empaquetadas. La comprobación no guarda cambios.

## Resultados que condicionan el proyecto
{table(['Área','Grado / confianza','Resultado'],grades)}
Las siete pruebas modulares mantienen sus resultados de cápsula y soporte para H=1,60/1,75/1,90 m y r=0,35 m. Las dos rutas del conjunto desde la pasarela posterior suman 948 y 1110 poses **por altura y por recorrido**, respectivamente. Tras corregir el adaptador se repitieron esas seis pruebas y su soporte. No son CharacterMovement ni NavMesh.

La rejilla nueva de 10 cm no conecta centro/navegación con la pasarela posterior, tanto para H=1,60 como 1,90 m. No se interpreta como prueba de imposibilidad absoluta. La alternativa nueva que la rejilla propone para la pasarela roza un soporte al refinar el margen; no reemplaza el recorrido previo que sí pasó.

Las puertas laterales cruzan superficies de cerramiento en fracciones intermedias. La posterior mantiene contactos de borde/tangencia, sin bolsillo probado. Se ensayaron desplazamientos normales y elevaciones pequeños: ninguno dejó todas sus poses libres de contactos. Además, el adaptador original cruzaba las hojas posteriores abiertas; se retranquearon **0,14 m** sus paredes/techo, manteniendo el suelo. La revisión elimina esos cruces transversales en la pose abierta, sin certificar el mecanismo.

## Qué se entrega y qué se conserva
Nueve informes, índice, galería, 33 capturas revisadas, cuatro láminas analíticas, hojas de contacto, tablas CSV/JSON, scripts y logs; ZIP local en `PAQUETE/VOY02_ENTREGA.zip`. El `.blend` y los NPZ geométricos permanecen fuera del ZIP; sus rutas figuran en el índice. El archivo principal es `ESCENAS/VOY02_Laboratorio.blend`.

Se preservan resultados antiguos, incluido el estado anterior a la corrección del OBJ, las capturas originales y los datos anteriores al retranqueo. Las revisiones y descartes se explican en el informe 08. No se modificaron modelos originales, Sutherland, parámetros del personaje o proyectos UE. No hubo instalación, integración, publicación, commit, fusión ni cambios en main.

## Siguiente decisión
Conservar 1,10 como referencia experimental mientras se resuelven escalones/accesos y se ajustan los puestos localmente. A continuación, prototipar una puerta completa con alojamiento físico, una estación sentada y una conexión terminada. Las decisiones artísticas corresponden al usuario; la hoja de ruta separa tareas Blender, pruebas UE futuras y sistemas del videojuego. El cierre de este laboratorio no inicia esas fases.
''')
zone_rows=[]
for z in erg['zones']:
 zone_rows.append([z['zone'],f"{z['floor']['point'][2]:.3f}" if z.get('floor') else 'sin suelo',f"{z['overhead_clearance_m']:.3f}" if z.get('overhead_clearance_m') else 'sin hit',', '.join(str(p['height']) for p in z.get('standing',[]) if p['clear']) or 'ninguna'])
seat_rows=[[s['id'],' / '.join(s['seat_object']),f"{s['seat_height_above_floor_m']:.3f}",f"{sum(a['result']['clear'] for a in s['approach_tests'])}/{len(s['approach_tests'])}"] for s in erg['seats']]
save('01_ESCALAS_ERGONOMIA.md',f'''# VOY-02 — Escalas, ergonomía y accesibilidad
## Escala recomendada y confianza
El OBJ no proporciona una unidad física autoritativa. Se compararon factores 1,00 / 1,10 / 1,15 / 1,20 / 1,25 / 1,30 / 1,50813535 utilizando hojas completas y cápsulas reales. H=1,90 m falla en las tres puertas a 1,00 y pasa los tramos locales a 1,10 y superiores probados. H=1,60 y 1,75 pasan a 1,00. Por ello, **1,10 es el mínimo factor de la serie probada que satisface los tres vanos para 1,90 m**, con confianza arquitectónica media y confianza baja como escala global definitiva. No se ha buscado el mínimo continuo entre 1,00 y 1,10.

La envolvente pasa de 13,150 × 13,011 × 3,840 a aproximadamente 14,465 × 14,312 × 4,224 m. La derecha tiene altura central de 1,775576 unidades OBJ: a 1,10 son ~1,953 m, apenas 53 mm sobre 1,90 m antes de otros márgenes. Sus anchuras medidas rondan 0,832 m a 1,10; en izquierda/posterior, ~0,922 m a las alturas muestreadas. No se convierten rayos centrales en rectángulos totalmente libres.

La similitud MAX ≈ OBJ ×1,50813535 + (−0,11236;1,875563;−0,466607) coincide en nueve parejas arquitectónicas independientes, con máximo ≤8,80 µm. No prueba un origen de unidades ni equivalencia de todas las piezas. `strudextends` presenta RMS ~0,443 m y máximo ~1,018 m; muebles y sillas requieren correspondencia individual. No se adopta 1,508 como escala humana.

## Suelos, techo y poses de pie
{table(['Zona (coordenadas en DATOS)','Suelo Z m','Primera superficie desde suelo+1,80 m: altura relativa m','H de pie que pasan en el punto'],zone_rows)}
Se identifican tanto la primera superficie sobre el suelo como el impacto al iniciar un rayo a +1,80 m. Este último puede ser una viga o remate: **no es automáticamente el techo arquitectónico**. Las sondas laterales elegidas chocan con geometría local a las cuatro alturas. Las zonas central, navegación y posterior seleccionadas admiten las poses; una pose correcta no demuestra una ruta entre ellas. El ensayo añade 1,80 m como referencia histórica de Sutherland, sin cambiar personaje alguno.

Los niveles fuente principales son ~0,021205 / 0,297639 / 0,435856 / 0,712296. A escala 1,10, algunas secciones laterales muestran un salto directo de **~0,305 m** entre soporte central y superior, y otra separación de ~0,456 m desde el nivel frontal. En el eje aparecen huellas fragmentadas y ausencia de soporte en puntos concretos. Los rayos horizontales elegidos no describen todas las escaleras; no se aprueba una subida por deducirla del desnivel. Se conservan todas las muestras a 1 cm en `secciones_niveles.csv` y `ergonomia_detallada.json`.

## Asientos y puestos
{table(['Puesto','Superficie medida','Altura sobre soporte m','Poses de aproximación H=1,90 libres / muestreadas'],seat_rows)}
La revisión semántica distingue cojín de carcasa: los centrales se miden sobre ChamferBox_27–29 y 34–36, no Box_6/8. La estimación preliminar ~0,642 m correspondía al borde de carcasa y se conserva como resultado sustituido. El asiento central real da ~0,494 m. Las superficies laterales dan ~0,599 m. Navegación da ~0,630 m respecto al rayo de soporte de Object_75; el suelo de los pies vecinos está ~23 mm más alto. Son cotas de superficies muestreadas, no altura cargada de cojín ni dimensiones útiles de una persona sentada.

Se ensayaron tres familias paramétricas de cuerpo H=1,60/1,75/1,90 m: torso/cabeza y pares de muslos/piernas como cápsulas, frente a todos los triángulos externos. Se excluye explícitamente el grupo propio de silla para no confundir contacto con apoyo con un obstáculo externo. Los parámetros de miembros están publicados en `puestos_revision.json`; **no son percentiles ANSUR ni un rig humano validado**. En navegación chocan muslos/piernas con Object_129 en las tres variantes. En los otros cuatro puestos no aparecen contactos externos en esos miembros de referencia; esto no aprueba postura, comodidad ni entrada/salida.

Las plantas de pies hipotéticas quedan elevadas respecto al suelo local ~0,141–0,215 m en navegación, ~0,133–0,207 m en laterales y ~0,029–0,102 m en mando. Señalan que hacen falta ajustes/referencias humanas, no una obligación de bajar todas las sillas por esas cantidades. Se midieron centros de pantallas, alturas y distancias al hombro; una comparación con brazo hipotético 0,38×H no certifica articulaciones, alcance fino, mano, visibilidad ni operación. Las aproximaciones ensayadas son cuatro desplazamientos cardinales de 0,75 m, con ausencia de suelo anotada por separado; no son animaciones de sentarse.

Como criterios externos independientes: OSHA recomienda apoyo completo de pies y posibilidad de ajustar asiento/profundidad; NASA exige estudiar ajuste, alcance y visión para tareas y posturas concretas. Se usan como principios de evaluación, sin afirmar conformidad de estos asientos. [OSHA: sillas](https://www.osha.gov/etools/computer-workstations/components/chairs), [NASA: acomodación antropométrica](https://www.nasa.gov/reference/4-0-physical-characteristics-and-capabilities-vol-2/).

## Accesibilidad
Se ha revisado el alcance físico, no solo el paso de una cápsula de pie. La referencia comparativa CTE DB-SUA contempla puertas de 0,80 m, giro de 1,50 m, altura de umbral 2,00 m y transferencia lateral de cama de 0,90 m; para escaleras generales, huella mínima 28 cm y contrahuella hasta 18,5 cm, con condiciones más estrictas según uso. Se cita únicamente como contraste de escala humana, sin aplicación jurídica a una nave ficticia o al videojuego. [Documento oficial, SUA 1/SUA 2 y anejo A](https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf).

Los giros cilíndricos locales de Ø1,50 ×1,35 m resultan libres en centro de puente, cruce, cabina y centro de habitación, con 8/8 rayos de soporte perimetral; junto a la cama chocan con el proxy. El cilindro se recorta entre +25 mm y +1,35 m y se prueba contra superficies, no volúmenes sólidos certificados. No hay continuidad accesible desde el centro; cambios de nivel, umbrales y aproximación siguen condicionándola. **Grado E para accesibilidad física continua y para acomodación humana completa.** Accesibilidad de UI, control, visión, audición y mareo requieren diseño de juego e intervención humana posterior.

![Asientos medidos](LAMINAS/L03_asientos_medidos.png)
Evidencia: `medidas_puertas.csv`, `alturas_zonas.csv`, `medidas_puestos.csv`, `secciones_niveles.csv`, `puestos_revision.json`, `accesibilidad_camarote.json` y logs 15/18/21. La recomendación es mantener escala provisional y adaptar localmente, sin forzar resultados mediante cápsulas menores.
''')
case_rows=[]
for c in cases:
 case_rows.append([c['id'],' / '.join(j['grade_geometric_interface'] for j in c['joins']),' / '.join(f"{j['width_delta_m']*1000:.1f}" for j in c['joins']),' / '.join(f"{j['profile_sampled_hausdorff_m']*1000:.1f}" for j in c['joins']),c['routes'][0]['samples'],'sí' if c['floor_support']['clear'] else 'no'])
save('02_MODULARIDAD_PASILLOS.md',f'''# VOY-02 — Modularidad y pasillos
## Catálogo y significado de las interfaces
Se conservan 83 mallas nativas, no 317 módulos: la cifra mayor del GLB corresponde a divisiones por material. `clasificacion_modulos.csv/json` cubre cada malla con padre fuente, familia descriptiva, triángulos, envolvente, puertos candidatos y grado. Los nombres ayudan a clasificar, pero no certifican función, habitación completa o transitabilidad.

Familias: rectos corto/medio/largo, curva 90°, T/cuatro vías, tramos con puertas; accesos residenciales, marcos y nichos; cabina/accesos turbolift; conductos Jefferies; mantenimiento y conexiones verticales; envolventes y sala/sanitario. Jefferies, de ~0,914 m de altura exterior en las piezas revisadas, no es un pasillo de pie. La cabina no es un ascensor funcional y Mesh57 es acceso residencial, no un camarote suministrado.

Hay 332 sondeos cardinales en `interfaces.csv`; incluye los rechazados. Un puerto candidato exige anchura ≥0,65 m a las alturas examinadas, suelo compatible y centro sin bloqueo. Los segmentos se extraen 2 mm hacia dentro; se conservan ancla, normal, nivel, techo y anchuras a 0,4/1/1,7/2,2 m. La orientación normal y el ancla definen el ensamblaje; ni bbox ni pivote de catálogo se aceptan como socket final. El catálogo completo tiene grado E para usos aún no ensayados; los recursos seleccionados tienen C global por preparación pendiente. El grado B/C de cada unión se registra aparte.

## Siete ensamblajes ejecutados
{table(['Caso','Grado por unión','Δ ancho mm','Hausdorff aproximado mm','Poses por H','Soporte del recorrido'],case_rows)}
En todos los casos, H=1,60/1,75/1,90 m y r=0,35 m pasan el recorrido central seleccionado, con muestras ≤25 mm y margen 12,5 mm. El soporte usa cinco rayos por pose, cada ≤50 mm, huella de radio 0,20 m y error vertical ≤10 mm. Los resultados y matrices existentes se recuperaron íntegros; no se repitieron por cambiar cámaras.

La diferencia de perfil es un Hausdorff aproximado sobre segmentos muestreados cada 10 mm. No mide un ajuste sólido continuo ni toda la moldura. Residuos de ancla ~0 no eliminan diferencias de hasta 0,422 m de ancho o ~0,376 m en sección de la garganta a cabina. Los rectos comparten sección humana aproximada; algunos encuentros necesitan remates, otros adaptadores completos.

En B06 se conserva el negativo de suelo a ±0,90 m en el extremo estrecho de acceso→cabina: faltan 8/12 sondas amplias. El centro y la huella seleccionada sí tienen soporte. Esto impide afirmar continuidad del extremo completo. Los módulos con hojas laterales cerradas no demuestran un tránsito lateral.

## Decisión de arquitectura modular
Se puede construir una red pequeña mediante anclas propias y adaptaciones. No se demuestra un kit de perfiles intercambiables perfecto. Ninguna unión obtiene A. Priorizar Mesh12/13/18 como familia recta; usar Mesh41/40/38 para desvíos reducidos; completar una única familia de molduras y materiales antes de extender la red. Los accesos de puertas fusionadas exigirán separación local o nuevas hojas de diagnóstico en la fase funcional.

Las matrices en `matrices_instancias.csv/json` aplican normalización y giro/traslación a la geometría fuente en mundo. No son matrices locales de importación nativa: en Blender se componen además con la matriz fuente guardada en VOY-01. No aplicar nuevamente el factor 0,01 ni 100 por costumbre. Hay 24 colocaciones: 18 en los siete casos y seis en G; el mosaico B añade desplazamientos de presentación recogidos en `escenas_manifest.json`.

## Evidencia visual y límites
Las 15 capturas B se revisaron con encuadre dependiente del aspecto. Cada caso oculta temporalmente a los vecinos; las fuentes guardadas permanecen completas. Los cortes Z=2,30 m son solo de captura. Los colores son diagnósticos, sin texturas o PBR validados. La galería muestra perfiles distintos, no una continuidad artística aprobada.

Evidencias: [galería](GALERIA.html), `ensamblajes_pruebas.json`, `compatibilidades.csv`, `interfaces.csv`, `clasificacion_modulos.csv`, `matrices_instancias.json`, `pruebas_rutas.csv`. Pruebas UE, colisión simple, luz, rendimiento y circulación de NPC: E. Reutilizar las interfaces medidas; posponer el resto de la biblioteca hasta necesitarla.
''')
ad_rows=[[a['id'],f"{a['length']:.2f}",f"{a['widthA']:.3f} → {a['widthB']:.3f}",f"{a['heightA']:.3f} → {a['heightB']:.3f}"] for a in proto['adapters']]
save('03_CONEXION_PUENTE_PASILLOS.md',f'''# VOY-02 — Conexión puente–pasillos y acceso central
## Configuración comprobada
Se usa el acceso posterior, a factor de puente 1,10. La traslación exacta es `{proto['bridge_translation']}` m, para llevar su umbral al origen. La biblioteca modular mantiene su escala numérica 1. Las tres parejas completas de hojas están desplazadas a apertura estática, nunca ocultadas para superar cápsulas. Los giros y colocaciones precisos están en `prototipo_conjunto.json` y `matrices_instancias.json`.

La red contiene Mesh13 (recto principal), Mesh38 (cruce), Mesh37 (acceso turbo), Mesh17 (cabina), Mesh18 (ramal camarote) y Mesh4 (envolvente). Hay seis adaptadores nuevos, independientes y naranjas:
{table(['Adaptador','Longitud m','Anchura libre inicio→fin m','Altura libre inicio→fin m'],ad_rows)}
Suelo/techo de diagnóstico de 60 mm y paredes de 80 mm; no son restauración final ni especificación constructiva de la nave. Los verdes son tres obstáculos de mobiliario de referencia.

## Revisión de encuentros y corrección R1
Se revisaron los seis adaptadores contra todos los triángulos próximos del prototipo mediante BVH/SAT. Se conservan contactos de borde, coplanares y cruces transversales por separado en `encuentros_adaptadores.json`. En la primera revisión, AD_PUENTE intersectaba hojas completas ya abiertas, en particular Mesh_1979/1987 y sus remates; el suelo seguía siendo transitable por el centro, pero no era un encuentro correcto.

R1 conserva el suelo desde Y=0 y retranquea paredes/techo hasta **Y=+0,14 m**. Las hojas llegan aproximadamente hasta Y=+0,02338 m y el marco fijo hasta ~+0,135 m. No se cambia ni una hoja ni el puente fuente. La revisión elimina los cruces transversales de AD_PUENTE con las hojas en esa pose, conservando el diagnóstico anterior en `TRASPASO/ANTES_RETRANQUEO_*`. Queda una junta constructiva nominal de unos 5 mm y acabados por resolver. El adaptador sigue siendo C; no se declara recinto estanco ni bolsillo funcional. No se desactivaron colisiones o superficies para aparentar paso.

## Recorridos positivos
Después de R1 se repitieron únicamente las rutas afectadas del conjunto:
{table(['Ruta: inicio real en pasarela posterior','Poses por H','H m','Colisión muestreada','Soporte cinco rayos'],[[r['id'],r['routes'][0]['samples'],'1,60 / 1,75 / 1,90','libre' if all(x['clear'] for x in r['routes']) else 'fallos','correcto' if r['support']['clear'] else 'fallos'] for r in proto['routes']])}
Muestras ≤25 mm, r=0,35 m, margen 12,5 mm. El soporte se comprueba cada 50 mm. Se ensayan triángulos del puente, módulos, adaptadores y tres muebles. Los archivos JSON incluyen todos los puntos, radios, alturas y límites; un mínimo `null` sin candidatos no es una holgura infinita.

## Acceso desde el centro: resultado negativo conservado
El ensayo nuevo utiliza rejilla de 0,10 m reales, con inicios/destinos fijos y ajustes máximos de 0,20 m. Los ajustes encontrados son solo 30 mm desde el centro, 40 mm desde navegación, 50 mm desde pasarela y ~16 mm en la salida. H=1,60 y 1,90 m, r=0,35 m: no se encuentra ruta centro→posterior ni navegación→posterior. Se obtienen 5770 y 5767 nodos libres, respectivamente, repartidos en componentes.

La separación mínima entre componentes de centro y posterior es ~0,838 m en 3D; el diagnóstico recto cruza Mesh_1755, Mesh_1859, Mesh_1892, Mesh_1915, Object_119 y remates. Desde navegación, la separación entre componentes es ~0,926 m y el diagnóstico encuentra Mesh_1739/Mesh_1861, entre otros obstáculos. Estos son lugares de investigación, no puentes virtuales que el personaje pueda saltar. Los cambios de altura observados y la capacidad de subir peldaños requieren un solver apropiado.

La rejilla permite optimistamente diferencias de nivel ≤0,31 m entre vecinos, pero no simula un escalón. Su ruta nueva pasarela→posterior falla un margen refinado junto a `hallwaysupports_3` (~10,50 mm frente a 12,50 mm exigidos). Se conserva ese fallo; no invalida ni sustituye la ruta anterior distinta de pasarela que sí pasó y se utilizó en el conjunto. Una búsqueda finita negativa tampoco demuestra inexistencia absoluta de ruta geométrica o de una solución con cambios locales.

**Grado E para acceso jugable desde el centro y circulación integral. C para el prototipo conectado parcial.** El siguiente paso técnico es caracterizar/subir los cambios de nivel y despejar rutas mediante intervenciones visibles y justificadas, sin reducir cápsula ni esconder arquitectura.

## Contraste de escena guardada
El contraste final cubre los 645 componentes de G, con triángulos en mundo, correspondencia de centroides y permutaciones de vértices; para las tres cajas nuevas se admite distinta diagonal coplanar mediante distancia bidireccional de superficie. Tolerancia de 20 µm, error máximo ~11,44 µm por cancelación float32 en módulo nativo lejano. El diagnóstico más estricto de 10 µm se conserva. El umbral de 20 µm es 625 veces menor que el margen de cápsula, se declara expresamente y no altera ningún baseline.

![Acceso central](LAMINAS/L01_acceso_central.png)
Evidencias: `acceso_central_revision.json`, `contraste_blend.json`, `encuentros_adaptadores.json`, `retranqueo_adaptador.json`, logs 14/17/22/24 y capturas C/G. La escena no prueba CharacterMovement, NavMesh, ascensor, concurrencia ni NPC.
''')
save('04_CAMAROTE_JUGADOR.md',f'''# VOY-02 — Camarote del jugador
## Recurso realmente disponible
Mesh4 / Group4 es una envolvente existente de aproximadamente 8,628 ×6,676 ×2,763 m a escala de catálogo. El sondeo previo 7×7 registró suelo y techo en 49/49 puntos: suelo fuente Z≈1,110166 y techo ≈3,87327. Su entrada X− mide ~1,079792 m a alturas 0,4/1,0/1,7 m y ~0,80679 m a 2,2 m. No se infiere un vano rectangular completo, estanquidad o colisión sólida válida de esas muestras.

En el conjunto, la pieza se rota +90° y se enlaza mediante AD_CAMAROTE. La escena D sitúa la misma habitación alrededor del origen, con pasillo de entrada y adaptador. El alcance no identifica esta habitación como camarote canónico de Voyager ni aprueba su forma artística.

## Comparación de estrategias
{table(['Alternativa','Grado de evidencia','Evaluación'],[[x['option'],x['grade'],x['recommendation']] for x in room['room_options']])}
Se recomienda A como base espacial del laboratorio, con confianza media. B y C son alternativas analizadas, **no habitaciones fabricadas**. Mesh57 es un acceso residencial sin habitación conectada acreditada; no sustituye Mesh4.

Otros recursos: Mesh1 presenta suelo/techo en 49/49 muestras, con techo variable; Mesh5/6, 43/49 y dos cotas separadas ~0,5597 m; Mesh9 conferencias, 28/49 suelo y 25/49 techo; Mesh81 sanitario, 21/49. Son muestreos históricos conservados en `habitaciones_sondeo.json`, sin script original asociado en el traspaso: no se asegura que una receta reconstruida sea idéntica. Las pruebas de posición central de `prototipo_conjunto.json` y los sondeos de interfaces aportan evidencia independiente. No se convierten estos recuentos en porcentaje de superficie o habitaciones completamente acabadas.

## Mobiliario y recorridos
La cama verde mide 1,10 ×2,10 ×0,60 m; el escritorio 0,65 ×1,40 ×0,75; armario 0,65 ×1,50 ×2,00. Son cajas nuevas de diagnóstico con posiciones precisas registradas, no mobiliario recuperado. El escritorio macizo no prueba espacio de rodillas, cajones o postura sentada; la cama no demuestra animación, uso o interacción. Se ha comprobado únicamente el espacio con esos obstáculos y el recorrido a la zona lateral de cama.

La ruta desde pasarela posterior hasta el punto próximo a la cama pasa H=1,60/1,75/1,90 m, r=0,35 m, con 1110 poses por altura y soporte muestreado. Se repitió después de la revisión del adaptador del puente; no se convirtió el inicio en el centro del puente.

## Accesibilidad y márgenes locales
En el centro de la habitación pasa un cilindro de giro Ø1,50 ×1,35 m y ocho rayos de soporte perimetral. En el punto de llegada junto a cama, el mismo cilindro toca el proxy de cama: hay que diferenciar acceso con cápsula de pie y giro grande en ese lugar.

Se midieron rayos laterales desde los bordes de cama a Z=0,10/0,40/1,00/1,70 m. La derecha dispone de aproximadamente **1,137 m** hasta la primera pared; la izquierda, ~3,224 m a alturas bajas por el mobiliario y ~4,437 m por arriba; a los pies, ~4,623 m. Son rayos puntuales, no un rectángulo completo de transferencia. El detalle completo está en `accesibilidad_camarote.json`; no se certifican accesibilidad de vivienda, transferencia humana o circulación de silla de ruedas.

## Preparación necesaria para un camarote funcional
Resolver identidad artística/canónica, escala visual, espesores y conexión de molduras; construir puerta, bolsillos y marco; definir mobiliario independiente, rodillas/alcance, cama utilizable y almacenamiento; verificar suelo/techo/colisión completa, paso de puerta y navegación de llegada. Ventana, baño y replicador deben responder a una decisión de diseño, no añadirse por extender el catálogo. Elegir primero estancia útil y coherente con los pocos pasillos previstos.

Evidencias: capturas D01–D03 y G02/G03; `habitaciones_sondeo.json`, `interfaces.csv`, `prototipo_conjunto.json`, `accesibilidad_camarote.json`. **C como base espacial; E para uso completo, mobiliario final e integración.**
''')
motion_rows=[[d['id'],f"{d['stroke_m']:.4f}",max(p['new_pairs'] for p in d['poses']),max(p['transverse'] for p in d['poses']),', '.join(sorted({c['object'] for p in d['poses'] for c in p['by_object']}))] for d in motion['doors']]
save('05_PUERTAS_SILLAS_CONSOLAS.md',f'''# VOY-02 — Puertas, sillas y consolas
## Puertas: grupos completos y ensayo de carrera
Las tres parejas se recuperaron mediante correspondencia MAX/OBJ y medidas independientes; `puertas_medidas.json` conserva todos los fragmentos, vectores, tangente, normal y carrera. No se confunden paneles Doorpanel con hojas. El control de cápsula en cerrada bloquea, y los ensayos de vano desplazan conjuntos completos, con adornos presentes.

La investigación nueva amplía cinco poses a **21 fracciones de apertura** por puerta. BVH filtra candidatos y SAT de triángulos en 17 ejes cuenta contactos/intersecciones. Se compara con la pose cerrada; una pareja de índices nueva no equivale por sí sola a penetración volumétrica nueva. Para separar evidencia, se exige que ambos triángulos atraviesen el plano del otro >10 µm para clasificarlos transversales; el resto conserva coplanaridad o borde/tangencia.
{table(['Puerta','Carrera por hoja m a 1,10','Máx. parejas nuevas','Máx. cruces transversales','Obstáculos'],motion_rows)}
Izquierda y derecha presentan cruces transversales reales de superficies, con testigos de cruce de planos que llegan a ~9,6 mm y ~38,3 mm en algunas poses, respectivamente. Esas cifras no son profundidad mínima de penetración sólida. Los contactos de suelo a cota del umbral se conservan aparte. D_POST no satisface el criterio transversal en las muestras, pero mantiene contactos de borde/tangencia con marco y suelo; no se transforma ese resultado en un bolsillo libre.

Se ensayaron seis variantes por puerta: desplazamiento normal hacia fuera/dentro de 10/30 mm y elevaciones de 2/10 mm, cada una en cinco fracciones. Ninguna dejó todas las poses sin contactos. No se aplicó ninguno de esos desplazamientos al puente guardado. La comprobación de bordes de los obstáculos, con soldadura diagnóstica de 10 µm, registra bordes abiertos/no manifold; no se deduce cavidad útil por el extremo abierto. No hay barrido continuo, solver mecánico o movimiento Unreal.

El retranqueo R1 del adaptador es otra corrección: elimina cruces del adaptador con hojas posteriores **estáticas abiertas**. No modifica la carrera ni valida abrir/cerrar. Grado C de adaptación; funcionamiento y seguridad E. Para continuar: alojamiento físico medido, marco/guías/remates coherentes, margen bajo hoja, barrido continuo en ida/vuelta, ocupante en vano y ensayos de puertas completas con sus destinos.

![Carreras investigadas](LAMINAS/L02_carreras_contactos.png)

## Sillas: revisión de semántica y movimiento
El agrupado provisional de navegación incluía Object_75 (plataforma) y Object_126/127/129 (consola). Se excluyen del grupo móvil propuesto, quedando **8 piezas**. Los laterales conservan **31 piezas** cada uno. Los grupos de mando pasan de cuatro piezas de carcasa/apoyabrazos a **11**, al añadir siete almohadillas/cojines ChamferBox por silla. La escena aislada E se actualiza para mostrar esa agrupación; no se modifica la geometría fuente ni los puestos del puente.

Los antiguos ensayos rígidos +10° y 10 cm generaban contactos en los cinco grupos; navegación 1172/696, laterales 30/12 y 50/9, mando 2701/2193 y 2917/2199. Se conservan como ensayos de agrupaciones **anteriores**, no validaciones de la semántica corregida. En particular, mover la consola con una silla producía falsos problemas de articulación. No se ha usado ese ensayo para declarar imposibilidad del asiento.

Las piezas bajas no se aceptan automáticamente como base fija. Hacen falta pivote, separación de base/asiento/respaldo/ruedas, límites, pose de ocupante y barrido. Las cápsulas de miembros de `puestos_revision.json` muestran interferencias de piernas con consola de navegación; los otros puestos solo pasan ese proxy externo limitado. Altura, apoyo de pies, alcances y aproximación se estudian en el informe 01. No existe silla funcional u ocupante transportado demostrado. No se copian los 30 cm de Sutherland.

## Consolas y superficies LCARS
Se identificaron 59 objetos con materiales `scrn`/`Mainscreen`: **57 A para separabilidad geométrica plana**, dos B por mezcla/curvatura o error de plano. No se clasifica A la consola completa ni la función. `Mesh_1746` / Mainscreen tiene desviación máxima de planitud ~98,45 mm: no debe alojar automáticamente un widget plano sin adaptación. Se conserva UV0 de origen.

`pantallas.csv` contiene material, triángulos, planitud, normal candidata y grado. `ergonomia_detallada.json` y `puestos_revision.json` añaden alturas y centros vecinos a los asientos. Un centro cercano no asegura mano/visión: las proporciones paramétricas de cuerpo son hipótesis, no antropometría validada; tampoco se implementó cámara de interacción, ampliación, Render Target o UI. Los LCARS existentes siguen siendo imágenes estáticas.

Recomendación: conservar carcasas estáticas, separar la superficie de salida, elegir una estación piloto y validar postura/alcance/vista antes de extender comportamiento al resto. Decisiones artísticas de LCARS y asignación canónica de puestos quedan al usuario. Geometría editable B/C, interactividad E.

Evidencias: `preparacion_funcional.json` (histórico), `carreras_investigacion.json`, `puestos_revision.json`, `presentacion_revision.json`, `pantallas.csv`, capturas E y logs 16/18/20. Los defectos no se eliminan de los informes por presentar una pose abierta.
''')
save('06_MATERIALES_RENDIMIENTO.md',f'''# VOY-02 — Materiales y rendimiento
## Estado real de los materiales
La base VOY-01 aporta 49 imágenes de color utilizables, 102 materiales y UV0 en los 630 objetos OBJ. La colección modular blanca tiene geometría, sin texturas artísticas recuperadas. VOY-02 no ha reconstruido PBR, pintado materiales definitivos, modificado imágenes, remapeado UV, reducido resolución ni optimizado activos de producción. Workbench muestra colores de diagnóstico; sus renders no prueban acabado, iluminación o emisión.

La consolidación de los metadatos glTF identifica **101 OPAQUE y un BLEND (`Window`, alfa ~0,2), 102 doubleSided**. El estado glTF es una exportación de referencia, no una configuración recomendada para todos los materiales UE. `materiales_canales.csv` conserva por material los canales presentes y factores. No se presupone que una imagen de color proporcione normal, ORM o una emisión selectiva útil. Debe distinguirse color, máscara de emisión LCARS, normal y mapas lineales, sin derivar automáticamente PBR convincente de los albedos.

## Presupuesto de imágenes calculado
{table(['Hipótesis, 49 imágenes','RGBA8 nivel base MiB','RGBA8 + mips ideales MiB'],[['Original',f"{budget['RGBA8_base_MiB']:.3f}",f"{budget['RGBA8_ideal_mips_MiB']:.3f}"],['Lado máximo 4096',f"{budget['cap4096_RGBA8_base_MiB']:.3f}",f"{budget['cap4096_ideal_mips_MiB']:.3f}"],['Lado máximo 2048',f"{budget['cap2048_RGBA8_base_MiB']:.3f}",f"{budget['cap2048_ideal_mips_MiB']:.3f}"]])}
Se usa width×height×4 bytes y factor ideal 4/3 de mipmaps. Los límites se simulan manteniendo relación de aspecto y redondeando píxeles, sin ampliar imágenes pequeñas. No se aplica padding potencia de dos, compresión GPU, residencia, streaming, formatos de canal o costes de mipmaps reales. **No es VRAM medida**. Los ficheros comprimidos pequeños pueden decodificar imágenes grandes; ejemplos: scn6.4 7536×5056, scn6.7/scn2.3 6546×5056 y scn4.1 10933×2917.

2K reduce mucho el presupuesto teórico, pero puede destruir legibilidad de LCARS en primer plano. 4K conserva mayor detalle a coste teórico superior. La selección debe ser por uso y densidad de texel, con comparación visual de lecturas cercanas/lejos; no un recorte global ya aprobado. `texturas_presupuesto.csv` permite revisar cada imagen y ambos escenarios. No se han cargado ni reescalado los píxeles para este cálculo.

![Presupuesto teórico](LAMINAS/L04_texturas_hipotesis.png)

## Geometría, slots y riesgos localizados
Leather2 agrupa 68.392 de 271.705 triángulos del puente (~25,2%). Algunos apoyabrazos tienen ~1500 triángulos. Antes de reducir todo, revisar esas concentraciones, repetición, slots, dobles caras y superficies transparentes. `materiales_triangulos.csv` contiene la distribución completa. El número de objetos o materiales no equivale al número real de draw calls de una escena UE.

VOY-01 registra en su GLB derivado 578 triángulos de área <1e−10, 11.919 de UV con área cero y 5368 duplicados locales a cuantización 1e−6. Se atribuyen a aquella validación y conversión concreta, no a un ensayo nuevo de producción. Repararlos exige preservar UV/sombreado y comprobar falsos bloqueos; no se ha limpiado silenciosamente el recurso. El contraste actual demuestra correspondencia de laboratorio con sus superficies ensayadas, no una topología de producción perfecta.

## Plan para Lumen y pruebas UE futuras
La documentación oficial de Lumen recomienda interiores con paredes, suelos y techos separados y revisar cobertura de Surface Cache; una habitación completa con muebles fusionada en una malla no es una preparación suficiente. En Voyager conviene separar por arquitectura y función conservando UV/materiales, revisar los modelos modulares de una sola malla y comprobar caras reversas, espesores y cobertura. Es una recomendación, no un resultado de Unreal ejecutado. [Epic: detalles técnicos de Lumen](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine).

Evitar tratar pequeñas superficies LCARS muy brillantes como única fuente de luz; contrastar emisión artística con luminarias controladas y revisar ruido/reflejos. No aumentar todos los materiales a doubleSided por defecto ni eliminar transparencia sin revisar su intención. [Epic: GI y reflejos de Lumen](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine).

Preparar una escena UE de laboratorio separada solo cuando se autorice esa fase: resolución interna/salida y escalabilidad fijas; comparar calidad de GI/reflejos, iluminación, Surface Cache, geometría y coste GPU/CPU; medir residencia de texturas y streaming con cámaras de uso real. Los objetivos de rendimiento de Epic para sus plataformas son presupuestos de referencia, no FPS prometidos para la RTX 4070 Laptop del MSI. [Epic: guía de rendimiento](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine). El streamer selecciona mips según punto de vista y memoria disponible; medir ese estado antes de fijar presupuesto. [Epic: texture streaming](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-overview-for-unreal-engine).

Grado C de preparación PBR/optimización; E de rendimiento real, Lumen y memoria UE. No se ha abierto un proyecto Unreal ni alterado su configuración. Evidencias locales: `materiales_rendimiento_revision.json`, los tres CSV de materiales/texturas y referencias VOY-01.
''')
save('07_HOJA_DE_RUTA_RECOMENDADA.md','''# VOY-02 — Hoja de ruta recomendada
## Orden de trabajo y criterios de salida
El objetivo sigue siendo un puente excelente, pocos pasillos creíbles, acceso al puente/turbolift y un camarote funcional. No extender cubiertas ni convertir toda la biblioteca. Los bloqueos principales son circulación entre niveles, ergonomía de puestos, puertas con alojamiento y coherencia entre familias. Resolverlos antes de PBR general o sistemas de juego.

| Prioridad | Trabajo Blender autónomo propuesto | Evidencia exigida antes de cerrar |
| --- | --- | --- |
| 1 | Medir escalones y rutas desde centro/navegación; probar alternativas locales visibles de peldaños/rampa o redistribución en copias | Recorrido continuo desde origen explícito, cápsulas 1,60/1,75/1,90 y soporte; subida no inferida de teletransporte |
| 2 | Un puesto de navegación y un sillón de mando completos, con base/cojines/respaldo y cuerpo adecuado | Ajuste de pies/rodillas, torso, alcance y visión; entrada/salida; cada articulación y contexto ensayados |
| 3 | Una puerta posterior completa con bolsillos, guías y encuentro AD_PUENTE | Trayectorias de hojas enteras sin cruces, vuelta, umbral ocupado; volúmenes de alojamiento acreditados |
| 4 | Terminar uniones B01 y una unión C representativa, con perfiles reales | Molduras, suelo/techo, espesores y colisiones sin vacíos/falsos bloqueos; mismas matrices reproducibles |
| 5 | Camarote A/Mesh4 como estancia piloto y mobiliario útil | Acceso completo, puerta, rodillas/escritorio, llegada a cama/almacenamiento y giro donde se requiera |
| 6 | Preparación visual localizada y exportación de prueba | UV/materiales conservados, unidades y pivotes verificados; política de slots y texturas por uso |

Los trabajos propuestos no se han iniciado por entregar la hoja de ruta. La autorización de VOY-02 no se convierte en permiso para modificar originales o proyectos UE.

## Decisiones artísticas del usuario
Elegir fidelidad canónica frente a ajustes de escala humana, sensación de amplitud del puente, tratamiento de los cambios de nivel, qué puestos usarán NPC/jugador, arquitectura del camarote y LCARS/interacción visual. La escala 1,10 queda como referencia provisional, no decisión irreversible. Aprobar un módulo de molduras y una estación piloto antes de extender apariencia. Conservar referencias originales para que los cambios locales puedan compararse visualmente.

## Pruebas UE5 futuras, separadas del principal
Crear un laboratorio independiente autorizado y verificar primero importación en centímetros/escala 1 sin multiplicar 100 otra vez, UV/orientación, pivotes y colisión por pieza. Después: CharacterMovement real subiendo/bajando, aproximación a sillas, puertas barridas con actores/ocupante y concurrencia, NavMesh con rutas completas y tratamiento de puertas cerradas. Una cápsula Blender o una ancla coincidente no sustituye esas pruebas. Fijar el personaje Voyager antes de cambiar parámetros: los valores históricos de Sutherland no son especificación del nuevo juego.

Medir GPU/CPU y texturas con cámara, resolución y escalabilidad documentadas. Validar Surface Cache, reflejos, transparencias y legibilidad LCARS. Solo después, decidir Nanite/LOD, instancias, reducción selectiva y límites de texturas; no inventar FPS a partir de triángulos. Ninguna integración en el proyecto UE principal sin autorización expresa.

## Reutilización conceptual de Sutherland
Reutilizar metodología: raíz local de puerta, agrupaciones móviles con base fija, separación entre intención/permiso/ocupación, contactos y pruebas de ida/vuelta; validación de colisiones simples contra arquitectura visible; recargas y pruebas funcionales con personaje real. Adaptar conceptos, no copiar carreras, 30 cm de sillas, convexos, vanos o parámetros sin medir Voyager. No mover ni ejecutar nada en Sutherland. Sus informes históricos siguen pendientes de la revisión humana que documentan.

## Sistemas futuros del videojuego
Interacción de consolas y cámaras de acercamiento; ocupación de asientos y animaciones; NPC con aproximación/espera/cesión; eventos de puertas y permisos; CoreRPG; turbolift con transporte y destinos; persistencia y accesibilidad de entrada/UI. Son dependencias futuras, sin implementación VOY-02. La existencia de una cabina, pantalla o silla 3D no significa que el sistema exista.

## Qué conviene posponer
Conductos Jefferies explorables, mantenimiento vertical, todas las estancias secundarias, puertas sin destino, cubiertas completas, restauración de todas las versiones MAX, rehacer toda la colección, optimización general sin perfil y decoración final antes de asegurar circulación. Una nave menor y coherente reduce incertidumbre frente a una red extensa sin puestos funcionales.

## Próximo encargo técnicamente acotado
Se recomienda un laboratorio de circulación y puesto piloto que use este estado y sus evidencias, conserve originales y mantenga cambios reversibles. Su resultado debería permitir decidir el tratamiento visible de escalones y navegación con referencias humanas. La restauración artística o integración UE requiere un encargo posterior; este cierre no las ejecuta.
''')
save('08_PRUEBAS_Y_LIMITACIONES.md',f'''# VOY-02 — Pruebas, trazabilidad y limitaciones
## Qué significa el cierre
Se cierra una evaluación técnica, con análisis y ensayos documentados y paquete local. **No se declara aprobada una Voyager final.** E significa no demostrado, aunque se haya ejecutado una búsqueda o evaluación cuyo resultado sea negativo. El laboratorio reduce incertidumbre y conserva tanto éxitos como defectos.

Clasificación: A verificado/compatible en el alcance expresamente probado; B ajustes menores; C adaptación importante; D reconstrucción recomendada; E no demostrado. La ausencia de grado D global no implica que todos los detalles merezcan conservarse: la decisión de reconstrucción local depende del siguiente prototipo. Los 57 A de pantallas solo acreditan separabilidad plana.

## Registro de pruebas y autoridad
| Evidencia | Ejecución | Resultado y límites |
| --- | --- | --- |
| Integridad de recuperación 13 | Rehash nuevo, antes de modificaciones | 207 archivos, 115 entradas originales y 106 copias coinciden; 59 JSON/NPZ/PNG legibles |
| Sondeos/importación 01–06 | Recuperados del trabajo previo | Geometría, correspondencias, vanos completos y factores; no reimportados |
| Ensamblajes 07 | Recuperados, sin cambio de geometría | Siete casos ×tres H pasan rutas centrales y soporte; B/C de perfiles |
| Tránsitos 08 | Históricos de VOY-02 | Ruta pasarela verificada; centro/navegación no acreditados |
| Prototipo 09 | Recuperado y repetido en 24 tras R1 | Dos recorridos ×tres H y soporte; inicio pasarela, no centro |
| Funcional 10 | Histórico de VOY-02 | Carreras y grupos provisionales; resultados no transferidos a grupos revisados |
| Escenas 11, corrección 14c y presentación 20 | Guardado y revisión nuevos | Base OBJ reparada, agrupación semántica y cuello de referencias; ocho escenas, 49 imágenes |
| Contraste 14 | Lectura del `.blend` final sin guardar | 645/645 componentes de G coinciden a tolerancia 20 µm; máximo {maxerror*1e6:.3f} µm |
| Ergonomía 15 y 18 | Nuevas mediciones | Superficies de asiento, suelos/alturas, aproximaciones y miembros hipotéticos; sin rig humano aprobado |
| Carreras 16 | Nuevas 21 fracciones +seis variantes de cinco poses/puerta | Cruces laterales; posterior con contactos; ningún pequeño offset resuelve todos |
| Acceso 17 | Nueva rejilla 10 cm, H=1,60/1,90 | Centro/navegación desconectados bajo hipótesis; ruta nueva pasarela falla refinado marginal |
| Materiales 19 | Recalculo desde metadatos VOY-01 | 49 imágenes, 102 materiales, escenarios 2K/4K; ninguna memoria UE medida |
| Accesibilidad 21 | Nuevos cilindros/soporte y rayos de cama | Cuatro giros locales libres, uno junto a cama bloqueado; no accesibilidad continua |
| Encuentros 22 y revisión 24 | Nuevos SAT por los seis adaptadores | AD_PUENTE cruzaba hojas estáticas; R1 retranquea paredes/techo y se vuelve a contrastar |
| Capturas 12 y galería 23 | Regeneración tras cambios pertinentes | 33 PNG, bounds proyectados, aislamiento B y detalles; atlas y láminas |

No se suman recargas, revisiones o renders como casos nuevos. Los datos por prueba permiten reconstruir qué se ejecutó, sobre qué superficies y en qué versión. `pruebas_rutas.csv`, `contactos_puertas.csv`, `incidencias.csv`, `clasificacion_final.csv` y `DATOS/estado_final.json` son entradas de revisión, no sustitutos de los JSON completos.

## Incidencias resueltas y resultados sustituidos
1. **Base OBJ omitida en 11:** comparación inicial mostraba diferencias de metros. Se confirmó la matriz +90° X del cache y se horneó solo en datablocks copiados. Se conserva `TRASPASO/VOY02_Laboratorio_ANTES_CORRECCION_OBJ.blend`, SHA-256 igual al fichero original inventariado. `correccion_base_obj.json` registra las 630 mallas. Se corrigió también el generador 11 para que no reintroduzca la pérdida de base.
2. **Orden de vértices:** el primer comparador ordenaba flotantes casi iguales lexicográficamente. Ese diagnóstico mezclaba cambios de orden con distancias geométricas. Se sustituyó por KDTree de centroides y seis permutaciones; el JSON preliminar y logs permanecen. No se movió geometría para resolver ese defecto del comparador.
3. **Residuo float32:** una tolerancia preliminar de 10 µm dejaba ACCESO_TURBO a ~11,44 µm. Se documentó una tolerancia final de 20 µm por transformación/cancelación de coordenadas nativas lejanas, manteniendo el residual publicado y el log estricto. No se cambiaron baselines.
4. **Cámaras y vecinos:** encuadre ortográfico por proyección sobre ejes de cámara y aspecto, margen 12%; aislamiento temporal del caso; plantas largas en formato vertical. Se conservan capturas/script previos en ZIP de TRASPASO. Los cortes BMesh y cámaras de captura nunca se guardan sobre el maestro.
5. **Agrupaciones y asientos:** navegación incluía consola/plataforma, mando omitía cojines. Se revisó la semántica y la escena E. El JSON `ergonomia_preliminar_shell_no_asiento.json` se conserva como resultado sustituido: su medida de carcasa no es una altura de cojín. No se ocultan los fallos de scripts previos ni se usan como resultados válidos.
6. **AD_PUENTE:** se detectaron cruces con las hojas estáticas abiertas. Se preservan JSON/NPZ/SAT previos en `TRASPASO/ANTES_RETRANQUEO_*`; R1 cambia solo paredes/techo nuevos. Se repiten rutas G, SAT de encuentros, contraste y capturas C/G afectados. Sigue C y necesita acabado de junta; no se certifica carrera.

Los logs de fallos de 01 y 15 se mantienen. 01_sondeo_max.log y 15_ergonomia_cojines_reales.log acreditan las ejecuciones que los sustituyen. `13_verificar_reanudacion.py` es una auditoría inicial con aserción contra la parada y **no debe repetirse al cerrar**, porque detectaría los cambios de laboratorio autorizados. La verificación final compara originales/copias contra su baseline y lista los cambios derivados por separado.

## Límites geométricos y humanos
Las cápsulas usan distancia exacta segmento–triángulo sobre candidatos espaciales. El recorrido es discreto (≤25 mm), con margen declarado; no solver continuo de cuerpos o escalones. Las superficies por debajo de pie+2 mm se excluyen del obstáculo y el soporte se verifica aparte. Cinco u ocho rayos no cubren un disco continuo. La rejilla no prueba imposibilidad absoluta y un nodo libre no prueba una conexión.

SAT cuenta superficies triangulares y contactos; no resuelve contención en volúmenes sólidos ni cavidades mecánicas. Una hoja dentro de una pared cerrada podría no cruzar superficie en el extremo abierto. Los controles de topología no certifican un bolsillo. La profundidad publicada es testigo de cruce de planos, no distancia mínima de salida del sólido.

Los proxies sentados son hipótesis paramétricas publicadas: no cubren percentiles, ropa, articulaciones, ocupante animado o confort. Los centros de pantalla no representan toda su área de botones ni una tarea manual. No se afirma campo visual, legibilidad dinámica o acceso universal. Los criterios externos son referencias de diseño con enlaces, no certificados de NASA/OSHA/CTE.

Los NPZ originales contienen superficies con sus defectos; no se limpiaron para pasar pruebas. La correspondencia numérica con esas superficies y la legibilidad de ficheros no convierten el activo en producción. El tamaño del `.blend` comprimido no es memoria GPU ni presupuesto de FPS.

## Preservación y alcance
Fuentes registradas, recursos originales, Sutherland, proyectos UE y parámetros del personaje permanecen intactos. Ningún proyecto Unreal se abrió. No hay cambios Git/publicaciones/fusiones ni instalaciones. La biblioteca original indicada por el usuario fue consultada para comprobar acceso; el trabajo se ejecutó en las copias existentes del laboratorio.

ZIP compartible: informes, tablas JSON/CSV, capturas, láminas, scripts, logs y documentos de continuidad. Fuera quedan modelos y texturas originales, `.blend`, NPZ de geometría y respaldos voluminosos; se enumeran rutas exactas en README. El paquete conserva baseline y resúmenes de integridad, sin duplicar los grandes recursos. `PAQUETE/COMPROBACION_ZIP.json` y el SHA-256 final permiten verificarlo. Las limitaciones de licencias de VOY-01 no se interpretan como prohibición de este ZIP local solicitado; no se publica en ningún servicio.
''')
names=['00_RESUMEN_EJECUTIVO.md','01_ESCALAS_ERGONOMIA.md','02_MODULARIDAD_PASILLOS.md','03_CONEXION_PUENTE_PASILLOS.md','04_CAMAROTE_JUGADOR.md','05_PUERTAS_SILLAS_CONSOLAS.md','06_MATERIALES_RENDIMIENTO.md','07_HOJA_DE_RUTA_RECOMENDADA.md','08_PRUEBAS_Y_LIMITACIONES.md']
index='# Voyager — VOY-02\n\nEvaluación técnica cerrada el 21/10/2026. Hay adaptación pendiente antes de producción; el acceso desde el centro del puente no está demostrado.\n\n## Nueve informes\n\n'+'\n'.join(f'- [{n[3:-3].replace("_"," ")} ]({n})' for n in names)+'\n\n## Revisión visual\n\n[Galería de las 33 capturas](GALERIA.html). [Acceso central](LAMINAS/L01_acceso_central.png), [carreras](LAMINAS/L02_carreras_contactos.png), [asientos](LAMINAS/L03_asientos_medidos.png), [presupuesto de texturas](LAMINAS/L04_texturas_hipotesis.png). Las cuatro hojas CONTACTO muestran todas las vistas con leyendas.\n\n## Estado y paquete\n\n[Clasificación final](DATOS/clasificacion_final.csv), [incidencias](DATOS/incidencias.csv), [pruebas de rutas](DATOS/pruebas_rutas.csv), [estado final](DATOS/estado_final.json), [cambios frente a parada](DATOS/cambios_desde_parada.json), [matrices](DATOS/matrices_instancias.json). [ZIP de entrega](PAQUETE/VOY02_ENTREGA.zip), [comprobación](PAQUETE/COMPROBACION_ZIP.json).\n\n## Archivos grandes locales, fuera del ZIP\n\n'
for rel in ['ESCENAS/VOY02_Laboratorio.blend','DATOS/obj_geometria.npz','DATOS/modulos_geometria.npz','DATOS/max_geometria.npz','DATOS/prototipo_geometria.npz','TRASPASO/VOY02_Laboratorio_ANTES_CORRECCION_OBJ.blend','TRASPASO/CAPTURAS_Y_SCRIPT_ANTES_CORRECCION.zip','TRASPASO/ANTES_RETRANQUEO_prototipo_geometria.npz']:
 index+='- `'+str(R/rel)+'`\n'
index+='\nLas copias de fuentes existentes están en FUENTES/OBJ, FUENTES/COLECCION y FUENTES/MAX; las rutas originales se conservan en DATOS/entradas_antes.json y TRASPASO/VOYAGER_HANDOFF.md. No se han movido ni recreado.\n\n## Continuidad\n\nComenzar por los informes 00, 01, 03 y 08. El generador 00_preparar no debe repetirse. Los scripts 13, 14c, 20 y 24 tienen un propósito/estado específico y guardas contra repetición; no ejecutarlos en lote. Los scripts 11 y 09 reconstruyen/sobrescriben productos y no se utilizan para leer o verificar el cierre. El contraste 14 es de solo lectura; el cierre no inicia UE ni restauración artística. Ver la hoja de ruta para el siguiente encargo.\n'
index=index.replace('[ZIP de entrega](PAQUETE/VOY02_ENTREGA.zip), [comprobación](PAQUETE/COMPROBACION_ZIP.json).','ZIP local: `PAQUETE/VOY02_ENTREGA.zip`; su checksum y comprobación se guardan fuera del propio ZIP en `PAQUETE/COMPROBACION_ZIP.json`. [Cómo verificar](VERIFICACION_ENTREGA.md).')
index+='\nEl ZIP es autocontenido para lectura y revisión de resultados. Repetir las pruebas geométricas requiere los NPZ y archivos Blender locales excluidos, en las rutas anteriores.\n'
(R/'README.md').write_text(index,encoding='utf8')
def csvout(name,headers,rows):
 with (P/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)
csvout('clasificacion_final.csv',['area','grado','alcance'],grades)
inc=[('I01','Base OBJ omitida en escenas','RESUELTA','Solo mallas de laboratorio; respaldo y contraste 645 componentes','correccion_base_obj.json'),('I02','Encuadre ortográfico recortado','RESUELTA','Proyección y aspecto; plantas verticales; QA','capturas_qa.json'),('I03','Vecinos visibles en B','RESUELTA','Ocultación temporal y restauración','capturas_manifest.json'),('I04','Acceso desde centro/navegación','NO_DEMOSTRADO','Rejilla refinada negativa; estudiar niveles y arquitectura','acceso_central_revision.json'),('I05','Escalones y soporte fragmentado','ADAPTACION_PENDIENTE','Secciones reales; no solver de subida','ergonomia_detallada.json'),('I06','Cruces de puertas laterales','ADAPTACION_PENDIENTE','Offsets pequeños ensayados sin solución completa','carreras_investigacion.json'),('I07','Bolsillo posterior','NO_DEMOSTRADO','Contactos de borde y contención no certificada','carreras_investigacion.json'),('I08','Agrupación de navegación con consola','RESUELTA_SEMANTICA','8 piezas propuestas; mecánica sin validar','puestos_revision.json'),('I09','Cojines de mando omitidos','RESUELTA_SEMANTICA','11 piezas por grupo; medida sobre cojín','presentacion_revision.json'),('I10','Postura sentada y apoyo de pies','ADAPTACION_PENDIENTE','Proxies hipotéticos; navegación cruza Object_129','puestos_revision.json'),('I11','AD_PUENTE cruza hojas abiertas','RESUELTA_POSE_ESTATICA','R1 retranqueo 140mm; junta final y carrera pendientes','encuentros_adaptadores.json'),('I12','Accesibilidad continua','NO_DEMOSTRADO','Giros locales no resuelven ruta ni cambios de nivel','accesibilidad_camarote.json'),('I13','Texturas y PBR','PREPARACION_PENDIENTE','Escenarios 2K/4K calculados; sin reducción de imágenes','materiales_rendimiento_revision.json'),('I14','Rendimiento y sistemas UE','NO_EJECUTADO','Fase futura explícita; sin FPS prometidos','../06_MATERIALES_RENDIMIENTO.md'),('I15','Familias MAX no equivalentes','LIMITACION_CONSERVADA','No mezclar muebles por escala global','correspondencias_max_obj.json')]
csvout('incidencias.csv',['id','problema','estado','respuesta','evidencia'],inc)
csvout('giros_accesibilidad.csv',['id','diametro_m','alto_m','libre','soportes','obstaculos'],[[t['id'],t['diameter_m'],t['vertical_envelope_m'],t['clear'],f"{t['ring_support_hits']}/{t['ring_probes']}",';'.join(t['blocking_objects'])] for t in room['turning_spaces']])
csvout('encuentros_adaptadores.csv',['id','parejas_superficie','cruces_transversales','coplanares','detalle'],[[a['id'],a['surface_pairs'],sum(c['transverse'] for c in a['contacts']),sum(c['coplanar'] for c in a['contacts']),json.dumps(a['contacts'],ensure_ascii=False)] for a in enc['adapters']])
csvout('pruebas_acceso_central.csv',['altura_m','ruta','rejilla_encontrada','refinado_libre','ajuste_inicio_m','ajuste_destino_m','separacion_componentes_m'],[[t['height_m'],r['id'],r['optimistic_grid_route_found'],r.get('capsule_refined',{}).get('clear'),r['start_adjustment_m'],r['goal_adjustment_m'],r.get('closest_component_gap_m')] for t in access['tests'] for r in t['routes']])
print('REPORTS',len(names),'words',sum(len((R/n).read_text(encoding='utf8').split()) for n in names))
