# LORE-05E — Idiomas, comunicación y traductor universal
**Fecha:** 13-11-2026 · **Corte narrativo:** 2383 · **Estado:** diseño documental; sin runtime.

## Propósito
La traducción hace accesible una galaxia diversa, pero no elimina diferencias lingüísticas, semánticas, sociales ni jurídicas. Este documento **interpreta** reglas preexistentes; no instala un traductor nuevo, no redefine fórmulas de señal ni crea un motor de IA.

## 1. Ocho asociaciones lingüísticas ya presentes
El catálogo `sistemas/gameplay/languages/initial_language_catalogue.json` registra klingon, romulano, bajorano, ferengi, trill, breen, kazon y talaxiano. Los dos últimos están marcados `DLC_DELTA_FUTURE`, **no se convierten en personajes, viajes ni culturas visitables del juego principal**. El catálogo es ilustrativo, no contiene todas las lenguas posibles de la galaxia. Un individuo puede dominar varias, ninguna de las esperadas o dialectos específicos. Especie, país, organización, ciudadanía y lengua no son sinónimos. No inferir carácter o afiliación por acento.

El modelo de personaje existente registra `known_languages`, niveles de fluidez, alfabetización, formación lingüística y acceso al traductor. Para el jugador se recomienda la presentación en **castellano de España** por decisión `player_facing_language.md`; esto es una convención de interfaz, no prueba que todos hablen español diegéticamente.

## 2. Qué puede y qué no puede hacer el traductor
Se respetan **exactamente** los seis estados de `language_runtime_model.json`: `direct_shared_language`, `universal_translator_confident`, `universal_translator_partial`, `universal_translator_literal_only`, `analysis_required` y `untranslated`. No se fijan probabilidades de éxito ni tiempos fijos; los determina la simulación propietaria a partir de evidencia, matriz lingüística, conocimiento, señal y medios.

- **Comprender palabras no equivale a comprender intención.** El caso `Darmok` (TNG) demuestra traducción léxica sin referencias metafóricas compartidas. El jugador debería poder solicitar análisis cultural, revisar la expresión original y comparar testimonios antes de tomar decisiones.
- **La incertidumbre es visible.** Si una traducción es parcial o literal, la interfaz puede mostrar advertencias comprensibles: «Traducción literal; intención no confirmada». No fingir diálogo perfecto ni inventar una gramática entera.
- **Voz, escritura, gestos y otras modalidades** requieren evidencias y recursos distintos; interpretar voz no desbloquea un alfabeto. Nombres y títulos pueden necesitar transliteración o interpretación política.
- **Mejora causal:** observaciones, intercambios recíprocos, lingüistas, corpus y estudios autorizados alimentan una matriz persistente ya prevista en `universal_translator_bootstrap_v0.1.json`. La IA no cambia el estado por conveniencia narrativa.
- **Error sin villanos:** una ambigüedad cultural no prueba hostilidad, fraude ni torpeza de los interlocutores. La reparación de un malentendido puede exigir diálogo, disculpa o abstención.
- **Tamariano:** ejemplo de pantalla para entender la limitación semántica. No se añade automáticamente al catálogo jugable ni se presupone una nueva civilización activa en 2383.

## 3. Comunicaciones navales y diplomáticas
Los sistemas `communications_model.json` y `subspace_communication_contract.json` ya separan canal, intensidad, latencia, interferencia, cifrado, traducción, repetidores y destinatario. Respetamos sus estados, incluidos `degraded`, `delayed`, `store_and_forward`, `jammed` y `recipient_refused`.

Antes de exponer un mensaje como cierto, verificar **quién lo emitió**, si la transmisión fue recibida, si está completa, a quién iba dirigida, cuándo pudo conocerse, qué fragmentos son traducibles, qué clasificación posee y si las credenciales son auténticas. Una llamada visual no concede por sí sola acceso a pensamientos, archivos ni idioma original.

