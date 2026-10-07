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
| Duty shifts / watches | ✅ COMPLETE | Flexible 3/4/custom model plus class/configuration-specific generated watches, relief/on-call pools, handoffs, off-watch obligations and individual schedule integration. When the player is captain, generated watch policy is reviewable/changeable/delegable command policy. |
| Command succession / acting command | ✅ COMPLETE | CO → XO → second officer → qualified designated successor. |
| Qualifications, regulations, protocols and Prime Directive | ✅ COMPLETE | Command qualification, Prime Directive, medical authority and classified-directive model established for baseline scope. |
| Assignments, promotions, commendations and discipline | ✅ COMPLETE | Career-event baseline, service record and disciplinary consequences established. |

## Starfleet Academy

| Area | Status |
|---|---|
| History and campus | ✅ COMPLETE | Playable hub, location graph and gameplay-relevant era differences established. |
| Admissions and cadet life | ✅ COMPLETE | Access v1.0 locked: five-block general curriculum, candidate manual source, holistic admission, targeted reassessment and persistent attempt history; four-year cadet progression/conduct baseline retained. |
| Departments and specializations | ✅ COMPLETE | Playable divisions, specializations, medical route and change/cross-training rules established. |
| Curriculum and courses | ✅ COMPLETE | Four-year architecture, 60 main course/process definitions, 7 branch curricula and 501 unit designs are locked. Study-material v1.0 packs now derive from the same academic source. |
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
| Academy + career | ✅ ESTABLISHED | 🟨 IN_PROGRESS — entry systems, four-year unit curriculum and study-material v1.0 packs closed; PDF/web publishing, Academy-life scheduling and post-Academy depth remain |
| People and life aboard | ✅ ESTABLISHED | ✅ BASELINE COMPLETE — class/configuration habitability, watches, off-watch obligations, leisure constraints and persistent schedules closed in Shipboard Life v0.1; future classes/content extend the same contracts. |
| Habits, wellbeing and daily life | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Starfleet professional life | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Gameplay-required lore | ✅ READINESS PLAN | 🟨 IN_PROGRESS |
| AI and narrative | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Procedural universe and population | ✅ ESTABLISHED | 🟨 IN_PROGRESS |
| Starship Computer | ✅ ESTABLISHED | 🟨 IN_PROGRESS |

Control document: `docs/roadmap/game_design_readiness_v0_2.md`.

## Procedural content-depth baseline

Control documents:
- `docs/roadmap/procedural_content_depth_plan_v0.1.md`
- `docs/roadmap/procedural_content_depth_status_v0.1.json`

Current defined baseline:
- **63 / 63 packages COMPLETE**;
- **Wave A** species/person foundations: 18/18;
- **Wave B** cultures/social context: 12/12;
- **Wave C** organizations/factions: 9/9;
- **Wave D** ships/facilities/homeworlds: 18/18;
- **Wave E** visual/NAP depth: 6/6.

This means the currently defined depth pass has coherent source/provenance, gameplay hooks, persistence rules, AI boundaries, visual/NAP mappings and representative validation. It does **not** mean every Star Trek species, planet, ship, organization, historical event or production asset is exhaustively populated.

## Shipboard life & procedural starship generation v0.1

Control documents:
- `docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md`
- `docs/roadmap/shipboard_life_and_procedural_starship_generation_status_v0.1.json`

Current baseline:
- **15 / 15 packages COMPLETE**;
- Starfleet class/configuration life profiles;
- Klingon, Romulan and Cardassian class life profiles;
- procedural civilian design and life profiles;
- three/four/custom watch generation;
- relief, on-call and off-watch obligations;
- constrained off-duty life from actual facilities and schedules;
- source-confidence-aware staffing guidance;
- causal persistent ship-generation pipeline;
- deterministic reference generators and locked Oberth fixture;
- player-captain authority over captain-owned automated decisions;
- manual / proposal-with-approval / delegated-autonomous command modes;
- mandatory registry for future automated command decisions.

**Runtime boundary:** content/contracts/reference implementation are complete for v0.1, but authoritative live World State, schedule arbitration and off-screen catch-up remain dependent on CoreRPG 4.5+.

## Procedural facilities & station life v0.1

Control documents:
- `docs/roadmap/procedural_facilities_and_station_life_plan_v0.1.md`
- `docs/roadmap/procedural_facilities_and_station_life_status_v0.1.json`

Current baseline:
- **15 / 15 packages COMPLETE**;
- **12 reusable/controlled/restricted canonical station designs** catalogued;
- **12 canonical facility identities** reserved;
- **14 procedural functional design families**;
- strict anti-"space gas station" existence rules;
- temporary/mobile alternatives checked before permanent construction;
- smallest-sufficient-scale and existing-coverage suppression;
- construction, partial operation, commissioning, expansion, mothball and decommission states;
- operator staff, contractors, residents, dependents, tenants, visitors, patients/detainees and docked ship crews separated;
- continuous watches + day/peak work + tiny-outpost active/on-call patterns;
- finite berths, service nodes, inventory/staff dependencies and queues;
- traffic generated from real routes/missions/services/economy rather than visual decoration;
- design-specific station-life and visual/NAP profiles;
- deterministic facility reference generator;
- locked positive Relay Station 47-type fixture;
- locked negative fixture proving `player_needs_repairs` cannot create a station.

