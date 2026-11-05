# VOY-04 — Propuesta para Unreal Engine 5.8.2

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Alcance exclusivamente propuesto

No se ha abierto Unreal, importado assets, creado Blueprints, Widgets, Render Targets o lógica CoreRPG. La propuesta se basa en la geometría y la metodología histórica de Sutherland. Su compatibilidad concreta con el proyecto/versión final deberá verificarse en una fase autorizada.

Conservar carcasa de consola y arquitectura como Static Meshes fijas. Mantener Plane_94/95 separadas con UV de origen. Separar guía fija, carro móvil, casquillo, conjunto de asiento y grupo de respaldo, respetando la unión entre cojín y carcasa. Los ejes y matrices de referencia están entregados; convertir expresamente el marco diagnóstico reflejado del maniquí a un sistema de exportación coherente, y metros a centímetros. No hornear a ciegas las transformaciones de la referencia ni exportar todo como una única malla convexa.

## Colisiones e interacción corporal

Crear colisiones simples por pieza o subconjunto que conserven huecos de piernas y espalda. La silla tiene superficies abiertas y capas coincidentes: una envolvente convexa global puede cerrar espacios funcionales. Los triángulos y ensayos de Blender sirven como referencia comparativa, no como receta de colisión de producción. Ensayar obstáculos de control, interfaces internas, suelo real y barridos por todo el recorrido; perfilar coste y contrastar la simplificación contra la referencia.

La cápsula de un personaje de pie no demuestra una postura sentada. Habrá que definir una representación de colisión sentada acorde con el cuerpo, con cambio de estado controlado y comprobaciones de espacio. No resolver un bloqueo apagando toda colisión del puesto o reduciendo arbitrariamente al personaje. La colocación de pelvis/pies/manos debe retargetearse al rig final con longitudes reales, ropa y deformación, repitiendo la evaluación para cada talla.

## Actor y estados propuestos

Un controlador de puesto puede agrupar `Free → Reserved → Approach → Retract → Align → Sit → Occupied → Stand → Exit → Return → Free`, con estados de cancelación y bloqueo. Reservar tanto silla como espacio de transición; impedir órdenes opuestas, dobles ocupaciones y retorno mientras un cuerpo invade el volumen. La animación Blender no implementa estas reglas.

Para NPC persistentes, guardar identificadores estables de puesto y ocupante, regulación de altura y estado seguro; recuperar poses coherentes después de cargar y liberar reservas de actores ausentes. Replanificar acceso si hay obstáculos y comprobar conflictos entre jugador/NPC. No persistir un mero número de frame como sustituto de un estado válido. La regulación individual puede mantenerse al salir; el retorno horizontal de la silla es independiente.

## Animaciones, puntos y consola

Preparar animaciones reales de aproximación con apoyo de pies, orientación, ajuste de silla, sentado, trabajo, retirada de manos, levantado y salida. Resolver equilibrio, pelvis, respaldo, IK de dedos y manejo del dispositivo. La traslación lateral del laboratorio no es una animación final de marcha.

Los anclajes y cámaras de Blender son puntos de partida para aproximación, pelvis sentada, alcance e inspección ampliada. El punto de aproximación está junto al puesto y ya orientado: su conexión con navegación del juego, rutas de VOY-03 y giros debe probarse. Una futura interfaz por pantalla necesita foco/entrada de ratón o mando, mapa de UV y estados de cámara; preservar los LCARS originales hasta diseñar esa capa. Nada de ello está implementado ahora.

## Condiciones antes de promoción

Revisar primero apoyo dorsal, postura de cabeza alta y mecanismo real. Después validar importación/UV/pivotes, colisiones, retarget, movimiento ocupado con los pies, transición de cápsula, obstáculos intermedios, cancelación/reanudación y múltiples NPC. No atribuir a Sutherland o al motor resultados que solo se han muestreado aquí en Blender.
