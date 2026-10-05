# Ship Operations

This directory contains gameplay-facing contracts and rules for operating Starfleet ships.

## Major subsystems

- `consoles/` — reusable functional console families.
- `sensor_resolution/` — deterministic observer-relative sensor detection.
- `ship_memory/` — persistent ship knowledge such as contact dossiers.
- `interconsole/` — structured data handoffs between functional consoles.
- `operational_event_log/` — append-only operational history used as evidence by debrief, evaluation, memory and career systems.

## Architecture rule

Functional gameplay logic, persistent knowledge, operational history and presentation are separate concerns.

The Star Trek repository defines universe/gameplay contracts. Generic authoritative runtime capability belongs in `CoreRPG`; do not duplicate the engine here.
