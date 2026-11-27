# F12 — LIVING WORLD: investigación de motores, técnicas y reutilización

**Fecha:** 2026-11-24. **Estado:** investigación documental y propuesta técnica autorizada para preparar F12; NO implementación, certificación, cambio del plan maestro ni nueva dependencia aprobada. **Prioridad de producto:** credibilidad de la vida social por encima del hiperrealismo AAA. Toda relación, memoria, decisión y consecuencia debe funcionar localmente, incluso con OpenAI desconectado. La IA generativa es una interfaz de interpretación/dialogo; jamás autoridad social.

## 0. Lectura obligatoria al retomar F12

1. Leer este informe junto con [README de F12](README.md), [acta de referencia](ACTA_P01_P05_REFERENCIA_2026-10-14.md), [anexo familiar](ANEXO_IDEA-0017_VIDA_PERSONAL_Y_FAMILIAR.md) y las fuentes contractuales existentes.
2. Auditar las versiones efectivamente fijadas de CoreRPG y HOST, no asumir que una capacidad documentada está implementada.
3. Ejecutar los prototipos externos seleccionados, fijar revisión/licencia, comparar con baseline propia y conservar evidencias. No descargar, copiar o añadir dependencias por el mero hecho de figurar aquí.
4. Desarrollar el laboratorio local con NPC↔NPC y jugador↔NPC antes de certificar una sociedad compleja en UE5. Preservar las cinco subfases oficiales; los paquetes LW son propuestas subordinadas, no nueva numeración aprobada.

## 1. Diagnóstico de nuestros cimientos

Inspección directa de main (rama de trabajo creada desde main el 24-11) y documentos CoreRPG consultados. No se compiló el código ni se midió rendimiento.

| Fuente existente | Ya define | Brecha a resolver |
|---|---|---|
| sistemas/gameplay/social/relationship_graph_model.json | Relaciones dirigidas, familiaridad, afinidad, confianza, respeto, intimidad, conflictos, historia y límites | Evaluador ejecutable, transiciones causales, actualización y decisiones |
| sistemas/gameplay/relationships/relationship_change_provenance_contract.json | Causa, valores antes/después, visibilidad, prohibición de amistad por mera proximidad | Resolver y validar transacciones reales, historial consultable |
| sistemas/ai/memory/character_memory_contract.json y lifecycle referido | Memoria episódica/social/profesional, saliencia, confianza, claves de recuperación, olvido sin borrar verdad | Formación, refuerzo, consolidación, presupuesto, recuperación local y versión persistente |
| sistemas/gameplay/personality/persistent_personality_profile_contract_v0.1.json | 24 dimensiones escalares y familias de etiquetas; semilla estable, evolución por experiencia | Motivos activos, valoración emocional, aprendizaje lento y explicación |
| sistemas/gameplay/social/social_event_rules.json | Familias de interacción, contexto, consecuencias asimétricas, consentimiento y rechazo | Generar candidatos, resolver aceptación/ejecución, efectos específicos y evitar bucles |
| sistemas/gameplay/social/social_knowledge_propagation.json | Canales, origen, confianza, privacidad, distorsión, verdad ≠ creencia | Difusión autónoma, competencia de testimonios, retractación y límites |
| F03/F04/F05 | Identidad, tiempo, persistencia y visibilidad; dotación/autoridad/agenda e iniciativa en cortes previos | Auditar APIs y pin actual; integrar sin duplicar scheduler, autoridad ni identidad |
| F12 referencia offline | 45 escenarios, cribado de actividad, proyección por observador, LOD visual, reproducción de hasta 24 meses | El replay recibe causas externas: NO demuestra que surjan por decisión autónoma; no save/load autoritativo ni rendimiento real |
| Academy Life v0.1 e IDEA-0017 | Bases de convivencia, continuidad académica, vida personal y familiar | Reutilizar el mismo grafo y ciclo vital; no crear otro simulador para Academia o familia |

La carencia crítica no es un catálogo adicional de emociones o relaciones: es un **bucle autónomo de generación, ejecución, observación y consecuencias**, con vida independiente del jugador. No sustituir los contratos actuales ni añadir un segundo World State. CoreRPG conserva la autoridad genérica; Star Trek aporta reglas, contenido y semántica social; HOST coordina proveedores y adaptadores; UE5 representa. Revisar qué tipos/capacidades genéricos requieren ampliación de CoreRPG, con su propio PR y pruebas. No meter canon Trek en la biblioteca genérica.

## 2. Método de selección y reutilización

Fuentes públicas primarias (repositorios, documentación de autores, artículos y charlas), revisadas documentalmente el 24-11-2026. La matriz diferencia: **R** referencia conceptual/reimplementación propia; **L** laboratorio externo desacoplado; **C** candidato a reutilización de componentes concretos, NO dependencia aprobada. Prioridades A (primera oleada), B (segunda), C (solo si resuelve problema medido). El coste es relativo, estimado, no benchmark.

### 2.1 Neighborly — A / L+C / coste bajo-medio

Fuentes: https://github.com/ShiJbey/neighborly ; https://neighborly.readthedocs.io/en/latest/ ; https://neighborly.readthedocs.io/en/latest/relationships.html ; https://neighborly.readthedocs.io/en/stable/life_events.html ; https://github.com/ShiJbey/neighborly/blob/main/docs/source/location-preferences.rst

