# Procedural Living Universe Depth Plan v0.1

Status: **FOUNDATION FIXED — CONTENT/IMPLEMENTATION DEPTH PENDING**

## Purpose

Deepen Star Trek procedural generation from macro world population into a causally coherent living universe: ships, stations, colonies and planets must contain people who exist for a reason, have stable identities when materialized, belong to real organizational/social structures, follow schedules, know only what they can know, form persistent relationships and continue to exist when the player is not looking at them.

This plan is informed by the reusable architecture proven in the Nimroel project. It imports **simulation patterns**, not fantasy-specific content.

## Core lesson imported from Nimroel

The strongest reusable pattern is layered authority:

```
universal simulation rules
        ↓
era / polity / culture defaults
        ↓
organization / entity-class rules
        ↓
local context
        ↓
instance-specific overrides
        ↓
authoritative World State
```

Generated content is not a bag of independent random rolls. Each lower layer inherits constraints from the layers above and may override only where explicitly allowed.

Star Trek already has the macro procedural foundation. This plan closes the micro-simulation gap.

## 1. Context-resolution hierarchy

Star Trek procedural generation must resolve context in this order:

1. generic simulation/CoreRPG capability;
2. campaign date and playable era;
3. canonical reservations and known history;
4. polity/faction/operator;
5. civilization/species/culture context;
6. entity class and function;
7. local location context;
8. instance-specific authored/generated state;
9. live World State and campaign history.

Species and culture are **compositional constraints**, not rigid inheritance. A Vulcan raised on Earth, a Human citizen of another polity or a multi-species station must remain possible when canon/context allows it.

## 2. Population materialization model

### Tier A — authored/canonical persistent characters

Defined by canon, authored content or explicit campaign design.

- persistent from the start;
- never replaced by procedural generation;
- procedural systems may fill missing runtime state only within authored constraints.

### Tier B — generated persistent individuals

Materialized from a real population/staffing slot.

Once created they receive stable identity and persist:

- stable character ID;
- origin seed/provenance;
- species and culture context;
- residence/quarters;
- assignment/employment/function;
- schedule/shift context;
- qualifications;
- personality seed/state;
- knowledge state;
- memory state;
- relationship references;
- current live state.

Materialization is irreversible. They are not rerolled because the player leaves.

### Tier C — latent population

Represents people who canonically exist but do not yet need full individual simulation.

Examples:

- most crew on a large starship;
- station residents;
- passengers;
- planetary settlement population;
- academy background population.

Tier C stores enough aggregate structure to preserve:

- headcount;
- role/department distribution;
- species/culture distribution where relevant;
- shift coverage;
- residence capacity;
- family/household or social-unit structure where relevant;
- vacancies;
- visitor/passenger counts.

When an individual becomes relevant, the system promotes one deterministic latent slot into Tier B rather than spawning a new person outside the population.

## 3. Generate structure before individuals

The generator must not create arbitrary NPCs and invent their reason for existing afterward.

### Starfleet / organized starship

```
ship role + class + mission
→ departments/functions
→ positions
→ shift coverage
→ qualification requirements
→ latent staffing slots
→ persistent individuals
```

### Station / facility

```
facility function
→ required services
→ staffing/security/logistics
→ resident + worker + visitor populations
→ schedules/shift coverage
→ persistent individuals
```

### Colony / planetary settlement

```
civilization + settlement role
→ infrastructure/economy/services
→ residential/social structure
→ population bands
→ institutions/occupations
→ households/family units where culturally valid
→ persistent individuals
```

### Civilian vessel

```
operator + vessel role + route
→ required crew
→ passenger/cargo demand
→ duty structure
→ transient population
→ persistent individuals as needed
```

## 4. Deterministic randomness

One global sequential RNG is forbidden for persistent world construction.

Every important subsystem derives its own seed from stable context:

```
campaign_seed
+ stable_entity_id
+ subsystem_key
+ rules_version
```

Suggested subsystem keys:

- identity;
- naming;
- species_population;
- culture;
- residence;
- career_or_assignment;
- qualifications;
- personality;
- knowledge;
- memory;
- relationships;
- social_circles;
- schedule;
- appearance;
- possessions;
- local_activity.

Adding a new subsystem must not silently reroll unrelated existing results.

Visible names never define technical identity.

## 5. Species, culture and individual identity

Species may constrain or inform:

- physiology;
- lifespan;
- environmental compatibility;
- medical requirements;
- sensory/capability limits;
- reproduction/kinship possibilities where relevant;
- language/translator context;
- canon-valid demographic plausibility.

Species must **not** directly determine:

- morality;
- personality;
- loyalty;
- political opinion;
- friendship;
- competence;
- romantic preference;
- individual behavior.

Culture/polity may supply norms, institutions, naming profiles and probability biases, but individual state remains character-specific.

## 6. Relationships and social circles

