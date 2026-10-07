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
- `gameplay/duty_system/shipboard_watch_generation_contract_v0.1.json`
- `gameplay/duty_system/duty_watch_state.json`
- `gameplay/duty_system/duty_assignment_model.json`
- `gameplay/duty_system/watch_handoff_model.json`
- `gameplay/characters/activity_schedule_model.json`

### Life aboard
- `gameplay/ship_operations/shipboard_life_state_contract.json`
- `gameplay/ship_operations/off_watch_obligation_model_v0.1.json`
- `gameplay/ship_operations/off_duty_activity_catalog_v0.1.json`
- `gameplay/ship_operations/shipboard_habitability_profile_contract_v0.1.json`
- `lore/starships/classes/shipboard_life/SHIPBOARD_LIFE_PROFILE_CATALOG_v0.1.json`

### Generation
- `universe/generation/procedural_starship_rules.json`
- `universe/generation/procedural_ship_design_contract_v0.1.json`
- `universe/generation/procedural_starship_instance_generation_pipeline_v0.1.json`
- `universe/generation/procedural_ship_crew_watch_schedule_pipeline_v0.1.json`
- `universe/generation/ship_staffing_generation_guidance_v0.1.json`
- `universe/generation/procedural_civilian_ship_design_profiles_v0.1.json`
- `universe/generation/operator_ship_naming_registry_contract_v0.1.json`

### Reference implementations
- `tools/generation/generate_starship_instance.py`
- `tools/generation/generate_civilian_starship.py`
- corresponding unit-test modules in `tools/generation/`

### Validation
- `validation/fixtures/procedural_starship_generation/oberth_science_2372_v0.1/`
- `validation/consistency/shipboard_life_and_procedural_starship_invariants_v0.1.json`

## Important distinction

**Class reference complement ≠ live crew manifest ≠ current watch headcount.**

A Galaxy-class ship can carry a large mixed community. A Defiant-class ship is an austere combat vessel. A B'rel or Hideki can be so small that one injured crewmember changes the watch plan. The schedule is therefore generated from the actual ship, crew, mission and readiness state.

## Runtime boundary

The repository now contains the content rules and deterministic reference generators. CoreRPG 4.5+ remains the future authoritative runtime for persistent live World State, schedule arbitration and off-screen catch-up.
