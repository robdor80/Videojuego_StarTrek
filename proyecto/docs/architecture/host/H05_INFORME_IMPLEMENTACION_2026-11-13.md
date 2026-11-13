# H05 — Implementación de la pasarela nativa y M0

Fecha: 2026-11-13. Rama: `feature/host-h05-pasarela-m0`. Base `main`:
`cf8fffe755ba04cf66ed09042858ec923d7b100b` (incluye PR #138).
Código inicial: `5ee7b169e87ab24aa141cd3c4f81c3bec6c37803`.
Refuerzo RESOLVING: `0f753ad16bbea18dfbc58f57e56ef53146ed002b`.
Código final, incluido enlace MSVC: `0b022b1188b0a3490441af0769fffcefdc6f8ce0`.
[PR #139 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/139), sin fusionar.
CoreRPG: `76a7b7b485616d8c4994f384a90f123bf333591d`, checkout limpio,
comprobado por CMake y por el binario cargado. Ningún pin histórico cambia.

Estado de entrega: **IMPLEMENTADO; M0 PROBADO en el alcance nativo;
NO CERTIFICADO; NO FUSIONADO**. La evidencia final,
comandos y ejecuciones están en [resultados M0](H05_RESULTADOS_M0_2026-11-13.md).
La PR permanece Draft para auditoría independiente.

[CI final de código, run 43467528745](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43467528745):
cinco jobs success. GCC 15.2: **236/236**; MSVC 19.51.36260.0: **236/236**;
Clang 21.1.8 ASan/UBSan: **81/81**. Producto Release OFF: carga/exports/pin
**PASS Linux y Windows**. F11 aislada: **17/17 por SO**; H01: **11/11 por SO**.
HM-01–HM-28 tienen resultado PASS en su alcance nativo, desglosado con los
oráculos reales y las excepciones de semántica en el informe de resultados.
El último commit de publicación solo actualiza estos dos informes; el SHA
de código ensayado es `0b022b1188b0a3490441af0769fffcefdc6f8ce0`.

## Arquitectura y tipos reales

`SessionOwner` conserva su único `NativeSession`, `F04Session*` activo, FIFO de
32 solicitudes y trabajador propietario. `Dispatch` se añade a la variante de
solicitudes existente. No hay coordinador, mundo, historial, reloj, RNG, caché
autoritativa ni serializador de partida nuevos. SAVE/RESTORE siguen siendo H04.

La interfaz interna C++ añade `query_view`, `submit_order`, `query_order`,
`cancel_order` e `institutional_command`. Retornan `future<OperationResult>`;
`correlation_id` es un entero de transporte que se conserva también en errores y
revocaciones. No modifica `OrderIntent.key`, clave de campaña de F05.

Las proyecciones nativas de semántica v1 son `CampaignView` (generación, revisión,
tick, persona vinculada y nave), `OrderView` (datos de solicitud y recibo,
ejecución opcional), `OrderReceipt` y `ExecutionResult`. Se copian campos de los
tipos reales **`F04Stats`, `F04Person`, `F05PlayerBinding`, `F05Receipt`,
`F05OrderView` y `F05ResultView`**. Los estados y códigos permanecen en el
vocabulario F04/F05. No se mantiene una copia entre llamadas. Los eventos se
consultan mediante `f05_events_page` solo en el oráculo nativo; no se incorpora
un bus de eventos H08 ni una API de conocimiento NPC.

`OrderIntent` contiene destinatario y estación como IDs locales de campaña,
key, revisión esperada, plazo, causa y operación F04. No contiene actor, issuer,
scope, nave elegida ni permisos. Cada despacho revalida generación y BOUND en el
trabajador; consulta el vínculo persistente mediante `f05_player_binding`,
contrasta el F04Ref operativo y consulta PERSON desde ese observador. Las
referencias de emisor/nave/scopes se construyen en ese mismo hilo. F05 valida
destinatario, estación, competencia, plazos y revisión. Los IDs copiados de una
vista nunca son acreditaciones para otra llamada.

`query_order` usa ese mismo observador en `f05_order` y, únicamente cuando el
recibo declara un resultado, `f05_result`. Una denegación normalizada no devuelve
generación, vista ni recibo; el código original queda en el diagnóstico nativo
privado `F04/F05 code`. Un código desconocido se normaliza como DOMAIN_REJECTED,
sin producir éxito ni contenido. Los pendientes/cancelados/refusados sin resultado
no inventan una ejecución.

Las llamadas Core se hacen con el mutex de admisión liberado. Cierre/LOAD
invalidan solicitudes pendientes; un resultado de generación revocada se
descarta aunque Core haya confirmado antes del cierre. No se promete rollback de
ese commit. SAVE admitido detrás de un despacho espera a que termine; una respuesta
de orden aceptada no confirma durabilidad. Solo el resultado H04 de SAVE lo hace.

## Diferencias justificadas frente al contrato propuesto

1. **F05 conserva denegaciones auditadas.** `f05_submit` registra ISSUED y
   REFUSED para una revisión caducada, falta de competencia u operación no
   soportada. No son rechazos atómicos sin hechos. Se conservan esos resultados
   reales y se comprueban ausencia de task/attempt/result, RNG y reloj idénticos,
   y replay sin nuevos hechos. Scope estructural inválido y conflicto de key sí
   conservan todos los bytes. HOST no copia reglas para evitar esa auditoría.
2. **Idempotencia precede a revisión en F05.** Misma key y payload original
   devuelve la misma orden incluso tras LOAD con la revisión original. Cambiar
   causa, revisión u otro dato del payload con la misma key produce conflicto.
   HOST no refresca ni reejecuta una intención stale automáticamente.
3. **Tirada Core y revisión.** `StreamRollAction` consume RNG sin aumentar la
   revisión WorldState por sí misma: `core_revision_before == core_revision_after`.
   La auditoría posterior F05 sí aumenta la revisión de campaña. El ensayo
   comprueba ambas cosas, el resultado aceptado y el cambio del stream persistido.
4. **Receptor cerrado en producto.** No se añaden receive/execute públicos a
   `SessionOwner`: necesitan la coordinación H08/H09. El ejecutable separado
   `host_m0_tests` compila las mismas fuentes con `TREK_HOST_GATEWAY_TESTING` y
   usa `GatewayTestAccess` únicamente en su trabajador para simular la llamada
   legítima del destinatario. `f05_receive` y `f05_execute_order` reales distinguen
   emisor y receptor. Los tests rechazan al capitán intentando recibir/ejecutar
   la orden destinada a otro PERSON. No hay setter NPC ni actor libre en TrekHost.
5. **F11** retorna SERVICE_UNAVAILABLE, sin mutación ni dependencia trial. No se
   incorpora lectura institucional, emisor, rangos, ascensos ni UE.

No se añadió F04_COMMAND genérico: M0 siempre atraviesa F05. Las únicas operaciones
F04 de preparación son infraestructura del fixture de pruebas, no una API de juego.

## Inventario de archivos

| Archivo | Cambio |
|---|---|
| `desarrollo/integration/host/include/trek/host/session_owner.h` | Intenciones, proyecciones, resultados y métodos internos; SERVICE_UNAVAILABLE aditivo. |
| `desarrollo/integration/host/src/session_owner.cpp` | Admisión/revalidación, FIFO, revocación y correlación del despacho; visitante solo en build de ensayo. |
| `desarrollo/integration/host/src/native_session.h` | Entrada privada de despacho; acceso al Core solo para el ensayo separado. |
| `desarrollo/integration/host/src/native_session.cpp` | Normalización existente F04/F05 y fallo cerrado institucional; hook de ensayo compilado condicionalmente. |
| `desarrollo/integration/host/src/gateway.h` | Solicitud privada tipada por operación. |
| `desarrollo/integration/host/src/gateway_bridge.cpp` | Revalidación del binding, consultas y delegación a F05. |
| `desarrollo/integration/host/tests/gateway_test_access.h` | Infraestructura exclusiva del ejecutable M0, inaccesible sin su macro. |
| `desarrollo/integration/host/tests/gateway_fault_bridge.cpp` | Stub adicional para enlazar el ejecutable histórico de fallos; sus oráculos no cambian. |
| `desarrollo/integration/host/tests/m0_tests.cpp` | Fixture poblado real, escenarios M0, concurrencia, escritor y lector. |
| `desarrollo/integration/host/tests/m0_process.py` | Procesos separados, PIDs y mediciones por contenido SHA256. |
| `desarrollo/integration/host/tests/inspect_product.py` | Carga Release OFF, exports, dependencias y pin Linux/Windows. |
| `desarrollo/integration/host/CMakeLists.txt` | Composición aditiva y 26 pruebas M0 separadas del DLL productivo. |
| `.github/workflows/host-h02-native.yml` | Suite H02–H05; pruebas y artefactos M0; inspección de producto en ambos SO. |
| Este informe y `H05_RESULTADOS_M0_2026-11-13.md` | Evidencia permanente aprobada expresamente por el encargo. |

No se modifican fuentes Core, fuentes/oráculos históricos F04/F05/F11, pins,
formatos de guardado, assets, proyectos UE ni laboratorios anteriores.

## Mediciones, límites y riesgos

El fixture usa 130 PERSON de dotación, plantilla Sutherland explícita, turno Alpha
y tick Core 28800; el capitán de ensayo vinculado es PERSON 3. No representa al
cadete definitivo ni a un escenario narrativo/productivo completo. La operación
es F04_SCAN: tirada 1..100, sin detección de contactos F06.

La primera medición Linux obtuvo 96 289 bytes de sobre/snapshot nuevo (2 objetos
Core), 98 619 bytes tras completar una orden (2 objetos), y otros 98 619 bytes
al guardar sin jugar: ambos objetos, 98 345 bytes, se repiten por SHA256. Tras
RESTORE y otra publicación se conservan 3 objetos/98 967 bytes. La rama pendiente
ocupa 97 029 bytes y, tras recuperarla y ejecutarla, 195 374 bytes/4 objetos porque
conserva los objetos históricos previos. Ver la tabla reproducida en resultados.

Los límites H04 de 64 MiB/objeto, 512 MiB/historial y 4096 entradas no cambian.
Máximo objeto observado: 97 997 bytes; máximo historial observado: 195 100
bytes de objetos, muy por debajo de 512 MiB; como máximo 8 archivos en la versión
medida frente a 4096 entradas admitidas. No se extrapola ese margen al juego final.
No aparece un hallazgo crítico en este dataset. H12-P04 debe valorar almacén de
objetos por contenido y retención explícita, conservando publicación durable,
validación y procedencia. No se implementa deduplicación ni se elimina generación
alguna. Las mediciones pequeñas no estiman campañas de años ni desgaste de disco.

Los builds conservan las flags históricas de F04, incluido F04_HISTORY_TESTING;
H05 no añade hooks HOST al producto. El puente ABI C nativo sigue siendo una capa
de confianza interna: no es una frontera contra código arbitrario del mismo
usuario. Los consumidores UI/IA deben usar SessionOwner, no la ABI privilegiada.

Los resultados brutos están en `laboratorios/host/h05/`, ignorados por Git.
La raíz Windows literal de AGENTS corresponde al equipo del usuario; este trabajo
se ejecuta en su checkout conectado `/workspace/Videojuego_StarTrek`, sin un árbol
paralelo de producto. El laboratorio es prescindible y eliminable completo una
vez terminadas las ejecuciones; no hay dependencia productiva de sus archivos.
No se borra durante esta entrega. MSI/UE y cortes eléctricos físicos: NOT_RUN.

La certificación integral sigue en H13 y la auditoría/fusión corresponde al
usuario y ChatGPT. H05 no queda CERTIFICADA ni FUSIONADA por esta entrega.
