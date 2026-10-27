# B07 — Integración con documentación anterior y migración diferida

## Fuentes de verdad del proyecto (no replicar)

| Pregunta | Archivo de referencia en `main` |
|---|---|
| ID de evento histórico | `lore/diplomacy/historical_events_v0.1.json` o ancla en `lore/historical_events/lore03_a_chronology_index_v0.1.json` |
| Definición histórica de conflicto | `lore/conflicts/conflict_definition_contract.json` |
| Acuerdos y conflictos preexistentes | `lore/diplomacy/agreements_conflicts_v0.1.json` |
| Relaciones bilaterales y evidencias | `lore/diplomacy/relation_index_v0.1.json`, `relation_evidence_v0.1.json` |
| Civilizaciones, instituciones y culturas | `lore/factions/*`, `lore/cultures/*` |
| Cronología, incertidumbres y 2383 | `lore/historical_events/lore03_a_*`, `docs/decisions/lore03a_valhalla_2383_academy.md` |
| Tecnología, ciencia, medicina y riesgos | LORE-02 (sin incluir capacidades inventadas) |
| Causas, escalada, operaciones, paz | `gameplay/conflict/conflict_war_index_v0.1.json` (17 contratos de referencia) |
| Pérdidas y consecuencias | `gameplay/consequences/conflict_war_event_contract_v0.1.json`, `world_event_consequence_contract.json` |
| Estado autoritativo y persistencia | CoreRPG (futura integración, NO implementada en LORE-03B) |

## Contrato de importación FUTURO (solo especificación editorial)

`LORE03B historical dossiers -> mapping verified historical event/faction/source IDs -> campaign bootstrap before D (D precisa fecha) -> CoreRPG state initialization under its contracts -> no post-D historical scheduling`.

La primera transformación exige comparar identificadores con el repositorio **ya reorganizado**, revisar las incertidumbres de fuente, normalizar participantes dentro de sus contextos temporales y definir subactores sin inventar entidades. Esta fase NO genera un JSON de runtime listo para cargar en UE5 o CoreRPG.

## Dependencias críticas de ST-ORG-01

- Los enlaces y directorios del paquete usan rutas observadas en `main` el 27-10-2026.
- **NO** trasladar ficheros al repositorio hasta revisar resultado y mapa de ST-ORG-01.
- No crear ramas ni PR hasta verificación del cierre.
- Si cambian rutas, actualizar referencias y validadores conservando los IDs estables y la trazabilidad de los originales.

## Límites de LORE-03C/D/E

- **C**: memoria específica, conocimientos, secretos, veteranos, memoriales y biografías a nivel NPC.
- **D**: divergencia efectiva desde D, temporadas, registro de historia por guardado.
- **E**: auditoría transversal de A–D.

B prepara documentación útil para estas fases, pero no pretende cerrarlas anticipadamente.