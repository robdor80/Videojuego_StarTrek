# VOY-02 — Escalas, ergonomía y accesibilidad
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Escala recomendada y confianza
El OBJ no proporciona una unidad física autoritativa. Se compararon factores 1,00 / 1,10 / 1,15 / 1,20 / 1,25 / 1,30 / 1,50813535 utilizando hojas completas y cápsulas reales. H=1,90 m falla en las tres puertas a 1,00 y pasa los tramos locales a 1,10 y superiores probados. H=1,60 y 1,75 pasan a 1,00. Por ello, **1,10 es el mínimo factor de la serie probada que satisface los tres vanos para 1,90 m**, con confianza arquitectónica media y confianza baja como escala global definitiva. No se ha buscado el mínimo continuo entre 1,00 y 1,10.

La envolvente pasa de 13,150 × 13,011 × 3,840 a aproximadamente 14,465 × 14,312 × 4,224 m. La derecha tiene altura central de 1,775576 unidades OBJ: a 1,10 son ~1,953 m, apenas 53 mm sobre 1,90 m antes de otros márgenes. Sus anchuras medidas rondan 0,832 m a 1,10; en izquierda/posterior, ~0,922 m a las alturas muestreadas. No se convierten rayos centrales en rectángulos totalmente libres.

La similitud MAX ≈ OBJ ×1,50813535 + (−0,11236;1,875563;−0,466607) coincide en nueve parejas arquitectónicas independientes, con máximo ≤8,80 µm. No prueba un origen de unidades ni equivalencia de todas las piezas. `strudextends` presenta RMS ~0,443 m y máximo ~1,018 m; muebles y sillas requieren correspondencia individual. No se adopta 1,508 como escala humana.

## Suelos, techo y poses de pie

| Zona (coordenadas en DATOS) | Suelo Z m | Primera superficie desde suelo+1,80 m: altura relativa m | H de pie que pasan en el punto |
| --- | --- | --- | --- |
| CENTRO | 0.479 | 2.575 | 1.6, 1.75, 1.8, 1.9 |
| NAVEGACION_PASO | 0.327 | 2.880 | 1.6, 1.75, 1.8, 1.9 |
| DELANTE_MANDO | 0.479 | 2.632 | 1.6, 1.75, 1.8, 1.9 |
| PASARELA_DERECHA | 0.784 | 1.992 | 1.6, 1.75, 1.8, 1.9 |
| POSTERIOR | 0.784 | 2.225 | 1.6, 1.75, 1.8, 1.9 |
| LATERAL_DER | 0.023 | 2.073 | ninguna |
| LATERAL_IZQ | 0.023 | 2.125 | ninguna |
| TRAS_MANDO | 0.784 | 2.422 | 1.6, 1.75, 1.8, 1.9 |

Se identifican tanto la primera superficie sobre el suelo como el impacto al iniciar un rayo a +1,80 m. Este último puede ser una viga o remate: **no es automáticamente el techo arquitectónico**. Las sondas laterales elegidas chocan con geometría local a las cuatro alturas. Las zonas central, navegación y posterior seleccionadas admiten las poses; una pose correcta no demuestra una ruta entre ellas. El ensayo añade 1,80 m como referencia histórica de Sutherland, sin cambiar personaje alguno.

Los niveles fuente principales son ~0,021205 / 0,297639 / 0,435856 / 0,712296. A escala 1,10, algunas secciones laterales muestran un salto directo de **~0,305 m** entre soporte central y superior, y otra separación de ~0,456 m desde el nivel frontal. En el eje aparecen huellas fragmentadas y ausencia de soporte en puntos concretos. Los rayos horizontales elegidos no describen todas las escaleras; no se aprueba una subida por deducirla del desnivel. Se conservan todas las muestras a 1 cm en `secciones_niveles.csv` y `ergonomia_detallada.json`.

## Asientos y puestos

| Puesto | Superficie medida | Altura sobre soporte m | Poses de aproximación H=1,90 libres / muestreadas |
| --- | --- | --- | --- |
| NAVEGACION | ChamferBox_22 | 0.630 | 0/3 |
| LATERAL_DER | ChamferBox_37 | 0.599 | 1/4 |
| LATERAL_IZQ | ChamferBox_38 | 0.599 | 0/4 |
| MANDO_IZQ | ChamferBox_27 / ChamferBox_28 / ChamferBox_29 | 0.494 | 1/3 |
| MANDO_DER | ChamferBox_34 / ChamferBox_35 / ChamferBox_36 | 0.494 | 1/3 |

