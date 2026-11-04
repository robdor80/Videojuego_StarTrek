# IDEA-0016 — Insignias Starfleet y sistema universal de comunicaciones inteligentes

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación conceptual:** 4 de noviembre de 2026  
**Estado:** **APROBADA CONCEPTUALMENTE; propuesta registrada en el buzón. Sin implementación ni pruebas jugables.**  
**Origen:** el autor propone una insignia personal en el pecho para jugador y NPC, con indicador de rama al estilo visual de *Star Trek: Strange New Worlds* (era del capitán Pike), que se activa con tecla o mando para hablar con computadora, nave, un NPC o cualquier destinatario accesible. En el debate posterior propone **enmascarar la latencia mediante respuestas orales progresivas**, y aprueba expresamente esa mejora («Aprobado»).  
**Prioridad editorial:** preservar ambas decisiones como una sola idea y tratar el procesamiento progresivo como requisito de experiencia, no como promesa de latencia medida.  
**Áreas:** personajes y uniformes 3D, comunicaciones, interacción por voz/texto, IA natural, director de intenciones, computadora de nave, roles/autorizaciones, NPC persistentes, CoreRPG y UE5.

## 1. Visión de la idea

Cada **miembro de la Flota Estelar** del elenco jugable —jugador y NPC— llevará una **insignia personal en el pecho**, que indique su **rama/especialidad** mediante el aspecto del emblema y actúe además como **comunicador funcional**. Los NPC no pertenecientes a la Flota deberán conservar su afiliación real, con un dispositivo o vestuario alternativo cuando corresponda: no convertir a civiles, invitados u oficiales extranjeros en miembros de Starfleet por portar una malla decorativa.

**Inspiración artística expresa:** insignias metálicas de `Star Trek: Strange New Worlds` (estética época Pike), adaptadas de forma deliberada al periodo TNG/DS9/Voyager del juego como elemento de arte propio; **funcionalidad equivalente a los comunicadores personales de la época de Picard**. La rama se determina desde la asignación/identidad institucional válida y no únicamente por una textura; un cambio profesional debe reflejarse en el uniforme apropiado.

**Comportamiento principal:** pulsar una tecla configurable del teclado o un botón del mando **simula tocar la insignia**. Se oye el aviso característico, se abre el canal de voz/texto y el jugador puede **preguntar o pedir cualquier cosa con lenguaje natural**, sin tener que memorizar órdenes fijas. El sistema interpreta una intención o una conversación y la enruta al servicio adecuado.

Las insignias deben ser **objetos reales 3D** en el pecho de los personajes, visualmente legibles, no iconos puramente HUD. La animación de mano tocando la insignia es **deseable pero no obligatoria** para una primera versión: puede emplearse gesto corto, sonido y reacción visual sin crear bloqueo de jugabilidad por falta de animación corporal.

## 2. Experiencia del jugador

1. El jugador está caminando, descansando, trabajando en el puente, en un camarote o en otro espacio con comunicaciones operativas.
2. Pulsa la tecla/botón de comunicación: simulación de toque en insignia, tono y pequeño indicador del canal.
3. Habla o escribe una frase libre. Ejemplos:
   - «Computadora, ¿dónde está Geordi La Forge?»
   - «Puente, aquí el capitán. Informe de situación».
   - «Comunícame con la doctora».
   - «Computadora, baja la iluminación de mi camarote».
   - «Avise al teniente que venga cuando termine de trabajar».
   - «¿Qué sabemos de esta especie?»
   - «Alerta roja».
   - «¿Quién estuvo reparando ayer los motores auxiliares? Comunícame con él».
4. El sistema resuelve **destinatario, tipo de solicitud, contexto, autorizaciones e información disponible**. Puede contestar, pedir aclaración, iniciar una comunicación, enviar una solicitud, preparar una orden o denegar una petición imposible.
5. Solo el motor autoritativo efectúa actos que alteren la partida; la IA no inventa respuestas de sistemas, disponibilidad de NPC ni resultados.
6. La conversación puede continuar durante varios turnos y cerrarse explícitamente al volver a tocar la insignia, mediante botón de cancelación o al concluir la llamada.

