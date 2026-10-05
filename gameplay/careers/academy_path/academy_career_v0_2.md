# Starfleet Academy + Career Design v0.2

Status: **FOUNDATION IN PROGRESS**

This document extends the existing Academy baseline into the intended full RPG experience.

## Career arc

```text
ACCESS / ADMISSION
      ↓
4th YEAR
      ↓
3rd YEAR
      ↓
2nd YEAR
      ↓
1st YEAR
      ↓
GRADUATION
      ↓
ENSIGN
      ↓
LT. JG
      ↓
LIEUTENANT
      ↓
SENIOR OFFICER / MENTOR / COMMAND PATH
```

The displayed year naming is intentionally Academy-flavoured: the cadet enters **4th Year** and progresses toward **1st Year** before graduation.

Internal sequence indexes may remain ascending for implementation clarity.

## Academic structure

Each year is divided into three trimesters.

Each subject can contain units built from real game systems.

```text
YEAR
└── TRIMESTER
    └── SUBJECT
        └── UNIT
            ├── THEORY
            ├── CLASS
            ├── PRACTICE
            └── EVALUATION
```

### Theory
Manuals, PADDs, regulations, reference material and self-study.

### Class
Persistent instructor NPC teaches, demonstrates, answers free-form questions and can reformulate explanations.

### Practice
The cadet uses the **same gameplay backend** later used in active service.

### Evaluation
Evidence-based assessment from actual actions/events. AI may explain the result but does not invent grades.

## Curriculum philosophy

Academy study must teach what the player will genuinely use.

Examples include:

- ranks and insignia;
- chain of command;
- shipboard roles;
- orders and reporting;
- duty watches;
- bridge operations;
- galactic map / astrography;
- ship and station types;
- warp fundamentals;
- transporters;
- replicators;
- holodecks;
- ship weapons;
- personal equipment;
- tricorders;
- Federation cultures;
- sensors;
- navigation;
- operations;
- engineering;
- tactical/security;
- medicine/science;
- emergency procedures.

It must not become a passive Star Trek wiki.

## Specialization

The player chooses the final professional direction.

Instructors may recommend. They do not choose for the player.

Broad playable paths already supported by the current specialization model include:

- Command;
- Flight Control / Navigation;
- Operations;
- Engineering;
- Security / Tactical;
- Science;
- specialist science fields;
- Medical.

Cadets may begin undecided, explore divisions, cross-train and change direction with realistic catch-up requirements.

## Academic record

The Academy Record is persistent and evidence-based.

It may contain:

- course completion;
- practical results;
- exam results;
- instructor observations;
- strengths;
- weaknesses;
- disciplinary incidents;
- commendations;
- simulator performance;
- qualifications;
- recommendations;
- specialization history;
- field-training performance;
- capstone/final practical results.

The record is not a single score.

## Instructor model

Instructors are persistent characters with:

- rank and role;
- subject expertise;
- personality;
- teaching style;
- strictness;
- mentoring tendency;
- memory of the cadet;
- knowledge and authority limits.

AI supports natural explanation and dialogue. Authoritative systems decide schedules, grades, qualifications and sanctions.

## Real-system training

Wrong-but-valid actions normally execute.

Example:

- assignment: passive scan of sector 14;
- cadet correctly configures a passive subspace scan;
- cadet scans sector 16;
- scan executes;
- instructor later evaluates: procedure correct, target wrong.

This preserves system realism and creates meaningful evidence.

## Kobayashi Maru

The Kobayashi Maru is a late-Academy capstone experience.

It is not a puzzle with one correct solution.

It evaluates conduct under a no-win or irreducibly adverse situation:

- judgment;
- leadership;
- communication;
- responsibility;
- ethical reasoning;
- risk handling;
- consistency;
- team use;
- response to uncertainty.

Command candidates may command the full scenario.

Other branches experience the event from their real station and receive branch-specific evaluation.

The exact trimester placement remains configurable until the complete master curriculum is scheduled.

## Graduation

Graduation means:

> **ready to begin professional service**

not:

> **fully mastered officer**

The cadet becomes an Ensign and enters supervised operational learning.

## Post-Academy principle

Academy teaches Starfleet standards and controlled practice.

Active service teaches:

- this ship;
- this crew;
- real consequences;
- class-specific systems;
- operational tempo;
- judgment under live conditions.

## Progression philosophy

```text
ENSIGN
→ supervised real-world consolidation

LT. JG
→ increasing autonomy and advanced qualifications

LIEUTENANT
→ consolidated professional capability and early leadership

SENIOR OFFICER
→ supervision, department responsibility, mentorship and command pathways
```

There is no requirement for a generic visible XP level.

Growth is represented by qualifications, evidence, responsibility, trust and service history.

## Integration

Consumes:

- Operational Event Log;
- service record;
- timekeeping;
- character memory;
- relationship/social systems;
- habits/wellbeing;
- real console operations.

Produces:

- academic evaluations;
- qualifications;
- recommendations;
- career evidence;
- relationships with instructors/classmates;
- first-assignment candidates.
