# Persistent Personality System

Sistema de personalidad persistente para NPC.

## Regla central

**La IA interpreta una personalidad existente; no la inventa en cada conversación.**

Una vez resuelto `personality_profile_id`, queda vinculado permanentemente a `entity_id`.

## Componentes

- `persistent_personality_profile_contract_v0.1.json` — estructura del núcleo.
- `npc_personality_assignment_contract_v0.1.json` — tiers A/B/C y promoción.
- `abstract_personality_trait_lexicon_v0.1.json` — vocabulario abstracto.
- `procedural_personality_recipe_library_v0.1.json` — 46 recetas iniciales originales.
- `species_culture_expression_modifiers_v0.1.json` — expresión cultural/especie.
- `personality_evolution_continuity_contract_v0.1.json` — evolución sin reroll.
- `persistent_personality_generation_pipeline_v0.1.json` — orden de resolución.
- `../../ai/personality/ai_personality_dialogue_context_contract_v0.1.json` — bloque para IA.

## Investigación canónica

- `../../research/personality/star_trek_personality_research_sources_v0.1.json`
- `../../research/personality/star_trek_character_trait_corpus_v0.1.json`

Los personajes canónicos son **muestras de investigación**, nunca perfiles procedurales.

## Fórmula de expresión

`PERSONALIDAD PERSISTENTE + CULTURA/EDUCACIÓN + INSTITUCIÓN + RELACIÓN + ESTADO ACTUAL + ESCENA = EXPRESIÓN ACTUAL`

## Tiers

Los tiers de personalidad A/B/C son distintos de cualquier tier de población/materialización.

- **A**: NPC principal; personalidad escrita a mano preferente.
- **B**: NPC interactivo persistente; personalidad procedural completa.
- **C**: fondo; puede conservar solo semilla latente hasta una posible promoción.

C→B y B→A no rerollean identidad.
