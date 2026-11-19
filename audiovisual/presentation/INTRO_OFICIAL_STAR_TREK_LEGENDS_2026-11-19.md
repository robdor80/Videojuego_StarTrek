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
- Esta presentación de **cinco leyendas** es **distinta** de la cinemática narrativa S04 sobre el protagonista, el consejo de Janeway/Picard y el acceso a la Academia: no mezclarlas ni considerarlas sustitutas.

## Ruta definitiva y persistencia del proyecto

Proyecto Unreal existente: `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`.

Ubicación de diseño para los activos Unreal de producción, dentro de **ese mismo proyecto**:

```text
juego/UE5/StarTrekRPG/Content/Intro/
  Images/
  Audio/
  Sequences/
  Materials/
  UI/
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
