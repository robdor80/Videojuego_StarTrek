# VOY-03 — Pruebas de cápsulas

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Protocolo y resultados

Alturas totales 1,60 / 1,75 / 1,90 m, radio invariable 0,35 m, eje vertical. Semiesferas y segmento central se calculan analíticamente; los polígonos de las cápsulas Blender son solo representación visual. No se redujo el radio ni se cambió silenciosamente el cuerpo. Se ejecutaron los 39 casos, con 48090 poses y 48051 intervalos. El contador suma los tres tamaños; las huellas de apoyo coinciden entre tamaños y esa igualdad se verifica.

| Recorrido | Longitud 3D m | Poses por altura | Resultado geométrico |
| --- | --- | --- | --- |
| CENTRO_A_PASARELA | 8.330 | 832 | Superado original · tres alturas · ida/vuelta |
| CENTRO_A_NAVEGACION | 6.047 | 607 | Superado original · tres alturas · ida/vuelta |
| NAVEGACION_A_PASARELA | 14.302 | 1451 | Superado original · tres alturas · ida/vuelta |
| CENTRO_A_MANDO_IZQ | 1.664 | 173 | Superado original · tres alturas · ida/vuelta |
| CENTRO_A_MANDO_DER | 1.664 | 173 | Superado original · tres alturas · ida/vuelta |
| PASARELA_A_POSTERIOR | 5.132 | 533 | Superado original · tres alturas · ida/vuelta |
| ESCALERA_DERECHA | 1.700 | 156 | Superado original · tres alturas · ida/vuelta |
| ESCALERA_IZQUIERDA | 1.699 | 156 | Superado original · tres alturas · ida/vuelta |
| ESCALERA_NAV_CENTRAL | 1.110 | 101 | Superado original · tres alturas · ida/vuelta |
| CENTRO_PUENTE_AL_TURBOLIFT | 31.542 | 3177 | Superado original · tres alturas · ida/vuelta |
| REGRESION_PUENTE_AL_TURBOLIFT | 23.212 | 2345 | Superado original · tres alturas · ida/vuelta |
| CENTRO_PUENTE_AL_CAMAROTE | 35.544 | 3579 | Superado original · tres alturas · ida/vuelta |
| REGRESION_PUENTE_AL_CAMAROTE | 27.214 | 2747 | Superado original · tres alturas · ida/vuelta |

Todos los casos finales: **Superado sobre geometría original de trabajo**. No hay rutas que dependan de adaptación. Los resultados negativos de versiones anteriores siguen presentes y su clasificación provisional no debe confundirse con el estado final.

## Qué se comprueba entre poses

La búsqueda de rejilla de 10 cm solo propone candidatos. Se refinan a separación XY máxima 1 cm; los extremos solicitados se conservan expresamente. Cada intervalo lineal se comprueba como un volumen continuo: el segmento central vertical de la cápsula barre un cuadrilátero, cuya distancia exacta a cada triángulo próximo se calcula con vértices, aristas e intersecciones de caras. Se resta el radio 0,35 m. No se acepta un enlace solo porque sus dos poses estén libres.

Umbrales de barrido: 0,5 mm respecto a terreno y 3 mm respecto a otros obstáculos; selección de poses con separación 4 mm del terreno y umbrales de 1 / 5 mm. El mínimo final de todos los casos es aproximadamente 3,90 mm, principalmente próximo al suelo. Los 20 µm de contraste guardado quedan por debajo de esos márgenes, pero la prueba no garantiza tolerancia a futuras simplificaciones de colisión.

Para acreditar apoyo continuo se identifica, en cada intervalo, al menos un triángulo real situado al menos 0,179 m por debajo de ambos centros de la esfera inferior. Ambos extremos están a distancia ≤0,358 m del mismo triángulo. La distancia a un triángulo convexo es convexa a lo largo del segmento: todo el intervalo queda a ≤radio+8 mm, con componente vertical de contacto ≥0,50. El barrido impone simultáneamente que no hay penetración. No se crea una superficie entre triángulos. Todos los intervalos finales satisfacen el certificado sin subdivisión adicional.

El espacio de giro de una cápsula circular no cambia con el yaw; en las posiciones y trayectorias validadas su giro axial conserva el volumen libre. No se certifican brazos extendidos, locomoción de cuerpo articulado, adelantamiento de dos personajes ni giro de silla de ruedas.

## Ida y vuelta

Invertir una polilínea reproduce exactamente el mismo conjunto de cápsulas, obstáculos y apoyos. Se conserva el orden inverso y se aplica la misma cota absoluta de 18 cm para subida y bajada. Así se acredita la reversibilidad geométrica bajo esta hipótesis simétrica. No se ha ejecutado una simulación dinámica independiente de descenso; la futura gravedad, velocidad y resolución de contactos del motor pueden diferir.

Datos: `resultados_rutas.csv`, `rutas_puntos.csv`, `barridos_resultados.json`, `apoyo_continuo.json`. Los resultados contienen todos los puntos inferiores de cápsula y los niveles de suelo. [Comparativa de tres alturas](LAMINAS/06_tres_alturas.png).
