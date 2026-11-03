# F05-P05B — certificación integral en MSI

**PENDIENTE / NO EJECUTADA.** P05A es una auditoría Cloud; CI Windows no
acredita este procedimiento. MSI apagado. F05 permanece EN_CURSO, P01–P04
EN_REVISION y F06 bloqueada. La suite documental histórica P05 no certifica
P05A/P05B. Solo un acta posterior, después de auditar las evidencias reales,
podrá proponer el cierre; este runner no cambia el estado del proyecto.

## Requisitos e identidades

- MSI del propietario, Windows x64, PowerShell **7**, Developer PowerShell de
  Visual Studio con MSVC, SDK Windows, `dumpbin`, Git, Python 3 y CMake >=3.25.
  Registrar versiones realmente utilizadas; no inferirlas de ejecuciones previas.
- Checkout Star Trek limpio en el **HEAD auditado de la PR P05A**, obtenido
  del informe/PR, no en un `main` que todavía no contenga la entrega.
- Checkout Core limpio y separado en
  `76a7b7b485616d8c4994f384a90f123bf333591d`, pin F05 sin cambios.
  No cambiar el `main` del propietario: usar un checkout/worktree independiente.
- Instalación real **UE 5.8.2**, comprobada leyendo `Engine/Build/Build.version`;
  registrar changelist. No modificar el motor instalado.
- GPU/controlador y sesión gráfica aptos para RHI real. No usar NullRHI como
  sustituto. No abrir proyectos artísticos; el harness contiene solo fuentes
  técnicas y recursos del motor. No necesita claves, proveedor remoto ni costes IA.
- Directorio de salida ASCII **nuevo**, dentro de los laboratorios del repositorio.
  El runner crea dos laboratorios limpios independientes. No borrar ni reutilizar
  laboratorios anteriores. Descargas de dependencias de compilación no son una
  dependencia de Internet de la autonomía en ejecución.

## Procedimiento reproducible

Desde Developer PowerShell 7, en la raíz del checkout Star Trek:

```powershell
$Repo = (Get-Location).Path
$Expected = '<SHA completo auditado de la PR P05A>'
$Core = '<checkout Core independiente fijado>'
$UE = '<raiz de instalacion UE 5.8.2>'
$Output = Join-Path $Repo ('laboratorios/f05/p05b/msi-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))

git rev-parse HEAD
git -C $Core rev-parse HEAD
git status --short
cmake --version
python --version
cl 2>&1

./desarrollo/integration/f05/run_p05b_msi.ps1 `
  -ExpectedTrekSha $Expected -CoreSource $Core -BuildRoot $Output `
  -EngineRoot $UE -Generator 'Visual Studio 18 2026'
```

El script rechaza SHA incorrecto, fuentes modificadas, salida preexistente,
ruta no permitida o versión UE distinta. Invoca el runner nativo común para
Core completo con JSON y el [runner F05 existente](../../../../../../desarrollo/integration/f05/run_f05.ps1)
para Native → Stage → Unreal → TestUnreal → TestUnreal con RealRHI,
**dos veces con builds, DLL, datos y reportes nuevos**. No borra archivos.

En cada repetición se espera:

1. Core completo: inventario **483 tests**. La auditoría Linux exige 483 PASS.
   En Windows, Core puede omitir explícitamente
   `ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt`
   porque `std::filesystem::permissions` no impide la lectura con semántica POSIX.
   Conservar mensaje y JUnit original: si ocurre, son **482 PASS + 1 SKIP**, nunca
   483 PASS. El runner solo admite ese SKIP condicional en Core/Windows, informa
   `PASS_COMPATIBLE_WITH_PLATFORM_SKIP` y rechaza cualquier otra omisión o fallo.
   No se modifica Core ni su oráculo; no acredita pruebas de ACL Windows.
2. Suite F04/F05: **395 tests**, incluidos P01=20, P02=20, P03=26, P04=38 y
   P05A=30. Incluye los productores/consumidores separados de monolítico e
   historial, RNG futuro exacto, revocación, permisos, privacidad e idempotencia.
   Los 11 diagnósticos monolíticos históricos excluidos conservan esa condición;
   no contarlos ni alterar sus oráculos.
