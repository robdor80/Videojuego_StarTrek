# Star Trek Legends — introducción oficial en Unreal Engine

**Decisión de autor:** 19-11-2026 · **Estado:** producción definitiva autorizada en diseño; pendiente de montaje y certificación en Unreal Engine 5.8.2.

## Intención vinculante

La secuencia de presentación de **Star Trek Legends** (duración objetivo: **53 segundos**) no es un prototipo, experimento ni laboratorio descartable: será la **introducción oficial del videojuego**. Se realizará **entre el autor y ChatGPT, directamente en el editor de Unreal Engine 5.8.2**, sin exigir Codex ni programación C++ para el montaje audiovisual.

Se parte de material que el autor **ya tiene preparado** (las imágenes, la música y el concepto narrativo). No sustituirlo por imágenes genéricas o versiones de ejemplo. Los materiales concretos se importarán desde los archivos locales que facilite el autor al abrir el editor.

## Contenido creativo fijado anteriormente

- Homenaje a cinco capitanes y sus respectivas naves/estación, en orden: **Christopher Pike — Enterprise NCC-1701; James T. Kirk — Enterprise NCC-1701-A (Kelvin); Kathryn Janeway — Voyager NCC-74656; Benjamin Sisko — Deep Space Nine; Jean-Luc Picard — Enterprise NCC-1701-D**.
- Imágenes panorámicas horizontales de cada nave/estación completa y retratos de los capitanes preparados para fondo **negro puro**, con transiciones suaves integradas en negro.
- Sincronización con la selección musical realizada por el autor (tema principal de *Star Trek* de 2009), respetando el diseño de 53 s ya acordado. Los puntos exactos de entrada y corte se fijarán al colocar la pista real.
- Aparición final del título **STAR TREK LEGENDS**, como parte de la presentación oficial.
- La presentación de **cinco leyendas** y la cinemática narrativa **S04** son **capítulos creativos distintos de una misma introducción completa** del videojuego. Se producen y guardan separadamente, pero el jugador los verá unidos sin interrupciones de menú.

## Unidad de la introducción completa y producción por etapas (ampliación autoral 19-11-2026)

**Decisión aprobada:** la presentación musical de las cinco leyendas **NO** es la totalidad de la introducción de la campaña; es **su primer capítulo**. La apertura oficial del videojuego comprenderá varias secuencias producidas en distintos momentos pero **enlazadas, consecutivas y presentadas como un único prólogo**.

1. **Capítulo 1: homenaje a las cinco leyendas.** Material de 10 imágenes (cinco capitanes, cinco naves/estación) y pista de Michael Giacchino disponibles en local según inventario aportado por el autor. Producción **inmediata** directamente en UE5. Duración de referencia **53 segundos**; el autor ha considerado un posible ajuste a 54 s al recortar la música. La duración exacta se decidirá y registrará al sincronizar el montaje musical.
2. **Capítulo 2: Consejo de la Flota Estelar / expediente del protagonista.** Cinemática narrativa 2D de la admisión del personaje híbrido y descendiente de Khan, con debate del alto mando, recuerdos de la vida previa y posiciones institucionales, conforme a **S04 / DEC-0022**. **Producción posterior**: requiere definir ilustraciones, montaje y voces. Las grabaciones o referencias de voz de **Picard, Janeway y Riker** están pendientes de recopilar o preparar según indique el autor. La intervención concreta de Riker, lugar en la escena y texto **no quedan fijados por esta nota**; respetar la composición/competencias institucionales ya aprobadas.
3. **Capítulo 3: resolución y comienzo de campaña.** Continuación audiovisual hacia la notificación/admisión legítima y entrada en la Academia en 2383; detalles y duración pendientes de guion. No confundir representación narrativa con la creación de plazas, identidades o rango por la cinemática.

**Transición obligatoria:** cuando termine el capítulo musical, **fundido a negro** y comienzo del capítulo 2 **sin volver al menú ni exigir una segunda acción**. De igual modo, encadenar la resolución y entrada a la Academia. La música del capítulo 1 no debe arrastrarse por error al diálogo del Consejo; las mezclas, silencios y transiciones se ajustarán en edición.

