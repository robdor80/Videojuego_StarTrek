# HOST H06 / IA-03A — Auditoría y diseño de las reglas objetivas de F10

**Fecha:** 15/11/2026. **Responsable:** ChatGPT (arquitectura y auditoría).  
**Base auditada:** `main` `b147ed9d30a3c58f5d1832a01bb92a6b117bcd86`, tras IA-02/PR #165.  
**Estado de este documento:** **AUDITADO / DISEÑO PROPUESTO**; no es una aprobación de reglas nuevas, implementación, test funcional ni certificación.  
**Fase:** IA-03A, primera entrega del trabajo IA-03.  
**Restricción:** documentación aditiva; no se modifican contratos bloqueados, código, CoreRPG ni sus versiones, F11, H03/H04 o Unreal.

## Nota de ratificación posterior — ciudadanía (decisión definitiva del autor)

El autor ha ampliado la primera decisión: **si la especie jugable pertenece a la Federación Unida de Planetas, el personaje tiene automáticamente ciudadanía federada**, sin importar en qué planeta nació. F10 no pedirá certificados, prueba de nacimiento, expedientes ni evaluación de OpenAI para justificarla. Humanos, vulcanos, andorianos y tellaritas son ejemplos confirmados de especies fundadoras; el catálogo concreto de otras especies federadas debe derivar de fuentes aprobadas del juego, sin inventar afiliaciones. Esta regla sustituye la excepción anterior «humano nacido en Tierra», ahora incluida en la regla general. Ciudadanía federada **no** concede automáticamente membresía de Flota Estelar, rango, plaza de Academia, destinos ni autorizaciones. Para especies sin pertenencia federada, la política de ciudadanía permanece sin decidir; no se aplica la regla por analogía. **Estado: DECIDIDO / DOCUMENTADO; comportamiento productivo NO IMPLEMENTADO aún en IA-03A.**

## Decisiones autorales posteriores — alcance de especies y formulario

### Ciudadanía: alcance aprobado para el primer lanzamiento

El autor precisa que **las únicas especies seleccionables inicialmente son humano, vulcano e híbrido humano-vulcano**. Para las tres, la ciudadanía **Federación Unida de Planetas** es **automática**, independientemente de dónde haya nacido el personaje. No pedir documentación, certificado, registro civil, investigación o consulta a IA; no implantar ahora un catálogo de legislación ni resolver casos de especies todavía no jugables. No se conceden rangos, admisión, membresía Starfleet, plazas ni autorizaciones.

Esta precisión sustituye interpretaciones anteriores que exigían nacimiento en Tierra o verificaciones para asignar ciudadanía a alguna de las tres especies. Otras especies podrán considerarse más adelante cuando el autor amplíe el elenco jugable. El catálogo técnico de 26 especies de F10 no equivale a selección inicial jugable de 26 especies.

### Formulario: segunda pregunta, decisión aprobada

**Formulario detallado con información personal adicional OPCIONAL.** El usuario quiere conservar riqueza de campos para quien desee crear una historia extensa, **sin obligar a rellenar familia, crianza detallada, aficiones adicionales, estudios detallados, experiencia profesional, idiomas, personalidad u otros antecedentes**. El formulario ofrecerá una biografía libre opcional y datos básicos obligatorios suficientes para crear un personaje. Los campos no introducidos no deben generar hechos ficticios, certificados, penalizaciones, errores ni requisitos de justificación adicionales.

**Nota de integración técnica:** el contrato F10 `character_creation_contract_v1_0.json` mantiene campos canónicos obligatorios como `origin`, `prior_education`, `prior_experience`, `prior_activities_and_hobbies`, `culture_context`, etc. El futuro adaptador de formulario debe proponer representaciones explícitas de ausencia/no declarado/ninguna experiencia donde el tipo lo admita, **sin inventar antecedentes** y sin alterar a escondidas el contrato LOCKED. Si un valor técnico indispensable no puede representarse de manera neutral, elevar la incompatibilidad documental antes de código; evitar convertirlo en un campo libre obligatorio para el jugador.

La revisión semántica solo evalúa datos realmente aportados. Aportar más narrativa no concede habilidades, méritos ni derechos. La IA no inventará biografías para superar el validador.

**Estado:** ciudadanía y criterio de obligatoriedad del formulario **DECIDIDOS / DOCUMENTADOS**, aún sin implementación de IA-03A/IA-03C. Las siguientes cuestiones del autor se resolverán por separado.

## Decisión autoral — antecedentes y certificaciones ficticias con efectos reales

**Aprobada en la conversación de IA-03A (15/11/2026):** si el jugador declara, por ejemplo, que posee **4.º dan de karate** y su biografía supera la revisión de coherencia de IA y las comprobaciones F10 aplicables, ese antecedente **forma parte real de su PERSON en CoreRPG** tras el alta autorizada. No es un mero comentario decorativo ni debe quedar pendiente indefinidamente por ausencia de un diploma/documento externo de una persona real.

