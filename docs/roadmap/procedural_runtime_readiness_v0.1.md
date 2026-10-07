# STAR TREK — PROCEDURAL RUNTIME READINESS v0.1

**Status:** STAR TREK DESIGN READY / RUNTIME DEPENDENCY OPEN  
**Control plan:** `docs/roadmap/procedural_layers_master_plan_v0.1.md`  
**Master validation:** `validation/consistency/procedural_master_acceptance_v0.1.json`

---

## 1. Result

The Star Trek repository now has a coherent procedural design baseline covering:

- authority, canon/campaign precedence and provenance;
- stable persistent identity;
- deterministic generation and migration;
- characters, personality, knowledge, memory and relationships;
- kinship, species biology, culture and lifecycle;
- organizations, Starfleet service and career;
- ships, staffing, watches, facilities and shipboard life;
- astrography, planets, biospheres, settlements and civilizations;
- movement, logistics, economy and diplomacy;
- technology, communications, transporters and exceptional entities;
- visual identity, Visual Bibles and NAP handoff;
- off-screen simulation, events, consequences, death and emergent missions;
- cross-domain validation and a Sensors vertical-slice acceptance fixture.

This is a **design/content-contract readiness statement**, not a claim that the complete game runtime already exists.

---

## 2. Core architecture now fixed

### Reality

`authoritative World State → observation/knowledge → presentation`

Never:

`player asks / AI needs drama → invent hidden World Truth retroactively`

### Persistent identity

`persistent identity + authoritative history + current state = current entity`

Materialized entities are loaded/evolved, not rerolled.

### Generation

Persistent procedural variation uses isolated derived seeds:

`campaign_seed + stable_entity_id + subsystem_key + rules_version`

### AI

AI may:
- interpret;
- phrase;
- summarize;
- roleplay;
- return candidate intents/actions.

AI may not:
- directly mutate authoritative World State;
- invent hidden facts;
- bypass capability, authority or knowledge constraints.

### Visual/NAP

`World/Entity State → resolved visual context → Visual Bibles/profiles → asset request → NAP → production asset`

Entity-backed assets preserve `entity_id` and `visual_identity_id` lineage.

---

## 3. Validation coverage

The master acceptance index references dedicated validation packs for:

1. governance and authority;
2. identity, persistence, save/load and LOD;
3. persistent population;
4. cognition, memory and social state;
5. species, culture and lifecycle;
6. organizations, service and career;
7. ships, crew and facilities;
8. planets and civilizations;
9. movement, logistics, economy and diplomacy;
10. technology and exceptional states;
11. visual system and NAP;
12. living simulation, events and consequences.

The Sensors v0.0.1 acceptance fixture provides the first end-to-end representative case.

---

## 4. Sensors vertical slice

Star Trek-side contracts already define:

`generated persistent system`
→ `pre-existing signatures`
→ `sensor request`
→ `deterministic detection resolution`
→ `observer-relative result`
→ `knowledge/presentation`
→ `append-only operational events`

The acceptance fixture uses campaign date **2372-03-14**, inside the approved `tng_ds9_voyager` playable era.

The former worked example date 2399 was corrected because it fell outside current playable scope.

---

## 5. Verified CoreRPG dependency

Current CoreRPG `main` was re-audited before this readiness statement.

Verified current state:

- Phase **4.4 — Content Pack System** is closed.
- `WorldState` remains intentionally minimal.
- It currently owns monotonic `EntityId` creation, containment/count and revision.
- General live domain records are not implemented.
- The general `DefinitionId → EntityId` instantiation bridge is not implemented.
- Generic gameplay persistence, population, knowledge and simulation are not implemented.
- CoreRPG documentation explicitly places **Generic World State** in phase **4.5**.

Therefore:

> **Do not implement a parallel RPG engine inside Videojuego_StarTrek.**

The Star Trek repository is now a strong source of real requirements for CoreRPG 4.5+.

---

## 6. Runtime gate

Full runtime readiness requires CoreRPG to provide, at minimum:

1. generic live entity records;
2. definition → persistent instance materialization with provenance;
3. authoritative mutable World State;
4. generic action/validation pipeline;
5. deterministic subsystem support;
6. event/state mutation model;
7. save/load persistence and migration;
8. simulation/LOD hooks;
9. observer knowledge/perception support sufficient for Sensors;
10. Content Pack mapping for Star Trek domain definitions.

UE5/Host then presents those systems; it does not own reality.

---

## 7. What is deliberately not duplicated

This repository must not implement its own competing:

- generic Entity system;
- generic World State;
- generic persistence engine;
- generic action engine;
- generic event engine;
- generic simulation scheduler;
- generic Content Pack loader.

Star Trek defines the **requirements and content** those systems must satisfy.

---

## 8. Development status

The 120-layer plan can now be treated as having:

- Layers 001–118: procedural design/contracts/validation baseline closed.
- Layer 119: Star Trek-side Sensors acceptance fixture defined; executable gameplay/UX completion remains in the existing console vertical-slice roadmap.
- Layer 120: runtime integration blocked on CoreRPG 4.5+ and later generic runtime capabilities.

This is not a design blocker. It is the intended architectural dependency.

---

## 9. Next autonomous workstream

While CoreRPG advances, Star Trek can continue safely in parallel with **content depth** rather than reimplementing the engine:

- expand concrete species biology/culture profiles from validated canon;
- expand faction/organization profiles;
- expand starship classes/configurations and source-backed interiors;
- expand planetary/civilization generation grammars;
- build visual profiles and reference packs for the three playable eras;
- prepare Star Trek Content Pack mappings against the evolving CoreRPG contract;
- continue Academy/Sensors UX and other console presentation design where runtime-independent.

All such additions must satisfy the contracts and validation packs already established.
