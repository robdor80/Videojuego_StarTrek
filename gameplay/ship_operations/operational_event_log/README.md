# Operational Event Log

## Status

**DESIGN CONTRACT v0.1 — FIXED FOR THE CURRENT SHIP-CONSOLE VERTICAL SLICE**

## Purpose

The Operational Event Log records what actually happened during ship operations in a structured, append-only form.

It exists so later systems can reason from evidence instead of reconstructing history from dialogue or AI memory.

Typical consumers include:

- duty and mission debriefs;
- Academy evaluation;
- mentor/supervisor feedback;
- service records;
- professional reputation;
- NPC knowledge and memory;
- investigations;
- command review;
- future career and recommendation systems.

## Core rule

> **The log records events. It does not judge them.**

An event may say that an officer received an order, began a scan, created a result and made a report.

Whether that performance was excellent, late, negligent, courageous or inappropriate belongs to an evaluation system.

## Domain boundary

The Operational Event Log is a cross-console ship-operation subsystem.

It is deliberately separate from:

- `consoles/` — functional behavior of each console;
- `sensor_resolution/` — what sensors can actually detect;
- `ship_memory/` — persistent ship knowledge such as contact dossiers;
- `interconsole/` — structured transfer of known data between consoles;
- UI — presentation of logs, reports or history.

## Internal event stream vs visible operational log

The runtime may ultimately keep a richer authoritative event stream than any character can see.

This contract therefore separates:

1. **authoritative operational event** — the immutable fact that an operational event occurred;
2. **visibility / knowledge projection** — who can know or retrieve that event and through what channel;
3. **derived records** — service record, Academy evaluation, NPC memory, mission summary, investigation file, etc.

Creating an event does **not** grant universal knowledge of it.

## Append-only history

Recorded events are not silently edited.

If an earlier report was wrong, a later correction is another event.

If an order is cancelled, cancellation is another event.

If knowledge changes, later events or records supersede current interpretation without rewriting history.

## Identity and references

Events should reference stable IDs rather than duplicate large payloads.

Examples:

- `order_id`
- `operation_id`
- `result_id`
- `contact_id`
- `package_id`
- `character_id`
- `station_id`
- `ship_id`
- `location_id`

A sensor result remains the authoritative sensor-data snapshot. The event log only records that it was created, reviewed, transmitted or acted upon.

## Minimal vertical-slice flow

```text
ORDER_ISSUED
    ↓
ORDER_ACKNOWLEDGED
    ↓
ACTION_STARTED
    ↓
ACTION_EXECUTED
    ↓
RESULT_CREATED
    ↓
REPORT_MADE
    ↓
DATA_SENT
    ↓
ACTION_COMPLETED
```

Not every operation requires every event.

## Evaluation boundary

Examples of facts the log may contain:

- order issued at 10:42:11;
- scan started at 10:42:18;
- result created at 10:42:29;
- report made at 10:42:41;
- operator used passive mode;
- operator targeted sector 14.

Examples the log must **not** decide:

- “excellent response time”;
- “poor judgement”;
- “cadet deserves 8.7/10”;
- “captain now trusts this officer”.

Those are derived by later systems from events plus applicable rules/context.

## AI boundary

AI may:

- verbalize events;
- summarize an authorized subset;
- explain them during debrief;
- use them as evidence when given appropriate context.

AI may not:

- invent events that did not occur;
- mutate recorded history;
- make hidden world truth visible;
- convert an event into universal NPC knowledge.

## CoreRPG boundary

This repository defines the Star Trek gameplay contract and expected semantics.

The generic runtime implementation belongs in CoreRPG once its world-state/action/event capabilities are ready.

Do not implement a duplicate authoritative runtime engine here.

## Files

- `operational_event_contract.json` — event record contract.
- `event_type_catalog.json` — fixed v0.1 event vocabulary for the vertical slice.
- `visibility_projection_rules.json` — knowledge/access rules.
- `sensors_vertical_slice_example.json` — worked example from order to report.