La revisión semántica distingue cojín de carcasa: los centrales se miden sobre ChamferBox_27–29 y 34–36, no Box_6/8. La estimación preliminar ~0,642 m correspondía al borde de carcasa y se conserva como resultado sustituido. El asiento central real da ~0,494 m. Las superficies laterales dan ~0,599 m. Navegación da ~0,630 m respecto al rayo de soporte de Object_75; el suelo de los pies vecinos está ~23 mm más alto. Son cotas de superficies muestreadas, no altura cargada de cojín ni dimensiones útiles de una persona sentada.

Se ensayaron tres familias paramétricas de cuerpo H=1,60/1,75/1,90 m: torso/cabeza y pares de muslos/piernas como cápsulas, frente a todos los triángulos externos. Se excluye explícitamente el grupo propio de silla para no confundir contacto con apoyo con un obstáculo externo. Los parámetros de miembros están publicados en `puestos_revision.json`; **no son percentiles ANSUR ni un rig humano validado**. En navegación chocan muslos/piernas con Object_129 en las tres variantes. En los otros cuatro puestos no aparecen contactos externos en esos miembros de referencia; esto no aprueba postura, comodidad ni entrada/salida.

Las plantas de pies hipotéticas quedan elevadas respecto al suelo local ~0,141–0,215 m en navegación, ~0,133–0,207 m en laterales y ~0,029–0,102 m en mando. Señalan que hacen falta ajustes/referencias humanas, no una obligación de bajar todas las sillas por esas cantidades. Se midieron centros de pantallas, alturas y distancias al hombro; una comparación con brazo hipotético 0,38×H no certifica articulaciones, alcance fino, mano, visibilidad ni operación. Las aproximaciones ensayadas son cuatro desplazamientos cardinales de 0,75 m, con ausencia de suelo anotada por separado; no son animaciones de sentarse.

Como criterios externos independientes: OSHA recomienda apoyo completo de pies y posibilidad de ajustar asiento/profundidad; NASA exige estudiar ajuste, alcance y visión para tareas y posturas concretas. Se usan como principios de evaluación, sin afirmar conformidad de estos asientos. [OSHA: sillas](https://www.osha.gov/etools/computer-workstations/components/chairs), [NASA: acomodación antropométrica](https://www.nasa.gov/reference/4-0-physical-characteristics-and-capabilities-vol-2/).

## Accesibilidad
Se ha revisado el alcance físico, no solo el paso de una cápsula de pie. La referencia comparativa CTE DB-SUA contempla puertas de 0,80 m, giro de 1,50 m, altura de umbral 2,00 m y transferencia lateral de cama de 0,90 m; para escaleras generales, huella mínima 28 cm y contrahuella hasta 18,5 cm, con condiciones más estrictas según uso. Se cita únicamente como contraste de escala humana, sin aplicación jurídica a una nave ficticia o al videojuego. [Documento oficial, SUA 1/SUA 2 y anejo A](https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf).

Los giros cilíndricos locales de Ø1,50 ×1,35 m resultan libres en centro de puente, cruce, cabina y centro de habitación, con 8/8 rayos de soporte perimetral; junto a la cama chocan con el proxy. El cilindro se recorta entre +25 mm y +1,35 m y se prueba contra superficies, no volúmenes sólidos certificados. No hay continuidad accesible desde el centro; cambios de nivel, umbrales y aproximación siguen condicionándola. **Grado E para accesibilidad física continua y para acomodación humana completa.** Accesibilidad de UI, control, visión, audición y mareo requieren diseño de juego e intervención humana posterior.

![Asientos medidos](LAMINAS/L03_asientos_medidos.png)
Evidencia: `medidas_puertas.csv`, `alturas_zonas.csv`, `medidas_puestos.csv`, `secciones_niveles.csv`, `puestos_revision.json`, `accesibilidad_camarote.json` y logs 15/18/21. La recomendación es mantener escala provisional y adaptar localmente, sin forzar resultados mediante cápsulas menores.