Python, licencia MIT declarada por el repositorio. Usa entidades/componentes, relaciones con rasgos y estadísticas, eventos vitales extensibles y preferencias de lugares. La documentación describe pasos mensuales: excelente para historial y población lejana, no para cada interacción presencial.

**Traslado:** ejecutar un barrio de 20–100 personas convertido en dotación ficticia; mapear lugares a comedor, gimnasio, laboratorio y holocubierta, y ocupaciones a puestos. Utilizar sus ideas de reglas sociales y selección ponderada de eventos para construir candidatos según disponibilidad F04, afinidad y necesidades. La mera coincidencia aumenta oportunidad, nunca amistad automática. Traslado y guardias proceden de Core/HOST, no de Neighborly. Importar solo escenarios/resultados sintéticos de laboratorio (IDs de fixture, no personajes de la partida). Portar algoritmos pequeños o adaptarlos en C++ tras comparación; no ejecutar Python como segundo motor permanente. Comprobar versión exacta de docs/paquete, licencia y dependencias.

**Prueba:** mismas semillas y 20 agentes durante 1/5/10 años; comparar número/distribución de contactos, vínculos recíprocos, cambios de destino, aislados y repetibilidad. Medir minutos reales y memoria; no exigir que las cifras de Neighborly sean verdad humana. Resultado esperado: guía para distribución y eventos de baja fidelidad.

### 2.2 Talk of the Town — A / R+L / coste medio

Fuentes: Ryan et al., *Toward Characters Who Observe, Tell, Misremember, and Lie* (2015), https://ojs.aaai.org/index.php/AIIDE/article/view/12825 ; https://jamesryan.computer/ ; https://github.com/james-owen-ryan/talktown (localizador candidato; comprobar acceso/revisión/licencia antes de ejecutar).

Distingue lo observado, lo comunicado y los recuerdos imperfectos. Su modelo usa relevancia de personas y atributos para modular la adquisición, propagación y pérdida de conocimiento.

**Traslado:** ampliar implementación de character_memory_contract y social_knowledge_propagation sin duplicarlos. Cada creencia: observador, sujeto, proposición tipada, fuente/cadena de transmisión, momento, certeza, privacidad y última corroboración. El evento real queda inmutable. Si A interpreta mal una reprimenda y se lo dice a B, B puede guardar una afirmación incierta; C ausente no sabe nada. Recuperar recuerdos por persona, tipo, tema y saliencia, no enviar el historial completo a IA. Alteración/olvido afecta creencia, no expediente de servicio. Mentira deliberada como acción distinta, opcional tras verificar motivos y límites; no necesaria en MVP. Evitar distorsión de hechos oficiales por defecto.

**Prueba:** secreto en camarote, observación parcial desde corredor, rumor con tres eslabones, contradicción por parte oficial y reconciliación años después. Asegurar que nunca se atribuye el rumor a conocimiento directo y que ni el jugador ni la IA reciben datos privados no autorizados. Desafío: memoria y número de afirmaciones; deduplicación y compresión preservando origen. No integrar código externo si la licencia no es comprobable.

### 2.3 Comme il Faut (CiF) / Ensemble — A / R+L / coste medio

Fuente: https://github.com/ensemble-engine/ensemble y wiki del repositorio; antecedente Prom Week. Ensemble documenta esquema social, reglas de activación, reglas de intención (volition), acciones e historia. JavaScript; verificar LICENSE.md en revisión fijada.

**Traslado:** capa declarativa pequeña de reglas Trek (JSON validado, sin scripts arbitrarios). Separar (a) deseo de invitar a otro, (b) disponibilidad/autoridad y reglas de seguridad, (c) aceptación independiente, (d) ejecución, (e) efectos sobre participantes y testigos que realmente observaron. Un favor puede elevar confianza, un incumplimiento reiterado erosiona confianza aunque exista afinidad. Reglas de intención puntúan candidatos, reglas de efecto solo operan sobre evento confirmado. Reutilizar las familias actuales, no inventar un esquema paralelo. Índices por familia, rasgo y ámbito; evitar búsqueda combinatoria sobre todos los agentes.

**Prueba:** tres versiones del mismo conflicto con personalidades diferentes, situación de rivalidad triangular y reputación asimétrica. Reglas duplicadas o cíclicas no multiplican efectos: aplicar por event_id y rule_id una vez, con prioridades explícitas y presupuesto. Comparar motor de tablas simples con motor de inferencia; mantener el más barato que satisfaga los casos. No introducir un intérprete general hasta demostrar necesidad.

### 2.4 FAtiMA Toolkit — A / R+L / coste medio-alto

Fuente: https://github.com/GAIPS/FAtiMA-Toolkit ; https://www.gamecomponents.eu/content/582 . Arquitectura de valoración emocional, decisión y creencias. C#; catálogo reporta MIT para la versión descrita, verificar License.txt de la revisión exacta.

**Traslado:** usar su separación de valoración y decisión: evento → interpretación por observador según metas y creencias → emoción temporal → modificación de utilidad de las acciones. Valorar relevancia, control, responsabilidad percibida y expectativas. Un oficial puede experimentar gratitud hacia quien lo ayudó y vergüenza por su propio error. Las emociones transitorias no son cambios permanentes de personalidad ni demuestran hechos. No reconocimiento emocional del usuario ni captación externa: fuera de alcance. Seleccionar pequeño conjunto de emociones antes de modelos completos.

