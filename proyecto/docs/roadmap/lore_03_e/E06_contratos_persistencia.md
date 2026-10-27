# E06 — Contratos existentes y transferencia técnica futura
## Matriz de dependencias con propietario
| Función | Artefacto de contrato en ST | Requisito de integración pendiente |
|---|---|---|
| historia y fuente | mundo/lore/historical_events/historical_event_contract.json; mundo/sources/provenance_policy.md | parser con mapeo por ID y pruebas de cutoff |
| conflicto | mundo/lore/conflicts/conflict_definition_contract.json; sistemas/gameplay/conflict/conflict_war_index_v0.1.json | eventos de guerra aprobados y no reprocesados |
| consecuencias | sistemas/gameplay/consequences/world_event_consequence_contract.json | adaptador de candidatos, autoridad y rechazo |
| memoria/conocimiento | sistemas/ai/memory/character_memory_contract.json; sistemas/gameplay/knowledge/character_knowledge_state.json | difusión con control de permisos y marcas temporales |
| identidad | sistemas/universe/generation/persistent_entity_identity_contract.json | identidad tras guardado/LOD y referencias estables |
| guardado | sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json | pruebas de round-trip, idempotencia y segregación de partidas |
| fuera de pantalla | sistemas/gameplay/simulation/professional_offscreen_simulation_contract.json | catch-up determinista y resolución con CoreRPG |
| presentación | UE5/NPC/IA futuros consumidores | proyecciones sin escritura autoritativa |

## Contratos que esta fase NO crea
No se añade una segunda capa de WorldState ni otro esquema de guardado, calendario, cronología, tratado o evento runtime. La autoridad de mutación, el reloj, la persistencia, asignación de identidades y aceptación de sucesos pertenecen a CoreRPG.

## Gate de entrega a futura implementación
Para declarar una integración operativa será necesario demostrar con CoreRPG real: reconstrucción de estado 2383 con fechas ambiguas, dos saves divergentes, idempotencia load/save, continuidad de entidades, secreto filtrado por actor, cuatro años Academia offscreen, eventos de guerra con causas y no aparición forzada de futuros. A día de la auditoría documental **no están certificados**. No son bloqueos para cerrar el paquete documental E una vez fusionado.

## Cotejo independiente con el repositorio CoreRPG
**Fuente comprobada:** robdor80/CoreRPG, main@4f282863737bcd8f5add401202a9e1064c133672 (consulta GitHub 2026-10-27). Contratos consultados: docs/architecture.md, docs/phases/4.5-generic-world-state.md, docs/phases/4.7-persistence.md, docs/phases/4.10-actions-simulation.md, docs/persistence-format-v3.md e interfaces include/corerpg/world_state.hpp, persistence.hpp y simulation.hpp; PR #10 y #11 fusionadas (4.12 y 4.13 respectivamente).

**Capacidades verificables por código/contrato existente:** WorldState conserva EntityId, revisión, contención y estado estructural; Persistence v1/v2/v3 conserva identidades, relaciones/Knowledge y RNG conforme a versión; ActionEngine procesa primitivas tipadas con precondiciones; Simulation::step ejecuta pasos explícitos ordenados, de forma acotada, sin saltar la autoridad de CoreRPG. 4.12 incorpora un constructor de contexto de ObserverView autorizado, no una IA con escritura sobre WorldState. 4.13 ensaya un Content Pack real de **Nimroel**, no certifica un Content Pack runtime Star Trek.

**Límite contrastado especialmente relevante:** la API pública Simulation::step es un conductor **sin reloj, cola de acontecimientos, scheduler autónomo, motor de misiones ni sistema de carrera o diplomacia de Star Trek**. Persistence v3 tampoco contiene un ledger histórico general de acontecimientos de campaña con sincronización intranual. Las políticas E05/D07 de Academia 2383–2387, bifurcación causal, noticias, memoria biográfica y guerra aún requieren integración de dominio/adaptadores y pruebas. No rebajar esta brecha porque CoreRPG tenga tests propios. La autenticación y deduplicación del transporte competen al Host; Inspector y diagnósticos privilegiados no pueden pasarse a IA/NPC como si fueran ObserverView.

**Conclusión de compatibilidad:** no hay conflicto conceptual con la autoridad única del Core; sí hay capacidades específicas no implementadas. Compatibilidad arquitectónica documental ≠ interoperabilidad de contenido Star Trek ni funcionamiento runtime validado.
