# Provenance Policy

## Purpose

Every important factual claim must remain traceable to its origin.

Provenance is separate from confidence:
- **authority** describes the type/strength of the source;
- **confidence** describes how certain we are that the structured claim correctly represents the evidence.

## Required provenance categories

- `SCREEN_CANON`
- `OFFICIAL_REFERENCE`
- `LICENSED_NOVEL`
- `LICENSED_COMIC`
- `RELIABLE_SECONDARY`
- `GENERAL_WEB`
- `INFERRED`
- `GAME_ADDITION`

## Confidence

Use:
- `HIGH` — directly and unambiguously supported.
- `MEDIUM` — supported but interpretation, dating or wording is not fully explicit.
- `LOW` — plausible but weak, incomplete or dependent on indirect evidence.

A low-confidence screen-derived interpretation is still not the same thing as a high-confidence game addition; authority and confidence must remain distinct.

## Minimum source record

A source registry entry should contain where applicable:

```json
{
  "source_id": "stable-project-id",
  "source_type": "SCREEN_CANON",
  "title": "Source title",
  "work": "Series / film / novel / comic",
  "season": null,
  "episode": null,
  "issue": null,
  "chapter": null,
  "page": null,
  "url": null,
  "publisher": null,
  "release_date": null,
  "accessed_at": null,
  "notes": null
}
```

For screen evidence, later detailed records may also include scene description and timecode where useful.

## Claim-level provenance

Structured lore should be able to cite more than one source:

```json
{
  "value": "...",
  "provenance": [
    {
      "source_id": "...",
      "confidence": "HIGH",
      "claim_scope": "...",
      "notes": null
    }
  ]
}
```

The exact runtime schema is intentionally **not** fixed here; CoreRPG schemas will evolve. This is the authoring/provenance contract.

## Derived information

### INFERRED

Must record:
- the source IDs used,
- the reasoning in concise human-readable form,
- confidence,
- what evidence would invalidate the inference.

### GAME_ADDITION

Must record:
- why the game needs the addition,
- affected era(s),
- constraints imposed by canon,
- Roberto approval when the decision materially changes the setting or player experience.

## Source granularity

Do not create a registry record for every web page merely because it was opened.

Register a source when it materially supports repository content. Episodes, films, novels and comic issues used as evidence should receive stable IDs as they enter active research.

## Citation discipline

A secondary source is useful for finding a fact. Whenever practical, follow its citation back to the episode, film, licensed work or official reference that actually supports the claim.
