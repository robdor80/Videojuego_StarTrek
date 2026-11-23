# H06 · IA-03C-05 — Auditoría independiente de cierre documental y puerta M1

**Fecha:** 22-11-2026. **Auditor:** ChatGPT. **Alcance:** PR #200, resultado técnico de C-03/C-04 en MSI, aceptación de usuario y criterios G0–G7 del protocolo C-05.
**DICTAMEN:** **AUDITORÍA DE CÓDIGO FAVORABLE CON RESERVAS DE EVIDENCIA. CIERRE DOCUMENTAL PREPARADO. M1 NO CERTIFICADO.**
**PR #200:** abierta, Draft, no fusionada. Último SHA de **código** revisado: **148dc86a91402399141ee87f9e305ba9e077e110**. La inclusión posterior de estos informes es documental y no debe confundirse con una nueva ejecución UE del HEAD documental.
**Procedencia de pruebas:** GitHub inspeccionado directamente; resultados de logs MSI comunicados por Codex; interacción manual narrada por el usuario y acompañada de capturas en la conversación.

## 1. Dictamen ejecutivo

El objetivo técnico de C-05 —comprobar que el mínimo integrado UE 5.8.4 / HOST / CoreRPG crea y recupera una candidatura sin saltarse la autoridad— muestra **resultado favorable en las pruebas realizadas**. Los problemas detectados durante la validación se corrigieron de forma localizada en PR #200:

1. Cabecera Slate inexistente y C4458 impidieron UBT al comenzar; corregidos y compilación Editor/Game PASS en MSI.
2. Tres FAIL de Automation por lectura inmediata de atributos Slate sin prepass/sin separar selección; tras corrección 6/6 pruebas dirigidas PASS según Codex, sin suavizar las aserciones de identidad y versiones dañadas.
3. ESC perdía eficacia cuando el foco pasaba al viewport: se añadió un preprocesador de entrada con alcance limitado al viewport de Academia y control de ciclo de vida. El usuario volvió a probar ambos fallos originales y las rutas de catálogo/confirmación: PASS.

La PR #200 contiene **7 archivos de código** en la revisión auditada. El código permanece sin cambios en CoreRPG, contratos del HOST, SDK nativo, H03/H04, F05/F11, pin o assets de Unreal.

**Valoración de integración:** apta para revisión de fusión del alcance corregido **si el usuario la autoriza**. **No equivale a certificación M1**, pues la evidencia bruta local no fue accesible a ChatGPT y hay reservas de cobertura detalladas a continuación. El informe compañero registra resultados y procedencia [Resultados C-05](H06_IA03C05_RESULTADOS_M1_2026-11-22.md).

## 2. Fuentes efectivamente contrastadas

- Repositorio, base main y commit revisado; cambios de la PR: https://github.com/robdor80/Videojuego_StarTrek/pull/200
- Comprobaciones GitHub Actions del commit de código **148dc86a**: https://github.com/robdor80/Videojuego_StarTrek/actions/runs/45077407568
- **SUCCESS 5/5**: Linux nativo, Linux Clang ASan/UBSan, Windows nativo, producto Linux y producto Windows; verificado directamente el 22-11-2026 mediante el recurso GitHub de check-runs.
- Fuentes nuevas/modificadas en la PR: HostSlateAutomation.h; SHostAcademyMenu.h/.cpp; HostAcademyMenuAutomation.cpp; HostAcademyNavigationAutomation.cpp; HostDiagnosticGameMode.h/.cpp.
- Protocolo y cierre binario: [H06 IA-03C-05 Protocolo](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md).
- Informes históricos de C-03 y C-04; tablero único H06; AGENTS.md.
- Informes locales de Codex comunicados por el usuario (R0, R1, R2, Escape/R3) y capturas/confirmaciones manuales del usuario de la misma conversación.

**No verificado de forma independiente por ChatGPT:** contenido literal de los informes locales del MSI, command lines ejecutadas, JSON de Automation, logs UBT/Unreal, manifiestos y hashes de DLL/saves. No se deducen cifras de CI UE a partir de los 5 checks de GH (CI nativa); el 9/9 de automatizaciones UE proviene de Codex.

## 3. Revisión de diseño y código (7 archivos)

