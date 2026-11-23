# H06-P06-A2 · Factibilidad de la madurez jugable nativa

**Fecha** 14-11-2026. **Base** `bcc6f77e8491677f573ebbde6a1964a19f9e5d1d` (PR #153). **Propietario** F10.

## IMPLEMENTADO

El validador nativo de la PR #152 ya separa las reglas objetivas, la revisión semántica y la comprobación de vigencia del recibo privado. Su generador incorpora los perfiles biológicos, el contrato de creación y la campaña del contrato de candidatos. El mismo generador puede compilar la tabla de madurez en el binario y vincular sus contenidos a la huella de las reglas.

- El [contrato de madurez](../../../../sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json) aporta los umbrales en años terrestres, los casos especiales y la disponibilidad de las 25 especies. La [decisión autoral](H06_P06_A_MADUREZ_ESPECIES_APROBADA_2026-11-14.md) explica su aplicación a protagonistas.
- El [contrato de creación](../../../../sistemas/gameplay/character_creation/character_creation_contract_v1_0.json) exige adultez equivalente; el [contrato de biología](../../../../sistemas/gameplay/species/species_biology_contract.json) exige usar perfiles de especie y estado individual. La tabla jugable complementa esos controles.
- El [contrato de candidatos](../../../../sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json) confirma el escenario Academia, la era TNG/DS9/Voyager y el año 2383. La [interfaz de biografía](../../../../sistemas/gameplay/character_creation/f10_biography_validation_interface_v0.1.json) exige ambas puertas y procedencia interna antes de un futuro commit.

## PROBADO

El checkout de partida coincide con el merge de la PR #153. La configuración HOST exige un checkout limpio del CoreRPG fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`. El flujo HOST existente ofrece Windows, Linux, Clang con ASan/UBSan y Release sin pruebas para los dos sistemas. La suite F10 de referencia fija por separado los valores exactos aprobados.

## BLOQUEADO

Faltan una autoridad F10 aprobada para autenticar evidencia individual y un proveedor real de revisión semántica. Los tres casos especiales requieren reglas de desarrollo propias. La disponibilidad del DLC Delta queda cerrada en la campaña principal.

## PENDIENTE

Quedan por decidir el día y el mes de inicio. Los nacimientos en el año límite se mantienen en revisión. La auditoría independiente decide la integración de este corte. El candidato real y la admisión académica siguen sujetos a los contratos de sus respectivas operaciones.
