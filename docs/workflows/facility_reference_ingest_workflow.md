# Workflow — ingest facility blueprints/reference sheets

This workflow bridges external/local reference gathering (including BlueprintGrabber output) into the Star Trek gameplay repository.

## 1. Download outside the game repository

Use the external downloader/tooling to obtain the original full-size sheets and its provenance metadata.

Do not point automated bulk downloads directly at this repository.

## 2. Review the set

Before importing:
- confirm the sheets belong to the intended subject;
- confirm numbering/order;
- remove exact duplicates;
- preserve source URL and visible credits;
- note whether the set is official/licensed/fan/secondary/unknown;
- do not decide authority from visual polish.

## 3. Register provenance

Add a source entry to:

`sources/source_registry/source_registry.json`

using the normal project authority taxonomy:
- SCREEN_CANON
- OFFICIAL_REFERENCE
- LICENSED_NOVEL
- LICENSED_COMIC
- RELIABLE_SECONDARY
- GENERAL_WEB
- INFERRED
- GAME_ADDITION

For most Cygnus-X1-hosted fan plan sets, default expectation is **GENERAL_WEB** unless the underlying work is independently shown to be an official/licensed reference.

## 4. Import selected assets

Place the reviewed set under:

`assets/facilities/reference/<faction>/<facility_or_design>/<reference_set_id>/`

Normalize sheet filenames to zero-padded ordering:

`01.jpg`, `02.jpg`, ...

Preserve original filenames/URLs/checksums in `reference_index.json`.

## 5. Extract gameplay evidence

Extract only what the images actually support.

Useful targets:
- decks/levels;
- rooms/sections;
- corridors/lifts;
- docking ports;
- command/medical/security/cargo/repair spaces;
- service nodes;
- critical-system spaces;
- restricted areas;
- evacuation/boarding chokepoints.

Do **not** promote printed specs to canon automatically.

## 6. Build topology

When enough geometry exists, update/create:
- `facility_topology_model` instances;
- service-node data;
- location graph;
- access zones;
- live-state bindings.

Keep baseline topology separate from damage/security/pressure state.

## 7. Validate

Required checks:
- no invented missing rooms;
- no accidental individual→class generalization;
- provenance on nontrivial claims;
- no fake exact capacity;
- no silent conflict resolution between sheets;
- player-facing names in Spanish when shown in game.

## 8. Commit boundaries

Prefer two commits:
1. asset/reference ingest;
2. gameplay extraction.

That keeps evidence separate from interpretation.
