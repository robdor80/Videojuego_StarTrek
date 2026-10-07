# Procedural Facility Generation fixtures

## Positive fixture — relay outpost, 2372

A persistent subspace-communications gap has existed long enough to justify fixed infrastructure.

The generator resolves:

```text
sustained communications need
→ alternatives insufficient
→ micro-outpost is enough
→ Starfleet / 2372
→ reusable Relay Station 47-type
→ construction project
→ persistent facility identity
→ 15-month construction
→ operational after 24 elapsed months
→ 2 Starfleet officers
→ alternating active/on-call coverage
→ communications + smallcraft support only
→ very light traffic
```

This station is **not** canonical Relay Station 47. It is a new individual facility using the same reusable design family.

## Negative fixture — player repair convenience

The second fixture intentionally gives enormous numeric demand values but uses:

`origin_trigger = player_needs_repairs`

The generator must still return:

`NO_PERMANENT_FACILITY`

This is the anti-"space gas station" invariant. The correct world response is an existing facility, mobile support, rescue/tow/tender, temporary infrastructure, diversion, delay, or no convenient solution.
