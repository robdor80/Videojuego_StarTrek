# AI Architecture

## Status

**FOUNDATION v0.1 — IN PROGRESS**

## Core rule

> **AI interprets and expresses. Authoritative game systems decide and preserve reality.**

No language model owns:

- World State;
- character inventory/state;
- ship state;
- mission truth;
- sensor truth;
- qualifications;
- grades;
- promotions;
- relationships;
- access permissions;
- historical events.

AI may consume authorized structured context and produce language, interpretations, candidate intents or summaries.

## Primary AI roles

### Dialogue

Express NPC personality, knowledge, relationship, duty context, uncertainty, humor, tension and subtext.

### Natural-language interpretation

Translate free-form player language into candidate structured intents such as:

- order;
- request;
- report;
- question;
- social invitation;
- training question;
- computer query.

The authoritative system then validates whether the requested action exists, is possible and is authorized.

### Teaching

Academy instructors and mentors may:

- explain;
- reformulate;
- answer questions;
- create compatible practice variations;
- debrief evidence.

AI does not award a qualification or invent a grade.

### Narrative presentation

Use sparingly for:

- time transitions;
- off-camera summaries;
- important scene framing;
- recap;
- log drafting.

UE5 should show what can naturally be shown.

### Analysis / language synthesis

The Starship Computer may use AI for complex natural-language analysis or presentation after deterministic systems retrieve and calculate the relevant facts.

## Provider independence

Gameplay systems do not depend directly on a branded model name.

Use logical capability routes such as:

- `FAST_LANGUAGE`;
- `REASONING_LANGUAGE`;
- `DIALOGUE`;
- `COMPUTER_ANALYSIS`;
- `NARRATIVE_SUMMARY`.

Provider/model selection is configuration.

This permits changing between Gemini, OpenAI, Mistral or future providers without redesigning gameplay contracts.

## Cost and latency rule

Do not call a language model when deterministic code can correctly answer.

Examples that should normally be deterministic:

- current ship time;
- known crew location lookup;
- access checks;
- opening a door;
- retrieving a sensor result;
- mathematical correlation;
- retrieving a service record.

AI may turn the resulting structured answer into natural language when needed.

## Knowledge boundary

AI context must be intentionally assembled.

An NPC receives only the knowledge, memories and relationship state that character is authorized to possess.

The Starship Computer receives only data the requester/system is allowed to access.

## Hallucination rule

A fluent answer is not evidence.

If required authoritative data is missing, acceptable outcomes include:

- insufficient data;
- unable to determine;
- access denied;
- no record found;
- clarification required.

Inventing a plausible answer is forbidden.

## Existing subdomains

- captain behavior;
- command interpretation;
- dialogue;
- director;
- game master;
- knowledge filters;
- lore context;
- memory;
- navigation;
- NPC behavior;
- personality;
- recap generation;
- terminology.

These should converge on the authority rules above.
