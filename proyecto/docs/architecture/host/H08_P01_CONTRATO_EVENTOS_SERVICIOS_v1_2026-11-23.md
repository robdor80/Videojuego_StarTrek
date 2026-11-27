# H08-P01 — Contrato de eventos, servicios, deduplicación, precedencia y visibilidad v1

Fecha: 2026-11-23. **Estado: DISEÑADO / NO IMPLEMENTADO / NO CERTIFICADO.**
Responsable: ChatGPT (contrato). Implementación de dispatcher en H08-P02; reloj en H08-P03; formateo/aceptación en H08-P04.
Fuente verificable: `PLAN_MAESTRO_HOST_v1.2_2026-11-11.md`, H01-P01/P02, `H01_REGISTRO_CONTRATOS_v1.json`,
`f04_bridge.h`, `f05_orders.h`, `f11_host_reader.h` y H02–H05 ya integrados.
Registro estructurado: `H08_P01_REGISTRO_EVENTOS_v1.json`. **No se crea una ABI ni un endpoint de producto**.

## 1. Objetivo, autoridad y fronteras

H08 convierte **hechos ya registrados** en mensajes de presentación por observador. Es un coordinador local de
una única campaña, no un segundo `WorldState`, motor de reglas, cronología, registro profesional ni emisor F11.
CoreRPG sigue siendo la fuente de verdad de hechos, relaciones, conocimiento, persistencia y tiempo; F04/F05
conservan la semántica de dotación y órdenes; F11 conserva exclusivamente la normativa y el emisor institucional
en el proyecto principal Star Trek. Una notificación nunca concede un ascenso, ejecuta una orden ni modifica Core.

H08-P01 **solo define contrato**. `SUBSCRIBE_EVENTS` existe en H01 como operación lógica con
`existing_api=null`; no se afirma que exista todavía `trek_host_subscribe_events`, `poll_events` ni un
bus nativo, una cola guardada o un servicio en Unreal. H08-P02/P03 requerirán comprobación de hilo, composición
nativa y nuevas pruebas. No introducir red, servidor, hilos Core extra ni modificaciones a pins Core.

## 2. Fuentes reales verificadas y límites

| Fuente autorizada | Lectura real | Identidad candidata | Límites, tratamiento |
| --- | --- | --- | --- |
| Hechos F04/Core | `f04_history_page`, `f04_history_relations` | `F04HistoryFact.id` | Requiere historial habilitado, generación/cursor y observador válidos; un `definition` no demuestra por sí solo una notificación visible ni todo su contexto |
| Transiciones de orden F05 | `f05_events_page` y `f05_order` | `F05EventView.id` | Lectura **por orden** y por observador autorizado; no es un feed general ni un detector F06 |
| Ascenso F11 **confirmado** | `trek::f11_host::promotion` | `Promotion.promotion_event` | Lector privado de hechos existentes, sujeto legítimo y divulgación aprobada; sin emisor de producto F11 la emisión permanece `SERVICE_UNAVAILABLE` |
| Hora/avance Core | `f04_stats` y `f04_advance` | No aplica a notificaciones | `f04_stats` es diagnóstico privilegiado; `f04_advance` muta el reloj Core y **queda fuera de H08-P01**; H08-P03 diseñará su presupuesto y autorización |

Las rutas son **fuentes de posible proyección, no garantías de cobertura universal**. Para sucesos sin
lector autorizado y estable, el servicio devuelve `SERVICE_UNAVAILABLE` o resincro­nización de vista, jamás
inventa un hecho. Una cifra `events` de `F04Stats` no representa un catálogo de eventos accesible a UI.

## 3. Sobre lógico de transporte y elemento entregado

La petición de suscripción/consulta y su respuesta conservan el sobre H01: `host_contract=1.0`,
`session_generation`, `correlation_id` y `operation=SUBSCRIBE_EVENTS`. La respuesta expresa estado
normalizado H01; ninguna versión nueva de ABI se da por compilada.

Cada elemento lógico (no estructura C implementada) contiene:

- `event_contract=1`; `campaign_id` técnico H04 (no credencial); `session_generation` operacional H02;
  `source`, `source_event_id`, `kind` y `core_revision` cuando el lector lo garantice;
