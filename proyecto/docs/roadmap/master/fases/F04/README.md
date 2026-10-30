# F04 — Naves, dotaciones, turnos y cadena de mando

## Plan operativo de cierre, 31-10-2026

- [F04-VALHALLA-01 — plantilla de 1.800 Flota, 400 civiles y 90 secciones, 550/380/255/615 en día de referencia](F04-VALHALLA-01_PLANTILLA_1800_Y_CIVILES_400.md). La dotación de Defiant (40 especialistas navales) y Marines Hijos de Odín (60 soldados, no pilotos) se cuenta dentro de los 1.800. Solo diseño por ahora.
- [Secuencia de cinco entregas para cerrar F04](PLAN_CIERRE_F04_2026-10-31.md): Valhalla, Guardia Miranda/Intrepid, Historial largo, Integración secciones/Defiant y Auditoría final. Cada subfase precisa PR Draft y auditoría independiente.
- Decisiones de autor vinculantes: [DEC-0017–0019](../../../decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md). F04 **EN_CURSO** hasta pruebas, auditoría y acta real.


**Actualización 2026-10-30: F04 EN_CURSO.**
[F04-MIRANDA-01 — Organización de la USS Sutherland](F04-MIRANDA-01_ORGANIZACION_USS_SUTHERLAND.md):
130 plazas, siete departamentos, 32 secciones y Alpha ilustrativa de 53 personas,
persistidas en CoreRPG. [Plantilla completa](F04-MIRANDA-01_PLANTILLA_130.md).
La fase permanece abierta; las notas de revisión siguientes son antecedentes.

**Auditoría y trabajo F04:** 2026-10-11; **actualización de dependencias:** 2026-10-13. **Estado en esta rama:** P01–P04 DOCUMENTADOS; P05 MATRIZ DE REFERENCIA PROBADA en CI, solo para reglas de referencia. **F04 global EN_REVISION**: F01–F03 ya fusionadas; **F04 PR #5 fusionada** y suite de 39 casos de fixture + 17 unit tests superada, pero Core/UE5 y validación operativa siguen pendientes. **Madurez objetivo:** `REFERENCIA_PROBADA` con límites expresos.

## Objetivo

Una nave existe con puestos reales, oficiales activos, guardias causales, autoridad derivada del destino y restricciones que no desaparecen por tener un rango alto.

## Entregables F04

| Paso | Trabajo | Evidencia de esta rama |
|---|---|---|
| F04-P01 | [Auditoría catálogo/clases, plazas y dotación](AUDITORIA_NAVES_DOTACIONES_P01.md) | Fuentes reales identificadas; generación runtime NO_EJECUTADA |
| F04-P02 | [Turnos, agendas, incompatibilidades, bajas y relevos](GUARDIAS_AGENDAS_P02.md) | Política temporal y ejemplos; arbitraje Core NO_EJECUTADO |
| F04-P03 | [Cadena de mando contextual y delegación](MANDO_NOMBRAMIENTOS_P03.md) | Matriz de cuatro roles y sucesión; API externa NO_APROBADA |
| F04-P04 | [Autoridad médica, profesional, Primera Directriz y normas](LIMITES_MEDICOS_NORMATIVOS_P04.md) | Límites y precedencia de ámbito; decisiones en Core NO_EJECUTADAS |
| F04-P05 | [Pruebas de aceptación, matriz y transferencia](VALIDACION_Y_TRASPASO_P05.md) | **39 escenarios + 17 tests** de referencia verificados en CI, sin runtime Core/UE5 |

## Caso de prueba adicional — Miranda-120 (13-10-2026)

Se documenta [el ejemplo Miranda de 120 tripulantes, 3×8 frente a 4×6 y francos 5+2](EJEMPLO_MIRANDA_120_TURNOS_Y_FRANCOS.md), con [fixture ilustrativo](../../../../../../desarrollo/validation/fixtures/f04/miranda_120_watch_5x2_example_v0.1.json) y [pruebas automatizadas](../../../../../../desarrollo/tools/validation/test_f04_miranda_example.py). **Es un ejercicio de cálculo semanal, no dotación Miranda canonizada ni régimen obligatorio de Flota.** Comprueba cobertura 24/7 de seis funciones y días francos sin duplicar NPC; **NO** prueba vacaciones, bajas simultáneas, cobertura sanitaria integral, equidad multisemanal ni integración con Core/UE5. No modifica el estado global F04 ni sustituye las 39 situaciones y 17 unit tests de referencia previas.

## Reutilización respetada

`sistemas/gameplay/chain_of_command/`, `sistemas/gameplay/duty_system/`, `sistemas/gameplay/ship_operations/`, `sistemas/gameplay/characters/`, `mundo/lore/federation/starfleet/`, `mundo/lore/starships/classes/`, `sistemas/universe/generation/` y `proyecto/docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md`. El plan previo **SB001–SB015 COMPLETE** solo significa cierre de contenido y generadores de referencia; no equivale a juego integrado.

