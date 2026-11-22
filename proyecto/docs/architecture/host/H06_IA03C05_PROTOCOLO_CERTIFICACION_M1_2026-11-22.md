# H06 · IA-03C-05 — Protocolo de pruebas, auditoría y aceptación M1

**Fecha de preparación:** 22-11-2026. **Responsable documental:** ChatGPT. **Ejecutor UE/MSI:** Codex (GPT-6, razonamiento Alto). **Aceptación interactiva:** usuario.
**Estado:** PLANIFICADO Y DOCUMENTADO; **NO EJECUTADO** en MSI, **NO PROBADO** en UE 5.8.4, **M1 NO CERTIFICADO**. Este documento es el protocolo previo a la ejecución, no un acta de resultados.
**Repositorio:** robdor80/Videojuego_StarTrek. **Base verificada:** main a27af56c200ebf5d8fbbaff23cb1b0cecbf56cb7 (merge PR #197, 22-11-2026).
**Proyecto:** juego/UE5/StarTrekRPG/StarTrekRPG.uproject; **motor requerido:** Unreal Engine 5.8.4.

## 1. Fuentes y precondiciones verificadas

Se han contrastado AGENTS.md, laboratorios/README.md, el tablero H06, los informes IA-03C-01/02/03/04, el diseño C-04, el README del proyecto UE, los nombres de pruebas en HostAcademyMenuAutomation.cpp y HostAcademyAutomation.cpp, la PR #197 y su auditoría Cloud. El HEAD de C-04 fue revisado en PR #197 (5b98f3a510b98b23712f1b1eea2f79445f4eeb8f) y fusionado mediante a27af56c200ebf5d8fbbaff23cb1b0cecbf56cb7. La auditoría fue **favorable con reserva expresa de validación UE**; no se equipara a certificación.

**Evidencia histórica ya existente** (no reejecutada en C-05): C-04 en CI Linux y Windows, 297/297 CTest; 142/142 ASan/UBSan; consumidores de producto Release y SDK/controlador de presentación 5/5 por SO; seis checks de la PR correctos. Los cinco checks de Actions del merge main están también en SUCCESS. Las automatizaciones de Slate **solo están escritas**, no ejecutadas sobre Unreal. El informe de C-04 conserva el detalle y los enlaces al workflow.

El cierre M1 depende de ejecutar el flujo en UE **real**, con evidencias y revisión posterior. No extrapolar los PASS nativos a UHT/UBT, render, eventos Slate, DLL dentro de UE, UWorld ni juego empaquetado.

## 2. Objetivo y límites de C-05

Cadena de éxito: **Unreal -> menú -AcademyMenu -> Nueva partida -> nombre válido -> CREATE Academy v2 -> PERSON canónica CoreRPG -> vínculo H03 confirmado -> QUERY -> SAVE H04 en ranura principal confirmado -> cierre del proceso completo -> nuevo proceso Unreal con el mismo UserDir -> Continuar -> SLOTS paginado -> elección de versión H04 exacta -> RESTORE -> QUERY -> misma campaña, PERSON, hecho de creación y nombre; nueva generación**.

La ficha debe seguir indicando **Candidato**, sin admisión, matrícula, rango, puesto, mando, nave o acceso F05/F11 concedidos implícitamente. Se debe confirmar que el gateway F05 sigue denegando las órdenes navales previstas y que no hay mutación autoritativa. El único campo de creación editable actualmente es el **nombre**. CoreRPG conserva la verdad, HOST coordina, Unreal muestra e interactúa.

No crear otras subfases, editor general, servidor, sistemas de IA/voz, progreso F10/F11, cine, planeta, academia detallada ni gameplay naval adicional. Los defectos de C-03/C-04 se corrigen con trazabilidad en **C-05**, identificando el origen y sin reescribir los contratos ya fijados.

## 3. Decisión de diseño: Academia introductoria ligera

**Decisión del usuario, registrada en C-05:** la Academia de la Flota Estelar no se desarrollará como gran entorno 3D explorable comparable a una nave. Se orientará a una **introducción/tutorial narrativo más sencillo**, previsiblemente mediante escenas **2D**, creación del protagonista y presentación de la trayectoria. La técnica final de esas escenas queda pendiente de su fase audiovisual/UX, no es requisito ni prueba de M1. Se concentra el esfuerzo de escenarios 3D complejos en la USS Enterprise NCC-1701-D modernizada, Proyecto Valhalla.

La decisión no anula los contratos ya implementados de PERSON, campañas, H03, H04, Academy v2 ni el menú Slate técnico de C-04. Tampoco equivale a aprobar una biografía libre ni altera por sí sola las reglas de Academia/F10. C-05 certifica el núcleo funcional, **no la Academia narrativa final**. Los planes externos de UI, narrativa o Valhalla se reconciliarán en sus ámbitos correspondientes; no editarlos aquí por inferencia.

## 4. Preparación y aislamiento obligatorio

1. Leer nuevamente AGENTS.md y laboratorios/README.md. Confirmar rama/commit exactos, árbol limpio y ausencia de modificaciones ajenas. No hacer reset/clean de material del usuario ni borrar laboratorios anteriores.
2. Verificar el ejecutable/instalación con Engine/Build/Build.version: **5.8.4 exacto**, arquitectura Win64 y toolchain UBT disponible. Comprobar CoreRPG limpio y fijado en **76a7b7b485616d8c4994f384a90f123bf333591d**; no actualizar el pin.
3. Usar una **copia autocontenida desde Git** del proyecto bajo laboratorios/host/h06-c05/<identificador-de-ejecucion>/, por ejemplo un archivo git archive y extracción, y UserDir distintos por caso/RHI. Conservar outputs, DDC redirigida, TEMP/TMP, builds nativas, logs, capturas y reportes allí. No introducir rutas de laboratorio como dependencia permanente.
4. Ejecutar Prepare-Host.ps1 del proyecto versionado apuntando a esa copia y a Core legítimo. Comprobar cabeceras host_abi.h y academy_abi.h, TrekHost.dll y TrekF04Bridge.dll, hashes y procedencia; inspeccionar la ABI naval 1 y extensión Academy 2. No sustituir DLL con copias desconocidas.
5. Nunca sobrescribir Content/Diagnostics/HostDiagnostic.umap ni recursos originales. El commandlet crea el mapa si no existe en la copia. Si alguna operación requiere **modificar Content principal**, parar esa operación hasta que haya snapshot verificado en otra unidad física con Backup-Content.ps1 y Verify-ContentBackup.ps1; preferir hacer toda la validación sobre copias.
6. Todo daño deliberado a slots (COMMITTED corrupto, ruta inaccesible), DLL ausente y otras inyecciones negativas se realizará **solo en copias de prueba**. Nunca usar partidas del usuario ni el UserDir real.

## 5. Orden de ejecución — puertas sin saltos

| Puerta | Ejecución en MSI | Oráculo para PASS | Evidencia exigida |
| --- | --- | --- | --- |
| **G0 — entorno** | Verificar versión motor, pin Core, fuente main/PR, directorios aislados y staging Prepare-Host | Motor **5.8.4**, pin exacto, DLL/cabeceras emparejadas, originales intactos | Build.version, SHA de repo/Core y DLL, rutas relativas del laboratorio |
| **G1 — compilación** | UHT/UBT Development Win64: StarTrekRPGEditor y StarTrekRPG; repetir Editor con -ForceUnity | Compilaciones completas sin error; sin conflicto Unity, símbolos, includes ni problemas de enlace | Logs UBT separados, exit codes y versiones toolchain |
| **G2 — mapa y carga** | Commandlet HostDiagnosticMap en copia; iniciar juego real en -nullrhi y -d3d12 | Mapa existente conservado o generado en copia; carga real de ABI 1, Academy v2 y ambas DLL; sin fallback naval para Academia | Logs de motor con mensaje de carga, hashes/staging, RHI observado |
| **G3 — puente y mundos** | Ejecutar StarTrek.H06.Academy.Seed y Resume en procesos separados por cada RHI; StarTrek.H06.DiagnosticFlow | Cambio efectivo de UWorld; no callback a mundo destruido ni segunda PERSON; sesión y diagnóstico naval sin regresión | Automation JSON por prueba, log, estado de campaña y oráculos de prueba |
| **G4 — Slate C-04** | StarTrek.H06.AcademyMenu.Seed, Resume y SaveFailure con -AcademyMenu por cada RHI, almacenamiento aislado y mismo UserDir solo entre Seed/Resume; Unavailable en copia sin TrekHost.dll | UI lógica ejecutada **en UE**: doble clic único CREATE, guardado confirmado, catálogo paginado mixto (incluidas páginas vacías), versión dañada rechazada, RESTORE exacto, error de disco explicado, ausencia de DLL sin cuelgue; estados y eventos correctos | JSON/estados Success, logs íntegros, fixtures y prueba de no mutación |
| **G5 — interacción humana** | Abrir juego con -AcademyMenu en D3D12; probar manualmente Nueva partida, ficha, Guardar, Guardar y cerrar, Continuar, selección histórica, cancelar cierre y cierre de ventana | Teclado (Tab/flechas/Intro/Escape), ratón, foco, botones, errores y estados legibles; sin «Guardado» antes de completion. Probar 1920x1080 y 2560x1600 (si soportadas) | Capturas no alteradas, notas por control, log de sesión y **aceptación expresa del usuario** |
| **G6 — Win64 producto** | Construir/ejecutar juego Win64 empaquetado (no sustituir por Editor -game), con staging oficial y -AcademyMenu; cerrar y reiniciar proceso | Misma ruta end-to-end y bibliotecas funcionales sin dependencia del Editor, del proyecto de laboratorio como artefacto final ni de tests internos | Logs UAT/empaquetado, manifiesto DLL, log del ejecutable y dos procesos distintos |
| **G7 — auditoría** | ChatGPT revisa commits, informes, discrepancias, CI y prueba real; usuario valida resultado interactivo | Cero bloqueantes de M1, regresiones justificadas, trazabilidad y evidencias reproducibles; dictamen explícito | Informe C-05 de resultados, matriz, enlaces a PR/checks y decisión final |

**Política de interrupción:** cada G debe ser PASS para avanzar a aceptación global; FAIL/BLOCKED detiene la afirmación de certificación, identifica causa y origina corrección localizada. SKIP/NOT_RUN no equivale a PASS. Si una herramienta no permite automatizar un oráculo, registrar evidencia manual independiente o dejarlo NO VALIDADO, sin fabricar resultado.

## 6. Matriz obligatoria C-03 (ocho verificaciones heredadas)

| ID | Verificación | Estado al preparar C-05 |
| --- | --- | --- |
| C03-MSI-01 | UBT StarTrekRPGEditor | **NOT_RUN** |
| C03-MSI-02 | UBT StarTrekRPG Win64 | **NOT_RUN** |
| C03-MSI-03 | Unreal real NullRHI | **NOT_RUN** |
| C03-MSI-04 | Unreal real D3D12 | **NOT_RUN** |
| C03-MSI-05 | Cambio real UWorld y observaciones de generación | **NOT_RUN** |
| C03-MSI-06 | Carga real DLL HOST y puente en UE, negociación Academy v2 | **NOT_RUN** |
| C03-MSI-07 | Crear, guardar, cerrar proceso y recuperar en UE | **NOT_RUN** |
| C03-MSI-08 | Prueba interactiva del usuario en MSI | **NOT_RUN** |

Estas ocho verificaciones no se cierran con el PASS CTest nativo ni con las pruebas sin motor del SDK. Deben registrar el motor real, resultados y log.

## 7. Matriz C-04 y cobertura de riesgos

| Identificador | Caso exigible para M1 | Estado Unreal/MSI al preparar |
| --- | --- | --- |
| UX-01/02/03/04 | Servicio/DLL ausente, nombre rechazado, doble CREATE, SAVE inicial tras QUERY | **NOT_RUN** |
| UX-05/06/07/08 | SAVE fallido o incierto, Continuar desde nuevo proceso, más de 64 versiones y página vacía con cursor, dañada no recuperable | **NOT_RUN** |
| UX-09/10/11/12 | RESTORE de versión exacta, cursor caducado, cambio UWorld/generación, SAVE→CLOSE y aviso de pérdida | **NOT_RUN** |
| UX-13/14/15 | Diagnóstico naval sin regresión, autoridad Candidate/H03/F05, teclado/ratón/foco/visual | **NOT_RUN** |
| UI-AUTO-01 | StarTrek.H06.AcademyMenu.Seed | **NOT_RUN** |
| UI-AUTO-02 | StarTrek.H06.AcademyMenu.Resume | **NOT_RUN** |
| UI-AUTO-03 | StarTrek.H06.AcademyMenu.SaveFailure | **NOT_RUN** |
| UI-AUTO-04 | StarTrek.H06.AcademyMenu.Unavailable | **NOT_RUN** |

Reutilizar las recetas C-03/C-04 documentadas y comprobar el código actual antes de ejecutarlas. **Validar tanto el código de salida como el JSON** de cada Automation: succeeded=1, failed=0, notRun=0, test correcto y estado Success. No asumir PASS si solo se abrió UE, el proceso finalizó con 0 o el test no llegó a registrarse. El caso Unavailable debe ejecutarse en copia separada; los corruptos y la obstrucción de guardado deben introducirse solo después de crear los fixtures reales en su UserDir de laboratorio.

## 8. Oráculos de continuidad e integridad de M1

Antes de cerrar el primer proceso, registrar por lectura de Core/HOST: campaign UUID completo, PERSON id, nombre, hecho de creación, revisión/checkpoint verificable, generación, candidato, número de versión y confirmación final de SAVE. Después de cerrar completamente el proceso, restaurar por catálogo/versión en otro proceso con **el mismo UserDir** y comparar:
- Campaña, PERSON, nombre y **hecho de creación**: igualdad exacta.
- Generación de HOST: nueva, no reciclada como si fuera la misma sesión.
- H03: BOUND correspondiente a esa única PERSON; sin duplicados tras reintento, reapertura, doble pulsación ni cambio de mundo.
- H04: versión elegida y procedencia correctas; restauración rechazada de archivo dañado/incompatible; sin mutación parcial ante error.
- Institucional: estado **Candidato** y acceso naval F05 denegado sin efectos laterales; F10/F11 no concedidos por UI.
- La ausencia o incompatibilidad de Academy v2 nunca puede activar OPEN naval en su lugar; los errores de cierre y SAVE incierto no se convierten en éxito.
- Las vistas de un mundo destruido no deben reaparecer como autoritativas, ni existir bloqueos prolongados/deadlock del Game Thread por el trabajador.

Si un resultado de campo no puede extraerse de la UI mínima, comprobarlo mediante proyecciones HOST, logs o prueba automatizada **del mismo proceso**, sin inspeccionar a ciegas el almacén para simular autoridad. No guardar claves ni datos privados en informes públicos.

## 9. Registro de resultados y dictamen

Codex registrará una fila por puerta, test, RHI y proceso, con **PASS / FAIL / BLOCKED / NOT_RUN**, fecha/hora, HEAD exacto, entorno, comandos reproducibles, oráculo, evidencia y defectos. Logs brutos/JSON/capturas temporales quedan dentro del laboratorio local (gitignored); el informe **permanente y versionable** en proyecto/docs/architecture/host/ resumirá resultados aprobados, hashes y referencias verificables, sin depender del laboratorio para que funcione el producto.

Cuando una incidencia exija cambios, usar rama y PR Draft trazados a C-03/C-04 dentro de C-05, con CI y retest correspondiente; no fusionar sin autorización. No ejecutar ni aprobar automáticamente un cambio peligroso de Core, S04, F11, H03/H04 o pin. En caso de que se modifique el código probado, repetir las puertas impactadas; no reutilizar éxitos de una revisión diferente como si validaran el nuevo HEAD.

**Criterio binario final:** M1 solo podrá pasar de PENDIENTE a CERTIFICADO cuando G0–G7, las ocho C03-MSI y las UX/automatizaciones aplicables tengan evidencia suficiente en UE 5.8.4, el flujo entre procesos esté probado, las negativas de autoridad e integridad se sostengan, la regresión naval esté cubierta, ChatGPT emita auditoría favorable sobre los cambios definitivos y el usuario acepte la interacción. En otro caso: **M1 NO CERTIFICADO**, con pendientes concretos.

## 10. Referencias de ejecución

- [Tablero único H06](H06_CONTROL_UNICO_ESTADO_2026-11-21.md).
- [Integración C-03 y reproducción de Seed/Resume](H06_IA03C03_INTEGRACION_UNREAL_2026-11-21.md).
- [Diseño UX-01 a UX-15](H06_IA03C04_DISENO_FUNCIONAL_MENU_ACADEMIA_2026-11-21.md).
- [Implementación C-04 y recetas Slate](H06_IA03C04_IMPLEMENTACION_MENU_ACADEMIA_2026-11-22.md).
- [Proyecto UE / reconstrucción y copias](../../../../juego/UE5/StarTrekRPG/README.md).
- [Normas del repositorio](../../../../AGENTS.md).
- [Auditoría de la PR #197](https://github.com/robdor80/Videojuego_StarTrek/pull/197) y [merge main](https://github.com/robdor80/Videojuego_StarTrek/commit/a27af56c200ebf5d8fbbaff23cb1b0cecbf56cb7).

**Siguiente puerta:** preparar al ejecutor Codex en MSI; **ninguna ejecución MSI se ha realizado al crear este protocolo**.
