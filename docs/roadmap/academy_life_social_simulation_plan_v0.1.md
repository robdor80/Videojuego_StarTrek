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
| 4 | Quarters and roommates | COMPLETE |
| 5 | Personal schedules | COMPLETE |
| 6 | Free time | COMPLETE |
| 7 | Extracurricular activities | COMPLETE |
| 8 | Conferences, seminars and additional courses | COMPLETE |
| 9 | Social life | COMPLETE |
| 10 | Romance and dating | COMPLETE |
| 11 | NPC↔NPC relationships | COMPLETE |
| 12 | Mentors and instructors | COMPLETE |
| 13 | Wellbeing and balance | COMPLETE |
| 14 | Obligations and consequences | COMPLETE |
| 15 | Campus events | COMPLETE |
| 16 | Off-screen Academy life | COMPLETE |
| 17 | Social LOD | COMPLETE |
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

## Step 4 — Quarters and roommates

Step 4 closes Academy residential assignment over **finite, pre-existing quarters capacity**.

A quarters assignment is anchored to `population_slot_ref`, so latent cadets can already have a stable room and roommate context before individual materialization. Materializing the cadet does not change housing.

**Roommate ≠ friend.** Sharing a room creates co-residency/shared-history opportunity only. It never creates trust, affection, rivalry or romance by itself.

Hard medical, environmental, accessibility, safety or represented legal requirements constrain eligible housing. Species ID itself is never a roommate rule; a species-specific physiological need must first resolve into an explicit housing requirement. Personality likewise does not determine mandatory compatibility.

If no compatible room/bed exists, housing remains explicitly unresolved; the system does not synthesize a new room.

Temporary absence does not automatically release the room. Reassignment/release requires a real event. Quarters establish residence, not current physical presence: **personal schedule and actual presence remain Step 5**.


## Step 5 — Personal schedules

Step 5 closes persistent **personal timetable construction and feasibility** for Academy cadets.

Schedules are anchored to `population_slot_ref`, not to whether an NPC is currently materialized. A latent cadet may therefore already have a stable class/practical/study timetable; later materialization must preserve it.

The schedule contains fixed institutional commitments, explicitly configured protected personal/medical windows, deterministic placement of flexible required preparation/study obligations, and derived transit blocks where travel is required between locations.

**Schedule ≠ actual presence.** A timetable states where a cadet is expected to be. Runtime World State remains authoritative for where that cadet actually is. Later systems may represent lateness, absence, emergencies or deliberate non-compliance without rewriting historical schedule truth.

Travel consumes time. Two commitments at different locations are invalid when the configured location graph cannot provide sufficient transfer time; the scheduler records an explicit conflict rather than granting zero-time movement.

Uncommitted intervals are exposed as temporal capacity only. Step 5 does not choose leisure, clubs, social encounters, dates or other free-time behavior.

Schedule mutation requires an explicit revision/exception event and preserves prior versions/history.

**Boundary:** free-time choice remains Step 6; extracurricular activity Step 7; social life Step 9; romance Step 10; wellbeing consequences Step 13; obligation/discipline consequences Step 14; off-screen life execution Step 16.


## Step 6 — Free time

Step 6 converts the **real uncommitted temporal capacity** exposed by Step 5 into optional off-duty activity plans without stealing time from academic obligations.

Free time is not generated independently of the schedule. An activity must fit wholly inside an available interval, including travel from the previous anchor and to the next anchor. If no suitable activity fits, the interval may remain genuinely unallocated.

NPC cadets may choose autonomous free-time plans from authored activities using persistent interests, hobbies and explicit preference state. **Species is not a leisure stereotype** and player proximity is never a selection weight.

The player character is treated differently for agency: the system exposes feasible options but does not automatically choose a leisure activity for the player. A player-selected activity is accepted only if it is physically and temporally valid.

Activity selection is capability-driven. A location/facility must actually support the activity, limited capacity may be consumed, and authorized leave is required for off-campus leave activities. No holodeck, gym, social venue or other capability is invented merely because an activity would be convenient.

