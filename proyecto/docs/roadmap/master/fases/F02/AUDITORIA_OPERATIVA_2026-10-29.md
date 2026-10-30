# F02-P01/P02: auditoría operativa, 29-10-2026

Complemento actual a los entregables históricos de 11–13 de octubre. No se reescriben sus líneas base ni los contratos de dominio. Referencia de planificación: [Plan Maestro](../../PLAN_MAESTRO.md) y [criterios oficiales](../../CRITERIOS_DE_CIERRE.md).

## Referencias y protección inicial

| Árbol | HEAD comprobado | Situación |
|---|---|---|
| CoreRPG local y `origin/main`, comprobado mediante fetch | `4f282863737bcd8f5add401202a9e1064c133672` | Limpio; ninguna modificación de fuentes |
| Star Trek checkout original local | `7ee52d59427ba9f1e027dd78200b938c37687f86` | `main`; 21 entradas no versionadas, incluidos informes y árbol Unreal Sutherland |
| Star Trek `origin/main`, comprobado mediante fetch | `00822e24ecd2333988e5b6369be1ae9e3089de01` | Ocho commits por delante del `main` local original |
| Base del trabajo aislado | `00822e24ecd2333988e5b6369be1ae9e3089de01` | Rama nueva `codex/f02-core-ue5-integration-20261029` |

Se comprobaron ramas locales y remotas antes de crearla: no existía una rama homónima. El trabajo se creó con `git worktree add -b ... <ruta aislada> origin/main`. La herramienta de worktrees gestionados rechazó el repositorio por estar fuera de las carpetas asociadas al chat; se utilizó Git directamente dentro del espacio de trabajo autorizado.

Inventario previo: **19.030 archivos originales**, incluyendo versionados, ignorados y no versionados. Se registraron por separado `git ls-files`, archivos ignorados, no versionados y estado Git. Se localizaron Blender/PBR/Unreal en `juego/Clase Miranda`, recursos de USS Sutherland y Valhalla en `assets`/`3D Star Trek`, y `TABULA RASA COPIA SEGURIDAD`, con sus proyectos experimentales. No se abrieron editores de esos recursos ni se ejecutaron sus scripts.

La comparación final de rutas, tamaños y mtime en nanosegundos confirma **19.030 antes / 19.030 después, cero archivos nuevos, ausentes o cambiados** en el checkout original. Es una comprobación de metadatos y aislamiento, no un hash completo de todos los assets. Las listas detalladas permanecen locales y se conservan además en un ZIP privado de Drive, con sus hashes individuales en el índice de evidencias; no incluye los contenidos artísticos. `main` local, sus archivos no publicados y CoreRPG permanecen intactos. Sólo el fetch actualiza referencias remotas Git.

## Capacidades comprobadas en headers, implementación y tests

| Capacidad real | Interfaz pública | Aplicación F02 / límite |
|---|---|---|
| Identidad y estructura | `WorldState::create_entity/contains/revision/place_entity`, `EntityId` | Una sola fuente de mundo. ID de 64 bits, cero inválido, ámbito de mundo |
| Relaciones y población | `entity_structure.hpp`, `declare_population/materialize_population` | Disponibles en Core; no equivalen a tripulación con agenda ni generación Trek |
| Catálogos | `ContentCatalog`, definición/binding, Content JSON opcional | Compilados y probados con suite Core. No se inventan payloads Trek |
| RNG | `RandomStreams`, `DeterministicRandom` | Flujo 7 del laboratorio, continuidad exacta tras restauración |
| Acciones y revisión | `ActionEngine::process`, `ActionRequest::expected_revision` | Colocación y tirada reales, rechazos atómicos. Actor no confiere autorización sobre objetivos |
| Simulación | `Simulation::step` | Driver de acciones ordenadas, no reloj, cola, historial ni agenda |
| Persistencia | `Persistence::capture/serialize/deserialize/restore/load` | Formatos v1/v2/v3 reales, validación e integridad. IO y exclusión de concurrencia son del Host |
| Conocimiento y visibilidad | `learn_fact`, `Visibility::project`, `ObserverView` | Proyección filtrada y pruebas negativas reales; no implementa contactos de Sensores |
| Contexto | `ContextBuilder::build` | Selección sólo desde vista autorizada; sin mutación ni RNG |
| Inspección | `Inspector` | Diagnóstico privilegiado disponible; no se expone a Blueprint/IA |

