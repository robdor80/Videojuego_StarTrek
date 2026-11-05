# VOY-05A — Propuesta conceptual de interfaz

Propuesta para revisión, **sin implementación ni norma dimensional definitiva**. Cada instalación enlaza arquitectura, contorno de hueco, adaptador opcional, marco/cassette, hojas, guías, controles y decoración. El mecanismo recibe parámetros de recorrido y estados sin depender de nombres de malla Voyager.

La raíz local se sitúa en el centro del umbral terminado. +Z es arriba; +X es normal hacia el destino documentado; +Y completa la base y es tangente al deslizamiento. Para una doble candidata, hoja izquierda abre hacia −Y y derecha hacia +Y vistas según el contrato de normal. El inventario conserva `center_world` de contorno (centro de envolvente, excepto las tres raíces históricas del puente en suelo), `floor_z`, normal y tangente: no se deben confundir sus centros con un pivote ya implementado.

Parámetros propuestos:

| Grupo | Datos necesarios |
| --- | --- |
| Hueco | Perfil 2D ordenado, W/H de envolvente, anchos a distintas alturas, cota de suelo, rango de profundidad útil y tolerancias |
| Montaje | Transformación de raíz a arquitectura; puntos de jamba izquierda/derecha y dintel; patrón de fijaciones definido por adaptador |
| Marco | Profundidad frontal/posterior, espesores, sellos, remates, máscara del contorno y zonas que no se deben recortar |
| Hojas | Uno o más subensamblajes, geometría local, volumen sólido, solapes, posición cerrada, transformaciones abiertas y límites |
| Recogida | Dos o más volúmenes reservados, guías físicas, fondo, retornos y acceso de mantenimiento |
| Circulación | Prisma/perfil libre, radio/altura de personaje objetivo, zonas de aproximación y ocupación, soporte y destino existente |
| Interacción | Puntos para controles y sensores; referencias locales, permisos y estado de destino; desacoplados de LCARS/materiales |
| Apariencia | IDs de superficies y materiales, UV, decoración/sonido y variantes por nave |

Los puntos propuestos son semánticos; sus coordenadas se derivarán del perfil y del cassette elegido, no de una tabla universal de metros. La profundidad puede ser asimétrica. Una puerta puede compartir tipo mecánico con otra y necesitar adaptador distinto. La interfaz debe rechazar instalación si su recorrido/cavidad o paso no caben en la arquitectura.

Adaptación: conservar transformaciones rígidas de arquitectura; dimensionar nuevo hueco según cada nave; definir nuevos montajes y geometría; recalcular hojas, guías y espacios; validar límites antes de compartir comportamiento. No se ha creado un objeto Root, socket, articulación, animación ni volumen de colisión. Este documento prepara B/C sin ejecutar esos trabajos.
