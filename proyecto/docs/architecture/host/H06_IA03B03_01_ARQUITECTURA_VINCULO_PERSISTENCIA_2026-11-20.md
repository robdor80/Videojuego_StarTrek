# HOST H06 / IA-03B03-01 — Arquitectura de vínculo H03 y persistencia H04 de Academia

**Fecha:** 20-11-2026 · **Responsable:** ChatGPT (arquitectura y revisión del código)  
**Estado:** PROPUESTA DE INTEGRACIÓN / SOLO DOCUMENTACIÓN; **NO IMPLEMENTADO NI PROBADO EN RUNTIME**.  
**Base:** `main` posterior a las PR #188 y #189 fusionadas; CoreRPG fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`.  
**Fase siguiente:** IA-03B03-02/03, Codex Cloud; auditoría B03-04 por ChatGPT.  
**Objetivo verificable:** crear mediante B02 → vincular legítimamente al jugador local mediante H03 → guardar Academia mediante H04 → cerrar el proceso → cargar la MISMA PERSON y campaña, sin F05 ni hechos profesionales ficticios.

## 1. Resultado de la inspección real y alcance

| Código revisado en main | Situación actual comprobada | Consecuencia para B03 |
| --- | --- | --- |
| `src/f10/academy_campaign.{h,cpp}`, `academy_candidate_factory.h` | B02 construye en `corerpg::WorldState` una PERSON, un hecho `candidate_created`, fuente autoral, identidad de campaña y nombre; el Core está en `AcademyCampaign` y se consulta mediante recibo privado | Se puede **reutilizar** ese mismo WorldState y catálogo para H03/H04; no hay que crear otro protagonista |
| `src/session_owner.cpp` | `AcademyCreationIntent` y `AcademyCreationReceipt` son privados, ligados a sesión/generación/perfil; B02 publica candidatura `ACTIVE` pero `UNBOUND` | B03 debe vincular sin aceptar ningún `person_id` arbitrario desde UI |
| `src/native_session.{h,cpp}` | Una única reserva de campaña protege `session_` naval y `academy_`; `commit_academy` ya almacena el objeto Core en memoria | Construir snapshot y stage/restore Academy sobre el miembro existente; no abrir Miranda |
| `src/player_bootstrap.h`, `session_owner.cpp` | `PlayerBootstrap::prepare/bind` naval resuelve F04 PERSON y termina llamando a `f05_bind_player`. La ruta Academy se rechaza expresamente | Crear **un vínculo H03 de Academia distinto del naval**, sin alterar las firmas ni aceptar F05 como credencial |
| `SessionOwner::current_player` | Devuelve `PlayerIdentity{generation, person_id}` sólo si `binding==BOUND` | Reutilizar proyección para ambos escenarios, con revalidación del tipo y pertenencia en cada operación |
| `SessionOwner::Impl::execute(Dispatch&)` | Una vez `BOUND` despacha al gateway F05 sin comprobar el tipo de campaña | **RIESGO P0 de B03:** al vincular Academy no debe entrar en gateway naval con `session_==nullptr`. Añadir bloqueo explícito por `Academy` *antes* de cualquier llamada a F05/bridge |
| `SessionOwner::Impl::execute(Save&)` | `academy_receipt` devuelve `SAVE_INCOMPATIBLE`; si no, exige vínculo F05 | Añadir SAVE académico independiente, conservando flujo naval intacto |
| `src/slot_store.{h,cpp}` | H04 v1 fija `TREKHOST4 1` y una tupla F05 de `person/record/revision/tick` en manifiesto y registro; verificación antes de `COMMITTED` | Un `Academy` requiere sobre discriminado/versionado y **ancla de identidad propia**; no reinterpretar v1 ni sustituir la tupla F05 |
| `src/f04_session_bridge.cpp` | El lector H04 abre `f04_create(1,"miranda",...)` y reconstruye un vínculo F05 | Esta ruta debe continuar SÓLO para slots navales; lector Academy con catálogo de producto y CoreRPG |
| `src/f10/academy_campaign.cpp` | `stage` crea IDs y `inspect` depende de `campus_`, `person_`, `creation_fact_`; no hay factory de recuperación | B03 debe **reconstruir esos miembros al recuperar** desde el WorldState guardado; jamás llamar a `stage` de creación como sustituto de LOAD |
| `src/f10/academy_campaign.cpp` | Guarda nombre y campaña como relaciones ordenadas; catálogo `starfleet_academy/v2`; no consume plazas; origen canónico S04 v2 por hash | Guardar y verificar el catálogo exacto, UTF-8, nombre, origen, PERSON y hecho sin introducir datos no conocidos |