**Prueba:** ayuda, crítica pública, pérdida, ascenso, promesa incumplida y disculpa con personalidades contrapuestas; comparación de signo/intensidad/decadencia. Exportar tablas de valoración a fixture. Usar FAtiMA como referencia de diseño y banco aislado, no introducir CLR/Unity al runtime C++ sin justificación.

### 2.5 GAMYGDALA — A / R+C / coste bajo-medio

Fuentes: https://github.com/broekens/gamygdala ; https://ii.tudelft.nl/~joostb/gamygdala/index.html ; https://www.dare.uva.nl/id/35ae74ce-768e-445a-9d71-7a7cb0e884d3 . Autor declara MIT; motor basado en metas, utilidad y valoración de creencias. No necesita IA generativa.

**Traslado:** candidato preferente a MVP emocional por simplicidad. Meta activa proteger compañero/ser competente/descansar/cuidar familia; evidencia congruente o contraria, importancia, certeza y agente atribuido generan señal emocional acotada. Usar decaimiento por tiempo simulado, no por FPS. Desacoplar de FAtiMA: comparar ambos enfoques y elegir una sola política de appraisal; no sumar sus emociones dos veces. Un modelo propio C++ pequeño con interfaces deterministas es preferible a portar todo el motor JS.

**Prueba:** resultados esperados por evento y meta, saturación, evidencia contradictoria, persistencia temporal, no excitación repetida por evento duplicado. Perfil de CPU en lotes de 1.000 NPC; el paper no acredita nuestro rendimiento.

### 2.6 TDRS — A / R+C / coste bajo-medio

Fuentes: https://github.com/ShiJbey/TDRS ; https://github.com/ShiJbey/TDRS/wiki . C#/Unity; rasgos de agentes y relaciones, modificadores sociales condicionados, eventos sociales. Revisar LICENSE.md, no confundir con condiciones de Unity Asset Store.

**Traslado:** aplicar modificadores derivados de rasgos persistentes (p. ej. humor, afinidad musical) al cálculo de preferencia y al efecto de eventos en el grafo existente. Separar valor base causal de modificador contextual derivado; retirar el modificador cuando deja de cumplirse su condición. Evitar acumulación irreversible al recalcular. Rivalidad entre departamentos puede influir sin imponer enemistad a todos. No importar GameObjects ni duplicar relaciones de CoreRPG.

**Prueba:** A aprecia humor directo, B lo rechaza; el efecto de una broma varía. Cambio de afiliación retira modificador temporal sin borrar la amistad histórica. Los rasgos jamás sustituyen consentimiento o procedencia.

### 2.7 Versu — A / R / coste medio

Fuentes: Evans y Short, *Versu—A Simulationist Storytelling System*, https://ieeexplore.ieee.org/document/6648395/ ; https://versu.com/about/how-versu-works/ ; https://emshort.blog/2013/02/26/versu-conversation-implementation/ . Prácticas sociales como planes conjuntos reactivos; cada agente selecciona su propia acción por utilidad. No se presupone licencia de código.

**Traslado:** plantilla de práctica social con roles, contexto, acciones disponibles, turnos, duración, interrupciones y salida. Ejemplos: ajedrez, comida, consulta médica (privacidad), mentoring, reunión del puente, conversación informal. La práctica coordina, no obliga a responder ni escribe el resultado. Dos NPC se ponen de acuerdo, reservan hueco real, se encuentran o cancelan por alarma, y registran resultado. El jugador puede rechazar o intervenir explícitamente.

**Prueba:** tres participantes, ausencia de uno, interrupción por alerta, entrada tardía, conversación privada en sala compartida. Evitar secuencias de turnos infinitas. Implementar inicialmente cinco prácticas; no construir un DSL universal.

### 2.8 Aithena — A / L+C / coste medio, incertidumbre alta

Fuentes: https://github.com/sa-aris/aithena ; https://github.com/sa-aris/aithena/blob/main/README.md . README describe biblioteca C++17 modular, decisiones, percepción, memoria, relaciones, persistencia, mundo, pruebas, Lua y API C; MIT declarada. No equivale a certificación de madurez.

**Traslado:** inspeccionar interfaces de percepción/memoria/decisión, pruebas de consecuencias locales y benchmarks, revisar historial, CI, licencia y dependencias. Por idioma y CMake es el candidato más natural a reutilizar funciones aisladas si realmente superan el baseline. Crear ejecutable de laboratorio con fixtures equivalentes; mapear IDs externos solo en memoria del adaptador. No incorporar su World, reloj, persistencia, scripting Lua, scheduler o grafo si duplican CoreRPG. No permitir que código externo mutile autoridad. Portar pequeños componentes o probar interfaz pura candidata con entradas/salidas tipadas.

**Prueba:** build MSVC/GCC, tests propios, reproducibilidad, ausencia de red, sanitizadores, escalado 20/100/1.000, comparación de calidad y coste con implementación mínima. Rechazar si dependencia invasiva, código opaco o mantenimiento desproporcionado; MIT no garantiza calidad.

### 2.9 Anthology — B / R+L / coste medio

Fuente: Azad, Wellnitz, Garcia y Martens (2022), https://ojs.aaai.org/index.php/AIIDE/article/view/21967 ; https://sashazad.me/publication/azad-2022-anthology/ . Motivos, conocimiento relacional, acciones precondición-efecto y una interfaz de inspección. No verificada licencia de implementación.

