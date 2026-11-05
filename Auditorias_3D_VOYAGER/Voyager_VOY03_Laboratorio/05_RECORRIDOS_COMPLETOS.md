# VOY-03 — Recorridos completos

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

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
