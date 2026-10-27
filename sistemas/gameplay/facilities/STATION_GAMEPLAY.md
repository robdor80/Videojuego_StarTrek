# Facility assignments and station gameplay

Stations, starbases, outposts, drydocks and shipyards are persistent duty/living environments.

## Core loop

```text
FACILITY
→ departments / tenants / residents
→ continuous watches + day/peak work
→ traffic / service queues
→ local operational state
→ role-specific tasks
→ incidents / support requests
→ persistent consequences
```

A station assignment is not a waiting room for the next starship posting.

## Population is layered

Keep separate:
- operator duty staff;
- contractors;
- civilian residents and dependents;
- business tenants and their employees;
- diplomats/students;
- patients/detainees;
- transient visitors;
- crews of docked ships.

A docked starship crew does not become station personnel.

## Work patterns

Critical operations can run 24/7:
- traffic control;
- power/engineering;
- security response;
- medical readiness;
- communications;
- critical industrial control;
- duty command.

Other work can be day/peak/project based:
- administration;
- research;
- construction/refit teams;
- education;
- commercial tenants;
- diplomacy.

Tiny outposts may use **automation + alternating active/on-call staff** rather than fake three-watch rosters.

## Playable duties

Examples:
- coordinate incoming traffic and holding patterns;
- process docking/visitor clearance;
- manage repair/service queues;
- investigate security incidents;
- handle medical overflow or quarantine;
- supervise engineering isolation after damage;
- manage cargo/personnel transfers;
- coordinate patrol/search-and-rescue;
- support construction/refit work;
- perform scientific monitoring;
- operate communications relay functions;
- work in tenant/civilian services where career context permits;
- participate in diplomacy/administration.

## Services are finite

Emergency priority can reorder a queue. It cannot create:
- a berth;
- a drydock;
- spare parts;
- a medical bed;
- a qualified specialist;
- a capability the design never had.

## Traffic is causal

Ships arrive because of:
- route/economic traffic;
- cargo/passenger movement;
- mission/tasking;
- repair/resupply/medical needs;
- construction/logistics;
- diplomatic/security activity.

The engine never generates ships just to make the station look busy.

## Construction and history

Permanent facilities pass through:
`proposed → surveying → authorized → construction → partial operation → commissioning → operational`

They may later expand, refit, degrade, mothball, be captured, abandoned or decommissioned.

Once construction is committed, `facility_id` persists through all of those changes.

## Main contracts

- `facility_identity_model.json`
- `facility_capability_model.json`
- `facility_topology_model.json`
- `facility_construction_and_lifecycle_state_v0.1.json`
- `facility_watch_and_work_schedule_contract_v0.1.json`
- `facility_residency_tenancy_visitor_model_v0.1.json`
- `facility_service_berth_throughput_generation_contract_v0.1.json`
- `../../universe/generation/facility_existence_and_construction_causality_v0.1.json`
- `../../universe/generation/procedural_facility_generation_pipeline_v0.1.json`
- `../../lore/stations_and_facilities/facility_design_generation_index_v0.1.json`

The same authority, knowledge, schedule and persistence principles used aboard ships apply here where relevant.
