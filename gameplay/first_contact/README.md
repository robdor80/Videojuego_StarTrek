# First Contact

First Contact is a gameplay system, not a scripted cutscene.

## Core chain

```text
pre-existing civilization
→ detection
→ observation/knowledge
→ technology + warp assessment
→ Prime Directive review
→ culture/government/language preparation
→ First Contact brief
→ command decision
→ initial approach
→ mutual identification
→ dialogue/boundaries
→ refusal, delay, limited contact or formal contact
→ persistent diplomatic state
```

## Important distinctions

```text
warp capable != automatically contacted
first contact != public contact
contact with one official != contact with whole planet
first contact != treaty
first contact != Federation membership
translation != cultural understanding
```

## Generated civilizations

A civilization exists before discovery. Low-LOD World State may contain only stable aggregate facts. When gameplay requires detail, the system deterministically materializes:
- species morphology/biology;
- self-names and external designations;
- language/writing;
- government and representative authority;
- major settlements;
- economy/resources;
- culture/visual profiles;
- relevant representatives/NPCs.

Once materialized, those facts persist.

## Prime Directive

Use `prime_directive_operational_protocol_v0.1.json`.

The Prime Directive is contextual and not reduced to `pre_warp = forbidden`. It covers contamination, self-determination and interference in internal development. Physically possible violations can remain playable and generate consequences.

## Captain

First Contact policy is a registered command domain. Staff may recommend contact, delay or observation; a player captain retains the lawful decision inside mission/Prime Directive/diplomatic constraints.

## Language

The Universal Translator may begin with no translation, partial analysis or literal-only translation. It improves from actual samples and does not grant automatic cultural competence.

## Files

- `civilization_contact_status_model_v0.1.json`
- `first_contact_readiness_assessment_v0.1.json`
- `prime_directive_operational_protocol_v0.1.json`
- `starfleet_first_contact_operational_protocol_v0.1.json`
- `universal_translator_bootstrap_v0.1.json`
- `first_contact_diplomatic_initialization_v0.1.json`
- `first_contact_brief_v0.1.json`
