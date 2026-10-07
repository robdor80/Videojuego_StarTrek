# Star Trek Visual System + NAP Contract v0.1

Status: **FOUNDATION + WAVE E CONTENT DEPTH COMPLETE**

## Purpose

Define how authoritative Star Trek world data becomes a visual production request without allowing image generation to invent world truth.

## Fundamental rule

> **World data decides what exists. Visual rules decide how that truth is represented.**

A generated image, prompt or asset may never silently decide species, culture, affiliation, era, rank, division, ship class, location identity or persistent damage/state.

## Compositional visual context

Star Trek requires composition of independent authorities:

- global art direction;
- era;
- species biology;
- culture;
- polity/affiliation;
- organization;
- asset category;
- role/function;
- uniform/equipment family;
- division;
- rank;
- local environment;
- persistent instance identity;
- current temporary state.

Example:

```text
species=vulcan
culture=earth-raised
affiliation=federation
organization=starfleet
era=tng
division=sciences
rank=lieutenant
```

No profile may infer personality from species.

## Permanent identity vs current visual state

Keep separate:

### Identity
- stable morphology/appearance anchors;
- species traits;
- individual facial/body traits;
- organization/class design;
- uniform/equipment model;
- persistent modifications.

### Current state
- duty/off-duty clothing;
- dirt/contamination;
- wetness;
- injury;
- fatigue presentation;
- equipment carried now;
- ship/facility damage;
- emergency lighting;
- smoke/fire;
- weather;
- time-of-day lighting.

Current state changes through World State/events. It must not mutate the stable visual identity.

## Bible families

- Global;
- Era;
- Species;
- Culture;
- Affiliation;
- Organization;
- Uniform;
- Character/Portrait;
- Ship Exterior;
- Ship Interior;
- Facility/Settlement;
- Planet/Environment;
- Equipment/Prop.

Lower profiles specialize the resolved context but cannot contradict higher authoritative facts.

## Required resolved visual specification

Before NAP generation, a request should be able to resolve:

- `entity_id`;
- `asset_id`;
- `asset_category`;
- `campaign_era`;
- applicable bible/profile IDs + versions;
- canonical/procedural provenance;
- identity anchors;
- allowed variation;
- forbidden variation;
- current visual state;
- environment/location;
- composition/camera requirements when relevant;
- output profile;
- prompt provenance;
- source/reference provenance.

## NAP lifecycle

```text
authoritative entity/world state
→ resolve visual context
→ validate profile stack
→ generate candidate
→ human/AI review
→ NAP ingest
→ AI PASS
→ archive master via ArchiveRoot
→ derive production format/profile
→ write production asset + legitimate documentation to ProductionRoot
→ physical verification
→ COMPLETED
```

### Repository policy

- Visual Bibles and schemas belong in `Videojuego_StarTrek`.
- Master archival images do not belong in the visual-bible tree.
- NAP controls archive/production lifecycle.
- Production assets must retain traceability to entity ID, bible versions and prompt/identity metadata.
- Git automation for a production repository is not assumed by this contract.
- Do not create unauthorized ProductionRoot folders ad hoc; NAP is authoritative for production-path creation.

## Naming and identity

Visible names are not technical identity.

Asset paths/names may be human-readable, but manifests must retain stable `asset_id` and, when entity-backed, stable `entity_id`.

Changing a visible ship/person/place name must not create a new identity.

## Validation

Reject or quarantine a candidate when it:
- violates era;
- violates species morphology;
- confuses species with culture;
- applies the wrong organization/uniform;
- uses an invalid rank/division combination;
- contradicts persistent identity;
- invents unsupported technology;
- contradicts current World State;
- introduces generic sci-fi elements unsupported by the applicable Trek profile;
- loses provenance;
- cannot be traced to the bible/profile versions used.

## Migration from the Nimroel pattern

Reuse:
- global → category → culture/profile → variation → final prompt → asset;
- explicit visual identity metadata;
- exact prompt preservation;
- approved production derivative plus documentation;
- contextual state rather than arbitrary visual dirt/damage.

Extend for Star Trek:
- compositional multi-authority resolution;
- era as first-class context;
- species separate from culture;
- organization/affiliation separate from species;
- uniform division/rank resolution;
- ship/facility class + individual-instance separation;
- live World State overlays;
- NAP as lifecycle authority.

## Next contracts

