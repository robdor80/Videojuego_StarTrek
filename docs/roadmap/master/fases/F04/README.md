# F04 — Naves, dotaciones, turnos y cadena de mando

**Auditoría y trabajo F04:** 2026-10-11. **Estado en esta rama:** P01–P04 DOCUMENTADOS; P05 MATRIZ DE REFERENCIA IMPLEMENTADA, su nivel de evidencia depende de CI. **F04 global no cerrada**: F01–F03 y Core/UE5 siguen pendientes de integración. **Madurez objetivo:** `REFERENCIA_PROBADA` con límites expresos.

## Objetivo

Una nave existe con puestos reales, oficiales activos, guardias causales, autoridad derivada del destino y restricciones que no desaparecen por tener un rango alto.

## Entregables F04

| Paso | Trabajo | Evidencia de esta rama |
|---|---|---|
| F04-P01 | [Auditoría catálogo/clases, plazas y dotación](AUDITORIA_NAVES_DOTACIONES_P01.md) | Fuentes reales identificadas; generación runtime NO_EJECUTADA |
| F04-P02 | [Turnos, agendas, incompatibilidades, bajas y relevos](GUARDIAS_AGENDAS_P02.md) | Política temporal y ejemplos; arbitraje Core NO_EJECUTADO |
| F04-P03 | [Cadena de mando contextual y delegación](MANDO_NOMBRAMIENTOS_P03.md) | Matriz de cuatro roles y sucesión; API externa NO_APROBADA |
| F04-P04 | [Autoridad médica, profesional, Primera Directriz y normas](LIMITES_MEDICOS_NORMATIVOS_P04.md) | Límites y precedencia de ámbito; decisiones en Core NO_EJECUTADAS |
| F04-P05 | [Pruebas de aceptación, matriz y transferencia](VALIDACION_Y_TRASPASO_P05.md) | 38 escenarios + 16 tests independientes; CI añadida, comprobar workflow |

## Reutilización respetada

`gameplay/chain_of_command/`, `gameplay/duty_system/`, `gameplay/ship_operations/`, `gameplay/characters/`, `lore/federation/starfleet/`, `lore/starships/classes/`, `universe/generation/` y `docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md`. El plan previo **SB001–SB015 COMPLETE** solo significa cierre de contenido y generadores de referencia; no equivale a juego integrado.

## Límites de autoridad e integración

- Core RPG: verdad, entidades, agendas, mutaciones y persistencia, si la versión realmente las ofrece.
- Star Trek: clases, tripulación, puestos, guardias, restricciones de Flota y Primera Directriz.
- UE5: actores y escenas interactivos, no fuente independiente de World State; IA aconseja sin ejecutar.
- No mover contratos, no crear Core paralelo y no fijar la Dama de Imperator sin DEC-0001.
- F01 [PR #2](https://github.com/robdor80/Videojuego_StarTrek/pull/2), F02 [PR #3](https://github.com/robdor80/Videojuego_StarTrek/pull/3), F03 [PR #4](https://github.com/robdor80/Videojuego_StarTrek/pull/4) siguen abiertas: la rama F04 deriva de `main@6069f6aa` de forma independiente, sin esconder estas dependencias.
- `docs/roadmap/master/ESTADO_GLOBAL.json` y plan maestro no se alteran para no falsear el estado principal.

**Condición para cierre real:** pruebas de matriz autorizativa y turnos integradas con Core versionado, restricciones negativas demostradas, conexión con guardia jugable y trazabilidad de la aceptación. No marcar `CERRADA` con documentación y Python únicamente.

[Plan maestro](../../PLAN_MAESTRO.md) · [Criterios comunes](../../CRITERIOS_DE_CIERRE.md) · [Dependencias Core](../../DEPENDENCIAS_CORE_RPG.md)
