# H06 · IA-03C-05 — Encargo técnico listo para Codex en MSI

**PREPARADO, NO ENVIADO NI EJECUTADO.** Entregar este encargo a Codex **cuando el usuario tenga disponible el MSI** y haya integrado o decidido cómo consumir la PR documental C-05. **Modelo recomendado: GPT-6. Nivel de razonamiento: ALTO.**

## Contexto y autoridad

Trabajas en el videojuego privado **Star Trek Legends**, repositorio **robdor80/Videojuego_StarTrek**. Estamos **EN C-05 de H06/IA-03C**, no en una fase nueva. UE **5.8.4**, proyecto **juego/UE5/StarTrekRPG/StarTrekRPG.uproject**, HOST local como coordinador y CoreRPG como autoridad. C-01/02/03/04 están fusionadas; PR #197 fusionada sobre main en **a27af56c200ebf5d8fbbaff23cb1b0cecbf56cb7**, con auditoría favorable solo en Cloud.

M1 **NO CERTIFICADO**. Las ocho verificaciones de C-03 y las pruebas de Slate/interacción de C-04 constan **NOT_RUN en MSI**, incluso si las pruebas nativas Linux/Windows y los checks CI fueron PASS. La Academia será **intro/tutorial narrativo ligero, probablemente con escenas 2D**, no un campus 3D completo. Esto **NO** cambia el núcleo del candidato ni introduce trabajo gráfico en C-05.

Lee primero, en main o en la rama documental C-05 ya integrada:
- AGENTS.md y laboratorios/README.md.
- proyecto/docs/architecture/host/H06_CONTROL_UNICO_ESTADO_2026-11-21.md.
- proyecto/docs/architecture/host/H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md (**contrato principal de este encargo**).
- proyecto/docs/architecture/host/H06_IA03C03_INTEGRACION_UNREAL_2026-11-21.md.
- proyecto/docs/architecture/host/H06_IA03C04_DISENO_FUNCIONAL_MENU_ACADEMIA_2026-11-21.md.
- proyecto/docs/architecture/host/H06_IA03C04_IMPLEMENTACION_MENU_ACADEMIA_2026-11-22.md.
- juego/UE5/StarTrekRPG/README.md.
- Las fuentes reales de HostAcademyMenuAutomation.cpp, HostAcademyAutomation.cpp, HostSessionSubsystem y HostRuntime. La fuente efectiva prevalece sobre los comandos de un informe antiguo.

## Encargo: trabajar POR PUERTAS

**G0 — Diagnóstico sin cambios.** Confirma git status limpio y HEAD, versión REAL de UE 5.8.4 desde Build.version, toolchain Win64, CoreRPG checkout limpio en pin 76a7b7b485616d8c4994f384a90f123bf333591d, integridad de fuentes y scripts. No actualices Core ni el pin. Prepara copia versionada del proyecto y almacenes de prueba exclusivamente bajo laboratorios/host/h06-c05/<identificador>/ (sin modificar ni borrar laboratorios anteriores). Redirige TEMP, DDC, logs y artefactos de prueba al laboratorio si la herramienta lo permite. Ante cualquier salida impuesta del motor fuera de estas rutas, registra la excepción; no dejes artefactos de proyecto finales allí.

**G1 — Compilaciones.** Desde la copia aislada ejecuta Prepare-Host.ps1 con el Core correcto y comprueba hashes/cabeceras/exports. Compila por UHT/UBT **StarTrekRPGEditor Win64 Development** y **StarTrekRPG Win64 Development**; repite el primero con **-ForceUnity**. Conserva cada log y salida. Si falla, documenta error exacto, corrige únicamente el componente responsable en una rama/PR Draft, y repite las pruebas afectadas antes de continuar.

**G2 — Entorno UE y DLL.** Regenera únicamente en la copia el mapa de diagnóstico mediante HostDiagnosticMap si falta, sin sobrescribir mapas reales. Inicia UE en **-nullrhi** y **-d3d12**, documenta RHI efectivo y confirma mediante log la carga real de TrekHost.dll, TrekF04Bridge.dll, ABI naval 1 y Academy v2. No confundir staging o CTest de SDK con carga efectiva dentro del motor.

**G3 — Puente, cambio de UWorld y naval.** Ejecuta en procesos UE distintos y UserDir específicos los tests **StarTrek.H06.Academy.Seed**, **StarTrek.H06.Academy.Resume** y **StarTrek.H06.DiagnosticFlow** siguiendo el protocolo C-03. Verifica viajes entre mundos, retención de observaciones, generaciones, carga/guardado y ausencia de regresión v1. No reutilices datos de producción.

