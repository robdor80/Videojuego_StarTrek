# F13 — Acta de preparación autónoma P01–P05 (referencia offline)

**Fecha:** 14-10-2026. **Rama:** `feat/f13-dynamic-universe-reference-20261014`.  
**Base de partida:** `main@ae40c9c4af3e9c651d621250098dbf6068f8258b` (F12 fusionada mediante PR #18).  
**Madurez:** referencia comprobable y auditoría de contratos, **no** `CORE_INTEGRADO`, `UE5_JUGABLE` ni aceptación final.  
**Gobierno:** F02 sigue siendo la única fase principal `EN_CURSO`; F13 permanece `PLANIFICADA` globalmente y P01–P05 no se marcan cerrados.

## 1. Fuentes reutilizadas y frontera de autoridad

Se auditan y reutilizan sin mover ni reescribir:

- `docs/roadmap/procedural_layers_master_plan_v0.1.md`
- `docs/roadmap/procedural_runtime_readiness_v0.1.md`
- `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`
- `docs/roadmap/procedural_civilization_evolution_galactic_interaction_status_v0.1.json`
- `docs/roadmap/procedural_colonization_expansion_borders_status_v0.1.json`
- `docs/roadmap/procedural_conflict_war_status_v0.1.json`
- `universe/generation/procedural_civilization_economy_resource_trade_grammar_v0.1.json`
- `universe/generation/traffic_activity_model.json`
- `universe/generation/network_disruption_crisis_contract.json`
- `universe/generation/population_movement_contract.json`
- `gameplay/economy/civilian_trade_operator_contract.json`
- `gameplay/economy/replicator_post_scarcity_contract.json`
- `gameplay/first_contact/prime_directive_operational_protocol_v0.1.json`
- `gameplay/first_contact/civilization_contact_status_model_v0.1.json`
- `gameplay/first_contact/first_contact_readiness_assessment_v0.1.json`
- `gameplay/diplomacy/diplomatic_state_contract.json`
- `gameplay/exploration/travel_event_scheduler.json`
- `gameplay/exploration/astrographic_discovery_event.json`
- `gameplay/missions/emergent_mission_from_world_state_contract.json`

**CoreRPG** conserva la autoridad sobre World State, tiempo, eventos, persistencia, inventarios y mutaciones. Esta rama solo calcula resultados candidatos sobre copias de fixtures. UE5 no se ejecuta y la IA no recibe capacidad de escribir realidad.

## 2. Resultado por paso

| Paso | Entrega de esta rama | Límite explícito |
|---|---|---|
| **F13-P01** | Auditor de la fotografía 001–120: 001–118 se aceptan únicamente en la madurez ya declarada por el plan; 119 debe seguir `PARTIAL`; 120 debe seguir `BLOCKED_RUNTIME` | No convierte contratos en runtime ni altera el plan maestro |
| **F13-P02** | Puerta automática de secuencia 1→10: exige 1–3 cerrados a nivel referencia y señala **4** como siguiente bloque; rechaza saltos a 5–10 | No declara terminado el bloque 4; el plan original conserva `READY_TO_RESUME` |
| **F13-P03** | Referencia causal de sistemas, planetas, civilizaciones, estaciones, rutas, tráfico, inventarios, demandas, comercio y disrupciones | Los datos son sintéticos y no canónicos; no hay economía autoritativa, simulación de flota ni mutación persistente |
| **F13-P04** | Cribado conservador de Primera Directriz/primer contacto y derivación de candidatos de misión desde necesidades existentes, capacidades y acceso | No implementa el bloque dinámico 9 ni crea incidentes para fabricar misiones; toda asignación necesita autoridad real |
| **F13-P05** | Replay determinista de eventos causales, transferencias económicas, consumo/producción, rutas, descubrimiento, contacto y necesidades, con SHA-256 reproducible | No es save/load Core ni simulación galáctica viva; no demuestra NPC, mundo o misión ejecutados en UE5 |

## 3. Invariantes comprobables

1. Las capas 119 y 120 no pueden promocionarse por inferencia desde 001–118.
2. No se permite empezar 5–10 mientras el primer bloque abierto anterior siga pendiente; con la fotografía actual, el siguiente es el **bloque 4**.
3. Tráfico y comercio requieren causa, origen/destino, ruta y demanda ya existentes.
4. Un comercio no puede consumir stock inexistente ni producir inventario negativo.
5. Una disrupción afecta redes y tráfico preexistentes; no crea naves o escasez arbitraria.
6. Una civilización prewarp no pasa a contacto formal simplemente porque el jugador lo solicite; se conserva la evaluación contextual de Primera Directriz.
7. Alcanzar warp convierte el contacto en candidato, no en obligación automática.
8. Descubrir algo cambia conocimiento del observador, no la verdad física.
9. Una misión emergente solo puede derivarse de una necesidad viva del World State y de una unidad con capacidad y acceso; cercanía del jugador no basta.
10. Un evento reproducido necesita procedencia causal y orden temporal.
11. El replay opera sobre una copia y no modifica el fixture de entrada.
12. Toda salida de referencia lleva `OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION`.

## 4. Evidencia de prueba

Artefactos nuevos:

- `tools/validation/f13_dynamic_universe_reference.py`
- `tools/validation/test_f13_dynamic_universe_reference.py`
- `validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json`
- `.github/workflows/f13-dynamic-universe-reference.yml`

Comandos de referencia:

```bash
python -m py_compile tools/validation/f13_dynamic_universe_reference.py tools/validation/test_f13_dynamic_universe_reference.py
python -m json.tool validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json >/dev/null
python tools/validation/f13_dynamic_universe_reference.py --scenario validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json --output validation/results/f13_dynamic_universe_offline_report.json
python -m unittest discover -s tools/validation -p 'test_f13_*.py' -v
```

**Prueba previa a publicación de la rama:** 44/44 escenarios y 27/27 pruebas unitarias pasan; huella de escenarios `b3dc0451d28243ccbc8ada708b9911fb27e821f98a66c2dc507a8849a041a519`.  
**GitHub Actions del HEAD/PR:** requisito de revisión; comprobar el run del HEAD antes de fusionar.  
**Integración CoreRPG:** `NO_EJECUTADO`. **UE5/MSI:** `NO_EJECUTADO`. **Save/load real:** `NO_EJECUTADO`.

## 5. Estado de los bloques dinámicos

La rama respeta el estado original, no lo reescribe:

- Bloques 1–3: cerrados en sus paquetes de **referencia** existentes.
- Bloque 4 — Living Interplanetary / Interstellar Economy: **sigue `READY_TO_RESUME`**; esta rama aporta un arnés de cribado/evidencia, no su cierre.
- Bloques 5–10: no iniciados ni cerrados por esta preparación.
- El contrato de misiones emergentes se usa únicamente para demostrar la frontera “misión deriva de estado”; **no equivale a implementar el bloque 9**.

## 6. Bloqueos para cierre real de F13

Para alcanzar la puerta global `CORE_INTEGRADO` siguen haciendo falta, como mínimo:

- versión/ref concreta de CoreRPG con interfaces realmente disponibles;
- aplicación autoritativa de eventos, inventarios, tiempo y persistencia;
- save/load y evolución off-screen sobre World State real;
- completar los bloques dinámicos 4→10 respetando su orden;
- integración de navegación, diplomacia, exploración y misiones con autoridad real;
- pruebas de continuidad, conflicto, recursos y consecuencias en ejecución;
- integración UE5 donde corresponda y aceptación del autor con evidencias de partida.

## 7. Decisiones de autor

No se han introducido decisiones creativas nuevas. Se mantienen canon, Primera Directriz, separación Core/Star Trek, causalidad, eras y política de misiones ya documentados.

**Criterio de revisión de esta PR:** fusionar solo la preparación verificable de F13. Una CI verde acredita los escenarios y regresiones offline, no el cierre de F13 ni el bloque 4, ni integración CoreRPG/UE5.
