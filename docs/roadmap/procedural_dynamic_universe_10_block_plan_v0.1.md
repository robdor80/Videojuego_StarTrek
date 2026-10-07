# Procedural Dynamic Universe — 10-block plan v0.1

**Status:** ACTIVE  
**Execution rule:** blocks are implemented strictly in order. A later block may be documented as a dependency, but implementation does not start until the current block is COMPLETE, validated, cross-referenced and recorded in `CONTENT_STATUS.md`.

| Block | Scope | Status |
|---|---|---|
| 1 | Procedural Civilization Evolution & Galactic Interaction | COMPLETE |
| 2 | Colonization, Expansion & Borders | TODO |
| 3 | Procedural Conflict & War | TODO |
| 4 | Living Interplanetary / Interstellar Economy | TODO |
| 5 | Procedural History & Major Events | TODO |
| 6 | Science, Technology & Discovery | TODO |
| 7 | Phenomena, Anomalies & Procedural Archaeology | TODO |
| 8 | Systemic Crises | TODO |
| 9 | Emergent Missions from World State | TODO |
| 10 | Background Galactic Evolution | TODO |

## Block separation

Block 1 owns long-horizon evolution of an already-existing civilization: demographic trend, institutional continuity/change, political cohesion, internal resilience, capability maturation, relationship evolution, extinction/continuity semantics and LOD/off-screen catch-up contracts.

It intentionally does **not** implement:
- colony founding, borders or territorial expansion — Block 2;
- battle/front/war simulation — Block 3;
- detailed interstellar production/markets/routes — Block 4;
- retroactive historical-world generation — Block 5;
- research projects/breakthrough generation — Block 6;
- anomaly/archaeology generation — Block 7;
- crisis generators — Block 8;
- mission generation — Block 9;
- whole-galaxy scheduling/priority simulation — Block 10.

Cross-block hooks may be emitted as candidates/refs, never silently resolved by the wrong block.
