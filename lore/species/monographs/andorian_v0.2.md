# Andorianos — expediente LORE-01 A v0.2

**Identificador:** `andorian` · **Ámbito:** `MAIN_GAME_EXISTING_LOW_TNG_EVIDENCE` · **Estado:** documentación de investigación ampliada, no certificado de motor.  
**Ficha operativa heredada:** `gameplay/species/profiles/andorian_v0.1.json`. **Evidencias estructuradas:** `lore/species/evidence/andorian_v0.2.json`.

## 1. Evidencias verificables y límites de la observación

| Fuente registrada | Afirmación acotada | Nivel de fuente |
|---|---|---|
| `TOS_JOURNEY_TO_BABEL` | Representantes andorianos participan en la diplomacia de la Federación; el cuerpo diplomático no describe por sí solo la sociedad. | SCREEN_CANON |
| `MA_ANDORIAN` | Referencia secundaria para morfología pigmentada y antenas; los detalles funcionales necesitan episodios retenidos de apoyo. | RELIABLE_SECONDARY |
| `MA_ANDORIA` | Ancla secundaria para planeta Andoria; no justifica emplazamientos o ecología sin contraste. | RELIABLE_SECONDARY |
| `ST_OFFICIAL_GET_TO_KNOW_FEDERATION` | La pertenencia histórica al marco federado es un contexto político general, no ciudadanía de cada individuo. | OFFICIAL_REFERENCE |

El nivel de fuente clasifica el **tipo de material** y no certifica que todos los pormenores se hayan comprobado mediante transcripción o escena a escena. Ante contradicción, recurrir a `sources/canon_policy.md`; no fusionar versiones incompatibles.

## 2. Morfología, sentidos y medicina

El fenotipo reconocible incluye pigmentación azul y antenas craneales; una función sensorial precisa de las antenas y sus consecuencias clínicas NO queda demostrada suficientemente con fuentes TNG/DS9/VOY actualmente asociadas. No modelar daño de antenas como pérdida automática de equilibrio sin respaldo de alcance.

**Regla clínica:** cada diagnóstico y capacidad procede del estado individual, historial médico y examen autorizado; la especie no suministra constantes clínicas inventadas ni acceso automático a datos privados.

## 3. Nacimiento, desarrollo, reproducción y ciclo vital

La estructura reproductiva, gestación, maduración y parentescos complejos descritos fuera del corpus TNG se mantienen separados; la ficha actual no permite fijar herencia, número de progenitores ni edades médicas universales.

**Regla de persistencia:** el nacimiento, envejecimiento, condición reproductiva, enfermedad, transformación y fallecimiento son eventos reales del personaje, no decisiones libres de la IA.

## 4. Culturas, costumbres, parentesco y diversidad

El orgullo institucional de la Federación y la figura de diplomáticos andorianos sí caben en el contexto retenido. Ideas sobre desafíos, duelos y estructuras familiares proceden en parte de Enterprise excluida; etiquetarlas como referencias externas que exigen otra decisión si se quisieran trasladar.

**Regla social:** la afiliación cultural, parentesco, ciudadanía, credo y oficio se almacenan de forma independiente. Ningún patrón cultural determina de antemano la personalidad.

## 5. Lengua, nombres, traducción y conocimiento

Andoriano/andorii como denominación de trabajo no constituyen en sí mismos un diccionario ni una gramática. Mantener lengua y escritura como no normalizadas hasta autorización documentada.

**Regla de comunicación:** la interfaz de traducción no concede confianza, comprensión social ni acceso a conversaciones privadas. La competencia lingüística depende de aprendizaje/contacto.

## 6. Cronología TNG/DS9/VOY y contactos

La especie es conocida en la Federación antes de TNG; no inventar conflictos de 2370. El hecho de que haya Andorianos no significa que los Aenar sean visibles o conocidos individualmente.

**Regla temporal:** una fecha de emisión o de observación no supone nacimiento de la especie. El narrador consulta fecha, región, archivo histórico y conocimiento adquirido por cada actor.

## 7. Casos operativos para NPC, tripulación y computadora

1. Oficial andoriano federado: conservar profesión y ciudadanía como hechos personales.
2. Un daño visual en una antena no autoriza automáticamente un efecto clínico numérico.
3. En un diálogo diplomático no convertir franqueza individual en obligación de duelo.

La computadora puede exponer la síntesis pública si su base de datos tiene esa entrada; no debe desvelar secretos personales ni especular sobre individuos recién descubiertos.

## 8. Límites pendientes e investigación negativa

- **No confirmado:** Fisiología exacta de antenas bajo corpus retenido.
- **No confirmado:** Longevidad y reproducción.
- **No confirmado:** Culturas regionales de Andoria documentadas en TNG.
- **No confirmado:** Lenguas, escritura y normas de parentesco canónicas retenidas.

**Conflicto o cautela:** Parte del legado cita ENT_UNITED/ENT_BABEL_ONE; Enterprise está fuera del corpus seleccionado. El material anterior se conserva marcado, no se reafirma como canon TNG.

## 9. Trazabilidad e integración futura

- Perfil biológico preexistente: `gameplay/species/profiles/andorian_v0.1.json` (no se sobrescribe el contrato).
- Fuentes concretas: identificadores de la tabla, resueltos en `sources/source_registry/source_registry.json`.
- Compatibilidad: `gameplay/species/species_gameplay_contract.md`, `gameplay/species/character_lifecycle_contract.json`.
- **Pendiente de implementación:** programación de conocimiento NPC, validación de fuentes contra escenas, configuraciones médicas numéricas si las aprobase el canon, y adopción del dossier por el contenido del juego.
