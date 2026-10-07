# Star Trek Procedural Development Master Plan v0.1

Status: **ACTIVE — MASTER WORK PLAN**

## Purpose

Turn `Videojuego_StarTrek` into the authoritative Star Trek-specific data/rules layer required by the future CoreRPG + Unreal Engine 5 game and by the NAP asset pipeline.

This plan does not replace the existing `PROCEDURAL_UNIVERSE_BIBLE_v0.1` or existing contracts. It organizes, audits and completes them.

## Prime principles

1. **Generate reality first. Observe it second.**
2. **Structure before individual.**
3. **Stable identity before presentation.**
4. **Species is not culture and neither is personality.**
5. **World State is authoritative; AI expresses it.**
6. **LOD reduces simulation cost, never existence.**
7. **Persistent materialized entities never silently reroll.**
8. **Visual generation consumes world truth; it does not create world truth.**
9. **NAP compatibility is a design requirement from the beginning.**

## Authority layers

```text
CoreRPG generic simulation semantics
→ campaign era/date
→ canon reservations/history
→ polity / affiliation / operator
→ species + culture
→ organization / entity class / function
→ local context
→ instance identity
→ live World State
```

Visual resolution is compositional rather than a single inheritance chain. Example:

```text
global Trek visual rules
+ era
+ species biology
+ culture
+ affiliation
+ organization
+ uniform family
+ division
+ rank
+ individual identity
+ current visual state
→ resolved visual specification
→ NAP production request
```

## Workstreams

### P0 — Architecture and governance
- procedural domain inventory;
- Star Trek ↔ Nimroel reuse matrix;
- CoreRPG ownership boundary;
- stable ID and derived-seed policy;
- rules/version migration;
- validation registry;
- NAP handoff contract.

### P1 — Characters and living population
- population tiers A/B/C;
- identity and demographics;
- physiology;
- culture;
- naming;
- personality;
- needs;
- emotion/mood/stress;
- knowledge;
- memory/forgetting;
- relationships/social circles;
- family/kinship/partnership;
- schedules/routines;
- career/employment;
- residence/quarters;
- possessions;
- health/injury/disability;
- death/grief/legacy;
- visitors/passengers/transient populations.

### P2 — Organizations and societies
- Federation;
- Starfleet;
- Vulcan institutions;
- Klingon institutions;
- Romulan institutions;
- Cardassian institutions;
- Bajoran institutions;
- Ferengi institutions;
- Dominion;
- Borg;
- independent/minor civilizations;
- government, law, diplomacy, economy, services and logistics.

### P3 — Astrography and worlds
- sectors/regions;
- stellar systems;
- stars and orbital bodies;
- planets/moons;
- atmosphere/hydrosphere/geology;
- climate/weather continuity;
- biospheres/ecosystems;
- resources;
- civilizations;
- settlements;
- planetary infrastructure;
- anomalies/subspace phenomena;
- exploration/contact/knowledge state.

### P4 — Ships, facilities and traffic
- ship design grammars;
- canonical class reservations;
- procedural classes where allowed;
- individual vessel identity/history;
- departments/posts/shifts;
- crew generation;
- interiors/decks/compartments;
- stations/starbases/outposts;
- shipyards/depots/relays;
- civilian traffic;
- logistics/routes;
- damage/repair/refit;
- detectable signatures.

### P5 — Star Trek technology and exceptional beings
- warp/impulse;
- transporters;
- replicators;
- sensors;
- communications;
- shields/weapons;
- medical technology;
- holodecks/holograms;
- android/artificial life;
- telepathy/empathy;
- Trill symbiosis;
- Borg assimilation;
- Changelings;
- cloning;
- stasis/hibernation;
- temporal/subspace edge cases;
- non-humanoid life.

### P6 — Academy and career lifecycle
- living Academy population;
- cohorts/classes/schedules;
- instructors/services/residences;
- training/evaluations;
- seven specializations;
- graduation;
- first assignment;
- transfers/promotions/discipline;
- persistent relationships carried into service.

