# H08-P03 — Reloj de campaña y trabajos acotados de CoreRPG

**Fecha:** 2026-11-23. **Estado inicial de esta rama: IMPLEMENTADO / PRUEBAS PENDIENTES DE CI.**
No se declara certificación ni fusión hasta disponer de evidencias verificables.

## Decisión de arquitectura

El HOST no mantiene un reloj de campaña propio ni ejecuta las reglas de las actividades.
Solo tramita una **petición explícita** a `f04_advance` en el hilo propietario de `SessionOwner`,
después de validar la sesión naval, la generación y el jugador enlazado en F05.
`f04_advance` es un servicio privilegiado de F04/Core y **no** una orden disponible
para NPC, Blueprint o IA. Todo `WorldState`, RNG, cronología, estados de tareas y
posibles eventos de actividad son propiedad de CoreRPG.

La nueva operación `SessionOwner::advance_clock(generation, ClockIntent, correlation)`
es **C++ nativa interna**; no se exporta como nueva operación en `host_abi.h` y no
se añaden accesos Unreal, IA o UI. `ClockIntent` especifica:

- `intent_id`: número no nulo, estrictamente creciente entre nuevas peticiones
  de la **misma generación**. Es identificador operativo, **no permiso** ni clave Core.
- `expected_revision` y `expected_now`: se comparan con la revisión y el tick
  verdaderos obtenidos en F04, ya en el hilo propietario. Se devuelve
  `REVISION_STALE` si cualquiera cambió, sin ejecutar el avance.
- `horizon`: segundo **absoluto** de campaña Core, no duración de sistema ni
  tiempo real/Unreal. Se acepta `expected_now <= horizon <= expected_now+600`.
- `task_budget`: **1–128** tareas como límite inicial del HOST, dentro del
  presupuesto propio de F04 (hasta 4096). Sin bucles automáticos para agotarlo.
- `correlation_id`: solo contexto de transporte, no clave de idempotencia.

Estos límites son conservadores y revisables mediante cambios versionados y pruebas;
no definen aún el ritmo jugable ni prometen aceleración. El juego podrá pedir avances
sucesivos de forma explícita cuando lo autorice su capa de control.

## Ejecución, parciales y consistencia

`NativeSession::advance` solo usa la campaña naval real; la Academia ligera no
dispone de servicio F04 equivalente y devuelve `SERVICE_UNAVAILABLE`. La
función privada `bridge::advance` vuelve a obtener `f05_player_binding`, verifica
la misma persona/ámbito que el vínculo H03, comprueba con `f04_person` y lee
`f04_stats` antes y después de la única llamada a `f04_advance`.

**Punto fundamental:** cuando F04 devuelve `F04_CAPACITY`, **ya puede haber
confirmado parte del avance**. H08 lo presenta como `ClockResult{error=OK,
more_due=true}`, con `before_tick`, `after_tick`, revisión inicial/final y
`processed` reales leídos de Core. No traduce esta situación en un error que
deba reintentarse. Si `F04_OK`, se exige llegar exactamente al horizonte. Si
un valor/lector posterior es inconsistente, el HOST deniega con error interno,
no fabrica un recibo de finalización.

Los reintentos con **idéntico `intent_id` y todos los parámetros iguales**
devuelven el **recibo observado previamente** (marcado `replayed=true`),
sin volver a llamar a Core. Mismo ID con payload distinto: `IDEMPOTENCY_CONFLICT`.
Se conservan solo las últimas **32** respuestas operativas; las claves antiguas
ya desalojadas se rechazan mediante límite superior de clave, nunca se reejecutan.
No se promete «exactamente una vez» entre procesos ni después de RESTORE:
los recibos son efímeros y una carga restablece el estado auténtico Core,
renueva la generación y obliga a reconstruir las intenciones.

En cierre o restauración, las peticiones en cola y resultados de generación
anterior se invalidan; un resultado tardío no se presenta como vigente.
Los trabajos aceptados por F04 antes de un cierre no constituyen confirmación
de guardado: la durabilidad sigue bajo la política H04. SAVE es serializado
por el mismo hilo propietario; no tiene lugar en paralelo con `f04_advance`.

## Pruebas de aceptación (CTest nativo real)

- `hk01_basic`: avanza tick Core sin inventar tareas.
- `hk02_partial`: dos tareas F04 reales, budget=1, confirmación parcial y
  continuación **explícita**.
- `hk03_stale`: revisión caducada rechazada sin mutación.
- `hk04_replay` / `hk05_conflict`: replay idéntico sin nuevos efectos;
  colisión de identificador con parámetros distintos denegada.
- `hk06_unbound`: no se permite avanzar sin jugador H03 vinculado.
- `hk07_limits`: cero, horizonte retrógrado, plazo excesivo y presupuesto
  fuera de límites sin efectos.
- `hk08_restore`: persistencia H04 del tick, renovación de generación y
  revocación de recibos efímeros.
- `hk09_concurrent`: dos solicitudes simultáneas a FIFO sin doble avance.
- `hk10_close` / `hk14_queued_close`: cierre durante Core, sin entrega
  tardía ni trabajo en cola ejecutado tras invalidación.
- `hk11_events`: avance del reloj no inventa transiciones de orden F05.
- `hk12_partial_replay`: repetir el recibo parcial no consume otra tarea.
- `hk13_worker`: llamada iniciada desde worker cliente se encamina al único
  hilo Core; jamás pasa punteros Core a otro hilo.
- `hk15_same_tick`: sin tareas y con horizonte igual al tick actual no
  se fabrica progreso, eventos ni RNG.

Las 15 pruebas se añaden como `host.clock.*` al ejecutable real
`host_m0_tests`; reutilizan CMake/Actions actual: Linux nativo,
Windows nativo, ASan/UBSan y compilación de producto tests=OFF. No hay nuevo
laboratorio permanente ni cambio de pin Core.

## Pendiente para cierre

La evidencia CI de los commits de esta PR debe demostrar que no hay regresiones.
El sistema F04/Core **ya** decide vencimientos, resultado de tareas, tiempo y
eventos; P03 se limita a coordinar su invocación. Para gameplay dinámico,
temporización visual, pausar/reanudar en Unreal y proyecciones de misiones,
las fases posteriores definirán políticas específicas antes de activarlas.
No se declara probado en MSI/Unreal ni certificado el HOST integral.