**Comportamiento de producto previsto:**

- El grado/historial aceptado queda registrado como **hecho biográfico ficticio inicial**, con su procedencia y la versión/huella de validación F10.
- Debe poder reflejarse en la **competencia inicial correspondiente** cuando exista la regla de progresión/capacidad del dominio; no crear un sistema paralelo de puntuaciones, ni convertir arbitrariamente un 4.º dan en «maestría absoluta». Se distingue la habilitación o certificación ficticia del valor cuantitativo de una habilidad. No suponer que esa traducción está implementada hoy.
- Los NPC solo pueden conocer o utilizar el antecedente si su ámbito de conocimiento/permisos lo permite; no conceder omnisciencia.
- Persistir y recuperar con la misma identidad e historia. No otorgar rango F11, plaza de Academia, autorizaciones Starfleet ni acceso a sistemas institucionales por un título civil/marcial.
- Las certificaciones se comprueban **por plausibilidad interna de edad, años de práctica, trayectoria y entorno de la ficción**. No se exigirá al jugador presentar un certificado real ni un expediente de una entidad preexistente ficticia que todavía no tenga PERSON. Si una afirmación es cronológicamente imposible, F10 la rechaza o solicita corrección.
- **Frontera de autoridad:** la IA revisa, **F10 decide**, y solo el flujo autorizado de creación en CoreRPG fija el antecedente; una cadena enviada por el cliente o una respuesta no verificada de IA no adquiere autoridad por sí sola.

Esta decisión **precisa y corrige** las frases anteriores que podrían interpretarse como «un título ficticio nunca se incorpora a la PERSON» o «toda certificación requiere un certificado histórico preexistente». La protección válida es **no conceder capacidades incongruentes sin validación**, no prohibir los antecedentes narrativos certificados. **Estado: AUTORALMENTE DECIDIDO / DOCUMENTADO, todavía NO IMPLEMENTADO ni PROBADO en IA-03A/IA-03B.**

## Decisión autoral — habilidades iniciales y reacciones de NPC por formación validada

**Aprobada durante la revisión IA-03A (15/11/2026).** La biografía inicial validada tiene **efectos reales de juego**. Un personaje con **doctorado en Física y Astronomía** coherente y aceptado por F10 debe conservar ese hecho en CoreRPG como antecedente y **tener capacidades iniciales acordes con su especialidad**. Lo mismo aplica, proporcionalmente, a otras titulaciones, entrenamientos y habilidades, como el 4.º dan de karate.

**Consecuencias de diseño obligatorias para integraciones posteriores:**

1. **Persistencia autoritativa:** CoreRPG registra el hecho biográfico inicial y lo restaura con el mismo personaje; no queda solo como texto para un prompt de IA.
2. **Competencia inicial derivada:** reutilizar la futura/actual autoridad de habilidades del RPG para traducir formación/experiencia validada a conocimientos prácticos y posibilidades jugables. No inventar puntos ni niveles numéricos desde la IA. Si el motor de competencias aún no existe en producto, declarar la dependencia explícita, no fingir implementación.
3. **NPC conscientes de lo que saben:** cuando un NPC conozca legítimamente el doctorado o experiencia del jugador, sus diálogos, consultas, confianza profesional y posibles encargos deben reflejarlo. Un NPC **sin** ese conocimiento no recibe información omnisciente por compartir mundo con la PERSON.
4. **Interacciones contextuales y misiones:** la formación relevante puede desbloquear opciones de análisis, respuestas técnicas, hipótesis y planteamientos de soluciones **cuando el sistema de misiones/sensores/reglas las soporte**. No supone el éxito automático de toda acción.
5. **Separación del ámbito institucional:** ser doctor civil no da automáticamente rango F11, plaza de Academia, autorizaciones clasificadas, pertenencia a la Flota ni destino naval.
6. **Frontera de autoridad:** OpenAI/F10 validan coherencia; solo el dominio autorizado fija hechos y capacidades. NPC/IA consultan proyecciones de conocimiento y no modifican hechos autoritativos sin operación aprobada.

**Ejemplo de aceptación futura:** ante una anomalía espacial, un personaje con doctorado en Física y Astronomía podrá proponer hipótesis especializadas; un NPC científico informado de su título podrá dirigirse a él como experto. Un personaje sin esa formación no obtiene por defecto la misma especialización. Este contraste se comprobará en fases de capacidades, NPC y misiones, **no** se simula como prueba PASS de IA-03A.

**Estado:** criterio **DECIDIDO / DOCUMENTADO**. IA-03A aún no ha implementado ni probado esta integración en CoreRPG, habilidades o NPC. IA-03B conservará los antecedentes; la aplicación en NPC/IA y misiones corresponde a sus fases propietarias sin duplicar reglas en HOST.

