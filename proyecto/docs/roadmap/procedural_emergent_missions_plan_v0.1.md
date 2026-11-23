# Planificación 2 — Bloque 9: Misiones emergentes derivadas del estado del universo

**Fecha:** 12/11/2026 · **Madurez objetivo:** `REFERENCE_COMPLETE` · **Alcance:** contrato Trek, evaluador Python offline, fixture ficticio, pruebas adversariales, CI y puertas de integración. **No se implementa runtime CoreRPG, HOST, UE5 ni B10.**

## Visión jugable

El universo no necesita a la Enterprise-D. Las colonias, hospitales, civiles, estaciones, naves de la Flota y gobiernos tienen necesidades que nacen de consecuencias previamente aceptadas. Una escasez de material médico **real**, acreditada por la economía B04 y su causa, puede llevar a solicitar transporte, especialistas o escolta. Una proyección de peligro de B08 por sí sola **no** implica ni escasez ni misión. La Academia, una Miranda, otra nave NPC o un organismo civil pueden resolver un problema antes de que el capitán jugador conozca su existencia.

El resultado deseado es un **mercado causal y persistente de oportunidades**, no una lista de misiones que se genera por proximidad, misión de temporada, nivel del jugador o necesidad de espectáculo. La experiencia de mando incluye decidir no intervenir, delegar o recibir sólo un informe tardío; ello no bloquea automáticamente la respuesta institucional.

## Auditoría: respetar lo construido

- B01/B02: población, derechos, instituciones, asentamientos, soberanía, jurisdicción y hechos locales.
- B03: guerra y decisiones militares; una misión B09 jamás declara guerra, decide bajas o desplaza tropas.
- B04: stocks, compras, producción, costes, rutas, transporte y reservas **reales**; B09 no escribe inventarios.
- B05: hechos históricos y consecuencias persistentes; la resolución tiene procedencia, no borra una crisis pasada.
- B06: habilidades científicas y tecnologías certificadas; una misión no desbloquea invenciones.
- B07: anomalías, ruinas, custodia, permisos y conocimiento; no nacen anomalías para dar exploración.
- B08: riesgos y crisis sistémicas; un valor de presión no es una necesidad aceptada y B08 no ofrece misiones.
- F13 ya contiene `derive_mission_candidate` con una validación mínima de necesidad/capacidad; B09 conserva esa frontera y la desarrolla **sin reemplazar su código ni atribuirle autoridad real**.
- `sistemas/narrative/` y temporadas son diseño narrativo; la temporada no controla el reloj ni inventa necesidades sistémicas.
- F11/HOST: autenticación, órdenes, jerarquía y sesiones; CoreRPG: único escritor WorldState; B10: scheduler/offscreen. UE5/NAP/PADD sólo proyectarán información ya autorizada.

## Veinte paquetes EM001–EM020

| Paquete | Entrega |
|---|---|
| EM001 | Necesidad real y no cubierta como origen obligatorio |
| EM002 | Hecho causal aceptado y anterior a la necesidad |
| EM003 | Proyecciones B08 insuficientes para generar misión |
| EM004 | Campaña, corte temporal y hechos no futuros |
| EM005 | Identidad estable por necesidad y recurso; sin reroll |
| EM006 | Conocimiento entregado, confidencialidad y noticias tardías |
| EM007 | Capacidad y disponibilidad de medios existentes |
| EM008 | Rutas y destinos existentes; sin teletransporte por guion |
| EM009 | Jurisdicción, Primera Directriz y excepción prewarp |
| EM010 | Órdenes independientes del proponente, alcance concreto |
| EM011 | Reserva externa real, sin duplicación de medios |
| EM012 | NPC y agencias capaces de completar sin jugador |
| EM013 | No centrar el universo en la Enterprise-D |
| EM014 | Ciclo propuesta → autorización → asignación → verificación/cancelación |
| EM015 | Resultado y resolución acreditados fuera de B09 |
| EM016 | Oportunidades caducas y competencia no se reofrecen automáticamente |
| EM017 | No alterar recursos, población, política, daños o recompensas |
| EM018 | Replay determinista, rechazo atómico, colisiones e idempotencia |
| EM019 | Fixture no canónico, pruebas adversariales y CI transversal |
| EM020 | Acta, manifiesto, cierre de referencia y puerta B10 |

