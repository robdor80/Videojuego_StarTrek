# AUDITORÍA INDEPENDIENTE DE HOST — H00–H13 / H06–IA / M0–M1

**Fecha:** 20 de noviembre de 2026.  
**Repositorio:** robdor80/Videojuego_StarTrek.  
**Corte auditado:** main en 57fcc1c99f3075b026525ab1411421da925cb5e5 (19-11-2026, 16:37:52 UTC).  
**Ámbito:** documentación, fuente C++/CMake de TrekHost, ABI C, interfaz UE5 StarTrekRPG, evidencia CI, trazas de PR/issue, F04/F05/F10/F11, centralización IA-01/IA-02/IA-03A, correspondencia con Sistemas S01–S19, Planificación 1 y 2.  
**Tipo de auditoría:** inspección estática y contraste remoto de código, documentos, PR y ejecuciones históricas de CI. **No se han ejecutado CTest, Unreal ni una llamada OpenAI LIVE en el equipo del auditor**, ni se ha accedido al MSI.  
**Alcance de esta PR:** solo añadir el presente informe; **no** modificar código, contratos LOCKED, pines, pruebas, mundos, materiales, laboratorios ni estados de producto; **no fusionar sin autorización del autor**.

## 1. Dictamen ejecutivo

**HOST es real y su hito M0 nativo está alcanzado y probado en el alcance previsto, pero HOST NO está terminado ni certificado como infraestructura integral del juego.** H06 tiene una integración técnica UE5 diagnóstica funcional y fusionada; M1, entendido como primera partida productiva de Academia, continúa abierto. H07–H13 no constituyen un runtime de producto terminado. IA-01 es un servicio C++ centralizado con HTTPS, límites y pruebas offline; IA-02 lo consume para revisión de biografías; IA-03A aporta reglas objetivas y fuentes internas. Nada de ello crea todavía al protagonista en CoreRPG desde Unreal, conecta todos los NPC/computadora ni acredita una llamada real al proveedor.

El obstáculo principal ha cambiado desde el primer diseño: la decisión DEC-0022 del 17-11-2026 obliga a **un protagonista único híbrido humano-vulcano, 45 años en 2383**, con biografía canónica y edición limitada. El código productivo F10/IA-03A aún permite tres especies y el planteamiento anterior. Debe **versionarse y migrarse**, no eliminar contratos históricos ni saltarse la admisión en F10.

**No hay evidencia para afirmar que HOST tenga una corrupción activa, un fallo de seguridad explotable o CI fallida.** Los riesgos enumerados incluyen ausencias de integración, políticas obsoletas, pruebas no ejecutadas y defectos de cobertura; el estado de cada uno se distingue. Tampoco es honesto calcular «porcentaje total» de funcionalidad sin una matriz de aceptación ponderada: no es equivalente completar un contrato y cerrar una campaña de Academia real.

## 2. Inventario contrastado de entregas

