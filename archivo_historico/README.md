# Índice de históricos conservados

Se conservan íntegros en sus rutas actuales porque no se ha demostrado que puedan moverse sin romper referencias históricas o dependencias de Blender:

- `../3D Star Trek/`: auditorías, exportaciones y herramientas anteriores.
- `../Auditorias_3D_VOYAGER/`: laboratorios y publicaciones históricas; contiene referencias absolutas y una antigua copia de worktree sin metadatos Git activos.
- `../Sutherland_PBR_Lab/`: biblioteca de texturas asociada a trabajo anterior, sin promoción al juego.
- `../assets/ships/starfleet/bridges/USS Suntherland/`: cinco referencias de textura no resueltas previamente en `Sutherland_PBR_Lab_v01.blend`.
- `../assets/stars/sistema_solar_animado/`: quince referencias de textura no resueltas previamente en `Solar System.blend`.

`../TABULA RASA COPIA SEGURIDAD/` es un respaldo crítico protegido: no se mueve, renombra ni edita. Contiene los tres proyectos Unreal encontrados y los recursos Valhalla recuperados. No es una dependencia del juego definitivo, todavía pendiente de creación.

Estos contenidos permanecen excluidos de Git. El inventario, los hashes y las copias de seguridad se documentan en `../desarrollo/REORGANIZACION_20261027.md`. La reubicación física de los históricos queda pendiente de una auditoría de dependencias específica.