**Ni B02 ni el ensayo antiguo `academy_core_feasibility.cpp` acreditan todavía SAVE/LOAD productivo.** Esta B03-01 define cómo hacerlo; no ejecuta pruebas.

## 2. Arquitectura acordada como objetivo (conceptual, no nuevas APIs ya existentes)

```text
Nueva campaña Academia (B02 ya fusionada)
     SessionOwner / hilo Core propietario
         | AcademyCandidateFactory::create()
         v
     AcademyCampaign (Core WorldState real)
         PERSON + candidate_created + fuente S04 + nombre
         |
         | B03: H03 vincula principal LOCAL a la PERSON exacta
         |      comprobando recibo privado + identidad Core
         v
     Campaña Academy BOUND (sin capacidad F05)
         |
         | H04: snapshot del mismo WorldState/historial/RNG/reloj
         v
     Slot H04 Academy VERSIONADO + registro local + COMMITTED
         |
      Cierre del proceso / nuevo SessionOwner
         |
         | H04: validación de sobre, procedencia, catálogo,
         |      histórico Core, ancla PERSON y vínculo H03
         v
     AcademyCampaign RESTAURADA en staging
         |
         | una única publicación, nueva generación
         v
     MISMA PERSON, mismo historial y estado academic candidate,
     BOUND local válido, sin F05 ni comisión F11
```

**Principio de unicidad:** existe un solo WorldState autoritativo por campaña. El objeto `AcademyCampaign` lo posee durante la ejecución. La identidad H03 y la procedencia H04 son **metadatos técnicos del HOST vinculados a ese Core**, no un segundo almacén de biografía, académico o autoridad. No se pretende que una referencia numérica por sí sola conceda acceso.

## 3. H03: vínculo académico de identidad sin F05

### Entrada de confianza

1. B02 devuelve `AcademyReceipt` interno para la PERSON candidata de la activación. Su `inspect` comprueba campaña, fuente, revisión, persona y hecho contra `AcademyCampaign::inspect()`.
2. El dueño H03 verifica que el intento pertenece al mismo principal local y generación activa; la PERSON tiene definición Core de `person`, está vinculada a campus y hecho de candidatura, y **no hay otro sujeto jugable** en esa campaña.
3. Una operación interna `bind_academy_player` (nombre conceptual) publica el vínculo si sigue `UNBOUND`; replay del mismo recibo no crea una segunda mutación ni revoca el sujeto. Si ya hay otro sujeto o la generación caducó, rechaza.
4. La proyección `current_player(generation)` devuelve el mismo `person_id` autorizado de Core bajo el ámbito presente. El ID se expone como dato de consulta, jamás como credencial o parámetro de selección pública.
5. Para origen local duradero, persistir **una constancia de vínculo verificable por procedencia de H04** (perfil local/campaña + ancla de creación validada + sujeto), sin un segundo WorldState. Si la implementación exige una relación/facto Core para reconstruir la constancia, debe ser una representación de control H03 documentada y autorizada, **no un hecho F10 de admisión**. No introducir `f05_bind_player`, `F04Ref` naval ficticio ni fila profesional F11.

### Ancla estable frente a generación mutable

