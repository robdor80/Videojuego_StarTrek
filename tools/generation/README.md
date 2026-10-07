# Generation tools

## v0.0.1 observable-system generator

`generate_v0_0_1_system.py` is the reference deterministic generator for the first sensor vertical slice.

Properties:

- standard-library Python only;
- same campaign seed + sector + era + date produces the same world;
- stable generated entity IDs;
- generated truth is materialized before any sensor query;
- output includes detectable signatures, hidden properties and interference;
- built-in v0.0.1 validation.

Example:

```bash
python tools/generation/generate_v0_0_1_system.py \
  --seed academy_sensor_test_001 \
  --sector 041 \
  --era tng_ds9_voyager \
  --date 2368-01-01 \
  --validate \
  --output content/generated/universe/v0_0_1/system_041.json
```

Regression tests:

```bash
python tools/generation/test_v0_0_1_generator.py
```

The reference regression seed is locked by SHA-256 digest. An intentional generator-algorithm change must increment the generator version and update the expected digest deliberately.

- `simulate_civilization_evolution.py` — deterministic reference simulator for Block 1 civilization evolution; major transitions require explicit causes and later-block boundaries are enforced.
