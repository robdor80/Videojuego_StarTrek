# Records and Logs

## Status

**FOUNDATION v0.1 — REQUIRED STAR TREK SYSTEM**

Logs are an intrinsic part of the Star Trek experience and are not optional flavour text.

This subsystem models authored institutional and personal records across Academy, ships, stations and a character's career.

## Core distinction

> **The Operational Event Log preserves what happened. A log entry preserves what a person or institution chose to record about it.**

This distinction is mandatory.

### Operational Event Log

Location: `gameplay/ship_operations/operational_event_log/`

- authoritative operational facts;
- append-only;
- objective references to actions/results/events;
- not a diary;
- does not judge.

### Records and Logs

This directory:

- Captain's Log;
- Personal Log;
- Department Log;
- Duty Log;
- Medical/Security/other restricted institutional logs;
- player and NPC-authored entries;
- privacy/access;
- voice/transcription;
- assisted drafting;
- search/retrieval.

## Log families

### Captain's Log

Official command-level narrative record.

Normally authored or approved by the commanding officer. It may summarize mission status, decisions, discoveries, risks and intent.

### Personal Log

Private subjective record belonging to an individual character.

A personal log may contain opinions, fears, beliefs or interpretations that are not objectively true.

### Department Log

Professional record for a department such as Engineering, Science, Medical or Security.

### Duty Log

Operational continuity record associated with a watch, post or duty responsibility.

### Restricted institutional logs

Medical, Security, Intelligence or classified records use additional domain-specific access controls.

## Persistence

Logs follow the owning person/institution, not a specific UI or console.

A player's Personal Log remains part of that character's career after transfers between ships or stations.

## Computer integration

The Starship Computer is a primary access channel but does not own the records.

Examples:

- "Computer, open my personal log."
- "Computer, begin captain's log."
- "Computer, find science logs mentioning gravimetric distortions."
- "Computer, prepare a draft summary of the last eight hours."

The computer must authenticate the requester and enforce access rules.

## AI boundary

AI may:

- transcribe spoken entries;
- structure a draft;
- summarize authorized factual sources;
- express an NPC's subjective entry using that NPC's authorized knowledge, memories and personality.

AI may not:

- invent authoritative events;
- expose information the author could not know;
- publish a draft without the required approval;
- bypass privacy/access controls.

## NPC logs

NPCs may create their own personal or professional logs.

Their entries are not automatically known to the player.

The existence of a private log does not grant player access.

## Voice

Entries may preserve:

- original audio;
- transcription;
- approved edited text;
- metadata and links to relevant events.

Audio is presentation/media; the structured log entry remains the durable gameplay record.

## Search and investigation

Authorized logs can become gameplay evidence.

The computer may search across permitted records and operational data, preserving source/provenance and access boundaries.

## Required files

- `log_entry_contract.json`
- `access_and_privacy_rules.json`
- `assisted_drafting_rules.json`
