# LORE-03D — Continuidad y divergencia histórica
**Fecha:** 2026-10-27 · **rama:** `lore/03-d-continuity-divergence` · **estado:** NEEDS_REVIEW_DOCUMENTARY; no fusionado.
**Base auditada:** `main@32f4a018bc75b37ff0a4e10fb466ffac6963c381` tras PR #44 y #45.

## Propósito
El canon consolidado establece el pasado de la campaña. Desde el instante efectivo `D` de inicio, cada partida desarrolla historia propia, causal y persistente, incluso fuera del alcance perceptivo del jugador. Las series no constituyen agenda futura. Esta carpeta especifica **adaptación editorial**, no un motor, API, esquema autoritativo o contenido activado.

| Documento | Entrega |
|---|---|
| [D01](D01_auditoria_y_arquitectura.md) | inventario de propietarios y límites |
| [D02](D02_estado_inicial_corte_temporal.md) | bootstrap por fecha y resolución de incertidumbre |
| [D03](D03_divergencia_futuro_abierto.md) | reglas de desviación histórica |
| [D04](D04_autonomia_galactica.md) | actores e instituciones autónomos |
| [D05](D05_causalidad_y_consecuencias.md) | efecto diferido y persistencia |
| [D06](D06_npc_naves_organizaciones.md) | biografías y carreras, Academia |
| [D07](D07_historia_por_partida.md) | log, identidad, guardado y LOD |
| [D08](D08_auditoria_y_cierre.md) | auditoría, pruebas y deuda residual |

**Material de comprobación:** `D_escenarios_documentales_v0.1.json` contiene hipótesis **no instanciadas**; `desarrollo/tools/validation/validate_lore03_d.py` y `test_lore03_d.py` validan políticas/escenarios como modelos de referencia documentales. No migran datos a CoreRPG.

**Decisiones de autor preservadas:** 2383 propuesto sin día/mes; Academia ~4 años hasta ~2387; Rómulo íntegro al inicio; Picard almirante, Riker capitán de USS Titan; posibilidad (no garantía de asignación) Valhalla; TNG/DS9/Voyager y posteriores como única época jugable; no viajes temporales jugables. LORE-03A/B/C y LORE-01/02 intactas.

**Gobierno:** pendiente de aprobación humana para fusión. `COMPLETE` exclusivamente tras fusión autorizada y evidencia de CI. LORE-03E sigue pendiente; no se dan por validados Host, CoreRPG, UE5 ni actuaciones de NPC reales.
