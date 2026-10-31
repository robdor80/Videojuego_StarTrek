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
4. Declarar la carpeta eliminable solo cuando no queden referencias ni dependencias hacia ella.
5. **Borrar exclusivamente con autorización expresa del usuario**; poder eliminar la carpeta completa sin romper el resto del repositorio.

No crear laboratorios dispersos fuera de `Videojuego_StarTrek`. Los respaldos deliberados en HDD son distintos de los laboratorios.

**Esta política se aplica a trabajos futuros y no mueve ni borra archivos actuales.** Las auditorías y pruebas antiguas con referencias pendientes permanecen en sus rutas existentes, registradas en `../archivo_historico/README.md`.

Ver instrucciones obligatorias para Codex en `../AGENTS.md`.
