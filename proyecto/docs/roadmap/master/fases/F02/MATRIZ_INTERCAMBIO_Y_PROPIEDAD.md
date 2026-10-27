# F02-P02 — Matriz verificada de datos, identidades y límites de integración

**Estado del paso:** **CERRADA COMO INVENTARIO AUDITADO** a 2026-10-11. **No significa CONTRATO_VALIDADO con CoreRPG, ni integración ejecutada**. F02 continúa abierta. Este inventario sustituye la primera matriz preliminar.
**Evidencia indexada:** [INVENTARIO_INTERCAMBIO_P02.json](INVENTARIO_INTERCAMBIO_P02.json). Se comprobaron en GitHub **24 fuentes JSON (23 contratos/modelos y 1 fixture), 73 selectores existentes**, **5 cabeceras del Core/main** y la decisión de reloj/fecha estelar (verificación remota, no compilación local).

## Línea base fija y límites

| Fuente | SHA / evidencia | Interpretación |
|---|---|---|
| `robdor80/Videojuego_StarTrek` `main` | `164be98ab02d81ac9580160e555e75a10e6d489f` | Contratos Star Trek usados para esta auditoría |
| `robdor80/CoreRPG` `main` | `dcfcb83c9853e005b5450bd39e0ba693cb91e257` | API efectiva mínima: `EntityId`, `WorldState`, `DefinitionId`, `ContentCatalog`, `RollAction` |
| `CoreRPG` `feat/generic-world-state` | `2a3da891d8c56e9868c7bd67dbeb6041509df2ce` | Avance 4.5 **NO integrado en main** |
| `CoreRPG` Content Contract | `0.1.0`, `desarrollo/schemas/content/0.1.0/` | Contrato declarativo de **desarrollo/manifests/definiciones sin payloads de dominio**. No confundir con `schema_version` de JSON Star Trek |
| `proyecto/docs/decisions/universal_stardate_system.md` | blob `7dcc26bfe717e65bcdd33b8a63fb4b99d4ba514e` | El timestamp exacto de campaña es autoritativo; fecha estelar derivada: 1.000 unidades/año |

**El índice JSON es una tabla de procedencia y selectores de campos; NO es un esquema de intercambio nuevo.** Cada registro remite al archivo y al hash Git blob de su propia versión en `main`, evitando copiar silenciosamente versiones incompatibles.

## Catálogo por familia, con propiedad y exposición

| IDs auditados | Familia / contratos originales | Propiedad lógica | Qué cruza hacia Core, Host o IA | Estado en CoreRPG/main |
|---|---|---|---|---|
| ID-01…ID-03 | Identidad persistente; entidad observable; sistema generado, en `sistemas/universe/generation/` | Trek: canon, semilla, firmas y atributos; Core: identidad viva y autoridad | `entity_id`, `origin_seed`, contexto de generación, verdad interna y observables **separados** | Identidad básica disponible; mundo rico NO |
| ID-04…ID-06 | Personaje vivo, nave viva, manifiesto, en `sistemas/gameplay/characters/` y `sistemas/gameplay/ship_operations/` | Trek: puestos, clases, biografía y dotación; Core: estado mutable único | Referencias cruzadas de nave/miembro/puesto, ubicación, historial, estado de servicio | Fichas y dotación NO |
| TM-01…TM-04 | Agenda, asignación, guardia, vigilancia pasiva, en `sistemas/gameplay/characters/`, `sistemas/gameplay/duty_system/` | Trek: doctrina de guardias; Core: exclusividad/tiempo y simulación | `schedule_item_id`, `starts_at`, `ends_at`, `watch_id`, `duty_assignment_id`, estado; continuidad off-screen | Reloj/simulación NO |
| AC-01…AC-04 | Orden nave/tarea y petición/resultado de barrido, en `sistemas/gameplay/orders/` y `ship_operations/sensor_resolution/` | Trek: mando y sensores; Core: ejecutar/validar estado | `order_id`, `issuer_character_id`, `target_entity_id`, `scan_id`, `observer_id`, operaciones/resultados estructurados | `RollAction` no es framework general; NO |
| AU-01…AU-03 | Delegación, visibilidad de eventos y acceso al ordenador | Trek: mando, clasificación y privilegios; Core: límites actor-relativos | Contexto de autoridad, control_mode, vigencia/revocación, scopes y permisos; **nunca acceso libre a la verdad** | NO |
| EV-01…EV-03 | Bitácora operacional, paquete interconsola y dossier de contacto | Trek: tipos de hecho y transferencia; Core: causalidad/almacenamiento y conocimiento | `event_id`, `occurred_at`, `actor_refs`, `subject_refs`, `causal_refs`, `package_id`, `contact_id` | Sin event store ni Knowledge |
| PS-01 | Roundtrip de `sistemas/gameplay/persistence/` | Core futuro: serializar/restaurar hechos; Trek: invariantes de identidad | Estado, relaciones, referencias, historial, semilla/reglas y versiones | NO |
| AI-01 | Petición del ordenador | Host/IA: intención candidata; Core: permiso/ejecución | `request_id`, `requester_id`, `resolved_intent`, `authorization_result`; no texto con autoridad | NO |
| CR-01 | Expediente profesional | Trek: semántica carrera; Core: historia de hechos cuando exista | `event_id`, `source_event_id`, ascensos/destinos/evaluaciones derivadas | NO |
| QA-01 | Fixture de aceptación de v0.0.1 | Verificación de diseño Trek | Oráculo de 13 invariantes del corte; no datos de producción ni runtime | NO EJECUTADO como E2E |

