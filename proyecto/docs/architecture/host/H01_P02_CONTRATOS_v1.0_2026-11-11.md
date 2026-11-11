# H01-P02 — Contrato de operaciones y errores del HOST v1.0

Estado: DISEÑO VERSIONADO, no API compilada. Propietario del envoltorio: HOST. Propietario de decisiones de negocio: F04/F05/F11/CoreRPG. Versión host_contract 1.0. Registro estructurado: H01_REGISTRO_CONTRATOS_v1.json.

## Envoltura lógica común

Todos los mensajes llevan host_contract, session_generation, correlation_id y operation. Las mutaciones llevan expected_core_revision, actor/resolved_principal **derivados internamente del vínculo de campaña** y, cuando el dominio requiere, clave de idempotencia y cause. Un cliente nunca establece privilegios por enviar un actor, F04Ref, F11CharacterId, grant, validated=true, CAUSE=110501 ni un documento. Estos son datos o referencias, no credenciales.

Ejemplo ilustrativo de solicitud (JSON explicativo, NO protocolo de red ni firma existente):

~~~json
{"host_contract":"1.0","session_generation":9,
 "correlation_id":"req-0007","operation":"F05_SUBMIT_ORDER",
 "expected_core_revision":212,"idempotency_key":7807,"cause":12009,
 "payload":{"order_kind":"F04_SCAN","target_role":"current_sensors_operator"}}
~~~

El HOST resuelve en hilo propietario el actor/observador y destinatario reales, sin aceptar permisos del texto. F05 valida competencia y revisión. Los IDs y cifras son didácticos y no acreditan entidades existentes.

Respuesta lógica:

~~~json
{"host_contract":"1.0","session_generation":9,
 "correlation_id":"req-0007","kind":"RESULT","status":"ACCEPTED",
 "core_revision_before":212,"core_revision_after":213,
 "domain_receipt_id":410}
~~~

ACCEPTED no implica ejecución de una orden, publicación durable de un guardado, ni ascenso. Los recibos y estados reales se consultan en el dominio.

## Operaciones y API de apoyo

| Operación HOST propuesta | Condición HOST | API real / dueño | Efecto |
|---|---|---|---|
| OPEN_CAMPAIGN | CLOSED, configuración admitida | f04_create_population / H02 | Una sesión |
| CLOSE_CAMPAIGN | sesión existente, hilo propio | f04_destroy / H02 | Invalidar handles |
| RESOLVE_PRINCIPAL | ACTIVE, vínculo legítimo | H03 y f05_bind_player | Vincular jugador, nunca otorgar rango |
| QUERY_VIEW | ACTIVE, observador autorizado | f04_* / f05_* / lector F11 | Proyección filtrada |
| F04_COMMAND | ACTIVE, actor y revision | f04_execute | Resultado F04 |
| F05_SUBMIT_ORDER | ACTIVE, key/cause válidos | f05_submit | Orden ISSUED; NO ejecución |
| F05_RECEIVE_ORDER | receptor correcto, revision | f05_receive | Recepción y tarea si procede |
| F05_EXECUTE_ORDER | receptor correcto, revision | f05_execute_order | Intento único; resultado Core |
| F05_CANCEL_ORDER | actor correcto, revision | f05_cancel | Cancelación según dominio |
| ADVANCE_CAMPAIGN | ACTIVE, presupuesto acotado | f04_advance | Tick Core |
| SAVE_SLOT | ACTIVE, ruta/ranura válida | H04 + persistencia Core | Solo confirmar tras IO durable |
| RESTORE_SLOT | transición controlada | H04 + Core load/history_open | Validar, activar y renovar scopes |
| F11_READ_PERSONNEL | sujeto y divulgación comprobados | trek::f11_host::career/promotion | Solo lectura de hechos confirmados |
| F11_INSTITUTIONAL_COMMAND | API futura aprobada y competente | Exclusivamente F11 | Por ahora SERVICE_UNAVAILABLE |
| SUBSCRIBE_EVENTS | ACTIVE, vista autorizada | H08 hechos Core | Avisos derivados |

La API existente f11_commit_promotion valida un tipo de promoción; NO resuelve el emisor institucional productivo, sus raíces de autoridad ni su bootstrap. Nunca exponerla directamente a Blueprint, LLM, NPC o consola de emisión. F11-P05-A02-03 sigue en el proyecto principal.

