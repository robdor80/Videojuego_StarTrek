# Auditoría técnica F03 — 30-10-2026

Auditoría local en MSI Raider GE78 HX 14VGG, Windows 11, i9-14900HX,
RTX 4070 Laptop y 32 GB. No se utiliza Codex Cloud ni una simulación de Unreal.

Antes de crear ramas se ejecutó `git fetch origin main` en ambos originales.
Star Trek: `main` local/HEAD `7ee52d59427ba9f1e027dd78200b938c37687f86`,
`origin/main` actualizado `9b33f32caab21ce0eb1ecb74cd38739b45d2f035`.
Las tres consultas `git merge-base --is-ancestor <SHA> origin/main` devolvieron 0
para `bb77c98d`, `f5ef4181` y `9b33f32`. CoreRPG local y remoto:
`4f282863737bcd8f5add401202a9e1064c133672`, exactamente la dependencia F02.
No se actualizó ni cambió de rama ninguno de los checkouts originales.

Worktrees nuevos: `codex/f03-mundo-autoritativo-persistencia-20261030`, desde
`origin/main` de Star Trek, y `codex/f03-authoritative-timeline-20261030`, desde
`origin/main` de Core. Builds/evidencias externos en `C:/F03`. No se encontraron
instrucciones AGENTS.md aplicables en los repositorios ni sus directorios padres.

## Capacidad comprobada, propietario y reutilización

Todas las rutas Core de esta tabla se inspeccionaron en el SHA base `4f282863`.
Los nombres son símbolos reales de sus cabeceras y fuentes, no APIs propuestas.
Las pruebas citadas están en `CoreRPG/tests/` y se reejecutaron en la suite completa.

| Necesidad | Ruta y símbolos comprobados | Pruebas existentes | Clasificación / decisión |
|---|---|---|---|
| Mundo e identidad | `include/corerpg/world_state.hpp`, `entity_id.hpp`; `WorldState::create_entity`, `contains`, `entity_count`, `revision`, `next_entity_id` | `world_state_test.cpp`, `world_state_integration_test.cpp`, `world_state_allocation_test.cpp` | REUTILIZABLE. ID scoped a campaña; cero inválido; no es UUID global |
| Estructura/ubicación | `entity_structure.hpp`, `world_state.hpp`; `place_entity`, `container_of`, relaciones | `entity_structure_test.cpp`, `action_test.cpp` | REUTILIZABLE. Sectores discretos del fixture; no posición física continua |
| Generación determinista | `random.hpp`, `random_streams.hpp`; `DeterministicRandom::uniform_closed`, `RandomStreams::stream`; `WorldState::materialize_population` | `random_streams_test.cpp`, `population_test.cpp`, `population_persistence_test.cpp` | ADAPTACIÓN_NECESARIA. Bootstrap Trek fijo + stream `0xF0301`; no generador galáctico |
| Catálogo | `content_catalog.hpp`; `ContentCatalog::create`, `WorldState::bind_definition` | `content_catalog_test.cpp`, `entity_structure_test.cpp` | REUTILIZABLE. Definiciones estructurales; no fingir fichas completas de nave |
| Acciones | `action.hpp`, `src/action.cpp`; `ActionEngine::process`, cinco variantes `ActionOperation`, revisión y condiciones | `action_test.cpp`, `action_determinism_test.cpp`, `action_allocation_test.cpp` | REUTILIZABLE. No añadir otro motor |
| Autorización externa | Contrato de `ActionRequest` / `ActionEngine`: Host autentica y autoriza antes de cruzar la frontera | `context_security_test.cpp`, tests Host F02 | ADAPTACIÓN_NECESARIA. Permiso Host revocable, refs de observador scoped y canales fijos; no jerarquía de Flota |
| Conocimiento | `knowledge.hpp`, `world_state.hpp`; `learn_fact`, `revoke_fact`, `knowledge_of` | `knowledge_test.cpp`, `knowledge_persistence_test.cpp`, `knowledge_allocation_test.cpp` | REUTILIZABLE. Memorias estructurales separadas de verdad; no inferencia narrativa |
| Percepción / vista | `visibility.hpp`; `Visibility::project`, `ObserverView::facts/find/knows` | `visibility_test.cpp`, `context_security_test.cpp` | ADAPTACIÓN_NECESARIA. Observación por colocalización y transmisión de subconjunto; grants nunca proceden del consumidor |
| Contexto IA | `context_builder.hpp`; `ContextBuilder::build` sobre `ObserverView` | `context_builder_test.cpp`, `context_allocation_test.cpp` | REUTILIZABLE. Ruta de lectura filtrada; no proveedor conversacional |
| Ejecución ordenada | `simulation.hpp`, `src/simulation.cpp`; `Simulation::step` | `simulation_test.cpp` | REUTILIZABLE para secuencia explícita. Declara ausencia de reloj/cola; no atribuirle una agenda |
| Reloj, agenda y recuperación temporal | No existe propietario runtime en el checkout base. Simulation no los implementa | Los tests Simulation prueban acciones, no tiempo | DEPENDENCIA_CORE → IMPLEMENTACIÓN_NUEVA en Core: `Timeline`, `TimedAction`, `TimedRecord` |
| Persistencia mundo/RNG | `persistence.hpp`, `src/persistence.cpp`; `Persistence::capture/serialize/deserialize/restore/load`, SAVE v1–v3, CRC32C | `persistence_test.cpp`, `persistence_allocation_test.cpp`, `knowledge_persistence_test.cpp`, `action_persistence_test.cpp` | REUTILIZABLE. La agenda nueva exige extensión genérica adicional |
| Archivo con agenda | No existe en base | Nuevos `timeline_test.cpp`, `timeline_allocation_test.cpp` | DEPENDENCIA_CORE → IMPLEMENTACIÓN_NUEVA: `CampaignPersistence`, contenedor aditivo `CRPGTIME` v1; SAVE previo intacto |
| EntityId ↔ Actor / UWorld | Star Trek `desarrollo/integration/f02/`, ABI C y `UF02CampaignSubsystem::Represent` | 15 tests nativos y 6 UE; regresión `WorldScopedRepresentation` | ADAPTACIÓN_NECESARIA. Se conserva F02 byte por byte; overlay F03 en laboratorio externo |
| Fecha exacta / estelar | `proyecto/docs/decisions/universal_stardate_system.md` | Fixture documental F03 y nuevo `f03.calendar` | ADAPTACIÓN_NECESARIA. Un tick = segundo; época fixture fija, calendario gregoriano, estelar derivada |
| Memoria psicológica, sensores completos, viaje galáctico, economía, NPC con agenda profesional | Contratos declarativos de memoria, generación y operaciones | Validadores estáticos no acreditan runtime | NO_APLICABLE_AL_ALCANCE del mínimo vertical. No se declara implementación de esas capas |

