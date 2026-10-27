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
