# IDEA-0014 — Intercomunicadores inteligentes en puertas de camarotes

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación conceptual y registro:** 4 de noviembre de 2026  
**Estado:** **APROBADA CONCEPTUALMENTE; pendiente de planificación, implementación en UE5/CoreRPG y pruebas.**  
**Decisión del autor:** «Dale», tras describir expresamente el flujo de timbre, respuesta libre del jugador, interpretación de IA y ejecución estructurada, y aceptar la propuesta bidireccional.  
**Alcance prioritario:** puertas de camarotes de las naves, especialmente la Clase Valhalla; extensible posteriormente a despachos y otras salas con privacidad.  
**Principio rector:** **la IA interpreta la intención expresada en lenguaje natural; el motor del juego valida y ejecuta la decisión en el estado real.**

## 1. Idea principal

Dotar a las **puertas de cada camarote** de un **panel exterior de intercomunicación con botón**, con el aspecto y un **aviso sonoro reconocible de Star Trek**, para permitir visitas y comunicaciones creíbles entre el jugador y los NPC.

No se trata de abrir puertas pulsando una tecla ni de un simple diálogo cosmético: el timbre origina una solicitud real, los personajes que están en su camarote pueden contestar, la persona que llama puede identificarse o explicar qué desea, y la decisión de abrir, esperar, denegar o continuar hablando se materializa únicamente cuando el sistema autoritativo la valide.

**Debe funcionar en ambos sentidos:**
- **Jugador visitante:** pulsa el intercomunicador ante el camarote de otro NPC, escucha el aviso/respuesta y espera la decisión del ocupante legítimo.
- **Jugador en su camarote:** recibe un aviso cuando un NPC llama y puede **responder libremente**, hablando o escribiendo: «¿Quién es?», «Adelante», «Espere un momento», «¿Qué necesita?», «Ahora no», o cualquier frase cotidiana equivalente.
- **NPC↔NPC:** el mismo mecanismo puede resolver llamadas entre NPC cuando haya relevancia simulada, sin cargar actores o reproducir audios innecesarios fuera de cámara.

## 2. Experiencia del jugador: visita a un NPC

1. El jugador se acerca físicamente a un **camarote existente**, sin teleportarse ni inventar una habitación.
2. Interactúa con el botón junto a la puerta, si está disponible y no hay una llamada activa incompatible.
3. El panel reproduce el sonido correspondiente **en el interior del camarote**; puede producirse también confirmación local para el visitante, pero no se presupone que oiga físicamente el timbre interior a través de una pared aislada.
4. El sistema consulta presencia/ocupación, horario, privacidad, descanso, daños y estado de intercomunicaciones del camarote.
5. Si un NPC está allí y es capaz de responder, **ese mismo NPC persistente** decide cómo actuar conforme a sus circunstancias, su personalidad y las reglas: «¿Quién es?», «Adelante», «¿Qué quiere?», «Vuelve después», «Un momento».
6. Si el NPC requiere identificación, el visitante puede responder por intercomunicador sin abrir la puerta. Una respuesta natural puede convertirse en solicitud estructurada de identidad, motivo o apertura.
7. Solo cuando el ocupante **autorice** la entrada y las restricciones físicas/de seguridad lo permitan, el motor cambia el estado de acceso y UE5 reproduce la apertura animada.
8. El NPC puede estar fuera, dormido, indispuesto o no querer contestar; una llamada **no garantiza respuesta ni acceso**.

**No teleportar al NPC desde otro departamento ni atribuirle información privada sobre el visitante sin una vía legítima de conocimiento.** Si está ausente, deben existir respuestas apropiadas de no contestación o señalización permitida.

## 3. Experiencia del jugador: un NPC llama a su camarote

