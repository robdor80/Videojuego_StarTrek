# F05-P03 — Iniciativa de capitán NPC, oficiales y coordinación fuera de escena
Fecha: 2026-10-11 · **Diseño de referencia; no motor ejecutado**.

## Principio central
La tripulación **vive y decide sin esperar al jugador**, pero solo a partir del estado y el conocimiento propio. El capitán NPC conserva iniciativa y autoridad legal incluso cuando el jugador es un alférez de guardia en Sensores. Si el jugador es capitán, conserva la última palabra dentro de sus atribuciones reales; su XO puede preparar soluciones, no imponerlas cuando el control es manual o requiere aprobación.

## Ciclo de deliberación no omnisciente
1. Un tick/evento de mundo autoritativo genera necesidad (contacto observado, relevo pendiente, anomalía, reparación, reporte o misión).
2. El servicio planificador selecciona actor disponible usando **agenda, localización, aptitud, puesto, cualificación, órdenes y cargas** reales; no materializa un Actor 3D innecesario.
3. Se compone solo el conocimiento de **ese personaje**: sensores publicados, órdenes recibidas, registros que puede consultar, memoria, objetivos y prioridades; la verdad secreta no se transmite.
4. Política determinista Star Trek elige entre **no actuar, solicitar información, informar, proponer, emitir orden dentro de mandato, ejecutar tarea o escalar**; la IA remota puede ayudar a redactar/proponer, nunca autorizar.
5. Antes de cada ejecución se reevalúan mando, delegaciones, prioridades, recursos, revisión y capacidad. Se procesa con IDs estables e idempotencia.
6. Se registran intención, orden/tarea, resultado, comunicaciones, respuesta del destinatario y evento causal. Solo se muestra la proyección visible al observador.
7. Las agendas reciben el consumo de trabajo **cuando Core lo implemente**. En ausencia de actor 3D la lógica no se suspende; reducir detalle no elimina decisiones ya resueltas.

## Responsabilidades y prioridades
| Personaje | Iniciativa normal | Límite |
| --- | --- | --- |
| Capitán NPC titular | Ordenar barrido, alertas válidas, respuesta a misión/aviso, delegación | No inventa contactos ni ignora aptitud/superiores/interlocks |
| Primer oficial | Coordinar dotación, tareas interdepartamentales, preparar decisiones | No reemplaza la autoridad reservada al capitán cuando está presente y habilitado |
| Jefe de departamento | Distribuir personal del área, priorizar trabajos permitidos y elevar obstáculos | No emite política de toda la nave sin nombramiento |
| Oficial de guardia | Gestionar alertas rutinarias y tareas acotadas por guardia/órdenes permanentes | Fin de guardia o revocación termina autoridad temporal |
| Alférez de Sensores (jugador o NPC) | Operar consola cualificada, registrar contacto, informar y pedir precisión | Ni capitanía automática ni acceso a verdad total |
| Capitán jugador | Elegir, aceptar, corregir, sustituir o delegar decisiones autorizadas | Las propuestas automáticas no son órdenes; límites médicos, físicos y normativos prevalecen |

## Prioridad de trabajo y conflictos
Seguridad vital vigente → orden superior válida y obligatoria → misión/guardia autorizada → órdenes permanentes aplicables → iniciativa local rutinaria → ocio/otros. No es un sistema de puntuación moral ni una excusa para incumplir derechos; los conflictos de órdenes requieren evaluación contextual. Una emergencia no habilita mágicamente a personal incapacitado, ni permite doble ocupación imposible. Orden de rango superior no equivale a autorización fuera del dominio. Controversias, insubordinación, errores humanos y resultados parciales se modelarán como decisiones/eventos, no como bugs que se corrigen silenciosamente.

## NPC↔NPC aun fuera de escena
- **Sensor NPC → capitán NPC:** contacto detectado en su proyección → informe con `knowledge_ref` → capitán solicita barrido autorizado → operador/tarea → resultado → informe y evento.
- **Capitán NPC → jefe Ingeniería NPC:** avería registrada → prioridad y delegación → jefe organiza personal y turnos disponibles → resuelve o informa imposibilidad.
- **Capitán jugador → XO NPC:** propuesta de cuadrante en modo `proposal_requires_approval` → solo aprobación positiva genera orden; una recomendación no la suplanta.
- **NPC → jugador de Sensores:** si jugador no responde, conservar pendiente/caducidad/traspaso explícito; nunca simular en secreto que el jugador aceptó o ejecutó.

## Antiesperas y límites
La simulación no depende de que esté abierta la escena del puente, de animaciones, del UI ni de la API de IA. Un NPC descargado lógicamente tiene misma identidad y hechos; la acción no se ejecuta dos veces al reaparecer. Determinismo se verifica con semilla/revisión/timestamp estables. LOD latente nunca revela retroactivamente secretos al jugador. Propuestas de IA no se tratan como descubrimientos autoritativos.

**Integraciones pendientes:** scheduler Core, ocupación, conocimiento de 4.9, acciones 4.10, historial 4.7, UE5. Fuentes: `ai/npc_behavior/character_decision_guardrails.md`, `ai/director/operational_need_guardrails.md`, `gameplay/chain_of_command/command_decision_delegation_state_v0.1.json`, F03 y F04 en PR #4/#5. No se decide nueva doctrina de Starfleet.
