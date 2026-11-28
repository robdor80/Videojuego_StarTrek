# F06-BIS — Siete trabajos nativos: matriz de entrega (06-11-2026)

**Rama:** `feat/f06-bis-seven-workstreams-20261106`, PR #93 sobre PR #91. **F06 global NO cerrada**. Se respeta CoreRPG, el calendario F04 y las órdenes F05. No se ha utilizado Codex ni el MSI.

## Objetivo

Transformar las capacidades ya implementadas de F06 en una cadena verificable: mundo materializado → observación real → trabajo temporal autorizado → resultado científico con evidencia → respuesta de departamentos → archivo y restitución tras guardar/cargar. Asegurar que la Enterprise-D modernizada no hereda sensores funcionales de un platillo físicamente desconectado.

| Trabajo aprobado | Entregable nativo | Límite actual |
|---|---|---|
| 1. Ciencia planetaria | `f06_host_complete_science`: mide T, presión, H₂O superficial, N₂/O₂/CO₂, superficie e indicios biológicos; deriva clase M/H/J/L/P/Y únicamente desde mediciones y **confianza** de un resultado focal real. `build_aster_science.py` produce instrumentos desde la realidad física privada de los seis mundos Aster, **solo para tests**. | Química, atmósfera y habitabilidad todavía usan modelos aproximados; el Host del universo definitivo debe aportar mediciones comprobables y la consola de Ciencia debe mostrarlas. `class` significa candidata, no etiqueta canon ni inferencia de vida inteligente. |
| 2. Historial y procedencia | Entidad `f06_science_report` persistente con refs Core a handoff y observación focal, identidad pública opaca, fecha, calidad, datos y conclusión. Reenvío idempotente; no modifica clase de nave. | Falta un dossier científico extenso de múltiples observaciones por objeto, incertidumbres por especie e informes narrativos. |
| 3. Tiempo/recursos | `f06_begin_timed_scan`, `f06_cancel_timed_scan`, `f06_timed_scans_page`. Duración ≥30 s, coste y concurrencia reservados, ejecución al vencer en **el mismo reloj Core**, interruptores de fallos reales, operador revalidado. | La reserva se expresa en unidades abstractas de Sensores: no equivale a vatios suministrados por el núcleo warp. La cola de acciones global / consumo físico de ingeniería requiere integración departamental posterior. |
| 4. Interferencias | `f06_host_environment`: cinco bandas independientes EM, térmica, gravimétrica, subespacial y biológica (0–550), revisión estrictamente creciente, penalizaciones por categoría, reescaneo pasivo y persistencia Core. | El Host F13 debe calcular la posición respecto de la nebulosa/tormenta y publicar su estado real. No hay simulación de camuflaje óptico o subespacial complejo. |
| 5. Ciencia e Ingeniería | Handoff existente `f06_science_handoff` pasa de `queued` a `completed` solo con un informe respaldado por observación focal; `f06_host_apply_power` aplica una asignación real **solo tras** aprobación en Core y comprobando cantidad y vencimiento. | Comprobar presupuesto energético global y seleccionar donante corresponde a Ingeniería/Operaciones del Host, no a Sensores; jamás una aprobación lógica crea potencia por sí sola. |
| 6. Secciones de Enterprise-D | Dos entidades Core `f06_section_array` de platillo/cuerpo de batalla, cada una con potencia, integridad, funciones y conectividad. Selección de la mejor matriz **conectada**; no utiliza hardware de una sección separada. Solo instalables con perfil 5, Enterprise-D reconstruida individual. | La separación real, tripulación y sensores de la nave secundaria como **observador diferente** requieren estados de naves independientes del mundo/Host y F13. No se afirma que exista otra nave Core jugable. |
| 7. Validación | Ocho escenarios nativos; cobertura de F06 preexistente y regresión F05, Linux+Windows, pruebas de determinismo, idempotencia y guardado/carga, README, CI. | Pruebas UE5/MSI/LCARS, aceptación de jugador y tiempos reales de simulación permanecen pendientes. |

## Invariantes innegociables

- **No se generan planetas/naves al barrer.** El puerto `f06_host_world_snapshot` conserva autoridad y revela solo contactos detectados. La verdad privada `science_truth` del JSON **no se instala como C++ de producción**.
- **Nunca medir sin observación:** un informe planetario exige un handoff Core existente, un resultado `f06_observation` del **mismo contacto** y que la categoría planeta ya sea observable. La muestra es aportada por el Host de instrumentación confiable, no por Luna/Sol o LCARS.
- **Posible vida ≠ vida confirmada.** La etapa `biological_evidence=3` exige segunda observación independiente y corroboración previa con calidad suficiente. La falta de señales biológicas **no prueba ausencia de vida**.
- **No ejecutar con un mando revocado:** al concluir un barrido el servicio revalida puesto, disponibilidad, contacto y matrices. Cancelaciones persisten y no producen resultados secretos.
- **No duplicar resultados:** `request_key` y `instrument_revision` previenen reenvíos ambiguos. IDs Core no salen por las APIs de observador.
- **No energía de fantasía:** la aprobación F06 se registra por autoridad F04; únicamente un asignador físico confiable aplica una cantidad dentro del límite aprobado. El motor de Sensores no deduce ni fabrica reservas del resto de la nave.
- **No hardware fantasma:** una matriz desconectada persiste pero no contribuye a la detección del observador del casco conectado; el segundo casco necesita su observador legítimo para operar por separado.
- **F04 histórico intacto:** los nuevos campos se añaden al overlay de F06; no se editan ni regeneran fuentes ni oráculos congelados de F04.

## API y esquema

- `desarrollo/integration/f06/include/f06_bis.h`: ABI aditiva nativa.
- `desarrollo/integration/f06/src/f06_bis.inc`: funciones transaccionales sobre el mismo `F04Session` y `Campaign`.
- `desarrollo/integration/f06/src/f06_schema.inc`: rechazo de documentos inválidos antes y después de guardar/cargar.
- `f04_bridge_overlay_patches.json`: enum, relaciones y tipos de Core append-only dentro del build generado, con validación de SHA histórico.

## Plan real de aceptación

1. Ejecutar toda la CI nativa F06 en Ubuntu y Windows del **mismo commit**, incluyendo `bis_science`, `bis_science_corrob`, `bis_timed`, `bis_timed_interrupt`, `bis_environment`, `bis_power`, `bis_sections` y `bis_sections_modes`.
2. Verificar regresiones F02–F05 y los tests ASTRO, referenciales.
3. Registrar el resultado de cada CI; no afirmar PASS hasta que Actions lo reporte.
4. Fase posterior, sin Codex obligatorio para el código: enlazar fuente espacial F13 y proveedor de datos científicos; validar entre dos naves observadoras.
5. Fase posterior **con MSI/Unreal**: consola LCARS, transiciones de visualizador, guardia de ocho horas y fallos de matrices, NullRHI/D3D12.

**Conclusión:** la integración nativa de Ciencia/Operaciones/Sensores puede dejarse preparada y comprobada automáticamente sin MSI. La experiencia jugable, ingeniería energética global y la simulación autónoma completa de F13 no se presumen terminadas.
