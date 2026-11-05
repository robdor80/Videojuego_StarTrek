# VOY-02 — Puertas, sillas y consolas
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Puertas: grupos completos y ensayo de carrera
Las tres parejas se recuperaron mediante correspondencia MAX/OBJ y medidas independientes; `puertas_medidas.json` conserva todos los fragmentos, vectores, tangente, normal y carrera. No se confunden paneles Doorpanel con hojas. El control de cápsula en cerrada bloquea, y los ensayos de vano desplazan conjuntos completos, con adornos presentes.

La investigación nueva amplía cinco poses a **21 fracciones de apertura** por puerta. BVH filtra candidatos y SAT de triángulos en 17 ejes cuenta contactos/intersecciones. Se compara con la pose cerrada; una pareja de índices nueva no equivale por sí sola a penetración volumétrica nueva. Para separar evidencia, se exige que ambos triángulos atraviesen el plano del otro >10 µm para clasificarlos transversales; el resto conserva coplanaridad o borde/tangencia.

| Puerta | Carrera por hoja m a 1,10 | Máx. parejas nuevas | Máx. cruces transversales | Obstáculos |
| --- | --- | --- | --- | --- |
| D_IZQ | 0.4605 | 186 | 106 | Mesh_1837, Mesh_1855, Object_81 |
| D_DER | 0.4605 | 272 | 264 | Mesh_1858, Object_82 |
| D_POST | 0.4605 | 120 | 0 | Mesh_1832, Mesh_1833, hallwayfloor_1 |

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
