# STAR TREK — SHIP EXTERIOR VISUAL BIBLE v0.1

**Status:** FOUNDATION APPROVED FOR PROCEDURAL TESTING
**Inherits:** STAR_TREK_GLOBAL_VISUAL_BIBLE_v0.1

## Principle

A ship image represents a **specific design or vessel in a specific state**.

Resolve in this order:

`era → operator → class/design → dated configuration/refit → individual vessel identity → current state → environment/camera`

## Class vs vessel

Class defines:
- hull language;
- proportions;
- baseline systems and visible structures;
- normal configuration families.

Individual vessel defines:
- ship_id;
- registry/name;
- dated refits/modifications;
- persistent damage/repairs;
- campaign history.

Never use damage, name or registry to redefine the class.

## Canon geometry

Where reliable blueprint/reference material exists:
- preserve major silhouette;
- preserve primary hull relationships;
- preserve nacelle count/placement and major structures;
- do not “improve” proportions for generic sci-fi aesthetics.

Unknown detail must not become pseudo-canon merely because an image generator filled it.

## Materials

Use physically coherent hull materials, glazing, illumination and emissive systems appropriate to the profile.

Avoid:
- excessive panel noise;
- generic battleship plating;
- random blue neon;
- atmospheric weathering in vacuum without a cause;
- unexplained weapon ports or engines.

## Registry and markings

Registry/name are data overlays tied to the individual vessel.
Malformed text or wrong registry is a rejection reason.

## Operational state

Visual overlays may include:
- normal cruise;
- docked;
- warp/impulse context;
- shields/weapon activity when visually represented by approved profile;
- battle damage;
- repair/refit;
- emergency power;
- contamination/debris.

Every overlay requires World State cause.

## Camera

Choose camera to communicate:
- identity/silhouette;
- scale;
- operational context.

Avoid poster drama that hides hull recognition.

## Persistence

Refit and repair evolve the same ship identity.
A later image must remain traceable to the same ship_id and its configuration/history.
