# H06 · IA-03C-04 — Diseño funcional y contrato UX de Nueva partida / Continuar

**Fecha:** 21-11-2026. **Responsable del diseño:** ChatGPT. **Ejecución prevista:** Codex, GPT-6, razonamiento ALTO (Cloud para fuentes; MSI para Unreal real).  
**Estado:** DISEÑADO / NO IMPLEMENTADO / NO PROBADO EN UE. **No equivale a certificación M1.**  
**Repositorio:** `robdor80/Videojuego_StarTrek`. Proyecto principal: `juego/UE5/StarTrekRPG/StarTrekRPG.uproject` (UE 5.8.4).

## 1. Propósito, límites y criterio de éxito

Diseñar una **interfaz mínima funcional en castellano** para iniciar y continuar la candidatura de Academia utilizando **exclusivamente** el HOST existente. No es un editor general de personaje, ni una escena 3D, ni la interfaz gráfica final.

Un flujo considerado funcional es: menú -> Nueva partida -> nombre -> CREATE Academy v2 -> BOUND confirmado -> QUERY candidato -> primera SAVE H04 confirmada -> ficha de candidatura; después cerrar partida y, en otro proceso Unreal, menú -> Continuar -> recorrer SLOTS paginado -> elegir **versión exacta** recuperable -> RESTORE H04 -> QUERY -> misma campaña/PERSON/hecho, nueva generación.

**Fuente de verdad:** CoreRPG. El HOST coordina. Unreal solo presenta proyecciones y envía solicitudes. Crear candidato NO supone matrícula, admisión, curso, rango, nave, plaza o competencia F05/F11. El protagonista S04 v2 es canónico y **solo se edita su nombre**; nunca especie, sexo, edad, biografía, procedencia, PERSON ni hechos. No introducir un segundo editor de biografía ni reutilizar el formulario histórico IA-03A como pantalla de entrada.

No abrir nuevas C-06/C-07, no crear un nuevo proyecto UE ni mover C-04 hacia F10/F11, cinemática, escenarios, NPC/voz, IA LIVE, cosmética o misiones. Todo eso mantiene sus dependencias y fases.

## 2. Base real inspeccionada: qué puede consumir la UI

Revisados en `main` tras fusión de #193/#194/#195: `HostSessionSubsystem.{h,cpp}`, `HostRuntime`, `HostDiagnosticGameMode`, `HostAcademyAutomation.cpp`, `academy_abi.h`, `DefaultEngine.ini`, `StarTrekRPG.Build.cs`, `AGENTS.md` y los documentos C-01/C-03 y tablero H06.

| API existente de C-03 | Qué significa para C-04 |
| --- | --- |
| `UHostSessionSubsystem::IsAvailable()`, `IsInitializing()`, `GetAcademyAvailability()`, `IsTransitioning()`, `GetStatus()` | Disponibilidad y control de transiciones; no asumir que cargar DLL implica sesión operativa |
| `CreateAcademy(World, Name)` | Admite CREATE con nombre validado por HOST; respuesta inmediata OK **solo admite ticket** |
| `QueryAcademy(World)` | Consulta autoritativa de candidatura ya vinculada |
| `ListAcademySlots(World, Cursor)` | Lee página Academy SLOTS; `Cursor=0` inicia; máximo 64 filas y `NextCursor` puede continuar incluso tras página vacía |
| `RestoreAcademy(World, FHostAcademySlot)` | Restaura versión H04 exacta **solo desde CLOSED**, y H04 la vuelve a comprobar |
| `Save(World, Slot)` / `Close(World)` | Guardado versionado H04 y cierre de la sesión; ambos asíncronos y con resultado separado |
| `UHostWorldProjection::GetAcademyCandidate()` | Ficha de lectura: campaña, nombre, PERSON, hecho, revisión, tick, digest y estado candidato |
| `GetAcademyPage()` / `GetAcademyResult(Operation)` / `GetCompletion()` | Página de lectura, resultado de Academy por operación y resultado ABI v1, respectivamente; las vistas pueden invalidarse al viajar o cambiar generación |

