# Entorno compartido MSI — Unreal / Blender

Fecha de conservación: 21 de octubre de 2026, Europe/Madrid. Documento local de continuidad, sin instalación, integración ni publicación. Leer junto a [Sutherland](SUTHERLAND_ESTADO_FINAL.md) y [Voyager](VOYAGER_HANDOFF.md).

## Estado de parada

La instrucción vigente del usuario es detener Voyager y conservar el trabajo. Esta sesión termina después del traspaso; no inicia nuevas pruebas. La nueva sesión debe comprobar este estado antes de continuar con la misión que el usuario le encargue. No hay que cerrar automáticamente aplicaciones o sesiones.

En la inspección de parada no había procesos Blender, Python de laboratorio, UnrealEditor ni UnrealBuildTool en ejecución. El propio registrador de conservación se excluye de ese inventario. No había una operación de guardado o render que hubiera que terminar ni trabajo propio conocido únicamente en memoria. No se ha usado una interfaz gráfica para certificar buffers de otras aplicaciones del usuario.

## Equipo e instalaciones comprobadas

| Elemento | Dato y procedencia |
|---|---|
| Equipo | Micro-Star International, Raider GE78 HX 14VGG; consulta CIM durante el traspaso |
| Sistema | Microsoft Windows 11 Pro, versión 10.0.26200, build 26200 |
| RAM visible | 34.116.366.336 bytes, aproximadamente 31,8 GiB; no es una medida de memoria libre |
| GPU | NVIDIA GeForce RTX 4070 Laptop GPU; controlador 32.0.16.1714 |
| Unreal instalado | `C:\Program Files\Epic Games\UE_5.8` |
| Versión real de Unreal | 5.8.2, CL 56702186, CompatibleChangelist 55116800; leído en `Engine\Build\Build.version` |
| Asociación de proyecto | Los `.uproject` de referencia usan `EngineAssociation: 5.8`; no convertir por esa diferencia con el parche 5.8.2 |
| Blender del laboratorio | `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, 5.2.2 LTS, hash d13f752e3b9c; build 2026-09-15 |
| Python numérico | `C:\Program Files\Blender Foundation\Blender 5.2\5.2\python\bin\python.exe`; NumPy 2.3.4 disponible |
| Python del sistema usado | `python`, Python 3.10.11, Pillow 12.2.0; no estaban disponibles NumPy, SciPy, trimesh ni matplotlib en ese intérprete |
| Shell | PowerShell en Windows; usar rutas literales y comillas en rutas con espacios |
| Espacio de conversación | `C:\Users\andro\Documents\ChatGPT\UE5 y Blender`; solo contenía `.git` antes del traspaso, sin commits en `master` |

No se instalaron dependencias para VOY-02. No confundir el Python interno de Blender, que tiene NumPy, con el Python del sistema. Los scripts que importan `bpy` o `mathutils.bvhtree` deben ejecutarse dentro de Blender, no solo con su binario Python. Los scripts numéricos que importan `geom.py` pueden usar directamente el Python incluido con Blender.

## Rutas de proyecto que no deben confundirse

| Función | Ruta |
|---|---|
| Repositorio documental/lógico | `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek` |
| Biblioteca de modelos original | `C:\Users\andro\Documents\GitHub\3D Star Trek` |
| Raíz de trabajos 3D / laboratorios Sutherland | `C:\Users\andro\Documents\StarTrek_3D` |
| Sutherland principal de los informes F07 | `C:\Users\andro\Documents\StarTrek_3D\f07sutherland\f07sutherland.uproject` |
| Otra carpeta distinta existente | `C:\Users\andro\Documents\StarTrek_3D\F07_sutherland\F07_sutherland.uproject` |
| Laboratorio humano de sillas | `C:\Users\andro\Documents\StarTrek_3D\Sutherland_ChairLab\Sutherland_ChairLab.uproject` |
| Sutherland sillas automatizadas | `C:\Users\andro\Documents\StarTrek_3D\F07_Chair_AutoLab` |
| Sutherland puertas finales F/G | `C:\Users\andro\Documents\StarTrek_3D\F07_P03FG_DoorLab` |
| Sutherland colisiones e integración técnica de laboratorio | `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab` |
| Recursos PBR Sutherland observados | `C:\Users\andro\Documents\StarTrek_3D\Sutherland_PBR_Lab` |
| Auditoría VOY-01 | `C:\Users\andro\Documents\Auditorias_3D\Voyager_Puente_2026-10-21` |
| Laboratorio VOY-02 | `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio` |
| Estos cuatro documentos | `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO` |

`F07_sutherland` y `f07sutherland` difieren también en el guion bajo: son dos carpetas existentes, no una variación de mayúsculas de la misma ruta. Utilizar la ruta exacta indicada en cada informe. No promover un laboratorio a principal ni deducir cuál contiene los últimos materiales por el nombre.

El checkout local de `Videojuego_StarTrek` se comprobó limpio en `main`, HEAD `3479faefb9aa56980265c5b03aeab3ba3ddd083f`. El estado respecto a `origin/main` procede de referencias locales, sin fetch durante esta parada. Los documentos nuevos se guardan fuera del repositorio para no alterar ese checkout. No se hizo commit, push, merge o publicación durante VOY-02 o durante este traspaso.

## Referencias reutilizables de Unreal

Los siguientes valores proceden de los informes Sutherland ya existentes, releídos ahora; no de una nueva ejecución de Unreal:

- Personaje: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`.
- Cápsula real de esos ensayos: radio 35 cm, semialtura 90 cm, altura total 180 cm; `MaxStepHeight` 45 cm.
- Los scripts históricos distinguían commandlet de inventario, editor con mundo físico inicializado, y Play con CharacterMovement/Walking/Tick. Un barrido o una prueba Blender no equivale a caminar en Unreal.
- Automatización histórica: Python Editor Script Plugin, GeometryScripting y ProceduralMeshComponent; algunos se habilitaban en línea de comandos. Consultar los wrappers existentes del laboratorio concreto antes de repetir una operación.
- Puertas Sutherland: fuentes `STAutomaticDoor.cpp`, `STDoorIntent.cpp`, configuración compartida y eventos de acceso. No hay conexión CoreRPG/NPC en esos laboratorios. No copiar sus carreras o huecos a Voyager sin medirlos.
- Exportaciones de sillas históricas: Blender en metros; exportaciones locales horneadas; Unreal en centímetros, escala 1. Se verificó UV y orientación. No aplicar un factor 100 adicional por costumbre.