**Traslado:** priorizar necesidades y objetivos que expliquen tanto ocio como carrera. Diseñar acciones con precondiciones, roles, resultados y motivaciones. Inspector que muestre candidatos descartados, utilidad y causas, no solo valor final. Usar F05 para iniciativa y F04 para obligaciones; no nuevo motor de órdenes.

**Prueba:** oficial exhausto decide dormir aunque su amigo lo invite; otro busca mentoría ante evaluación; un tercero prefiere ajedrez. Cambiar una motivación y observar causalidad en comparación contrafactual.

### 2.10 PsychSim — B / R+L / coste alto

Fuentes: https://github.com/usc-psychsim/psychsim ; https://ict.usc.edu/research/projects/psychsim-social-simulation/ . Agentes de decisión con teoría de la mente; verificar licencia y APIs antes de uso.

**Traslado:** no hacer teoría de la mente recursiva para mil tripulantes. Para agentes relevantes, estimación de primer orden de preferencias y respuestas de otro basada únicamente en creencias propias, no acceso a mente ajena. Prever aceptación probable de una invitación o consejo sin convertir probabilidad en consentimiento. Segundo nivel opcional solo ante conflicto importante.

**Prueba:** A cree que B lo apoyará por una promesa, B cambió de opinión en privado; A se sorprende y actualiza su modelo solo tras conocer respuesta. Límite de profundidad, candidatos y tiempo de cálculo.

### 2.11 Gossamer — B / R+L / coste medio

Fuente: https://github.com/mkremins/gossamer . El repositorio se presenta como herramienta de gossip para simulaciones narrativas; detalle del algoritmo/licencia pendiente de lectura de código.

**Traslado:** evaluar pertinencia de difundir un tema por interés, relación, confianza en fuente, riesgo social, confidencialidad, novedad y disponibilidad de canal. Los rumores son afirmaciones, no nuevos hechos del mundo. Un rumor repetido por dos personas con misma fuente no equivale a dos corroboraciones independientes. Limitar fan-out por contacto y presupuesto de evento.

**Prueba:** rumor sin contacto no viaja, persona discreta no divulga confidencia, dos testimonios del mismo origen se deduplican, corrección oficial llega solo a receptores autorizados. Verificar que no hay avalanchas ni difusión instantánea galáctica.

### 2.12 Felt — A / R+L / coste medio

Fuente: https://github.com/mkremins/felt ; https://mkremins.github.io/ . Consultas de patrones sobre historia de simulación.

**Traslado:** detectar arcos sobre el log confirmado, por ejemplo ayuda → deuda/agradecimiento → oportunidad de reciprocidad → ayuda efectiva. El patrón no crea ninguno de esos eventos. Indexar por tipo, tiempo y participante. Vista derivada: story_id, patrón, eventos origen, participantes, importancia, acceso por observador. Solo presentar al jugador hechos conocidos o que conozca por canal legítimo; inspector de desarrollo privilegiado separado. No usar narrador omnisciente.

**Prueba:** dataset con casos positivos y negativos (eventos fuera de orden, agente equivocado, coincidencia sin causalidad, secretos). El sifter no modifica estado ni altera RNG. Si no encuentra historias, no fabricar drama.

### 2.13 Winnow — B / R+L / coste medio

Fuente: https://github.com/mkremins/winnow ; https://mkremins.github.io/ . Patrones incrementales y parciales de historias.

**Traslado:** al superar coste de búsquedas históricas, mantener estado derivado incremental para arcos en desarrollo. Usar límites temporales y expiración; candidatos parciales pueden sugerir oportunidades de ocio/charla, nunca forzar acción o desenlace. Priorizar novedad y relevancia del jugador; controlar sesgo de selección y repetición. Si se pierde caché, reconstruir del log, no alterar verdad.

**Prueba:** misma historia detectada por análisis batch e incremental, tras save/load y tras cambio de nave; coste por nuevo evento acotado.

### 2.14 Viv — B / L+R / coste medio-alto

Fuentes: https://viv.sifty.studio/ ; https://viv.sifty.studio/introduction/ ; https://github.com/siftystudio/viv . Lenguaje de acciones, planes coordinados y patrones narrativos. Autor declara uso no comercial permitido y comercial sujeto a licencia: verificar condiciones concretas, no clasificar como MIT.

**Traslado:** laboratorio comparativo de acciones y cronologías largas; explorar expresividad de planes y consultas en casos equivalentes. No introducir su lenguaje/runtime ni su mundo autoritativo en la ruta principal. Si aporta una solución clara a coordinación de prácticas o sifting, reimplementar concepto con contratos propios o evaluar licencia de un componente.

**Prueba:** misma situación social descrita en Viv y tablas locales; medir complejidad de autoría, legibilidad y cobertura. Rechazar incorporación si requiere mantener dos crónicas o dos motores de acciones.

### 2.15 Mismanor / Grail — B / R / coste medio

Fuente: https://escholarship.org/uc/item/004129jn . RPG social basado en interacciones y niveles narrativos.

**Traslado:** permitir objetivos profesionales/personales resolubles de varias maneras mediante relaciones reales: solicitar mentoría, negociar un relevo voluntario, pedir consejo, reconciliar compañeros. La amistad no permite eludir protocolos de seguridad ni ascensos por favoritismo automático. Reutilizar reglas de F05/F11 para acciones que tengan efecto profesional. No introducir una trama artificial solo para exhibir relaciones.

