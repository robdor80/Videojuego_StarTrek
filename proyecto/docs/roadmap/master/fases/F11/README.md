# F11 — Carrera profesional y flota jugable

> **Actualización autoral 11-11-2026:** el objetivo narrativo aprobado es capitanear la **USS Enterprise NCC-1701-D modernizada**, con oportunidades de progresión garantizadas de forma creíble y sin vacantes arbitrarias. El alcance de P01–P05 se ha actualizado en [PLAN_F11_ACTUALIZADO_2026-11-11.md](PLAN_F11_ACTUALIZADO_2026-11-11.md). La P01 actual dispone de [reglamento y casos](F11-P01_JERARQUIA_CADENA_MANDO_V1.md), contrato y pruebas offline, **sin integración jugable**. Las afirmaciones sobre «nueva clase Valhalla» y los pasos de octubre que aparecen más abajo se conservan como **histórico**, no como la decisión creativa vigente. El Plan Maestro y el estado global aún requieren reconciliación específica y no se cambian para simular un cierre.

> **F11-P02 — trabajo de referencia 11-11-2026:** [Diseño de destinos, 7 áreas de F04, perfiles de puesto y vacantes](F11-P02_DESTINOS_DEPARTAMENTOS_PUESTOS_V1.md). Incluye catálogo y evaluador Python independiente con pruebas automatizadas; **no hay plazas, destinos ni ofertas efectivas en CoreRPG/UE5**. No se da por integrada la progresión garantizada de P03/P04 ni se altera el estado global de F11.

> **F11-P03 — preparación de progresión (11-11-2026):** [Reglamento de evaluaciones, ascensos y oportunidades garantizadas](F11-P03_EVALUACIONES_ASCENSOS_Y_OPORTUNIDADES_V1.md). Contrato de meses ficticios **solo ilustrativos**, planificador offline no mutador, control de evaluaciones, sanciones, formación, preferencias, planes idempotentes y escalado cuando vence el horizonte. **No se han implementado todavía ascensos reales, vacantes de NPC ni integración en CoreRPG/UE5; la carrera garantizada integral depende de P04/P05.**

> **F11-P04 — sucesiones causales de NPC (11-11-2026):** [Modelo de carreras de NPC, jefaturas, primer oficial y capitanía de la Enterprise-D](F11-P04_TRAYECTORIAS_NPC_Y_SUCESIONES_CAUSALES_V1.md). Incluye contrato y director Python **offline** de opciones creíbles, motivación del NPC, aceptación/rechazo, órdenes, salida y comprobación efectiva de vacante; no borra NPC ni asciende automáticamente al jugador. **NO integra CoreRPG/UE5: la garantía jugable y la persistencia son P05.**

> **F11-P05-A01 — auditoría del código (11-11-2026):** [Inventario de capacidades reales F04/F05/CoreRPG, riesgos de integración y primer corte A02](F11-P05-A01_AUDITORIA_INTEGRACION_CORE_2026-11-11.md). A01 identifica como bloqueos el ascenso autoritativo, la autorización de Personal de Flota, la identidad inter-naves y la diferencia entre guardia descubierta y plaza libre. **Solo auditoría estática; no se ha implementado ni ejecutado aún P05.**

> **F11-P05-A02-00 — contrato profesional (11-11-2026):** [Identidad de carrera, rangos 1101–1106 y autoridad de Personal de Flota](F11-P05-A02-00_CONTRATO_IDENTIDAD_RANGOS_AUTORIDAD_2026-11-11.md). Base contractual conservada como histórico de diseño.

