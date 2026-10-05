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
7. 🟨 Procedural observable universe + interactive ship consoles
8. 🟨 Species, factions, astrography and wider universe
9. 🟨 Narrative, AI, presentation and runtime content derived from validated lore

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
| Admissions and cadet life | ✅ COMPLETE | Access v1.0 locked: five-block general curriculum, candidate manual source, holistic admission, targeted reassessment and persistent attempt history; four-year cadet progression/conduct baseline retained. |
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
| Functional console catalogue v0.1 | ✅ COMPLETE | Sixteen reusable console families fixed under `gameplay/ship_operations/consoles/`; functional console is separated from physical station and UX. |
| Observable universe core | ✅ COMPLETE | Authoritative world truth, observable-entity/signature contracts, deterministic seeded v0.0.1 generator and deterministic sensor-detection resolution are implemented for the current vertical-slice scope. |
| Operational event log v0.1 | ✅ COMPLETE | Cross-console append-only event contract, event vocabulary, visibility projection and Sensors worked example established; evaluation remains a separate consumer. |
| Records and logs foundation | ✅ COMPLETE | Captain's, personal, department, duty and restricted-log foundations established with privacy/access and AI-assisted drafting boundaries. |
| Universal stardate / timekeeping | ✅ COMPLETE | All playable eras use one project rule of 1,000 stardate units per campaign year; exact campaign time remains authoritative, with 24-hour ship time and human-readable player reference. |

## Game Design Readiness v0.2

The project is using the CoreRPG lead time to complete eight game-facing design pillars before runtime integration.

| Pillar | Foundation | Content depth |
|---|---|---|
| Academy + career | ✅ ESTABLISHED | 🟨 IN_PROGRESS — access/character-entry/objectives closed; four-year curriculum depth remains |
| People and life aboard | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Habits, wellbeing and daily life | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Starfleet professional life | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Gameplay-required lore | ✅ READINESS PLAN | 🟨 IN_PROGRESS |
| AI and narrative | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Procedural universe and population | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Starship Computer | ✅ ESTABLISHED | 🟨 IN_PROGRESS |

Control document: `docs/roadmap/game_design_readiness_v0_2.md`.

## Major remaining domains

| Domain | Status |
|---|---|
| Characters | 🟨 IN_PROGRESS | Initial player creation v1.0, mandatory biography validation, evidence-based capability growth and objective/trajectory models are now established in addition to identity/runtime, personality, knowledge, memory, relationships and reputation. Canonical-character catalogues and deeper behavioral content remain progressive. |
| Species / cultures / languages | 🟨 IN_PROGRESS | Founding species plus Klingon, Romulan, Cardassian, Bajoran, Ferengi, Trill, Betazoid, Dominion-engineered species and Borg/Changeling state models established; language runtime and Universal Translator failure/ambiguity rules added. Wider coverage remains progressive. |
| Factions and organizations | 🟨 IN_PROGRESS | Major gameplay baseline established for Federation, Klingon Empire, Romulan Star Empire, Cardassian Union, Bajor, Ferengi Alliance, Borg Collective and Dominion; wider organizations and deeper era-specific state remain progressive. |
| Astrography | 🟨 IN_PROGRESS | Gameplay-first astrography and navigation runtime established: provenance-aware locations/distances, sector reference scheme, route scoring, structured navigation orders, persistent warp travel, ETA uncertainty, era-aware chart knowledge, political-space anchors and border crossings. Wider system/route coverage remains progressive. |
| Starships and ship systems | 🟨 IN_PROGRESS | Identity model, class-vs-ship separation, runtime system state, generated-ship rules and temporal validation established. |
| Stations and facilities | 🟨 IN_PROGRESS | Facility identity/design separation, topology/live interior state, docking/access, service nodes, traffic/transfer simulation, playable assignments, shipyard/refit support and blueprint-ingest workflow are established; wider catalogue and source-backed interiors remain progressive. |
| Technology and equipment | 🟨 IN_PROGRESS | Game-ready technology framework and readiness plan established; concrete equipment/technology depth remains progressive. |
| Medicine and science | 🟨 IN_PROGRESS | Game-ready medical/scientific capability contracts established; concrete canon/gameplay content remains progressive. |
| Conflicts and historical events | 🟨 IN_PROGRESS | Machine-usable conflict and historical-event contracts established; event catalogues and provenance-backed depth remain progressive. |
| Gameplay | 🟨 IN_PROGRESS | Navigation, travel, exploration, encounters, missions, duty watches, consequences, operational needs, autonomous fleet tasking, logistics/endurance, facility traffic/support, station-duty loops and persistent ship refits are connected to World State. Current vertical slice: procedural observable world → sensor resolution → interactive console → event log/evaluation. |
| Narrative | 🟨 IN_PROGRESS | Travel encounters, mission hooks, operational-needs generation and briefing/debrief structures established; campaign arcs and authored narrative structures remain future work. |
| AI | 🟨 IN_PROGRESS | AI authority, deterministic-first routing, provider-independent capability routes and NPC interaction foundation established; deeper prompt/context/presentation content remains progressive. |
| Presentation and UI | ⬜ TODO |
| Assets / audio / NAP mappings | ⬜ TODO |
| Runtime content / schemas / manifests | ⬜ TODO |
| Validation suites | ⬜ TODO |

## Pillar 1 — closed sub-blocks

| Sub-block | Status | Notes |
|---|---|---|
| Academy access v1.0 | ✅ COMPLETE | Five compact blocks, manual source, assessment model, holistic admission and targeted retakes. |
| Player profile + initial character sheet | ✅ COMPLETE | Nickname separated from character identity; adult-equivalent rule; biography-driven starting state. |
| Biography validation | ✅ COMPLETE | Mandatory deterministic + semantic coherence gate before campaign start. |
| Character development semantics | ✅ COMPLETE | Universal evidence-driven learning/practice model; no player-allocated attributes or generic visible XP. |
| Objectives / trajectory | ✅ COMPLETE | Long-term aspiration + medium-term goals, descriptive trajectory coherence, no guaranteed outcomes. |
| Specialization decision timing | ✅ COMPLETE | Selected by end of Third Class; formally active in Second Class T1. |
| Kobayashi Maru scope | ✅ COMPLETE | Project-wide Academy tradition for every playable era, with era-specific presentation. |

## Active block

**Pillar 1 remains active: entry systems are closed; the next work is the definitive four-year grouped-subject curriculum and its unit-level depth.**

The Sensors vertical slice remains preserved and ready for later UX/runtime continuation. Current priority has shifted to deep game-design readiness: Academy/career, social life, wellbeing, professional service, gameplay-required lore, AI/narrative, full procedural universe/population and the Starship Computer. The first architecture foundation pass for all eight pillars is complete. Design-depth pass 1 has also begun: Academy master curriculum, external study interoperability, social transitions, habit formation, lore contracts, procedural celestial/civilization requirements and Computer query/action catalogue are now in place. Next work adds deeper branch/course content and provenance-backed universe data without duplicating CoreRPG runtime responsibilities.