**Free-time plan ≠ actual activity execution.** The plan represents an intention/tentative schedule item. Runtime presence/action state decides what actually happens; interruptions or changes require state/event provenance rather than retroactively rewriting the plan.

A Step-6 activity may place a cadet in a common/public space, but it does not create a social event or relationship change. Participants, friendships, invitations, dating and NPC↔NPC social evolution remain later steps.

**Boundary:** extracurricular commitments remain Step 7; conferences/additional courses Step 8; social-life event resolution Step 9; romance Step 10; NPC↔NPC relationship evolution Step 11; wellbeing effects Step 13; obligations/consequences Step 14; off-screen execution Step 16.


## Step 7 — Extracurricular activities

Step 7 introduces **persistent organized extracurriculars**: clubs, teams, associations, service groups and recurring non-curricular activities that cadets may voluntarily join.

An extracurricular is a real Academy-life entity with a stable ID, category, membership capacity, eligibility/prerequisite rules, recurring session schedule and required facility/location capabilities. It is not a cosmetic trait attached to the player.

Membership is anchored to `population_slot_ref`. Latent cadets may already belong to an extracurricular and later materialization must preserve that membership.

NPC cadets may autonomously join eligible activities using persistent hobbies/interests/preferences as affinity inputs, subject to capacity and timetable feasibility. **Species, player proximity and narrative convenience are never membership selectors.**

The player is never automatically enrolled. The system exposes eligible activities and accepts only an explicit player join request that satisfies the same requirements and capacity rules as NPCs.

Recurring sessions become real schedule commitments and therefore must fit existing available windows, including travel. If the recurring pattern cannot fit, the membership is not created merely to satisfy story intent.

**Membership ≠ attendance ≠ relationship ≠ skill.** Joining an activity creates a persistent organizational context and recurring obligation. It does not prove attendance at every session, create friendship/rivalry/romance, grant competence, improve grades or produce wellbeing bonuses. Actual participation can later provide evidence to the appropriate systems only when runtime events confirm it.

Extracurricular capacity is finite when configured. Existing valid memberships are preserved before new allocations, so observing/materializing the player cannot reshuffle club rosters.

Step 7 does not implement academic seminars, guest lectures or additional formal courses; those belong to Step 8.

**Boundary:** conferences/seminars/additional courses remain Step 8; social event resolution Step 9; romance Step 10; NPC↔NPC relationships Step 11; mentors Step 12; wellbeing Step 13; obligation/consequence handling Step 14; off-screen execution Step 16.


## Step 8 — Conferences, seminars and additional courses

Step 8 introduces **formal optional academic enrichment** as persistent Academy offerings distinct from ordinary curriculum and from Step-7 extracurricular clubs.

Three offering families are supported:
- **conference** — normally one-off or short-form academic presentation; may require registration/attendance but need not include assessment;
- **seminar** — focused small-group or workshop-style instruction that may require active participation or practical evidence;
- **additional_course** — optional formal multi-session instruction that may define assessment/completion requirements.

An offering has stable identity, type, capacity, eligibility/prerequisites, presenter/instructor reference, presenter availability, session schedule, venue/capability requirements and a completion policy.

Existing valid registrations are preserved before new allocation. Capacity is finite; when a valid candidate cannot be admitted because the offering is full, the result is a **waitlist**, not a fabricated extra seat.

NPC cadets may register autonomously from academic interests, branch interests and explicit enrichment preferences after eligibility and schedule feasibility are satisfied. **Species, player proximity and narrative convenience are never registration selectors.**

The player is never automatically registered. The system exposes eligible offerings and accepts only explicit player registration requests. Full offerings may place the player on the same waitlist logic used for NPCs.

All sessions must fit real available timetable windows, including travel. Multi-session seminars/courses are admitted only when every required scheduled session is feasible. The offering must also have a real compatible venue and a represented presenter available for the required sessions.

