# Simulation tools

## Sensor Detection Resolution v0.1

`resolve_sensor_scan.py` consumes a materialized world JSON and a structured scan request, then emits only the knowledge detectable by that observer.

Example:

```bash
python tools/simulation/resolve_sensor_scan.py \
  --world content/generated/universe/v0_0_1/system_041.json \
  --request scan_request.json \
  --output scan_result.json
```

Regression tests live in `test_sensor_detection_v0_1.py`.

The current suite covers deterministic output, anti-leakage, resolution-gated hidden information, filters, range, interference and active/passive behavior.
