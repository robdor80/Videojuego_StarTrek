# LORE-04A / A01 — Auditoría inicial de reutilización y huecos

**Fecha:** 2026-10-29. **Base verificada:** `main@289a1074b9b2767692823bfe5b8b94662af72a98`. **Resultado:** `AUDITED_DOCUMENTARY`. No auditoría de runtime CoreRPG en esta PR.

## 1. Fuentes verificadas y mapa de propiedad

| Dominio | Fuente existente de referencia | Nivel detectado | Trabajo real de LORE-04 |
|---|---|---|---|
| Identidad y población civil | `sistemas/universe/generation/persistent_population_materialization_rules.json`, `procedural_population_rules.json` | Contratos de población A/B/C, materialización y persistencia | A: contextos civiles: hogar, profesión, relaciones locales; no otro generador |
| LOD social y vínculos | `sistemas/gameplay/social/social_simulation_lod.json`, `relationship_graph_model.json` | Contratos `foundation_fixed` | A: casos cotidianos y restricciones; sin duplicar grafo |
| Familia, crianza, culturas | `mundo/lore/cultures/cultural_profile_contract_v0.1.json`; perfiles humanos/Federación, klingon, romulano, cardassiano, ferengi y bajorano | Dimensiones y perfiles `CONTENT_DEPTH_BASELINE` | A: ejemplos situados, lagunas y fuentes de pantalla; no esencialismo biológico |
| Academia y vida social | `proyecto/docs/roadmap/academy_life_final_closure_v1.0.md` | 20/20 `COMPLETE` en contratos/referencia | A: enlazar, no reescribir horarios, alojamientos, cortejos, sanciones |
| Gobierno Federación | `mundo/lore/federation/government/federation_government.json`, `sistemas/gameplay/organizations/profiles/FEDERATION_INSTITUTIONS_v0.1.json` | Presidente, Consejo y subordinación civil de Flota; mecánica constitucional sin fijar | D: competencias y jurisdicciones con incertidumbres; no inventar elecciones |
| Bajor | `sistemas/gameplay/organizations/profiles/BAJORAN_INSTITUTIONS_v0.1.json` | Gobierno, Milicia y religión diferenciados | A/D: consecuencias para ciudadanos, no igualar Bajor a Federación |
| Gobernanza procedural | `sistemas/universe/generation/procedural_government_institution_representation_grammar_v0.1.json`, `civilization_economy_governance_history_contract.json` | Gramática de instituciones y representación | D: comparación cultural y jurisprudencia; no segundo contrato |
| Economía/comercio | `sistemas/gameplay/economy/replicator_post_scarcity_contract.json`, `civilian_trade_operator_contract.json`, `procedural_civilization_economy_resource_trade_grammar_v0.1.json` | Contratos base de replicación, operadores y causalidad económica | B: fuentes por civilización y límites, **no** ejecutar economía viva |
| Economía viva dinámica | `proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md` | Bloque 4 `READY_TO_RESUME` / no iniciado | B: no atribuir su implementación a documentación |
| Instalaciones y sociedades | `proyecto/docs/roadmap/procedural_facilities_and_station_life_status_v0.1.json`; `procedural_worlds_settlements_civilizations_first_contact_status_v0.1.json` | 15/15 y 18/18 paquetes respectivamente, contratos/referencia | C: servicios de uso civil, cargas, causas/operadores reales, no duplicar |
| Movimiento/logística | `desarrollo/validation/consistency/movement_logistics_economy_diplomacy_invariants_v0.1.json` | Escenarios/invariantes **de diseño** | C: añadir cobertura civil e interfaces |
| Población viva | `desarrollo/validation/consistency/procedural_living_population_invariants_v0.1.json` | Escenarios/invariantes **de diseño** | A: usar mismas garantías de causalidad, no afirmar pruebas runtime |
| Canon abierto, fechas | `proyecto/docs/decisions/lore03a_valhalla_2383_academy.md`; LORE-03E cierre | 2383 propuesto, futuras decisiones reservadas | A–E: no prescribir eventos postinicio |