**Limitación contractual importante:** las filas SLOTS incluyen campaña UUID, ranura, versión, familia, formato, procedencia, compatibilidad, recuperabilidad y motivo de rechazo. **No incluyen nombre de candidato, fecha, hora, duración, misión ni ubicación**. La UI NO debe inventarlos, inferirlos de versiones o leer los archivos del almacén por su cuenta. Mostrar etiquetas «Partida [UUID abreviado]», «Ranura [texto]», «Versión [número]». El nombre se muestra **solo después** de RESTORE + QUERY. Tampoco existe un atributo «última vez jugada» para ordenar por recencia: respetar la ordenación determinista nativa (campaña ASCII, ranura ASCII, versión descendente).

## 3. Decisión de implementación: interfaz reconstruible desde Git

**Opción aprobada para C-04:** interfaz mínima **Slate/C++** sobre el proyecto Win64 actual, aprovechando los módulos `Slate` y `SlateCore` ya presentes y el panel de diagnóstico existente. Componentes visuales: textos, campo de nombre, lista desplazable, botones, indicadores de actividad, mensajes de error y confirmaciones.

Motivo: `*.uasset` y `*.umap` están ignorados en Git; crear ahora una UMG esencial que no viaja en la PR impediría reproducir la implementación en Cloud/CI y protegerla. El uso de Slate aquí **no prohíbe** una interfaz UMG/LCARS definitiva cuando la infraestructura de recursos y copias esté comprobada.

**Entrada reproducible requerida:** incorporar un modo de menú Academy activable explícitamente, por ejemplo `-AcademyMenu`, reutilizando el mapa diagnosticable y el controlador actuales sin sobrescribir `Content/Diagnostics/HostDiagnostic.umap` ni eliminar el panel naval. Preservar por defecto la vía diagnóstica actual durante la validación C-04; la decisión de hacer Academy menú predeterminado del juego se tomará con evidencia en C-05. La UI de C-04 ha de ser accesible y testable, no limitarse a un diseño estático. No inventar un nuevo mapa/binario obligatorio. Si Codex encuentra una alternativa más simple con el mismo aislamiento, documentar por qué.

**Fronteras:** la UI obtiene un `UHostSessionSubsystem` de su `GameInstance` y la `UHostWorldProjection` del mundo en curso. No abre `TrekHostClient`, no carga DLL, no ejecuta operaciones de Core directamente, no utiliza `person_id` como autorización y no crea un segundo sistema de persistencia. Las copias visuales de `FHostAcademyCandidate` y `FHostAcademySlot` son DTO de lectura, no estado autoritativo.

## 4. Estructura de pantallas, navegación y textos

### M0 — Menú Academy

```text
STAR TREK LEGENDS — ACADEMIA
[ Nueva partida ]    [ Continuar ]    [ Salir ]
Estado del HOST: Conectando... / Disponible / No disponible
```

- Mostrar `Conectando con HOST…` mientras `IsInitializing()`; no ejecutar acciones prematuras.
- `Nueva partida` y `Continuar` habilitados solo con cliente y Academy v2 disponibles, estado de sesión permitido y sin transición incompatible.
- Si Academy v2 no está disponible pero la ABI naval v1 sí lo está, mostrar «Academia no disponible»; **no recurrir a OPEN naval**.
- El menú no realiza automáticamente CREATE, RESTORE ni SAVE al abrirse, ni por reproducir/saltar una intro futura.
- `Salir` solicita cierre seguro si existe sesión; no declarar guardado sin respuesta OK.

### M1 — Nueva partida

```text
NUEVA PARTIDA — ACADEMIA
Tu protagonista está definido por la historia.
Nombre del personaje: [____________________________]
[ Crear candidatura ]      [ Volver ]
```

