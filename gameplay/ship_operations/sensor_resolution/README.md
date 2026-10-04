# Sensor Detection Resolution v0.1

This directory owns the simulation rules that convert an authoritative materialized world plus a structured sensor request into the information an observer is allowed to discover.

It is deliberately separate from `gameplay/ship_operations/consoles/sensors/`:

- **sensor resolution** decides what can be detected;
- **Sensors console** decides how the player configures and launches the operation;
- **UI** decides how controls and results are presented.

## Core rule

**World truth is authoritative; sensor output is derived knowledge.**

The resolver never creates anomalies, ships, planets or signatures. It reads entities already present in world state.

## Inputs

A scan request supplies observer/operator, origin position, sector/system scope, range mode, active/passive mode, requested resolution, filters, optional priority, duration and normalized sensor capability/power/integrity.

## Detection states

- `not_detected`: no player-visible contact.
- `trace_detected`: a signal exists, with very little detail.
- `detected_unclassified`: contact plus approximate position.
- `partially_resolved`: entity type and ordinary observable properties.
- `resolved`: classification plus any hidden properties whose resolution/filter requirements are met.

## No ground-truth leakage

Player-facing detection objects use a stable observer-relative `contact_id`. They do not expose authoritative `entity_id` values or unrevealed hidden properties.

## Scope of v0.1

The numerical model is a gameplay abstraction, not a claim that Star Trek canon defines these exact sensor equations. It is deterministic, tunable and explainable. Later class/era-specific sensor profiles can change capability inputs without replacing this pipeline.
