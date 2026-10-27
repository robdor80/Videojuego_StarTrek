# B04 — Acuerdos, cambios de postura y salidas pacíficas

## Registro existente: reutilización por ID

Se enlaza a los **siete** acuerdos ya conservados en `lore/diplomacy/agreements_conflicts_v0.1.json`:

| ID existente | Función histórica | Precaución |
|---|---|---|
| `organian_peace_treaty` | Intervención restrictiva histórica | No impone buena voluntad universal |
| `khitomer_accords` | Marco de paz entre Federación y Klingon | Puede coexistir con una ruptura política posterior |
| `federation_cardassian_border_settlement` | Reajuste fronterizo y desmilitarización | Desplazamientos coloniales y agravios sobreviven |
| `bajoran_dominion_nonaggression` | Neutralidad de Bajor | No implica pertenecer al Dominio |
| `romulan_dominion_nonaggression` | Neutralidad romulana inicial | No congela entrada posterior en guerra |
| `tholian_dominion_nonaggression` | Acuerdo de no agresión referido oficialmente | No inventar cláusulas no documentadas |
| `treaty_of_bajor` | Rendición y término de guerra | No borra pérdidas ni determina por sí solo todos los arreglos |

## Modelo documental de negociación (no sistema ejecutable)

Cualquier supuesto de negociación debe describir: contendientes acreditados; reclamación y capacidad política; representación legítima; terceros mediadores; condiciones negociables; garantías verificables; medidas humanitarias; implementación y supervisión; posibles incumplimientos. No se añade JSON runtime nuevo: existen `ceasefire_armistice_peace_rules_v0.1.json` y `war_authority_rules_of_engagement_contract_v0.1.json`.

## Cambios temporales dentro de una sola guerra

Federación y Klingon colaboran, rompen cooperación por invasión cardassiana y vuelven a cooperar frente al Dominio. Romulanos pasan de no agresión a coalición. Cardassia entra aliada del Dominio, pero hay una resistencia y unidades que cambian de lado en 2375. La alianza nunca se hereda automáticamente por **especie**, sino por autoridad/facción/contexto y fecha.

## Casos pacíficos para juego emergente

Pacto de observadores, verificación de cargamentos, inspección consentida, retirada bilateral, arbitraje sobre accesos, pasillos de evacuación y alto el fuego territorial. Cada acuerdo deberá ser un evento estructurado del futuro WorldState. Un comunicado de IA que diga «se firmó la paz» no puede crear el tratado real.