**Controles propuestos:** pulsación para abrir/cerrar, opción *pulsar y mantener* como push-to-talk, remapeo de teclas/mando, texto como alternativa siempre disponible, subtítulos y volumen configurable. Priorizar que el jugador distinga visual/acústicamente canal abierto, procesamiento, interlocutor conectado, espera y canal cerrado.

La activación voluntaria evita que la computadora trate una charla normal entre personajes como una orden de voz. A futuro, llamadas entrantes pueden activarse con tono y respuesta del jugador, sin escucha de micrófono permanente por defecto.

## 3. Arquitectura: un único enrutador universal, no una IA por dispositivo

**Principio confirmado en el repositorio: «AI interprets. Core executes.»** Compartir el patrón existente de `sistemas/ai/command_interpretation/starship_computer_system.md`.

```text
INSIGNIA (jugador o NPC)
   ↓
CAPTURA DE VOZ / TEXTO + IDENTIDAD DEL EMISOR + CONTEXTO
   ↓
TRANSCRIPCIÓN PROGRESIVA, SI ES VOZ
   ↓
RUTEO LOCAL DE INTENCIONES CONOCIDAS / IA SI HACE FALTA
   ↓
CANDIDATO ESTRUCTURADO DE INTENCIÓN + DESTINATARIO(S)
   ↓
VALIDACIÓN DE ESQUEMA, ACCESO, IDENTIDAD, CONTEXTO Y DISPONIBILIDAD
   ↓
SERVICIO CORRESPONDIENTE / EJECUTOR AUTORITATIVO
   ↓
RESULTADO REAL + RESPUESTA PROGRESIVA SEGURA
   ↓
AUDIO, TEXTO, HUD, REACCIÓN Y EVENTO PERSISTENTE
```

**Familias de intención candidatas:**
- `COMPUTER_QUERY`: preguntas sobre estado, información validada o conocimientos disponibles.
- `OPEN_COMMUNICATION`: llamada a persona, departamento, puesto, otra nave o instalación.
- `SOCIAL_MESSAGE`: dejar aviso, solicitar reunión, enviar mensaje u ofrecer encuentro; el destinatario puede aceptar/rechazar.
- `SHIP_SYSTEM_REQUEST`: luces, sistema ambiental, consulta de sistemas, servicios autorizados.
- `OPERATIONAL_ORDER`: orden legítima según rango, puesto, mando efectivo, doctrina y condiciones técnicas.
- `LOCATION_LOOKUP`: averiguar dónde está un personaje o lugar, según información accesible.
- `COMMUNICATION_CONTROL`: cortar, redirigir, retener, responder a una llamada entrante.
- `CLARIFICATION`: preguntar al jugador por destinatario/objeto/acción ambiguos.
- `GENERAL_DIALOGUE`: conversación natural que no corresponde a una orden concreta.

**Estos nombres son de propuesta, no enums implementados.** La implementación debe auditar los contratos efectivos y crear extensiones versionadas sin introducir un esquema paralelo incompatible ni reutilizar indebidamente un contrato específico de sensores para todas las comunicaciones.

El intérprete puede devolver **múltiples acciones candidatas** cuando el usuario mezcla conversación y órdenes («Puente, mantengan el rumbo y avísenme de cualquier cambio»), pero cada acción se valida por separado. No se ejecutará una instrucción sensible solo porque aparezca mencionada dentro de una pregunta.

**Ejemplo conceptual de intención (NO contrato final):**

```json
{
  "intent": "OPEN_COMMUNICATION",
  "target_type": "CHARACTER",
  "target_ref": "geordi_laforge",
  "needs_clarification": false
}
```

El juego debe comprobar si el personaje existe en la campaña, si el emisor dispone de información suficiente para resolverlo, qué dispositivo/canal usa, si se puede localizar y si el receptor desea o puede contestar. Nunca completar entidades desconocidas por suposición.