**Integración UE5:** mantener cada bloque como activo/secuencia independiente bajo `Content/StarTrek/Intro/` y preparar el encadenamiento posterior mediante un controlador/secuencia maestra de introducción o mecanismo equivalente compatible con Sequencer/UE5. **No obligar a recrear el capítulo 1** cuando lleguen ilustraciones y voces de capítulos posteriores. La selección definitiva del método de reproducción y transición se hará al probarlo en el proyecto. La intro completa se presenta al inicio de una **nueva partida**; omitirla o revisitarla no debe duplicar admisiones, guardar consecuencias ficticias ni recrear personajes (CoreRPG/F10 son autoridad).

**Condición de entrega por fases:** el **capítulo 1 sí puede darse por terminado y persistente** una vez montado y validado en el proyecto real, aunque los demás bloques no estén listos. No afirmar que la **introducción completa** está terminada hasta enlazar todos los capítulos con los recursos finales y probar el paso a la partida.

**Fuentes locales informadas por el autor, no versionadas en Git:** `Content/StarTrek/Intro/Imagenes_Originales/Capitanes/` (5 PNG), `Imagenes_Originales/Naves/` (5 JPEG) y `Musica original/` (MP3). Son fuentes originales que podrán mantenerse separadas de los activos importados Unreal en sus propias carpetas; confirmar la importación real antes de declararla realizada. Las copias periódicas del proyecto completo a SSD externo constituyen el respaldo habitual informado por el autor; comprobar que incluyen estos originales y los `.uasset`/`.umap` de `Content`.

## Ruta definitiva y persistencia del proyecto

Proyecto Unreal existente: `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`.

Ubicación definitiva de los activos Unreal de producción, dentro de **ese mismo proyecto y del árbol `Content/StarTrek` existente**:

```text
juego/UE5/StarTrekRPG/Content/StarTrek/Intro/
  Imagenes/
  Audio/
  Materiales/
  Secuencias/
  Mapas/
  Widgets/
```

La introducción se materializará como activos Unreal persistentes (por ejemplo, **Level Sequence** con pistas de imagen/animación/audio y elementos de UI/escena apropiados); la elección concreta entre actores, widgets o medios se tomará al verificar los recursos reales dentro del editor. **No debe desarrollarse como demo en otro .uproject ni en laboratorios temporales**. Guardar las modificaciones y comprobar que se recuperan al cerrar y reabrir el proyecto.

El archivo `.uproject` es un descriptor, no un contenedor autosuficiente: los recursos finales residen principalmente en **Content**. Evitar alterar otros niveles, flujos de juego o sistemas ya existentes sin necesidad.

## Requisitos de cierre de producción

1. Reproducir la intro **en el proyecto real** `StarTrekRPG` con las imágenes y música del autor, no solo en una vista previa externa.
2. Confirmar la duración y el orden y la sincronización de cada aparición con la pista musical definitiva.
3. Confirmar fondo negro, encuadre completo de las cinco naves/estación, transiciones y título.
4. Guardar todos los recursos/activos que requiere la secuencia y verificar **cerrar UE5 → volver a abrir → reproducir sin errores ni referencias perdidas**.
5. Prever su disparo desde el inicio del juego y su transición al siguiente estado de presentación/menú; la integración de arranque no se considera terminada hasta probarla, aunque el montaje audiovisual sí pueda completarse previamente.
6. Garantizar **respaldo verificable** de los activos finales y archivos fuente (imágenes y audio), además de la copia local. No equiparar guardado local con respaldo en Git.

## Precaución específica de versionado

A fecha de la decisión, el `.gitignore` del repositorio **excluye expresamente** `*.uasset`, `*.umap`, `*.ubulk`, `*.uexp` y más binarios, por la política vigente de no versionar paquetes grandes ni usar Git LFS. Por ello, documentar las rutas de los activos y mantener una copia de seguridad definitiva y verificable por el procedimiento de respaldo que acuerde el autor; **no forzar `git add -f` ni modificar el `.gitignore` a escondidas**. La documentación textual sí podrá versionarse.

**Estado técnico actual:** esta acta **solo registra la aprobación de producción**. Todavía **no** se han importado imágenes/audio al proyecto, creado la secuencia, comprobado persistencia o integrado el arranque. No afirmar lo contrario.
