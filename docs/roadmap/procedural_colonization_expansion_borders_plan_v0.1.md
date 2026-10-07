# Procedural Colonization, Expansion & Borders — Plan v0.1

**Status:** COMPLETE  
**Parent sequence:** `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`

## Goal

Define how an already-existing spacefaring civilization expands without spawning colonies, territory or borders for player convenience.

```text
need / motive / capacity
→ known reachable candidates
→ rights + Prime Directive + biosphere checks
→ target evaluation
→ expedition / population movement
→ founding
→ survival / dependency / growth
→ administration / autonomy
→ claim + effective control
→ political-space overlay / border consequences
```

## Packages

| Package | Scope | Status |
|---|---|---|
| CX001 | Authority, ownership and block boundaries | COMPLETE |
| CX002 | Expansion drivers and prerequisites | COMPLETE |
| CX003 | Candidate-system/world selection | COMPLETE |
| CX004 | Indigenous life / Prime Directive safeguards | COMPLETE |
| CX005 | Expedition authorization and founding | COMPLETE |
| CX006 | Colony lifecycle and maturity | COMPLETE |
| CX007 | Population transfer and residency | COMPLETE |
| CX008 | Logistics, viability and dependency | COMPLETE |
| CX009 | Claim / control / jurisdiction / sovereignty separation | COMPLETE |
| CX010 | Border and political-overlay derivation | COMPLETE |
| CX011 | Overlapping claims and expansion encounters | COMPLETE |
| CX012 | Colonial governance, autonomy and independence | COMPLETE |
| CX013 | Failure, evacuation and abandonment | COMPLETE |
| CX014 | Off-screen / LOD expansion persistence | COMPLETE |
| CX015 | Reference simulator, fixtures and executable tests | COMPLETE |
| CX016 | Cross-domain integration and closure | COMPLETE |

## Hard rules

1. A habitable world is not automatically a colony candidate.
2. Colonization requires motive, technological/logistical capacity, route access, population and lawful/recognized authority context.
3. Player arrival or player need can never create a colony.
4. Colonists move from existing populations; they are not duplicated.
5. Pre-warp/protected sapient populations cannot be colonized through this system.
6. Contacted sovereign populations require an explicit right, invitation, treaty or joint-colony basis.
7. Terraforming is never a free eligibility override; an actual capability/project and environmental/legal context must exist.
8. Colony existence does not automatically create sovereignty over a star system.
9. Claim, presence, effective control, jurisdiction, sovereignty and external recognition are separate facts.
10. Political borders are not Voronoi spheres or automatic colored bubbles around colonies.
11. Unclaimed gaps, corridors, enclaves, shared areas and isolated systems are valid.
12. Overlapping claims create a dispute state, not automatic combat or war.
13. Neutral/demilitarized zones require an explicit agreement/rule; they are not generated merely because two borders meet.
14. A colony may fail, shrink, evacuate or be abandoned.
15. Abandonment removes effective control unless another persistent presence actually remains; historical claims may persist separately.
16. Autonomy pressure does not automatically create independence.
17. Recognized colonial independence creates/changes polity authority; it does not automatically create a new species/culture/civilization.
18. A true civilization split must use the Block 1 lineage rules.
19. Off-screen colonies obey the same causal facts at lower simulation fidelity.
20. World Truth and observer knowledge remain separate.

## Sequential boundary

Block 2 does **not** implement:
- war/front/battle resolution — Block 3;
- detailed markets, production chains or interstellar trade simulation — Block 4;
- pre-campaign historical synthesis — Block 5;
- invention/research/technology breakthroughs — Block 6;
- anomaly/archaeology generation — Block 7;
- crisis generators — Block 8;
- mission generation — Block 9;
- galaxy-wide scheduler/prioritization — Block 10.

It may emit explicit candidate/dispute/dependency refs for those later blocks.

## Runtime boundary

CoreRPG 4.5+ owns authoritative World State mutation, clocks/scheduling, generic actions/events, persistence and LOD execution. The Python tool is a deterministic Star Trek-side reference implementation.
