# Starfleet Academy Master Curriculum v0.2

Status: **FOUR-YEAR ARCHITECTURE LOCKED — UNIT DESIGN COMPLETE**

## Purpose

Define a complete playable academic spine from pre-admission preparation through graduation.

This is a gameplay curriculum, not a list of Star Trek trivia.

Every subject should eventually connect to one or more real game systems.

## Pre-Admission / Access Preparation

Optional study layer before the formal admission process.

Focus:

- Starfleet mission and institutional basics;
- Federation foundations;
- basic mathematics/scientific reasoning;
- spatial reasoning;
- communication and reading comprehension;
- physical readiness;
- introductory ranks/divisions;
- general technological literacy.

The access layer prepares the player without requiring them to memorize wiki facts.

## Cadet 4th Class — Foundations and Discovery

### Trimester 1 — Becoming a Cadet

Common core:

- Starfleet structure, mission and values;
- ranks, insignia and forms of address;
- chain of command;
- divisions, departments and common shipboard roles;
- Academy procedures and conduct;
- Federation foundations and major cultures;
- basic physical readiness;
- introduction to the Starship Computer and PADD workflow.

Gameplay goals:

- know who can order whom;
- address officers correctly;
- understand basic Starfleet institutional context;
- navigate Academy systems;
- use the Computer for simple authorized queries.

### Trimester 2 — Life Aboard a Starship

Common core:

- shipboard organization;
- duty watches, relief and reporting;
- bridge station overview;
- starship class/role overview;
- emergency alarms and alert states;
- basic communications;
- personal equipment / tricorder familiarization;
- environmental and life-support awareness;
- basic damage-control safety.

Gameplay goals:

- understand a normal duty day;
- receive and acknowledge an order;
- make a basic professional report;
- identify major ship systems/stations;
- respond correctly to common alarms.

### Trimester 3 — Operational Technology Fundamentals

Common core:

- warp and impulse concepts;
- basic navigation / astrography;
- basic sensor concepts;
- transporters;
- replicators;
- holodecks;
- shields and weapons overview;
- scientific method;
- emergency response practical;
- division exploration rotations.

Gameplay goals:

- understand what major technologies can and cannot do;
- distinguish Sensors from Science interpretation;
- understand normal navigation concepts;
- begin choosing likely professional direction.

## Cadet 3rd Class — Professional Exploration

### Trimester 1 — Applied Ship Operations

Common/applied:

- bridge operations;
- Operations coordination;
- energy/power fundamentals;
- Engineering fundamentals;
- sensor/search fundamentals;
- navigation plotting;
- structured reports and information handoff;
- teamwork practical.

Gameplay goals:

- participate in a multi-station exercise;
- pass data to another department;
- understand system dependencies;
- operate under a supervising instructor.

### Trimester 2 — People, Risk and the Federation

Common/applied:

- interspecies protocol;
- first-contact principles;
- Prime Directive/regulations;
- diplomacy fundamentals;
- medical/triage basics;
- security fundamentals;
- survival;
- away-team fundamentals;
- field-study / EVA hooks where era/profile supports them.

Gameplay goals:

- recognize legal/ethical constraints;
- operate with incomplete information;
- work with cultures/species without stereotype shortcuts;
- understand away-team risk and authority.

### Trimester 3 — Division Decision Window

Common:

- integrated simulations;
- leadership foundations;
- advanced reporting;
- professional self-assessment;
- instructor guidance;
- branch exposure practicals.

Specialization:

- candidate specialization modules begin;
- the player selects specialization by the end of this trimester;
- instructors may recommend but never choose;
- formal specialization begins in 2nd Class / Trimester 1.

Gameplay goals:

- demonstrate enough exposure to make an informed branch choice;
- create an initial academic strengths/weaknesses profile.

## Cadet 2nd Class — Specialization and Integration

The player now spends substantially more time in the chosen professional path.

### Trimester 1 — Specialization Core I

Each branch begins its real professional curriculum.

Examples:

- Command: leadership, regulations, command decision fundamentals;
- Flight/Navigation: helm, astrogation, maneuvering;
- Operations: ship systems coordination and resource management;
- Engineering: power, propulsion, maintenance, damage control;
- Tactical/Security: threat analysis, weapons/defense, security procedure;
- Science/Sensors: sensor operations, scientific observation, analysis workflow;
- Medical: diagnostics, emergency medicine, xenomedicine foundations.

Cross-training/elective slots remain available.

### Trimester 2 — Specialization Core II

Focus shifts toward:

- more complex procedures;
- multi-system interaction;
- supervised independent work;
- error recovery;
- cross-department coordination.

### Trimester 3 — Specialization Core III

Focus shifts toward:

- sustained practical work;
- difficult scenarios;
- uncertainty;
- workload;
- responsibility;
- formal intermediate qualification.

## Cadet 1st Class — Service Preparation

### Trimester 1 — Advanced Specialization

- advanced branch material;
- class/system familiarization concepts;
- leadership appropriate to branch;
- operational judgement;
- advanced simulations;
- supervised service-like watches.

### Trimester 2 — Integrated Starship Operations

All branches operate together.

Focus:

- bridge/team integration;
- engineering/medical/security response;
- orders and reports;
- interconsole handoffs;
- mission progression;
- extended simulation;
- duty continuity;
- debrief.

The experience should increasingly resemble real Starfleet service rather than school exercises.

### Trimester 3 — Capstone and Commissioning

Includes:

- final branch evaluations;
- service-readiness evaluation;
- capstone simulation window;
- Kobayashi Maru;
- training cruise / active-unit exposure where applicable;
- assignment interviews/preferences;
- graduation requirements;
- commission preparation.

## Branch commitment

The normal selection point is:

```text
END OF 3rd Class — Trimester 3
```

Formal specialization begins in 2nd Class / Trimester 1.

Changing specialization later remains possible with realistic catch-up.

## Sensors as a full professional course

The already-designed Sensors functional tree can become a three-trimester specialization course.

Example:

### Sensor Operations I
- Status;
- Scans;
- Search / Localization.

### Sensor Operations II
- Contacts;
- Tracking;
- Sensor Readout;
- Interference / Compensation.

### Sensor Operations III
- Configuration;
- Results;
- Diagnostics;
- Integrated Operations.

Each unit uses:

```text
THEORY
→ INSTRUCTOR
→ REAL CONSOLE PRACTICE
→ CONTINUOUS EVALUATION
```

## Scheduling principle

The exact weekly timetable is runtime/content data.

The curriculum defines what must be learned and its academic order, not a single immutable Monday timetable.

## Era handling

The curriculum architecture stays stable across playable eras.

Technology examples, interfaces, equipment, historical context and some named courses/practicals may vary by era.

## Web / external study compatibility

Curriculum data should be consumable by the Starfleet Academy study website.

A student profile may track:

- completed theory;
- practice attempts;
- exam/practice results;
- current course;
- current trimester;
- optional external-study progress.

The external website must not silently grant in-game qualifications unless the game explicitly imports/validates an approved result.


## Unit deployment v1.0

The complete four-year unit design now lives under `curriculum/`.

Deployment summary:

- 60 main course/process definitions;
- 7 professional branch curricula;
- 35 branch stages;
- 501 designed units;
- single-source rule for game, web, manuals, PDF and assessments.

Control files:

- `curriculum/curriculum_manifest_v1_0.json`
- `curriculum/CURRICULUM_DEPLOYMENT_v1_0.md`
- `curriculum/VALIDATION_v1_0.md`

The next content layer is study-material production, not further year-architecture design.
