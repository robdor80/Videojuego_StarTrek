# Klingon — monografía documental LORE-01 A v0.2

**Especie:** `klingon` · **Disponibilidad:** `MAIN_GAME` · **Motor:** no integrado, solo conocimiento de autoría.  
**Base anterior:** `sistemas/gameplay/species/profiles/klingon_v0.1.json` · **Datos por afirmación:** `mundo/lore/species/evidence/klingon_v0.2.json`.

## A. Evidencias primarias y fuentes de apoyo

| Obra/registro | Qué demuestra (y qué NO) | Prioridad |
|---|---|---|
| `TNG_SINS_OF_THE_FATHER` | Las Casas y la deshonra familiar afectan las instituciones políticas y la identidad de Worf. | SCREEN_CANON |
| `TNG_REUNION` | La sucesión del canciller y la intervención de facciones muestran rivalidades políticas internas. | SCREEN_CANON |
| `TNG_A_MATTER_OF_HONOR` | Riker participa temporalmente en una nave klingon; jerarquía, prácticas navales y desconfianza varían por capitán. | SCREEN_CANON |
| `DS9_THE_WAY_OF_THE_WARRIOR` | Un cambio político desplaza la relación con Federación/Cardassia; la diplomacia depende de fecha. | SCREEN_CANON |
| `DS9_SOLDIERS_OF_THE_EMPIRE` | El mando de Martok ilustra moral de tripulación, prestigio y disciplina sin monopolio de una sola ética del honor. | SCREEN_CANON |
| `DS9_TACKING_INTO_THE_WIND` | La crítica a Gowron y el papel de Martok muestran que honor y legitimidad son objeto de conflicto político. | SCREEN_CANON |
| `ST_OFFICIAL_KLINGON_WORF` | Análisis oficial del ideal personal de Worf y sus tensiones con los actos de otros klingon. | OFFICIAL_REFERENCE |

Estas referencias son **anclajes por episodio**, no verificación exhaustiva escena por escena ni afirmaciones de que todo atributo aparezca literalmente en pantalla. Separar siempre pantalla, referencia oficial, interpretación y añadido del juego.

## B. Biología, anatomía, percepción y medicina

Humanoides de frente y crestas craneales variables en el corpus audiovisual, cuya representación requiere cronología y biblia visual, no un único molde. En algunas escenas se observan resistencia física y fisiología redundante; no extrapolar blindaje natural, inmunidad ni multiplicadores de fuerza fijos.

**Aplicación:** diagnóstico y tratamiento dependen de evaluación clínica individual y privacidad, no de multiplicadores raciales.

## C. Desarrollo, reproducción, pareja, parentesco y vejez

Casas, parentesco, adopción, filiación y sucesión afectan la historia social; Worf criado entre humanos no tiene la misma socialización que un oficial nacido en Qo'noS. Ritos de emparejamiento, vínculos y luto requieren tradición concreta, parentesco válido y fecha. La longevidad global y la gestación no deben inventarse.

**Aplicación:** conservar biografía, vínculos familiares, eventos vitales y estados médicos. La especie no decide relaciones ni condiciones personales.

## D. Sociedad, costumbres, política interna y variaciones

Honor es un vocabulario político, personal y familiar que admite desacuerdos. Religiosidad y referencias a Kahless coexisten con ambición y prácticas oportunistas, y no sustituyen leyes. Los civiles —artistas, científicos, comerciantes, médicos— son indispensables para una civilización, aunque el drama televisivo priorice guerreros y oficiales.

**Aplicación:** separar `species`, educación/cultura, ciudadanía, organización, profesión, opiniones y conducta. La diversidad interna es obligatoria.

## E. Idioma, nombres y comunicación

El klingon tiene vocabulario y escritura de uso cultural verificable; no imponer a un personaje nivel nativo ni convertir palabras rituales en órdenes válidas. El traductor universal facilita diálogo, pero malinterpretar desafío/insulto puede tener consecuencias culturales contextuales.

**Aplicación:** una traducción correcta no concede conocimiento cultural, claves de seguridad ni consentimiento. No crear vocabulario ficticio y etiquetarlo como canon.

## F. Fechas, contacto y cambios del siglo XXIV

El Imperio participa en múltiples fases políticas. La alianza con Federación en TNG no borra la tensión del inicio de DS9 temporada 4 ni concede información anticipada de la guerra. Casas, cancilleres y declaraciones de hostilidad son registros fechados, no constantes raciales.

**Aplicación:** los acontecimientos históricos afectan al estado global solo tras ocurrir legítimamente en la campaña o estar ya establecidos en su punto de partida.

## G. Escenarios concretos para personajes persistentes

1. Un capitán klingon puede ser fiel a su nave y contrario a una decisión de Gowron; son lealtades distintas.
2. La computadora exige documento familiar para responder a qué Casa pertenece un pasajero.
3. Una petición de duelo no inicia batalla sin participantes, ritual vigente, jurisdicción y aceptación.

Para la computadora de a bordo, acceso a conocimiento y datos privados se deriva de autorización y contacto registrado; el director IA no materializa esas escenas sin estado causal.

## H. Incertidumbres explícitas: prohibido rellenar por imaginación

- Tabla médica universal de redundancia de órganos.
- Parentesco y adopción en todas las Casas.
- Cantidad y función de dialectos.
- Evolución exacta de distribución de longevidad.
- Exhaustividad de ritos funerarios y sus excepciones.

**Cautela de canon y conflicto:** Distinguir representación cinematográfica de TOS, TNG y DS9; los cambios visuales no autorizan retcon biológico simplista. Evitar la guerra política transformada en enemistad innata.

## I. Contratos y alcance técnico

- Fuente operativa sigue siendo `sistemas/gameplay/species/profiles/klingon_v0.1.json`; esta ampliación **no cambia** los atributos esperados por CoreRPG.
- Contratos de biología/cultura y ciclo vital: `sistemas/gameplay/species/species_gameplay_contract.md` y `sistemas/gameplay/species/character_lifecycle_contract.json`.
- Los identificadores fuente se resuelven con `mundo/sources/source_registry/source_registry.json`; para hechos críticos se requiere revisión de escena antes de definir números u obligaciones jurídicas.
- Integración de conocimientos de la computadora, NPC y fechas en el runtime **pendiente**; el estado `v0.2` califica investigación escrita, no terminación de la implementación.
