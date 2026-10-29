# F02: laboratorio real CoreRPG / Unreal Engine 5.8.2

Este laboratorio enlaza **CoreRPG real**, fijado en `4f282863737bcd8f5add401202a9e1064c133672`, con un Host C++20 y un proyecto Unreal independiente. No contiene código copiado de Core, assets artísticos ni otro estado de mundo. Es un corte técnico de identidad, acciones, proyección y persistencia; no implementa la guardia de Sensores de F08.

## Repetir en Windows

Requisitos comprobados en MSI: CMake 4.4.3; Visual Studio Community 2026 18.9.1; MSVC 19.51.36256 / toolset 14.51.36231; SDK 10.0.26100.0; UE 5.8.2 CL 56702186. UBT advierte que MSVC es más reciente que el preferido, pero compilación, enlace y ejecución han pasado. Usar una ruta **ASCII** de compilación: UBA/MSVC falló al manejar `Planificación` en su ruta de PCH.

```powershell
# Ejecutar desde la raíz de este repositorio. CoreSource no se modifica.
./desarrollo/integration/f02/run_f02.ps1 -Stage All `
  -CoreSource C:/Users/andro/Documents/GitHub/CoreRPG `
  -BuildRoot C:/Users/andro/Documents/ChatGPT/F02_reproduction

./desarrollo/integration/f02/run_f02.ps1 -Stage Demo `
  -CoreSource C:/Users/andro/Documents/GitHub/CoreRPG `
  -BuildRoot C:/Users/andro/Documents/ChatGPT/F02_reproduction
```

`All` compila Core y el puente, ejecuta 15 tests nativos, prepara exclusivamente Source/Config y binarios propios en un laboratorio marcado, compila el módulo Editor y ejecuta cinco tests Unreal. `Demo` abre una ventana gráfica DX11, reproduce el ciclo, guarda una captura única y sale. La captura y los saves quedan en `ue/Saved/F02Evidence`; cada comando conserva su log con fecha. No se sobrescriben saves existentes ni se copian proyectos artísticos. No usar la misma carpeta de laboratorio desde dos ejecuciones simultáneas.

Para examinar el laboratorio: abrir `BuildRoot/ue/F02CoreLab.uproject`, o lanzar `UnrealEditor.exe <uproject> /Engine/Maps/Entry -game -dx11`. El proyecto utiliza solamente el cubo y el mapa Entry del motor instalado.

La suite completa de Core, incluido Content JSON, se ejecutó por separado:

```powershell
cmake -S C:/Users/andro/Documents/GitHub/CoreRPG -B C:/F02/core-build `
  -G 'Visual Studio 18 2026' -A x64 -DBUILD_TESTING=ON -DCORERPG_BUILD_CONTENT_JSON=ON
cmake --build C:/F02/core-build --config Release --parallel 4
ctest --test-dir C:/F02/core-build -C Release --output-on-failure --parallel 4
```

`audit_originals.py before/after --original <checkout original> --evidence <carpeta externa>` permite repetir el inventario protector sin escribir en los originales. Rechaza sobrescribir una línea base existente. `collect_evidence.py` reúne los informes ya ejecutados y sus SHA-256; la ejecución fechada utiliza `--native-evidence <F02_evidence_20261029> --ue-run <F02_Run_20261029>`. Rechaza sobrescribir artefactos publicados. El índice de Drive se completa únicamente después de la subida y lectura de metadatos, conservando los resultados originales.

Integración portable sin Unreal:

```sh
cmake -S desarrollo/integration/f02 -B build/f02 -DCORERPG_SOURCE_DIR=/path/to/CoreRPG
cmake --build build/f02 --config Release --parallel 4
ctest --test-dir build/f02 -C Release --output-on-failure
```

## Frontera y propiedad

- `TrekF02Bridge` es una DLL con ABI C v1. Dentro vive un único `WorldState` y su `RandomStreams`. Se enlaza el target CMake original `CoreRPG::CoreRPG`; la biblioteca Core sigue independiente de Unreal y de Star Trek.
- Sólo cruzan enteros, registros de tamaño fijo y buffers propiedad del llamador. La DLL asigna y libera sus objetos; Unreal asigna y libera los suyos. No cruzan STL, referencias a Core, excepciones ni objetos UObject. La DLL compila con `/EHsc`; captura excepciones y devuelve un estado. El módulo Unreal deshabilita excepciones.
- Todas las llamadas de sesión exigen el hilo propietario. Unreal añade el control de Game Thread. La vida de la sesión corresponde a `UGameInstanceSubsystem`; los Actors sólo representan una identidad autorizada.
- Cada binding incluye un ámbito efímero, distinto entre sesiones y renovado tras una carga correcta. Se invalidan bindings y Actors viejos; el `EntityId` persistido conserva su valor. Estos ámbitos no son IDs globales de campaña ni contactos de Sensores.
- El fixture crea tres entidades reales: sujeto/observador 1, contenedor 2 y entidad oculta 3. Sólo el Host inicializa el fixture. La acción permitida coloca al sujeto en el contenedor; también se prueba una tirada real. `ActionEngine` revalida revisión y operación. El permiso Host, revocable, es deliberadamente mínimo y no representa la jerarquía de Flota.
- `Visibility::project` construye el `ObserverView`; `ContextBuilder` selecciona contexto de ese valor. UI/Actor no recibe el mundo, el RNG, el censo de secretos ni permisos configurables. Los IDs visibles son diagnósticos del fixture, **no** el protocolo de resultados de Sensores.
- `Persistence` captura, serializa, valida y restaura. El Host se ocupa de IO. El fixture produce formato v3 por su conocimiento; no introduce un serializador propio. La carga admite exclusivamente el fixture de tres entidades y rechaza definición/conocimiento fuera de ese alcance. No implementa migraciones ni el guardado completo del videojuego.

## Evidencias y límites

[Informe de ejecución](../../../proyecto/docs/roadmap/master/fases/F02/INFORME_EJECUCION_REAL_2026-10-29.md) · [Auditoría actual](../../../proyecto/docs/roadmap/master/fases/F02/AUDITORIA_OPERATIVA_2026-10-29.md).

No hay reloj de campaña, agenda persistente, bitácora causal, catálogo Trek de producción, proveedor IA, red, consola de Sensores ni distribución empaquetada. La recuperación probada cubre cierre/reapertura de sesión y un save válido, no la durabilidad frente a corte eléctrico o muerte del proceso durante una escritura. Cambiar el SHA de Core exige reauditar y repetir los tests. La certificación de ABI queda limitada a esta combinación de versiones y Win64; la CI Linux sólo verifica el Host nativo.
