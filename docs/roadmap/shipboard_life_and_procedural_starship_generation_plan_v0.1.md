# Shipboard Life & Procedural Starship Generation — Plan v0.1

**Status:** ACTIVE  
**Purpose:** complete the operational life of generated starships: why the ship exists, which design it uses, who serves aboard, how watches are staffed, what people do off watch, what the ship offers as a living environment, and how all of it persists.

## Packages

| Package | Scope | Status |
|---|---|---|
| SB001 | Canon/source audit for watches, quarters and recreation | COMPLETE |
| SB002 | Shipboard watch-generation contract | COMPLETE |
| SB003 | Off-watch obligations and on-call model | COMPLETE |
| SB004 | Off-duty activity and social-life catalogue | COMPLETE |
| SB005 | Habitability/life profile contract | COMPLETE |
| SB006 | Starfleet class/configuration life profiles | COMPLETE |
| SB007 | Klingon/Romulan/Cardassian class life profiles | COMPLETE |
| SB008 | Procedural ship-design generation contract | COMPLETE |
| SB009 | Procedural ship-instance generation pipeline | COMPLETE |
| SB010 | Crew + watch + schedule generation pipeline | COMPLETE |
| SB011 | Operator naming/registry collision contract | COMPLETE |
| SB012 | Runtime integration, fixtures and invariants | COMPLETE |

## Core principles

1. **A reference complement is not a live manifest.**
2. **A watch pattern is operational policy, not immutable class data.**
3. **Three-shift and four-shift schedules have exact hours only at the individual-ship level.**
4. **Duty, off-watch obligations, rest and leisure all consume real time.**
5. **Off duty does not mean unavailable or nonexistent.**
6. **Small ships create higher social density, lower privacy and stronger consequences from vacancies.**
7. **Large ships may support families, education and substantial recreation only when the actual class/configuration/mission permits it.**
8. **Alien operators do not inherit Starfleet Alpha/Beta/Gamma terminology unless explicitly authored.**
9. **A procedurally generated ship must exist for a causal reason and persists once materialized.**
10. **Generated design != generated individual ship. One procedural design may produce multiple persistent vessels.**
11. **Canonical ships, registries and unique identities are reserved and never duplicated.**
12. **AI can describe resolved schedules and life aboard but cannot invent personnel, facilities, free time, cargo, shifts or authority.**

## Watch model

Starfleet supports:
- three-watch rotation;
- four-watch rotation;
- custom rotation.

For a 24-hour shipboard cycle, the simulation may use:
- three watches × 8 hours;
- four watches × 6 hours;

as a **GAME_ADDITION_CANON_COMPATIBLE** scheduling default. Canon supports Enterprise-D normally operating three shifts and a commanded move to four shifts; the exact start hour remains individual-ship policy.

Non-Starfleet operators use operator-specific watch doctrine profiles. When canon does not define a schedule, the project models a plausible continuous-coverage system without claiming it as canon.

## Life aboard

Life resolution includes:
- assigned duty watch;
- station/department work;
- handoff;
- maintenance and technical call-outs;
- briefings/reports;
- training and recertification;
- medical obligations;
- fitness/readiness;
- sleep/rest;
- meals;
- hygiene;
- social activity;
- recreation;
- holodeck only if available;
- family/private time;
- personal projects/study;
- cultural/religious practice when individually applicable;
- shore leave;
- emergency recall.

## Completion target

A generated ship must be able to answer, from authoritative state:

- Why is this ship here?
- What class/design/configuration is it?
- How many duty crew, civilians and passengers are actually aboard?
- Which watch pattern is active?
- How many people are assigned to each watch?
- Who is working right now?
- Who is asleep, eating, training, socializing or on call?
- What facilities are actually available to them?
- How does the answer change during yellow/red alert, casualties or shortages?
- Does all of this remain the same ship and the same people after save/load/off-screen simulation?


## v0.1 closure

**SB001–SB012: 12/12 COMPLETE** for the current content/reference-implementation scope.

Delivered:
- class/configuration-specific shipboard life for Starfleet, Klingon, Romulan and Cardassian vessels;
- procedural civilian design/life profiles;
- generated three/four/custom watches;
- off-watch obligations and leisure;
- staffing guidance with provenance/confidence separation;
- persistent ship/design identity rules;
- deterministic reference generators for catalogued and civilian procedural vessels;
- locked Oberth fixture and cross-domain invariants.

Runtime note: CoreRPG 4.5+ remains responsible for future authoritative live World State, schedule arbitration and off-screen catch-up. Reference generator tests are present in the repository; this closure does not claim they have been executed by CI because no CI runner is configured in this repository.