- Único campo modificable: **nombre**. No casillas de raza, sexo, edad, biografía ni credenciales.
- Texto con caracteres Unicode; comprobar límites de la API: **máximo 96 bytes UTF-8**, no 96 letras. Se puede hacer una validación orientativa en el campo, pero **la decisión es siempre la de HOST/S04**. No truncar ni «corregir» en silencio; mostrar rechazo recibido.
- Al pulsar «Crear candidatura» una vez: congelar edición, inhabilitar dobles pulsaciones y observar CREATE. `TREK_HOST_OK` al enviar = **admisión**, no «personaje creado».
- En `RETRY`, reintentar únicamente cuando no se haya admitido ticket; en error terminal mostrar mensaje y permitir corrección. En `IDEMPOTENCY_CONFLICT` no crear de inmediato con otra clave ni otra campaña; explicar el conflicto y ofrecer reanudar nombre exacto, volver o cerrar sesión según estado.
- Tras CREATE completado OK, validar generación y ejecutar QUERY; solo mostrar «Candidatura creada» si QUERY ha confirmado candidato y vínculo. Una transición que destruya el mundo requiere reanclar la proyección nueva y consultar, **nunca reenviar CREATE por un viaje de mapa**.
- Se inicia **primera SAVE H04** en ranura estable `principal` después de confirmar vinculación; el indicador «Partida guardada» solo aparece tras resultado final SAVE OK. Este guardado inicial evita que el usuario salga con una candidatura volátil creyéndola persistente.
- Si falla el guardado, conservar la campaña activa y mostrar «Candidatura creada, pero aún sin guardar». Ofrecer `Reintentar guardar` y `Cerrar sin guardar` con confirmación inequívoca. Si H04 informa publicación incierta, NO repetir ciegamente: explicar que el estado debe comprobarse por H04/catálogo antes de una nueva solicitud.
- No salir del proceso ni cerrar automáticamente el CLIENT durante CREATE, QUERY o SAVE pendientes.

### M2 — Continuar

```text
CONTINUAR — PARTIDAS DE ACADEMIA
Partida 4e31…  | Ranura principal | Versión 65 | Recuperable
Partida 4e31…  | Ranura principal | Versión 64 | Recuperable
Partida 9bf2…  | Ranura principal | Versión  7 | Dañada — no recuperable
[ Recuperar versión seleccionada ]
[ Cargar más ]             [ Empezar listado ]    [ Volver ]
```

- SLOTS debe consultarse **sin introducir manualmente el UUID**. Solicitar `ListAcademySlots(World, 0)` y avanzar con `NextCursor` hasta cero o cuando usuario pida «Cargar más».
- Mostrar **solo familia Academy** (`TREK_HOST_KIND_ACADEMY`). Las filas navales permanecen íntegras en HOST pero no constituyen candidaturas. Si la página contiene solo filas navales, o es vacía y `NextCursor≠0`, **no declarar terminado el catálogo**: continuar asíncronamente o dejar accesible «Cargar más». Como máximo una petición SLOTS pendiente a la vez, sin bucles síncronos en el Game Thread.
- Una versión dañada/no compatible/no recuperable debe poder verse identificada como tal (información de diagnóstico de lectura), pero **no habilita Recuperar**. Mostrar motivo estructurado de H04 traducido al español, sin afirmar «guardado perdido» por un error de enumeración.
- Las versiones no son fechas. No mostrar «hoy», «más reciente» global o «última partida» inventados. Presentar campaña abreviada, ranura, versión y estado. El UUID completo se conserva internamente para `RestoreAcademy`.
- Preferir una página visible de hasta 64 filas para memoria acotada, con navegación «Cargar más»/«Empezar listado». Se puede mantener historial limitado de cursores de UI; ningún cursor es durable y un token expulsado puede caducar. El retroceso fiable siempre puede reiniciarse con cursor cero.
- `GENERATION_EXPIRED` (SAVE, CLOSE, RESTORE, cambio de generación, token expulsado o extranjero): descartar las páginas y selección antiguas, notificar «El listado ha cambiado; actualízalo» y ofrecer reinicio en cursor cero; no repetir en bucle sin límite.
- `CAPACITY_LIMIT` o `RETRY`: mensaje y opción de reintentar; no interpretar una página vacía con cursor de continuación como «sin partidas».
- Seleccionar fila recuperable y confirmar la versión exacta con `RestoreAcademy(World, Row)` desde `CLOSED`. Mostrar actividad hasta completion v1 RESTORE OK. Si el archivo cambia entre lista y elección, H04 puede rechazarlo: conservar lista/reiniciar y avisar; **el listado no autoriza RESTORE**.
- Tras RESTORE, consultar la ficha con QUERY y verificar nueva generación. La UI no altera nombre, PERSON, checkpoint ni hecho; mostrar solo los datos proporcionados por CoreRPG.
- Cuando ninguna versión Academy existe tras agotar páginas, texto «No hay candidaturas guardadas» y botón «Nueva partida». Si HOST o SLOTS fallan, mostrar error (nunca afirmar falsamente «no hay partidas»).

