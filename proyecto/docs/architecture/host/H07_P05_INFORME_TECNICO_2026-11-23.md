# H07-P05 y corrección H06 — Informe técnico para auditoría

**PR:** [#205](https://github.com/robdor80/Videojuego_StarTrek/pull/205), abierta y sin fusionar, sobre `feat/host-h07-p03` (#204). #203 y #204 permanecen abiertas. **Rama:** `feat/host-h07-p05-ue-h06-windowed`. **Código verificado:** `2e75db5998151719f47933904a8729d9916cbde7`; integración H07 en `61d03ce760eadb7e1db4b58061ee2a3f16960e02` y corrección H06 en el commit siguiente. Los commits posteriores añaden evidencia/documentación y guardas de trazabilidad. El HEAD final y sus Actions se contrastan en la PR; este documento no puede incluir su propio hash Git.

**Estado:** implementación y validación técnica para auditoría independiente. H07 **NO CERTIFICADA**. La aceptación visual y funcional final pertenece al usuario y ChatGPT. Sin emisor institucional de producto F11, el alcance posible sigue limitado a **consulta y denegación**.

## Entorno y protección

El equipo de ejecución fue el MSI Raider GE78 HX 14VGG, FATIROBERMSI, Windows 11, RTX 4070 Laptop y 32 GB. Se leyó la instalación real `C:/Program Files/Epic Games/UE_5.8/Engine/Build/Build.version`: **5.8.4**, CL **58902052**. El checkout CoreRPG estaba limpio en `76a7b7b485616d8c4994f384a90f123bf333591d` y se conserva ese pin.

Se trabajó en un worktree aislado bajo la raíz autorizada, dentro de `laboratorios/host/h07-p05-20261123/work`; compilaciones, registros, capturas, proyectos de ensayo y UserDir quedaron en ese laboratorio. Los ensayos de persistencia H07 usaron además una raíz corta `laboratorios/h7p05r3`, para que la copia de archivos realizada por std::filesystem en la prueba de importación no excediera MAX_PATH. Ningún binario de producto depende de estas rutas. No se borraron laboratorios, no se tocaron guardados personales ni recursos Unreal originales, y no se modificó main.

El árbol principal ya tenía una modificación local del `.uproject` y archivos de solución del usuario. Se preservaron. El staging de DLL/cabeceras se realizó mediante el `Build/Prepare-Host.ps1` del worktree, dirigido a su proyecto aislado. No se copiaron DLL de ensayo al producto.

## Implementación H07

La extensión C de lectura institucional v1 es aditiva y reutiliza el cliente HOST H05 y su cola propietaria. No expone F04Session, selección de observador, vínculo arbitrario ni capacidades administrativas. El HOST resuelve identidad, procedencia y ámbito antes de usar `InstitutionalQueries` de P03. Se conservan ABI naval v1 y Academy v2.

Unreal negocia versión y exports, genera correlaciones, sondea sin esperar al worker y presenta solo la proyección autorizada. El getter comprueba vigencia inmediatamente antes de devolver hechos. SAVE/RESTORE/CLOSE y retirada del UWorld borran resultados y tickets, incluidas respuestas tardías. No se añade expediente paralelo, emisor, presented_at ni mutación Core. La vista técnica se reutiliza en diagnóstico y candidatura Academy.

El consumidor C reveló un defecto previo de H04 con raíces Windows expresadas usando `/`: se construía una ruta extendida Win32 antes de normalizar separadores. `make_preferred()` corrige ese caso sin relajar restricciones de volumen local, ruta absoluta y enlaces. [Contrato de integración](H07_P05_CONTRATO_UNREAL_v1_2026-11-23.md).

## Pruebas institucionales realmente ejecutadas

Los hechos positivos procedieron de `f11.process_save` en **otro proceso F11 aislado**, y se cargaron mediante el acceso de prueba P03 para crear un guardado H04 con vínculo persistido. Unreal restaura una copia de ese guardado por la ABI de producto; no contiene bootstrap de oficiales. La composición de producto conserva `TREK_HOST_TESTS=OFF` y excluye F11_NATIVE_TEST_HOST, f11_commit_promotion y TrekF11TrialHost.

| Escenario | Evidencia actual |
|---|---|
| Expediente propio autorizado | P03 canonical, consumidor C y UE NullRHI/D3D12: PASS |
| Ascenso propio confirmado | P03 compara con F11; C y UE conservan evento/revisión original: PASS |
| Cadete sin comisión | P03 y UE: SERVICE_UNAVAILABLE, vista vacía, sin rango: PASS |
| Persona legacy sin expediente F11 | P03 capability/uncommissioned: DOMAIN_REJECTED sin datos: PASS |
| Evento ajeno | P03 foreign, persona comisionada distinta: ACCESS_DENIED; C/UE comprueban evento desconocido con el mismo resultado vacío: PASS |
| Sesión cerrada | P03/C/UE: SESSION_CLOSED y sin datos: PASS |
| Generación caducada | P03, C tras RESTORE, descarte UE: PASS |
| SAVE y RESTORE | P03 incluye proceso nuevo; C y UE repiten lectura tras recuperar: PASS |
| Repetición inmutable | P03 compara bytes Core completos, RNG/tick incluidos; UE conserva revisión: PASS |
| Emisión institucional no disponible | P02/P03 ejercitan el comando real, C/UE comprueban capacidad SERVICE_UNAVAILABLE: PASS |

La ejecución UE registrada devolvió rango **1102**, estado de servicio **1**, hecho/evento **40**, tick efectivo **0**, revisión original **449** y revisión de lectura **455**, consistente con el archivo Core confirmado y el binding HOST posterior. Estas cifras identifican exclusivamente el ensayo; no son el expediente del usuario ni se distribuyen como una partida de producto.

`StarTrek.H07.Institutional.Roundtrip` aprobó con **Unreal real NullRHI y D3D12**. Restaura H04, pulsa los controles Slate de carrera/ascenso, contrasta los hechos, deniega un lookup desconocido, guarda, recupera una generación nueva, descarta una consulta en vuelo al cerrar y verifica una nueva candidatura sin comisión. La suite no afirma haber pulsado botones desde un escritorio desbloqueado.

## Compilación y regresiones MSI

| Suite / compilación | Resultado |
|---|---|
| HOST CMake/MSVC x64 Release, tests ON | Build PASS; **315/315** CTest seleccionados HOST/F04/F05 PASS, incluidos P02 5/5, P03 12/12 y P05 ABI 1/1 |
| F11 aislada MSVC | **17/17 PASS**; emisor de ensayo solo en su proceso de laboratorio |
| HOST Release tests OFF | Prepare-Host PASS; inspección de símbolos/dependencias/pin y ABI PASS |
| Consumidor C de producto | **5/5 PASS** contra DLL Release tests OFF |
| SDK Academy y presentación pura | **5/5 PASS** en MSI, sin sustituir las pruebas UE |
| UHT / UBT Editor Win64 Development | PASS |
| UBT Game Win64 Development | PASS |
| ForceUnity efectiva | **PASS efectivo**: 13 unidades C++ en Module.StarTrekRPG.cpp; fuentes/cabeceras idénticas, solo dos reglas Unity distintas en la copia de ensayo |
| Win64 cocinado/empaquetado | **PASS**: cook y stage UAT con salida 0; seis automatizaciones del ejecutable empaquetado PASS |

**Unreal real, revisión final:** 29 ejecuciones individuales Automation, todas con `succeeded=1, failed=0, notRun=0` y proceso con salida 0. **23** fueron con UnrealEditor `-game` y **6** con el ejecutable Win64 empaquetado. No son 29 escenarios distintos: incluyen variantes RHI y reejecuciones en procesos nuevos.

- H07 Roundtrip: NullRHI y D3D12 en Editor/Game y en paquete.
- H06 geometría: cuatro ejecuciones Editor/Game y una empaquetada con las transiciones completas.
- Academia C-04: Seed, Resume, Navigation y SaveFailure en ambos RHI; DiagnosticFlow naval en ambos; Unavailable con una copia sin TrekHost.dll en NullRHI.
- Academia C-03: Seed/Resume en ambos RHI, con versión 2 corrupta y directorios vacíos de paginación preparados según el protocolo.
- Compatibilidad M1: copia del guardado de ensayo anterior, Resume y DiagnosticFlow D3D12; campaña `dbfc84fb2119708acfccfe9dbb0a2cbe`, PERSON 2, hecho 3, revisión 172, tick 0 y digest preservados. El guardado original quedó intacto.
- Paquete: H07 en ambos RHI, geometría/transiciones, Academy Seed, Resume y DiagnosticFlow naval D3D12 en procesos separados.

La copia sin DLL, los archivos deliberadamente corruptos y la obstrucción del guardado pertenecen exclusivamente a sus UserDir de laboratorio. El paquete mínimo omitía la plantilla HTML de informes y emitió ese aviso; los seis **index.json sí se generaron**, identifican el test y PASS, y los procesos salieron con código 0. No se distribuyó un fixture profesional ni una biblioteca trial dentro del paquete.

La selección CTest coincide con la del workflow nativo: HOST completo, F05 y las regresiones F04 indicadas por ese workflow; **no** se afirma haber ejecutado los 572 tests registrados en el grafo ni reauditar todas las campañas históricas. Para repetir el caso F05 I_process_save se utilizó un directorio de salida nuevo: ese test exige explícitamente una historia inexistente. No se borró la salida anterior. Se configuró una raíz H07 corta mediante la opción de pruebas TREK_HOST_H07_TEST_ROOT. Los escenarios que comparten el guardado P03 usan un resource lock CTest.

## Corrección H06 y aceptación visual

El [diagnóstico H06](H06_M1_UX_WINDOWED_2560_CORRECCION_2026-11-23.md) contiene mediciones anteriores y posteriores, fórmula del tamaño disponible y límites de captura. La copia anterior produjo un cliente físico **3840×2400** al solicitar 2560×1600 bajo Windows 150 %, con DPI-unaware. El código corregido usa DPI 144 y limita el cliente a **2538×1472**, dentro del área de trabajo **2560×1528**. No cambia automáticamente a pantalla completa.

Las cuatro ejecuciones D3D12 de geometría aprobaron: ventana 1920×1080, ventana 2560×1600 solicitada con ForceRes, pantalla completa sin bordes 2560×1600 y transiciones ventana→pantalla completa→ventana. En cada modo se comprobaron menú principal y Continuar; las transiciones muestrean seis estados. El comando de transición es el mismo del motor usado por Alt+Intro, sin afirmar una pulsación física.

Computer Use mostró la pantalla de bloqueo de Windows y se detuvo. Las capturas del viewport Unreal y las mediciones internas son evidencia técnica; **no** se declara aceptación visual humana, comprobación física de ratón/foco ni nuevas pruebas físicas de Escape/Alt+F4. Estas últimas siguen en la lista de aceptación.

## Ejecuciones iniciales que no se ocultan

Se conservan los logs de configuración inicialmente incompleta por checkout reducido, del primer error de compilación de macro de exportación, de la ruta extendida con separadores incorrectos y de las iteraciones geométricas. Dos pruebas iniciales de importación requerían rutas más cortas. Un reintento de la suite F05 reutilizó una salida que exigía ser nueva. Una prueba UE usó metadatos de un fixture que se había regenerado y terminó por timeout; se repitió con la copia estable junto al UserDir. El intento ForceUnity mientras había un proceso Editor/Game activo fue rechazado por Live Coding. Los primeros Resume/SaveFailure omitieron la corrupción/obstrucción exigida por C-04 y los primeros Resume C-03 omitieron su versión corrupta; las ejecuciones verified repiten los casos con esas precondiciones. El primer stage de UAT encontró el mutex del cook aún activo; el reintento con espera de mutex terminó correctamente. Ninguno se transforma retrospectivamente en PASS.

## CI, matriz y límites

Las ejecuciones Cloud/Actions se distinguen de MSI. Actions de código `2e75db5`: [HOST nativo/producto](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/45158039799), [frontera H07](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/45158039851) y [contratos H01](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/45158039832). **7/7 trabajos SUCCESS en ese código**: Linux/GCC 315/315, Windows/MSVC 315/315, Clang ASan/UBSan 160/160; F11 aislada 17/17 por trabajo nativo; producto Release tests OFF aprobado en Linux y Windows; H01 y frontera H07 aprobados. Los logs de los trabajos se consultaron para contrastar esos conteos. La CI del HEAD documental se verifica adicionalmente en la PR, sin atribuirla a ejecución MSI.

La matriz P04 conserva sus 27 escenarios y los 33 externos F11. Solo se actualizan los escenarios con evidencia ejecutada, identificando SHA y hash del artefacto. Los escenarios externos permanecen NOT_RUN: esta entrega no certifica reglas/emisión F11. La composición sin lector no se ha reejecutado localmente en P05. No se ejecutó una inyección directa de actor/verified desde LLM/NPC en Unreal; la nueva interfaz carece de esos campos y no concede ese canal.

## Entrega y revisión humana

El [manifiesto permanente](H07_P05_EVIDENCIAS_MSI_2026-11-23.json) recoge hashes de binarios, logs, informes Automation, CTest y capturas seleccionadas, junto a los resultados. Los datos brutos permanecen en el laboratorio local identificado arriba, prescindible para el juego; no se fuerzan dentro de Git. Conservarlo hasta terminar la auditoría si se necesitan los registros originales.

Para aceptar: comprobar base #204 y diff de #205; verificar ausencia de trial/issuer en DLL producto y pin Core; revisar las respuestas autorizadas/denegadas; desbloquear MSI y usar únicamente los lanzadores/UserDir de ensayo; revisar Academia principal/Continuar a 1920, 2560 solicitado y pantalla completa; comprobar teclado, ratón, foco, Escape, Alt+F4 y Alt+Intro físicos; crear/guardar/cerrar/relanzar/continuar; revisar que un cadete no obtiene expediente. Las pruebas positivas F11 deben usar la copia de laboratorio, nunca incorporar sus oficiales al producto. ChatGPT realizará la auditoría y decidirá la certificación limitada que corresponda. No se fusiona ninguna PR.


Desde la raíz principal del repositorio, abrir el paquete para la aceptación visual sin tocar guardados personales:

```powershell
$lab = (Resolve-Path 'laboratorios/host/h07-p05-20261123').Path
& "$lab/staged/Windows/StarTrekRPG.exe" -AcademyMenu -d3d12 -windowed -ForceRes -ResX=2560 -ResY=1600 "-UserDir=$lab/aceptacion-visual" "-AbsLog=$lab/aceptacion-visual.log"
```

Repetir con ResX=1920/ResY=1080 y después con Alt+Intro. No añadir `-unattended` a esta comprobación. Para revisar los hechos profesionales de ensayo, lanzar el mismo paquete **sin -AcademyMenu**, con `-UserDir` dirigido a `pkg-h07-user`; recuperar la campaña `07dd73f9191e6ff7980e7763ac8d0fc4`, ranura `career`, y consultar el evento 40. La identidad ya está vinculada y verificada por H04: no hay selector de observador. Es una partida aislada de laboratorio, no el personaje del usuario.

Archivos del corte: la extensión ABI y su implementación/consumidor C; normalización de ruta H04; negociación DLL, proyección, vista Slate y automatización H07; preparación y reglas UBT; ajuste DPI/ventana y prueba geométrica H06; README; workflow nativo; guardas y matriz P04; contrato, informes y manifiesto. El diff de #205 enumera los archivos exactos. No cambian pins, reglas F11, mapas/materiales originales ni recursos artísticos.
