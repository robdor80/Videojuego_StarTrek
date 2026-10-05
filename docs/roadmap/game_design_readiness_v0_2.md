# Star Trek Game Design Readiness — v0.2

Owner: project design / lore / gameplay architecture  
Status: **IN PROGRESS**

## Goal

Use the period before full CoreRPG runtime readiness to complete the game-facing Star Trek design so that future implementation does not have to invent core rules, progression, social behavior, procedural population or ship-computer semantics on the fly.

The target is not merely lore completeness. The target is:

> **validated lore + explicit gameplay rules + machine-usable contracts + clear CoreRPG boundaries**

## Eight work pillars

| # | Pillar | Foundation | Content depth | Primary goal |
|---|---|---|---|---|
| 1 | Academy + career | ✅ ESTABLISHED | 🟨 IN_PROGRESS | Full four-year/trimesters learning path through post-Academy professional development |
| 2 | People and life aboard | ✅ ESTABLISHED | 🟨 IN_PROGRESS | NPC↔NPC and player↔NPC social simulation with memory, trust, friendship, conflict and adult relationships |
| 3 | Habits, wellbeing and daily life | ✅ ESTABLISHED | 🟨 IN_PROGRESS | Long-horizon routines, recovery and character operational readiness without gamey happiness bars |
| 4 | Starfleet professional life | ✅ ESTABLISHED | 🟨 IN_PROGRESS | Watches, qualifications, mentorship, evaluations, transfers, promotions and service progression |
| 5 | Gameplay-required lore | ✅ READINESS PLAN | 🟨 IN_PROGRESS | Fill technology, medicine/science, conflicts, historical and operational knowledge needed by mechanics |
| 6 | AI and narrative | ✅ ESTABLISHED | 🟨 IN_PROGRESS | Define AI roles, authority boundaries, dialogue, narration, interpretation and context routing |
| 7 | Procedural universe and population | ✅ ESTABLISHED | 🟨 IN_PROGRESS | Generate coherent persistent systems, worlds, traffic, ships, crews, NPCs and local activity |
| 8 | Starship Computer | ✅ ESTABLISHED | 🟨 IN_PROGRESS | Canon-feeling neutral computer interface, access control, deterministic queries/actions and routed AI assistance |

## Foundation pass completed

The first architecture pass now includes:

### 1 — Academy + career
- `gameplay/careers/academy_path/academy_career_v0_2.md`
- three-trimester year model;
- Academy state aligned away from standalone fatigue/stress meters;
- Kobayashi Maru capstone rules;
- post-Academy mentorship/qualification foundation.

### 2 — People and life aboard
- `gameplay/social/`
- multidimensional directional relationship graph;
- friendship/professional/romantic distinctions;
- adult consent/privacy rules;
- social simulation LOD.

### 3 — Habits, wellbeing and daily life
- `gameplay/characters/wellbeing/`
- acute vs longitudinal state;
- 24h/7d/30d windows;
- preference-aware recovery;
- cognitive-assistance gameplay translation.

### 4 — Starfleet professional life
- `gameplay/careers/starfleet_service/`
- evidence-based professional evaluation;
- promotion/transfer rules;
- qualifications and mentorship.

### 5 — Gameplay-required lore
- `docs/roadmap/gameplay_lore_readiness.md`
- technology root made generation/gameplay-aware;
- explicit backlog for technology/equipment, medicine/science, conflicts/history, species, factions, astrography and non-combat infrastructure.

### 6 — AI and narrative
- `ai/README.md`
- `ai/runtime_orchestration.md`
- `gameplay/interactions/npc_interaction_framework.md`
- deterministic-first routing and no direct AI state mutation.

### 7 — Procedural universe and population
- `universe/generation/PROCEDURAL_UNIVERSE_BIBLE_v0.1.md`
- generator-domain catalogue;
- starship-role generation;
- population generation;
- traffic/activity model.

### 8 — Starship Computer
- `gameplay/ship_operations/ship_computer/`
- neutral Starfleet computer personality;
- access control;
- request contract;
- deterministic/fast/reasoning routing;
- console separated from ship-wide service.

## Cross-cutting systems already established

- authoritative observable universe;
- deterministic minimal procedural generator;
- Sensors v0.1;
- Operational Event Log;
- Records and Logs including Captain's / Personal / Department / Duty Logs;
- universal project stardate rule;
- service record foundation;
- character memory and dialogue-context constraints;
- Starfleet institutional baseline.

## Architecture rules

1. **Generate reality first. Observe it second.**
2. **AI may interpret and express; it does not own world truth.**
3. **CoreRPG owns generic authoritative state/rules/actions/persistence.**
4. **Videojuego_StarTrek owns Star Trek-specific content, constraints, behaviors and presentation contracts.**
5. **The same real systems used in service are used in Academy training.**
6. **No duplicate Star Trek-only engine is created to bypass missing CoreRPG capability.**
7. **Professional progression should emerge from evidence, qualifications and responsibility rather than a visible generic XP bar.**
8. **Social, lifestyle and AI systems must preserve player agency and NPC knowledge limits.**

## Delivery strategy

Each pillar is developed in two layers:

### Foundation
- vocabulary;
- ownership boundaries;
- state/contracts;
- gameplay loops;
- integration points;
- prohibited shortcuts.

### Content depth
- era/species/faction/class-specific data;
- course content;
- procedural distributions;
- concrete examples;
- validation suites;
- player-facing material.

The first foundation pass is complete. The project now cycles through the pillars to add content depth and consistency.

## Runtime dependency

Design work proceeds independently.

Runtime implementation is deferred where CoreRPG does not yet expose the required generic world-state, action, simulation, persistence or event capabilities.

## Next design-depth priorities

1. Build the **Academy master curriculum** down to year → trimester → subject → unit, before mass-producing Sensors exercises.
2. Define **social event/state transitions** and knowledge propagation from real events into memories/relationships.
3. Define **wellbeing activity inputs and habit formation** without exposing optimization bars.
4. Connect **professional evidence** to formal evaluation, recommendations and career opportunities.
5. Begin concrete **technology/equipment + medicine/science lore packs** required by Academy and procedural generation.
6. Define **AI context assembly and privacy filters** for dialogue/computer/log drafting.
7. Add **procedural generation grammars/profiles** for stars, worlds, civilizations, ship roles/operators, facilities and traffic.
8. Expand **Starship Computer command/query catalogue**, profiles by era/civilization and integrations.

## Roberto decision policy

Work continues autonomously while rules can be derived from already approved principles and repository architecture.

If a choice would materially determine creative canon/gameplay direction and is not already approved, mark it `NEEDS_ROBERTO` and stop that branch rather than silently deciding it.
