# F05 — Registro centralizado de validaciones pendientes (MSI)

Fecha de conciliación: **2026-11-03**. Responsable de seguimiento: auditoría técnica ChatGPT; ejecución local por el propietario/Codex local. **Este documento no certifica resultados que no se han ejecutado.**

## Regla de salida

**F06 NO puede iniciarse y F05 no puede declararse cerrada / CORE_INTEGRADO** hasta disponer de evidencia satisfactoria de todas las pruebas F05 obligatorias, incluidas las del MSI y el cierre final de P05. Se permite avanzar de una subfase F05 a la siguiente, manteniendo visible la deuda de pruebas.

## Estado del desarrollo

| Subfase | Desarrollo | Cloud/nativo | Pruebas MSI |
|---|---|---|---|
| F05-P01 — Órdenes | PR #81 fusionada | Auditadas, CI Linux/Windows verde | **PENDIENTES** |
| F05-P02 — Delegación | PR #82 fusionada | Auditadas, CI Linux/Windows verde | **PENDIENTES** |
| F05-P03 — Iniciativa NPC | PR #84 fusionada | Evidencia en [informe P03](F05-P03_IMPLEMENTACION.md) | **PENDIENTES** |
| F05-P04 — IA opcional | PR #85 fusionada; autonomía P03 independiente de IA | Nativa auditada; véase [informe P04](F05-P04_IMPLEMENTACION.md) | **PENDIENTES** |
| F05-P05 — Cierre global | Solo suite documental histórica de referencia | No certifica F05 completa | Auditoría integral futura |

## P01: verificaciones obligatorias aún pendientes

- [ ] **P01-01.** Compilar nativamente con MSVC en el MSI y comprobar carga real de DLL, ABI y SHA Core fijado.
- [ ] **P01-02.** Compilar con UBT/UHT y cargar el módulo aislado en **UE 5.8.2** del MSI (ready=1, sin errores de DLL).
- [ ] **P01-03.** Automatización UE5 `F05.P01.LifecycleAndRecovery`: ciclo de orden, resultado real, guardado/restauración, replay idempotente.
- [ ] **P01-04.** Automatización UE5 `F05.P01.Negatives`: autoridad, cualificación y operaciones no permitidas, sin efectos ficticios.
- [ ] **P01-05.** Automatización UE5 `F05.P01.WorldAndActorIndependence`: destruir actor/UWorld no altera la campaña, ejecución fuera de escena.
- [ ] **P01-06.** Repetir las tres pruebas P01 en un **directorio limpio nuevo**, conservando logs, resultados y versión real de motor.

Fuente reproducible: [VALIDACIONES_PENDIENTES_MSI.md](VALIDACIONES_PENDIENTES_MSI.md).

## P02: verificaciones adicionales aún pendientes

- [ ] **P02-01.** Compilación MSVC de la ABI de delegaciones, exports `f05_delegate` y dependencias DLL, en el MSI.
- [ ] **P02-02.** Compilación/carga del harness UBT/UHT de UE 5.8.2, con SHA y DLL P02 correctos.
- [ ] **P02-03.** Automatización UE5 `F05.P02.DelegationRevocationRecovery`: revocación antes del efecto, recuperación y replay.
- [ ] **P02-04.** Automatización UE5 `F05.P02.ModesAndLimits`: aprobación efectiva, propuesta sin efecto, subdelegación denegada.
- [ ] **P02-05.** Automatización UE5 `F05.P02.ExpiryAndChainOfCommand`: caducidad, revocación de nombramiento y límites de sucesión.
- [ ] **P02-06.** Ejecutar las **seis pruebas automatizadas P01+P02** juntas y repetirlas en un **directorio limpio nuevo**, sin reutilizar DLL ni datos previos.
- [ ] **P02-07.** Carga del módulo con el **RHI real** del MSI; registrar problemas de carga. NullRHI no acredita gráficos ni interfaz jugable.

Fuente reproducible: [VALIDACIONES_PENDIENTES_MSI_P02.md](VALIDACIONES_PENDIENTES_MSI_P02.md).

## P03: verificaciones adicionales pendientes