**Prueba:** mismo problema con conocidos, amigos y desconocidos; cambia quién acepta y qué alternativa resulta viable, sin saltarse autoridad.

## 3. Experiencia comercial: estudiar resultados, no asumir código interno

| Referencia y fuente | Lección aplicada | Límite/prueba propia |
|---|---|---|
| Dwarf Fortress: https://dwarffortresswiki.org/Profile y https://dwarffortresswiki.org/Thoughts_and_preferences | Recuerdos fundamentales, necesidades y cambio lento de rasgos; perfil depurable | Una vivencia decisiva deja huella, cien saludos no regeneran personalidad; wiki secundaria |
| Shadows of Doubt: https://colepowered.com/shadows-of-doubt-devblog-2-finding-the-game/ | Simular habitantes y lugares antes de representarlos; registros consistentes | Turnos, presencia y contactos fuera de cámara; no extrapolar cifra ni rendimiento |
| Los Sims: autonomía por necesidades y oportunidades (referencia de producto) | Actividades de ocio con utilidad, variedad y duración, decisiones no guionizadas | Medir monotonía y hambre social; no afirmar algoritmo propietario |
| RimWorld (referencia de producto) | Opiniones derivadas de actos concretos, tensión y consecuencias visibles | Mostrar motivos comprensibles sin revelar secretos; no copiar código |
| Crusader Kings III (referencia de producto) | Continuidad vital, familia y relaciones que repercuten durante décadas | Guardar historia entre destinos y generaciones, sin forzar eventos |
| Wildermyth (referencia de producto) | Seleccionar situaciones compatibles con historia y personalidad | Storylet condicionado por hechos, no generar pasado retrospectivo |
| Sombras de Mordor (referencia de producto): https://patents.google.com/patent/US10926179B2/en | Reconocer encuentros previos y consecuencias personales | Inspiración general, no clonar sistema Némesis; revisar alcance de patentes si alguna vez se plantea reutilización específica. No extraer código ni afirmar libertad jurídica |

GTA VI es una aspiración de experiencia del usuario, no evidencia de su implementación interna. Los títulos comerciales son referencias de diseño, no candidatos de código; cuando no hay documentación primaria técnica verificada se indica expresamente.

## 4. Catálogo de técnicas e implementación concreta

| Técnica | Propuesta propia | Prioridad |
|---|---|---|
| Física social / Social Exchanges | Reglas disparadas por acción confirmada y dimensiones de relación, efectos dirigidos | A |
| Utility AI | Filtrar restricciones, puntuar necesidades, metas, relación, contexto y coste; desempate por RNG explícito | A |
| GOAP (Orkin, F.E.A.R.) | Solo planes pequeños con precondición/efecto: buscar hueco, invitar, reservar, acudir; replantear ante alerta | B |
| BDI | Creencias privadas, deseos ponderados, intención persistente hasta éxito/cancelación; no motor formal completo inicialmente | A |
| OCC | Evaluar consecuencias para metas y responsabilidades; subconjunto inicial | A |
| Big Five/OCEAN | Referencia conceptual, no reemplazar las 24 dimensiones existentes ni añadir duplicados | B |
| Memoria episódica | Recuerdo de acto confirmado/observado con referencia, relevancia y certeza | A |
| Memoria semántica | Conocimiento tipado por observador; reutilizar proyecciones Core | A |
| Consolidación | Detalle se atenúa; recordar gist, promesas y sucesos críticos; límites por NPC y tipo | A |
| Grafos sociales dirigidos | Aristas dispersas por contacto real; consultas por participante, no matriz N² | A |
| Teoría de la mente | Estimación de primer orden solo desde creencias, sin omnisciencia | B |
| Propagación de información | Mensajes y rumores por canal, procedencia y receptores; límite de saltos y duplicados | A |
| Social Practices | Plantillas coordinadas con roles, fases, interrupción y decisión propia | A |
| Multiagente | Proponer intenciones desde snapshot autorizado, resolver conflictos en orden estable | A |
| Story Sifting | Detectar patrones causales en log confirmado; solo lectura | B |
| Storylets | Ofrecer oportunidades compatibles con historia y permisos, no imponer resultados | B |
| Social LOD | Resolución individual activa, simplificada y agregada; conservar historia de todos los identificados | A |
| Eventos discretos | Cola por tiempo simulado, presupuesto de pasos, cambios relevantes y pausa/catch-up acotados | A |
| Grafo causal | Evento padre y referencias a causas, transición con antes/después, inspección reproducible | A |
| Histéresis y enfriamiento | Evitar oscilación de amistad, fatiga de acciones y ciclos de invitaciones; no umbral único | A |

Fuentes complementarias: Kevin Dill y Dave Mark, GDC, https://www.gdcvault.com/play/1012841/Improving-AI-Decision-Modeling-Through ; GOAP recursos de Jeff Orkin, https://static.hlt.bme.hu/semantics/external/pages/GOAP/alumni.media.mit.edu/_jorkin/goap.html . Los detalles de adaptación son propuestas nuestras; no citas textuales ni afirmación de que todos los autores usen nuestras fórmulas.

## 5. Arquitectura propuesta: un bucle, una verdad

Flujo por tiempo de campaña, no cada frame:

