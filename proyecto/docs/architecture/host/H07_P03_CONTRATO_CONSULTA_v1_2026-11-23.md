# H07-P03 — Contrato privado de consulta institucional v1

`trek::host::detail::InstitutionalQueries` es una interfaz C++ interna del HOST
local. Opera sobre el `SessionOwner` de la partida. H07-P05 podrá consumir la
proyección autorizada desde código nativo integrado en el HOST. El SDK H05/H06
conserva sus cabeceras, tablas ABI y operaciones.

## Peticiones y vigencia

- `career(owner, generation, correlation)` consulta el expediente del jugador
  vinculado.
- `promotion(owner, generation, event_id, correlation)` consulta un evento
  confirmado que pertenece a ese mismo jugador. `event_id` es el identificador
  persistente de un hecho Core usado exclusivamente como clave de búsqueda.
- El worker de `SessionOwner` resuelve el vínculo F05 de Core y comprueba que la
  persona y el ámbito coinciden con el vínculo activo del HOST. El observador y
  el sujeto son esa misma persona. F11 comprueba pertenencia e identidad del
  evento y la visibilidad `F11_SUBJECT_AND_PERSONNEL`.
- El origen admitido es `CREATED_LOCALLY` o `KNOWN_LOCAL`. H04 verifica el
  registro local de la ranura, el UUID de campaña, el vínculo persistido y el
  esquema Core/F04/F11 antes de publicar una restauración. La procedencia
  acredita continuidad local de la partida.
- La consulta revalida generación, estado, vínculo, procedencia y época de
  persistencia antes de publicar. `SAVE` y `RESTORE` admitidos hacen caducar
  la época anterior desde la entrada en cola. `SAVE` conserva la generación
  H04. Un `RESTORE` exitoso renueva también generación y ámbito F04.
  `CLOSE` invalida la generación y descarta las consultas pendientes.
- El consumidor debe ejecutar `is_current(owner, result)` inmediatamente
  antes de usar una vista y descartar su copia si falla. La vista ya entregada
  es una fotografía a la revisión indicada. `is_current` comprueba la vigencia
  de sesión y persistencia de esa fotografía.

## Vista v1

| Parte | Campos | Semántica |
| --- | --- | --- |
| Sobre privado | `generation`, `correlation_id`, `persistence_epoch` | Vigencia local y correlación de transporte |
| Vista institucional | `world_revision`, `facts` | Revisión Core del turno de lectura y una sola proyección tipada |
| `CareerViewV1` | `rank_event_id`, `rank`, `service_status` | Hecho vigente de rango, código de rango y estado de servicio de F11 |
| `PromotionViewV1` | `event_id`, `effective_tick`, `original_revision`, `from_rank`, `to_rank` | Evento confirmado, tick de efecto y revisión del commit original en Core |

`rank_event_id` puede identificar el hecho inicial de comisión. Una consulta
de promoción solo tiene éxito cuando F11 reconoce un evento de promoción
visible. Los campos de la vista son datos de presentación. El ámbito, el
puntero de sesión, la identidad profesional interna y los antecedentes de
autoridad permanecen en el código nativo. La vista se reconstruye a partir de
Core en cada consulta y el consumo conserva los tiempos originales del hecho.

## Resultados

| Resultado | Condición |
| --- | --- |
| `OK` | Vista completa del propio sujeto admitida por F11 |
| `SESSION_CLOSED`, `GENERATION_EXPIRED`, `BUSY_STATE`, `CAPACITY_LIMIT` | Ciclo de sesión, época, estado ocupado o cola llena |
| `PRINCIPAL_UNBOUND`, `ACCESS_DENIED` | Vínculo inexistente o inválido, identidad discrepante, evento desconocido o ajeno |
| `SAVE_UNTRUSTED` | Procedencia fuera del conjunto admitido |
| `SCOPE_INVALID`, `WRONG_THREAD` | Ámbito F04 renovado o incorrecto, o guardia del hilo F04 |
| `DOMAIN_REJECTED` | F11 respondió `F11_UNCOMMISSIONED` |
| `SERVICE_UNAVAILABLE` | La composición carece de lector F11 o la sesión es Academy |
| `INVALID_ARGUMENT` | Generación vacía en sesión activa o ID cero de evento |
| `INTERNAL_ERROR` | La lectura Core/F11 falló por otra causa |

En todo error se conserva la correlación y se devuelve vista ausente,
generación vacía y época cero. Un evento desconocido y uno ajeno comparten el
mismo resultado observable. El comando institucional existente conserva la
admisión de H02–H06 y devuelve `SERVICE_UNAVAILABLE` al ser admitido en la
sesión naval. El contrato v1 ofrece exclusivamente lecturas.
