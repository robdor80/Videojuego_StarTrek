# F01 — Visión del producto y canon

**Estado global:** **CERRADA a nivel de diseño**, revisión y [acta de cierre documental](ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md) de 2026-10-13. **Madurez real:** `DISENO_VALIDADO` para P01–P05; no supone integración Core/UE5, fecha de servicio Valhalla ni puente piloto elegido.

## Objetivo

Consolidar la visión del videojuego 3D para PC, verificar épocas/canon y cerrar el primer corte de alcance, **sin trasladar contratos originales ni inventar decisiones creativas**. F00 está cerrada por PR #1, commit `0f989948`.

## Pasos y evidencias

- [x] **F01-P01 — Visión 3D MSI, carrera libre, universo autónomo.** [Visión de producto](../../../../vision/VISION_PRODUCTO_RPG_3D_v0.1.md). Se reconcilian los acuerdos existentes y se declaran exclusiones; decisión original mantenida.
- [x] **F01-P02 — Auditoría de épocas y canon.** [Auditoría de canon](AUDITORIA_EPOCAS_Y_CANON.md). Confirmadas tres épocas; continuidad emergente; extension Sovereign explícita y precaución Odyssey.
- [x] **F01-P03 — Nueva Clase Valhalla.** [Análisis de Damas y elección](ANALISIS_DAMAS_IMPERATOR.md) + [acta autoral](ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md). `DEC-0001 APROBADA`: **Galaxy** como referencia; **Valhalla** clase nueva, rediseño exterior reconocible. Decisión, fuentes y límites comprobados en el acta de cierre de diseño; modelos y jugabilidad corresponden a fases posteriores.
- [x] **F01-P04 — Primer corte técnico y presupuesto medible.** [Contrato aprobado de prototipo de Sensores](PROPUESTA_MVP_Y_PRESUPUESTO.md) y [política de prototipos internos](../../../../decisions/prototype_validation_and_release_policy.md). `DEC-0002 APROBADA`: v0.0.1 interna, solo guardia de Sensores; criterios funcionales fijados; métricas de rendimiento cuantitativas se instrumentarán y validarán en F07/F08, sin inventarlas.
- [x] **F01-P05 — Catálogo de decisiones y fuentes.** [Registro de decisiones](REGISTRO_DECISIONES_Y_TRAZABILIDAD.md). `DEC-0001/0002` registradas y acta Valhalla disponible; **QA documental y fusión PR #2 comprobadas** en el [acta de cierre](ACTA_CIERRE_DOCUMENTAL_F01_2026-10-13.md).

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

**Decisiones resueltas:** `DEC-0001` = **Galaxy → nueva Clase Valhalla**, `DEC-0002` = prototipo interno Sensores. **Cierre de F01 registrado el 13-10-2026**, tras revisión de P01–P05 y PR #2 ya fusionada, solo al nivel `DISENO_VALIDADO`. `DEC-0003` (puente piloto/licencias) se resolverá técnicamente en F07. **Pendientes exteriores a F01:** año de servicio, modelo/puentes UE5, Core RPG, pruebas de rendimiento y licencias.

Consúltese [PLAN_MAESTRO](../../PLAN_MAESTRO.md), [DECISIONES_Y_RIESGOS](../../DECISIONES_Y_RIESGOS.md), [CRITERIOS_DE_CIERRE](../../CRITERIOS_DE_CIERRE.md) y [ESTADO_GLOBAL.json](../../ESTADO_GLOBAL.json).
