# F11 — Carrera profesional y flota jugable

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
