# F02-P03 — Secuencias de adaptación y casos de contraste

**Estado:** contratos **de comportamiento exigido**, no clases, API, JSON de transporte ni tests ejecutados. CoreRPG `main@dcfcb83` no dispone de estas operaciones generales. Propietarios: Core para autoridad/estado; Star Trek para dominio; UE5 para presentación.

## S1 — Actor temporal sin destruir una identidad real

**Precondiciones:** contexto de partida único, entidad lógica `EntityId` creada por Core; existe la definición/identidad Trek asociada **cuando el mecanismo aprobado lo permita**.

1. Host consulta identidad lógica con Core; comprueba que existe **en ese mundo**.
2. Host materializa un Actor UE5 a partir del recurso visual correspondiente; guarda una asociación efímera local, no un WorldState paralelo.
3. Actor se descarga por cambio de cubierta, presupuesto de renderizado o distancia.
4. Core conserva entidad, identidad histórica, destino, guardia, tarea y posición lógica **según capacidades que se desarrollarán**.
5. Al regresar el jugador, Host consulta vista vigente y crea **un nuevo Actor** enlazado a la misma identidad; no genera NPC.
6. Si la entidad murió/fue trasladada durante el intervalo, Host usa el estado nuevo y no coloca el Actor por nostalgia.

**Resultados esperados:** al desaparecer Actor no cambia `entity_count`, no aparece nuevo `EntityId` para la misma persona ni se inventa una nueva vida. **Prueba real pendiente F07**; no usar la relación estructural de contención 4.5 como ubicación física.

## S2 — Guardia de Sensores normal (núcleo v0.0.1)

**Precondiciones:** universo ya materializado y persistido; capitán NPC con autoridad de turno; alférez destinado a Sensores, estación operativa; fuente de tiempo de campaña.

```text
Core: verdad preexistente y tiempo
   -> Star Trek: autoridad de capitán NPC (orden)
   -> Core: recepción/validación de orden cuando exista Actions
   -> Host UE5: menú de Sensores + parámetros autorizados
   -> Star Trek: barrido determinista contra datos de mundo
   -> Core: control de acción, recursos, resultado y estado
   -> Core/Star Trek: proyección de detección para observador
   -> Host: presentar sólo observación filtrada
   -> Core: eventos causales y guardado cuando existan
   -> Star Trek: informe y valoración derivados de hechos
```

**Datos origen ya existentes:** `gameplay/orders/starship_order_contract.json` (`order_id`, `issuer_character_id`, `action_id`, `constraints`); `sensor_scan_request_contract.json` (`scan_id`, `observer_id`, `scan_mode`, `resolution`, `filters`); `sensor_result_contract.json` (`contact_id`, `confidence`, `observed`); `operational_event_contract.json` (`event_id`, `causal_refs`, `visibility`). **No inferir que éstos sean los tipos C++/parámetros públicos de Core.**

**Aceptación futura:** quien no ve la verdad del objeto no la recibe como JSON de UI/IA; ordenar no supone completar; reporte válido no cambia identidad del fenómeno; si el puente se descarga el universo sigue.

## S3 — Resultado incierto y guardia tranquila

**Precondiciones:** no hay contactos nuevos detectables, o filtros/resolución/interferencia reducen alcance; `sensor_watchstanding_state_v0.1.json` exige vigilancia pasiva continua.

- Puede transcurrir una guardia entera sin alerta: **prohibido inyectar anomalías para entretener**.
- Se puede detectar sólo una traza, una lectura sin clasificar o un dato parcial, según `resolution_state` del resultado; no asignar nombre, afiliación u hostilidad sin evidencia.
- La detección no crea nave ni firma a posteriori.
- Un contacto perdido por causa desconocida **no** se presume destruido ni oculto; su dossier anterior puede consultarse sólo con permisos, pero no actuar sobre él como si fuera observable en vivo.

**Aceptación futura:** `SW-001`, `SW-003`, `SW-004`, `SW-007`, `SW-009` del fixture `validation/fixtures/sensor_watchstanding_acceptance_v0.1.json`.

## S4 — Orden pendiente y delegación revocada

**Precondiciones:** un NPC o jugador capitán emite orden permitida por delegación en momento T1; antes de aplicar efectos se revoca o expira.

1. Estado admite la orden como **solicitud histórica** a T1 (o queda en cola).
2. Cambia autoridad/turno/recursos a T2 y se registra mediante mecanismo competente.
3. Al ejecutar en T3 se revalida el contexto contemporáneo, no sólo el permiso original.
4. Se rechaza o replantea la acción según norma Trek, conservando que la orden **fue emitida**.
5. No hay doble ejecución silenciosa ni éxito falso si el Host perdió una respuesta.

