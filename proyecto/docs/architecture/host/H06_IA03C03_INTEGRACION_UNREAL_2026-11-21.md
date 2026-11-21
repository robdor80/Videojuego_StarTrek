# H06 · IA-03C-03 · Integración de Academia con Unreal Engine 5.8.4

**Corte 21-11-2026.** Integración implementada en `codex/h06-ia03c03-academy-unreal` desde `main` en `098246e1bda8c40377f0e344949610c1f7cb948d`. C-01 y C-02 constan fusionadas en [#193](https://github.com/robdor80/Videojuego_StarTrek/pull/193) y [#194](https://github.com/robdor80/Videojuego_StarTrek/pull/194). Auditoría independiente de ChatGPT y certificación integral Unreal/M1 pendientes. La [PR #195](https://github.com/robdor80/Videojuego_StarTrek/pull/195) permanece Draft y sin fusionar.

**HEAD de implementación** `d36bfafc77dd56f62976c4631a202e0262735646`. El commit posterior registra la evidencia y el estado de C-03. La revisión exacta de entrega queda en el historial y en la descripción de la [PR Draft #195](https://github.com/robdor80/Videojuego_StarTrek/pull/195/commits).

## Arquitectura y contratos

`FStarTrekRPGModule` carga las mismas DLL Win64 de producto. `FHostApi` valida primero la ABI 1 y negocia después los tres símbolos de Academy. La negociación acepta v2. Un export ausente o una versión cero indican `SERVICE_UNAVAILABLE`. Otra versión indica `ABI_MISMATCH`. Ambos casos mantienen operativo el cliente v1. Las comprobaciones de tamaño cubren request/completion/status v1 (80/120/24 bytes), request/ficha/fila/completion Academy (48/240/104/6696) y los offsets de salida 72 y 32. [ABI v1](../../../../desarrollo/integration/host/include/trek/host/host_abi.h) · [Academy ABI v2](../../../../desarrollo/integration/host/include/trek/host/academy_abi.h).

| Consumidor C++ | Operación en HOST | Proyección de lectura |
| --- | --- | --- |
| `CreateAcademy(World, Name)` | Academy CREATE con nombre UTF-8 y clave monotónica de cliente. B02 genera la PERSON y H03 confirma el vínculo | `GetAcademyCandidate()` y `GetAcademyResult(TREK_HOST_ACADEMY_CREATE)` |
| `QueryAcademy(World)` | Academy QUERY con la generación actual y comprobación del vínculo en HOST | Campaña, PERSON descriptiva, nombre, hecho de creación, revisión, tick, digest y estado candidato |
| `ListAcademySlots(World, Cursor)` | Academy SLOTS con generación actual y cursor opaco. Cursor cero inicia | `GetAcademyPage()` y resultado SLOTS con error. Hasta 64 filas con familia, formato, procedencia, compatibilidad, recuperabilidad, versión y motivo de H04 |
| `Save(World, Slot)` y `RestoreAcademy(World, Row)` | SAVE y RESTORE v1. Continuar requiere sesión cerrada y usa UUID, ranura y versión explícita. H04 ejecuta sus validaciones de nuevo con RESTORE/AUTO | Resultado con `GetCompletion()`. Tras RESTORE se consulta la ficha nueva por Academy QUERY |
| Diagnóstico naval | OPEN, QUERY_VIEW, SAVE, RESTORE y CLOSE v1 | Mismo panel y vista v1. Su RESTORE histórico conserva la selección de última versión por dirección |

El retorno de submit indica admisión del ticket. Los resultados de dominio se publican por operación en la proyección de mundo, con código, ticket y generación. `RETRY` permite reenviar al no haber admitido la petición. Las referencias retornadas apuntan a la última proyección del mundo y se invalidan al cambiarla. La ficha solo representa un candidato vinculado; admisión F10, rango, destino, F05 y F11 permanecen bajo sus contratos nativos.

Para reintentar CREATE, se conserva la clave y el nombre exacto por cliente. El nombre se copia antes de submit para admitir también un argumento tomado de la ficha de mundo que la transición invalida. CLOSE retira el intento. Un cambio de nombre durante el mismo intento devuelve `IDEMPOTENCY_CONFLICT`. Ninguna entrada de creación acepta un `person_id` o un recibo. El UUID en `GetCampaignAddress()` es la última dirección publicada para el diagnóstico y puede seguir visible tras CLOSE.

## Concurrencia, mundos y catálogo

- GameInstance conserva el único cliente y el ticker existente. La preparación del directorio de guardados y la creación del cliente se ejecutan en segundo plano. El ticker toma la inicialización cuando está lista y serializa status, submit, poll y discard. El trabajador nativo resuelve las peticiones Core y H04 fuera del Game Thread.
- Ocho observaciones compartidas, con reserva de CLOSE. Cada observación marca su familia de poll. Se comprueba la generación con status después del poll antes de aplicar payload. Si hay contención, el ticker conserva la respuesta consumida hasta obtener el status. CLOSE revoca observaciones previas y RESTORE publica la generación nueva.
- Cada mundo mantiene una proyección con enlace débil. EndPlay descarta sus observaciones y vistas. Una transición admitida queda en GameInstance hasta completarse, aunque su observador ya se haya destruido. El mundo siguiente consulta la generación vigente. Descartar un ticket de SAVE deja continuar el trabajo H04.
- La inicialización y la retirada capturan la API por referencia compartida y usan hilos que pueden finalizar tras el cierre del Task Graph. La retirada puede esperar una inicialización pendiente fuera del Game Thread. El módulo Unreal Win64 permanece residente durante el proceso para que el callable siga disponible durante `ShutdownModule`. Las DLL nativas mantienen sus referencias hasta terminar `Destroy`. El cierre completo del proceso conserva las versiones ya confirmadas por H04.
- Se sigue `NextCursor` mientras sea distinto de cero, con independencia del número de filas. El consumidor solicita una página por turno. La siguiente petición debe usar el cursor publicado por esa proyección y generación. Los cambios de generación, las transiciones y SAVE invalidan la proyección del catálogo, incluso si SAVE conserva la generación. El puente retira la vista en cuanto se admite el ticket de SAVE, aunque la validación posterior de H04 devuelva un error. Un ticket de catálogo retirado por SAVE informa `GENERATION_EXPIRED`. Ante caducidad, el consumidor puede iniciar otra consulta desde cero. El catálogo es de lectura viva y H04 vuelve a comprobar el archivo al recuperar.

## Archivos

| Archivo | Cambio |
| --- | --- |
| `Source/StarTrekRPG/Private/HostRuntime.{h,cpp}`, `HostAcademyExports.h` | Carga y negociación opcional, comprobación de ABI y retención asíncrona de las DLL |
| `Source/StarTrekRPG/Private/HostSessionSubsystem.{h,cpp}` | Operaciones Academy, proyecciones tipadas y despacho por familia dentro del ticker y cliente existentes |
| `Build/Prepare-Host.ps1`, `Source/StarTrekRPG/StarTrekRPG.Build.cs` | Staging y comprobación de ambas cabeceras antes de UBT. x64 Release y pin Core se verifican con el build existente |
| `Build/Tests/{CMakeLists.txt,HostAcademyExportsTest.cpp}`, `.github/workflows/host-h02-native.yml` | Prueba del negociador con producto real. El job Windows ejecuta el staging oficial en copia aislada, coteja hashes y carga las DLL desde el SDK |
| `Source/StarTrekRPG/Private/HostAutomation.cpp`, `HostAcademyAutomation.cpp` | El diagnóstico histórico espera la inicialización asíncrona. Se añaden Seed y Resume para uso posterior en UE |
| `juego/UE5/StarTrekRPG/README.md` | Inventario de cabeceras y DLL requeridas para preparar el proyecto |
| Este informe y `H06_CONTROL_UNICO_ESTADO_2026-11-21.md` | Estado de C-01 a C-03 y verificaciones pendientes |

Las rutas de fuentes y scripts Unreal de la tabla se resuelven desde `juego/UE5/StarTrekRPG`. CoreRPG conserva el pin `76a7b7b485616d8c4994f384a90f123bf333591d`. La entrega se limita a fuentes y procedimientos de Unreal, comprobaciones de SDK y documentación de H06.

## Pruebas ejecutadas

| Verificación | Resultado y evidencia |
| --- | --- |
| Cloud Linux Release, HOST y regresiones F04/F05 | **297/297 PASS**, GCC 14.2.0. JUnit y logs locales `native.xml` y `native-tests.log`. Incluye ABI, continuidad de PERSON/hecho, tickets cruzados, reserva CLOSE, generaciones, paginación y cursores caducados |
| Cloud Linux Release con tests OFF | **5/5 PASS** en consumidores independientes. Inspección del producto, ABI v1, pin, exports y dependencias PASS. |
| Cloud Linux, negociador del SDK contra biblioteca Release | **1/1 PASS**, con los exports reales, omisión individual de cada símbolo, versión cero, versión Draft incompatible y uso posterior de ABI v1. |
| Cloud H01 y regresión aislada F11 | **11/11 PASS** en contratos y **17/17 PASS** en la regresión. |
| Cloud Linux, ensayo nativo de los datos de Seed/Resume | **PASS** contra producto tests OFF en dos procesos. Misma PERSON, hecho y checkpoint tras recuperar la versión 1. Validó el nombre, 66 versiones, la página vacía, el rechazo de la versión dañada, CLOSE con una consulta pendiente y el cursor retirado. |
| Actions Linux nativo Release | **297/297 PASS**, H01 y F11 PASS. [Job Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44913289761/job/136873455554). |
| Actions Windows nativo Release | **297/297 PASS**, H01 y F11 PASS. [Job Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44913289761/job/136873455645). |
| Actions Linux Clang ASan/UBSan | **142/142 PASS**. [Job ASan/UBSan](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44913289761/job/136873455539). |
| Actions Linux Release con tests OFF | **5/5 PASS** y **1/1 PASS** del negociador con producto real. [Job producto Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44913811410/job/136875011283). |
| Actions Windows x64 Release con tests OFF | **5/5 PASS** y **1/1 PASS** del negociador con las DLL del SDK preparado por `Prepare-Host.ps1`. Los hashes de ambas cabeceras y DLL coincidieron con la fuente y el build Release. [Job producto Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44913811410/job/136875011357). |

La primera ejecución compiló y preparó el SDK Windows, y el consumidor nuevo falló al cargar la DLL. La comprobación pasó tras normalizar la ruta Win64 y cargar primero `TrekF04Bridge.dll`, como hace `HostRuntime`. La matriz anterior al ajuste de copia del nombre y el check H01 tienen sus propias ejecuciones. El HEAD de entrega activa los mismos checks. La comprobación del reintento desde una ficha de mundo forma parte de Seed, pendiente de UE en MSI. [Carga inicial de prueba](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44913289761/job/136873455636) · [Matriz anterior al ajuste de copia del nombre](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44914154850) · [H01 de esa revisión](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44914154848) · [Checks de la PR](https://github.com/robdor80/Videojuego_StarTrek/pull/195/checks).

Unreal Engine 5.8.4 y UBT están ausentes en Cloud. La prueba del negociador solo compila C++ contra las cabeceras C y carga el producto nativo. Seed y Resume ejercitan el subsistema Unreal y quedan preparados para ejecutarse en MSI.

## Pruebas MSI pendientes

| Verificación UE 5.8.4 | Estado |
| --- | --- |
| Compilación UBT de `StarTrekRPGEditor` | **NOT_RUN** |
| Compilación UBT de `StarTrekRPG` Win64 | **NOT_RUN** |
| Ejecución real con Unreal NullRHI | **NOT_RUN** |
| Ejecución real con Unreal D3D12 | **NOT_RUN** |
| Cambio real de `UWorld` en Unreal | **NOT_RUN** |
| Carga real en Unreal de las DLL preparadas en MSI | **NOT_RUN** |
| Creación, guardado, cierre de proceso y recuperación desde Unreal | **NOT_RUN** |
| Prueba interactiva del jugador en MSI | **NOT_RUN** |

## Reproducción en MSI

1. Desde la raíz del repositorio con el HEAD de la PR, definir `$engine` como la instalación de UE 5.8.4, `$core` como el checkout limpio del pin y `$work` como un directorio de pruebas nuevo según `AGENTS.md`. Usar una copia aislada del mismo proyecto versionado para conservar sus originales. [Procedimiento oficial de reconstrucción](../../../../juego/UE5/StarTrekRPG/README.md).

   ```powershell
   $source = Join-Path $PWD 'juego/UE5/StarTrekRPG'
   $version = Get-Content "$engine/Engine/Build/Build.version" -Raw | ConvertFrom-Json
   if ("$($version.MajorVersion).$($version.MinorVersion).$($version.PatchVersion)" -ne '5.8.4') {
       throw 'Seleccionar Unreal Engine 5.8.4.'
   }

   New-Item -ItemType Directory "$work/tmp", "$work/ue-src" -Force | Out-Null
   $env:TEMP = "$work/tmp"
   $env:TMP = $env:TEMP
   $env:TMPDIR = $env:TEMP
   $env:UE_LOCAL_CACHE = "$work/ddc"
   [Environment]::SetEnvironmentVariable('UE-LocalDataCachePath', $env:UE_LOCAL_CACHE, 'Process')
   git archive --format=zip --output="$work/project.zip" HEAD juego/UE5/StarTrekRPG
   if ($LASTEXITCODE) { throw 'No se pudo copiar la fuente versionada.' }
   Expand-Archive -LiteralPath "$work/project.zip" -DestinationPath "$work/ue-src"
   $projectDir = Join-Path "$work/ue-src" 'juego/UE5/StarTrekRPG'
   $project = Join-Path $projectDir 'StarTrekRPG.uproject'

   & "$source/Build/Prepare-Host.ps1" -CoreSource $core -BuildRoot "$work/native" -ProjectDir $projectDir
   $build = "$engine/Engine/Build/BatchFiles/Build.bat"
   foreach ($target in @('StarTrekRPGEditor', 'StarTrekRPG')) {
       & $build $target Win64 Development "-Project=$project" -WaitMutex -NoHotReload -NoUBA -NoXGE -MaxParallelActions=3 "-Log=$work/ubt-$target.log"
       if ($LASTEXITCODE) { throw "UBT falló para $target" }
   }
   $editor = "$engine/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
   & $editor $project -run=HostDiagnosticMap -nullrhi -unattended -nop4 -NoZenAutoLaunch -ddc=NoZenLocalFallback "-UserDir=$work/map-user" "-AbsLog=$work/map.log"
   if ($LASTEXITCODE) { throw 'Falló la generación del mapa.' }
   ```

2. Ejecutar dos procesos por RHI. Seed crea una campaña, hace `LoadMap` con CREATE aún observado por GameInstance, compara la misma ficha tras reintentar y guarda 66 versiones. Entre procesos se prepara un caso de página vacía y una versión dañada dentro de ese mismo almacenamiento de prueba. Resume recorre todas las páginas, conserva el rechazo de H04, restaura la versión H04 1 y compara PERSON, hecho, campaña, nombre y checkpoint. Ambos procesos comprueban el RHI real y el cierre con observaciones pendientes.

   ```powershell
   function Invoke-AcademyTest($Test, $Rhi, $UserSandbox, $Output) {
       & $editor $project -game $Rhi -unattended -nop4 -nosound -nosplash -windowed -resx=960 -resy=650 `
           -NoZenAutoLaunch -ddc=NoZenLocalFallback "-UserDir=$UserSandbox" "-AbsLog=$Output.log" `
           "-ExecCmds=Automation RunTests $Test" '-TestExit=Automation Test Queue Empty' `
           "-ReportExportPath=$Output-report"
       if ($LASTEXITCODE) { throw "$Test falló con $Rhi" }
       $report = Get-Content -LiteralPath "$Output-report/index.json" -Raw | ConvertFrom-Json
       if ($report.succeeded -ne 1 -or $report.failed -ne 0 -or $report.notRun -ne 0 -or
           @($report.tests).Count -ne 1 -or $report.tests[0].fullTestPath -ne $Test -or $report.tests[0].state -ne 'Success') {
           throw "Informe inesperado para $Test con $Rhi"
       }
       if (!(Select-String -LiteralPath "$Output.log" -SimpleMatch 'H06 HOST ABI 1 loaded with TrekF04Bridge; Academy v2: OK')) {
           throw "No se confirmó la carga real de Academy v2 en $Output.log"
       }
   }

   foreach ($mode in @('nullrhi', 'd3d12')) {
       $user = Join-Path $work "academy-$mode"
       if (Test-Path -LiteralPath $user) { throw "La prueba necesita un UserDir nuevo: $user" }
       New-Item -ItemType Directory $user | Out-Null
       Invoke-AcademyTest 'StarTrek.H06.Academy.Seed' "-$mode" $user "$work/$mode-seed"

       $root = Join-Path $user 'Saved/HostSlots'
       $campaign = (Get-Content -LiteralPath "$root/academy-c03-identity.txt" -Raw).Split('|')[0]
       if ($campaign -cnotmatch '^[0-9a-f]{32}$') { throw 'La ficha de prueba carece de un UUID válido.' }
       $slots = Join-Path $root "campaigns/$campaign/slots"
       foreach ($index in 0..139) {
           New-Item -ItemType Directory (Join-Path $slots ('0empty{0:D3}' -f $index)) | Out-Null
       }
       Set-Content -LiteralPath "$slots/academy_c03/v2/COMMITTED" -Encoding ascii -NoNewline -Value 'fixture-corrupto'
       Invoke-AcademyTest 'StarTrek.H06.Academy.Resume' "-$mode" $user "$work/$mode-resume"
   }
   ```

3. Ejecutar también `StarTrek.H06.DiagnosticFlow` con un `-UserDir` distinto por RHI. Para el fixture naval y el smoke Win64 empaquetado, usar el procedimiento histórico con la instalación 5.8.4. Abrir el juego de diagnóstico en D3D12 de manera interactiva, probar OPEN/VIEW/CLOSE y registrar la aceptación del jugador por separado. Nueva partida y Continuar de Academia se ejercitan con Automation en C-03. Su interfaz interactiva corresponde a C-04. Guardar logs, informes JSON, hashes de las dos DLL y el archivo `Build.version` de la instalación utilizada. [Comandos del diagnóstico H06](H06_RESULTADOS_2026-11-13.md).

## Límites pendientes

El catálogo refleja una lectura viva del disco y un cursor puede caducar entre páginas. El cliente mantiene solo la página actual por proyección. Continuar exige que se conserve el dato de la versión seleccionada y que H04 aún acepte su dirección. Una creación sin SAVE confirmado sigue siendo volátil al finalizar el proceso. La auditoría debe revisar el ciclo de carga y retirada de DLL y los resultados reales de UE 5.8.4 en MSI. La evidencia de implementación y el HEAD de entrega se consultan en la [PR Draft #195](https://github.com/robdor80/Videojuego_StarTrek/pull/195/commits).