1. El scheduler existente ofrece oportunidades (tiempo, ubicación, guardia, instalación, otros agentes) y despacha eventos del mundo.
2. Cada NPC recibe exclusivamente su vista autorizada. Genera candidatos a partir de motivos y relaciones conocidos: descansar, estudiar, conversar, invitar, ayudar, evitar, pedir consejo, disculparse.
3. Filtro duro de autoridad, tiempo, ubicación, acceso, edad/consentimiento según contratos, capacidad y disponibilidad. Rechazar antes de puntuar. El deseo del jugador nunca se deduce por IA.
4. Utility ordena candidatos factibles; si es útil, plan GOAP corto. NPC receptor decide por su cuenta. Resolución de reservas/acciones en orden estable; revalidar revisión, tiempo y permisos al ejecutar. Un intento no equivale a evento completado.
5. Core/HOST confirma evento causal y observadores autorizados; el motor de valoración propone cambios derivados. Validar y aplicar una sola vez con identificadores y versión de reglas. Si falla la operación, no quedan efectos parciales.
6. Memoria de cada observador, creencias, emoción, relaciones y motivos se actualizan conforme a reglas. Terceros reaccionan únicamente si se enteran. Generar siguientes oportunidades, no cadenas infinitas de reglas.
7. Sifter lee el historial y señala arcos o temas. UI, UE5 y diálogo consumen vistas filtradas. No escriben relaciones directamente.
8. Guardar estado, intenciones pendientes, agenda, RNG, reglas/versiones y curso de eventos mediante mecanismos Core/HOST auditados. Reconstruir caches derivados; replay idempotente.

Interfaces conceptuales (NO APIs existentes): SocialOpportunity, SocialIntent, SocialActionRequest, ConfirmedSocialEvent, AppraisalResult, RelationshipDelta, MemoryRecord, BeliefClaim, StoryMatch. Adaptar nombres/tipos a contratos ya existentes. El evaluador debe ser puro donde sea posible; las mutaciones solo por frontera de autoridad. No duplicar WorldState.

### Decisión y emoción, ejemplo de tuning inicial

Puntuación de candidato = suma ponderada de necesidad, meta, afinidad, expectativa de resultado y oportunidad, menos coste, riesgo y repetición. Normalizar factores y usar curvas no lineales cuando se justifique. Selección entre candidatos casi empatados mediante RNG reproducible; conservar el desglose. No fijar pesos universales: calibrar por escenarios; elección de descansar válida y preferible a socializar siempre.

Valoración inicial = relevancia de la meta × impacto percibido × certeza, modulada por rasgos y atribución. La emoción decae en tiempo simulado; cambiar estado duradero requiere evidencia específica. Evitar confundir el impacto percibido con verdad. Las fórmulas son hipótesis de MVP, no modelos psicológicos validados.

### Relaciones auténticas

Conservar dimensiones del contrato. Separar amistad de respeto profesional y de intimidad; preferir historial de evidencias variadas (reciprocidad, confianza probada, tiempo, interacción elegida), no barra única de regalos. Afinidad puede facilitar iniciar conversaciones, no producir amistad por sí sola. Usar histéresis en estados, saturación y ventanas de evidencia, y registrar el hecho que justificó cada transición. Las ausencias no borran vínculos, el contacto a distancia es una acción con canal real. Perdonar no equivale a olvidar; obedecer no equivale a confiar. No imponer amistad, pareja o enemistad por guion, especie, rango o presencia del jugador. Respetar decisiones autorales y reglas de consentimiento ya aprobadas; ningún valor interno sustituye la aceptación.

### Memoria, personalidad y rumores

Registro de verdad separado de recuerdo subjetivo. Emplear índices por observador, participante y tema; consolidar recuerdos ordinarios repetidos en resumen con referencias, conservar eventos críticos y las consecuencias confirmadas. La evolución de rasgos necesita causa, límites y baja frecuencia; no reroll en LOD ni ascenso. No deducir rasgos de especie. Los rumores llevan fuente, certeza y versión; controlar repetición, confidencialidad, y correcciones. No comunicar datos de Inspector a IA ni jugador.

### LOD y coste

- A: agentes con interacción próxima o situación importante; decisiones por oportunidad, recuerdos ricos.
- B: agentes identificados fuera de escena; agenda real, decisiones discretas y memoria relevante; conservar IDs y vínculos.
- C: población agregada no materializada; estadísticas y flujos, no atribuir recuerdos individualizados inexistentes. Si se materializa un agente, respetar procedencia y no inventar una relación con el jugador.
- Cambiar LOD visual no cambia verdad; el LOD lógico afecta granularidad, con equivalencia de invariantes. No mover al NPC mágicamente ni borrar decisiones pendientes.
- Índices por lugar/agenda y vecindad social; máximo K candidatos configurables (empezar 8–16, medir), procesamiento por evento, colas y caché invalidada por revisión. Evitar N²: 1.000 agentes con 30 vínculos salientes medios son 30.000 aristas frente a 999.000 de grafo dirigido completo; ejemplo de diseño, no medida. No escanear grafo entero por interacción.
- Ninguna consulta a OpenAI, red o GPU requerida para lógica. IA de diálogo recibe únicamente proyección autorizada y contexto relevante; devuelve texto o propuesta de intención tipada que debe ser validada. Con IA desconectada, usar diálogos/actos convencionales y seguir simulando. Las palabras libres del jugador solo provocan efectos sociales por una acción validada (ej. disculpa/ofensa explícita o clasificación confirmada), no por un texto generado sin verificar.

## 6. F12-LAB LIVING WORLD: plan experimental propuesto

