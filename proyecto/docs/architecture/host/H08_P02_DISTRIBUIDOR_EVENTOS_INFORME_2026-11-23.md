# H08-P02 — Distribución local de eventos confirmados (primera fuente F05)

**Fecha:** 2026-11-23. **Estado de entrega:** IMPLEMENTADO EN RAMA; pruebas y fusión pendientes de la evidencia CI de esta PR. **No certificado H08.**
Responsable: ChatGPT (implementación y auditoría). CoreRPG sigue siendo la única fuente de hechos.

## Qué se implementa

Se incorpora un distribuidor **nativo C++ dentro del HOST** con suscripciones a eventos de una **orden F05 concreta**. Es deliberadamente local (single-player), con cola acotada por suscripción y acuse **de visualización**. No es un historial paralelo ni copia reglas F05. Solo proyecta la fuente real `f05_events_page` después de autenticar al jugador enlazado a la sesión, y `f05_order` confirma acceso a la orden según el propio dominio F05.

Superficies internas añadidas en `SessionOwner`:

- `subscribe_order_events(generation, order, correlation)`: valida generación, estado ACTIVE, jugador H03 vinculado, observador de F05 y existencia/visibilidad de orden; emite token efímero no reutilizable.
- `poll_order_events(generation, subscription, correlation)`: devuelve hasta **16** transiciones F05 auténticas en orden causal, repitiendo las pendientes hasta su acuse; hace lecturas de Core exclusivamente en el hilo propietario.
- `ack_order_events(generation, subscription, presented_event_id)`: consume únicamente mensajes previamente entregados de ese token. No invoca `f05_receive` ni cambia hechos/órdenes/reloj/revisión/RNG.
- `EventDelivery`: máximo **16 suscriptores**, un máximo de **16 eventos por lote**, cursor de IDs de eventos Core y publicación atómica de páginas. No persiste acuses ni implementa un bus externo.

El lector `NativeSession::events` usa `bridge::events`, que resuelve `f05_player_binding` desde Core, comprueba mismo principal y vuelve a pasar `binding.person` a `f05_order` y `f05_events_page`. El consumidor nunca aporta `F04Ref`, permisos ni fuente de autoridad.

`EventNotice` ofrece solo `source=F05_ORDER`, `id`, `previous`, `order`, `tick`, `state` y `code` de la página filtrada; evita exponer el resto de relaciones y diagnósticos. La cadena `previous` se verifica antes de publicarla. Si hay un hueco o una página incompatible, el token pasa a `resync_required` (señal local, **no un nuevo hecho**), no fabrica eventos omitidos.

## Convivencia con H02–H07 y persistencia

- Se reutiliza el único hilo propietario/FIFO H02 con tres nuevos tipos de solicitud. Los límites de **32 solicitudes ya existentes** y las denegaciones H03 permanecen.
- `CLOSE` y `RESTORE` invalidan el distribuidor, incluidos tokens, páginas pendientes y acuses. Tras carga válida, una suscripción nueva reconstruye su página desde F05/Core. Una carga fallida deja intacta la sesión vigente.
- El distribuidor no se guarda en ranuras H04 y no modifica el historial Core. **El mismo hecho puede reaparecer después de RESTORE**: el consumidor lo deduplica según la identidad fuente/campaña definida en P01 si desea continuidad visual. No prometer «exactamente una vez» entre procesos.
- Las reglas de órdenes siguen en F05; las reglas y el emisor institucional en F11. **No se enlaza emisor F11** ni lector H07 de sus PR apiladas #203–#205.
- No se cambia ni añade ningún símbolo a la **ABI C** consumida por Unreal (H06). La nueva interfaz es C++ nativa interna, no exportación para Blueprint.

## Qué NO se entrega en P02

No hay adaptación todavía de `f04_history_page` a vistas generales, ni notificaciones F11/ascensos, ni interfaz Slate/LCARS, ni reloj/scheduler de campaña. La infraestructura de P02 admite ampliar fuentes siempre que existan lecturas, visibilidad y claves estables reales; se hará con pruebas específicas, nunca inventando eventos.

**Dependencias futuras:** H07 apilada/pendiente (consulta F11), H08-P03 (reloj Core y presupuesto), H08-P04 (proyección/formateo y UI). El caso de duplicación/reconstrucción tras migración de historial F04 necesitará verificar retención de fuente antes de prometer replay general.

## Verificaciones previstas y evidencia a completar tras ejecución

1. **13 pruebas CTest end-to-end** (`host.event.he01_delivery`…`he13_generation`) ejecutan el F05/Core real: lectura autorizada, cadena issued/accepted/executing/completed, relectura, idempotencia, denegación de observador externo, jugador no vinculado, CLOSE/RESTORE, límites, errores, no mutación y serialización.
2. **8 pruebas unitarias** de cola `host.event.unit.*`: aceptación causal, página rota, fuente ajena, señalización de más sin datos, acuses inválidos, capacidad, invalidación y tamaño máximo.
3. Suites previas H02–H06, H04/F04/F05, sanitizers y producto Release `TREK_HOST_TESTS=OFF` conservan el alcance que ya cubren.
4. CI obligatorio Linux/GCC, Windows/MSVC y Linux/Clang ASan/UBSan. No se atribuyen pruebas MSI/Unreal ni certificación antes de evidencia.

**Criterio de cierre de P02:** pruebas anteriores aprobadas, sin mutar Core, sin regresiones y rama fusionada por autorización del usuario. La certificación completa H08 queda pendiente de P03/P04 e integración posterior.
