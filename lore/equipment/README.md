# LORE-02 B — Equipamiento personal y especializado

Este directorio ya no está reservado. **Catálogo único**: [equipos y tecnologías](lore02_b_equipment_catalogue_v0.1.json) (73 fichas, 7 familias). [Dotaciones, perfiles y plantillas](lore02_b_roles_loadouts_v0.1.json) y [45 escenarios adversariales](lore02_b_adversarial_scenarios_v0.1.json).

**Investigación y límites:** [dossier](../../docs/roadmap/lore_02_b_equipment_research_dossier_v0.1.md), [fuentes](../../sources/source_registry/source_registry.json). Categorías A–G: ciencia/exploración; seguridad/armas; medicina; ingeniería; protección ambiental/EVA; comunicaciones/informática; equipos de otras civilizaciones.

El mismo equipo puede ser usado por diferentes funciones sin duplicar fichas en directorios de especialidad. Las carpetas `personal/`, `scientific/`, `weapons/`, `medical/`, `engineering/` y `tools/` sirven como índices temáticos, **no** catálogos paralelos.

Definiciones documentales ≠ instancias físicas ≠ inventario asignado ≠ permisos del actor ≠ estado actual ≠ capacidades ejecutadas en UE5. El estado pertenece exclusivamente a CoreRPG; la capa de juego debe resolver las reglas particulares de Star Trek. Todos los datos nuevos son `EDITORIAL_NON_RUNTIME`, con fuente/inferencia/adición del juego diferenciadas y sin datos de rendimiento inventados.

**Validación:** `python tools/validation/validate_lore02_b.py` y `python tools/validation/test_lore02_b.py`; CI `.github/workflows/lore02-b-equipment.yml`. Estado pendiente de revisión humana.