| Hallazgo | Evaluación | Razón |
| --- | --- | --- |
| A-01. Include de FChildren | **RESUELTO** | Sustitución de Widgets/Children.h por Layout/Children.h; compilación UBT confirmada por Codex |
| A-02. Ocultación de SWidget::Tag | **RESUELTO** | Parámetro de Button renombrado WidgetTag, sin alterar .Tag ni acciones |
| A-03. Caché de atributos Slate | **RESUELTO EN PRUEBA / RETEST PASS REPORTADO** | Prepass antes de IsEnabled, paso separado para seleccionar v1 y diagnósticos específicos. Rechazo de v2/v66 y CanRestore conservados |
| A-04. Escape tras pérdida de foco | **RESUELTO EN PRUEBA Y VALIDADO POR USUARIO** | SHostAcademyMenu reutiliza HandleEscape; un IInputProcessor solo atiende ESC sin modificadores cuando el foco coincide con SViewport del juego de Academia. Se registra al mostrar menú y desregistra en EndPlay. No maneja otras teclas ni intercepta en otros focos |
| A-05. Riesgo de autoridad/cambio de Core | **SIN CAMBIOS NUEVOS DETECTADOS** | Diff de la PR solo contiene menú, GameMode y Automation; ausencia de cambios Core, ABI, persistencia y permisos. Oráculos de permiso siguen siendo requisitos del sistema |
| A-06. Interacción empaquetada | **FAVORABLE** | Uso de ejecutable Win64 real comunicado y comprobación humana de flujo principal con UserDir aislado. Aceptación manual no sustituye una comprobación criptográfica de integridad del paquete |
| A-07. Discrepancia salida proceso/Automation | **RESUELTA EN INFORMES** | Tres fallos iniciales con exit code 0 se trataron correctamente como FAIL en JSON, y solo se cerraron tras posteriores Success reportados |

No se han encontrado incompatibilidades contractuales nuevas en el alcance del diff. **Riesgos residuales:** el preprocesador de teclado depende de que el viewport sea el widget enfocado; este comportamiento específico fue reproducido manualmente y cubierto por nueva automatización. Si otras futuras ventanas o capas Slate introducen focos adicionales, corresponderá evaluarlos en su propia fase, no anticipar rediseños aquí.

## 4. Matriz de evidencias y estado de certificación

| Criterio M1 | Dictamen actual | Condición para cierre sin reservas |
| --- | --- | --- |
| G0 versión UE 5.8.4, pin Core, aislamiento | **PASS REPORTADO** | Consolidar metadata y hashes del laboratorio local |
| G1 UBT Editor, Game y Unity real | **PASS EN RONDAS DIFERENTES** | Editor/Game en R3; Unity real probada R2. Para atribuir Unity al último código del input processor y nueva Automation, se necesita log de compilación Unity real de R3 o decisión documentada de suficiencia por alcance |
| G2 carga ABI/DLL y ambos RHI | **PASS REPORTADO** | Adjuntar digest/resumen reproducible de logs de carga |
| G3 Seed/Resume, UWorld, identidad, negativa naval | **PASS REPORTADO** | Revisar matriz individual, generaciones, F05 sin mutación, procedencia y logs/JSON del MSI |
| G4 Automation AcademyMenu y negativos | **PASS RETEST REPORTADO** | La cifra 9/9 es de la última ronda; para auditoría reproducible indicar nombres, RHI, SHA y resultado JSON de cada caso |
| G5 usuario/interfaz | **ACEPTACIÓN FUNCIONAL FAVORABLE** | Guardar acta de resolución/legibilidad específica en ambos tamaños si se exige literalidad del G5. La X es no comprobable en paquete sin barra; Alt+F4 y Salir sí comprobados |
| G6 Win64 producto y reinicio | **PASS REPORTADO + VALIDADO VISUALMENTE** | Referencia verificable a manifiesto de empaquetado, DLL y mismo UserDir en los dos procesos |
| G7 dictamen y gobierno | **AUDITADO CON RESERVAS, NO CERTIFICADO** | Cerrar reservas materiales y fusionar solo con permiso del usuario; verificar el árbol definitivo |

### Inventario explícito de reservas

**R-01 — Disponibilidad de evidencia bruta MSI. Severidad: documental, potencialmente bloqueante de certificación.**
Los informes de Codex y la aceptación manual son consistentes, pero no se han abierto directamente los logs/JSON originales de las carpetas locales. Antes de firmar M1 CERTIFICADO, incorporar un **manifiesto de evidencia** con nombres de prueba, SHA, RHI, succeeded/failed/notRun/state, comandos de ejecución relevantes, hashes SHA-256 de logs/JSON, metadatos UE/Core y rutas relativas de los laboratorios. Un manifiesto aprobado se puede guardar como texto bajo proyecto/docs/architecture/host/; no se versionarán logs ni datos de juego de los laboratorios. Nunca inventar un hash o un PASS.

**R-02 — Fuerza Unity y matriz completa en la revisión final. Severidad: cobertura de revisión.**
La Unity real se probó con 920701dd; luego se añadieron cambios C++ de Escape y el nuevo HostAcademyNavigationAutomation.cpp en 148dc86a. Codex informa Editor/Game compilados y 9/9 automatizaciones finales, pero **no consta explícitamente Unity real ejecutada en 148dc86a**, ni lista nominal de los 9 casos. Para certificar literalmente G1/G4 en SHA final, pedir únicamente la evidencia precisa que falte; no repetir todo sin motivo.

