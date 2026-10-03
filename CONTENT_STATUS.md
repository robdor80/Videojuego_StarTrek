# Star Trek Content Status

Master progress index for the Star Trek universe repository.

## Status legend

- ⬜ `TODO` — not started.
- 🟨 `IN_PROGRESS` — active research or structuring.
- 🟧 `NEEDS_REVIEW` — substantially researched, pending consistency/provenance review.
- 🟦 `NEEDS_ROBERTO` — requires a creative/game-design decision that cannot be resolved from sources alone.
- ✅ `COMPLETE` — researched to the current defined scope, structured, provenance recorded, validated, translated into game-usable design/data where applicable, with no known blocking gaps.

A folder not explicitly listed here inherits `TODO`. `COMPLETE` is not permanent: new evidence or a detected contradiction can reopen a block.

## Current command priority

1. ✅ Documentary foundation
2. ✅ Chronology and era model
3. ✅ Starfleet institutional baseline
4. ✅ Starfleet Academy
5. ✅ Career bridge: Academy → first assignment → service record
6. ✅ Starfleet technology and starships
7. 🟨 Species, factions, astrography and wider universe
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
| `docs/decisions/universal_rank_insignia.md` | ✅ COMPLETE | TNG-style pips standardised across all playable eras by design. |
| `docs/decisions/player_facing_language.md` | ✅ COMPLETE | Internal IDs may be English; all normal player-facing text is es-ES. |
| `docs/decisions/lore_to_game_rule.md` | ✅ COMPLETE | Lore is input; gameplay/data/runtime usability is the required output. |

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

## Federation / Starfleet

| Area | Status | Notes |
|---|---|---|
| Federation government, law, diplomacy, economy and member worlds | 🟨 IN_PROGRESS | Founding, civil-government and founding-member baseline established; law, economy, wider membership and era-specific diplomacy remain progressive work. |
| Starfleet organization and command structure | ✅ COMPLETE | Upper command model, unit succession, acting command and operational chain established without speculative over-detail. |
| Commissioned and flag officer ranks | ✅ COMPLETE | Base ladder fixed. |
| Universal pip insignia | ✅ COMPLETE | TNG-style project standard across all eras. |
| Uniform division colors | ✅ COMPLETE | Era-aware baseline fixed. |
| Departments, positions and duty stations | ✅ COMPLETE | Core model and era-aware baseline established. |
| Duty shifts / watches | ✅ COMPLETE | Flexible 3/4/custom shift model; duty-officer command separated from permanent rank. |
| Command succession / acting command | ✅ COMPLETE | CO → XO → second officer → qualified designated successor. |
| Qualifications, regulations, protocols and Prime Directive | ✅ COMPLETE | Command qualification, Prime Directive, medical authority and classified-directive model established for baseline scope. |
| Assignments, promotions, commendations and discipline | ✅ COMPLETE | Career-event baseline, service record and disciplinary consequences established. |

## Starfleet Academy

| Area | Status |
|---|---|
| History and campus | ✅ COMPLETE | Playable hub, location graph and gameplay-relevant era differences established. |
| Admissions and cadet life | ✅ COMPLETE | Playable admission flow, soft-failure/retake model, four-year cadet progression and conduct consequences established. |
| Departments and specializations | ✅ COMPLETE | Playable divisions, specializations, medical route and change/cross-training rules established. |
| Curriculum and courses | ✅ COMPLETE | Four-year modular curriculum, playable course catalogue and character-vs-player resolution model established. |
| Instructors | ✅ COMPLETE | Persistent canonical/generated instructor model, temporal validity and AI authority limits established. |
| Evaluations and examinations | ✅ COMPLETE | Multi-axis evaluation, exam formats, recovery and persistent record model established. |
| Simulations and field training | ✅ COMPLETE | Simulation, active-unit field study, training cruise and live-world interruption models established. |
| Training ships | ✅ COMPLETE | Era/date-aware training-asset selection; famous ships are possible but never guaranteed. |
| Graduation and first assignments | ✅ COMPLETE | Graduation eligibility, ceremony, commission and live-world first-assignment generation established. |
| Academy era profiles | ✅ COMPLETE | Pike, Kirk and TNG/DS9/Voyager technology, presentation and training overrides established without duplicating the Academy. |

