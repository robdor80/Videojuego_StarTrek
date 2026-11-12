# Procedural Dynamic Universe — 10-block plan v0.1

**Status:** ACTIVE  
**Execution rule:** blocks are implemented strictly in order. A later block may be documented as a dependency, but implementation does not start until the current block is COMPLETE, validated, cross-referenced and recorded in `CONTENT_STATUS.md`.

| Block | Scope | Status |
|---|---|---|
| 1 | Procedural Civilization Evolution & Galactic Interaction | COMPLETE |
| 2 | Colonization, Expansion & Borders | COMPLETE |
| 3 | Procedural Conflict & War | COMPLETE |
| 4 | Living Interplanetary / Interstellar Economy | REFERENCE_COMPLETE |
| 5 | Procedural History & Major Events | REFERENCE_COMPLETE |
| 6 | Science, Technology & Discovery | REFERENCE_COMPLETE |
| 7 | Phenomena, Anomalies & Procedural Archaeology | TODO |
| 8 | Systemic Crises | TODO |
| 9 | Emergent Missions from World State | TODO |
| 10 | Background Galactic Evolution | TODO |

## Block separation

Block 1 owns long-horizon evolution of an already-existing civilization: demographic trend, institutional continuity/change, political cohesion, internal resilience, capability maturation, relationship evolution, extinction/continuity semantics and LOD/off-screen catch-up contracts.

It intentionally does **not** implement:
- colony founding, borders or territorial expansion — Block 2;
- battle/front/war simulation — Block 3;
- detailed interstellar production/markets/routes — Block 4;
- retroactive historical-world generation — Block 5;
- research projects/breakthrough generation — Block 6;
- anomaly/archaeology generation — Block 7;
- crisis generators — Block 8;
- mission generation — Block 9;
- whole-galaxy scheduling/priority simulation — Block 10.

Cross-block hooks may be emitted as candidates/refs, never silently resolved by the wrong block.

## Block 2 ownership

Block 2 closes causal colony founding/growth/abandonment, population transfer, claim/control/sovereignty separation, sparse political-border derivation, claim disputes and colonial autonomy/independence semantics. It does not implement war or the later blocks.

## Block 3 ownership

Block 3 closes crisis/escalation, culture/faction/government conflict behaviour, authority/ROE, objectives, real-force mobilization, strategic operations, losses, occupation/blockade, civil conflict and peace. It does not implement Blocks 4–10.

## Temporary priority gate — Academy Life

Academy Life 20/20 had removed the earlier gate. **Update 2026-11-12:** Block 4 is now COMPLETE on the Star Trek reference-contract/test side, with [plan](procedural_living_economy_plan_v0.1.md), [status](procedural_living_economy_status_v0.1.json) and [acceptance evidence](P2_B04_ACTA_CIERRE_REFERENCIA_20261112.md). It does not certify CoreRPG/UE5/HOST runtime. **Block 5 — Procedural History & Major Events is the next eligible block.**

## Actualización secuencial — 12/11/2026, P2-B05

Bloque 5 **REFERENCE_COMPLETE** sólo a nivel de contrato, simulador histórico offline, 36 pruebas y regresiones. Ver [plan B05](procedural_history_major_events_plan_v0.1.md), [estado B05](procedural_history_major_events_status_v0.1.json) y [acta B05](P2_B05_ACTA_CIERRE_REFERENCIA_20261112.md). **Siguiente elegible: Bloque 6 — Science, Technology & Discovery.** La fase F13 global, el runtime CoreRPG, HOST y UE5 no cambian de madurez.

## Actualización secuencial — 12/11/2026, P2-B06

**Bloque 6 — Ciencia, tecnología y descubrimientos: REFERENCE_COMPLETE** en los 18 paquetes ST001–ST018. Contrato, simulador de referencia y fixture científico→ingeniería→astillero→ensayo individual, con 54 pruebas nuevas, 152 regresiones dinámicas incluyendo B06 y 28 de F13 superadas en [Actions #43198790144](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43198790144). Ver [plan B06](procedural_science_technology_discovery_plan_v0.1.md), [estado B06](procedural_science_technology_discovery_status_v0.1.json) y [acta](P2_B06_ACTA_CIERRE_REFERENCIA_20261112.md).

**Siguiente elegible: Bloque 7 — Fenómenos, anomalías y arqueología procedural**, tras fusión y CI final de B06. Bloques 7–10 no iniciados. F13 global, CoreRPG, HOST, UE5, investigación offscreen y guardado autoritativo no cambian de estado. Las referencias anteriores que fijaban B4/B5/B6 como siguiente son fotografías históricas conservadas por trazabilidad.
