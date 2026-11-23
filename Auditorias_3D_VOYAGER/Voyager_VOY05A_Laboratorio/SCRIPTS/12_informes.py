import json,csv,collections,datetime,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
rows=read('DATOS/inventario_puertas_accesos.json');counts=read('DATOS/recuentos.json');by={x['id']:x for x in rows};sources=read('VERIFICACION/originales_antes.json')
def put(name,text):
 (R/'INFORMES'/name).write_text(text.strip()+'\n',encoding='utf8')
def table(headers,data):return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+'\n'.join('| '+' | '.join(str(v).replace('|','/').replace('\n',' ') for v in row)+' |' for row in data)
def fmt(x):return f'{x:.4f}' if isinstance(x,(int,float)) else 'E / no determinado'
def dim(x):
 e=x.get('front_surface_envelope');return (f'{e["width"]:.4f} × {e["height"]:.4f} (frente)' if e else f'{fmt(x["width"])} × {fmt(x["height"])}')
closed=[x for x in rows if x['kind']=='puerta_cerrada'];room=[x for x in rows if x['architectural_family']=='AR_HUECO_HABITACION'];door_mod=[x for x in closed if x['source']=='coleccion']
put('00_RESUMEN_EJECUTIVO.md',f'''# VOY-05A — Resumen ejecutivo

Auditoría local del 22/10/2026, Blender 5.2.2 LTS. **Entrega técnica con reservas**: se han inspeccionado los recursos disponibles, sin ejecutar VOY-05B/C/D/E. La publicación remota solo se considera confirmada por `VOY05A_Drive_Verificacion.json`, entregado junto a los ZIP; este informe no sustituye esa comprobación.

Se registran **187 elementos**: **23 puertas o cierres**, 115 bocas/huecos, 27 bocas de conductos bajos, 18 bocas de ejes verticales (9 ejes, dos extremos cada uno), un registro de techo con tapa, un acceso de cabina del puente sin hojas y dos aberturas estructurales de función incierta. Son registros de catálogo: cada extremo de módulo es una interfaz distinta. No equivalen a 187 puertas, habitaciones o mecanismos de un escenario montado. Los formatos alternativos no vuelven a sumarse.

Hay **10 familias arquitectónicas** y **27 grupos de dimensiones de contorno/frente**, redondeados a 1 mm. Los grupos dimensionales no certifican geometrías completas idénticas. Se observan tres familias visuales de cierre: puente detallado, bipartida modular y asimétrica. Un mecanismo doble lineal es candidato para 21 cierres; los dos asimétricos requieren decidir el movimiento. La tapa de techo requiere otra solución. No se ha desarrollado ninguno.

El puente detallado aporta **3 puertas dobles (6 grupos de hojas recuperables)** y **1 acceso de turbolift sin hojas identificadas**. La colección contiene **20 cierres**, además de los huecos de salas, intersecciones y zonas técnicas. Sus accesos de habitación suman 18 registros de contorno, incluidos dos estructurales E; solo tres envolventes Mesh4/5/6 son cajas de habitación, y no se acredita ningún camarote final equipado. Mesh9/11 son variantes de envolvente de sala; Mesh7/10 son estructuras parciales; Mesh81 es un sanitario parcial; Mesh103 es otro puente de menor detalle.

**Puertas completas independientes actualmente: 0.** Las tres parejas del puente conservan piezas independientes de hoja; el sistema completo sigue requiriendo marco y alojamiento. De los 23 cierres: **20 son C**, intervención importante en contexto/marco o separación de malla, y **3 son D**, reconstrucción recomendada (Mesh53, Mesh55, Mesh93). Estos tres objetos son placas separadas, pero sus hojas y marco siguen fusionados. No se confunde objeto suelto con sistema modular.

El puente mide aproximadamente **0,757–0,758 × 1,776 m** en los planos estáticos examinados. Con el factor experimental **1,10**, resulta **0,833–0,834 × 1,953 m**. No se adopta ese factor como estándar. Los frentes de cierre modular más repetidos son de **1,034 × 2,194 m**, mientras que varios residenciales alcanzan **2,524 m** de altura frontal. Una medida de frente no garantiza igual vano útil.

Las reservas principales son la profundidad exacta de marcos fusionados, la distribución individual de espesores de hojas integradas, los alojamientos aún no acreditados, tres registros E y diferencias entre formatos/conversión MAX. Las dimensiones desconocidas se dejan como `null`, sin sustituirlas por la envolvente del pasillo. VOY-02 documentó cruces transversales al abrir las laterales del puente; aquí se conserva esa evidencia histórica, sin repetir mecanismos.

Para Valhalla son aprovechables rectos, curva 90°, T y cruce de cuatro vías, sujetos a sus propias medidas y remates. Mesh2 sí presenta una bifurcación geométrica **Y de tres bocas**; dos bordes necesitan saneado. Mesh52/80 son conectores quebrados con cierres laterales; Mesh56 es una T de conducto bajo. No se propone una dimensión universal de puerta.

El plan recomendado está en [11_PLAN_VOY05B.md](11_PLAN_VOY05B.md). El inventario completo está en [JSON](../DATOS/inventario_puertas_accesos.json), [CSV](../DATOS/inventario_puertas_accesos.csv) y [galería](../GALERIA.html). Capturas reales: [puente](../CAPTURAS/LAM_FINAL_01_PUENTE.jpg), [cierres modulares](../CAPTURAS/LAM_FINAL_02_PUERTAS_MODULARES.jpg), [desvíos](../CAPTURAS/LAM_FINAL_03_PASILLOS_Y_DESVIOS.jpg), [salas y técnicos](../CAPTURAS/LAM_FINAL_04_SALAS_Y_TECNICOS.jpg).
''')
formatrows=[]
for p in sorted((R/'DATOS').glob('*_auditoria.json')):
 a=read(str(p.relative_to(R)));formatrows.append([a['label'],len(a['objects']),sum(x['triangles'] for x in a['objects']),a['unit_system'],a['scale_length']])
