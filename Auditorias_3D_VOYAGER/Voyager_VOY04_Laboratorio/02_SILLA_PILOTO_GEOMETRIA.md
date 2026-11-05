# VOY-04 — Silla piloto: geometría y preparación

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Elección

Se elige CONN/navegación. Sus ocho objetos forman un conjunto sencillo: `MSB_30191` pedestal inferior; `MSB_30194` vástago superior; `Object_77` carcasa de asiento; `ChamferBox_22` cojín; `MSB_30192` y `MSB_30193` soporte de respaldo; `Object_76` carcasa de respaldo y `Layer__3` tapizado. No tiene reposabrazos que haya que inventar o animar. Su consola original ofrece dos pantallas centrales separadas.

La envolvente completa es aproximadamente 0,653 × 0,718 × 1,274 m. El cojín mide aproximadamente 0,534 × 0,534 × 0,032 m de envolvente, con centro superficial a Z=0,629890 m. La cara inferior, el relieve del cojín y el borde frontal impiden tratar todo ese rectángulo como superficie útil plana. `inventario_medidas.json` conserva extremos y dimensiones por objeto.

## Jerarquía preparada

`CTRL_DESLIZAMIENTO` lleva el casquillo inferior y el carro. `CTRL_ALTURA`, hijo de ese control, lleva el conjunto superior. `CTRL_RESPALDO`, hijo del control de altura, lleva soporte, carcasa y tapizado del respaldo. La guía nueva y el suelo quedan fuera del grupo móvil. Las capas de cada cojín/carcasa se mantienen juntas. La escena 02 conserva la pose original con pivotes corregidos; las escenas 04 aplican el experimento.

Se recalculó el origen de cada copia con compensación de coordenadas de vértices y conservación de su matriz mundial. Error máximo de la preparación de pivotes <20 µm, con valores por pieza en `manifest_blender.json`, sección `chairs`. No se aplicaron indiscriminadamente escalas o rotaciones. Las matrices anteriores, posteriores y los controles están registradas; sus matrices se refieren al estado de montaje, antes de aplicar la animación/regulación.

La base diagnóstica de cálculo es `[lateral heredado, delante, arriba]`, de determinante −1. El control de silla usa `[lateral heredado, atrás, arriba]`, de determinante +1. Se entregan ambas matrices explícitas; **no exportar automáticamente el marco reflejado del maniquí a Unreal**. La traslación del puente heredada de VOY-03 es `[-1.310244083404541, -7.020256042480469, -0.7835251092910767]` m. No se cambia la corrección de importación +90° X ni el factor provisional 1,10.

## Cambios experimentales

| Altura humana | Descenso del asiento | Asiento sobre suelo de pies | Retirada | Distancia tronco–respaldo | Mirada descendente al centro |
| --- | --- | --- | --- | --- | --- |
| 1.60 m | 21.54 cm | 39.12 cm | 40 cm | 7.59 cm | 30.6° |
| 1.75 m | 17.83 cm | 42.82 cm | 40 cm | 6.72 cm | 40.4° |
| 1.90 m | 14.13 cm | 46.53 cm | 40 cm | 5.84 cm | 48.2° |

Los descensos son regulaciones de la silla, no escalados del personaje. El casquillo inferior original era demasiado largo para esos descensos; en la copia experimental se remapea solo su cota Z entre el apoyo nuevo Z=0,048326 m y la parte superior `Z_asiento_original − descenso − 0,080 m`. Se conservan topología y UV de esa copia, aunque la proporción axial cambie. La referencia conserva la pieza completa sin modificar.

Se añade una guía estrecha de 7 cm de ancho y un carro de 15 × 16 cm. Sus cotas están en `bodygeom.py`, función `rail`, y las mallas reales en Blender. Son propuestas para estudiar el volumen ocupado; no hay diseño de rodamientos, topes, anclajes o carga física. Su contacto carro–guía se registra como interfaz específica, sin excluir el resto del mobiliario.

Se ensayaron retiradas de 20–60 cm. 30 cm falla para las tallas 1,75/1,90; 40 cm es el menor valor común que pasa la serie de 10 cm. No se buscó un mínimo continuo. No fue necesario girar la silla ni crear reposabrazos. La corrección de altura resuelve el espacio de piernas sin cortar la consola. No demuestra que sea la única solución: reposapiés u otros ángulos podrían estudiarse para conservar la cota, pero no se han validado. El respaldo se adelantó 18 cm, pero todavía queda una separación de 5,8–7,6 cm al tronco: ajuste de apoyo pendiente.

## Conservación y resultado

Las 8 piezas originales están preservadas en referencia. Siete se trasladan rígidamente en la copia adaptada; solo se reconstruye axialmente el casquillo inferior. La geometría de consola y arquitectura guardada no cambia. 1184 copias verificadas conservan UV/materiales y datos independientes, con error esperado máximo 2.14 µm. No se acredita un mecanismo físico por esa coincidencia.

![Despiece](CAPTURAS/B05_DESPIECE_REAL.png)
![Pivotes](CAPTURAS/B06_PIVOTES_Y_CONTROLES.png)
