# F09 — Resto de consolas y operaciones interconectadas

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO, REFERENCIA_PROBADA o UE5_JUGABLE según cada paso.

## Objetivo

Desarrollar gradualmente las 15 familias restantes, manteniendo Sensores como referencia.

## Pasos y entregables

- [ ] **F09-P01** — Priorizar Ciencia, CONN, Navegación y Operaciones con contratos operativos comprobables.
- [ ] **F09-P02** — Completar Ingeniería, Táctica, Seguridad y Comunicaciones, con fallos, recursos y alertas.
- [ ] **F09-P03** — Completar Mando, Misiones, Transportador, Médica, Ambiental, Hangar y Ordenador.
- [ ] **F09-P04** — Probar flujo interconsolas, permisos, transferencias y acciones compartidas bajo el Core.
- [ ] **F09-P05** — Validar situación de avería, combate, misión y orden multitarea con diferentes clases de nave.

## Material ya creado que no se mueve

- `sistemas/gameplay/ship_operations/consoles/`
- `sistemas/gameplay/ship_operations/interconsole/`
- `sistemas/gameplay/ship_operations/ship_computer/`
- `sistemas/gameplay/orders/`
- `audiovisual/ui/`

**Tratamiento:** reutilizar lo existente tras auditar el alcance y documentar brechas; no reescribir material original para que coincida con la numeración.

## Dependencias

F06 y F08 como patrón; F02–F05 para acciones y persistencia.

## Puerta de cierre

Pruebas ejecutables por estación y operación integrada; el catálogo de 16 familias no acredita operación completa. Deben quedar registrados las pruebas realizadas, evidencias, commit/PR y decisiones de autor. Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).

## Preparación paralela F09 · 13-10-2026 (NO jugable)

Se ha iniciado, con autorización del autor, el trabajo autónomo **P01–P05 a nivel de referencia**: [inventario, prioridades, contratos, pruebas y bloqueos](PREPARACION_P01_P05_REFERENCIA.md). [Matriz de las 16 familias](../../../../../../sistemas/gameplay/ship_operations/consoles/f09_reference_matrix_v0.1.json), [verificador puro de datos](../../../../../../desarrollo/tools/validation/f09_interconsole_reference.py) y [tests](../../../../../../desarrollo/tools/validation/test_f09_interconsole_reference.py). La CI de referencia verifica la estructura y casos negativos, **no** un puente UE5 ni acciones Core. F02 sigue siendo la única fase global EN_CURSO; F09 no adquiere estado CERRADA ni UE5_JUGABLE por esta preparación.