put('01_FUENTES_Y_MODELOS.md',f'''# VOY-05A — Fuentes y modelos

Las rutas indicadas en el encargo existen. Se copiaron físicamente al laboratorio; `VERIFICACION/originales_antes.json` registra **{len(sources)} archivos** (modelos, materiales, texturas, ZIP y auxiliares). Las copias utilizadas están en `FUENTES/PUENTE`, `FUENTES/COLECCION` y `FUENTES/RECOVERY`. El `.max` original se conserva y se identifica, pero no se abrió con 3ds Max: se inspeccionó su conversión Blender disponible. Ese límite se mantiene expresamente.

{table(['Recurso analizado','Mallas','Triángulos','Sistema','scale_length'],formatrows)}

El nativo de colección es `star-trek-voyager-collection/source/StarTrekVoyagerCollection.blend`, localizado dentro de la ruta orientativa. GLB y nativo son vistas de la misma colección, con diferencias que se cuantifican en `DATOS/contraste_formatos_actual.json`; las particiones GLB se tratan como materiales, no habitaciones nuevas. El puente OBJ conserva 630 mallas; el Blend de trabajo y el GLB del escritorio reducen el conjunto a una. Se usa OBJ para trazabilidad de hojas.

MAX y OBJ no se declaran copias geométricas perfectas: tienen diferencias reales de conversión, colocación o contenido. La afinidad histórica MAX≈OBJ×1,50813535+traslación se vuelve a comprobar como hipótesis, no calibración física. Véase `DATOS/max_residuos_por_objeto.json`. No se suman automáticamente accesos del MAX como instancias adicionales; los seis grupos de hojas se contrastan mediante nombres, posición y el mapa VOY-02.

Se consultaron informes originales VOY-01/02/03/04 y los informes Sutherland de puertas F07-P02/P03C/P03D/P03E/P03F/P03G disponibles. Sus copias están en `REFERENCIAS`; los hashes de los documentos leídos están en `VERIFICACION/referencias_antes.json`. Las escenas antiguas y los proyectos Unreal no se abrieron ni se guardaron. Los resultados de movimiento de VOY-02 y Sutherland se atribuyen a sus informes; no son pruebas nuevas de VOY-05A.

Disponibilidad: rectos, curva 90°, desvíos T y cuatro vías, Y Mesh2, conectores quebrados Mesh52/80, cabina Mesh17, accesos Mesh37/42/94, envolventes de habitaciones y salas, conductos y mantenimiento. No se acredita una biblioteca de camarotes terminados, zonas técnicas equipadas completas ni mecanismos de puerta. La asignación canónica de cada sala queda pendiente. En `14_CATALOGO_COBERTURA.md` se documentan las 83 piezas, incluidas las que no aportan un acceso aceptado.
''')
inventorytable=table(['ID','Contexto/objeto','Clase','Dimensión m','Grado','Evidencia'],[[x['id'],','.join(x['objects'][:2]) if x['source']=='coleccion' else x.get('legacy_id','cabina'),x['kind'],dim(x),x['grade'],f'[imagen](../{x["capture"]})'] for x in rows])
put('02_INVENTARIO_GENERAL_PUERTAS.md',f'''# VOY-05A — Inventario general

**187 registros de interfaces/cierres de catálogo**, no 187 mecanismos. Se separan 23 cierres representados de las bocas abiertas. Se contabilizan ambos extremos de un tramo o eje porque tienen posiciones y normales distintas; `shaft_pair` vincula los dos extremos de cada eje vertical. La tapa Mesh54 se cuenta una sola vez, evitando sumar su perímetro como un segundo hueco.

Los identificadores `AC_MeshN_XX` derivan del borde fuente `L_MeshN_XX`; `PT_MeshN_XX` identifica los cierres confirmados visualmente; BR_01/02/03 enlazan D_IZQ/D_DER/D_POST; BR_04 corresponde al acceso de cabina. Son estables para esta versión, vinculados a los hashes fuente. No se deben renumerar al separar geometría posteriormente.

El JSON incluye archivo, escena, colecciones, nombres de malla, transformaciones completas por objeto, coordenadas de perfil, normal, tangente, cotas, medidas, escala, materiales, UV, grado, obstáculos y capturas. Los grupos móviles del puente se enumeran íntegros. Una fila sin medidas libres conserva envolvente frontal y explica el método. `null` significa E/no determinado, nunca cero. El CSV replica los mismos campos; las listas y matrices se serializan como JSON dentro de la celda.

{inventorytable}

La selección de bordes está en `DATOS/decisiones_bordes.json`; los bordes descartados siguen disponibles en `DATOS/bordes_abiertos.json`. Se excluyeron pequeñas ranuras de luces/controles, ventanas inclinadas y perímetros exteriores de placas. Los 332 rayos cardinales (`puertos_sondeo_actual.json`) producen 74 candidatos centrales; sirven de contraste, no de inventario exhaustivo. Los bordes y la revisión visual añaden entradas desplazadas y diagonales.
''')
familynames={
 'AR_BOCA_MODULAR':'Bocas de conexión de tramos, marcos/nichos y desvíos; no hojas suministradas en la boca.',
 'AR_HUECO_HABITACION':'Entradas de envolventes de habitación, sala, sanitario o puente simplificado; dos aberturas estructurales E.',
 'AR_CONDUCTO_BAJO':'Secciones técnicas de altura insuficiente para marcha de pie; no trasladar automáticamente el mecanismo humano.',
 'AR_TURBOLIFT':'Gargantas de cabina/acceso con perfil menor; ninguna cabina demuestra transporte funcional.',
 'AR_MANTENIMIENTO':'Conexiones técnicas de pie y entre tramos de mantenimiento; algunas están elevadas en el catálogo.',
 'AR_EJE_VERTICAL':'18 extremos de 9 conductos verticales; requieren otro tratamiento de circulación y protección.',
 'AR_REGISTRO_TECHO':'Un hueco con tapa geométrica dentro de Mesh54, sin articulación identificada.',
 'AR_PUERTA_BIPARTIDA':'18 cierres modulares de aspecto bipartido; 16 integrados y dos placas D.',
 'AR_CIERRE_ASIMETRICO':'Dos cierres complementarios/asimétricos Mesh27/53; movimiento E.',
 'AR_PUENTE_DETALLADO':'Tres parejas de hojas y acceso abierto de cabina del puente detallado.'}