## Ciclo contractual

1. **Hecho y necesidad:** un sistema propietario admite una consecuencia; otro registra una necesidad `accepted` y vincula causa, tiempo, jurisdicción, ruta, capacidades y confidencialidad. Los `accepted` del fixture no son comprobantes CoreRPG.
2. **Descubrimiento:** sólo actores autorizados que recibieron la noticia o conocen legítimamente esa necesidad pueden proponer. El jugador no altera el nacimiento de la necesidad. Los mensajes tienen fecha de envío y llegada.
3. **Evaluación:** un par necesidad–recurso disponible produce `CANDIDATE` o `NO_MISSION`. No hay misión sin causa, ni transporte a rutas inexistentes, ni recursos creados porque faltan.
4. **Propuesta:** genera identificador de expediente `p2b09:<campaña>:<necesidad>:<recurso>`; nada se reserva, consume o ejecuta.
5. **Autorización:** exige una orden externa aceptada para ese expediente, proponente, jurisdicción y alcance, aprobada por emisor independiente. En cultura prewarp debe existir además revisión explícita aprobada de excepción a la Primera Directriz; no basta con «emergencia».
6. **Asignación:** otra orden más una reserva externa aceptada y medios disponibles; impide asignar dos veces el mismo recurso en el expediente de referencia. El bloqueo definitivo multiagente corresponde al sistema transaccional CoreRPG.
7. **Resultado:** misión `completed` sólo con informe de resultado verificado **y** hecho de necesidad resuelta aceptado; cancelar requiere decisión externa. Si otro NPC resuelve la necesidad, no se crea nueva misión por la llegada tardía de una notificación.
8. **Memoria e historia:** conservar expediente y cronología; no reescribir pasado ni retroceder reloj, y tampoco usar temporadas como fuente de autoridad.

## Fixture de prueba, expresamente no canónico

Campaña ficticia `demo-2383`: hay dos consecuencias acreditadas *en datos sintéticos*, una necesidad sanitaria en Lyra y una necesidad de observación junto a una cultura prewarp. Una agencia NPC informa a un capitán con retraso y envía una nave médica existente. La autoridad independiente acepta órdenes y una reserva, un informe externo certifica atención sanitaria y resolución. La nave médica completa la misión **sin que intervenga el jugador**. La segunda necesidad sólo llega a `proposed`; la autorización sin excepción de Primera Directriz fracasa. Un observador sin entrega no recibe información secreta. El capitán recibe una noticia que ya ha quedado obsoleta, sin que la llegada tardía reabra la necesidad.

Los escenarios comprueban hechos futuros, causa inexistente/no aceptada, campañas ajenas, conocimiento y rango insuficientes, rutas cerradas, capacidad insuficiente, medios ocupados, duplicaciones, permisos, exenciones prewarp, resultados falsos, noticias clasificadas, hash manipulado, reloj retroactivo y generación provocada por el jugador.

## Entregas y definición de cierre

- `sistemas/universe/generation/emergent_missions_worldstate_reference_contract_v0.1.json`
- `desarrollo/tools/generation/simulate_emergent_missions.py`
- `desarrollo/tools/generation/test_simulate_emergent_missions.py`
- `desarrollo/validation/fixtures/emergent_missions/verified_unmet_need_npc_response_v0.1.json`
- `.github/workflows/p2-b09-emergent-missions.yml`
- Plan, manifiesto, acta, índice y auditorías F13/Academia reajustadas a nueva frontera.

`REFERENCE_COMPLETE` requiere pruebas B09, regresiones B01–B09 y F13, contrato/JSON válidos, CI final del HEAD y PR fusionada. El estado global F13 sigue `PLANIFICADA`; capas 119/120 conservan sus bloqueos. **La siguiente fase independiente será B10 — Evolución galáctica en segundo plano**, que dará calendario y arbitraje offscreen a la simulación, nunca autoridad de escribir WorldState fuera de CoreRPG. No añadir laboratorios ni binarios temporales al historial de Git; aplicar `AGENTS.md`.