### P7 — Visual Bibles and NAP
- global visual bible;
- era profiles;
- species visual profiles;
- culture visual profiles;
- affiliation/organization profiles;
- uniform system;
- rank/division insignia rules;
- character/portrait rules;
- ship exterior rules;
- ship interior rules;
- facility/settlement rules;
- planet/environment rules;
- equipment/prop rules;
- current-state overlays (damage, dirt, injury, weather, lighting);
- prompt-resolution contract;
- visual identity contract;
- NAP production metadata/manifest contract.

### P8 — Simulation and consequences
- event causality;
- off-screen/catch-up simulation;
- economy/resource movement;
- politics/conflict;
- missions from existing world state;
- environmental continuity;
- births/deaths/migration;
- history/legacy.

### P9 — Validation and readiness
- deterministic replay;
- canonical collision;
- era legality;
- population conservation;
- staffing/qualification;
- schedule/location consistency;
- knowledge provenance;
- relationship provenance;
- species/culture anti-stereotype;
- visual inheritance validation;
- NAP package validation;
- UE5/CoreRPG handoff readiness.

## NAP boundary

The Star Trek repository owns **authoritative source rules and production metadata**, not archival masters.

Target lifecycle:

```text
Star Trek procedural truth
→ resolved visual specification
→ visual bible/profile stack
→ generation/review
→ NAP ingest
→ AI PASS
→ archival master handled by NAP ArchiveRoot
→ production derivative + legitimate metadata handled by NAP ProductionRoot
→ game/UE5 consumption
```

The repository must not assume that master PNGs belong beside production assets. Production assets must be reproducible/traceable through stable IDs, provenance, bible versions and prompt/visual-identity metadata.

## Initial visual-bible families

```text
art_direction/
  visual_bibles/
    global/
    eras/
    species/
    cultures/
    affiliations/
    organizations/
    uniforms/
    characters/
    ships/
    interiors/
    facilities/
    planets/
    environments/
    equipment/
  schemas/
  nap/
```

These folders contain rules/profiles/contracts. Existing `assets/` remains the logical asset-facing area until the NAP production-root integration contract is finalized; do not duplicate binary masters into the bible tree.

## Definition of done for a procedural domain

A domain is not COMPLETE until it has, where applicable:

- authority/ownership;
- inputs and outputs;
- stable IDs;
- deterministic seed policy;
- generation rules;
- persistence rules;
- live-state/event rules;
- cross-domain dependencies;
- canonical/era constraints;
- validation invariants;
- AI boundary;
- visual/NAP implications;
- migration/versioning considerations;
- at least one representative test fixture or example.

## Current priority

1. complete repository audit;
2. build Star Trek ↔ Nimroel reuse matrix;
3. establish visual/NAP contracts;
4. close character/population foundations;
5. close species/culture composition;
6. close ships/crew;
7. close worlds/settlements;
8. expand technology/special cases;
9. global validation/readiness.

## Author-decision gate

Implementation may proceed autonomously unless a change would establish or alter:
- playable canon/era;
- major gameplay philosophy;
- simulation scope limits;
- species representation;
- reproduction/relationship boundaries;
- death/content boundaries;
- major political/canonical divergence.

Those decisions remain authorial.

## Dynamic-universe deepening sequence

The structural procedural baseline remains closed through the existing master-layer plan. Detailed long-horizon simulation depth is now tracked separately by:

`docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`

Current sequential state:
- **Block 1 — Procedural Civilization Evolution & Galactic Interaction: COMPLETE**;
- **Blocks 2–10: not implemented**;
- the next eligible block is **Block 2 — Colonization, Expansion & Borders**, but it is not started by this update.

This separation prevents the earlier 001–118 design-readiness closure from being mistaken for completion of all detailed dynamic-universe behavior.

### Dynamic-universe sequence update

- Block 1 — Procedural Civilization Evolution & Galactic Interaction: COMPLETE.
- **Block 2 — Colonization, Expansion & Borders: COMPLETE.**
- Blocks 3–10 remain unimplemented; Block 3 is next in strict sequence.