Initial relationships require a plausible shared context.

Possible generators include:

- same household/family;
- same Academy cohort;
- same department;
- same duty shift;
- long shared assignment;
- mentorship chain;
- neighborhood/residential proximity;
- repeated social venue;
- prior mission/event history.

No relationship is created merely because two NPCs are currently in the same scene.

Relationship state remains directional and multidimensional using the existing relationship graph.

## 7. Knowledge and memory

Generated NPCs are never omniscient.

Knowledge may derive from:

- direct experience;
- professional role;
- authorized records;
- training;
- local familiarity;
- conversation/disclosure;
- formal reports;
- witnessed events;
- rumor with uncertainty.

Memory is actor-specific and may preserve gist while losing detail. It cannot rewrite World State.

AI dialogue receives filtered knowledge/memory context; it does not read hidden global truth.

## 8. Agenda, routines and availability

A persistent character needs temporal plausibility.

The future runtime should distinguish:

- duty/shift obligations;
- scheduled professional tasks;
- travel time;
- meals/rest/recreation;
- medical appointments;
- training;
- social commitments;
- family/private commitments where relevant;
- emergencies and interruptions.

A character cannot perform incompatible activities simultaneously.

The player beginning a conversation does not magically create free time or teleport a person to the requested location.

Expected presence derives from schedule + current state; it is not a forced spawn rule.

## 9. Environmental generation — lesson from Nimroel climate

Nimroel's strongest environmental lesson also transfers:

> **existence and current state are separate.**

For planetary environments:

```
star/orbit
+ rotation/axial context
+ atmosphere
+ hydrosphere
+ geography
+ latitude/altitude
+ season
+ recent weather history
= plausible local environmental state
```

A biome/climate label supplies context, not the final weather.

For ships/stations, the equivalent is:

```
design
+ life support
+ compartment
+ power
+ damage
+ contamination/radiation
+ current operations
= local environmental state
```

Environment must persist and evolve causally rather than reset when the player re-enters an area.

## 10. Network coherence before local randomness

Nimroel generates settlements inside a regional network. Star Trek should apply the same principle at larger scales.

Examples:

- facilities generate traffic needs;
- mining creates haulage;
- colonies create supply/passenger demand;
- shipyards create repair/refit traffic;
- borders create patrol/customs activity;
- wars alter routes and staffing;
- research regions create science traffic;
- a station's services constrain what nearby ships depend on it for.

Local generation must know nearby infrastructure and avoid absurd duplication or unexplained functional deserts.

## 11. Validation invariants

Generation must be validated, not only randomized.

Required invariant families:

- canonical identity collision prevention;
- date/era legality;
- species/culture/faction plausibility;
- staffing and shift coverage;
- qualification coverage;
- population conservation during Tier C → Tier B promotion;
- no duplicate occupancy of incompatible duty posts;
- residence/quarters capacity;
- visitor/passenger separation from permanent population;
- relationship provenance;
- knowledge provenance;
- schedule compatibility;
- local service/infrastructure coverage;
- deterministic reproducibility;
- no silent reroll after generator/rules upgrades.

## 12. CoreRPG boundary

Generic simulation semantics should ultimately live in CoreRPG when they are universe-independent:

- stable entity identity;
- deterministic sub-seeding;
- population LOD/materialization;
- schedules;
- memory/knowledge containers;
- relationship primitives;
- environmental persistence;
- causal event application;
- migration/versioning.

`Videojuego_StarTrek` owns:

- Star Trek era rules;
- canonical reservations;
- species/culture/polity profiles;
- Starfleet organization;
- ship/station/civilization grammars;
- technology constraints;
- player-facing presentation and Star Trek-specific behavior.

Do not duplicate a Star Trek-only engine when the concept belongs in CoreRPG.

## 13. Implementation order

### Phase A — architecture
- context hierarchy contract;
- population materialization contract;
- derived-seed contract;
- validation invariants.

### Phase B — Starfleet crew/station depth
- crew slot → latent person → persistent NPC;
- shifts, quarters, availability;
- initial professional/social graph generation.

### Phase C — species/culture composition
- species demographic compatibility;
- culture/naming/language profiles;
- environmental/medical constraints;
- anti-stereotype validation.

### Phase D — civilian/planetary populations
- settlements/colonies;
- family/household structures where culturally valid;
- occupations/institutions/services;
- visitors/passengers/migration.

### Phase E — dynamic life
- agendas;
- routines;
- off-screen catch-up;
- relationship/memory evolution;
- environmental state.

### Phase F — validation and runtime integration
- deterministic replay tests;
- migration tests;
- population conservation tests;
- contradiction tests;
- CoreRPG integration.

## Final principle

> **The universe may simulate fewer people than exist, but once a person becomes somebody, they remain somebody.**

And:

> **Generate the reasons a person exists before generating the person.**
