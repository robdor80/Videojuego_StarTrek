# H03-P01 — Contrato de identidad local y vínculo jugador–campaña–personaje

**Fecha:** 2026-11-13 · **Versión:** diseño 1.0 · **Estado:** DISEÑADO; NO IMPLEMENTADO NI PROBADO en H03.  
**Responsable:** ChatGPT (contrato) · Codex (implementación H03-P02/P03).  
**Dependencias:** H00/H01; H02 [PR #132 fusionada](https://github.com/robdor80/Videojuego_StarTrek/pull/132), `TrekHost` nativo; contrato F05 existente; H04 para continuidad durable.

## 1. Hechos comprobados

- H02 expone `trek::host::SessionOwner` (`open`, `close`, `snapshot`, `check_active`) y una `Generation` opaca. El único acceso real a la `F04Session` está encapsulado en el hilo propietario de H02; **no existe aún un vínculo de jugador en `TrekHost`** ni una operación pública de carga. Los estados `SAVING/LOADING` siguen reservados.
- `f04_bridge.h` define `F04Session` opaca, `F04Ref{scope,id}`, `f04_handles`, `f04_stats`, `f04_person`, `f04_manifest_page` y las operaciones F04. Un `F04Ref` no identifica por sí solo una sesión de HOST ni constituye autenticación.
- `f05_initiative.h` declara `f05_bind_player(F04Session*,F04Ref,uint64_t revision)`. La implementación de F05 valida `observer(s,p)`, impide sustituir un vínculo preexistente (conflicto), permite repetir el mismo vínculo de forma idempotente y exige revisión actual al vincular por primera vez. **Registra la selección en el Core de la campaña**, no en una tabla paralela.
- En la ABI pública F05 examinada no se observa una consulta dedicada de lectura de `f05_player`. No debe presumirse que existe un getter para restauración; cualquier carencia de lectura se resolverá con el propietario F05 sin acceder a internals del Core desde HOST.
- El proyecto UE principal no ha sido certificado aquí como aplicación final. Los `F04Handles` del escenario sintético son referencias de prueba, nunca prueba de que exista ya un flujo de creación del cadete de la Academia.

## 2. Identidades y sus límites

| Concepto | Responsable / duración | Capacidad legítima | No equivale a |
|---|---|---|---|
| `LocalPrincipal` | HOST, contexto local de un solo jugador | Identifica al usuario de la ejecución local frente al flujo HOST; selecciona su campaña desde una ruta permitida | Login externo, certificado o acreditación de la Flota |
| `CampaignIdentity` | Metadato de partida HOST + validación Core, estable tras guardar/cargar | Distingue campañas incluso con iguales IDs numéricos de entidades | `ship_identity`, scope, seed o licencia para mutar |
| `PlayerCharacter` | Entidad PERSON real en la campaña autoritativa Core, seleccionada por flujo confiable | Sujeto jugable único de esa campaña | Observador arbitrario aportado por Blueprint, NPC o IA |
| `F04Ref` / observador | F04/Core; scope efímero de la sesión | Referencia operativa resuelta en el hilo propietario | Identidad local, token de permiso o identidad persistente |
| `SessionGeneration` | H02; nueva en cada apertura y tras restauración | Rechazar solicitudes/callbacks caducados | ID durable de campaña |
| `F11CharacterId`, destino y rango | F11/CoreRPG | Hechos profesionales consultables según permisos y conocimiento | Campos elegidos por HOST o autorización institucional |

El acceso efectivo requiere la **coincidencia verificada** de principal local + campaña correcta + personaje correcto + generación viva + permisos del dominio. No se deduce de un número, `F04Ref`, causa de operación, nombre, save importado o texto del cliente.

## 3. Ciclo de vida lógico H03 (sin alterar estados H02)

`SessionOwner::ACTIVE` significa **campaña Core abierta**, pero no implica que las operaciones de jugador estén autorizadas. H03 introduce **estado de vínculo privado**, independiente de `State` H02:

- `UNBOUND`: campaña abierta sin sujeto admitido. Solo bootstrap/contenido inocuo estrictamente necesario; negar operaciones por personaje.
- `RESOLVING`: el hilo propietario valida la intención procedente del flujo controlado. Solo un intento en vuelo y ninguna operación de juego antes de completar.
- `BOUND`: `LocalPrincipal`, `CampaignIdentity`, sujeto PERSON estable y `Generation` activa coinciden; `f05_bind_player` ha aceptado el vínculo cuando corresponda.
- `INVALID`: incoherencia, error de restauración o vínculo previo incompatible; denegar por defecto, sin cambiar de personaje para «arreglarlo».

Al cerrar o fallar H02, invalidar vínculo operativo y respuestas pendientes antes de permitir nuevo acceso. Reabrir genera otra `Generation` y exige validación de vínculo; nunca reutilizar `F04Ref` del proceso anterior. No añadir un segundo hilo dueño de `F04Session`.

## 4. Alta de partida nueva

1. El HOST inicia la partida mediante el flujo local de confianza. La elección del personaje por interfaz es **una petición**, no una referencia autenticada ni un permiso.
2. Resolver en el propio contexto de campaña un sujeto PERSON elegible y real mediante consultas/autorización disponibles; su condición de «jugable» depende del flujo de creación admitido, **no se inventa** a partir de una prueba F04. No asignar automáticamente el `ensign` de un fixture como cadete final.
3. Comprobar exclusividad del principal local para esa campaña, ámbito correcto, generación vigente y no existencia de otro vínculo incompatible. El `F04Ref` operativo se resuelve dentro del hilo propietario.
4. Realizar `f05_bind_player` **por el mismo hilo propietario** con la revisión correcta cuando sea necesario para F05. El resultado puede mutar la revisión Core: no conservar la revisión anterior como si siguiera vigente. Un resultado de código ajeno a éxito deja el vínculo sin publicar.
5. Publicar `BOUND` de una sola vez después de validar el resultado completo. Ninguna UI/IA/NPC puede invocar un setter de actor, un `bind_player` libre ni pasar punteros `F04Session`.

El HOST no debe «autenticar» al usuario por conocer `person.id`, `ship_identity` o una supuesta firma local; el criterio de confianza es el control del flujo del proceso legítimo, no antitrampas frente al propietario del ordenador.

## 5. Continuación y restauración — frontera con H04

H03 especifica la invariante, **H04 aportará IO durable y carga**:

- Una campaña recuperada aporta identidad estable y metadatos mínimos de vínculo desde una ranura legítima, que deben contrastarse con el Core restaurado antes de habilitar juego.
- Un save extranjero válido **no** pasa a confiable por contener un ID conocido, rango, `CAUSE=110501` o un manifiesto editable. Cuando no exista prueba local suficiente de pertenencia, mantener `UNBOUND/INVALID` y denegar operaciones privilegiadas.
- El identificador Core estable del personaje debe resolverse en el scope actual y verificarse como PERSON perteneciente a la misma campaña. El scope anterior y `Generation` antigua quedan caducados.
- Si existe un vínculo F05 diferente, devolver conflicto y mantener el acceso cerrado; no cambiar `f05_player` ni reinterpretar expedientes. Si no se dispone de una API pública segura para inspeccionar el vínculo restaurado, **no inventarla ni consultar estructuras privadas**: registrar la dependencia con F05/H04 y mantener cerrada la recuperación afectada.
- H03 no publica archivos, no promete roundtrip entre procesos y no implementa `f04_load`/historial. La prueba de restauración durable se aplaza explícitamente a H04.

## 6. Contrato interno a concretar en C++ por Codex

Propuesta semántica, **no API ABI existente**:

- `bind_new_player(session_generation, trusted_creation_context)` (primitiva **interna**, no exportada a Blueprint/LLM) → vínculo o error; el sujeto se resuelve desde el contexto seguro, no desde un permiso enviado por cliente.
- `resolve_current_player(session_generation, local_principal_context)` → proyección mínima de sujeto validado o `PRINCIPAL_UNBOUND`; no expone `F04Session`.
- `invalidate_binding_on_close_or_restore()` y `validate_restored_binding(...)` → coordinación con H02/H04, no restaura por mera coincidencia numérica.

Codex definirá nombres, tipos y límites exactos al extender el `SessionOwner` existente; no crear un segundo objeto propietario de sesión. Son requisitos: cierre/competencia sin deadlock, FIFO del propietario o semántica equivalente auditada, errores sin efectos parciales, buffers sin datos en denegaciones, y no cruzar STL/excepciones/UObject por la ABI C.

Errores normalizados a documentar/probar: `PRINCIPAL_UNBOUND`, `ACCESS_DENIED`, `SCOPE_INVALID`, `GENERATION_EXPIRED`, `REVISION_STALE`, `IDEMPOTENCY_CONFLICT`, `BUSY_STATE`, `DOMAIN_REJECTED`. No adjudicar nuevos números F04/F05 sin comprobar cabeceras. H02 solo implementa parte de esta lista.

## 7. Relación con F11, H04, H05 y UE

- **F11:** HOST no emite grados, identidad profesional, órdenes institucionales ni permisos; lector F11 con control de divulgación será H07. Identidad jugable y oficial profesional se relacionan por hechos Core/F11, no por una tabla de rangos del HOST.
- **H04:** dueño de guardado, importación, procedencia y activación segura de una sesión restaurada; H03 proporciona validación de identidad, no añade una segunda persistencia.
- **H05:** al despachar órdenes, el actor/observador se resuelve de un vínculo `BOUND`, no se acepta de la UI. F05 decide competencia.
- **H06:** la interfaz Unreal consume una vista de «personaje actual»; nunca recibe `F04Session` o capacidad de cambiar actor sin flujo interno.

## 8. Riesgos, decisiones pendientes y cierre

| Riesgo | Mitigación | Estado |
|---|---|---|
| H02 solo abre población; personaje final Academia aún sin flujo certificado | Limitar H03 inicial a vínculo probado en campaña controlada; no afirmar creación jugable definitiva | Pendiente integración futura |
| F05 no expone lectura dedicada del vínculo persistido en cabecera pública | Acordar consulta solo lectura con dueño F05 o aplazar validación de restauración a H04; nunca acceso privado desde HOST | Pendiente Codex/F05 |
| Revisión Core cambia tras vincular F05 | Obtener/revalidar revisión antes de cada operación, test nativo | Planificado |
| Caller concurrente cierra mientras se vincula | Serialización H02, invalidación de generación y publicación atómica del resultado | Planificado |
| Metadatos de ranura y save no coinciden | Denegar y preservar campaña válida, prueba H04 | Planificado |

**Criterio de cierre de H03:** contrato + matriz revisados, vinculación controlada implementada y **probada** con el puente nativo real en Windows/Linux, rechazo de sujeto ajeno/campaña distinta/concurrencia y regresiones H02/F05. Pruebas durables de load/restore se etiquetarán «PENDIENTES H04» hasta existir implementación. **FUSIONADO no equivale a CERTIFICADO.**
