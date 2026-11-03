# F05-P03 — Entrega de iniciativa NPC para auditoría independiente

Estado: **implementación nativa en revisión, PR Draft; no aprobación final**.
F05 permanece **EN_CURSO**, sin cierre global ni madurez CORE_INTEGRADO global.
F06 sigue bloqueada hasta todas las pruebas F05 obligatorias. P04/P05/F06 no se
han comenzado en esta entrega y ninguna PR debe fusionarse por esta publicación.

## Base y procedencia

Star Trek `robdor80/Videojuego_StarTrek`, rama nueva
`codex/f05-p03-npc-initiative`, desde main
`aff01c31c386fe0813320b82a828e2e6c5ab23d8`, comprobado remotamente antes de trabajar.
CoreRPG main remoto y pin compatible P01/P02:
`76a7b7b485616d8c4994f384a90f123bf333591d`, checkout limpio, sin cambios ni PR Core.
No se trabaja sobre ramas antiguas P01/P02. Sus PR #81/#82 ya están fusionadas.

Las regresiones antiguas preservan sus pins: F02
`4f282863737bcd8f5add401202a9e1064c133672`, F03
`9c53a33787de13d91eb2abe4da07033ee0fa1dc1` y campañas históricas F04
`89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`. El origen del oráculo F04 completo
sigue en `63d2401edaf85960b4baaf6b537ae571ba52a439`. No se alteran oráculos,
aceptaciones antiguas ni procedencia para obtener resultados positivos. El
manifiesto conserva las huellas previas de las dos fuentes F04 ampliadas.

## Resultado funcional

Una necesidad operativa autorizada de escanear durante un servicio de Sensores
F04 se guarda en Core y se comunica explícitamente a cada personaje. El capitán
NPC puede reconocerla, comprobar autoridad y proveedor de servicio, emitir una
orden P01 y permitir al operador NPC recibirla y ejecutarla. El efecto es la
consecuencia real `StreamRollAction{0xF0401,1,100}` de Core. No hay contactos de
sensores ni hallazgos inventados.

El controlador consulta `Visibility` y `ContextBuilder` por personaje, sin grants
temporales, y ejecuta como máximo una transición por evaluación. Reutiliza
F04Session, WorldState, Timeline, RandomStreams, ActionEngine, CampaignPersistence
e HistoryPersistence. Autoridad, puestos y guardias pertenecen a F04; órdenes a
P01; mandatos y aprobaciones a P02. No existe otro mundo NPC ni un scheduler global.
Los detalles de esquema, límites, keys, causalidad y reproducción están en
[INITIATIVE.md](../../../../../../desarrollo/integration/f05/INITIATIVE.md).

## Escenarios nativos reproducibles

| Escenario solicitado | Pruebas CTest P03 |
|---|---|
| A. Capitán NPC → operador NPC, efecto y eventos reales | `scenario` |
| B. Oficial sin autoridad, XO y ámbito de jefatura | `authority`, `preissue_relief` |
| C. Delegación P02 vigente | `delegation` |
| D. Revocada antes del efecto, sin eludir mandato | `revoked` |
| E. Relevo, incapacidad, fin de servicio | `relief`, `medical`, `watch_end`, `population_relief`, `selection` |
| F. Jugador ausente y capitán jugador | `player`, `player_captain` |
| G. Conocimiento insuficiente y no compartido | `knowledge`, `communication`, `bounded` |
| H. Persistencia, reinicio y replay | `idempotency`, `process_save`, `process_load`, `history`, `history_fault` |
| I. Fuera de escena, mismo futuro lógico | `determinism`, `scenario`, `process_load` |
| J. Campaña F04 realmente poblada | `population`, `population_relief` |

También se prueban `requirement`, `scope`, `atomic` y `corrupt`: creación
autorizada, revisión/scopes/hilo, colisión con keys P01, conocimiento y causalidad
inválidos en archivos aceptables para Core. Los dos tests de proceso se ejecutan
como procesos separados por CTest, con fixtures y comparación byte a byte de
futuros, decisiones, RNG y recuperación histórica.

## Validación de entrega

Ejecutado en Cloud Linux, GCC **14.2.0**, CMake **4.4.4**, Release/C++20:

| Suite | Recuento verificado | Resultado |
|---|---:|---|
| P03 | 26 | PASS |
| P01 íntegra | 20 | PASS |
| P02 íntegra | 20 | PASS |
| F04 cortas, organización, persistencia e historial | 261 | PASS |
| Total de la integración F05/F04 | **327** | **327/327 PASS**, sin omitidas |
| CoreRPG completo, JSON y BUILD_TESTING activados | 483 | PASS |
| F02 con su pin original | 15 | PASS |
| F03 con su pin original | 25 | PASS |
| Campañas históricas F04 con oráculos originales | 6 | **6/6 PASS**, incluidos 730 días |
| Tests documentales F05 | 22 | PASS; no acredita runtime |
| Fixtures documentales F05 | 48 | Sin fallos; no acredita runtime |
| Referencias transversales | 3 | PASS; no implementa F06 |
| Gobierno del Plan Maestro | 16 fases / 80 pasos | PASS documental |

La evidencia permanente se exporta en [evidence/F05-P03](evidence/F05-P03/summary.json):
JUnit por suite, logs documentales, aceptaciones/logs de las seis campañas, huellas
de fuentes y SHA256 de los archivos publicados. Los reportes normalizan únicamente
las rutas temporales a `$OUTPUT` y la raíz a `$REPO`; se conservan resultados,
recuentos y nombres. Las huellas de fuentes permiten comprobar que el código
nativo validado coincide con el del commit publicado aunque la evidencia se añada
en un commit posterior. El exportador rechaza resultados fallidos/omitidos.

Muestra real en `native.xml`, `f05.p03_scenario`: necesidad **26**, capitán **3**,
operador **5**, petición **29**, orden **30**, tarea **34**, intento **38**, resultado
**40**, evento terminal **41**. Core devolvió stream **984065 (`0xF0401`)**, valor
**99**, `performed=1`, `consumed_random=1`; los cuatro eventos P01 conservan su
cadena. `population` usa una dotación real de **130**, servicio **357**, operador
**47**, puesto **196** y orden **440**. No son resultados documentales inventados.

`determinism` compara bytes del futuro lógico con/sin representación auxiliar;
`process_save`/`process_load` terminan y recuperan en procesos separados;
`history_fault` verifica recuperación tras publicación incierta, con bloqueo hasta
recuperar disco; `revoked` impide la tirada después de revocar P02. La restauración
rechaza conocimiento no comunicado, causalidad rota y actor de decisión falsificado.
La campaña histórica de 730 días verifica **866.849 hechos originales**, **105
bloques** y recuperación en proceso nuevo; su auditoría confirma todos los hashes
de bloques originales. Las seis aceptaciones conservan `reference_contract_verified`
y `all_blocks_equal_complete_history`, sin cambiar las expectativas originales.

La CI [F05 nativa](https://github.com/robdor80/Videojuego_StarTrek/actions/workflows/f05-native-orders.yml)
ejecuta Core completo, P01/P02/P03/F04 y F02/F03 en **Linux y Windows**.
La CI [histórica F04](https://github.com/robdor80/Videojuego_StarTrek/actions/workflows/f04-history-persistence.yml)
conserva las seis campañas en Windows. Los resultados del SHA de entrega están
en Checks de la [PR Draft #84](https://github.com/robdor80/Videojuego_StarTrek/pull/84);
su descripción conserva enlaces a los runs exactos del HEAD final. Runs de otro
SHA no acreditan el HEAD final. Las pruebas nativas Linux/Windows no sustituyen
ninguna comprobación local MSI.

## MSI y límites

Tres automatizaciones UE están preparadas, **no ejecutadas en Cloud**:
`F05.P03.NPCInitiativeAndOrders`, `F05.P03.AuthorityAndKnowledge` y
`F05.P03.OffscreenPersistenceAndRecovery`. La última prueba real de UWorld/Actors
debe ejecutarse en el MSI; una representación nativa auxiliar no la acredita.
El script admite P01/P02/P03/All, nueve pruebas integrales y RHI real explícito.

[Registro centralizado actualizado](REGISTRO_VALIDACIONES_MSI.md), conservando
íntegramente las validaciones P01/P02 y añadiendo P03 **PENDIENTE**.
[Comandos y criterios MSI](VALIDACIONES_PENDIENTES_MSI_P03.md).

No se implementan contactos F06, averías/reparaciones, IA remota, diálogo, búsqueda
global de sustitutos, asignación de recursos ni scheduler de flota. La necesidad
es una obligación real comunicada para un servicio; no una emergencia inventada.
Propuestas e informes nunca equivalen a aprobación o ejecución del jugador.
La ABI requiere Host nativo de confianza y un solo hilo propietario.

No se modifican recursos artísticos, naves, modelos Blender, interiores, materiales,
texturas, copias de seguridad ni proyectos artísticos Unreal. El harness aislado
contiene solo fuentes de automatización. Los temporales son eliminables sin
dependencias del producto y no se incluyen en Git; no se borran laboratorios previos.
Ninguna PR se fusiona. La publicación de P03 termina en auditoría independiente.