put('03_FAMILIAS_ARQUITECTONICAS.md',f'''# VOY-05A — Familias y repeticiones

{table(['Familia','Registros','Interpretación'],[[k,v,familynames[k]] for k,v in counts['architectural_families'].items()])}

**Tipo arquitectónico** define perfil, uso y montaje. **Tipo mecánico** describe trayectoria. **Tipo visual** define forma visible y materiales. Un turbolift y una habitación pueden compartir un mecanismo doble lineal sin compartir perfil, dimensión, hojas ni controles.

Cierres observados: 3 del puente detallado, 18 bipartidos modulares y 2 asimétricos. Hay también una tapa. No se ha confirmado un diseño inequívoco de puerta humana simple corredera ni una bisagra funcional. No se inventan esas familias. Las superficies de cierre son geometría, aunque incluyan franjas y placas; no se han contado simples pantallas negras o paneles de servicio como puertas.

Repetición de aspecto y frente: Mesh14/25/26/51/54/52/80/93 comparten frentes cercanos a 1,034×2,194 m. Mesh28/57 presentan la misma pauta residencial inclinada, con frente de 2,524 m de alto. Mesh27/53 comparten cierre asimétrico de unos 2,221×2,526 m. Mesh55 presenta un frente mayor, 2,068×2,525 m. Las tres parejas del puente tienen dimensiones muy próximas, seis hojas con trim distinto según orientación.

`grupos_dimensionales.json` contiene **27 grupos** a 1 mm. Son candidatos de reutilización por envolvente, no pruebas de igualdad de topología/UV. La huella de nube de vértices tras quitar solo traslación no produjo duplicados exactos entre las 83 mallas completas. Eso no demuestra que todos sus subcomponentes sean distintos. La identidad de una puerta completa fusionada no puede certificarse antes de definir sus caras: se mantiene esa reserva y se propone hacerlo en B.

Previsión mecánica: **un algoritmo parametrizable doble lineal** puede cubrir 21 cierres candidatos si se construyen cavidades compatibles; se necesitan definiciones de forma/recorrido particulares. Los dos asimétricos y la tapa no se adjudican a ese mecanismo. Los 163 registros restantes sin hojas no necesitan un mecanismo hasta decidir dónde instalar puertas.

Conectividad confirmada por geometría: Mesh12/13/18 rectos; Mesh41 curva de 90°; Mesh40/92 T; Mesh38 cruce de cuatro vías. **Mesh2 es una Y**, tres bocas y dos brazos diagonales, con bordes no cíclicos que requieren saneado. Mesh52/80 tienen dos extremos y acceso interior adicional, más cierres laterales: su planta quebrada no los convierte automáticamente en una Y. Mesh56 es una T de conducto bajo (normales cardinales), no una Y de pasillo humano.
''')
bridgedims=table(['ID','Vano mínimo muestreado original m','A 1,10 experimental m','Hojas originales: ancho × alto × espesor de envolvente m'],[[x['id'],dim(x),f'{x["experimental_1p10"]["width"]:.4f} × {x["experimental_1p10"]["height"]:.4f}',' / '.join(f'{q["width"]:.4f} × {q["height"]:.4f} × {q["thickness_envelope"]:.4f}' for q in x['leaf_dimensions'])] for x in rows if x['id'] in ['BR_01','BR_02','BR_03']])
put('04_DIMENSIONES_Y_ESCALAS.md',f'''# VOY-05A — Dimensiones y escalas

Se usa **1 unidad de mundo Blender = 1 m de trabajo**. El `scale_length` observado es 1,0, con sistema métrico. Es una convención de trabajo del recurso; no certifica dimensiones canónicas o antropometría final. Se conservan matrices fuente sin aplicar normalizaciones a las mallas. No se aplica por costumbre ni ×100 ni ×0,01.

{bridgedims}

Los vanos del puente se miden sin mover hojas: el cálculo de rayos omite sus triángulos y examina siete planos normales entre −80 y +80 mm, a cinco alturas. Se registra el mínimo hallado, sin afirmar continuidad entre muestras ni un prisma rectangular libre. Todos los valores están en el JSON, incluidos los rayos sin respuesta. La altura BR_04 de 1,7756 m y ancho 0,7583 m proceden de un borde no cíclico, error de plano ≈11 mm: son envolventes, grado E para vano mínimo.

El factor **1,10 es exclusivamente experimental** en la columna de comparación. La escena de auditoría conserva 1,00. A 1,10 la altura lateral ronda 1,953 m: deja aproximadamente 53 mm nominales sobre 1,90 m, antes de tolerancias, cascos, pendientes y colisión. No es una aprobación de paso. La transformación MAX/OBJ ≈1,50813535 pertenece a versiones de recurso, no se adopta como nueva escala humana.

Frentes modulares: estándar ≈1,0341×2,1935 m; residenciales inclinados ≈1,0341×2,5237 m; asimétrico ≈2,2210×2,5263 m; Mesh55 ≈2,0681×2,5249 m. **Son caras de cierre, no medidas de vano útil.** El espesor normal casi cero de `front_surface_envelope` describe la coplanaridad de las caras: no el espesor de una hoja. No se usa ese cero como espesor físico.

Los contornos de bocas de pasillo suelen alcanzar ≈2,9613×2,8164 m de envolvente; hay molduras y perfiles estrechados, por lo que deben consultarse `widths_by_height`. Las entradas Mesh4/5/6 miden ≈1,0798×2,2034 m de envolvente. Su cota de catálogo inferior es ≈1,1102 m; otras salas empiezan en ≈0,2380 m. Los módulos técnicos elevados conservan niveles ≈3,2792 m. Estas cotas no implican escaleras construidas ni un suelo de cubierta común.

Los conductos Jefferies tienen secciones de altura ≈0,9144 m; escotillas pequeñas ≈0,768–1,102 m. Su adaptación a personaje agachado o reptando está fuera de A. Las dos dimensiones de `boca_vertical` y del registro de techo son X/Y horizontales; no se interpreta su segundo valor como altura de pie.

La profundidad exacta de cada marco integrado y los tamaños individuales de hojas fusionadas quedan E: no hay pertenencia de caras inequívoca que permita medirlos como piezas físicas sin hacer la separación de B. Se entregan coordenadas, planos, caras frontales y envolventes fuente para realizarla posteriormente. Esa falta no se oculta con medidas de caja del pasillo.
''')
put('05_INDEPENDENCIA_Y_SEPARACION.md',f'''# VOY-05A — Independencia y separación

Los grados del inventario corresponden a la **viabilidad del sistema completo** o, en bocas sin puerta, a su interfaz arquitectónica. No son aprobaciones funcionales. A = independiente hoy; B = organización/intervención menor; C = geometría/contexto importante; D = reconstrucción recomendada; E = evidencia insuficiente.

{table(['Grupo de cierres','Cantidad','Grado','Motivo'],[['Puente detallado',3,'C (hojas B)','Grupos de hoja ya identificables; marco y alojamiento no modulares.'],['Cierres modulares integrados',17,'C','Comparten malla y conectividad soldada con arquitectura o marco.'],['Placas Mesh53/55/93',3,'D','Objeto separado, pero hojas/marco fusionados, espesor global limitado y sin alojamiento.']])}

Total cierres: 20 C y 3 D. **A completos = 0; parejas con hojas recuperables independientes del puente = 3.** La tapa Mesh54 es C: isla desconectada dentro de la misma malla, no objeto funcional. Los grados B de las bocas abiertas describen conservar y montar un inserto; no suman puertas independientes.

Se examinó conectividad con soldadura diagnóstica de 10 µm, sin modificar ninguna malla. Mesh14/25/26/27/28/51/53/55/57/93 forman una componente principal común de arquitectura y cierre; Mesh54 tiene una segunda isla correspondiente a la tapa. La conectividad es evidencia de integración, pero ni una sola componente impide por sí misma una futura separación, ni múltiples islas prueban componentes semánticamente correctos.

Para B: duplicar el módulo fuente, crear grupos de caras de hoja, marco, remate y mamparo; preservar materiales y todos los UV; guardar correspondencia cara original→pieza nueva. La operación debe producir una arquitectura utilizable con puerta retirada, sin dejar una pared tapando el hueco o un vacío alrededor del marco. Cerrar espesores y conservar una copia íntegra como referencia oculta y explícita, sin superponerla al resultado.

En el puente, recoger todos los fragmentos de cada lista `leaf_dimensions.objects`: franjas, tiras y adornos no deben quedarse flotando. Doorpanel es un control; no una hoja. El pivote actual no se acepta como raíz modular. No se han creado pivotes, jerarquías móviles, separación definitiva ni animaciones en A.

Evidencias: `coleccion_componentes.json`, topología en los siete `*_auditoria.json`, [marcos y placas](../CAPTURAS/LAM_FINAL_05_MARCOS_Y_PLACAS.jpg), planos frontales y manifest de captura. La tolerancia de soldadura sirve para diagnosticar costuras de importación; no es tolerancia de fabricación ni de colisión.
''')
put('06_MARCOS_HUECOS_Y_CAVIDADES.md','''# VOY-05A — Marcos, huecos y cavidades

No se ha certificado ningún bolsillo físico de recogida como parte de un sistema reutilizable. Un lado abierto o una pared sin grosor no son un alojamiento. La libertad visual tras una superficie no prueba espesor, guías, cierre posterior ni ocultación oblicua.

En BR_01/02/03 las hojas están separadas del contexto por objetos, pero marcos y mamparos no forman un cassette independiente. La evidencia VOY-02 conservada documenta cruces transversales en las laterales: BR_01 con Mesh_1837/Mesh_1855/Object_81 y BR_02 con Mesh_1858/Object_82. En el máximo de su ensayo anterior hubo 106 y 264 parejas transversales, respectivamente; no se equiparan a profundidad sólida. BR_03 no mostró cruces transversales en aquellas muestras, pero mantuvo contactos con Mesh_1832/Mesh_1833/hallwayfloor_1. Su ausencia de cruces no certifica bolsillo libre. VOY-05A no repite movimientos ni declara resueltos esos casos.

Mesh14/25/26/54 tienen hojas frontales en mamparos laterales del tramo; al abrir hacia el interior de la pared pueden invadir molduras, luces, suelo y remates. En Mesh28/57 y Mesh52/80 las hojas están en planos diagonales: el desplazamiento debe expresarse con tangente local, y un bolsillo puede invadir el brazo vecino. Mesh51 añade cierres a ambos extremos de un nicho: no se debe destinar el volumen del otro cierre al alojamiento del primero.

Mesh27/53 presentan un cierre asimétrico con elementos superiores e inferiores entrelazados; no se presupone deslizamiento horizontal idéntico al estándar. Mesh53/55/93 son placas de ≈73 mm de profundidad global, incluida su parte fija. Ese espesor no contiene por sí solo una cavidad lateral de más de medio ancho. Se recomienda reconstrucción del cassette en B/C, preservando la placa como referencia visual.

En huecos sin hojas, el borde mide la conexión, no un marco independiente. Algunos contornos corresponden al extremo de un volumen abierto y deberán recibir juntas/adaptadores. Mesh2/24/45/62 y otros contornos ramificados presentan bordes que requieren saneado. Los marcos integrados no tienen profundidad nominal certificada: `frame_depth=null`, explicado por fila y por método en el informe 04.

La propuesta conceptual distingue tres volúmenes: paso de personaje; recorrido de hoja; espacio de recogida con paredes/guías físicas. Para una hoja de ancho b, la carrera inicial candidata debe cubrir la parte necesaria para liberar el perfil más un margen a definir; no se fija una fórmula a partir de la mitad del vano sin estudiar solapes, bandas y jambas. El espesor y el margen lateral deben medirse después de delimitar la pieza.

Cada familia deberá revisar suelo real bajo umbral, techo/dintel en toda la profundidad y paredes a ambos lados. Los rayos y envolventes de A no sustituyen barrido continuo, colisión o paso de personaje de D. No se valida una puerta haciendo desaparecer su hoja dentro del mamparo.
''')
put('07_COMPATIBILIDAD_VALHALLA.md','''# VOY-05A — Reutilización para Valhalla

Los interiores se consideran escenarios independientes del exterior. No se impone ajuste físico a sus cubiertas exteriores. Voyager suministra una base modular, pero Valhalla debe fijar sus propias dimensiones y acabados.

Conservar como candidatos de arquitectura: rectos Mesh12/13/18; curva 90° Mesh41; T Mesh40/92; cuatro vías Mesh38; Y Mesh2 tras sanear las dos bocas diagonales; conectores quebrados Mesh52/80 después de estudiar cierres y perfiles. Las diferencias históricas VOY-02 de garganta, ancho, moldura y soporte siguen vigentes. No se declara un kit de encaje perfecto.

Los 20 cierres modulares no permiten retirar hoy solo el diseño Voyager e instalar otro. Hay mallas conectadas, caras de pared tras el frente, perfiles diagonales y placas demasiado finas para resolver alojamiento. La migración conceptual es: definir el contorno arquitectónico→retirar geometría de cierre→reparar el mamparo→normalizar el hueco a la regla Valhalla→montar adaptador/cassette→instalar hojas y controles Valhalla→usar un mecanismo parametrizado compatible. Todo ello es trabajo futuro.

No se acepta escala no uniforme de todo el conjunto como sustituto de rediseñar hojas, espesor de pared y cavidad. Se parametrizan W/H/perfil/D y espacios de recogida por nave. Un cambio de altura puede alterar dintel, acceso y techo; un cambio de ancho puede destruir una curva o acercar dos alojamientos de puertas vecinas. Las puertas en 45° necesitan evaluar las dos arquitecturas que limitan su bolsillo.

La separación visual permite sustituir materiales/UV y decoración sin cambiar la lógica de apertura. Los materiales PBR Valhalla deberán ser exclusivos y producirse en su fase; no se han aplicado materiales nuevos ni diseñado hojas Valhalla. Los UV existentes se preservan como evidencia y no se declaran listos para PBR.

Viabilidad: buena para conservar tramos y reutilizar la idea de mecanismo doble lineal; condicionada para los huecos; no demostrada para un cassette físico común de dimensiones fijas. Los cierres asimétricos y las bocas verticales necesitan soluciones propias. No se copian las medidas Sutherland o Voyager a Valhalla.
''')
put('08_REFERENCIAS_SUTHERLAND.md','''# VOY-05A — Referencias Sutherland

Se leyeron copias de informes disponibles de F07_P03FG_DoorLab, incluidos los baselines de P02/P03B/P03C/P03D/P03E y los informes finales P03F/P03G. No se modificó ningún archivo Sutherland ni se abrió Unreal. Los hashes de estos documentos se conservan en `VERIFICACION/referencias_antes.json`. El informe de sillas leído por VOY-04 es contexto ergonómico, no fuente de dimensiones de puerta.

La última entrega Sutherland se describe como **preparada para revisión humana, sin integración en producción**. Registra cuatro puertas/ocho hojas y un único BP parametrizado. D04 tiene cabina construida; D01–D03 permanecen bloqueadas por falta de destino. Esas pruebas no aprueban automáticamente Voyager ni Valhalla.

Procedimientos aprovechables: identificar caras originales de las hojas y preservar UV/normales; usar raíz de puerta con X normal, Y deslizamiento y Z altura; agrupar toda la hoja y conservar las bases/mamparos fijos; fabricar alojamientos huecos sólidos y retornos que oculten la hoja en vistas oblicuas; mantener referencias originales sin duplicados activos; comprobar lectura de assets importados frente a Blender guardado.

Problemas documentados y lecciones: D02/D04 necesitaron pequeñas elevaciones propias para holgura con sus suelos; D03 necesitó carcasa posterior menos profunda para evitar techo/paneles; D04 detectó discrepancia Chaos frente a SAT y se recocinó un convexo exacto en assets nuevos, sin encoger hojas. Una jamba siguió bloqueando un carril lateral y no se recortó para falsear el paso. El fallo de NavMesh provenía de un volumen temporal recolocado al origen por el fixture; se comprobó la posición real después de construirlo.

No se trasladan los recorridos ≈86,8 cm, vano ≈164 cm, ranuras, márgenes, elevaciones o tiempos de Sutherland: pertenecen a sus hojas y contexto. El puente Voyager examinado tiene aproximadamente la mitad de ese ancho a escala fuente. Reutilizar el procedimiento y el contrato de ejes resulta razonable; reutilizar dimensiones sin medición no.

Pruebas futuras a tomar como referencia en C/D: poses intermedias y barrido completo ida/vuelta; geometría real antes de interpretar cajas; comprobar contactos intencionales por separado; ocultación física en varias vistas; paso y soporte en cabina real; bloqueo mientras no exista destino. VOY-05A no ejecuta esos ensayos ni crea Blueprints. La organización desacoplada de sillas informa el criterio de componente fijo/móvil, sin importar su desplazamiento de 30 cm.
''')
put('09_PROPUESTA_INTERFAZ_MODULAR.md','''# VOY-05A — Propuesta conceptual de interfaz

Propuesta para revisión, **sin implementación ni norma dimensional definitiva**. Cada instalación enlaza arquitectura, contorno de hueco, adaptador opcional, marco/cassette, hojas, guías, controles y decoración. El mecanismo recibe parámetros de recorrido y estados sin depender de nombres de malla Voyager.

La raíz local se sitúa en el centro del umbral terminado. +Z es arriba; +X es normal hacia el destino documentado; +Y completa la base y es tangente al deslizamiento. Para una doble candidata, hoja izquierda abre hacia −Y y derecha hacia +Y vistas según el contrato de normal. El inventario conserva `center_world` de contorno (centro de envolvente, excepto las tres raíces históricas del puente en suelo), `floor_z`, normal y tangente: no se deben confundir sus centros con un pivote ya implementado.

Parámetros propuestos:

| Grupo | Datos necesarios |
| --- | --- |
| Hueco | Perfil 2D ordenado, W/H de envolvente, anchos a distintas alturas, cota de suelo, rango de profundidad útil y tolerancias |
| Montaje | Transformación de raíz a arquitectura; puntos de jamba izquierda/derecha y dintel; patrón de fijaciones definido por adaptador |
| Marco | Profundidad frontal/posterior, espesores, sellos, remates, máscara del contorno y zonas que no se deben recortar |
| Hojas | Uno o más subensamblajes, geometría local, volumen sólido, solapes, posición cerrada, transformaciones abiertas y límites |
| Recogida | Dos o más volúmenes reservados, guías físicas, fondo, retornos y acceso de mantenimiento |
| Circulación | Prisma/perfil libre, radio/altura de personaje objetivo, zonas de aproximación y ocupación, soporte y destino existente |
| Interacción | Puntos para controles y sensores; referencias locales, permisos y estado de destino; desacoplados de LCARS/materiales |
| Apariencia | IDs de superficies y materiales, UV, decoración/sonido y variantes por nave |

Los puntos propuestos son semánticos; sus coordenadas se derivarán del perfil y del cassette elegido, no de una tabla universal de metros. La profundidad puede ser asimétrica. Una puerta puede compartir tipo mecánico con otra y necesitar adaptador distinto. La interfaz debe rechazar instalación si su recorrido/cavidad o paso no caben en la arquitectura.

Adaptación: conservar transformaciones rígidas de arquitectura; dimensionar nuevo hueco según cada nave; definir nuevos montajes y geometría; recalcular hojas, guías y espacios; validar límites antes de compartir comportamiento. No se ha creado un objeto Root, socket, articulación, animación ni volumen de colisión. Este documento prepara B/C sin ejecutar esos trabajos.
''')
put('10_RIESGOS_Y_BLOQUEOS.md','''# VOY-05A — Riesgos y reservas

La auditoría técnica queda **con reservas**, no bloqueada para estudiar B. Los recursos están accesibles y existe inventario visual. La entrega remota depende de su verificación independiente. Ningún resultado autoriza comenzar las otras subfases.

| Riesgo/reserva | Evidencia | Consecuencia y siguiente resolución |
| --- | --- | --- |
| Escala física provisional | Puente ≈0,758×1,776 m; 1,10 experimental | Resolver dimensiones objetivo antes de normalizar huecos |
| Cierres fusionados | Conectividad soldada y caras frontales | Definir pertenencia de caras en B; no basta separar materiales |
| Marcos/espesores E | No hay pieza semántica delimitada | Medir sección completa tras definir componentes; no usar bbox de pasillo |
| Cavidades sin certificar | Paredes abiertas y antecedentes VOY-02 | Diseñar alojamiento físico; resolver suelo/dintel y vistas oblicuas |
| Diferencias entre formatos | Contraste de vértices y MAX residual | Trabajar con fuente trazada; no mezclar silenciosamente versiones |
| Y Mesh2 y bordes ramificados | Dos perfiles diagonales no cíclicos | Sanear antes de montar puertas o certificar unión |
| Tres registros E | AC_Mesh7_00, AC_Mesh103_05, BR_04 | Confirmar función o vano mínimo; no asignar puerta final |
| Espacios sin destino | Catálogo de partes, no nave ensamblada | No habilitar tránsito hacia habitaciones supuestas |
| Niveles diferentes | Cotas 0,238/1,110/3,279 m | Definir transformaciones de montaje, suelo y transiciones |
| Exactitud numérica ≠ física | Contornos y rayos discretos | En D verificar barridos, colisión, ocupante y soporte continuo |
| Alcance de repetición limitado | 27 grupos por envolvente; no piezas separadas | Comparar geometría completa/UV una vez definidas las caras en B |

Las categorías de salas describen geometría disponible. No hay evidencia de camarote final aprobado, habitación funcional equipada, puertas animadas o interiores Valhalla creados. Las variantes MAX con geometría residual no se convierten en nuevos accesos sin revisión semántica. El `.max` nativo se conserva sin inspección en su aplicación original; la conversión Blender sí fue enumerada y contrastada.

Las capturas son renders de Blender de los modelos reales, con colores de diagnóstico y en algunos casos recorte frontal/corte desechable. No demuestran PBR, colisión ni tránsito. El texto y las líneas amarillas identifican contornos medidos; no reconstruyen superficies ausentes.
''')
put('11_PLAN_VOY05B.md','''# VOY-05B — Plan de intervención propuesto (no ejecutado)

Objetivo de B: dejar arquitectura, hueco, marco, hojas y decoración como componentes sustituibles. **No comenzar mecanismos C, animaciones/pruebas D ni biblioteca E por incluirlos en este plan.** Cada intervención futura debe partir de otra copia física y conservar originales y manifiesto.

| Orden | Piloto/variantes | Trabajo propuesto | Criterio de salida de B |
| --- | --- | --- | --- |
| 1 | BR_03 posterior, después BR_01/02 | Conservar grupos completos de hojas; delimitar marco/mamparo; estudiar sección de alojamiento y umbral | Listas semánticas verificadas; arquitectura íntegra con hojas retiradas; UV y posición cerrada conservados; no afirmar cavidad libre por ausencia histórica de cruces |
| 2 | PT_Mesh14_01; comparar _02, Mesh25/26/54 | Piloto modular recto; separar hojas/marco y remates de pared; preservar otro lateral | Un tramo completo con hueco normalizable y piezas independientes; sin pared duplicada tapando el acceso |
| 3 | PT_Mesh28_01 y Mesh57 | Definir caras en plano 45°, recuperar ambas hojas y marcos; reservar volumen fuera de brazos vecinos | Plano local, contorno y componentes; diferencias residenciales de altura documentadas |
| 4 | PT_Mesh52_01/02 y Mesh80 | Revisar dos cierres diagonales y boca interior; adaptar montaje a planta quebrada | Sin invadir el conector ni confundirlo con Y; mapa de piezas repetidas y variantes |
| 5 | PT_Mesh27_01 y PT_Mesh53_01 | Confirmar composición del cierre asimétrico; decidir separación o nueva geometría | Despiece claro y propuesta de movimiento aún conceptual; no forzar mecanismo estándar |
| 6 | PT_Mesh93_01, PT_Mesh55_01 | Reconstrucción modular de placas recomendada, usando frente/UV como referencia | Marco y hojas sustituibles; arquitectura separada; cavidad diseñada sin animación |
| 7 | AC_Mesh17_00 y accesos Mesh37/42/94; BR_04 | Establecer garganta real, soporte de umbral y relación con cabina | Vano mínimo definido; destino y suelo identificados; ningún ascensor funcional supuesto |
| 8 | AC_Mesh4_00, Mesh5/6 y Mesh9/11/81 | Priorizar una envolvente de habitación; ajustar niveles; separar solo su acceso | Habitación base y hueco definidos; no inventar camarote equipado |
| 9 | Y Mesh2, T Mesh40/92, cruce Mesh38 y curva Mesh41 | Sanear perfiles, conservar arquitectura de circulación y diseñar insertos donde hagan falta | Bordes de montaje claros; no instalar puertas en todas las bocas por defecto |
| 10 | Conductos bajos, ejes verticales y tapa Mesh54 | Despiece específico de escotillas/registros; conservar pares de extremos | Piezas independientes y uso previsto, sin tratarlos como puertas humanas de pie |

BR_03 se propone primero porque sus hojas son identificables y el antecedente VOY-02 no detectó cruces transversales, aunque sí contactos. BR_02 concentra las interferencias más severas y resulta útil después como prueba de arquitectura difícil. Mesh14 es el mejor segundo piloto para aprender a separar el módulo nativo sin depender del formato OBJ fragmentado.

Antes de fabricar: elegir escala objetivo con datos físicos del proyecto; mantener 1,10 solo como comparación; delimitar caras de cada marco/hoja; documentar espesores y profundidad; resolver tres E. No copiar la carrera Sutherland de ≈0,868 m ni la experimental Voyager sin calcular el nuevo perfil.

Entregables esperados de B: Blend de componentes estáticos, arquitectura sin cierres integrados, mapa de caras originales, matrices/pivotes propuestos, superficies UV preservadas, registro de recortes/reconstrucciones y comparativas antes/después. Comparar la geometría fija conservada y las piezas fuente; controlar dobles superficies y pérdida de adornos. El diseño debe permitir retirar Voyager e instalar una variante Valhalla mediante adaptador sin rehacer el mecanismo.

Lo que se pospone a C/D: recorridos funcionales, curvas de apertura, jerarquía operativa final, detección de intención, colisiones móviles, personajes, Blueprint/Unreal y pruebas de ida/vuelta. VOY-05A solo entrega este orden y los candidatos.
''')
put('12_VERIFICACION_INTEGRIDAD.md','''# VOY-05A — Verificación de integridad y entrega

Los archivos originales se inventariaron y calcularon con SHA-256 antes de usar las copias. `VERIFICACION/originales_antes.json` y `referencias_antes.json` enumeran el alcance exacto: no es un hash global de todo el MSI, de CoreRPG ni de todos los proyectos Sutherland. La relectura final está en `VERIFICACION/integridad_final.json`, que distingue cambios de bytes y metadatos. Consultar su resultado, no inferir integridad a partir de este texto.

Las escenas de revisión conservan posiciones/hojas estáticas y materiales/UV fuente. Se comprueban por recarga de Blender contra las coordenadas mundiales, triángulos y nombres fuente; `VERIFICACION/escenas_readback.json` documenta resultados. Se empaquetan recursos de imagen disponibles; los ausentes se informan, sin sustituirlos por texturas nuevas. Las escenas distribuidas son las `*_Revision.blend`; las primeras escenas de importación quedan como pasos intermedios locales.

`VERIFICACION/validacion_local.json` comprueba IDs, CSV/JSON, existencia de cada captura, dimensiones de PNG, enlaces relativos de Markdown/HTML y estructura de informes. Los datos numéricos, scripts, manifiestos y referencias acompañan el paquete documental. No se incluyen cachés, bytecode ni dependencias Python descargadas en los ZIP documentales.

Cada ZIP se abre, comprueba CRC, nombres únicos y rutas relativas seguras, se extrae a verificación temporal dentro del laboratorio y se contrasta su SHA-256 por miembro. `VERIFICACION/paquetes_validacion.json` guarda la comprobación y `PAQUETE/VOY05A_Paquetes_SHA256.txt` sus hashes. Cada paquete debe permanecer por debajo de 100 MiB; si se divide la colección de imágenes, cada ZIP conserva rutas completas y es extraíble por sí mismo en la misma raíz.

La entrega remota tiene una verificación separada: `VOY05A_Drive_Verificacion.json` y `VOY05A_Drive_SHA256.txt`. Se exige metadata real de Drive, tamaño y SHA-256 remoto cuando esté disponible. Si solo existe MD5 se compara también con el archivo local; no se afirma descarga si no se hizo. Los dos manifiestos finales se suben después de los paquetes. Su propio hash no se incluye dentro de sí mismos, para evitar autorreferencia.

No se hicieron commits ni PR, no se abrió Unreal, no se añadieron animaciones o mecanismos, y no se guardó sobre los originales. Los cambios temporales son cámaras, visibilidad, líneas de contorno y cortes sobre mallas desechables. Las copias locales se conservan después de la publicación.
''')
put('13_METODO_Y_REPRODUCCION.md','''# VOY-05A — Método y reproducción

Entorno observado: Windows 11, Blender 5.2.2 LTS instalado en `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`; Python de análisis con NumPy/Pillow y SciPy. `requirements.txt` identifica las dependencias; la copia instalada de SciPy en HERRAMIENTAS solo pertenece al laboratorio. No modifica Blender ni proyectos del usuario.

En una copia nueva del laboratorio: ejecutar `00_preparar.py` para copiar entradas originales disponibles y generar baseline; `01_inspeccionar_blender.py` con los siete nombres de recurso para exportar matrices/triángulos; el modo `catalogo` produce caras opuestas y cortes. Las vistas ISO/TOP de la primera pasada se conservan; `09_capturas_inventario.py` y las elevaciones del script 04 suministran la evidencia final por registro. No repetir el preparador sobre una entrega cuyo baseline se quiera preservar.

Orden de análisis: 03 conectividad→06 rayos/superficies→07 bordes de colección y puente→08 inventario→10 contraste/grupos→09 capturas→11 láminas→12 informes→14 recarga de escenas→15 validación/paquetes. El inventario tiene selección semántica explícita de caras frontales, verificada con elevaciones; no es un detector automático de puertas genérico. Las caras se identifican por índices de triángulo fuente y hashes, no por color/material.

Se sueldan coordenadas solo para análisis a 10 µm. Se extraen componentes de borde y se filtran secciones verticales de ancho ≥0,50 m y alto ≥0,65 m, error de plano <0,07 m; la revisión visual excluye placas exteriores, ranuras y ventanas inclinadas. Los 18 extremos de ejes verticales y el registro con tapa se incorporan explícitamente. Se conservan todos los rechazos. Las tres E no se fuerzan a una función.

`widths_by_height` conserva intersecciones reales de segmentos a distintas cotas. La envolvente de borde no garantiza la anchura libre mínima en cada profundidad. Los rayos del puente omiten hojas estáticas para sondear el hueco; no se desplazan piezas. No se ejecuta apertura/cierre ni se crean keyframes en A. Los datos de barrido anteriores permanecen bajo REFERENCIAS con su atribución histórica.

Los renders usan Workbench, geometría y colores originales de diagnóstico. CAT_*_CUT se obtiene de bisección de una malla desechable. Las líneas amarillas siguen segmentos de borde real; el texto añadido explica ID y medida. Las vistas del puente usan recorte frontal para evitar que otra arquitectura tape el acceso. No se usa ImageGen ni evidencia ficticia.

La comparación de formatos usa vecino de vértice más cercano en ambos sentidos, sin muestreo. Un máximo distinto de cero no implica automáticamente agujero o superficie distinta: puede haber teselación diferente. Tampoco una nube equivalente demuestra UV/topología/materiales iguales. Se separa esta prueba de la verificación exacta de las escenas guardadas.

Las escenas de revisión incluyen geometría completa e inventario como texto Blender; no tienen dependencias geométricas enlazadas a los originales. Los paquetes de fuentes opcionales preservan los recursos usados para reproducir las variantes. Los ZIP no incluyen el `.max` original; su conversión Blender y el registro SHA permanecen disponibles.
''')
catalog=[]
for o in read('DATOS/coleccion_auditoria.json')['objects']:
 selected=[x for x in rows if x['objects']==[o['object']]];catalog.append([o['object'],o['parent'],len(selected),', '.join(x['id'] for x in selected) or 'sin acceso aceptado; revisar función del componente',f'[general](../CAPTURAS/CAT_{o["object"]}_ISO.png) / [sección](../CAPTURAS/CAT_{o["object"]}_CUT.png)'])
