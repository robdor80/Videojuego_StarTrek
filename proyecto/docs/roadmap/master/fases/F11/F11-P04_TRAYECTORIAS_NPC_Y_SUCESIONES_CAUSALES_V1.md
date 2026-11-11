# F11-P04 — Carreras autónomas de NPC y sucesiones causales (v1)

**Fecha:** 11-11-2026. **Madurez:** diseño autoral + contrato verificable + director Python **OFFLINE**. No hay nombramientos ni sucesiones ejecutándose en CoreRPG/Unreal; **F11 no está cerrada**.

**Norma principal:** la trayectoria del jugador hacia la capitanía de la **USS Enterprise NCC-1701-D modernizada** debe contar con oportunidades garantizadas y creíbles, **no** con un sorteo que pueda bloquearla indefinidamente. La historia de los NPC debe tener una lógica profesional propia, preparación anticipada, consecuencias y continuidad. La narración controla las circunstancias, **no falsifica** una vacante ni una autorización.

## 1. La separación decisiva

- **Jugador:** aspiración, formación, mérito, grado, responsabilidad, voluntad de aceptar o rechazar.
- **NPC:** rango, expediente, competencias, intereses, relaciones y objetivos profesionales individuales. Los NPC pueden progresar aunque el jugador esté en otra nave o no presencie su ceremonia.
- **Plaza de la nave:** entidad F04/Core persistente que puede estar ocupada, prevista, reservada o realmente libre. `planned` NO equivale a `vacant`.
- **Oportunidad de la Flota:** futuro destino independiente para el NPC (otro mando, puesto de Flota, traslado solicitado, retiro **ya programado legítimamente**).
- **Director de sucesión P04:** propone una cadena causal y la revisa ante nuevas circunstancias. No efectúa ninguna transferencia.
- **CoreRPG/Host (P05):** valida identidad, reloj y revisión, emite/registra decisiones autorizadas y aplica cese/incorporación atómicamente. UE5 solo representa el resultado confirmado.
- **Narrativa e IA:** decide el diálogo, comunicación, ceremonia, impacto social y presentación; nunca tiene credenciales para crear vacantes o firmar órdenes.

El ascenso de grado y la promoción a un **puesto** se mantienen separados: un comandante puede seguir de jefe de departamento; un capitán puede mandar otro buque; el grado de capitán no concede por sí solo la silla de la Enterprise-D.

## 2. Cuatro metas profesionales reconocidas

| Etapa | Condiciones del candidato | ¿Qué hay que conseguir? |
|---|---|---|
| Jefatura de departamento | Teniente comandante o comandante, habilitado para el departamento | Nombramiento legítimo sobre plaza real; jefe anterior puede recibir otro destino si ya existe ocupante |
| Primer oficial de Enterprise-D | Comandante, cualificado para mando | Vacante auténtica de primer oficial + selección de Flota; evolución coherente del XO actual |
| Capitán de otra nave | Capitán cualificado, elección del jugador | Puesto de CO real y oferta profesional; puede ser trayectoria intermedia, **no obligatoria** |
| Capitán de Enterprise-D | Capitán cualificado, trayectoria/evaluación apropiada | Cambio de mando autorizado, plaza libre y selección; **inicio de una etapa jugable extensa**, no epílogo |

El jugador puede **permanecer en la Enterprise-D como primer oficial** mientras no quiera otro destino, o salir temporalmente y regresar como candidato. P04 no hace obligatorio pasar exactamente dos años en otro buque; es un ejemplo narrativo de buen ritmo que después se calibrará. La era de campaña, clases y puestos verdaderamente implementados se verifican contra el catálogo de naves y WorldState; el nombre Enterprise-D no significa que su representación y dotación Core estén ya activadas.

## 3. Ejemplo de sucesión de primer oficial

