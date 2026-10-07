# Persistent Personality System — Master Plan v0.1

**Status:** ACTIVE  
**Purpose:** give persistent NPCs distinct, stable, canon-informed personalities without cloning canonical characters or collapsing species/culture into personality.

## Core principle

Canonical Star Trek characters are used only as **research samples** from which observable behavioral traits are extracted.

The production library never contains procedural profiles named after Kirk, Picard, Janeway, Worf, Spock or any other canonical character.

## Work packages

| Package | Scope | Status |
|---|---|---|
| P001 | Canon personality research corpus | IN_PROGRESS |
| P002 | Abstract personality trait lexicon | IN_PROGRESS |
| P003 | Persistent personality profile contract | COMPLETE |
| P004 | NPC personality assignment/promotion contract | COMPLETE |
| P005 | Species/culture expression modifiers | TODO |
| P006 | Procedural personality recipe library | TODO |
| P007 | AI dialogue personality context contract | COMPLETE |
| P008 | Personality evolution / continuity rules | COMPLETE |
| P009 | Validation fixtures and anti-caricature tests | TODO |
| P010 | Authored personality mode for principal NPCs | COMPLETE |

## NPC depth tiers

This system uses **personality depth tiers**, distinct from any population/materialization tier used elsewhere.

- **A — principal/major NPC:** authored personality preferred. Procedural fallback allowed only when intentionally chosen.
- **B — interactive persistent NPC:** full procedural personality profile resolved once and then fixed.
- **C — background/light NPC:** no full personality package required. A persistent C entity may carry a latent deterministic personality seed so later promotion to B can remain consistent with prior observed behavior.

A C→B promotion is irreversible with respect to personality identity: once the full personality profile is resolved, it is never rerolled.

## Composition

Final dialogue behavior resolves from:

**persistent personality core**
+ **species/culture expression**
+ **career/institutional socialization**
+ **relationship toward interlocutor**
+ **current emotional/physical state**
+ **scene context**
= **current expression**

Current state can modulate expression; it does not replace core personality.

## Research rule

The canonical research corpus stores:
- observable traits;
- interaction style;
- humor style;
- authority/rule relationship;
- stress behavior;
- relationship tendencies;
- evolution where useful;
- source provenance.

The generator consumes only **abstracted traits and recipes**, never canonical names or likeness/personality clones.
