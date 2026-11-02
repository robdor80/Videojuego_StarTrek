# F05-P01 — Órdenes sobre la sesión autoritativa F04

Incremento nativo para auditoría. No cierra F05 ni desarrolla P02–P05.
CoreRPG **main `76a7b7b485616d8c4994f384a90f123bf333591d`**, sin modificaciones.
La [API C](include/f05_orders.h) amplía `TrekF04Bridge`; recibe el mismo
`F04Session*`. No crea otro mundo, reloj, historial ni almacén de órdenes.

## Compilar y reproducir

CMake >=3.25, compilador C++20, Python 3, Git y CoreRPG en el SHA del pin.
`OUTPUT` designa un directorio temporal nuevo permitido por el propietario,
fuera de las fuentes definitivas. En el puesto del propietario debe estar
dentro del directorio de laboratorios del repositorio. No usar la raíz de un
proyecto artístico. El código definitivo no depende de los resultados de pruebas.

```sh
cmake -S desarrollo/integration/f05 -B "$OUTPUT" -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR="$CORE_SOURCE"
cmake --build "$OUTPUT" --config Release --parallel 4
ctest --test-dir "$OUTPUT" -C Release -R '^f05\.' --no-tests=error --output-on-failure
ctest --test-dir "$OUTPUT" -C Release -E 'history_campaign_|persistence_baseline_|persistence_resume_' --no-tests=error --output-on-failure
```

La última selección incluye las regresiones F04 de corto plazo e inyección de
fallos del historial, además de P01. Las campañas históricas de 365/730 días
conservan su workflow F04 independiente. Los builds F02/F03/F04 originales
siguen usando sus pins; no se actualizan silenciosamente.

## Flujo

1. Host autentica emisor y destinatario y obtiene sus `F04Ref` de la campaña.
   `f05_submit` recibe identidad de nave, puesto, operación, plazo del reloj
   Core, causa, revisión e idempotency key de campaña.
2. Se crean petición y orden `issued` con IDs Core distintos; autoridad,
   origen del nombramiento y capacidad contemporáneas determinan si permanece
   emitida o termina `refused`, con motivo y evento. Emitir no ejecuta.
3. Solo el destinatario puede llamar `f05_receive`. Revalida y crea la tarea
   `acknowledged`, llevando la orden a `accepted`. Aceptar no consume RNG.
4. `f05_execute_order` revalida autoridad de origen, mando vigente, aptitud,
   pertenencia, cualificación, guardia, puesto, presencia física y plazo.
   Crea intento y evento `executing`; llama al mismo `perform(F04_SCAN)` de F04.
5. Resultado Core, tarea terminal y evento `completed`/`failed` se confirman
   juntos mediante la transacción por copia ya usada en F04. No se publica un
   estado intermedio `executing`. Una excepción conserva campaña y RNG previos.

`f05_cancel` permite cancelar órdenes emitidas/aceptadas al emisor con autoridad
vigente o al mando actual. No deshace acciones ya realizadas. Un fallo de
revisión en recepción/ejecución no consume el intento: el Host debe refrescar
contexto antes de decidir un nuevo envío. No hay reintentos automáticos.

## Efecto realmente soportado

**F04_SCAN** ejecuta `ActionEngine::process` con `StreamRollAction{0xF0401,1,100}`
sobre el ejecutor existente. Se registran el outcome, rejection, revisiones,
stream, valor y consumo de RNG devueltos por Core. La tirada no incrementa por
sí misma la revisión de mundo; las relaciones de auditoría sí lo hacen.
No se declara detección de contactos, blancos, conocimiento nuevo ni éxito de
un modelo de sensores F06. No se admiten parámetros/objetivos ocultos.
Cualquier otra operación da `F05_UNSUPPORTED`, sin ejecutarla.

Las comprobaciones de autoridad son las de F04: mando efectivo o jefatura
vigente de Sensores; el rango aislado no basta. No se añaden delegaciones,
iniciativa NPC, interpretación de lenguaje ni proveedor IA.

## Persistencia, causalidad e idempotencia

Las seis clases de objetos son entidades `trek.f04:f05_*`, con relaciones
versionadas del vocabulario Trek. Se guardan por `CampaignPersistence` de Core,
incluidos semilla, streams y Timeline. También se admite migración, publicación,
consolidación y recuperación con el `HistoryPersistence` existente de Core.
No hay un JSON/SQLite lateral que pueda divergir de WorldState.

Cada evento conserva petición, orden, actor, tick Core, evento anterior y,
cuando existen, tarea/intento/resultado. Los eventos creados nunca se reescriben.
El validador de restauración comprueba formas, unicidad, referencias, cadena de
transiciones, estados terminales y resultado. Un archivo válido para Core pero
incoherente para P01 se rechaza antes de sustituir la sesión viva.

La key es única en la campaña. Payload idéntico devuelve la orden y su estado
actual sin nuevas entidades, eventos ni RNG, incluso después de carga o
caducidad. Payload distinto con la misma key da `F05_IDEMPOTENCY_CONFLICT`.
El payload incluye la revisión original, operación, causa, plazo e identidades;
los scopes de proceso se renuevan al cargar. `F05OrderView.input_revision`
permite reconstruir un replay con referencias de la nueva sesión.

Confirmar en memoria no equivale a confirmar en disco: el Host debe guardar el
archivo completo o publicar la generación Core antes de reconocer durabilidad
externa. El único efecto de esta operación pertenece al estado Core persistido;
no hay efectos externos que puedan duplicarse tras una caída. El historial
reutiliza el bloqueo F04 tras publicación incierta hasta recuperar disco.

## Límites deliberados

- Un ejecutor, una operación síncrona y un intento máximo por orden. No hay
  scheduler nuevo: la orden pendiente conserva su estado hasta recibir,
  ejecutar o cancelar explícitamente; el plazo se revalida en esas entradas.
- Máximo **512 órdenes por campaña** en este incremento; no se borran tombstones.
  El historial mantiene los objetos P01 residentes y su cierre de dependencias
  para conservar idempotencia. Escalado/retención de órdenes queda como deuda.
- ABI nativa de confianza y un único hilo propietario. Un `F04Ref` vincula una
  identidad lógica; no autentica por sí solo a un usuario de red o un LLM.
- Consultas limitadas al emisor, destinatario y mando actual. Son diagnóstico
  del Host; no constituyen reportes de conocimiento para NPC ni UI final.
- El build F04 antiguo rechaza archivos con definiciones P01 desconocidas.
  El build P01 sí carga los archivos F04 anteriores. No hay migración destructiva.
- Harness UE preparado, todavía **NO EJECUTADO en UE 5.8.2**. No se acredita
  consola jugable, diálogo, RHI real ni integración con Valhalla/Sutherland.

Estado, evidencia y continuación local:
[informe P01](../../../proyecto/docs/roadmap/master/fases/F05/F05-P01_IMPLEMENTACION.md)
y [validaciones MSI](../../../proyecto/docs/roadmap/master/fases/F05/VALIDACIONES_PENDIENTES_MSI.md).
