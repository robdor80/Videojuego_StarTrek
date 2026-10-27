# Ferengi — monografía documental LORE-01 A v0.2

**Especie:** `ferengi` · **Disponibilidad:** `MAIN_GAME` · **Motor:** no integrado, solo conocimiento de autoría.  
**Base anterior:** `sistemas/gameplay/species/profiles/ferengi_v0.1.json` · **Datos por afirmación:** `mundo/lore/species/evidence/ferengi_v0.2.json`.

## A. Evidencias primarias y fuentes de apoyo

| Obra/registro | Qué demuestra (y qué NO) | Prioridad |
|---|---|---|
| `TNG_THE_LAST_OUTPOST` | Primeros contactos con Ferengi exhiben rivalidad comercial y prejuicios de ambas partes. | SCREEN_CANON |
| `DS9_RULES_OF_ACQUISITION` | Pel oculta su identidad para trabajar en un ámbito comercial excluyente; muestra resistencia a normas de género. | SCREEN_CANON |
| `DS9_FAMILY_BUSINESS` | Ishka demuestra actividad mercantil femenina pese a prohibiciones institucionales. | SCREEN_CANON |
| `DS9_PROFIT_AND_LACE` | Las reformas sobre vestir y actividad económica de mujeres causan conflicto político interno. | SCREEN_CANON |
| `DS9_THE_DOGS_OF_WAR` | La sucesión del Gran Nagus y reformas ilustran cambio, no ley eterna. | SCREEN_CANON |
| `DS9_THE_ASCENT` | Quark y Odo muestran negociación, rivalidad y colaboración entre individuos de normas diferentes. | SCREEN_CANON |
| `ST_OFFICIAL_ISHKA` | Historia oficial de cambios promovidos por Ishka en derechos de mujeres ferengi. | OFFICIAL_REFERENCE |

Estas referencias son **anclajes por episodio**, no verificación exhaustiva escena por escena ni afirmaciones de que todo atributo aparezca literalmente en pantalla. Separar siempre pantalla, referencia oficial, interpretación y añadido del juego.

## B. Biología, anatomía, percepción y medicina

Humanoides con pabellones auriculares voluminosos, odontología y morfología craneal reconocibles; el lóbulo no mide inteligencia empresarial ni moralidad. Rasgos sensoriales asociados deben permanecer cualitativos hasta contar con valores médicos específicos.

**Aplicación:** diagnóstico y tratamiento dependen de evaluación clínica individual y privacidad, no de multiplicadores raciales.

## C. Desarrollo, reproducción, pareja, parentesco y vejez

Familia, herencia, negocios, crianza y expectativas comerciales pueden influir en trayectorias de individuos como Quark, Rom, Nog e Ishka, que difieren mucho entre sí. No deducir longevidad, edad legal o biología reproductiva a partir de las reglas mercantiles.

**Aplicación:** conservar biografía, vínculos familiares, eventos vitales y estados médicos. La especie no decide relaciones ni condiciones personales.

## D. Sociedad, costumbres, política interna y variaciones

Las Reglas de Adquisición son un cuerpo de tradición social y económica, no un código informático que obligue a cualquier ferengi a maximizar beneficio. Normas patriarcales históricas se cuestionan y reforman a lo largo de DS9; existen agentes morales divergentes, carreras de ingeniería y acceso a la Flota.

**Aplicación:** separar `species`, educación/cultura, ciudadanía, organización, profesión, opiniones y conducta. La diversidad interna es obligatoria.

## E. Idioma, nombres y comunicación

Ferengi está en el catálogo; no atribuir automáticamente competencia contractual, comprensión de leyes financieras ni descifrado de cláusulas. La traducción exacta de un contrato exige terminología y jurisdicción.

**Aplicación:** una traducción correcta no concede conocimiento cultural, claves de seguridad ni consentimiento. No crear vocabulario ficticio y etiquetarlo como canon.

## F. Fechas, contacto y cambios del siglo XXIV

El tratamiento jurídico de mujeres en Ferenginar cambia explícitamente durante las últimas temporadas de DS9. Un NPC de 2364 no debería citar decretos posteriores, y otro de 2375 no debería actuar como si la reforma jamás existió, salvo contexto local.

**Aplicación:** los acontecimientos históricos afectan al estado global solo tras ocurrir legítimamente en la campaña o estar ya establecidos en su punto de partida.

## G. Escenarios concretos para personajes persistentes

1. Ferengi comerciante puede valorar honestidad o familia más que una transacción concreta.
2. Un cadete ferengi como Nog necesita expediente de Flota, no se le excluye por especie.
3. Un contrato fraudulento necesita acto, prueba y regulación: no basta 'ser ferengi'.

Para la computadora de a bordo, acceso a conocimiento y datos privados se deriva de autorización y contacto registrado; el director IA no materializa esas escenas sin estado causal.

## H. Incertidumbres explícitas: prohibido rellenar por imaginación

- Biología auditiva cuantitativa.
- Esperanza de vida y parámetros médicos reproductivos.
- Lenguaje de contratos regionales.
- Extensión efectiva de las reformas por regiones y fechas.
- Censo de Ferenginar y clases sociales.

**Cautela de canon y conflicto:** No convertir sátira económica en rasgo racial; evitar leyes ferengi de 2375 como atemporales. La cuestión de género debe documentar prácticas y reformas sin endorsar ni universalizar opresión.

## I. Contratos y alcance técnico

- Fuente operativa sigue siendo `sistemas/gameplay/species/profiles/ferengi_v0.1.json`; esta ampliación **no cambia** los atributos esperados por CoreRPG.
- Contratos de biología/cultura y ciclo vital: `sistemas/gameplay/species/species_gameplay_contract.md` y `sistemas/gameplay/species/character_lifecycle_contract.json`.
- Los identificadores fuente se resuelven con `mundo/sources/source_registry/source_registry.json`; para hechos críticos se requiere revisión de escena antes de definir números u obligaciones jurídicas.
- Integración de conocimientos de la computadora, NPC y fechas en el runtime **pendiente**; el estado `v0.2` califica investigación escrita, no terminación de la implementación.
