# Videojuego Star Trek — RPG 3D

Repositorio de **diseño, canon, contratos específicos, recursos de referencia, generación y validación** del videojuego Star Trek RPG. No debe confundirse con un proyecto Unreal Engine 5 ya integrado.

## Dirección del proyecto (punto de entrada)

- **[Plan Maestro — fases F00–F15](docs/roadmap/master/PLAN_MAESTRO.md)**: ruta de entrega y 80 pasos iniciales.
- [Estado de fases](docs/roadmap/master/ESTADO_GLOBAL.json) y [F00 — auditoría cerrada](docs/roadmap/master/fases/F00/README.md).
- [Auditoría técnica e inventario](docs/roadmap/master/AUDITORIA_F00.md) y [matriz de reutilización](docs/roadmap/master/MATRIZ_REUTILIZACION.md).
- [Ideas nuevas](ideas/BUZON.md): anotarlas sin desviar la fase activa.
- [Normas de cierre](docs/roadmap/master/CRITERIOS_DE_CIERRE.md) y [decisiones/riesgos](docs/roadmap/master/DECISIONES_Y_RIESGOS.md).

## Contenido técnico (conservar rutas originales)

- `gameplay/`, `universe/`, `lore/`: reglas, simulación, cronología y fuentes.
- `ai/`, `narrative/`, `art_direction/`, `assets/`, `presentation/`, `ui/`, `audio/`: sistemas y recursos de juego.
- `tools/`, `validation/`: generadores, fixtures, pruebas de referencia y validaciones.
- `docs/roadmap/`: subplanes históricos, conservados con sus números y resultados.
- `CONTENT_STATUS.md`: estado **editorial/diseño por su alcance**, no indicador automático de jugabilidad UE5.

**Fronteras:** Core RPG aloja capacidades genéricas autoritativas cuando estén disponibles; este repositorio define el universo/reglas de Star Trek; UE5 los representa en 3D. La IA por API remota asesora o interpreta pero nunca escribe el World State directamente.