## Fuentes Trek contrastadas

Se revisaron el estado global, criterios de cierre, F02 (auditoría, fronteras,
README, informe de revisión PR60), los seis documentos F03, los validadores y el
fixture inerte `desarrollo/validation/fixtures/f03/continuity_reference_v0.1.json`.
El fixture documental permanece inerte e intacto; el fixture C++ nuevo es distinto.

Fuentes de contenido y restricciones aplicadas, preservadas sin mover:

- `sistemas/universe/chronology/temporal_anchors/temporal_anchors.json`, perfiles de era y decisión de fecha estelar: calendario exacto primero; no imponer futuros canónicos.
- `sistemas/universe/generation/persistent_entity_identity_contract.json`, `persistent_population_materialization_rules.json`: identidad permanente, stream estable y cupos C→B reales del Core.
- `observable_entity_model.json`, `ship_facility_offscreen_simulation_contract.json`: observar no genera verdad; descarga visual no detiene actividad.
- `sistemas/gameplay/ship_operations/sensor_resolution/sensor_result_contract.json`, `sensor_detection_rules.json`: no presentar este fixture como consola o resolución física de sensores.
- `sistemas/gameplay/ship_operations/operational_event_log/operational_event_contract.json`, `visibility_projection_rules.json`, `event_type_catalog.json`: causalidad y acceso por canal, historial privilegiado.
- `sistemas/gameplay/ship_operations/ship_memory/contact_dossier_model.json` y `sistemas/ai/memory/character_memory_lifecycle_contract.json`: conocer no equivale a verdad ni a memoria psicológica completa.
- `sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json`: restaurar estado, no regenerarlo. Persistencia general de todos sus campos queda fuera de este fixture estructural.

## Diseño mínimo decidido

Una sola autoridad Core por sesión de campaña. Trek aporta catálogo y bootstrap
determinista, una ruta discreta de prueba, política de observación y representación.
Core añade exclusivamente reloj genérico, agenda y archivo integrado. Unreal recibe
estado autorizado y crea Actors efímeros por identidad/mundo. Ni FPS ni Tick de Actor
avanzan el universo.

Referencia Core final: `9c53a33787de13d91eb2abe4da07033ee0fa1dc1`,
[PR Draft CoreRPG #12](https://github.com/robdor80/CoreRPG/pull/12).
Dependencia todavía no fusionada: impide declarar F03 integrada en `main`.
Véase [informe de ejecución y límites](INFORME_EJECUCION_2026-10-30.md).
