# F06 — Consola de Sensores

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** CONTRATO_VALIDADO o INTEGRACION_PROBADA según cada paso.

## Objetivo

Completar funcionalmente el puesto piloto y sus vínculos con Ciencia, informes y órdenes.

## Pasos y entregables

- [ ] **F06-P01** — Revisar árbol de Sensores, diez ramas, manual y alcance funcional de v0.1.
- [ ] **F06-P02** — Validar detección relativa al observador, firmas, barridos, resultados parciales y conocimiento.
- [ ] **F06-P03** — Conectar transferencias Sensores→Ciencia, memoria de nave y registro de operaciones.
- [ ] **F06-P04** — Mapear cada operación a órdenes, recursos, puesto, criterios de fallo, disponibilidad y demora.
- [ ] **F06-P05** — Ejecutar pruebas de consola independientes de la presentación gráfica y fijar interfaz para UE5.

## Material del repositorio que se aprovecha sin moverlo

- `gameplay/ship_operations/consoles/sensors/`
- `gameplay/ship_operations/sensor_resolution/`
- `gameplay/ship_operations/interconsole/`
- `gameplay/ship_operations/ship_memory/`
- `docs/manuals/sensors/`
- `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F03–F05 para ejecución integral; base documental y pruebas de referencia preexistentes.

## Puerta de cierre

Operaciones reales probadas y resultados observables; un árbol de menús documentado no basta. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
