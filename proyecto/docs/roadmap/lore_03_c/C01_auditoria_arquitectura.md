# C01 — Auditoría de memoria histórica y arquitectura
**Fecha:** 2026-10-27 · **base:** main@9bcf3428b00ad04d59a48e45eb8be77053930094 · **estado:** propuesta documental, pendiente de revisión/fusión.

## Hallazgo y decisión técnica
**No construir una segunda memoria, biografía, historia institucional, grafo social ni estado del mundo.** LORE-03C añade política de enlace, ejemplos y validaciones; los sistemas existentes son dueños de sus respectivos dominios. Las fichas históricas describen hechos y fuentes, nunca son eventos ejecutados ni alteran CoreRPG.

| Dominio y propietario | Contrato existente (ruta real tras ST-ORG-01) | Uso permitido / deuda |
|---|---|---|
| Verdad histórica previa a D | mundo/lore/historical_events/historical_event_contract.json y lore03_a_chronology_index_v0.1.json | Solo referencias por event_id; conservar precisión aproximada |
| Guerra histórica | mundo/lore/conflicts/conflict_definition_contract.json; lore03b_dossier_index_v0.1.json | Referir conflict_id; no duplicar guerras ni tratados |
| Recuerdo individual | sistemas/ai/memory/character_memory_contract.json y character_memory_lifecycle_contract.json | event_ref, sujeto, gist, salience y reconstrucción sin inventar pasado |
| Conocimiento y creencias | sistemas/gameplay/knowledge/character_knowledge_state.json | origen, confianza y clasificación separados de verdad |
| Propagación | sistemas/gameplay/social/social_knowledge_propagation.json | canales verificables; rumor no equivale a hecho |
| Acceso restringido | sistemas/gameplay/knowledge/mission_information_access.json; sistemas/gameplay/records_and_logs/access_and_privacy_rules.json | clearance + necesidad; no filtrar en respuesta de IA |
| Relaciones | sistemas/gameplay/relationships/relationship_state_model.json; relationship_change_provenance_contract.json | shared_history_refs, causalidad, asimetría |
| Parentesco | sistemas/gameplay/relationships/kinship_family_network_contract.json | filiación no presupone conocimiento, cariño ni trato |
| Personalidad | sistemas/gameplay/personality/persistent_personality_profile_contract_v0.1.json; personality_evolution_continuity_contract_v0.1.json | ningún prejuicio ni trauma inherente al evento/especie |
| Ficha e identidad | sistemas/gameplay/characters/character_definition_contract.json; character_runtime_model.json | biografía inicial separada de estado vivo |
| Generador y población | sistemas/gameplay/characters/generated_character_rules.json; sistemas/universe/generation/persistent_population_materialization_rules.json | slots legítimos, identidad y semilla persistentes |
| Vida y simulación social | sistemas/gameplay/social/social_simulation_lod.json | A/B/C varía detalle, no reescribe pasado |
| Trayectoria | sistemas/gameplay/careers/service_record/service_record_model.json | expediente append-only con evidencia |
| Consecuencias | sistemas/gameplay/consequences/world_event_consequence_contract.json y world_state_consequence_event.json | único conducto CoreRPG validado para cambios |
| Fallecimientos | sistemas/gameplay/consequences/death_destruction_mourning_continuity_contract.json | pérdida no borra identidad ni crea duelo obligatorio |
| Registros | sistemas/gameplay/records_and_logs/log_entry_contract.json | testimonio subjetivo distinto del evento |
| Reputación | sistemas/gameplay/reputation/reputation_state_model.json | reputación localizada, no mundial instantánea |
| Civilizaciones | sistemas/universe/generation/civilization_economy_governance_history_contract.json | persistencia de conflicto, migración y memoria colectiva |
| Legado científico | mundo/lore/science/lore02_d_scientific_legacy_policy_v0.1.json | atribución y nombramiento solo autorizados; sin segunda cadena |
| Continuidad | proyecto/docs/decisions/campaign_continuity.md | canon hasta D; historia posterior por guardado |

## Brechas constatadas
1. Falta una relación documental verificable de hecho → posición biográfica → acceso → recuerdo/creencia → posible consecuencia; la añaden C02/C03 y ejemplos, sin nuevos campos runtime obligatorios.
2. La memoria institucional/colectiva necesita políticas editoriales y de visibilidad, no un almacén paralelo.
3. Las historias de terceros y NPC generados necesitan pruebas de edad, fecha, cargo, presencia y confidencialidad, además de las validaciones genéricas ya disponibles.
4. Hay que documentar reservas del canon: Wolf 359 año aproximado 2367 frente a ofensiva Borg 2366 de LORE-01D; ocupación de Bajor sin inicio único exacto; una única Guerra del Dominio; falsa noticia tzenkethi; día/mes D aún sin fijar.
5. Hay documentos de seguimiento antiguos con tres épocas jugables; no corregirlos indiscriminadamente en C ni activar era Pike/Kirk. Es deuda preexistente de regularización transversal.

## Límites duros
**CoreRPG** es única autoridad de WorldState. La IA recibe contexto filtrado; no genera recuerdos, relaciones, reputaciones, promociones o descubrimientos autoritativos al conversar. UE5 solo presenta. Ningún fichero de C se importa automáticamente. Se mantienen intactos contratos propietarios y carpetas ST-ORG-01. No se modifica 03A/03B. Las referencias a CoreRPG son diseño de interoperabilidad, NO verificación del repositorio/runtime CoreRPG.

## Salidas C01
Este inventario constituye la base de decisiones; C02–C07 detallan los huecos y C08 valida referencias, invariantes y casos contra los catálogos reales. La PR permanece sin fusión hasta autorización humana.