## Distinciones de identidad: ocho espacios NO intercambiables

| Espacio / clave observada | Origen real | Regla innegociable |
|---|---|---|
| `PackId` | Core Content Pack | Identifica la línea de un paquete, no un mundo ni una nave viva |
| `DefinitionId` | Core `ContentCatalog` | Definición reutilizable; no instancia; **no existe puente general de instanciación** |
| `EntityId` | Core `WorldState` | Entero de 64 bits no cero; existencia y unicidad **dentro del mundo**, no global entre campañas |
| `character_id`, `ship_id` | Modelos Trek | Referencias semánticas de personaje/nave; su representación y vínculo con `EntityId` requieren convenio concreto, **no asumir equivalencia automática** |
| Matrícula `registry` y `ship_definition_id` | Identidad Trek de nave | Identificador de negocio/plantilla; ni un registro NCC ni un nombre sustituyen la identidad viva |
| `contact_id` | Sensores / dossier del observador | Estable **para ese observador**, no equivale al `authoritative_entity_id`; visibilidad derivada |
| `order_id`, `task_order_id`, `scan_id`, `package_id` | Operaciones Trek | Identifican hechos y solicitudes con ciclo de vida propio; **no son EntityId por definición** |
| `event_id`, `observation_id`, `request_id` | Bitácora, memoria, ordenador | Referencias causales/auditoría, con alcances de unicidad aún por concretar para Core; no usar el asignador de entidades a ciegas |

**Gap P03-G01:** algunos modelos Trek describen IDs como `unique`/`globally stable`, mientras Core solo garantiza `EntityId` en un `WorldState`. No redefinir globalidad ni formato sin acuerdo. El modelo `starship_state_model.json` describe `ship_definition_id` y `registry` sin declarar `ship_entity_id` explícito en `identity_fields`; en cambio `crew_manifest_model.json` refiere `ship_id` como `ship_entity_id`. Se necesita convenio de enlace, **no una corrección silenciosa del canon**.

## Flujos concretos de información (diseño, no API)

| Flujo | Fuente y campos existentes | Consumidor y restricciones |
|---|---|---|
| **Creación / instanciación** | `generated_system_contract`: `campaign_seed`, `campaign_date`, `system_id`; `persistent_entity_identity_contract`: `origin_seed`, `entity_id` | Core registra identidad y vida una vez; reconsulta no vuelve a generarla. El vínculo definición→instancia no existe en Core/main |
| **Nave y dotación** | `starship_state_model`: `crew_manifest`, `commanding_officer`; `crew_manifest_model`: `ship_id`, `character_id`, `position_id`, `shift_id` | Consulta de puestos/guardia por identidad estable. El 3D no tiene autoridad sobre listas de tripulación |
| **Agenda/guardia** | `activity_schedule_model`: `schedule_item_id`, `time_window_or_anchor`; `duty_watch_state`: `starts_at`, `ends_at`; `duty_assignment_model`: `starts_at`, `ends_at` | Core deberá impedir ocupaciones físicas incompatibles; el turno indica presencia esperada, no teletransporta NPC |
| **Tiempo único** | Reloj exacto definido en `universal_stardate_system.md` | `issued_at`, `created_at`, `occurred_at`, `received_at`, `first_seen`, `last_seen` usan **tiempo de campaña** cuando aplique; formato/precisión exactos aún requieren contrato |
| **Orden→acción** | `starship_order_contract`: `order_id`, `issuer_character_id`, `issuer_position_id`, `issuer_authority_context`, `target_station_id`, `action_id`, `constraints` | Validar autoridad, disponibilidad, recursos, reglas y estado actual antes de ejecutar. `outcome_states` actuales de Trek no implican API Core existente |
| **Escaneo** | `sensor_scan_request_contract`: `scan_id`, `observer_id`, `operator_id` opcional, `range_mode`, `sensor_profile` | Motor resuelve frente a firmas materializadas; no genera el objetivo por petición ni usa IA como ejecutor |
| **Resultado público** | `sensor_result_contract`: `contact_id`, `confidence`, `observed`, `observed_signatures` | UI/IA recibe observación filtrada. **Prohibidos** `authoritative_entity_id`, `ground_truth`, `unrevealed_hidden_properties` |
| **Evento causal** | `operational_event_contract`: `event_id`, `occurred_at`, `actor_refs`, `subject_refs`, `causal_refs`, `visibility` | Registro append-only; la corrección es nuevo evento con `correction_of_event_id`, no reescritura; evento registrado no da conocimiento universal |
| **Sensor→Ciencia** | `interconsole_data_package_contract`: `package_id`, `source_system`, `target_system`, `payload_refs`, `provenance` | Ciencia recibe únicamente observaciones transferibles; interpreta sin apropiarse de la fuente de verdad de Sensores |
| **Memoria/contacto** | `contact_dossier_model`: `contact_id`, `observations`, `known_facts`, `classification_history` | Mantener procedencia, contradicciones y pérdidas de contacto sin inventar causas o identidades |
| **Permiso contextual** | `access_control_rules`: `character_id`, `position`, `duty_status`, `clearance`, `requested_function`, `temporary_authorization` | Autenticación != autorización; rango no concede lectura médica/privada; revocar delegación bloquea acciones posteriores |
| **Guardado/carga** | `persistent_state_roundtrip_contract`: `entity_id`, `entity_type`, `rules_version`, `generator_version`, `seed_provenance`; enlaces a historia y memoria | Save/load atómico y versionado en Core futuro; sin regenerar identidades. No confundir con almacenar Actors |
| **Informe/carrera** | `service_record_model`: `source_event_id`, `event_type`, `authority_id` | El expediente selecciona hechos elegibles, no incorpora íntegro un log operacional ni recalcula realidad |
| **Lenguaje natural** | `computer_request_contract`: `request_id`, `requester_id`, `resolved_intent`, `authorization_result` | IA propone; Core verifica y devuelve resultado; contexto permitido por usuario/personaje. Fallback manual determinista |

