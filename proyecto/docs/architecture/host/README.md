# Proyecto HOST — Índice técnico

> **Estado actualizado a 27-11-2026:** H08-P01…P04 están **fusionadas** (PR #207–#210). **H07-P01…P05 se han IMPLEMENTADO, PROBADO técnicamente y FUSIONADO** en `main` mediante PR [#203](https://github.com/robdor80/Videojuego_StarTrek/pull/203), [#204](https://github.com/robdor80/Videojuego_StarTrek/pull/204) y [#205](https://github.com/robdor80/Videojuego_StarTrek/pull/205), culminando en el commit `5125d8ace7df655f8a44452d001ab745b37c42fc`. [Acta de cierre técnico y auditoría](H07_AUDITORIA_RECONCILIACION_2026-11-27.md). **No certificada presencialmente:** faltan la aceptación visual/control de Unreal y la verificación humana de la corrección DPI de H06 (cliente técnico 2538×1472 al 150 %). El emisor F11 de producto sigue `SERVICE_UNAVAILABLE`; no se considera dentro de esta certificación. Los párrafos posteriores conservan estados históricos en su fecha y no sustituyen el presente aviso.

> **Cierre H09-P01 (27-11-2026):** contrato e inventario de consolas **PROBADOS ESTÁTICAMENTE Y FUSIONADOS** mediante [PR #211](https://github.com/robdor80/Videojuego_StarTrek/pull/211), SHA de integración `dd9b51678c85de4d3c33776772d0d305cf497237`. **H09-P02 BLOQUEADA** hasta aceptación expresa del usuario de la jugabilidad F06 en el MSI (prevista, no garantizada, para el sábado 28-11-2026) y reconciliación de la versión F06 aceptada. No hay certificación de H09 global ni nueva operativa sensorial Core/UE. [Acta y CI](H09_P01_ACTA_AUDITORIA_FUSION_2026-11-27.md).

Fecha de creación: 2026-11-11. **Estado revisado: 2026-11-23**. **M1 CERTIFICADO EN ALCANCE LIMITADO** para HOST Academy mínimo en Unreal 5.8.4 y presentación en pantalla completa; [acta de certificación](H06_IA03C05_ACTA_CERTIFICACION_M1_2026-11-23.md). PR #200 fusionada en `main` (`9ab15007ee3cdeb8bf1453069ec327b0012d0a22`).

HOST coordina una campaña local entre Unreal Engine 5, F04/F05/F11 y CoreRPG, que conserva la autoridad sobre el universo. **El hito mínimo M1 está CERTIFICADO CON LIMITACIÓN**, no el HOST integral. H00–H05 están fusionadas en sus respectivos alcances; H06 C-01…C-05 se han cerrado para la integración mínima UE 5.8.4. La presentación Slate a **2560×1600 en modo ventana presenta un defecto de escalado/centrado y NO está certificada**; a esa resolución el menú y «Continuar» fueron aceptados tras Alt+Intro a pantalla completa. Se conserva el límite en el [acta M1](H06_IA03C05_ACTA_CERTIFICACION_M1_2026-11-23.md). Las capacidades institucionales F11 y las fases H07–H13 siguen fuera de este certificado.

> **Nota de vigencia:** el [Plan Maestro v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md) y muchas actas describen el estado histórico **en su fecha**. No deben utilizarse como estado actual de ramas, PR o módulos. Consultar también la [auditoría H00–H13 del 20/11, PR Draft #183](https://github.com/robdor80/Videojuego_StarTrek/pull/183) en su rama/PR Draft #183 mientras no se fusione.

## Documentos de gobierno

- [Plan Maestro v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md): fases H00-H13, hitos M0/M1 y frontera con F11.
- [H00 — Inventario](H00_INVENTARIO_DEPENDENCIAS_2026-11-11.md): componentes reales y pines.
- [H00 — Gobierno y riesgos](H00_GOBIERNO_RIESGOS_2026-11-11.md): separación de responsabilidades y protección GitHub.
- [H00 — Acta](H00_ACTA_2026-11-11.md): evidencia de auditoría documental. PR #111 fusionada.

## H01 — Arquitectura y contratos (entrega documental histórica, ya integrada)

1. [H01-P01 Arquitectura](H01_P01_ARQUITECTURA_v1.0_2026-11-11.md): módulos, hilos, ciclo de vida y propiedad.
2. [H01-P02 Contratos](H01_P02_CONTRATOS_v1.0_2026-11-11.md): solicitudes, resultados, errores y versiones.
3. [H01-P03 Confianza](H01_P03_CONFIANZA_v1.0_2026-11-11.md): principal, partida importada y límites offline.
4. [H01-P04 Compatibilidad](H01_P04_COMPATIBILIDAD_v1.0_2026-11-11.md): pines Core, CMake, historial y no duplicación.
5. [Matriz de conformidad H01](H01_MATRIZ_CONFORMIDAD_v1.0_2026-11-11.md): 35 casos para futuras fases; no ejecutados en runtime.
6. [Registro de contratos v1](H01_REGISTRO_CONTRATOS_v1.json): catálogo lógico verificable, no ABI compilada.
7. [Acta H01](H01_ACTA_2026-11-11.md): entregas, límites y transición a H02.

Validador estático: desarrollo/tools/validation/test_host_h01_contracts.py y CI host-h01-contracts.yml. No constituye prueba del HOST de producto.

## H06 — Academia integrada, pruebas MSI y puerta de certificación M1

- [Tablero operacional H06](H06_CONTROL_UNICO_ESTADO_2026-11-21.md): fuente actual del estado de C-01…C-05 y M1.
- [Protocolo C-05](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md): requisitos G0–G7.
- [**Acta definitiva M1 con alcance limitado**](H06_IA03C05_ACTA_CERTIFICACION_M1_2026-11-23.md): decisión G0–G7, aceptación del usuario, limitación de presentación a 2560×1600 en ventana y siguiente fase H07.
- [Resultados UE/MSI y aceptación](H06_IA03C05_RESULTADOS_M1_2026-11-22.md): rondas por commit, Automation y pruebas manuales.
- [Auditoría independiente C-05](H06_IA03C05_AUDITORIA_CIERRE_2026-11-22.md): informe previo e histórico a la certificación.
- [PR #200 — reparación UBT/Slate/Escape](https://github.com/robdor80/Videojuego_StarTrek/pull/200): FUSIONADA; el código probado es 148dc86a.

La Academia definitiva será un prólogo narrativo ligero, probablemente 2D, no un campus 3D extenso. Los trabajos artísticos y narrativos posteriores no bloquean M1.

## H08-P01 — Eventos y servicios (contratos, sin dispatcher aún)

- [Contrato H08-P01 v1](H08_P01_CONTRATO_EVENTOS_SERVICIOS_v1_2026-11-23.md): fuentes F04/F05/F11, deduplicación, orden causal, visibilidad, resincro­nización y separación del reloj Core.
- [Registro lógico H08-P01](H08_P01_REGISTRO_EVENTOS_v1.json): invariantes comprobables y matriz HE-01…HE-16.
- Validador estático: `desarrollo/tools/validation/test_host_h08_p01_contract.py`, CI Ubuntu/Windows `.github/workflows/host-h08-p01-contracts.yml`.

**Madurez H08-P01:** diseño versionado; no hay nuevas APIs nativas, suscripción runtime, nuevo reloj ni notificaciones UE. H08-P02, P03 y P04 mantienen sus pruebas de producto pendientes. La fuente autoritativa es CoreRPG y las emisiones institucionales pertenecen a F11.

## H08-P02 — Distribuidor local de eventos nativos (F05)

- [Informe de implementación y límites H08-P02](H08_P02_DISTRIBUIDOR_EVENTOS_INFORME_2026-11-23.md): suscripciones C++ de órdenes F05, FIFO, acuses de presentación, no duplicación y relectura tras carga.
- 13 pruebas integradas con el Core real (`host.event.he01_delivery`…`he13_generation`) y 8 pruebas de cola aislada (`host.event.unit.*`) añadidas a la matriz de Actions nativa.
- **Alcance:** F05 únicamente, sin cambios ABI C/Unreal; F04/F11 y formateadores de avisos quedan pendientes de sus fases/contratos. Consultar CI de su PR antes de afirmar probado o fusionado.

## H08-P03 — Reloj de campaña y tareas acotadas

- [Especificación y pruebas del avance de reloj Core](H08_P03_RELOJ_ACTIVIDADES_CORE_2026-11-23.md): servicio C++ interno, `f04_advance` en hilo propietario, guardas de identidad y revisión, máximo 600 segundos / 128 tareas por petición.
- 15 casos `host.clock.*` con el F04/Core real, además de regresiones H02–H06 y producto Linux/Windows. Una ejecución parcial de Core es un recibo con `more_due=true`, **no un error que dispare reintentos**.
- Estado de este enlace: implementación en PR; la evidencia de CI y el estado de la fusión determinan si queda probado. Sin API C/Unreal nueva ni reloj paralelo.

## H08-P04 — Proyecciones de notificación no mutadoras

- [Contrato, catálogo de mensajes y matriz H08-P04](H08_P04_NOTIFICACIONES_V1_2026-11-23.md): proyección de transiciones F05 en textos seguros en castellano, usando la misma suscripción, hechos y acuses de H08-P02.
- API **C++ interna** `SessionOwner::poll_order_notifications`; sin nueva ABI C/Unreal, sin emisor F11, sin duplicar reloj ni historial.
- 14 pruebas con la fuente real F05/Core (`host.notification.hn*`) y 10 puras (`host.notification.unit.*`); la CI de la PR determina su estado de probado. El cierre de P04 no certifica automáticamente Unreal ni H08 integral.

## H09-P01 — Inventario y contrato de consolas (CERRADA EN ALCANCE DOCUMENTAL)

- [Contrato y matriz de 18 escenarios de aceptación](H09_P01_INVENTARIO_CONTRATO_CONSOLA_v1_2026-11-23.md).
- [Registro estructurado de 16 familias y 13 operaciones](H09_P01_REGISTRO_CONSOLAS_v1.json).
- [**Acta de cierre H09-P01, auditoría y fusión #211**](H09_P01_ACTA_AUDITORIA_FUSION_2026-11-27.md): evidencia GitHub Actions de 11/11 contratos en Linux y Windows, regresiones nativas y commit exacto fusionado.
- Validación estática: `desarrollo/tools/validation/test_host_h09_p01_contract.py` y `.github/workflows/host-h09-p01-contracts.yml`.
- **H09-P02 no se iniciará ni se considerará desbloqueada antes de la aprobación personal de F06 en el MSI**, y deberá utilizar únicamente la versión finalmente aceptada. Las PR #213 y #215 de F06 continúan Draft a 27-11-2026. La fecha prevista del sábado 28-11-2026 no es una autorización. No se declara F06 jugable, ni H09 operativa/certificada.

## H09-P03 — Navegación y CONN (diseño de producto y dependencias)

- [Auditoría y plan P03-A…G](H09_P03_AUDITORIA_ARQUITECTURA_PLAN_2026-11-27.md): propuesta de rutas distinta de orden CONN y movimiento real.
- [Contrato lógico P03 y 24 escenarios futuros](H09_P03_CONTRATO_NAVEGACION_CONN_v1.json): \`NAVIGATION_ROUTE_PROPOSE\` y \`CONN_MANEUVER_ORDER\` siguen **indisponibles en runtime**. Sin ABI nueva ni certificación.
- [H09-P03-C01 — Informe de factibilidad nativa](H09_P03_C01_FACTIBILIDAD_CORE_2026-11-27.md): **FUSIONADO, PR #231**; pin Core con conocimiento, contención, reloj y persistencia, pero sin ubicación/cartas ni ejecutor naval de producto. Pruebas C01 documentales y de regresión existentes; **no** se probó navegación.
- [H09-P03-C02 — Diseño de ubicación/carta/propuesta](H09_P03_C02_DISENO_DOMINIO_NAVAL_2026-11-27.md): opción de dominio en composición de producto, sujeta a compatibilidad con esquema y guardado F04.
- [H09-P03-C02 — Contrato lógico y 14 escenarios **NO EJECUTADOS**](H09_P03_C02_CONTRATO_DOMINIO_NAVAL_v1.json): ubicación discreta Core, conocimiento autorizado, propuesta pura sin mover nave y compatibilidad de partidas viejas.
- [H09-P03-C02 — Encargo Codex Cloud preparado, Sol 6.2 Medium](H09_P03_C02_ENCARGO_CODEX_CLOUD_2026-11-27.md): P0 de factibilidad; implementar solo dentro de las autorizaciones reales, PR Draft y sin fusión.
- Validadores de diseño: \`desarrollo/tools/validation/test_host_h09_p03_contract.py\` y \`test_host_h09_p03_c02_contract.py\`; CI Linux/Windows. No sustituyen pruebas C++.
- **Estado:** C01 FUSIONADA; C02 **PREPARACIÓN DOCUMENTAL**. Ubicación y carta no funcionan en HOST; propuestas, órdenes, vuelo y UE pendientes. H09-P02 continúa BLOQUEADA por aceptación F06 en MSI; H09-P04 no iniciada y H09-P03-E/F pendientes.


## Fases y responsables

H00 y H01: ChatGPT (auditoría y diseño). H02: Codex (núcleo). H03: ChatGPT+Codex (identidad). H04: Codex (persistencia). H05: Codex (Core/F04/F05). H06: Codex (UE real). H07: ChatGPT+Codex (lector y pasarela NO emisora de F11). H08-H11: coordinación y sistemas progresivos. H12-H13: estabilidad y certificación.

## Restricciones vinculantes

- Solo CoreRPG conserva WorldState y tiempo autoritativo. F11 del proyecto principal desarrolla y certifica su emisor de Personal de Flota. HOST no emite comisiones, grados ni rangos, ni replica sus reglas.
- Las APIs F04/F05/F11 usan una única F04Session en hilo propietario. ID, F04Ref, cause y CAUSE=110501 no son credenciales.
- El proyecto principal UE **sí** incluye `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`. La compilación requiere preparar `host_abi.h`, `TrekHost.dll` y `TrekF04Bridge.dll` mediante `Build/Prepare-Host.ps1`. La generación del mapa diagnóstico sigue el [README de StarTrekRPG](../../../../juego/UE5/StarTrekRPG/README.md); las pruebas históricas documentadas fueron en UE 5.8.2, no certifican por sí mismas UE 5.8.4.
- Los pins históricos siguen intactos. H01 propone F05/F11 Core SHA 76a7b7b485616d8c4994f384a90f123bf333591d como candidato, no upgrade automático.
- Fases y PR independientes; solo el usuario autoriza fusiones. Estados PLANIFICADO, IMPLEMENTADO, PROBADO, CERTIFICADO y FUSIONADO no son intercambiables.
- Logs y artefactos temporales solo en laboratorios/ dentro del repositorio, excluidos de Git. No hay dependencias permanentes hacia esos resultados.

La H01 documental registró 11/11 comprobaciones estáticas PASS (Actions run 43089381278) y se integró posteriormente. Estas pruebas no sustituyen una certificación del juego ni de F11.

## H04 — Guardado, recuperación y procedencia

Implementación **fusionada** mediante [PR #135](https://github.com/robdor80/Videojuego_StarTrek/pull/135). Probada en el alcance nativo/fixtures H04; **no significa que el circuito de nueva partida M1 esté terminado ni certificado**.

- [Arquitectura H04](H04_PERSISTENCIA_2026-11-13.md): ranuras, procedencia, persistencia Core completa, publicación, recuperación e identidad H03.
- [Matriz y evidencia H04](H04_PRUEBAS_2026-11-13.md): casos nativos, procesos, inyección, compilaciones, CI y límites.
- [Acta técnica H04](H04_ACTA_2026-11-13.md): commits, auditoría, incidencias y riesgos pendientes.