> **F11-P05-A02-01 — primer ascenso nativo (11-11-2026):** [PR #106 fusionada](https://github.com/robdor80/Videojuego_StarTrek/pull/106). Ascenso autoritativo **1101→1102**, expediente Core, persistencia e idempotencia; [reauditoría histórica](../../../../../../desarrollo/integration/f11/REAUDIT.md) y CI Linux/MSVC satisfactorias. **No** implica emisor institucional de producto, UE5 jugable ni la carrera completa.

> **F11-P05-A02-02 — certificación de persistencia y compatibilidad (11-11-2026):** [Informe de alcance, matriz G1–G10 y nueva CI independiente](F11-P05-A02-02_CERTIFICACION_PERSISTENCIA_COMPATIBILIDAD_2026-11-11.md). Verifica integridad del árbol ya auditado y vuelve a ejecutar las regresiones sobre Linux/MSVC. **No cerrar A02-02 hasta que la PR de certificación y todos sus checks concluyan satisfactoriamente.**

> **Decisión narrativa aprobada de ascensos diegéticos (11-11-2026):** [Acta permanente de comunicaciones, encuentros con superiores, ceremonias y presentación profesional diferida](../../../../decisions/f11_p05_ascensos_diegeticos_presentacion_narrativa_2026-11-11.md). [Issue abierta #104](https://github.com/robdor80/Videojuego_StarTrek/issues/104): A02-01 aporta evento Core estable, P05-C garantiza cola/acuse persistente y P05-D implementa experiencia jugable. **No se ha implementado todavía la interfaz ni las ceremonias**. No cerrar F11 sin P05-D/E verificadas.

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

La carrera surge de méritos, cualificaciones y destinos opcionales; llegar a capitanear una nave de **Clase Valhalla** nunca es final forzoso. «Imperator» fue un nombre provisional ya descartado.

## Pasos y entregables

- [ ] **F11-P01** — Revisar rutas científica, táctica/operativa y exploración/mando, con clases disponibles según época.
- [ ] **F11-P02** — Modelar primer destino de alférez y autonomía progresiva sin asignar capitanía automáticamente.
- [ ] **F11-P03** — Probar evaluaciones, expediente, ascensos, renuncias, traslado, mando temporal y efectos sociales.
- [ ] **F11-P04** — Programar escalera de clases y prioridades de modelado 3D; Galaxy/Sovereign/Odyssey como clases existentes/referencias y **Valhalla como nueva clase original inspirada en Galaxy**, todavía sin fecha de entrada en servicio.
- [ ] **F11-P05** — Validar permanencia en una nave, cambio de puesto o especialidad y acceso eventual al mando de una Valhalla, sin premiar automáticamente al jugador.

## Material ya creado que no se mueve

- `sistemas/gameplay/careers/`
- `sistemas/gameplay/chain_of_command/`
- `mundo/lore/starships/classes/`
- `proyecto/docs/decisions/`
- `sistemas/gameplay/characters/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F04–F05, F10; F01 para **decisión de Dama ya aprobada**. La fecha de disponibilidad Valhalla y su integración jugable siguen pendientes; véase [acta F01](../F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md).

## Puerta de cierre

Recorridos de carrera persistentes con alternativas reales, sin ascenso forzoso ni recompensa automática. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).

## Avance autónomo de referencia — 14-10-2026

Se ha implementado una **preparación verificable P01–P05**, con código de cribado de destinos y peticiones profesionales, un catálogo de rutas y prioridades por clase/época y una batería automatizada de **40 escenarios y 36 pruebas unitarias**. Véase la [auditoría y acta F11](ACTA_P01_P05_REFERENCIA_2026-10-14.md).

- Reglas: `sistemas/gameplay/careers/starfleet_service/f11_route_plan_v0.1.json`.
- Ejecutor sin autoridad: `desarrollo/tools/validation/f11_career_reference.py`.
- Evidencias offline: `desarrollo/validation/fixtures/f11/f11_career_scenarios_v0.1.json`.
- Pruebas: `desarrollo/tools/validation/test_f11_career_reference.py`, workflow `.github/workflows/f11-career-reference.yml`.

**Alcance del avance:** REFERENCIA_PROBADA si la CI final del HEAD es verde; jamás concesión real de rango, vacante, mando, acceso a la Valhalla ni partida UE5. Se mantiene sin cambios el estado maestro `PLANIFICADA` y los pasos oficiales sin marcar hasta validación CoreRPG/Host/UE5 y prueba presencial en MSI. La secuencia de la Fase 10 tiene igualmente bloqueos jugables pendientes.
