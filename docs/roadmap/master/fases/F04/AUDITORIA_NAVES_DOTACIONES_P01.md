# F04-P01 — Auditoría de naves, puestos y dotación (11-10-2026)

**Resultado de auditoría del 11-10-2026:** contratos fuente reconciliados; **no** se crea una dotación jugable ni una clase nueva con este documento. **Actualización de decisión autoral 13-10-2026:** Galaxy inspira una **nueva Clase Valhalla** (DEC-0001 aprobada), **sin** matrícula o año de entrada en servicio fijados. Madurez `DISENO_VALIDADO` (auditoría), no `CORE_INTEGRADO`.

## Fuentes reales, sin traslado

| Fuente en `main@6069f6aa` | Auditoría | Decisión |
|---|---|---|
| `gameplay/ship_operations/class_definition_contract.json` (blob `9a94af8f`) | Clase = diseño inmutable, variantes/configuración y capacidades, no una tripulación viva | Una instancia referencia una única definición de clase válida |
| `gameplay/ship_operations/starship_state_model.json` (`eb464e4c`) | Identidad, asignación, mando y manifiesto son estado de nave | Nunca derivar mando actual del catálogo |
| `gameplay/ship_operations/crew_requirement_model.json` (`1f3b2440`) | Entradas: misión, configuración, sistemas instalados, preparación, turnos, requisitos médicos | Generar **plazas exigidas** antes de NPC; desocupadas persisten |
| `gameplay/ship_operations/crew_manifest_model.json` (`3436d19f`) | Tripulantes, civiles, pasajeros, vacantes y guardias separados | No convertir civiles/pasajeros en oficiales |
| `gameplay/ship_operations/bridge_station_model.json` (`41ac95f8`) | Consolas con sistema, cualificaciones, puesto, permiso y ámbito de conocimiento | Tener acceso físico ≠ permiso de orden |
| `lore/starships/classes/class_catalogue_index_v0.1.json` y `core_starship_classes.json` | Catálogo existente que se consulta al instanciar | No introducir clases ficticias en este paso |
| `universe/generation/procedural_ship_crew_watch_schedule_pipeline_v0.1.json` | Diseño → nave persistente → puestos → guardias/personas | Respeta causalidad e identidad; no spawn por cercanía del jugador |
| `tools/generation/generate_starship_instance.py` y su test | Generador determinista de referencia, no World State autoritativo | Reutilizar sin convertir sus resultados en runtime |
| `validation/fixtures/procedural_starship_generation/oberth_science_2372_v0.1/` | Fixture de Oberth: 80 de dotación objetivo, 28/24/24 + 4 de relevo | Caso de regresión; los recuentos no son universales |

## Flujo operativo necesario

1. Resolver necesidad causal de nave, operador, época, clase, variante, capacidades y misión; reservar identidad.
2. Calcular cobertura de seguridad y operación por departamento y estación, diferenciando puestos **continuos**, **diurnos**, **localizados** y **relevo**.
3. Crear `crew_slot_id` estables: puesto, departamento, cualificación, habilitación, cobertura temporal y prioridad. No rellenar vacantes con personajes improvisados.
4. Asignar personas *existentes* o crear entidades persistentes mediante el materializador de población **cuando** el mundo autoritativo lo permita. Conservar `character_id`.
5. Generar guardias individuales, responsables reales, sustituciones e incidencias. Los civiles y pasajeros solo acceden a funciones autorizadas expresamente.
6. Registrar modificaciones de manifiesto, destino, bajas y relevos como cambios causales auditables; no regenerar la nave tras recargar.

## Invariantes y negativos

- `class_id` no concede personal, buques auxiliares, habitaciones o sistemas operativos por arte de magia; la configuración de la nave debe soportarlos.
- `crew_reference` no es ni el manifiesto, ni la fuerza disponible, ni la guardia actual.
- Misma persona **no** cubre simultáneamente dos estaciones incompatibles, aunque tenga doble cualificación.
- Si falla un mínimo de guardia, se informa de déficit/riesgo; no se autocrea un sustituto.
- **DEC-0001 RESUELTA:** Galaxy/Enterprise-D se elige como referencia de la **Clase Valhalla**, nueva clase propia y no actualización Galaxy. Sovereign y Odyssey no son ya candidatas a base de Valhalla, pero permanecen disponibles como referencias/naves NPC cuando su modelado y cronología se validen. La decisión no modifica automáticamente el catálogo, los manifiestos, el fixture de Oberth ni las capacidades implementadas.

**Prueba P01:** reutilización de fuentes comprobada en GitHub. Casos ejecutables de plazas y ausencias en `tools/validation/f04_reference.py` / `test_f04_reference.py`. **NO_EJECUTADO:** validación con Core/UE5 y generación de NPC runtime.