## Decisión autoral aprobada — interpretación asistida del personaje en diálogos

**APROBADA por el autor en la conversación de IA-03A, 15/11/2026.** El conocimiento de un personaje puede superar al del jugador humano que lo controla. Un personaje con doctorado en Física y Astronomía validado por F10 podrá participar en diálogos técnicos sin obligar al jugador a conocer física avanzada. Se adopta un sistema de **interpretación asistida del personaje**, reutilizando el servicio de IA central IA-01 y los hechos/competencias autorizativos de CoreRPG cuando las fases de diálogos y NPC los integren.

**Modos previstos, intercambiables:** (1) diálogo guiado por intenciones comprensibles, con respuesta técnica redactada por IA; (2) diálogo libre por voz o texto, adaptando la intención del jugador a formación y personalidad validadas; (3) delegación de la explicación, en la que el jugador decide objetivo y el personaje expone detalles técnicos.

**Límites obligatorios:** la decisión/objetivo pertenece al jugador; la IA no puede otorgar conocimientos no acreditados, inventar resultados de sensores, secretos del universo, soluciones confirmadas, acciones ejecutadas, cargos ni permisos. Las comprobaciones y consecuencias pertenecen a CoreRPG y a los servicios institucionales propietarios. La información suministrada a cada NPC respeta su conocimiento y permisos; no hay omnisciencia. La IA no modifica directamente hechos autoritativos. El sistema debe ofrecer opciones comprensibles sin exigir habilidades técnicas al usuario.

**Alcance:** decisión de DISEÑO aprobada y documentada, **no implementación de diálogos ni prueba de funcionamiento**. IA-03A valida antecedentes; IA-03B los conserva en PERSON; las futuras fases de NPC/IA, diálogos y misiones implementarán esta interpretación sin duplicar la autoridad del HOST ni CoreRPG.

## Decisión autoral aprobada — origen libre, incluidos lugares inventados

**APROBADO por el autor el 15/11/2026** dentro de las seis cuestiones de F10. El jugador puede declarar libremente dónde nació y se crió su personaje, incluyendo **Tierra, Vulcano, colonias, estaciones espaciales, naves y lugares de origen inventados**. No es necesario que un lugar inventado aparezca previamente en un catálogo para admitirlo como dato biográfico personal.

**Única condición de validación:** la historia debe resultar razonablemente coherente con el universo Star Trek y el contexto de campaña en 2383. F10 no exigirá un registro oficial del planeta, una partida de nacimiento, una fuente histórica preexistente o pruebas documentales. La IA podrá detectar contradicciones narrativas; F10 decidirá la aceptación de los hechos del personaje.

**Alcance de autoridad:** aceptar que *el personaje dice haber nacido y crecido* en un lugar inventado **no publica por sí solo** un planeta nuevo como hecho global autoritativo ni modifica las entidades de CoreRPG de terceros. No concede automáticamente membresías, cargos o permisos. Para los tres tipos inicialmente jugables (humano, vulcano, híbrido humano-vulcano), la ciudadanía federada sigue siendo automática por decisión autoral previa.

**Estado:** DECIDIDO / DOCUMENTADO; todavía no IMPLEMENTADO en la ruta productiva F10. Codex IA-03A no podrá bloquear lugares originales por falta de catálogo si el relato supera la coherencia establecida.

## 1. Decisión arquitectónica

Una biografía de inicio es una **propuesta de hechos ficticios personales**, no una solicitud documental de identidad real. El jugador puede inventar un pasado verosímil. F10 comprueba esa propuesta y genera **atestaciones internas, acotadas y vinculadas al borrador**, exclusivamente cuando pueda justificar lo que está respaldando.

Distinguir expresamente:

1. **Antecedente personal narrativo**: nacido en un lugar plausible, afición, estudios generales, trabajo civil o ausencia de experiencia. Puede formar parte de la biografía tras validación sin acreditar permisos o capacidades especiales.
2. **Afirmación reglada**: estatus legal específico, formación formal, certificación, acceso tecnológico, capacidad especial. Requiere regla/itinerario/fuente interna cuando sea pertinente; **excepción autoral explícita: la ciudadanía federada se asigna automáticamente a miembros de especies federadas, independientemente del nacimiento**. Nada de ello concede credenciales profesionales o institucionales.
3. **Hecho institucional autoritativo**: rango F11, autorización, plaza en Academia, pertenencia real a la Flota o expediente oficial. No nace del formulario ni de OpenAI; pertenece a operaciones de dominio posteriores y autorizadas.

