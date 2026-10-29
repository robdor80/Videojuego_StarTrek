# LORE-04 — Plan maestro de vida civil, economía e instituciones galácticas v0.1

**Fecha:** 2026-10-29. **Estado:** PLANIFICADO / revisión pendiente del autor; LORE-04A en inicio documental. **Rama de trabajo:** `docs/lore04a-vida-civil-20261029`.
**Alcance jugable:** TNG/DS9/Voyager y continuidad; 2383 como **año de entrada a Academia propuesto**, no día cerrado. Corte temporal abierto; las secuelas futuras de otras series no se imponen.
**Cierre de referencia:** LORE-03 PR #50, `main@289a1074b9b2767692823bfe5b8b94662af72a98`.

## 1. Propósito y límites

Describir por qué, dónde y cómo viven los civiles, qué instituciones les afectan y qué actividad económica o logística es plausible. La documentación solo puede restringir o enriquecer las definiciones y decisiones del videojuego. **No crea un simulador alternativo a CoreRPG ni afirma que exista un runtime completo**. CoreRPG es propietario exclusivo del WorldState autoritativo, eventos, mutaciones, persistencia y resolución de consecuencias; Star Trek aporta reglas de dominio, perfiles, hechos canon, ejemplos, fixtures e invariantes. UE5/IA/NAP consumen vistas autorizadas.

Separar `SCREEN_CANON` (escena/episodio concreto), `INFERRED` (inferencia identificada y justificada), `GAME_ADDITION` (propuesta de contenido jugable) y `UNKNOWN` (dato no establecido). Los artículos oficiales o secundarios orientan la búsqueda pero **no ascienden automáticamente** una inferencia a canon de pantalla. Respetar `mundo/sources/canon_policy.md` y `mundo/sources/provenance_policy.md`.

## 2. Auditoría de reutilización obligatoria

Consultar antes de crear cualquier contrato:
- `sistemas/universe/generation/persistent_population_materialization_rules.json`; `procedural_population_rules.json`; `sistemas/gameplay/social/social_simulation_lod.json`; `relationship_graph_model.json`: existencia, identidad, vínculos y LOD.
- `mundo/lore/cultures/cultural_profile_contract_v0.1.json` y perfiles por cultura: hogar, formación, ocupaciones, rituales y variación individual.
- `sistemas/universe/generation/civilization_economy_governance_history_contract.json`; `procedural_civilization_economy_resource_trade_grammar_v0.1.json`; `sistemas/gameplay/economy/replicator_post_scarcity_contract.json`; `civilian_trade_operator_contract.json`.
- `sistemas/universe/generation/procedural_government_institution_representation_grammar_v0.1.json`; `sistemas/gameplay/organizations/profiles/FEDERATION_INSTITUTIONS_v0.1.json` y `BAJORAN_INSTITUTIONS_v0.1.json`.
- `sistemas/universe/generation/settlement_infrastructure_contract.json`; `population_movement_contract.json`; contratos de estaciones, naves civiles, apoyo y logística existentes.
- `proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`: **Bloque 4 (economía viva) READY_TO_RESUME, no iniciado**. LORE-04B NO cambia el estado del bloque ni lo suplanta.
- `proyecto/docs/roadmap/academy_life_final_closure_v1.0.md`: 20/20 paquetes de Academia cerrados a nivel contrato/referencia; no duplicar socialización/horarios.
- `proyecto/docs/decisions/lore_to_game_rule.md`: toda ficha debe incluir utilidad jugable o una reserva explícita de integración.
- `proyecto/docs/roadmap/procedural_runtime_readiness_v0.1.md` y acta `lore_03_e/E08_dictamen_y_cierre.md`: distinguir cierre documental de integración ejecutable. Referencias antiguas a versiones de CoreRPG no son verificación del runtime actual.

La matriz de hallazgos y huecos está en `lore_04_a/A01_auditoria_reutilizacion.md`.

## 3. Fases y paquetes

