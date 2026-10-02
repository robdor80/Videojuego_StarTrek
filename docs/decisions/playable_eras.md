# Playable Eras

Status: **APPROVED**

This document fixes the playable-era scope of the project.

## Playable eras

### 1. Pike / Strange New Worlds

Primary screen scope:
- `Star Trek: Strange New Worlds`

Anchor:
- Christopher Pike
- USS Enterprise NCC-1701

### 2. Kirk / TOS + films

Primary screen scope:
- `Star Trek: The Original Series`
- films centred on Kirk and the original crew

Anchor:
- James T. Kirk
- USS Enterprise NCC-1701
- USS Enterprise NCC-1701-A when chronologically applicable

### 3. TNG + DS9 + Voyager

One shared late-24th-century playable period with three major branches:

- **TNG** → Jean-Luc Picard
- **DS9** → Benjamin Sisko
- **Voyager** → Kathryn Janeway

These are not separate universes. Characters, ships, stations and events coexist only when the selected campaign date makes them temporally valid.

## Explicitly outside playable scope

The following television series are excluded by project decision:

- `Star Trek: Picard`
- `Star Trek: Discovery`
- `Star Trek: Enterprise`

Jean-Luc Picard remains fully in scope as the TNG-era character/captain.

## Critical campaign rule

The screen material defines the **starting historical state**, not a mandatory storyline.

Selecting:
- Pike does not mean replaying Strange New Worlds episodes;
- Kirk does not mean replaying TOS or the films;
- TNG does not mean replaying Picard's television adventures;
- DS9 does not mean replaying Sisko's television story;
- Voyager does not mean replaying Voyager season by season or inevitably returning to the Alpha Quadrant in the canonical way.

Once the campaign begins, its own world state and history become authoritative.

See: `docs/decisions/campaign_continuity.md`.

## Architecture rule

There are exactly three playable era profiles:

```text
pike
kirk
tng_ds9_voyager
```

An era profile is a temporal filter over one Star Trek knowledge base. It is not a duplicate universe.

## Change control

Changing this list is a project design decision and requires explicit approval from Roberto.
