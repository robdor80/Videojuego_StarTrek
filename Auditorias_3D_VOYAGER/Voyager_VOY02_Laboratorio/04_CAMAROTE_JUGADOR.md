# VOY-02 — Camarote del jugador
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Recurso realmente disponible
Mesh4 / Group4 es una envolvente existente de aproximadamente 8,628 ×6,676 ×2,763 m a escala de catálogo. El sondeo previo 7×7 registró suelo y techo en 49/49 puntos: suelo fuente Z≈1,110166 y techo ≈3,87327. Su entrada X− mide ~1,079792 m a alturas 0,4/1,0/1,7 m y ~0,80679 m a 2,2 m. No se infiere un vano rectangular completo, estanquidad o colisión sólida válida de esas muestras.

En el conjunto, la pieza se rota +90° y se enlaza mediante AD_CAMAROTE. La escena D sitúa la misma habitación alrededor del origen, con pasillo de entrada y adaptador. El alcance no identifica esta habitación como camarote canónico de Voyager ni aprueba su forma artística.

## Comparación de estrategias

| Alternativa | Grado de evidencia | Evaluación |
| --- | --- | --- |
| A_ADAPTAR_MESH4 | C | Preferred spatial basis: existing shell, selected capsule route and floor/ceiling evidence; supply artistic fit, independent furniture, door and collision design. |
| B_FABRICAR_CON_MODULOS | E | Not fabricated in VOY-02; measured corridor interfaces can supply access, not proof of a complete room. |
| C_ESTANCIA_NUEVA | E | Artistically flexible; would require new room construction, UV/PBR, architecture and full spatial tests. No new production room created. |

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
