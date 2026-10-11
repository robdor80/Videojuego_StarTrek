# IDEA-0002 — Biblioteca musical personal en los camarotes

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación:** 2026-10-11  
**Estado:** APROBADA (diseño) — pendiente de planificación técnica e implementación  
**Decisión del autor:** aprobada expresamente el 11-10-2026 («luz verde»), con aclaración específica de que la importación es **local desde el MSI**.  
**Plataforma inicial:** Windows, PC del jugador (MSI).  
**Relación:** ordenador de la nave, interacción por voz, camarotes personales, ocio, audio espacial, persistencia de preferencias.

## 1. Visión aprobada

Permitir que el jugador escuche en su camarote **su propia colección musical** de archivos **MP3 y FLAC** desde el ordenador MSI, mediante peticiones de voz al ordenador de a bordo y controles de reproducción manuales.

Ejemplo: al regresar al camarote después de una guardia, el jugador dice «Computadora, reproduce Dire Straits»; el ordenador encuentra las canciones **disponibles en su biblioteca local** y las reproduce por los altavoces virtuales del camarote. Puede seguir interactuando con el mundo, usar el replicador, consultar el PADD, sentarse o descansar.

**Principio esencial aprobado:** los archivos del usuario se seleccionan/importan **desde el almacenamiento local del MSI**. No se envían ni suben a servidores, GitHub, Firebase, nube, servicios de IA ni a ningún repositorio del proyecto. El término «importar» designa registrar archivos locales y, opcionalmente, copiarlos dentro del almacenamiento local privado del juego.

## 2. Modos de importación y valor predeterminado

El juego proporcionará un menú **Importar música** que permita seleccionar archivos sueltos o carpetas completas de Windows:

1. **Vincular carpeta (predeterminado):** indexar y reproducir desde su ubicación original, **sin duplicar los MP3/FLAC**. Permitir añadir varias carpetas y volver a escanearlas.
2. **Copiar a biblioteca (opcional y explícito):** copiar archivos seleccionados a una carpeta local privada del juego, accesible únicamente como recurso del usuario, sin enviarlos fuera del MSI.

El índice musical guardará referencias a rutas locales, metadatos y estado de disponibilidad. La ubicación concreta del almacenamiento privado debe definirse conforme a las convenciones de Windows/UE5 en la implementación; no se fija aquí una ruta absoluta.

El usuario podrá consultar y gestionar su biblioteca: añadir, quitar del índice, actualizar catálogo y resolver archivos movidos o eliminados. **Quitar del índice nunca debe borrar originales por defecto**; cualquier eliminación física requeriría una acción independiente y confirmación clara.

**No duplicar gigabytes innecesariamente.** El modo de vinculación es la experiencia por defecto aprobada.

## 3. Catálogo musical y búsqueda

El juego indexará, cuando existan, metadatos locales (etiquetas ID3/Vorbis/FLAC según formato): título, intérprete, álbum, género, número de pista, duración e imagen de portada si está disponible. Si faltan etiquetas, usar nombre de archivo y directorio como información de respaldo **sin inventar datos**.

Se podrán consultar y reproducir canciones, artistas, álbumes, géneros y listas de reproducción personales. Se proponen búsqueda textual, favoritos, aleatoria, repetición, cola y «reproduce mi lista de favoritos».

Si hay varias coincidencias, pedir una aclaración breve o usar una regla de selección visible y consistente. Si no existe música coincidente, el ordenador **no debe fingir** que ha encontrado o reproducido algo.

Una biblioteca local no equivale a un catálogo de streaming. No se necesitan licencias o credenciales de Spotify ni otra plataforma externa para la función básica.

## 4. Interacción natural con el ordenador de la nave

Aprovechar **Starship Computer** existente, que ya contempla órdenes desde camarotes por voz o terminal, su carácter conciso y la separación entre interpretación y ejecución.

Ejemplos:
- «Computadora, reproduce Queen».
- «Pon Sultans of Swing».
- «Reproduce mi lista de favoritos».
- «Pon música relajante», cuando existan etiquetas/listas apropiadas que permitan resolver la petición.
- «Siguiente canción», «pausa», «continúa», «para la música», «baja el volumen».

