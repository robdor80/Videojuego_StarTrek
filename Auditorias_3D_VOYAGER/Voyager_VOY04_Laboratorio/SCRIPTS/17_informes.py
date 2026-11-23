import json,math,html
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'DATOS'/n).read_text(encoding='utf8'))
inv=load('inventario_medidas.json');erg=load('ergonomia_resultados.json');comp=load('comparacion_puestos.json');verify=load('verificacion_animacion_guardada.json');copies=load('verificacion_copias_blender.json');integrity=load('integridad_final.json');internal=load('contactos_internos_originales.json');bear=load('apoyos_bases.json');components=load('componentes_clasificados.json');screens=load('consola_superficies.json');leg=load('holguras_piernas_consola.json');meta=load('manifest_blender.json')
assert integrity['pass_check'] and not copies['bad'] and all(x['all_sampled_geometry_pass'] for x in verify)
def table(head,rows):return '\n'.join(['| '+' | '.join(head)+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])
def write(name,title,body):
 (R/name).write_text(f'# VOY-04 — {title}\n\n22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.\n\n[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)\n\n'+body.strip()+'\n',encoding='utf8')
heighttable=table(['Altura humana','Descenso del asiento','Asiento sobre suelo de pies','Retirada','Distancia tronco–respaldo','Mirada descendente al centro'],[[f'{r["H"]:.2f} m',f'{r["seat_drop_m"]*100:.2f} cm',f'{r["adapted_seat_height_over_local_foot_floor_m"]*100:.2f} cm','40 cm',f'{r["backrest_min_capsule_gap_m"]*100:.2f} cm',f'{r["look_down_to_center_deg"]:.1f}°'] for r in erg])
write('00_RESUMEN_EJECUTIVO.md','Resumen ejecutivo',f'''
## Cierre: COMPLETADA CON RESERVAS

El laboratorio demuestra un recorrido cinemático **muestreado** de entrada, sentado, trabajo, levantado, salida y retorno de la silla para 1,60 / 1,75 / 1,90 m, en una copia adaptada del puesto delantero de navegación. No acredita que el conjunto original ya sea ergonómico o móvil, ni una simulación biomecánica. La arquitectura y la consola se conservan. Quedan problemas concretos de respaldo, mirada, marcha y mecánica del soporte.

Se inventariaron cinco asientos y 92 piezas de silla: navegación 8, laterales 31 + 31, mando 11 + 11. La base común de mando Mesh_2093 pertenece al contexto fijo. El OBJ aporta 630 objetos; la referencia de VOY-03 reúne 645 piezas con su contexto/adaptadores. Operaciones no se identifica como una sexta silla.

### Respuestas a los doce criterios de cierre

1. **Asientos reales:** dos sillones de mando y tres sillas de estación. Por posición y comparación contextual: capitán a babor, primer oficial a estribor, CONN delante, ciencia e ingeniería en los laterales bajos. Operaciones y Táctica son puestos posteriores de pie. La asignación al modelo es una inferencia de su proa hacia −Y; los nombres históricos IZQ/DER son de coordenadas, no navales. [Referencia contextual primaria](https://roddenberry.x.io/2371-uss-voyager-ncc-74656/).
2. **Piloto:** navegación, con ocho piezas separadas, sin reposabrazos, pedestal y dos superficies LCARS principales independientes. Permite investigar un problema real de piernas sin reconstruir la consola.
3. **Geometría móvil:** sí, con jerarquía, pivotes corregidos y mallas independientes. El OBJ no contiene una guía funcional acreditada. El prototipo incorpora carro/guía nuevos y reconstruye localmente la longitud del casquillo inferior; no se presenta como mecanismo original descubierto.
4. **Aproximación:** geométricamente positiva en la traslación lateral cercana ensayada, con silla retirada y elevación del pie sobre la guía. El maniquí empieza ya alineado. No es marcha terminada ni prueba de giros desde cualquier rumbo.
5. **Sentado:** positivo en la copia con altura ajustada y pies en suelo. La pose original conserva fallos de borde/rodilla y pies elevados. La espalda queda sin apoyo suficiente incluso tras avanzar el respaldo 18 cm.
6. **Trabajo:** ambas manos alcanzan puntos interiores de Plane_94/95, con envolvente de contacto a 2 mm de la superficie; sus centros son visibles desde los ojos estimados. El ángulo descendente llega a 48,2° en 1,90 m. No se valida comodidad prolongada, lectura completa, dedos o uso de toda la consola.
7. **Levantado y salida:** recorrido inverso muestreado positivo; silla vuelve a su referencia horizontal. El asiento queda en la regulación de altura de cada usuario. No se afirma marcha física o estabilidad del cuerpo.
8. **Tres alturas:** no se cambió la talla para hacerlas pasar. Se modificó la altura del asiento, manteniendo constantes las longitudes de cada maniquí.
9. **Modificaciones:** descenso 14,13–21,54 cm, avance de respaldo 18 cm, casquillo inferior ajustado, guía fija y carro nuevos, retirada común 40 cm y trayectorias específicas de pies/manos. El ajuste de respaldo aún es insuficiente. No se movió ni recortó la consola en el prototipo guardado.
10. **Otros asientos:** comparten metodología, pero siguen E por ergonomía completa pendiente. Navegación original recibe C por intervención importante. Ningún asiento se promueve a A.
11. **Unreal:** faltan colisiones, retarget y animación real, validación física/marcha, ocupación/reservas/NPC, persistencia y la futura interfaz. Se entregan anclajes y cámaras sin implementar sistemas.
12. **Aceptación técnica:** preparada para revisión y aceptación **con reservas** del laboratorio; no para aprobar ergonomía definitiva, mecanismo de producción o integración jugable.

{heighttable}

## Evidencia y conservación

Se contrastaron 301 poses + 300 subfotogramas por altura: **1803 posiciones** de la animación guardada. No hubo penetraciones principales por encima del umbral de 2 mm del proxy. El error máximo de ejes de rig fue {max(x['max_axis_endpoint_error_m'] for x in verify)*1e6:.2f} µm. La silla adaptada pasó 81 posiciones por altura, cada 5 mm, sin contactos externos; se distingue su interfaz carro–guía. Estos resultados no son un barrido continuo certificado.

Las {copies['count']} copias de malla verificadas conservan UV, asignaciones de material y datos independientes; error de vértices esperado máximo {copies['max_world_vertex_error_m']*1e6:.2f} µm. La escena de referencia está intacta. Los fallos A1 (pie/guía) y A3 (manos/canto) están conservados en datos, renders y otro Blender.

La relectura SHA-256 de **{integrity['protected_count']} archivos protegidos** no detectó cambios, bajas o altas dentro de los árboles registrados. No se abrió Unreal ni se realizaron escrituras en GitHub. La comprobación no pretende ser un inventario de todo el disco.

![Antes/después real](CAPTURAS/LAMINA_ANTES_DESPUES.png)

Escena principal: `{R / 'ESCENAS/VOY04_Laboratorio.blend'}`. Escenas de fallo: `{R / 'ESCENAS/VOY04_Fallos_y_Comparativa.blend'}`. [Secuencia animada](ANIMACIONES/VOY04_Ciclo_175.gif). [Paquete documental](PAQUETE/VOY04_Entrega.zip). VOY-04 termina aquí; VOY-05 no se inicia.
''')
body='''## Identificación y sistema de coordenadas

La búsqueda cruza familias ChamferBox/Layer/MSB/Object/Box/Armrest con las piezas reales del puente y renders de contexto. Se encontraron tres cojines de estación, sus tres respaldos y los dos grupos de mando; no otra silla independiente. Las cotas se calcularon de nuevo con los vértices transformados de VOY-03, sin trasladar tamaños de Sutherland. Se usó rayo sobre el cojín para la superficie de asiento y sobre triángulos de apoyo identificados, evitando confundir base común, consola y suelo.

En el marco del puente, la proa es aproximadamente −Y y la vertical +Z. Mirando a proa, babor es aproximadamente +X. Así, MANDO_DER (+X histórico) se asocia contextualmente a capitán y MANDO_IZQ (−X) a primer oficial; LATERAL_DER se asocia a ciencia y LATERAL_IZQ a ingeniería. Son inferencias de disposición, no etiquetas semánticas del OBJ. No llamar Operaciones a cualquiera de las sillas por proximidad. [Roddenberry Archive](https://roddenberry.x.io/2371-uss-voyager-ncc-74656/) sitúa Operaciones/Táctica detrás y ciencia/ingeniería en los laterales bajos.

'''
body+=table(['ID geométrico','Asignación contextual','Piezas','Envolvente local ancho × fondo × alto m','Cojín Z','Suelo de referencia Z','Altura relativa'],[[m['id'],{'NAVEGACION':'CONN / navegación','LATERAL_DER':'Ciencia, babor','LATERAL_IZQ':'Ingeniería, estribor','MANDO_DER':'Capitán, babor','MANDO_IZQ':'Primer oficial, estribor'}[m['id']],len(m['parts']),' × '.join(f'{x:.3f}' for x in m['dimensions']),f'{m["seat_point"][2]:.4f}',f'{m["floor_m"]:.4f}',f'{m["seat_above_floor_m"]:.4f} m'] for m in inv])
body+='''

En navegación, Object_75 está a Z≈0 bajo el pedestal; los pies de trabajo pisan Mesh_1728 a Z=0,023326 m. La altura original sobre ese suelo de pies es **0,606564 m**, distinta de 0,629890 m sobre Object_75. En mando, Mesh_2093 sostiene las carcasas a Z=0,865392 m y el suelo de pies está a Z=0,479442 m: no confundir la distancia cojín–base común con altura ergonómica.

Las envolventes incluyen soportes y, en los laterales, ruedas. No equivalen a ancho útil del cojín. Las orientaciones y matrices completas están en `inventario_medidas.json` / `objetos.json`; `orientacion_contraste.json` contrasta el eje heredado con el vector asiento–respaldo medido otra vez.

## Componentes y contactos por silla

'''
for m in inv:
 body+=f'### {m["id"]}\n\nPosición de asiento (marco puente, metros): `{m["seat_point"]}`. Eje hacia delante: `{m["forward"]}`. Apoyo inferior próximo: `{next(x for x in bear if x["id"]==m["id"])["under_chair_bearing_object"]}`.\n\n'
 body+=table(['Objeto','Función geométrica','Dimensiones locales m'],[[p['key'],p['role'],' × '.join(f'{x:.4f}' for x in p['dimensions_m'])] for p in components if p['station']==m['id']])+'\n\n'
 contacts=next(x for x in internal if x['id']==m['id'])['contacting_object_pairs']
 body+=f'Hay {len(contacts)} parejas de objetos con contactos/cruces de superficies en el estado original. Ejemplos: '+', '.join(f'`{x["a"]}` / `{x["b"]}`' for x in contacts[:5])+'. El detalle y los cruces transversales están en `contactos_internos_originales.json`; no se convierten estos contactos internos en articulaciones acreditadas.\n\n'
