# F05-P03 — Continuación en MSI, pendiente

Todas las comprobaciones de este documento están **PENDIENTES**. Cloud no dispone
de la instalación del propietario de Unreal Engine 5.8.2. CI Windows verifica la
integración nativa en un runner, no acredita UE, UWorld, RHI ni ejecución en el MSI.
Conservar P01/P02 y el [registro centralizado](REGISTRO_VALIDACIONES_MSI.md).

## Prerrequisitos y rutas

Obtener la rama `codex/f05-p03-npc-initiative` y registrar su SHA exacto. Core debe
estar en un checkout limpio y separado, **detached** en
`76a7b7b485616d8c4994f384a90f123bf333591d`. No cambiar Core main ni reutilizar
binarios de P01/P02. CMake >=3.25, Python 3, Git, Visual Studio 2026 con MSVC x64 y
Windows SDK, y la instalación real UE **5.8.2**. El script verifica los tres
componentes de `Engine/Build/Build.version`; no editar ese archivo para pasar.

Desde la raíz Star Trek, definir `$CoreSource` con la ruta del checkout Core,
`$EngineRoot` con la instalación UE y `$BuildRoot` con **un directorio nuevo** ASCII
bajo la carpeta de laboratorios permitida del repositorio, exclusivo para P03.
Definir `$CleanBuildRoot` con otro directorio nuevo para la repetición limpia.
No usar proyectos artísticos, laboratorios anteriores ni borrar contenidos.

```powershell
git rev-parse HEAD
git -C $CoreSource rev-parse HEAD
git -C $CoreSource diff --exit-code HEAD
Get-Content "$EngineRoot/Engine/Build/Build.version"

# Compilar, probar nativamente, copiar el harness aislado, UBT/UHT y nueve tests UE.
./desarrollo/integration/f05/run_f05.ps1 -Stage All -Suite All `
  -CoreSource $CoreSource -BuildRoot $BuildRoot -EngineRoot $EngineRoot

# Selección por suite, sobre los binarios recién compilados.
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite P01 -CoreSource $CoreSource -BuildRoot $BuildRoot -EngineRoot $EngineRoot
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite P02 -CoreSource $CoreSource -BuildRoot $BuildRoot -EngineRoot $EngineRoot
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite P03 -CoreSource $CoreSource -BuildRoot $BuildRoot -EngineRoot $EngineRoot

# Carga con el RHI real; se omite NullRHI explícitamente.
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite All -RealRHI `
  -CoreSource $CoreSource -BuildRoot $BuildRoot -EngineRoot $EngineRoot

# Repetición integral desde cero, sin copiar DLL/datos del primer laboratorio.
./desarrollo/integration/f05/run_f05.ps1 -Stage All -Suite All `
  -CoreSource $CoreSource -BuildRoot $CleanBuildRoot -EngineRoot $EngineRoot
```

`-Stage Native -Suite P01/P02/P03/All` también filtra los tests nativos. `All` añade
las regresiones F04 cortas. Las seis campañas históricas conservan su workflow y
Core histórico original; no cambiar sus pins para esta ejecución.

El harness generado está en `$BuildRoot/ue/F05OrdersLab.uproject`; las DLL se copian
a `ThirdParty/Win64` y `Binaries/Win64`, las cabeceras a `ThirdParty/include`.
Los binarios nativos están en `$BuildRoot/native/f04/Release`. Logs con fecha en
`$BuildRoot/logs`; reportes en `$BuildRoot/<fecha>-ue-report/index.json` y JUnit
nativo en `$BuildRoot/<fecha>-native.xml`. TEMP/TMP se redirigen durante el script.

## Criterios de aceptación

- **MSVC/ABI/DLL:** build completo sin símbolos faltantes; comprobar exports
  `f05_bind_player`, `f05_scan_need`, `f05_brief_need`, `f05_evaluate` y
  `f05_decisions_page`, además de P01/P02. Registrar versión del compilador y SHA
  Core real. El módulo debe registrar `F05 P01/P02/P03 bridge ready=1`.
- **UBT/UHT/carga:** `F05OrdersLabEditor Win64 Development` compila y carga en UE
  5.8.2, sin modificar originales ni depender de un proyecto artístico.
- **F05.P03.NPCInitiativeAndOrders:** servicio F04 real → obligación autorizada y
  comunicación → detección → decisión del capitán NPC → petición/orden P01 →
  recepción NPC → tarea/intento/resultado. `performed=1`, stream `0xF0401`, una
  tirada entre 1 y 100. No se espera un contacto de sensores.
- **F05.P03.AuthorityAndKnowledge:** necesidad desconocida no habilita acción;
  informar a otro NPC no comparte conocimiento; XO propone sin autoridad de
  capitán; una orden al jugador permanece `issued`, sin tarea ni efecto automático.
- **F05.P03.OffscreenPersistenceAndRecovery:** ejecutar con UWorld/Actor de prueba,
  destruirlos, restaurar la misma campaña y ejecutar sin escena. Misma entrada,
  semilla, revisión y tiempo → mismos bytes, IDs y RNG. Restaurar el resultado y
  repetir la evaluación no añade eventos ni efectos.
- **Integrales:** nueve pruebas UE exitosas, ninguna omitida/no ejecutada y cero
  fallos; repetir en directorio nuevo. `P01`, `P02` y `P03` esperan tres cada una.
  NullRHI permite comprobar lógica, no certifica carga con RHI real ni gráficos.

Publicar posteriormente evidencia verificable: fecha/equipo, SO, motor/CL,
compilador, SHAs, comandos, código de salida, recuentos, `index.json`, XML y logs.
Solo entonces actualizar casillas individuales del registro centralizado.
La preparación del harness y una CI verde nunca equivalen a PASS en este documento.

F05 continúa abierta. **F06 bloqueada** hasta todas las pruebas obligatorias F05
y la auditoría final P05 autorizada en otra entrega. No iniciar P04/P05 aquí.
