# D01 — Auditoría de contratos y arquitectura de continuidad

## 1. Estado real y conclusión
Tras ST-ORG-01 se conservaron `mundo/`, `sistemas/`, `proyecto/` y `desarrollo/`. LORE-03A (PR #38), B (#41), C (#44 y cierre #45) están cerradas documentalmente en `main@32f4a018bc75b37ff0a4e10fb466ffac6963c381`. La responsabilidad del **WorldState, reloj efectivo, planificación, arbitraje de eventos, aplicación y persistencia** sigue siendo **CoreRPG**. Ningún expediente D define otra autoridad.

## 2. Matriz contractual (propietario → lector/operación permitida)

| Dominio propietario | Ruta existente | Integración D |
|---|---|---|
| Selección de continuidad y fecha | `proyecto/docs/decisions/campaign_continuity.md`, `sistemas/universe/global_rules/canon_vs_campaign.md` | decidir corte `D`, canon previo; no futuro automático |
| Fechas, eras y procedencia | `sistemas/universe/chronology/`; `mundo/lore/historical_events/historical_event_contract.json` | precisión, ancla y frontera sin inventar horas |
| Hechos y conflictos | `mundo/lore/diplomacy/historical_events_v0.1.json`; `mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json`; `mundo/lore/conflicts/lore03b_dossier_index_v0.1.json` | referencias por ID; eventos del pasado no se ejecutan |
| Fuente y fiabilidad | `mundo/sources/canon_policy.md`; `mundo/sources/provenance_policy.md` | conservar clase de verdad y error/rumor |
| Guerra y diplomacia | `sistemas/gameplay/conflict/conflict_war_index_v0.1.json`; `sistemas/gameplay/diplomacy/` | comprobar causas/recursos/autoridad antes de efectos |
| Economía y evolución civilizatoria | `sistemas/universe/generation/civilization_economy_governance_history_contract.json`; `civilization_offscreen_evolution_contract_v0.1.json` | cambios explícitos, agregación sin historias falsas |
| Acontecimientos y consecuencias | `sistemas/gameplay/consequences/world_event_consequence_contract.json`; `world_state_consequence_event.json` | única vía candidata de cambios CoreRPG |
| Identidad y población | `sistemas/universe/generation/persistent_entity_identity_contract.json`; `persistent_population_materialization_rules.json` | sin reroll, continuidad de instancias |
| Identidad y carrera NPC | `sistemas/gameplay/characters/character_runtime_model.json`; `sistemas/gameplay/careers/service_record/service_record_model.json` | puestos, méritos, ascensos y expedientes |
| Conocimiento, memoria, privacidad | `sistemas/gameplay/knowledge/character_knowledge_state.json`; `sistemas/ai/memory/character_memory_contract.json`; `sistemas/gameplay/records_and_logs/access_and_privacy_rules.json` | datos individualizados; IA sin omnisciencia |
| Simulación remota y detalle | `sistemas/gameplay/simulation/professional_offscreen_simulation_contract.json`; `sistemas/gameplay/social/social_simulation_lod.json` | hechos remotos solo autorizados |
| Guardados | `sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json` | historia append-only, versiones, identidad y aislamiento |
| Legado científico | `mundo/lore/science/lore02_d_scientific_legacy_policy_v0.1.json` | investigación/aplicación/nombre requieren actos |

Estas rutas son **referencias a contratos existentes**, no un manifiesto de ejecución ni una prueba de integración entre repositorios.

## 3. Límites de subsistemas y flujo de autoridad
`catalogo historico + fecha D + fuente → propuesta de estado inicial validada → CoreRPG confirma WorldState inicial → motores propietarios producen candidatos → reglas/autoridad CoreRPG validan → evento y delta confirmados → historial propio de partida → vistas filtradas al jugador, NPC e IA`.

Se separan estrictamente: **hecho** / **afirmación** / **conocimiento** / **presentación**. Un expediente histórico no es una orden de simulación. El director narrativo no eleva candidatos a hechos: falta de evidencia ⇒ rechazo o aplazamiento, nunca completar huecos fabricando causas. UE5 representa hechos, no los promulga.

## 4. Brechas y deuda — sin duplicación
No consta aquí la integración probada de un adaptador temporal A/B/C→CoreRPG, migración del estado inicial, versionado real de eventos o aislamiento real de saves; requieren proyecto consumidor y aceptación operativa posterior. Existe deuda anterior de selectores de tres eras; no se corrige por borrado de datos históricos. Las fechas internas precisas 2383 y Valhalla siguen abiertas; no se generan día, mes, matrícula ni tripulaciones concretas. El alcance D se limita a normas, casos, validador estructural y pruebas de rechazo.
