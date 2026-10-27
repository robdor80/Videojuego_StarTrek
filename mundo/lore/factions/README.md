# LORE-01 B — Civilizaciones, instituciones y potencias

**Estado:** investigación documental revisable; **no** simulación política ejecutable.

## Alcance e índice

El índice verificable está en `LORE01_B_civilizations_index_v0.1.json` y referencia 16 expedientes: uno por identidad política/organizativa; el texto está en `monographs/` y las afirmaciones fechadas y sus fuentes en `evidence/`. El catálogo previo `sistemas/gameplay/diplomacy/major_faction_catalogue.json` (ocho potencias) sigue siendo el punto de referencia original del modelo. Este conjunto lo complementa; no duplica ni sustituye los contratos ya aprobados.

## Fronteras de identidad

`species_id` (biología) ≠ `culture_ids` (socialización) ≠ ciudadanía (estatuto jurídico) ≠ gobierno (poder soberano) ≠ organización (adscripción laboral o política) ≠ puesto/mandato (autoridad legal) ≠ convicciones y memoria individual. Ni un klingon ni un cardassiano tienen automáticamente deberes con su gobierno de origen.

## Tipo de entidad

Estados soberanos, potencias y gobiernos internos se estudian separadamente de colectivos especiales, redes no estatales, grupos ilegales, organismos médicos y facciones insurgentes. La **Colectividad Borg** no es una especie; asimila especies biológicas diversas. Su presencia en el juego principal se limita a causalidad y canon TNG. Las civilizaciones Delta del futuro DLC siguen bloqueadas para generación ordinaria, mapas y encuentros; IDEA-0011 no existe en ejecución y el portal no permite llegada Borg a Alfa.

## Qué no hace este repositorio todavía

No define fronteras (LORE-01 C), transacciones/técnicas diplomáticas (D), datos ejecutables definitivos (E) ni modifica un bit del estado vivo de CoreRPG, IA o Unreal. Todas las fichas tienen `automatic_generation_enabled: false` hasta que sistemas futuros consuman reglas autorizadas. La IA no crea leyes, tratados, guerra, cargos ni gobierno a partir de diálogos; solo CoreRPG procesa cambios en World State.

## Lectura y trazabilidad

Usar `mundo/sources/canon_policy.md`, `mundo/sources/provenance_policy.md` y `mundo/sources/source_registry/source_registry.json`. Cada episodio es **anclaje de investigación**, no certificado escena por escena. Distinguir canon ya sucedido antes de la fecha de inicio de campaña de hechos de la serie posteriores, que nunca se fuerzan. Anotaciones de personajes pueden ser falsas en su universo (ejemplo: supuesto golpe tzenkethi de `DS9_THE_ADVERSARY`).

Documentos complementarios: `proyecto/docs/roadmap/lore_01_b_audit_report_v0.1.md`, `mundo/lore/factions/historical_context_v0.1.md` y `mundo/lore/factions/ai_npc_political_context_cases_v0.1.json`.
