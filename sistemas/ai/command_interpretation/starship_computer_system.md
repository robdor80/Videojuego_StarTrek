# Starship Computer System

Status: **FOUNDATION v0.1**

## Purpose

The ship computer is a shared runtime service for all stations and departments. It is not a separate game simulation and it is not allowed to mutate authoritative state directly.

The intended player experience is:

```
PLAYER SPEAKS / TYPES
        ↓
SHIP COMPUTER INTERPRETS INTENT
        ↓
STRUCTURED COMMAND PLAN
        ↓
AUTHORITY + SAFETY + CONTEXT VALIDATION
        ↓
DETERMINISTIC GAME SYSTEM EXECUTES
        ↓
AUTHORITATIVE RESULT
        ↓
SHIP COMPUTER REPORTS / ASKS FOR DECISION
```

The same contract must be usable by:
- the Holodeck web prototypes;
- Unreal runtime;
- text input;
- voice input;
- NPC-issued orders;
- future console families beyond Sensors.

## Core rule

**AI interprets. Core executes.**

The model may:
- understand imperfect natural language;
- resolve context when the active computer profile permits it;
- decompose a request into one or more candidate actions;
- ask a clarification;
- summarize a deterministic result;
- suggest technically valid options.

The model may not:
- fabricate sensor results;
- fabricate ship state;
- create energy/resources;
- bypass permissions;
- decide which crew member/contact/resource to sacrifice when that decision belongs to an officer;
- directly mutate authoritative game state.

## Input modes

Text and voice are peers. Both end at the same interpretation contract.

```
TEXT ─────┐
          ├─> NORMALIZED UTTERANCE -> INTERPRETER -> COMMAND PLAN
VOICE ────┘
```

Voice transcription is transport, not authority. A transcription error must still pass through the same validation and clarification rules.

## Computer generations

Computer capability is data-driven and belongs to the ship/era, not the UI skin.

### Pike / Constitution 2259

- minimal contextual inference;
- explicit targets preferred;
- short single-step automation;
- frequent clarification;
- no hidden multi-step autonomy.

### Kirk / Constitution 2266

- basic conversational context;
- can reuse a recently selected/mentioned object;
- short procedural chains;
- limited automatic watches/macros.

### Picard / Galaxy 2364

- broad operational context;
- multi-step procedural decomposition;
- automatic preparation of routine sensor configuration;
- persistent watches;
- proactive warnings and option generation;
- still requires human authority for command decisions.

Future computer profiles should extend this matrix rather than hard-code era checks into individual consoles.

## Ship state context

The interpreter may receive a filtered read-only snapshot of authoritative state, subject to role and clearance.

Potential domains:
- Sensors;
- Tactical;
- Operations;
- Engineering;
- Propulsion;
- Shields;
- Weapons;
- Damage control;
- Environmental systems;
- Transporters;
- Shuttlebays;
- Navigation;
- Communications;
- crew location/duty state;
- alert condition;
- mission orders;
- captain standing orders.

The AI only sees what the requesting actor is entitled to know.

## Required context envelope

A runtime request should contain, at minimum:

```json
{
  "requestId": "uuid",
  "inputMode": "text|voice",
  "utterance": "...",
  "issuer": {
    "entityId": "player-or-npc",
    "role": "sensor_officer",
    "rank": "...",
    "clearance": ["..."]
  },
  "computerProfile": "galaxy_2364",
  "station": "sensors",
  "selection": {
    "contactId": "C-43"
  },
  "localState": {},
  "shipState": {},
  "missionContext": {},
  "conversationContext": []
}
```

Only the smallest relevant state should be sent to the external model.

## Command plan

The interpreter returns a plan, never a state mutation.

```json
{
  "version": "1.0",
  "intentSummary": "Maintain C-43 under priority warp-signature watch",
  "needsClarification": false,
  "clarificationQuestion": null,
  "actions": [
    {
      "type": "track_signature",
      "contactId": "C-43",
      "signature": "warp",
      "priority": "priority"
    },
    {
      "type": "watch",
      "contactId": "C-43",
      "condition": "course_change",
      "threshold": 5
    }
  ]
}
```

The engine validates each action against:
- schema;
- issuer authority;
- system availability;
- physical state;
- resource/capacity constraints;
- current mission/standing orders;
- computer-profile autonomy limits.

## Clarification / dead ends

If the plan cannot be executed safely or deterministically, return control to the operator.

Examples:
- tracking capacity exhausted;
- target ambiguous;
- requested system offline;
- insufficient clearance;
- conflicting standing order;
- requested action would require abandoning another protected task.

The computer should say what blocks execution and ask for the smallest missing decision.

## Model routing policy

The personal runtime uses quota-aware routing.

- **Gemini 3.5 Flash-Lite** is the default interpreter.
- A transient HTTP 503 is retried once after a short delay.
- **Gemini 3.8 Flash** is used automatically only when 3.5 remains technically unavailable after that retry.
- 3.8 also receives one retry for a transient 503.
- A schema/contract validation failure or interpreter uncertainty from 3.5 does **not** automatically consume a 3.8 call; the Computer asks the officer for clarification instead.
- The operator may explicitly force 3.8 when desired.
- If both external models remain unavailable, a deterministic local fallback may handle supported intents without mutating state outside normal validators.

This policy exists to preserve the limited 3.8 quota for cases where the higher-capability model is genuinely needed because the default model is unavailable, rather than using it as a generic repair mechanism for unsupported contracts.

## Result presentation layer

After deterministic execution, the authoritative result is not sent back to the LLM by default.

The runtime uses a local contextual response composer:

```
PLAYER ORDER
   ↓
GEMINI INTERPRETS
   ↓
COMMAND PLAN
   ↓
DETERMINISTIC ENGINE
   ↓
AUTHORITATIVE RESULT
   ↓
LOCAL RESPONSE COMPOSER
   ↓
PLAYER
```

The composer receives the original plan plus structured engine results and decides what belongs in the primary Computer reply. It must:

- answer the actual condition requested by the officer;
- avoid presenting non-matching observations as if they were successful matches;
- keep full raw observations available in technical details/logs;
- never invent or reinterpret authoritative state;
- avoid a second model call merely to phrase routine results.

Example: if the officer asks to mark **new** contacts above 60% confidence, existing contacts above 60% may remain visible in technical details but must not be presented in the main reply as qualifying candidates.

A future optional LLM summarization pass may exist for special narrative or conversational cases, but it is not part of the default operational path.

## Transparency

Routine use should be simple. Advanced technical data remains inspectable.

Every executed plan should keep a structured trace:
- user utterance;
- interpreter provider/model;
- command plan;
- validation result;
- actions actually executed;
- authoritative result IDs;
- any clarification or override.

This enables debugging, training evaluation and deterministic replay without exposing unnecessary model internals.

## Web prototype relationship

`academiaflota/holodeck/sensors-v02` is the first executable client of this architecture.

It should be treated as a laboratory for:
- natural-language command quality;
- voice/text parity;
- computer-generation differences;
- clarification policy;
- resource conflicts;
- training integration;
- UI simplification;
- API latency/failure behavior.

Once validated, the same contract is implemented behind Unreal interfaces rather than redesigning the behavior from scratch.
