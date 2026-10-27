# LORE-02 D — Ciencia, investigación y fenómenos

**Estado de fase:** COMPLETE documental tras PR #35 fusionada (2026-10-22). `NEEDS_REVIEW` permanece en los JSON para indicar fichas editoriales no homologadas/importables; ningún sistema científico está ejecutándose todavía. Las referencias no son content packs CoreRPG ni objetos UE5.

## Catálogos

- `lore02_d_disciplines_v0.1.json`: especialidades, observables y límites de interpretación.
- `lore02_d_phenomena_atlas_v0.1.json`: familias de fenómenos, ejemplos específicos y riesgos **posibles**, nunca automáticos.
- `lore02_d_research_methods_v0.1.json`: cadena pregunta → medición → alternativas → revisión.
- `lore02_d_facilities_roles_v0.1.json`: perfiles referenciales y referencias a equipos A/B e instalaciones existentes.
- `lore02_d_research_cases_v0.1.json`: diez casos con resultados inciertos y estado de conocimiento parcial.
- `lore02_d_adversarial_scenarios_v0.1.json`: fallos y tentativas de cruzar límites de autoridad.
- `lore02_d_scientific_legacy_policy_v0.1.json`: decisiones de autoría, carrera científica accesible, investigación hasta reforma en astillero y reconocimiento histórico (ejemplo: «Sensores Rise»).

Contrato existente: `scientific_domain_contract.json`. Consumidor de diseño: `sistemas/gameplay/science/sensor_analysis_model.json`, contratos de consola/sensor, `mundo/lore/astrography/`, `mundo/lore/medicine/`. **No duplicarlos ni alterarlos**.

## Principio de investigación

Un fenómeno existe o no en el mundo **independientemente** de un personaje. El observador sólo recibe lecturas derivadas de sensor instalado, calidad, tiempo, permisos y alcance. La IA puede contrastar hipótesis y proponer órdenes; sólo las acciones autorizadas y el CoreRPG podrán transformar el mundo. Un fenómeno no dispara una misión ni amenaza por definición.

Clasificación: `SCREEN_CANON` identifica un caso concreto; `INFERRED` es una familia/generalización; `GAME_ADDITION` representa procedimientos y posibilidades del RPG, no características de pantalla. Los valores numéricos del atlas permanecen `null` donde no están respaldados.

Ver investigación y compatibilidad en `proyecto/docs/roadmap/lore_02_d_science_research_dossier_v0.1.md`.

## Decisiones vinculantes de autoría (22-10-2026)

Catálogo abierto y ciencia autónoma; profundidad opcional para oficiales científicos, con informes comprensibles para capitanes. **No habrá viajes en el tiempo jugables.** Los agujeros de gusano transitables serán raros y deberán referenciar astrogeografía real. **Omega requiere al menos una misión especial escrita en una fase narrativa posterior**, con confidencialidad y autorización; su hallazgo no dispara automáticamente esa misión ni desbloquea tecnología ordinaria. Los avances tecnológicos derivados de investigación podrían acabar en naves, tras revisión, desarrollo de ingeniería, instalación en astillero y pruebas. Las designaciones honoríficas oficiales podrán sobrevivir años y ser citadas por NPC con conocimiento suficiente, pero no se adjudican automáticamente.

Fuente de aprobación: `proyecto/docs/decisions/lore_02_d_author_decisions_v0.1.md`. Ninguna decisión constituye funcionalidad operativa antes de la integración posterior de LORE y CoreRPG.