Los experimentos VOY-02 han usado radio de cápsula 0,35 m y alturas 1,60 / 1,75 / 1,90 m. El conjunto final ensayado tiene puente a factor 1,10 y biblioteca modular a su escala numérica existente. Son hipótesis del laboratorio, no una modificación del Character Sutherland ni de parámetros del futuro juego. Al recuperar el trabajo puede añadirse una comparación con 1,80 m si aporta valor, indicando que el dato histórico del Character no certifica la configuración futura de Voyager.

## Procedimientos de continuidad

Primero leer manifiestos y resultados guardados. No ejecutar scripts `00_isolate`, `00_preparar` o scaffold para «comprobar» un resultado ya entregado: pueden reconstruir o redefinir referencias. Los archivos grandes guardados no se duplicaron durante este traspaso.

Ejemplo de apertura manual futura del laboratorio Voyager, solo después de reanudar:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' `
  'C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\ESCENAS\VOY02_Laboratorio.blend'
```

Ejemplo de ejecución Blender futura de un script específico, no una orden para ejecutarlo al leer este documento:

```powershell
$voyLab = 'C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio'
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python "$voyLab\SCRIPTS\12_capturas.py"
```

El script `12_capturas.py` actual tiene encuadres pendientes: no repetirlo sin revisar primero el punto de continuidad. Sus cortes de inspección se hacen en memoria y no guardan sobre el `.blend` maestro.

## Conservación y límites de la comprobación

En `TRASPASO/ESTADO_PARADA.json` se conserva fecha exacta, procesos, estado Git y pruebas de legibilidad. `INVENTARIO_ARCHIVOS.csv` registra rutas, tamaños, fechas y SHA-256 de los 207 archivos preexistentes del laboratorio, excluyendo esta carpeta de traspaso. `COMPROBACION_ENTRADAS.json` verifica nuevamente las 115 entradas originales registradas al iniciar VOY-02 y las 106 copias de recursos: coinciden.

Ese alcance no certifica todos los archivos de Sutherland, todos los repositorios ni cambios de terceros. En esta parada Sutherland se ha leído para documentar, sin escribir sobre sus archivos, ejecutar sus scripts o abrir sus proyectos. Las validaciones históricas se atribuyen a sus informes originales, no se presentan como recién ejecutadas.
