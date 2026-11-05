# VOY-03 — Diagnóstico de circulación

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

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