No presupone nuevas fases oficiales. Separar laboratorio (laboratorios/F12/living_world, según política local del repositorio) y evidencia/versiones documentales duraderas en F12. Reutilizar el baseline de 45 escenarios, no sustituirlo.

| Paquete | Entregable y evidencia | Vinculación F12 | Responsable propuesto |
|---|---|---|---|
| LW-00 | Auditoría de contratos, APIs reales, pin Core/HOST, licencias y revisión exacta de fuentes; matriz de brechas | P01 | ChatGPT diseño/auditoría + Codex técnico |
| LW-01 | Laboratorio aislado: Neighborly, Aithena, Ensemble; MVP propio comparable, fixtures y logs | P01/P05 | Codex/ChatGPT según entorno; MSI para ejecución nativa |
| LW-02 | Scheduler social, oportunidades y Utility; 20 NPC, sin jugador ni red | P02/P03 | Codex C++ |
| LW-03 | Prácticas sociales y eventos confirmados con aceptación, cancelación y restricciones reales | P02/P03 | Codex + diseño ChatGPT |
| LW-04 | Valoración emocional, motivos y rasgos; comparar GAMYGDALA/FAtiMA | P01/P03 | ChatGPT reglas/fixtures + Codex |
| LW-05 | Relaciones direccionales, transiciones justificadas y mantenimiento de vínculos | P01/P03 | Core/HOST, Codex |
| LW-06 | Memoria/creencias, rumores, conocimiento privado y recuperación para diálogo | P01/P03 | Core/HOST, Codex |
| LW-07 | Sifting e inspector de desarrollo, consultas autorizadas, narrativa emergente | P03/P05 | ChatGPT patrones + Codex |
| LW-08 | LOD lógico, tiempo discreto, 50/100/500/1.000 NPC y save/load | P04/P05 | Codex y MSI |
| LW-09 | Integración con guardias, Academia, carrera, LIFE y traslados; pruebas E2E | P02/P05 | Codex |
| LW-10 | Representación UE5, pruebas de naturalidad y aceptación por propietario | P04/P05 | Codex + propietario |
| LW-11 | Auditoría de cierre, decisiones, métricas, regresiones F03–F05/F10/F11 | P05 | ChatGPT/Codex + propietario |

No iniciar desarrollo por el mero hecho de registrar esta investigación. Al retomar F12, decidir alcance de LW y posibles cambios del Plan Maestro; evitar alterar fases activas.

### Experimentos y criterios de aceptación

**E0 reproducibilidad:** mismas semillas, versiones y entradas → mismo estado e historial canónico (considerar aleatoriedad por streams y orden explícito). Sin red, cero llamadas generativas. Save/load en mitad de invitación, alerta y rumor; comparar ejecución continua, sin duplicados o desapariciones. Con red caída, mantener autonomía.
**E1 causalidad:** sin contacto plausible o canal, no existe cambio social nuevo; familiaridad no amistad; cada transición significativa rastrea causa confirmada, percepción y regla. Caso negativo: replay de evento duplicado no suma confianza; texto IA no crea hecho. 
**E2 individualidad:** al menos 20 perfiles, mismas experiencias controladas, respuestas diferentes y explicables. Caso contrario: el mismo perfil y semilla reproduce resultado. No todos hacen amigos ni se enamoran.
**E3 autonomía:** simulación sin jugador; NPC eligen ocio, rechazan invitaciones, colaboran, crean vínculos/conflictos y pueden reconciliarse. No exigir que todos los escenarios produzcan drama; medir tasas de eventos, variación y ausencia de cambios arbitrarios. Semillas propuestas 10 para MVP, ampliar a 30 para validación; sin selección de resultados favorables.
**E4 conocimiento:** privado vs público, testigos parciales, rumor, fuente compartida, corrección, olvido. Cero revelaciones no autorizadas en UI/IA, incluyendo patrones narrativos y logs de usuario.
**E5 vida larga:** simular 1/5/10 años inicialmente y 30 como objetivo de estrés; traslados, ascensos, fallecimientos, familia si está en alcance, continuidad y promesas. Sin retroescribir historia ni resolver una cita pendiente como si hubiera ocurrido.
**E6 escala:** 20 → 50 → 100 → 500 → 1.000 NPC, distintos horizontes; observar p50/p95/p99 tiempo por lote, latencia bajo carga, CPU, RAM, tamaño de guardado, crecimiento de aristas/recuerdos, tiempo catch-up. Comparar MVP vs variantes externas con mismo fixture. No prometer 30 años en minutos ni fijar SLA definitivo antes de medir. Objetivo exploratorio MSI: durante juego, trabajo social incremental con presupuesto configurable y sin bloquear el hilo de render; valorar inicialmente 1–2 ms/frame de entrega al game thread (no coste total) y ejecutar lotes en tiempo simulado según contrato; medir en RHI real. No mover mutaciones a hilos no autorizados. 
**E7 naturalidad:** inspector privado presenta biografías derivadas y motivos; propietario revisa historias anonimizadas por semilla sin saber si son baseline o variante. Puntuar 1–5 coherencia, personalidad, consecuencia, variedad y continuidad; anotar ejemplos repetitivos y absurdos. Criterio provisional: ninguna violación de invariantes, mejora observable sobre baseline en al menos coherencia y causalidad, y revisar todos los casos de puntuación 1–2. La nota no acredita psicología humana. Mantener catálogo de regresiones de comportamiento.
**E8 integración:** NPC físicamente ausente sigue actuando; volver a su ubicación conserva identidad/estado. UE5 representa agenda, conversación y consecuencias autorizadas; F04/F05 autoridad y F11 ascensos no se alteran por afecto. Guardado de campaña compatible o migración explícita.

