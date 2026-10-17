# Humanos — expediente LORE-01 A v0.2

**Identificador:** `human` · **Ámbito:** `MAIN_GAME` · **Estado:** documentación de investigación ampliada, no certificado de motor.  
**Ficha operativa heredada:** `gameplay/species/profiles/human_v0.1.json`. **Evidencias estructuradas:** `lore/species/evidence/human_v0.2.json`.

## 1. Evidencias verificables y límites de la observación

| Fuente registrada | Afirmación acotada | Nivel de fuente |
|---|---|---|
| `TNG_ENCOUNTER_AT_FARPOINT` | La Enterprise-D reúne personas humanas en servicio profesional, mando y familia; el contexto institucional no equivale a la totalidad de la cultura humana. | SCREEN_CANON |
| `TNG_FAMILY` | La familia Picard permite observar vínculos rurales, duelo, memoria familiar y tensiones entre vida civil y carrera de la Flota. | SCREEN_CANON |
| `TNG_FIRST_DUTY` | La Academia forma a cadetes con disciplina, obligaciones éticas y consecuencias ante una investigación. | SCREEN_CANON |
| `DS9_EMISSARY` | Sisko afronta pérdida familiar y reasignación profesional; identidad humana y rol de oficial no son intercambiables. | SCREEN_CANON |
| `DS9_HOMEFRONT` | La seguridad de la Tierra, el debate público y las medidas excepcionales muestran tensión entre instituciones y libertades. | SCREEN_CANON |
| `VOY_RESOLUTIONS` | Janeway y Chakotay afrontan aislamiento; se documenta adaptación individual, no una especialización biológica por etnia. | SCREEN_CANON |

El nivel de fuente clasifica el **tipo de material** y no certifica que todos los pormenores se hayan comprobado mediante transcripción o escena a escena. Ante contradicción, recurrir a `sources/canon_policy.md`; no fusionar versiones incompatibles.

## 2. Morfología, sentidos y medicina

Fisiología humanoide terrestre de referencia para medicina comparada, no patrón obligatorio de normalidad galáctica. Los fenotipos humanos son diversos; región de origen, patrimonio genético, edad y modificaciones individuales requieren registros separados.

**Regla clínica:** cada diagnóstico y capacidad procede del estado individual, historial médico y examen autorizado; la especie no suministra constantes clínicas inventadas ni acceso automático a datos privados.

## 3. Nacimiento, desarrollo, reproducción y ciclo vital

Embarazo, infancia, madurez, senescencia y muerte dependen de una biografía personal; no convertir la edad laboral o militar en límite reproductivo. Las relaciones familiares y la crianza incluyen contextos terrestres, coloniales y mixtos.

**Regla de persistencia:** el nacimiento, envejecimiento, condición reproductiva, enfermedad, transformación y fallecimiento son eventos reales del personaje, no decisiones libres de la IA.

## 4. Culturas, costumbres, parentesco y diversidad

La Tierra, colonias humanas, familias mestizas y cultura cívica federada no forman una sola tradición. El estilo de liderazgo de Picard, Sisko o Janeway es personal y profesional; la Academia y la Flota son instituciones adquiridas, no cultura innata.

**Regla social:** la afiliación cultural, parentesco, ciudadanía, credo y oficio se almacenan de forma independiente. Ningún patrón cultural determina de antemano la personalidad.

## 5. Lengua, nombres, traducción y conocimiento

El inglés terrestre es habitual en la interfaz audiovisual, pero no demuestra monolingüismo de toda la humanidad. Idiomas nacionales, comunidades coloniales y capacidad de traducción se resuelven en la biografía y registro de contacto, sin inventar un catálogo completo.

**Regla de comunicación:** la interfaz de traducción no concede confianza, comprensión social ni acceso a conversaciones privadas. La competencia lingüística depende de aprendizaje/contacto.

## 6. Cronología TNG/DS9/VOY y contactos

La Flota y la Federación existen durante TNG, DS9 y Voyager, pero sus políticas de seguridad, diplomacia y defensa cambian; la invasión del Dominio no puede preexistir a su propia cronología.

**Regla temporal:** una fecha de emisión o de observación no supone nacimiento de la especie. El narrador consulta fecha, región, archivo histórico y conocimiento adquirido por cada actor.

## 7. Casos operativos para NPC, tripulación y computadora

1. Una médica humana con familia en una colonia no conoce automáticamente información clasificada sobre ese mundo.
2. Un cadete humano puede haber nacido fuera de la Tierra; su ciudadanía y rango necesitan expediente.
3. Un oficial de la Flota no representa por defecto la postura de todos los civiles humanos.

La computadora puede exponer la síntesis pública si su base de datos tiene esa entrada; no debe desvelar secretos personales ni especular sobre individuos recién descubiertos.

## 8. Límites pendientes e investigación negativa

- **No confirmado:** Distribución de esperanza de vida humana a escala federada en 2370.
- **No confirmado:** Impacto clínico universal de tratamientos avanzados sobre el envejecimiento.
- **No confirmado:** Censo completo por planetas, lenguas y parentescos mixtos.
- **No confirmado:** Normas de reproducción de cada cultura humana.

**Conflicto o cautela:** Distinguir capacidad médica de siglos XXIV y medias demográficas no demostradas; nunca deducir 'humanidad sin enfermedades' ni 'sin conflicto'.

## 9. Trazabilidad e integración futura

- Perfil biológico preexistente: `gameplay/species/profiles/human_v0.1.json` (no se sobrescribe el contrato).
- Fuentes concretas: identificadores de la tabla, resueltos en `sources/source_registry/source_registry.json`.
- Compatibilidad: `gameplay/species/species_gameplay_contract.md`, `gameplay/species/character_lifecycle_contract.json`.
- **Pendiente de implementación:** programación de conocimiento NPC, validación de fuentes contra escenas, configuraciones médicas numéricas si las aprobase el canon, y adopción del dossier por el contenido del juego.