### M3 — Ficha / partida activa

```text
EXPEDIENTE DE CANDIDATURA — ACADEMIA
Nombre: [nombre confirmado por CoreRPG]
Estado: Candidato
Campaña: [UUID abreviado]
[ Guardar ]   [ Guardar y cerrar ]   [ Cerrar partida ]
Mensaje de guardado: Guardado confirmado / Pendiente / Error
```

- Estado de candidatura: `TREK_HOST_CANDIDATE`, no «cadete admitido», «oficial», ni rango.
- Datos técnicos (PERSON, hecho, revisión, tick, digest) pueden mostrarse bajo «Detalles técnicos», **solo lectura**, sin presentarlos como credenciales.
- `Guardar` usa H04 `Save(World, "principal")`, genera versiones históricas y espera completion final. Nunca llamarlo al pintar la pantalla o desde Tick automáticamente.
- `Guardar y cerrar`: guardar; esperar éxito; CLOSE; esperar confirmación; volver a M0. Si SAVE falla o es incierto, no cerrar silenciosamente.
- `Cerrar partida`: si hay cambios o guardado no confirmado, confirmar explícitamente «Se perderá el progreso desde el último guardado»; usar CLOSE. No borrar campañas ni versiones.
- «Salir del juego» sigue el mismo principio de cierre seguro; el proceso puede abandonar la vista solo tras reflejar la situación de SAVE/CLOSE. Nunca mostrar «Guardado» a partir del mero ticket OK.
- Tras viaje de `UWorld`, la pantalla antigua deja de recibir resultados y la nueva pantalla lee `GetStatus` y vuelve a solicitar QUERY; no vuelve a crear PERSON.

### M4 — Confirmaciones y mensajes

- Confirmación de versión: «¿Recuperar la versión N de la ranura [X] de la partida [ID abreviado]?»
- Error de nombre: «El HOST ha rechazado el nombre. Revísalo e inténtalo de nuevo».
- Servicio indisponible: «No se puede acceder al HOST de Academia. Comprueba que las bibliotecas estén preparadas».
- Estado sin guardar: «Candidatura creada, pero el guardado aún no se ha confirmado».
- Archivo incompatible/corrupto: «Esta versión no se puede recuperar: [motivo]».
- Error de cursor: «El listado ha caducado. Vuelve a cargar las partidas».
- Identidad/vínculo no válido: «No se ha podido verificar la candidatura. No se ha iniciado una partida jugable».

Usar textos localizables, controles de teclado/foco y botones con etiquetas; no depender únicamente de color. Estado ocupando pantalla visible, nunca spinner perpetuo sin explicación si una operación falla. La pantalla no convierte códigos de error en acciones automáticas destructivas.

## 5. Máquina de estados UX (no sustituye al estado HOST)

| Estado de presentación | Entrada | Transición aceptada |
| --- | --- | --- |
| `STARTING` | Panel aparece; cliente aún no disponible | `READY_CLOSED` si Academy v2 está listo; `UNAVAILABLE` en error |
| `READY_CLOSED` | HOST en CLOSED | `EDIT_NAME`, `BROWSING` o cierre de proceso |
| `EDIT_NAME` | Nueva partida; sin sesión activa | `CREATING` tras submit admitido |
| `CREATING` | Ticket CREATE pendiente | `VERIFYING` tras completion OK; `ERROR` en fallo |
| `VERIFYING` | QUERY de candidato BOUND | `INITIAL_SAVE` si correcto; `ERROR` si no |
| `INITIAL_SAVE` | Primer SAVE H04 | `ACTIVE` tras completion OK; `ACTIVE_UNSAVED` si falla |
| `BROWSING` | SLOTS paginado | `RESTORING` con selección válida; `READY_CLOSED` al volver |
| `RESTORING` | RESTORE v1 exacto pendiente | `VERIFYING_RESTORE` tras completion OK |
| `VERIFYING_RESTORE` | QUERY tras RESTORE | `ACTIVE`, sin otro CREATE |
| `ACTIVE` | Candidato válido; guardado confirmado | `SAVING`, `CLOSING` o vista estable |
| `ACTIVE_UNSAVED` | Candidato válido pero SAVE no confirmado | Reintentar con cautelas H04 o confirmar cierre sin guardar |
| `SAVING` | Ticket SAVE pendiente | `ACTIVE` al confirmar; error/indeterminación tratado expresamente |
| `CLOSING` | Ticket CLOSE pendiente | `READY_CLOSED` al confirmar |
| `UNAVAILABLE / ERROR` | Fallo de disponibilidad/operación | Reintentar acción admisible o salir sin engañar al usuario |

