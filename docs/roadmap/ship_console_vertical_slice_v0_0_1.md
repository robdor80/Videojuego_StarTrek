# Ship-console vertical slice — v0.0.1

Owner: project design/runtime architecture
Status: **IN PROGRESS**

## Goal

Prove the core gameplay loop:

**authoritative procedural world → player receives an order → player operates a console → engine resolves the action → console presents the result → event is logged → superior can evaluate performance**

## Locked design decisions

- Sixteen functional console families are fixed under `gameplay/ship_operations/consoles/`.
- Functional console and physical station are separate concepts.
- Academy and operational ships use the same underlying operations with different UX.
- World truth exists before observation.
- AI may communicate structured results but does not own or invent world truth.
- No visible XP bar is required for professional progression; operational events can feed service evaluations.

## Implementation sequence

| Phase | Status | Deliverable |
|---|---|---|
| A. Console family catalogue | ✅ COMPLETE | 16 functional families fixed |
| B1. Authoritative observable-world rule | ✅ COMPLETE | Decision document |
| B2. Observable entity contract | ✅ COMPLETE | Entity model |
| B3. Detectable signature contract | ✅ COMPLETE | Signature model |
| B4. Procedural generation baseline | ✅ COMPLETE | Deterministic generation rules |
| B5. v0.0.1 generation profile | ✅ COMPLETE | Minimal test-world scope |
| B6. Generator implementation | ✅ COMPLETE | Seeded persistent system materialization + regression tests |
| C. Sensor detection resolution | ✅ COMPLETE | Deterministic scan request → observable result engine + contracts/tests |
| D. Sensors console functional tree | ✅ COMPLETE | All ten Sensors branches approved and fixed for v0.1; inter-console handoffs and persistence contracts defined |
| E. Operational event log | ⬜ TODO | Structured record of player console actions |
| F. Academy Sensors UX | ⬜ TODO | Training presentation over same operations |
| G. Galaxy-class Sensors UX | ⬜ TODO | Operational presentation over same operations |
| H. v0.0.1 duty scenario | ⬜ TODO | Order → scan → report → evaluation |

## Management rule

This file is the control sheet for the current vertical slice and must be updated whenever one of the phases changes state. `CONTENT_STATUS.md` mirrors the project-level status.

## Immediate next task

Begin **E. Operational event log**.


## Required post-D deliverable

Delivered for Sensors v0.1:
- ✅ in-game Starfleet/PADD study manual;
- ✅ visually polished external PDF operator manual.

Control document: `docs/roadmap/sensors_operator_manual_plan.md`.


## CoreRPG dependency

The playable implementation of **H. v0.0.1 duty scenario** depends on the separate `robdor80/CoreRPG` engine reaching the minimum runtime capabilities required by this vertical slice.

Current verified CoreRPG state: foundation through phase 4.4 is closed; `WorldState` is still the minimal identity/revision state and the repository is prepared to begin **4.5 — Generic World State**. General live records, DefinitionId→EntityId instantiation, functional rules, general actions/simulation and gameplay persistence are not yet available.

Rules for this project:

- **Do not implement a duplicate game engine inside Videojuego_StarTrek.**
- Star Trek defines content, gameplay contracts, console behavior and presentation requirements that CoreRPG must later host.
- E (Operational Event Log) can be specified now as a reusable contract.
- F/G may be designed and prototyped as UX, but final runtime integration waits for the necessary CoreRPG milestones.
- H is **runtime-blocked by CoreRPG**, not by missing Star Trek console design.
