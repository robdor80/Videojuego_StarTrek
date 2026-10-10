# Generation tools

## v0.0.1 observable-system generator

`generate_v0_0_1_system.py` is the reference deterministic generator for the first sensor vertical slice.

Properties:

- standard-library Python only;
- same campaign seed + sector + era + date produces the same world;
- stable generated entity IDs;
- generated truth is materialized before any sensor query;
- output includes detectable signatures, hidden properties and interference;
- built-in v0.0.1 validation.

Example:

```bash
python tools/generation/generate_v0_0_1_system.py \
  --seed academy_sensor_test_001 \
  --sector 041 \
  --era tng_ds9_voyager \
  --date 2368-01-01 \
  --validate \
  --output content/generated/universe/v0_0_1/system_041.json
```

Regression tests:

```bash
python tools/generation/test_v0_0_1_generator.py
```

The reference regression seed is locked by SHA-256 digest. An intentional generator-algorithm change must increment the generator version and update the expected digest deliberately.

- `simulate_civilization_evolution.py` — deterministic reference simulator for Block 1 civilization evolution; major transitions require explicit causes and later-block boundaries are enforced.

- `simulate_colonization_expansion.py` — deterministic Block 2 reference for target selection, colony lifecycle, population transfer, claim overlap and abandonment.

- `simulate_conflict_war.py` — deterministic Block 3 reference for doctrine/context response, war-authority gating and strategic-LOD operations with persistent force identities.


### Academy Life Step 5 — personal schedules

- `generate_academy_schedule_step5.py` is a deterministic reference scheduler for fixed Academy commitments, flexible required obligations and transfer feasibility.
- `test_generate_academy_schedule_step5.py` validates determinism, slot continuity, travel-time feasibility, conflict exposure and strict Step-6+ boundaries.


### Academy Life Step 6 — free time

- `generate_academy_free_time_step6.py` builds deterministic NPC leisure intentions and player-facing feasible choices strictly from real Step-5 schedule gaps.
- `test_generate_academy_free_time_step6.py` covers agency, facility/capacity gating, travel feasibility, background affinity, determinism and strict Step-7+ boundaries.


### Academy Life Step 7 — extracurricular activities

- `generate_academy_extracurricular_step7.py` deterministically builds/preserves finite extracurricular memberships and recurring schedule commitments from real availability.
- `test_generate_academy_extracurricular_step7.py` validates eligibility, capacity, player agency, NPC autonomy, travel/time feasibility, persistence and strict Step-8+ boundaries.


### Academy Life Step 8 — conferences, seminars and additional courses

- `generate_academy_academic_enrichment_step8.py` deterministically preserves/allocates optional formal academic registrations, waitlists and session commitments.
- `test_generate_academy_academic_enrichment_step8.py` validates offering type, capacity, eligibility, presenter availability, facility/travel feasibility, player agency, NPC autonomy and registration/attendance/completion boundaries.


### Academy Life Step 9 — social life

- `generate_academy_social_life_step9.py` deterministically preserves/plans non-romantic Academy social attendance from real time, place, invitations, circles and capacity.
- `test_generate_academy_social_life_step9.py` validates player agency, NPC autonomy, invitations, open gatherings, capacity, travel/venue constraints, non-romantic boundaries and no automatic relationship mutation.


### Academy Life Step 10 — romance and dating

- `resolve_academy_romance_dating_step10.py` deterministically validates player↔NPC romantic eligibility, invitations, responses and bilateral date feasibility under the locked adult heterosexual canon.
- `test_resolve_academy_romance_dating_step10.py` validates adult/sex-category eligibility, player agency, directional NPC interest, consent boundaries, rejection semantics, dual schedules/travel, venue requirements and strict Step-11+ boundaries.


### Academy Life Step 11 — NPC-to-NPC relationships

- `resolve_academy_npc_relationships_step11.py` deterministically evolves persistent directional NPC relationship edges from confirmed causal events.
- `test_resolve_academy_npc_relationships_step11.py` validates asymmetry, familiarity/friendship thresholds, conflict/reconciliation history, adult heterosexual NPC romance, bilateral commitment, player exclusion and strict Step-12+ boundaries.


### Academy Life Step 12 — mentors and instructors

- `resolve_academy_mentors_instructors_step12.py` validates teaching assignments, tutoring, voluntary mentorship, mentoring sessions and evidence-backed recommendations.
- `test_resolve_academy_mentors_instructors_step12.py` validates role separation, player agency, finite capacity, authority/scope, schedule/travel/facility constraints and strict Step-13+ boundaries.


### Academy Life Step 13 — wellbeing and balance

- `resolve_academy_wellbeing_step13.py` derives individualized acute/weekly/monthly wellbeing from confirmed actual activity and emits routine-observation candidates.
- `test_resolve_academy_wellbeing_step13.py` validates longitudinal behavior, profile-based sleep/load/recovery, no universal activity rewards, no superhuman bonuses, player agency, World-Truth isolation and strict Step-14+ boundaries.


### Academy Life Step 14 — obligations and consequences

- `resolve_academy_obligations_consequences_step14.py` resolves mandatory/voluntary Academy obligations from confirmed evidence, represented justifications, recurrence and authority-gated disciplinary decisions.
- `test_resolve_academy_obligations_consequences_step14.py` validates no-fault absence, make-up/remediation, lateness tolerance, recurrence, formal-review gating, authority, proportionality, player agency and strict Step-15+ boundaries.
