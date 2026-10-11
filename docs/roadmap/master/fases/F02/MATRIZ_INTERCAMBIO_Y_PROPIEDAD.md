# F02-P02 — Inventario de responsabilidades e intercambio

**Corte:** 2026-10-11. **Tipo:** inventario trazable de requisitos, **NO** schema serializable ni API prometida. Separar lo ya expuesto en Core/main de los modelos conceptuales Star Trek.

## Matriz de entidades y fronteras

| Concepto / dato | Origen canónico | Consumidor | Evidencia Star Trek | Disponibilidad de Core/main |
|---|---|---|---|---|
| `EntityId` de nave, NPC, contacto materializado | CoreRPG / mundo vivo | Star Trek, Host UE5 | `gameplay/ship_operations/starship_state_model.json`, `crew_manifest_model.json` | Sólo creación, existencia, recuento y revisión |
| Definición canónica de tipo/plantilla | Content Pack + catálogo Core | Generación, adaptación | `class_definition_contract.json`, `individual_ship_definition_contract.json` | `DefinitionId` y catálogo de definiciones **sin payload de dominio** |
| Datos Trek: registros, clases, dotación, rangos, destinos | Reglas y contenido de Star Trek | Solicitudes al futuro Core | `gameplay/ship_operations/`, `gameplay/chain_of_command/` | **Sin almacenamiento semántico general hoy** |
| Reloj de campaña, fecha estelar, turnos | Tiempo autoritativo futuro / conversión Trek | NPC, misiones, evaluaciones | `docs/decisions/universal_stardate_system.md`, `gameplay/duty_system/` | **Sin reloj de campaña expuesto** |
| Estado de sensores y sistemas | Estado vivo futuro en Core, semántica en Trek | Resolución Sensores | `gameplay/ship_operations/sensor_resolution/`, `system_state_model.json` | **No disponible en main** |
| Solicitud de barrido y resultado | Adaptación Star Trek; ejecución autorizada futura Core | Sensores, Ciencia, UI | `gameplay/ship_operations/consoles/sensors/`, `tools/simulation/resolve_sensor_scan.py` | `RollAction` **no equivale** a barrido ni acción general |
| Orden, remitente, destinatario, autoridad, delegación | Semántica Star Trek; invariante genérica futura Core | Puente, dotación, NPC | `gameplay/orders/`, `gameplay/chain_of_command/` | **No disponible** sistema genérico de órdenes |
| Evento operacional, causalidad, registro | Core futuro para durabilidad; vocabulario Trek | Evaluación, historiales, IA | `gameplay/ship_operations/operational_event_log/` | **Sin event store** |
| Estado guardable y restaurable | Core (futuro 4.7), transporte en Host | Partidas, carga de cubiertas | `docs/roadmap/ship_console_vertical_slice_v0_0_1.md` | **Sin save/load** |
| Proyección de conocimiento | Core futuro 4.9, políticas Trek | NPC, pantalla, contexto IA | `docs/decisions/authoritative_observable_universe.md` | **Sin proyecciones autorizadas** |
| Instancias 3D, animaciones, streaming de actores | UE5 Host; no autoridad lógica | Jugador | `presentation/`, `ui/`, `assets/ships/` | **Fuera de Core** |
| Progreso académico web / identidad Google | `academiaflota` para web; partida para progreso jugable | Intercambio opcional futuro | `gameplay/careers/academy_path/` | **No integrar aún** |
| Procedencia/modelos/arte generado | NAP / repos de assets | Importación en UE5 | `art_direction/nap/`, `nap/` | **Fuera de Core** |
| Petición en lenguaje natural / voz | IA o entrada de Host produce intención candidata | Adaptador, validador | `ai/runtime_orchestration.md` | **Nunca mutación directa** |

## Identidades que NO deben confundirse

1. `DefinitionId`: identidad global de definición declarativa del contenido; **no** es entidad de campaña.
2. `EntityId`: identidad de instancia **dentro de un WorldState**; el mismo número puede existir en otra partida. La identidad de campaña debe acompañar referencias cuando cruzan contextos; **no se fija aquí un nuevo tipo público**.
3. Identificadores de negocio Star Trek: matrícula (p. ej. NCC), puesto, rango, contacto sensorial, escena 3D. No asumir correspondencia 1:1 con `EntityId`.
4. Los contactos observados son **proyecciones**. Conocer una señal o marcador no implica acceso a la entidad real ni conocimiento de su identidad.

## Flujo semántico mínimo: alférez de Sensores

1. El universo/materialización existe **antes** de escanear.
2. Una autoridad NPC emite orden válida según normativa Star Trek. El jugador recibe sólo lo permitido por su conocimiento.
3. La UI reúne parámetros; el adaptador produce solicitud estructurada **sin publicar un endpoint inexistente**.
4. El runtime autoritativo, cuando esté disponible, revalida actor, puesto, recursos, versión/revisión, permisos y consecuencias.
5. Sensores calcula observables y límites de incertidumbre; Ciencia podrá analizarlos después, no confundir funciones.
6. Los hechos/eventos se registran y persisten (cuando las fases Core correspondientes existan); UI recibe **proyección** filtrada.
7. La IA puede redactar el informe desde datos autorizados; no revelar ground truth secreto.
8. Descargar la cubierta elimina actores visuales, **no** la entidad, dotación ni su historia.

## Invariantes obligatorios para contratos futuros

- No dos `WorldState` para la misma partida; no transportar punteros `Actor` dentro de Core.
- Ningún evento registrado concede conocimiento universal.
- No se cumplen órdenes sin validar autoridad contextual y contexto actual.
- No se reasignan IDs al cargar: preservar identidad y causalidad.
- Nada de doble puesto incompatible simultáneo para un personaje.
- Host y servicios remotos no escriben directamente estado persistente.
- Si Core no puede confirmar una capacidad, no simular éxito autoritativo; las pruebas offline deben señalarse como simuladas.

**Estado de P02:** requisitos inventariados; contratos de intercambio definitivos pendientes de 4.5–4.12 y contrastación de consumidores. No declarar `CONTRATO_VALIDADO` para campos que no tiene el Core.
