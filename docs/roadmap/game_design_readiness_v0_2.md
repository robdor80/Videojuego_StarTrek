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

## Design-depth pass 1 progress

### Pillar 1 — closed entry sub-blocks

- ✅ **Academy Access v1.0 locked**: five-block general candidate curriculum, candidate manual source, holistic admission review and targeted reassessment.
- ✅ **Player profile + character creation v1.0 locked**: nickname separated from in-world identity; adult-equivalent rule; no manual attributes/skill points.
- ✅ **Mandatory biography validation locked**: deterministic hard checks plus semantic coherence review before the character can enter the campaign.
- ✅ **Evidence-based character growth locked**: study, practice, habits, instruction, simulation and live experience change capabilities; no generic visible XP.
- ✅ **Objectives and trajectory locked**: one primary long-term aspiration plus a small set of medium-term goals; descriptive coherence, no completion percentage and no goal-spawned world events.
- ✅ **Specialization timing locked**: choice by the end of Third Class, formal specialization begins in Second Class.
- ✅ **Kobayashi Maru normalized as a project-wide Academy tradition** across Pike, Kirk and TNG/DS9/Voyager with era-appropriate implementation.
- ✅ **Fourth Class / Year 1 architecture locked v1.0**: three trimesters, five grouped subjects per trimester, with PHY as a longitudinal line and professional specialization explicitly deferred.
- ✅ **Third Class / Year 2 architecture locked v1.0**: supervised ship operations → people/risk/field action → integration/leadership/branch choice.
- ✅ **Second Class / Year 3 architecture locked v1.0**: formal specialization → complex/degraded operations → supervised professional competence and intermediate qualification.

### Earlier design-depth progress

- ✅ Academy master curriculum baseline: year → trimester → subject structure created.
- ✅ External Academy study/profile interoperability contract created.
- ✅ Social event transitions and knowledge-propagation rules created.
- ✅ Wellbeing activity inputs and emergent habit-formation rules created.
- ✅ Professional evidence and career-progression rules created.
- ✅ Game-ready contracts created for technology, medicine, science, conflicts and historical events.
- ✅ Restrained AI narration rules added; deterministic-first orchestration already established.
- ✅ Procedural celestial/civilization generation requirement contracts added.
- ✅ Starship Computer query/action catalogue added.

## Next design-depth priorities

1. Complete the **First Class / Year 4 grouped-subject architecture** with Roberto before any unit-level deployment. Once all four years are locked, begin the autonomous deployment pass starting with Fourth Class / Trimester 1.
2. Build **branch curricula** for Command, Flight/Navigation, Operations, Engineering, Tactical/Security, Science/Sensors and Medical.
3. Define **professional evaluation/recommendation outputs** that consume operational evidence without becoming global scores.
4. Start concrete **technology/equipment, medicine/science and historical-conflict content packs** with provenance.
5. Add **procedural generation grammars and distributions** for ordinary stars/planets, civilizations, ship roles/operators, facilities and traffic.
6. Define **AI context filtering/assembly implementation requirements** in a form compatible with CoreRPG/Host privacy boundaries.
7. Expand **Starship Computer integration** with records/logs, crew lookup, ship status, navigation and analysis.
8. Add validation rules checking cross-pillar contradictions as the content grows.

## Pillar 1 current boundary

The following are now **closed to the current defined scope** and should only reopen for explicit revision or discovered contradiction:

- access curriculum and admission philosophy;
- pre-game player profile / nickname distinction;
- initial character sheet structure;
- mandatory character-coherence validation;
- growth through life evidence rather than point allocation;
- long-term and medium-term objective semantics;
- specialization selection timing;
- project-wide Kobayashi Maru tradition;
- Fourth Class / Year 1 three-trimester grouped-subject architecture;
- Third Class / Year 2 three-trimester grouped-subject architecture;
- Second Class / Year 3 three-trimester specialization architecture.

The remaining Pillar 1 work is primarily **First Class / Year 4 architecture, then autonomous unit-level deployment of all four years, branch curriculum depth, Academy-life scheduling/content, evaluation outputs and post-Academy career depth**.

## Roberto decision policy

Work continues autonomously while rules can be derived from already approved principles and repository architecture.

If a choice would materially determine creative canon/gameplay direction and is not already approved, mark it `NEEDS_ROBERTO` and stop that branch rather than silently deciding it.