## Límites de autoridad e integración

- Core RPG: verdad, entidades, agendas, mutaciones y persistencia, si la versión realmente las ofrece.
- Star Trek: clases, tripulación, puestos, guardias, restricciones de Flota y Primera Directriz.
- UE5: actores y escenas interactivos, no fuente independiente de World State; IA aconseja sin ejecutar.
- No mover contratos ni crear un Core paralelo. **DEC-0001 ya está resuelta**: Galaxy/Enterprise-D es la inspiración de la nueva **Clase Valhalla**, no un refit; su año de servicio sigue sin definirse. Este acuerdo creativo no acredita naves runtime ni afecta al puente de prueba de Sensores.
- **Reconciliación 2026-10-13:** F01–F04 [PR #2–#5](https://github.com/robdor80/Videojuego_StarTrek/pull/5) y F05/F06 PR #6/#7 están **fusionadas en `main`**. La [suite transversal F04→F05→F06](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38321712021) pasó **3/3 ejecutadas sin omisiones**. El estado oficial F04 queda **EN_REVISION**, aunque sus cinco entregables documentales/de referencia están cerrados a su nivel, porque siguen faltando Core/UE5 reales.
- `proyecto/docs/roadmap/master/ESTADO_GLOBAL.json` y plan maestro **ya reflejan** esta distinción entre referencia cerrada por paso y fase todavía en revisión.

**Condición para cierre real:** pruebas de matriz autorizativa y turnos integradas con Core versionado, restricciones negativas demostradas, conexión con guardia jugable y trazabilidad de la aceptación. No marcar `CERRADA` con documentación y Python únicamente.

[Plan maestro](../../PLAN_MAESTRO.md) · [Criterios comunes](../../CRITERIOS_DE_CIERRE.md) · [Dependencias Core](../../DEPENDENCIAS_CORE_RPG.md)


## Endurecimiento de auditoría — 2026-10-12

A-02: `issue_reference_binding` emite únicamente un **comprobante de referencia**
para F05 cuando `evaluate` responde ALLOW y coinciden `actor_id`,
`action_id`, `station_id`, `state_revision` y ventana temporal.
La identidad, revisión y tiempo deben proceder de una fuente confiable en la
integración real. Este diccionario **no es un token firmado ni un permiso Core**;
ni la UI ni una LLM pueden usarlo para autenticar una acción. La nueva prueba
negativa comprueba denegación, acción cruzada y caducidad imposible.

CI comprobada en el último código previo a este apunte:
[Actions 38228139402](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38228139402)
SUCCESS, 39 escenarios de fixture y **17 tests unitarios**. La fase global
permanece abierta; faltan Core/UE5 y pruebas transversales post-merge.

## F04-ODYSSEY-01 — Implementación para auditoría

[Organización y tres guardias](F04-ODYSSEY-01_ORGANIZACION_Y_TRES_GUARDIAS.md):
1.600 personas y plazas, siete departamentos, 72 secciones; día exacto
500 Alpha / 330 Beta / 205 Gamma / 565 fuera. Reutiliza el planificador de
Sovereign; [plantilla completa](F04-ODYSSEY-01_PLANTILLA_1600.md) y
[evidencias](evidence/F04-ODYSSEY-01/RESULTADOS.md). Odyssey operativa en 2383
como GAME_ADDITION, flujo cuántico experimental sin instalación automática.
F04 permanece EN_CURSO; Draft sin fusionar.

## F04-VALHALLA-01 — Nueva doctrina militar del Proyecto Defiant (2026-10-31)

**Separación de funciones sin excepciones por defecto:** solo la tripulación de Flota especializada gobierna y pilota la Defiant; los Marines Hijos de Odín se embarcan como fuerza de operaciones especiales y **NO desempeñan puestos navales ni pilotan la Valhalla o la Defiant**. El equivalente es submarino y equipo SEAL. No duplicar identidades, cualificaciones o puestos para darles funciones navales.

**El autor aprueba** [DEC-0017–0019](../../../../decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md): la Valhalla de 1.800 tripulantes de Flota + 400 civiles incluye una **Defiant de guerra furtiva con tripulación naval especializada** y el destacamento de Marines de Flota **«Hijos de Odín»**, explícitamente soldados, no personal de seguridad disfrazado. **60 Marines + 40 tripulantes especializados** es únicamente una **hipótesis cuantitativa** pendiente de ratificación al validar espacios, turnos y misión; forman parte de los 1.800 de Flota, no son personas adicionales.

**Contexto:** Federación exploradora y diplomática, pero con capacidad militar de disuasión y operaciones ofensivas bajo mandos, permisos y consecuencias reales. Integración F04-VALHALLA-01 todavía no implementada; no fabricar plantillas, rangos, dotaciones de Defiant ni misión en CoreRPG por esta sola actualización documental. F04 permanece **EN_CURSO**.