1. **Años previos:** el XO realiza misiones, recibe buenas evaluaciones y comunica interés por su propio mando. Los datos se registran sin relacionarlos necesariamente con la situación del jugador.
2. **Nueva necesidad de Flota:** existe (o se activa mediante un hecho coherente) una vacante real de capitán en otra nave. El sistema comprueba que dicho puesto pertenece a una unidad operativa, es compatible, tiene autorización y existe evaluación/promoción adecuada del XO.
3. **Oferta al NPC:** el XO considera la propuesta. Puede aceptarla o rechazarla. La decisión del NPC no se reescribe porque el jugador necesite la plaza.
4. **Si la acepta:** se producen evaluación de ascenso y órdenes de Flota válidas, con preaviso. El XO sigue siendo el XO de Enterprise-D **hasta la fecha efectiva del traslado**. No se crea una plaza libre antes.
5. **Se efectúa el traslado:** Core registra cese, relevo, destino nuevo, posibles promociones y continuidad histórica. **Solo entonces** verifica que la antigua plaza está realmente vacante.
6. **Selección de sucesor:** nuestro comandante es candidato cualificado junto a otros. El capitán puede recomendarlo y el órgano competente debe confirmar el nombramiento según la autoridad de P01.
7. **Si somos seleccionados y aceptamos:** Core registra la nueva ocupación atómica. Cambian responsabilidades, acceso operativo, guardias, camarote y relaciones; **el rango no cambia necesariamente**.

La oportunidad **se prepara deliberadamente** para favorecer la progresión del jugador, pero cada decisión visible es profesionalmente defendible. Las carreras de NPC siguen durante la ausencia del jugador y el primer oficial que se marcha no desaparece: puede regresar en temporadas futuras como capitán de otro buque.

## 4. Ejemplo de acceso al mando de Enterprise-D

Un capitán de la D consolidado en su puesto puede recibir promoción a una responsabilidad superior de Flota, traslado a otra nave de especial relevancia o una jubilación que **ya era creíble y estaba planificada**. De aceptar, dejará la D en una fecha con suficiente preaviso. Podría recomendar a nuestro antiguo XO, que quizá lleve un periodo al mando de otra nave y conozca bien el buque y su dotación. El Mando de Flota comprueba las candidaturas, necesidad operacional y la trayectoria del personaje.

Una promoción a almirante **NO** se produce porque el jugador ya sea capitán: necesita expediente, puesto de Flota auténtico y decisión autorizada. En este contrato, `fleet_staff` es una **categoría de oportunidad**, no una plaza implementada. Requiere que el futuro cargo de Estado Mayor esté realmente catalogado y verificado en Core/Host; P04 no lo inventa.

El jugador puede rechazar el regreso o preferir permanecer al mando de su otra nave; el sistema no cancela otras opciones. Si quiere llegar a capitanear la D, el planificador mantiene abierta una ruta razonable. **No se declara aún que el juego real sepa garantizar ese resultado**: lo demostrarán P05 y la simulación de campañas a largo plazo.

## 5. Qué ocurre si el NPC rechaza el traslado

**Prohibido:** convertir su rechazo en una aceptación, despedirlo por incompetencia ficticia, inventar un accidente, simular que su puesto está vacante, promover un oficial sin pruebas o alterar el pasado para que parezca lógico.

**Correcto:**
- Conservar al NPC y su puesto, registrar su decisión y la razón profesional.
- Consultar otros destinos plausibles que Flota pueda ofrecerle (cuando sean coherentes con su expediente y prioridades).
- Preparar alternativas **legítimas**: otra convocatoria de mando, una comisión superior realmente disponible, solicitud de traslado propia o relevo escalonado planificado.
- Mantener el ancla temporal de P03, la obligación de ofrecer oportunidades al jugador y el histórico de alternativas fallidas.
- Si ninguna alternativa está comprobada, emitir **`FLEET_ALTERNATIVE_REQUIRED`** o, vencido el plazo, **`URGENT_FLEET_ESCALATION`**; **nunca** reportar progreso ficticio.

Un rechazo puede alargar la historia y variar el camino. Lo que no puede ocurrir es que el juego «olvide» que el protagonista sigue esperando una oportunidad durante quince años.

## 6. Estados del director de sucesión (referencia)

| Resultado | Interpretación |
|---|---|
| `INVALID_CONTEXT` | Identidad, puesto, mérito, revisión, plan P03 o hechos no verificables |
| `PLAYER_PAUSED` | Jugador rechaza/pospone, sin cambio forzado |
| `ALREADY_IN_TARGET_POST` | El jugador ya ocupa el puesto, demostrado por la misma entidad/ocupante |
| `DIRECT_SELECTION_POSSIBLE` | La plaza realmente está libre; falta evaluación/selección/orden |
| `AWAITING_NPC_DECISION` | Hay una oportunidad profesional fundada; NPC debe decidir |
| `AWAITING_VALID_ORDERS` | NPC ha aceptado; falta orden autorizada |
| `AWAITING_EFFECTIVE_DEPARTURE` | Existen órdenes, pero el NPC sigue en el puesto hasta el relevo |
| `AWAITING_VACANCY_CONFIRMATION` | Se alega salida efectiva, pero la plaza Core todavía figura ocupada; resolver contradicción, no expulsar |
| `FLEET_ALTERNATIVE_REQUIRED` | El NPC rechaza o no existen opciones fundadas; buscar otra vía |
| `URGENT_FLEET_ESCALATION` | Se alcanzó el horizonte de P03 sin vía válida; la obligación permanece |