El **ancla de creación** propone: `campaign_id` (UUID Core/HOST), `person_id` dentro del Core de esa campaña, `candidate_created_fact_id`, `S04 source identity/version/digest` y un identificador de vínculo local H03. Debe poder demostrarse desde hechos Core y registro local en LOAD. El perfil local no es el nombre diegético ni confiere poder naval.

**Separar expresamente valores inmutables de los mutables:**
- Persistir de forma estable el ancla anterior para continuidad. No usar `world.revision` o `tick` de una operación como ancla global inmutable de la campaña: avanzar el reloj, registrar una consecuencia o admitir al alumno no debe hacer imposible el guardado siguiente.
- Registrar la **revisión/tick del snapshot** en el sobre de la versión, cotejándola con Core al restaurar, pero permitir su evolución legítima entre versiones.
- La clave efímera/puntero `shared_ptr` del recibo B02 NO sobrevive al proceso. LOAD **reconstruye y revalida la identidad** desde Core + sobre/registro y emite un nuevo ámbito/recibo técnico interno ligado a la nueva generación; jamás reutilizar el puntero antiguo.

La admisión y el rango son otro dominio. `candidate` no consume plaza; `admitted` futuro necesita acto F10 y cohorte real. B03 no anticipa ese acto ni exige `cadet_year_1`.

## 4. Seguridad de operaciones: puerta explícita para Academy

B02 deniega órdenes porque su sujeto permanece `UNBOUND`. **Eso deja de ser garantía suficiente al vincularlo.**

Antes de publicar `BOUND`, el owner debe distinguir `Academy` de `Naval` y rechazar **todas** las operaciones navales (consulta de puente, `SUBMIT`, `ORDER`, `CANCEL`, `INSTITUTIONAL`), sin llamar a `bridge::dispatch` con sesión nula ni inventar una `F04Session` de academia. La denegación no debe mutar WorldState y debe mantenerse tras LOAD.

Puede utilizarse `ACCESS_DENIED` o `SERVICE_UNAVAILABLE` según la API existente, con significado estable y tests precisos. La futura consulta de ficha de Academy tendrá su propio puerto tipado, no un `query_view` naval disfrazado. F05/F11 quedan intactos.

## 5. H04: guardado tipado con compatibilidad retroactiva

### Decisión de formato: versión aditiva

**Conservar exactamente** `TREKHOST4 1` para navales: formato, lector F05, pruebas y slots existentes. Proponer un **formato nuevo separado** con discriminador `ACADEMY`, versión de esquema, versión/hash catálogo `starfleet_academy/v2`, pin CoreRPG, campaña, ranura y versión, ancla PERSON/hecho/fuente y marca de vinculación H03, más revisión/tick del snapshot. El nombre `TREKHOST4 2` es una **opción de diseño**, no una cadena ya implementada ni una decisión de wire obligatoria; Codex definirá el mínimo exacto, con rechazo de formatos desconocidos.

**No basta** añadir `scenario_id=academy` a `PersistentIdentity` v1 manteniendo F05 obligatorio: su registro F05 `person/record/revision/tick` tiene otro significado. Definir estructura/vía Academy tipada y no cambiar la interpretación antigua.

La **identidad duradera de registro** Academy debe anclarse a IDs/huella autoral inmutables; no al valor variable de revisión/tick. H04 necesita permitir varias versiones de una campaña sin rechazar una evolución legítima. Los datos variables son por *snapshot*, nunca una credencial inmutable de campaña.

### Publicación durable

Reutilizar la mecánica probada de H04: raíz de almacenamiento explícita, exclusión `host.lock`, raíces ancladas (sin symlinks/reparse), límites, carpeta de versión nueva, copia de estado/historial en área *staging*, comprobación de lector real, sincronización de archivos/directorios, manifiesto, `prepared` y **`COMMITTED`**, con resultado `PUBLICATION_UNCERTAIN` si el estado durable es ambiguo.

