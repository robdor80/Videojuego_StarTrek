# Playable Eras

Status: **APPROVED**

This document fixes the playable-era scope of the project.

## Playable eras

### 1. Pike / Strange New Worlds

Primary screen scope:
- `Star Trek: Strange New Worlds`
- related on-screen material only when necessary to understand this era

Anchor:
- Christopher Pike
- USS Enterprise NCC-1701

### 2. Kirk / TOS + films

Primary screen scope:
- `Star Trek: The Original Series`
- films centred on Kirk and the original crew

Anchor:
- James T. Kirk
- USS Enterprise NCC-1701 and, when chronologically applicable, NCC-1701-A

Transitional/crossover material is placed where chronology requires it; it does not create a fourth playable era.

### 3. TNG + DS9 + Voyager

One shared broad playable period containing three major contemporary branches:

- **TNG** → Jean-Luc Picard
- **DS9** → Benjamin Sisko
- **Voyager** → Kathryn Janeway

These are not three separate universes. Their events, characters, ships and institutions are placed on one shared late-24th-century chronology and become available according to exact campaign date.

## Explicitly outside playable scope

The following television series are excluded by project decision:

- `Star Trek: Picard`
- `Star Trek: Discovery`
- `Star Trek: Enterprise`

They do not receive playable-era profiles and are not part of the planned content-filling queue.

Jean-Luc Picard remains fully in scope as the TNG-era character/captain. Excluding the series `Picard` does **not** exclude the character.

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