**Regla propuesta:** el sistema puede admitir como *historia ficticia de origen* antecedentes personales comprobados sin pedir pruebas reales al usuario, pero **no** convertirlos tácitamente en credenciales, atribuciones numéricas o hechos institucionales. F10 conserva el doble filtro: puerta objetiva completa y después revisión semántica IA-02. La IA no sustituye ninguna evidencia objetiva ni escribe en CoreRPG.

## 2. Fuentes examinadas y precedencia

- `sistemas/gameplay/character_creation/character_creation_contract_v1_0.json` — **locked_baseline**, campos requeridos/opcionales, orden de creación, dos puertas y bloqueo posterior de la biografía.
- `sistemas/gameplay/character_creation/biography_validation_rules.md` — **LOCKED BASELINE**; no corregir silenciosamente.
- `sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json` — identidad de ruta estable, **schema 0.1.2**, política autoral posterior: edad declarada por el jugador, sin demostración individual.
- `proyecto/docs/architecture/host/H06_P06_CORRECCION_EDAD_DECLARADA_2026-11-14.md` — prevalece sobre cláusulas históricas de madurez individual.
- `sistemas/gameplay/character_creation/f10_initial_background_policy_v0.1.json` — **DESIGN_PROPOSAL_NOT_RUNTIME_AUTHORITY**, clases de antecedentes y registro interno; no tratar este JSON como implementador productivo.
- `sistemas/gameplay/character_creation/f10_biography_evidence_semantic_boundary_v0.1.json` — frontera de fuentes/procedencia, parcialmente histórica.
- `sistemas/ai/OPENAI_RUNTIME_DECISION_2026-11-15.md` y `sistemas/gameplay/character_creation/f10_openai_semantic_policy_v0.1.json` — autorizan OpenAI y reemplazan solo las restricciones antiguas de proveedor/transporte.
- `sistemas/gameplay/character_creation/player_profile_contract.json` — distingue identidad local/nickname de identidad de PERSON.
- `sistemas/gameplay/organizations/character_affiliation_citizenship_contract.json` — ciudadanía, estatus legal, afiliación, asignación, lealtad y cultura son conceptos distintos.
- `sistemas/gameplay/character_creation/prior_activity_model.json` — afición, trayectoria y títulos no son puntos de habilidad automáticos.
- `sistemas/gameplay/character_creation/f10_formulario_inicial_v0.3.json` — **formulario de referencia**, no autoridad productiva; incluye `unknown` para ciudadanía.
- `sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json`, `H06_P06_CIERRE_FUNCIONAL_MINIMO_2026-11-14.md` — candidatura es distinta de admisión/matrícula.
- Nativo: `desarrollo/integration/host/src/f10/biography_validation.{h,cpp}`, `biography_evidence.h`, `openai_biography.{h,cpp}`, `embed_biography_rules.py`; pruebas `tests/biography_tests.cpp` y `tests/biography_ai_tests.cpp`.
- H03: `desarrollo/integration/host/src/player_bootstrap.h`; HOST: `native_session.h` y `include/trek/host/host_abi.h`.

No crear un segundo catálogo de edades, ni un registro de pruebas de madurez, ni introducir una fecha de día/mes de campaña no aprobada.

## 3. Inventario de lo que ya está IMPLEMENTADO en el código inspeccionado

| Alcance | Evidencia concreta | Estado |
|---|---|---|
| Validación de forma y campos | `parse_draft`, `objective_checks` detectan borrador no válido, claves repetidas, campos reservados, ausencia de campos y forma de entradas | **IMPLEMENTADO**; tests históricos disponibles |
| Edad inicial | Catálogo de 26 especies: 22 suelos numéricos, 3 especies especiales sin mínimo y 5 perfiles Delta fuera del juego principal; sin edad máxima forzada | **IMPLEMENTADO** conforme a política 0.1.2 |
| Año 2383 | `valid_context` comprueba escenario/era/año; umbral de cumpleaños ambiguo sin mes/día queda pendiente | **IMPLEMENTADO** |
| Cronología y tecnología explícita | `validate_moment`, `validate_technology` rechazan imposibilidades comprobables y posponen casos de acceso/no catalogados | **IMPLEMENTADO PARCIAL** |
| Aficiones verificables | `validate_history` y fuente `initial_background_source` soportan una comprobación acotada de periodos personales estructurados | **IMPLEMENTADO PARCIAL** |
| Evidencias registradas | `RegisteredBiographyAuthority::resolves` exige fuente registrada, vinculación de borrador/contexto, decisión y no revocación; `evidence_ref` escrito por jugador no vale | **IMPLEMENTADO como mecanismo**, sin evaluadores productivos de las cinco fuentes pendientes |
| Revisión semántica | IA-02 conecta el servicio OpenAI y comprueba procedencia, versión y vigencia; `PENDING` no da recibo | **IMPLEMENTADO y PROBADO con dobles**, OpenAI LIVE **NOT_RUN** |
| PERSON/candidatura | `academy_core_feasibility.cpp` es ensayo de capacidad Core; no es factory F10 productivo | **NO IMPLEMENTADO en este flujo** |