**Contenido de la foto real Academy:** mismo WorldState de B02 con la PERSON y `candidate_created`, fuente y antecedentes cualitativos, nombre, relaciones, historia Core, RNG y Timeline; además de metadatos técnicos H03/H04 que permitan su verificación. Sin datos gráficos ni cachés pesadas. Las versiones Core pueden repetir bytes de snapshot por durabilidad; no prometer deduplicación física entre versiones sin demostrarla. La biografía debe ser **una única definición lógica con referencias** en el estado, no una biografía duplicada por escena/NPC.

Para historia Core, el pin dispone de `HistoryPersistence::migrate/publish/recover` y `CampaignPersistence::capture/restore`. El ensayo nativo previo demuestra viabilidad de `migrate/recover`. Codex debe elegir el camino con las mismas garantías H04 y demostrar que **realmente recupera** el estado productivo Academy entre procesos. No serializar una ficha JSON decorativa ni usar `f04_history_snapshot` sobre una sesión naval.

### Inspección

`SessionOwner::inspect(root)` y `SlotInspection` deben distinguir tipo/versión y exponer compatibilidad/recuperabilidad reales para ambas familias. Los IDs del sobre son información de control; solo el lector de Core puede demostrar el sujeto y la fuente. Un importado sin constancia local debe continuar en `IMPORTED_UNVERIFIED` y no adquirir legitimidad por traer un campo `trusted=true`.

## 6. H04: recuperación de la MISMA PERSON, nunca alta nueva

1. Leer `SlotAddress` y seleccionar el último `COMMITTED` según las reglas H04; no saltar automáticamente una última versión confirmada corrupta.
2. Detectar familia/formato y verificar manifest/COMMITTED, árbol permitido, constancia del registro local, campaña UUID, versión y Core pin. Rechazar un slot naval con lector Academy y viceversa.
3. Seleccionar **catálogo Academy de producto en versión permitida** y verificar su huella y la del canon autoral. Si una versión legacy no está soportada, marcar `SAVE_INCOMPATIBLE`; **nunca convertir silenciosamente** una biografía libre en el héroe fijo.
4. Recuperar en **WorldState/RandomStreams/Timeline/HistoryArchive separados de la sesión activa** mediante el lector Core apropiado. Contrastar campaña, integridad, entidad PERSON, hecho `candidate_created` que apunta a ella, relaciones, origen de S04, exactamente una PERSON jugable y ausencia de plazas para estado `candidate`.
5. Reconstruir `AcademyCampaign` **a partir del estado recuperado**: hoy `inspect()` requiere `campus_`, `person_`, `creation_fact_`; esos IDs se obtienen y validan del grafo persistente, **no se recrean con `AcademyCampaign::stage` ni se presuponen ordinales de fixture**.
6. Comparar ancla inmutable y vínculo H03 contra el registro duradero de la raíz; verificar perfil local/identidad de campaña de acuerdo con la política local aprobada. Rechazar sustitución de PERSON por ID coincidente pero otra campaña, fuente o hecho.
7. Preparar estado de vinculación H03, nueva generación y todas las estructuras que puedan fallar antes de publicar. El dueño único hace **un solo swap controlado**, invalida tickets/recibos/vistas anteriores y publica `ACTIVE + BOUND` con la misma persona, sin llamar a F05.
8. Al fallar la preparación, mantener intacta una sesión activa válida, o CLOSED si la carga partía de cerrado. El cierre admitido durante la carga prevalece; una devolución tardía no reactiva una generación caducada.

**Restauración desde ACTIVE:** elegir e implementar de forma explícita una de dos políticas seguras: (A) stage Academy aislado + swap atómico conservando la campaña si falla, o (B) denegar esa restauración con error estable mientras exista una campaña activa, requiriendo `close()` antes. No ofrecer un swap parcial de Academy o un fallback naval. La ruta desde CLOSED y la recuperación entre procesos **sí son obligatorias**.

