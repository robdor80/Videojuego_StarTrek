# F05-P05B — acta de ejecución MSI, 05-11-2026

**Estado general: BLOQUEADA. No certificada. F05 permanece EN_CURSO y F06 BLOQUEADA.**

Se ejecutó el runner oficial en el MSI real. Su primera repetición se detuvo al rechazar tres SKIP no admitidos por falta de privilegio para crear enlaces simbólicos. No se elevó la sesión, no se cambió Windows ni se amplió la lista de omisiones. Las comprobaciones independientes posteriores permiten diagnosticar DLL y Unreal, pero no sustituyen las dos repeticiones completas.

## Identidades y entorno

- Base remota y fuentes nativas probadas: `486099abd36c18c5ee69c38cd43a95b95910cc5f`, `main` comprobada con fetch. PR #87 fusionada; su merge `d1d4c409a5cc5b66da911c942978d37bf3bab1d0` es antecesor. Las fuentes F04/F05 coinciden con la entrega final P05A `8e37b706cd1fabd2944b1095cfaa8a521b7e3c63`.
- Rama aislada: `codex/f05-p05b-msi-20261105`. Corrección final del harness: `5dcb1d47e26815258fd0c9693758411deccd1a77`; solo cambia el montaje técnico de mundos en tres automatizaciones. No cambia producto nativo, pin, contratos ni resultados esperados.
- Core independiente y sin modificaciones: `76a7b7b485616d8c4994f384a90f123bf333591d`.
- Equipo `FATIROBERMSI`, MSI Raider GE78 HX 14VGG, Windows build 26200, RAM 31,77 GiB. Espacio inicial libre: 420.798.971.904 bytes.
- Visual Studio Community 2026 **18.9.1 / 18.9.12112.369**, generador disponible `Visual Studio 18 2026`. MSVC **19.51.36256**, toolset **14.51.36231**, Windows SDK **10.0.26100.0**.
- PowerShell **7.6.5**, CMake/CTest **4.4.3**, Python externo **3.10.11**; Python interno UE **3.11.8** y .NET UE **10.0** según logs.
- UE **5.8.2**, changelist **56702186**, compatible **55116800**, leído de `Build.version`. Motor instalado conservado.
- GitHub devolvió listas vacías para estados clásicos y workflows del SHA base consultado. No se atribuye CI verde a ese SHA a partir de esa ausencia.

## Resultados y cobertura

| Ejecución | PASS | SKIP | FAIL / pendiente |
|---|---:|---:|---|
| Core completo, 483 descubiertos | 479 | 4 | 0 tests fallidos; runner rechaza 3 SKIP |
| F04/F05 nativa | 395 | 0 | 0; incluye los 30 P05A |
| Unreal final NullRHI | 12 | 0 | 0 fallos y 0 advertencias de prueba; diagnóstico |
| Unreal final D3D12 hardware | 12 | 0 | 0 fallos y 0 advertencias de prueba; diagnóstico |
| Repeticiones completas aceptadas | 0 de 2 | — | Primera incompleta; segunda no iniciada |

El SKIP permitido es `ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt`. Los otros tres son:

- `ContentPackLoaderSymlinkTest.RejectsResourceSymlinkEscapingPackRootWhenSupported`.
- `ContentPackLoaderSymlinkTest.RejectsManifestSymlinkEscapingPackRootWhenSupported`.
- `ContentPackLoaderSymlinkTest.AllowsPackRootSymlinkWhenSupported`.

Los tres informan que el cliente no dispone del privilegio requerido. `whoami /priv` no muestra `SeCreateSymbolicLinkPrivilege`. No se acepta como PASS ni se modifica Core para ocultarlo. El XML y el `acceptance.json` original INCOMPLETE se conservan. El `run.json` de Core permanece INCOMPLETE porque el runner valida los SKIP antes de publicar sus contadores; los 479/4/0 se extraen del JUnit original.

Los 395 casos incluyen autoridad, delegación, revocación, recuperación en procesos separados, historial, idempotencia, autonomía sin proveedor remoto, rechazo de manipulación y `f05.p05a_J_time`. Los productores/consumidores fueron ejecutados por CTest con sus fixtures. No se añadieron rondas nativas redundantes tras el bloqueo.

## DLL, Unreal e incidencias

