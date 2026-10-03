# Validation tools

Repository-local validation utilities.

## Internal reference validator

Run from repository root:

```bash
python tools/validation/validate_internal_references.py
```

It currently checks JSON cross-references for:

- source registry IDs;
- navigation distance `edge_ref` IDs;
- anchor location IDs used by route edges;
- Federation major-relation anchor references.

The validator is intentionally conservative. It does not infer or repair missing data; it only reports dangling references.

Extend it when new cross-file ID families become important enough to validate automatically.
