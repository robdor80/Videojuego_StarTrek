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
- Operational history is append-only: the event log records facts and later systems perform evaluation.
- Recording an event does not create universal NPC knowledge; visibility/knowledge requires a valid projection path.

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
| E. Operational event log | ✅ COMPLETE | Cross-console append-only event contract, fixed event vocabulary, visibility projection and Sensors worked example |
| F. Academy Sensors UX | ⬜ TODO | Training presentation over same operations |
| G. Galaxy-class Sensors UX | ⬜ TODO | Operational presentation over same operations |
| H. v0.0.1 duty scenario | ⬜ TODO | Order → scan → report → evaluation |

## Management rule

This file is the control sheet for the current vertical slice and must be updated whenever one of the phases changes state. `CONTENT_STATUS.md` mirrors the project-level status.

## Immediate next task

Begin **F. Academy Sensors UX**.

The Academy UX should reuse the same Sensors operations and event log, adding teaching context, supervised practice and later evaluation without creating a separate tutorial-only sensor system.

## Required post-D deliverable

Delivered for Sensors v0.1:
- ✅ in-game Starfleet/PADD study manual;
- ✅ visually polished external PDF operator manual.

Control document: `docs/roadmap/sensors_operator_manual_plan.md`.

## Phase E deliverable

Delivered under `gameplay/ship_operations/operational_event_log/`:

- ✅ operational event contract;
- ✅ event type catalogue for the current vertical slice;
- ✅ visibility/knowledge projection rules;
- ✅ worked Sensors order → scan → result → report → interconsole transfer example.

Evaluation remains a separate consumer: the log records evidence and does not itself judge performance.

## CoreRPG dependency

The playable implementation of **H. v0.0.1 duty scenario** depends on the separate `robdor80/CoreRPG` engine reaching the minimum runtime capabilities required by this vertical slice.

Current verified CoreRPG state: foundation through phase 4.4 is closed; `WorldState` is still the minimal identity/revision state and the repository is prepared to begin **4.5 — Generic World State**. General live records, DefinitionId→EntityId instantiation, functional rules, general actions/simulation and gameplay persistence are not yet available.

Rules for this project:

- **Do not implement a duplicate game engine inside Videojuego_StarTrek.**
- Star Trek defines content, gameplay contracts, console behavior and presentation requirements that CoreRPG must later host.
- E (Operational Event Log) is now specified as a reusable Star Trek-side contract; its authoritative runtime implementation belongs in CoreRPG.
- F/G may be designed and prototyped as UX, but final runtime integration waits for the necessary CoreRPG milestones.
- H is **runtime-blocked by CoreRPG**, not by missing Star Trek console design.


## Procedural acceptance fixture

The Star Trek-side end-to-end acceptance contract is now defined at:

`validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`

Fixture campaign context:
- era: `tng_ds9_voyager`;
- date: **2372-03-14**;
- deterministic campaign seed: `fixture_sensor_v0_0_1`.

The fixture validates:
- world materialization before observation;
- deterministic identities;
- sensor-state-dependent detection;
- hidden-information gating;
- observer-relative contacts;
- anti-leakage;
- append-only operational event chain;
- knowledge visibility;
- save/load identity continuity;
- AI/UI authority boundaries.

The worked operational-event example was aligned to 2372 because 2399 lies outside the project's currently approved playable-era scope.

### Runtime status

Star Trek-side contracts and acceptance expectations are defined.

Executable F/G/H completion remains dependent on presentation work and on CoreRPG capabilities beginning with **4.5 — Generic World State**. The verified CoreRPG `main` still reports 4.4 closed and a deliberately minimal `WorldState`.

This remains an architectural dependency, not permission to implement a duplicate engine in this repository.