**G4 — Slate Academy.** Ejecuta **StarTrek.H06.AcademyMenu.Seed**, **.Resume**, **.SaveFailure**, **.Unavailable**, con **-AcademyMenu**. Ejecuta Seed/Resume en procesos separados por RHI pero con el mismo UserDir de prueba de su par. Conserva los tests para **NullRHI y D3D12** donde aplique; Unavailable en otra copia del proyecto con DLL HOST apartada, nunca en la original. Prueba más de 64 versiones, página vacía con cursor, campaña naval mezclada, versiones corruptas, doble CREATE, SAVE fallido, cierre, error y cursor caducado. El test Unavailable se efectúa en copia aparte con el export/DLL retirado. Los fixtures corruptos y el bloqueo de escritura se introducen exclusivamente en rutas descartables bajo laboratorios.

**No basta con exit code 0**: comprueba por cada Automation el JSON, que coincida el test esperado y succeeded=1, failed=0, notRun=0 y state=Success. Un PASS de C++ nativo no suple la interacción Slate en motor. Se conservarán resultados por prueba y proceso.

**G5 — Inspección manual y aceptación del usuario.** Abre el menú Academy real en D3D12; reproduce el flujo completo Nueva partida -> nombre -> candidato -> guardado -> cerrar todo el proceso -> relanzar -> Continuar -> seleccionar versión histórica exacta -> restaurar -> ficha. Comprueba por proyección HOST los mismos campaign UUID, PERSON, nombre y hecho de creación; generación nueva; estado Candidato y denegación F05 sin mutaciones. Revisa teclado (Tab, flechas, Intro, Escape), ratón, foco, mensajes, estados no confirmados, cierre por botón y ventana, errores y presentación en **1920×1080 y 2560×1600** cuando las pantallas lo permitan. **Solicita explícitamente la aceptación personal del usuario** y deja el estado PENDIENTE mientras no se produzca. No la suplas con tu opinión.

**G6 — Juego empaquetado.** Construye **Win64 empaquetado** mediante las herramientas oficiales del proyecto/Unreal en copia aislada; verifica staging DLL y ejecuta **el .exe real**, no solo UnrealEditor -game. Repite al menos el camino feliz entre procesos con -AcademyMenu, registrando logs y continuidad. Si el empaquetado está bloqueado por una dependencia del proyecto no esencial de M1, explica por qué y mantén G6 BLOCKED/NOT_RUN hasta decisión documentada; no digas PASS.

**G7 — Informe verificable y entrega.** Incluye cada puerta G0–G6 y los **8 C03-MSI** y **UX-01..UX-15**, indicando **PASS/FAIL/BLOCKED/NOT_RUN**, oráculo y evidencia real; especifica commit y configuración. Adjunta rutas de logs brutos en laboratorio, evidencias resumidas reproducibles, hashes, versión real UE y comandos. Prepara documento permanente **proyecto/docs/architecture/host/H06_IA03C05_RESULTADOS_M1_2026-11-22.md** (o fechado en el día efectivo) y actualiza el tablero H06 con hechos comprobados, sin declarar M1 certificado. Abre una **PR Draft** de evidencia y, en su caso, correcciones, para auditoría de ChatGPT; **no fusiones**.

## Límites no negociables

- No crear nuevo repositorio ni nuevo proyecto principal UE, no reescribir Academy, no añadir servidores, gráficas definitivas, tutorial 2D o funcionalidades extra.
- No modificar F10/F11, CoreRPG, su pin, reglas institucionales ni pruebas históricas/LOCKED para hacer pasar los tests. **CoreRPG es fuente de verdad**.
- Sin credenciales F05 por crear candidatura. SAVE debe constar confirmado antes de anunciarlo; RESTORE debe seleccionar versión H04 exacta. No crear PERSON duplicadas por doble clic o tras UWorld.
- Los .uasset/.umap de la obra no están en Git: protege originales, no sobrescribas Content. Si excepcionalmente es necesaria una modificación real, verificar antes snapshot de Content en otra unidad física según README y pedir autorización para ampliar alcance si fuese necesario.
- Ningún archivo de laboratorio se confirma ni se publica en Git; no dejar dependencias permanentes apuntando a él. No eliminar archivos/laboratorios previos.
- Cada corrección técnica relevante debe justificar qué fallo observado resuelve, su nueva prueba y el impacto sobre contratos antiguos. La PR se mantiene Draft; el usuario autoriza las fusiones.
- Una incidencia pendiente, una automatización que no llega a correr o una compilación sin log es **NOT_RUN/BLOCKED/FAIL**, nunca PASS.
- No certifiques M1 por tu cuenta: entregar evidencia para auditoría ChatGPT y aceptación del usuario.

## Formato de respuesta que espero de Codex

Indica **HEAD y rama**, entorno UE/Core y pin; resultados de G0–G6 y de las ocho C-03; automations C-04 + UX; incidencias y correcciones (con SHA); directorio de laboratorio, logs e informe; enlace a **PR Draft**; estado exacto **M1 NO CERTIFICADO** salvo decisión final posterior. Separar IMPLEMENTADO, PROBADO EN UE, AUDITADO, FUSIONADO y CERTIFICADO.

**No iniciar ninguna ejecución de este encargo hasta que el usuario lo entregue expresamente a Codex en MSI.**
