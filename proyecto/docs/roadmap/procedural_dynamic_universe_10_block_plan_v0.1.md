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
| 7 | Phenomena, Anomalies & Procedural Archaeology | REFERENCE_COMPLETE |
| 8 | Systemic Crises | REFERENCE_COMPLETE |
| 9 | Emergent Missions from World State | REFERENCE_COMPLETE |
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

**Bloque 6 — Ciencia, tecnología y descubrimientos: REFERENCE_COMPLETE** en los 18 paquetes ST001–ST018. Contrato, simulador de referencia y fixture científico→ingeniería→astillero→ensayo individual, con 54 pruebas nuevas, 152 regresiones dinámicas incluyendo B06 y 29 de F13 superadas en [Actions #43199308066](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43199308066). Ver [plan B06](procedural_science_technology_discovery_plan_v0.1.md), [estado B06](procedural_science_technology_discovery_status_v0.1.json) y [acta](P2_B06_ACTA_CIERRE_REFERENCIA_20261112.md).

**Siguiente elegible: Bloque 7 — Fenómenos, anomalías y arqueología procedural**, tras fusión y CI final de B06. Bloques 7–10 no iniciados. F13 global, CoreRPG, HOST, UE5, investigación offscreen y guardado autoritativo no cambian de estado. Las referencias anteriores que fijaban B4/B5/B6 como siguiente son fotografías históricas conservadas por trazabilidad.

## Actualización secuencial — 12/11/2026, P2-B07

Bloque 7 **REFERENCE_COMPLETE** para fenómenos, anomalías y arqueología en los 18 paquetes PA001–PA018, con PR #116 **fusionada** en `main` (squash `73eb7e59e1032ac5975c9e459f27d2c1f5609522`) y CI B07/F13 de referencia exitoso. La generación/simulación Python, un caso de perturbación subespacial y ruinas protegidas, el control de canon/semillas/LOD y 56 pruebas adversariales no suponen un runtime galáctico. Ver [plan B07](procedural_phenomena_archaeology_plan_v0.1.md), [estado B07](procedural_phenomena_archaeology_status_v0.1.json) y [acta B07](P2_B07_ACTA_CIERRE_REFERENCIA_20261112.md).

**Siguiente elegible: Bloque 8 — Crisis sistémicas.** Bloques 9–10 TODO; F13, CoreRPG, HOST, UE5, escáneres reales, editor procedural y guardado autoritativo NO cambian de madurez. Los párrafos anteriores que señalan B4/B5/B6/B7 como «siguiente» conservan su fecha histórica y no se han eliminado.


## Actualización secuencial — 12/11/2026, P2-B08

Bloque 8 **REFERENCE_COMPLETE en contrato y simulación de referencia**: 20 paquetes CR001–CR020, crisis causales desde hechos externos aceptados, propagación controlada por redes existentes, combinación de choques, contención/recuperación verificadas y conocimiento distribuido con permisos y retraso. La PR [#118](https://github.com/robdor80/Videojuego_StarTrek/pull/118) incorpora contrato, fixture, tests y CI, con primera validación [Actions #43259713758](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43259713758): **56/56 B08, 264/264 B01–B08 y 30/30 F13**. Ver [plan B08](procedural_systemic_crises_plan_v0.1.md), [estado](procedural_systemic_crises_status_v0.1.json) y [acta](P2_B08_ACTA_CIERRE_REFERENCIA_20261112.md).

**Siguiente elegible tras CI final y fusión: Bloque 9 — Misiones emergentes derivadas del estado del universo.** B10 TODO. F13 global sigue PLANIFICADA, CoreRPG mantiene única autoridad, no se ejecutan economía, población, pérdidas, decisiones de guerra, misiones o scheduler, y no hay UE5/HOST jugable. Los textos anteriores que mencionan B4–B8 como «siguiente» se conservan como instantáneas históricas.


## Confirmación administrativa — 12/11/2026, B08

La PR #118 se fusionó en main, squash `bffa7be364cd7e06a1b6c50b823dcb89d7e95cc9`; la CI previa fue 19/19 SUCCESS y la posfusión volvió a certificar 19/19 SUCCESS ([B08](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43260787149), [F13](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43260787238)). La **puerta B09 está abierta** para referencia; no modifica el carácter no autoritativo de B08 ni cierra B10 o F13 global.

## Actualización secuencial — 12/11/2026, P2-B09

**Bloque 9 — Misiones emergentes derivadas del estado del universo: REFERENCE_COMPLETE sólo en contratos y referencia offline**, 20 paquetes EM001–EM020. Requiere hechos de necesidad y consecuencia ya aceptados; proyectar un riesgo B08 no genera misión; autoridad, recursos y rutas externos, intervención prewarp con excepción independiente, NPC sin jugador, noticias retrasadas, resultado y resolución verificados. Ver [plan B09](procedural_emergent_missions_plan_v0.1.md), [estado](procedural_emergent_missions_status_v0.1.json) y [acta](P2_B09_ACTA_CIERRE_REFERENCIA_20261112.md). **La puerta del Bloque 10 — Evolución galáctica en segundo plano se abre tras CI definitivo y fusión de B09.** F13 global PLANIFICADA, CoreRPG/HOST/UE5 sin runtime, capas 119/120 sin cambio. Declaraciones antiguas sobre bloque siguiente son fotografías históricas.

## Confirmación administrativa — 12/11/2026, B09

La [PR #120](https://github.com/robdor80/Videojuego_StarTrek/pull/120) fue **fusionada** en main (squash `4c8733da7cef6acf2b0a0c4259734a615ffed2d0`) después de CI **20/20 SUCCESS** del último HEAD premerge (`94f71f812400e5dbbd9fd3c143a53ad01a235a68`), incluyendo el workflow [B09 #43266888009](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43266888009). Las ejecuciones posteriores a la fusión no han podido comprobarse con la herramienta actual y no se dan por certificadas. **B10 es el siguiente bloque secuencial de referencia**, no un scheduler ya implementado; F13 PLANIFICADA y capas 119/120 sin cambios.