**Registration ≠ attendance ≠ completion.** Registration creates schedule commitments. Attendance remains runtime/event truth. Completion may require attendance, practical evidence and/or assessment according to the offering policy.

Step 8 may define **completion evidence candidates**, but it does not write final Academy-record credit, qualification or transcript state. That authoritative integration remains Step 19. No registration alone grants competence, grade, reputation or wellbeing benefit.

**Boundary:** social event resolution remains Step 9; romance Step 10; NPC↔NPC relationships Step 11; mentors/instructors as relationship systems Step 12; wellbeing Step 13; obligations/consequences Step 14; campus events Step 15; off-screen execution Step 16; Academy-record integration Step 19.


## Step 9 — Social life

Step 9 turns Academy co-presence into a **persistent but causal social layer**: invitations, open gatherings, shared meals, common-room time, informal group activities and conversation opportunities.

A social opportunity is not spawned because the player is nearby. It has a stable ID, time, place, access mode, capacity and contextual eligibility. It must fit real available time, real travel and a real venue/capability.

Two access modes are supported:
- **open_gathering** — eligible cadets may independently plan to attend;
- **invitation_required** — only represented invitees may RSVP/plan attendance.

NPCs may autonomously form social attendance intentions from explicit social preferences and relevant social-circle context. **Species, sex category and player proximity are not selectors for ordinary non-romantic social life.**

The player is never auto-RSVPed or auto-socialized. The system exposes feasible invitations/gatherings and accepts explicit player decisions. Rejecting or ignoring an invitation is a valid outcome.

Social circles are contextual indexes such as class section, roommate context, practical team, extracurricular or enrichment cohort. **Circle membership is not friendship.**

**Plan ≠ attendance ≠ interaction ≠ relationship.** Planning to attend does not prove presence. Co-presence does not prove conversation. Conversation does not automatically create friendship. Confirmed interaction may later create familiarity/shared-history evidence, but authoritative relationship transitions remain event/rule driven. NPC↔NPC relationship evolution is still Step 11.

Step 9 deliberately forbids romantic/sexual event generation. The project-wide author canon is now locked in `gameplay/social/adult_heterosexual_relationship_canon_v0.1.json`: romance/sexual relationship systems apply only to adult-equivalent characters and are heterosexual-only. Step 10 must consume that canon rather than reinterpret it.

**Boundary:** romance/dating remains Step 10; NPC↔NPC relationship evolution Step 11; mentors Step 12; wellbeing Step 13; obligation/consequence handling Step 14; campus events Step 15; off-screen execution Step 16.


## Step 10 — Romance and dating

Step 10 closes **Academy player↔NPC romance and dating mechanics** under the project-wide author canon in `gameplay/social/adult_heterosexual_relationship_canon_v0.1.json`.

### Hard eligibility

Romantic/dating mechanics require:
- both participants are represented as adult-equivalent;
- one participant has authored sex category `male` and the other `female`;
- both are current eligible Academy-life characters;
- no represented hard boundary forbids the interaction.

Missing sex/adult state is unresolved/ineligible. The system does not infer it from species, name, appearance or prose.

**Heterosexual compatibility ≠ attraction.** Compatibility only determines whether romance is permitted by project canon. Attraction/interest is separate, directional relationship state with causal provenance.

### Player agency

The player character's romantic interest is **never inferred or generated**. Player flirting, invitation, acceptance, rejection, commitment or withdrawal must come from explicit player action.

An NPC may initiate a romantic invitation toward the player only when an authoritative NPC→player romantic-interest state already exists and other eligibility/boundary rules pass. Player proximity or narrative convenience cannot synthesize interest.

### Invitation and dating

A romantic invitation is a proposal, not consent to a relationship. The recipient may:
- accept;
- decline;
- leave unanswered/expire;
- withdraw acceptance before the date.

A declined invitation does not automatically create hostility, humiliation, resentment or rivalry.

An accepted date must fit **both participants' real schedules**, real travel time and an actual compatible venue. No private/social venue is invented for convenience.

