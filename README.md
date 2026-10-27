# Videojuego Star Trek — RPG 3D

Repositorio de **diseño, canon, contratos específicos, recursos de referencia, generación y validación** del videojuego Star Trek RPG. No debe confundirse con un proyecto Unreal Engine 5 ya integrado.

## Dirección del proyecto (punto de entrada)

- **[Plan Maestro — fases F00–F15](proyecto/docs/roadmap/master/PLAN_MAESTRO.md)**: ruta de entrega y 80 pasos iniciales.
- [Estado de fases](proyecto/docs/roadmap/master/ESTADO_GLOBAL.json) y [F00 — auditoría cerrada](proyecto/docs/roadmap/master/fases/F00/README.md).
- [Auditoría técnica e inventario](proyecto/docs/roadmap/master/AUDITORIA_F00.md) y [matriz de reutilización](proyecto/docs/roadmap/master/MATRIZ_REUTILIZACION.md).
- [Ideas nuevas](proyecto/ideas/BUZON.md): anotarlas sin desviar la fase activa.
- [Normas de cierre](proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md) y [decisiones/riesgos](proyecto/docs/roadmap/master/DECISIONES_Y_RIESGOS.md).

## Contenido técnico

- `sistemas/gameplay/`, `sistemas/universe/`, `mundo/lore/`: reglas, simulación, cronología y fuentes.
- `sistemas/ai/`, `sistemas/narrative/`, `audiovisual/art_direction/`, `assets/`, `audiovisual/presentation/`, `audiovisual/ui/`, `audiovisual/audio/`: sistemas y recursos de juego.
- `desarrollo/tools/`, `desarrollo/validation/`: generadores, fixtures, pruebas de referencia y validaciones.
- `proyecto/docs/roadmap/`: subplanes históricos, conservados con sus números y resultados.
- `CONTENT_STATUS.md`: estado **editorial/diseño por su alcance**, no indicador automático de jugabilidad UE5.

**Fronteras:** Core RPG aloja capacidades genéricas autoritativas cuando estén disponibles; este repositorio define el universo/reglas de Star Trek; UE5 los representa en 3D. La IA por API remota asesora o interpreta pero nunca escribe el World State directamente.

## Organización local y almacenamiento

- `assets/`: biblioteca de originales, clasificada por tipo. Git conserva sus metadatos y licencias; los binarios permanecen locales.
- `juego/`: trabajo definitivo. `juego/UE5/StarTrekRPG/` es una estructura preparada, sin proyecto funcional todavía.
- `laboratorios/`: experimentos independientes, excluidos de Git.
- `archivo_historico/`: índice de material histórico conservado; las rutas antiguas con dependencias pendientes siguen intactas.
- [Política de almacenamiento y hook local](desarrollo/POLITICA_ALMACENAMIENTO.md).
- [Resultado, excepciones y restauración](desarrollo/REORGANIZACION_20261027.md).

Instalar la comprobación de commits en cada clon: `python desarrollo/tools/install_git_guard.py`.
Reconstruir las carpetas vacías: `python desarrollo/tools/restore_structure.py`.
