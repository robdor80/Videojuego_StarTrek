# Vulcanos — expediente LORE-01 A v0.2

**Identificador:** `vulcan` · **Ámbito:** `MAIN_GAME` · **Estado:** documentación de investigación ampliada, no certificado de motor.  
**Ficha operativa heredada:** `sistemas/gameplay/species/profiles/vulcan_v0.1.json`. **Evidencias estructuradas:** `mundo/lore/species/evidence/vulcan_v0.2.json`.

## 1. Evidencias verificables y límites de la observación

| Fuente registrada | Afirmación acotada | Nivel de fuente |
|---|---|---|
| `TOS_AMOK_TIME` | El pon farr es un proceso fisiológico relevante para Spock; su manejo tiene componentes de privacidad, ritual y riesgo médico. | SCREEN_CANON |
| `VOY_BLOOD_FEVER` | Vorik atraviesa pon farr a bordo de Voyager y su conducta ocasiona un conflicto de consentimiento; la fisiología no exime responsabilidad. | SCREEN_CANON |
| `VOY_DAY_OF_HONOR` | Tuvok muestra prácticas de disciplina y protocolo vinculadas a su educación, junto a decisiones concretas de un oficial. | SCREEN_CANON |
| `DS9_TAKE_ME_OUT_TO_THE_HOLOSUITE` | Un equipo vulcano de la Flota dirigido por Solok exhibe rivalidad, competencia y motivaciones propias; lógica no significa ausencia de ego. | SCREEN_CANON |
| `TOS_JOURNEY_TO_BABEL` | Sarek y Amanda muestran una familia intercultural y diplomacia vulcana en un contexto federado. | SCREEN_CANON |
| `ST_OFFICIAL_PON_FARR_CONSENT` | Referencia oficial que distingue el proceso biológico de la conducta interpersonal responsable. | OFFICIAL_REFERENCE |

El nivel de fuente clasifica el **tipo de material** y no certifica que todos los pormenores se hayan comprobado mediante transcripción o escena a escena. Ante contradicción, recurrir a `mundo/sources/canon_policy.md`; no fusionar versiones incompatibles.

## 2. Morfología, sentidos y medicina

Humanoides de orejas puntiagudas y rasgos no idénticos a los humanos. La fisiología y la neurobiología tienen necesidades médicas específicas; no crear cifras universales de fuerza o temperatura. La fusión mental es una acción psíquica contextual, no un permiso para leer toda memoria.

**Regla clínica:** cada diagnóstico y capacidad procede del estado individual, historial médico y examen autorizado; la especie no suministra constantes clínicas inventadas ni acceso automático a datos privados.

## 3. Nacimiento, desarrollo, reproducción y ciclo vital

El pon farr puede generar necesidades médicas y presiones sociales; no se activa por un temporizador genérico del jugador ni tiene el mismo desarrollo para todo el mundo. Matrimonio, vínculo familiar, mentorazgo y celibato requieren biografía, consentimiento y circunstancias.

**Regla de persistencia:** el nacimiento, envejecimiento, condición reproductiva, enfermedad, transformación y fallecimiento son eventos reales del personaje, no decisiones libres de la IA.

## 4. Culturas, costumbres, parentesco y diversidad

La disciplina lógica y la supresión/gestión emocional son prácticas culturales y filosóficas aprendidas. Existen variaciones, disidentes, matrimonios mixtos y diferencias entre individuos. La cortesía formal de un interlocutor no proporciona su afiliación religiosa o política.

**Regla social:** la afiliación cultural, parentesco, ciudadanía, credo y oficio se almacenan de forma independiente. Ningún patrón cultural determina de antemano la personalidad.

## 5. Lengua, nombres, traducción y conocimiento

Existe lengua vulcana, pero no hay corpus completo normalizado en el proyecto: pronunciaciones, competencia nativa, escritura ceremonial y traductor deberán elaborarse bajo contrato lingüístico separado. No asociar automáticamente vulcanidad con habla de un solo idioma.

**Regla de comunicación:** la interfaz de traducción no concede confianza, comprensión social ni acceso a conversaciones privadas. La competencia lingüística depende de aprendizaje/contacto.

## 6. Cronología TNG/DS9/VOY y contactos

Las evidencias TOS corresponden a una era anterior; Voyager y DS9 muestran supervivencia de costumbres sin convertir su ejecución en determinista. Las políticas y relaciones con romulanos tienen sus propias fechas.

**Regla temporal:** una fecha de emisión o de observación no supone nacimiento de la especie. El narrador consulta fecha, región, archivo histórico y conocimiento adquirido por cada actor.

## 7. Casos operativos para NPC, tripulación y computadora

1. Un médico valida identidad y síntomas antes de proponer atención al pon farr; respeta privacidad.
2. La fusión mental exige capacidad, situación, autorización y consecuencias, nunca es un interrogatorio gratuito.
3. Un vulcano deportista puede ser competitivo sin dejar de ser vulcano.

La computadora puede exponer la síntesis pública si su base de datos tiene esa entrada; no debe desvelar secretos personales ni especular sobre individuos recién descubiertos.

## 8. Límites pendientes e investigación negativa

- **No confirmado:** Valores clínicos de referencia generales por edad y sexo.
- **No confirmado:** Incidencia exacta y variedades de pon farr.
- **No confirmado:** Capacidad telepática y formación de cada individuo.
- **No confirmado:** Normas matrimoniales universales y esperanza de vida máxima estadística.

**Conflicto o cautela:** No extrapolar diálogos de Spock, Sarek o Tuvok a toda la especie; la telepatía no crea omnisciencia, ni el autocontrol elimina emociones.

## 9. Trazabilidad e integración futura

- Perfil biológico preexistente: `sistemas/gameplay/species/profiles/vulcan_v0.1.json` (no se sobrescribe el contrato).
- Fuentes concretas: identificadores de la tabla, resueltos en `mundo/sources/source_registry/source_registry.json`.
- Compatibilidad: `sistemas/gameplay/species/species_gameplay_contract.md`, `sistemas/gameplay/species/character_lifecycle_contract.json`.
- **Pendiente de implementación:** programación de conocimiento NPC, validación de fuentes contra escenas, configuraciones médicas numéricas si las aprobase el canon, y adopción del dossier por el contenido del juego.