## 2. Huecos reales

- **A:** casos evidenciados de vida civil por territorio/época, compatibilidad de servicios con rutinas y accesibilidad, diversidad ocupacional, convivencias y calendarios culturales **sin** fijar comportamientos por especie; observabilidad y privacidad en interacciones.
- **B:** mapa de medios de intercambio según jurisdicción y situación, propiedad/escasez/intercambio entre sociedades; distinguir artefactos de pantalla de especulación. No asumir una moneda universal. El estado de economía viva debe ser coordinado con Bloque 4.
- **C:** catálogo contextual de servicios civiles, causalidad de proveedores y pasajeros, mantenimiento civil y competencia legal de infraestructuras; las reglas genéricas ya existen.
- **D:** fichas comparadas de facultades civiles, alcance jurídico sobre territorios, cuerpos de seguridad y resolución de disputas. La jerarquía constitucional exacta de Federación queda no especificada.
- **E:** compatibilidad transversal con LORE-01/02/03, ST-ORG-01 y F00–F15 sin inventar pruebas de integración.

## 3. Reservas e inconsistencias que no se resolverán como canon

- `mundo/lore/federation/economy/README.md` está reservado, no contiene modelo económico final.
- Los documentos de las capas procedurales dicen `foundation_fixed` o `COMPLETE` para contratos, no para el runtime del juego.
- `proyecto/docs/roadmap/procedural_runtime_readiness_v0.1.md` contiene referencias históricas a fases de CoreRPG. El informe de LORE-03E consigna desarrollos más recientes, pero sin integración ejecutada Trek + UE5: **se auditará CoreRPG de nuevo solo cuando se autorice/inicie integración**, sin fijar una versión ausente de prueba actual.
- Las fuentes divulgativas de StarTrek.com sobre economía o vida cotidiana **no son episodios**. Cada afirmación CANON requiere una referencia audiovisual contrastable; los artículos se citan como apoyo editorial o investigación.
- El corpus conserva perfiles Pike/TOS a efectos históricos; solo TNG/DS9/Voyager es jugable.

## 4. Decisiones

**Autorizado como trabajo técnico:** indexar, investigar, clasificar, proponer casos, anotar fuentes, redactar criterios e invariantes de diseño. **Reservado al autor:** fijar nuevas instituciones/derechos, sistema monetario interno no demostrado, obligaciones universales, elecciones precisas, ciudad/colonia original prioritaria o fecha exacta de campaña. Estos huecos no bloquean A02 documental, pero impedirían marcar sus propuestas creativas como aprobadas.

**Resultado A01:** inventario y frontera localizados; LORE-04A puede iniciar documentación sin alteraciones a contratos, `CONTENT_STATUS.md` o `main`.

## 5. Resultado final A01 y procedencia concreta (auditoría del corpus)

Se incorporan por referencia **cinco anclas de episodios nuevas** y **doce referencias editoriales oficiales** al registro central `mundo/sources/source_registry/source_registry.json`, sin duplicar las fuentes ya presentes. El inventario verificado pasa a 530 entradas; las 14 afirmaciones/casos de investigación constan en `lore04a_evidence_ledger_v0.1.json`. El registro identifica episodios, pero sus minutajes siguen **pendientes** y los artículos oficiales no adquieren carácter de `SCREEN_CANON`.

La separación entre los tres niveles es obligatoria: **existencia poblacional A/B/C** ≠ **detalle social LOD A/B/C** ≠ **documentación lore A01–A08**. A01 no modifica ninguno de los contratos existentes ni implementa reglas nuevas en CoreRPG. `A03`–`A07` amplían investigación y casos, mientras `A08` audita restricciones. A01 es `COMPLETE_DOCUMENTARY_CANDIDATE`, sujeto a CI, revisión y fusión autorizada. No introduce decisiones materiales vinculantes.
