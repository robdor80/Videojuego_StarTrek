# D06 — Continuidad de personas, naves e instituciones

## 1. Identidad ≠ asignación ≠ rango ≠ ubicación
El mismo `character_id` vive una carrera, mantiene su identidad visual y sus anclas biográficas, pero puede cambiar puesto, rango, división, uniforme, relaciones y localización. Los eventos de expediente (`service_record_model.json`) son append-only: un ascenso requiere méritos, vacante/procedimiento y autoridad, no solo años; mando interino no equivale a ascenso. Cada traslado cierra una asignación anterior y abre otra, con fechas compatibles, desplazamiento y disponibilidad. Las naves mantienen `vessel_entity_id` durante reparaciones/refits; cambios de clase y herencias de nombre o matrícula no son reemplazo silencioso de identidad.

## 2. Escenario 2383 — roles iniciales
Picard es **almirante**, no capitán al mando fijo de la Valhalla. Riker dirige la **USS Titan**, sin asignación arbitraria a Sovereign/Odyssey. Janeway es almirante. La Forge mantiene carrera conocida sin fabricar destino exacto. Rómulo existe. Cada personaje canónico conserva su pasado confirmado, pero no está contratado para representar episodios futuros.

## 3. Academia y cronología alternativa
Entre entrada de 2383 y graduación aproximada 2387, instructores pueden retirarse o cambiar departamento; cadetes pueden graduarse, retrasarse o suspender según reglas académicas; tripulaciones pueden rotar y oficiales asumir vacantes. Un alumno no es automáticamente alférez por agotar cuatro años, ni se le asigna Valhalla al graduarse: esta es una opción plausible condicionada a sus méritos, disponibilidad real de la nave, plaza y proceso de la Flota. Si la clase entra en servicio durante 2383, la falta de mes/día impide fijar qué curso coincidirá con su botadura exacta.

## 4. Fallecimiento, retiro, desaparición y reputación
Un fallecimiento verificado finaliza servicio activo y puede originar vacantes, expedientes, memorias y medidas organizativas **a través de eventos**; no elimina la identidad ni garantiza reacción emocional uniforme. Desaparecido no equivale a muerto sin prueba. Un ascenso conocido por la institución no es conocimiento universal: un personaje lejano puede mantener una noticia anticuada. La promoción a LOD A no reescribe nunca el pasado de quien ya existía en LOD C.

## 5. Integridad de identidades
- `entity_id` estable, linaje persistente y semilla no reinterpretada tras save/load/LOD.
- `rank_ref`, `position_ref`, `assignment_ref` diferenciados y vinculados a autoridad temporal.
- Naves: construcción, asignaciones, refit, reparaciones y pérdida en historia de **la misma** entidad.
- Organizaciones: continuidad de identidad, cambios de gobierno/mando registrados; segregación, fusión o sucesión con linaje explícito.
- El filtro de IA nunca revela traslados, secretos o defunciones sin `knowledge_state` y canales válidos.
- Un desenlace posterior al corte no se aplica a un personaje solo porque figure en Memory Alpha o una película.
