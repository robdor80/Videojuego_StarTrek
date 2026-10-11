# F01-P03 — Análisis de Damas para Imperator (DEC-0001)

Fecha: 2026-10-11. Estado: BLOQUEADA POR DECISIÓN DE AUTOR. No hay elección aprobada.

## Candidatas
| Base | Estado comprobado | Ventaja | Riesgo |
|---|---|---|---|
| Galaxy (Enterprise-D) | Clase existente en `core_starship_classes.json` y referencias de puente en `assets/ships/starfleet/galaxy_class/enterprise_d/` | Vida a bordo profunda; referencias aprovechables | Tamaño/dotación e interiores; imágenes no equivalen a malla 3D |
| Sovereign (Enterprise-E) | Clase presente en catálogo; extensión cinematográfica tardía | Nave avanzada y potencial de mando | Disponibilidad por fecha (registrada para 2373); diseño/modelos por verificar |
| Odyssey (Enterprise-F) | Ausente del catálogo de clases actual | Gran plataforma avanzada | Fuentes y fecha no incorporadas al alcance aprobado; necesita resolución expresa |

La Clase Imperator será creación de juego, distinta de la Enterprise de referencia. Las otras dos Damas podrán existir como NPC y serán jugables solo cuando estén sus interiores. Ascender a capitán de la Imperator será opcional, por trayectoria y oportunidad real, nunca automático.

La clase elegida para Imperator no determina el puente piloto de F07 ni puede saltarse los filtros cronológicos. Antes de fijar Odyssey deberán aprobarse época/fecha y fuentes; no se puede colar un nuevo canon en el catálogo por accidente.

Recomendación técnica provisional (no decisión): separar `imperator_reference_class`, `imperator` y `prototype_bridge_class`.

**Decisión requerida:** Roberto selecciona Galaxy, Sovereign u Odyssey.

Fuentes: `docs/roadmap/master/DECISIONES_Y_RIESGOS.md`, `docs/decisions/playable_eras.md`, `docs/decisions/starship_identity_model.md`, `lore/starships/classes/core_starship_classes.json`.
