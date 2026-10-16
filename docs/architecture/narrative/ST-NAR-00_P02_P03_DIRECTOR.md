# ST-NAR-00 — Arquitectura del Director de Acontecimientos (P02/P03)
# Estado
Decisiones D01–D09 aprobadas por el autor el 16-10-2026. Documento de diseño y contrato de autoría offline, NO integración CoreRPG/UE5 ni temporada narrativa aprobada.

## Autoridad y límites
- CoreRPG conserva la verdad, el tiempo, los eventos, las acciones, la identidad y el estado persistente. Star Trek define la semántica de temporadas, la doctrina, las órdenes y la coordinación.
- El director observa cambios autoritativos, evalúa elegibilidad, propone oportunidades, coordina arcos y filtra perspectiva; NUNCA confirma consecuencias, crea misiones unilateralmente o reescribe historia.
- UE5 presenta y la IA redacta o interpreta únicamente hechos autorizados y conocimientos accesibles. Una escena no altera World State.
- Reusar gameplay/missions/emergent_mission_from_world_state_contract.json, gameplay/command/mission_state.json, gameplay/command/operational_need_model.json, gameplay/command/mission_participation_by_role.json, narrative/events/world_event_state.json.

## Invariantes
1. El mundo y sus eventos existen independientemente de la visibilidad del jugador. No observar no causa ni cancela acontecimientos.
2. Estado de conflicto, estado de temporada y vinculación del protagonista son tres proyecciones independientes con referencias al mismo registro de eventos.
3. Una sola temporada principal en primer plano por campaña; arcos secundarios y conflictos NPC pueden coexistir.
4. D07: favorecer una oportunidad SOLAMENTE entre opciones ya operativamente elegibles y mediante la autoridad apropiada; prohibidas teletransportación de amenazas, alteración de eficacias NPC o inventar crisis.
5. D08: transición contextual si finaliza la temporada o deja de existir participación viable; espera temporal no supone abandono; puede no haber temporada principal.
6. D09: varios desenlaces, incluido fracaso o resolución NPC; nunca se exige victoria ni reinicio de guardado.
7. El capítulo NO es misión; un capítulo puede agrupar varias misiones, un hecho o ninguna tarea al jugador. No duplicar mission_state.
8. Carrera libre: ninguna historia concede rango o destino automáticamente; se aplican evidencias, vacantes y mando F11.
9. El reloj autoritativo es timestamp exacto de campaña; fecha estelar se deriva. No avanzar por días reales transcurridos fuera de juego sin política aprobada.

## Protocolo del director (propuesta de adaptador Star Trek)
1. Recibir el par (campaign_revision, event_cursor) desde la capa autoritativa; ordenar eventos por secuencia confirmada.
2. Actualizar índices de dependencias y detectar capítulos candidatos; no crear hechos por el mero hecho de haber contenido instalado.
3. Comprobar origen legítimo, era, fecha, estado, conocimiento permitido, capacidades, restricciones profesionales, inventario, misión actual y órdenes.
4. Entregar necesidades operativas al pipeline de Star Trek; la autoridad institucional escoge y formaliza la misión. La preferencia contextual es un desempate no coercitivo.
5. Emitir una propuesta de avance narrativo con event_refs, expected_revision e idempotency_key. El adaptador valida, confirma o rechaza de forma atómica.
6. Recalcular la perspectiva del jugador a partir de eventos y filtros de conocimiento; la IA NO tiene acceso por defecto a verdad oculta.

## Modelo de datos mínimo
SeasonDefinition: identidad, paquete/version, era, capacidades, origen de activación, grafo de capítulos.
ChapterDefinition: condiciones declarativas, dependencias, roles participantes, resultados y alternativas.
SeasonInstance: referencia a definiciones + versión inmutable instalada, estado por campaña y cursor de eventos.
ChapterProgress: estado y motivos, event_refs, tiempos y causa de transición, idempotencia.
PlayerSeasonEngagement: una ranura principal opcional, participación (PLAYER / NPC / MIXED / NONE), conocimiento y últimas interacciones.
NarrativeOpportunity: propuesta efímera no autoritativa (no orden/misión) con trazabilidad.
NarrativeEventLink: conecta capítulos con event_id/mission_id/order_id originales.
PackRegistration: identidad inmutable de la versión publicada, dependencias, digest y estado de instalación.

## Activación de premisas
El valor activation.origin=existing_world_event solo permite consumir un evento ya confirmado. El modo authorized_seed_candidate NO crea nada por sí mismo: exige una capacidad registrada y una propuesta a un generador/regla autorizada que materialice el evento antes de observarlo; el validador offline solo puede revisar declaración, nunca certificar que ese generador exista en Core.
Si no existe origen verificable: el capítulo permanece inelegible, no inventamos anomalías por presión narrativa.

## Estados y transición
El estado de misión sigue siendo gameplay/command/mission_state.json. Para capítulos se proponen LOCKED, CANDIDATE, AUTHORIZED, ACTIVE, SUSPENDED, RESOLVED, FAILED, EXPIRED, SUPERSEDED. La aplicación final dependerá de un evento confirmado y será idempotente; estado de participación distinto de estado de capítulo.
La transición entre principales usa cierre, inviabilidad duradera o resolución, no el simple transcurso de un cooldown. La existencia de relatos secundarios no bloquea vida a bordo.

## Reglas del pack P03
Las definiciones editables residen en narrative/story_arcs/seasons/ y las publicaciones derivadas, tras aprobación creativa, en content/packs/startrek/seasons/. Evitar dos copias maestras.
JSON Schema Draft 2020-12 documenta tipos y límites. Un validador de referencia stdlib comprueba subconjunto y vínculos cruzados; NO debe afirmar validación JSON Schema completa sin un motor adecuado.
Nada de código interpretado, expresiones libres, comandos embebidos, mutaciones de estado o rutas absolutas. Solo identificadores y relaciones autorizadas.
El fixture en validation/fixtures/seasons/reference_pack es exclusivamente una muestra estructural, nunca una temporada instalable. La Academia S00 se escribirá creativamente en ST-NAR-01.

## Dependencias y bloqueos de implementación
Faltan contratos/adaptadores CoreRPG para cursor atómico, referencias de historia, transiciones narrativas y extensión de saves, además de UE5/importación; no se asume que existan.
Quedan por demostrar la sincronía/atomicidad de Core, seguridad real de cargador, migración entre versiones, exactitud de exportaciones en partidas largas, integración con cadena de mando y representación. El CI offline no acredita estas pruebas.

## Decisiones aprobadas
D01 NPC autónomos; D02 nueva partida por defecto + compatibilidad optativa; D03 una principal, secundarias paralelas; D04 ritmo contextual; D05 consecuencias sin reinicio forzoso; D06 mejor expediente académico compatible sin importar recuerdos ajenos; D07 oportunidades legítimas; D08 transición contextual; D09 desenlaces múltiples.
Ninguna etapa autoriza crear una trama completa sin colaboración con el autor.