- `core_tick` **solo si figura en la fuente**, nunca calculado a partir del reloj de pared;
  `causal_parent` **solo si la fuente lo prueba**; `origin_correlation_id` opcional, no identificador de hecho;
- `observer_context` **resuelto por HOST** desde H03 y la campaña, nunca desde el cliente;
  `view_payload` mínimo **ya filtrado** conforme a la lectura autorizada.

Una lectura de historia con ID pero sin vista permitida no puede publicarse. Ninguna clave de autorización
se infiere de `campaign_id`, `F04Ref`, `cause`, revisión o nombre de personaje.

**Ejemplo exclusivamente ilustrativo, no datos reales ni endpoint disponible:**

```json
{
  "host_contract": "1.0", "operation": "SUBSCRIBE_EVENTS",
  "session_generation": 8, "correlation_id": "ui-148",
  "items": [
    {"event_contract": 1, "source": "F05_ORDER", "source_event_id": 135,
     "kind": "ORDER_TRANSITION", "campaign_id": "example-not-a-credential",
     "session_generation": 8, "core_tick": 5400, "observer_context": "HOST_RESOLVED",
     "view_payload": {"status": "COMPLETED"}}
  ]
}
```

Los números y el texto del ejemplo son ficticios. No suponen que una orden F05 concreta haya existido.

## 4. Identidad, deduplicación y relectura

La identidad de un **hecho** se compone de `campaign_id + source + source_event_id + kind`. Debe provenir
de la fuente Core/F05/F11 y conservarse mientras esa fuente garantice su identidad. La identidad de entrega
incluye además un identificador **interno de proyección/observador autorizado** (nunca una referencia aportada
por UI). El cursor de historial o paginado **no es** identidad de evento.

`session_generation`, `correlation_id`, revisión mutable, posición de página y hora de presentación
**no forman parte de la clave estable**: permitirían duplicar el mismo hecho después de RESTORE o al reintentar.
Si una misma clave de hecho retorna contenido incompatible, bloquear proyección, registrar diagnóstico privado
y exigir reconciliación desde Core; no sustituir silenciosamente el anterior.

Entrega objetivo **al menos una vez**, con deduplicación de proyección en la generación activa. El consumo
visual es idempotente. Tras RESTORE se elimina todo cursor/acuse efímero y se reconstruye desde lecturas
canónicas en la nueva generación, dentro del historial que **Core aún conserve**. No prometer relectura de
hechos archivados o purgados fuera de la capacidad real del lector. Si no hay prueba de continuidad de cursor
o falta historia, publicar estado `RESYNC_REQUIRED` (control interno, **no** hecho de juego) para que la UI
refresque su vista; nunca inventar ni extrapolar eventos perdidos.

Los acuses de UI se refieren a entrega/proyección, **no** a efectos Core. No implican `f05_receive`,
ejecución de orden, confirmación de guardado ni aceptación institucional. H08-P02 decidirá si los acuses
son solo efímeros; H08-P01 no introduce persistencia de acuses ni contratos de escritura.

## 5. Precedencia, causalidad, reloj y presupuesto

- Respetar el orden real por fuente y sus relaciones explícitas: `F05EventView.previous` puede establecer
  precedencia dentro de una orden; no invertirla al agrupar avisos. `F05_ISSUED`, `F05_ACCEPTED`,
  `F05_EXECUTING` y un estado terminal son **estados de F05**, no decisiones H08.
- Entre F04, F05 y F11 no se declara un orden total autoritativo sin relación Core verificable.
  El orden `core_tick, source, source_event_id` puede servir únicamente de presentación determinista
  cuando existan esos campos; coincidencia temporal no prueba causalidad.
- No usar `monotonic_ms` de IA, temporizador de Unreal ni hora de pared como reloj de campaña.
  Solo el Core controla `now`, cronología y resultado de `f04_advance`. No avanzar en P01 ni
  repetir avance por timeout; H08-P03 limitará horizonte/budget y probará reproducibilidad.
- Las lecturas, deduplicación, entrega y acuses no deben cambiar revisión Core, RNG, WorldState ni
  historial. Si la biblioteca real no demuestra esta garantía, H08-P02 deberá corregir y probar.

