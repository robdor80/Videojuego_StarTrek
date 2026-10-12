# F01 — Visión del producto y canon

**Estado global:** EN_CURSO (pendiente de revisión y cierre formal de fase). **Revisión:** 2026-10-13. **Madurez actual:** `DISENO_VALIDADO` en P01/P02/P04; P03 decisión creativa resuelta y en revisión; P05 traza ampliada, pendiente QA/cierre de PR.

## Objetivo

Consolidar la visión del videojuego 3D para PC, verificar épocas/canon y cerrar el primer corte de alcance, **sin trasladar contratos originales ni inventar decisiones creativas**. F00 está cerrada por PR #1, commit `0f989948`.

## Pasos y evidencias

- [x] **F01-P01 — Visión 3D MSI, carrera libre, universo autónomo.** [Visión de producto](../../../../vision/VISION_PRODUCTO_RPG_3D_v0.1.md). Se reconcilian los acuerdos existentes y se declaran exclusiones; decisión original mantenida.
- [x] **F01-P02 — Auditoría de épocas y canon.** [Auditoría de canon](AUDITORIA_EPOCAS_Y_CANON.md). Confirmadas tres épocas; continuidad emergente; extension Sovereign explícita y precaución Odyssey.
- [ ] **F01-P03 — Nueva Clase Valhalla.** [Análisis de Damas y elección](ANALISIS_DAMAS_IMPERATOR.md) + [acta autoral](ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md). `DEC-0001 APROBADA`: **Galaxy** como referencia; **Valhalla** clase nueva, rediseño exterior reconocible. Decisión documentada; paso pendiente de QA y formalización de cierre, no de autor.
- [x] **F01-P04 — Primer corte técnico y presupuesto medible.** [Contrato aprobado de prototipo de Sensores](PROPUESTA_MVP_Y_PRESUPUESTO.md) y [política de prototipos internos](../../../../decisions/prototype_validation_and_release_policy.md). `DEC-0002 APROBADA`: v0.0.1 interna, solo guardia de Sensores; criterios funcionales fijados; métricas de rendimiento cuantitativas se instrumentarán y validarán en F07/F08, sin inventarlas.
- [ ] **F01-P05 — Catálogo de decisiones y fuentes.** [Registro de decisiones](REGISTRO_DECISIONES_Y_TRAZABILIDAD.md). `DEC-0001/0002` registradas y acta Valhalla disponible; validar consistencia documental y la PR antes del cierre.

## Reutilización exacta

- `docs/decisions/`, `sources/canon_policy.md`, `sources/provenance_policy.md` — fuentes y decisiones existentes.
- `CONTENT_STATUS.md` — editorial sin modificaciones de estado.
- `lore/starships/classes/core_starship_classes.json` y `core_catalog.md` — clases ya aprobadas para fecha.
- `docs/roadmap/game_design_readiness_v0_2.md` — objetivos y fronteras.
- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md` — primer bucle jugable orientativo.
- `gameplay/careers/academy_path/` y `gameplay/careers/starfleet_service/` — formación/carrera, sin duplicación.
- `assets/ships/starfleet/galaxy_class/enterprise_d/` — referencia de arte, no prueba de puente 3D jugable.

## Pruebas y límites del avance

**HECHO:** revisión documental de los archivos enlazados, reconciliación de criterios, inventario de decisiones; los cinco entregables son inspeccionables en rama/PR.

**NO_EJECUTADO:** pruebas de Core RPG, compilación o sesión UE5, pruebas de rendimiento en MSI o licencia/importación de mallas. Es trabajo de visión, no runtime.

**Decisión creativa resuelta:** `DEC-0001` = **Galaxy → nueva Clase Valhalla**, y `DEC-0002` = prototipo interno Sensores. `DEC-0003` (puente piloto/licencias) se decidirá técnicamente en F07, sin imponer que sea de la Valhalla. **Pendiente real:** QA de documentos/estado y validaciones de gobierno necesarias para el cierre formal de F01; la fusión de la PR #2 es un paso independiente y no acredita runtime. No declarar F01 cerrada hasta registrar su cierre. La fecha de entrada en servicio de Valhalla se mantiene abierta expresamente.

Consúltese [PLAN_MAESTRO](../../PLAN_MAESTRO.md), [DECISIONES_Y_RIESGOS](../../DECISIONES_Y_RIESGOS.md), [CRITERIOS_DE_CIERRE](../../CRITERIOS_DE_CIERRE.md) y [ESTADO_GLOBAL.json](../../ESTADO_GLOBAL.json).