**Estrategia:** órdenes simples mediante reconocimiento determinista de intenciones; usar IA cuando haga falta desambiguar peticiones complejas. La IA trabaja **sobre títulos y metadatos permitidos**, no necesita recibir el contenido de los archivos de audio. La decodificación y reproducción de MP3/FLAC ocurre localmente.

La transcripción de voz podría depender del proveedor o la tecnología elegida; si se usa un servicio remoto de transcripción/interpretación, deberá aplicarse la política de privacidad y ofrecer modo manual/local. **Nunca enviar los archivos musicales a una API remota**.

### Contrato conceptual (no API real acordada)

```json
{
  "action": "personal_audio.play",
  "scope": "player_quarters",
  "query": {
    "artist": "Dire Straits"
  }
}
```

Este JSON es solo un ejemplo para orientar la futura definición del contrato. Los nombres de acciones/campos, autorizaciones y adaptadores se cerrarán en F02 sin inventar APIs ni implementaciones de Core RPG.

## 5. Reproducción real dentro del mundo UE5

La música debe salir de un **emisor sonoro situado en el camarote** y comportarse como audio ambiental diegético, no como banda sonora global que sigue al personaje.

Comportamiento objetivo:
- Dentro del camarote se oye la música desde el equipo/altavoces virtuales.
- Al alejarse se atenúa; con la puerta cerrada, la oclusión/amortiguación reduce o impide la escucha según la configuración acústica definitiva.
- Fuera del camarote el sonido no «persigue» al jugador.
- Si el reproductor permanece activo, al regresar debe continuar en el punto temporal correspondiente, según las reglas de simulación y pausa.
- Los controles de volumen, reproducción, pausa, salto de pista y parada deben responder de manera coherente.

Usar herramientas de audio de UE5 (emisor, atenuación, espacialización, oclusión y mezcla de buses, según la plataforma/versión). **No se declara resuelto el soporte de MP3/FLAC en caliente**: comprobar codecs y plugin/adaptador de reproducción en tiempo de ejecución, versiones, licencia, streaming, memoria y pruebas en build empaquetada. No presupone que una importación de assets hecha en el editor sea suficiente para archivos escogidos por el jugador durante una partida.

Durante una alerta roja, comunicaciones prioritarias o eventos de seguridad, el sistema podrá atenuar, pausar o detener la música según políticas de la nave que deberán acordarse; mantener la prioridad de sonidos críticos y voces de misión.

## 6. Persistencia y límites del estado

Separar dos responsabilidades:

- **Configuración local por instalación/jugador:** rutas privadas del MSI, biblioteca indexada, enlaces o copias y preferencias personales; estos datos **no son activos públicos de la nave ni deben incorporarse a un guardado portable por defecto**.
- **Estado jugable autoritativo cuando proceda:** el personaje está en su camarote, el reproductor está activo, una orden ha sido aceptada y sus consecuencias de juego (por ejemplo, ocio) se resuelven por el sistema correspondiente, sin que la capa de IA modifique directamente el World State.

Una partida copiada a otro PC no debe presuponer que los mismos archivos existen allí. Mostrar biblioteca no disponible y permitir volver a vincular carpetas sin corromper el guardado.

El sistema debe preservar límites de acceso: escuchar música en un camarote no permite consultar o revelar automáticamente otras carpetas privadas del equipo ni bibliotecas de otros usuarios.

## 7. Ocio, vida cotidiana y ampliaciones

La música será una actividad de ocio real y coherente con el tiempo libre del personaje. **No se fijan bonificaciones automáticas ni valores de bienestar en esta idea**: cualquier efecto se integrará con las reglas reales de descanso/estado de ánimo cuando existan.

Posibles extensiones, **no condición para el MVP**:
- Preferencias musicales del personaje y recuperación de lo escuchado.
- Escuchar canciones acompañado de un NPC y comentarios si están respaldados por gustos, memoria y contexto existentes.
- Reutilizar la infraestructura en salas recreativas o estaciones espaciales autorizadas, con bibliotecas y permisos apropiados.

Estas ampliaciones no justifican inventar artistas, canciones o gustos que no consten en los datos.

## 8. Privacidad, seguridad y distribución