1. Un NPC disponible y con motivo social/profesional plausible llega realmente a la puerta del camarote del jugador.
2. **Pulsa el intercomunicador** y se reproduce un sonido interior de estilo Star Trek. La pantalla permite atenderlo sin abrir automáticamente.
3. El jugador puede expresarse **con lenguaje natural libre** (entrada de texto y, cuando esté disponible, voz con transcripción): no se exige escoger únicamente un menú de frases fijas.
4. El intérprete de IA recibe texto/transcripción y **contexto mínimo autorizado**: quién es el propietario del camarote, si se conoce al visitante, quién pulsó, estado de la llamada, ocupación y acciones permitidas.
5. La IA genera una **intención estructurada candidata** y, si procede, parámetros o aclaración: solicitar identificación, conceder entrada, pedir espera, rechazar, preguntar motivo, terminar, combinar instrucciones compatibles.
6. El juego **valida identidad, autoridad, contexto, estado de puerta y seguridad**. El intérprete no abre la puerta ni modifica el estado persistente por sí mismo.
7. El ejecutor confirma la acción: puede reproducir un diálogo en el panel, abrir la puerta, mantenerla cerrada, registrar una espera o rechazar la solicitud.
8. El NPC reacciona según sus capacidades, preferencias, horario y continuidad; no tiene por qué aceptar una espera ilimitada ni permanecer junto a la puerta durante una alerta roja.

**Ejemplos funcionales de lenguaje libre (IDs provisionales, NO contratos ya implementados):**

| Respuesta del jugador | Intención interpretada | Comportamiento validado esperado |
|---|---|---|
| «¿Quién es?» | `REQUEST_IDENTITY` | Puerta cerrada; solicitar al visitante que se identifique. |
| «Adelante» / «Pasa, hombre» | `GRANT_ENTRY` | Validar invitado/seguridad y abrir solo si procede. |
| «Espera un momento, estoy ocupado» | `REQUEST_WAIT` | Puerta cerrada; avisar al NPC y registrar espera con límites. |
| «Ahora no puedo atenderte» | `DENY_ENTRY` | Puerta cerrada; comunicar rechazo y cerrar interacción. |
| «¿Qué necesitas?» | `REQUEST_REASON` | Puerta cerrada; permitir respuesta del visitante. |
| «Pasa y cierra la puerta» | `GRANT_ENTRY` + `REQUEST_CLOSE_AFTER_ENTRY` | Autorizar acceso si es seguro y cerrar detrás según el sistema de puertas. |
| «Si eres la doctora, pasa; si no, espera» | `CONDITIONAL_ENTRY` | Verificar identidad real; **nunca abrir por conjetura**. |
| «No sé quién está ahí» | `NEEDS_CLARIFICATION` | Preguntar o conservar estado de espera sin abrir. |

La comprensión de frases complejas no implica ejecutar cualquier petición arbitraria: **la IA clasifica solo acciones que el juego conoce, y pregunta o responde sin actuar cuando no puede ejecutar algo**.

## 4. Dos papeles de la IA: comprensión de órdenes y diálogo natural

### A. Interpretación de intención con límites estrictos

```text
NPC EN LA PUERTA / BOTÓN
       ↓
AVISO SONORO Y SESIÓN DE INTERCOMUNICADOR
       ↓
VOZ O TEXTO DEL JUGADOR
       ↓
TRANSCRIPCIÓN (si hay voz)
       ↓
INTÉRPRETE IA + CONTEXTO AUTORIZADO
       ↓
CANDIDATO DE INTENCIÓN ESTRUCTURADA
       ↓
VALIDACIÓN ESQUEMA / IDENTIDAD / AUTORIZACIÓN / SEGURIDAD
       ↓
EJECUTOR DEL JUEGO / WORLD STATE AUTORITATIVO
       ↓
RESULTADO: MENSAJE / ESPERA / APERTURA / RECHAZO / CIERRE
       ↓
UE5 (ANIMACIÓN, AUDIO, PRESENTACIÓN) + REACCIÓN DEL NPC
```

El principio ya documentado en [contrato de interpretación de órdenes](../../sistemas/ai/command_interpretation/starship_command_contract.md) es **«AI interprets. Core executes.»**. Se reutilizará como **patrón**, pero un intercomunicador **no debe introducirse a la fuerza como orden táctica de nave**: habrá que comprobar contratos reales y definir, si hace falta, un esquema especializado para `IntercomInteractionIntent` y un ejecutor de puertas.

