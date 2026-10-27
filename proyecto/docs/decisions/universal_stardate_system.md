# Universal Stardate System

Status: **PROJECT DECISION — FIXED**

## Decision

All playable Star Trek eras use the same project stardate progression rule:

> **1,000 stardate units = 1 campaign year**

This applies to Pike, Kirk, TNG, DS9 and Voyager-era play.

The project intentionally does not reproduce the inconsistent stardate formulas used across different Star Trek productions. Immersion, continuity and usability take priority.

## Authoritative time

Stardate is not the authoritative simulation clock.

The runtime stores exact campaign time using a normal calendar timestamp, for example:

```text
2371-03-18T06:40:00
```

That exact time drives watches, travel, sleep, Academy schedules, NPC routines, mission deadlines, aging, event ordering, procedural simulation and logs.

## Universal rate

All eras use:

```text
1 campaign year = 1,000 stardate units
```

No era-specific progression formula is used.

## Presentation

Normal player-facing presentation should prioritize the stardate while preserving a smaller human-readable reference:

```text
STARDATE XXXXX.X
SHIP TIME 06:40
(18 March 2371 · 06:40)
```

Ship time remains normal 24-hour time for daily life, duty watches and appointments.

## Storage rule

Gameplay systems store the exact campaign timestamp and derive:

- stardate;
- ship time;
- human-readable campaign date;
- elapsed-time labels.

A formatted stardate is never the sole source of temporal truth.

## Logs

Captain's Logs, Personal Logs, Department Logs and Duty Logs retain the exact campaign timestamp and may display the stardate plus the human-readable reference.

## Design rule

> **The universe runs on exact campaign time. Starfleet presents stardates. Roberto may also see a human-readable reference underneath.**
