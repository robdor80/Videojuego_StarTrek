# Reparación del editor StarTrekRPG — UE 5.8.4

Fecha: 20 de noviembre de 2026. Alcance: preparación nativa, compatibilidad y creación de recursos desde el editor del proyecto existente. Procedimiento reproducible: [README de StarTrekRPG](../../../../juego/UE5/StarTrekRPG/README.md).

**Resultado:** Editor y Game compilan con UE 5.8.4, la copia principal abre y el navegador vuelve a ofrecer creación de recursos. En la copia aislada se crearon, guardaron y recuperaron los recursos exigidos, incluido el diseñador UMG. HOST mantiene su integración: 111/111 pruebas nativas y flujo H06 con persistencia en NullRHI/D3D12 correctos. Los cinco criterios de aceptación quedan cubiertos por las comprobaciones enumeradas abajo, dentro del alcance indicado.

## Causa raíz

Se encontraron dos problemas independientes y una instrucción de apertura ambigua:

1. **Perfil de plugins insuficiente para autoría.** `StarTrekRPG.uproject` contiene `DisableEnginePluginsByDefault=true` y únicamente habilitaba `WindowsDeviceProfileSelector`. Esto deja fuera proveedores y servicios que el editor necesita. Se reprodujo el navegador vacío, sin carpetas y con Añadir desactivado, aun existiendo el mapa de diagnóstico. Editar tampoco ofrecía Complementos. El problema se reprodujo con la instalación 5.8.4 antes de cambiar el descriptor; no fue necesario reinstalar el motor.
2. **Dependencias nativas ausentes en la copia de conversión.** El registro UBT del 19 de noviembre identifica `juego/UE5/StarTrekRPG 5.8/Source/StarTrekRPG/StarTrekRPG.Build.cs`. Esa copia no contiene la preparación en `Binaries/Host`; UBT aborta al instanciar las reglas, antes de compilar C++. La copia principal sí conservaba el header y las DLL de la ejecución anterior. La corrección es preparar HOST para el `ProjectDir` exacto que se va a compilar, manteniendo el pin Core existente.
3. **El README solo mostraba apertura con `-game`.** Ese modo ejecuta el diagnóstico, pero no abre las herramientas de autoría. Se documentan por separado la apertura del editor y la ejecución del juego.

Las carpetas físicas vacías y las imágenes/audio copiados desde Windows son un asunto distinto. El navegador puede ocultar carpetas vacías y solo registra recursos Unreal importados; los PNG/JPEG/MP3 originales no son `.uasset`. No se importaron ni modificaron los originales para resolver este incidente.

## Reparación aplicada

Se conserva el perfil restringido de plugins y se añaden referencias con `TargetAllowList: ["Editor"]`:

| Plugin | Función verificada |
| --- | --- |
| `ContentBrowserAssetDataSource` | Carpetas, recursos, Añadir e Importar |
| `ContentBrowserClassDataSource` | Árbol de clases C++ |
| `EngineAssetDefinitions` | Tipos y acciones de recursos del motor, incluidos Blueprint y Material |
| `PropertyAccessEditor` | Soporte necesario para abrir/compilar UMG y recursos de animación |
| `PluginBrowser` | Editar > Complementos |

Durante la validación se descubrió un cierre real al abrir el Widget Blueprint sin `PropertyAccessEditor`. Se preservaron el log y el minidump. La dirección del fallo en `UnrealEditor-AnimGraph.dll` cae en `UAnimBlueprintExtension_PropertyAccess::HandleStartCompilingClass` al contrastarla con los exports del DLL instalado. El descriptor `PropertyAccessEditor.uplugin` indica expresamente que este servicio es necesario para UMG y animación. Después de habilitarlo, el mismo widget guardado volvió a abrir en su diseñador. No se modificaron fuentes ni binarios del motor.

`Prepare-Host.ps1` sigue utilizando el CMake existente y sus controles de pin/limpieza. Se comprueba la presencia de ambos DLLs Release antes de cambiar la preparación del proyecto y se imprime el destino exacto. `StarTrekRPG.Build.cs` conserva las dependencias y el staging NonUFS; sus errores ahora incluyen la ruta que falta e instrucciones de `-ProjectDir`. Se actualiza el README a 5.8.4, con comprobación de `Build.version`, preparación, Editor/Game, generación del mapa y apertura correcta.

