# H08-P04 — Notificaciones derivadas de hechos autorizados (v1)

**Fecha:** 2026-11-23 · Responsable: ChatGPT · Estado del contenido: IMPLEMENTADO EN RAMA / VALIDACIÓN CI PENDIENTE.
No confundir documentación y código de esta PR con certificación de Unreal o de la fase H08 completa.

## Alcance y autoridad

Se añade un **formateador nativo C++** de notificaciones locales de la fuente F05 ya
implementada en H08-P02. Se consumen exclusivamente eventos `f05_events_page`
después de comprobar identidad H03, ámbito y visibilidad F05 en el hilo propietario
del HOST. No se consulta ni cambia el `WorldState` desde el formateador:
CoreRPG sigue siendo la fuente de verdad de hechos, tiempo y consecuencias.

**Nueva operación interna:** `SessionOwner::poll_order_notifications(generation,
subscription,correlation)`. Reutiliza **la misma** suscripción y el mismo
`poll_order_events` de P02, en el mismo hilo propietario y bajo el mismo estado
de sesión. No abre una segunda cola, no vuelve a ejecutar una orden, no avanza
tiempo, no crea hechos y no admite referencias de actor/observador desde UI.

La entrega en la respuesta `NotificationBatchResult` contiene:

- `generation`, `subscription`, `correlation_id` y `campaign_id` H04 (identidad
  técnica, **no una credencial**) para desambiguar la identidad del hecho entre
  campañas;
- `NotificationNotice{source=F05_ORDER, kind, level, source_event_id,
  previous_event_id, order, core_tick, title, body}`: los identificadores y
  el tick son **exclusivamente** los de F05/Core. Los títulos/cuerpos no
  incluyen resultados sensibles, causas ocultas ni mensajes inventados;
- `more` y `resync_required`: señales de **control de entrega**, no hechos
  de juego. En denegaciones, cualquier texto/ID/campaña sensible queda vacío.

No hay API C pública ni conexión a widgets de Unreal en esta entrega. Una
interfaz LCARS podrá **consumir** estas proyecciones mediante un adaptador
posterior, sin calcular permisos ni usar la notificación como autoridad.

## Catálogo local de F05 (castellano, versión 1)

| Fuente F05 | Kind | Nivel UI | Título |
| --- | --- | --- | --- |
| `F05_ISSUED` | `ORDER_ISSUED` | INFO | Orden emitida |
| `F05_ACCEPTED` | `ORDER_ACCEPTED` | INFO | Orden recibida |
| `F05_EXECUTING` | `ORDER_EXECUTING` | INFO | Orden en curso |
| `F05_COMPLETED` | `ORDER_COMPLETED` | SUCCESS | Orden completada |
| `F05_FAILED` | `ORDER_FAILED` | ERROR | Orden no completada |
| `F05_REFUSED` | `ORDER_REFUSED` | WARNING | Orden rechazada |
| `F05_CANCELLED` | `ORDER_CANCELLED` | WARNING | Orden cancelada |

La traducción es **semántica y conservadora**: `ORDER_ACCEPTED` no significa
ejecución; un aviso de fallo no revela códigos, tiradas ni motivos no
autorizados; un texto de éxito solo acompaña `F05_COMPLETED` real.
Estados desconocidos o fuentes distintas de F05 fallan cerrados: **cero
notificaciones**, sin completar una página parcialmente ni interpolar
información.

## Duplicados, orden y acuses

La clave estable de presentación es
`campaign_id + F05_ORDER + source_event_id + kind`; un consumidor puede
usarla para su deduplicación visual entre generaciones, sin tratar el
`correlation_id`, reloj de pared o token de suscripción como identidad del
hecho. `previous_event_id` mantiene la cadena causal intraorden y
`core_tick` no se sustituye por temporizadores de Unreal.

Se conserva el ack `SessionOwner::ack_order_events(generation, subscription,
source_event_id)` **único de P02**. Este ack retira de la cola solo lo que se
presentó, no equivale a `f05_receive`, no da por ejecutada una tarea y no
modifica Core. La lectura repetida previa al ack entrega la misma proyección.
La entrega es `at least once`, **no exactamente una vez** al restaurar.

Ante `RESTORE` o `CLOSE`, H02/P02 invalidan generación, token y cola;
las notificaciones pendientes anteriores no vuelven como callbacks tardíos.
Una nueva suscripción reconstruye desde la fuente F05 que Core conserve.
En historial insuficiente o discontinuidad de página se transmite
`resync_required` **sin generar una notificación de ficción**.

## F11 y visibilidad institucional

El contrato H08-P01 permite proyectar en el futuro **solo ascensos F11 ya
confirmados por Core y divulgables al observador**. Pero las PR apiladas de
H07 (#203, #204, #205) siguen sin fusionar al redactar esta especificación,
y el emisor F11 de producto no se incorpora a H08-P04.

Por tanto, el catálogo ejecutable **no contiene ninguna notificación F11**.
Una `EventSource` desconocida no se convierte a F05 y se descarta;
`SessionOwner` no dispone de API para publicar un ascenso, acto de mando,
expediente profesional ni comunicado institucional. Las ceremonias,
contratos y normas de publicación pertenecen a F11 y sus fases posteriores.
**No inferir ascensos de rango, revisiones, ticks, titulares o textos IA.**

## Matriz de pruebas de P04

**14 casos nativos con la composición de producto F04/F05/Core:** estados,
transiciones parciales, repoll, restore, close, observador ajeno, jugador no
vinculado, token inválido, ack parcial, avance de reloj sin eventos ficticios,
generación vacía, identidad compartida con P02, segundo suscriptor y ack sin
mutaciones (`host.notification.hn01…hn14`).

**10 casos puros de formateador:** siete estados, estado desconocido, fuente
ajena, metadatos inválidos, preservación de IDs/tick, idempotencia,
privacidad, denegación, resync y origen no autenticado
(`host.notification.unit.*`).

La matriz existente de Actions compila ambos grupos en Linux/Windows,
incluido ASan/UBSan, y conserva la construcción Release de producto
`TREK_HOST_TESTS=OFF`, la regresión H02–H08 y F11 aislado.

La CI deberá acreditar:
1. Que la consulta de notificaciones no altera bytes autoritativos ni RNG.
2. Que un observador ajeno nunca puede obtener una página ni siquiera sus IDs.
3. Que un estado terminal, una carga y el cierre no crean mensajes sintéticos.
4. Que el mismo token/ID sirve para consulta cruda autorizada y proyección,
   sin cola secundaria ni acuses Core.
5. Que las 24 pruebas nuevas y las regresiones anteriores pasan en las
   plataformas de CI.

**Criterio de cierre H08-P04:** código y pruebas nativas aprobadas y PR
fusionada. **No** equivale a demostrar una UI funcional en MSI/Unreal,
notificaciones F04 globales, emisión F11 ni certificación de H08 integral.
Esas dependencias deben documentarse explícitamente, no simularse.
