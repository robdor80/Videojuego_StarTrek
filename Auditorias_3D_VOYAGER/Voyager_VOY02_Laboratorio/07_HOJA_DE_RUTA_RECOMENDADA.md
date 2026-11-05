# VOY-02 — Hoja de ruta recomendada
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Orden de trabajo y criterios de salida
El objetivo sigue siendo un puente excelente, pocos pasillos creíbles, acceso al puente/turbolift y un camarote funcional. No extender cubiertas ni convertir toda la biblioteca. Los bloqueos principales son circulación entre niveles, ergonomía de puestos, puertas con alojamiento y coherencia entre familias. Resolverlos antes de PBR general o sistemas de juego.

| Prioridad | Trabajo Blender autónomo propuesto | Evidencia exigida antes de cerrar |
| --- | --- | --- |
| 1 | Medir escalones y rutas desde centro/navegación; probar alternativas locales visibles de peldaños/rampa o redistribución en copias | Recorrido continuo desde origen explícito, cápsulas 1,60/1,75/1,90 y soporte; subida no inferida de teletransporte |
| 2 | Un puesto de navegación y un sillón de mando completos, con base/cojines/respaldo y cuerpo adecuado | Ajuste de pies/rodillas, torso, alcance y visión; entrada/salida; cada articulación y contexto ensayados |
| 3 | Una puerta posterior completa con bolsillos, guías y encuentro AD_PUENTE | Trayectorias de hojas enteras sin cruces, vuelta, umbral ocupado; volúmenes de alojamiento acreditados |
| 4 | Terminar uniones B01 y una unión C representativa, con perfiles reales | Molduras, suelo/techo, espesores y colisiones sin vacíos/falsos bloqueos; mismas matrices reproducibles |
| 5 | Camarote A/Mesh4 como estancia piloto y mobiliario útil | Acceso completo, puerta, rodillas/escritorio, llegada a cama/almacenamiento y giro donde se requiera |
| 6 | Preparación visual localizada y exportación de prueba | UV/materiales conservados, unidades y pivotes verificados; política de slots y texturas por uso |

Los trabajos propuestos no se han iniciado por entregar la hoja de ruta. La autorización de VOY-02 no se convierte en permiso para modificar originales o proyectos UE.

## Decisiones artísticas del usuario
Elegir fidelidad canónica frente a ajustes de escala humana, sensación de amplitud del puente, tratamiento de los cambios de nivel, qué puestos usarán NPC/jugador, arquitectura del camarote y LCARS/interacción visual. La escala 1,10 queda como referencia provisional, no decisión irreversible. Aprobar un módulo de molduras y una estación piloto antes de extender apariencia. Conservar referencias originales para que los cambios locales puedan compararse visualmente.

## Pruebas UE5 futuras, separadas del principal
Crear un laboratorio independiente autorizado y verificar primero importación en centímetros/escala 1 sin multiplicar 100 otra vez, UV/orientación, pivotes y colisión por pieza. Después: CharacterMovement real subiendo/bajando, aproximación a sillas, puertas barridas con actores/ocupante y concurrencia, NavMesh con rutas completas y tratamiento de puertas cerradas. Una cápsula Blender o una ancla coincidente no sustituye esas pruebas. Fijar el personaje Voyager antes de cambiar parámetros: los valores históricos de Sutherland no son especificación del nuevo juego.

Medir GPU/CPU y texturas con cámara, resolución y escalabilidad documentadas. Validar Surface Cache, reflejos, transparencias y legibilidad LCARS. Solo después, decidir Nanite/LOD, instancias, reducción selectiva y límites de texturas; no inventar FPS a partir de triángulos. Ninguna integración en el proyecto UE principal sin autorización expresa.

## Reutilización conceptual de Sutherland
Reutilizar metodología: raíz local de puerta, agrupaciones móviles con base fija, separación entre intención/permiso/ocupación, contactos y pruebas de ida/vuelta; validación de colisiones simples contra arquitectura visible; recargas y pruebas funcionales con personaje real. Adaptar conceptos, no copiar carreras, 30 cm de sillas, convexos, vanos o parámetros sin medir Voyager. No mover ni ejecutar nada en Sutherland. Sus informes históricos siguen pendientes de la revisión humana que documentan.

## Sistemas futuros del videojuego
Interacción de consolas y cámaras de acercamiento; ocupación de asientos y animaciones; NPC con aproximación/espera/cesión; eventos de puertas y permisos; CoreRPG; turbolift con transporte y destinos; persistencia y accesibilidad de entrada/UI. Son dependencias futuras, sin implementación VOY-02. La existencia de una cabina, pantalla o silla 3D no significa que el sistema exista.

## Qué conviene posponer
Conductos Jefferies explorables, mantenimiento vertical, todas las estancias secundarias, puertas sin destino, cubiertas completas, restauración de todas las versiones MAX, rehacer toda la colección, optimización general sin perfil y decoración final antes de asegurar circulación. Una nave menor y coherente reduce incertidumbre frente a una red extensa sin puestos funcionales.

## Próximo encargo técnicamente acotado
Se recomienda un laboratorio de circulación y puesto piloto que use este estado y sus evidencias, conserve originales y mantenga cambios reversibles. Su resultado debería permitir decidir el tratamiento visible de escalones y navegación con referencias humanas. La restauración artística o integración UE requiere un encargo posterior; este cierre no las ejecuta.
