# LORE-01 D — Relaciones diplomáticas y geopolítica galáctica

**Estado:** COMPLETE documental — PR #29 fusionada 19-10-2026 (`a1a261f6`). **No** es una máquina diplomática ni integración runtime.

## Lectura recomendada
1. Identidades y clasificación: lore/factions/LORE01_B_civilizations_index_v0.1.json (16 entidades heterogéneas).
2. Índice diplomático: relation_index_v0.1.json; fichas monográficas: dossiers/.
3. Evidencia y cambios: relation_evidence_v0.1.json y historical_events_v0.1.json.
4. Tratados/conflictos: agreements_conflicts_v0.1.json.
5. Separación territorial y derechos: geopolitical_layers_v0.1.json.
6. Uso sin simulación: player_npc_cases_v0.1.json; dudas: open_questions_v0.1.json.
7. Auditoría: docs/roadmap/lore_01_d_diplomatic_audit_v0.1.md.

## Semántica del calendario
Un anclaje con reference_year=2373 NO significa que estuviera en vigor el 1 de enero, ni que se conozca en todo 2373. Cada transición queda ligada a effective_after_event_id. Los acontecimientos en el mismo año requieren orden narrativo concreto. **No** seleccionar automáticamente el último estado anual sin confirmar que el acontecimiento ya sucedió. Una campaña iniciada antes de ese hito NO ejecuta el episodio después por calendario. Los anclajes sirven únicamente como investigación/semilla inicial condicionada a fecha y continuidad; CoreRPG gobierna el futuro emergente.

## Qué se separa
Política oficial y opiniones personales; gobierno y especie; nación y red criminal; ocupación y soberanía; control efectivo y reclamación; zonas neutras y tránsito; conocimiento de cada observador y verdad mundial; rumor de infiltrado y hecho histórico probado. Los estatutos jurídicos nunca se deducen de un icono o mapa de aficionados. Las fechas y valores son documentales, nunca contratos o enums de runtime.

## Restricciones
No importar estos JSON directamente a gameplay/ ni ejecutar reglas en UE5. No sobrescribir gameplay/diplomacy/, gameplay/conflict/, gameplay/navigation/, tratados ni permisos de mando. No crear rutas, coordenadas, polígonos ni fronteras exactas. Sin puerta Borg (IDEA-0011), sin Delta jugable, sin encuentros automáticos del DLC. IA propone e interpreta según su acceso/autoridad; sólo CoreRPG decide cambios del mundo a través de futuros mecanismos autorizados.

## Calidad de evidencia
Los source_refs apuntan al registro existente. Identifican episodio o artículo oficial que respalda el contexto; no certifican cada afirmación a nivel de escena. Las monografías describen por qué evolucionan relaciones, cuál es el detonante, qué no se puede inferir y qué depende del momento histórico. El estado UNKNOWN es preferible a rellenar diplomacia ficticia.
