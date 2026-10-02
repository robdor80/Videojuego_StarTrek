# Canon Policy

## Purpose

This document defines how information is admitted into the Star Trek knowledge base used by the project.

The project models one historically continuous Star Trek universe while preserving separate continuities/timelines where the screen material itself requires them. Era profiles are temporal filters, not duplicate universes.

## Research order

The default research order is:

1. **Released television series and films**
2. **Licensed novels and comics**
3. **Internet research**, prioritising official sources, then reliable specialist secondary sources, then general sources

This is a research order, not an instruction to make all three levels equally authoritative.

## Authority levels

### A — SCREEN_CANON

Released Star Trek television episodes, streaming episodes, animated episodes and films.

This is the primary authority for factual universe state. When a fact is visible, spoken or otherwise established on screen, it outranks contradictory tie-in material.

The official Star Trek site describes the franchise through its Series & Movies catalogue. An official StarTrek.com interview with novelist Michael A. Martin also explicitly describes canon as official on-screen continuity and the official history shown in movies or television.

### B — OFFICIAL_REFERENCE

Official Star Trek / Paramount material that describes screen works: official series pages, episode pages, film pages, recaps, production notes, official interviews and comparable reference material.

Useful for metadata, terminology, production context and locating primary evidence. It must not silently override what is actually shown on screen.

### C — LICENSED_NOVEL / LICENSED_COMIC

Officially licensed Star Trek prose fiction and comics.

These are valuable for:
- filling gaps left open by screen canon,
- generating research leads,
- enriching culture, routine, characterisation and institutional detail,
- identifying plausible interpretations.

They do **not** override conflicting screen canon. If a detail first appears in licensed print and is later established on screen, the project records the screen source as the canonical basis.

### D — RELIABLE_SECONDARY

Specialist reference works and well-maintained databases such as Memory Alpha, plus reputable interviews or reference publications.

These are excellent discovery and cross-checking tools, but claims should be traced back to stronger evidence whenever practical.

### E — GENERAL_WEB

General websites, articles, forums, videos and unspecialised sources.

Use for discovery only unless independently corroborated. A gameplay-critical or chronology-critical fact must not rely solely on this level.

### F — INFERRED

A conclusion logically inferred from stronger evidence when no source states it directly.

Inference must:
- be explicitly labelled,
- name the evidence it depends on,
- state uncertainty,
- never be presented as screen canon.

### G — GAME_ADDITION

A project-created fact required to make the RPG coherent or playable where source material is silent.

Game additions must be explicit and must not contradict higher-authority material.

## Conflict resolution

1. Screen canon beats contradictory licensed print.
2. Official reference material helps interpret screen canon but does not rewrite it.
3. A contradiction between two screen sources is **not** resolved by blindly choosing the newer one.
4. First check whether the conflict is explained by:
   - different timelines/continuities,
   - different dates or eras,
   - unreliable in-universe testimony,
   - retcon,
   - incomplete information.
5. If unresolved, preserve both claims and create an entry under `sources/unresolved_conflicts/`.
6. Licensed novels/comics that disagree with one another are retained as alternatives; no artificial synthesis is required.
7. General-web claims without traceable evidence remain research leads, not lore facts.

## Timeline rule

Every chronology-sensitive fact should eventually carry enough temporal context to determine whether it is valid for a campaign date.

Examples:
- character alive/active status,
- rank and assignment,
- ship commissioned/decommissioned status,
- technology availability,
- political borders and alliances,
- institutional doctrine,
- uniform generation.

## Project rule

**Never hide the boundary between canon, licensed expansion, inference and game invention.**

The game may use all four, but the repository must always know which is which.
