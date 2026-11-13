# H05 — Acta de auditoría independiente, fusión y continuidad

**Fecha:** 2026-11-13. **Auditor:** ChatGPT (arquitectura y control de alcance).  
**Repositorio:** `robdor80/Videojuego_StarTrek`. **Hito:** M0 — HOST nativo mínimo funcional.  
**Estado:** H05 IMPLEMENTADA, PROBADA en alcance nativo y FUSIONADA; **NO CERTIFICADA**. H13 mantiene la certificación transversal.

## 1. Procedencia y decisión

- [PR #139 — pasarela F05 y M0](https://github.com/robdor80/Videojuego_StarTrek/pull/139), entregada inicialmente Draft y revisada antes de fusionar.
- HEAD de Codex auditado: `43d2adb6d69509b3b222511010db6b1dc3cdd4b0`.
- Base auditada: `cf8fffe755ba04cf66ed09042858ec923d7b100b` (incluía el contrato y matriz H05 de ChatGPT, PR #138).
- Commit resultante de fusión squash de #139: **`3fb74093278f880e51f1fe37ddaae1e19c54ce7b`**; confirmado como HEAD de `main` inmediatamente después de fusionar.
- Pin autoritativo CoreRPG: **`76a7b7b485616d8c4994f384a90f123bf333591d`**, verificado por CMake/CI y producto cargado. No se cambia Core ni los pins históricos.

**Dictamen:** APTA PARA FUSIÓN dentro del alcance H05. Se ha fusionado tras confirmar integridad de las interfaces, composición real, pruebas y límites. Esta auditoría es una inspección independiente de código/diff y de evidencias en GitHub Actions; **no** es una ejecución adicional de CTest en la máquina del auditor.

## 2. Auditoría del código y fronteras

Se inspeccionaron los 15 archivos cambiados en la PR; los cambios quedan acotados a la composición nativa HOST, pruebas M0, CI y dos informes permanentes. No aparecen ediciones de CoreRPG, F11, Unreal, assets, oráculos congelados ni formatos de H04.

- `SessionOwner` continúa como único dueño de `F04Session*`, generación, vinculación H03, cola FIFO y transiciones H04. `Dispatch` entra en la variante de solicitudes existente, sin segundo dueño de WorldState.
- `gateway_bridge.cpp` reconsulta `f05_player_binding`, comprueba que corresponde al jugador unido y resuelve actor, referencias y observador dentro del hilo propietario; `OrderIntent` no acepta actor, issuer, scopes ni permisos autodeclarados. El dominio F05 valida la competencia del emisor, destinatario, estación, plazo y revisión.
- Las proyecciones `CampaignView`/`OrderView` son lecturas derivadas de F04/F05, sin cache persistente. Rechazos no entregan datos ni recibos. El `correlation_id` operativo permanece independiente de la clave de idempotencia F05.
- El flujo M0 usa `f05_submit`, `f05_receive`, `f05_execute_order` y las consultas F05 reales. La **recepción/ejecución por destinatario existe solo dentro del ejecutable de pruebas** a través de `GatewayTestAccess` compilado con `TREK_HOST_GATEWAY_TESTING`; no se publica API cliente para suplantación o ejecución arbitraria.
- El `SAVE/RESTORE` productivo utiliza H04; los bytes Core diagnósticos solo forman parte de la comprobación de igualdad, no de una recuperación alternativa.
- Las operaciones institucionales permanecen con `SERVICE_UNAVAILABLE` y sin `TrekF11TrialHost` o emisor F11. `F04_SCAN` sigue siendo una operación F05 de prueba con resultado RNG, **no** detección de contactos ni sensores F06.
- Se revisaron los escenarios de pruebas de cierre/LOAD, revisión, scope, ausencia de vínculo, observador, idempotencia, denegación, orden pendiente y dos procesos separados.

## 3. Evidencia contrastada en GitHub

La repetición final sobre **HEAD completo `43d2adb6`** fue [HOST native H02–H05, run 43468890126](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43468890126): cinco jobs con conclusión `success`. Se comprobaron los registros de ejecución (no solo el cuerpo de la PR):

| Job | Comprobación directa |
|---|---|
| Ubuntu/GCC nativo | **236/236 CTest PASS**, 0 FAIL |
| Windows/MSVC nativo | **236/236 CTest PASS**, 0 FAIL |
| Linux/Clang con ASan/UBSan | **81/81 CTest PASS**, 0 FAIL |
| Linux Release, `TREK_HOST_TESTS=OFF` | Biblioteca cargada; exports, dependencias, pin y ausencia de hooks/F11 trial: PASS |
| Windows Release, `TREK_HOST_TESTS=OFF` | Biblioteca cargada; exports, dependencias, pin y ausencia de hooks/F11 trial: PASS |
| F11 aislada, H01 documental | Ejecutadas en ambos jobs nativos con `success`; no forman parte del grafo de producto HOST |

Los cinco artefactos del run final están publicados y no constaban expirados durante esta revisión. Los detalles por escenario `HM-01..HM-28`, ejemplos, SHA, resultados de plataforma, comandos y mediciones permanecen en [H05_RESULTADOS_M0_2026-11-13.md](H05_RESULTADOS_M0_2026-11-13.md). Se comprobó la correspondencia de los casos `host.m0.*` y los scripts de proceso en el diff.

Las incidencias previas están en los informes de Codex: primer fallo de enlace MSVC en la prueba M0, adaptación de oráculos a las semánticas reales F04/F05 y uso involuntario de un destino temporal no nuevo en una repetición F05. Se conservó el historial de CI; el código final volvió a pasar en Windows/Linux. No se relajaron las pruebas históricas.

## 4. Matices, mediciones y deuda técnica

1. Las denegaciones F05 por revisión obsoleta, falta de competencia o operación no admitida pueden producir un hecho `REFUSED` auditado dentro de Core. No ejecutan el `F04_SCAN` ni consumen RNG; no deben interpretarse como rechazo necesariamente idéntico en bytes a un estado previo. La comparación byte a byte se exige para los errores cuyo contrato sí es atómico (p. ej. scope estructural o clave conflictiva).
2. El resultado `F04_SCAN` modifica su stream RNG cuando corresponde, aunque la propia tirada no incremente la revisión WorldState. La revisión de auditoría posterior puede variar. Se comparan revisiones y streams reales, no una suposición del HOST.
3. El producto no ofrece aún operación interactiva general de recepción/ejecución de órdenes para NPC; corresponderá a coordinación H08/H09, conservando fronteras de identidad y reglas F05.
4. Los ensayos entre procesos cubren orden completada y orden pendiente, SAVE/RESTORE e idempotencia. No cubren un juego Unreal en el MSI, D3D12/NullRHI, sensores F06 ni corte de alimentación física. Esas verificaciones están **NOT_RUN** en H05.
5. Medición inicial documentada: 96 289 bytes en la generación nueva; 98 619 bytes con orden ejecutada; tras guardar de nuevo sin cambios se repiten 2 objetos (98 345 bytes) por hash. Es un fixture de 130 PERSON, **no** una estimación de campañas narrativas completas. La reutilización por contenido, deduplicación y retención se evaluarán en **H12-P04** sobre tamaños medidos. No se han borrado versiones.
6. H05 no autoriza a H06 a asumir ya identificado un `.uproject` principal definitivo ni a tratar fixtures sintéticos como cadetes reales de Academia.

## 5. Cierre y siguiente fase

| Elemento | Estado validado |
|---|---|
| H05-P01 composición nativa | IMPLEMENTADA / PROBADA |
| H05-P02 pasarela F05 | IMPLEMENTADA / PROBADA (emisor/consultas de producto; receptor en fixture) |
| H05-P03 proyecciones nativas | IMPLEMENTADA / PROBADA |
| H05-P04 ciclo end-to-end | PROBADO nativo en procesos separados |
| PR #139 / producto H05 | **FUSIONADA** |
| Hito M0 del HOST | **ALCANZADO Y PROBADO en alcance nativo** |
| Certificación integral H13 | PENDIENTE / NO CERTIFICADA |

**Siguiente etapa: H06 — Integración real de HOST en Unreal Engine 5.** Antes de programar, verificar cuál es el `.uproject` definitivo y diseñar la conexión con `UGameInstance`, `UWorld` y callbacks sin duplicar Core ni introducir un segundo propietario de sesión. H07/F11 institucional permanece separado, conforme al Plan Maestro y a F11-P05-A02-03 del proyecto principal.

**No se hizo ninguna modificación de producto en esta acta documental.** La lectura de los informes originales de Codex debe considerarse contemporánea a su entrega: sus rótulos «NO FUSIONADO» eran correctos antes de fusionar; este documento registra el estado posterior sin reescribir evidencia histórica.