**Atención:** `tests/biography_tests.cpp` y `tests/biography_ai_tests.cpp` crean **fixtures** de fuentes para cubrir el camino positivo. Esas fuentes no demuestran una autoridad de producto; no permitir que su existencia se utilice para afirmar que un jugador real puede obtener ya un recibo válido.

## 4. Los cinco bloqueos efectivos de una biografía corriente

`objective_checks` emite indiscriminadamente algunos códigos de revisión pendiente y `validate_history` difiere otros. `RegisteredBiographyAuthority` no dispone de sus atestaciones de producción. En una ficha normal permanecen:

| Código pendiente | Problema real | Solución mínima PROPUESTA para IA-03A | Lo que NO autoriza |
|---|---|---|---|
| `ORIGIN_EVIDENCE_REQUIRED` | Falta registrar en producto la política autoral de origen narrativo libre | Aceptar lugar de nacimiento y crianza **conocido o inventado** si la biografía es coherente con 2383; no exigir catálogo ni documentación. Registrar el origen como hecho personal, no como entidad planetaria global | Cargos, secretos, rangos o permisos |
| `CITIZENSHIP_EVIDENCE_REQUIRED` | El producto todavía no aplica la regla autoral de ciudadanía por especie federada | **Regla APROBADA:** si la especie pertenece a la Federación => ciudadanía federada automáticamente, sea cual sea el lugar de nacimiento, mediante una regla F10 simple sin certificados ni IA. Fuera de especies federadas, ninguna ciudadanía se inventa | Membresía Starfleet, rango, admisión o permisos |
| `EDUCATION_EVIDENCE_REQUIRED` | Falta verificar trayectoria de educación antes de PERSON | Atestar educación general/civil narrativa **sin título ni habilitación**, si periodo y contexto son compatibles; títulos formales requieren trayecto/centro/criterio verificable dentro de la ficción | Doctorado, licencia, rango o puntos |
| `EXPERIENCE_EVIDENCE_REQUIRED` | Falta distinguir trabajo/experiencia civil de servicio institucional | Permitir experiencia civil razonable o **ninguna experiencia**, conservando su carácter narrativo; para mandos, accesos o años de servicio Starfleet exigir hechos institucionales existentes, nunca fabricarlos | Experiencia militar, competencia profesional acreditada, F11 |
| `PROFILE_EVIDENCE_REQUIRED` | Un `profile` sintácticamente válido no prueba que pertenezca a la sesión | Fuente privada HOST/H03: perfil local real del propietario de la campaña, identidad/versión/generación obtenidas de sesión confiable. **No leer `player_profile_id`, `nickname` ni identificadores autoritativos del borrador** | Identidad real de una persona, selección arbitraria de PERSON |

**No hay que crear «cinco certificados» para cubrir cinco campos.** Se necesita un evaluador de antecedentes iniciales F10 limitado y una fuente confiable para el perfil HOST. El registro actual de `RegisteredBiographyAuthority` ya proporciona el formato de atestación por problema.

## 5. Flujo propuesto de IA-03A (sin PERSON)

1. El HOST crea el contexto de campaña/identidad local **confiable**. El formulario únicamente propone campos del personaje.
2. El validador F10 comprueba **primero** formato, especie disponible, mínimo de edad, año 2383 y prohibiciones objetivas. Un rechazo inequívoco es `CHANGES_REQUIRED`, sin coste OpenAI.
3. F10 clasifica cada afirmación como `PERSONAL_BACKGROUND`, `SOURCE_REVIEW`, `LEGAL_STATUS_REVIEW` o `INSTITUTIONAL_AUTHORITY`, a partir de política/versiones aprobadas. Nunca confundir texto narrativo con una prueba.
4. El evaluador interno y la fuente H03 generan únicamente `BiographyClaimEvidence` cuya decisión esté justificada, para la **misma biografía canónica, contexto, generación, política y versión de regla**; incluyen fuente/emisor registrados. No existe setter cliente ni importación de evidencias desde IA.
5. Una afirmación no verificable se queda `REVIEW_REQUIRED`; una contradicción demostrable no queda suavizada por una «opinión» de OpenAI.
6. Solo con `OBJECTIVE_VALID` se envía el mínimo contexto a IA-02. `COHERENT` o sugerencias no equivalen a autorización de F10; `CHANGES_REQUIRED` exige correcciones. Error/timeout/clave ausente => `REVIEW_UNAVAILABLE`, sin recibo.
7. Tras ambas verificaciones, F10 genera **recibo privado** sujeto a `eligible`. IA-03A termina ahí. IA-03B hará posteriormente el alta de `PERSON`, vínculo H03 y guardado H04. No confundir estas responsabilidades.

