# F13 — Universo dinámico, exploración y misiones

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

Ampliar un universo persistente que genera situaciones causales y respeta canon/era.

## Pasos y entregables

- [ ] **F13-P01** — Consolidar estado de capas 001–120 y planes procedurales sin confundir contrato con runtime.
- [ ] **F13-P02** — Retomar, siguiendo el orden interno, bloques dinámicos 4–10 (1–3 cerrados a nivel de referencia).
- [ ] **F13-P03** — Integrar navegación, sistemas, planetas, civilizaciones, estaciones, tráfico, recursos, política y economía.
- [ ] **F13-P04** — Cerrar experiencia de primer contacto, Primera Directriz, diplomacia, exploración y misiones emergentes.
- [ ] **F13-P05** — Ejecutar pruebas de simulación fuera de escena, coherencia galáctica, conflicto y consumo de recursos.

## Material ya creado que no se mueve

- `sistemas/universe/`
- `sistemas/gameplay/first_contact/`
- `sistemas/gameplay/conflict/`
- `sistemas/gameplay/diplomacy/`
- `sistemas/gameplay/exploration/`
- `proyecto/docs/roadmap/procedural_layers_master_plan_v0.1.md`
- `proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`
- `sistemas/narrative/`
- `desarrollo/validation/fixtures/procedural_first_contact/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F03–F05 y Core runtime; respetar bloque 4 antes del 5 en adelante sin duplicar subsistemas.

## Puerta de cierre

Mundo con eventos reproducibles, vida persistente y misiones derivadas de estados existentes. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).


## Avance autónomo de referencia — 14-10-2026

Preparación **P01–P05** con auditoría de capas 001–120, puerta estricta de bloques dinámicos 4→10, economía/tráfico/recursos/disrupciones, Primera Directriz y primer contacto, derivación de misiones desde necesidades preexistentes y replay causal determinista **solo offline**. Ver [acta de evidencias y bloqueos](ACTA_P01_P05_REFERENCIA_2026-10-14.md).

- Ejecutor sin autoridad Core: `desarrollo/tools/validation/f13_dynamic_universe_reference.py`.
- **44 escenarios** sintéticos y no canónicos: `desarrollo/validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json`.
- Pruebas unitarias: `desarrollo/tools/validation/test_f13_dynamic_universe_reference.py`.
- CI: `.github/workflows/f13-dynamic-universe-reference.yml`.

La preparación conserva 001–118 en su madurez declarada, 119 `PARTIAL`, 120 `BLOCKED_RUNTIME` y el **bloque 4 como siguiente bloque real**. No cierra el bloque 4 ni implementa 5–10; el uso del contrato de misión emergente solo valida la frontera causal y no adelanta el bloque 9.

**No hay mutaciones de World State, integración CoreRPG, save/load real ni ejecución UE5/MSI.** F13 continúa globalmente `PLANIFICADA` y F02 sigue siendo la única fase principal `EN_CURSO`.

## Actualización P2-B05 — 12-11-2026

El bloque 4 de economía fue cerrado de referencia mediante PR #113 y el **bloque 5** alcanza `REFERENCE_COMPLETE` mediante PR #114 (historia procedural, causalidad, rectificaciones y conocimiento filtrado). La frontera del siguiente trabajo de referencia es el **Bloque 6**, sin ejecutar todavía sus contenidos. Las frases del acta de octubre que sitúan el bloque 4 como siguiente describen un estado histórico y se conservan para trazabilidad. F13 global permanece **PLANIFICADA** y no se atribuye a CoreRPG/HOST/UE5 esta implementación de referencia.

## Actualización P2-B06 — 12-11-2026

El Bloque 6, Ciencia, tecnología y descubrimientos, dispone de contrato Star Trek y referencia Python independiente, fixture y **54/54 pruebas**; CI [#43199308066](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43199308066) con 152/152 regresiones B1–B6 y 29/29 F13. El bloque conserva los ocho pasos aprobados de LORE-02 D y las restricciones Omega, temporalidad, astilleros y crédito NPC. Véase [plan B06](../../../procedural_science_technology_discovery_plan_v0.1.md) y [acta](../../../P2_B06_ACTA_CIERRE_REFERENCIA_20261112.md).

El siguiente trabajo **secuencial de referencia** es Bloque 7 (anomalías y arqueología); B08–B10 no iniciados. F13 **PLANIFICADA**, sin integración CoreRPG/HOST/UE5, IA productiva, memoria persistida ni ejecución offscreen demostradas.

## Actualización P2-B07 — 12-11-2026

B07 dispone de 18 paquetes PA001–PA018 de referencia, contrato, generador Python offline, fixture de anomalía subespacial/ruinas arqueológicas, 56 pruebas adversariales y regresiones dinámicas/F13. Ver [plan B07](../../../procedural_phenomena_archaeology_plan_v0.1.md) y [acta](../../../P2_B07_ACTA_CIERRE_REFERENCIA_20261112.md). **La frontera secuencial de referencia pasa a B08, crisis sistémicas, después de CI final y fusión PR #116.** Los párrafos anteriores son estados históricos.

La fase global F13 permanece **PLANIFICADA**. El material nuevo no es un generador físico operativo de CoreRPG, ni el escáner de F06, ni arqueología UE5, ni persistencia transaccional real, ni AI de NPC ejecutiva, ni scheduler B10. No se cambia el estado de las capas 119/120.

## Confirmación de fusión P2-B07 (12-11-2026)

La PR #116 fue fusionada en `main` (`73eb7e59e1032ac5975c9e459f27d2c1f5609522`) con B07 y F13 CI de referencia verdes. La puerta de trabajo de Planificación 2 está ahora en **B08 — Crisis sistémicas**. En ningún caso implica cierre runtime de F13. La auditoría adicional de Academia conserva su traspaso histórico B04 y debe leer el estado vivo sin exigir que B04 vuelva a ser pendiente.
