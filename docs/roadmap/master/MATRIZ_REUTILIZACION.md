# Matriz de reutilización: lo que existe → dónde se aprovechará

**Corte auditado:** `main@0800322d4321cc781f0d9603f9a900dcb2f2bc27` (11-10-2026). No mueve archivos ni obliga a repetir trabajo. Los estados pertenecen al **alcance indicado**, no a «todo el juego terminado». El inventario completo de archivos está en [INVENTARIO_BASELINE_2026-10-11.json](INVENTARIO_BASELINE_2026-10-11.json).

## Planes superiores ya creados

| Origen existente | Estado comprobado del origen | Encaje prioritario | Acción |
|---|---|---|---|
| `CONTENT_STATUS.md` | Seguimiento documental de 567 líneas, amplio y vivo; mezcla ámbitos y cierres delimitados | F00 y transversal | **CONSERVAR**; enlazar, no reemplazar con un porcentaje genérico |
| `docs/roadmap/game_design_readiness_v0_2.md` | 8 pilares, foundation establecida, profundidad desigual | F01–F13 | **CONSERVAR** subplan transversal y correspondencia en fichas |
| `docs/roadmap/procedural_layers_master_plan_v0.1.md` | Capas 001–118 `COMPLETE` en diseño, 119 parcial, 120 `BLOCKED_RUNTIME` | F03, F04, F12, F13, F14, F15 | **REUTILIZAR** reglas; **NO** equiparar a runtime |
| `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md` | Bloques 1–3 referencia `COMPLETE`, 4 `READY_TO_RESUME` | F13-P01..P05 | **CONTINUAR** desde 4, sin reabrir 1–3 salvo errores |
| `docs/roadmap/academy_life_final_closure_v1.0.md` | 20/20; manifest con 482 pruebas definidas y workflow CI | F10, F12 | **REUTILIZAR**; integración UE5 aparte |
| `docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md` | 15/15 contratos y generadores de referencia | F04, F11, F12 | **REUTILIZAR**; simular en Core después |
| `docs/roadmap/ship_console_vertical_slice_v0_0_1.md` | catálogo/Sensores y log con base v0.1; ejecución integral bloqueada | F06–F08 | **REUTILIZAR** como corte obligatorio v0.0.1 |

## Reglas de juego, Academia, universo y pruebas

