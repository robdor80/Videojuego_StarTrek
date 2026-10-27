# Cardassianos — monografía documental LORE-01 A v0.2

**Especie:** `cardassian` · **Disponibilidad:** `MAIN_GAME` · **Motor:** no integrado, solo conocimiento de autoría.  
**Base anterior:** `sistemas/gameplay/species/profiles/cardassian_v0.1.json` · **Datos por afirmación:** `mundo/lore/species/evidence/cardassian_v0.2.json`.

## A. Evidencias primarias y fuentes de apoyo

| Obra/registro | Qué demuestra (y qué NO) | Prioridad |
|---|---|---|
| `TNG_THE_WOUNDED` | Militares cardassianos y oficiales federados negocian consecuencias de conflictos fronterizos. | SCREEN_CANON |
| `TNG_CHAIN_OF_COMMAND_PART_I` | Las tensiones estratégicas con la Federación condicionan trato a prisioneros y mandos. | SCREEN_CANON |
| `DS9_DUET` | Marritza y Kira confrontan culpa, responsabilidad y memoria de la ocupación de Bajor. | SCREEN_CANON |
| `DS9_NECESSARY_EVIL` | La vida en Terok Nor durante la ocupación distingue administraciones, civiles y coerción institucional. | SCREEN_CANON |
| `DS9_DEFIANT` | La cadena de mando y la Orden Obsidiana muestran conspiración y agendas que divergen de la diplomacia pública. | SCREEN_CANON |
| `DS9_THE_DIE_IS_CAST` | Operaciones de la Orden Obsidiana tienen consecuencias históricas, y no describen a todos los habitantes de Cardassia. | SCREEN_CANON |
| `DS9_THE_DOGS_OF_WAR` | La resistencia interna de Damar frente al Dominio modifica la legitimidad de facciones. | SCREEN_CANON |

Estas referencias son **anclajes por episodio**, no verificación exhaustiva escena por escena ni afirmaciones de que todo atributo aparezca literalmente en pantalla. Separar siempre pantalla, referencia oficial, interpretación y añadido del juego.

## B. Biología, anatomía, percepción y medicina

Humanoides de crestas y placas craneocervicales características; pigmentación variable por individuo. Su fisiología no justifica resistencia a tortura, fuerza o metabolismo constantes sin fuente médica y caso individual.

**Aplicación:** diagnóstico y tratamiento dependen de evaluación clínica individual y privacidad, no de multiplicadores raciales.

## C. Desarrollo, reproducción, pareja, parentesco y vejez

La familia, la obligación con hijos y la continuidad social se presentan como valores relevantes para personajes y discursos cardassianos. No fijar convivencia, filiación biológica, longevidad ni fertilidad generales por declaraciones de oficiales concretos.

**Aplicación:** conservar biografía, vínculos familiares, eventos vitales y estados médicos. La especie no decide relaciones ni condiciones personales.

## D. Sociedad, costumbres, política interna y variaciones

La retórica del Estado y las instituciones militares, la Orden Obsidiana, académicos, comerciantes, familias y disidentes forman contextos divergentes. La ocupación de Bajor es un hecho histórico estructural, pero culpa criminal individual necesita hechos probados. Distinción entre vida civil en Cardassia y guarniciones exteriores.

**Aplicación:** separar `species`, educación/cultura, ciudadanía, organización, profesión, opiniones y conducta. La diversidad interna es obligatoria.

## E. Idioma, nombres y comunicación

Cardassiano no consta desarrollado en el catálogo inicial; su existencia como lengua no permite inventar sintaxis militar, códigos o pronunciación. Los registros pueden incluir procedimientos de clasificación; conocer una lengua no concede claves de acceso.

**Aplicación:** una traducción correcta no concede conocimiento cultural, claves de seguridad ni consentimiento. No crear vocabulario ficticio y etiquetarlo como canon.

## F. Fechas, contacto y cambios del siglo XXIV

Fin de ocupación de Bajor anterior a la llegada de Sisko; tensiones fronterizas preceden a la guerra del Dominio; alianza cardassiana con Dominio en 2373, insurrección final en 2375. Ningún capítulo futuro se impone retrospectivamente.

**Aplicación:** los acontecimientos históricos afectan al estado global solo tras ocurrir legítimamente en la campaña o estar ya establecidos en su punto de partida.

## G. Escenarios concretos para personajes persistentes

1. Exoficial de ocupación requiere historial específico antes de enfrentarse a testigos bajoranos.
2. Un comerciante cardassiano no controla la Orden Obsidiana por ciudadanía.
3. Pruebas judiciales e interrogatorio no se sustituyen por conocimiento del narrador sobre el canon.

Para la computadora de a bordo, acceso a conocimiento y datos privados se deriva de autorización y contacto registrado; el director IA no materializa esas escenas sin estado causal.

## H. Incertidumbres explícitas: prohibido rellenar por imaginación

- Distribución de edades, natalidad y esperanza de vida.
- Sistema de educación regional y dialectos.
- Variabilidad médica de fenotipos y adaptación climática.
- Censos civiles bajo cada gobierno.
- Quién participó individualmente en abusos sin historial.

**Cautela de canon y conflicto:** Evitar unir estado militar, población civil y etnia; evitar presentar liberación, guerra y ocupación como hechos idénticos simultáneos.

## I. Contratos y alcance técnico

- Fuente operativa sigue siendo `sistemas/gameplay/species/profiles/cardassian_v0.1.json`; esta ampliación **no cambia** los atributos esperados por CoreRPG.
- Contratos de biología/cultura y ciclo vital: `sistemas/gameplay/species/species_gameplay_contract.md` y `sistemas/gameplay/species/character_lifecycle_contract.json`.
- Los identificadores fuente se resuelven con `mundo/sources/source_registry/source_registry.json`; para hechos críticos se requiere revisión de escena antes de definir números u obligaciones jurídicas.
- Integración de conocimientos de la computadora, NPC y fechas en el runtime **pendiente**; el estado `v0.2` califica investigación escrita, no terminación de la implementación.
