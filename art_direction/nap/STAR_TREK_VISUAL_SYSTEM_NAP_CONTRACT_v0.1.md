# Star Trek Visual System + NAP Contract v0.1

Status: **FOUNDATION**

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