- [ ] **P03-01. PENDIENTE.** Compilar con MSVC en el MSI; verificar ABI y exports `f05_bind_player`, `f05_scan_need`, `f05_brief_need`, `f05_evaluate` y `f05_decisions_page`, DLL y SHA Core fijado.
- [ ] **P03-02. PENDIENTE.** Compilar/cargar el harness aislado con UBT/UHT de **UE 5.8.2**, `ready=1`, sin símbolos faltantes ni DLL antiguas.
- [ ] **P03-03. PENDIENTE.** Automatización UE `F05.P03.NPCInitiativeAndOrders`: necesidad de servicio real, decisión NPC, petición/orden/tarea/intento/resultado P01 y consecuencia Core.
- [ ] **P03-04. PENDIENTE.** Automatización UE `F05.P03.AuthorityAndKnowledge`: información limitada, propuesta sin atribuciones y jugador ausente sin consentimiento supuesto.
- [ ] **P03-05. PENDIENTE.** Automatización UE `F05.P03.OffscreenPersistenceAndRecovery`: UWorld y Actor prescindibles, equivalencia de campaña, guardado/restauración y replay sin duplicados.
- [ ] **P03-06. PENDIENTE.** Ejecutar las **nueve pruebas P01+P02+P03**, conservar reportes y repetirlas en un **directorio nuevo y limpio** sin reutilizar DLL/datos.
- [ ] **P03-07. PENDIENTE.** Repetir carga y automatización con **RHI real** del MSI; NullRHI no acredita este punto ni gráficos jugables.

Comandos, rutas, prerrequisitos, criterios y resultados esperados:
[VALIDACIONES_PENDIENTES_MSI_P03.md](VALIDACIONES_PENDIENTES_MSI_P03.md).
Ningún test Unreal P03 ha sido ejecutado en Cloud. Se conservan todas las
validaciones P01 y P02 anteriores, sin marcar ninguna como superada.

## P04: verificaciones adicionales pendientes

- [ ] **P04-01. PENDIENTE.** MSVC/DLL, ABI y exports IA, SHA Core y dependencias reales en MSI.
- [ ] **P04-02. PENDIENTE.** UBT/UHT y carga del módulo aislado en UE **5.8.2**, `ready=1`.
- [ ] **P04-03. PENDIENTE.** `F05.P04.AIProposalValidation`.
- [ ] **P04-04. PENDIENTE.** `F05.P04.StaleAuthorityAndFallback`.
- [ ] **P04-05. PENDIENTE.** `F05.P04.OffscreenRecoveryAndSafety`.
- [ ] **P04-06. PENDIENTE.** Las **12 pruebas P01/P02/P03/P04**, incluidas las nueve anteriores intactas, y repetición en directorio nuevo/limpio.
- [ ] **P04-07. PENDIENTE.** RHI real, recuperación de partida y fallback con proveedor simulado sin conexión remota.

Comandos y criterios: [VALIDACIONES_PENDIENTES_MSI_P04.md](VALIDACIONES_PENDIENTES_MSI_P04.md).
No se ha ejecutado ninguna prueba Unreal P04 en Cloud. Ningún pendiente previo
queda acreditado por esta ampliación. P03 figura fusionada en PR #84; sus pruebas
MSI siguen pendientes.

## Criterios de aceptación y registro de resultados

Los pasos comunes de compilación/carga pueden acreditarse con **una sola ejecución integral** si los reportes demuestran explícitamente la compatibilidad de P01, P02, P03 y P04. Se mantienen las **seis pruebas P01/P02** obligatorias y se añaden **tres P03**: se añaden tres P04 y deben pasar las **12 pruebas de automatización UE**; ausencia de pruebas, tests omitidos o falta de logs no equivale a PASS.

Guardar en un commit posterior, sin alterar registros históricos: fecha/hora, equipo, versión UE exacta, compilador, SHA Star Trek y Core, comandos ejecutados, `index.json` de Automation, XML/logs relevantes, número de pruebas y resultado por test. La ejecución local no queda acreditada por la CI Windows de GitHub.

Las nuevas pruebas P04 se añaden sin borrar ni marcar automáticamente las anteriores. Antes de comenzar F06, realizar la auditoría integral P05 sobre el HEAD definitivo, comprobar regresiones y dejar acta explícita de cierre. La fusión P04 no certifica pruebas UE ni autoriza cerrar F05 o comenzar F06; la auditoría integral P05 sigue pendiente.