**Invitation ≠ accepted date ≠ attendance ≠ completed date ≠ relationship.** A completed date may produce relationship-change evidence, but dating/commitment state requires validated reciprocal events/provenance.

### Consent and adult intimacy boundary

Any romantic or intimate escalation is context-specific and independently consented. Friendship, rank, favors, persistence, prior dates, attraction or established relationship never imply consent. Consent may be refused or withdrawn.

Step 10 models relationship state and consent gates without graphic sexual content. Intimate adult relationship events, when represented, remain non-automatic and subject to the same canon/provenance rules.

### Step boundary

Step 10 implements the player↔NPC romance/dating mechanics. **Autonomous NPC↔NPC relationship evolution remains Step 11**, which must reuse these eligibility, provenance and consent rules rather than inventing another romance model.

**Boundary:** NPC↔NPC relationship evolution remains Step 11; mentors Step 12; wellbeing Step 13; obligation/consequence handling Step 14; campus events Step 15; off-screen execution Step 16.


## Step 11 — NPC↔NPC relationships

Step 11 closes **autonomous persistent relationship evolution between Academy NPCs**.

The resolver consumes confirmed social/professional/relationship events and evolves **directional, multidimensional edges**. It does not use a single friendship score and it never creates relationship history merely because two NPCs occupy the same room, class, club or social event.

Supported evolution includes:
- familiarity from confirmed encounters;
- personal affinity/trust from represented positive or negative history;
- professional respect from actual collaboration/conduct;
- developing friendship from sustained positive shared history;
- conflict, apology and partial reconciliation without erasing the original history;
- adult heterosexual romantic-interest emergence, expression, dating and commitment when the locked project canon and event evidence permit it;
- separation/estrangement while retaining shared history.

**A→B and B→A are separate edges.** One NPC may trust, admire, resent or feel romantic interest toward another without the reverse being true.

Friendship is never created by one positive interaction. A friendship transition requires sufficient prior familiarity plus multiple positive shared-history references. Close friendship requires an already established friendship plus further represented history.

Conflict is likewise causal. A disagreement may create tension without permanent hostility. Apology/reconciliation may repair dimensions partially while preserving the underlying conflict event in history.

### Autonomous romance between NPCs

Step 11 reuses the exact Step-10 canon and does not create an alternative romance model:
- both NPCs must be adult-equivalent;
- romantic/sexual eligibility is heterosexual-only under the locked author canon;
- eligibility does not create attraction;
- romantic interest may be unilateral;
- interest emergence/expression requires represented causal event provenance;
- mutual interest does not automatically create dating;
- dating/commitment requires bilateral evidence;
- rejection alone never creates hostility;
- relationship/intimacy consent remains contextual and cannot be inferred.

### Player boundary

The autonomous Step-11 resolver **rejects any event containing the player**. Player↔NPC romance/social decisions remain under the player-facing mechanics of Steps 9–10.

### Persistence boundary

Materialization state, player proximity, species identity and camera observation do not change relationship outcomes. Relationship history belongs to persistent World Truth.

**Boundary:** mentors/instructors remain Step 12; wellbeing Step 13; obligations/consequences Step 14; campus events Step 15; off-screen execution Step 16; social LOD Step 17.


## Step 12 — Mentors and instructors

Step 12 closes the Academy's **persistent instructor, tutoring and professional mentorship layer**.

The same character may teach, tutor and mentor, but these are separate roles:
- **instructor assignment** — institutional authority to teach/evaluate specified subjects;
- **tutoring** — a one-off or limited academic-help session;
- **mentorship** — a persistent voluntary professional relationship with explicit scope, capacity and history.

**Instructor ≠ tutor ≠ mentor.** Being assigned to teach a cadet does not create mentorship. A tutoring session does not create mentorship. Mentorship does not enlarge an instructor's academic, disciplinary or qualification authority.

Instructors remain persistent characters and retain the existing temporal/campaign-validity rules. Canonical characters may only teach or mentor when their actual date, assignment and campaign history allow it.

