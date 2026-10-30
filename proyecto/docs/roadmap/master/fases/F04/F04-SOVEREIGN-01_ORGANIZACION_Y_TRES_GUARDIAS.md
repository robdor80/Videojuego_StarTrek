# F04-SOVEREIGN-01 — Organización y tres guardias

Entrega para auditoría independiente mediante PR Draft contra `main`, sin fusión. **F04 permanece EN_CURSO**.
Base exacta: `ff975c8b9d4b02ba8fe2a3f36d2b184f95a6ecee` (PR #68 incluida).
Rama: `codex/f04-sovereign-organizacion-tres-guardias`.
Worktree aislado: `C:/F04/Sovereign01`; compilación y laboratorio: `C:/F04/SovereignBuild`.

## Perfil y alcance

Perfil aditivo `F04_SOVEREIGN_MULTIMISSION=3`: Sovereign estándar multimisión posterior a Nemesis, 700 plazas permanentes de Flota, cero civiles residentes nominales, siete departamentos y 59 secciones. Sutherland=1 e Intrepid=2 conservan sus tablas, claves, distribuciones y operaciones anteriores.

Se reutilizan `F04TemplateSpec`, `F04SectionSpec` y `trek_templates::Profile`. El mismo motor acepta demandas por sección y servicios críticos por perfil. Miranda e Intrepid no reciben nuevas distribuciones Beta/Gamma: la operación nueva devuelve REVIEW si el perfil carece de demandas aprobadas. No se implementan Odyssey ni Valhalla.

Fuentes locales verificadas: catálogo `mundo/lore/starships/classes/core_starship_classes.json`, perfil `classes/depth/STARFLEET_CLASS_DEPTH_PROFILES_v0.1.json` y `classes/shipboard_life/STARFLEET_SHIPBOARD_LIFE_PROFILES_v0.1.json`. Las proporciones orientativas de vida a bordo no sustituyen la tabla explícitamente aprobada para esta configuración.

## Dotación completa y día de referencia

[Las 700 plazas identificadas](F04-SOVEREIGN-01_PLANTILLA_700.md) y [snapshot consultado a la DLL](evidence/F04-SOVEREIGN-01/reference-snapshot.json).
Cada plaza posee una clave estable `nave / perfil / sección*100+ordinal`; 700 claves y 700 personas Core diferentes. Cada persona ocupa un destino nominal único y una sola guardia ordinaria en el día. Los nombramientos y las funciones no generan identidades adicionales. La fixture es explícita y sintética sobre población Core ya existente; no impone cualificaciones a una campaña previamente caracterizada.

| Departamento | Total | Alpha | Beta | Gamma | Fuera |
|---|---:|---:|---:|---:|---:|
| Mando y navegación | 50 | 17 | 10 | 7 | 16 |
| Ingeniería y mantenimiento | 180 | 60 | 38 | 27 | 55 |
| Ciencias y sensores | 130 | 50 | 25 | 16 | 39 |
| Operaciones y comunicaciones | 115 | 36 | 26 | 18 | 35 |
| Seguridad y táctica | 110 | 32 | 27 | 19 | 32 |
| Lanzaderas y logística | 75 | 22 | 16 | 7 | 30 |
| Medicina | 40 | 13 | 8 | 6 | 13 |
| **Total** | **700** | **230** | **150** | **100** | **220** |

Las 59 secciones aprobadas:

| Nº | Sección | Total | Alpha | Beta | Gamma | Fuera |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Capitán | 1 | 1 | 0 | 0 | 0 |
| 2 | Primer oficial | 1 | 1 | 0 | 0 | 0 |
| 3 | Segundo oficial y oficiales de guardia | 8 | 2 | 2 | 2 | 2 |
| 4 | Timón y navegación | 14 | 4 | 3 | 3 | 4 |
| 5 | Planificación estratégica y misiones | 9 | 4 | 2 | 1 | 2 |
| 6 | Diplomacia y protocolo | 7 | 3 | 1 | 0 | 3 |
| 7 | Coordinación de expediciones | 5 | 1 | 1 | 1 | 2 |
| 8 | Enlace con Flota y registros de mando | 5 | 1 | 1 | 0 | 3 |
| 9 | Jefatura y adjuntos | 4 | 2 | 1 | 0 | 1 |
| 10 | Motores warp e impulso | 36 | 10 | 8 | 6 | 12 |
| 11 | Reactor y antimateria | 28 | 8 | 7 | 5 | 8 |
| 12 | Distribución de energía EPS | 21 | 7 | 4 | 4 | 6 |
| 13 | Integridad estructural y escudos | 20 | 7 | 4 | 2 | 7 |
| 14 | Soporte vital y control ambiental | 18 | 6 | 4 | 3 | 5 |
| 15 | Núcleos de ordenador y hardware | 15 | 5 | 3 | 2 | 5 |
| 16 | Deflectores, tractores y emisores | 14 | 4 | 3 | 2 | 5 |
| 17 | Mantenimiento y reparación general | 18 | 9 | 3 | 2 | 4 |
| 18 | Control de daños técnico | 6 | 2 | 1 | 1 | 2 |
| 19 | Jefatura científica y adjuntos | 4 | 2 | 1 | 0 | 1 |
| 20 | Sensores y astrometría | 28 | 10 | 6 | 4 | 8 |
| 21 | Física y astrofísica | 18 | 8 | 4 | 2 | 4 |
| 22 | Biología y xenobiología | 18 | 7 | 3 | 2 | 6 |
| 23 | Geología y planetología | 14 | 6 | 2 | 1 | 5 |
| 24 | Xenolingüística y culturas | 10 | 5 | 1 | 1 | 3 |
| 25 | Laboratorios y muestras | 16 | 6 | 3 | 2 | 5 |
| 26 | Cartografía y expediciones | 12 | 4 | 3 | 2 | 3 |
| 27 | Análisis de datos científicos | 10 | 2 | 2 | 2 | 4 |
| 28 | Jefatura de Operaciones | 4 | 2 | 1 | 0 | 1 |
| 29 | Comunicaciones subespaciales | 20 | 6 | 5 | 4 | 5 |
| 30 | Transportadores | 21 | 6 | 5 | 4 | 6 |
| 31 | Informática y software | 20 | 7 | 5 | 2 | 6 |
| 32 | Gestión de recursos | 14 | 5 | 3 | 2 | 4 |
| 33 | Circulación interna y control de servicios | 12 | 3 | 3 | 2 | 4 |
| 34 | Holocubiertas y servicios recreativos | 10 | 3 | 2 | 1 | 4 |
| 35 | Cifrado y enlaces protegidos | 8 | 2 | 1 | 2 | 3 |
| 36 | Sistemas auxiliares operativos | 6 | 2 | 1 | 1 | 2 |
| 37 | Jefatura de seguridad y táctica | 4 | 2 | 1 | 0 | 1 |
| 38 | Táctica del puente y control de armas | 19 | 5 | 4 | 4 | 6 |
| 39 | Fáseres y torpedos: operación y custodia | 18 | 5 | 4 | 4 | 5 |
| 40 | Escudos y contramedidas | 14 | 4 | 4 | 2 | 4 |
| 41 | Seguridad interior y patrullas | 25 | 7 | 7 | 4 | 7 |
| 42 | Custodia y control de accesos | 10 | 3 | 2 | 2 | 3 |
| 43 | Equipos de intervención y abordaje | 10 | 3 | 2 | 2 | 3 |
| 44 | Protección de misiones exteriores | 6 | 2 | 2 | 1 | 1 |
| 45 | Investigación de seguridad | 4 | 1 | 1 | 0 | 2 |
| 46 | Jefatura de hangares y logística | 3 | 1 | 1 | 0 | 1 |
| 47 | Pilotos de lanzaderas | 12 | 3 | 3 | 2 | 4 |
| 48 | Operación de hangares | 14 | 4 | 3 | 1 | 6 |
| 49 | Mantenimiento de naves auxiliares | 12 | 3 | 2 | 1 | 6 |
| 50 | Carga, almacenes e inventario | 15 | 5 | 3 | 1 | 6 |
| 51 | Abastecimiento y reciclaje | 7 | 2 | 1 | 1 | 3 |
| 52 | Equipos de misiones exteriores | 8 | 3 | 2 | 1 | 2 |
| 53 | Transporte VIP y servicios especiales | 4 | 1 | 1 | 0 | 2 |
| 54 | Jefatura médica | 3 | 1 | 0 | 0 | 2 |
| 55 | Médicos de guardia y urgencias | 11 | 3 | 3 | 2 | 3 |
| 56 | Enfermería | 12 | 4 | 3 | 2 | 3 |
| 57 | Diagnóstico y biocontención | 6 | 2 | 1 | 1 | 2 |
| 58 | Cirugía y traumatología | 5 | 2 | 0 | 1 | 2 |
| 59 | Psicología y asesoramiento | 3 | 1 | 1 | 0 | 1 |

## Responsabilidades, cualificaciones y servicios

Mando dirige, navega, planifica misiones, coordina expediciones y presta diplomacia/protocolo y enlace institucional. Ingeniería mantiene propulsión, reactor, EPS, estructura, escudos, soporte vital, hardware, emisores y reparaciones. Ciencias opera sensores y sus disciplinas/laboratorios. Operaciones gestiona comunicaciones, transportadores, software, recursos, servicios y holocubiertas. Seguridad controla táctica, armas, escudos, accesos, patrullas e intervención. Logística gestiona hangares, pilotos, suministros y misiones exteriores. Medicina presta dirección sanitaria, clínica, enfermería, diagnóstico, cirugía y asesoramiento.

La especialidad principal se conserva en la plaza. Una suplencia exige la máscara completa de competencias real y su vigencia durante el intervalo, sin añadir credenciales. Se añaden IDs de especialidad 31–35 para psicología, diplomacia, xenolingüística, cifrado y cirugía; las máscaras anteriores no cambian. Psicología no concede atención clínica de urgencias; diplomacia no concede cualificación de mando; xenolingüística no concede sensores. Cirugía tiene habilitación clínica explícita en la fixture. Ingeniería mantiene escudos sin adquirir operación táctica; operar armas no concede mando. Timón y pilotos auxiliares son cualificaciones diferentes.

Ocho funciones críticas independientes por ventana: mando, timón, sensores, operaciones, comunicaciones, ingeniería, táctica y respuesta médica presencial cualificada. Cada función se asigna explícitamente a una persona de servicio. Una persona no ocupa dos funciones críticas simultáneas. Las funciones representan presencia lógica en la instalación correspondiente, sin requerir un Actor ni simular desplazamientos. Las demás personas de ciencias trabajan en laboratorios, análisis o instalaciones de su sección; no se materializa a todos en el puente. Sus agendas siguen siendo válidas sin el jugador.

## Reloj y ventanas

Se utiliza exclusivamente `CoreRPG.Timeline`, en segundos de campaña, con intervalos `[start,end)`:

- Gamma de D: `[D+0,D+28800)` (00:00–08:00).
- Alpha de D: `[D+28800,D+57600)` (08:00–16:00).
- Beta de D: `[D+57600,D+86400)` (16:00–24:00).
- Gamma siguiente comienza exactamente en D+86400.

Las consultas comprueban comienzos, finales, ausencias interiores, cancelaciones y caducidad de credenciales. No equiparan disponibilidad nominal con cobertura. Las 220 personas Fuera no generan eventos REST automáticos. El descanso protegido se crea expresamente mediante REST y se respeta como obligación.

## Cadena de mando y relevos

Capitán y primer oficial trabajan Alpha en el día de referencia. Existe exactamente un segundo oficial: ordinal 1 de la sección 3, con nombramiento SECOND explícito. Los otros siete integrantes no reciben ese título. Jefes y adjuntos tienen nombramientos separados, sin sucesión automática por rango o adjuntía. Solo ordinales 1 y 2 de las jefaturas técnicas son HEAD y DEPUTY; las demás plazas del grupo son especialistas de la jefatura.

SCHEMA 4 exige disponibilidad, cualificación y servicio efectivo para ejercer mando operativo. La precedencia es CAPTAIN, FIRST, SECOND, SUCCESSOR y WATCH autorizado por intervalo. Un WATCH no se convierte permanentemente en capitán. La función de táctica y la autoridad médica no otorgan sucesión. Un adjunto departamental continúa sin ser sucesor automático, preservando la corrección de PR #67.

Ingeniería dispone de un DUTY_HEAD temporal cualificado por guardia, incluso Gamma, separado del jefe titular y de la sucesión del buque. Su autoridad técnica queda limitada a su departamento y ventana. Los ocho servicios críticos reciben responsables reales; no se exige presencia del jefe titular las 24 horas. La respuesta médica inicial puede prestarla personal clínico o de enfermería habilitado, sin contar un EMH como tripulante.

## Política ordinaria y planificación multisemanal

`F04_PLAN_WATCHES`: inicio/fin a medianoche; horizonte explícito de 1–28 días; patrón 3×8. REFERENCE programa un único día con la tabla exacta. ROTATING puede sembrar ese primer día y modificar las asignaciones posteriores. El patrón 4×6 existente permanece para los esquemas anteriores; un cuadrante SCHEMA 4 exige revisar su planificación antes de cambiar a otro patrón.

Se imponen cinco turnos como máximo en cualquier ventana móvil de 168 horas, al menos 12 horas entre obligaciones ordinarias, un turno como máximo por día natural, ausencia de solapamientos y credenciales/nombramientos vigentes. Las obligaciones ya existentes se consideran, incluidas las realizadas antes de una cancelación. Un STOP conserva el tramo trabajado para impedir que una cancelación borre carga de trabajo del historial. Los francos se distribuyen mediante una fase determinista por persona y semana; la preferencia de guardia y los días sin servicio cambian con la semana.

Primero se protegen los servicios críticos. Se reserva hasta ocho personas reales, ya cualificadas y diferentes por servicio, para impedir que la actividad discrecional agote sus cinco turnos al comienzo de la semana. Capitán y primer oficial quedan fuera de esa reserva cuando hay oficiales de guardia suficientes. Las plazas y cualificaciones no cambian. Después se intenta alcanzar el cupo departamental diario; se reduce actividad no crítica cuando la política de relevos/descanso impide llenarlo. Las actividades científicas y técnicas programadas siguen durante Beta/Gamma sin presencia del protagonista.

No es un optimizador exhaustivo: una carencia del algoritmo no demuestra que cualquier otro cuadrante sea matemáticamente imposible. La repetición literal de cada sección sí tiene incompatibilidades, como 7 Alpha de capitán frente a capacidad 5, o 21 turnos semanales de una jefatura de cuatro personas frente a capacidad 20. Estas incompatibilidades no se ocultan ni se resuelven inventando competencias.

## Simulaciones ejecutadas

Cada horizonte parte de la misma fixture de 700 personas y siembra el día de referencia. La auditoría independiente de los registros consultados comprueba individuos, cualificaciones, ventanas móviles, separación y cobertura en todos los límites. El guardado/carga conserva el mismo futuro al avanzar de una vez o por ventanas.

| Días | Turnos programados | Objetivo departamental | Sin programar respecto al cupo | Servicios críticos cubiertos | Máximo móvil | Separación mínima | Turnos capitán |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 3184 | 3360 | 176 | 168/168 | 5 | 16 h | 5 |
| 14 | 6414 | 6720 | 306 | 336/336 | 5 | 16 h | 10 |
| 28 | 12648 | 13440 | 792 | 672/672 | 5 | 16 h | 20 |

No hay déficits críticos en estos horizontes sin incidencias. Las carencias de cupo son reales y persisten como `roster_gap`: reducen actividad programada, no personas ni plazas. No equivalen a otros tantos servicios críticos caídos. Véanse [simulaciones](evidence/F04-SOVEREIGN-01/simulations.json), [cuadrante de 28 días](evidence/F04-SOVEREIGN-01/roster-28-days.csv), [recuentos por día](evidence/F04-SOVEREIGN-01/daily-counts-28-days.json) y [carencias](evidence/F04-SOVEREIGN-01/gaps-28-days.json).

En 28 días cambian de guardia 675 personas y hay 6952 persona-días sin guardia ordinaria. Esos días no se etiquetan automáticamente como descanso protegido. El capitán trabaja 20 turnos con días libres; las pruebas también verifican los del primer oficial.

## Bajas, vacaciones, transferencias y emergencias

ABSENCE y MEDICAL conservan el evento y hacen visible la vacante operativa. Las incidencias de agenda, credenciales, traslado, salida, cancelación o revocación generan snapshots persistentes de los servicios críticos descubiertos en los planes afectados. `roster_gap` conserva el historial de planificación/incidencias; la consulta de cobertura vuelve a calcular la situación actual y no interpreta un déficit histórico como todavía abierto tras resolverlo.

`f04_relief_candidates_page` propone personas existentes con cualificaciones completas, nombramientos, disponibilidad y límites de jornada válidos. Es una consulta y no concede autoridad. `F04_COVER_DUTY` confirma una sustitución temporal con causa y mando vigente, detiene el tramo sustituido y conserva la relación con la actividad original. No desasigna la plaza nominal de ninguna persona ni cambia su departamento o especialidad. Requiere nombramiento válido si el destino lleva responsabilidad; no convierte a un suplente del puente en capitán permanente.

`F04_CANCEL_DUTY` cancela servicio futuro sin borrar el pasado. `F04_TRANSFER`, ASSIGN, DEPART y EMBARK conservan su finalidad explícita de destino/miembro; se prueban vacantes, retorno de la misma identidad y reasignación. Un traslado detiene actividades/funciones y nombramientos temporales afectados. La salida de un emisor en SCHEMA 4 no cancela indiscriminadamente las guardias y nombramientos legítimos de otras personas. RELIEF anterior sigue siendo el relevo con cambio de asignación nominal; COVER_DUTY es la alternativa temporal aditiva.

Las bajas y vacaciones caducan sin inventar una persona de reemplazo. Sin sustituto habilitado se mantiene la carencia. No hay un agente autónomo que confirme todos los relevos: la búsqueda y la propuesta requieren una decisión con autoridad vigente. El test de inviabilidad retira a las 32 personas habilitadas para sensores, incluida la jefatura: registra los 21 servicios de sensores descubiertos de siete días. La fixture parcial de 25 personas mantiene 700 plazas y carencias reales.

RECALL exige emergencia documentada y conserva deuda de descanso. El planificador excluye a quien tenga deuda pendiente; no la liquida automáticamente al pasar el tiempo o cargar. La programación extraordinaria y una política de recuperación/compensación de fatiga siguen separadas de los turnos ordinarios; no se simula aún fisiología por especie.

## Persistencia y compatibilidad

La autoridad única sigue en WorldState, relaciones Core y Timeline. El índice por tipo/persona es una proyección descartable, invalidada al mutar, cargar o cambiar de llamada; nunca se guarda como otro almacén. Las propuestas del planificador solo viven durante la transacción, cuyo resultado se publica atómicamente tras validar.

ABI C 1 ampliada sin cambiar estructuras/valores anteriores. INSTALL/BOOTSTRAP siguen generando SCHEMA 3. PLAN_WATCHES migra explícitamente 3→4 y añade tipos `roster_plan`/`roster_gap`, referencia PLAN=10 y escalares ORDINARY=41, TEMPORARY=42 y STOP=43. No se reutiliza el significado de un campo antiguo ni se modifica el formato binario Core. El nuevo lector acepta 1/2/3/4; los lectores anteriores no aceptan 4. No hay migración inversa implícita.

Se prueban guardado/carga idénticos, continuidad temporal, diferentes procesos, rechazo atómico de corrupción de checksum y de vocabulario/semántica, protección de claves y separación de scopes tras cargar. Los archivos Miranda e Intrepid producidos por sus DLL anteriores se cargan y continúan con el lector nuevo, sin recompilar sus productores. Los fixtures históricos SCHEMA 1/2 siguen pasando. [Procedencia y compatibilidad](evidence/F04-SOVEREIGN-01/compatibility.json).

## Pruebas ejecutadas

| Suite | Resultado |
|---|---|
| F04 nativo MSVC Release | 136/136; 107 regresiones previas + 29 Sovereign |
| F02 / F03 | 15/15 y 25/25; fuentes comparadas con las de sus builds |
| Core completo con Content JSON | 447 superadas, 4 omitidas por plataforma, 0 fallos |
| Unreal 5.8.2 Win64 / NullRHI | Compilación real y 21/21 automatizaciones |
| Referencias documentales F04 / Miranda / F03 / F02 | 22 + 4 + 26 + 9 = 61 superadas |
| Fixture de autoridad F04 / roadmap | PASS / PASS |
| Validador global de referencias | FAIL: 566 incidencias idénticas en la base y esta rama |

Las cuatro omisiones Core no se cuentan como éxitos; sus nombres están en [resultados](evidence/F04-SOVEREIGN-01/test-results.json). El fallo global previo está conservado con su comparación y no se presenta como superado. Las pruebas documentales no sustituyen la ejecución nativa. NullRHI acredita integración lógica, UWorld, guardias, Actors selectivos y persistencia sin jugador; no una escena artística jugable completa. Se mantienen cero Actors automáticos de dotación; la prueba solo representa identidades solicitadas.

Los casos Sovereign comprueban estructura/subtotales, referencia exacta, 7/14/28 días, medianoche, mando y adjuntos, baja/vacaciones/suplencia, carencia real, plantilla parcial, descanso/deuda, urgencias, salida/reincorporación, traslado, cancelación, credenciales caducadas, persistencia/migración/corrupción, consultas paginadas, propuestas y autoridad, procesos distintos y rendimiento. [Evidencia y comandos](evidence/F04-SOVEREIGN-01/RESULTADOS.md).

## Rendimiento medido

MSI local, MSVC Release, Core real, sin 700 Actors. Medidas puntuales de pared, no garantía de latencia ni percentiles. Creación incluye población, instalación de 700 plazas y bootstrap explícito. Guardado incluye la consulta de tamaño y la serialización al buffer.

| Horizonte | Crear personas/plazas ms | Manifiesto ms | Plan ms | Cobertura ms | Guardar ms | Cargar ms | Avanzar reloj ms | Bytes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 131.48 | 0.41 | 9.87 | 0.54 | 20.70 | 16.80 | 6.80 | 567116 |
| 7 | 132.47 | 0.39 | 54.14 | 2.90 | 53.27 | 45.05 | 44.25 | 1476893 |
| 14 | 132.58 | 0.39 | 128.60 | 7.71 | 91.28 | 78.52 | 125.65 | 2563761 |
| 28 | 131.89 | 0.38 | 323.91 | 27.11 | 168.92 | 145.09 | 415.77 | 4671275 |

[Mediciones originales](evidence/F04-SOVEREIGN-01/performance.json). Se evita buscar todas las actividades de todas las personas repetidamente: índice descartable de tipos/persona y candidatos/obligaciones locales durante el plan. Las búsquedas de cobertura usan límites temporales relevantes. El corte admite hasta 28 días por llamada, 65536 entidades por archivo operativo y 64 MiB de carga. No hay compactación de historial ni promesa de calendario ilimitado; deben atenderse CAPACITY y el horizonte antes de agotarlos.

## Equipamiento e instalaciones configurables

Warp/impulso, energía, escudos, fáseres, torpedos fotónicos/cuánticos, sensores, informática, replicadores, transportadores, ciencia, medicina y hangares se referencian funcionalmente; sus cantidades y características pertenecen a la nave. No se copia tripulación, daños, matrícula, misiones ni modificaciones de Enterprise-E. No se instala Cousteau ni otro yate por defecto, no se fija número de lanzaderas ni de holocubiertas, no se crean civiles residentes.

El [contrato Sovereign](../../../../../../desarrollo/integration/f04/tests/fixtures/sovereign_facilities_contract.json) reutiliza literalmente el contrato mínimo de campos/reglas de Intrepid por referencia, con cantidad de instalaciones sin configurar y lista vacía. Jugadores y NPC usarán las mismas reglas y el mismo reloj cuando se implemente su ejecución. EMH es configurable, sin identidad de tripulante automática. No se implementan reservas, minijuegos, entrenamiento, XP ni escenarios 3D; esta entrega solo valida el contrato de datos.

## Decisiones pendientes y límites

La distribución definitiva por rangos sigue pendiente del autor. También quedan la aprobación del compromiso entre reserva de relevos/cupos no críticos y su posible optimización, la configuración individual de equipamiento e instalaciones, recuperación de deuda de descanso y planificación extraordinaria, y la interfaz de decisiones ante incidentes.

Los planes tienen horizonte finito y sin recurrencia implícita: debe autorizarse su ampliación antes del final. Al agotarlo, las consultas muestran ausencia de servicio/mando de guardia; no simulan una cobertura infinita. La detección y propuesta de suplencias están implementadas, su confirmación exige autoridad. La actividad futura se representa por estados/agendas, sin IA social avanzada, combate ni simulación automática de proyectos científicos de fases posteriores.

CoreRPG no se modifica. Solo se trabaja en integración/documentación F04 y el worktree autorizado. No se modifican modelos, puentes, texturas, mapas artísticos, materiales, Valhalla, respaldos TABULA RASA ni archivos ignorados de 3D; véase la comprobación de protección. No se fusiona ninguna rama ni se cierra F04.
