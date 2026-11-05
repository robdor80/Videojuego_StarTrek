# VOY-03 — Escalones y desniveles

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Perfiles laterales completos

| Tramo | Ascenso | Contrahuella cm | Huella de referencia cm | Apoyos OBJ |
| --- | --- | --- | --- | --- |
| DERECHA | 1 | 15.204 | 24.32 | floorfront_1 → Mesh_1860 |
| DERECHA | 2 | 15.205 | 24.32 | Mesh_1860 → Mesh_1862 |
| DERECHA | 3 | 15.204 | 24.32 | Mesh_1862 → Mesh_1859 |
| IZQUIERDA | 1 | 15.204 | 24.50 | floorfront_1 → Mesh_1861 |
| IZQUIERDA | 2 | 15.205 | 24.50 | Mesh_1861 → Mesh_1863 |
| IZQUIERDA | 3 | 15.204 | 24.50 | Mesh_1863 → Mesh_1859 |

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
