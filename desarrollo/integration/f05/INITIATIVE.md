# F05-P03 — Iniciativa NPC determinista

Entrega nativa para auditoría independiente sobre Star Trek main
`aff01c31c386fe0813320b82a828e2e6c5ab23d8`. CoreRPG main comprobado y fijado en
`76a7b7b485616d8c4994f384a90f123bf333591d`, sin modificaciones.
F05 permanece abierta; P04/P05/F06 no se desarrollan en esta entrega.

## Necesidad real y alcance

La primera necesidad soportada es **un escaneo pendiente para un servicio de
Sensores existente**. El mando efectivo o una jefatura Sensores autorizada registra
una obligación mediante `f05_scan_need`, indicando el registro DUTY F04 y un
intervalo contenido en ese servicio. No afirma que haya contactos, averías ni
incidentes. Es una instrucción operativa persistente de efectuar una comprobación,
no una detección simulada de F06. Cada servicio admite una obligación en P03.

La autoridad y el servicio se verifican al crearla. La obligación no se conoce
automáticamente: `f05_brief_need` registra una comunicación formal explícita,
autorizada por su autor aún habilitado o por el mando efectivo. Core aprende solo
existencia/definición de la obligación, intervalo y referencias a puesto, servicio
y proveedor. El informe no comparte conocimientos privados del emisor.

`f05_evaluate` es un controlador acotado del dominio Trek, invocable después de
`f04_advance` o de un evento/entrada real del Host. Core tiene Timeline y
ActionEngine, pero no un servicio de planificación de oficiales compatible.
Por eso no se instala ningún scheduler global ni se atribuye esa capacidad al
Core. El Host decide qué NPC/necesidad evaluar y cuándo, usando el reloj Core.
No debe inventar ticks, necesidades ni una aceptación del jugador.

## Decisiones y autorización

La API aditiva [f05_initiative.h](include/f05_initiative.h) usa el mismo
`F04Session`. Primero se fija una vez la identidad autenticada del jugador con
`f05_bind_player`. Este dato persiste, y cambiarlo dentro de la campaña se rechaza.
Una sesión sin esa configuración no habilita autonomía. Los otros militares de
la nave son candidatos NPC; categoría, pertenencia y scopes se comprueban.

El contexto se obtiene con `Visibility::project` **sin grants temporales**, seguido
de `ContextBuilder` filtrado al sujeto solicitado. Solo se decide desde los siete
hechos de obligación recibidos por ese personaje. Una necesidad existente pero
desconocida y un ID inexistente producen la misma solicitud de información, sin
referencia visible ni detección. No se consulta un registro global para reconstruir
conocimiento. La autorización y las condiciones físicas sí se consultan contra el
estado real: son comprobaciones que impiden efectos, no descubrimientos del NPC.

| Situación | Decisión y efecto |
|---|---|
| Contexto desconocido o incompleto | `CLARIFY`, sin orden |
| Obligación aún no debida | `NO_ACTION`, sin detección ni orden |
| Obligación vencida | `REPORT`, sin ejecutar |
| Actor incapacitado | `NO_ACTION`, sin ordenar |
| Oficial sin atribución | `ESCALATE` al mando efectivo, sin orden |
| XO sin atribución efectiva | `PROPOSE`, sin orden ni sucesión implícita |
| Mando/jefatura Sensores habilitados | `ISSUE_ORDER` mediante P01 |
| Mandato P02 efectivo | Emisión P01 con mandato fijado, estación/ejecutor/límites P02 |
| Mandato manual o propuesta | `PROPOSE`; orden `issued`, sin tarea hasta aprobación P02 real |
| Destinatario jugador | `WAIT_PLAYER`; jamás se recibe/ejecuta automáticamente |
| Destinatario NPC de orden conocida | `CONTINUE_TASK`: recibir **o** ejecutar por P01 |
| Intento ya terminal | Sin nuevo intento ni otra orden para esa obligación |

La selección usa **un proveedor conocido**, el ocupante del servicio F04 indicado
en la obligación. Se comprueban cualificación, nombramientos cuando proceden,
disponibilidad, guardia, puesto y presencia lógica. No busca reemplazos secretos,
no mueve personas y no reasigna guardias. Si no es elegible informa o escala.
El rango y la proximidad al jugador no conceden autoridad. F04 determina el mando
efectivo; ser XO por sí mismo no permite ordenar mientras otro conserva el mando.

La recepción y ejecución pasan por `f05_receive` y `f05_execute_order` originales.
P01/P02 revalidan origen, cualificación, disponibilidad, guardia, ubicación, revisión,
plazo y mandato. Revocar un mandato ya fijado no permite sustituirlo por otro
cargo o delegación. Se conserva el resultado fallido con `performed=0` y los
eventos reales P01. No se revierte una acción confirmada anteriormente.