### B. Conversación social natural

Una vez que el NPC responde o pide explicaciones, un diálogo contextual puede usar la IA narrativa habitual, **sin atribuirle autoridad de abrir puertas, teletransportar visitantes ni decidir unilateralmente una amistad**.

**Optimización de costes:** timbre, mensajes obvios y respuestas de acciones deterministas pueden resolverse localmente; llamar a IA externa solo cuando se requiere comprensión libre, ambigüedad o diálogo narrativo real. Evitar una llamada de IA por cada sonido o animación. La elección concreta de modelos/API queda pendiente.

**Privacidad:** aportar al modelo solo datos autorizados por conocimiento y contexto; evitar exponer secretos del jugador/NPC o telemetría de toda la nave a través de un timbre.

## 5. Modelo de interacción y estados sugeridos (a definir)

La llamada necesita identidad y trazabilidad independientes de la animación de puerta. Campos conceptuales:

- `intercom_session_id`, `door_id`, `quarters_location_id`, `ship_id`.
- `caller_character_id`, `occupant_character_id` / `authorizing_resident_id` según quién conteste.
- `caller_location`, `occupant_location`, `speaker`, `recipient`, `started_at`, `last_activity_at`.
- `door_state`, `lock/access_state`, `privacy_mode`, `ship_alert_state`.
- `call_state`, `pending_intent`, `authorization_outcome`, `wait_deadline`, `last_authoritative_result`.

**Estados candidatos, no definidos todavía como contrato canónico:**

`idle` → `ringing` → `connected` → `awaiting_identity` / `awaiting_reason` / `waiting` / `entry_granted` / `entry_denied` → `completed` / `cancelled` / `timed_out` / `interrupted`.

Evitar sesiones duplicadas, dobles aperturas por reintentos de API, respuestas tardías después de la salida del visitante y desincronizaciones entre el sonido de la llamada y el estado persistente.

**Persistencia:** si se interrumpe, guardar al menos los eventos y resultados sociales relevantes; definir si la sesión efímera se cierra con seguridad al guardar/cargar o se restaura. La puerta real y la posición de los personajes **no pueden quedar en un estado incompatible**.

## 6. Privacidad, permisos y emergencias

- Cada camarote tiene **residente(s) y política de acceso**, determinados por la asignación/ocupación reales, no por una suposición de la IA.
- Visitar a un NPC **no concede acceso automático** por amistad, rango, romance o simple presencia del jugador frente a la puerta.
- La respuesta «Adelante» debe venir de un personaje **legitimado para autorizar esa entrada**, o de una excepción de acceso explícita y validada.
- El visitante debe seguir **en la puerta** cuando se autoriza; no abrir una puerta vacía por una respuesta de IA retrasada.
- Si el NPC está de guardia, ausente, dormido, en atención médica o incomunicado, las consecuencias se basan en su **estado real**, no en un texto inventado.
- **Seguridad, emergencias médicas y órdenes operativas** pueden tener procedimientos específicos para apertura de emergencia y acceso autorizado: deben estar registrados y sujetos a reglas de necesidad, seguridad y trazabilidad; no usar la conversación como llave maestra.
- El intercomunicador nunca debe servir para acceder automáticamente a habitaciones privadas o información personal no disponible.
- En condiciones de avería, fallo de energía, incendio, despresurización o aislamiento, actuar conforme al estado técnico real del barco; una animación o frase no debe ignorar una puerta físicamente bloqueada.
- «Espere» es una petición al visitante, **no una orden que le confiere inmovilidad infinita**. El visitante puede retirarse, avisar o tener una obligación más urgente.
- Varias personas en un camarote o en la puerta necesitan resolución clara de **quién contesta y quién tiene permiso**, sin duplicar voces.

## 7. Vida a bordo, relaciones, horarios y presencia física

Integración directa con los contratos documentados en este repositorio:

