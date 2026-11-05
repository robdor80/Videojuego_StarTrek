# VOY-05A — Dimensiones y escalas

Se usa **1 unidad de mundo Blender = 1 m de trabajo**. El `scale_length` observado es 1,0, con sistema métrico. Es una convención de trabajo del recurso; no certifica dimensiones canónicas o antropometría final. Se conservan matrices fuente sin aplicar normalizaciones a las mallas. No se aplica por costumbre ni ×100 ni ×0,01.

| ID | Vano mínimo muestreado original m | A 1,10 experimental m | Hojas originales: ancho × alto × espesor de envolvente m |
| --- | --- | --- | --- |
| BR_01 | 0.7572 × 1.7756 | 0.8330 × 1.9531 | 0.3786 × 1.7758 × 0.0425 / 0.3786 × 1.7756 × 0.0425 |
| BR_02 | 0.7572 × 1.7756 | 0.8330 × 1.9531 | 0.3786 × 1.7756 × 0.0425 / 0.3786 × 1.7756 × 0.0425 |
| BR_03 | 0.7583 × 1.7756 | 0.8341 × 1.9531 | 0.3786 × 1.7756 × 0.0425 / 0.3786 × 1.7756 × 0.0425 |

Los vanos del puente se miden sin mover hojas: el cálculo de rayos omite sus triángulos y examina siete planos normales entre −80 y +80 mm, a cinco alturas. Se registra el mínimo hallado, sin afirmar continuidad entre muestras ni un prisma rectangular libre. Todos los valores están en el JSON, incluidos los rayos sin respuesta. La altura BR_04 de 1,7756 m y ancho 0,7583 m proceden de un borde no cíclico, error de plano ≈11 mm: son envolventes, grado E para vano mínimo.

El factor **1,10 es exclusivamente experimental** en la columna de comparación. La escena de auditoría conserva 1,00. A 1,10 la altura lateral ronda 1,953 m: deja aproximadamente 53 mm nominales sobre 1,90 m, antes de tolerancias, cascos, pendientes y colisión. No es una aprobación de paso. La transformación MAX/OBJ ≈1,50813535 pertenece a versiones de recurso, no se adopta como nueva escala humana.

Frentes modulares: estándar ≈1,0341×2,1935 m; residenciales inclinados ≈1,0341×2,5237 m; asimétrico ≈2,2210×2,5263 m; Mesh55 ≈2,0681×2,5249 m. **Son caras de cierre, no medidas de vano útil.** El espesor normal casi cero de `front_surface_envelope` describe la coplanaridad de las caras: no el espesor de una hoja. No se usa ese cero como espesor físico.

Los contornos de bocas de pasillo suelen alcanzar ≈2,9613×2,8164 m de envolvente; hay molduras y perfiles estrechados, por lo que deben consultarse `widths_by_height`. Las entradas Mesh4/5/6 miden ≈1,0798×2,2034 m de envolvente. Su cota de catálogo inferior es ≈1,1102 m; otras salas empiezan en ≈0,2380 m. Los módulos técnicos elevados conservan niveles ≈3,2792 m. Estas cotas no implican escaleras construidas ni un suelo de cubierta común.

Los conductos Jefferies tienen secciones de altura ≈0,9144 m; escotillas pequeñas ≈0,768–1,102 m. Su adaptación a personaje agachado o reptando está fuera de A. Las dos dimensiones de `boca_vertical` y del registro de techo son X/Y horizontales; no se interpreta su segundo valor como altura de pie.

La profundidad exacta de cada marco integrado y los tamaños individuales de hojas fusionadas quedan E: no hay pertenencia de caras inequívoca que permita medirlos como piezas físicas sin hacer la separación de B. Se entregan coordenadas, planos, caras frontales y envolventes fuente para realizarla posteriormente. Esa falta no se oculta con medidas de caja del pasillo.
