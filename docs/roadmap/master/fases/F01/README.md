# F01 — Visión del producto y canon

**Estado global:** EN_CURSO (F01-P03 y F01-P04 requieren decisión del autor). **Revisión:** 2026-10-11. **Madurez actual:** `DISENO_VALIDADO` del material heredado para P01/P02; propuesta revisable para P03–P05.

## Objetivo

Consolidar la visión del videojuego 3D para PC, verificar épocas/canon y cerrar el primer corte de alcance, **sin trasladar contratos originales ni inventar decisiones creativas**. F00 está cerrada por PR #1, commit `0f989948`.

## Pasos y evidencias

- [x] **F01-P01 — Visión 3D MSI, carrera libre, universo autónomo.** [Visión de producto](../../../../vision/VISION_PRODUCTO_RPG_3D_v0.1.md). Se reconcilian los acuerdos existentes y se declaran exclusiones; decisión original mantenida.
- [x] **F01-P02 — Auditoría de épocas y canon.** [Auditoría de canon](AUDITORIA_EPOCAS_Y_CANON.md). Confirmadas tres épocas; continuidad emergente; extension Sovereign explícita y precaución Odyssey.
- [ ] **F01-P03 — Dama base Imperator.** [Análisis comparado](ANALISIS_DAMAS_IMPERATOR.md). `NECESITA_AUTOR (DEC-0001)`: no seleccionar automáticamente entre Galaxy, Sovereign y Odyssey.
- [ ] **F01-P04 — Primer MVP y presupuestos.** [Propuesta de escenario y métricas](PROPUESTA_MVP_Y_PRESUPUESTO.md). `NECESITA_AUTOR (DEC-0002)`: aprobar/ajustar guardia de Sensores como primer ejecutable; fijar criterios de rendimiento sin inventar mediciones.
- [ ] **F01-P05 — Catálogo de decisiones y fuentes.** [Registro de decisiones](REGISTRO_DECISIONES_Y_TRAZABILIDAD.md). Matriz de acuerdos adoptados, no aprobados y pendientes creada; debe actualizarse con DEC-0001/0002 y acta definitiva para cerrar.

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

**Bloqueos actuales:** DEC-0001 (Dama) y DEC-0002 (MVP). DEC-0003 (puente piloto y licencias) pertenece a F07. La fase **no** se declarará cerrada hasta recoger decisión de autor, actualizar registros, validar enlaces/estado y fusionar PR.

Consúltese [PLAN_MAESTRO](../../PLAN_MAESTRO.md), [DECISIONES_Y_RIESGOS](../../DECISIONES_Y_RIESGOS.md), [CRITERIOS_DE_CIERRE](../../CRITERIOS_DE_CIERRE.md) y [ESTADO_GLOBAL.json](../../ESTADO_GLOBAL.json).
