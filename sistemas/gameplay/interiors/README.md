# Sistema 12 — Interiores y desplazamiento

> **ACTUALIZACIÓN AUTORAL 18-11-2026 — PROTOTIPO S12 NO APROBADO:** la identidad/autenticación/permisos de puertas privadas **pertenecen ahora al Sistema 18 (DEC-0024, fusionada en main)**, no a S12. S12 se concentra en puertas mecánicas/automáticas, pulsadores, turboascensores que llegan a la **parada real más próxima**, navegación de NPC y geolocalización/mapas LCARS. **No es un sistema de decoración, texturas ni construcción de recorridos Blender.** Véase S12_FUNCIONAL_PRIORIDADES_ADENDA_2026-11-18.md.

**Fecha:** 18-11-2026 · **Estado:** PROPUESTA DE DISEÑO PARA REVISIÓN DEL AUTOR. **No aprobado, implementado ni fusionado.**

**Distinción importante:** Sistema 12 del catálogo de diecisiete sistemas **NO es la fase técnica F12** del plan F00–F15. La fase F12 ya existente en `proyecto/docs/roadmap/master/fases/F12` corresponde a **vida a bordo, NPC y relaciones**; ambos deben integrarse sin duplicación.

**Idea:** visitar la Enterprise-D reconstruida por el Proyecto Valhalla como un lugar habitable, con caminar en 3D en sectores conectados, puertas, corredores, turbolifts como traslados coherentes entre escenarios y localización persistente de tripulantes. Reutilizar y proteger la geometría y módulos Blender existentes, sin intentar construir un casco completo a escala como mapa único.

Documentos:
- [Diseño del Sistema 12](S12_INTERIORES_DESPLAZAMIENTO_PROPUESTA_v1.md)
- [Base A–H del Proyecto Valhalla](s12_valhalla_deck_basis_v0.1.json)
- [Contrato de escenas, puertas y transiciones](s12_scene_travel_contract_v0.1.json)
- [Escenarios de aceptación](s12_acceptance_scenarios_v0.1.json)
- [Estado de diseño](s12_status_v0.1.json)
- [Plan de puesta en marcha](../../../proyecto/docs/roadmap/S12_INTERIORES_DESPLAZAMIENTO_PLAN_2026-11-18.md)

Contratos ya existentes que **NO se sustituyen**: `sistemas/gameplay/ship_operations/interior_location_model.json`, `interior_navigation_graph_v0.1.schema.json`, `interior_functional_profiles_v0.1.json`, `desarrollo/tools/validation/interior_navigation.py` y los modelos de horarios/presencia/NPC.

**No se ha tocado ni reconstruido ningún .blend, .skp, modelo de casco, proyecto Unreal o binario.**
