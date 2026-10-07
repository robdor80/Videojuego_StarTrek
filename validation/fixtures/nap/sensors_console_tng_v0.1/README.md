# NAP fixture — Sensors console / TNG v0.1

**Status:** VERIFIED COMPLETE FIXTURE  
**Production art:** NO

This package proves the Star Trek visual/NAP contract with a real binary master and a real WebP derivative.

It represents the already-approved functional Sensors console model:

`primary navigation → active workspace → persistent operational status`

The image is deliberately a minimal geometric test render. It is **not** a final LCARS design and must never be shipped as game art.

## Why no prompt?

This fixture was produced by a deterministic programmatic renderer, not an image-generation prompt. The NAP handoff schema permits `exact_prompt_ref = null`; provenance points instead to `renderer_spec.json`.

## Files

- `visual_identity.json` — stable fixture identity.
- `resolved_visual_context.json` — profile stack and authoritative functional context.
- `handoff.json` — NAP lifecycle record.
- `renderer_spec.json` — deterministic rendering specification.
- `archive/*.png` — fixture master.
- `production/*.webp` — derived production-format fixture.
- `manifest.json` — hashes, blob SHAs and lifecycle assertions.

## Hard rule

A future production Sensors console may replace all visual styling while preserving the **functional model**. Presentation cannot add capabilities, leak World Truth or auto-execute decisions.
