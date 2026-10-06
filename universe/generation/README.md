# Procedural universe generation

This directory contains the authoritative procedural-world contracts used by gameplay systems.

## Purpose

Procedural generation creates persistent world entities that can later be observed and affected by gameplay systems. It does not create ad-hoc answers for UI prompts.

## Core rule

**Generate reality first. Observe it second.**

Sensor consoles, tricorders, science analysis, the Starship Computer and NPC reports consume generated/persistent world state. They never become the source of truth themselves.

## Two scopes

### Vertical-slice scope

Already established:

1. observable entity model;
2. detectable-signature model;
3. deterministic generation rules;
4. minimal v0.0.1 generation profile;
5. deterministic generator implementation;
6. sensor-resolution model.

### Full-universe expansion

Foundation now established in:

- `PROCEDURAL_UNIVERSE_BIBLE_v0.1.md`;
- `generator_domain_catalog.json`;
- `procedural_starship_rules.json`;
- `procedural_population_rules.json`;
- `traffic_activity_model.json`;
- `procedural_context_resolution_hierarchy.json`;
- `persistent_population_materialization_rules.json`;
- `docs/roadmap/procedural_living_universe_depth_plan.md`.

The long-term generator covers coherent:

- cosmic structures and phenomena;
- worlds/civilizations;
- starships of civilian, scientific, industrial, passenger, government and military roles;
- facilities/infrastructure;
- traffic/logistics;
- crews and populations;
- current activity;
- campaign-conditioned persistence.

## Persistence

Once a procedural entity is materialized, it is loaded and evolved through simulation/events rather than rerolled whenever the player returns.

## LOD

Simulation fidelity may vary with relevance.

LOD changes computational detail, not whether an entity exists.


## Living-population depth

The procedural universe now uses an explicit layered-context and population-materialization architecture inspired by reusable simulation lessons from Nimroel:

- resolve structure before individuals;
- preserve authored/canonical characters;
- keep background population latent until needed;
- promote latent population deterministically into persistent individuals;
- never reroll a materialized person;
- isolate deterministic subsystem seeds;
- validate population conservation, staffing, knowledge, relationships and schedules.

Generic runtime semantics remain CoreRPG responsibilities; Star Trek owns era, canon, species/culture, Starfleet, technology and setting-specific generation rules.
