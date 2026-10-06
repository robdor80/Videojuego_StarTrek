# NIMROEL → STAR TREK — PROCEDURAL REUSE MATRIX v0.1

**Status:** ACTIVE AUDIT  
**Purpose:** classify what Star Trek can inherit conceptually or structurally from Nimroel without importing setting-specific assumptions.

## Classification
- **A — Core candidate:** reusable almost directly as generic simulation semantics.
- **B — Adapt:** strong reusable model, requires Star Trek extensions.
- **C — Concept only:** keep principle, redesign contract/data.
- **D — Setting-specific:** do not migrate.
- **E — Trek extension:** Star Trek needs capabilities beyond Nimroel.

## Audited matrix

| Domain | Nimroel evidence | Current Star Trek evidence | Class | Action |
|---|---|---|---|---|
| Persistent population A/B/C | Treskal NPC population contract | persistent_population_materialization_rules | A/B | Preserve irreversible C→B promotion; strengthen permanent identity and visual identity |
| Stable entity identity | persistent NPC promotion and LOD rules | persistent_entity_identity_contract + context hierarchy | A | Treat as generic CoreRPG invariant; Trek adds species/canon/registry anchors |
| Deterministic generation | deterministic Treskal materialization | derived subsystem seeds in context hierarchy | A | Standardize seed provenance and migration |
| Memory vs World Truth | Nimroel memory salience/forgetting Core contract | ai/memory/character_memory_contract | A/B | Merge semantics: salience, gist, uncertainty, reinterpretation, no fabricated recall |
| Relationship dimensions | Nimroel affective pairing Core contract | Trek relationship refs currently distributed | A/B | Create generic multidimensional relationship state; add Trek professional/service dimensions |
| Kinship/family | Nimroel kinship network Core contract | population brief requires species-aware family | B/E | Reuse graph semantics; Trek must support non-human reproduction, Trill/Changelings/etc. |
| Personality independence | Nimroel NPC principles | personality_state_model | A | Keep species/culture/personality separation invariant |
| Knowledge provenance | Nimroel knowledge provenance + NPC contracts | Trek knowledge/memory/dialogue rules | A/B | Unify source/provenance semantics and access channels |
| Schedules/routines | Treskal routines/activity | activity_schedule_model | B | Add duty shifts, transporters, travel, ship alert states, Academy timetable |
| Commerce/inventory | Treskal provider/stock persistence | Trek logistics/economy domains | C/E | Rebuild for replicator/post-scarcity/local scarcity/operator constraints |
| Visual identity | Nimroel portrait visual_identity packages | Trek visual/NAP contract | B | Preserve stable identity anchor; add era/species/culture/affiliation/org/uniform composition |
| Portrait state/patina | NPC Portrait Bible v0.3 | visual/NAP identity-vs-state rule | B | Translate from medieval wear to duty/off-duty, contamination, damage, medical state, environment |
| Culture profiles | Norgard + local profiles | Trek species/culture/affiliation split required | B/E | Use compositional profiles; never collapse species into culture |
| Settlement/world state | Treskal World State and access contracts | planetary/environment generation | B/E | Extend to planetary scale, advanced infrastructure, transport, comms and offscreen simulation |
| Vessel simulation | Nimroel vessel navigation contract | procedural_starship_rules | C/E | Retain causal vessel existence; Trek requires warp, impulse, crew departments, sensors, damage/refit |
| Canon/era reservations | not equivalent | Trek context hierarchy/canon history | E | Trek-only authority layer |
| Starfleet chain of command | not equivalent | character runtime institutional fields | E | Trek-only organization/service layer |
| Exceptional beings/technology | not equivalent | planned Trek domains | E | Trek-specific contracts and validation |

## Decisions fixed by audit

1. **Core semantics are reused; setting assumptions are not.**
2. **Materialized identity is permanent.** Generator upgrades, LOD, save/load and elapsed time cannot reroll it.
3. **History changes state, not identity.**
4. **Visual generation consumes entity identity and World State. It never creates replacement identity.**
5. **Species, culture, citizenship, affiliation, organization, rank, position, personality and current state remain separate dimensions.**
6. **AI expresses authorized state; it does not manufacture missing world facts.**
7. **Star Trek extensions remain explicit instead of contaminating generic CoreRPG contracts.**

## Next audit blocks
- complete character lifecycle: birth/creation → development → career → aging → death/legacy;
- relationship graph and social provenance;
- species/culture/biology;
- organizations, ranks, posts and crew structure;
- ships/facilities;
- planets/civilizations;
- technology and exceptional lifeforms;
- visual schemas and NAP handoff;
- cross-domain validation fixtures.

This matrix is deliberately versioned. New findings update the matrix rather than silently changing earlier classifications.
