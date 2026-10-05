# Timekeeping

## Status

**FOUNDATION v0.1 — FIXED**

This subsystem defines how exact campaign time, ship time and player-facing stardates coexist.

## Three simultaneous views of time

1. **Authoritative campaign time** — exact runtime time used by simulation.
2. **Stardate** — Star Trek-facing presentation derived from authoritative time.
3. **Human-readable reference** — accessibility aid for the real player.

Universal project rate:

```text
1 campaign year = 1,000 stardate units
```

All playable eras use the same rate.

## Ship time

Ships use normal 24-hour local ship time for daily life and duty scheduling.

## Runtime rule

No gameplay system should use a formatted stardate as its only temporal source.

Store exact campaign timestamps and derive:

- stardate;
- ship time;
- Gregorian/human reference;
- elapsed-time labels.

## Related systems

Timekeeping is consumed by:

- Operational Event Log;
- Records and Logs;
- Academy schedules;
- duty watches;
- NPC routines;
- travel;
- procedural simulation;
- career/service records;
- Starship Computer queries.