No se modificó la arquitectura HOST, su ABI, CoreRPG, la lógica del juego, los contratos ni las pruebas existentes. No se añadieron plugins de scripting ni contenido de la introducción.

## Entorno y copias

- Repositorio utilizado: raíz de trabajo exigida por `AGENTS.md`, `C:/Users/andro/Documents/GitHub/Videojuego_StarTrek`.
- Base de reparación: `origin/main` en `f9074d28c`, tras consultar el remoto. La rama inicialmente abierta era `feature/host-h06-ue-m1`, anterior a cambios HOST ya integrados. Se conserva esa rama y se trabaja en `codex/ue584-editor-repair-main-20261120`.
- Proyecto definitivo: `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`. La copia `StarTrekRPG 5.8` permanece intacta. Su asociación GUID de conversión no se reutiliza; se lanza el ejecutable instalado con la ruta explícita al proyecto principal.
- Motor comprobado por `Engine/Build/Build.version` y los logs de ejecución: **5.8.4**, changelist **58902052**, compatible changelist **55116800**. La asociación del proyecto sigue siendo `5.8`.
- CoreRPG existente, limpio: **76a7b7b485616d8c4994f384a90f123bf333591d**. No se cambia de revisión ni se modifica su checkout.
- Compilador detectado: MSVC **14.51.36256**, x64; generador CMake `Visual Studio 18 2026`. UBT avisa que su versión preferida es 14.50.35717; los targets compilados terminan correctamente.
- Los ensayos de creación de recursos se hacen sobre una copia aislada del mismo proyecto, no sobre un proyecto nuevo. Se conservan los binarios anteriores y la configuración de usuario como respaldo local. Los hashes de los archivos originales de Content y de la copia de conversión no cambian.

Las salidas brutas, respaldos, capturas, informes Automation/JUnit y volcado de crash quedan en la unidad temporal de esta tarea según `AGENTS.md`; no se incluyen en Git. Ningún archivo definitivo referencia esa unidad. Las fuentes, scripts y dependencias preparadas de la copia principal funcionan sin utilizarla como dependencia de ejecución.

## Preparación nativa comprobada

Se ejecutó el script del proyecto del repositorio, primero con `-ProjectDir` dirigido a la copia aislada y después para la copia principal. Compilación de producto **Release x64**, `TREK_HOST_TESTS=OFF`, utilizando la composición HOST/F05/F04 existente. El CMake exige el checkout Core limpio y su pin; no se sustituyeron estos controles.

`inspect_product.py` y `inspect_abi.py` existentes terminaron con código 0. Verificaron carga de DLLs, dependencias, exports, pin Core, negociación ABI 1 y ausencia de hooks de prueba/F11 trial en el producto. El header se cotejó con la fuente, y los DLLs preparados coinciden con los que UBT despliega en `Binaries/Win64`.

| Archivo | SHA-256 de la preparación verificada |
| --- | --- |
| `host_abi.h` | `E2915A5C42C82F35ED2AECFECE41CBBD50C901857D9203B870358DEF0406002A` |
| `TrekHost.dll` | `BB5A7C75C9508756F36B09FB779405E863667E0266FCE8F6256BEBB07E11D7AD` |
| `TrekF04Bridge.dll` | `65BABEFC2D9294CE014147470D115677BBF8EA495E5842DC27CBE7A1AA1CA45A` |

Los hashes identifican esta compilación local; no son pins contractuales para compilaciones futuras.

## Pruebas y resultados