### Mentorship

Mentorship requires:
- an active represented instructor;
- a professional scope the instructor is actually allowed to mentor;
- causal provenance for the proposal;
- available mentor capacity;
- cadet mentor-capacity availability;
- represented acceptance by both sides.

The player is never assigned a mentor automatically. A proposal to the player remains unresolved until the player explicitly accepts or declines. NPC acceptance likewise requires represented state rather than narrative convenience.

Mentorship is professional context, **not friendship, romance, grade advantage or command privilege**. Species, sex category, materialization state and player proximity are not mentor-selection shortcuts.

### Tutoring and mentoring sessions

Tutoring and mentoring meetings consume real time. Instructor and cadet must both have compatible windows, real travel time and an actual location with the required capability.

A planned session does not prove attendance. Actual participation remains runtime/event truth.

### Recommendations and authority

A mentor may create a recommendation evidence candidate only when:
- an active mentorship exists;
- the instructor has recommendation authority;
- the recommendation cites real observed evidence.

A recommendation may influence later systems but **never guarantees a grade, qualification, posting, billet, promotion or assignment**. Mentorship cannot bypass curriculum, evaluation, qualification, discipline or career rules.

### Continuity

Mentorship history persists. Ending or changing a mentorship does not erase previous sessions/recommendations.

Academy mentorship does not automatically continue after graduation. Its history may remain part of the relationship, but active-duty mentorship requires a new valid post-Academy assignment.

**Boundary:** wellbeing/balance remains Step 13; obligations/consequences Step 14; campus events Step 15; off-screen Academy life Step 16; social LOD Step 17.


## Step 13 — Wellbeing and balance

Step 13 connects Academy life to the shared character habits/wellbeing system. It does **not** create Academy-specific happiness, stress or fatigue bars.

Wellbeing is derived from **confirmed actual behavior**, not from plans:
- sleeping;
- studying;
- duty/training;
- exercise;
- meals;
- quiet or active recovery;
- leisure;
- social connection;
- romantic/intimate time when actually represented and consensual;
- exceptional/emergency stressors.

A planned gym visit, date, rest period or mentoring session contributes nothing until authoritative runtime/event evidence confirms that the activity occurred.

### Time horizons

The resolver observes overlapping windows:
- **24 hours** — acute fatigue/current load;
- **7 days** — short-term accumulated fatigue, recovery and overload;
- **30 days** — longitudinal pattern/routine evidence and persistent stress context.

One poor night normally creates an acute effect, not a month-long collapse. Sustained overload matters more than a single ordinary deviation.

### Individual baselines

Each character uses an explicit wellbeing profile:
- sleep target;
- sustainable workload;
- preferred recovery activity families;
- other authored physiological/preference context.

**Species ID alone never determines wellbeing.** Species/culture may inform an authored character profile elsewhere, but Step 13 consumes the explicit profile rather than stereotyping from species identity.

### Balance and gameplay effect

Good balance preserves normal professional/learning capacity. It **does not create superhuman buffs**.

Sustained imbalance may reduce character-side:
- concentration readiness;
- sustained attention;
- learning readiness;
- physical readiness;
- contextual professional assistance.

It never alters authoritative World Truth. A fatigued sensor officer does not make a real contact disappear; the character may simply provide less assistance interpreting it.

The player keeps agency. Fatigue/stress never force dialogue, morality or decisions.

### Habits

Repeated **actual** activity may generate routine-observation candidates. One isolated activity cannot become a habit. Habits remain evidence-based patterns rather than selectable perks.

### Strict Step-14 boundary

Step 13 calculates wellbeing/balance state only.

It does **not**:
- mark absence/tardiness;
- fail a course;
- issue punishment;
- create disciplinary action;
- change standing;
- automatically excuse obligations;
- create academic/career consequences.

Those causal obligation/consequence rules remain Step 14.

**Boundary:** obligations/consequences remain Step 14; campus events Step 15; off-screen Academy life Step 16; social LOD Step 17.


