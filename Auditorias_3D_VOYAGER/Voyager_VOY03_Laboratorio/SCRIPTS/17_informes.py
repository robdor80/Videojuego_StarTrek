from pathlib import Path
import json,csv,textwrap
R=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((R/'DATOS'/n).read_text(encoding='utf8'))
metrics=read('resumen_metricas.json');measure=read('mediciones_finales.json');contrast=read('contraste_VOY03.json');manifest=read('manifest_blender.json');assert metrics['all_passed'] and contrast['all_geometry_matches'] and all(r['certified'] for r in read('apoyo_continuo.json')['results'])
head='**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**\n\n[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)\n\n'
def write(name,title,body):
 (R/name).write_text('# '+title+'\n\n'+head+textwrap.dedent(body).strip()+'\n',encoding='utf8')
def table(rows,cols):return '| '+' | '.join(h for h,k in cols)+' |\n| '+' | '.join('---' for c in cols)+' |\n'+'\n'.join('| '+' | '.join(str(r[k]) for h,k in cols)+' |' for r in rows)
route_rows=[]
for r in metrics['results']:
 if r['height_m']==1.9:route_rows.append(dict(id=r['route'],length=f"{r['path_length_3d_m']:.3f}",samples=r['poses'],result='Superado original · tres alturas · ida/vuelta'))
route_table=table(route_rows,[('Recorrido','id'),('Longitud 3D m','length'),('Poses por altura','samples'),('Resultado geométrico','result')])
stair_rows=[]
for flight in measure['lateral_flights']:
 for i,r in enumerate(flight['risers']):stair_rows.append(dict(side=flight['id'],i=i+1,rise=f"{r['riser_m']*100:.3f}",depth=f"{flight['tread_depth_axis_m']*100:.2f}",source=r['from_object']+' → '+r['to_object']))