**Runtime boundary:** content/contracts/reference implementation are complete for v0.1. Authoritative live construction catch-up, facility population simulation, queues, traffic and persistence remain dependent on CoreRPG 4.5+.

## Procedural worlds, settlements, civilizations & First Contact v0.1

Control documents:
- `docs/roadmap/procedural_worlds_settlements_civilizations_first_contact_plan_v0.1.md`
- `docs/roadmap/procedural_worlds_settlements_civilizations_first_contact_status_v0.1.json`

Current baseline:
- **18 / 18 packages COMPLETE**;
- latent civilizations exist before discovery;
- deterministic persistent species morphology/appearance;
- generated language/naming systems;
- governments, institutions and representative authority;
- cities/colonies/settlements with causal infrastructure;
- economy/resources/trade grammar;
- technology and warp-state grammar;
- observer-scoped contact knowledge;
- operational Prime Directive protocol;
- First Contact readiness/briefing/protocol;
- warp threshold **does not** auto-trigger contact;
- captain command decision integrated;
- Universal Translator bootstrap with partial/ambiguous states;
- divided-world contact remains polity-scoped;
- procedural civilization visual/NAP identity;
- deterministic reference generator;
- four First Contact fixtures including pre-warp, first warp, mutual post-warp encounter and divided world.

**Runtime boundary:** civilization/settlement/contact content and reference implementation are complete for v0.1. Physical planet generation remains its separate existing contract layer; authoritative runtime execution waits on CoreRPG 4.5+.

## Procedural Civilization Evolution & Galactic Interaction v0.1

Control documents:
- `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`
- `docs/roadmap/procedural_civilization_evolution_galactic_interaction_plan_v0.1.md`
- `docs/roadmap/procedural_civilization_evolution_galactic_interaction_status_v0.1.json`

Current baseline:
- **Block 1 COMPLETE — CE001–CE015: 15/15**;
- civilizations evolve after generation/First Contact instead of freezing;
- demographic evolution is conservative and causal;
- government succession/regime change preserves civilization identity;
- cohesion/fragmentation is separated from species/culture stereotypes;
- internal economic resilience feeds evolution without pre-implementing Block 4;
- capability maturity may create a Block 6 candidate but cannot auto-advance technology;
- diplomatic relationships evolve from explicit events and preserve polity scope;
- high tension cannot silently create war;
- split/merge/extinction semantics preserve lineage/history;
- off-screen/LOD catch-up preserves identity and explicit major transitions;
- deterministic reference simulator + **9 executable tests**;
- **4 locked fictional fixtures**: stable growth, regime change, divided-world post-contact relations and causal extinction.

**Sequential boundary:** Blocks 2–10 remain TODO and have not been implemented. Block 2 is next only after this Block 1 closure.

**Runtime boundary:** Star Trek-side rules/contracts/reference simulation are complete. CoreRPG 4.5+ remains responsible for authoritative scheduling, persistence, generic event/action execution and World State mutation.

## Major remaining domains

