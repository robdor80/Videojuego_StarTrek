# VOY-03 — Preparación técnica para UE5

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Estado de esta fase

1. **Prueba geométrica en Blender:** superada para las rutas y cápsulas documentadas.
2. **Viabilidad estimada en Unreal:** favorable si la importación conserva la arquitectura y las colisiones representan los apoyos reales; todavía estimación.
3. **Validación real en Unreal:** pendiente. No se abrió ni modificó Unreal Engine 5.8.2, ningún proyecto UE ni CoreRPG.

## Colisiones propuestas por tipo de pieza

| Piezas / función | Preparación futura propuesta | Condición de contraste |
| --- | --- | --- |
| Mesh_1728 foso; floorfront_1 anillo; Mesh_1857 centro; Mesh_1859 pasarela | Colisiones simples separadas por regiones cóncavas y niveles, espesor constructivo local | No cubrir el foso, escaleras, vanos ni huecos con un único convexo general |
| Mesh_1860–1863 huellas laterales | Prismas ajustados a cada huella y contrahuella; conservar alturas y profundidad | Repetir las rutas incluyendo aproximación a barandillas y narices |
| Mesh_1856 marcos; Mesh_1739/1740/1755/1807–1811 remates | Separar función de apoyo y detalles salientes, manteniendo el volumen visual real | No suprimir la nariz que producía contacto; no inventar una rampa sobre un hueco |
| Mesh_2121–2124 rejillas; Mesh_1968 /1848 relleno y placa | Reconstruir colisión según la superficie realmente existente y su soporte; revisar normales | No rellenar huecos no medidos ni duplicar planos para simular suelo |
| Mesh_1787/1788 y demás consolas | Colisión de obstáculo por panel/volumen, sin rol de suelo transitable | Conservar espacio de rodillas y separación real; no convertir tapas en rutas |
| Barandillas y montantes | Convexos o prismas estrechos por elemento importante | Validar hombros, barrido lateral y giro, sin cerrar el paso con un bloque global |
| Módulos de pasillo y AD_* existentes | Suelo, pared, techo y marco separados; reutilizar matrices R1 | Repetir ambos itinerarios completos y la unión exacta posterior |
| Hojas de puerta | Pivote/raíz local por hoja completa y grupo móvil | Fase posterior de carrera y alojamiento; abierto estático no equivale a mecanismo válido |
| Sillas y muebles | Mantener bases fijas y grupos móviles identificados por el trabajo previo | Aproximación validada no significa asiento usable; pivotes/interacción siguen pendientes |

Las normales hacia abajo de varias huellas y rejillas deben revisarse antes de depender de superficies de una cara. No se voltearon ahora. Una colisión simple puede diferir del detalle visible en pocos milímetros y consumir el margen ensayado; comparar de nuevo el modelo de colisión con las secciones de VOY-03. Una simplificación no debe crear apoyos donde no los hay.

## Parámetros de referencia para un futuro laboratorio autorizado

Metros Blender y conversión explícita a centímetros de motor. Radio 35 cm; alturas totales 160 /175 /190 cm; semialturas 80 /87,5 /95 cm. Conservar referencia 1,10 aplicada al puente y matrices de módulos existentes; no duplicar conversiones de escala.

Contrahuella de laboratorio máxima 18 cm, frente a las medidas nominales 15,20 cm. Es una hipótesis de capacidad ambulante para comparar, no un valor configurado o certificado de CharacterMovement. Probar primero ese límite con el personaje y colisión reales; no empezar permitiendo 30–45 cm para ocultar un fallo. Pendiente a estudiar posteriormente: 40° como hipótesis de comparación; las huellas de esta fase son casi horizontales y no se ensayó una rampa de 40°. La inclinación media de la línea de escaleras no sustituye la medición de sus peldaños.

En VOY-03 se exigieron planos de apoyo casi horizontales (|normal Z|>0,999, unos 2,56°), cambios de suelo ≤18 cm, apoyo inferior real y barridos de cápsula. Ese algoritmo no reproduce gravedad, aceleración, fricción, velocidad, ajuste del pie ni el algoritmo de subida del motor. El desplazamiento vertical de una cápsula redondeada sobre narices tampoco es una animación de pies humanos.

## NavMesh y aceptación futura

Comprobar generación de regiones en foso de navegación, ambos vuelos laterales, plataforma central, entorno de sillones, pasarela y salida posterior, además de cada adaptador y ambos destinos. Contrastar radio, altura y escalón del agente con los tres cuerpos de referencia. Revisar todas las transiciones y áreas de puerta abiertas/cerradas; un enlace especial no debe ocultar falta de suelo.

El futuro criterio de aceptación debe repetir subida y bajada con personaje real, varias velocidades y aproximaciones, detención en huellas, colisión de cabeza/hombros, giro y retorno. Conservar negativos y comparar con los puntos de VOY-03. No se exportaron activos ni se implementó nada de esto durante esta misión.