**Aceptación futura:** cambio revocatorio impide efectos no autorizados; el capitán legal conserva decisión sobre su ámbito, pero límites profesionales/reglamentarios siguen vigentes. Depende de Core 4.10+; no inventar `UniversalCommandSystem`.

## S5 — IA ausente, lenta o incompatible

**Precondiciones:** usuario puede operar consola con menús deterministas y teclado/ratón; ruta IA remota es opcional.

- Si no hay IA, los menús siguen generando solicitudes estructuradas válidas; no bloquear Sensores.
- Si un modelo devuelve una intención no compatible con opciones/autoridad vigentes, no ejecutarla ni crear entidades.
- Si una respuesta de IA llega tras daño, revocación o cambio de observador, **revalidar** antes de aplicar cualquier acción; sin API de reconciliación, permanecer en estado desconocido y no repetir efectos.
- El texto de IA/voz sólo puede referir las propiedades previamente filtradas por observador y con procedencia.
- No registrar transcripciones privadas extensas si no existe política explícita de diagnóstico/consentimiento.

**Aceptación futura:** `F02-T06`, `F02-T07`. Depende de política P04 y del futuro Core/Host; no requiere elegir proveedor IA en P03.

## S6 — Guardado, carga y off-screen

**Precondiciones:** entidad de mundo ya creada, identificador de observador/contacto, guardia y evento causal; WorldState tiene versión de guardado publicada (aún inexistente).

1. Guardar estado **autoritativo** consistente: identidad, semilla/materialización, tiempo, dotación, tareas, observaciones conocidas, eventos e historia.
2. Cerrar Host y reabrir partida por mecanismo validado; cargar de forma atómica.
3. Mantener la misma identidad del NPC/nave/sistema, contactos válidos para el mismo observador, referencias causales y bitácora.
4. Reinstanciar Actors visuales sólo si la escena los necesita; no volver a tirar dados para aspecto/biografía/órbita.
5. Resolver tiempo fuera de escena mediante reglas verificadas, no mediante velocidad aparente de animación ni spawn arbitrario.

**Aceptación futura:** invariantes de `gameplay/persistence/persistent_state_roundtrip_contract.json`, `F02-T05`; falta Core 4.7+, por tanto **NO EJECUTADO**.

## S7 — Sensor→Ciencia y límites de conocimiento

**Precondiciones:** oficial de Sensores ha observado un contacto con `contact_id` relativo al observador. Ciencia tiene capacidad para recibir información según política.

1. Sensores construye `interconsole_data_package_contract.json` con `payload_refs` a resultados observados y `provenance`, no referencia directa a todo el objeto autoritativo.
2. Canal de transferencia valida remitente/receptor y límites de acceso.
3. Ciencia obtiene datos **transmitidos y autorizados**, puede derivar hipótesis y resultado nuevo con origen propio; no adquiere conocimiento secreto por mera transferencia.
4. Evento de transferencia no concede el dossier completo a todo NPC de la nave; si se entrega a mando o terceros, se reevalúan canales y permisos.

**Aceptación futura:** no existe `authoritative_entity_id`, `ground_truth` o `unrevealed_hidden_properties` en payload visible; las inferencias científicas no reescriben datos de Sensores. Depende de Core 4.9/4.10 y es opcional para el primer spike UE5.

## Matriz de casos negativos y niveles de evidencia

| Caso | Bloqueo/observación esperada | Origen de verdad | Estado |
|---|---|---|---|
| Entidad de otra partida con mismo número ID | Rechazar asociación cruzada, no crear clon | Core `EntityId` scoped al mundo | CRITERIO, no probado |
| Actor de la cubierta descargada | Mantener personaje y agenda | Core futuro + Host UE5 | CRITERIO, no probado |
| Contacto perdido | No ofrecer acciones vivas sin reacquisición | Sensores + conocimiento | CRITERIO, no probado |
| Jugador alférez ordena mando reservado | Rechazo/aclaración contextual; no efecto | Autoridad Trek validada | CRITERIO, no probado |
| Capitán NPC actúa mientras jugador no mira | Orden/evento debe continuar sin UI activa | Simulación de Core futuro | CRITERIO, no probado |
| Resultado muestra entidad oculta | Rechazar proyección, fail-closed | Core 4.9 + Trek | CRITERIO, no probado |
| IA inventa nueva detección | Rechazar acción candidata o texto factual | Core + Sensor result | CRITERIO, no probado |
| Guardado corrupto | Rechazar y conservar partida anterior | Core 4.7 futuro | CRITERIO, no probado |
| Desconexión del Companion | El juego PC sigue funcional | Host UE5 | FUTURO fuera del MVP |

**Nota:** no se ha ejecutado ninguna secuencia en Core+UE5; estos casos se convierten en pruebas ejecutables únicamente al alcanzar las fases dependientes.
