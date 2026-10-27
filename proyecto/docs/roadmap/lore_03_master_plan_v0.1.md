> **CIERRE GLOBAL DE LORE-03 — hechos verificados 2026-10-27; regularización administrativa propuesta:** A/B/C/D/E están desarrolladas y fusionadas: PR #38, #41, #44, #46 y **#49**. La PR #49 se fusionó el 2026-10-27 a las 18:40:47 UTC, commit `22b7e7db7a0fab138879927d6fb05ce7a43e16e7`; la rama fuente `lore/03-e-global-integration-audit` ya no existe. En ese commit, LORE-03E [#40562209896](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40562209896) y LORE-03A [#40562209868](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40562209868) terminaron `success`. El resultado final es **COMPLETE_DOCUMENTARY para A–E**, con reservas de precisión históricas preservadas, día/mes de Academia y fechas precisas de Valhalla sin inventar; CoreRPG conserva autoridad exclusiva del WorldState y no se certifica runtime ni UE5. Esta nota prevalece sobre estados históricos inferiores; el archivo de evidencias es `proyecto/docs/roadmap/lore_03_e/lore03_global_closure_evidence_v0.1.json`. La propuesta de actualización administrativa NO supone por sí misma que su propia PR se haya fusionado.

> **LORE-03D cerrada documentalmente — 2026-10-27:** la PR [#46](https://github.com/robdor80/Videojuego_StarTrek/pull/46) fue fusionada en `main` el 2026-10-27 12:41:51 UTC, commit `6aafca0ef74787184c840c82a92386ff05f532f4`. D01–D08, 35 escenarios y 45 pruebas documentales; dos workflows posteriores en `success`: [LORE-03D #40505811905](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40505811905), [LORE-03A #40505812149](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40505812149). **Estado COMPLETE_DOCUMENTARY**, pendiente únicamente de fusionar la regularización administrativa, sin activar CoreRPG, UE5 o IA. En la auditoría posterior, **la rama fuente todavía existía** en GitHub a pesar de haberse comunicado eliminada; no afirmar eliminación. **LORE-03E continúa pendiente.** Los addenda inferiores son trazabilidad histórica del proceso.

> **LORE-03D en revisión (2026-10-27; rama `lore/03-d-continuity-divergence`):** D01–D08 preparados en `proyecto/docs/roadmap/lore_03_d/` con ejemplos no instanciados y validadores de continuidad/causalidad; **NEEDS_REVIEW_DOCUMENTARY**, no `COMPLETE`, PR pendiente de autorización. Los hechos anteriores a 2383 quedan protegidos; la destrucción posterior de Rómulo no es obligatoria; el año 2383 no dispone aún de día/mes inicial. No hay integración CoreRPG/UE5/IA. Esta nota es el estado vigente de D; las anotaciones cronológicas anteriores se conservan. LORE-03E sigue pendiente.

> **Actualización 2026-10-27 — LORE-03C fusionada:** PR [#44](https://github.com/robdor80/Videojuego_StarTrek/pull/44) fusionada en `main` el 27-10-2026, commit `56abff20c46d4614fb309e4258a44ed0eb9c33b9`, 8 subfases C01–C08 desarrolladas, 13 casos y 6 patrones hipotéticos, 167 pruebas positivas/de mutación/regresión correctas; comprobaciones de `main` tras fusión en `success`. **Estado documental COMPLETE**, sujeto a esta regularización administrativa; no implementa CoreRPG, UE5 ni IA. **LORE-03D/E pendientes.** Las notas históricas inferiores anteriores a la fusión se conservan como trazabilidad temporal.

> **Cierre de LORE-03B — 27-10-2026:** PR [#41](https://github.com/robdor80/Videojuego_StarTrek/pull/41) fusionada en `main`, commit `2b1447d4469fb8f52c98486342be61c9a069b90a`, rama eliminada, CI de LORE-03B y LORE-03A posterior al merge en `success`. Estado documental: **COMPLETE** con reservas históricas trazadas; CoreRPG/UE5 no se han implementado. Esta actualización prevalece sobre los informes anteriores que indicaban B pendiente. **LORE-03C, D y E todavía no están iniciadas.**

> **Actualización LORE-03B (27-10-2026; PR #41 pendiente):** ST-ORG-01 completó la reorganización de carpetas y el autor levantó su suspensión. LORE-03B ha preparado 22 expedientes, 12 escenarios y validadores en las rutas actuales: `mundo/`, `proyecto/` y `desarrollo/`. Su estado es `NEEDS_REVIEW`, no `COMPLETE`; únicamente CoreRPG tendrá autoridad sobre el WorldState. Esta anotación mantiene intacta la historia de las decisiones anteriores; no se fusionará sin autorización.

# LORE-03 — Plan maestro: Historia, conflictos y continuidad galáctica

**Fecha:** 2026-10-23. **Base auditada:** `main@867077e4a0108f5ae71485ba668c0419ee29aa2f`.  
**Estado actualizado 2026-10-23:** PLAN DOCUMENTAL; **03-A COMPLETE** tras [fusión PR #38](https://github.com/robdor80/Videojuego_StarTrek/pull/38) (`d0efab2c9d4b2451ad678b651bd6ecf2283d8235`). B–E NO INICIADAS.  
**Frontera:** no hay implementación CoreRPG/UE5/Host/IA ni Content Pack integrado por efecto de estos ficheros.

## Addendum 2026-10-23 — Año 2383 con cuatro cursos de Academia

El autor propone empezar en **2383**, graduarse alrededor de **2387** como alférez y poder servir en Valhalla. El desarrollo/construcción de esta clase se propone tras *Némesis* (2379–2383), con puesta en servicio objetivo en 2383, como GAME_ADDITION no canonizada. Las fechas exactas y desempeño posterior del programa requieren eventual aprobación. Referencia: proyecto/docs/decisions/lore03a_valhalla_2383_academy.md.

## 1. Decisión marco aprobada

La **única época jugable es TNG/DS9/Voyager**, con `2364–2378` como ventana **referencial** y fecha concreta de comienzo **sin determinar**. Pike/Kirk quedan en el catálogo histórico; su material no se borra. Los hechos de pantalla anteriores a fecha `D` dan forma a la historia de arranque, pero **desde `D` ninguna fecha futura fuerza guiones**. Las excepciones creativas anteriores a `D` exigen aprobación como `GAME_ADDITION`, preservando evidencia de pantalla. Viajes temporales **no jugables**.

**Autoridad de decisión:** `proyecto/docs/decisions/playable_eras.md` y `proyecto/docs/decisions/campaign_continuity.md`.

## 2. Auditoría de fuentes y reutilización: no reconstruir

| Fuente existente | Qué reutiliza LORE-03 | Lo que NO debe duplicarse |
|---|---|---|
| `sistemas/universe/chronology/master_timeline/MASTER_TIMELINE_v0.1.md`, `temporal_anchors.json`, `era_profiles/*` | Columna vertebral y filtros de fechas | Crear nueva selección de era o inventar día exacto |
| `mundo/lore/historical_events/historical_event_contract.json` | Campos obligatorios, incertidumbre, antigüedad | Esquema runtime paralelo |
| `mundo/lore/diplomacy/historical_events_v0.1.json` | **40 registros** de LORE-01 D, unidos por IDs | Volcar/copiar íntegramente 40 registros a una segunda verdad |
| `mundo/lore/diplomacy/relation_evidence_v0.1.json`, `agreements_conflicts_v0.1.json` | Hechos políticos, relaciones y acuerdos | Reescribir relaciones como sucesos automáticos |
| `mundo/lore/conflicts/conflict_definition_contract.json` | Enlace de conflictos históricos a campaña | Duplicar reglas estratégicas |
| `sistemas/gameplay/conflict/conflict_war_index_v0.1.json` y `sistemas/gameplay/consequences/*` | Contratos de causalidad y consecuencias | Activar conflictos a partir de lore |
| `mundo/sources/canon_policy.md`, `mundo/sources/provenance_policy.md`, registro de fuentes | Jerarquía de evidencia y categorías | Cambiar procedencia `INFERRED` por `SCREEN_CANON` |
| `sistemas/gameplay/ship_operations/era_technology_matrix.json`, `mundo/lore/starships/classes/core_starship_classes.json` | Hitos tecnológicos y alta de clases | Suponer una nave disponible por disponer de un GLB |
| `sistemas/gameplay/careers/academy_path/academy_era_profiles.json` y F01 | Contexto formativo anterior y trazabilidad | Borrar perfiles de material histórico sin auditar |
| `proyecto/docs/roadmap/master/fases/F03`, `sistemas/universe/global_rules/canon_vs_campaign.md` | Estado inicial, causalidad, conocimiento y guardados | Repartir autoridad de CoreRPG entre IA y UE5 |

**Hallazgo de alcance:** documentos y contratos de referencia previos siguen mencionando tres épocas jugables. Se regularizan las decisiones rectoras y se registra una **deuda de migración documental** para consumidores antiguos; no se declara por ello runtime actualizado.

## 3. Entregables y criterios por fase

### LORE-03 A — Cronología y acontecimientos
- Inventario de fuentes, matriz de precisión temporal, tipología de hechos y referencias históricas anteriores.
- Índice *por referencia* sobre los 40 acontecimientos de LORE-01 D, diferenciando informes falsos de sucesos históricos.
- Nuevas fichas **solo** para huecos reales (Wolf 359, agujero de gusano, Voyager, etc.), con ID estable, fecha aproximada, pantalla/fuente y límites.
- Unir personajes, instituciones, lugares y naves mediante referencias existentes cuando estén identificadas; no fabricar IDs de instancias.
- Tabla de escenarios `D` anterior/posterior a acontecimiento; conocimiento institucional versus individual queda reservado para C.
- **Cierre A:** corpus cronológico cubre hitos mayores del periodo y prehistoria pertinente, fuentes verificadas y ambigüedades abiertas, auditoría de anacronismos de naves, al menos 10 pruebas negativas/positivas, CI verde, revisión y aprobación humana. El arranque v0.1 **NO acredita el cierre**.

### LORE-03 B — Guerras, conflictos y crisis
- Dossiers históricos de ocupación bajorana, Guerra del Dominio, Maquis, Borg/Wolf 359, Federación-Cardassia, cambios de alianzas y tratados.
- Comprobación de comienzos/finales inciertos y consecuencias sin pronosticar campañas.
- Datos de participantes, frentes, causas, bajas e instituciones **solo cuando estén documentados**.
- Reutilizar `mundo/lore/conflicts/*` y contratos `sistemas/gameplay/conflict/*`; no segunda simulación.
- **Cierre B:** trazabilidad evento↔conflicto, fronteras y acuerdos, escenarios de paz/ocupación y regresión A/LORE-01.

### LORE-03 C — Memoria y consecuencias
- Causalidad de daños, veteranos, refugiados, memoriales, herencias científicas, biografías, servicios en naves e instituciones.
- Matriz de `hecho real / conocido por institución / sabido por NPC / creencia errónea / secreto`; ninguna especie comparte omnisciencia.
- Prevención de trasvases automáticos de informes clínicos, información Omega o reputaciones.
- **Cierre C:** casos de NPC con biografías temporales coherentes y pruebas negativas de conocimiento, reputación y pérdidas.

### LORE-03 D — Divergencia de campaña
- Modelo **documental** de estado inicial para una fecha `D` seleccionada, sucesos futuros no obligatorios, temporadas narrativas y simulación autónoma.
- Cambios de causalidad, registro de historia real por guardado, preservación de resultados, estado tras recarga; sin preparar código de CoreRPG.
- Autonomía NPC y director de acontecimientos: proponer ≠ declarar verdad; la simulación se somete a Core.
- **Cierre D:** ejemplos de partida iniciada antes/durante/después de grandes hitos y consecuencias diferentes sin reescritura del pasado.

### LORE-03 E — Auditoría transversal
- Verificar A–D contra LORE-01, LORE-02, F00–F15, fuentes y mecanismos de coherencia existentes.
- Control de fechas/IDs, falsos eventos, anacronismos, límites de especie, sistemas reservados Delta y disponibilidad individual de clases.
- Documentar deuda de migración a datasets de juego, adaptadores Host/CoreRPG y representación UE5 para una **fase posterior**.
- **Cierre E:** informe de reservas, CI/regresiones y decisión humana; una PR propia, sin fusionar automáticamente.

## 4. Gobierno de PR y estado

1. Crear **rama y PR independiente por A–E**; la PR A puede contener la decisión de alcance necesaria antes del desarrollo del corpus.
2. `IN_PROGRESS` mientras se investiga; `NEEDS_REVIEW` tras entregar, `COMPLETE` solamente con aprobación/fusión y evidencia de CI.
3. No fusionar, activar auto-merge, borrar ramas, modificar `main` directamente ni activar runtime.
4. Conservar la auditoría histórica y actuar con cambios explícitos/no destructivos.
5. En CI ejecutar validadores nuevos y regresiones existentes; verde **documental**, no homologación audiovisual escena a escena.

## 5. Riesgos y decisiones pendientes

| Código | Riesgo / decisión | Tratamiento |
|---|---|---|
| DEC-03-01 | Año inicial | **2383 preferido y propuesto**; día/mes no fijado, no hardcodear todavía |
| DEC-03-02 | Clase Valhalla | **Objetivo de entrada en servicio 2383**, desarrollo tras Némesis y alféreces de la promoción 2387; fechas técnicas aún por consolidar |
| DEC-03-03 | **Odyssey** y ejemplar Enterprise-F | Año y estatus **por acreditar**; no incorporar retroactivamente |
| DEC-03-04 | Mecanismo de excepciones temporales creativas | Cada excepción concreta requiere aprobación y registro `GAME_ADDITION`, jamás por deducción |
| R-03-05 | Epoch flags antiguos en Academia, naves, tecnología, cronologías | Mantener fuentes; auditar selectores antes de implementación; el histórico no es jugable |
| R-03-06 | Eventos con fechas inferidas, emisión confundida con tiempo interno | Marcar `YEAR_APPROXIMATE` y fuente; no fabricar mes/día |
| R-03-07 | Alegaciones falsas/operaciones secretas | Registrar como alegación, creencia o informe; no afirmar golpe de Estado o conocimiento público |
| R-03-08 | Retorno Voyager, guerras, muertes predeterminadas | Sólo pasado al empezar después del hecho; antes de él, futuro emergente |
| R-03-09 | Canon cinematográfico tardío y Endgame | Aceptar excepciones creativas documentadas, no disponibilidad universal ni viajes temporales jugables |

## 6. Aprobación y siguiente puerta

LORE-03 A se completa editorialmente con `proyecto/docs/roadmap/lore_03_a_baseline_audit_v0.1.md` y `mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json` como línea base más el atlas y la auditoría final v0.2; consta **COMPLETE** tras fusión de PR #38 y validaciones documentales. La condición administrativa previa para **preparar B** queda satisfecha, sin iniciarse B automáticamente.
