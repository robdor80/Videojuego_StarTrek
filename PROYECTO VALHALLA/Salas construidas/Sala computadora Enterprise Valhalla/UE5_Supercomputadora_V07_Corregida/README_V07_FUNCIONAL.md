# Enterprise-D — V07 funcional

Entrega local nueva, conservando V06 y el V07 anterior:

`PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V07_Funcional/ValhallaComputer.uproject`

Mapa: `/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional`.
Unreal 5.8.2; Play, WASD, ratón y Espacio. Quinn oficial y Enhanced Input.

MEM_C01–MEM_C06 son seis puertas dobles nuevas con el mecanismo
`AVHAutomaticDoor` existente. Se retiran 35 cm y deslizan lateralmente 100 cm;
conservan barrido, ocupación, reapertura y política de acceso. C01/C02/C04/C05 abren
recintos de servicio acotados, de 180 cm de ancho y hasta 400 cm desde el paño
original. C03/C06 usan conexiones de 180 cm hasta el corredor exterior existente,
conservando el recorrido curvo. Los laterales, fondos donde corresponden, suelos
y techos protegen el recorrido; el cerramiento exterior original sigue activo.
El paso libre tiene 230 cm de altura. Son recintos funcionales de servicio;
su equipamiento y acabado artístico no forman parte de esta entrega.

D01 sigue habilitada. D02–D04 siguen bloqueadas por destinos sin construir.
Se mantienen B01–B09 y los peldaños. Las escaleras norte y sur reciben dos
cubiertas a Z=610 cm y cerramientos superiores; no se añade una planta ni se
habilitan las salidas superiores protegidas. La iluminación sigue siendo técnica.

Blender de trabajo, con materiales originales empaquetados y doce hojas animadas
en los fotogramas 1/60/120:

`PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/Sala_Supercomputadora_V07_Funcional.blend`

Unreal contiene la integración física y jugable autorizada; la animación Blender
sirve para inspeccionar las posiciones cerrada y abierta. Los originales no se
sobrescriben. Los recursos locales excluidos por Git se reproducen con los scripts.

## Reconstrucción

Todas las variables de trabajo y evidencia deben apuntar a directorios nuevos
permitidos por AGENTS.md. No reutilizar ni borrar ejecuciones anteriores.
`$Scripts` corresponde a esta carpeta `Scripts`; `$UE` es UnrealEditor-Cmd.exe.
La fuente `$V07` es la entrega histórica anterior a esta finalización.

1. `python "$Scripts/prepare_v07_completion.py" --source-project "$V07" --target "$Target"`.
   Copia el proyecto, incorpora el código versionado y rechaza destinos existentes.
2. Compilar la copia:

```powershell
& "$UEInstall/Engine/Build/BatchFiles/Build.bat" ValhallaComputerEditor Win64 Development "$Target/ValhallaComputer.uproject" -WaitMutex -NoHotReloadFromIDE "-Log=$Evidence/build.log"
```

3. Exportar la geometría del mapa histórico de la copia:

```powershell
$env:VH_GEOMETRY_FILE="$Evidence/source_geometry.json"
& $UE "$Target/ValhallaComputer.uproject" /Game/ValhallaV07/Maps/L_Supercomputadora_V07 "-ExecutePythonScript=$Target/Scripts/capture_v07_geometry.py" -unattended -RenderOffscreen -nosound "-Abslog=$Evidence/export.log"
```

4. Preparar Shapely 2.2.0 para Python 3.13 de Blender en `$Dependencies`.
   La ejecución validada descarga la rueda Windows con `pip download
   --only-binary=:all: --no-deps --python-version 313 --implementation cp --abi cp313
   --platform win_amd64 --no-cache-dir --dest "$Wheels" shapely==2.2.0` y la extrae
   con `zipfile` dentro de `$Dependencies`. NumPy viene incluido en Blender.
5. Generar los recortes y las superficies complementarias:

```powershell
& $Blender -b --factory-startup --python "$Scripts/build_v07_memory_geometry.py" -- --geometry "$Evidence/source_geometry.json" --accesses "$Scripts/v07_memory_accesses.json" --output "$Generated" --dependency-dir "$Dependencies" --source-blend "$V04E"
```

El generador conserva UV, materiales y normales interpoladas fuera del volumen de
paso. Resta la cobertura horizontal existente antes de crear suelo o techo.
Las posiciones de colocación, escala, rotación y malla se verifican antes de
eliminar cualquier instancia; un manifiesto de otra versión debe rechazarse.

6. Crear el mapa funcional, sin sobrescribir el histórico:

```powershell
$env:VH_COMPLETION_MANIFEST="$Generated/completion.json"
$env:VH_EVIDENCE_DIR="$Evidence/author"
& $UE "$Target/ValhallaComputer.uproject" /Game/ValhallaV07/Maps/L_Supercomputadora_V07 "-ExecutePythonScript=$Target/Scripts/author_v07_completion.py" -unattended -RenderOffscreen -nosound "-Abslog=$Evidence/author.log"
```

7. Reabrir con `check_v07_completion.py`, usando otro `VH_EVIDENCE_DIR` nuevo.
   Exige diez mecanismos, 108 posiciones con suelo/techo, seis barridos libres,
   cubiertas en los puntos de recorrido y Map Check/materiales válidos.
8. Para el Blender definitivo, exportar el mapa funcional mediante
   `capture_v07_geometry.py`, con `VH_GEOMETRY_MAP` apuntando al mapa funcional
   y un `VH_GEOMETRY_FILE` nuevo. Después ejecutar:

```powershell
& $Blender -b --factory-startup --python "$Scripts/export_v07_blender_work.py" -- --geometry "$FinalGeometry" --source-blend "$V04E" --completion "$Generated/completion.json" --output "$NewBlend"
```

## Validación

Pruebas de recorte y superficies: ejecutar `test_v07_memory_geometry.py` con
Blender y `VH_PYTHON_DEPS=$Dependencies`.

Generar el plan de Quinn con `make_v07_completion_plan.py --output "$Plan"`.
`--captures "$Captures"` añade seis capturas en rutas temporales proporcionadas.

```powershell
& $UE "$Target/ValhallaComputer.uproject" /Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional -game -unattended -RenderOffscreen -nosound "-VH06Plan=$Plan" "-VH06Report=$RuntimeReport" "-Abslog=$Evidence/runtime.log" -ExecCmds="t.MaxFPS 60"
python "$Scripts/check_v07_completion_reports.py" --plan "$Plan" --output "$Checked" "$RuntimeReport"
```

Son 54 casos: entrada, salida, ocupación, bloqueo, límite exterior, dos laterales y seis
ciclos por acceso, más seis regresiones de B08. El verificador admite varios
informes ordenados cuando se repiten casos; el último resultado de cada nombre
es el vigente, y no se ocultan resultados fallidos seleccionando sólo los éxitos.
Comprueba además el cruce del umbral, la posición ante una puerta bloqueada,
la ocupación y los ciclos. Repetir `v07_validation_plan.json` para los 49 casos
heredados. Los antiguos casos de memoria cerrada pertenecen al mapa histórico.

Usar RHI real para validar apariencia. Revisar los JSON y todos los campos de
resultado; el código de salida del motor no acredita por sí solo el éxito.
La aceptación manual de cámara, iluminación y recorrido continúa pendiente.