| Domain | Status |
|---|---|
| Characters | 🟨 IN_PROGRESS | Initial player creation v1.0, mandatory biography validation, evidence-based capability growth and objective/trajectory models are now established in addition to identity/runtime, personality, knowledge, memory, relationships and reputation. Canonical-character catalogues and deeper behavioral content remain progressive. |
| Species / cultures / languages | 🟨 IN_PROGRESS | Canonical baseline remains progressive, while **procedural civilization v0.1 now adds persistent generated species morphology, language/naming profiles and Universal Translator bootstrap for newly encountered civilizations**. Wider canon coverage remains progressive. |
| Factions and organizations | 🟨 IN_PROGRESS | Major gameplay baseline established for Federation, Klingon Empire, Romulan Star Empire, Cardassian Union, Bajor, Ferengi Alliance, Borg Collective and Dominion; wider organizations and deeper era-specific state remain progressive. |
| Astrography | 🟨 IN_PROGRESS | Gameplay-first astrography/navigation remains progressive. **Procedural Worlds/Civilizations v0.1 now closes civilization/settlement materialization on pre-existing worlds, including technology, governments, cities, economy and contact state.** Wider systems/routes and exhaustive physical-world generation remain progressive. |
| Starships and ship systems | 🟨 IN_PROGRESS | Identity/class/design separation, runtime system state, causal persistent ship generation, class-specific shipboard life, civilian procedural design grammar, staffing/watch generation and deterministic reference generators are established; wider class/system content and CoreRPG runtime mapping remain progressive. |
| Stations and facilities | 🟨 IN_PROGRESS | **Procedural Facilities & Station Life v0.1 baseline is COMPLETE (15/15):** strict causal existence, reusable canonical/procedural designs, construction lifecycle, staffing/residents/tenants/visitors, watches, finite services/queues, causal traffic, expansion/drawdown, visual profiles, deterministic generator and positive/negative fixtures. Wider canon catalogue and source-backed interiors remain progressive. |
| Technology and equipment | 🟨 IN_PROGRESS | Game-ready technology framework and readiness plan established; concrete equipment/technology depth remains progressive. |
| Medicine and science | 🟨 IN_PROGRESS | Game-ready medical/scientific capability contracts established; concrete canon/gameplay content remains progressive. |
| Conflicts and historical events | 🟨 IN_PROGRESS | Machine-usable conflict and historical-event contracts established; event catalogues and provenance-backed depth remain progressive. |
| Gameplay | 🟨 IN_PROGRESS | Navigation/travel/operations remain active. Facility generation rejects player-convenience stations, and **First Contact is now a full gameplay protocol: observation → Prime Directive assessment → readiness brief → captain decision → linguistic bootstrap → scoped diplomacy**, with no automatic hail at warp threshold. |
| Narrative | 🟨 IN_PROGRESS | Travel encounters and mission hooks remain progressive. **Procedural First Contact can now generate episode-like situations from pre-existing World State rather than scripted retroactive civilizations.** Campaign arcs and authored narrative structures remain future work. |
| AI | 🟨 IN_PROGRESS | AI authority, deterministic-first routing, provider-independent capability routes and NPC interaction foundation established; deeper prompt/context/presentation content remains progressive. |
| Presentation and UI | ⬜ TODO |
| Assets / audio / NAP mappings | 🟨 IN_PROGRESS | Visual/NAP content-depth baseline is closed for current species/organization/ship/interior/homeworld scope and now also includes station-design visual profiles. Verified Sensors-console NAP fixture remains the representative binary lifecycle fixture. Wider production assets/audio remain progressive. |
| Runtime content / schemas / manifests | 🟨 IN_PROGRESS | Procedural contracts, validation manifests and machine-readable 120-layer status are established; final runtime mapping depends on CoreRPG 4.5+ contracts. |
| Validation suites | 🟨 IN_PROGRESS | Cross-domain design invariants and Sensors acceptance fixture established; executable runtime suites expand as CoreRPG gains Generic World State/actions/persistence. |

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
| Fourth Class / Year 1 architecture | ✅ COMPLETE | T1 cadet identity, T2 shipboard life/service, T3 operational foundations; five grouped subjects per trimester; PHY longitudinal and habit-driven. |
| Third Class / Year 2 architecture | ✅ COMPLETE | T1 supervised ship operations, T2 people/risk/field action, T3 integration/leadership/branch choice; specialization selected at year end. |
| Second Class / Year 3 architecture | ✅ COMPLETE | Formal specialization, cross-training, degraded operations, supervised duty and evidence-based intermediate qualification. |
| First Class / Year 4 architecture | ✅ COMPLETE | Advanced specialization, service-like watches, practicum, Kobayashi Maru, service-readiness review, first assignment and playable commissioning. |

## Active block

**Pillar 1 remains active: four-year architecture, unit curriculum and study-material v1.0 are closed; provenance pass 1 now covers 60/60 main courses and 7/7 branches, and academiaflota v0.5.0 publishes all 60 courses plus 7 branch manuals. Remaining Academy work is deeper bespoke editing, PDF production, richer interactive assessment, Academy-life scheduling/content and post-Academy depth.**

**Procedural-universe depth note:** reusable simulation patterns extracted from Nimroel have been formalized for Star Trek: layered authority/context resolution, derived subsystem seeds, Tier A/B/C populations, irreversible latent→persistent NPC promotion, schedule/knowledge/relationship constraints and validation invariants. The D001–D063 content-depth baseline is now closed across species, cultures, organizations, ships, facilities, homeworlds and visual/NAP profiles. Wider universe coverage and runtime/CoreRPG integration remain active work.

The Sensors vertical slice remains preserved and ready for later UX/runtime continuation. Current priority has shifted to deep game-design readiness: Academy/career, social life, wellbeing, professional service, gameplay-required lore, AI/narrative, full procedural universe/population and the Starship Computer. The first architecture foundation pass for all eight pillars is complete. Design-depth pass 1 has also begun: Academy master curriculum, external study interoperability, social transitions, habit formation, lore contracts, procedural celestial/civilization requirements and Computer query/action catalogue are now in place. Next work adds deeper branch/course content and provenance-backed universe data without duplicating CoreRPG runtime responsibilities.


## Procedural living-universe master plan

Control documents:
- `docs/roadmap/procedural_layers_master_plan_v0.1.md`
- `docs/roadmap/procedural_layers_status_v0.1.json`
- `docs/roadmap/procedural_runtime_readiness_v0.1.md`
- `docs/roadmap/nimroel_to_star_trek_procedural_reuse_matrix_v0.1.md`

Current layer status:
- **118 / 120 COMPLETE** at Star Trek design/contract/validation-foundation level;
- **119 PARTIAL** — Sensors acceptance fixture exists; executable console UX/duty scenario remains;
- **120 BLOCKED_RUNTIME** — waits on CoreRPG Generic World State and later runtime capabilities.

This status does **not** mean all species, planets, ships, organizations or assets are exhaustively populated. It means their governing procedural contracts and cross-domain rules now have a coherent baseline.