3. `dumpbin /EXPORTS` y `/DEPENDENTS` sobre la DLL recién compilada; carga real
   con `LoadLibraryExW`, resolución de todos los exports públicos F04/F05 y lectura
   real de `f04_core_sha`. Hash SHA256 de la DLL y SHA Core coincidentes.
4. Stage copia solo el harness, headers e import library/DLL propios al laboratorio.
   UBT construye `F05OrdersLabEditor Win64 Development` con `-WaitMutex
   -NoHotReload -MaxParallelActions=4`. Conservar la salida UBT/UHT real; el módulo
   no declara UClasses propias, por lo que puede no haber generación UHT adicional.
   No declarar compilación UHT por deducción de una revisión estática.
5. Carga del módulo con `bridge ready=1`, sin DLL antiguas ni símbolos faltantes.
6. Las **12** automatizaciones siguientes, primero NullRHI diagnóstico y después
   con RHI real, todas en estado `Success`. El runner comprueba nombres exactos,
   duplicados, número, `notRun` y fallos, además del código de salida del editor.

## Inventario Unreal revisado

Se revisaron las fuentes y las declaraciones ABI disponibles en Cloud. El
[inventario ejecutable](../../../../../../desarrollo/integration/f05/unreal/expected-tests.json)
y `check_unreal_preparation.py` verifican 12 nombres únicos y 25 llamadas ABI
declaradas. Eso **no compila Unreal ni verifica sus overloads, UBT/UHT o RHI**.

| Test | Aceptación observable |
|---|---|
| `F05.P01.LifecycleAndRecovery` | Orden, aceptación, efecto Core real, futuro idéntico tras restaurar y replay sin efecto adicional |
| `F05.P01.Negatives` | Autoridad/cualificación/operación incorrectas rechazadas; colisión conserva estado |
| `F05.P01.WorldAndActorIndependence` | Destruir Actor/UWorld conserva orden y permite ejecución nativa |
| `F05.P02.DelegationRevocationRecovery` | Revocar antes del efecto, `performed=0`, recuperación y replay exactos |
| `F05.P02.ModesAndLimits` | Propuesta pendiente, autoaprobación denegada, aprobación real, subdelegación denegada |
| `F05.P02.ExpiryAndChainOfCommand` | Origen revocado y límite temporal exacto bloquean ejecución |
| `F05.P03.NPCInitiativeAndOrders` | Servicio auténtico, detección/decisión/orden y resultado `0xF0401` de Core |
| `F05.P03.AuthorityAndKnowledge` | Conocimiento no compartido, XO sin atribución propone, jugador no autoaceptado |
| `F05.P03.OffscreenPersistenceAndRecovery` | Bytes y futuro equivalentes con/sin UWorld, replay exacto |
| `F05.P04.AIProposalValidation` | JSON corrupto rechazado, propuesta válida sin ejecución, handoff P03 explícito |
| `F05.P04.StaleAuthorityAndFallback` | Cambio médico invalida respuesta; timeout simulado deja autonomía determinista operativa |
| `F05.P04.OffscreenRecoveryAndSafety` | Actor/UWorld prescindibles, resultado real retenido y ninguna duplicación tras restaurar |

No añadir reparaciones, contactos F06, personalidad, memoria social, servicios
permanentes ni progreso offline. P05A añade comprobaciones nativas que complementan
las 12 pruebas UE; no introduce supuestas automatizaciones UE nuevas.

## Tiempo, recuperación y continuidad

Ver en los JUnit nativos de **ambas repeticiones**:

- `f05.p05a_J_time`: espera real y timeout de transporte sin avanzar juego;
  cargar conserva tick y bytes; `f04_advance(10)` no autoejecuta F05 y el Host
  evalúa explícitamente; retroceso temporal rechazado. Pausa significa que el
  Host deja de avanzar el reloj Core: F05 no incorpora un subsistema de pausa UE.