### Atestación concreta: contrato interno reutilizado

No cambiar los tipos de entrada de cliente para simular procedencia. Reutilizar:
`BiographySourceIdentity` (id, version, issuer, origin), `BiographyEvidenceClaim` (IssueCode, field), `BiographyClaimEvidence` (source, claim, ReviewBinding, SUPPORTED/CONTRADICTED/INSUFFICIENT/NOT_APPLICABLE, revoked).

La nueva lógica debe **emitir** los registros tras evaluar el contenido, no construirlos en lote con `SUPPORTED` para todas las incidencias, como hacen exclusivamente las fixtures. Cada registro atestigua **todo el campo/colección** cubierto por su código y su política.

Si cambia cualquier elemento relevante del borrador, estado legal, fuente, perfil, política o generación, se invalida la atestación y se reevalúa. Contradicciones o revocaciones aplicables prevalecen incluso con otros respaldos positivos.

## 6. Decisiones de producto propuestas, pendientes de ratificación antes de implementar

**D-01 — Fondo personal ordinario:** permitir que una biografía ficticia plausible sea un antecedente narrativo inicial sin documentos reales; **no** confiere competencias, títulos o privilegios. Deriva del principio y clases de la política A5, pero su extensión productiva para origen/estudios/experiencia requiere implementación y revisión.

**D-02 — Ciudadanía federada automática de las tres especies inicialmente jugables: APROBADA POR EL AUTOR (15/11/2026).** Si el jugador crea un personaje de **especie perteneciente a la Federación**, F10 asignará ciudadanía de la Federación Unida de Planetas **independientemente del planeta natal**. No solicitar partida de nacimiento, certificado, expediente real, justificación adicional ni consulta OpenAI. Humanos, vulcanos, andorianos y tellaritas son especies fundadoras indiscutidas; para cualquier otra, usar pertenencia aprobada por el proyecto, no inventarla. Esta regla general **sustituye y engloba** la primera decisión humano+nacido en Tierra. No atribuye automáticamente membresía de Starfleet, rango, autorización, destino o plaza académica. La ciudadanía de especies **no** federadas se tratará por separado: no bloquear este caso por falta de una regla universal. No reintroducir comprobaciones burocráticas.

**D-03 — Educación y experiencia:** aceptar como narrativa no titulada «educación general», «afición a astronomía», «prácticas civiles supervisadas» y «sin experiencia laboral» si los datos temporales son compatibles. Los diplomas/credenciales formales o experiencia Starfleet se tratan aparte; no se acreditan automáticamente por autorrelato.

**D-04 — Origen libre, incluidos lugares inventados: APROBADO POR EL AUTOR (15/11/2026).** Se admiten orígenes reales del universo e inventados por el jugador, sin exigir catálogo, certificado, partida de nacimiento ni expediente; basta coherencia narrativa con Star Trek y la campaña 2383. No se publican por ello nuevos planetas como hechos globales ni se conceden cargos o permisos.

**D-05 — Edad:** mantener la política 0.1.2 sin pruebas de madurez; los tres casos especiales `changeling`, `jem_hadar`, `vorta` y el umbral de cumpleaños con día/mes no decidido quedan pendientes de decisión autoral. Ningún arreglo IA-03A los desbloquea indirectamente.

**D-06 — Frontera narrativa:** la aspiración a ser capitán es un **objetivo futuro** válido; «ya fui capitán durante quince años» es una **afirmación de pasado institucional** que requiere rechazo/evidencia, nunca un otorgamiento de rango. La IA puede detectar incoherencia adicional pero no puede legalizarlo.

**D-07 — Composición confiable:** el perfil H03 y las fuentes F10 se obtienen desde el HOST y un catálogo/política autoral, no desde el formulario. No crear una segunda cuenta ni un servidor.

**Ratificación parcial:** ciudadanía F10 automática para humano, vulcano e híbrido humano-vulcano; formulario detallado pero información personal adicional opcional. Ambas **APROBADAS por el autor**. Las demás decisiones se resolverán individualmente. Esta PR solo documenta, sin modificar código ni contratos históricos.

## 7. Riesgos adicionales detectados en la auditoría

**R-00 — Certificaciones coherentes con efecto en PERSON (MEDIO):** registrar una titulación ficticia validada (por ejemplo 4.º dan) como antecedente real de la PERSON; su traducción a destreza inicial debe usar las reglas de habilidades existentes o quedar explícitamente pendiente si aún no hay integración. Prohibido convertirla en dato meramente decorativo o exigir diplomas reales al jugador. La IA sugiere; F10 valida; CoreRPG registra.\n\n**R-01 — Sobreaprobación de fuentes (ALTO):** `RegisteredBiographyAuthority` ya comprueba un registro, pero las fixtures generan todos los `SUPPORTED` directamente. Si Codex copia ese patrón al producto, se aprueba cualquier texto. Exigir oráculos de decisión por campo y casos negativos; nada de «autocompletar los cinco registros».