step_table=table(stair_rows,[('Tramo','side'),('Ascenso','i'),('Contrahuella cm','rise'),('Huella de referencia cm','depth'),('Apoyos OBJ','source')])
write('00_RESUMEN_EJECUTIVO.md','VOY-03 — Resumen ejecutivo',f'''
## Cierre: COMPLETADA

Los recorridos geométricos objetivo están validados sobre la geometría original **de trabajo de VOY-02**, sin reparación arquitectónica. Opción A recomendada. Se ha conservado la orientación de importación +90° X y la escala experimental 1,10. «Original de trabajo» incluye las puertas en su pose estática abierta y los adaptadores experimentales existentes de VOY-02; no significa OBJ sin preparar ni versión definitiva para producción.

Hay **39 casos finales positivos**: 13 trayectorias × alturas 1,60 / 1,75 / 1,90 m, radio constante 0,35 m. Incluyen las seis rutas exigidas, tres vuelos de escalera, los dos recorridos completos y dos regresiones. Se verificaron {metrics['pose_samples_total']:,} poses y {metrics['swept_intervals_total']:,} intervalos barridos. Los recorridos inversos comparten el mismo volumen barrido y apoyo con criterio simétrico de subida/bajada; no se cuentan como otros 39 experimentos independientes.

## Respuestas a los diez criterios de cierre

1. **Causa de la desconexión:** el algoritmo anterior mantenía el pie de la cápsula sobre el suelo bajo su centro, sin resolver su paso por narices y contrahuellas. La selección de suelos por material omitía apoyos reales y admitía una consola. La rejilla y las diagonales añadían falsos bloqueos y un cruce real. No había prueba de imposibilidad física del puente.
2. **Geometría original transitable:** sí, en los recorridos y poses documentados. No se han movido, borrado ni reconstruido piezas. No se certifica cada punto de la planta.
3. **Superficies problemáticas:** las escaleras son compuestas; marcos, rejillas y remates no están todos en una sola malla. Hay normales invertidas, bordes abiertos y coincidencias que exigen colisiones futuras cuidadosas. Las escaleras laterales ofrecen tres ascensos de aproximadamente 15,20 cm y huellas de 24,3–24,5 cm, no un salto directo de 30–45 cm.
4. **Tres alturas y continuidad:** sí. Cápsula completa contra mallas, barridos de intervalos y apoyo continuo sobre triángulos reales. El peor cambio vertical entre muestras de la ruta centro–pasarela es aproximadamente 1,27 cm, conectado por un segmento probado; no hay teleportación.
5. **Solución que funciona:** opción A, interpretación física de apoyos y búsqueda con rechazo de aristas incorrectas. Se conservan candidatos fallidos, incluido un atajo de esquina con apoyo lateral inválido.
6. **Mejor conservación visual:** opción A; diferencia de arquitectura y transformaciones respecto a referencia = cero. B–E no se ejecutaron porque A cumplió los objetivos.
7. **Centro a turbolift y camarote:** sí, aproximadamente 31,54 m y 35,54 m, tres alturas, conexión y adaptadores existentes reutilizados. Puertas estáticamente abiertas; sus mecanismos siguen fuera del alcance.
8. **Regresiones de VOY-02:** los dos itinerarios de pasarela/red posterior a sus destinos vuelven a superar los ensayos geométricos para las tres alturas.
9. **Pendiente en Unreal:** colisiones importadas, CharacterMovement real, subir/bajar, giro con cuerpo/animación, contactos de narices, puertas dinámicas y NavMesh. No se ha abierto Unreal ni se declara validación en el motor.
10. **Paso a VOY-04:** la circulación geométrica del alcance está suficientemente resuelta para planificar la siguiente fase. La escala sigue provisional y la naturalidad de marcha requiere personaje y movimiento reales. VOY-04 no se ha iniciado y requiere autorización.

## Límites que acompañan al aprobado

Se acredita viabilidad geométrica de una cápsula ambulante, no simulación biomecánica, certificación normativa, accesibilidad en silla de ruedas ni funcionamiento de asientos. Las rutas de mando terminan cerca de los sillones y navegación en un acceso junto al asiento, no sentadas. Las trayectorias son polilíneas verificables, no animaciones terminadas ni caminos optimizados. La separación de unos 4 mm de las mallas es una tolerancia de contacto geométrico; la futura colisión debe contrastarse de nuevo.

El archivo Blender final contiene cuatro escenas y comparte las 645 piezas de referencia. Se reabrió y contrastó: máximo residual numérico {max(r['error_m'] for r in contrast['objects'])*1e6:.3f} µm con tolerancia explícita de 20 µm; las huellas de vértices, caras y matrices coinciden exactamente con las copias de origen. La integridad protegida final se detalla en `DATOS/integridad_final.json`.

Entregables: nueve informes, escenas en `ESCENAS/VOY03_Circulacion.blend`, datos completos, scripts, registros, capturas originales y finales, láminas y ZIP verificado. Véase [README](README.md).
''')
write('01_DIAGNOSTICO_CIRCULACION.md','VOY-03 — Diagnóstico de circulación','''
## Evidencia que explica VOY-02

Se consultaron los nueve informes de continuidad, los datos prioritarios de acceso central, secciones y rutas, el prototipo numérico y las escenas existentes. El archivo fuente completo se copió con SHA-256 coincidente antes de intervenir en VOY-03. VOY-02 conserva intactos informes, errores y resultados.

El grafo de 10 cm de VOY-02 no implementaba un ascenso de escalones. Una cápsula con su base a suelo +2 mm encuentra la cara vertical y el vuelo de la nariz antes de poder colocar su centro sobre la siguiente huella. Que dos nodos acepten alturas distintas no proporciona una trayectoria entre ambos. Refinar la misma regla a 1 cm sigue produciendo bloqueos: el control negativo arroja 177 muestras bloqueadas en la primera ruta candidata centro–pasarela, 102 centro–navegación y 312 navegación–pasarela. Son controles sobre las candidatas iniciales, conservados en `comparacion_algoritmos.json`, no conteos de la ruta final.

También fallaba la interpretación semántica: Voygray no es una definición de «suelo». Las rejillas Mesh_2121–2124, el relleno Mesh_1968, su placa Mesh_1848 y remates Mesh_1739/1740/1755/1807–1811 participan físicamente en el paso. Mesh_1787 y Mesh_1788 pertenecen al frente de consola: se excluyen como suelo, pero siguen presentes como obstáculos. Mesh_1856 contiene muchos marcos/narices, no toda la escalera visible.

## Piezas, niveles y obstáculos

`mediciones_finales.json` inventaría los objetos críticos con límites, caras, niveles, normales y topología; `topografia_objetos.json` amplía el inventario. Todas las coordenadas de estos datos son metros del marco A del puente: importación corregida +90° X, escala 1,10. El Blender ensamblado usa A + T, T = (-1,310244095; -7,020256090; -0,783525112) m. Las matrices completas por pieza están en `manifest_blender.json`.

Las escaleras laterales son oblicuas. Se midieron sobre sus ejes, no mediante una sección X arbitraria: derecha aproximadamente (-0,652907; +0,757438), izquierda (+0,653454; +0,756966). Los perfiles anteriores en X fijo podían pasar fuera del vuelo útil. Los niveles absolutos principales son 0,023326 / 0,327403 / 0,479442 / 0,631488 / 0,783525 m. Hay bajadas y subidas intermedias; no basta restar extremos.

Las barandillas y consolas permanecen en las pruebas. Un enlace diagonal inicialmente libre en sus extremos atraviesa Mesh_2096 cerca de (-2,6933; -1,5933); se rechaza y busca otro enlace. No se quitó la pieza. Se encontró además un candidato que cortaba la esquina de la escalera derecha: sus extremos estaban libres, pero el intervalo 364 pasaba a un apoyo prácticamente horizontal sobre una contrahuella. Se conserva en `barridos_A1_sin_apoyo_continuo.json` y `apoyo_A0_esquina_negativa.json`. La ruta definitiva lo evita con apoyo de componente vertical ≥0,50.

## Incidencias del comprobador nuevo

Un triángulo decorativo diminuto de Mesh_1944 produjo una falsa intersección: la tolerancia absoluta de los productos de borde tenía unidades m⁴ y dominaba su área. Se normalizó por el área al cuadrado; se añadieron controles de interior/exterior a escalas 0,001 / 1 / 1000 y el triángulo real como regresión. Se conservan versión y resultados anteriores.

El rayo BVH de precisión simple fallaba exactamente en Y=8,420256090 m, unión AD_PUENTE/PASILLO_PRINCIPAL. Los límites de ambas superficies coinciden: hueco medido 0 m. El respaldo en doble precisión intersecta los mismos triángulos, sin desplazar puntos ni extender el suelo. A ±1 µm el BVH encontraba ambos lados. No se añadió ninguna colisión invisible ni puente virtual.

## Resultado

La falta de conexión anterior no demostraba una ausencia de escalera ni una imposibilidad del modelo. La prueba nueva conserva todos los obstáculos y exige apoyo durante el desplazamiento. La opción A encuentra rutas válidas. Las restricciones que siguen pendientes pertenecen al movimiento real, a las colisiones futuras y al uso de puestos, no a un bloqueo geométrico restante de las rutas objetivo.

Visuales: [planta y rutas](LAMINAS/02_planta_soportes_y_rutas.png), [atajo negativo y ruta final](LAMINAS/05_atajo_descartado_y_ruta_final.png), [escalera real](CAPTURAS/B03_escalera_derecha_apoyo.png).
''')
write('02_ESCALONES_Y_DESNIVELES.md','VOY-03 — Escalones y desniveles',f'''
## Perfiles laterales completos

{step_table}

Cada lateral enlaza anillo frontal 0,327403 m → primer apoyo 0,479442 m → segundo 0,631488 m → pasarela 0,783525 m. Los dos peldaños intermedios más la plataforma superior proporcionan tres contrahuellas reconocibles. La profundidad de tabla es la distancia entre centros geométricos de las huellas sobre el eje; las transiciones del perfil a 2 mm corroboran aproximadamente 24,4 / 24,2 cm a la derecha y 24,4 / 24,6 cm a la izquierda. La incertidumbre de localización del borde del perfil es del orden de su muestreo; los objetos y límites precisos se conservan en JSON.

Orígenes del perfil: derecha (4,001830; 0,045579; 0,479442), izquierda (-3,993118; 0,047012; 0,479442). Recorrido diagnóstico de cada vuelo: u=-0,85 → +0,70 m. Perfil de medición: u=-0,60 → +0,70 m, muestras de 2 mm. Sus inicios/finales son apoyos reales, no anclas flotantes.

## Anchura y espacio libre

Las secciones transversales con cápsula de radio 35 cm dan, en la primera huella, un intervalo continuo de centros de 40 cm derecha y 34 cm izquierda, equivalente a una banda ocupada por cápsulas de aproximadamente 1,10 y 1,04 m. En la segunda huella la banda es aproximadamente 1,15 m. Son medidas de sección con rejilla lateral de 1 cm; no se presentan como anchura constante de toda la escalera ni margen libre universal. Los barridos completos son la prueba decisiva de paso.

Altura libre mínima de rayo vertical sobre el eje ensayado: 2,523 m en ambos laterales, contexto arquitectónico completo. Se muestrearon 23 posiciones por vuelo; la cápsula 1,90 m se contrastó además con todas las mallas durante su desplazamiento, incluida cabeza y hombros. Las barandillas, consolas y remates no se suprimieron.

## Navegación y plataforma central

La sección X=0, Y=-3,00 → -1,20 m muestra tres cambios nominales de 15,20 cm desde el foso 0,023326 m hasta el centro 0,479442 m. Marcos/narices en aproximadamente 0,175364 y 0,327403 m, rellenos Mesh_2121 y Mesh_2122 a 0,169515 y 0,321553 m. La diferencia marco–relleno es unos 5,85 mm; las fluctuaciones del perfil son reales y se mantuvieron. Los apoyos nominales empiezan cerca de Y=-2,312 / -2,050 / -1,776 m; huellas centrales aproximadas 26,2 y 27,4 cm, medidas en esa sección.

Mesh_2123/2124 son las rejillas laterales de navegación. El acceso final a navegación se fija en (-0,80; -2,90), sobre el foso real junto al asiento. No se usa el antiguo destino (0; -4,84), situado en el anillo exterior frontal, ni una posición encima de la silla. La prueba separada de la escalera central baja por X=0, Y=-1,50 → -2,50; no pretende llegar al asiento ni atravesar la consola.

Los saltos aparentes de 30,4 / 45,6 cm son diferencias acumuladas de niveles. El laboratorio no autoriza superar esas alturas de un solo paso. Hipótesis de movimiento: cambio de suelo consecutivo máximo 18 cm; cada contrahuella real medida queda por debajo. El volumen redondeado de cápsula anticipa el siguiente peldaño y puede elevar su punto inferior sobre el suelo bajo su centro; esa separación no es un salto ni un pie humano. Se exige contacto inferior real y componente vertical de apoyo, y se conserva la trayectoria completa.

## Continuidad, solapes, normales y triangulación

Las escaleras ensayadas disponen de apoyo continuo de cápsula en triángulos existentes. No se ha demostrado que toda la malla sea un sólido cerrado. El recuento con soldadura virtual a 1 µm detecta en Mesh_1856 seis triángulos coincidentes adicionales, 6129 bordes de una cara y numerosas caras horizontales orientadas hacia abajo. Las rejillas y varias huellas izquierdas también tienen normales descendentes. Estos conteos no equivalen automáticamente a defectos que deban borrarse: el modelo contiene paneles, rellenos y remates independientes.

El ensayo geométrico trata las caras por sus dos lados y conserva coincidencias. La preparación UE deberá revisar normales y colisiones por pieza, sin convertir consolas en suelo ni cerrar huecos deliberados. Los recuentos de bordes dependen del redondeo geométrico a 1 µm y no sustituyen una reparación de topología. No se ejecutó ninguna reparación automática.

Evidencias: [sección derecha](LAMINAS/03_seccion_derecha.png), [izquierda](LAMINAS/03_seccion_izquierda.png), [navegación](LAMINAS/04_seccion_navegacion.png), `DATOS/escalones_medidos.csv`, `DATOS/mediciones_finales.json` y `DATOS/perfiles_escaleras.json`.
''')
write('03_PRUEBAS_CAPSULAS.md','VOY-03 — Pruebas de cápsulas',f'''
## Protocolo y resultados

Alturas totales 1,60 / 1,75 / 1,90 m, radio invariable 0,35 m, eje vertical. Semiesferas y segmento central se calculan analíticamente; los polígonos de las cápsulas Blender son solo representación visual. No se redujo el radio ni se cambió silenciosamente el cuerpo. Se ejecutaron los 39 casos, con {metrics['pose_samples_total']} poses y {metrics['swept_intervals_total']} intervalos. El contador suma los tres tamaños; las huellas de apoyo coinciden entre tamaños y esa igualdad se verifica.

{route_table}

Todos los casos finales: **Superado sobre geometría original de trabajo**. No hay rutas que dependan de adaptación. Los resultados negativos de versiones anteriores siguen presentes y su clasificación provisional no debe confundirse con el estado final.

## Qué se comprueba entre poses

La búsqueda de rejilla de 10 cm solo propone candidatos. Se refinan a separación XY máxima 1 cm; los extremos solicitados se conservan expresamente. Cada intervalo lineal se comprueba como un volumen continuo: el segmento central vertical de la cápsula barre un cuadrilátero, cuya distancia exacta a cada triángulo próximo se calcula con vértices, aristas e intersecciones de caras. Se resta el radio 0,35 m. No se acepta un enlace solo porque sus dos poses estén libres.

Umbrales de barrido: 0,5 mm respecto a terreno y 3 mm respecto a otros obstáculos; selección de poses con separación 4 mm del terreno y umbrales de 1 / 5 mm. El mínimo final de todos los casos es aproximadamente 3,90 mm, principalmente próximo al suelo. Los 20 µm de contraste guardado quedan por debajo de esos márgenes, pero la prueba no garantiza tolerancia a futuras simplificaciones de colisión.

Para acreditar apoyo continuo se identifica, en cada intervalo, al menos un triángulo real situado al menos 0,179 m por debajo de ambos centros de la esfera inferior. Ambos extremos están a distancia ≤0,358 m del mismo triángulo. La distancia a un triángulo convexo es convexa a lo largo del segmento: todo el intervalo queda a ≤radio+8 mm, con componente vertical de contacto ≥0,50. El barrido impone simultáneamente que no hay penetración. No se crea una superficie entre triángulos. Todos los intervalos finales satisfacen el certificado sin subdivisión adicional.

El espacio de giro de una cápsula circular no cambia con el yaw; en las posiciones y trayectorias validadas su giro axial conserva el volumen libre. No se certifican brazos extendidos, locomoción de cuerpo articulado, adelantamiento de dos personajes ni giro de silla de ruedas.

## Ida y vuelta

Invertir una polilínea reproduce exactamente el mismo conjunto de cápsulas, obstáculos y apoyos. Se conserva el orden inverso y se aplica la misma cota absoluta de 18 cm para subida y bajada. Así se acredita la reversibilidad geométrica bajo esta hipótesis simétrica. No se ha ejecutado una simulación dinámica independiente de descenso; la futura gravedad, velocidad y resolución de contactos del motor pueden diferir.

Datos: `resultados_rutas.csv`, `rutas_puntos.csv`, `barridos_resultados.json`, `apoyo_continuo.json`. Los resultados contienen todos los puntos inferiores de cápsula y los niveles de suelo. [Comparativa de tres alturas](LAMINAS/06_tres_alturas.png).
''')
write('04_SOLUCIONES_EXPERIMENTALES.md','VOY-03 — Soluciones experimentales','''
## Alternativa recomendada: A, sin modificar geometría

El problema original era una prueba incapaz de resolver los apoyos compuestos de la escalera, no la ausencia demostrada de una conexión. La modificación experimental afecta al comprobador y a la trayectoria candidata: inventario por función real de pieza, envolvente inferior de cápsula, rechazo de contactos laterales, rechazo de diagonales y barrido completo. Objetos arquitectónicos modificados: ninguno. Diferencia de vértices, caras y matrices respecto a las copias de referencia: cero. No hay cambios globales de escala.

El archivo final comparte los mismos 645 componentes en referencia, diagnóstico, experimento A y recorrido completo. Las curvas, cámaras y cápsulas añadidas son auxiliares y no participan en colisiones. Se omitieron de la selección física 24 piezas de torso/pelvis/piernas de los antiguos maniquíes diagnósticos VOY-02: eran ayudas de representación, no mobiliario ni arquitectura. Los tres muebles de referencia del camarote sí se conservan y se contrastan como obstáculos, igual que sus datos numéricos.

## Comparativa de opciones, en el orden solicitado

| Opción | ¿Ejecutada? | Resultado | Consecuencia visual / traslado futuro |
| --- | --- | --- | --- |
| A · geometría existente | Sí | Todas las rutas objetivo superadas | Conserva arquitectura; necesita colisión y movimiento real posteriores |
| B · ajuste menor de piezas | No necesaria | No ensayada; no se atribuye un aprobado | Evitar cambios sin defecto geométrico demostrado |
| C · reconstruir peldaños | No necesaria | No ensayada | Las huellas reales ya resuelven el itinerario |
| D · adaptador nuevo | No necesaria | No ensayada | No se añade rampa, piso invisible ni nueva transición |
| E · circulación alternativa | No necesaria como solución arquitectónica | No ensayada | La ruta usa accesos y escaleras existentes; el replanteo local de búsqueda no es una reforma |

El conjunto sí reutiliza adaptadores de VOY-02, incluido AD_PUENTE revisado R1. Eso es el estado de referencia, no una adaptación creada en VOY-03. La opción A se refiere a no cambiar ese estado de trabajo.

## Ensayos rechazados y correcciones

1. Primer inventario incompleto de apoyos: no conectaba el grafo. Se preserva `busqueda_original_A0_sin_narices.json`.
2. Inventario con narices laterales pero remates centrales incompletos: diagnóstico intermedio conservado en `busqueda_original_A1_sin_1810_1811.json`.
3. Diagonal junto a Mesh_2096: libre en nodos y bloqueada entre ellos. Se conserva la coordenada y se prohíbe la arista en el grafo.
4. Barrido con tolerancia absoluta incorrecta: falso Mesh_1944 y fallo BVH en una arista compartida. Versiones antiguas en REFERENCIAS y resultados negativos en `barridos_A0_errores_numericos.json`. No se corrigió moviendo una pieza.
5. Candidato de esquina: el barrido libre no garantizaba apoyo vertical; se descarta tras certificado continuo. Se preservan `rutas_A2_atajo_esquina.json`, `barridos_A1_sin_apoyo_continuo.json` y `apoyo_A0_esquina_negativa.json`.
6. Ruta final: componente vertical de apoyo ≥0,50 y todos los intervalos certificados sobre triángulos reales. Los cambios y decisiones están en `incidencias.json`, `soluciones.json` y `cambios_experimentales.json`.

No se borraron coincidencias, consolas o barandillas. Los recortes de techo/pared para capturas se realizaron después de guardar, en copias temporales en memoria; todos los ensayos usan la geometría completa. No existe suelo invisible de ensayo ni definitivo.

[Antes/después de trayectoria](LAMINAS/05_atajo_descartado_y_ruta_final.png) · [Comparativa de la misma escalera](LAMINAS/07_comparativa_sin_reparacion.png).
''')
write('05_RECORRIDOS_COMPLETOS.md','VOY-03 — Recorridos completos',f'''
## Centro → pasarela → salida → red existente

Se conserva la secuencia de VOY-02 desde su pasarela posterior y se antepone el tramo central ahora validado. Las matrices de módulos, adaptadores R1, puertas abiertas y muebles de referencia se reutilizan. No se reconstruyó la red ni se alteraron uniones para obtener los resultados.

Centro → escalera lateral derecha → pasarela posterior → salida posterior → AD_PUENTE → pasillo principal → cruce y ramal existente → acceso y cabina de turbolift: **superado**, aproximadamente 31,542 m de trayectoria de cápsula.

Centro → misma conexión posterior → pasillos y adaptadores existentes → camarote de referencia: **superado**, aproximadamente 35,544 m. El destino es una posición de llegada dentro del camarote; no acredita uso de cama, escritorio o almacenamiento.

Cada uno se ejecutó para 1,60 / 1,75 / 1,90 m y radio 0,35 m, con barrido completo y apoyo continuo. Las longitudes corresponden a polilíneas ensayadas y al ascenso de la cápsula; no son distancias mínimas arquitectónicas.

## Regresión y compatibilidad

Se repiten los tramos originalmente validados por VOY-02: 23,212 m hacia turbolift y 27,214 m hacia camarote, tres alturas. Todos pasan. No se modificó la geometría ni las transformaciones que soportaban aquellos resultados. El fallo numérico en la arista AD_PUENTE/PASILLO_PRINCIPAL se resolvió intersectando los mismos triángulos en doble precisión, conservando el diagnóstico anterior.

El prototipo de prueba contiene los 630 objetos del puente OBJ, seis módulos existentes, seis adaptadores y tres muebles de referencia: **645 componentes numéricos**. El contraste del Blender guardado comprueba todos ellos, no solo los suelos. El resto de auxiliares visibles son trayectorias/cápsulas/cámaras identificadas y no actúan como arquitectura.

## Referencias espaciales y extremos

En marco A: centro (0; -0,77), navegación (-0,80; -2,90), mando izquierdo (-1,43; -0,22), mando derecho (1,43; -0,22), pasarela (3,96; 2,97), posterior (1,3101; 6,688). Coordenadas XY, metros; Z se resuelve sobre apoyos reales. El enlace inicial al grafo se refina y comprueba; no se acepta por desplazamiento silencioso al nodo más próximo.

El marco G guardado coloca la salida posterior cerca del origen de ensamblaje; convertir A→G sumando T=(-1,310244095; -7,020256090; -0,783525112). Los recorridos numéricos de módulos de VOY-02 ya estaban en G, por lo que para probar junto al puente A se resta T. El JSON registra ambos marcos y las matrices exactas; no aplicar escala 1,10 otra vez a los módulos.

## Límites de uso

Puertas en pose abierta estática. No se ensayan sus carreras, bolsillos, permisos, ocupantes ni bloqueos dinámicos. No hay transporte funcional de turbolift ni NPC. Los adaptadores y muebles verdes/naranjas siguen siendo recursos de laboratorio heredados, no restauración final. La prueba inversa es geométrica simétrica, no CharacterMovement en descenso.

Evidencia: [planta completa](CAPTURAS/B07_red_completa_planta.png), [vista general](CAPTURAS/B08_red_completa_axonometrica.png), [encuentro posterior](CAPTURAS/B09_union_posterior.png), escena `04_RECORRIDOS_COMPLETOS`, CSV de rutas y todos los intervalos en JSON.
''')
write('06_PREPARACION_UE5.md','VOY-03 — Preparación técnica para UE5','''
## Estado de esta fase

1. **Prueba geométrica en Blender:** superada para las rutas y cápsulas documentadas.
2. **Viabilidad estimada en Unreal:** favorable si la importación conserva la arquitectura y las colisiones representan los apoyos reales; todavía estimación.
3. **Validación real en Unreal:** pendiente. No se abrió ni modificó Unreal Engine 5.8.2, ningún proyecto UE ni CoreRPG.

## Colisiones propuestas por tipo de pieza

| Piezas / función | Preparación futura propuesta | Condición de contraste |
| --- | --- | --- |
| Mesh_1728 foso; floorfront_1 anillo; Mesh_1857 centro; Mesh_1859 pasarela | Colisiones simples separadas por regiones cóncavas y niveles, espesor constructivo local | No cubrir el foso, escaleras, vanos ni huecos con un único convexo general |
| Mesh_1860–1863 huellas laterales | Prismas ajustados a cada huella y contrahuella; conservar alturas y profundidad | Repetir las rutas incluyendo aproximación a barandillas y narices |
| Mesh_1856 marcos; Mesh_1739/1740/1755/1807–1811 remates | Separar función de apoyo y detalles salientes, manteniendo el volumen visual real | No suprimir la nariz que producía contacto; no inventar una rampa sobre un hueco |
| Mesh_2121–2124 rejillas; Mesh_1968 /1848 relleno y placa | Reconstruir colisión según la superficie realmente existente y su soporte; revisar normales | No rellenar huecos no medidos ni duplicar planos para simular suelo |
| Mesh_1787/1788 y demás consolas | Colisión de obstáculo por panel/volumen, sin rol de suelo transitable | Conservar espacio de rodillas y separación real; no convertir tapas en rutas |
| Barandillas y montantes | Convexos o prismas estrechos por elemento importante | Validar hombros, barrido lateral y giro, sin cerrar el paso con un bloque global |
| Módulos de pasillo y AD_* existentes | Suelo, pared, techo y marco separados; reutilizar matrices R1 | Repetir ambos itinerarios completos y la unión exacta posterior |
| Hojas de puerta | Pivote/raíz local por hoja completa y grupo móvil | Fase posterior de carrera y alojamiento; abierto estático no equivale a mecanismo válido |
| Sillas y muebles | Mantener bases fijas y grupos móviles identificados por el trabajo previo | Aproximación validada no significa asiento usable; pivotes/interacción siguen pendientes |

Las normales hacia abajo de varias huellas y rejillas deben revisarse antes de depender de superficies de una cara. No se voltearon ahora. Una colisión simple puede diferir del detalle visible en pocos milímetros y consumir el margen ensayado; comparar de nuevo el modelo de colisión con las secciones de VOY-03. Una simplificación no debe crear apoyos donde no los hay.

## Parámetros de referencia para un futuro laboratorio autorizado

Metros Blender y conversión explícita a centímetros de motor. Radio 35 cm; alturas totales 160 /175 /190 cm; semialturas 80 /87,5 /95 cm. Conservar referencia 1,10 aplicada al puente y matrices de módulos existentes; no duplicar conversiones de escala.

Contrahuella de laboratorio máxima 18 cm, frente a las medidas nominales 15,20 cm. Es una hipótesis de capacidad ambulante para comparar, no un valor configurado o certificado de CharacterMovement. Probar primero ese límite con el personaje y colisión reales; no empezar permitiendo 30–45 cm para ocultar un fallo. Pendiente a estudiar posteriormente: 40° como hipótesis de comparación; las huellas de esta fase son casi horizontales y no se ensayó una rampa de 40°. La inclinación media de la línea de escaleras no sustituye la medición de sus peldaños.

En VOY-03 se exigieron planos de apoyo casi horizontales (|normal Z|>0,999, unos 2,56°), cambios de suelo ≤18 cm, apoyo inferior real y barridos de cápsula. Ese algoritmo no reproduce gravedad, aceleración, fricción, velocidad, ajuste del pie ni el algoritmo de subida del motor. El desplazamiento vertical de una cápsula redondeada sobre narices tampoco es una animación de pies humanos.

## NavMesh y aceptación futura

Comprobar generación de regiones en foso de navegación, ambos vuelos laterales, plataforma central, entorno de sillones, pasarela y salida posterior, además de cada adaptador y ambos destinos. Contrastar radio, altura y escalón del agente con los tres cuerpos de referencia. Revisar todas las transiciones y áreas de puerta abiertas/cerradas; un enlace especial no debe ocultar falta de suelo.

El futuro criterio de aceptación debe repetir subida y bajada con personaje real, varias velocidades y aproximaciones, detención en huellas, colisión de cabeza/hombros, giro y retorno. Conservar negativos y comparar con los puntos de VOY-03. No se exportaron activos ni se implementó nada de esto durante esta misión.
''')
write('07_RECOMENDACIONES_FUTURAS.md','VOY-03 — Recomendaciones futuras','''
## Decisión recomendada

Conservar la arquitectura de los escalones. La opción A satisface la circulación geométrica del alcance con cero cambios de malla o posición. No hay fundamento en estos ensayos para rehacer el suelo completo, ampliar el puente, reducir la cápsula, eliminar barandillas o sustituir definitivamente la escalera por una rampa.

Mantener 1,10 como escala experimental documentada. Antes de decidir una escala final, contrastar el personaje, el uso de los puestos y las colisiones en una fase posterior autorizada. No utilizar el aprobado geométrico para dar por resuelta la ergonomía sentada de navegación o mando.

## Orden útil para una fase siguiente, sin iniciarla

1. Revisar conjuntamente las láminas y las escenas. Aceptar o ajustar los criterios de personaje, fidelidad y locomoción.
2. Preparar colisiones por función de pieza en una copia independiente, conservando los apoyos medidos y las narices. Revisar normales y no borrar coincidencias sin determinar su función.
3. Cuando se autorice un laboratorio UE, importar una muestra y repetir con CharacterMovement y colisión reales todas las rutas, subida y bajada. Dar prioridad a las aproximaciones oblicuas y al atajo negativo de esquina, que debe seguir rechazado.
4. Verificar acceso al asiento y postura sentada por separado, después puertas completas con alojamiento y ocupación. Esas tareas no se convirtieron en parte de VOY-03.
5. Solo después decidir restauración visual, interacciones/NPC y optimización basadas en pruebas de motor.

## Riesgos y asuntos secundarios anotados

Las huellas son compuestas y algunas caras apuntan hacia abajo. El detalle de rejilla y marco difiere 5,85 mm; el margen de colisión de la cápsula es milimétrico. Una colisión simplificada puede producir una regresión aunque parezca igual en pantalla. Las polilíneas verificadas no están suavizadas para animación ni circulación de múltiples agentes.

Persisten asuntos heredados fuera del alcance: ergonomía completa de puestos, carreras y bolsillos de puertas, uso real del camarote, materiales/PBR, parámetros de rendimiento e integración RPG. VOY-03 no los declara corregidos. Las puertas abiertas de la red son solo condiciones estáticas de estos ensayos.

La circulación ambulante medida no proporciona acceso sin escalones. La misión no evaluó silla de ruedas, cuerpo con equipamiento voluminoso, combate, evacuación ni cumplimiento normativo. Cualquier nuevo cuerpo o cambio de radio exige un experimento identificado, no sustituir esta referencia.

## Criterio para avanzar

**Sí hay base geométrica suficiente para planificar VOY-04**: seis rutas objetivo y conexiones completas resueltas sin alterar la identidad visual. Esto no es autorización ni ejecución de VOY-04. La misión se detiene al entregar el laboratorio y su ZIP; no hay integración Unreal, commit, PR, publicación ni inicio de la siguiente fase.
''')
write('08_METODOLOGIA_Y_LIMITACIONES.md','VOY-03 — Metodología, trazabilidad y límites',f'''
## Entradas, aislamiento y conservación

Laboratorio anterior: `{R.parent / 'Voyager_VOY02_Laboratorio'}`. Laboratorio nuevo: `{R}`. Se leen copias de datos geométricos y la referencia Blender, nunca se guarda sobre VOY-02. La toma inicial SHA-256 incluye **2762 archivos protegidos**: VOY-01, todo VOY-02 y los 115 originales registrados por la fase anterior. También se registran hashes de las 27 copias iniciales de referencia y, por separado, diez capturas de continuidad copiadas para revisión. Las 33 capturas originales siguen intactas en VOY-02. `baseline_protegido.json` es inmutable; la comprobación final genera otro archivo, no reemplaza el estado inicial.

No se realizaron operaciones sobre Sutherland, proyectos Unreal, CoreRPG ni otros proyectos. No se ejecutó Git, se crearon commits/PR, se accedió a GitHub ni se hicieron publicaciones. No se instaló software. La prueba de hashes cubre los conjuntos registrados; no se presenta como un hash global de todos los discos del MSI.

## Procedimiento reproducible

`01_topografia.py` reconstruye coordenadas físicas desde la importación OBJ numérica de VOY-02, aplica solo la escala de referencia y las poses abiertas completas de las puertas. `walkgeom.py` clasifica apoyos por función explícita y conserva el resto como obstáculos. El BVH busca superficies horizontales por ambos lados; si falla en una arista coincidente, se intersectan esos mismos triángulos en doble precisión.

`04_busqueda_original.py` propone una rejilla de 10 cm. `06_replanificar_aristas.py` vuelve a comprobar nodos con apoyo vertical, usa cambios de suelo ≤18 cm y rechaza enlaces cuyo refinamiento a 1 cm colisione o pierda apoyo. No se presenta la mera resolución del grafo como un aprobado físico. `07_barridos_y_recorridos.py` comprueba cada tamaño de cápsula contra mallas completas y los intervalos de traslación. `09_apoyo_intervalos.py` exige apoyo continuo por convexidad sobre triángulos reales; su certificado final incluye componente vertical ≥0,50 y cota de separación ≤8 mm. `14_datos_y_exportacion.py` exige ambos resultados antes de producir tablas finales.

`10_mediciones.py` mide perfiles y secciones transversales, conserva límites y anomalías de topología. `11_comparacion_algoritmos.py` reproduce el control negativo del pie fijo sobre las primeras candidatas. `12_laboratorio_blender.py` crea cuatro escenas compartiendo los 645 componentes físicos; las viejas 24 piezas de maniquí se identifican como auxiliares y no se incorporan a la arquitectura. `16_contraste_guardado.py` reabre el archivo final, contrasta todos los componentes contra los triángulos del prototipo y comprueba sus huellas geométricas y matrices.

El contraste admite 20 µm por cancelación de precisión simple en módulos con coordenadas nativas alejadas del origen; máximo observado **{max(r['error_m'] for r in contrast['objects'])*1e6:.3f} µm**. No se cambió una pieza para borrar ese residual. Se comprueba además igualdad exacta de vértices/caras/matrices con las copias de origen y que el archivo no cambió durante la verificación.

## Errores y resultados negativos conservados

Los scripts y resultados intermedios registran inventario incompleto, arista diagonal bloqueada, tolerancia de triángulo errónea, fallo BVH y candidato con apoyo lateral. Los informes finales distinguen esos diagnósticos del resultado definitivo. Las primeras capturas B se conservan en `CAPTURAS/REVISION_A1_NO_VALIDADA`; algunas estaban recortadas u ocluidas y sus rutas no tenían certificado de apoyo. No son evidencia de aprobación. Las nuevas plantas usan límites de cámara medidos, y los detalles de cápsula se reencuadraron. El montaje QA inicial también se conserva.

El primer lanzamiento de depuración tuvo una ruta mal escrita y no ejecutó el script; se corrigió la ruta. El registro `05_perfiles_y_bloqueos.log` conserva un error de sintaxis de la primera versión, corregido antes de medir. Un código de salida cero de Blender no se usa como criterio único: se revisan los JSON, el número de casos, las métricas, imágenes y el contraste guardado.

## Qué significa el resultado

Se demuestra existencia de una trayectoria continua de cápsula con apoyo geométrico y sin intersecciones dentro de las tolerancias declaradas. No se demuestra comportamiento dinámico de un controlador, equilibrio biomecánico, contacto de la planta del pie, animación, confort, velocidad, inercia ni accesibilidad universal. El algoritmo de envolvente inferior permite que la cápsula redondeada suba progresivamente por las narices, sin suponer un salto de nivel. La ruta final mantiene apoyos intermedios y rechaza el atajo que perdía soporte vertical.

La reversibilidad usa identidad del volumen barrido y una hipótesis simétrica de subida/bajada de 18 cm. No es una segunda simulación física. Los obstáculos son caras trianguladas por ambos lados; el futuro motor puede interpretar normales y colisiones de otra manera. La clasificación COMPLETADA se refiere al alcance **geométrico** de VOY-03, no a un puente jugable terminado.

## Reproducción

Usar Blender 5.2.2 LTS en segundo plano con `--background --python RUTA_SCRIPT`. Los scripts resuelven R desde su carpeta SCRIPTS. No volver a ejecutar `00_copias_y_baseline.py` sobre este laboratorio: se detiene si ya existe el baseline. Para una repetición íntegra usar una copia nueva del laboratorio y conservar primero los resultados entregados. No ejecutar los antiguos scripts VOY-02 desde su carpeta.

Orden funcional: 01 → 04 → 05 → 06 → 07 → 09 → 10 → 11 → 14; después 12 → 16 → 15 → 17 → 18 → 19 → 20 → 21. `15_laminas.py` y `17_informes.py` usan Python del sistema con Pillow para las láminas; los demás cálculos geométricos usan NumPy y mathutils de Blender. 18 se ejecuta con Blender; 19–21 con Python del sistema. No precisan instalar paquetes. `02_planta_soportes.py` y 03 son diagnósticos iniciales y no sustituyen las salidas finales. 08 y 13 son reproducciones de errores conservados; sus salidas no deciden el estado final.

Se incluyen NPZ de entrada suficientes para repetir el cálculo sin el blend fuente. La referencia Blender completa queda en REFERENCIAS/VOY02 dentro del laboratorio local, documentada por ruta/hash; la escena final se incluye en el ZIP. Los datos de baseline conservan rutas absolutas del MSI para auditoría local.
''')
files=[('00_RESUMEN_EJECUTIVO.md','Resumen y diez respuestas'),('01_DIAGNOSTICO_CIRCULACION.md','Causas del bloqueo'),('02_ESCALONES_Y_DESNIVELES.md','Perfiles y cotas'),('03_PRUEBAS_CAPSULAS.md','Pruebas por altura'),('04_SOLUCIONES_EXPERIMENTALES.md','Comparación de alternativas'),('05_RECORRIDOS_COMPLETOS.md','Red completa y regresiones'),('06_PREPARACION_UE5.md','Información para pruebas futuras'),('07_RECOMENDACIONES_FUTURAS.md','Próximas decisiones'),('08_METODOLOGIA_Y_LIMITACIONES.md','Método y límites')]
readme='# Voyager VOY-03 — Laboratorio reproducible\n\n**Estado: COMPLETADA · circulación geométrica · opción A sin modificar arquitectura.**\n\n'+head+'\n'.join(f'- [{title}]({name})' for name,title in files)+f'''

## Abrir las escenas

Archivo final: `{R / 'ESCENAS/VOY03_Circulacion.blend'}`. Incluido en el ZIP bajo ESCENAS.

1. `01_REFERENCIA_ORIGINAL`: conjunto físico de referencia VOY-02, puertas abiertas y adaptadores existentes.
2. `02_DIAGNOSTICO`: mismas piezas, perfiles y cápsulas de referencia; ayudas sin colisión.
3. `03_EXPERIMENTO_A_SIN_CAMBIOS`: rutas validadas del puente, arquitectura intacta.
4. `04_RECORRIDOS_COMPLETOS`: centro a turbolift y camarote sobre el ensamblaje existente.

Los 645 objetos físicos se comparten entre escenas para evitar duplicación. No editar su malla en una escena esperando que las demás sean independientes; crear otra copia explícita para una futura modificación. En diagnóstico se muestra por defecto la cápsula de 1,90 m; las de 1,60 y 1,75 están ocultas para evitar superposición y pueden activarse en el Outliner. Referencia original completa de ocho escenas: `{R / 'REFERENCIAS/VOY02/VOY02_Laboratorio.blend'}` (fuera del ZIP para evitar duplicarla; SHA en baseline). Fuente anterior intacta: `{R.parent / 'Voyager_VOY02_Laboratorio/ESCENAS/VOY02_Laboratorio.blend'}`.

## Datos y evidencia

Empezar por [GALERIA.html](GALERIA.html), las láminas y `DATOS/resultados_rutas.csv`. `barridos_resultados.json` conserva todas las poses y fallos finales; `apoyo_continuo.json` acredita soporte entre muestras. NPZ y scripts reproducen las pruebas. `contraste_VOY03.json` verifica el archivo guardado. `baseline_protegido.json` / `integridad_final.json` comparan fuentes antes/después. Los JSON A0/A1/A2 y la carpeta REVISION_A1_NO_VALIDADA son resultados descartados conservados, no aprobados.

Reproducción y orden de scripts en [metodología](08_METODOLOGIA_Y_LIMITACIONES.md). Los scripts 00 y los archivos de cierre son operaciones de auditoría/paquete; no borrar el baseline ni reemplazar las evidencias originales de una repetición.

ZIP: `PAQUETE/VOY03_Entrega.zip`. Incluye informes, datos, NPZ, scripts, registros, capturas, láminas y Blender final. Excluye únicamente la referencia Blender duplicada, cachés Python y el propio directorio PAQUETE. `MANIFIESTO_SHA256.json` dentro del ZIP permite comprobar cada entrada; verificación externa en `PAQUETE/verificacion_zip.json`.

No se abrió Unreal ni se inició VOY-04. No hay commits, PR ni publicaciones. Mantener separadas viabilidad geométrica, estimación para Unreal y validación real en Unreal pendiente.
'''
(R/'README.md').write_text(readme,encoding='utf8')
# Compact semantic collision inventory and explicit future test parameters.
collision=[]
for o in measure['objects']:
 collision.append(dict(object=o['name'],role=o['role'],bounds=o['bounds'],future_collision='obstacle' if 'obstacle' in o['role'] else 'measured support / solid local stair collision; preserve openings',normal_review=any(l['down'] for l in o['levels'])))
(R/'DATOS/preparacion_ue5.json').write_text(json.dumps(dict(executed_in_ue=False,geometry_blender_passed=True,ue_viability='estimated favorable, pending real tests',radius_cm=35,total_heights_cm=[160,175,190],half_heights_cm=[80,87.5,95],step_limit_cm_lab_hypothesis=18,slope_degrees_future_hypothesis=40,objects=collision),indent=2,ensure_ascii=False),encoding='utf8')
with (R/'DATOS/obstaculos_y_superficies.csv').open('w',newline='',encoding='utf-8-sig') as f:
 wr=csv.writer(f);wr.writerow(['object','role','normal_review','min_x_A','min_y_A','min_z_A','max_x_A','max_y_A','max_z_A'])
 for o in collision:wr.writerow([o['object'],o['role'],o['normal_review'],*o['bounds'][0],*o['bounds'][1]])
print('NINE_REPORTS_AND_README_WRITTEN')
