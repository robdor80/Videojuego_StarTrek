# Acta de reconciliación de gobierno — F00 a F06

**Fecha:** 2026-10-13  
**Repositorio:** `robdor80/Videojuego_StarTrek`  
**Punto de partida verificado:** `main@dfe2ef57458056a130b49a0b87dc41e90726bfff`  
**Alcance:** estados de planificación, decisiones, pruebas de referencia y puertas técnicas. **No se ha ejecutado Core con UE5 ni se certifica juego jugable.**

## 1. PR realmente fusionadas en main

| Fase | PR | Commit de fusión comprobado | Qué se incorporó |
| --- | --- | --- | --- |
| F00 | [#1](https://github.com/robdor80/Videojuego_StarTrek/pull/1) | F00 cerrada previamente | Línea base y gobierno inicial |
| F01 | [#2](https://github.com/robdor80/Videojuego_StarTrek/pull/2) | `f3bba78aac76d15f0e34672e18bd91d0ebaa2248` | Visión, canon, elección de nueva Clase Valhalla |
| F02 | [#3](https://github.com/robdor80/Videojuego_StarTrek/pull/3) | `2610be5197e3bcf789fb154023fc4ad8c8d2c9c4` | Arquitectura documental, contratos candidatos y QA estática |
| F03 | [#4](https://github.com/robdor80/Videojuego_StarTrek/pull/4) | `3d353871b5e014eb14ed3f8504547adb08a9fe3f` | Continuidad, conocimiento, persistencia de referencia |
| F04 | [#5](https://github.com/robdor80/Videojuego_StarTrek/pull/5) | `c19356ad61d740c2054843ff91448f0ff00ac02b` | Dotaciones, guardias, permisos y cadena de mando de referencia |
| F05 | [#6](https://github.com/robdor80/Videojuego_StarTrek/pull/6) | `ddfd728712d12cd240ccd1ecc5ddf352d5f9576a` | Órdenes, delegación, iniciativa NPC e IA en referencia |
| F06 | [#7](https://github.com/robdor80/Videojuego_StarTrek/pull/7) | `dfe2ef57458056a130b49a0b87dc41e90726bfff` | Sensores, proyecciones, Ciencia y validación cruzada |

Los números #2–#7 proceden de verificaciones de `merged=true` sobre GitHub. La fusión **no equivale al cierre de la fase**.

## 2. Cierre documental F01 — decisión de gobierno

Se revisaron en `main` los cinco entregables F01 y su relación con el registro central:

- P01: visión 3D PC/MSI, vida NPC y carrera opcional — `docs/vision/VISION_PRODUCTO_RPG_3D_v0.1.md`.
- P02: fuentes y tres épocas, continuidad propia — `fases/F01/AUDITORIA_EPOCAS_Y_CANON.md`.
- P03: [decisión creativa aprobada](fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md), con `DEC-0001` resuelta. **Galaxy/Enterprise-D inspira una nueva Clase Valhalla**, no un refit ni una nave ya jugable.
- P04: alcance de la prueba v0.0.1 de Sensores y mediciones pendientes — `fases/F01/PROPUESTA_MVP_Y_PRESUPUESTO.md`, `DEC-0002`.
- P05: [trazabilidad](fases/F01/REGISTRO_DECISIONES_Y_TRAZABILIDAD.md), [riesgos](DECISIONES_Y_RIESGOS.md), acta Valhalla, PR #2 fusionada.

**Verificación realizada:** presencia y lectura de artefactos, coherencia entre decisiones, referencia de PR y ausencia de decisiones creativas pendientes para el **alcance F01**. **Resultado:** F01 `CERRADA` / `DISENO_VALIDADO`; P01–P05 `CERRADA` **solo en diseño**. No hubo benchmark, sesión UE5, compilación Core ni verificación de licencias en esta puerta. La entrada en servicio de Valhalla, su nombre de unidad/matrícula y la elección de puente piloto no se fijan.

## 3. Estado regularizado

| Fase | Estado oficial | Madurez de evidencia comprobada | Puerta que falta |
| --- | --- | --- | --- |
| F00 | `CERRADA` | `DOCUMENTACION_AUDITADA` | No reabrir sin anomalía |
| F01 | `CERRADA` | `DISENO_VALIDADO` | La implementación 3D pertenece a fases posteriores |
| **F02** | **`EN_CURSO`**, principal | `DISENO_VALIDADO` + QA documental P04 | Contratos/ABI reales Core y Host para `CONTRATO_VALIDADO` |
| F03 | `EN_REVISION` | `REFERENCIA_PROBADA` de fixture | Generación, conocimiento, eventos y save/load en Core |
| F04 | `EN_REVISION` | `REFERENCIA_PROBADA` | Guardias, cargos y permisos en Core, pruebas operativas negativas |
| F05 | `EN_REVISION` | `REFERENCIA_PROBADA` | Motor de órdenes/acciones, NPC y persistencia con Core real |
| F06 | `EN_REVISION` | `REFERENCIA_PROBADA` | Inspección visual PDF P01, Core/Host UE5, Ciencia, save/load y E2E |
| F07–F08 | `PLANIFICADA` (pausadas) | No certificadas como producto jugable | Reactivación, puente viable, Core↔UE5 y guardia en MSI |

La condición `CERRADA` de un **paso** F04 o de suites P05 indica **solo el entregable referencial descrito en `step_evidence_maturity`**. No autoriza interpretar la fase global como terminada. Los pasos cuya implementación requiere Core quedan `BLOQUEADA` y las fases respectivas `EN_REVISION`, evitando borrar el trabajo documental ya hecho.

## 4. Evidencia de prueba transversal, no runtime

Ejecución [GitHub Actions 38321712021](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38321712021), correspondiente a la PR integrada F06 contra `main`:

| Batería | Resultado observado |
| --- | --- |
| Regresión motor Sensores | 8/8 |
| F06 referencia | 23/23 |
| Cadena F04→F05→F06 | **3/3 ejecutadas, 0 skips** |
| F03 referencia | 26/26 |
| F04 referencia | 17/17 |
| F05 referencia | 19/19 |
| **Total unit tests** | **96 superados** |

El workflow aislado en la rama permitía 3 skips **solo** porque el checkout no contenía F04/F05; el job de PR integrada **ejecutó** realmente los tres casos. La CI no demuestra mutación auténtica de `WorldState`, guardado/carga del videojuego, autonomía NPC real, sensores interactivos UE5 ni consola 3D lista.

## 5. Estado Core y tareas siguientes

El 13-10-2026 se volvió a consultar [`CoreRPG/main`](https://github.com/robdor80/CoreRPG/tree/dcfcb83c9853e005b5450bd39e0ba693cb91e257), todavía en `dcfcb83c9853e005b5450bd39e0ba693cb91e257` (corte 4.4 de la auditoría). El diseño de F02–F06 no valida automáticamente 4.5, 4.7, 4.9, 4.10 ni interfaces UE5.

**Orden operativo:** (a) contrastar Core 4.5 y negociar contratos concretos para el corte Sensores; (b) inspeccionar el manual PDF F06-P01 y registrar correspondencia con árbol; (c) reactivar F07 para elegir y verificar puente/pipeline en MSI; (d) integrar, probar y aceptar F08 v0.0.1; (e) actualizar estados sólo al pasar la evidencia necesaria. La autorización de estas fases no se inventa con la regularización.

## 6. Regla de mantenimiento

`ESTADO_GLOBAL.json` es el registro oficial, `PLAN_MAESTRO.md` es su presentación y este documento es el **acta fechada del corte**. La CI de gobierno valida ambos frente a los 16 IDs/80 pasos y la fase principal. Los expedientes históricos del 11–12 de octubre no deben reescribirse como si sus fotografías iniciales fueran falsedades; se agregan actualizaciones explícitas.
