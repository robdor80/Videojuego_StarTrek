# Shipboard Life & Procedural Starship Generation

This subsystem connects **ship generation** with **the actual lives of the people aboard**.

## Core chain

```text
WORLD NEED
→ operator / role
→ class or reusable procedural design
→ persistent ship identity
→ installed systems / configuration
→ staffing requirements
→ watch policy and rosters
→ persistent crew
→ individual schedules
→ off-watch obligations
→ leisure / family / private life
→ alerts / casualties / schedule changes
→ persistent history
```

## Key files

### Watches and schedules
- `sistemas/gameplay/duty_system/shipboard_watch_generation_contract_v0.1.json`
- `sistemas/gameplay/duty_system/duty_watch_state.json`
- `sistemas/gameplay/duty_system/duty_assignment_model.json`
- `sistemas/gameplay/duty_system/watch_handoff_model.json`
- `sistemas/gameplay/characters/activity_schedule_model.json`

### Life aboard
- `sistemas/gameplay/ship_operations/shipboard_life_state_contract.json`
- `sistemas/gameplay/ship_operations/off_watch_obligation_model_v0.1.json`
- `sistemas/gameplay/ship_operations/off_duty_activity_catalog_v0.1.json`
- `sistemas/gameplay/ship_operations/shipboard_habitability_profile_contract_v0.1.json`
- `mundo/lore/starships/classes/shipboard_life/SHIPBOARD_LIFE_PROFILE_CATALOG_v0.1.json`

### Generation
- `sistemas/universe/generation/procedural_starship_rules.json`
- `sistemas/universe/generation/procedural_ship_design_contract_v0.1.json`
- `sistemas/universe/generation/procedural_starship_instance_generation_pipeline_v0.1.json`
- `sistemas/universe/generation/procedural_ship_crew_watch_schedule_pipeline_v0.1.json`
- `sistemas/universe/generation/ship_staffing_generation_guidance_v0.1.json`
- `sistemas/universe/generation/procedural_civilian_ship_design_profiles_v0.1.json`
- `sistemas/universe/generation/operator_ship_naming_registry_contract_v0.1.json`

### Reference implementations
- `desarrollo/tools/generation/generate_starship_instance.py`
- `desarrollo/tools/generation/generate_civilian_starship.py`
- corresponding unit-test modules in `desarrollo/tools/generation/`

### Validation
- `desarrollo/validation/fixtures/procedural_starship_generation/oberth_science_2372_v0.1/`
- `desarrollo/validation/consistency/shipboard_life_and_procedural_starship_invariants_v0.1.json`

## Important distinction

**Class reference complement ≠ live crew manifest ≠ current watch headcount.**

A Galaxy-class ship can carry a large mixed community. A Defiant-class ship is an austere combat vessel. A B'rel or Hideki can be so small that one injured crewmember changes the watch plan. The schedule is therefore generated from the actual ship, crew, mission and readiness state.

## Runtime boundary

The repository now contains the content rules and deterministic reference generators. CoreRPG 4.5+ remains the future authoritative runtime for persistent live World State, schedule arbitration and off-screen catch-up.


## Captain command authority

When the player is the lawful commanding officer, engine-generated operational choices inside command authority are **defaults/proposals**, not immutable decisions.

The captain may:
- accept the proposal unchanged;
- modify it;
- reject it and ask the XO/staff for another;
- issue a different policy;
- delegate the domain;
- revoke delegation;
- create standing orders.

Supported control modes:
- `manual`;
- `proposal_requires_approval`;
- `delegated_autonomous`.

This applies to watches, rosters, training/drills, maintenance priorities, readiness/alerts, leave, resource/department priorities, security posture, away-team policy and other registered command domains.

Every future automatic operational decision must be registered in:

`sistemas/gameplay/chain_of_command/automatic_command_decision_registry_v0.1.json`

Captain authority remains subject to physical capability, qualification, valid medical authority, law/higher tasking and explicitly non-overrideable safety constraints.
