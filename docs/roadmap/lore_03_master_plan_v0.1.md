# LORE-03 — Plan maestro: Historia, conflictos y continuidad galáctica

**Fecha:** 2026-10-23. **Base auditada:** `main@867077e4a0108f5ae71485ba668c0419ee29aa2f`.  
**Estado (2026-10-23):** PLAN DOCUMENTAL; **03-A NEEDS_REVIEW** (corpus y pruebas preparados, pendiente autorización del autor). B–E NO INICIADAS.  
**Frontera:** no hay implementación CoreRPG/UE5/Host/IA ni Content Pack integrado por efecto de estos ficheros.

## 1. Decisión marco aprobada

La **única época jugable es TNG/DS9/Voyager**, con `2364–2378` como ventana **referencial** y fecha concreta de comienzo **sin determinar**. Pike/Kirk quedan en el catálogo histórico; su material no se borra. Los hechos de pantalla anteriores a fecha `D` dan forma a la historia de arranque, pero **desde `D` ninguna fecha futura fuerza guiones**. Las excepciones creativas anteriores a `D` exigen aprobación como `GAME_ADDITION`, preservando evidencia de pantalla. Viajes temporales **no jugables**.

**Autoridad de decisión:** `docs/decisions/playable_eras.md` y `docs/decisions/campaign_continuity.md`.

## 2. Auditoría de fuentes y reutilización: no reconstruir

| Fuente existente | Qué reutiliza LORE-03 | Lo que NO debe duplicarse |
|---|---|---|
| `universe/chronology/master_timeline/MASTER_TIMELINE_v0.1.md`, `temporal_anchors.json`, `era_profiles/*` | Columna vertebral y filtros de fechas | Crear nueva selección de era o inventar día exacto |
| `lore/historical_events/historical_event_contract.json` | Campos obligatorios, incertidumbre, antigüedad | Esquema runtime paralelo |
| `lore/diplomacy/historical_events_v0.1.json` | **40 registros** de LORE-01 D, unidos por IDs | Volcar/copiar íntegramente 40 registros a una segunda verdad |
| `lore/diplomacy/relation_evidence_v0.1.json`, `agreements_conflicts_v0.1.json` | Hechos políticos, relaciones y acuerdos | Reescribir relaciones como sucesos automáticos |
| `lore/conflicts/conflict_definition_contract.json` | Enlace de conflictos históricos a campaña | Duplicar reglas estratégicas |
| `gameplay/conflict/conflict_war_index_v0.1.json` y `gameplay/consequences/*` | Contratos de causalidad y consecuencias | Activar conflictos a partir de lore |
| `sources/canon_policy.md`, `sources/provenance_policy.md`, registro de fuentes | Jerarquía de evidencia y categorías | Cambiar procedencia `INFERRED` por `SCREEN_CANON` |
| `gameplay/ship_operations/era_technology_matrix.json`, `lore/starships/classes/core_starship_classes.json` | Hitos tecnológicos y alta de clases | Suponer una nave disponible por disponer de un GLB |
| `gameplay/careers/academy_path/academy_era_profiles.json` y F01 | Contexto formativo anterior y trazabilidad | Borrar perfiles de material histórico sin auditar |
| `docs/roadmap/master/fases/F03`, `universe/global_rules/canon_vs_campaign.md` | Estado inicial, causalidad, conocimiento y guardados | Repartir autoridad de CoreRPG entre IA y UE5 |

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
- Reutilizar `lore/conflicts/*` y contratos `gameplay/conflict/*`; no segunda simulación.
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
| DEC-03-01 | Año exacto de inicio | **Pendiente del autor. No fijar en una prueba o diseño como norma** |
| DEC-03-02 | Entrada en servicio de **Clase Valhalla** | **Pendiente del autor**; referencia F01 y addendum posterior |
| DEC-03-03 | **Odyssey** y ejemplar Enterprise-F | Año y estatus **por acreditar**; no incorporar retroactivamente |
| DEC-03-04 | Mecanismo de excepciones temporales creativas | Cada excepción concreta requiere aprobación y registro `GAME_ADDITION`, jamás por deducción |
| R-03-05 | Epoch flags antiguos en Academia, naves, tecnología, cronologías | Mantener fuentes; auditar selectores antes de implementación; el histórico no es jugable |
| R-03-06 | Eventos con fechas inferidas, emisión confundida con tiempo interno | Marcar `YEAR_APPROXIMATE` y fuente; no fabricar mes/día |
| R-03-07 | Alegaciones falsas/operaciones secretas | Registrar como alegación, creencia o informe; no afirmar golpe de Estado o conocimiento público |
| R-03-08 | Retorno Voyager, guerras, muertes predeterminadas | Sólo pasado al empezar después del hecho; antes de él, futuro emergente |
| R-03-09 | Canon cinematográfico tardío y Endgame | Aceptar excepciones creativas documentadas, no disponibilidad universal ni viajes temporales jugables |

## 6. Aprobación y siguiente puerta

LORE-03 A se completa editorialmente con `docs/roadmap/lore_03_a_baseline_audit_v0.1.md` y `lore/historical_events/lore03_a_chronology_index_v0.1.json` como línea base más el atlas y la auditoría final v0.2; sigue **NEEDS_REVIEW** hasta revisión/fusión. No avanzar a B hasta PR A aceptada por el autor.
