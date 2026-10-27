# F02-P03 — Diseño de adaptadores y fronteras de integración

**Corte de auditoría:** 11-10-2026 · **Estado P03:** **ESPECIFICACIÓN DOCUMENTAL COMPLETA / CONTRATO EXTERNO PENDIENTE**. Este documento describe **responsabilidades y requisitos de adaptación**, **no** métodos, ABI, protocolos binarios, schemas Core ni una integración ejecutada. **F02 no está cerrada.**

## Versiones realmente contrastadas (no intercambiables)

- [CoreRPG `main`](https://github.com/robdor80/CoreRPG/tree/dcfcb83c9853e005b5450bd39e0ba693cb91e257) `dcfcb83c9853e005b5450bd39e0ba693cb91e257`: `EntityId` (`uint64_t`; cero inválido; identidad dentro de un `WorldState`), `WorldState::create_entity/contains/entity_count/revision`, `DefinitionId`, `ContentCatalog::create`, `RollAction` no mutante y Content JSON `0.1.0` opcional.
- [Rama 4.5 de Core](https://github.com/robdor80/CoreRPG/tree/2a3da891d8c56e9868c7bd67dbeb6041509df2ce) `2a3da891d8c56e9868c7bd67dbeb6041509df2ce`: incorpora en código de rama enumeración y contención opcional; **no está en `main`**, ni establece residencia, puesto, ubicación espacial o propiedad.
- [ADR-0002 de Core](https://github.com/robdor80/CoreRPG/blob/dcfcb83c9853e005b5450bd39e0ba693cb91e257/docs/adr/0002-platforms-presentation-companion.md): Star Trek es Host UE5/Windows, independientes los actores 3D de las entidades; Nimroel 2D y Companion no obligan a convertir Core en UE5.
- [Regla multiuniverso de Core](https://github.com/robdor80/CoreRPG/blob/dcfcb83c9853e005b5450bd39e0ba693cb91e257/docs/multi-universe-architecture.md): no crear un segundo motor, framework/plugin API especulativo ni lógica específica Trek en el núcleo.

Las capacidades posteriores de Core 4.6 (reglas), 4.7 (guardado), 4.8 (población), 4.9 (conocimiento), 4.10 (acciones/simulación), 4.12 (contexto IA) y 4.14 (UE5) son **dependencias futuras**, no funciones implementadas. La ausencia de PR abierta de 4.5 no demuestra que se haya abandonado; sólo documenta la situación remota del corte.

## 1. Arquitectura lógica acordada

```text
                   TECLADO / RATÓN / CONSOLA UE5
                               |
                         HOST WINDOWS UE5
                    entrada, renderizado, IO, red
                               |
                       capa de adaptación Trek
            normalización / contenido / doctrina / permisos
                       (sin autoridad paralela)
                               |
                    capacidades públicas de CoreRPG
                 IDENTIDAD → ESTADO → REGLAS → ACCIONES
                         → EVENTOS → PERSISTENCIA
                               |
                  proyección autorizada por observador
                               |
                    UI UE5 / NPC / diálogo IA
```

El dibujo expresa **responsabilidades a futuro**, no un pipeline técnico implementado completo. **Únicamente CoreRPG acepta cambios de estado autoritativo.** Un módulo de reglas Trek puede proponer efectos y comprobar invariantes Trek dentro de un mecanismo acordado con Core, nunca modificar libremente la memoria de WorldState. UE5/Blueprint, IA remota, consola de sensores y registros de demostración no son motores alternativos.

La adaptación debe residir junto al **Host Star Trek/UE5 o una biblioteca de integración específica**. Evitar añadir referencias a Unreal, vocabulario Trek, HTTP, JSON de sensores o accesos de red al target `CoreRPG`. El contrato **no obliga a utilizar herencia, interfaces virtuales, subsistemas UE, RPC, ECS, registries o plugins**; escoger la tecnología tras el spike real.

## 2. Inventario operativo de adaptadores

| ID | Responsabilidad | Datos Trek fuente | Resultado expuesto, sin inventar API | Dependencia / estado |
|---|---|---|---|---|
| **ADP-01 Identidad** | Mantener vínculo controlado instancia lógica–referencia Trek–Actor temporal | `sistemas/universe/generation/persistent_entity_identity_contract.json`; `starship_state_model.json` | Referencia de entidad válida en mundo, nunca `AActor` como identidad | Core `main` sólo identidad básica; unión de conceptos pendiente |
| **ADP-02 Contenido** | Validar referencias declarativas y separar catálogo de instancia | `sistemas/gameplay/ship_operations/class_definition_contract.json`, `individual_ship_definition_contract.json` | Definición identificable; propiedades Trek cuando exista modelo extensible | `ContentCatalog` actual sí; payload/instanciación no |
| **ADP-03 Tiempo y actividad** | Reloj exacto, turnos, ocupación, simulación sin escena | `proyecto/docs/decisions/universal_stardate_system.md`; `activity_schedule_model.json`; `duty_watch_state.json` | Estado de guardia consistente + fecha estelar calculada para UI | Core 4.8/4.10 futuros |
| **ADP-04 Orden y autoridad** | Traducir órdenes Trek y revalidar autor, estación, puesto, delegación, recursos y momento | `sistemas/gameplay/orders/starship_order_contract.json`; `sistemas/gameplay/chain_of_command/` | Aceptación, aclaración, rechazo o ejecución referenciable; nunca ejecutar texto | Core 4.6/4.10 futuros |
| **ADP-05 Sensores** | Aplicar mecánica Trek determinista a firmas preexistentes | `sensor_scan_request_contract.json`; `sensor_result_contract.json` | Resultado observado por `observer_id`, no verdad oculta | Referencia Trek sí; integración Core 4.9/4.10 pendiente |
| **ADP-06 Evento** | Conservar causalidad, identidad de origen y bitácora append-only | `operational_event_contract.json`, `event_type_catalog.json` | ID de evento y referencias; no evaluaciones automáticas ni conocimiento implícito | Core 4.7/4.10 futuros |
| **ADP-07 Conocimiento** | Filtrar antes de enviar a cliente/UI/IA; dosificar revelación | `visibility_projection_rules.json`; `contact_dossier_model.json` | `contact_id` relativo a observador y campos detectados, sin IDs de verdad interna | Core 4.9 futuro |
| **ADP-08 Guardado y continuidad** | Guardar/cargar identidad, agenda, estado observable, historia y semillas sin re-randomizar | `sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json` | Restauración coherente e íntegra; nada de serializar Actors como campaña | Core 4.7 futuro |
| **ADP-09 Puente UE5** | Traducir entrada/resultado, asociar Actor visible temporal, manejar hilo/ciclo de vida | `audiovisual/presentation/`, `audiovisual/ui/`, ADP-01, ADR-0002 Core | Actor y HUD renovables sin tocar hechos; interacción en teclado/ratón | Spike real C++/UE5 y ABI, Core 4.14 futuro |
| **ADP-10 IA e intérprete** | Petición remota autorizada, interpretación/propuesta, revalidación, fallo seguro | `sistemas/ai/runtime_orchestration.md`; `computer_request_contract.json` | Candidato no confiable, o texto derivado de proyección; nunca efectos directos | Core 4.12 futuro para Context Builder; **IA no obligatoria para prototipo** |
| **ADP-11 Interconsolas** | Transferir observaciones con procedencia y permisos | `interconsole_data_package_contract.json` | Paquete Sensor→Ciencia de hechos ya observados, no nuevos secretos | Core 4.9/4.10 futuros; opcional para primer corte |
| **EXT-01 Academia/NAP/Companion** | Mantener fronteras: estudio web, recursos visuales, tablet opcional | `sistemas/gameplay/careers/academy_path/`; `audiovisual/art_direction/nap/`; ADR-0002 Core | **Sin dependencia runtime mínima** y sin mutación paralela | F10/F14/Companion futuro; NO es adaptador obligatorio en F08 |

**Registro verificable:** [MAPA_ADAPTADORES_P03.json](MAPA_ADAPTADORES_P03.json) recoge propietario, consumidores, fases, dependencias, riesgos y puertas de cada ADP. [P02](MATRIZ_INTERCAMBIO_Y_PROPIEDAD.md) conserva las 24 fuentes auditadas; no mover ni copiar sus contratos a un segundo esquema de producción.

## 3. Reglas exactas de frontera

### Identidad, instanciación y representación (G01, G04, G09)

- `PackId` nombra el paquete, `DefinitionId` la definición inmutable, `EntityId` un objeto vivo del `WorldState` actual. `ship_id`, `character_id`, `registry`, `contact_id`, `event_id` y `Actor` tienen semánticas separadas.
- **No inferir por coincidencia numérica o textual** que dos referencias corresponden a la misma identidad. El convenio de mapeo de claves, referencias cruzadas y su persistencia está pendiente de aceptación Core–Star Trek.
- La **contención 4.5**, incluso cuando se integre, modela relación estructural opcional: no es coordenada 3D, empleo, turno, propiedad, cama, hogar ni actividad.
- Entidad no representada 3D sigue existiendo. Destruir un Actor o descargar una cubierta no implica despido, fallecimiento, desaparición del NPC ni reasignación de ID.
- Si el Core no puede demostrar instancia viva y roundtrip, **no** presentar el bind de Actor como integración persistente terminada.

### Reloj y resolución temporal (G02, G04)

- Verdad temporal: marca exacta de tiempo de campaña; la **fecha estelar es derivada**, siguiendo `proyecto/docs/decisions/universal_stardate_system.md` (1.000 unidades/año de campaña).
- Establecer más adelante, con Core, formato de timestamp, resolución mínima, origen, orden total de eventos concurrentes y control de avance. No introducir hoy una convención técnica irreversible.
- La guardia no fuerza posición física: `watch_id`, asignación, localización, viaje y descanso conservan significados diferentes. Ausencia visual no congela el turno simulado.

### Orden, autoridad y fallos de ejecución (G05, G11)

- **Tres conceptos:** intención en lenguaje natural → orden Trek estructurada → acción validada. Una orden puede quedar `queued`, `refused` o `clarification_required`; no debe confundirse emisión con ejecución exitosa.
- La jerarquía de Flota, Primera Directriz, control de capitán, delegación o permisos médicos son **específicos Trek**. Un eventual Core genérico únicamente soportará invariantes de autoridad si quedan justificadas y acordadas.
- Los permisos han de comprobarse **al aplicar efectos**, no sólo al pulsar botón: una revocación, cambio de turno, daño o cambio de objetivos puede invalidar una solicitud pendiente.
- Reintento tras timeout: **estado desconocido** hasta reconciliar con fuente autoritativa; no presumir idempotencia, no aplicar dos veces una acción y no elegir formato público de correlation ID ahora.
- Si una regla prohibe actuar, registrar denegación/historia sólo cuando exista soporte autoritativo; no inventar una aceptación local para animar el puente.

### Sensores, conocimiento, interconsolas (G06, G08)

- El sistema astronómico y las firmas **existen antes del escaneo**. `scan_id` identifica operación; `observer_id` al observador; `operator_id` al profesional opcional; `contact_id` es persistente para ese observador, no ID del objeto real.
- `sensor_result_contract.json` prohíbe entregar al jugador `authoritative_entity_id`, `ground_truth`, `unrevealed_hidden_properties`. La filtración debe evitarse **antes de construir el DTO de UI/IA**, no sólo ocultarse mediante CSS/Widget.
- Las propiedades `resolved_hidden_properties` sólo pueden incluir hallazgos efectivamente revelados y elegibles; no volcar indiscriminadamente `hidden_properties`.
- Pérdida de contacto ≠ destrucción, invisibilidad deliberada ni salto warp sin prueba; recuperar expediente histórico no habilita acciones de seguimiento “en vivo” imposibles.
- `event_id` crea rastro causal, no concede automáticamente conocimiento a NPC; compartir con Ciencia es un paquete de **observaciones ya conocidas** y conserva procedencia.

### Persistencia y versiones (G07)

- Persistir ID, revisiones, materialización/semillas, relaciones, resultados relevantes, conocimiento, dotación, tiempo y eventos según dependencias; la versión del savegame es **distinta** del Content Contract `0.1.0` y del build UE5.
- Guardar/cargar ha de preservar hechos y rechazar datos corruptos/incompatibles sin cambiar parcialmente la partida. Política de migración y representación binaria: **no decididas** hasta Core 4.7.
- La presentación reconstruye escenas y Actors desde el estado persistente, no al revés. No agregar aquí SQLite propia ni guardar un segundo WorldState en Star Trek.

### Host UE5 e IA (G09, G10, G11)

- Core es biblioteca C++20 estática **sin promesa de ABI estable**; el Host deberá probar toolchain, CRT, configuración, enlace, excepciones, ownership, hilos y duración de referencias antes de estabilizar adaptadores.
- Hasta que Core publique reglas de concurrencia, **no** asumir thread-safety; el Host serializará sus invocaciones a estado mutable y reflejará resultados a Game Thread para UI/Actors, propuesta pendiente de spike técnico.
- IA y conexiones remotas pertenecen al Host: sólo contexto autorizado, interpretaciones no confiables, y degradación sin bloquear controles deterministas de Sensores. No es necesario elegir modelo de IA para cerrar diseño de P03.
- `academiaflota` es una web educativa con perfiles propios; identidad de Google/web y `EntityId` de partida no se fusionan por coincidencia de usuario. El progreso de Academia jugable se aborda en F10, no en esta fase.
- Assets NAP/Rob3D, uniformes o cubiertas son recursos visuales; no originan por sí mismos personajes persistentes.

## 4. Flujos y secuencias de contraste

[SECUENCIAS_Y_CASOS_P03.md](SECUENCIAS_Y_CASOS_P03.md) descompone:
1. Ciclo de identidad lógica ↔ Actor UE5;
2. Guardia normal `NPC capitán → orden → barrido → informe → evento`;
3. Respuesta sin contacto o con lectura parcial;
4. Revocación de autoridad durante una orden pendiente;
5. IA caída/retrasada y cambio de escenario;
6. Guardado/carga, continuidad del contacto y dotación;
7. Consulta Sensor→Ciencia sin divulgar mundo oculto.

**Estos casos son criterios de aceptación futuros y nunca pruebas ya ejecutadas.** El motor Python de referencia Trek no sustituye la validación Core ni la ejecución UE5.

## 5. P03: brechas heredadas de P02 y propietarios

| Gap | Propuesta de cierre **de diseño**, no de API | Pendiente real para contrato validado |
|---|---|---|
| G01 IDs | Ámbitos separados y referencias explícitas | Acuerdo Core–Star Trek de enlace/instanciación y continuidad |
| G02 reloj | Timestamp de campaña único; fecha estelar derivada | Precisión/serialización/orden de eventos en Core |
| G03 contenido | Definición ≠ instancia; Catálogo sólo envelope | Payload Trek y compatibilidad con contrato futuro acordados |
| G04 mundo/LOD | Actor ≠ entidad; actividad/schedule/ubicación distintos | APIs 4.5+/simulación y pruebas offscreen |
| G05 acciones | Revalidación al ejecutar; cadena de mando Trek | API Core 4.10 y mecanismo de reglas/efectos |
| G06 conocimiento/eventos | Proyección obligatoria antes de UI/IA; causales append-only | Knowledge 4.9 y event store 4.10/4.7 |
| G07 save/load | Roundtrip y migraciones atómicas como requisito | Persistencia Core 4.7 y tests |
| G08 contactos | `contact_id` relativo al observador; estados perdidos honestos | Persistencia/observación 4.7/4.9 |
| G09 UE5 | Binding visual temporal, Core ajeno a UObject | Spike Windows/UE5 real F07 |
| G10 web/Academia | Web educativa ≠ identidad/progreso de partida | Acuerdo opcional F10, no bloquea v0.0.1 |
| G11 fallos/IA | Fail-closed, candidato no confiable, consulta de resultados | Acción Core/reconciliación 4.10 y pruebas Host |

Los gaps G01–G09 y G11 **no se declaran resueltos técnicamente**: tienen dueño, límite y requisito de cierre. G10 tiene su frontera de arquitectura delimitada y permanece pendiente funcional futura. Remitir las decisiones de tecnología/contrato a [handoff a Core](SOLICITUD_COORDINACION_CORE_P03.md).

## 6. Alcance obligatorio para la primera prueba interna

**v0.0.1 = guardia interna de Sensores**, no lanzamiento ni misión final del juego. Requiere para **integración real**: ADP-01 + ADP-03 (tiempo/guardia mínima) + ADP-04 + ADP-05 + ADP-06 + ADP-07 + ADP-08 + ADP-09. ADP-02 será necesario para contenido escalable, pero el primer test podrá usar un fixture autoral fijo sin fingir instanciación genérica. ADP-10 (IA), ADP-11 (transferencia ampliada), Companion, Academia completa, todas las consolas y Dama definitiva **no son requisitos para comenzar el spike visual/identidad**.

La secuencia productiva aún depende de versiones reales Core 4.5–4.10 y UE5; el prototipo con datos de prueba debe identificarse de forma inequívoca como simulado. La selección Galaxy/Sovereign/Odyssey para Imperator sigue siendo decisión del autor de F01 (PR #2), no una suposición arquitectónica de P03.

## 7. Validación y puerta de cierre

- **Ejecutado como revisión documental:** inspección de códigos `main` y rama 4.5, Core ADR-0002 y reglas multiuniverso; P02 con 24 fuentes verificadas; matriz P03 consistente, fuentes enlazadas, separación de identidad/conocimiento/persistencia.
- **No ejecutado:** compile/link C++/UE5, validación API 4.5 integrada, tests de órdenes/permisos, Knowledge, save/load, IA en producción, motor de simulación y end-to-end v0.0.1.
- **Cierre de especificación P03:** entregables, responsables, adaptadores, gaps, secuencias, handoff y evidencias, **pendiente de contraste formal con Core y Host**. No etiquetar `CONTRATO_VALIDADO` hasta que Core exponga interfaces reales y se cotejen con esta matriz.
- No merge con `main` ni cambio a `ESTADO_GLOBAL.json` por adelantado mientras F01 siga pendiente de DEC-0001.

Referencias: [auditoría P01](AUDITORIA_CORE_RPG_2026-10-11.md), [matriz P02](MATRIZ_INTERCAMBIO_Y_PROPIEDAD.md), [fallos P04](FALLOS_VERSIONES_Y_PRUEBAS.md), [plan P05](PLAN_INTEGRACION_PRIMER_CORTE.md), [criterios comunes](../../CRITERIOS_DE_CIERRE.md).