## Step 14 — Obligations and consequences

Step 14 closes the Academy's **obligation-resolution and consequence pipeline**.

The system begins from a pre-existing real obligation and authoritative evidence. It never invents a missed class, failed duty or disciplinary incident merely to create drama.

The causal chain is:

`obligation → confirmed evidence → justification/context → resolution → proportionate consequence or review → authorized decision`

### Obligation outcomes

The resolver distinguishes:
- fulfilled;
- fulfilled within lateness tolerance;
- late breach;
- excused/no-fault absence;
- unexcused absence;
- incomplete/failed required activity;
- authorized withdrawal;
- conduct/safety/order breach;
- unresolved/missing evidence.

**Failure to perform is not automatically misconduct.** An incomplete assessment may require remediation without creating a disciplinary offense.

### Justification and no-fault cases

Represented approved contexts may include:
- authorized medical reason;
- authorized leave;
- institutional schedule conflict;
- emergency preemption;
- authorized accommodation.

A justified absence may still require a make-up activity. **Make-up work is not punishment.**

Wellbeing from Step 13 is relevant context but never an automatic excuse. A fatigue/stress state only changes obligation status when an authorized rule/process actually grants accommodation, medical restriction or other recognized justification.

### Recurrence

Repeated unexcused failures may accumulate evidence and cross an authored review threshold. Recurrence does not retroactively turn earlier no-fault/justified events into misconduct.

### Discipline and due process

The project-wide Starfleet rule remains: there is **no universal sentencing table** of “offense X = punishment Y”.

Formal discipline requires:
- a recorded conduct/order/safety breach or qualifying recurrent pattern;
- intent/harm/order/context where relevant;
- a formal review basis;
- competent authority;
- confirmed decision provenance;
- authority sufficient for the measure;
- proportionality to the reviewed context.

The resolver may validate an explicitly represented disciplinary decision, but it does **not choose a punishment autonomously**.

Invalid authority or a disproportionate measure is rejected.

### Player agency

The system never invents a confession, excuse, appeal or acceptance for the player. Missing player action remains unresolved where that action is required.

### Strict downstream boundaries

Step 14 may produce:
- make-up requirements;
- remediation requirements;
- attendance/conduct concern records;
- formal-review candidates;
- validated disciplinary-action events.

It does **not** directly:
- write the final Academy/service record — Step 19;
- decide annual advancement/repetition/dismissal — Step 18;
- invent campus-wide events — Step 15;
- execute off-screen catch-up — Step 16.

**Boundary:** campus events remain Step 15; off-screen Academy life Step 16; social LOD Step 17; year progression Step 18; Academy-record integration Step 19.


## Step 15 — Campus events

Step 15 closes the Academy's **institutional campus-event layer**.

A campus event is a persistent institutional/world event with stable identity, source/cause, authority, time, location, capacity, priority and participation rules. It is not generated because the player is nearby or because pacing needs “something to happen”.

Three event origins are supported:
- **scheduled_institutional** — calendar/authority-backed ceremonies, assemblies, competitions, drills or other planned institutional activity;
- **emergent_incident** — a campus incident registered from a pre-existing causal event;
- **crisis_alert** — a high-priority institutional alert activated from real causes and competent authority.

A quiet period with no event is a valid state.

### Existing world first

Scheduled events require an institutional source and scheduling authority.

Emergent incidents and crisis alerts require explicit cause-event provenance. A template cannot retroactively invent the incident it claims to represent.

External visitors/guests must already exist as known entities. The event cannot materialize an admiral, celebrity or visiting officer merely because the event wants one.

### Participation

Campus events may use:
- **mandatory_scope**;
- **role_assignment**;
- **optional_open**;
- **invitation_only**.

Mandatory/assigned events create **obligation candidates**, not attendance facts.

Optional events never auto-enroll or auto-attend the player. NPCs may create deterministic optional participation plans from real interests/preferences, capacity and schedule feasibility.

