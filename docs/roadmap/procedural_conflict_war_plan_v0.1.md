# Procedural Conflict & War — Plan v0.1

**Status:** COMPLETE  
**Parent sequence:** `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`

## Goal

Allow political crises, armed incidents and wars to emerge from persistent World State without turning every dispute into combat or spawning forces because the player needs action.

```text
grievance / threat / dispute / obligation
+ faction/cultural doctrine
+ government + leader + era
+ military/logistical reality
+ legal authority
→ response / escalation / de-escalation
→ objectives
→ committed real forces
→ operations / losses / control changes
→ ceasefire / armistice / peace
→ persistent consequences
```

## Packages

| Package | Scope | Status |
|---|---|---|
| CW001 | Authority, ownership and sequential boundaries | COMPLETE |
| CW002 | Conflict/crisis state model | COMPLETE |
| CW003 | Causes, grievances and casus-belli context | COMPLETE |
| CW004 | Cultural-political conflict behaviour composition | COMPLETE |
| CW005 | Escalation and de-escalation | COMPLETE |
| CW006 | War authority and rules of engagement | COMPLETE |
| CW007 | Political/military war objectives | COMPLETE |
| CW008 | Force availability, mobilization and logistics | COMPLETE |
| CW009 | Fronts, theaters and strategic operations | COMPLETE |
| CW010 | Strategic-LOD operation resolution | COMPLETE |
| CW011 | Damage, casualties, prisoners and displacement | COMPLETE |
| CW012 | Blockade, occupation and territorial control | COMPLETE |
| CW013 | Civil/internal conflict | COMPLETE |
| CW014 | Ceasefire, armistice, surrender and peace | COMPLETE |
| CW015 | Post-conflict consequences and memory | COMPLETE |
| CW016 | Off-screen / LOD conflict persistence | COMPLETE |
| CW017 | Procedural civilization conflict-doctrine generation | COMPLETE |
| CW018 | Simulator, fixtures, executable tests and integration closure | COMPLETE |

## Core behaviour rule

**Species is not a war-propensity variable.**

Conflict behaviour is resolved from:
- attached cultural context;
- faction/polity doctrine;
- government and legal authority;
- current leader/policy;
- era;
- relations and historical grievances;
- perceived threat and objective stakes;
- actual military/logistical capability;
- casualties, exhaustion and domestic pressure.

Therefore a Klingon Imperial government can be more willing than a Vulcan mainstream political context to escalate the same crisis, while a weakened/exhausted Klingon government can still prefer restraint. A Klingon species label alone does nothing.

## Hard rules

1. Dispute does not imply armed conflict.
2. Mobilization does not imply war.
3. A border crossing or single weapon discharge does not automatically create interstellar war.
4. War requires an explicit cause, political/military objective and valid authority state.
5. AI may propose threats, demands or plans but cannot mutate war state.
6. Culture supplies priors, never deterministic behavior.
7. Species biology cannot directly supply aggression/war weights.
8. Faction, government, culture, leader and individual actor remain separate.
9. No force unit may be spawned because a battle requires more opposition.
10. Strategic resolution consumes pre-existing force identities and produces persistent damage/loss records.
11. Tactical detail may delegate to ship/ground tactical systems; Block 3 owns strategic context/outcome.
12. Occupation/effective control does not automatically change sovereignty or recognition.
13. Blockade requires real forces, location, objective and sustained presence/capability.
14. Civil political fragmentation does not automatically become civil war.
15. Civil war requires armed factions, causes, objectives and force/control state.
16. Ceasefire is not peace; armistice is not automatic reconciliation.
17. Peace does not erase casualties, grievances, veterans, destruction, occupation or treaty obligations.
18. Off-screen conflict cannot change rules merely because the player is absent.
19. Player presence is not an escalation variable.
20. Campaign-start canon initializes the world; after campaign start, live World State is authoritative.

## Sequential boundary

Block 3 may consume Block 1 civilization state and Block 2 claims/borders. It does **not** implement:
- detailed interstellar economy and market/logistics simulation — Block 4;
- procedural pre-campaign historical synthesis — Block 5;
- new inventions/research breakthroughs — Block 6;
- anomalies/archaeology — Block 7;
- systemic crisis generation — Block 8;
- emergent mission generation — Block 9;
- whole-galaxy scheduling/prioritization — Block 10.

## Runtime boundary

CoreRPG 4.5+ remains responsible for authoritative clocks, World State mutation, generic actions/events, persistence and LOD scheduling. This repository owns Star Trek conflict rules/content and a deterministic reference implementation.