## Incidencias/decisiones a elevar a F02-P03, sin bloquear el inventario

| ID | Severidad | Contrato pendiente / discrepancia | Responsable propuesto |
|---|---|---|---|
| **P03-G01** | ALTA | Asociación entre `EntityId` scoped por mundo, claves Trek, `DefinitionId`, matrículas, `contact_id` y referencias causales. Definir ámbito y vida útil de cada ID sin hacerlos intercambiables | Core + Star Trek |
| **P03-G02** | ALTA | Fecha/hora exacta: tipo serializable, precisión, zona y orden de sucesos; presentación de fecha estelar independiente | Core + Star Trek |
| **P03-G03** | ALTA | Extensión de Content Pack para propiedades Trek: Core `0.1.0` carece de payloads de dominio | Core + Star Trek |
| **P03-G04** | ALTA | Estado vivo, agendas, contención/LOD y simultaneidad. 4.5 no está en main y 4.8+ es posterior | Core |
| **P03-G05** | ALTA | Orden/tarea/acción: identidades, precondiciones, idempotencia cuando sea necesaria, resultado, revisión, autoridad contextual y revocación | Core + Star Trek |
| **P03-G06** | ALTA | Event store causal, visibilidad real y proyecciones anti-filtración; no exponer `ground_truth` ni memoria privada por accidente | Core + Star Trek |
| **P03-G07** | ALTA | Save/load, versionado, migraciones, reversión/rechazo atómico, historia y procedencia estable | Core |
| **P03-G08** | MEDIA | Estatus de observaciones/contactos perdidos; reconexión de referencias de contacto tras carga y seguimiento fuera de escena | Star Trek + Core |
| **P03-G09** | MEDIA | Adaptación UE5: `EntityId ↔ Actor`, ownership, hilos/ABI y descarte visual sin tocar historia | Host UE5 + Core |
| **P03-G10** | MEDIA | Delimitar identidad/progreso web de Academia, la partida real y datos privados; no hay sincronización acordada | Star Trek + Academia |
| **P03-G11** | ALTA | Fallos/timeouts/respuestas IA tardías; distinguir solicitud, aceptación, ejecución y confirmación persistente | Host + Core |

**No se decide aquí** ABI, serialización final, payload del Core, contador global de IDs, formato de `event_id` o token de deduplicación. Esas cuestiones se resuelven en P03/P04 con Core real, para evitar contratos imaginarios.

## Verificación y criterios de cierre P02

- **Sí verificado:** lectura de las 24 fuentes JSON de Star Trek desde la línea base; comprobación de existencia de **73 rutas de campos/selectores** (cero ausentes); lectura de los cinco headers Core publicados y tres afirmaciones del documento de fecha estelar. Todos los hashes de fuentes están en `INVENTARIO_INTERCAMBIO_P02.json`.
- **Sí verificado:** Core/main expone `WorldState` mínimo; `RollAction` no muta el mundo y no equivale a escaneos; los `schema_version` fuente tienen versiones independientes del Content Contract.
- **No ejecutado:** CMake/CTest local, pruebas E2E, carga real de guardados, persistencia, simulación fuera de escena, observadores Core ni integración UE5.
- **Cierre preciso:** **F02-P02 cerrado a nivel inventario y trazabilidad**; todas las API/interfaces para implementación siguen bloqueadas o sujetas a validación en P03–P05. No se ha modificado CoreRPG, canon, modelos JSON ni `ESTADO_GLOBAL.json`; la F01 permanece abierta.

Relacionados: [auditoría P01](AUDITORIA_CORE_RPG_2026-10-11.md), [adaptadores P03](ADAPTADORES_Y_FRONTERAS.md), [plan P05](PLAN_INTEGRACION_PRIMER_CORTE.md) y `proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md`.