### Fixture de oro: oficial desconocido → amigo a largo plazo

20 NPC ficticios, nave con turnos y lugares finitos. Protagonista A y NPC B inicialmente desconocidos; C compañero de B; D testigo parcial. Disponibilidad de ajedrez y motivos compatibles crean oportunidad, no relación. Si B elige invitar y A acepta, evento confirmado. Posteriormente A ayuda a B durante guardia, B conserva recuerdo; otro evento puede generar tensión. Una oportunidad de disculpa puede prosperar o fracasar; con suficiente historia causal variada, surge amistad, no garantizada por fixture. Traslado de B, mensajes por canal real y posible reencuentro. Verificar historia, independencia del jugador, recuerdo y motivos. Ejecutar variante sin jugador, variante con A que rehúsa todo y variante con A que incumple promesas. No guionizar el desenlace para hacer pasar la prueba. 

### Inspector

Dos niveles separados: (1) herramienta privilegiada de QA con ID, hora, agenda, intención, lista de candidatos y motivos de descarte, rasgos, emoción, grafo antes/después, recuerdos y referencias de causa, LOD, métricas y replay; (2) UI de jugador, solo actos, observaciones y conversaciones autorizadas. Nunca usar nivel 1 como prompt de diálogo.

## 7. Orden de inversión y condiciones para reutilizar software

**Primera oleada:** Neighborly para comunidad/largo plazo; Ensemble y TDRS para reglas; GAMYGDALA frente a FAtiMA para emoción; Aithena para C++ y benchmarks; Talk of the Town para memoria. En paralelo, una implementación mínima propia para comparación. **Segunda:** Versu para prácticas (diseño desde el MVP), Felt para lectura de historias, Anthology para motivaciones/inspector, Gossamer para difusión, Winnow para escala, PsychSim y Viv como experimentos selectivos. No mantener simultáneamente 15 motores.

Antes de copiar o vincular un componente, registrar: URL, commit/tag, fichero LICENSE real y avisos, licencia de dependencias, API/superficie, coste de portar/integrar, resultados de CI y tests locales, determinismo, mantenimiento, seguridad/supply chain, titular de estado, decisión adopt/reimplement/reject y mecanismo de retirada. No asumir que disponibilidad pública equivale a código reutilizable. MIT declarado en Neighborly, GAMYGDALA y Aithena no sustituye esa comprobación. No se ha descargado ni ejecutado código externo en esta investigación. No introducir dependencias, telemetría ni licencias restrictivas sin evaluación. El proyecto es privado; igualmente merece trazabilidad técnica y evitar dependencias problemáticas.

Regla de decisión: si una biblioteca pequeña, compatible y mantenible resuelve mejor una necesidad probada, reutilizarla. Si el motor es útil pero su arquitectura invade Core, adoptar el algoritmo o la idea sin duplicar autoridad. Si no aporta diferencia comprobable, descartarlo. No programar por orgullo algo ya resuelto, ni integrar por novedad.

## 8. Registro de riesgos

| Riesgo | Mitigación |
|---|---|
| Mundo social aparentemente vivo pero guionizado | Prueba sin jugador y sin eventos sociales suministrados |
| Todos se hacen amigos por repetición | Evidencia variada, rechazo autónomo, saturación y relaciones asimétricas |
| Caos de rumores o melodrama permanente | Presupuesto, motivación, novedad, privacidad, ausencia de drama como resultado válido |
| IA omnisciente o alucinaciones | ObserverView filtrada; validación de acciones, simulación local |
| Estado duplicado entre Core y motor externo | Un dueño; laboratorios desacoplados; adaptadores puros |
| Complejidad de reglas incontrolable | Catálogo pequeño, inspector, pruebas por regla y escenarios negativos |
| Coste cuadrático o crecimiento sin límite | Grafo disperso, índices, eventos discretos, compactación, LOD, benchmarks |
| Inconsistencia por simultaneidad, save/load o LOD | Orden estable, transacciones idempotentes, RNG explícito y pruebas de interrupción |
| Métricas favorables pero comportamiento artificial | Revisión cualitativa ciega, múltiples semillas, regresiones semánticas |
| Sobrecarga de desarrollo | MVP por escalones y stop/go; evitar DSLs/planificadores complejos sin evidencia |
| Licencias y mantenimiento de terceros | Inventario y revisión por versión, no incorporar en este PR |

## 9. Conclusiones y decisiones pendientes

Priorizar el comportamiento por encima de recursos AAA es dirección del autor. La presente investigación recomienda un motor social local basado en acontecimientos, motivaciones, memoria, valoración y reglas, reutilizando cimientos de F12. No necesita OpenAI para vivir. El valor de los modelos generativos reside en interpretar el estado y conversar.

La viabilidad está respaldada por antecedentes, no por una prueba de nuestro juego. El mayor riesgo es calidad emergente, no persistir variables. No afirmar que las capacidades de otros motores estén ya disponibles en Core. No certificar F12 por green CI de documentación. Queda pendiente ejecución comparativa de software externo, revisión de licencias por commit, inspección completa de APIs y validación en MSI. No se han cambiado canon, números de fases, estado global ni contratos oficiales. 
