# USS Reliant NCC-1864 — Miranda-class reference blueprints

This directory stores an 18-sheet blueprint set for **USS Reliant NCC-1864**, a Miranda-class Starfleet vessel.

## Project role

This material is used as a **technical/spatial reference** for the Miranda-class gameplay model and for USS Reliant-specific overrides.

It is not SCREEN_CANON and must not be treated as proof that every Miranda-class vessel shares the exact same:
- compartment layout;
- crew complement;
- passenger capacity;
- shuttle complement;
- weapon count;
- internal equipment placement;
- bridge or mission configuration.

## Gameplay extraction rule

Use the set only to support game-usable structures such as:
- deck indexing;
- compartment/location graphs;
- turbolift and corridor connectivity;
- engineering and tactical spaces;
- transporter, shuttle and escape-system placement;
- class-level interior baselines;
- Reliant-specific configuration overrides.

Any numeric or technical specification promoted into structured gameplay data must be cross-checked against higher-authority sources where available and retain provenance/confidence.

## Naming

The original uploaded filenames have been normalized to stable zero-padded ordering:

```text
sheets/01.jpg
...
sheets/18.jpg
```

The original source filenames are preserved in `blueprint_index.json`.

## Modeling rule

```text
Miranda class baseline
        +
era / mission configuration
        +
individual ship overrides
        =
actual playable vessel
```

USS Reliant is therefore a reference vessel, not a universal Miranda template.
