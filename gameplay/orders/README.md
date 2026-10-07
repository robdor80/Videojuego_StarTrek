# Orders

Orders are structured stateful commands, not direct AI mutations.

## Main models

- `starship_order_contract.json` — common validation/outcome contract.
- `captain_policy_order_v0.1.json` — persistent operating-policy changes made by the commanding officer.
- `subordinate_task_order.json` — delegated execution tasks.
- `starfleet_mission_tasking_order.json` — higher-level mission tasking.
- `starship_order_pipeline.md` — interpretation → validation → execution → authoritative state change.

## Captain policy orders

Policy orders cover decisions such as:
- watch pattern/times;
- readiness;
- training/drills;
- maintenance priority;
- leave/liberty;
- department/resource priorities;
- security posture;
- delegation and standing orders.

A policy order may tell the XO to **prepare implementation** rather than forcing the captain to assign every crewmember personally.

Authority is resolved through:

`../chain_of_command/captain_operational_decision_authority_contract_v0.1.json`

The engine may recommend the objectively stronger option, but recommendation is not command authority.
