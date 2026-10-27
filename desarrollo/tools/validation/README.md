# Validation tools

Repository-local validation utilities.

## Internal reference validator

Run from repository root:

```bash
python desarrollo/tools/validation/validate_internal_references.py
```

It currently checks JSON cross-references for:

- source registry IDs;
- navigation distance `edge_ref` IDs;
- anchor location IDs used by route edges;
- Federation major-relation anchor references.

The validator is intentionally conservative. It does not infer or repair missing data; it only reports dangling references.

Extend it when new cross-file ID families become important enough to validate automatically.

## F02 architectural contract audit (P02/P03/P04)

Run from the repository root with Python 3.10+ and the F02 branch checked out:

```bash
python desarrollo/tools/validation/validate_f02_contracts.py
python -m unittest discover -s desarrollo/tools/validation -p 'test_validate_f02_contracts.py' -v
```

The first command detects unexpected changes to the **24 P02 source files** (Git blob hashes and 73 selected fields), broken P03 references/coverage, invalid P04 failure-to-test mappings and missing anti-leak constraints in the Sensors result contract. A mismatch is a **review trigger**; update the P02 baseline only after re-auditing intentional changes. Supports CRLF Windows checkouts for blob normalization.

The nine unit tests use **temporary synthetic files** to verify rejection paths, including a normal valid fixture. They do NOT compile CoreRPG, run UE5, demonstrate knowledge filtering at runtime or migrate saves. Core integration and E2E tests remain independently blocked.

[GitHub Actions workflow `f02-contracts.yml`](../../../.github/workflows/f02-contracts.yml) runs both checks on a real repository checkout. Initial run [38149311936](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38149311936) completed successfully (24 P02 sources / 73 selectors / 12 P03 adapters / 9 hermetic tests).