- `f05.p05a_I_process_save/load`: productores/consumidores son procesos CTest
  distintos. Orden emitida, aprobación requerida, aceptación, propuesta aplicada,
  petición externa pendiente retirada, scopes nuevos y futuro/RNG exactos.
- P01–P04 `process_save/load`, tests `history/history_fault`, publicación incierta
  y recuperación: verificar todos, no ejecutar solo el test con nombre recovery.
- Los tests de capacidad y colisiones deben conservar estado previo/RNG y no
  ampliar autoridad. Alcanzar topes persistentes bloquea nuevas entradas del
  subsistema correspondiente; no existe retención F05 ilimitada.

Para diagnóstico individual, conservar el laboratorio fallido y ejecutar en
**otra salida nueva** la suite nativa; para aislar un test en un build ya creado,
usar CTest con `--output-junit` nuevo. Los fixtures `process_save/load` deben
seleccionarse juntos y no sobrescribir una historia preexistente:

```powershell
ctest --test-dir "$Output/clean-1/native" -C Release -N
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite P04 `
  -CoreSource $Core -BuildRoot "$Output/clean-1" -EngineRoot $UE
```

## Evidencias y diagnóstico PASS/FAIL

| Evidencia | Ruta relativa a Output | FAIL / diagnóstico |
|---|---|---|
| Estado global de la ejecución y entorno | `acceptance.json`, `windows.json` | INCOMPLETE o SHA/versiones distintos: conservar salida y corregir checkout/requisitos |
| Core completo | `core-1/`, `core-2/`: `run.json`, `tests.xml`, logs y `build/CMakeFiles/*/CMakeCXXCompiler.cmake` | Test ausente/fallido: leer tests.log y LastTest.log; no actualizar pin para obtener PASS |
| MSVC y nativos | `clean-1/`, `clean-2/`: `logs/*configure.log`, `*build.log`, `*native-tests.log`, `*-native.xml` | Compilación: revisar primera causa MSVC, SDK y arquitectura; fallo de test: conservar XML y payload de prueba |
| DLL real | `clean-*/logs/dll-exports.txt`, `dll-dependents.txt`, `dll-load.json` | Error 126: dependencias/rutas; 193: arquitectura; export o SHA incorrectos: staging/build equivocado; crear laboratorio nuevo |
| UBT/UHT | `clean-*/logs/*ue-build.log`, `clean-*/ue/Saved/Logs/` | Primera causa de compilación/enlace; confirmar versión y headers staged; no tocar instalación UE ni arte |
| Automatización | `clean-*/*-ue-report/index.json`, demás archivos del reporte y `logs/*ue-tests.log` | Código !=0, test ausente/duplicado, estado distinto de Success o conteo !=12: FAIL; no confundir queue vacía con éxito |
| RHI real | Último log `*ue-tests.log` de cada clean-* y logs del editor | Confirmar adaptador hardware y D3D/Vulkan efectivo. NullRHI, WARP/software, fallo de driver o ausencia de evidencia hardware no acreditan RHI real |
| Integridad de entrega | `evidence-sha256.json` | Hash o archivos incompletos: no certificar; reconstruir evidencia desde originales conservados |

`PASS` automatizado exige completar ambas repeticiones. La aceptación definitiva
exige además revisión de logs de hardware RHI, advertencias y acta del propietario.
No declarar UE5_JUGABLE, F05 CERRADA ni desbloquear F06 desde el resultado automático.
Si una etapa falla, `acceptance.json` queda INCOMPLETE; no limpiar la evidencia.
Tras corregir una causa, repetir todo en otra salida nueva para certificar.

Publicar después únicamente las evidencias aprobadas y verificadas en un
directorio permanente nuevo bajo `evidence/F05-P05B/`, con fecha, equipo,
comandos, SHAs, compilador/SDK/UE/CL, recuentos exactos, resultados por prueba,
logs, XML, reportes Automation y hashes. Actualizar el
[registro central](REGISTRO_VALIDACIONES_MSI.md) solo con ejecuciones reales.
Los laboratorios no se versionan y no son dependencias del producto; no borrarlos
sin autorización. La auditoría independiente de ChatGPT sigue siendo un paso
separado de cualquier aprobación de fusión.
