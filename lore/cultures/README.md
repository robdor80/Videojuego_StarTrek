# Culturas — índice autoritativo

Este directorio contiene la capa cultural del universo procedural.

## Principio

**Especie ≠ cultura ≠ ciudadanía ≠ organización ≠ profesión ≠ personalidad.**

La cultura aporta normas aprendidas, expectativas, referencias y probabilidades sociales. No obliga a un individuo a comportarse de una forma concreta.

## Contrato

- `cultural_profile_contract_v0.1.json`
- `gameplay/species/culture_socialization_contract.json`

## Perfiles de profundidad

### Fundadores / Federación

- `profiles/HUMAN_FEDERATION_CULTURAL_COMPOSITION_v0.1.json`
- `profiles/VULCAN_CULTURAL_PROFILE_v0.1.json`
- `profiles/ANDORIAN_AENAR_CULTURAL_PROFILES_v0.1.json`
- `profiles/TELLARITE_CULTURAL_PROFILE_v0.1.json`

### Culturas mayores

- `profiles/KLINGON_CULTURAL_PROFILE_v0.1.json`
- `profiles/ROMULAN_CULTURAL_PROFILE_v0.1.json`
- `profiles/CARDASSIAN_CULTURAL_PROFILE_v0.1.json`
- `profiles/BAJORAN_CULTURAL_PROFILE_v0.1.json`
- `profiles/FERENGI_CULTURAL_PROFILE_v0.1.json`
- `profiles/TRILL_CULTURAL_PROFILE_v0.1.json`
- `profiles/BETAZOID_CULTURAL_PROFILE_v0.1.json`
- `profiles/DOMINION_CULTURAL_HIERARCHY_PROFILE_v0.1.json`

## Resúmenes operativos

- `founding_species_interaction_profiles.json`
- `major_species_interaction_profiles.json`

Esos archivos son resúmenes para sistemas de interacción. La profundidad cultural autoritativa vive en `profiles/`.

## Reglas

- Un personaje puede tener varias `culture_refs`.
- El planeta natal no decide una cultura completa.
- La especie no adjunta automáticamente una cultura.
- Familia, hogar, religión, ciudadanía, organización, profesión y cultura son estados separados.
- Los huecos de canon permanecen como `unknown`.
- La IA puede expresar cultura conocida, pero no inventar matrimonios, Casas, cargos, parentesco, fe, obligaciones o autoridad.
- El contenido cultural que afecta a formación de oficiales se deriva hacia Academia mediante `gameplay/careers/academy_path/cultural_operations_reference_v0.1.json`.