- [Vida a bordo](../../sistemas/gameplay/ship_operations/shipboard_life_state_contract.json): camarotes reales, privacidad, ocupantes, descanso, ocio y alertas.
- [Horarios](../../sistemas/gameplay/characters/activity_schedule_model.json): ningún NPC puede estar a la vez en el puente y ante una puerta; desplazamiento y espera consumen tiempo.
- [Ubicaciones interiores](../../sistemas/gameplay/ship_operations/interior_location_model.json): `crew_quarters`, `connections`, `access_level`, `access_state`, `occupants`, alertas y ocupación.
- [Eventos sociales](../../sistemas/gameplay/social/social_event_rules.json): conversación, visita, invitación, desacuerdos y efectos relacionales derivados de hechos reales, sin puntos de amistad obligatorios.
- [Interpretación de IA](../../sistemas/ai/command_interpretation/starship_command_contract.md): misma separación entre comprensión, plan, validación y ejecución.
- [F12 — Vida a bordo, NPC y relaciones](../docs/roadmap/master/fases/F12/README.md): fase candidata de integración social y persistencia, todavía sujeto a sus condiciones de cierre.
- [IDEA-0012 — Ajedrez con NPC](IDEA-0012_ajedrez_clasico_3d_con_npc.md): una invitación a jugar podría comenzar llamando al camarote, siempre conforme a horarios/consentimiento.

**No se crea un NPC ficticio para atender una llamada** ni se marca un vínculo afectivo solo por permitir una visita.

## 8. Diseño gráfico y sonoro

**Aspecto deseado:** panel pequeño de intercomunicador integrado junto al marco exterior de las puertas de camarotes, inspirado en interfaces Star Trek (LCARS u otra estética apropiada de la época y clase), sin ocupar exageradamente la pared.

**Audio:** un aviso de puerta/intercomunicador con timbre característico y sensación Star Trek, idealmente con reproducción espacial dentro del camarote y confirmación breve donde esté el visitante; seleccionar y verificar los recursos de sonido reales al implementarlo. No declarar que ya existe un clip importado.

**UE5:** interacción por proximidad y botón, activación de indicador luminoso, cámara y subtítulos opcionales, sonido localizado, reproducción de voz si procede, animaciones del panel y de la puerta **como resultado del estado validado**.

**Escenarios modulares:** el exterior del camarote y su interior pueden estar en mapas/escenas separados si así se construye la Valhalla. **La autorización y la sesión pertenecen al mundo persistente**; el paso de umbral puede usar una transición disimulada sin exigir continuidad geométrica real.

**Accesibilidad:** permitir escribir la respuesta además de hablar, mostrar nombre de interlocutor solo si realmente es conocido/confirmado, subtítulos y volumen de intercomunicación configurable; el jugador no debe quedar bloqueado por no usar micrófono.

## 9. Hoja de ruta propuesta (NO iniciada)

1. **ICOM-01 — Inventario y contratos:** auditar modelos de puertas/camarotes, controles de acceso, datos de residentes, ubicación, señales y flujo de interpretación IA. Definir alcance mínimo.
2. **ICOM-02 — Prototipo visual:** botón junto a puerta, sonido localizado dentro/fuera, indicadores de llamada; UX accesible sin conexión remota.
3. **ICOM-03 — Máquina de estados y permisos:** sesión, ocupación, timbre, identidad, autorización, tiempos de espera y cierre; validación determinista y protección contra reintentos.
4. **ICOM-04 — Llamada jugador→NPC:** comprobar NPC realmente presente, horario, decisión social, respuesta/rechazo, apertura válida y transición de interior.
5. **ICOM-05 — Llamada NPC→jugador:** frase natural libre por texto y eventual voz, IA → intención estructurada candidata → validador → juego; cubrir «quién es», «adelante», «espere», «no», «qué desea» y condiciones compuestas.
6. **ICOM-06 — Diálogo y continuidad:** diálogo contextual, relaciones, horarios, privacidad, visitantes múltiples, esperas e interrupciones por alertas.
7. **ICOM-07 — Rendimiento y persistencia:** no usar IA innecesariamente; pruebas de latencia, fallos de API, save/load, repetición de mensajes, escenas modulares y NPC fuera de cámara.
8. **ICOM-08 — QA en MSI:** demostrar intercomunicador desde ambos lados con al menos un NPC real, puerta que abre/cierra correctamente, respuesta libre, rechazo de intentos de abrir sin permiso y presencia/tránsito persistentes.

