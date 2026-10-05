# Starship Computer

Status: **FOUNDATION v0.1 — IN PROGRESS**

## Purpose

The Starship Computer is a ship-wide service, not merely one console screen.

It can be accessed through appropriate:

- bridge stations;
- wall terminals;
- engineering terminals;
- quarters;
- PADD interfaces;
- combadge/voice interfaces;
- sickbay/security systems;
- dedicated Computer console surfaces.

## Character

The default Starfleet computer experience is:

- neutral;
- concise;
- professional;
- literal when appropriate;
- non-chatty;
- unemotional in normal operation;
- precise about uncertainty;
- explicit about access denial;
- willing to request clarification;
- consistent with Starfleet terminology.

It must not behave like a friendly general-purpose chatbot wearing an LCARS skin.

## Core authority rule

> **The computer may query, calculate, interpret and request actions. Authoritative game systems decide what is true and what actions actually occur.**

The language layer does not directly mutate world state.

## Query examples

Deterministic/simple queries may include:

- current time;
- duty roster;
- known crew location;
- current course/ETA;
- ship status;
- known sensor results;
- maintenance history;
- authorized log search;
- environmental status.

Complex queries may include:

- correlate sensor and navigation records;
- summarize the last six hours of relevant events;
- compare current readings against historical records;
- explain a technical pattern from authorized sources.

## Action examples

The player may request:

- open/close an authorized door;
- transfer data;
- adjust environmental settings;
- reserve a holodeck;
- initiate an allowed diagnostic;
- contact a person/department;
- execute a permitted ship-system command.

Every consequential action is validated for:

- requester identity;
- authority;
- location/context;
- system capability;
- current state;
- safety/interlocks;
- any required secondary authorization.

## No invented reality

If the player asks:

> "Are there Romulan ships in the system?"

the answer must derive from what the ship currently knows.

"None detected" is not equivalent to "none exist."

The computer must preserve observation/knowledge limits.

## Access

Speaking to the computer does not grant universal authority.

Crewmembers may access ordinary services while sensitive functions require role/rank/clearance/department-specific authorization.

Some operations may require explicit command codes or multi-person authorization.

## Interaction

Default natural interaction may use:

- push-to-talk Computer key;
- optional wake word;
- typed terminal/PADD input.

A permanent always-listening microphone should be optional rather than required.

## AI routing

Do not use a large language model for every request.

Preferred route:

```text
request
  ↓
known deterministic intent?
  ├── yes → deterministic query/action
  └── no / complex language
          ↓
       AI interpretation
          ↓
       structured candidate
          ↓
       authority validation
```

Complex analysis may use a stronger reasoning route after data retrieval/calculation.

## Provider independence

The game uses logical routes rather than hard-coding a branded model:

- `COMPUTER_FAST`;
- `COMPUTER_REASONING`.

Current/future Gemini, OpenAI, Mistral or other providers can be configured behind those routes.

## Records and logs

The Computer is the primary conversational gateway for:

- Personal Logs;
- Captain's Logs;
- Department Logs;
- Duty Logs;
- authorized historical search.

The records themselves live under `gameplay/records_and_logs/` and are not owned by this subsystem.

## Operational history

The Computer may query:

- Operational Event Log;
- sensor results;
- navigation records;
- diagnostics;
- maintenance;
- service records;
- authorized logs;
- other structured ship data.

It may correlate these sources without inventing missing events.

## Computer profiles

Different civilizations and ship generations may have different:

- capabilities;
- interfaces;
- voice/personality profile;
- access model;
- language behavior;
- database scope;
- analysis capability.

Starfleet ships share a common philosophy but a Galaxy-class computer need not have identical capability to every earlier vessel.

## CoreRPG boundary

Generic query/action validation and authoritative state remain CoreRPG concerns where reusable.

Star Trek defines the ship-computer personality, Starfleet access semantics, LCARS-facing behavior and universe-specific query/action vocabulary.