## Causalidad, persistencia y límites de trabajo

| Entidad Core nueva | Función |
|---|---|
| `f05_player` | Identidad del jugador fijada por Host, revisión y tick |
| `f05_scan_need` | Obligación autorizada e inmutable; servicio, origen, intervalo, causa |
| `f05_brief` | Comunicación explícita, emisor, receptor, necesidad, key/revisión/causa/tick |
| `f05_detection` | Detección de obligación conocida ya debida, por actor/revisión/tick |
| `f05_decision` | Decisión inmutable, motivo, contexto examinado, key, detección y orden si existe |

La petición P01 añade una referencia opcional a su necesidad. La orden, recepción,
tarea, intento, resultado y eventos son exactamente los de P01. Propuestas e
informes se distinguen por el tipo de decisión y nunca se presentan como acciones
ejecutadas. El destinatario de una propuesta/informe indica el mando al que debe
dirigirse; **no entrega ni aprueba automáticamente** esa propuesta, ni enseña al
destinatario nuevos hechos. La difusión posterior requiere una comunicación real.

Los campos y referencias se validan antes de publicar o restaurar: formas cerradas,
unicidad de keys y servicio, máximo una orden por necesidad, causalidad de decisiones,
referencias a orden/detección y conocimiento permitido por comunicaciones. Un
archivo válido para Core puede rechazarse por incumplir estos contratos Trek.
Todas las escrituras relacionales pasan por ActionEngine; `learn_fact` captura
los hechos comunicados usando la API de conocimiento Core empleada en F03.

La transacción por copia abarca la llamada P01 y el registro P03, preservando
WorldState, RNG y Timeline ante un fallo. No hay almacén lateral. Se reutilizan
CampaignPersistence e HistoryPersistence. Se retienen las obligaciones y sus
dependencias históricas para no perder tombstones al consolidar.

Límites explícitos: una necesidad, un proveedor, **una transición P01 máxima por
evaluación**, de 1 a 32 hechos examinados; selección completa requiere los siete
hechos de la obligación. El contexto truncado no autoriza. Máximos persistentes:
128 obligaciones, 512 comunicaciones, 2048 decisiones, 4096 hechos conocidos por
personaje y un jugador; permanecen los topes P01/P02 y de residentes F04. Las
consultas de decisiones devuelven páginas propias de 1 a 64. Los índices y el
validador siguen recorriendo estado F04 acotado por esos presupuestos; no se ofrece
una garantía de latencia constante ni un planificador para toda la tripulación.

Las keys se separan por obligación, comunicación y evaluación. Misma key/payload
reproduce el registro, incluso tras recuperación y revisión posterior; payload
distinto se rechaza. La emisión P01 usa la key de evaluación en el espacio de keys
P01: el Host debe reservar keys no utilizadas por otras órdenes. Una colisión
rechaza atómicamente la evaluación, sin detecciones, órdenes o RNG parciales.
Una key nueva reevalúa el estado actual pero no duplica una obligación ya ordenada.
No hay reintento automático de órdenes terminales. Los scopes de proceso se renuevan
al cargar, manteniendo los EntityIds persistentes.

## Verificación y límites deliberados

Compilar con los comandos del [README](README.md). `ctest -R '^f05.p03_'` ejecuta
los escenarios nativos; `ctest -R '^f05\.'` incluye P01/P02. La selección corta del
README incluye regresión F04. F02/F03 y las campañas largas conservan sus pins
originales; las campañas usan sus seis oráculos congelados, sin cambiar expectativas.
La suite completa Core se compila aparte con JSON y BUILD_TESTING activados.

No existe dependencia de Actor, UWorld, animación, UI, puente o proveedor IA en
el controlador. Las pruebas nativas comparan bytes de campaña, decisiones, reloj
y streams tras recuperar en otro proceso. Las pruebas con **UWorld real** están
preparadas en el harness aislado y continúan pendientes del MSI; el test nativo
de representación no sustituye la ejecución Unreal.

Solo se ejecuta `F04_SCAN`: `ActionEngine::process(StreamRollAction{0xF0401,1,100})`.
No produce contactos, averías, descubrimientos, tareas de reparación, política de
guardias, asignación de recursos, diálogo, IA remota ni autonomía de flota. No hay
retención escalable, aprobación implícita, recepción de informes universal ni
teletransporte del operador. El host de confianza y propietario único no equivale
a autenticación de red. La durabilidad externa exige guardar/publicar y confirmar
la generación Core; el bloqueo tras publicación incierta se conserva.

[Entrega y evidencias](../../../proyecto/docs/roadmap/master/fases/F05/F05-P03_IMPLEMENTACION.md)
· [Continuación MSI](../../../proyecto/docs/roadmap/master/fases/F05/VALIDACIONES_PENDIENTES_MSI_P03.md).
