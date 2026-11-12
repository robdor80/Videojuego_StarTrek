# P2-B09 — Acta de cierre de referencia (12/11/2026)

**Fase:** Planificación 2, Bloque 9/10. **Objetivo:** `REFERENCE_COMPLETE` de contratos y demostración offline. **Estado administrativo:** PR [#120](https://github.com/robdor80/Videojuego_StarTrek/pull/120), pendiente de CI del HEAD documental definitivo y fusión. **No equivale a misiones operativas en CoreRPG, HOST ni Unreal Engine.**

## Auditoría de las dependencias

- B01–B03: civilizaciones, colonización y conflicto; B04: recursos, demanda, tráfico y rutas; B05: hechos e historia; B06: investigación; B07: anomalías y arqueología; B08: crisis y proyecciones. Todos cerrados a nivel de referencia.
- B08 PR #118 fue fusionada en `main` (`bffa7be364cd7e06a1b6c50b823dcb89d7e95cc9`) y el cierre documental posterior habilitó el inicio B09.
- Existe una prueba F13 anterior de necesidad→misión candidata. Se conserva sin reescribir la autoridad de F13 ni el código de referencia. B09 añade el ciclo de propuesta, orden, reserva y cierre externo.
- F11 y HOST siguen como dueños de autorización real de mando/sesión; CoreRPG debe aceptar y autenticar hechos y escribir WorldState. B10 será responsable del scheduler galáctico y arbitraje offscreen.
- Respeto a `AGENTS.md`: sólo archivos de referencia y validación definitivos; no se añaden laboratorios, texturas, assets ni pruebas temporales al repo.

## Paquetes y archivos

Los 20 paquetes EM001–EM020 constan en:
- `proyecto/docs/roadmap/procedural_emergent_missions_plan_v0.1.md`
- `proyecto/docs/roadmap/procedural_emergent_missions_status_v0.1.json`
- `sistemas/universe/generation/emergent_missions_worldstate_reference_contract_v0.1.json`
- `desarrollo/tools/generation/simulate_emergent_missions.py`
- `desarrollo/tools/generation/test_simulate_emergent_missions.py`
- `desarrollo/validation/fixtures/emergent_missions/verified_unmet_need_npc_response_v0.1.json`
- `.github/workflows/p2-b09-emergent-missions.yml`

## Resultado de escenario, limitado a datos sintéticos

Dos consecuencias `accepted` en un fixture no canónico preceden dos necesidades; una agencia NPC conoce ambas. Una necesidad médica es atendida por un recurso NPC existente mediante propuesta, órdenes independientes, reserva externa y comprobación de informe/resultado. La necesidad se resuelve en la simulación de referencia; el jugador no es requisito. Un capitán recibe una noticia sobre ese asunto **después** de resolverse y no puede resucitar la misión por escucharla. Un observador no autorizado no recibe información secreta.

El segundo expediente afecta a un mundo prewarp: puede identificarse como candidato pero queda bloqueada su autorización sin una excepción explícita y aprobada de Primera Directriz. La existencia de hechos aceptados en este fixture **no verifica hechos de juego firmados**.

## Pruebas y puertas

- **65/65 casos adversariales ejecutados y superados**: hechos no aceptados, origen independiente, confidencialidad, rutas/recursos, Primera Directriz, órdenes/reservas, cierre, replay, timeouts y atomicidad.
- Regresiones ejecutadas B01–B09: **329/329 pruebas de simuladores** (264 B01–B08 + 65 B09); **30/30 F13** y **9/9 Academia** superadas.
- Auditorías F13 y Academia: se actualizan sólo las expectativas de frontera 9→10 al quedar B09 en estado de referencia. F13 global sigue `PLANIFICADA`; capas 119/120 sin promoción.
- **Puerta final:** CI de HEAD de PR, comprobaciones transversales, cambios acotados, sin archivos temporales ni intervención en ramas ajenas; después, fusión autorizada en `main`. Evidencia inicial completa: [Actions #43266460616](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43266460616), HEAD `878951af8f18ad9dedae99be2db0cda5a8c0aa46`: 65/65 B09, 329/329 B01–B09, 30/30 F13 y 9/9 Academia; **20/20 workflows SUCCESS** del mismo HEAD. Esta validación es anterior a las últimas actualizaciones de acta y manifiesto; se exigirá nuevo CI verde del HEAD documental definitivo.

## Fuera de alcance

No hay motor de generación de necesidades real, WorldState auténtico, órdenes F11/HOST validadas, contratación/consumo de combustible, comercio real, reservas transaccionales, despachos NPC galácticos en segundo plano, economía o daños mutados, recompensas, misiones UE5, mapas ni PADD funcional. Ninguna misión creada por crisis proyectada o por presencia del jugador; no se altera la temporada narrativa ni los hechos canónicos.

**Decisión condicional de cierre:** con pruebas verificadas y PR fusionada, B09 = `REFERENCE_COMPLETE` y **B10 — Evolución galáctica en segundo plano** es el siguiente bloque elegible. De lo contrario, mantener la puerta pendiente y consignar fallos.
