# C07 — Integración documental: NPC, carreras, contexto IA y LOD

## Itinerario conceptual
1. **Precampaña:** resolver historia hasta fecha `D` solo para hechos *estrictamente anteriores*; mismo año sin orden temporal probado se mantiene `UNRESOLVED_SAME_YEAR`.
2. **Personaje canónico:** cargar definición y hechos canónicos disponibles por fecha, sin completar biografías desconocidas; no extrapolar destinos posteriores a D.
3. **Personaje procedimental:** reservar plaza de población/plantilla conforme al generador; asignar identidad persistente; validar origen, edad, formación, destino, temporalidad y contexto; antecedentes interesantes no obligatorios.
4. **Semillas justificadas:** cargar conocimiento, personalidad, relaciones y recuerdos pertinentes **solo tras validar** su procedencia. No generar amistad porque dos NPC comparten destino o fama.
5. **Vivo:** solo CoreRPG aplica los cambios de estado. La IA recibe proyección filtrada de información y recuerdos; puede expresar dudas, contradicciones y desconocimiento.
6. **Persistencia:** guardar/cargar y LOD A/B/C no alteran ID, hechos, recuerdos relevantes ni relaciones; puede variar detalle simulado. Eventos futuros reales van al log de campaña, no al canon.
7. **Información de terceros:** noticias requieren comunicación/acceso; el rumor no promueve automáticamente una afirmación a verdad.

## Mapa de consumos (propietario → lector)
| Propietario | Lectura documental prevista |
|---|---|
| LORE-03A/LORE-01D eventos y 03B conflictos | antecedentes y referencias, no scripts |
| `character_definition_contract` y `character_runtime_model` | definición y estado actual por identidad |
| `persistent_population_materialization_rules` | plaza, formación y persistencia de NPC |
| `character_memory_contract` y `character_knowledge_state` | recuerdo y conocimiento actor-específico |
| `relationship_state_model` y `kinship_family_network_contract` | vínculos persistentes con justificación |
| `social_simulation_lod` | detalle de simulación, no existencia de pasado |
| `world_event_consequence_contract` | cambios autorizados por CoreRPG |
| `ai/knowledge_filters` y `ai/lore_context` | proyectores futuros; directorios reservados hoy |

## Protección de fuentes y privacidad
No inyectar `World Truth` completo en prompts de un NPC. Filtrar documentos institucionales y médicos **antes** de la llamada de IA. Un personaje puede ignorar un informe que el jugador conoce; no revelar secretos mediante citas de origen, resúmenes, traducciones o búsqueda. Lo clasificado no se desclasifica retroactivamente por subir de rango.

## NPC autónomos, jamás ficción sin causa
Un personaje puede investigar, viajar, ascender, formar familia o descubrir algo fuera de pantalla cuando el simulador real deje trazas de tiempo, contacto, recursos y autoridad; `LOD=C` no permite inventar episodios destacados al recuperar al personaje. Los casos del dossier son **tests editoriales**, no NPC materializados o un nuevo motor.

## Dependencias aplazadas
Proyección concreta Host↔CoreRPG, índices de recuperación, migraciones runtime y rendimiento se auditarán en una fase de implementación posterior. Aquí no se afirma que esos adaptadores funcionen en producción.