## Starfleet starships / technology

| Area | Status | Notes |
|---|---|---|
| Ship identity / class / classification model | ✅ COMPLETE | Classification ≠ class ≠ individual ship. |
| Individual ship live state | ✅ COMPLETE | Service, command, location, damage and campaign history modeled. |
| Ship-system runtime state | ✅ COMPLETE | Damage, power, degradation, repair and dependencies modeled. |
| Generated Starfleet ships | ✅ COMPLETE | Game-added ships constrained by era/class and collision validation. |
| Era technology baseline | ✅ COMPLETE | Qualitative availability matrix established, including Kirk subperiod split and class-specific late-24th-century technologies. |
| Core Starfleet class catalogue | ✅ COMPLETE | Initial eight-class gameplay catalogue complete for current scope; future classes are added progressively when needed. |
| Individual canonical ship catalogue | ✅ COMPLETE | Eight core retained-era ships seeded for current scope; additional ships are progressive content, not a blocker. |
| Interiors / bridge stations / crew complements | ✅ COMPLETE | Bridge station permissions/POVs, interior location state and live crew/shift manifest models established. |
| Orders / alerts / power / damage | ✅ COMPLETE | Natural-language order pipeline, authority validation, alert states, power allocation, localized damage and timed repairs established. |
| Playable ship duty loops | ✅ COMPLETE | Navigation, Tactical, Engineering, Science, Communications and Medical loops share authoritative ship/world state. |

## Major remaining domains

| Domain | Status |
|---|---|
| Characters | ⬜ TODO |
| Species / cultures / languages | 🟨 IN_PROGRESS | Founding-species gameplay baseline established for Humans, Vulcans, Andorians and Tellarites; broader species, culture and language coverage remains progressive. |
| Factions and organizations | 🟨 IN_PROGRESS | Major gameplay baseline established for Federation, Klingon Empire, Romulan Star Empire, Cardassian Union, Bajor, Ferengi Alliance, Borg Collective and Dominion; wider organizations and deeper era-specific state remain progressive. |
| Astrography | 🟨 IN_PROGRESS | Gameplay-first astrography and navigation runtime established: provenance-aware locations/distances, sector reference scheme, route scoring, structured navigation orders, persistent warp travel, ETA uncertainty, era-aware chart knowledge, political-space anchors and border crossings. Wider system/route coverage remains progressive. |
| Starships and ship systems | 🟨 IN_PROGRESS | Identity model, class-vs-ship separation, runtime system state, generated-ship rules and temporal validation established. |
| Stations and facilities | 🟨 IN_PROGRESS | Facility identity/design separation, topology/live interior state, service nodes, docking/access, logistics support, playable facility assignments and blueprint-ingest workflow are established; wider station catalogue and source-backed interiors remain progressive. |
| Technology and equipment | ⬜ TODO |
| Medicine and science | ⬜ TODO |
| Conflicts and historical events | ⬜ TODO |
| Gameplay | 🟨 IN_PROGRESS | Navigation, travel, exploration, encounters, missions, duty watches, consequences, operational needs, autonomous fleet tasking, logistics/endurance, facility support and playable station-duty loops are connected to World State; broader wider-universe gameplay remains progressive. |
| Narrative | 🟨 IN_PROGRESS | Travel encounters, mission hooks, operational-needs generation and briefing/debrief structures established; campaign arcs and authored narrative structures remain future work. |
| AI | ⬜ TODO |
| Presentation and UI | ⬜ TODO |
| Assets / audio / NAP mappings | ⬜ TODO |
| Runtime content / schemas / manifests | ⬜ TODO |
| Validation suites | ⬜ TODO |

## Active block

**Wider Star Trek universe: species, factions and astrography.**

Starfleet starships are complete at the current structural/gameplay scope: era technology, class/ship identity, live systems, interiors, crews, bridge orders and role-specific duty loops are all modeled. Class/ship catalogues expand progressively as content requires them.
