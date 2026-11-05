# F05-P05B — certificación integral MSI para auditoría independiente, 05-11-2026

**Resultado: dos repeticiones oficiales completas, PASS_AUTOMATED, con un SKIP POSIX permitido por repetición y una incidencia de arranque del motor reproducida en controles independientes. Pendiente de auditoría independiente de ChatGPT y acta del propietario. F05 EN_CURSO; F06 BLOQUEADA. PR #89 Draft, sin fusionar.**

## Alcance e identidades

Se ejecutó el procedimiento `desarrollo/integration/f05/run_p05b_msi.ps1` sin modificar su lógica, inventario ni criterios. Una invocación oficial comprende las dos repeticiones; no se sustituyen por diagnósticos aislados ni se reutilizan sus DLL. HEAD contrastado con la PR #89 y la rama remota antes de comenzar: `027bb1d680da1f3317dac00d23ef06e0640c14ba`, rama `codex/f05-p05b-msi-20261105`. El checkout estuvo limpio durante las ejecuciones. Los cambios posteriores de esta entrega son exclusivamente informe, conciliación documental y evidencias; no cambian las fuentes probadas.

Core separado, limpio y sin modificaciones: `76a7b7b485616d8c4994f384a90f123bf333591d`. Se conservaron el checkout del propietario, los laboratorios anteriores, los resultados symlink 3/3 previos y el primer intento bloqueado publicado en la misma PR. No se modificaron CoreRPG, motor, proyectos artísticos, modelos, seguridad permanente de Windows ni oráculos.

Entorno medido: `FATIROBERMSI`, Windows 11 build 26200, PowerShell 7.6.5, Visual Studio Community 2026 18.9.1, MSVC 19.51.36256 / toolset 14.51.36231, SDK 10.0.26100.0, CMake/CTest 4.4.3 y Python 3.10.11. UE **5.8.2**, CL **56702186**, compatible CL **55116800**. Los registros reales de entorno y los archivos de identificación del compilador acompañan el paquete.

## Procedimiento, elevación y conservación

Se creó un checkout nuevo de la misma rama dentro del laboratorio autorizado; no se abrió otra PR. Para acortar rutas se utilizó `subst P:` apuntando a ese checkout, solo durante el proceso elevado. El script retiró esa asociación al terminar. Las rutas efectivas del harness fueron `P:\laboratorios\p\clean-1\ue` y `P:\laboratorios\p\clean-2\ue`.

El lanzador solicitó UAC mediante `Start-Process ... -Verb RunAs`. El proceso comprobó el token de administrador y la creación efectiva de enlaces de archivo y directorio antes del procedimiento. Cada suite Core volvió a ejecutar las tres pruebas originales symlink, con resultado PASS en ambas repeticiones. No se alteró la política de ejecución, Developer Mode, asignación permanente de privilegios ni controles de Windows. `SeCreateSymbolicLinkPrivilege` puede aparecer deshabilitado por defecto en `whoami /priv`; la evidencia efectiva es la creación de los enlaces y los tres casos C++ ejecutados, no esa etiqueta aislada.

Comando oficial ejecutado desde Developer PowerShell 7 elevado:

```powershell
& P:\desarrollo\integration\f05\run_p05b_msi.ps1 `
  -ExpectedTrekSha 027bb1d680da1f3317dac00d23ef06e0640c14ba `
  -CoreSource '<checkout Core separado y limpio>' `
  -BuildRoot P:\laboratorios\p `
  -EngineRoot 'C:\Program Files\Epic Games\UE_5.8' `
  -Generator 'Visual Studio 18 2026'
