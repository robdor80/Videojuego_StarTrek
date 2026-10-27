# F08-P02–P05 — Matriz de ejecución y aceptación del primer turno de Sensores

**13-10-2026 · PLAN PREPARATORIO · 0 pruebas E2E ejecutadas**

La meta es una **guardia reproducible y jugable en MSI/UE5 con CoreRPG**, no validar prototipos Python ni vídeos. Fuente del contrato: `desarrollo/validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`; conservar los 13 identificadores exactamente y registrar sus resultados solo cuando el runtime esté disponible.

| Paso | Caso de ejecución | Evidencia exigida | Estado |
|---|---|---|---|
| P02 | Capitán NPC con rol/turno/autoridad válidos da orden; jugador reconoce; situación avanza fuera de escena | Trazas Core de orden/acuse/autoridad y proyección al jugador | NO_EJECUTADO |
| P02 | Capitán no autorizado, jugador fuera de servicio, reintento y caducidad | Denegaciones, sin cambios de verdad indebidos | NO_EJECUTADO |
| P03 | UI Sensores 3D activa barrido de firmas ya existentes; parámetros afectan detección | Captura del recorrido y trazas resolución/proyección contra Core | NO_EJECUTADO |
| P03 | Barrido sin hallazgos, sector con interferencia y datos ocultos | Resultado vacío/incierto válido, sin creación de contactos ni filtraciones | NO_EJECUTADO |
| P03 | Informe al capitán y cadena de eventos sin universalizar conocimiento | IDs causales de orden, operación, resultado e informe | NO_EJECUTADO |
| P04 | Guardar/cerrar/cargar a mitad y al final de una orden | Hash/versión partida, continuidad de IDs, revisiones, pendientes, conocimiento y eventos | NO_EJECUTADO |
| P04 | IA desconectada, Actor 3D descargado, guardado corrupto y respuesta tardía | Fallback sin ficción autoritativa, persistencia segura, fallo explícito | NO_EJECUTADO |
| P05 | Run completo repetible de orden→escaneo→informe→consecuencia→carga | Build UE5 fuera del editor, comandos/logs, vídeo y veredicto | NO_EJECUTADO |
| P05 | Rendimiento/estabilidad en MSI y licencias de assets | Versión UE5, hardware/driver, resolución, FPS/frame time, RAM/VRAM, incidencias y hashes | NO_EJECUTADO |

## Invariantes de aceptación (13/13 en Core↔UE5)
- **Mundo/identidad:** `deterministic_world`, `reality_precedes_scan`, `persistent_identity`, `era_validity`.
- **Conocimiento:** `hidden_information_gate`, `anti_leakage`, `observer_relative_contacts`, `knowledge_visibility`.
- **Sensor/IA:** `detection_not_truth_creation`, `system_state_matters`, `ai_boundary`.
- **Operación/persistencia:** `event_chain`, `save_load_roundtrip`.

El test solo contará como PASS cuando se ejecute una transacción real sobre Core y se verifique desde la presentación UE5. Los casos negativos forman parte de la aceptación, aunque los 13 invariantes se enumeren como cobertura funcional. Si falla uno, el veredicto global es **NO-GO**.

## Registro mínimo obligatorio de cada ejecución
`case_id`, `fixture_id`, `outcome` (PASS/FAIL/BLOCKED/NO_EJECUTADO), fecha local, versión/commit de Trek y Core, versión de UE5, configuración MSI, nivel/mapa, hash assets relevantes, acciones realizadas, resultado esperado/obtenido, evidencias (log/captura/vídeo), incidencia y responsable de resolución. No introducir datos sintéticos como métricas medidas.

## Límites de integración
- **CoreRPG**: entidades, identidad, tiempo, acciones, permisos, conocimiento, bitácora y save/load; nunca imitar Core con un motor paralelo en Star Trek.
- **Star Trek**: catálogo de consolas, reglas de sensores, órdenes y requisitos temáticos; resultados estructurados y vista por observador.
- **UE5**: movimiento, animaciones, consola 3D, entrada de usuario y presentación; no autoridad del mundo.
- **LLM remota**: texto/voz opcionales sobre datos autorizados; nunca inventar eventos/resultados ni validar órdenes.

**GO para preparar:** documentación, guiones, tabla de casos y mapeo de adaptadores. **NO-GO para declarar F08 completada:** Sutherland no transitado y probado en UE5/Windows, Core sin E2E y sin build/telemetría. F02 continúa única fase principal EN_CURSO mientras se trabaja en paralelo.