**Política fundamental:** un único comando en curso para cada flujo de UI; usar el estado y los tickets nativos, no temporizadores para decidir si CREATE/SAVE/RESTORE «han terminado». Si el usuario vuelve a abrir el menú, rehidratar únicamente con consultas HOST. Los reintentos de submit RETRY deben tener un límite/backoff respetuoso, pero un ticket admitido nunca se reenvía a ciegas. CLOSE mantiene su reserva nativa para cancelación/abandono seguro cuando proceda.

## 6. Estética y requisitos mínimos

- Identidad: **Star Trek Legends**, idioma español de España; estilo provisional oscuro/negro espacial con acentos azul/cian LCARS compatibles con la dirección artística A2, sin imponer iconografía ni fondos nuevos.
- Pantalla horizontal, legible a 1920×1080 y también 2560×1600; no diseñar para móvil ni integrar aquí el menú de la intro audiovisual.
- Botones claros, resaltado de teclado, control de foco, estados deshabilitados visibles, mensajes no solo de color; scroll correcto con listas largas y texto truncado con acceso a información completa.
- Nada de logos o fotografías externas ni nuevas texturas obligatorias. Recursos de la UI mínima generados por código Slate para quedar versionados en Git.
- El diagnóstico naval debe seguir disponible y sus automatizaciones previas no se eliminan ni se convierten en Academia.

## 7. Contrato de implementación para Codex (sin código en esta PR)

**Responsable:** Codex Cloud, GPT-6 / razonamiento ALTO. Basarse en la rama de esta PR o en `main` después de fusionar el diseño. Implementar C-04 **en el mismo proyecto UE**, preferentemente panel Slate C++ y pequeña capa de controlador de presentación asociada a mundo. No reconstruir HOST. Respetar `HostSessionSubsystem.h` y la extensión Academy v2. No editar `CoreRPG`, `F11`, `S04`, ABI naval, pin, ni pruebas LOCKED.

Se exigen expresamente:
1. Entrada reproducible al menú Academy sin destruir la vía diagnóstica, con selector `-AcademyMenu` o equivalente justificado.
2. M0/M1/M2/M3 y confirmaciones; UI navegable por teclado y ratón con etiquetas en castellano.
3. Nueva partida con único nombre, creación BOUND, QUERY y guardado inicial confirmado.
4. Continuar con lectura completa paginada, cursor de páginas vacías, selección de versión H04 exacta y errores; sin fechas/nombres ficticios en el catálogo.
5. Ficha solo lectura; guardado manual y guardar/cerrar; no salida silenciosa con cambios volátiles.
6. Adaptación a generación, transición, cambio de mundo y errores del HOST sin doble CREATE ni dobles tickets.
7. Pruebas automáticas del controlador/flujo en la medida permitida; ejecutar CTest/SDK/CI accesibles en Cloud y preparar automatizaciones Unreal/UI sin declarar que corrieron allí.
8. Proteger todos los assets `.uasset`/`.umap` ignorados; temporales solo en `laboratorios/`; no crear dependencias finales del laboratorio.
9. PR Draft independiente, informe técnico permanente de C-04 y actualización de `H06_CONTROL_UNICO_ESTADO_2026-11-21.md`; **NO fusionar sin usuario**.

**Excepción de alcance para Codex:** si la UI necesita algún método de lectura complementario en `HostSessionSubsystem`, agregar solo adaptador UE claramente documentado; no ampliar contratos nativos CoreRPG/H04 ni inventar un campo de fecha/nombre por campaña.