**R-03 — Presentación en dos resoluciones y cierre X. Severidad: aceptación UX no bloqueante del flujo principal, pero pendiente de caracterización.**
Codex midió 1920×1080 y 2560×1600 efectivas; sus capturas no incluían capa Slate. La conversación conserva capturas de interfaz y confirmación de legibilidad/control funcional, pero no identifica capturas manuales verificadas por separado a ambas resoluciones. El paquete observado no tenía barra de título, por lo que la X fue **NOT_RUN**; Alt+F4 y botón Salir fueron PASS. Se puede documentar X como **NO APLICA a modo sin bordes** si ese modo es configuración de producto acordada, o verificar un paquete en ventana con marco antes de cerrar G5 literal; no afirmar X PASS.

**R-04 — Datos autoritativos previos y posteriores a restaurar. Severidad: documental.**
La UI mostró el mismo nombre/campaña y PERSON 2, hecho 3, revisión 171, tick 0 tras recuperar v1; faltó una captura del valor numérico anterior. Las automatizaciones de Seed/Resume reportadas verifican igualdad real, nueva generación y negativa naval. El acta final debe identificar los resultados de esas aserciones desde JSON/logs, no deducirlos exclusivamente del texto del menú.

**R-05 — Fusión y estado definitivo. Severidad: de gobierno; bloqueante para FUSIONADO.**
La PR #200 está abierta y no fusionada. El usuario autorizó **auditoría y documentación**, no una fusión expresa en esta intervención. Conservar branch y proteger main; la certificación final exige que el código auditado sea efectivamente el integrado, con verificación postfusión cuando proceda.

## 5. Qué está cerrado y qué no

**Cerrado en esta intervención:**
- Auditoría de código de PR #200 sobre 148dc86a, sin hallazgos bloqueantes nuevos en su diff.
- Consolidación documental cronológica y matriz de pruebas MSI comunicadas.
- Registro de los 22 pasos de aceptación, corrección del fallo ESC y persistencia entre procesos.
- Contraste directo de GitHub Actions **5/5 SUCCESS** del último código.
- Registro honesto de limitaciones de lectura de evidencia local, Unity en revisión final y presentación por resolución.
- Coherencia con decisión de Academia como tutorial narrativo ligero: su producción audiovisual definitiva no forma parte de M1.

**NO cerrado / NO afirmar:**
- Que las 22 pruebas equivalgan a 22 JSON de Automation.
- Que 9/9 finales equivalgan a la ejecución completa de 17/17 en último SHA.
- Que exista un PASS manual del control X, dado que no estaba presente.
- Que los valores Core anteriores y posteriores se compararon manualmente campo a campo sin un informe nativo.
- Que el contenido de logs del MSI fue auditado directamente desde este entorno.
- Que la PR #200 ya está en main, o que **M1 está CERTIFICADO**.

## 6. Recomendación ejecutiva, orden mínimo sin nuevo desarrollo

1. **No programar más funcionalidades.** Los fallos funcionales conocidos en el alcance probado están corregidos.
2. Completar una **consolidación de evidencia** por Codex MSI de los informes y JSON ya existentes (sin repetir pruebas por defecto), e identificar si falta realmente una Unity efectiva en el último SHA. Si falta y es requisito de cierre, ejecutar solo esa compilación aislada.
3. Resolver administrativamente R-03: declarar la X no aplicable para el modo probado o solicitar una comprobación en modo ventana con borde; asociar visual a ambas resoluciones si se pretende certificación estricta del diseño.
4. ChatGPT verifica el manifiesto, dictamina el cierre de R-01…R-04, y solicita permiso explícito para fusionar la **PR #200**; comprobar HEAD y checks antes de fusionar.
5. Con PR fusionada, comprobar CI/main y emitir acta binaria **CERTIFICADO / NO CERTIFICADO**, con las evidencias finales y versión.

**Resultado de auditoría:** **FAVORABLE PARA EL CÓDIGO CORREGIDO; CON RESERVAS PARA LA CERTIFICACIÓN.** La subfase C-05 se encuentra **DOCUMENTADA Y AUDITADA; PENDIENTE DE CIERRE DE RESERVAS Y FUSIÓN**. M1 sigue **NO CERTIFICADO** hasta un acto posterior sustentado.

## 7. Enlaces

- [Resultados consolidados C-05](H06_IA03C05_RESULTADOS_M1_2026-11-22.md).
- [Protocolo y criterio binario M1](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md).
- [Tablero de H06](H06_CONTROL_UNICO_ESTADO_2026-11-21.md).
- [PR #200](https://github.com/robdor80/Videojuego_StarTrek/pull/200).
- [CI 5/5](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/45077407568).
