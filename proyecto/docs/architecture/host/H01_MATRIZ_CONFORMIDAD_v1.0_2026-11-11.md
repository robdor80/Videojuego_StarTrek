# H01 — Matriz de pruebas de conformidad v1.0

Todos los casos son **DISEÑADOS y NO EJECUTADOS contra HOST**. Las pruebas estáticas del registro solo verificarán coherencia de esta especificación, no runtime Core/UE.

| ID | Escenario | Resultado obligatorio | Responsable |
|---|---|---|---|
| HC-01 | OPEN en CLOSED | Una F04Session, ACTIVE | H02 |
| HC-02 | Fallo parcial al abrir | Sin recursos zombie | H02 |
| HC-03 | Doble OPEN simultáneo | BUSY_STATE y una sesión | H02 |
| HC-04 | Doble CLOSE/callback tardío | Sin use-after-free | H02 |
| HC-05 | Llamada Core fuera de hilo | WRONG_THREAD o cola | H02 |
| HC-06 | SAVE durante LOAD | BUSY_STATE, no overwrite | H02/H04 |
| HC-07 | F04Ref de otro scope | SCOPE_INVALID, salida vacía | H03/H05 |
| HC-08 | UI/IA forja actor/permiso | Denegar, resolver internamente | H03/H05 |
| HC-09 | F04 expected_revision vieja | REVISION_STALE sin reintento | H05 |
| HC-10 | F05 expected_revision vieja | Rechazo sin otra key | H05 |
| HC-11 | Reenvío F05 misma key/payload | Recibo previo sin ejecución doble | H05 |
| HC-12 | F05 misma key/payload distinto | IDEMPOTENCY_CONFLICT | H05 |
| HC-13 | Orden recibida no ejecutada | No presentar scan ejecutado | H05 |
| HC-14 | Timeout de ejecución | Consultar recibo, no reintentar | H05 |
| HC-15 | LOAD válido desde ACTIVE | Nuevo scope y generación | H04 |
| HC-16 | LOAD truncado/incompatible | Mantener estado/archivo bueno | H04 |
| HC-17 | Corte de escritura | Última generación recuperable | H04 |
| HC-18 | Historia migrada/export_active | No sustituye history_open | H04 |
| HC-19 | Save importado aparentemente válido | IMPORTED_UNVERIFIED sin autoridad | H04/H07 |
| HC-20 | NPC intenta leer facts ocultos | Vista filtrada sin diagnóstico | H05/H07 |
| HC-21 | IA propone orden no válida | Ninguna mutación en ai_finish | H05/H10 |
| HC-22 | Respuesta IA tras restore | GENERATION_EXPIRED, descartada | H02/H10 |
| HC-23 | Lector F11, sujeto ajeno | ACCESS_DENIED, buffer vacío | H07 |
| HC-24 | Emisión F11 sin servicio producto | SERVICE_UNAVAILABLE, cero cambios | H07 |
| HC-25 | CAUSE=110501 o F04Ref como permiso | Nunca acredita competencia | F11/H07 |
| HC-26 | F11 niega emisión | Sin rango/evento inventado | F11/H07 |
| HC-27 | Repetición de aviso | Sin segundo hecho Core | H08 |
| HC-28 | Recuperación de avisos | Visibilidad por observador | H08 |
| HC-29 | monotonic_ms y Core tick | No mezclar relojes | H05/H10 |
| HC-30 | Intentar enlazar TrialHost | Gate de build falla | H05/H07 |
| HC-31 | Falta .uproject | No declarar UE5_JUGABLE | H06 |
| HC-32 | Pin/flags no autorizados | Gate de compatibilidad falla | H05 |
| HC-33 | Repetir presentación ascenso | No duplicar F11 | H07/H11 |
| HC-34 | Salida F11 precargada y denegada | Vaciar salida | H07 |
| HC-35 | Restore con vínculo inconsistente | PRINCIPAL_UNBOUND | H03/H04 |

## Evidencias exigidas al ejecutar

Para cada test: Star Trek HEAD, Core SHA, flags, sistema operativo, toolchain, fichero/función, escenario, revisión antes/después, resultado PASS/FAIL/SKIP, logs ubicados dentro de laboratorios/host/<fase>/<tarea>/. No alterar suites históricas ni incluir logs temporales en Git. Pruebas F11-P05-A02-03 de la PR #110 pertenecen a F11 (33 casos preparatorios); HC-23..HC-26 no las duplican ni las certifican.

## Criterios de cierre documental H01

Arquitectura coherente con el código, contratos versionados y errores normalizados, seguridad offline y procedencia explícitas, matriz de Core sin cambiar pins, matriz de escenarios y validador estático con CI. Solo una ejecución real de H02-H07 permitirá marcar las comprobaciones runtime como PROBADAS. H01 nunca acredita un emisor institucional ni proyecto Unreal.
