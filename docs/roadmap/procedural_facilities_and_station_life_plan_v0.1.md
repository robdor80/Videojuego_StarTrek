# Procedural Facilities & Station Life — Plan v0.1

**Status:** COMPLETE  
**Purpose:** define which stations can exist, which designs they use, how they are built, staffed, inhabited, operated, visited and persisted.

## Packages

| Package | Scope | Status |
|---|---|---|
| PF001 | Canon/source audit for station designs and functions | COMPLETE |
| PF002 | Facility type / design / instance taxonomy | COMPLETE |
| PF003 | Canonical reusable station-design catalogue | COMPLETE |
| PF004 | Canonical unique/seeded facility catalogue | COMPLETE |
| PF005 | Procedural station-design grammar | COMPLETE |
| PF006 | Facility staffing/population guidance | COMPLETE |
| PF007 | Station watches, work and life profiles | COMPLETE |
| PF008 | Residents, businesses, visitors and tenancy model | COMPLETE |
| PF009 | Docking, services, queues and traffic integration | COMPLETE |
| PF010 | Construction / expansion / mothball lifecycle integration | COMPLETE |
| PF011 | Facility visual/NAP design profiles | COMPLETE |
| PF012 | Deterministic reference generator | COMPLETE |
| PF013 | Locked procedural facility fixture | COMPLETE |
| PF014 | Cross-domain invariants | COMPLETE |
| PF015 | Project status / documentation integration | COMPLETE |

## Core doctrine

```text
NEED
→ alternatives
→ scale
→ site
→ design
→ construction
→ commissioning
→ staff/residents/services
→ traffic
→ persistent operation
```

A facility is not a service icon placed for the player.

### Hard rules

1. **Facility type != design != individual facility != owner != operator.**
2. **Need before station.**
3. **Temporary/mobile solution before permanent construction when sufficient.**
4. **Smallest sufficient scale.**
5. **Existing nearby capacity suppresses duplicates.**
6. **Construction takes time.**
7. **A station must be maintainable after it is built.**
8. **Services are finite and design-specific.**
9. **Traffic is a consequence of demand/services, never decorative.**
10. **Once committed, a facility has persistent identity and history.**
11. **Canonical unique facilities are never cloned.**
12. **Reusable canonical designs may be instantiated only under their reuse policy.**
13. **Procedural designs are reusable designs, not one-off random geometry per station.**
14. **Major complexes require exceptional polity-scale justification.**

## Playable-era scope

- Pike / SNW
- Kirk / TOS + films
- TNG / DS9 / Voyager

Later appearances may be used only as evidence that a design already existed earlier when the source explicitly establishes that fact. Later political/technology state is not backfilled.

## Completion target

The facility system must be able to answer:
- Why does this station exist?
- Why here?
- Why this size and not smaller?
- Why this design?
- Who paid/built it?
- Who owns and operates it now?
- How many permanent workers/residents/civilians/visitors are present?
- Which watches are active?
- Which services actually exist and what capacity is available?
- Which ships are approaching, holding, docked or leaving, and why?
- What is being built/repaired/moved through the facility?
- What happens if demand disappears?
- Does the same facility remain through capture, refit, expansion, abandonment or save/load?


## v0.1 closure

**PF001–PF015: 15/15 COMPLETE** for the current content/reference-implementation scope.

Delivered:
- source-backed canonical reusable station designs;
- reserved canonical individual facilities;
- strict anti-"space gas station" causality;
- smallest-sufficient-scale and site-selection rules;
- procedural reusable station-design grammar;
- construction/commissioning/expansion/mothball lifecycle;
- station staffing, residents, tenants, visitors and docked-crew separation;
- continuous watches + day/peak work + tiny-outpost on-call schedules;
- finite berths/services/queues and causal traffic;
- station-life profiles by canonical design;
- facility visual/NAP profiles;
- deterministic reference generator;
- positive relay-station fixture and negative player-convenience fixture;
- cross-domain validation invariants.

### Runtime boundary

The repository contains the content contracts and deterministic reference implementation. CoreRPG 4.5+ remains the future authoritative owner of live facility World State, construction catch-up, queue arbitration, traffic, population schedules and persistence.

Reference Python tests exist in `tools/generation/`. This closure does not claim they have run under repository CI because no CI runner is currently configured for this subsystem.
