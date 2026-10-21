# LORE-02 D — Ciencia, investigación y fenómenos

**Estado:** NEEDS_REVIEW; autoría documental; ningún sistema en ejecución. Las referencias no son content packs CoreRPG ni objetos UE5.

## Catálogos

- `lore02_d_disciplines_v0.1.json`: especialidades, observables y límites de interpretación.
- `lore02_d_phenomena_atlas_v0.1.json`: familias de fenómenos, ejemplos específicos y riesgos **posibles**, nunca automáticos.
- `lore02_d_research_methods_v0.1.json`: cadena pregunta → medición → alternativas → revisión.
- `lore02_d_facilities_roles_v0.1.json`: perfiles referenciales y referencias a equipos A/B e instalaciones existentes.
- `lore02_d_research_cases_v0.1.json`: diez casos con resultados inciertos y estado de conocimiento parcial.
- `lore02_d_adversarial_scenarios_v0.1.json`: fallos y tentativas de cruzar límites de autoridad.

Contrato existente: `scientific_domain_contract.json`. Consumidor de diseño: `gameplay/science/sensor_analysis_model.json`, contratos de consola/sensor, `lore/astrography/`, `lore/medicine/`. **No duplicarlos ni alterarlos**.

## Principio de investigación

Un fenómeno existe o no en el mundo **independientemente** de un personaje. El observador sólo recibe lecturas derivadas de sensor instalado, calidad, tiempo, permisos y alcance. La IA puede contrastar hipótesis y proponer órdenes; sólo las acciones autorizadas y el CoreRPG podrán transformar el mundo. Un fenómeno no dispara una misión ni amenaza por definición.

Clasificación: `SCREEN_CANON` identifica un caso concreto; `INFERRED` es una familia/generalización; `GAME_ADDITION` representa procedimientos y posibilidades del RPG, no características de pantalla. Los valores numéricos del atlas permanecen `null` donde no están respaldados.

Ver investigación y compatibilidad en `docs/roadmap/lore_02_d_science_research_dossier_v0.1.md`.