La selección entre opciones está **ordenada y es determinista**: primero las ya aceptadas/autorizadas, luego las todavía en deliberación, respetando fechas y motivos verificados. No se elige arbitrariamente el primer NPC por facilidad; en esta versión P04 solo contempla el titular legítimo de la plaza, sin reemplazarlo por un personaje artificial.

Los planes derivan de `episode_id + upstream_plan_id + target_billet_id`: al avanzar un mes o cambiar el orden de consulta **no** se genera otro plan distinto. P03 aporta la **fecha de preparación y fecha límite persistentes**; P04 nunca reinicia ese reloj.

## 7. Estados y eventos que deben persistirse (F11-P05)

En un único origen autoritativo (CoreRPG) habrá que registrar:

- Identidad de episodio P03/P04, revisión del mundo, hora/mes ficticio, objetivos y alternativas.
- Méritos del NPC, su evaluación, ambiciones propias previas, oferta formal y aceptación/rechazo **real**.
- Candidaturas del NPC a otras plazas, autorización para promoción cuando corresponda, orden oficial y fecha efectiva.
- Evento de salida del NPC, actualización de su nueva plaza, guardias, accesos, relaciones y expediente (historial append-only).
- Comprobación de nueva vacante en la D **después** del cese.
- Evaluación de candidatos al puesto vacante, recomendación del capitán, selección de Flota, consentimiento del jugador y orden de nuevo destino.
- Promoción del jugador como un evento **distinto** de cambio de puesto, sin XP por decreto.
- Guardado/carga, deduplicación, reintentos, revisión de plazos y auditoría de que dos personajes nunca ocupan la misma plaza.

**F11-P05 deberá contener pruebas end-to-end reales** con los casos de cadena completa, NPC que rechaza, jugador que rechaza, destino incompatible, guardado durante relevo y recuperación con los mismos cargos sin duplicados.

## 8. Limitaciones técnicas expresas

El contrato `sistemas/gameplay/careers/succession/f11_p04_causal_succession_policy_v0.1.json` y el director `desarrollo/tools/validation/f11_p04_succession_reference.py` trabajan sobre **instantáneas de prueba**. Algunos indicadores terminados en `verified` son **suposiciones del escenario**: no autentican por sí solos una orden o una plaza. Por eso ninguna respuesta otorga autoridad ni modifica el estado del mundo. P01/P02 siguen teniendo la autoridad semántica para validar posiciones y vacantes; las pruebas P04 no sustituyen sus filtros de integración.

Los plazos de preaviso, elección del NPC y revisión alternativa son **ilustrativos**, igual que los meses de P03. El diseño narrativo definitivo puede ajustarlos. La cronología TNG/VOY/DS9 y la clase de nave deben ser coherentes con el catálogo de época. La mera presencia de la marca `enterprise_d_ncc_1701_d_refit` **no** constituye alta de nave operativa.

**Resultado comprobable de P04 en esta rama:** para situaciones simuladas correctamente preparadas, el director diseña rutas causales, evita doble ocupación, diferencia estados de decisión/orden/salida/vacante, conserva la urgencia y sugiere vías alternativas; **no** crea por sí mismo una oportunidad efectiva. Por tanto, no declarar en este paso «progresión garantizada jugable».

## 9. Puerta de aceptación de referencia P04

- [ ] Documentación/contrato de cuatro objetivos profesionales y NPC con carrera autónoma.
- [ ] Director no mutador con alternativas y pruebas de aceptación/rechazo, plazos, identidad y vacantes.
- [ ] Estados diferenciados antes/después de orden efectiva y revalidación de vacante Core.
- [ ] Recorrido sintético de cuatro etapas con progresión **por eventos externos**, sin ascensos automáticos.
- [ ] CI F11 completa + verificaciones de gobierno sin regresiones.
- [ ] PR trazable y explícita frontera P05 (CoreRPG/Host/UE5).