## 4. Comunicación efectiva y límites del universo

La insignia **no es un teléfono omnipotente**:
- Las comunicaciones dentro de una nave funcional pueden ser rápidas; entre naves/planetas/sectores dependen de disponibilidad real de canal, distancia, relés, subespacio, interferencia, cifrado y daños.
- Que una llamada se curse no significa que alguien conteste: un NPC puede estar dormido, ocupado, de servicio, herido, de misión, fuera de cobertura o no querer responder.
- Las respuestas de NPC respetan identidad, personalidad, recuerdos, relaciones, permisos, horarios y conocimientos realmente disponibles.
- El jugador puede hablar con «el puente», «ingeniería», «enfermería», un personaje concreto o la computadora, con enrutamiento al destinatario/contexto apropiado. Si hay dos doctores o varios tenientes candidatos, preguntar.
- El rango del jugador no garantiza poder ejecutar todas las órdenes ni permite irrumpir en una conversación privada; la autoridad se valida por rol/cadena de mando real.
- En alerta roja o crisis se pueden priorizar comunicaciones y permitir interrupciones legítimas, pero no crear teletransporte ni capacidad de red que no exista.
- Los NPC también **pueden originar llamadas mediante sus insignias**; se resolverán con el mismo modelo de enlace y disponibilidad, optimizando simulaciones fuera de cámara.

Relacionar con `sistemas/gameplay/communications/README.md`, cuyo bucle ya contempla destinatarios, calidad de enlace, retrasos, respuesta/no respuesta, traducción y registro.

## 5. Respuestas progresivas y enmascaramiento de latencia — APROBADO EXPRESAMENTE

**Mejora aprobada por el autor:** una respuesta puede **comenzar mientras se resuelve la información que falta**, para que la espera técnica se convierta en diálogo natural de la computadora. Ejemplo de intención: no contestar únicamente «Está en cubierta H», sino comenzar por una presentación confirmada del destinatario, **mientras se consulta su posición**.

### Ejemplo aprobado

**Jugador:** «Computadora, ¿dónde se encuentra Geordi La Forge?»

Si la identidad, rango, departamento y cargo se han validado antes, y la posición está aún pendiente:

1. Inicio de voz permitido: «El comandante Geordi La Forge, jefe de Ingeniería de la Enterprise…».
2. Durante esa voz se consulta una **ubicación autoritativa** vigente.
3. Tras obtener y validar el resultado, continuar: «…se encuentra ahora mismo en la cubierta H, en Ingeniería principal», **solo si esa ubicación, cubierta y condición están realmente confirmadas en la nave de la partida**.

La frase debe **adaptarse a las circunstancias reales**: en nuestro juego no hay obligación de que Geordi esté en la Enterprise, tenga ese rango/cargo o se halle en cubierta H. Los datos del ejemplo son ilustrativos.

### Regla de oro: introducciones basadas únicamente en hechos conocidos

**Jamás afirmar datos aún no comprobados.** El sistema debe:
- Preparar unidades de habla/prefijos **solo con datos ya verificados** y conocimiento autorizado.
- Paralelizar la reproducción de audio y una consulta en curso, sin esperar al resultado para preparar cada fonema si la arquitectura de síntesis/streaming lo permite.
- Construir el segmento final **después de la validación**; no generar/emitir la ubicación probable como si fuera segura.
- Si la consulta es lenta, continuar con un mensaje honesto: «Estoy comprobando su última ubicación registrada» o «Un momento, consultando los registros disponibles».
- Si falla o no hay autorización, **decir que no se ha podido determinar**; no completar la frase con información inventada.
- Evitar el relleno artificial y las introducciones largas para preguntas rápidas; preferir respuestas breves cuando el resultado ya está.
- No usar enmascaramiento para **simular la ejecución exitosa** de una orden que todavía está pendiente. Voz preliminar de una orden sensible: «Recibida la petición»; nunca «Escudos levantados» antes del resultado.
- Si el usuario interrumpe o cancela, detener voz y operaciones cancelables; evitar respuestas tardías de solicitudes antiguas.
- Respetar nombres y grados reales de cada campaña; no usar fórmulas erróneas para alargar el diálogo.

