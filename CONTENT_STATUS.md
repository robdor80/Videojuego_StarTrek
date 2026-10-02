# Star Trek Content Status

Master progress index for the Star Trek universe repository.

## Status legend

- ⬜ `TODO` — not started.
- 🟨 `IN_PROGRESS` — active research or structuring.
- 🟧 `NEEDS_REVIEW` — substantially researched, pending consistency/provenance review.
- 🟦 `NEEDS_ROBERTO` — requires a creative/game-design decision that cannot be resolved from sources alone.
- ✅ `COMPLETE` — researched to the current defined scope, structured, provenance recorded, validated, with no known blocking gaps.

A folder not explicitly listed here inherits `TODO`. `COMPLETE` is not permanent: new evidence or a detected contradiction can reopen a block.

## Current command priority

1. ✅ Documentary foundation
2. ✅ Chronology and era model
3. 🟨 Federation and Starfleet institutional baseline
4. ⬜ Starfleet Academy
5. ⬜ Career bridge: Academy → first assignment → service record
6. ⬜ Starfleet technology and starships
7. ⬜ Species, factions, astrography and wider universe
8. ⬜ Narrative, AI, presentation and runtime content derived from validated lore

## Documentary foundation

| Area | Status | Notes |
|---|---|---|
| `sources/canon_policy.md` | ✅ COMPLETE | Source authority and conflict rules fixed. |
| `sources/provenance_policy.md` | ✅ COMPLETE | Provenance and confidence model fixed. |
| `sources/source_registry/` | ✅ COMPLETE | Living registry established. |
| `docs/workflows/content_research_workflow.md` | ✅ COMPLETE | Standard research-to-commit workflow fixed. |
| `docs/decisions/playable_eras.md` | ✅ COMPLETE | Three playable eras fixed by Roberto. |
| `docs/decisions/campaign_continuity.md` | ✅ COMPLETE | Canon sets the starting state; campaign future is emergent. |

## Playable era scope

| Era | Status | Anchor |
|---|---|---|
| Pike / Strange New Worlds | ✅ SCOPE FIXED | Christopher Pike / NCC-1701 |
| Kirk / TOS + films | ✅ SCOPE FIXED | James T. Kirk / NCC-1701 and NCC-1701-A as date allows |
| TNG + DS9 + Voyager | ✅ SCOPE FIXED | Picard / Sisko / Janeway |

Excluded from playable scope: `Picard` (series), `Discovery`, `Enterprise`.

## Universe / chronology

| Area | Status | Notes |
|---|---|---|
| `universe/chronology/master_timeline/` | ✅ COMPLETE | Minimal backbone for current scope. |
| `universe/chronology/temporal_anchors/` | ✅ COMPLETE | Initial era/branch anchors fixed. |
| `universe/chronology/era_profiles/pike/` | ✅ COMPLETE | Reference profile established. |
| `universe/chronology/era_profiles/kirk/` | ✅ COMPLETE | TOS + Kirk-film reference profile established. |
| `universe/chronology/era_profiles/tng_ds9_voyager/` | ✅ COMPLETE | Shared late-24th-century profile established. |
| `universe/chronology/historical_events/` | ⬜ TODO | Filled progressively as later domains require events. |

**Critical rule:** reference chronology never forces the player to replay series or films.

## Federation / Starfleet

| Area | Status |
|---|---|
| Federation government, law, diplomacy, economy and member worlds | ⬜ TODO |
| Starfleet organization and command structure | 🟨 IN_PROGRESS |
| Ranks, departments, positions and duty stations | ⬜ TODO |
| Qualifications, regulations, protocols and Prime Directive | ⬜ TODO |
| Assignments, promotions, commendations and discipline | ⬜ TODO |
| Uniforms and era-specific institutional presentation | ⬜ TODO |

## Starfleet Academy

| Area | Status |
|---|---|
| History and campus | ⬜ TODO |
| Admissions and cadet life | ⬜ TODO |
| Departments and specializations | ⬜ TODO |
| Curriculum and courses | ⬜ TODO |
| Instructors | ⬜ TODO |
| Evaluations and examinations | ⬜ TODO |
| Simulations and field training | ⬜ TODO |
| Training ships | ⬜ TODO |
| Graduation and first assignments | ⬜ TODO |
| Academy era profiles | ⬜ TODO |

## Major remaining domains

| Domain | Status |
|---|---|
| Characters | ⬜ TODO |
| Species / cultures / languages | ⬜ TODO |
| Factions and organizations | ⬜ TODO |
| Astrography | ⬜ TODO |
| Starships and ship systems | ⬜ TODO |
| Stations and facilities | ⬜ TODO |
| Technology and equipment | ⬜ TODO |
| Medicine and science | ⬜ TODO |
| Conflicts and historical events | ⬜ TODO |
| Gameplay | ⬜ TODO |
| Narrative | ⬜ TODO |
| AI | ⬜ TODO |
| Presentation and UI | ⬜ TODO |
| Assets / audio / NAP mappings | ⬜ TODO |
| Runtime content / schemas / manifests | ⬜ TODO |
| Validation suites | ⬜ TODO |

## Active block

**Federation / Starfleet institutional baseline.**

The next pass establishes how Starfleet is organised before researching Academy gameplay in depth.