put('14_CATALOGO_COBERTURA.md','# VOY-05A — Cobertura de las 83 piezas\n\nCada malla nativa se enumeró y renderizó desde varios puntos de vista; las siete auditorías de formato conservan todos sus objetos y transformaciones. Las piezas sin registro no se omiten: varias son barandillas, techos o estructuras sin paso identificable.\n\n'+table(['Objeto','Padre','Registros','IDs','Vistas'],catalog))
# CSV is regenerated from the final JSON so group IDs cannot diverge.
fields=list(dict.fromkeys(k for x in rows for k in x))
with (R/'DATOS/inventario_puertas_accesos.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x.items()} for x in rows)
(R/'SCRIPTS/requirements.txt').write_text('numpy==2.3.5\nPillow\nscipy==1.18.1\n',encoding='utf8')
(R/'README.md').write_text('''# Voyager — VOY-05A

Auditoría de puertas y accesos, entrega técnica con reservas. No implementa VOY-05B/C/D/E.

Leer [resumen ejecutivo](INFORMES/00_RESUMEN_EJECUTIVO.md), [inventario](INFORMES/02_INVENTARIO_GENERAL_PUERTAS.md), [plan B](INFORMES/11_PLAN_VOY05B.md) y [galería](GALERIA.html). Extraer los ZIP en la misma raíz para conservar los enlaces relativos. Las capturas y escenas son reales de Blender.

La entrega remota se certifica por VOY05A_Drive_Verificacion.json, publicado junto a los ZIP. Conservar las copias locales. Los fuentes y dependencias locales están separados de los paquetes documentales. No se hicieron commits ni cambios en Unreal/Sutherland/CoreRPG.
''',encoding='utf8')
print('Informes',len(list((R/'INFORMES').glob('*.md'))),'CSV',len(rows))
