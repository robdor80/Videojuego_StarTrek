# H06 / IA-03C-05 — Acta de certificación del hito M1 con alcance delimitado

**Fecha:** 23-11-2026 (Europe/Madrid).
**Decisión:** **M1 CERTIFICADO EN ALCANCE LIMITADO — MENÚ DE ACADEMIA EN PANTALLA COMPLETA**.
**C-05:** **IMPLEMENTADA, PROBADA, AUDITADA, FUSIONADA y CERRADA** en este alcance.
**Aceptación:** usuario, expresamente aprobada en conversación el 23-11-2026 tras comparación de capturas y descubrimiento de una incidencia real del modo ventana a 2560×1600.
**No certificado:** presentación del menú Slate en **modo ventana a 2560×1600**, ni interfaz definitiva, narrativa, academia 3D, orden naval desde UE, resto del HOST H07–H13 ni videojuego completo.

> Esta acta es la decisión de cierre **posterior** al protocolo del 22-11-2026, a la auditoría preliminar y a la PR #200. Los documentos anteriores conservan su condición de registros históricos en la fecha en que se redactaron: sus menciones «M1 NO CERTIFICADO» no sustituyen el presente dictamen. No se alteran sus resultados históricos.

## 1. Identificación de lo que se certifica

- **Código Unreal/HOST auditado:** `148dc86a91402399141ee87f9e305ba9e077e110`.
- **PR #200:** https://github.com/robdor80/Videojuego_StarTrek/pull/200; **fusionada**.
- **Commit de fusión en main:** `9ab15007ee3cdeb8bf1453069ec327b0012d0a22`; commits posteriores al código probado en la PR solo documentales.
- **CI del último HEAD de la PR:** 6/6 SUCCESS, incluido contrato estático; CI posfusión main: 5/5 SUCCESS, https://github.com/robdor80/Videojuego_StarTrek/actions/runs/45080312560.
- **Motor:** Unreal Engine **5.8.4** (CL 58902052); Win64, NullRHI y D3D12 según los casos.
- **Pin CoreRPG:** `76a7b7b485616d8c4994f384a90f123bf333591d`.
- **Naturaleza:** HOST mínimo real de Academia que coordina **crear persona candidata, vincular identidad H03, consultar, guardar H04, cerrar completamente, relanzar y recuperar versión exacta**, sin atribuir graduación ni permisos institucionales. CoreRPG conserva la autoridad. No es certificado de sistema institucional F11.

## 2. Evidencia recibida y contraste

El usuario aportó en conversación estos tres documentos producidos en el MSI por Codex:
- `manifiesto-provisional.json`, **SHA-256 9fe1b4f30f7804158005e327fb22e17ecbfebe555779054938621ac964942b00**.
- `INFORME_PROVISIONAL_M1.md`, **SHA-256 6ec8223734d52964b6a32078b80bc6294a8bbd9af19891d517136bf231895902**.
- `verificacion-entrega.json`, cuyo control declara coincidencia de ambos hashes y 311 evidencias comprobadas en el MSI.

ChatGPT pudo **abrir y revisar directamente los tres adjuntos** y contrastar sus dos hashes SHA-256. El manifiesto indexa 34 JSON de Unreal Automation: 29 PASS y 5 FAIL históricos pertenecientes a revisiones previas a las correcciones. Las **9 ejecuciones de la última revisión de código** constan como `succeeded=1, failed=0, notRun=0, state=Success`; esos datos y sus referencias están en el manifiesto. Codex informó de la verificación local de 311 hashes de evidencias; ChatGPT **no abrió ni rehashó cada archivo bruto local de laboratorio**.

**ForceUnity efectiva:** el informe y manifiesto describen una compilación real en copia aislada con fuentes C++ y cabeceras idénticas a `148dc86a`: 10 ficheros `.cpp` en `Module.StarTrekRPG.cpp`, enlaces de `UnrealEditor-StarTrekRPG.lib/.dll` y salida 0. Los cambios de las reglas de Unity fueron **solo del entorno de prueba desechable**, no de producto.

**Autoridad / continuidad:** los casos `AcademyMenu.Resume` en NullRHI y D3D12 comparan campaña, PERSON=2, hecho de creación=3, revisión=172, tick y huella; el circuito C-03 y el producto empaquetado acreditan pares Seed/Resume en procesos distintos y UserDir compartido. El test nativo `host.academy.persistence_process` acredita nueva generación entre procesos y vínculo H03; `host.academy.abi_faults` acredita denegaciones F05 sin mutaciones. Las órdenes F05 **no fueron emitidas explícitamente desde UE en el último ensayo**, y no se afirma lo contrario.

**Aceptación funcional previa:** el usuario validó creación/guardado/continuación, restauración histórica y cierre, navegación con teclado, Escape aun tras pérdida de foco y Alt+F4; el paquete ejecutado carecía de barra de título y no ofrecía botón X. La interfaz técnica Slate no es la interfaz artística final.

## 3. Prueba visual G5 y defecto detectado

Pruebas manuales realizadas con dos copias del lanzador PowerShell de ensayo (`-AcademyMenu -d3d12 -windowed -ForceRes`) en el MSI, sin cambiar el código ni los guardados; las capturas fueron **compartidas en la conversación** y examinadas por ChatGPT:

