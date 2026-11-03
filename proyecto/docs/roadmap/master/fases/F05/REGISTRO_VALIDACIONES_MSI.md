# F05 — Registro centralizado de validaciones pendientes (MSI)

Fecha de conciliación: **2026-11-02**. Responsable de seguimiento: auditoría técnica ChatGPT; ejecución local por el propietario/Codex local. **Este documento no certifica resultados que no se han ejecutado.**

## Regla de salida

**F06 NO puede iniciarse y F05 no puede declararse cerrada / CORE_INTEGRADO** hasta disponer de evidencia satisfactoria de todas las pruebas F05 obligatorias, incluidas las del MSI y el cierre final de P05. Se permite avanzar de una subfase F05 a la siguiente, manteniendo visible la deuda de pruebas.

## Estado del desarrollo

| Subfase | Desarrollo | Cloud/nativo | Pruebas MSI |
|---|---|---|---|
| F05-P01 — Órdenes | PR #81 fusionada | Auditadas, CI Linux/Windows verde | **PENDIENTES** |
| F05-P02 — Delegación | PR #82 fusionada | Auditadas, CI Linux/Windows verde | **PENDIENTES** |
| F05-P03 — Iniciativa NPC | Implementada nativamente; entrega Draft para auditoría independiente | Evidencia en [informe P03](F05-P03_IMPLEMENTACION.md) | **PENDIENTES** |
| F05-P04 — IA | No implementada | No realizadas | Por definir |
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

## Criterios de aceptación y registro de resultados

Los pasos comunes de compilación/carga pueden acreditarse con **una sola ejecución integral** si los reportes demuestran explícitamente la compatibilidad de P01, P02 y P03. Se mantienen las **seis pruebas P01/P02** obligatorias y se añaden **tres P03**: deben pasar las **nueve pruebas de automatización UE**; ausencia de pruebas, tests omitidos o falta de logs no equivale a PASS.

Guardar en un commit posterior, sin alterar registros históricos: fecha/hora, equipo, versión UE exacta, compilador, SHA Star Trek y Core, comandos ejecutados, `index.json` de Automation, XML/logs relevantes, número de pruebas y resultado por test. La ejecución local no queda acreditada por la CI Windows de GitHub.

Tras P04, añadir aquí sus nuevas pruebas sin borrar ni marcar automáticamente las anteriores. Antes de comenzar F06, realizar la auditoría integral P05 sobre el HEAD definitivo, comprobar regresiones y dejar acta explícita de cierre. P03 no autoriza comenzar P04/P05 ni F06.

**Prohibido limpiar, borrar o reutilizar laboratorios previos sin autorización.** Directorios nuevos bajo `laboratorios/f05/` excluidos de Git; preservar fuentes y recursos artísticos.