## Idempotencia, revisión y rollback

- El HOST mantiene correlation_id operacional; **no lo confunde** con key de Core. En F05 las keys/cause son valores de campaña no nulos y de 48 bits según f05_orders.h. Una misma key con payload distinto es conflicto; no regenerar una nueva key a escondidas.
- Si la revisión está caducada, devolver REVISION_STALE y pedir que la UI refresque; reintentar una mutación exige nueva voluntad del jugador. La autoridad/revisión final la verifica F04/F05/F11.
- Separar ISSUED, recepción ACCEPTED y EXECUTING/COMPLETED/FAILED. Tras timeout de ejecución, consultar recibo/eventos; NO ejecutar de nuevo a ciegas.
- En operaciones denegadas, comprobar que el dominio no modifica WorldState. HOST no crea un rollback institucional manual ni un evento compensatorio.
- Al restaurar, la nueva session_generation invalida todas las intenciones y callbacks anteriores incluso si los IDs coinciden.
- Devolver salida vacía en denegación, error de scope o fallo de buffer; no filtrar diagnósticos. Las vistas y avisos están ligados al observador autorizado.

## Matriz de errores NORMALIZADOS (no enums ABI)

| Error lógico | Fuente típica | Tratamiento |
|---|---|---|
| INVALID_ARGUMENT | Mensaje mal formado, exceso de tamaño | Rechazo sin Core |
| SESSION_CLOSED | Sin campaña | No resolver referencias |
| BUSY_STATE | Guardando, cargando o cerrando | Rechazo sin mutación |
| WRONG_THREAD | Invocación directa por worker | No acceder a Core |
| GENERATION_EXPIRED | Callback de sesión antigua | Descartar y purgar |
| PRINCIPAL_UNBOUND | Jugador no vinculado | Denegar, no autovincular |
| ACCESS_DENIED | Canal u observador no autorizado | Denegar sin exposición |
| SCOPE_INVALID | F04_SCOPE o scope distinto | Renovar con identidad legítima |
| REVISION_STALE | F04_REVIEW/F04_STALE o equivalente | Refrescar, no autoejecutar |
| DOMAIN_REJECTED | F04_DENIED/QUALIFICATION, F11_* | Preservar código de dominio privado |
| IDEMPOTENCY_CONFLICT | F05_IDEMPOTENCY_CONFLICT, F11 similar | No inventar otra key |
| CAPACITY_LIMIT | F04_CAPACITY | No mutar parcialmente |
| SAVE_INCOMPATIBLE | Versión/esquema no compatible | Preservar original y sesión |
| SAVE_UNTRUSTED | Importado sin procedencia admitida | Rechazar elevación institucional |
| PERSISTENCE_FAILED | Fallo de IO/publicación | No confirmar durable |
| SERVICE_UNAVAILABLE | F11 institucional todavía inexistente | Fallo cerrado sin fixture |
| INTERNAL_ERROR | Excepción inesperada | Diagnóstico privado y limpieza |

No asignar valores numéricos ABI a estos nombres. Las API reales tienen F04Code, F05Code y F11Code propios; H05 implementará mapeos preservando rechazo original. No afirmar que F04 tiene devolución de rollback general.

## Consultas, eventos y versionado

QUERY_VIEW recibe observador solo desde HOST, produce datos por perspectiva y revisión, y pagina según API específica. Un evento H08 deriva de hecho canónico Core y se entrega con id de hecho, revisión y observador; no se convierte en nueva verdad ni añade rangos. El acuse de presentación no causa ascensos. Tras cambio de campaña se vacían colas y cachés.

- Diferente versión mayor de host_contract: rechazar mutaciones por incompatibilidad.
- ABI del puente y Core SHA: comprobar en inicialización/build, no confiar en una cadena aportada por archivo.
- Save schema: propiedad Core; migración probada explícitamente, no interpretación heurística.
- Capabilities: lo que está realmente compilado/validado, no lo que anuncia una pantalla.
- Operaciones F11 institucionales permanecen cerradas hasta contrato de producto real aprobado por F11.

Este documento **especifica comportamiento esperado**, no confirma que se haya implementado. H02/H05 concretarán C++ interno sin cruzar STL, excepciones o UObjects por la ABI C.
