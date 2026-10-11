# F04 — Naves, dotaciones, turnos y cadena de mando

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO o INTEGRACION_PROBADA según cada paso.

## Objetivo

Una nave existe con puestos reales, oficiales activos y autoridad dependiente del destino.

## Pasos y entregables

- [ ] **F04-P01** — Auditar catálogo de clases/configuración, necesidades de puestos y dotación generada.
- [ ] **F04-P02** — Conciliar guardias, agendas, bajas, cualificación y exclusividad temporal del personal.
- [ ] **F04-P03** — Precisar cadena de mando por puesto real, nombramiento, delegación y sustituciones.
- [ ] **F04-P04** — Integrar autoridad médica/profesional, órdenes superiores, Primera Directriz y límites técnicos.
- [ ] **F04-P05** — Crear casos de aceptación para jugador alférez, responsable de departamento, oficial de guardia y capitán.

## Material del repositorio que se aprovecha sin moverlo

- `gameplay/chain_of_command/`
- `gameplay/duty_system/`
- `gameplay/ship_operations/`
- `gameplay/characters/`
- `lore/federation/starfleet/`
- `docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F03 y F02; reglas Star Trek son propias, runtime genérico en Core RPG.

## Puerta de cierre

Matriz autorizativa probada, puestos y guardias sin ocupación simultánea imposible ni permisos por mero rango. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
