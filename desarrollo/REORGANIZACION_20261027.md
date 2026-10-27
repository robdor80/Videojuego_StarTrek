# Reorganización y protección de Git — 27 de octubre de 2026

## Resultado

Parte segura completada en la rama `reorganizacion/estructura-proteccion-20261027`. Cambios preparados para revisión local, sin commit, push, merge ni reescritura de historial.

- 15,656 archivos originales inventariados y verificados mediante SHA-256; 2,744 trasladados. Cero archivos originales perdidos y cero binarios originales modificados.
- Biblioteca ordenada en `assets/`; sistemas en `sistemas/`; lore y fuentes en `mundo/`; audiovisual en `audiovisual/`; herramientas, validaciones, NAP, esquemas y manifiestos en `desarrollo/`; documentos e ideas en `proyecto/`.
- `juego/`, sus naves y la estructura `UE5/StarTrekRPG` están preparados. No hay proyecto Unreal principal válido, ni `.uproject` inventado. El manifiesto `project_structure.json` y `restore_structure.py` reconstruyen las carpetas vacías.
- 51 archivos previamente versionados retirados solo del índice: 392,711,348 bytes (392.7 MB). Incluyen tres imágenes ya ausentes antes de empezar, cuyos blobs Git se copiaron y verificaron fuera del repositorio. No se recrearon sus originales.
- Dos auditorías JSON no versionadas, de 79.8 MB en conjunto, fueron bloqueadas por el hook al preparar el índice. Se retiraron de las adiciones propuestas y tienen exclusiones expresas. Sus originales y copias siguen intactos.
- 13,271 archivos locales excluidos: 18.67 GB. De ellos, 7,683 archivos en formatos binarios/3D/paquetes identificados suman 15.91 GB; el resto incluye informes y datos de laboratorios o respaldos. La clasificación por formato y muestreo de bytes NUL se detalla en la evidencia de exclusiones.

## Protección y recursos conservados

`.gitignore` mantiene las reglas antiguas y protege modelos en cualquier ruta, binarios de assets, paquetes, texturas PBR, laboratorios y cachés. Excepciones expresas conservan metadatos y licencias. No se excluyen globalmente `.uasset`, `.umap`, `Source`, `Config`, `Plugins` ni `Content`.

La herramienta versionada `tools/git_binary_guard.py` inspecciona el índice completo y bloquea formatos 3D, archivos locales prohibidos y blobs mayores de 25 MiB. `core.hooksPath` está configurado localmente a `desarrollo/tools/git_hooks`; sus seis pruebas de integración pasan. El registro de excepciones de tamaño está vacío. El hook debe instalarse en cada clon y no es una política remota de GitHub. No se usa LFS.

TABULA RASA conserva sus 3,368 archivos, rutas, hashes y fechas de modificación originales. La separación Valhalla, materiales, geometría, orígenes y transformaciones no se han alterado. Los tres proyectos Unreal hallados permanecen allí: no se han promovido ni migrado paquetes. `recursos_unreal_locales.json` registra 1.445 recursos esenciales históricos con tamaño, SHA-256, proyecto o clasificación pendiente, copia local y requisitos de restauración. Las dependencias de paquetes deben validarse todavía en Unreal; algunos recursos no tienen proyecto asignable.

La futura fusión retirará los 51 archivos relacionados de la versión corriente de GitHub. Los archivos presentes permanecen en el MSI; el historial anterior conserva los blobs. No se reduce el historial ni se ha cambiado el remoto.

## Validación

Se comprobaron 4.919 referencias locales de Markdown/JSON que existían antes, sin enlaces nuevos rotos en ese alcance. Se actualizaron workflows, rutas Python y pines de procedencia F02; los nombres históricos de ramas se conservaron. Los IDs de recursos y las fuentes originales de los metadatos se mantienen, con 94 directorios de metadatos actualizados.

Las 1.189 pruebas existentes producen 1.187 éxitos y los dos fallos previos: la expectativa F07 de estados UE5 y los enlaces de índice cultural LORE01-A1. También fallaban antes los validadores de referencias internas (confunden algunas rutas con IDs de fuentes) y LORE01-A1. Se guardó la línea base antes de los movimientos. Los validadores F02 y P05 pasan. Compilan 130 archivos Python. No se ejecutaron pruebas de CoreRPG ni del juego Unreal.

Blender abrió 11 archivos antes y después, sin guardar escenas. Se conservaron los paquetes relativos; la comprobación glTF no detecta pérdida de dependencias que antes se resolvían. Esto no certifica jugabilidad ni todas las dependencias de FBX/Unreal.

## Pendientes y bloqueos

- Respaldo externo pendiente para TODOS los recursos locales excluidos. La copia verificada de 18.76 GB está en `C:\Users\andro\Documents\StarTrek_Respaldo_Reorganizacion_20261027\files`, fuera del repositorio pero en el mismo MSI. No existe soporte externo o nube verificados. No se declara completo el respaldo del proyecto definitivo.
- `3D Star Trek/`, `Auditorias_3D_VOYAGER/` y `Sutherland_PBR_Lab/` siguen en sus rutas originales. Las auditorías contienen referencias absolutas y dependencias históricas; no se garantiza todavía un traslado seguro. `archivo_historico/README.md` las indexa. No se han recreado ni eliminado laboratorios antiguos.
- El paquete Sutherland de `assets/ships/starfleet/bridges/USS Suntherland/` conserva cinco referencias de texturas no resueltas previamente; `assets/stars/sistema_solar_animado/` conserva otras quince. No se movieron ni repararon. La reubicación requiere resolver esas dependencias en una tarea específica.
- Crear el proyecto Unreal principal real y auditar sus dependencias en el editor antes de integrar resultados de laboratorios o respaldos. No existe todavía una integración definitiva comprobada.

## Evidencias y reversión

`manifests/reorganizacion_20261027/` contiene el inventario unificado de rutas originales/actuales y hashes, el mapa de movimientos, índice previo, recursos retirados, manifiesto Unreal, excepciones y resultados de validación. Cada recurso apunta a su copia local; el campo `external_backup` sigue vacío. La copia conserva también el índice y estado Git previos.

Para revertir, detener aplicaciones que usen los archivos y guardar primero cualquier trabajo posterior. Validar los hashes actuales del inventario; leer `movimientos.json` y revertir sus unidades en orden inverso, abortando si un destino ya existe. Restaurar únicamente textos editados desde la copia `files/` después de preservar sus versiones actuales. No usar `reset --hard`, `clean`, borrados ni sobrescrituras ciegas. Restaurar `index-before` solo después de preservar el índice actual y confirmar que no contiene trabajo posterior; retirar la configuración local de hooks añadida en esta tarea. El procedimiento previo completo está en `C:\Users\andro\Documents\StarTrek_Respaldo_Reorganizacion_20261027\REVERSIÓN.txt`. No se ha ejecutado la reversión.
