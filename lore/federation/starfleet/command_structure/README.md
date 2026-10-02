# Starfleet Command Structure

## Foundational rule

Starfleet hierarchy must model four independent concepts:

```text
RANK
DEPARTMENT
POSITION
ASSIGNMENT
```

Example:

```text
Rank: Lieutenant Commander
Department: Engineering
Position: Chief Engineer
Assignment: USS Example
```

## Rank authority

Higher rank normally implies seniority, but operational command also depends on:
- assigned position,
- chain of command,
- watch/duty status,
- specific orders,
- acting appointments,
- emergency succession.

Therefore a higher-ranked officer does not automatically take over every technical or departmental decision.

## Commanding officer

`Commanding Officer` is a **position**.

`Captain` is a **rank**.

They often coincide, but they are not the same data field.

A ship/station can therefore have:
- a commanding officer with Captain rank,
- a commanding officer of another permitted rank,
- an acting commanding officer temporarily exercising command authority.

## First officer / executive officer

The First Officer / Executive Officer is likewise a position, usually held by a senior commissioned officer. It is not a rank.

## Senior staff

Senior staff is assembled from positions such as:
- Commanding Officer
- First Officer / Executive Officer
- Operations
- Helm / Flight Control
- Tactical / Security
- Chief Engineer
- Science Officer
- Chief Medical Officer

Exact composition and departmental mapping may vary by era and vessel/station.

## Next research

This file establishes the data model only. Detailed:
- command succession,
- departmental authority,
- watch structure,
- Starfleet Command hierarchy,
- ship vs station differences

will be filled in during the current institutional block.