### Rendimiento propuesto, no medido

**Objetivos de experiencia a validar en MSI:**
- Petición reconocible localmente: inicio de respuesta perceptible objetivo **inferior a 1 segundo**, cuando la entrada ya está disponible y el sistema esté listo.
- Interpretación con modelo externo: **respuesta perceptible progresiva** de ser posible antes del resultado, y resultado completo habitualmente en torno a **2–3 segundos**, sujeto a proveedor/red/transcripción.
- Consultas complejas: intentar que la espera normal no supere **unos 5 segundos**, y utilizar mensajes de estado honestos si la información tarda más; sin garantía rígida.
- Un ejemplo hipotético: si la consulta tarda 2,5 segundos y pronunciar un inicio **válido** ocupa 1,8 segundos durante la consulta, la espera muda antes del segmento final puede reducirse aproximadamente a 0,7 segundos. **Es una ilustración matemática, no una medición ni una promesa.**
- Registrar por separado `end_of_utterance → first_audio`, `end_of_utterance → first_action`, `end_of_utterance → verified_result`, `end_of_utterance → final_audio`, tasa de errores de transcripción, coste/calls por interacción.

**Limitación importante:** si para conocer la identidad hay que esperar precisamente a la misma llamada de IA que tarda, no puede darse una introducción que la presuponga. La respuesta progresiva se activa **solo cuando los hechos iniciales están confirmados localmente o por una consulta previa**. El sistema de voz por fragmentos (TTS) puede añadir latencia real y debe probarse.

Esta técnica beneficia también a consulta de tripulantes, información de sensores, comunicaciones, órdenes y diálogo NPC, **sin convertir todas las respuestas en discursos largos**.

## 6. Interpretación local primero y consumo responsable de API

- Crear índice local de nombres, alias, rangos, departamentos, órdenes directas y consultas simples. Una petición reconocida y validable no necesita LLM.
- Utilizar IA narrativa/interpretativa para **frases libres complejas**, referencias indirectas, acciones compuestas y conversaciones naturales.
- Pasar solo el **contexto mínimo y permitido**: identidad del emisor, destinatarios/candidatos relevantes, permisos, extractos read-only de World State y contexto de la comunicación actual.
- No enviar todo el universo, toda la base de NPC ni todos los datos confidenciales de la nave en cada toque.
- No invocar el modelo solo para producir un «Recibido» o reformular una respuesta determinista rutinaria; usar un compositor local.
- Diferenciar transcripción de voz, interpretación y síntesis de voz: se pueden sustituir por componentes específicos sin cambiar la capa autoritativa.
- Ante red/API caída, mantener comandos locales compatibles y responder de manera legible a lo que no pueda interpretarse.
- Evitar invocar automáticamente modelos de mayor coste por resultados mal tipados, peticiones ambiguas o falta de permisos: primero aclarar o validar según reglas.
- Registrar diagnósticos reproducibles sin guardar de forma indiscriminada audio personal ni información privada de NPC.

## 7. Representación de insignias y especialidades

**Referente visual:** estilo delta metálico y variantes de rama inspiradas en `Star Trek: Strange New Worlds`, con símbolos diferenciales, apariencia robusta y materiales PBR.

**Requisitos de diseño:**
- Identidad del portador y rama obtenidas de `character_id`, `current_department_ref`, `current_assignment_ref` y/o manifest/servicio autorizado, según los contratos realmente existentes.
- Cambios de destino/rama reflejados en el objeto del uniforme cuando proceda, sin reconstruir la identidad personal.
- Permitir ramas de mando, operaciones/ingeniería, ciencias y medicina conforme al modelo definitivo de divisiones, sin forzar que todos los personajes compartan la misma estética o símbolos de siglo XXIII.
- Insignia adherida a uniforme/pecho 3D con materiales, orientación y distancia adecuados para animación/cámara.
- Mismo mecanismo de activación lógica para jugador y NPC, pero representación animada según proximidad/LOD; fuera de cámara no es necesario renderizar gestos.
- **Seguridad:** un uniforme o insignia visible no constituye por sí solo autenticación; la identidad/afiliación/autorización proceden del World State.
- Civil/especie no miembro de Starfleet: no etiquetar falsamente como oficial de Flota; decidir dispositivo alternativo, o ausencia de insignia de Starfleet según canon de nave.