body+='''## Interpretación funcional

Las tres sillas de estación no tienen reposabrazos independientes. Sus cojines y carcasas son piezas distintas, con espesor superficial y contactos de tapizado; separar esas capas no autoriza moverlas entre sí. Las laterales tienen cinco radios y conjuntos de ruedas, vástagos y remates: su apariencia permite proponer rodadura/giro, pero no acredita ejes/rodamientos ni recorrido despejado. Los 31 componentes no equivalen a 31 mecanismos.

Los sillones de mando tienen dos reposabrazos por silla, cojines segmentados y carcasa; no se localizaron bisagras funcionales de reposabrazos. La base Mesh_2093 es común y fija. Mover el sillón rígidamente sin estudiar esa base puede dejarlo flotante o provocar cruces. Las superficies abiertas, capas coincidentes y contactos cojinera/carcasa se conservan, con diagnóstico en `topologia.json`.

Las distancias a pantallas vecinas se conservan para todos los asientos en `near_screens` del inventario. Un centro vecino no demuestra alcance humano; solo el piloto recibe poses articuladas completas. Las capturas A muestran el contexto seleccionado y las versiones aisladas, no un despiece mecánico ya validado.
'''
write('01_INVENTARIO_SILLAS.md','Inventario funcional de sillas',body)
write('02_SILLA_PILOTO_GEOMETRIA.md','Silla piloto: geometría y preparación',f'''
## Elección

Se elige CONN/navegación. Sus ocho objetos forman un conjunto sencillo: `MSB_30191` pedestal inferior; `MSB_30194` vástago superior; `Object_77` carcasa de asiento; `ChamferBox_22` cojín; `MSB_30192` y `MSB_30193` soporte de respaldo; `Object_76` carcasa de respaldo y `Layer__3` tapizado. No tiene reposabrazos que haya que inventar o animar. Su consola original ofrece dos pantallas centrales separadas.

La envolvente completa es aproximadamente 0,653 × 0,718 × 1,274 m. El cojín mide aproximadamente 0,534 × 0,534 × 0,032 m de envolvente, con centro superficial a Z=0,629890 m. La cara inferior, el relieve del cojín y el borde frontal impiden tratar todo ese rectángulo como superficie útil plana. `inventario_medidas.json` conserva extremos y dimensiones por objeto.

## Jerarquía preparada

`CTRL_DESLIZAMIENTO` lleva el casquillo inferior y el carro. `CTRL_ALTURA`, hijo de ese control, lleva el conjunto superior. `CTRL_RESPALDO`, hijo del control de altura, lleva soporte, carcasa y tapizado del respaldo. La guía nueva y el suelo quedan fuera del grupo móvil. Las capas de cada cojín/carcasa se mantienen juntas. La escena 02 conserva la pose original con pivotes corregidos; las escenas 04 aplican el experimento.

Se recalculó el origen de cada copia con compensación de coordenadas de vértices y conservación de su matriz mundial. Error máximo de la preparación de pivotes <20 µm, con valores por pieza en `manifest_blender.json`, sección `chairs`. No se aplicaron indiscriminadamente escalas o rotaciones. Las matrices anteriores, posteriores y los controles están registradas; sus matrices se refieren al estado de montaje, antes de aplicar la animación/regulación.

La base diagnóstica de cálculo es `[lateral heredado, delante, arriba]`, de determinante −1. El control de silla usa `[lateral heredado, atrás, arriba]`, de determinante +1. Se entregan ambas matrices explícitas; **no exportar automáticamente el marco reflejado del maniquí a Unreal**. La traslación del puente heredada de VOY-03 es `{meta['bridge_translation']}` m. No se cambia la corrección de importación +90° X ni el factor provisional 1,10.

## Cambios experimentales

{heighttable}

Los descensos son regulaciones de la silla, no escalados del personaje. El casquillo inferior original era demasiado largo para esos descensos; en la copia experimental se remapea solo su cota Z entre el apoyo nuevo Z=0,048326 m y la parte superior `Z_asiento_original − descenso − 0,080 m`. Se conservan topología y UV de esa copia, aunque la proporción axial cambie. La referencia conserva la pieza completa sin modificar.

Se añade una guía estrecha de 7 cm de ancho y un carro de 15 × 16 cm. Sus cotas están en `bodygeom.py`, función `rail`, y las mallas reales en Blender. Son propuestas para estudiar el volumen ocupado; no hay diseño de rodamientos, topes, anclajes o carga física. Su contacto carro–guía se registra como interfaz específica, sin excluir el resto del mobiliario.

Se ensayaron retiradas de 20–60 cm. 30 cm falla para las tallas 1,75/1,90; 40 cm es el menor valor común que pasa la serie de 10 cm. No se buscó un mínimo continuo. No fue necesario girar la silla ni crear reposabrazos. La corrección de altura resuelve el espacio de piernas sin cortar la consola. No demuestra que sea la única solución: reposapiés u otros ángulos podrían estudiarse para conservar la cota, pero no se han validado. El respaldo se adelantó 18 cm, pero todavía queda una separación de 5,8–7,6 cm al tronco: ajuste de apoyo pendiente.

## Conservación y resultado

Las 8 piezas originales están preservadas en referencia. Siete se trasladan rígidamente en la copia adaptada; solo se reconstruye axialmente el casquillo inferior. La geometría de consola y arquitectura guardada no cambia. {copies['count']} copias verificadas conservan UV/materiales y datos independientes, con error esperado máximo {copies['max_world_vertex_error_m']*1e6:.2f} µm. No se acredita un mecanismo físico por esa coincidencia.

![Despiece](CAPTURAS/B05_DESPIECE_REAL.png)
![Pivotes](CAPTURAS/B06_PIVOTES_Y_CONTROLES.png)
''')
write('03_ERGONOMIA_PERSONAJES.md','Ergonomía con personajes articulados',f'''
## Referencias humanas

La búsqueda por nombres de recursos humanos/rigs en los assets locales del proyecto y la inspección de la escena VOY-03 no localizaron un personaje reutilizable adecuado. Se documenta el alcance en `busqueda_rigs_locales.txt`; un resultado vacío no demuestra ausencia de cualquier recurso en todo el disco. No se abrieron proyectos Unreal para buscar sus maniquíes. Se construyeron tres rigs sencillos de laboratorio de **18 huesos** y cápsulas rígidas articuladas, con pesos 1:1 mediante Armature modifier.

Las alturas nominales son 1,60 / 1,75 / 1,90 m. Se usa cadera de pie a 0,53H, cabeza a +0,407H con radio 0,063H: el máximo vertical nominal es H. Fémur/tibia: 0,245H cada uno; húmero 0,186H; antebrazo 0,146H; hombro +0,288H sobre cadera. Radios muslo/pantorrilla: 0,043H/0,029H; pelvis semiancho 0,055H. Pies con radio 0,027H y eje 0,105H. Son proporciones razonables de un proxy documentado, **no percentiles antropométricos ni certificación normativa**. El JSON `proporciones_maniqui.json` recoge todos los parámetros.

La IK analítica mantiene longitudes y resuelve codos y rodillas. Los huesos son independientes y rígidos, sin piel, dedos, masa, ropa o deformación del cojín. No se escala un maniquí durante una prueba para hacerle pasar. Las cápsulas analíticas envuelven las superficies poligonales renderizadas.

## Postura original y adaptación

La pose original con muslos horizontales y cadera retrasada conserva interferencias de pantorrilla con el borde del asiento; adelantar el cuerpo puede invadir Object_129. Los pies quedan aproximadamente 16,4–23,8 cm por encima del plano bajo el pedestal en ese ensayo. No se acepta esa pose como éxito. Los archivos `original_1.xx.json` incluyen los triángulos testigo.

{heighttable}

Las posturas adaptadas ponen los pies a Z=0,023326 m sobre Mesh_1728, con seis rayos de apoyo por talla en la pose de trabajo de la animación reabierta. La cadera queda sobre el cojín; muslos horizontales, rodillas aproximadamente a 90° y piernas separadas según el ancho de pelvis. Los contactos por debajo de 2 mm se tratan como tolerancia del proxy, sin afirmar compresión física. No se excluyen globalmente la silla o la consola del chequeo.

'''+table(['Talla','Holgura mínima pierna–carcasa de consola','Alcance hombro–mano','Flexión interior de codo','Visibilidad'],[[f'{r["H"]:.2f} m',f'{min(x["minimum_console_surface_gap_m"] for x in next(v for v in leg if v["H"]==r["H"])["legs"])*100:.2f} cm',f'{min(x["shoulder_to_hand_m"] for x in r["hands"])*100:.1f}–{max(x["shoulder_to_hand_m"] for x in r["hands"])*100:.1f} cm',f'{min(x["elbow_inner_angle_deg"] for x in r["hands"]):.1f}–{max(x["elbow_inner_angle_deg"] for x in r["hands"]):.1f}°','Centros Plane_94/95 visibles'] for r in erg])+'''

Las holguras de la tabla se calculan contra Object_129/126/127, no son separación a todo el entorno ni profundidad volumétrica. Las manos terminan con su envolvente a 2 mm de cada pantalla; no se simulan dedos o presión. El arco de manos evita el canto que atravesaba la primera trayectoria directa. No se acredita alcanzar cualquier botón de las texturas.

## Reservas ergonómicas

El tronco mantiene 5,8–7,6 cm hasta el respaldo incluso tras adelantarlo. Es una postura posible sin apoyo dorsal completo, con comodidad prolongada pendiente. La mirada descendente estimada es de 30,6 / 40,4 / 48,2°: la talla alta necesita una revisión específica de cabeza, ojos y lectura, sin inferir un límite normativo. Solo se verificaron rayos a los centros, no campo visual completo u oclusión por manos.

No hay reposabrazos en este piloto. La cadera no rota anatómicamente y no se demuestra equilibrio durante sentarse. La aproximación lateral usa traslación guiada y un paso de elevación sobre la guía; no hay ciclo de marcha con apoyos alternados, fuerzas o transferencia de peso. El maniquí empieza orientado hacia la consola; otros giros y conexión exacta con las rutas VOY-03 quedan por contrastar. El resultado permite estudiar adaptación local, no aceptar ergonomía definitiva.

![Sección real adaptada](CAPTURAS/E_ADAPTADO_SECCION_1.75.png)
![Tallas](CAPTURAS/D03_COMPARACION_TRES_ALTURAS.png)
''')
write('04_ANIMACIONES_EXPERIMENTALES.md','Animaciones y recorridos experimentales','''
## Secuencia guardada

Tres escenas 04_PROTO contienen una acción técnica de 301 fotogramas a 24 fps (12,5 s entre primer y último frame). Se anima el rig articulado y el grupo móvil de silla, con claves lineales. La silla inicia y termina en su referencia horizontal; la altura/regulación individual se conserva. El personaje inicia y termina junto al puesto, ya orientado hacia la consola.

'''+table(['Fotograma','Estado'],[[1,'Silla en referencia, personaje junto al puesto'],[31,'Silla retirada 40 cm, guía libre de mobiliario'],[61,'Aproximación lateral completada; pie salva guía'],[91,'Sentado con silla retirada'],[121,'Desplazamiento ocupado finalizado'],[151,'Trabajo, manos próximas a pantallas'],[181,'Manos retiradas'],[211,'Silla de nuevo retirada'],[241,'Personaje de pie'],[271,'Personaje fuera del puesto'],[301,'Retorno vacío a referencia']])+'''

Durante el deslizamiento ocupado se elevan los pies hasta 35 mm y vuelven al suelo. La traslación lateral eleva el pie que cruza la guía hasta 40 mm. Las manos siguen un arco vertical adicional de 16 cm durante el acceso a controles y vuelven por el mismo recorrido. No se exige giro de silla en esta solución. No hay animación realista de marcha, agarrar la silla, empujarla con fuerza o activar la regulación.

## Qué se comprobó

Para cada talla se compararon 301 poses analíticas con los ejes del rig reabierto y se comprobaron otras 300 poses en mitad de los intervalos de Blender. Se evaluaron pelvis, tronco, cabeza, brazos, manos, muslos, pantorrillas y pies frente a los triángulos de silla y entorno, incluida la guía nueva. Resultado final: 1803 posiciones sin penetraciones principales por encima de 2 mm del proxy. La silla pasó 81 posiciones de traslación por talla (243 poses), con SAT de 17 ejes tras BVH; no hubo contactos externos. La ida/vuelta simétrica no se cuenta como otro experimento independiente.

Estos son **ensayos discretos densos**, no un barrido continuo certificado, ni un solver físico o biomecánico. Se conservan los resultados por altura, frame, miembro, objeto y triángulo. El chequeo de pertenencia a un sólido no es concluyente para objetos abiertos/no manifold; las superficies se tratan a doble cara. No se declara ausencia de todo contacto interno.

## Fallos y correcciones

La pose original falla en asiento/consola y pies. A1 añadió guía y carro, pero el pie derecho atravesaba la guía en 10/12/10 poses de las tallas 1,60/1,75/1,90. Se conserva el fallo en `trayectorias_A1_FALLO_GUIA.json` y Blender de evidencias; se corrigió elevando el pie.

A3 acercaba las manos por una línea que atravesaba el canto y las pantallas en 10/10/8 poses. La posición final era válida; la transición no. `trayectorias_A3_FALLO_MANOS.json` conserva esa trayectoria. El arco elevado corrigió los subtramos ensayados. Las versiones rechazadas no se incluyen en los recuentos finales positivos.

## Revisión visual

`ANIMACIONES/VOY04_001.png` … `VOY04_301.png` cada tres fotogramas son renders reales Blender. GIF y WebP reúnen esos 101 PNG a unos 125 ms por imagen (GIF alterna 120/130 ms); no representan un muestreo adicional. `LAMINA_SECUENCIA.png` selecciona diez poses con rótulos exteriores al render. Las secciones de consola son cortes visuales sobre copias de render, nunca una eliminación de obstáculos para la prueba de colisión.

La primera exportación visual repetía una pose por mantener otra escena activa. Se rechazó y regeneró desde la escena correcta (script 19); el script 20 contrasta hashes de píxeles y cantidad de frames de GIF/WebP. Ese error de exportación no afectó a los ensayos del rig guardado. La secuencia final verificada sustituye la exportación rechazada.

![Secuencia](CAPTURAS/LAMINA_SECUENCIA.png)
''')
write('05_CONSOLA_INTERACTIVA_ESTUDIO.md','Estudio de la consola y futura interacción',f'''
## Piezas reales

Object_129 es la carcasa principal asociada a navegación; Object_126/127 y remates vecinos completan el contexto. No se incluyeron en el grupo móvil de la silla. Las superficies principales Plane_94 y Plane_95 son objetos de pantalla independientes con `scrn10_3` y `scrn10_4`. Plane_96, Plane_139, Plane_138 y Plane_140 son pantallas laterales vecinas; no se declara alcanzable su superficie completa.

Las botoneras LCARS son gráficos de las texturas originales, no cientos de botones geométricos. Los marcos, carcasa y algunas molduras son geometría independiente. Las zonas luminosas siguen usando sus materiales/nodos de origen. Las 49 imágenes permanecen empaquetadas y las UV/materiales de las copias están verificadas; no se han sustituido gráficos ni creado PBR definitivo.

'''+table(['Pantalla','Material','Desviación máxima de planitud','Centro local (m)'],[[x['key'],', '.join(x['source_materials']),f'{x["planarity_m"]*1e6:.2f} µm',', '.join(f'{z:.3f}' for z in x['local_center'])] for x in screens])+f'''

Las dos pantallas centrales no forman exactamente un único plano. Cada superficie debe conservar su propia normal, contorno y UV. La carcasa es abierta/no manifold en este recurso: no se deduce volumen sólido o hueco útil a partir de una AABB. Los datos de planitud no convierten toda la consola en una pantalla plana.

## Preparación entregada

En cada escena 04 se guardaron anclajes de aproximación, cadera sentada, dos manos y punto de interacción, además de una cámara ampliada. `marcadores_interaccion.json` contiene posiciones locales/mundiales y matrices; `consola_superficies.json` contiene normales y planos. Se comprobó que añadir los anclajes no alteró las mallas. Son referencias geométricas, sin eventos de juego.

Una futura superficie dinámica puede reutilizar cada objeto de pantalla y sus UV0. La prueba de manos utiliza puntos interiores a y=0,405 m y x=±0,16 m del marco diagnóstico, con el extremo de la envolvente a 2 mm de su plano. Los hombros alcanzan esos puntos en las tres tallas. La cámara ampliada se orienta al centro de ambas pantallas; no constituye una cámara final de lectura aprobada ni garantiza que el FOV sea cómodo para todos los jugadores.

El futuro ratón podrá consultar la intersección sobre cada superficie y convertirla a sus UV; mandos y accesibilidad necesitarán una modalidad de foco/selección propia. La función, distribución de controles, Widgets, Render Targets, navegación de UI y enlace CoreRPG no están implementados. No se modificó el proyecto Unreal.

## Rodillas, manos y visión

Tras bajar la silla, la holgura mínima calculada de miembros de pierna frente a las tres carcasas ensayadas es aproximadamente 17,7 / 12,6 / 7,7 cm para 1,60 / 1,75 / 1,90. Esto describe la pose de trabajo concreta y esas carcasas; no es una envolvente universal para animaciones futuras. El canto bloqueó la trayectoria directa de manos y sigue siendo un obstáculo real en la versión final.

Los centros Plane_94/95 son visibles por rayo desde cada ojo estimado; quedan pendientes todo el campo visual, oclusión de manos, tipografía, reflejos, contraste y lectura desde la postura alta. No se cambia la inclinación ni altura de la consola para resolverlo en esta fase.

![LCARS originales, render de inspección](CAPTURAS/D04_LCARS_ORIGINALES.png)
''')
write('06_COMPARATIVA_PUESTOS.md','Comparativa y reutilización de procedimientos','''
## Criterio de clasificación

A exige geometría y ergonomía verificadas para el alcance completo. B admite ajustes menores ya identificados con evidencia suficiente. C necesita intervención importante. D recomienda reconstrucción. E indica evaluación insuficiente. Inventariar y medir no basta para asignar A/B a la ergonomía de una silla.

'''+table(['Puesto','Familia/piezas','Altura original sobre referencia','Grado global','Motivo'],[[r['id'],r['geometry_family']+f' / {r["parts"]}',f'{r["seat_height_m"]:.3f} m',r['grade'],r['reason']] for r in comp])+'''

Navegación es C en su estado original: bajar 14–22 cm, modificar casquillo y crear guía/carro supera un ajuste menor. El prototipo adaptado pasa las muestras geométricas pero mantiene reservas de respaldo, mirada y marcha. No se presenta como A ni se recomienda reconstruir toda la silla o consola.

Las dos laterales tienen 31 piezas y familia visual común de asiento/respaldo, soporte y base de cinco radios con ruedas. Pueden reutilizar la organización, identificación de capas y maniquíes. Deben estudiar de nuevo rodadura/giro, apoyo de ruedas, alturas, orientación, proximidad lateral de consolas y recorrido. Su altura de casi 60 cm requiere atención; no se ha demostrado que el descenso del piloto o su carrera funcione allí.

Los dos sillones de mando comparten estructura visual y base común Mesh_2093, con 11 piezas de carcasa, cojines y reposabrazos por silla. La altura sobre suelo de pies ronda 49 cm, pero reposabrazos, acceso entre muebles y base compartida pueden exigir otra solución. No se inventa un reposabrazos abatible ni un asiento giratorio por tener objetos separados. Las plataformas no deben viajar con la silla sin estudio propio.

## Componentes reutilizables

Son reutilizables el medidor de geometría/UV, el cambio compensado de pivotes, los controles abstractos de traslación/altura/respaldo, el maniquí proporcional, la IK, los ensayos de distancia cápsula–triángulo, SAT, exportación JSON/CSV y contraste después de recarga. Los controles no deben implicar que todas las sillas necesitan los mismos grados de libertad.

Se reutiliza de Sutherland el aislamiento, separación base/grupo móvil, controles locales, conservación de UV, poses intermedias, retorno y recarga. Sus seis sillas tenían otra estructura y una carrera de 30 cm documentada; no acreditaban sentado. Voyager obtiene sus 40 cm de su propia serie. No se copió geometría, dimensión ni Blueprint de Sutherland.
''')
write('07_PREPARACION_UE5.md','Propuesta para Unreal Engine 5.8.2','''
## Alcance exclusivamente propuesto

No se ha abierto Unreal, importado assets, creado Blueprints, Widgets, Render Targets o lógica CoreRPG. La propuesta se basa en la geometría y la metodología histórica de Sutherland. Su compatibilidad concreta con el proyecto/versión final deberá verificarse en una fase autorizada.

Conservar carcasa de consola y arquitectura como Static Meshes fijas. Mantener Plane_94/95 separadas con UV de origen. Separar guía fija, carro móvil, casquillo, conjunto de asiento y grupo de respaldo, respetando la unión entre cojín y carcasa. Los ejes y matrices de referencia están entregados; convertir expresamente el marco diagnóstico reflejado del maniquí a un sistema de exportación coherente, y metros a centímetros. No hornear a ciegas las transformaciones de la referencia ni exportar todo como una única malla convexa.

## Colisiones e interacción corporal

Crear colisiones simples por pieza o subconjunto que conserven huecos de piernas y espalda. La silla tiene superficies abiertas y capas coincidentes: una envolvente convexa global puede cerrar espacios funcionales. Los triángulos y ensayos de Blender sirven como referencia comparativa, no como receta de colisión de producción. Ensayar obstáculos de control, interfaces internas, suelo real y barridos por todo el recorrido; perfilar coste y contrastar la simplificación contra la referencia.

La cápsula de un personaje de pie no demuestra una postura sentada. Habrá que definir una representación de colisión sentada acorde con el cuerpo, con cambio de estado controlado y comprobaciones de espacio. No resolver un bloqueo apagando toda colisión del puesto o reduciendo arbitrariamente al personaje. La colocación de pelvis/pies/manos debe retargetearse al rig final con longitudes reales, ropa y deformación, repitiendo la evaluación para cada talla.

## Actor y estados propuestos

Un controlador de puesto puede agrupar `Free → Reserved → Approach → Retract → Align → Sit → Occupied → Stand → Exit → Return → Free`, con estados de cancelación y bloqueo. Reservar tanto silla como espacio de transición; impedir órdenes opuestas, dobles ocupaciones y retorno mientras un cuerpo invade el volumen. La animación Blender no implementa estas reglas.

Para NPC persistentes, guardar identificadores estables de puesto y ocupante, regulación de altura y estado seguro; recuperar poses coherentes después de cargar y liberar reservas de actores ausentes. Replanificar acceso si hay obstáculos y comprobar conflictos entre jugador/NPC. No persistir un mero número de frame como sustituto de un estado válido. La regulación individual puede mantenerse al salir; el retorno horizontal de la silla es independiente.

## Animaciones, puntos y consola

Preparar animaciones reales de aproximación con apoyo de pies, orientación, ajuste de silla, sentado, trabajo, retirada de manos, levantado y salida. Resolver equilibrio, pelvis, respaldo, IK de dedos y manejo del dispositivo. La traslación lateral del laboratorio no es una animación final de marcha.

Los anclajes y cámaras de Blender son puntos de partida para aproximación, pelvis sentada, alcance e inspección ampliada. El punto de aproximación está junto al puesto y ya orientado: su conexión con navegación del juego, rutas de VOY-03 y giros debe probarse. Una futura interfaz por pantalla necesita foco/entrada de ratón o mando, mapa de UV y estados de cámara; preservar los LCARS originales hasta diseñar esa capa. Nada de ello está implementado ahora.

## Condiciones antes de promoción

Revisar primero apoyo dorsal, postura de cabeza alta y mecanismo real. Después validar importación/UV/pivotes, colisiones, retarget, movimiento ocupado con los pies, transición de cápsula, obstáculos intermedios, cancelación/reanudación y múltiples NPC. No atribuir a Sutherland o al motor resultados que solo se han muestreado aquí en Blender.
''')
write('08_HOJA_DE_RUTA.md','Hoja de ruta y aceptación','''
## Decisiones que permite tomar VOY-04

Conservar la arquitectura y la consola es una alternativa viable para seguir investigando el piloto. El problema no exige escalar el personaje o mover todo el puente. La silla necesita altura adaptable y una solución mecánica de acceso. Puede conservar la mayor parte del conjunto superior original.

La aceptación propuesta es **COMPLETADA CON RESERVAS** del laboratorio documental y cinemático. No es aprobación del activo de producción. Las reservas tienen testigos y medidas; no se retocaron fuera de Blender para parecer resueltas.

## Trabajo pendiente priorizado

1. Ajustar apoyo dorsal y profundidad útil: aún quedan 58–76 mm. Probar acercar/reconstruir localmente el soporte o añadir apoyo coherente, comprobando otra vez todas las poses y capas.
2. Revisar cabeza y lectura en 1,90 m (mirada descendente estimada 48,2°), con un rig que tenga ojos/cuello y la tarea visual real. Evitar mover la consola sin evidencia adicional.
3. Diseñar casquillo, anclajes, topes, guía y carro con una relación mecánica creíble. El prototipo ocupa un volumen comprobado, pero no transmite cargas ni certifica contacto/desgaste.
4. Sustituir la traslación lateral por marcha articulada con apoyos alternados, giro cuando proceda, equilibrio y contacto. Repetir con ropa y rig real. Conectar la aproximación a los recorridos del puente.
5. Ejecutar comprobación continua o suficientemente conservadora de movimientos, incluidos contactos y sólidos cerrados reconstruidos donde sea necesario. Los 601 estados por altura no eliminan toda incertidumbre entre muestras.
6. Evaluar las cuatro sillas restantes con sus propias posturas/espacios; mantener grado E hasta esa prueba.
7. Solo en una fase autorizada posterior: importación y verificación en Unreal, colisiones, retarget, reservas/ocupación, persistencia de NPC e interfaces.

## Revisión humana sugerida

Abrir `VOY04_Laboratorio.blend`, elegir `04_PROTO_1.75`, revisar los marcadores 1/31/61/91/121/151/211/241/301 y después las otras tallas. Comparar con `03_ORIGINAL_1.xx`. La escena 01 conserva toda la referencia y 02 muestra los pivotes. Abrir `VOY04_Fallos_y_Comparativa.blend` para los fallos rechazados. Revisar las capturas E y la lámina antes/después sin confundir sus cortes visuales con modificaciones de arquitectura.

La aceptación del informe puede conservar esas reservas; una aceptación de ergonomía definitiva requiere resolverlas. No se inicia VOY-05 ni integración Unreal al terminar este trabajo.
''')
write('09_METODOLOGIA_LIMITACIONES.md','Metodología, reproducibilidad y límites',f'''
## Fuentes y aislamiento

Se identificaron y leyeron VOY-02/03 en sus rutas reales y el informe F07-CHAIR-01. Se copió `VOY03_Circulacion.blend` a `REFERENCIAS`, sin guardar sobre el origen. `baseline.json` registró SHA-256, tamaños y mtimes antes de crear experimentos. La relectura final conserva {integrity['protected_count']} archivos; `integridad_final.json` detalla el alcance y todos los hashes.

Todas las escrituras de artefactos del laboratorio se dirigen a `{R}`. Los proyectos Unreal no se abrieron; no hubo escrituras ni comandos remotos de GitHub. La carpeta de trabajo Git solo mostraba `.codex-remote-attachments/` sin seguimiento; no se hizo commit. No se afirma un hash de CoreRPG/Valhalla o de todo el equipo, cuyos proyectos no se abrieron ni editaron.

La referencia contiene 645 piezas, incluidas 630 del OBJ y contexto heredado. Cada escena de trabajo copia sus objetos y **datos de malla**, compensando padres al conservar matrices mundiales. No se modifican mallas compartidas de VOY-03. {copies['count']} copias contrastadas: UV/asignaciones iguales y mallas con un único usuario. El error máximo esperado de vértices fue {copies['max_world_vertex_error_m']*1e6:.2f} µm, por redondeo de coma flotante. Los 49 recursos de imagen se mantienen empaquetados.

## Cálculo geométrico

Se exportan vértices, triángulos e identidad de objeto del Blender real, transformados a metros del marco puente. Se miden superficies mediante rayos, extremos locales y ajuste SVD de planos. La geometría de cada silla se mide en Voyager; los números de Sutherland no intervienen en sus cotas o carreras. La escala arquitectónica 1,10 sigue siendo una hipótesis heredada, no una unidad original certificada.

La distancia segmento–triángulo se calcula con proyección, aristas y cruce del plano. Al restar el radio se obtiene la separación de cada cápsula corporal. Las superficies se consideran a doble cara. Se usa umbral de penetración principal de 2 mm; eso no significa que los pequeños contactos negativos sean físicamente aceptables. No se excluyen globalmente el asiento, las piernas o la consola. Los volúmenes contiguos del maniquí se solapan intencionadamente para formar articulaciones: no se interpreta su unión como autocolisión física.

La silla usa BVH para candidatos y SAT de 17 ejes para contactos de triángulos, con tolerancia de separación de 1 µm y test transversal de 10 µm. Contacto, coplanaridad y cruce transversal no son automáticamente volumen penetrado. El contacto carro–guía se conserva por separado como interfaz propuesta. Los contactos originales entre piezas se registran, no se borran.

La topología diagnóstica suelda puntos a 10 µm en memoria y cuenta bordes abiertos/no manifold; **no repara** el recurso. Una cápsula completamente contenida en un sólido cerrado exigiría además pertenencia volumétrica. Muchas piezas originales son abiertas/no manifold (Object_129 incluido), por lo que no se certifica un interior sólido ni ausencia universal de penetración por un resultado de superficies. Los recorridos parten de un estado exterior conocido y se inspeccionan visualmente; la certificación física queda pendiente.

## Muestreo, rig y límites

301 frames y 300 puntos medios por talla, más 81 posiciones de silla por talla, no son un barrido continuo. No se han probado todos los caminos, todas las tallas intermedias, todos los puntos LCARS o giros desde cualquier rumbo. La vuelta simétrica no duplica la independencia del ensayo. Se verifican ejes del rig reabierto con máximo error {max(x['max_axis_endpoint_error_m'] for x in verify)*1e6:.2f} µm; la cápsula analítica es una envolvente conservadora del polígono renderizado.

No hay fuerzas, equilibrio, peso, fricción, masas, presión sobre cojines, biomecánica, ropa, dedos o animación final de marcha. Los huesos rígidos conservan sus longitudes; la altura corporal no cambia de forma arbitraria. La traslación guiada no sustituye una prueba de locomoción. Los rayos de mirada solo acreditan dos centros de pantalla, no lectura o visibilidad completa.

Las capturas son renders de Blender. Las secciones E/D recortan copias **solo para visualización** y las comparativas aíslan el entorno. Las colisiones y la escena principal usan la consola completa. Las láminas solo reordenan y rotulan renders existentes; GIF/WebP reúnen los PNG sin alterar posiciones. No se generó ninguna evidencia con IA ni se ocultaron los ensayos fallidos de los datos.

## Reproducción

Conservar esta entrega. Para repetir, usar otra carpeta/copia, nunca ejecutar el aislamiento encima de un laboratorio protegido. Blender instalado: `C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe`. Su Python con NumPy: `5.2\\python\\bin\\python.exe`. El script 16 usa Python local con Pillow únicamente para ensamblar renders y verificar archivos.

Orden de reconstrucción final: 00 (nueva baseline y copias), 01 (Blender: extracción/renders), 02–04 (medidas y búsqueda), 06 (búsqueda de retiradas), 07 (trayectoria final), 08 (Blender/escenas/renders), 09 (Blender/SAT/topología), 10 (Blender/recarga), 11 y 14 (métricas), 12–13 (Blender/anclajes/evidencias), 15 (Blender/contactos internos), 16 (láminas/integridad), 18a (Blender/imágenes empaquetadas), 20 (píxeles y animación), 17 (informes), 18 (paquete). Repetir 10 tras añadir anclajes, como en la entrega. El script 19 regenera solo la exportación visual si se necesita; 08 ya incluye la corrección de escena activa.

07b/07c/07d documentan correcciones históricas y no son necesarios en una reconstrucción limpia con la función final de 06. Los JSON A1/A3 suministrados son entradas de reproducción de fallos para 12; conservan todas las poses rechazadas. No renombrar un ensayo nuevo como esos históricos. 00 y los archivadores históricos tienen guardas contra sobrescritura. El paquete contiene geometría numérica y scripts; los .blend de referencia/final quedan en el MSI y sus rutas están en README y manifiestos.
''')
reports=['00_RESUMEN_EJECUTIVO.md','01_INVENTARIO_SILLAS.md','02_SILLA_PILOTO_GEOMETRIA.md','03_ERGONOMIA_PERSONAJES.md','04_ANIMACIONES_EXPERIMENTALES.md','05_CONSOLA_INTERACTIVA_ESTUDIO.md','06_COMPARATIVA_PUESTOS.md','07_PREPARACION_UE5.md','08_HOJA_DE_RUTA.md','09_METODOLOGIA_LIMITACIONES.md']
readme='# VOY-04 — Índice de entrega\n\n22/10/2026. **COMPLETADA CON RESERVAS.** Laboratorio independiente; Unreal y VOY-05 no iniciados.\n\n'
readme+='\n'.join(f'- [{n}]({n}) — `{R/n}`' for n in reports)+'\n\n## Escenas y evidencias\n\n'
for folder,n in [('ESCENAS','VOY04_Laboratorio.blend'),('ESCENAS','VOY04_Fallos_y_Comparativa.blend'),('REFERENCIAS','VOY03_Circulacion.blend'),('ANIMACIONES','VOY04_Ciclo_175.gif'),('ANIMACIONES','VOY04_Ciclo_175.webp'),('PAQUETE','VOY04_Entrega.zip')]:readme+=f'- [{n}]({folder}/{n}) — `{R/folder/n}`\n'
readme+=f'\nImágenes reales y láminas: `{R/"CAPTURAS"}`. Secuencia PNG: `{R/"ANIMACIONES"}`. Datos: `{R/"DATOS"}`. Scripts: `{R/"SCRIPTS"}`. [Galería](GALERIA.html).\n\nEl ZIP excluye .blend y caches, incluye informes/datos/scripts/capturas/animaciones. Su CRC y SHA-256 se verifican en `PAQUETE/verificacion_zip.json` y `VOY04_Entrega.zip.sha256`. Los .blend quedan accesibles en las rutas completas anteriores.\n\n'
readme+='Escenas principales: '+', '.join(f'`{x}`' for x in meta['scenes'])+'. Todas tienen mallas independientes. En 04 se guardan 301 frames, cámaras y anclajes. Las escenas auxiliares de fallo usan snapshots evaluados y cortes de presentación; no sustituyen el contexto completo del prototipo.\n'
(R/'README.md').write_text(readme,encoding='utf8')
captions={'LAMINA_ANTES_DESPUES.png':'Original y adaptación — secciones visuales de consola, nunca geometría eliminada para colisiones.','LAMINA_SECUENCIA.png':'Ciclo 1,75 m — diez poses reales.','D03_COMPARACION_TRES_ALTURAS.png':'Azul 1,60 m; verde 1,75 m; naranja 1,90 m. Sillas reguladas, sin consola en esta comparativa.','D04_LCARS_ORIGINALES.png':'Materiales LCARS originales. Render de inspección, sin acabado PBR.','D02_FALLO_A1_GUIA.png':'Fallo rechazado A1: el pie cruza la guía. Snapshot real de la trayectoria preservada.','D02_FALLO_A3_MANOS.png':'Fallo rechazado A3: trayectoria directa de manos a través del canto.','B05_DESPIECE_REAL.png':'Ocho piezas originales aisladas; separación visual, no bisagras acreditadas.','B06_PIVOTES_Y_CONTROLES.png':'Ejes modelados en los pivotes preparados.','B01_PUESTO_PILOTO.png':'Puesto piloto en contexto cercano.'}
gallery='<!doctype html><html lang="es"><meta charset="utf-8"><title>VOY-04 — Galería técnica</title><style>body{font:16px system-ui;background:#15212b;color:#e8f0f6;max-width:1400px;margin:auto;padding:24px}a{color:#8cdcff}figure{background:#24333f;padding:14px;margin:24px 0}img{max-width:100%;height:auto}figcaption{padding:10px 0}h1{font-size:30px}</style><h1>VOY-04 — COMPLETADA CON RESERVAS</h1><p>Imágenes reales de Blender. Las secciones recortan copias de render; la escena principal y las pruebas conservan la consola completa. El respaldo, la marcha y la mecánica siguen pendientes.</p><p><a href="README.md">Índice e informes</a></p><h2>Ciclo técnico de 1,75 m</h2><img src="ANIMACIONES/VOY04_Ciclo_175.gif"><p>101 renders, 125 ms por imagen; no es una simulación física.</p>'
for name in list(captions)+[p.name for p in sorted((R/'CAPTURAS').glob('E_*.png'))]:
 cap=captions.get(name,'Sección visual para revisar asiento, rodillas, pies y separación del respaldo: '+name)
 gallery+=f'<figure><a href="CAPTURAS/{html.escape(name)}"><img loading="lazy" src="CAPTURAS/{html.escape(name)}"></a><figcaption>{html.escape(cap)}</figcaption></figure>'
gallery+='<h2>Inventario original</h2>'
for m in inv:gallery+=f'<figure><img loading="lazy" src="CAPTURAS/A_{m["id"]}_AISLADA.png"><figcaption>{m["id"]}: {len(m["parts"])} piezas. Captura aislada de la geometría original.</figcaption></figure>'
(R/'GALERIA.html').write_text(gallery+'</html>',encoding='utf8')
(R/'DATOS/leyendas_capturas.json').write_text(json.dumps(captions,indent=2,ensure_ascii=False),encoding='utf8');print('REPORTS',len(reports),'GALLERY',True,flush=True)