| Situación observada | Resultado |
| --- | --- |
| **1920×1080 solicitados, modo ventana** | **PASS visual**: menú principal dentro del área disponible, título y tres botones legibles, sin recortes aparentes. Captura de usuario. |
| **2560×1600 solicitados, modo ventana**, con pantalla Windows 2560×1600 y escala 150 % | **FAIL visual real**: panel desplazado a la derecha, mayor escala y borde derecho fuera de la imagen; **no se descarta ni se oculta**. Captura de usuario. |
| **2560×1600, tras pulsar Alt+Intro** y alternar el modo de presentación a pantalla completa | **PASS visual**: panel principal centrado, título y controles completos, sin recorte o solapamiento aparente. Captura de usuario. |
| **2560×1600 tras Alt+Intro, pantalla «Continuar»** | **PASS visual**: versiones de partida listadas y botones inferiores visibles, alineados y legibles. Captura de usuario. |

**Precisión de evidencia:** las dimensiones de ejecución provienen de argumentos del lanzador y resoluciones efectivas comunicadas en logs de pruebas, **no del tamaño de imagen mostrado por la interfaz de chat**. Las capturas acreditan disposición y legibilidad. No hay medición independiente de píxeles físicos de la superficie Unreal ni revalidación exhaustiva de todas las subpantallas a ambas resoluciones. El modo de pantalla completa mostrado tras Alt+Intro ha sido aceptado explícitamente por el usuario para M1.

**Incidencia abierta `M1-UX-WINDOWED-2560`:** reproducir y corregir **desalineación/escalado de Slate en modo ventana 2560×1600 a escala Windows 150 %**. Indicio de relación con gestión del viewport/escalado al lanzar `-windowed`; **causa raíz sin demostrar**, no asumir que la anchura fija de Slate sea la causa. Esta incidencia **no pertenece al alcance certificado**; requiere diagnóstico específico posterior sin reabrir las pruebas de integridad ya superadas. No certificar dicho modo hasta solución y retest. No generar una nueva subfase C-06 por inercia.

## 4. Puertas de aceptación M1 — alcance certificado

| Puerta | Decisión |
| --- | --- |
| **G0 — motor, Core, copias** | **PASS documentado**: motor/pin/staging/aislamiento acreditados por Codex y manifiesto. |
| **G1 — UBT Editor/Game/ForceUnity** | **PASS documentado**: compilaciones, incluida Unity real del código final en copia aislada de fuentes idénticas. |
| **G2 — mapa, ABI/DLL, RHI** | **PASS documentado**: inicialización del HOST Academy v2 y ambos RHI reales. |
| **G3 — ciclo Academy, UWorld, identidad y naval** | **PASS en cobertura combinada**: pruebas UE C-03 y regresiones nativas del último código, sin atribuir a UE una comparación numérica entre procesos que no se ejecutó allí. |
| **G4 — menú, errores y recuperación** | **PASS en cobertura combinada**: últimas 9/9 UE PASS, rondas anteriores pertinentes y fallos históricos reparados. |
| **G5 — aceptación humana y presentación** | **PASS LIMITADO por aceptación expresa del usuario**: 1920×1080 ventana y 2560×1600 tras Alt+Intro/pantalla completa. **FAIL excluido**: ventana 2560×1600. |
| **G6 — ejecutable Win64 real** | **PASS documentado/validado**: empaquetado, proceso nuevo con mismo UserDir, persistencia y restauración. |
| **G7 — auditoría y decisión** | **FAVORABLE CON LIMITACIÓN EXPRESA**: PR fusionada y CI verificada; usuario autorizó el cierre M1 **con este alcance reducido**. |

El protocolo previo pedía comprobar 2560×1600 en el modo ensayado: **no se convierte el FAIL en PASS**. La aceptación posterior del usuario constituye una **delimitación explícita del alcance certificado**; no una certificación completa de todos los modos de ventana. La negativa de F05 en UE y la inyección de SAVE incierto en Slate no se probaron explícitamente; los requisitos autoritativos mínimos correspondientes se apoyan en las pruebas nativas y en el camino UE, con esos límites trazados. La verificación visual detallada de todas las vistas a ambas resoluciones tampoco se afirma realizada.

## 5. Dictamen formal y continuación

**DICTAMEN FINAL BINARIO PARA EL ALCANCE APROBADO: M1 — CERTIFICADO (LIMITADO).**

Se cierra **C-05** como subfase ejecutada y auditada. Queda aceptado el primer HOST mínimo integrado con UE 5.8.4/CoreRPG para el circuito Academy y su interfaz técnica **en pantalla completa**, con la excepción `M1-UX-WINDOWED-2560` registrada. Esta certificación **no** es garantía de compatibilidad visual universal ni certificación de la totalidad del HOST.

**Próximo trabajo del Plan Maestro: H07**, pasarela de identidad/acceso HOST↔F11 sin emisor institucional propio; no iniciar implementación de nuevos permisos o reglas antes de examinar la API real aprobada de F11. El defecto visual queda como deuda técnica a abordar cuando convenga, sin bloquear la continuidad del proyecto.

**Referencias internas:** [Protocolo original](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md) · [Resultados históricos](H06_IA03C05_RESULTADOS_M1_2026-11-22.md) · [Auditoría previa](H06_IA03C05_AUDITORIA_CIERRE_2026-11-22.md) · [Tablero H06](H06_CONTROL_UNICO_ESTADO_2026-11-21.md) · [PR #200](https://github.com/robdor80/Videojuego_StarTrek/pull/200).