This foundation must be followed by:
1. resolved visual context schema;
2. bible/profile manifest schema;
3. NAP handoff manifest schema;
4. global Star Trek visual bible;
5. category bibles;
6. era/species/culture/organization profiles.


## Implemented foundation references

Schemas:
- `art_direction/schemas/persistent_visual_identity.schema.json`
- `art_direction/schemas/resolved_visual_context.schema.json`
- `art_direction/schemas/visual_profile_manifest.schema.json`
- `art_direction/schemas/nap_asset_handoff.schema.json`

Visual Bibles / profile families:
- `art_direction/visual_bibles/global/STAR_TREK_GLOBAL_VISUAL_BIBLE_v0.1.md`
- `art_direction/visual_bibles/characters/STAR_TREK_CHARACTER_PORTRAIT_VISUAL_BIBLE_v0.1.md`
- `art_direction/visual_bibles/eras/STAR_TREK_ERA_VISUAL_PROFILES_v0.1.json`
- `art_direction/visual_bibles/species/STAR_TREK_SPECIES_VISUAL_PROFILE_FRAMEWORK_v0.1.json`
- `art_direction/visual_bibles/cultures_affiliations/CULTURE_AFFILIATION_VISUAL_PROFILE_FRAMEWORK_v0.1.json`
- `art_direction/visual_bibles/organizations/STARFLEET_VISUAL_PROFILE_v0.1.json`
- `art_direction/visual_bibles/uniforms/STARFLEET_UNIFORM_VISUAL_PROFILES_v0.1.json`
- `art_direction/visual_bibles/ships/STAR_TREK_SHIP_EXTERIOR_VISUAL_BIBLE_v0.1.md`
- `art_direction/visual_bibles/interiors/STAR_TREK_INTERIOR_CONSOLE_FACILITY_VISUAL_BIBLE_v0.1.md`
- `art_direction/visual_bibles/planets/STAR_TREK_PLANET_ENVIRONMENT_VISUAL_BIBLE_v0.1.md`
- `art_direction/visual_bibles/equipment/STAR_TREK_EQUIPMENT_PROP_VISUAL_BIBLE_v0.1.md`

### Identity-lineage rule

For entity-backed assets, NAP must preserve both:
- `entity_id`;
- `visual_identity_id` lineage.

A new render, age progression, new uniform, injury state, ship refit or repaired environment is a new asset/state representation of the same persistent entity when World State says identity is continuous. It is not permission to generate an unrelated replacement identity.


## Wave E depth implementation

The content-depth pass now resolves through:

- `art_direction/STAR_TREK_VISUAL_DEPTH_INDEX_v0.1.json`
- `art_direction/visual_bibles/species/STAR_TREK_SPECIES_VISUAL_PROFILE_CATALOG_v0.1.json`
- `art_direction/visual_bibles/organizations/STAR_TREK_ORGANIZATION_VISUAL_PROFILE_CATALOG_v0.1.json`
- `art_direction/visual_bibles/ships/STAR_TREK_SHIP_CLASS_VISUAL_PROFILES_v0.1.json`
- `art_direction/visual_bibles/interiors/STAR_TREK_INTERIOR_ERA_OPERATOR_VISUAL_PROFILES_v0.1.json`
- `art_direction/visual_bibles/planets/STAR_TREK_HOMEWORLD_ENVIRONMENT_VISUAL_PROFILES_v0.1.json`
- `art_direction/visual_bibles/facilities/STAR_TREK_STATION_DESIGN_VISUAL_PROFILES_v0.1.json`

Representative NAP fixture:

- `validation/fixtures/nap/sensors_console_tng_v0.1/`

The fixture contains a physical PNG master, a physical WebP derivative, persistent visual identity, resolved visual context, lifecycle handoff, deterministic renderer specification and verification manifest.

The fixture is explicitly **not production art**. Its purpose is contract/regression validation.

### Completion meaning

Wave E completion means the current defined species/organization/ship/interior/homeworld scope has a coherent visual-resolution and NAP baseline. It does **not** mean every future species, ship class, facility, planet, uniform, prop or production asset has already been authored.


## Facility visual resolution

Facility generation resolves visual context only after:
`need → scale → site → design → individual facility identity → configuration/current state`.

Station visuals therefore cannot decide:
- that a station exists;
- which services it provides;
- how many berths/drydocks it has;
- who owns or operates it;
- which ships are docked;
- whether it is damaged, under construction or abandoned.

Reusable station designs may have multiple facility instances, but each instance retains its own `facility_id` and visual-state history.
