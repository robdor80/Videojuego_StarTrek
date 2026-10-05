# Star Trek Game Design Readiness — v0.2

Owner: project design / lore / gameplay architecture  
Status: **IN PROGRESS**

## Goal

Use the period before full CoreRPG runtime readiness to complete the game-facing Star Trek design so that future implementation does not have to invent core rules, progression, social behavior, procedural population or ship-computer semantics on the fly.

The target is not merely lore completeness. The target is:

> **validated lore + explicit gameplay rules + machine-usable contracts + clear CoreRPG boundaries**

## Eight work pillars

| # | Pillar | Status | Primary goal |
|---|---|---|---|
| 1 | Academy + career | 🟨 IN_PROGRESS | Full four-year/trimesters learning path through post-Academy professional development |
| 2 | People and life aboard | 🟨 IN_PROGRESS | NPC↔NPC and player↔NPC social simulation with memory, trust, friendship, conflict and adult relationships |
| 3 | Habits, wellbeing and daily life | 🟨 IN_PROGRESS | Long-horizon routines, recovery and character operational readiness without gamey happiness bars |
| 4 | Starfleet professional life | 🟨 IN_PROGRESS | Watches, qualifications, mentorship, evaluations, transfers, promotions and service progression |
| 5 | Gameplay-required lore | 🟨 IN_PROGRESS | Fill technology, medicine/science, conflicts, historical and operational knowledge needed by mechanics |
| 6 | AI and narrative | 🟨 IN_PROGRESS | Define AI roles, authority boundaries, dialogue, narration, interpretation and context routing |
| 7 | Procedural universe and population | 🟨 IN_PROGRESS | Generate coherent persistent systems, worlds, traffic, ships, crews, NPCs and local activity |
| 8 | Starship Computer | 🟨 IN_PROGRESS | Canon-feeling neutral computer interface, access control, deterministic queries/actions and routed AI assistance |

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

A pillar may have a complete foundation while its content catalogue remains progressive.

## Runtime dependency

Design work proceeds independently.

Runtime implementation is deferred where CoreRPG does not yet expose the required generic world-state, action, simulation, persistence or event capabilities.

## Current sequence

1. Formalize Academy + career v0.2.
2. Establish social/relationship foundation.
3. Establish habits/wellbeing foundation.
4. Establish professional-service foundation.
5. Build gameplay-lore readiness backlog.
6. Consolidate AI/narrative architecture.
7. Expand procedural generation from vertical-slice seed to full-universe framework.
8. Establish Starship Computer service architecture.

Work may then cycle back through all eight pillars for increasing content depth.