```

Los scripts y argumentos exactos, transcripciones, UAC, entorno y estados están conservados en `execution/`. Cada repetición crea Core, build nativo, DLL, harness, datos y reportes nuevos. El runner original escribe `PASS_AUTOMATED` con dos entradas PASS. Sus campos reservados `hardware_rhi_acceptance=PENDIENTE_REVISION_LOGS` y `final_certification=PENDIENTE_ACTA` permanecen sin editar; la revisión posterior del hardware se documenta en `summary.json`, sin reescribir la evidencia original ni atribuirse el acta del propietario.

## Resultados de ambas repeticiones

| Comprobación | Repetición 1 | Repetición 2 |
|---|---|---|
| Core, inventario 483 | 482 PASS + 1 SKIP, 0 FAIL | 482 PASS + 1 SKIP, 0 FAIL |
| Tres pruebas Core symlink | 3/3 PASS, 0 SKIP | 3/3 PASS, 0 SKIP |
| F04/F05 nativa | 395/395 PASS, 0 SKIP | 395/395 PASS, 0 SKIP |
| Casos P05A incluidos | 30/30 PASS | 30/30 PASS |
| DLL nueva: exports, dependencias y carga | 62 exports, SHA Core correcto | 62 exports, SHA Core correcto |
| UBT, F05OrdersLabEditor Win64 Development | Succeeded | Succeeded |
| Módulo y DLL staged | `bridge ready=1`, hashes coincidentes | `bridge ready=1`, hashes coincidentes |
| Automatización NullRHI | 12 Success, 0 advertencias de prueba | 12 Success, 0 advertencias de prueba |
| Automatización D3D12 hardware | 12 Success, 0 advertencias de prueba | 12 Success, 0 advertencias de prueba |
| Errores globales de arranque por backend | 14, reproducidos en control | 14, reproducidos en control |
| Procedimiento oficial | PASS | PASS |

El único SKIP de cada suite Core es `ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt`, admitido expresamente por el procedimiento Windows por la semántica de permisos POSIX. Se conservan el mensaje, el XML y `PASS_COMPATIBLE_WITH_PLATFORM_SKIP`. **No son 483 PASS ni una prueba de ACL Windows.** Las tres pruebas `ContentPackLoaderSymlinkTest.*` figuran ejecutadas en cada XML.

Los 395 casos incluyen los 30 P05A, `f05.p05a_J_time`, cancelación por sucesor, rechazo de plazo manipulado, límites, autoridad, privacidad, revocación, idempotencia, historial y recuperación productor/consumidor en procesos separados. Las exclusiones históricas del runner —seis campañas largas y once diagnósticos monolíticos/fixtures de persistencia— se mantienen excluidas; no se presentan como ejecutadas por esta certificación. El inventario por caso está en los JUnit y en el resumen.

Cada uno de los cuatro reportes Unreal contiene exactamente los 12 nombres de `expected-tests.json`, sin duplicados, `notRun`, fallos ni estados distintos de Success. Se acredita el harness técnico, las operaciones Core que verifican esas automatizaciones y su funcionamiento con/sin UWorld; no se acredita interfaz artística ni `UE5_JUGABLE`.

## DLL, compilación y hardware

La sonda oficial carga cada DLL nueva mediante `LoadLibraryExW`, resuelve sus **62 exports** públicos y lee `f04_core_sha`. `dumpbin /EXPORTS` y `/DEPENDENTS` quedan conservados. La revisión posterior compara SHA256 entre la DLL nativa, `ThirdParty/Win64` y `Binaries/Win64` en cada repetición. Los hashes concretos de ambas DLL se incluyen en `summary.json` y `clean-*/logs/dll-load.json`; las DLL no se publican.

UBT compila el target real con `-WaitMutex -NoHotReload -MaxParallelActions=4`. Se preserva su salida íntegra. UHT se describe solo en la medida registrada por los logs, sin deducir una generación adicional de código a partir de la existencia del target. Se mantienen visibles los avisos de toolchain más nuevo que el preferido, compatibilidad de orden de includes y deprecaciones que emita el motor. No se cambia el compilador ni UE para ocultarlos.

En ambas compilaciones nativas quedan visibles C4805 en `f05_initiative_tests.cpp:26` por comparación entre `uint32_t` y `bool`, y C4838 en `f05_ai_tests.cpp:98` por conversión de `F05AiRoute` a `uint32_t`. Cada arranque NullRHI oficial avisa del directorio Content inexistente del harness; cada arranque hardware avisa sobre `r.MotionVectorSimulation` en el render thread. El control también conserva un aviso de layout del editor. No aparecen otras líneas de categoría `Error:` en los cuatro logs oficiales además de las 14 estudiadas por arranque. Los avisos se conservan en los logs íntegros y en las listas del resumen. Cero advertencias en los reportes de automatización no significa cero advertencias en todo el proceso.

Los dos logs de hardware seleccionan **D3D12, SM5, adaptador 0 NVIDIA GeForce RTX 4070 Laptop GPU**, driver **617.14 / 32.0.16.1714**. Se comprueba `Chosen D3D12 Adapter Id = 0` y `RHI D3D12 ... will be used`, no solo que se enumere una NVIDIA. La enumeración del Microsoft Basic Render Driver no significa que se haya usado. NullRHI queda identificado por separado.

## Investigación de los 14 errores de arranque

Se creó `EngineControl.uproject` sin módulos de proyecto, sin código ni DLL F04/F05 y sin comando `Automation RunTests`. Se arrancó con la misma instalación, opciones de diagnóstico y ambos backends. Comando de salida: `-ExecCmds=QUIT_EDITOR`. Ambos controles terminaron con código **0** y reprodujeron **14** líneas idénticas `LogAutomationTest: Error: Condition failed` **antes de `LogEngine: Initializing Engine...`**. Ninguno carga `F05OrdersLab` ni emite `bridge ready=1`. El proyecto, argumentos y logs completos se publican en `engine-only/control-v2/`.

La incidencia se reproduce en el arranque de la instalación de **Unreal Engine sin nuestras automatizaciones**; no la causa la cola F05 ni la DLL del puente. Los cuatro arranques oficiales reproducen el mismo grupo anterior a la inicialización del motor. La revisión conserva las otras líneas de error y advertencia en el resumen para evitar reducir todo el log a esta incidencia.

El header local `Engine/Source/Runtime/Core/Public/Misc/LowLevelTestAdapter.h`, línea 130, contiene un macro `CHECK` que emite ese texto. Es una pista, **no una identificación de la aserción concreta**: no hay traza de pila recogida ni fuentes `.cpp`/PDB del módulo Core en esta instalación. La proximidad a mensajes `UE::UnifiedErrorTest` tampoco demuestra por sí sola un mismo origen. No se afirma que los 14 mensajes sean inocuos ni se presenta un arranque sin errores. No se modificó el motor, desactivaron plugins, cambiaron categorías de log ni suprimieron errores esperados para obtener el resultado.

## Incidentes de preparación conservados

1. El primer control usó `-ExecCmds=Quit`, que no terminó el editor. Se detuvo exclusivamente el PID identificado del control, se conservó su log con salida forzada y no se contó como control completado. El control corregido con `QUIT_EDITOR` se ejecutó en otro directorio y cerró normalmente en ambos backends. No había comenzado la suite oficial.
2. El primer intento oficial de esta continuación (`o`) completó Core con 482 PASS + 1 SKIP, pero la configuración F04/F05 falló porque el checkout parcial omitía los datos de catálogo de `mundo/` y el contrato de `sistemas/`. Se completó el checkout con los archivos originales del mismo HEAD, sin cambios versionados, y se validó el generador del catálogo antes de continuar. Ese intento conserva INCOMPLETE y **no cuenta como repetición aceptada**. El procedimiento se ejecutó completo desde cero en la nueva salida `p`; no se mezclaron sus resultados ni binarios con `o`.

Estas incidencias de preparación están documentadas con sus registros; no se atribuyen a defectos del producto ni se borran para presentar una ejecución sin incidentes.

## Evidencia y entrega a ChatGPT

[Resumen estructurado](evidence/F05-P05B/20261105-MSI-INTEGRAL/summary.json) · [Manifiesto SHA256](evidence/F05-P05B/20261105-MSI-INTEGRAL/SHA256SUMS.json) · [Aceptación original](evidence/F05-P05B/20261105-MSI-INTEGRAL/acceptance.json).

El paquete contiene logs íntegros, JUnit originales, cuatro reportes Automation originales, versiones, carga DLL, controles, scripts de ejecución y validación, e incidentes de preparación. Se copió cada archivo sin normalizar bytes y se comprobó contra su original. `.gitattributes` limita `-text` al paquete. `SHA256SUMS.json` recoge ruta relativa, bytes y SHA256 de cada archivo salvo el propio manifiesto. `evidence-sha256.json` es el índice original del runner sobre el laboratorio completo; puede referir archivos de compilación que deliberadamente no se publican. No confundir ambos inventarios.

El laboratorio local nuevo es `laboratorios/f05/p05b/official-20261105/` en el repositorio del propietario. Conserva los checkouts de prueba, las salidas completas y los controles. Los laboratorios anteriores permanecen intactos. No hay dependencias de ejecución del juego hacia estos archivos; el laboratorio completo es prescindible para el producto, pero se conserva para la auditoría y no se borra. UE/UBT también usan sus cachés y registros compartidos de AppData/Zen; no se limpiaron.

La auditoría independiente debe comprobar: identidad del HEAD y ausencia de cambios de fuentes posteriores; 483 descubiertos con el SKIP nominal explícito y symlink 3/3 en ambos XML; 395 nativos y fixtures reales por repetición; dos DLL nuevas y coherencia staged; UBT real; cuatro reportes de doce nombres exactos; selección hardware; controles sin nuestro módulo y errores globales conservados; integridad del paquete y límites de aceptación. La CI del commit documental final, si se activa, se evalúa por separado y no se presume verde.

**La doble ejecución automatizada exigida por P05B está completada. La auditoría independiente y el acta de aceptación siguen pendientes. Esta entrega no fusiona la PR #89, no cierra F05 y no desbloquea F06.**