## 6. Visibilidad, estados de sesión y errores

Todo acceso a datos se resuelve por el principal/campaña/personaje H03, comprobando antes del lector el
hilo propietario, estado `ACTIVE`, generación vigente y ámbito del observador. F04/F05/F11 conservan
su filtrado de dominio, que HOST **no sustituye**. Nunca poner hechos brutos o diagnósticos privilegiados
en un bus visible a toda UI, NPC, IA o PADD. Una proyección denegada entrega elemento vacío y error
normalizado (p. ej. `ACCESS_DENIED`/`SCOPE_INVALID`), sin filtrar existencia, ID ni contenido.

En `SAVING`, `LOADING`, `CLOSING`, `CLOSED`, `FAILED`: no emitir nuevas vistas de juego ni permitir
`SUBSCRIBE_EVENTS`; delimitar transición sin fuga de callbacks. `RESTORE` o `CLOSE` invalidan la
generación, los acuses, los cursores, las notificaciones sin presentar y los trabajos pendientes. Un
resultado tardío de generación antigua siempre se descarta. Tras fallo de carga que conserva la sesión,
H04 determina qué generación continúa; jamás adivinar.

Cola futura con tamaño y coste acotados, límites de páginas, presupuesto de trabajo y retro­presión.
Ante saturación, no perder hechos autoritativos (no pertenecen a la cola), no mutar Core ni dar
confirmación de entrega ficticia; señalizar `RESYNC_REQUIRED` o error `CAPACITY_LIMIT` al consumidor.
No reintentar automáticamente ninguna mutación para completar un aviso. Las lecturas reintentables
requieren ámbito/revisión/generación nuevamente comprobados.

## 7. Protocolo de evolución y aceptación

H08-P01 produce **solo artefactos versionados y comprobadores estáticos**; no declara P02/P03/P04
implementadas, probadas o certificadas. Un cambio mayor requiere compatibilidad H01/ABI,
aprobación del esquema consumidor y prueba de compatibilidad de carga. No modificar el pin
Core `76a7b7b485616d8c4994f384a90f123bf333591d` por conveniencia del contrato.

| Caso | Requisito verificable en P02–P04 | Estado ahora |
| --- | --- | --- |
| HE-01 | Mensajes H01, versión, operación y correlación coherentes | DISEÑADO |
| HE-02 | Fuente real y hecho confirmado; sin eventos inventados | DISEÑADO |
| HE-03 | Deduplicación por ID fuente estable dentro de un observador | DISEÑADO |
| HE-04 | RESTORE renueva generación; reconstrucción y no callbacks antiguos | DISEÑADO |
| HE-05 | CLOSE descarta cola, vistas, cursores y acuses | DISEÑADO |
| HE-06 | Orden causal F05 sin mezclarla con la orden de presentación | DISEÑADO |
| HE-07 | Ausencia de orden causal interfuente no provoca inferencias | DISEÑADO |
| HE-08 | Observador ajeno/ausente y datos prohibidos: salida vacía | DISEÑADO |
| HE-09 | F11 solo comunica ascenso previamente confirmado por Core | DISEÑADO |
| HE-10 | Fallo de lector: error cerrado, sin hecho sintético | DISEÑADO |
| HE-11 | Saturación/páginas limitadas, sin pérdida de fuente canónica | DISEÑADO |
| HE-12 | Acuse UI no modifica F05/F11 ni Core | DISEÑADO |
| HE-13 | Hora de campaña igual a Core, sin reloj paralelo | DISEÑADO |
| HE-14 | Avance Core con budget y sin reintento ciego (futura P03) | DISEÑADO |
| HE-15 | Vista resíncronizada tras cursor no fiable o historia insuficiente | DISEÑADO |
| HE-16 | Ninguna fuga durante SAVE/LOAD/CLOSE o acceso fuera de hilo | DISEÑADO |

**Cierre de H08-P01:** contrato y registro coherentes con headers reales, matriz HE-01…HE-16
y validador en CI; su paso acredita **contrato comprobado estáticamente**, nunca funcionamiento
de dispatcher, reloj ni Unreal. La certificación completa H08 exige pruebas nativas de P02/P03
y pruebas de proyecciones P04, incluidas save/restore y autorización por observador.