| Comprobación | Resultado | Evidencia local |
| --- | --- | --- |
| Preparación nativa de producto y staging principal | PASS | `prepare-host-main.log`, `staged-sha256.json` |
| Inspección de producto y C ABI existentes | PASS | `inspect-product.log`, `inspect-abi.log` |
| Suite nativa actual `ctest -R '^host\.'`, Release, tres procesos | **111/111 PASS** | `native-tests.log`, `native-tests.xml` |
| `StarTrekRPGEditor Win64 Development`, 5.8.4 | PASS, copia aislada y principal | `ubt-editor-accepted-lab.log`, `ubt-editor-accepted-main.log` |
| `StarTrekRPG Win64 Development`, 5.8.4 | PASS | `ubt-game-accepted-main.log` |
| Generación desde ausencia de `HostDiagnostic.umap` en copia aislada | PASS, código 0 | `map-baseline.log` |
| Regeneración con mapa presente | PASS, conserva el mapa, código 0 | `map-culture-en.log` |
| H06 DiagnosticFlow con fixture, NullRHI | PASS, 1 Success, 0 failed/notRun | `report-null/index.json` |
| H06 DiagnosticFlow con fixture, D3D12 SM6 | PASS, 1 Success, 0 failed/notRun, también tras PropertyAccessEditor | `report-accepted/index.json` |
| Navegador antes/después en la misma instalación y configuración de usuario aislada | PASS: reproduce y resuelve el fallo | `browser-before.jpg`, `browser-after.jpg` |
| Apertura de la copia principal, árbol Content y Añadir/Importar habilitados | PASS, mapa H06 cargado | `editor-primary.log`, `browser-primary-after.jpg` |
| Editar > Complementos y apertura de su ventana en la copia principal | PASS | `edit-menu-primary-after.jpg`, `plugin-browser-primary.jpg` |
| Carpeta + Blueprint Actor + Material + Widget Blueprint creados desde UI | PASS, guardados como `.uasset` | `assets-reopened.jpg`, logs de SavePackage |
| Persistencia tras reiniciar y apertura de diseñador UMG | PASS | `widget-designer-after.jpg`, `editor-accepted.log` |
| Integridad de originales y copia convertida | PASS, 0 archivos alterados | `original-assets-sha256.json`, `original-assets-diff.json` |

Los recursos de prueba son `BP_EditorRepairCheck`, `M_EditorRepairCheck` y `WBP_EditorRepairCheck`, únicamente en la copia aislada. El flujo H06 utiliza su fixture existente: comprueba ciclo de sesión, proyección, persistencia, recuperación y transición entre mundos. No certifica la creación productiva de cadetes ni introduce nuevas fases de juego.

## Avisos y límites

- En cultura española aparecen 14 entradas de arranque `LogAutomationTest: Error: Condition failed`, también anteriores a la reparación. Coinciden con [UE-305638](https://issues.unrealengine.com/issue/UE-305638), relativo al formato decimal en pruebas internas. Se verificó que desaparecen con `-culture=en` en una ejecución aislada; no se alteraron las preferencias globales del usuario ni se silenciaron errores. Los informes explícitos H06 tienen 0 fallos.
- El perfil mínimo también emite avisos de recursos de compresión ACL no montados. No se han habilitado plugins ajenos a las operaciones comprobadas; el trabajo no certifica todos los sistemas opcionales de animación del motor. Los avisos de APIs internas en headers del motor y del compilador más reciente no bloquearon los builds.
- El viewport negro del mapa H06 es esperable: contiene un punto de entrada y el panel de diagnóstico aparece al ejecutar el juego. No contiene una escena artística.
- No se repitieron suites Linux/ASan, empaquetado ni auditorías históricas completas: no hay cambios nativos y el alcance de esta reparación es Windows Editor/Game. Se ejecutó la suite HOST actual completa y su consumidor Unreal.
- UBT mantiene algunas trazas en su caché estándar de usuario y Unreal utiliza cachés internas del motor. Los logs de entrega y artefactos de ensayo se redirigen a la unidad temporal; no se borraron cachés ni archivos anteriores.

## Apertura y mantenimiento

Usar los comandos del [README](../../../../juego/UE5/StarTrekRPG/README.md), en este orden: preparar HOST para el proyecto exacto, compilar Editor, generar el mapa si falta, compilar Game y lanzar `UnrealEditor.exe` **sin `-game`** para autoría. Elegir Contenido (`/Game`) como destino de Añadir y mostrar carpetas vacías cuando proceda. Reservar `-game` para probar el panel H06.

No borrar `Binaries`, `Saved`, `Intermediate` ni la copia de conversión como paso rutinario. Al reconstruir en otro equipo, repetir la preparación y el build con sus fuentes y pin; los binarios no viajan en Git. Cerrar el editor antes de recompilar las DLL que utiliza.

Referencias del motor: [proveedor de recursos del navegador](https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/ContentBrowserAssetDataSource), [Property Access Editor](https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/PropertyAccessEditor) y los descriptores `.uplugin` y reglas UBT de la instalación 5.8.4 inspeccionada.