| Fase | Paquetes documentales propuestos | Dependencia principal | Criterio de salida documental |
|---|---|---|---|
| **04A — sociedad** | A01 inventario y trazabilidad; A02 familias, vivienda y redes; A03 educación, oficios y servicios; A04 ocio, cultura, movilidad diaria; A05 perfiles multijurisdiccionales; A06 rutinas/LOD/eventos; A07 casos de juego y conocimiento NPC; A08 pruebas, reservas y cierre | LORE-01 culturales, LORE-03 memoria, población/Academia/social existentes | Cada tema reutiliza reglas, discrimina canon/inferencia/adición, aporta casos, evidencia, límites temporales y ausencia de estereotipos |
| **04B — economía** | B01 inventario de modelos; B02 producción/escasez/replicación; B03 intercambio/monedas/latinio; B04 propiedad/trabajo/servicios; B05 fronteras y validación; B06 auditoría | Economía civil existente, Bloque procedural 4 como **propietario** de simulación económica | Matriz cultural de reglas, ninguna moneda/salario universal inventado ni creación de un motor económico paralelo |
| **04C — infraestructura** | C01 catálogo existente; C02 viviendas/servicios/estaciones; C03 rutas de pasajeros/carga; C04 recursos/mantenimiento; C05 casos off-screen; C06 validación | Instalaciones 15/15, asentamientos 18/18, logística/transporte | Rutas/instalaciones con operadores, capacidad, localización, causa, identidad y consecuencias; sin spawns por conveniencia |
| **04D — instituciones** | D01 mapa de autoridad; D02 Federación y mundos miembros; D03 gobiernos no federales; D04 justicia/servicios/seguridad; D05 conflictos de competencias; D06 validación | LORE-01 instituciones, gobierno procedural, acuerdos y LORE-03 | Distinción civil/militar/Flota, competencias y soberanía trazables; constituciones y leyes desconocidas quedan desconocidas |
| **04E — transversal** | E01 integridad; E02 temporalidad/canon; E03 sociedad/economía; E04 gobiernos/jurisdicción; E05 CoreRPG/IA/LOD; E06 F00–F15 y ST-ORG-01; E07 regresiones; E08 dictamen y PR de cierre | 04A–D aprobadas/fusionadas | Ausencia de contradicciones y duplicación, matrices, evidencia de pruebas y reservas explícitas; **nunca** confundir cierre documental con runtime |

**Secuencia:** 04A → 04B → 04C → 04D → 04E, pero preparación documental en paralelo solo si no invade contratos de otro bloque. Cada paquete necesita evidencia y no implica automáticamente aceptación ni merge.

## 4. Definición de terminado para cualquier subfase

1. Archivos de origen enlazados, no clonados; decisiones preexistentes respetadas.
2. Por afirmación delicada: episodio/escena o etiqueta de incertidumbre; fecha y jurisdicción válidas.
3. Salida útil para juego: condiciones, conocimiento, actores, acciones o invariantes existentes; nuevas propuestas claramente no aprobadas.
4. Toda acción material es propuesta/candidato hasta que CoreRPG la valida; la IA no inventa hechos ni controla WorldState.
5. Casos positivos y negativos de coherencia; pruebas reproducibles donde proceda.
6. README/índice mínimo de entregables, PR **Draft**, sin actualizaciones anticipadas de `CONTENT_STATUS.md` como COMPLETE.
7. Fusión y eliminación de rama únicamente bajo autorización del autor.

## 5. Gates del autor (no resolver por cuenta propia)

- Confirmación de fecha exacta del inicio/Academia en 2383, si resulta necesaria.
- Convenciones económicas **jugables** no verificadas: método de acceso a moneda en frontera, remuneración, propiedad y transacción; ninguna se fija aquí.
- Nuevos derechos, códigos penales, reparto competencial, leyes o constituciones no documentados en canon.
- Pueblos/colonias/civilizaciones originales clave, umbrales sociales o imposición de rutinas universales.
- Tratamiento de sucesos futuros y divergencia: mantener historia abierta, sin fijar eventos por llegar.

## 6. Riesgos y coordinación

El plan de desarrollo procedural del universo contiene el Bloque 4 de economía viva pendiente; LORE-04B aportará sus evidencias y reglas contextuales, **no creará ni marcará COMPLETE** ese bloque. ST-ORG-01, F00–F15 y CoreRPG son dependencias de compatibilidad y auditoría, no autorizaciones para modificarlos. No se certificará integración runtime sin prueba independiente. La auditoría E revisará esta distinción.

**Estado del presente documento:** planificación propuesta, lista para revisión; no aprobación creativa ni cierre de LORE-04.