**Separar cuatro capas:**
1. **Transmisión:** qué señal llega, con qué retraso, pérdidas o interferencia.
2. **Interpretación:** qué parte es legible, traducida y contextualizada.
3. **Conocimiento:** qué recibió realmente cada sujeto y con qué nivel de certeza.
4. **Autoridad:** si el emisor tiene competencias y si la orden, oferta o acuerdo es válido.

Una orden traducida del almirantazgo no es una orden ejecutable si falla autenticación, destino o validación del sistema F11. Un mensaje de una nave romulana no es automáticamente una declaración del Senado. Gobierno civil de la Federación y Flota Estelar mantienen atribuciones distintas (LORE-05D).

## 4. Ejemplos de escenas, no misiones creadas
**El saludo discutido.** Un capitán alienígena utiliza una expresión que el traductor interpreta literalmente como amenaza. El oficial de comunicaciones expone el original y el estado «literal», Ciencia propone una lectura alternativa y el capitán decide si responder, pedir aclaración o retrasar el contacto. Nadie inventa qué pensaba realmente el alienígena.

**Mensaje incompleto de socorro.** Una transmisión deteriorada permite identificar un peligro, no la ubicación exacta. Navegación y Sensores requieren datos; una IA no materializa una localización porque la urgencia narrativa lo sugiera. La información tardía llega solo cuando el enlace la entrega.

**La negociación mal atribuida.** Un comerciante ferengi propone un trato. La traducción puede ser buena, pero la capacidad contractual, el consentimiento y los efectos políticos no se deducen de su especie ni de la cortesía del diálogo.

**El cadete lingüista.** Un cadete registra una expresión original, estudia una hipótesis y solicita revisión académica. Una evaluación de Academia podrá reconocer su formación si la fase propietaria la implementa; no existe recompensa XP ni mejora instantánea por leer el texto.

**Vida cotidiana.** Se pueden oír expresiones originales, ver carteles multilingües y consultar traducciones del PADD **siempre que el personaje conozca o tenga permitido conocer el contenido**. No se asigna ahora locución ni modelos 3D.

## 5. Presentación recomendada
LCARS en castellano, con una indicación pequeña y contextual de: **idioma detectado / fuente original si está autorizada / confianza / ambigüedad / canal / timestamp de recepción**. Nunca una barra de porcentaje ficticio o cifras de certeza inventadas. Si una frase es ambigua, mostrar «significado no confirmado», no un subtítulo que revele la respuesta secreta del guion. La opción de mostrar texto original debe respetar derechos, activos existentes y la información materializada.

## 6. Propiedad técnica y límites
- **LORE-05E:** ejemplos, matices, evidencias y casos adversariales.
- **CoreRPG:** hechos, matrices realmente aceptadas, historia, receptor, conocimiento, daños, tiempo y guardado.
- **F11:** competencia, cadena de mando, órdenes. **HOST solo sirve consultas y transporte de servicios; no reimplementa F11.**
- **F06/comunicaciones/UE5:** futuras interfaces y subsistemas según su propietario; no se tocan.
- **IA:** redacta o explica únicamente desde las vistas autorizadas; no traduce como verdad lo que aún está `analysis_required`.
- **PADD exterior:** información aprendida + permiso efectivo, con exclusión de secretos exportables según política vigente.

## Fuentes y categorías
`SCREEN_CANON`: TNG «Darmok» (limitaciones semánticas); TNG «First Contact» (riesgo de exposición cultural); ENT «Breaking the Ice» (valor de traducción precisa). `OFFICIAL_REFERENCE` auxiliar: https://www.startrek.com/news/how-artificial-intelligence-is-getting-us-closer-to-star-treks-universal-translators ; https://www.startrek.com/news/hoshi-sato-created-a-linguistic-legacy ; https://www.startrek.com/news/striving-to-create-our-own-picard-and-dathon-at-el-adrel (enlace contextual orientativo). `GAME_ADDITION`: presentación LCARS contextual y casos jugables hipotéticos. Las escenas citadas no prueban disponibilidad exacta de tecnología o personal en 2383. Rigen `canon_policy.md` y `provenance_policy.md`.
