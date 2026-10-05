# AI Runtime Orchestration

Status: **FOUNDATION v0.1**

## Request pipeline

```text
PLAYER / NPC / SYSTEM INPUT
        ↓
CONTEXT RESOLUTION
        ↓
CAN DETERMINISTIC CODE HANDLE IT?
     ↙ YES                 NO ↘
DETERMINISTIC              AI ROUTE
RESULT                     (appropriate capability)
     ↘                     ↙
      STRUCTURED CANDIDATE
              ↓
      AUTHORITY VALIDATION
              ↓
      STATE CHANGE / QUERY RESULT
              ↓
      OPTIONAL NATURAL-LANGUAGE PRESENTATION
```

## Important distinction

A language model may parse:

> "Lieutenant, repeat the scan focused on subspace emissions."

into a candidate command.

It does not execute the scan.

The action system validates:

- issuer identity;
- recipient;
- authority;
- available console/system;
- valid parameters;
- current ship state.

## Capability routes

### FAST_LANGUAGE
Short interpretation, classification, concise response formatting and low-latency conversational work.

### REASONING_LANGUAGE
Complex synthesis over already-authorized data, difficult explanation or multi-source analysis.

### DIALOGUE
Character-authentic conversational response constrained by personality, knowledge, memory and relationship.

### NARRATIVE_SUMMARY
Recaps, transitions and log-draft language from structured sources.

### COMPUTER_ANALYSIS
Natural-language interface around ship-computer analytical queries after deterministic retrieval/calculation where possible.

## Escalation

A fast route may escalate only when the request genuinely requires more reasoning/context.

Escalation should preserve:

- source references;
- access boundaries;
- uncertainty;
- requested task.

## No direct state mutation

Language-model output must not directly mutate authoritative state.

It may return:

- a structured action candidate;
- a dialogue line;
- a draft;
- an explanation;
- a classification;
- a requested clarification.

State-changing requests pass through validated game actions.

## Auditing

Where AI output affects a meaningful player-facing action, retain enough structured provenance to know:

- which route was used;
- what authoritative sources were supplied;
- what candidate intent was produced;
- what validated action actually occurred.

Do not log unnecessary private raw text beyond the project's privacy/diagnostic requirements.