**Event exists ≠ invited/required ≠ participation plan ≠ attendance ≠ interaction.**

Actual attendance remains runtime/event truth.

### Schedule and crisis handling

Every event uses a real campus location/capability and real travel time.

A normal event that cannot coexist with a cadet's current schedule creates a **schedule conflict candidate** rather than silently rewriting the timetable.

A crisis alert may create a **schedule-revision/preemption candidate** only when:
- its preemption policy permits it;
- the activating authority has explicit preemption scope.

Even then the output is a candidate for authoritative schedule resolution, never an invisible mutation.

If an institutional preemption causes a conflict with another obligation, Step 15 may emit an **institutional schedule-conflict justification candidate** for Step 14. It does not mark the prior absence as automatically excused by itself.

### Cancellation and history

Cancellation requires explicit provenance and competent authority. A cancelled event remains historically addressable and produces no new attendance obligation.

### Cross-system boundaries

Campus events may create context for later social interactions, wellbeing activity evidence, academic/conduct consequences and records. Step 15 performs none of those mutations directly.

Academic conferences/seminars/courses remain owned by Step 8 and may be referenced by a campus event, not duplicated into a second academic-enrichment system.

**Boundary:** off-screen Academy life remains Step 16; social LOD Step 17; year progression Step 18; Academy-record integration Step 19.


## Step 16 — Off-screen Academy life

Step 16 closes deterministic Academy catch-up when cadets, staff or events are outside the player's current simulation focus.

Off-screen simulation does **not** mean free narrative invention. It consumes already-authorized state: schedules, obligations, plans, campus events, relationships, wellbeing context and world events.

Routine activity may be aggregated for efficiency, but consequential events remain explicit and provenance-backed.

The catch-up order is deterministic by time then stable event identity. A latent NPC and a materialized NPC with the same persistent state resolve the same World Truth.

### Player agency boundary

The player's optional social, romantic, extracurricular, enrichment and other discretionary choices are never auto-resolved merely because time advances.

Required obligations may still become due while the player is away, but unresolved player decisions remain unresolved unless an explicit time-skip policy/action authorized their handling.

### No time-is-progress magic

Elapsed time alone does not:
- create friendship, romance or breakup;
- complete courses/evaluations;
- award qualifications;
- promote or graduate;
- erase fatigue or discipline;
- create campus incidents.

All such changes require the same evidence/process used on-screen.

### Cross-system outputs

Confirmed off-screen activity may produce normal event evidence for:
- attendance/obligations (Step 14 rules);
- social contact/relationship resolution (Steps 9–11);
- wellbeing activity (Step 13);
- campus-event participation (Step 15);
- evaluation/progression later.

Step 16 owns **execution/catch-up**, not the downstream rule semantics.

**Boundary:** Social LOD remains Step 17; year progression Step 18; Academy-record integration Step 19.


## Step 17 — Social LOD

Step 17 adapts the shared A/B/C social-simulation LOD model to Academy life.

LOD controls **simulation richness and update cost**, never whether a person or relationship existed.

- **A — important_persistent:** close relationships, mentor/mentee, recurring rival, major teammate or otherwise deeply relevant cadet/staff.
- **B — persistent:** stable known individual with simplified but persistent routines, memories and relationship edges.
- **C — background/latent:** persistent population slot with low-detail state until direct relevance requires richer simulation.

C→B and B→A promotion preserve stable identity, history, relationships, group memberships, schedules and record references. A/B may later reduce simulation detail when sustained relevance falls, but **detail reduction is not identity demotion** and never erases established history.

Player proximity alone is insufficient to promote an NPC. Direct interaction, persistent relationship significance, mentorship, repeated shared activity or consequential history are valid relevance sources.

At low LOD, routine contact may aggregate, but friendship, romance, breakup, discipline, major conflict, injury and other consequential transitions still require explicit causal events. LOD is never permission to fabricate drama.

**Boundary:** year progression remains Step 18; Academy-record integration Step 19.