Se leyeron `CMakeLists.txt`, `tests/CMakeLists.txt`, headers públicos y el ejemplo `examples/authorized_context_host.hpp`. CMake fija Googletest y jsoncons por commit. La suite real incluye fallos de asignación, atomicidad, límites, seguridad, catálogos, contexto, persistencia y determinismo; no se sustituyó por fixtures Python.

**No se ha detectado un defecto reproducible del Core.** Los fallos encontrados fueron de ruta/harness/configuración del Host y se corrigieron en Star Trek. Core no recibió cambios ni commits.

## Reutilización de los entregables F02

Se conservaron y contrastaron todos los archivos del directorio F02, incluido el Plan Maestro, P01 remoto, P02, mapa/fronteras/secuencias/handoff P03, fallos P04, P05, D5 y auditorías previas de Sutherland. La auditoría geométrica histórica se reutiliza como antecedente; no se repite ni se declara una auditoría artística nueva. Los hashes de entradas figuran en `evidencias_20261029/input_inventory.json`.

Los validadores existentes comprobaron 24 fuentes/73 selectores P02, 12 fronteras/19 rutas/11 gaps P03, 13 fallos/6 ejes/16 casos P04 y 11 paquetes/13 invariantes P05. Sus estados históricos se mantienen con fecha; esta adenda registra las capacidades actuales sin ocultar los bloqueos anteriores.

| Adaptador | Conexión actual al Core real | Pendiente |
|---|---|---|
| ADP-01 identidad | Implementada para fixture, incluidos ámbitos de Host y continuidad | Alias semánticos de personaje/nave/campaña de producción |
| ADP-02 contenido | Core compilado con Content JSON y tests; laboratorio sin pack Trek | Payload/pack y referencias Trek de producción |
| ADP-03 tiempo | `Simulation` inspeccionada, sin reloj ficticio | Timestamp, agenda, guardias y actividad persistente |
| ADP-04 órdenes | Acción mínima con permiso Host revocable y revisión | Rangos, puestos, delegación temporal y órdenes Trek |
| ADP-05 sensores | Sin implementar en este laboratorio | Resolver barrido y observación Trek sobre Core |
| ADP-06 eventos | Consecuencias de ActionEngine disponibles | Event store causal persistente / bitácora |
| ADP-07 conocimiento | `ObserverView` y prueba anti-fuga del fixture | Contactos relativos, dossier y reglas de revelación Trek |
| ADP-08 persistencia | Roundtrip real de estado/RNG/conocimiento e identidad | Migraciones y datos de campaña aún no modelados |
| ADP-09 Unreal | Compilación, enlace, GameInstance y Actors reales | Integración posterior en proyecto de juego y controles de consola |
| ADP-10 IA | ContextBuilder real probado; sin entrada IA mutante | Proveedor/parser/transporte/deduplicación; opcional |
| ADP-11 interconsolas | Ninguna implementación nueva | Transferencia autorizada con procedencia Trek |
| EXT-01 Academia/NAP | Frontera conservada | Fuera del laboratorio mínimo |

## Compatibilidad y responsabilidades

Core posee estado, identidad, reglas genéricas y persistencia. Star Trek posee la política acotada del Host y las futuras reglas Trek. Unreal posee Actors, cámara, malla y presentación. La DLL no duplica el WorldState: encapsula el único objeto real del Core. Las copias de `CampaignSnapshot` son datos desconectados de persistencia, no otro motor.

No hay ABI C++ estable presumida: se utiliza ABI C v1 propia del laboratorio, build SHA fijo, memoria local a cada módulo y buffers copiados. `/MD` Release del puente/Core y módulo Unreal Development funcionan conjuntamente sin intercambiar objetos de STL. La DLL encapsula excepciones; el módulo Unreal no las habilita. El propietario único excluye concurrencia; el Game Thread gestiona UObject y visuales. No existe API Blueprint para cambiar WorldState.

La prueba de autoridad es un permiso mínimo revocable del fixture; **no valida la cadena de mando de Flota**. La proyección usa IDs de diagnóstico autorizados; **no es** el contrato SensorResult, que deberá seguir ocultando identificadores de verdad. Sin reloj, event store, órdenes Trek ni sensores operativos, el corte no acredita F03–F08 completas.