## 8. Integración con ideas anteriores y contratos existentes

- [IDEA-0014 — Intercomunicadores de camarotes](IDEA-0014_intercomunicadores_inteligentes_camarotes.md): comparte interpretación de intención, diálogo, enrutamiento, identidades, autorizaciones y privacidad; no igualar pulsar timbre físico a usar insignia personal.
- [IDEA-0015 — Turboascensores inteligentes](IDEA-0015_turboascensores_inteligentes_lenguaje_natural.md): comparte parser/entorno de lenguaje libre y catálogos de alias; la cabina cambia la **ubicación** mediante ruta validada, mientras la insignia tramita peticiones/comunicaciones **sin mover automáticamente** al emisor.
- [Starship Computer System](../../sistemas/ai/command_interpretation/starship_computer_system.md): ya define voz/texto, plan de órdenes, compositor local, contexto filtrado y validador. Esta idea añade **entrada por insignia** y **distribución universal** a dominios, sin sustituirla.
- [Contrato de interpretación IA](../../sistemas/ai/command_interpretation/starship_command_contract.md): el patrón `AI interprets. Core executes.` se conserva para todas las acciones.
- [Sistema de comunicaciones](../../sistemas/gameplay/communications/README.md): destinatario, enlace, subespacio, interferencia, recepción, respuesta y registro; extender mediante contratos verificados cuando se implemente, no duplicar.
- [Estado de personajes](../../sistemas/gameplay/characters/character_runtime_model.json): identidad persistente, asignación/ramas, localización, relaciones y conocimiento.
- [Vida a bordo](../../sistemas/gameplay/ship_operations/shipboard_life_state_contract.json): cambios de horarios/ubicación, descanso, alerta y condiciones materiales.
- [Buzón de ideas](BUZON.md): aprobación conceptual de IDEA-0016, pendiente del plan de construcción.

**No confundir el archivo `starship_computer_command_plan.schema.json` existente con un contrato ya general para todas las acciones sociales;** habrá que comprobar su alcance (p. ej., comandos de sensores) y diseñar un envoltorio o familia de intenciones versionada cuando la integración real lo requiera.

## 9. Etapas propuestas — BADGE-01 a BADGE-09 (NO iniciadas)

1. **BADGE-01 — Auditoría e identidad:** revisar uniformes, asignación de ramas, NPC/estado, instancias de insignia y controles disponibles, sin asumir assets 3D descargados.
2. **BADGE-02 — Prototipo visual:** delta por rama, attach al pecho, gesto mínimo de toque, sonido y señales UI, pruebas de escala y LOD.
3. **BADGE-03 — Activación multimodal:** teclado/mando remapeables, canal abierto/cerrado, push-to-talk opcional, texto, subtítulos y modo sin micrófono.
4. **BADGE-04 — Intérprete/enrutador universal:** captura, transcripción, lookup local, IA contextual, estructura validable y distribución por dominio.
5. **BADGE-05 — Computadora y consultas:** preguntas de mundo, tripulación, lugares y sistemas basadas en conocimiento real, resultado/compositor local.
6. **BADGE-06 — Comunicaciones NPC/puestos:** llamadas salientes y entrantes, disponibilidad, señales, reintentos, privacidad y continuidad social.
7. **BADGE-07 — Órdenes autorizadas:** solicitudes de sistemas, órdenes de nave, autoridad/rango, acciones compuestas y trazabilidad sin elevar permisos.
8. **BADGE-08 — Respuestas progresivas:** voz en fragmentos sobre hechos ya confirmados, consultas en paralelo, TTS, fallos/timeout, mediciones de latencia y uso API.
9. **BADGE-09 — QA integrado MSI:** pruebas UE5 de insignia real, mando/teclado, castellano libre, NPC, órdenes, fallos de conexión, interferencias, NPC ausente, eventos de emergencia, save/load y latencia.

