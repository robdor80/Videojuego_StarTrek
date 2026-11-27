# Laboratorios locales, aislados y eliminables

Este directorio es el **único destino autorizado para los resultados temporales** de pruebas, auditorías y experimentos de Codex del proyecto Star Trek.

## Organización

Crear cada tarea dentro de `laboratorios/<area>/<tarea>/` (por ejemplo, `laboratorios/Clase_Miranda/puente_ergonomia/` o `laboratorios/F04/persistencia/`). Guardar allí los scripts desechables, compilaciones de prueba, capturas, mediciones, logs y datos experimentales.

Los experimentos pueden utilizar UE5, Blender u otras herramientas, **siempre sobre copias de recursos originales**. La ubicación sigue estando dentro de este directorio.

`.gitignore` excluye todo `/laboratorios/**` excepto este `README.md`: el contenido experimental permanece local, no se confirma ni se publica en Git. No ejecutar `git add -f` sobre estos resultados.

## Ciclo de vida

1. Crear un laboratorio autocontenido y sin dependencias desde los archivos definitivos hacia él.
2. Ejecutar pruebas, mediciones y auditorías exclusivamente dentro de esa carpeta.
3. Si hay resultados útiles, integrar **solo lo aprobado** en las carpetas definitivas del proyecto y comprobar que funcionan sin el laboratorio.
4. Antes de limpiar, conservar los resultados verificables en `.md` y/o `.json` en la ubicación documental definitiva autorizada de la fase, fuera de `laboratorios/`, siguiendo los campos mínimos de `AGENTS.md`. Conservar el resultado, no el laboratorio: eliminar compilaciones, cachés, copias, logs brutos y demás recursos pesados regenerables propios, salvo excepciones justificadas. Declarar la carpeta eliminable solo cuando no queden referencias ni dependencias hacia ella.
5. **Limpiar obligatoriamente al cerrar cada tarea** los artefactos prescindibles que Codex haya generado para ella, sin autorización adicional, una vez registradas las evidencias y verificadas las dependencias. Eliminar el subdirectorio propio completo si es desechable. No borrar contenido preexistente, ajeno o de procedencia incierta sin autorización expresa.
6. Informar de las rutas limpiadas, espacio liberado y material retenido (motivo, tamaño y condición de eliminación), conforme a AGENTS.md. Preservar originales y evidencias imprescindibles; no seguir enlaces ni efectuar borrados globales.

No crear laboratorios dispersos fuera de `Videojuego_StarTrek`. Los respaldos deliberados en HDD son distintos de los laboratorios.

**Esta política se aplica a trabajos futuros y no mueve ni borra archivos actuales.** Las auditorías y pruebas antiguas con referencias pendientes permanecen en sus rutas existentes, registradas en `../archivo_historico/README.md`.

Ver instrucciones obligatorias para Codex en `../AGENTS.md`.
