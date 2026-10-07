# Procedural Civilization Evolution & Galactic Interaction — Plan v0.1

**Status:** COMPLETE  
**Parent sequence:** `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`

## Goal

Make an already-existing civilization remain historically alive after generation and First Contact without creating major events merely because the player is present.

```text
persistent civilization state
→ elapsed time + explicit causal events
→ demographic/institutional/economic/social evolution
→ relationship evolution
→ append-only history
→ observer knowledge later learns some subset
→ persistent next state
```

## Packages

| Package | Scope | Status |
|---|---|---|
| CE001 | Authority, ownership and boundaries | COMPLETE |
| CE002 | Civilization evolution state vector | COMPLETE |
| CE003 | Demographic evolution | COMPLETE |
| CE004 | Government, legitimacy and succession transitions | COMPLETE |
| CE005 | Cohesion, instability and fragmentation | COMPLETE |
| CE006 | Internal economic resilience | COMPLETE |
| CE007 | Capability maturation without automatic breakthrough | COMPLETE |
| CE008 | Diplomatic / inter-polity relationship evolution | COMPLETE |
| CE009 | First Contact → continuing relationship continuity | COMPLETE |
| CE010 | Civilization continuity, split/merge/extinction semantics | COMPLETE |
| CE011 | Off-screen / LOD catch-up | COMPLETE |
| CE012 | Evolution event and consequence contract | COMPLETE |
| CE013 | Deterministic reference simulator | COMPLETE |
| CE014 | Fixtures, tests and cross-domain invariants | COMPLETE |
| CE015 | Repository integration / status closure | COMPLETE |

## Hard rules

1. A civilization does not freeze because the player leaves.
2. Player proximity never creates demographic, political or diplomatic change.
3. Major transitions require causes and append explicit event history.
4. Government identity may change while `civilization_id` persists.
5. Culture/species never predetermine stability, aggression, legitimacy or political outcome.
6. Population is conserved across movement; Block 1 cannot duplicate people.
7. High tension does not automatically become war; Block 3 owns war resolution.
8. Capability can mature, but Block 1 cannot invent a technological breakthrough or advance `technology_band`; Block 6 owns that.
9. A partial-polity relationship cannot silently become planet-wide.
10. First Contact does not decay into treaty/trade/alliance automatically over time.
11. Extinction requires an explicit causal record; a zero-population inconsistency is not silently rewritten as history.
12. Splits/mergers require lineage; old identities/history are never erased.
13. Off-screen aggregation must reproduce a causally compatible state when the civilization is materialized again.
14. World Truth and observer knowledge remain separate.
15. AI may explain/propose, but cannot invent hidden transitions or mutate authoritative state.

## v0.1 scope boundary

This block deepens the evolution rules for civilizations already present in authoritative World State. It does not implement Blocks 2–10. Where those systems are needed, Block 1 emits explicit candidates, pressure states or dependency refs.

## Runtime boundary

CoreRPG 4.5+ remains the owner of authoritative time scheduling, generic events/actions, save/load, state mutation and LOD execution. The Python simulator in this repository is a deterministic reference implementation used to validate Star Trek-side contracts.
