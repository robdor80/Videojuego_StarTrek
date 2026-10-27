# Chain of Command

The chain-of-command layer decides **who may decide what**. Rank alone is not enough: current position, duty assignment, professional authority, external orders and delegation all matter.

## Player as commanding officer

When the player lawfully holds the commanding-officer/captain position:

> **Engine automation advises and maintains the ship; it does not silently replace command authority.**

For decision domains owned by the captain, the player may:

- accept the engine/XO proposal unchanged;
- modify it;
- reject it and request another proposal;
- issue a different policy;
- delegate the decision;
- revoke a delegation;
- establish standing orders;
- later revise the policy.

Accepting the proposed solution unchanged is still a **captain decision**.

## Control modes

Each command domain may be configured as:

- **manual** — the captain decides directly;
- **proposal_requires_approval** — XO/engine prepares the solution, captain approves or edits;
- **delegated_autonomous** — delegate applies routine decisions inside standing orders; captain retains review/revocation rights.

This allows a player captain to command at the desired level of detail without losing authority.

## Delegation

A normal pattern is:

```text
CAPTAIN
  ↓ defines policy / delegates
EXECUTIVE OFFICER
  ↓ prepares or coordinates implementation
DEPARTMENT HEADS
  ↓ build detailed assignments
CREW / STATIONS
  ↓ execute
```

Example:

```text
Captain: "I want four watches."
        ↓
XO receives policy/order
        ↓
engine + XO build a valid four-watch roster
        ↓
coverage/fatigue/qualification warnings
        ↓
Captain approves, edits or insists
        ↓
effective schedule + persistent command-history record
```

## Limits

Captain authority is broad but not magical.

It does not create:
- missing ship capabilities;
- nonexistent resources;
- professional qualifications;
- medical fitness;
- legal authority owned by someone else.

The Chief Medical Officer's valid fitness authority remains professionally scoped even over the captain. Higher tasking orders, law, treaties and non-overrideable safety constraints can also limit command discretion.

A captain may sometimes choose a worse operational solution than the engine recommends. If it is lawful and physically possible, the correct behavior is usually:

```text
warn → record decision → execute → simulate consequences
```

not:

```text
engine silently replaces captain's decision with its preferred answer
```

## Core files

- `captain_operational_decision_authority_contract_v0.1.json`
- `automatic_command_decision_registry_v0.1.json`
- `command_decision_delegation_state_v0.1.json`
- `command_operational_decision_record_v0.1.json`
- `../orders/captain_policy_order_v0.1.json`
- `../orders/starship_order_contract.json`

## Future-proofing rule

Every new automated operational decision must register:
- decision domain;
- authority owner;
- captain override/review policy;
- delegation policy;
- hard constraints.

No subsystem may quietly invent a new category of "the engine decides and the captain cannot touch it" unless the authority model explicitly says why.
