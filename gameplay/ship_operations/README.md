# Ship Operations

This directory contains gameplay-facing contracts and rules for operating Starfleet ships.

## Major subsystems

- `consoles/` — reusable functional console families.
- `sensor_resolution/` — deterministic observer-relative sensor detection.
- `ship_memory/` — persistent ship knowledge such as contact dossiers.
- `interconsole/` — structured data handoffs between functional consoles.
- `operational_event_log/` — append-only operational history used as evidence by debrief, evaluation, memory and career systems.
- `ship_computer/` — ship-wide Computer service: queries, access control, validated action requests and AI routing.

## Architecture rule

Functional gameplay logic, persistent knowledge, operational history, ship-wide services and presentation are separate concerns.

A console is an interface; it is not automatically the underlying ship-wide service.

The Star Trek repository defines universe/gameplay contracts. Generic authoritative runtime capability belongs in `CoreRPG`; do not duplicate the engine here.