La DLL recién compilada con MSVC se inspeccionó con `dumpbin /EXPORTS` y `/DEPENDENTS`. La sonda del runner oficial, extraída sin cambiar su lógica, ejecutó `LoadLibraryExW`, resolvió **62 exports** y leyó el SHA Core fijado. SHA256 DLL: `8A0320089B8E8A77417E3AF0B15B8F44673A514EE7BAB90B792AF8BF84B8533C`. Los logs de dependencias, exports y carga quedan publicados.

1. **Rutas Windows.** El primer checkout requirió `git -c core.longpaths=true worktree add`; no se cambió la configuración del propietario. UBT rechazó después rutas de hasta 269 caracteres. Se conservaron los logs y se usó una salida más corta dentro del laboratorio para el diagnóstico; no se movió el motor. No se presenta esa salida como build nativo limpio: contiene una copia de la DLL/import library recién comprobadas.
2. **Doble inicialización UWorld.** Con fuentes originales, UBT compila y el módulo informa `ready=1`. Dos pruebas P01 terminan Success; la tercera inicia y provoca fatal `Cannot generate unique name for WorldSettings`. No se obtiene `index.json` completo: no se inventa un reporte. Las tres automatizaciones que crean mundos invocaban `CreateWorld` y después `InitializeNewWorld`. Se pasan ahora las mismas opciones por `InIVS` de `CreateWorld`, eliminando la segunda inicialización. Firma contrastada con el header local UE 5.8.2 y la [API oficial UWorld](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorld).
3. **Contexto de destrucción.** La primera corrección obtiene 12 estados Success en ambos RHI, pero tres pruebas advierten `World has no context` al destruir Actor. Se registra ahora el contexto del mundo y se libera tras destruirlo; además se exige que `Marker->Destroy()` devuelva true. Se mantiene la destrucción de UWorld y la comparación de bytes/futuro. Se conserva toda evidencia intermedia y se verifica de nuevo en una salida nueva.
4. **Herramientas.** UBT advierte que MSVC 14.51.36256 supera la versión preferida 14.50.35717, orden de includes compatible 5.6 y deprecaciones de headers del motor. No se instala otro compilador ni se modifica UE. UBT termina Succeeded en los diagnósticos cortos. El log indica `UHT compiled-in object format Default`, pero no una invocación adicional de generación UHT; no se acredita generación independiente.

RHI hardware observado: **D3D12, SM5, adaptador 0 NVIDIA GeForce RTX 4070 Laptop GPU**, 7948 MB VRAM, driver **617.14 / 32.0.16.1714**. El adaptador software también se enumera, pero el log elige explícitamente el adaptador 0. En ambos backends el módulo debe mostrar `ready=1`; ver logs y matriz final.

## Evidencias, límites y continuación

[Paquete permanente](evidence/F05-P05B/20261105-MSI/summary.json): XML originales, logs Core/nativo/UBT/Unreal, reportes Automation originales, error y contexto del crash, sonda DLL, versiones y comandos. `SHA256SUMS.json` permite verificar cada archivo del paquete. No se publican DLL, import libraries, minidumps, cachés ni laboratorios completos. Los reportes incompletos o ausentes no se convierten en PASS.

Los originales y los worktrees permanecen en el laboratorio local de esta tarea, identificado en el informe al propietario. No se borró material anterior ni se alteró la rama del propietario. Los artefactos de proyecto están aislados; UBT/UE utilizaron además sus cachés/logs compartidos de AppData y Zen, conservados sin limpieza. El juego no depende de las salidas de diagnóstico; el worktree conserva el enlace administrativo normal de Git.

**Pendiente obligatorio:** una sesión con privilegios efectivos para ejecutar los tres casos symlink y dos ejecuciones íntegras del runner oficial sobre el SHA definitivo que se audite, cada una con Core, 395 nativos, DLL nueva, UBT y las 12 pruebas en NullRHI y RHI hardware. Usar worktree/salidas más cortos dentro de la raíz autorizada. No repetir Core en la sesión actual sin resolver primero ese requisito: reproduciría la misma carencia de permisos.

**Recomendación: F05 no está preparada para cierre.** La PR es Draft para revisión del diagnóstico y de las correcciones mínimas. Auditoría independiente ChatGPT y acta final siguen pendientes. No se fusiona la PR, no se cierra F05 y no se desbloquea F06.