**R-02 — Circularidad IA/objetivo (ALTO):** la puerta objetiva rechaza consulta IA cuando quedan evidencias pendientes. No usar la respuesta OpenAI como fuente que se autofirma para despejar esa puerta. Un relato muy elaborado tampoco confiere títulos.

**R-03 — Perfil introducido desde UI (ALTO):** `BiographyContext.profile` solo tiene verificación sintáctica; la posesión/identidad debe acreditarse desde sesión H03, y revalidarse con generación y campaña en la operación posterior. No permitir `player_profile_id` del borrador.

**R-04 — Campos libres confundidos (MEDIO):** el `draft_mapping` de `f10_formulario_inicial_v0.3.json` proyecta `biography` y `skills_narrative` en `prior_experience`. Esto puede reinterpretar aspiraciones como experiencia laboral o convertir texto libre en capacidades. En IA-03C, diseñar una proyección explícita entre campos/relato auxiliar, sin añadir claves prohibidas al borrador canónico ni dar autoridad al wrapper.

**R-04B — Mapeos ausentes en formulario v0.3 (MEDIO):** el formulario exige `citizenship` y recoge `upbringing_place`, pero `draft_mapping` no define un enlace explícito de esos campos a `citizenship_context` y `culture_context`. Tampoco `upbringing_type` del mapping figura en `common_fields` con ese nombre. IA-03C debe definir una conversión revisada y completa, con casos de pérdida de datos, antes de usar el formulario como entrada al F10 nativo. No inventar valores por defecto ni suprimir el campo requerido del contrato bloqueado.\n\n**R-05 — Actividades simultáneas (MEDIO):** `has_checkable_activity_budget` no avala automáticamente periodos solapados, incluso si dos aficiones son compatibles. No imponer una falsa prohibición de dos actividades; usar una evaluación F10 de tiempo suficiente o conservar `REVIEW_REQUIRED`. En el caso mínimo bastará una afición estructurada verificable.

**R-06 — Alcance de especies (MEDIO):** solo humano, vulcano e híbrido humano-vulcano son seleccionables inicialmente, según decisión expresa del autor. El catálogo nativo de 26 perfiles no amplía la selección. Evitar verificaciones de ciudadanía sobre especies fuera del lanzamiento inicial.

**R-07 — Pertenencia de especie a Federación (MEDIO):** la decisión autoral de ciudadanía automática exige identificar qué especies están aprobadas como federadas en el catálogo/continuidad del juego. No inventar afiliaciones, no crear procedimientos civiles ni requerir documentos. La Tierra de nacimiento no es condición; la ciudadanía no implica rangos ni permisos.

**R-08 — Confundir validación con creación (ALTO):** IA-03A no crea `PERSON`; IA-03B debe verificar recibo y `eligible`, admitir exactamente una solicitud en SessionOwner y garantizar publicación atómica, vínculo y recuperación sin elevar derechos.

**R-09 — Fuente de política histórica (MEDIO):** los JSON A3/A5 mantienen notas previas a PR #160/IA-01/IA-02. Respetar precedencias aprobadas y versionar adiciones sin reescribir contratos bloqueados.

**R-10 — Calidad semántica real (MEDIO):** IA-02 pasó pruebas con transportes y respuestas controladas, pero Luna real sigue `NOT_RUN`. Una prueba LIVE autorizada será necesaria antes de certificación extremo a extremo.

## 8. Matriz mínima de pruebas de IA-03A (casos propuestos, **NO EJECUTADOS**)