**Prohibido limpiar, borrar o reutilizar laboratorios previos sin autorización.** Directorios nuevos bajo `laboratorios/f05/` excluidos de Git; preservar fuentes y recursos artísticos.

## P05A Cloud / P05B MSI — auditoría integral, 03-11-2026

P05A **LISTA PARA VALIDACIÓN MSI** en alcance Cloud, entrega Draft [#87](https://github.com/robdor80/Videojuego_StarTrek/pull/87) para auditoría independiente y comprobación de CI del HEAD final. Las dos incidencias
reproducidas P05A-01 (cancelación por sucesor que era emisor delegado) y P05A-02
(plazo P04 manipulado >300 en restauración) están corregidas y sus regresiones
pasan. Evidencia local ejecutada: F04/F05 **395/395** (30 P05A), Core **483/483**, F02 **15/15**, F03 **25/25**, F04 original **259/259**, campañas **6/6** con pins/oráculos congelados; documentación **22 tests +48 fixtures +3 transversales** y gobierno PASS. Ocho repeticiones con red bloqueada PASS. CI final Linux/Windows y sus artefactos se publican en PR #87; no contar un SKIP condicional POSIX Core/Windows como PASS. Ver [auditoría y matriz](F05-P05A_AUDITORIA_INTEGRAL.md).
No hay ejecución MSI ni Unreal en Cloud, ni validaciones anteriores canceladas.

Pendientes adicionales agrupados, sin duplicar P01–P04:

- [ ] **P05B-01. PENDIENTE.** Repetir íntegramente los 30 casos nuevos P05A y la selección nativa F04/F05, Core completo, recuperación entre procesos e historia, con MSVC real en MSI. Incluye cancelación del sucesor y rechazo de plazo manipulado; no basta CI Windows.
- [ ] **P05B-02. PENDIENTE.** Acreditar tiempo autoritativo y ausencia de progreso offline con `p05a_J_time` y recuperación; el Host pausa dejando de avanzar Core. Sin daemon ni reloj real de simulación.
- [ ] **P05B-03. PENDIENTE.** Aplicar el procedimiento integral P05B, dos laboratorios limpios nuevos, verificación real de DLL/exports/SHA, las 12 pruebas UE exactas y RHI hardware. Reutiliza/acumula P01-01…P04-07; una evidencia integral puede acreditar requisitos equivalentes, conservando cada resultado.
- [ ] **P05B-04. PENDIENTE.** Revisar reportes, advertencias y hashes, publicar evidencia permanente y acta de aceptación posterior; no convertir PASS automatizado en cierre de fase.

[Procedimiento PowerShell, comandos, logs y diagnóstico](P05B_PLAN_CERTIFICACION_MSI.md).
P05A no cierra F05 ni desbloquea F06. `P05=CERRADA` en la referencia documental
histórica es independiente de P05A/P05B. Bloquean el cierre los fallos graves,
CI final incompleta, cualquier pendiente MSI obligatorio y la falta de acta P05B.

### Conciliación de recuperación Cloud — 03-11-2026

Comprobado en GitHub sobre `c3ede747225cc009da54a5d2c4732f4760c63c2e`:
[CI integral 41715049830](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41715049830)
SUCCESS, **10/10 jobs**, intento 1. Linux y Windows: F04/F05 **395/395**, F02
**15/15**, F03 **25/25**, F04 original **259/259**, campañas **6/6 por sistema**.
Core Linux **483 PASS**; Core Windows **482 PASS + 1 SKIP** exclusivamente de
`ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt`.
Referencia F05, gobierno y referencia F15 SUCCESS en ese mismo commit.
No quedan campañas pendientes de ese HEAD; las del último commit documental,
si las activa Actions, se identifican por separado en PR #87.

La conciliación contrasta metadatos/logs CI y hashes/JUnit/aceptaciones locales
publicados. Conserva enlaces, hashes y el límite de acceso a ZIP CI en la
[evidencia de recuperación](evidence/F05-P05A-CI-RECUPERACION/summary.json).
No añade ejecución MSI, no acredita ACL Windows ni Unreal, y no marca ninguna
casilla P01–P04/P05B como superada. Plan P05B revisado: dos builds limpios, DLL
real, 12 nombres UE exactos y RHI hardware; **PENDIENTE / NO EJECUTADO**.
No hay cambios nuevos de producto, Core, arte o laboratorios anteriores.