| Rutas existentes (no mover) | Qué está definido / evidencias localizadas | Fase / paso | Destino y brecha real |
|---|---|---|---|
| `sources/canon_policy.md`, `sources/provenance_policy.md`, `docs/decisions/` | Política de fuentes, épocas, decisiones y canon | F01-P02/P05 | Auditar compatibilidad con nuevas decisiones sin borrar fuentes |
| `lore/federation/starfleet/`, `lore/starships/` | Escalas de rangos, institución, clases y tecnología | F01, F04, F11 | Usar canon y tipos existentes, no convertir el lore en lógica duplicada |
| `gameplay/careers/academy_path/` | 4 años × 3 trimestres, 60 cursos + 7 ramas y material derivado; 463 archivos dentro del grupo de dos niveles en corte anterior | F10-P01/P03/P04 | Integrar con experiencia UE5 y `academiaflota`; no reescribir la currícula |
| `gameplay/careers/assignments/`, `promotions/`, `transfers/`, `service_record/` | Modelos de destino, expediente, ascenso y carrera | F11-P02/P03 | Conectar al runtime con decisiones opcionales y evidencias |
| `gameplay/chain_of_command/README.md` y cinco contratos asociados | Puesto/servicio/delegación, modos del capitán; no solo rango | F04-P03/P04, F05-P01/P02 | Completar estados borde: mando interino, sustitución, revocaciones |
| `gameplay/orders/starship_order_contract.json`, `subordinate_task_order.json`, `starship_order_pipeline.md` | Orden estructurada, validación, resultado, tarea y desobediencia posible | F05-P01/P02/P05 | Separar orden/solicitud/tarea y ejecución concurrente; coordinar con Core 4.10+ |
| `gameplay/ship_operations/operational_event_log/` | Contrato append-only, visibilidad, catálogo y ejemplo Sensores | F03-P03/P04, F05-P05, F06-P03 | Runtime genérico de eventos en Core; privacidad/observabilidad por Star Trek |
| `gameplay/ship_operations/sensor_resolution/`, `tools/simulation/resolve_sensor_scan.py` | Detección observador-relativa con motor determinista y tests | F06-P01/P02/P05 | Integrar consola, eventos y 3D sin filtrar verdad oculta |
| `gameplay/ship_operations/consoles/` | Catálogo de 16 familias funcionales, Sensores como primera | F06, F09 | Árbol operativo no implica implementación de todas las familias |
| `gameplay/ship_operations/interconsole/`, `ship_memory/` | Intercambio Sensor→Ciencia y dossiers de nave con procedencia | F03, F06, F09 | Transferencias y persistencia ejecutables en runtime |
| `gameplay/ship_operations/ship_computer/` | Servicio transversal y rutas deterministas/IA | F02, F05, F09 | Validar API, permisos, consultas y acciones reales |
| `gameplay/duty_system/`, `gameplay/characters/` | Guardias, actividad, objetivos, bienestar y desarrollo | F04, F10, F12 | Resolver conflictos de agenda/posición física y LOD |
| `gameplay/social/`, `gameplay/relationships/`, `ai/memory/`, `ai/personality/` | Contratos de relaciones, recuerdos y conducta | F12 | Integrar simulación larga y límites de conocimiento/privacidad |
| `universe/generation/`, `gameplay/first_contact/` | Universo materializado y protocolos de contacto/Primera Directriz | F03, F13 | Convertir referencia procedural en mundo persistente ejecutable |
| `gameplay/conflict/`, `gameplay/diplomacy/`, `gameplay/logistics/`, `narrative/` | Conflicto, reglas de autoridad, consecuencias, ganchos causales | F13 | Orden subplan 4–10 y simulación, no misiones inventadas por conveniencia |
| `art_direction/visual_bibles/`, `art_direction/nap/`, `nap/` | Biblias visuales y handoff; conexión con NAP | F07, F14 | Mantener maestro/derivado separados y controlar trazabilidad |
| `assets/ships/` | Planos de Constitution, Galaxy, Miranda, y POV de puente Enterprise-D | F07, F11, F14 | Son fuentes/referencias; **no hay por ello un modelo UE5 listo** |
| `presentation/`, `ui/` | Contratos de escenas, cámaras/POV, HUD, familias UI | F07, F08, F09, F14 | Construcción UE5 real y UX consola normal/ampliada |
| `audio/`, `manifests/` | Directorios de producción y preparación | F14 | Inventariar audio real vs README reservado; importar con licencias |
| `tools/generation/` | Simuladores/generadores y scripts `test_*.py` | F10, F13, F15 | Reutilizar, ejecutar y registrar pruebas al cambiar contratos |
| `validation/consistency/`, `validation/fixtures/` | Invariantes y casos de aceptación, incluidos Academia y Sensores | F03–F15 | Validar la ejecución del paso correspondiente, no contar fixtures como runtime |
| `.github/workflows/academy-life-closure.yml` | CI Academy; un run de 10-10-2026 completó con éxito | F10, F15 | Conservar y extender al integrar; revisar que nuevos cambios no rompan CI |
| `docs/manuals/sensors/Manual_Operador_Sensores_Flota_Estelar_v0.1.pdf` | Manual PDF real incluido | F06-P01, F10-P04 | Fuente formativa y operativa, no sustituto del motor de consola |

## Regla de clasificación

- **Diseño o canon existente**: se mantiene exactamente en su sitio y se cita por ruta y alcance.
- **Implementación de referencia**: scripts Python y fixtures que requieren ejecución/prueba propia; sus resultados no equivalen a conexión Core/UE5.
- **Runtime pendiente**: abrir tarea específica e identificar capacidad Core faltante; no duplicarla en `gameplay/`.
- **Presentación pendiente**: tareas UE5, assets y licencias; no confundir capturas, planos o materiales con mallas utilizables.
- **Autoral pendiente**: no inventar reglas nuevas (Dama, MVP o nuevas épocas) para completar una celda.

## Observaciones sobre el inventario íntegro

`INVENTARIO_BASELINE_2026-10-11.json` asigna **fase primaria por ruta mediante heurística**, con 1.720 entradas/SHAs/tamaños. La clasificación *no es inspección semántica individual* ni promesa de fase exclusiva: por ejemplo `validation/` participa transversalmente, aunque cada archivo tenga un único marcador primario orientativo. Esta matriz manda sobre el resumen automático cuando un sistema tenga varias fases reales.
