# F05-P05 — Pruebas y traspaso a Core 4.10+
Fecha: 2026-10-11. **La suite prueba una puerta de decisión de referencia, NO la simulación de un Core.**

## Cobertura
- `tools/validation/f05_reference.py`: evaluador puro, sin fichero de estado, sin red, sin persistencia ni acceso mutador. `ALLOW_REFERENCE` quiere decir **podría elevarse a evaluación Core**, no `executed`.
- `validation/fixtures/f05/order_initiative_reference_v0.1.json`: **48 escenarios** con tres rutas NPC→NPC, NPC→jugador y jugador capitán→NPC, más restricciones de autoridad, conocimiento, aprobación, aptitud, delegación, guardia, recursos, idempotencia, demora y LLM.
- `tools/validation/test_f05_reference.py`: **16 pruebas unitarias** (fixture, cobertura, seguridad y compatibilidad de contratos).
- `.github/workflows/f05-reference-orders.yml`: Python 3.12, compilación, unittest y fixture; sin dependencias externas.

## Qué está probado, y qué no
**Probar aquí:** clasificación reproducible y negativa segura para propuestas de IA, cambio de revisión, delegado revocado, orden ilegal, falta de recurso, jugador ausente, replay e incapacidad médica. Se verifica explícitamente que el evaluador declara `effects_applied=0` y `authoritative=false` en todos los casos. Una aceptación es solo permiso candidato.

**NO probado:** WorldState real, reserva real de tiempo, creación/revocación/guardado de objetos, reconciliación de tick, proveedor remoto, UE5, integración 4.10, órdenes vistas por UI ni eventos append-only persistidos. No utilizar la suite como prueba de esas propiedades.

## Comandos
```bash
python -m py_compile tools/validation/f05_reference.py tools/validation/test_f05_reference.py
python -m unittest discover -s tools/validation -p 'test_f05_reference.py' -v
python tools/validation/f05_reference.py --fixture validation/fixtures/f05/order_initiative_reference_v0.1.json
```

## Camino crítico para integración real
| Puerta | Dueño | Criterio de aceptación | Estado |
| --- | --- | --- | --- |
| F01/F02/F03/F04 | Star Trek | Resolver aprobación y dependencias; fuente única de autoridad, identidad y conocimiento | PR #2–#5 todavía abiertos en fase documental |
| Core 4.7 | CoreRPG | Orden/delegación/resultado/eventos sobrevivir save/load; IDs y retries idénticos | NO_EJECUTADO |
| Core 4.9 | CoreRPG | Una proyección actor-relativa no revela objetivos ocultos | NO_EJECUTADO |
| Core 4.10 | CoreRPG y Star Trek | Acordar adaptador Action/Result/Event/Agenda; ejecutar rechazo atómico, reintento, revocación, NPC→NPC y jugador | NO_EJECUTADO |
| Core 4.12/IA | CoreRPG/Host | Contexto seguro, timeout/caducidad y no mutación desde LLM real | NO_EJECUTADO |
| UE5/F08 | Host Star Trek | Guardia de Sensores con mando NPC real, feedback y prueba save/load en MSI | NO_EJECUTADO |

No se publica `UniversalCommandSystem`, nombres de API ni ABI hipotéticos. Mantener `ESTADO_GLOBAL.json` intacto hasta cierre de dependencias; no declarar la F05 `CERRADA` en plan global.

## Evidencia y anomalías
**Ejecución observada: 2026-10-11.** [GitHub Actions run 38178262402](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38178262402), sobre commit `9dc73e1366190bd1ba7956f329b11fe87b4f6892`, terminó `completed/success`. Logs: sintaxis Python OK, **16/16** unittest (Ran 16 tests, OK), **48/48** escenarios (0 failures). PR de revisión: [#6](https://github.com/robdor80/Videojuego_StarTrek/pull/6). **Nivel acreditado limitado a `REFERENCIA_PROBADA` de la puerta de evaluación; `CORE_INTEGRADO`/UE5/E2E siguen `NO_EJECUTADO`.** El historial de 48 fixtures no implica 48 acciones ejecutadas en partida.
