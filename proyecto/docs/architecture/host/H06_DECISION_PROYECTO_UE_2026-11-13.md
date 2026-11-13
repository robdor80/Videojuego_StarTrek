# H06 — Decisión pendiente sobre el proyecto Unreal principal

Fecha: 2026-11-13. Base `main` `5f12d9c152dd0003a6d971068d693184f45b213e`, [PR #141 fusionada](https://github.com/robdor80/Videojuego_StarTrek/pull/141). **G0 BLOQUEADA por aprobación del usuario.** No se identificó un descriptor principal autorizado. El árbol Git de `juego/UE5/StarTrekRPG/` solo tiene [README.md](https://github.com/robdor80/Videojuego_StarTrek/blob/5f12d9c152dd0003a6d971068d693184f45b213e/juego/UE5/StarTrekRPG/README.md); el checkout local contiene el README y las carpetas reservadas sin archivos adicionales.

## Inventario de solo lectura

Se examinó `git ls-tree -r` en el SHA base y se buscaron descriptores incluso ignorados con `rg --files --hidden --no-ignore -g '*.uproject'` en Documents (incluye checkout, worktrees, laboratorios y respaldos), Desktop, Downloads, las raíces locales de integración `C:/F03`, `C:/F04*`, y `C:/tmp`, `C:/Games`, `C:/ORDEN_PC`. Se agruparon 117 rutas locales por 17 SHA-256 de descriptor. El volumen de red R: no proporcionó inventario. La asociación de todos los candidatos Star Trek es `5.8`; el parche se verificó por separado en el motor. Los tamaños siguientes son del descriptor local, sin estimar su árbol de assets.

| Origen, tipo y estado Git | Descriptor, bytes, SHA-256 | Dependencias declaradas y coste de reutilización |
|---|---|---|
| `desarrollo/integration/f02/unreal/`, laboratorio versionado; copias F02/F03/F04 en `C:/F03`, `C:/F04*`, Documents/ChatGPT y worktrees | `F02CoreLab.uproject`, 292, `b02b2cfa94549c95db900ecf91e2d9f9bace0fa126c726044c8245cd8264bce2`; variante histórica 285, `a8ce36cb043d3b4f21003191895b0addd1909fd03609c6cfc2365ad3e3a188bf` | Módulo F02CoreLab y TrekF02Bridge. La variante F04 usa la misma base de laboratorio y puentes F02/F03/F04. Referencia de ciclo de vida y UBT; promoverla arrastraría código y fixtures ajenos a la campaña principal. |
| `desarrollo/integration/f05/unreal/`, laboratorio versionado y copias de pruebas en `laboratorios/f05/` | `F05OrdersLab.uproject`, 232, `1ed00b8d19cc1ff30c0b793ab72b13b7d6ba2f8a75050e5cdf684019596350cc` | F05OrdersLab, DLL TrekF04Bridge, fixtures de órdenes. El patrón de staging es reutilizable; la promoción requeriría sustituir la composición del laboratorio. |
| `juego/Clase Miranda/puente/unreal/Sutherland_Ergonomia03_ParteA/Unreal/`, escena versionada y copia protegida en `TABULA RASA COPIA SEGURIDAD/06_PROYECTO_UE_REUTILIZABLE/Unreal/` | `SutherlandPlayable01.uproject`, 1032, `8febafea2264a6752016c6800d63f39e7d5f827a2f56e7e9da37e1602f13e1aa` | F07P02, ChairAutoLab, ChairAutoLabEditor, STAutomaticDoors, PythonScriptPlugin, GeometryScripting, ProceduralMeshComponent, ModelingToolsEditorMode y EditorScriptingUtilities. Migrar paquetes requiere auditoría de referencias, plugins y licencias. |
| `TABULA RASA COPIA SEGURIDAD/08_VALHALLA_SEPARACION_PLATILLO_CUERPO/RECURSOS_CON_ESTRUCTURA_ORIGINAL/`, respaldos locales ignorados. Mismo descriptor en respaldos F07 y descarga `mi_puente` | `Galaxy_M11_Test.uproject`, `Galaxy_M11_Visual_HQ.uproject`, 227 cada uno, `08a75645ecdc6b96b0ac03c9ec6c27134101de59e3f533bdaa78641c76d1df49` | ModelingToolsEditorMode. El manifiesto conserva procedencia y auditoría de paquetes pendiente. Coste de migración sin medir. |
| `PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/`, siete escenas versionadas y variantes en `laboratorios/valhalla/` | `ValhallaComputer.uproject`, 366–825 bytes. Huellas por revisión abajo. | ValhallaComputer, ValhallaDoors, PythonScriptPlugin, EditorScriptingUtilities. Revisiones posteriores incorporan EnhancedInput y GameplayStateTree; V08 añade DLSS y StreamlineNGXCommon. Las revisiones dependen de escenas y paquetes propios. |
| `laboratorios/Enterprise_G/UE5_Paseo_D_E/` y `UE5_RedSur_Quinn_20261109/`, paseos locales ignorados | `EnterpriseG_Paseo.uproject`, 456, `223d143b43e6fc85d9a7a3f48459f3dc89d2a8d700f7d4ee1b6e4e487810764c` | EnterpriseG_Paseo, EnhancedInput, PythonScriptPlugin y EditorScriptingUtilities. Dependencias de contenido por auditar. |
| `proyecto/docs/roadmap/master/fases/F05/evidence/F05-P05B/20261105-MSI-INTEGRAL/engine-only/{control,control-v2}/`, controles versionados y copias locales | `EngineControl.uproject`, 151, `17cb7d838b1e1716c6bcfc8acf373fbb1810507642ad569f0cf6b47a1b4f3c3d` | Descriptor de control del motor sin módulo de juego ni integración HOST. |

Valhalla, huellas locales SHA-256 de los descriptores versionados y variantes locales adicionales:

| Revisión | Bytes | SHA-256 |
|---|---:|---|
| V05 | 367 | `ac6005fbe51b28c14a0307a87195a170a3c97f9018a877d15c6ff174b6946b41` |
| V06 | 660 | `73baf10ef20d4ca8a38667be456d1d5964b01da20cf39c8b79b6869798286b81` |
| V07 | 674 | `3b7d7b70b37093fbf50ad3465505d3c6bf6352cd3ec2fcbafa9d3e301541c438` |
| V07 Cerramientos R01 | 738 | `fd0e3adb62d27016746dc98d813080b9a6da2932d5a1894e39012b2cec3d2df9` |
| V07 Corregida | 708 | `a403cff07b421484fbc58725b3be98dc37f2072930a883f944383d9ec4089811` |
| V07 Funcional | 690 | `dceb2e13793185bac1ca405bba18bff008ba8efe8be0a660eed0640ef1ab7ef9` |
| V08 Auditoría | 825 | `80c565ff6906a1621094ae5722a2ecbf7f47d613d82b250caa08116be26f97d5` |
| Local V05 | 366 | `349a963e24c0ed249b1d8e29fb83311e3f14cad5970404549195ac3215437c09` |
| Local V06 | 683 | `0dea70bd902c7fa88f347732e804a8e756c9188f5706e9af2bd310a2c7107e69` |
| Local V07 | 671 | `a758f46d2cb09806853f87ac7ea1e54dc3d0cdd2d5c8e79d99f66d0fbb29d9e2` |

El otro descriptor agrupado corresponde a NimroelRPG, otro repositorio. Referencias de procedencia: [árbol base](https://github.com/robdor80/Videojuego_StarTrek/tree/5f12d9c152dd0003a6d971068d693184f45b213e), [manifiesto de recursos Unreal](https://github.com/robdor80/Videojuego_StarTrek/blob/5f12d9c152dd0003a6d971068d693184f45b213e/desarrollo/manifests/reorganizacion_20261027/recursos_unreal_locales.json).

## Entorno y propuesta

Windows 11 Pro 10.0.26200, MSI Raider GE78 HX 14VGG, i9-14900HX, RTX 4070 Laptop driver 32.0.16.2114, 34 116 366 336 bytes de RAM. Unreal instalado en `C:/Program Files/Epic Games/UE_5.8`, `Build.version` 5.8.2, changelist 56702186, compatible 55116800, rama `++UE5+Release-5.8`. Presentes `Build.bat` y `UnrealEditor-Cmd.exe`. Visual Studio 18 Community, MSVC 19.51.36256.0 y SDK 10.0.26100.0 identificados por CMake. La compatibilidad efectiva de UBT con ese toolchain queda pendiente de ejecución.

Se propone **crear un proyecto C++ mínimo Win64 en `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`**, asociación 5.8 y verificación de parche 5.8.2. Usaría targets Editor y Game, un módulo runtime con `UGameInstanceSubsystem` y un mapa propio pequeño de diagnóstico. La primera etapa requiere fuentes, configuración y el mapa de prueba. Los dos DLLs del build Release de producto se prepararían en staging relativo al proyecto, reutilizando el motor y Core existentes. La migración de assets y plugins artísticos tendría coste cero en este corte; para una futura migración quedan pendientes licencia, dependencias y coste real. El coste de mantenimiento inicial es sostener los targets, el empaquetado Win64 y la automatización UE del proyecto principal. El motor y los builds siguen siendo instalaciones/artefactos externos a Git.

**Aprobación pendiente.** La propuesta está lista para decisión del usuario. El descriptor, el módulo y las pruebas de Unreal están pendientes de G0. El bootstrap productivo del cadete sigue siendo una dependencia separada para nueva campaña vinculada y órdenes de jugador.