**Fases candidatas futuras:** F03–F05 (autoridad y acciones), F07 (interacción), F10 (IA), F12 (NPC y vida a bordo), F14 (audio/UI) y F15 (QA). No cerrar ninguna fase por registrar esta idea.

## 10. Criterios de aceptación futura

1. Jugador y miembros NPC de Starfleet llevan insignia 3D adecuada a rama/identidad, fijada al uniforme; no etiquetar indebidamente a civiles.
2. Tecla configurable o mando abre/cierra intercomunicador; se puede hablar/escribir y usarlo sin micrófono.
3. El sistema identifica solicitudes libres a computadora, departamentos, NPC, servicios de nave y órdenes operativas.
4. Personajes ambiguos, destino desconocido o permisos ausentes producen aclaración/rechazo, no inventan resultados.
5. El intérprete no muta directamente el World State ni abre canales inexistentes.
6. Comunicaciones entrantes y salientes respetan presencia, señal, autonomía del receptor, tiempos y privacidad.
7. Peticiones sensibles exigen autoridad, estado válido y condiciones de la nave.
8. Las respuestas progresivas empiezan **antes de finalizar el procesamiento cuando sea seguro y útil**, usando **exclusivamente hechos verificados**, sin anunciar un resultado pendiente.
9. Las preguntas simples reciben respuestas breves, no prefacios de relleno; si hay error/timeout se informa con honestidad.
10. Se registran y comparan tiempos reales de **primer audio**, **primer acto**, **resultado verificado** y **audio final**, además de costes API.
11. La reutilización con IDEA-0014 e IDEA-0015 evita duplicaciones y mantiene la separación de roles entre dispositivos.
12. Una demostración jugable y pruebas verificables en MSI/UE5 son necesarias para declarar implementación, no bastando documentos ni prototipos visuales.

## 11. Decisiones aprobadas y asuntos abiertos

### Aprobadas en la conversación de ideación
- **Insignias personales Starfleet** en pecho del jugador/NPC con rama diferenciada, **estética de Strange New Worlds**.
- **Pulsación de teclado o mando** para simular el toque y abrir comunicación universal.
- Poder **preguntar libremente** a computadora/nave/NPC, contactar a departamentos y dar instrucciones según capacidades del juego.
- Uso compartido de una capa de IA/interpretación, enrutada a sistemas validados, como solución propuesta.
- **Mejora aprobada expresamente: respuestas progresivas con enmascaramiento de latencia**, aprovechando la voz inicial de datos conocidos mientras se consulta lo que falta.
- No falsear hechos, estados ni éxito de órdenes para ganar tiempo.

### Pendientes de diseño técnico y selección de assets
- Diseño artístico exacto de cada emblema/ramas y el detalle de si se reproducen variantes históricas o se personalizan.
- Modelos 3D reales, PBR y gesto de toque (opcional al inicio).
- Asignación concreta de teclas y mandos, opciones de micrófono, TTS y subtítulos.
- Esquema común versionado de intents/multiacción, protocolo de llamadas y autentificación.
- Estándares de enrutamiento/contexto, elección del modelo para cada tipo de solicitud y política final de costes.
- Estrategia precisa de fragmentación TTS sin introducir pausas artificiales ni condiciones de carrera.
- Métricas de latencia y presupuesto objetivo definitivos tras medir en MSI.

**Resultado administrativo:** IDEA-0016 **APROBADA CONCEPTUALMENTE Y DOCUMENTADA**. No se afirma que existan todavía insignias jugables, canal de voz UE5, NPC que respondan mediante emblema, enrutador universal ni respuestas progresivas implementadas.
