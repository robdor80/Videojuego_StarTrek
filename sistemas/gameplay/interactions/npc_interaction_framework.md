# NPC Interaction Framework

Status: **FOUNDATION v0.1 — IN PROGRESS**

## Presentation model

Star Trek uses a hybrid interaction model:

> **3D UE5 world + free natural-language interaction + contextual intent gateways + authoritative action validation**

The game should not rely on fixed dialogue trees as its primary social interface.

## Interaction contexts

### Face-to-face
Normal physical conversation.

### Professional
Reports, coordination, technical questions and duty conversation.

### Command
Orders, clarifications, acknowledgement and chain-of-command behavior.

### Mentoring / teaching
Academy classes, tutoring, supervised practice and career mentorship.

### Social
Friendship, leisure, invitations, ordinary personal conversation.

### Private
Sensitive personal conversations with stronger privacy/context assumptions.

### Remote
Combadge, intercom, viewscreen, PADD/message or other communications channel.

## Contextual intent gateways

UI may provide high-level entries such as:

- Hablar libremente;
- Dar orden;
- Solicitar informe;
- Solicitar ayuda;
- Formación;
- Personal.

These select interaction context. They do not replace free dialogue.

## Natural-language action requests

Free language may map to structured intents.

Example:

```text
"¿Tomamos algo después del turno?"
→ social_invitation

"Repita el barrido, esta vez priorizando subespacio."
→ operational_order
```

The relevant game system validates the result.

## Ambiguity

NPCs may request clarification.

They should not blindly invent parameters for consequential professional orders.

## Reporting as gameplay

A superior may ask:

> "Informe."

The player can respond naturally.

Evaluation may compare the report against:

- information actually known to the player character;
- sensor/results data;
- required uncertainty;
- reporting procedure;
- omissions/misstatements.

The AI expresses the conversation. Evidence and scoring come from structured state/rules.

## Memory

Not every utterance becomes a permanent memory.

Persist socially/professionally meaningful events such as:

- promises;
- confidences;
- conflict;
- reconciliation;
- favors;
- instruction;
- praise/reprimand;
- invitation/date;
- rejection;
- significant shared experience.

## Availability

NPCs occupy real state.

They may be:

- on watch;
- sleeping;
- off duty;
- in training;
- eating;
- in a private meeting;
- on an away mission.

An NPC should not magically appear because the player selected a dialogue action.

## NPC ↔ NPC

Off-camera interactions can resolve abstractly as structured social events.

Full dialogue generation is reserved for cases where:

- the player is present;
- the scene is important;
- the exact conversation materially matters.

## Narration

Do not narrate obvious visible UE5 facts.

Use narration for:

- time transitions;
- unrendered/off-camera developments;
- concise scene framing;
- campaign recap;
- moments where cinematic prose adds value.
