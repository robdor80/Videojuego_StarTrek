# Decisión aprobada: ascensos y nombramientos diegéticos — F11-P05

**Aprobación del autor:** 11-11-2026.  
**Estado creativo:** APROBADO, **pendiente de implementación**.  
**Tarea de seguimiento:** [GitHub #104](https://github.com/robdor80/Videojuego_StarTrek/issues/104).  
**Subfase principal de ejecución jugable:** **F11-P05-D**.  
**Preparación técnica requerida:** F11-P05-A02-01, P05-B y P05-C.  
**Responsable de seguimiento y coordinación:** ChatGPT, como asistente de planificación del proyecto. **La implementación efectiva requiere herramientas/ejecuciones autorizadas y revisiones de aceptación; este registro no crea un proceso en segundo plano.**

## 1. Intención y experiencia que se preserva

Las promociones, propuestas de destino, cambios de puesto y ceremonias **NO** se presentan como ventanas de «nivel conseguido», barras de XP, recompensas de videojuego ni notificaciones genéricas diminutas. El mundo Star Trek debe comunicarlas **desde dentro**: un superior, un enlace de Flota, la computadora de la nave, un mensaje oficial por PADD, una conversación o una ceremonia.

Una promoción no se comunica igual a un alférez, un jefe de departamento, un primer oficial o un capitán. El sistema considera la **nave actual, el puesto, el superior competente, las relaciones NPC, el estado de servicio, el lugar y la disponibilidad física/temporal**. La IA puede redactar o interpretar frases y variaciones de diálogo sin tocar autoridad ni acontecimientos profesionales.

La Enterprise-D es la **USS Enterprise NCC-1701-D modernizada**, no la nueva clase histórica Valhalla. La llegada al mando será un acontecimiento especial, **pero el juego debe continuar después con mando jugable y no terminar en créditos**.

### Ejemplos ilustrativos, nunca diálogos obligatorios

- Primer ascenso: al concluir la guardia, una comunicación personal pide acudir al despacho del capitán; el superior entrega las nuevas insignias, que Core ya reconoce.
- Promoción de comandante: acto con algunos oficiales relevantes, quizá en una sala de reuniones; si la situación no permite celebrarlo, primero llega una comunicación legítima.
- Una oferta de destino: un almirante o Personal de Flota contacta al personaje; se solicita su aceptación conforme a la orden, no se altera unilateralmente su puesto.
- Oportunidad de mandar Enterprise-D: conversación con autoridad de Flota y posteriores actos de relevo de mando. Ser capitán **de grado** no supone mandar ese buque.

## 2. Tres tipos de acontecimientos: nunca confundirlos

| Tipo | Estado autoritativo Core | Presentación | ¿Requiere elección? |
|---|---|---|---|
| **Ascenso de grado ya aprobado y efectivo** | `promotion_event_id`, `effective_at`, nuevo rango, orden Personal de Flota | Comunicación o ceremonia posterior | La comunicación/ceremonia puede aplazarse; **no** se deshace el grado legal por no verla |
| **Oferta o propuesta de destino** | Oferta vigente emitida por autoridad, condiciones, vencimiento | Entrevista, PADD privado o comunicación subespacial | **Sí**, si el reglamento profesional exige aceptación |
| **Nombramiento/cambio efectivo de puesto** | Orden de nombramiento y cambio de plaza legítimos | Relevo, anuncio oficial, ceremonia de asunción | Nunca implica automáticamente otro rango ni permite ocupar plaza todavía ocupada |

**Regla decisiva:** separar `effective_at` (fecha real de efecto del acto) de `presented_at` (fecha de la experiencia narrativa). No programar retrasos artificiales del grado únicamente porque el jugador esté de guardia o el modelo del despacho no esté terminado.

## 3. Canal de presentación: prioridad y discreción

Secuencia propuesta para el director de presentación:

1. Recibe **solo hechos profesionales Core autorizados**, con ID estable e información de visibilidad, nunca órdenes generadas por UE5/IA.
2. Consulta el estado de actividad: combate, alerta roja, emergencias, misiones críticas, guardia, descanso, disponibilidad y localización del jugador.
3. Evalúa quién debe comunicarlo: superior del departamento, capitán, oficial de Personal de Flota, almirante u otro actor competente y disponible, según contenido y cargo; no invocar personajes ausentes por arte de magia.
4. Elige canal: intercomunicador, mensaje personal LCARS azul/cian, PADD con acceso privado, holocomunicación, despacho, puente o ceremonia física.
5. Si el contexto no permite el encuentro, conserva una **comunicación pendiente** recuperable; asigna alternativa remota o una nueva cita coherente.
6. Cuando realmente se presenta, registra el acuse/estado narrativo idempotente. Recargar, reintentar o cambiar de cubierta **no** vuelve a crear la misma ceremonia.
7. Muestra el grado y el destino que **Core ya tiene**; el UI no puede escribir directamente el rango, liberar NPC ni crear órdenes.

### Regla UX aprobada para el proyecto

**No enterrar una comunicación profesional importante en una lista de cientos de mensajes secundarios.** La computadora la presenta de forma clara, audible cuando corresponda y reconocible, pero sin tapar la consola de Sensores ni interrumpir combates. Una vez reconocida, queda accesible desde el expediente/PADD personal. Diferenciar «comunicación pendiente» de «acto profesional ejecutado».

## 4. Escenas, diálogos y grados de ceremonia

El director debe tener **plantillas configurables y variantes**, no escenas rígidas asociadas a un único rango:

- Ascensos iniciales: despacho, conversación privada o comunicación de superior con las insignias.
- Ascensos de mayor responsabilidad: entrega de insignias con compañeros y jefes de departamento; solo si hay lugar/personas disponibles.
- Capitán: acto formal de Flota, mando y presencia de personas pertinentes; posibilidad de transmisión a distancia si la nave está desplegada.
- Cambio de puesto: entrevista y notificación separadas del cambio de grado.
- Capitán de Enterprise-D: ceremonia/relevo de mando especial sin reproducirse dos veces después de cargar.

**Relaciones y conocimiento:** los amigos y superiores pueden expresar orgullo, rivalidad, sorpresa o distancia según su historial. La IA solo usa información a la que su personaje está autorizado y que ha adquirido; no desvela decisiones confidenciales de Personal de Flota ni el futuro antes de tiempo.

## 5. Reparto de trabajo y momento exacto

| Hito | Responsable técnico | Compromiso concreto | Requisito de cierre |
|---|---|---|---|
| **F11-P05-A02-01** | Codex Cloud (C++ nativo) | Evento `promotion` auténtico con ID estable, identidad, grados anterior/nuevo, autorización, causa y `effective_at`, consultable desde Core tras guardar/cargar. **NO** construir cinematográficas todavía | Sin evento autoritativo íntegro no se da por válido el ascenso |
| **F11-P05-B** | Codex (C++), ChatGPT revisa contrato | Eventos de oferta, decisión, nombramiento, cambio de unidad y sucesiones NPC con causalidad | No confundir propuesta con rango/puesto |
| **F11-P05-C** | Codex (C++ persistencia + pruebas), ChatGPT revisa | Proyección o cola **persistente** de presentación: `pending`, `scheduled`, `presented` y acuse idempotente asociado a `promotion_event_id` (y análogos) | Guardado/carga a mitad de comunicación, sin duplicados ni pérdida |
| **F11-P05-D** | **ChatGPT** diseña UX, guiones variables y criterios; **Codex** integra C++/UE5; **usuario** valida la inmersión | Director diegético contextual con intercom, PADD, LCARS, reuniones y ceremonia; jerarquía de mensajes y cambios de insignias | Un ascenso y una oferta se viven desde la nave, no una ventana de nivel |
| **F11-P05-E** | ChatGPT diseña batería, Codex ejecuta pruebas nativas/UE, usuario revisa en MSI | Pruebas E2E y campañas, también contra eventos duplicados y superiores ausentes | Evidencias nativas Core + Unreal (NullRHI/D3D12 cuando corresponda) y revisión jugable |

**La preparación de A02-01 es ligera:** no implementar aún un gestor visual de eventos ni un sistema de colas separado; basta con que el evento de promoción **incluya los datos mínimos necesarios** para presentarlo después. La cola persistente se cierra en P05-C y la representación en P05-D. Tampoco se bloquea el ascenso si falta un modelo 3D.

El seguimiento se conserva en [issue #104](https://github.com/robdor80/Videojuego_StarTrek/issues/104), que **permanece abierta** hasta cumplir P05-D/E. El enlace debe figurar en el README F11 y en el encargo A02-01 para que no pueda omitirse accidentalmente.

## 6. Pruebas de aceptación obligatorias

1. Ascenso correctamente autorizado y efectivo: se ve en el expediente Core aunque el jugador esté combatiendo; la ceremonia se aplaza sin bloquear el grado.
2. Final de combate: comunicación personal visible y clara, no equivalente a una alerta normal de Sensores.
3. Guardar **antes** de presentar, recargar y recibir una sola presentación. Guardar **después**, recargar y no repetir.
4. Fallo de escena, NPC superior ausente, jugador en otra cubierta o nave: mensaje personal remoto o cita reprogramada; nunca pérdida del evento.
5. Que el capitán entregue insignias **no** demuestra autorización: solo Core aplica la orden de Personal de Flota.
6. Actualizar insignias, tratamiento verbal y expediente conforme al grado confirmado, con independencia de la fecha de la ceremonia.
7. Oferta de puesto: no cambia plaza ni nave hasta aceptación/orden/efectividad; rechazo sin traslado.
8. Nuevo grado no concede mando de puente ni plaza de primer oficial automáticamente.
9. Ceremonia de mando Enterprise-D: identidad de nave correcta, puesto realmente vacante, cambio oficial de ocupante, continuidad de partida tras el relevo.
10. Eventos profesionales privados no aparecen en pantallas ni PADD de usuarios sin conocimiento/permisos.
11. Varias promociones/nombramientos en periodos acelerados se presentan de forma coherente sin disparar diálogos simultáneos ni caer en bucles.
12. Revisión manual de UX en MSI: idioma castellano, jerarquía LCARS azul/cian y comunicación sin ruido visual.

**No dar por completada esta decisión** solo por disponer de documentos, pruebas offline, un texto emergente o un evento Core sin entrega al jugador. Deben pasar los criterios de P05-D/E.

## 7. Salvaguarda frente a cambios de plan

Si otras fases —por ejemplo NPC sociales, temporadas, PADD o las cubiertas físicas— aún están incompletas, P05-D debe arrancar con una **presentación mínima diegética funcional** (comunicación personal + PADD/expediente + conversación contextual sustituible) y dejar las escenas avanzadas como mejoras incrementales explícitas. No se pierde la obligación ni se finge que la escena final existe.

**Decisión aprobada y persistida; ejecución pendiente de los hitos definidos.**