| Fase / subsistema | Estado al corte | Evidencia determinante | Límite real |
| --- | --- | --- | --- |
| H00 — auditoría y gobierno | Documentada y fusionada (#111) | H00_ACTA; PR #111 | El Plan Maestro conserva rótulos iniciales obsoletos |
| H01 — diseño, ABI y contratos | Documentada, pruebas estáticas y fusionada (#112) | H01_ACTA y contratos; workflow H01 | Los documentos no certifican runtime |
| H02 — TrekHost nativo / SessionOwner | Implementado, probado y fusionado (#132) | src/session_owner.cpp; CMake; tests | No es juego autónomo |
| H03 — identidad local / vínculo | Implementado, probado y fusionado (#134) | src/player_bootstrap.h, SessionOwner; H03_IDENTIDAD_NATIVA | Vínculo productivo Academia nuevo no resuelto |
| H04 — guardado y recuperación naval | Implementado, probado y fusionado (#135) | src/slot_store.cpp; H04 acta | Ruta tipada Academia no acreditada |
| H05 — pasarela F04/F05 y M0 | Implementado, probado y fusionado (#139/#140) | H05_ACTA_AUDITORIA_FUSION; run 43468890126 | Receptor de orden en fixture; F04_SCAN no es F06 |
| H06-P01–P05 — UE5 diagnóstico | Implementado, probado en su corte y fusionado (#141/#142) | StarTrekRPG.uproject; HostSessionSubsystem; H06_RESULTADOS | G3, HU-08/10/12 y aceptación manual real pendientes |
| H06-P06 — nueva partida Academia | Contratos, factibilidad y validadores; sin flujo productivo completo | issue #144 y #148, H06_P06_CIERRE_FUNCIONAL_MINIMO | No existe factory de campaña jugable unido a ABI/UE |
| IA-01 — servicio común OpenAI | Implementado C++, simulación y builds reales, fusionado (#164) | src/ai/*; tests/ai_tests.cpp; informe IA-01 | Sin LIVE, sin fachada general de consumo desde UE |
| IA-02 — revisión semántica F10 | Implementado y probado con transporte simulado, fusionado (#165) | src/f10/openai_biography.cpp; informe IA-02 | No es PERSON ni admisión; sin LIVE |
| IA-03A — reglas biográficas iniciales | Implementado y fusionado (#167) | biography_validation.cpp; initial_biography_tests.cpp; informe IA-03A | Política anterior a protagonista fijo DEC-0022 |
| IA-03B / IA-03C | Pendientes de producto | IA-03A informe y S04_MIGRACION_F10_HOST_v2 | Persistencia productiva del flujo y UI/ABI academia no cerradas |
| H07 — pasarela F11 no emisora | Planificada; reader F11 externo existe, pero integración HOST no probada | plan H07; PR #109 de F11; PR #110 Draft | En ABI H06: SERVICE_UNAVAILABLE deliberado |
| H08 — eventos y reloj | Pendiente de integración de producto | Plan Maestro H08 | Sin dispatcher/scheduler general probado |
| H09 — sensores y navegación | Pendiente de integración de producto | Plan Maestro H09; auditoría F00–F15 | F04_SCAN de M0 es fixture, no sensor espacial |
| H10 — NPC, ordenador e IA | Parcial por IA-01; H10 propia pendiente | Plan Maestro H10 y S01/S02 | Sin consumidor NPC/computadora E2E |
| H11 — misiones y temporadas | Pendiente de integración de producto | Plan Maestro H11 | Planificación 2 es referencia offline, no universo vivo Core |
| H12 — observabilidad/rendimiento | Pendiente para uso real prolongado | Plan Maestro H12 | No prueba de campaña larga CPU/VRAM/red |
| H13 — certificación integral | Pendiente | Plan Maestro H13 | No cierre de producto ni aceptación final |

Las PR #132, #134, #135, #139, #140, #142, #164, #165 y #167 aparecen **cerradas y fusionadas** en GitHub. Esto corrige los estados de «Draft», «no fusionada» o «no existe .uproject» que permanecen en documentos redactados antes de tales fusiones.

## 3. Evidencia de código y de CI

### 3.1 Fuentes efectivamente inspeccionadas

- desarrollo/integration/host/CMakeLists.txt; include/trek/host/host_abi.h, session_owner.h, ai/service.h.
- src/session_owner.cpp, host_abi.cpp, slot_store.cpp, gateway_bridge.cpp; src/f10/biography_validation.cpp, openai_biography.cpp; src/ai/service.cpp, https.cpp, credentials.cpp.
- juego/UE5/StarTrekRPG/Source/StarTrekRPG/Private/HostSessionSubsystem.cpp y README; descriptor uproject, configuración de mapa.
- .github/workflows/host-h01-contracts.yml y host-h02-native.yml; configuración sistemas/ai/host_service_config_v1.json.
- Plan Maestro HOST v1.2; informes y actas H00/H01/H05/H06/IA-01/IA-02/IA-03A; documentación de transición S04.
- Auditorías del 19-11 de Planificación 1, Planificación 2 y Sistemas, exclusivamente como fuentes de dependencias, **sin reabrir sus auditorías**.

### 3.2 Pruebas verificadas como evidencia histórica, no repetidas ahora

- H05/M0, run [43468890126](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43468890126): informe de auditoría anterior recoge 236/236 CTest Linux, 236/236 Windows, 81/81 ASan/UBSan y producto tests OFF en ambas plataformas. Corresponde al SHA H05 de aquella fecha.
- H06 integración UE5, run [43497059525](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43497059525): anterior auditoría contrastó 238/238 Linux y Windows, 83/83 ASan/UBSan, dos productos tests OFF. Los resultados UE5 NullRHI/D3D12, UBT/UHT y paquete Win64 están **declarados por informe local de Codex**, no ejecutados aquí.
- IA-03A corrección #167, run [43763464789](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43763464789), HEAD 1ae2013ebda95109b360c00644bbf34b3f51c827: GitHub confirma estado **completed/success** y cinco jobs terminados correctamente: native Linux, native Windows, ASan/UBSan, product Linux y product Windows. Las cantidades locales informadas (111 HOST, 17 F11, 529 Python) pertenecen a esa corrección, no a una ejecución realizada el 20-11.
- IA-01/IA-02/IA-03A informan explícitamente **OpenAI LIVE NOT_RUN**. Las respuestas semánticas probadas son simuladas, aunque el código de red y la integración de pruebas nativas sean reales.
- La consulta de main el 20-11 devuelve SHA 57fcc1... y no acredita por sí sola que todos los suites HOST hayan sido reejecutados en ese SHA. La CI de HOST actualmente no escucha push a main.

### 3.3 Fronteras arquitectónicas que se preservan

CoreRPG es el único dueño del estado y las mutaciones; TrekHost tiene un SessionOwner y un acceso propietario a F04Session; F04/F05 resuelven permisos/órdenes navales; F10 decide creación e ingreso académico; F11 emite y valida hechos institucionales fuera del HOST; Unreal expresa intenciones y presenta proyecciones; IA genera propuestas lingüísticas, **nunca concede hechos, rangos, plaza, autoridad o permisos**. La prohibición de publicar funciones del fixture M0 para suplantar receptor/ejecutor sigue vigente. El pin CoreRPG actualmente fijado es 76a7b7b485616d8c4994f384a90f123bf333591d y no debe cambiarse de forma incidental.

## 4. Hallazgos auditables y correctivos

Severidad: **P0** bloquea el primer recorrido productivo jugable; **P1** requiere corrección antes de su integración o cierre; **P2** deuda de robustez, cobertura y mantenimiento. P0 no significa que el diagnóstico actual esté roto.

### AH-01 [P0, confirmado] No existe bootstrap productivo Academia→PERSON→sesión→guardar→cargar desde Unreal

**Prueba:** issue #148 indica expresamente «NO IMPLEMENTADO»; host_abi.h expone OPEN de población de nave y RESTORE naval, no NEW_ACADEMY; CMake incluye un ejecutable academy_core_feasibility solo con TREK_HOST_TESTS, y prueba unsupported_academy_open. HU-08 está BLOCKED. **Riesgo:** no hay primera partida jugable real; fixture ≠ cadete. **Corrección:** factory autorizado por F10/Core, idempotencia por clave, alta exactamente una PERSON con estado candidato, unión H03 no naval, SAVE/RESTORE tipados H04, extensión ABI y UX UE. **Aceptación:** alta→vínculo→guardado→otro proceso→misma PERSON y contexto; rechazo de persona arbitraria, errores y duplicados.

### AH-02 [P0, confirmado] El runtime biográfico no cumple el protagonista canónico S04 v2

**Prueba:** H06_S04_TRANSICION_PROTAGONISTA_FIJO y S04_MIGRACION_F10_HOST_v2 dicen «HOST/CODEX POR ADAPTAR»; biography_validation.cpp sigue validando initial_species mediante selectable_species. **Riesgo:** el jugador podría seleccionar un personaje incompatible con la historia y la intro. **Corrección:** política nueva y versionada de protagonista fijo (DEC-0022), datos autorales internos, nombre/cosmética permitidos, pruebas negativas; preservar v1 y NPC multiespecie. **Aceptación:** ninguna nueva partida 2383 admite otra especie, sexo, edad ni antecedentes elegidos; no duplica admisión al repetir la intro.

### AH-03 [P1, confirmado] M1 y H06-P06 no pueden declararse cerrados

**Prueba:** H06_ACTA_AUDITORIA_FUSION_PARCIAL marca G3/HU-08/HU-10/HU-12 bloqueadas; issue #144 abierta. **Riesgo:** confundir «mapa de diagnóstico» con «videojuego iniciado». **Corrección:** mantener estatus PARTIAL hasta aceptación interactiva en MSI, con identidad de producto y órdenes válidas/denegadas; no exigir sensores F06 completos para probar el corte mínimo. **Aceptación:** matriz HU actualizada con pruebas efectivas y acta M1.

### AH-04 [P1, confirmado] Alta de candidato no equivale a admisión, plaza ni carrera

**Prueba:** issue #148 y H06_P06_CIERRE_FUNCIONAL_MINIMO distinguen CANDIDATE de ADMITTED/CADET; F11 sigue dueño de comisión/rangos. **Riesgo:** regalar el ingreso o tener un «cadete» sin hecho académico. **Corrección:** fuente F10 firmemente vinculada, transición institucional, cupo, idempotencia, rechazo y estados visibles. **Aceptación:** crear candidato no ocupa plaza; solo decisión F10 consume una plaza exactamente una vez.

### AH-05 [P1, confirmado] Acoplamiento H03/H04 a la campaña naval F05

**Prueba:** H05/issue #148 documentan bind_player naval y slot H04 de campaña de nave; no se documenta restauración de catálogo académico productivo. **Riesgo:** fingir tripulación de nave para vincular al candidato, otorgando capacidad indebida o rompiendo saves. **Corrección:** discriminador explícito por campaña, migración aditiva y preservación de slots H04 existentes. **Aceptación:** candidato sin F05 no puede emitir orden naval; slot naval previo recupera sin cambios.

### AH-06 [P1, confirmado] IA-03B/IA-03C aún no forman cadena productiva con UE

**Prueba:** informe IA-03A reserva IA-03B persistencia y IA-03C fachada/UI; HostSessionSubsystem solo expone Open, Close, Query, Save y Restore. **Riesgo:** validación local fuerte pero no disponible para el jugador. **Corrección:** adaptar a S04 v2, conectar evidencia y revisión a factory, representar estados pendiente/contradicción/error sin bloquear el Game Thread. **Aceptación:** UX usa únicamente recibo verificable de operación nativa, no flags enviados por Blueprint.

### AH-07 [P1, confirmado] Centralización IA existente, pero consumidores reales incompletos

**Prueba:** Service C++ interno tiene rutas FAST_LANGUAGE, REASONING_LANGUAGE, DIALOGUE, COMPUTER_ANALYSIS y NARRATIVE_SUMMARY; hoy el consumidor productivo implementado es F10/IA-02; documentación IA-01 deja la fachada UE/NPC/computadora para después. **Riesgo:** nuevas funciones crean clientes HTTPS duplicados o saltan las barreras de Core. **Corrección:** contrato genérico común, gateway/fachada ABI de consumo controlado, un contexto autorizado por tarea y prueba de no duplicación. **Aceptación:** NPC, ordenador y narración reutilizan el mismo servicio sin tener acceso a claves ni emitir cambios del mundo.

### AH-08 [P1, confirmado] No hay prueba LIVE de OpenAI ni de compatibilidad real de modelos configurados

**Prueba:** informes IA-01/02/03A dicen LIVE NOT_RUN; configuración establece gpt-6-luna y gpt-6.1-sol, sin evidencia de aceptación real por la API, cuotas, latencia o respuesta modelo/Structured Outputs. **Riesgo:** fallo en primera interacción real a pesar de tests simulados. **Corrección:** smoke con permiso del autor, clave local segura y gasto limitado; comprobar nombres reales del proveedor, campos de respuesta, refusals, rate limits, privacidad y comportamiento sin clave; publicar solo metadatos saneados. **Aceptación:** una revisión controlada verificable y manejo correcto de error sin crear PERSON.

### AH-09 [P1, confirmado en fuente] Presupuesto IA de 200 llamadas acumuladas por vida de Service, sin política visible de renovación

**Prueba:** host_service_config_v1.json fija max_calls=200; service.cpp incrementa calls y devuelve CAPACITY desde entonces, sin reset dentro de la instancia. **Riesgo:** en una campaña extensa con NPC, 200 solicitudes agotarían el servicio permanentemente hasta recrearlo; además, un único worker/cola puede producir bloqueo entre funciones. **Corrección:** documentar el propósito del límite y decidir presupuesto recargable por ventana/campaña y prioridad/fairness por consumidor, con prueba de carga, cancelación, starvation y cotas de coste. **Aceptación:** agotamiento controlado y recuperable según política; ninguna ráfaga NPC impide indefinidamente respuesta esencial.

### AH-10 [P1, confirmado] H07: lectura y pasarela institucional no certificadas en HOST

**Prueba:** host_abi.cpp presenta SERVICE_UNAVAILABLE; F11 reader externo #109 y documentos #110 no constituyen un emisor institucional productivo. **Riesgo:** presentar rangos o permisos deducidos desde HOST para suplir F11. **Corrección:** cuando F11 apruebe su API, H07 solo autentica, transmite y proyecta el hecho confirmado. **Aceptación:** ausencia de emisor causa denegación explícita; eventos F11 válidos se muestran sin crear grados.

### AH-11 [P1, confirmado] H08-H11 aún no aportan despacho/eventos/reloj/sensores/misiones del juego real

**Prueba:** Plan Maestro H08–H11; auditorías F00–F15 y Planificación 2: F06 y B01–B10 tienen referencias/offline pero no conexión de universo vivo autoritativo. **Riesgo:** introducir buses, mundos o schedulers paralelos ad hoc por sistema. **Corrección:** uno por uno según sus fases; definir dueño de acción, evento, causalidad, visibilidad y reintentos. **Aceptación:** pruebas cruzadas de órdenes/eventos y SAVE/LOAD, sin datos inventados por IA.

### AH-12 [P1, confirmado] CI HOST no vigila los cambios propios de Unreal ni hace regresión automática tras push a main

**Prueba:** .github/workflows/host-h02-native.yml solo declara pull_request y workflow_dispatch; sus paths no incluyen juego/UE5/StarTrekRPG/** ni el script Build/Prepare-Host.ps1; H01 solo hace push a una antigua rama design. **Riesgo:** fusiones posteriores a #167 pueden llegar a main sin suite HOST. **Corrección:** ampliar filtros UE y del contrato, trigger push main con coste razonable y tests nativos; UE5 local o runner autorizado en puerta separada, no fingirlo en GitHub-hosted. **Aceptación:** PR que altera HostSessionSubsystem o ABI dispara CI; tras merge hay traza de HEAD.

### AH-13 [P1, confirmado] Índices y Plan Maestro HOST con estados históricos tratados como estado actual

**Prueba:** Plan Maestro v1.2, línea inicial, afirma H01-H13 solo planificadas y H00 Draft, mientras #111/#112/#132... están fusionadas; README HOST dice que no existe .uproject, y llama a H04 «PR #135 Draft/no fusionada»; sí existe StarTrekRPG.uproject. **Riesgo:** Codex recibe encargos duplicados o intenta crear otro proyecto. **Corrección:** no reescribir evidencia del 11-11; añadir índice «estado vigente a 20-11», precedencia y referencias a actas posteriores, dejando histórico visible. **Aceptación:** un solo tablero claro de implementado/probado/fusionado/certificado.

### AH-14 [P1, confirmado] Falta aceptación funcional de UX del usuario y campaña real sobre MSI

**Prueba:** H06_RESULTADOS documenta automatización UBT/UHT, NullRHI/D3D12 sobre fixture; H06 acta y #144 mantienen aceptación manual pendiente. **Riesgo:** no detectar errores reales de iniciación, entrada, viaje entre mapas o cierre. **Corrección:** test interactivo manual y automatizado de nueva partida S04, GameInstance, dos mundos, salida y reanudación en hardware destino. **Aceptación:** grabación de evidencia, SHA y resultado del usuario en M1; no confundir automatización antigua con experiencia real completa.

### AH-15 [P1, confirmado como riesgo de reconstrucción] Mapa de arranque UE generado y excluido del repositorio

**Prueba:** DefaultEngine.ini apunta a /Game/Diagnostics/HostDiagnostic; .gitignore excluye *.umap; README describe commandlet que reconstruye ese mapa. **No es un fallo por sí mismo:** es una decisión para no versionar binarios. **Riesgo:** abrir una copia de Git sin ejecutar la generación puede conducir a mapa ausente/escenario vacío y confusión durante la intro definitiva. **Corrección:** bootstrap reproducible documentado y comprobado, diagnóstico explícito cuando falta mapa; coordinar la futura intro con F14/UE, sin tocar assets originales. **Aceptación:** clon limpio + comando reproducen mapa funcional y se detecta ausencia antes del lanzamiento.

### AH-16 [P1, confirmado] No equivalencia entre F04_SCAN técnico y sensores F06

**Prueba:** H05_ACTA_AUDITORIA_FUSION y H06 informan que F04_SCAN es tirada de fixture F05; F06 espacial completa permanece Draft. **Riesgo:** presentar un test M0 como sensor de nave terminado. **Corrección:** en H09 consumir la API de sensores autoritativa F06, con conocimiento por observador, protección de secretos y decisión de contexto. **Aceptación:** contactos reales de WorldState, ausencia de leak y navegación consecuente; prueba independiente de fixture.

### AH-17 [P2, confirmado] Protección main existente, pero sin aprobaciones obligatorias ni checks requeridos en el ruleset observado

**Prueba:** API de GitHub indica main protected:true; ruleset activo Proteccion MAIN - Star Trek RPG (id 27170774), con deletion, non_fast_forward y pull_request; required_approving_review_count=0. La lectura de branch-protection clásica devolvió 403 por el conector, no puede concluirse nada más sobre esa API. **Riesgo:** merge sin revisión independiente o CI obligatoria si no hay otra regla. **Corrección:** evaluar exigencia proporcionada de checks y revisión para cambios críticos, sin imponer burocracia a un proyecto privado de una persona. **Aceptación:** protección declarada y verificada, sin bloquear el flujo legítimo del autor.

### AH-18 [P2, confirmado como alcance pendiente] Persistencia: corrupción/versión no equivalen a autenticidad frente al dueño del equipo

**Prueba:** slot_store.cpp tiene control de raíz, no-follow, manifiesto, identidad, pin, publicación y pruebas de fallos; Plan Maestro advierte que integridad no es autenticación criptográfica frente a un ejecutable local alterado. **No se constata bypass explotable.** **Riesgo:** interpretar SAVE_UNTRUSTED como protección absoluta ante quien modifica datos, binarios y claves locales. **Corrección:** definir amenaza real offline, imports, migraciones y errores recuperables; no diseñar servidor/DRM. **Aceptación:** matriz de manipulación de slot, rollback, carga cruzada y directorios hostiles; mensajes honestos.

### AH-19 [P2, confirmado como verificación pendiente] Privacidad, costes y observabilidad central de IA sin pruebas de campaña

**Prueba:** IA-01 implementa límites de bytes, tiempo y rutas, y no registra texto bruto en resultados documentados; H12 y pruebas LIVE permanecen pendientes. **Riesgo:** latencia y presupuesto de API sin medición en el juego real, exceso de contexto en NPC. **Corrección:** telemetría agregada sin secretos, contadores por ruta, política de contexto mínimo, degradación offline, límites de coste y pruebas de presión. **Aceptación:** métricas locales reproducibles y ausencia comprobada de claves/biografías en logs.

### AH-20 [P2, confirmado] Reconciliación de dependencias y pines entre HOST, F05, F10, F11 y sistemas futuros

**Prueba:** CMake fija CoreRPG a 76a7b7... y comprueba el checkout; Planificación 1 mantiene abierta la corrección F05 #177, F11 emisor #110 Draft y S04 v2 pendiente. **Riesgo:** un cierre documental posterior mueve o contradice contratos sin prueba de compatibilidad. **Corrección:** matriz de propietarios y versiones por componente; rebase/pin solo bajo control de los respectivos proyectos, con regresión HISTÓRICA y nueva. **Aceptación:** certificado de compatibilidad de cada interfaz, negativa a alterar reglas no autorizadas y no duplicación de autoridad.

## 5. Qué falta realmente para alcanzar el siguiente hito útil

**Prioridad de producto, no expansión de infraestructura:**

1. Cerrar por S04/F10 el contrato vigente de protagonista fijo y su fuente interna confiable.
2. Implementar una sola operación de creación de candidato REAL en la sesión Core fijada, sin regalar admisión y sin admitir un PERSON elegido desde UI.
3. Vincular la identidad H03 y persistir por H04 una campaña Academia tipada, recuperable entre procesos.
4. Exponer ABI/UE mínima de nueva partida y ficha/vista; reutilizar IA-01/02 solo donde la política v2 realmente exija revisión y conservar modo de fallo cerrado.
5. Pasar las negativas esenciales (repetición, perfil incompatible, falta de fuente, conflicto de clave, cambio de mundo, orden naval sin competencia, archivo corrupto) y el recorrido manual D3D12.

**Eso cerraría M1**, no H07–H13 ni todas las fases del videojuego. En particular, no adelantar desarrollo completo de Sensores, NPC/temporadas o integración del universo de Planificación 2 solo para declarar «HOST terminado».

## 6. Hoja de ruta de corrección — R0 a R7

| Etapa | Responsable natural | Alcance autorizado recomendado | Salida objetiva |
| --- | --- | --- | --- |
| **R0 — reconciliación documental** | Conversación HOST + Codex documental | Estado vigente, precedencia S04, CI/PR/actas sin falsear el histórico | Índice único H00–H13 e IA con links y estados verificados |
| **R1 — puerta de producto F10/S04** | F10/S04 + HOST + Codex GPT-6 Alto | Política v2, origen autoral, perfiles y negativas; no modificar v1 LOCKED | Contrato nuevo y pruebas de adaptación |
| **R2 — M1 productivo** | HOST/UE y F10/Core; Codex GPT-6 Alto | Factory candidato, H03/H04 Academia, ABI y UE; sin emisor F11 | Flujo crear/guardar/cargar sin duplicados, campaña real |
| **R3 — endurecimiento IA y CI** | HOST + Codex GPT-6 Medio/Alto | Smoke LIVE opt-in, rutas/modelos, presupuesto, fairness, secretos; CI main/UE | Tests negativos y metadatos de latencia/coste sin secretos |
| **R4 — H07/F11** | F11 primero; HOST solo consume | Lector y pasarela no emisora; bloqueo cuando falta contrato F11 | Hechos institucionales auténticos en UE, sin duplicación |
| **R5 — H08–H11** | Conversaciones de fase y sistemas | Eventos/reloj, sensores/nav, NPC/computadora, misiones, escalonados | E2E reales por sistema sobre Core y misma sesión |
| **R6 — H12** | HOST/QA + Codex GPT-6 Medio/Alto | Instrumentación, campañas largas, budgets CPU/VRAM/API, recuperación de fallos | Benchmarks en MSI/UE, sin regresiones de producto |
| **R7 — H13** | Auditoría independiente + autor | Matriz de cobertura, CI multi-SO, D3D12/NullRHI, privacidad y aceptación | Certificación por alcance aprobado, jamás por documentación sola |

**Importante:** esta auditoría **no autoriza ejecutar de inmediato R1–R7 ni rediseñar Planificación 1, Planificación 2, Sistemas o F11**. Sirve para que la conversación específica de HOST corrija sus propios componentes cuando el autor lo indique. La migración S04 se coordina con su propietario; los problemas de F11, F06 y F13 corresponden a sus ámbitos.

## 7. Matriz mínima de aceptación futura

| ID | Escenario | Estado constatado al corte | Evidencia necesaria |
| --- | --- | --- | --- |
| MH-01 | M0 sesión Core + F05 + guardar/cargar nativo | HISTÓRICO PASS | Mantener regresiones |
| MH-02 | Cargar DLL Release ABI v1 Windows/Linux | HISTÓRICO PASS | Repetir en HEAD que se libere |
| MH-03 | UE5 diagnóstico NullRHI/D3D12 | INFORMADO PASS local en H06 | Repetir al cerrar M1 |
| MH-04 | Protagonista S04 único, sin editor libre | PENDIENTE | Nueva política v2 + pruebas |
| MH-05 | F10 crea exactamente una PERSON candidata | BLOCKED | Factory producto |
| MH-06 | Candidato no recibe comisión/plaza/orden naval | BLOCKED E2E | Denegación Core real |
| MH-07 | Alta→H03→H04→nuevo proceso→mismo sujeto | BLOCKED | Campaña Academia persistente |
| MH-08 | ABI/Unreal y manual D3D12 con personaje real | BLOCKED | UBT/UHT + interacción real |
| MH-09 | OpenAI LIVE controlada y sin datos sensibles en logs | NOT_RUN | Consentimiento y una ejecución acotada |
| MH-10 | 200+ solicitudes IA y presupuesto justo/reiniciable | NO ACREDITADO | Stress/saturación por rutas |
| MH-11 | HOST CI por cambio UE y por push a main | AUSENTE | Disparadores y run sobre SHA |
| MH-12 | F11 eventos autorizados sin HOST emisor | NO IMPLEMENTADO | Integración H07 |
| MH-13 | Sensores, reloj y universo conectado | NO IMPLEMENTADO | H08/H09/F06/F13 |
| MH-14 | NPC/ordenador con IA central, sin autoridad LLM | NO IMPLEMENTADO E2E | H10 y pruebas de aislamiento |
| MH-15 | Campañas largas, rendimiento en RTX 4070 | NO CERTIFICADO | H12 |
| MH-16 | Certificación integral HOST | PENDIENTE | H13 y autorización del autor |

## 8. Principios de corrección no negociables

- Proyecto de uso **exclusivamente privado**; no se justifica introducir servidor, DRM, autenticación remota ni políticas de publicación/distribución.
- Mantener un solo WorldState, SessionOwner y proveedor IA común; ni Blueprints ni prompts ni personajes arbitran permisos.
- No actualizar ni relajar sin aprobación el pin CoreRPG, los contratos históricos LOCKED, tests F11, oráculos de F04/F05 ni la política de confianza.
- Guardar historia y decisiones existentes; los informes viejos no se sobrescriben para fingir que siempre reflejaron el estado actual.
- No borrar ni forzar commit de laboratorios; no tocar assets Valhalla/intro ni fuentes 3D.
- Las pruebas históricas son evidencia del SHA de aquel momento, no una certificación nueva de main.

## 9. Fuentes y navegación

**Código y estado:**  
- [TrekHost C++](https://github.com/robdor80/Videojuego_StarTrek/tree/main/desarrollo/integration/host) · [Unreal StarTrekRPG](https://github.com/robdor80/Videojuego_StarTrek/tree/main/juego/UE5/StarTrekRPG) · [CI HOST](https://github.com/robdor80/Videojuego_StarTrek/blob/main/.github/workflows/host-h02-native.yml).  
- [Plan Maestro H00–H13](../architecture/host/PLAN_MAESTRO_HOST_v1.2_2026-11-11.md) · [Acta M0 H05](../architecture/host/H05_ACTA_AUDITORIA_FUSION_2026-11-13.md) · [Acta H06 parcial](../architecture/host/H06_ACTA_AUDITORIA_FUSION_PARCIAL_2026-11-13.md).  
- [IA-01](../architecture/host/H06_IA01_INFORME_IMPLEMENTACION_2026-11-15.md) · [IA-02](../architecture/host/H06_IA02_INFORME_IMPLEMENTACION_2026-11-15.md) · [IA-03A](../architecture/host/H06_IA03A_IMPLEMENTACION_REGLAS_F10_2026-11-15.md).  
- [Transición S04](../architecture/host/H06_S04_TRANSICION_PROTAGONISTA_FIJO_2026-11-17.md) · [Migración S04 v2](../../../sistemas/gameplay/character_creation/S04_MIGRACION_F10_HOST_v2.md).
- [Issue M1 #144](https://github.com/robdor80/Videojuego_StarTrek/issues/144) · [Issue factory #148](https://github.com/robdor80/Videojuego_StarTrek/issues/148).  
- [Auditoría Planificación 1](AUDITORIA_PLANIFICACION_1_F00_F15_2026-11-19.md) · [Auditoría Planificación 2](AUDITORIA_PLANIFICACION_2_B01_B10_2026-11-19.md) · [Auditoría Sistemas](AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md).

## 10. Conclusión y siguiente decisión

**La base HOST está bien encaminada y es aprovechable; el trabajo útil no consiste en reiniciar HOST, sino en reconciliar su dirección con S04 y completar la entrada productiva al juego.** No consta motivo para rehacer H02–H05 ni crear un HOST nuevo. La prioridad de corrección es **AH-01/02/03/04/05/06**; después IA/CI y solo posteriormente H07–H13 en sus tiempos.

**Estado de la auditoría:** documentación concluida en rama separada; **ningún hallazgo ha sido corregido por el mero hecho de redactarlo**. Su fusión y la ejecución de remediaciones necesitan revisión y autorización del autor.