## 8. Matriz de aceptación específica C-04 (planeada, NO ejecutada)

| ID | Escenario / procedimiento | Oráculo esperado |
| --- | --- | --- |
| UX-01 | Iniciar sin DLL o Academy v2 | Menú muestra indisponibilidad, no hace OPEN naval como sustituto ni se bloquea |
| UX-02 | Nombre vacío, exceso UTF-8, Unicode inválido rechazado por HOST | No crea PERSON ni guarda, muestra error coherente |
| UX-03 | Crear con nombre válido y pulsar dos veces | Un CREATE admitido; una campaña/PERSON/hecho; esperar BOUND/QUERY |
| UX-04 | Nueva partida y primera SAVE | «Guardado» solo tras completion SAVE OK; ranura `principal` recuperable |
| UX-05 | Fallo o publicación incierta de SAVE | Estado no confirmado, sin cerrar ni repetir ciegamente |
| UX-06 | Reiniciar proceso, abrir Continuar | SLOTS se consulta desde CLOSED, sin UUID manual |
| UX-07 | Más de 64 versiones, mezcla naval y Academy, página vacía con cursor | Todas las versiones Academy accesibles; naval filtrada; no falso «no hay partidas» |
| UX-08 | Fila H04 corrupta/no recuperable | Fila visible y bloqueada; otra versión buena restaurable |
| UX-09 | Recuperar versión 1 exacta | RESTORE H04 y QUERY: misma campaña/PERSON/hecho, generación distinta |
| UX-10 | SAVE/CLOSE/RESTORE caduca cursor | UI descarta selección, ofrece recargar desde cero |
| UX-11 | Cambiar UWorld durante CREATE/QUERY | No crea doble PERSON ni aplica la vista del mundo destruido |
| UX-12 | Guardar y cerrar / cerrar sin guardar | Mensajes y confirmaciones correctos; estado CLOSED y sin supuestos de guardado |
| UX-13 | Abrir panel diagnóstico naval histórico | OPEN/VIEW/SAVE/RESTORE/CLOSE v1 sin regresión |
| UX-14 | Reabrir una campaña Academy | La ficha muestra candidato, no admitido/oficial/naval, y F05 sigue denegado |
| UX-15 | Prueba visual/teclado en editor/juego Win64 | Menú accesible, selección por teclado/ratón, estados y etiquetas legibles |

**Pruebas Cloud del diseño documental:** revisión contra fuentes Git y presencia del fichero en PR. No afirmar PASS para UX-01…15 ni para UBT, NullRHI, D3D12, MSIs o aceptación del usuario. C-03 mantiene expresamente sus **ocho verificaciones MSI NOT_RUN**: UBT Editor, UBT Game, NullRHI, D3D12, viaje UWorld, DLL en UE, CREATE/SAVE/RESTORE entre procesos UE, prueba interactiva. C-04 añade sus verificaciones propias; no cancela ninguna de las anteriores.

## 9. Dependencias, riesgos y puerta de cierre

- **C-03 fusionada ≠ probada en UE 5.8.4**. La compilación UHT/UBT y el lifecycle real del panel siguen expuestos a incidencias que Cloud no detecta; no ocultarlas en la PR de interfaz.
- **Persistencia solo tras SAVE confirmado.** CREATE BOUND sin SAVE sigue siendo volátil. No inventar autoguardados ajenos al H04 real.
- **El catálogo es lectura viva**, con posible caducidad de cursor y filas cambiantes; identidad y restauración se revalidan con H04/Core.
- **Assets no versionados:** no depender de UMG/mapas binarios nuevos en C-04 sin estrategia de copia y regeneración probada.
- **No reproducir ni saltar la intro para crear campaña.** La intro audiovisual se integrará después y no es requisito de M1.
- **Cierre de mi parte:** documento aprobado en PR Draft, tablero alineado, implementación Codex pendiente.
- **Cierre posterior de implementación C-04:** código y tests disponibles entregados, auditoría ChatGPT favorable, pruebas UE/MSI anotadas sin falsos PASS. **Cierre M1:** únicamente C-05 tras verificación UE real y aceptación del usuario.

**Estado final del documento:** DISEÑADO; sin código, sin pruebas de ejecución Unreal, sin certificación y sin fusión.
