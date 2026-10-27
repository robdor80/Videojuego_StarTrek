# F08-P01 — Preparación del escenario de guardia v0.0.1

**13-10-2026 · PREPARACIÓN DOCUMENTAL · NO_EJECUTADO EN CORE/UE5**

## Objeto y límites
Especificar el mínimo escenario reproducible para la primera guardia de **Sensores**. El autor autoriza preparar F08 después del trabajo independiente posible en F07, **sin certificar F07 completada, sin cerrar la puerta de Core y sin modificar el estado global**. F02 sigue como única fase principal EN_CURSO; F08 continúa formalmente PLANIFICADA/PAUSADA para runtime.

No es la Academia, el juego final, un puente Kelvin, un prototipo de combate ni una implementación alternativa de CoreRPG. **Puente visual piloto: USS Sutherland** (DEC-0003). Su modelo 3D no implica fijar una clase ni identidad definitiva para la nave de ficción; anotar esta distinción en el paquete UE5.

## Línea base existente (reutilizar, no duplicar)
- `proyecto/docs/roadmap/master/fases/F07/README.md`: Sutherland elegido, importación/colisiones/recorrido pendientes.
- `proyecto/docs/roadmap/master/fases/F07/P04_PLAN_PRUEBA_UE5.md`: nivel aislado sugerido, controles, foco consola, salida y nueve casos UE07 sin ejecutar.
- `proyecto/docs/roadmap/master/fases/F07/P05_CONTROL_RENDIMIENTO_BUILD.md`: telemetría en MSI y empaquetado.
- `proyecto/docs/roadmap/ship_console_vertical_slice_v0_0_1.md`: cadena de operaciones autoritativas.
- `desarrollo/validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`: 13 invariantes obligatorias, **fixture de aceptación de diseño**.
- `sistemas/gameplay/ship_operations/operational_event_log/sensors_vertical_slice_example.json`: vocabulario y ejemplo de eventos, **no estado real**.
- `proyecto/docs/roadmap/master/fases/F02/PLAN_INTEGRACION_PRIMER_CORTE.md`: adaptadores necesarios y bloqueo Core↔Host.

## Condiciones iniciales reproducibles
| Elemento | Definición para prueba | Autoridad real pendiente |
|---|---|---|
| Campaña | Era `tng_ds9_voyager`, fecha `2372-03-14`, semilla `fixture_sensor_v0_0_1` | Generador y World State de Core |
| Escenario de navegación | Mapa de Sutherland aislado; spawn transitable y estación Sensores interactiva | UE5 en MSI |
| Jugador | Alférez asignado al puesto de Sensores, con identidad persistente, NO capitán | Core identidad/turnos/nombramiento |
| Superior | Capitán NPC con designación y autoridad comprobables | Core dotación/autoridad/órdenes |
| Situación inicial | Sistema y contacto/signaturas de prueba **ya materializados antes de barrer**; sin revelarlos al jugador | Core world/knowledge |
| Orden | Capitán emite orden válida, jugador reconoce; verificar ámbito/tiempo/permiso | Core Actions/autoridad |
| Recursos | Estado de sensores, energía, integridad, interferencia, modo/duración | Core + reglas Trek |
| Bitácora | Orden → acuse → barrido → resultado → informe → eventual evaluación | Eventos append-only y proyección |
| Persistencia | Mismos IDs, estado de orden, conocimiento propio e historial tras cargar | Core save/load |

**No fijar** nombre inventado del capitán, coordenadas de mapa, identidad/cantidad real de contactos, valores de rendimiento o resultados de barrido en un documento de planificación. Los identificadores `captain_001`, `player_001` y `example_ship` del ejemplo de bitácora son demostrativos, no registros Core.

## Secuencia de guion de primera guardia
1. Iniciar/cargar la campaña; materializar el sistema en Core antes de observación y persistir identidades.
2. Comprobar que existe el nombramiento del alférez, su guardia, el capitán NPC, el puente y una orden potencialmente legítima.
3. Entrar al mapa Sutherland, caminar hasta Sensores, fijar foco y activar UI en castellano.
4. Emitir desde Core la orden del capitán y presentarla; reconocerla sin inventar autoridad por texto de IA.
5. Seleccionar el modo y parámetros de barrido; aplicar permisos, costes y validación antes de ejecutar.
6. Resolver detecciones contra firmas preexistentes; mostrar **únicamente** datos visibles para ese observador y etiquetar incertidumbre.
7. Generar informe al capitán y registrar causalidad; el capitán puede valorarlo con reglas Core, no por narración arbitraria de IA.
8. Guardar, cerrar/cargar y comprobar órdenes, entidades, revisiones, contactos e historial, sin doble aplicación.
9. Repetir en desconexión de IA remota: órdenes y resolución deterministas siguen operativas.

## Fallos/negativos obligatorios (sin estados ficticios de éxito)
- Capitán sin autoridad, oficial fuera de guardia o consola dañada: denegar con motivo, sin evento de resultado exitoso.
- Región sin hallazgos: informar ausencia/limitación de detección, no generar una anomalía por guion.
- Propiedades ocultas: no filtrar `entity_id`, verdad completa ni información vedada por error/IA/UI.
- Timeout/caída de IA: fallback seguro; nunca repetir una acción mutadora por incertidumbre.
- Recarga/reintento: preservar identidad y evitar duplicar órdenes, escaneos o eventos.
- Descargar/reaparecer Actor 3D: no eliminar ni reinventar la identidad persistente del NPC.

## Puertas antes de llamar P01 completado en runtime
- F07 UE07-01…09 con evidencias de MSI y licencias/atribución de assets verificadas.
- F02/F03/F04/F05/F06 integradas contra revisión concreta de Core, no solo scripts de referencia.
- Generación/identidad, autorización de orden, resolución Sensor, proyección conocimiento, eventos y persistencia reales.
- Evidencia del build, ejecución offline de IA, logs y plan de pruebas F08-P02…P05.

**Estado P01:** ESCENARIO DOCUMENTADO como preparación; **NO** nave/guardia operacional, **NO** Core/UE5 integrado, **NO** pase de aceptación.
