# Academy Life & Social Simulation v0.1

**Status:** ACTIVE  
**Execution rule:** strictly one step at a time. A step is not started until the previous step is COMPLETE, validated, cross-referenced and recorded.

## Purpose

Turn Starfleet Academy from a complete academic/training framework into four lived years with persistent population, routines, free time, social life, relationships and off-screen continuity.

## 20-step sequence

| Step | Scope | Status |
|---|---|---|
| 1 | Academy population | COMPLETE |
| 2 | Procedural cadet generation | COMPLETE |
| 3 | Classmates, study groups and practical teams | COMPLETE |
| 4 | Quarters and roommates | TODO |
| 5 | Personal schedules | TODO |
| 6 | Free time | TODO |
| 7 | Extracurricular activities | TODO |
| 8 | Conferences, seminars and additional courses | TODO |
| 9 | Social life | TODO |
| 10 | Romance and dating | TODO |
| 11 | NPC↔NPC relationships | TODO |
| 12 | Mentors and instructors | TODO |
| 13 | Wellbeing and balance | TODO |
| 14 | Obligations and consequences | TODO |
| 15 | Campus events | TODO |
| 16 | Off-screen Academy life | TODO |
| 17 | Social LOD | TODO |
| 18 | Year progression and continuity | TODO |
| 19 | Academy-record integration | TODO |
| 20 | Final fixtures, invariants, simulator and test closure | TODO |

## Step 1 — Academy population

Step 1 defines **who exists as part of the Academy population and how that population is conserved**. It does not yet generate the full individual cadets of Step 2.

### Population accounting

Academy population is structure-first and separates:
- Cadet 4th Class.
- Cadet 3rd Class.
- Cadet 2nd Class.
- Cadet 1st Class.
- Instructional staff.
- Operational/support staff.
- Attached training personnel.
- Temporary visitors.

Exact Academy population numbers are not asserted as canon by this block. Production population is era/campaign/content configured. Validation fixtures use fictional numbers only.

### Identity / LOD

Each accounted population slot is one of:
- **Tier A** — authored/canonical persistent individual.
- **Tier B** — generated persistent individual.
- **Tier C** — latent population slot.

Materializing a Tier C cadet into Tier B consumes the same real slot. It never increases cohort population.

### Membership != presence

A cadet away on field study, training cruise, leave, medical treatment or authorized travel remains a member of the Academy cohort unless an explicit membership event changes that state.

### Player rule

The player cadet occupies one real cadet slot. Admission is a real membership event; the player is not added outside the Academy population accounting.

### Population transitions

Population changes only through explicit events such as:
- admission;
- transfer in/out;
- withdrawal;
- dismissal;
- death;
- graduation/commission;
- staff assignment/reassignment;
- visitor arrival/departure.

### Hard rules

1. The Academy is not populated because the player enters a room.
2. Population structure exists before individual materialization.
3. One cadet belongs to exactly one current cadet class.
4. Tier C→B promotion conserves population.
5. Materialized identity never returns to anonymous Tier C.
6. Canonical/authored cadets occupy real population slots.
7. The player occupies a real population slot.
8. Temporary absence does not change cohort membership.
9. Graduation/departure requires an explicit event.
10. Visitors are not cadets or staff unless separately assigned/enrolled.
11. Exact total Academy population is data/configuration, not silently invented as canon.
12. Species composition may constrain population context but cannot determine personality, morality, friendship or competence.

## Step 1 boundary

Step 1 deliberately does **not** implement:
- individual procedural cadet generation — Step 2;
- classmates/groups — Step 3;
- roommates — Step 4;
- personal scheduling — Step 5;
- social/romantic systems — Steps 9–11;
- off-screen Academy simulation — Step 16;
- final suite closure — Step 20.

## Deferred external work

**Procedural Dynamic Universe Block 4 — Living Interplanetary / Interstellar Economy remains TODO and is intentionally deferred until Academy Life & Social Simulation Step 20 is COMPLETE.** After Step 20, work returns to Dynamic Universe Block 4 before Block 5.

## Step 2 — Procedural cadet generation

Step 2 materializes a **persistent individual cadet** from one real latent cadet slot defined by Step 1.

### Generation pipeline

```text
real Academy population slot
→ stable cadet entity_id
→ species context
→ social/origin/culture/citizenship context
→ name from cultural/social naming context
→ prior education / interests / hobbies
→ Academy class state
→ branch interests or already-existing specialization
→ isolated personality seed + species-agnostic personality recipe
→ isolated knowledge/background seeds
→ persistent visual identity reference
→ consume latent slot without changing population total
```

### Identity rules

- Species, culture, citizenship, origin, Academy membership and personality are separate state.
- Species is selected from the campaign/era population context but **does not select personality**.
- Names resolve from the selected social/origin/cultural naming context, not directly from species.
- Culture may be mixed, off-world or cross-species when the supplied context supports it.
- Citizenship is not inferred from species or birthplace.
- A generated cadet must already have a valid Academy admission/membership basis.
- Exact age/birth date is not invented when species lifecycle data does not provide a valid range; adult-equivalent status remains mandatory.
- Reserved/canonical display-name collisions are rejected/avoided.

### Academy-state rules

- 4th Class and 3rd Class generated cadets have branch **interests**, not a prematurely locked specialization.
- 2nd Class and 1st Class cadets materialize with their already-existing specialization state because formal specialization has begun by then.
- Generation never grants capability scores without evidence; prior education/hobbies/interests are background evidence/context only.
- Knowledge is seeded independently and remains observer/experience constrained.

### Strict boundary

Step 2 does **not** create:
- classmates or study/practical groups — Step 3;
- roommates/quarters relationships — Step 4;
- personal schedules — Step 5;
- new Academy friendships/rivalries — Steps 9/11;
- romance — Step 10.

Those fields remain empty/null at Step 2 materialization.

### Persistence

The cadet is bound permanently to:
- one stable `character_id`;
- the consumed `population_slot_ref`;
- one personality seed;
- one knowledge seed;
- one background seed;
- one base visual identity lineage.

Save/load, LOD changes, later social importance or generator updates cannot reroll the cadet.


## Step 3 — Classmates, study groups and practical teams

Step 3 closes slot-first academic grouping: class sections, study groups and course-eligible practical teams. **Academic proximity is not a social relationship.** Membership is anchored to `population_slot_ref`, so latent cadets can already have stable classmates/teams and later materialization preserves them. Class sections never mix cadet classes; study groups do not create friendship; practical teams support deterministic, specialization-aligned or cross-branch policies. Player presence cannot reshuffle groups. Reassignment requires an explicit academic event.

**Boundary:** quarters/roommates remain Step 4; schedules Step 5; social relationship mutation Steps 9/11; romance Step 10.
