# H06 · IA-03C-04 · Implementación de Nueva partida, Continuar y ficha de Academia

**Corte 22-11-2026.** Implementación de [la especificación UX aprobada](H06_IA03C04_DISENO_FUNCIONAL_MENU_ACADEMIA_2026-11-21.md) sobre `main` en `9f96c2aa998dea6a66def517948c3d3cfcb3f769` ([PR #196](https://github.com/robdor80/Videojuego_StarTrek/pull/196)). Rama `codex/h06-ia03c04-academy-menu`. Revisión de implementación `1f3179f7f36eb5a7a8135361143496b029fd26ec`. El historial de la PR registra el HEAD de entrega, que incorpora este informe.

| Estado | Alcance |
| --- | --- |
| **IMPLEMENTADO** | Fuentes Slate/C++, integración con HOST y procedimientos de verificación en MSI |
| **PROBADO** | HOST nativo, producto Release, SDK y secuenciación C++ de presentación sin Unreal |
| **AUDITADO** | Pendiente de auditoría independiente de ChatGPT |
| **FUSIONADO** | Pendiente. Entrega en PR Draft |
| **CERTIFICADO** | Unreal Engine 5.8.4 y M1 pendientes. UBT, Slate real y aceptación en MSI figuran como **NOT_RUN** |

## Arquitectura y pantalla de entrada

`-AcademyMenu` selecciona Slate/C++ en el controlador del mapa `/Game/Diagnostics/HostDiagnostic`. La entrada habitual sigue siendo el diagnóstico naval. El commandlet histórico genera el mismo mapa en una copia recién preparada. La interfaz utiliza controles Slate y recursos de estilo del motor.

El `UHostSessionSubsystem` de GameInstance conserva el cliente y el flujo de presentación. Los widgets se reconstruyen por mundo. La capa C++ de presentación decide qué mostrar y qué solicitud enviar en respuesta a los controles. Obtiene catálogo y ficha de la `UHostWorldProjection` vigente y descarta esas vistas al cambiar de mundo o generación. HOST coordina las transiciones y H03/H04. CoreRPG aporta la PERSON, su vínculo y el hecho de creación.

| Pantalla | Comportamiento y contrato |
| --- | --- |
| Menú principal | Muestra conexión, disponibilidad de Academy v2 o error con código. Nueva partida y Continuar requieren sesión cerrada. Salir espera el cierre aplicable. La vía de Academia usa CREATE y RESTORE para entrar en sesión. |
| Nueva partida | Único campo editable, el nombre. `CreateAcademy` valida la conversión sin pérdida y HOST valida UTF-8 y las reglas de nombre. Tras resultado final CREATE se consulta `QueryAcademy`. La ficha exige campaña e identidad presentes, estado Candidato, generación vigente y vínculo H03 confirmado. Inicia el primer `Save` en `principal` y muestra su resultado final. Un rechazo del nombre deja el campo editable. Un conflicto permite retomar el nombre exacto o cerrar el intento antes de cambiarlo. |
| Continuar | `ListAcademySlots` empieza en cursor cero, conserva hasta 64 filas visibles y ofrece Cargar más si H04 devuelve cursor, también tras una página vacía. Respeta el orden nativo y filtra la familia Naval. El catálogo muestra la campaña, ranura, versión, integridad, compatibilidad y metadatos disponibles de H04. Un catálogo agotado sin filas Academy tiene un mensaje propio. Un error conserva su código y permite empezar el listado. Las versiones rechazadas se pueden seleccionar para consultar su estado. Solo las recuperables permiten confirmar `RestoreAcademy` con la versión exacta. Después, una QUERY valida la campaña y la generación nueva y presenta la identidad recuperada. |
| Ficha | Nombre de CoreRPG, estado Candidato, campaña, guardado y detalles técnicos de PERSON, hecho, revisión, tick y huella de origen en lectura. Guardar usa H04 en `principal`. Guardar y cerrar espera SAVE final OK y después CLOSE final OK. Cerrar partida y Salir piden confirmación si el progreso carece de guardado confirmado. La interfaz muestra el estado de candidatura sin otorgar credenciales institucionales. |
| Confirmaciones y recuperación | Confirma la dirección de H04 seleccionada, permite cancelar un cierre con pérdida y ofrece repetir QUERY si faltó verificar la ficha. Incluye mensajes en castellano con los códigos relevantes. La solicitud de cerrar la ventana del juego usa el mismo flujo cuando el visor admite el delegado. |

### Tickets, generaciones y errores

- El panel bloquea acciones incompatibles desde el clic. El controlador sigue un único ticket admitido. Para una respuesta de submit `RETRY` limita los reenvíos a cinco con 80 ms de espera entre intentos. Poll, creación de cliente, trabajo de CoreRPG y disco H04 conservan la ejecución del puente existente. El Game Thread consume las vistas y los resultados.
- Las mutaciones siguen observándose en GameInstance al viajar. CREATE y RESTORE ya eran transiciones retenidas de C-03. C-04 amplía la observación opcional al resultado de SAVE para conservar la confirmación real durante el viaje. El puente identifica ticket, familia, operación y generación. QUERY y SLOTS siguen publicando sus DTO en su mundo. Tras descartar un mundo se toma la generación vigente, se vuelve a consultar la candidatura y se invalida el catálogo anterior. Un cursor expirado requiere un nuevo recorrido desde cero.
- Los resultados finales `PUBLICATION_UNCERTAIN` y las observaciones ambiguas de un SAVE admitido dejan el guardado sin confirmar. La ficha bloquea otro SAVE durante esa sesión y permite cerrar con confirmación. Continuar ofrece la comprobación de las versiones que H04 puede leer y recuperar. El catálogo no prueba por sí solo qué versión produjo el intento incierto.
- El cliente, el ABI naval v1, Academy v2, la reserva de CLOSE y el pin Core `76a7b7b485616d8c4994f384a90f123bf333591d` se conservan. H03, H04, F04/F05, F11 y S04 mantienen sus contratos. Los archivos de mapa y recursos se conservan.

### Fuentes y pruebas

Rutas relativas a `juego/UE5/StarTrekRPG/` salvo el tablero y este informe.

| Archivos | Cambio |
| --- | --- |
| `Source/StarTrekRPG/Private/SHostAcademyMenu.{h,cpp}` | Pantallas, lista Slate con selección, avisos, confirmaciones, integración de foco y teclado |
| `Source/StarTrekRPG/Private/HostAcademyMenu{.h,.cpp,Flow.h}` | Secuenciación de presentación, catálogo por página y adaptación de acciones y resultados a la proyección vigente |
| `Source/StarTrekRPG/Private/HostSessionSubsystem.{h,cpp}` | Recibo opcional por ticket, SAVE observado tras viaje, validación del resultado v1 y protección de conversión Unicode |
| `Source/StarTrekRPG/Private/HostDiagnosticGameMode.{h,cpp}` | Entrada optativa al menú y coordinación del visor y cierre. Conserva la vía naval |
| `Source/StarTrekRPG/Private/HostAcademyMenuAutomation.cpp`, `HostSlateAutomation.h`, `HostAutomation.cpp` | Automatizaciones Slate y búsqueda de controles compartida con el diagnóstico histórico |
| `Build/Tests/{CMakeLists.txt,HostAcademyMenuFlowTest.cpp}` | Cuatro casos CTest de la lógica de presentación, integrados en los jobs SDK existentes |
| `README.md`, tablero e informe | Entrada reproducible, alcance probado y protocolo MSI |

## Evidencia Cloud

| Verificación | Resultado |
| --- | --- |
| Linux GCC 14.2.0, compilación Release y CTest HOST/F04/F05 | **297/297 PASS**. Selección de la matriz de CI. Incluye ABI v1/v2, identidad, fallos de persistencia, cursores, doble CREATE nativo y continuidad entre procesos |
| Linux Release con pruebas internas desactivadas | **5/5 PASS** consumidores de producto, inspección de exports y ABI **PASS**. Pin Core y ausencia de ganchos de pruebas verificados |
| Linux SDK y controlador de presentación | **5/5 PASS**. Un caso de negociación contra producto real y cuatro casos C++ sin Unreal |
| Contratos HOST H01 y regresión F11 aislada | **11/11 PASS** y **17/17 PASS**, respectivamente |
| Linux local ASan/UBSan y GitHub Actions Linux/Windows | Estado y enlaces en la revisión de evidencia de la PR |
| Unreal Engine 5.8.4 y UBT | **NOT_RUN**, herramientas ausentes en Cloud |

Los logs locales, XML de CTest, compilaciones y checkout exacto de Core se conservan en el laboratorio de esta ejecución según `AGENTS.md`. El proyecto y CI pueden recrear lo necesario a partir de las fuentes y del pin.

## Matriz UX-01 a UX-15

La columna Cloud identifica la evidencia de cada capa. La columna MSI reserva la aceptación Unreal.

| ID | Verificación y evidencia Cloud | Unreal/MSI |
| --- | --- | --- |
| UX-01 | **PASS SDK** para export ausente, versión cero, versión incompatible y ABI naval posterior. `AcademyMenu.Unavailable` comprueba el widget y la sesión cerrada sin DLL. | **NOT_RUN** |
| UX-02 | **PASS ABI v2** para nombre inválido, exceso y Unicode en el contrato; **PASS** transición C++ de rechazo. `Seed` comprueba exceso multibyte y nombre válido desde el campo. | **NOT_RUN** |
| UX-03 | **PASS ABI v2** y **PASS presentación** para el flujo CREATE → QUERY. `Seed` pulsa dos veces y comprueba la identidad y una sola campaña tras paginar con `Resume`. | **NOT_RUN** |
| UX-04 | **PASS H04** y **PASS presentación** para la secuencia de confirmación. `Seed` comprueba estado pendiente y marcador H04 de `principal/v1`. | **NOT_RUN** |
| UX-05 | **PASS H04** en fallos de publicación y **PASS presentación** para fallo inicial e incertidumbre. `SaveFailure` cubre error de disco real, espera y cierre cancelable. Inyección de publicación incierta en Slate **NOT_RUN**. | **NOT_RUN** |
| UX-06 | **PASS** consumidor Academy entre procesos. `Resume` abre Continuar sin UUID introducido por el jugador. | **NOT_RUN** |
| UX-07 | **PASS ABI/SDK** para más de 64 versiones, continuación vacía y lógica de catálogo. `Resume` recorre 66 versiones de Academia con páginas vacías, y la preparación MSI añade almacenamiento Naval en el mismo catálogo. | **NOT_RUN** |
| UX-08 | **PASS H04** y **PASS presentación** para filas dañadas o incompatibles. `Resume` selecciona una dañada y verifica que la recuperación está deshabilitada. | **NOT_RUN** |
| UX-09 | **PASS** consumidor real entre procesos y secuenciación RESTORE → QUERY. `Resume` verifica v1 con la ficha completa del proceso Seed. | **NOT_RUN** |
| UX-10 | **PASS ABI v2** para cursores caducados. `Resume` retira el catálogo por CLOSE, verifica descartes y pulsa Empezar listado. | **NOT_RUN** |
| UX-11 | **PASS presentación** para reconsulta. `Seed` recarga el mapa con CREATE, QUERY y primer SAVE admitidos y verifica descarte de la proyección anterior y resultado final correcto. | **NOT_RUN** |
| UX-12 | **PASS presentación** para SAVE → CLOSE, fallo e incertidumbre. `Seed` y `SaveFailure` verifican el cierre confirmado y la opción de cancelar el abandono. | **NOT_RUN** |
| UX-13 | **PASS** regresiones nativas v1/F04/F05. `StarTrek.H06.DiagnosticFlow` prepara la regresión Slate histórica. | **NOT_RUN** |
| UX-14 | **PASS HOST/F05/F11** dentro de sus ámbitos. `Resume` comprueba Candidato, H03 y disponibilidad institucional de la ficha real. | **NOT_RUN** |
| UX-15 | Foco y navegación incorporados en fuentes. La prueba de teclado, ratón y lectura de estados requiere ventana real. | **NOT_RUN** |

## Ocho comprobaciones C-03 y verificación adicional C-04 en MSI

| Comprobación | Estado |
| --- | --- |
| Compilación UBT de `StarTrekRPGEditor` | **NOT_RUN** |
| Compilación UBT de `StarTrekRPG` Win64 | **NOT_RUN** |
| Ejecución real NullRHI | **NOT_RUN** |
| Ejecución real D3D12 | **NOT_RUN** |
| Cambio de `UWorld` en Unreal | **NOT_RUN** |
| Carga real de las DLL en Unreal | **NOT_RUN** |
| CREATE, SAVE, cierre de proceso y RESTORE desde Unreal | **NOT_RUN** |
| Prueba interactiva del jugador | **NOT_RUN** |
| Slate Academy con DLL ausente, guardado fallido, cursor caducado y versión dañada | **NOT_RUN** |
| Navegación por Tab, flechas, Intro, Escape y ratón. Lectura de estados, selección y confirmaciones en 1920×1080 y 2560×1600. Cierre por botones y por la ventana | **NOT_RUN** |
| Juego Win64 empaquetado con `-AcademyMenu` y aceptación del jugador | **NOT_RUN** |

## Reproducción en MSI

1. Obtener el HEAD de la PR y seguir la preparación aislada del [informe C-03](H06_IA03C03_INTEGRACION_UNREAL_2026-11-21.md#reproducción-en-msi). Usar un `$work` absoluto y nuevo bajo el directorio de resultados de la tarea. El procedimiento verifica `Build.version`, genera una copia desde Git, ejecuta `Prepare-Host.ps1`, compila los dos targets y genera el mapa con el commandlet. Conservar el mapa original fuera de la copia de prueba.
2. Mantener los pares históricos `StarTrek.H06.Academy.Seed` / `Resume` y `StarTrek.H06.DiagnosticFlow` del procedimiento anterior. Ejecutar la matriz C-04 en procesos separados con el editor por línea de comandos. Cada RHI tiene almacenamientos propios. El diagnóstico entre Seed y Resume incorpora un guardado naval mediante el flujo histórico en el mismo catálogo.

   ```powershell
   function Invoke-HostUiTest($Project, $Test, $Mode, $UserDir, $Log, $Academy, $ExpectDll) {
       $menuArg = @()
       if ($Academy) { $menuArg += '-AcademyMenu' }
       & $editor $Project -game "-$Mode" @menuArg -unattended -nop4 -nosound -nosplash -windowed -resx=960 -resy=650 `
           -NoZenAutoLaunch -ddc=NoZenLocalFallback "-UserDir=$UserDir" "-AbsLog=$Log.log" `
           "-ExecCmds=Automation RunTests $Test" '-TestExit=Automation Test Queue Empty' "-ReportExportPath=$Log-report"
       if ($LASTEXITCODE) { throw "$Test falló con $Mode" }
       $report = Get-Content -LiteralPath "$Log-report/index.json" -Raw | ConvertFrom-Json
       if ($report.succeeded -ne 1 -or $report.failed -ne 0 -or $report.notRun -ne 0 -or
           @($report.tests).Count -ne 1 -or $report.tests[0].fullTestPath -ne $Test -or $report.tests[0].state -ne 'Success') {
           throw "Resultado inesperado de $Test con $Mode"
       }
       if ($ExpectDll -and !(Select-String -LiteralPath "$Log.log" -SimpleMatch 'H06 HOST ABI 1 loaded with TrekF04Bridge; Academy v2: OK')) {
           throw 'Falta evidencia de carga real de ambas DLL'
       }
   }

   foreach ($mode in @('nullrhi', 'd3d12')) {
       $user = Join-Path $work "c04-$mode"
       $failUser = Join-Path $work "c04-$mode-fallo"
       if ((Test-Path $user) -or (Test-Path $failUser)) { throw 'Usar almacenamientos nuevos' }
       New-Item -ItemType Directory $user, "$failUser/Saved/HostSlots" | Out-Null
       Invoke-HostUiTest $project 'StarTrek.H06.AcademyMenu.Seed' $mode $user "$work/c04-$mode-seed" $true $true
       Invoke-HostUiTest $project 'StarTrek.H06.DiagnosticFlow' $mode $user "$work/c04-$mode-naval" $false $true

       $root = Join-Path $user 'Saved/HostSlots'
       $campaign = (Get-Content -LiteralPath "$root/academy-c04-identity.txt" -Encoding utf8 -Raw).Split('|')[0]
       if ($campaign -cnotmatch '^[0-9a-f]{32}$') { throw 'UUID inválido en la ficha de prueba' }
       $slots = Join-Path $root "campaigns/$campaign/slots"
       if (!(Test-Path -LiteralPath "$slots/principal/v66/COMMITTED" -PathType Leaf)) { throw 'Falta la versión 66' }
       foreach ($index in 0..139) {
           New-Item -ItemType Directory (Join-Path $slots ('0empty{0:D3}' -f $index)) | Out-Null
       }
       Set-Content -LiteralPath "$slots/principal/v2/COMMITTED" -Encoding ascii -NoNewline -Value 'fixture-corrupto'
       Invoke-HostUiTest $project 'StarTrek.H06.AcademyMenu.Resume' $mode $user "$work/c04-$mode-resume" $true $true

       Set-Content -LiteralPath "$failUser/Saved/HostSlots/campaigns" -Encoding ascii -NoNewline -Value 'impide-crear-directorio'
       Invoke-HostUiTest $project 'StarTrek.H06.AcademyMenu.SaveFailure' $mode $failUser "$work/c04-$mode-fallo" $true $true
   }
   ```

3. Para `StarTrek.H06.AcademyMenu.Unavailable`, duplicar dentro de `$work` la copia preparada del proyecto, incluido el mapa y `Binaries`. En esa copia, renombrar `Binaries/Win64/TrekHost.dll` a `TrekHost.dll.disabled` y ejecutar `Invoke-HostUiTest` con esa copia, un `-UserDir` nuevo, `-nullrhi` (argumento `nullrhi` en la función), `$Academy=$true` y `$ExpectDll=$false`. Registrar también la negociación incompatible del SDK por separado.
4. Lanzar el juego interactivo según el [README del proyecto](../../../../juego/UE5/StarTrekRPG/README.md#ejecutar-el-menú-de-academia). Repetir con el ejecutable Win64 empaquetado. Con teclado y ratón, crear, guardar, salir, relanzar con el mismo UserDir, elegir una versión histórica y comparar PERSON y hecho. Probar el retorno, los avisos y la confirmación de cierre en la variante con error de guardado. Conservar logs, informe JSON, hashes de DLL, capturas, versión del motor y aceptación del jugador.

## Límites y riesgos

- UHT, UBT, Slate y el cierre de ventana de UE 5.8.4 siguen pendientes de MSI. La secuenciación de presentación y el SDK compilan en Cloud con CMake. El comportamiento de foco y la actualización de vistas con NullRHI siguen pendientes.
- El catálogo presenta una lectura viva. Una selección puede caducar o cambiar en disco antes de que H04 vuelva a validar la versión.
- H04 v1 devuelve un código final para SAVE y el catálogo omite fecha, hora y nombre. El menú comunica confirmación de `principal` y presenta la versión del catálogo mediante sus metadatos reales.
- Los cierres normales del menú esperan los resultados. Una terminación forzada del proceso puede perder una candidatura sin guardado confirmado. La certificación de M1 requiere las comprobaciones reservadas y la auditoría independiente.