Un `receipt` de B02 ya caducado no es autoritativo tras LOAD: la identidad se deriva y verifica de Core + metadatos, no se solicita crear otro sujeto.

## 7. Estados / errores esperados y límites

| Operación | Éxito mínimo B03 | Error de seguridad |
| --- | --- | --- |
| Vincular Academy | `BOUND` a una PERSON candidata real del mismo Core | Recibo falso/otro owner, generación antigua, candidato distinto → `SCOPE_INVALID` o `IDENTITY_MISMATCH` |
| Consultar jugador | ID Core de misma campaña/generación | No vinculado → `PRINCIPAL_UNBOUND`; ámbitos antiguos → `GENERATION_EXPIRED` |
| Operación F05 desde Academy BOUND | Nunca alcanza F05; sin mutación naval | `ACCESS_DENIED`/error explícito |
| SAVE Academy | Version nueva `COMMITTED`, snapshot Core legible y vínculo verificado | No encuadernada/slot inválido → rechazar; publicación incierta → `PUBLICATION_UNCERTAIN` |
| LOAD Academy | Mismo Core subject, nombre, hechos, reloj, RNG, estado; generación nueva | formato/fuente/registro/campaña incompatibles → fail closed |
| Migración | Naval v1 legible por su ruta antigua; Academy v2 por su ruta nueva | No convertir saves v1 a Khan ni viceversa |

**No se afirma** compatibilidad automática de cualquier versión futura del catálogo, ni resurrección de un guardado no confirmado, ni que el nuevo candidato esté matriculado. No modificar el estado académico mediante metadatos de HOST.

## 8. Orden de implementación recomendado para Codex

1. Inventariar puntos de contacto reales `SessionOwner` / `NativeSession` / `SlotStore` / `AcademyCampaign`. Fijar el *wire format* Academy y la política de unión a perfil, versión y catálogos; documentar cualquier imposibilidad sin cambiar CoreRPG.
2. **B03-02: vínculo H03 Academy y puerta F05 explícita.** Pruebas de falso recibo, ámbito, replay, identidad y denegación de navales. No aceptar `person_id` de cliente.
3. **B03-03: persistencia tipada H04 Academy.** Crear snapshot desde la instancia B02, comprobarlo con lector real, versionar slots, restaurar entre procesos y reconstruir el estado sin volver a crear PERSON.
4. Pruebas de fallos, corrupción, idempotencia, formatos cruzados, continuidad de slots navales y build de producto. CI Windows/Linux/ASan y Release tests-OFF.
5. PR Draft y documento de implementación con trazas reproducibles. ChatGPT hará auditoría B03-04 y el usuario autorizará fusiones.

Codex puede subdividir su **implementación interna** para control de riesgo, pero no pedir una ronda de decisiones por cada helper. Si el Core pin impide **materialmente** mantener identidad o historia, describir la incompatibilidad real con evidencias y detener únicamente la modificación invasiva; no falsificar un PASS para cumplir el plan.

## 9. Restricciones y certificación

- CoreRPG, la fuente S04, F10 y F11 conservan sus autoridades. **No** modificar el pin, el checkout Core, pruebas históricas, ni contratos LOCKED. No inventar un evento de admisión o comisión para justificar el guardado.
- Un solo juego, inicialmente local y privado; sin servidores, cloud save, DRM ni control de propiedad del equipo.
- Ninguna ruta productiva depende de `laboratorios/`. Evidencia temporal únicamente en un laboratorio aislado conforme a `AGENTS.md`, sin dependencias de producto ni borrado de material preexistente.
- B03-01 **solo arquitectura documental**. B03-02/03 requieren código probado; IA-03C y M1 exigen posteriormente UE 5.8.4 real y aceptación MSI. No convertir "implementado" en "certificado".
- El resultado B03 debe demostrar **PERSON + candidatura + H03 + SAVE + RESTORE entre dos procesos**, verificando generación nueva y prohibición de órdenes F05.