| ID | Borrador / contexto | Resultado exigido |
|---|---|---|
| A01 | Humano 20, nacido en Tierra o colonia exterior, ciudadanía Federación **automática por su especie conforme D-02**, educación general, ninguna experiencia, karate desde 8 | `OBJECTIVE_VALID` **solo después de resolver las demás fuentes F10 y perfil auténticos**; pasa a revisión IA |
| A02 | A01 sin conexión OpenAI | `REVIEW_UNAVAILABLE`, ninguna PERSON |
| A03 | Humano 17, restante ordinario | `CHANGES_REQUIRED`, cero HTTP |
| A04 | Vulcano 24 | `CHANGES_REQUIRED` por mínimo, cero HTTP |
| A05 | Humano 20; karate empezó a los 21 | `CHANGES_REQUIRED`, cero HTTP |
| A06 | Especie federada nacida en Tierra o fuera de su planeta natal (humano, vulcano, andoriano o tellarita) | F10 **asigna ciudadanía federada automáticamente** por pertenencia de especie, sin OpenAI ni certificado; no concede rango, plaza ni permisos |
| A07 | A01 con diploma oficial/certificación no respaldados | `REVIEW_REQUIRED`; ningún título concedido |
| A08 | A01 con servicio Starfleet/capitanía antigua declarados | No acreditar servicio/rango; contradicción objetiva o `REVIEW_REQUIRED` hasta verificación real, nunca aprobación ficticia |
| A09 | A01, `profile` o generación falsificada desde cliente | `REVIEW_REQUIRED`/rechazo, ningún recibo |
| A10 | A01; `evidence_ref` o emisor inyectado en texto cliente | No resuelve fuentes; campos de autoridad prohibidos rechazados |
| A11 | Cambio de origen/educación/perfil después de atestar | Rechaza atestación/recibo anterior; reevalúa con nueva huella |
| A12 | Revocación, contradicción entre fuentes o versión antigua | `REVIEW_REQUIRED`, aunque exista otro apoyo |
| A13 | Changelings, jem'hadar o vorta sin mínimo definido | `REVIEW_REQUIRED`, sin desbloqueo por fuentes genéricas |
| A14 | Ocampa en campaña principal | `CHANGES_REQUIRED`/DLC, cero HTTP |
| A15 | Biografía con dos aficiones simultáneas no incompatibles a priori | No «prohibir» por solapamiento; evaluar tiempo si hay política, o `REVIEW_REQUIRED` |
| A16 | Misma propuesta, texto «quiero ser capitán» vs «ya soy capitán» | Aspiración no otorga rango; pasado institucional requiere regla/fuente |
| A17 | A01 con revisión simulada `COHERENT` sin registro de procedencia | `REVIEW_UNAVAILABLE` o no elegible; ninguna PERSON |
| A18 | Caso positivo seguido de `eligible` con borrador/contexto cambiados | No reutilizar recibo, nueva revisión obligatoria |

Los resultados A01–A18 son **oráculos por implementar**; no figuran como PASS por haber sido descritos. Mantener regresiones históricas de `biography_tests.cpp`, IA-02, F04/F05/H03/H04 y F11, Windows/Linux y sanitizadores. La prueba LIVE de OpenAI será aislada, manual, de coste controlado y etiquetada separadamente.

## 9. Encargo IA-03A propuesto para Codex después de aprobar las decisiones

**Modelo recomendado: GPT-6.1 Sol — razonamiento MEDIO** para este corte acotado; escalar a ALTO solo si una auditoría revela refactorización delicada de autoridad o una dependencia de Core.

Alcance:
1. Releer este documento y fuentes; indicar cualquier contradicción normativa antes de código.
2. Crear únicamente los evaluadores/fuentes **internos F10/H03** necesarios para A01 y variantes, usando los puertos existentes y reglas aprobadas; ninguna fuente genérica «SUPPORTED» incondicional.
3. Probar que un jugador de especie federada con ciudadanía inferida automáticamente y sin certificados **puede** alcanzar revisión semántica; que afirmaciones formales y de permisos **no** reciben aprobación automática.
4. Respetar el doble filtro, binding/versiones, revocación, privacidad, cancelación, edad y política de 2383. Evitar cambiar el pin Core, F11, el servicio IA-01 o los contratos bloqueados.
5. Añadir pruebas de producto y negativas; PR Draft con informe y evidencia, sin fusión ni creación de PERSON.
6. Ejecutar regresiones disponibles Windows/Linux, ASan/UBSan, F10 Python, Release OFF y F11; informar explícitamente lo no ejecutado.

**Criterio de cierre IA-03A:** puede existir `OBJECTIVE_VALID` real de una biografía ordinaria respaldada por las fuentes F10/H03 esperadas; cualquier falta de fuente, regla, perfil o versión se bloquea. La revisión semántica sigue separada. Ninguna PERSON se crea en este corte.

## 10. Estado y decisiones pendientes

- **AUDITADO:** repositorio actual, reglas, interfaces, diferencias histórico/producto y puntos de bloqueo; sin ejecución nueva de tests en este documento.
- **DECISIÓN DE PRODUCTO APROBADA:** D-02 ciudadanía federada automática por especie perteneciente a la Federación (cualquier lugar natal). **DISEÑO PROPUESTO:** D-01 y D-03 a D-07, incluida ciudadanía de especies no federadas y antecedentes personales narrativos.
- **IMPLEMENTACIÓN IA-03A:** PENDIENTE.
- **IA-03B (PERSON/H03/H04), IA-03C (Unreal), OpenAI LIVE:** PENDIENTES.
- **H06/HU-08/M1:** NO CERTIFICADOS.

**Siguiente decisión de gobierno:** ratificar el alcance mínimo de D-01 a D-07 antes de pedir a Codex que convierta estas propuestas en reglas ejecutables. Evitar solicitar decisiones sobre la fecha exacta 2383, tres especies especiales y otras extensiones no necesarias para probar el candidato humano ordinario.