**Fases futuras candidatas:** F03/F04/F05 (estado/autorización/órdenes si existen contratos suficientes), F07/F09 (puertas y UE5/interacción), F10 (IA), F12 (vida a bordo y NPC), F14 (audio) y F15 (QA). La asignación exacta se decidirá sin alterar cierres de otras fases.

## 10. Pruebas y criterios de aceptación futura

1. Cada camarote disponible en el alcance definido tiene un botón exterior funcional y aviso sonoro apropiado.
2. El jugador puede llamar a un NPC y recibir una reacción consistente con presencia, agenda, privacidad y relación.
3. Un NPC puede llamar a la puerta del jugador y **espera la respuesta libre** en texto/voz.
4. «¿Quién es?» devuelve solicitud de identidad **sin abrir la puerta**; «Adelante» abre solo tras validación; «Espere» conserva puerta cerrada con espera de duración razonable; «Ahora no» deniega.
5. Una frase compuesta o coloquial se descompone sin elevar permisos; una frase ambigua requiere aclaración y no abre silenciosamente.
6. La IA puede interpretar o proponer; **solo el motor autoritativo concede acceso y actualiza estados**.
7. No hay teleportación de NPC, apertura duplicada, respuestas aplicadas a una llamada caducada, ni desincronización por reintentos.
8. Los NPC ausentes o dormidos pueden no contestar; las emergencias y averías tienen prioridad legítima.
9. Al pasar entre camarote/corredor o tras guardar/cargar se mantiene identidad, posición y puerta coherentes.
10. El sistema funciona sin micrófono mediante entrada de texto; se incluyen subtítulos/indicadores legibles.
11. Se respetan los permisos de privacidad y no se inventa amistad, consentimiento, autoridad ni conocimiento de identidad.
12. Al menos un caso de jugador→NPC y otro NPC→jugador se demuestra **realmente en el MSI con UE5** antes de afirmar que la idea está implementada.

## 11. Decisiones cerradas y pendientes

### APROBADAS
- Intercomunicador con botón físico/visual en la entrada de **cada camarote**.
- Aviso sonoro de carácter Star Trek que se escucha **dentro** al llamar desde fuera.
- Respuesta **libre y natural** del jugador, interpretada por IA en formato estructurado que comprende el motor.
- Intenciones de abrir, identificar, esperar, rechazar o preguntar motivo, entre otras compatibles con reglas reales.
- Funcionamiento **bidireccional**: visitante jugador o NPC; ocupante jugador o NPC.
- IA responsable de comprender/narrar y **juego responsable de ejecutar**.
- Respeto a presencia real, horarios, relaciones, privacidad, permisos y emergencias.
- Diseño común reutilizable para otras dependencias con puerta y llamada en fases futuras.

### POR DEFINIR AL IMPLEMENTAR
- Forma final del panel y muestra concreta del efecto sonoro; importación de assets.
- Si la entrada de voz ya disponible en el juego cubre este caso o requiere integración adicional.
- Esquema definitivo de acciones/intercomunicaciones y ubicación del ejecutor real sin duplicar contratos de órdenes.
- Política de identificación segura del visitante, varios ocupantes y visitantes, interrupción, caducidad y persistencia.
- Modalidad gráfica de cámaras, subtítulos y presentación en camarotes/escenas modulares.
- Modo de registro social y consecuencias discretas de visitas, sin puntos arbitrarios.
- Optimización de uso de API y comportamiento fiable ante fallos de transcripción/IA.

**Resultado administrativo:** IDEA-0014 **APROBADA Y REGISTRADA COMO DISEÑO**. No se han creado por esta ficha intercomunicadores UE5, sonidos instalados, permisos nuevos en CoreRPG, ni una interpretación IA real en ejecución.
