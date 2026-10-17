# Bajorianos — monografía documental LORE-01 A v0.2

**Especie:** `bajoran` · **Disponibilidad:** `MAIN_GAME` · **Motor:** no integrado, solo conocimiento de autoría.  
**Base anterior:** `gameplay/species/profiles/bajoran_v0.1.json` · **Datos por afirmación:** `lore/species/evidence/bajoran_v0.2.json`.

## A. Evidencias primarias y fuentes de apoyo

| Obra/registro | Qué demuestra (y qué NO) | Prioridad |
|---|---|---|
| `DS9_EMISSARY` | Salida de la ocupación, gobierno provisional y fe en los Profetas crean un contexto social frágil. | SCREEN_CANON |
| `DS9_DUET` | La memoria de los campos y la ocupación afecta a supervivientes de manera muy distinta. | SCREEN_CANON |
| `DS9_RECKONING` | Religión, Kai y debate sobre los Profetas afectan política y percepciones de la población. | SCREEN_CANON |
| `DS9_HEART_OF_STONE` | Kira representa a una oficial con historia de Resistencia, pero no toda la sociedad tiene ese servicio. | SCREEN_CANON |
| `DS9_NECESSARY_EVIL` | Los registros de Terok Nor permiten distinguir una sociedad bajo control extranjero de la estación administrada por Bajor después. | SCREEN_CANON |
| `ST_OFFICIAL_GET_TO_KNOW_WORLDS` | Referencia oficial a Bajor como mundo significativo para el desarrollo político/cultural de DS9. | OFFICIAL_REFERENCE |

Estas referencias son **anclajes por episodio**, no verificación exhaustiva escena por escena ni afirmaciones de que todo atributo aparezca literalmente en pantalla. Separar siempre pantalla, referencia oficial, interpretación y añadido del juego.

## B. Biología, anatomía, percepción y medicina

Humanoides diferenciados visualmente por pliegues o crestas nasales de variación individual. El uso religioso de oreja/pagh no establece que el sentido físico mida fe o virtud. El ciclo vital y la medicina requieren datos personales, sin características heroicas innatas por la ocupación.

**Aplicación:** diagnóstico y tratamiento dependen de evaluación clínica individual y privacidad, no de multiplicadores raciales.

## C. Desarrollo, reproducción, pareja, parentesco y vejez

Familias, pérdida, refugio, comunidades agrícolas y orfandad tras la ocupación son contextos vitales posibles. No forzar trauma a toda persona bajorana ni asignar participación en Resistencia por edad. La identidad religiosa de un hijo no viene determinada por nacimiento.

**Aplicación:** conservar biografía, vínculos familiares, eventos vitales y estados médicos. La especie no decide relaciones ni condiciones personales.

## D. Sociedad, costumbres, política interna y variaciones

El culto a los Profetas, posiciones del Kai y Vedeks, prácticas de oración y festividades pueden ser centrales para muchos, pero también existen escépticos, políticos seculares y posturas divergentes. Su orden de nombre, comunidad, profesión y pertenencia a milicias se deben tratar como información específica.

**Aplicación:** separar `species`, educación/cultura, ciudadanía, organización, profesión, opiniones y conducta. La diversidad interna es obligatoria.

## E. Idioma, nombres y comunicación

Bajorano figura en catálogo; la traducción de textos religiosos puede requerir interpretación cultural, no solo diccionario. Nombres y títulos no son una prueba automática de ideología. No inventar oraciones completas supuestamente canónicas.

**Aplicación:** una traducción correcta no concede conocimiento cultural, claves de seguridad ni consentimiento. No crear vocabulario ficticio y etiquetarlo como canon.

## F. Fechas, contacto y cambios del siglo XXIV

Ocupación termina en 2369; reconstrucción, gobiernos y contactos con Federación se desarrollan en DS9. La función religiosa de Sisko como Emisario depende de eventos de DS9 y del conocimiento del personaje; no ha ocurrido para todo pasado del siglo XXIV.

**Aplicación:** los acontecimientos históricos afectan al estado global solo tras ocurrir legítimamente en la campaña o estar ya establecidos en su punto de partida.

## G. Escenarios concretos para personajes persistentes

1. Un agricultor podría querer autonomía agrícola sin estar afiliado a partido alguno.
2. Una antigua resistente puede desconfiar de un cardassiano concreto, pero no está obligada a atacar a cada cardassiano.
3. La computadora no revela una confesión pastoral ni el pasado clandestino de un feligrés.

Para la computadora de a bordo, acceso a conocimiento y datos privados se deriva de autorización y contacto registrado; el director IA no materializa esas escenas sin estado causal.

## H. Incertidumbres explícitas: prohibido rellenar por imaginación

- Expectativa de vida general y fisiología reproductiva.
- Diversidad de ritos entre comunidades.
- Censo y territorios agrícolas posocupación.
- Religiosidad de cada ciudadano.
- Historia de participación individual en Resistencia.

**Cautela de canon y conflicto:** Profetas como entidad observada y creencia bajorana deben presentarse según observador; no etiquetar religión como capacidad biológica y no imponer fatalismo histórico.

## I. Contratos y alcance técnico

- Fuente operativa sigue siendo `gameplay/species/profiles/bajoran_v0.1.json`; esta ampliación **no cambia** los atributos esperados por CoreRPG.
- Contratos de biología/cultura y ciclo vital: `gameplay/species/species_gameplay_contract.md` y `gameplay/species/character_lifecycle_contract.json`.
- Los identificadores fuente se resuelven con `sources/source_registry/source_registry.json`; para hechos críticos se requiere revisión de escena antes de definir números u obligaciones jurídicas.
- Integración de conocimientos de la computadora, NPC y fechas en el runtime **pendiente**; el estado `v0.2` califica investigación escrita, no terminación de la implementación.
