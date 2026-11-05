# VOY-04 — Animaciones y recorridos experimentales

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Secuencia guardada

Tres escenas 04_PROTO contienen una acción técnica de 301 fotogramas a 24 fps (12,5 s entre primer y último frame). Se anima el rig articulado y el grupo móvil de silla, con claves lineales. La silla inicia y termina en su referencia horizontal; la altura/regulación individual se conserva. El personaje inicia y termina junto al puesto, ya orientado hacia la consola.

| Fotograma | Estado |
| --- | --- |
| 1 | Silla en referencia, personaje junto al puesto |
| 31 | Silla retirada 40 cm, guía libre de mobiliario |
| 61 | Aproximación lateral completada; pie salva guía |
| 91 | Sentado con silla retirada |
| 121 | Desplazamiento ocupado finalizado |
| 151 | Trabajo, manos próximas a pantallas |
| 181 | Manos retiradas |
| 211 | Silla de nuevo retirada |
| 241 | Personaje de pie |
| 271 | Personaje fuera del puesto |
| 301 | Retorno vacío a referencia |

Durante el deslizamiento ocupado se elevan los pies hasta 35 mm y vuelven al suelo. La traslación lateral eleva el pie que cruza la guía hasta 40 mm. Las manos siguen un arco vertical adicional de 16 cm durante el acceso a controles y vuelven por el mismo recorrido. No se exige giro de silla en esta solución. No hay animación realista de marcha, agarrar la silla, empujarla con fuerza o activar la regulación.

## Qué se comprobó

Para cada talla se compararon 301 poses analíticas con los ejes del rig reabierto y se comprobaron otras 300 poses en mitad de los intervalos de Blender. Se evaluaron pelvis, tronco, cabeza, brazos, manos, muslos, pantorrillas y pies frente a los triángulos de silla y entorno, incluida la guía nueva. Resultado final: 1803 posiciones sin penetraciones principales por encima de 2 mm del proxy. La silla pasó 81 posiciones de traslación por talla (243 poses), con SAT de 17 ejes tras BVH; no hubo contactos externos. La ida/vuelta simétrica no se cuenta como otro experimento independiente.

Estos son **ensayos discretos densos**, no un barrido continuo certificado, ni un solver físico o biomecánico. Se conservan los resultados por altura, frame, miembro, objeto y triángulo. El chequeo de pertenencia a un sólido no es concluyente para objetos abiertos/no manifold; las superficies se tratan a doble cara. No se declara ausencia de todo contacto interno.

## Fallos y correcciones

La pose original falla en asiento/consola y pies. A1 añadió guía y carro, pero el pie derecho atravesaba la guía en 10/12/10 poses de las tallas 1,60/1,75/1,90. Se conserva el fallo en `trayectorias_A1_FALLO_GUIA.json` y Blender de evidencias; se corrigió elevando el pie.

A3 acercaba las manos por una línea que atravesaba el canto y las pantallas en 10/10/8 poses. La posición final era válida; la transición no. `trayectorias_A3_FALLO_MANOS.json` conserva esa trayectoria. El arco elevado corrigió los subtramos ensayados. Las versiones rechazadas no se incluyen en los recuentos finales positivos.

## Revisión visual

`ANIMACIONES/VOY04_001.png` … `VOY04_301.png` cada tres fotogramas son renders reales Blender. GIF y WebP reúnen esos 101 PNG a unos 125 ms por imagen (GIF alterna 120/130 ms); no representan un muestreo adicional. `LAMINA_SECUENCIA.png` selecciona diez poses con rótulos exteriores al render. Las secciones de consola son cortes visuales sobre copias de render, nunca una eliminación de obstáculos para la prueba de colisión.

La primera exportación visual repetía una pose por mantener otra escena activa. Se rechazó y regeneró desde la escena correcta (script 19); el script 20 contrasta hashes de píxeles y cantidad de frames de GIF/WebP. Ese error de exportación no afectó a los ensayos del rig guardado. La secuencia final verificada sustituye la exportación rechazada.

![Secuencia](CAPTURAS/LAMINA_SECUENCIA.png)
