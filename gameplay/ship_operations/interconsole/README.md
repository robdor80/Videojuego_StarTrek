# Inter-console data exchange

Operational consoles may hand structured information to other ship systems.

For the Sensors v0.1 vertical slice, the first locked workflow is:

```text
SENSORS
→ observed contact/readings
→ ENVIAR DATOS A CIENCIA
→ analysis handoff
→ Science work queue
→ scientific interpretation
→ result appended to the same ship contact dossier
```

## Principles

- Transfer only information actually known by the ship.
- Preserve source, operator, timestamp and confidence.
- The receiving console performs its own domain-specific work; it does not merely relabel the source data.
- A receiver may answer that more data are required.
- Results return to shared ship memory while retaining provenance.
- Inter-console transfer never exposes unrevealed authoritative world truth.

This pattern is intended to generalize later to Tactical, Operations, CONN/Navigation, Engineering, Communications and Computer/Database.
