# F01-P03 — Análisis de las tres Damas y decisión DEC-0001

**Expediente original:** «Imperator» (denominación provisional, ya sustituida).  
**Actualización:** 2026-10-13 · **Decisión creativa:** APROBADA · **Validación de activos/runtime:** PENDIENTE.

## Comparativa histórica, conservada como evidencia
| Candidata | Fuentes/bases consideradas | Ventaja | Limitación |
|---|---|---|---|
| **Galaxy / Enterprise-D** | Clase existente en `core_starship_classes.json`; referencias en `assets/naves/starfleet/galaxy_class/enterprise_d/`; pruebas y modificaciones de separación de platillo efectuadas como prototipo Blender fuera de esta PR | Perfil de gran nave, interiores y separación del platillo como inspiración | Requiere una clase nueva completa; el prototipo Blender **no** acredita operación UE5 |
| **Sovereign / Enterprise-E** | Clase del catálogo; trabajos M05/M07 de hangar y materiales realizados externamente | Arquitectura y casco modernizados, hangar de referencia | **No** elegida como inspiración principal de Valhalla; sus trabajos siguen aprovechables en su propia nave |
| **Odyssey / Enterprise-F** | No incluida en el catálogo vigente de esta fase | Referencia posible y nave NPC futura | Tecnología/fecha/catálogo requieren definición específica; no insertarla retroactivamente en 2372 |

## DEC-0001 — RESUELTA POR EL AUTOR
1. La **Galaxy/Enterprise-D** queda seleccionada como **referencia de partida**.
2. La nave nueva se denomina **Clase Valhalla** (no «Clase Imperator»).
3. Valhalla será una **clase nueva derivada estéticamente de Galaxy**, **no** una actualización simple, subclase, ni cambio de matrícula de la Enterprise-D. Necesita identidad y ficha de clase independientes.
4. Su rediseño exterior será **reconocible**: se conserva la silueta Galaxy y se modernizan formas, barquillas, deflector, casco, hangares y detalles conforme permita el modelado.
5. Las otras Damas continuarán como potenciales naves NPC y visitas/misiones; su jugabilidad queda condicionada a puentes, interiores y pruebas reales.
6. **Fecha de servicio de Valhalla: SIN FIJAR** hasta estudiar tecnología, modelos y continuidad propia del juego; el autor permite cambios explícitos respecto al calendario televisivo.
7. Ser capitán de Valhalla es un **objetivo opcional de carrera**, sin ascenso automático y sin final forzado.

## Capacidades y límites ya elegidos
La separación funcional del platillo, autonomía prolongada sin warp, combate autónomo de ambas secciones, hangares híbridos operativos por sección, delegación real a mandos NPC y reacoplamiento asistido **están aprobados a nivel de diseño**. También el blindaje ablativo desplegable y los torpedos transfásicos, pendientes de validación 3D y de reglas específicas. **No** se declara implementada ninguna de estas capacidades.

**Acta fuente única:** [ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md](ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md).

## No confundir elecciones
- **Base creativa de Valhalla (Galaxy)** ≠ **puente piloto de la v0.0.1 de Sensores**; F07 valida el mejor recurso lícito y realmente navegable, pudiendo utilizar Sutherland, Kelvin u otro tras pruebas.
- **Clase** ≠ **nave individual**; nombre y matrícula de la unidad jugable no están fijados.
- **Actualización 13-10-2026:** decisión autoral, QA del expediente y PR #2 fusionada, por lo que F01 queda **CERRADA SOLO EN DISEÑO** (véase [acta F01](ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md)). **No** se declara terminada la construcción de Valhalla ni su presencia en un build UE5.

Fuentes: `proyecto/docs/roadmap/master/DECISIONES_Y_RIESGOS.md`, `proyecto/docs/decisions/playable_eras.md`, `proyecto/docs/decisions/starship_identity_model.md`, `mundo/lore/starships/classes/core_starship_classes.json` y acta anterior.
