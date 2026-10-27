# Romulanos — monografía documental LORE-01 A v0.2

**Especie:** `romulan` · **Disponibilidad:** `MAIN_GAME` · **Motor:** no integrado, solo conocimiento de autoría.  
**Base anterior:** `sistemas/gameplay/species/profiles/romulan_v0.1.json` · **Datos por afirmación:** `mundo/lore/species/evidence/romulan_v0.2.json`.

## A. Evidencias primarias y fuentes de apoyo

| Obra/registro | Qué demuestra (y qué NO) | Prioridad |
|---|---|---|
| `TOS_BALANCE_OF_TERROR` | La similitud visual con vulcanos se reconoce en un contexto de enfrentamiento e incertidumbre. | SCREEN_CANON |
| `TNG_UNIFICATION_I` | Spock contacta con un movimiento por reunificación en Romulus, prueba de disidencia interna. | SCREEN_CANON |
| `TNG_UNIFICATION_II` | La reunificación se ve instrumentalizada por sectores del poder, sin invalidar el deseo de la población civil. | SCREEN_CANON |
| `TNG_FACE_OF_THE_ENEMY` | El Tal Shiar y rutas de deserción ilustran vigilancia y oposición desde dentro. | SCREEN_CANON |
| `TNG_THE_ENEMY` | El encuentro médico y militar muestra restricciones de confianza entre estados, no incompatibilidad humana-racial. | SCREEN_CANON |
| `DS9_IN_THE_PALE_MOONLIGHT` | La participación romulana en la guerra del Dominio depende de decisiones e información política de fecha. | SCREEN_CANON |
| `ST_OFFICIAL_UNIFICATION_PRIMER` | Referencia oficial a ascendencia común con los vulcanos y a la variedad de posturas sobre reunificación. | OFFICIAL_REFERENCE |

Estas referencias son **anclajes por episodio**, no verificación exhaustiva escena por escena ni afirmaciones de que todo atributo aparezca literalmente en pantalla. Separar siempre pantalla, referencia oficial, interpretación y añadido del juego.

## B. Biología, anatomía, percepción y medicina

Humanoides de orejas puntiagudas con parentesco evolutivo/ancestral con vulcanos; no son vulcanos con otra ciudadanía. La apariencia facial cambia entre individuos y producciones. No conceder automáticamente fusión mental ni un repertorio de aptitudes vulcanas a personas romulanas.

**Aplicación:** diagnóstico y tratamiento dependen de evaluación clínica individual y privacidad, no de multiplicadores raciales.

## C. Desarrollo, reproducción, pareja, parentesco y vejez

El parentesco y la estructura familiar deben crearse por biografía individual. La política de secreto puede afectar documentación civil disponible al jugador, pero no determina natalidad, maduración, esperanza de vida ni necesidades médicas sin datos.

**Aplicación:** conservar biografía, vínculos familiares, eventos vitales y estados médicos. La especie no decide relaciones ni condiciones personales.

## D. Sociedad, costumbres, política interna y variaciones

Se distinguen aparato estatal, Senado, Tal Shiar, flota, poblaciones civiles y disidentes de la reunificación. Secreto, lealtad institucional o sospecha pueden ser respuestas situacionales, no personalidad de nacimiento. Existen profesionales, familias y pacifistas con distintas motivaciones.

**Aplicación:** separar `species`, educación/cultura, ciudadanía, organización, profesión, opiniones y conducta. La diversidad interna es obligatoria.

## E. Idioma, nombres y comunicación

Romulano está registrado en el catálogo inicial; la habilidad de descifrar documentación militar o formas ceremoniales no se deriva del simple conocimiento conversacional. Los nombres, rangos y títulos deben preservarse con su contexto.

**Aplicación:** una traducción correcta no concede conocimiento cultural, claves de seguridad ni consentimiento. No crear vocabulario ficticio y etiquetarlo como canon.

## F. Fechas, contacto y cambios del siglo XXIV

En TNG predominan enfrentamientos y contactos limitados; la evolución hacia la alianza anti-Dominio se produce en 2374, según hechos de DS9. No importar eventos posteriores de Picard ni Kelvin a la continuidad del juego sin puerta temporal expresa.

**Aplicación:** los acontecimientos históricos afectan al estado global solo tras ocurrir legítimamente en la campaña o estar ya establecidos en su punto de partida.

## G. Escenarios concretos para personajes persistentes

1. Una científica romulana disidente no puede revelar rutas navales que nunca conoció.
2. Un agente Tal Shiar requiere afiliación secreta registrada, no etiqueta de especie.
3. Una nave romulana no ataca sin reglas de contacto, órdenes y situación diplomática vigente.

Para la computadora de a bordo, acceso a conocimiento y datos privados se deriva de autorización y contacto registrado; el director IA no materializa esas escenas sin estado causal.

## H. Incertidumbres explícitas: prohibido rellenar por imaginación

- Cronología precisa del cisma antiguo.
- Vida media y fisiología diferencial completa.
- Alfabetos/dialectos regionales verificables.
- Distribución de movimientos políticos entre civiles.
- Reglas universales de parentesco.

**Cautela de canon y conflicto:** La procedencia común no es identidad cultural y un oficial no representa todo el Imperio; referirse a fuente oficial de reunificación sin trasladar sucesos de series excluidas.

## I. Contratos y alcance técnico

- Fuente operativa sigue siendo `sistemas/gameplay/species/profiles/romulan_v0.1.json`; esta ampliación **no cambia** los atributos esperados por CoreRPG.
- Contratos de biología/cultura y ciclo vital: `sistemas/gameplay/species/species_gameplay_contract.md` y `sistemas/gameplay/species/character_lifecycle_contract.json`.
- Los identificadores fuente se resuelven con `mundo/sources/source_registry/source_registry.json`; para hechos críticos se requiere revisión de escena antes de definir números u obligaciones jurídicas.
- Integración de conocimientos de la computadora, NPC y fechas en el runtime **pendiente**; el estado `v0.2` califica investigación escrita, no terminación de la implementación.