- Seleccionar archivos/carpetas mediante un diálogo del sistema operativo con consentimiento del usuario; no analizar arbitrariamente todo el disco.
- Limitar las extensiones/tipos aceptados; validar contenido y gestionar archivos corruptos, enormes, con rutas inválidas, rutas inaccesibles o datos de metadatos malformados.
- Evitar registrar rutas privadas completas en telemetría o logs externos; no subir portadas, listas, canciones ni archivos por defecto.
- Mantener música de terceros **fuera de GitHub, paquetes de distribución y builds públicas**. Que el usuario aporte música legítimamente accesible no otorga permiso de redistribución, emisión pública o streaming a terceros.
- Reproducción local y personal, sin compartir automáticamente audio entre jugadores o dispositivos.
- No almacenar binarios musicales en repositorios del juego, savegames sincronizados o servicios de IA.

## 9. Prueba incremental sugerida

**MVP independiente futuro**, sin alterar la Guardia de Sensores v0.0.1:
1. Importar por vinculación una carpeta del MSI con varios MP3 y FLAC.
2. Mostrar títulos y artistas reales obtenidos de etiquetas, con búsqueda y control manual.
3. Reproducir una canción local en un camarote UE5, con volumen, pausa, siguiente y atenuación a través de la puerta.
4. Gestionar una orden «Computadora, reproduce [artista/título]» contra el índice, sin conexión a Internet para las canciones.
5. Guardar y recuperar preferencias e índice local, incluso tras cerrar y reabrir el juego.
6. Comprobar archivo movido, falta de permisos, FLAC de gran tamaño, ausencia de etiquetas, coincidencia ambigua, micrófono no disponible y comunicación/alerta prioritaria.

Probar posteriormente el modo de copia opcional, cambio de dispositivo, distintas tasas de muestreo, carga de CPU/RAM y comportamiento en una build distribuible.

**Criterios de aceptación** (no probados aún):
- Importación local MP3/FLAC sin subidas a Internet y sin duplicar archivos en modo predeterminado.
- Música real desde la carpeta original con búsqueda por metadatos.
- Sonido localizado en el camarote que respeta puertas/distancias.
- La IA no modifica el mundo ni accede al contenido binario musical.
- Control manual disponible cuando la voz/IA falla o está desactivada.
- Una pista ausente produce aviso útil, nunca falsa confirmación de reproducción.
- No hay música protegida integrada en el repositorio ni en builds distribuidas.

## 10. Encaje en el Plan Maestro

Asignación **provisional**, sin adelantar trabajo ni declarar fases terminadas:

| Fase | Encaje |
|---|---|
| F02 — Arquitectura e integración | Contrato de intenciones de ordenador, adaptador al reproductor local, separación IA/Core/UE5, protección de datos |
| F07 — Pipeline 3D/UE5 | Punto de emisión e interacción de audio en un camarote, cuando corresponda |
| F12 — Vida a bordo | Actividad de ocio del jugador, persistencia y eventuales relaciones sociales |
| F14 — Recursos audiovisuales | Audio espacial, codecs, reproducción dinámica y pruebas de compatibilidad/rendimiento |

Reutilizar:
- [Plan Maestro F00–F15](../docs/roadmap/master/PLAN_MAESTRO.md).
- [Starship Computer](../gameplay/ship_operations/ship_computer/README.md).
- [Vida a bordo — plan previo](../docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md).
- [F02 — Arquitectura](../docs/roadmap/master/fases/F02/README.md).
- [F12 — Vida a bordo](../docs/roadmap/master/fases/F12/README.md).
- [F14 — Audio y producción](../docs/roadmap/master/fases/F14/README.md).
- [Buzón de ideas](BUZON.md).

## 11. Decisión y estado final

**APROBADO por el autor, 2026-10-11:** biblioteca musical personal reproducible en el camarote, MP3/FLAC seleccionados del **MSI local**, importación desde menú del juego, **vincular carpeta como predeterminado**, copia local opcional, control por ordenador de la nave y manual, reproducción diegética y sincronización razonable de preferencias.

**Pendiente de diseño/validación:** tecnología concreta de decoder en runtime y versión UE5, política exacta ante alertas, manejo de guardados y rutas, nombres de contratos, mejoras NPC/ocio y pruebas de una build empaquetada.

**No implementada; no altera el alcance de la v0.0.1 ni interrumpe la fase de desarrollo activa.**
