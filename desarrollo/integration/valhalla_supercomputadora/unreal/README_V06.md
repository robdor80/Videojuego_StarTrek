# Supercomputadora Valhalla — V06 con Quinn

V06 queda preparada para validación personal. No se considera definitivamente cerrada sin la aprobación del usuario. V04E y el proyecto local V05 se conservan aparte.

## Abrir y jugar

Abrir con **Unreal Engine 5.8.2**:

`PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V06/ValhallaComputer.uproject`

El mapa de inicio es **`L_Supercomputadora_V06_Quinn`**. Pulsar **Play**: Quinn aparece junto a D01 en tercera persona. **WASD** mueve, **ratón** orienta la cámara, **Espacio** salta y **Esc** termina Play. D01 abre por aproximación; no necesita una tecla de interacción. Atravesarla, volver al vestíbulo y recorrer los ramales hacia ambos recintos circulares y los pasillos exteriores.

Los paneles azules con remate claro cierran sectores que aún no tienen destino construido. Las escaleras existentes permiten recorrer sus tramos y regresar; las bocas hacia las cubiertas inexistentes permanecen cerradas. Los ocho módulos acristalados #206 siguen siendo estáticos.

Quinn procede de la plantilla Third Person instalada con el motor. Conserva cápsula de **35 cm de radio y 90 cm de semialtura**, escala 1, movimiento de 600 cm/s, escalón máximo de 45 cm y ángulo transitable de 44,765°. Usa `SKM_Quinn_Simple`, `ABP_Unarmed`, el controlador oficial con Enhanced Input y un GameMode propio. El brazo de cámara mantiene 400 cm, sonda de 12 cm y prueba de colisión. No se incorporan ataques, armas ni un sistema de combate.

## Cambios controlados

- Los 101 materiales utilizados por las instancias guardan el indicador de uso con ISM. Conservan sus nodos, colores, transparencias, imágenes, UV y asignaciones; permanecen de una cara.
- La orientación triangular importada se adapta a la convención comprobada contra Cube del propio motor. Se conservan posiciones, normales explícitas, UV y ranuras durante esa operación.
- Una segunda corrección, separada y documentada, orienta hacia arriba las caras de suelo invertidas de la cota principal. Utiliza 77 mallas privadas; corrige normal y orientación de 2.803 triángulos y conserva posiciones, UV y materiales. No añade superficies de suelo.
- Las dos variantes de malla de escalera reciben diez convexos por recurso, siguiendo los peldaños existentes. Esos dos recursos se reutilizan en los seis tramos. La malla visible no cambia y no se reduce la cápsula jugable.
- Las dos figuras de escala Nancy, formadas por ocho colocaciones, permanecen guardadas como referencias ocultas y sin colisión durante el juego. Ya no bloquean los desembarcos. No se eliminan estructuras para mejorar FPS.
- Siete cierres visibles, con siete remates, delimitan cuatro salidas sin continuidad y tres bocas de escalera hacia cubiertas sin construir. No se extiende el suelo a esos destinos.
- Iluminación técnica sustituible: 36 luces puntuales sin sombras, relleno direccional y exposición manual fija. Se desactivan las sombras de las luces direccionales de ensayo y el desenfoque de movimiento. Los actores nuevos llevan `V06_PROVISIONAL_LIGHT` o `V06_VISIBLE_BOUNDARY`. No es iluminación artística ni una fase PBR.

Los contactos heredados y condicionados siguen documentados: 76 relaciones banco/arquitectura y 656 relaciones de tapas con elementos del banco. Esta entrega no los convierte en una certificación estructural global.

## Reconstruir en una copia nueva

Usar una **ruta corta dentro del repositorio**, en la ubicación de pruebas autorizada por el AGENTS de la raíz. La ruta larga de entrega puede superar los límites de rutas de algunas herramientas de compilación. No ejecutar autoría sobre V04E, V05 ni una entrega existente. `prepare_v06.py` rechaza destinos existentes y no escribe en el proyecto de origen.

Definir `$SourceV05`, `$UEInstall`, `$NewCopy` y dos directorios nuevos de evidencia autorizada. Definir también `$RunLogs` como otro directorio nuevo de registros autorizado. `$UEInstall` es el directorio `UE_5.8` de la instalación legítima. Ejecutar desde esta plantilla:

Si se redirige la caché del motor, definir `UE-LocalDataCachePath` con una ruta temporal autorizada de **119 caracteres como máximo**. Unreal rechaza rutas más largas antes de ejecutar Python. No guardar esa ruta en la configuración entregada. La instalación de Zen y algunas trazas nativas de UnrealBuildTool pueden seguir escribiéndose en el perfil del usuario; no forman parte de la entrega.

```powershell
New-Item -ItemType Directory -Path "$RunLogs" -ErrorAction Stop | Out-Null
python -B Scripts/prepare_v06.py --source-project "$SourceV05" --engine "$UEInstall" --target "$NewCopy"
& "$UEInstall/Engine/Build/BatchFiles/Build.bat" ValhallaComputerEditor Win64 Development "$NewCopy/ValhallaComputer.uproject" -WaitMutex -NoHotReloadFromIDE "-Log=$RunLogs/build.log"
$env:VH_EVIDENCE_DIR = $AuthorEvidence
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$NewCopy/ValhallaComputer.uproject" "-ExecutePythonScript=$NewCopy/Scripts/author_v06.py" -unattended -RenderOffscreen -nosound "-Abslog=$RunLogs/author.log"
```

`author_v06.json` debe existir y declarar `ok: true`. El contenido oficial se copia mediante una lista de recursos necesarios de la instalación del motor. La entrega de ejecución conserva 56 paquetes oficiales y no necesita las plantillas ni una carpeta de ensayos para jugar; la reconstrucción sí necesita esas fuentes legítimas.

Cerrar el proceso de autoría y **reabrir con RHI real** para comprobar paquetes, Map Check y materiales:

```powershell
$env:VH_EVIDENCE_DIR = $ReopenEvidence
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$NewCopy/ValhallaComputer.uproject" "-ExecutePythonScript=$NewCopy/Scripts/audit_v06.py" -unattended -RenderOffscreen -nosound "-Abslog=$RunLogs/reopen.log"
```

`audit_v06.json` debe declarar `ok: true`. La comprobación espera las peticiones asíncronas de caché de materiales y la compilación; examina los recursos activos del RHI y el contenido de shader válido para renderizar, sin sustitución por el material predeterminado. Los indicadores transitorios de compilación de una shader map cargada de caché no sustituyen al predicado del motor `IsValidForRendering`. **NullRHI no valida el renderizado ni el rendimiento.**

## Repetir recorridos y medir

La sonda `AVH06Probe` permanece inactiva al jugar normalmente. Se activa solo con ambos argumentos `-VH06Plan` y `-VH06Report`:

```powershell
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$NewCopy/ValhallaComputer.uproject" /Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn -game -unattended -nullrhi -nosound "-VH06Plan=$NewCopy/Scripts/v06_validation_plan.json" "-VH06Report=$TraversalReport" "-Abslog=$RunLogs/traversal.log" -ExecCmds="t.MaxFPS 60"
```

La sonda posee al Quinn real del GameMode. Teletransporta únicamente al inicio de cada caso, después camina mediante Enhanced Input y CharacterMovement, con gravedad y colisión. Los casos de teclado y ratón inyectan sus eventos reales de entrada. Registra suelo, velocidad, huesos en espacio de componente, cámara y estados de D01. El resultado exige suelo estable; las pruebas de cierre deben encontrar el actor físico esperado. La tolerancia horizontal de llegada es 20 cm. La ruta exterior termina a X=5.500 cm; el extremo histórico X=5.550 cm queda protegido detrás de B03 y se comprueba como bloqueo esperado.

Para rendimiento, usar `v06_performance_plan.json`, RHI real, 1920×1080, porcentaje de resolución 100 y sin límite de FPS ni VSync:

```powershell
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$NewCopy/ValhallaComputer.uproject" /Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn -game -RenderOffscreen -ResX=1920 -ResY=1080 -ForceRes -Windowed -unattended -nosound "-VH06Plan=$NewCopy/Scripts/v06_performance_plan.json" "-VH06Report=$PerformanceReport" "-Abslog=$RunLogs/performance.log" -ExecCmds="t.MaxFPS 0,r.VSync 0,r.ScreenPercentage 100,r.SetRes 1920x1080w"
```

Cada vista espera seis segundos y mide ocho. El JSON registra la resolución real por caso, intervalos de fotograma, tiempo de juego/render/GPU, draw calls, primitivas y memoria local de GPU mediante RHI. No interpretar los campos de GPU de una ejecución NullRHI. Todas las salidas y registros deben dirigirse a la ubicación temporal autorizada.

Las verificaciones automáticas y las capturas no sustituyen la prueba personal. Revisar especialmente comodidad de la cámara en las escaleras, animaciones, claridad visual y límites de los sectores cerrados. El acabado artístico, PBR y la construcción de futuras cubiertas quedan fuera de esta fase. **PR #79 permanece en Draft y no se fusiona.**

## Resultado de la entrega del 2 de noviembre de 2026

La entrega local supera **43/43 casos con Quinn real**. Los planes publicados coinciden con los ejecutados. Incluyen doce rutas principales, tres recorridos de escaleras de ida y vuelta, siete casos de D01, los siete cierres físicos y saltos contra los cuatro límites exteriores, WASD, ratón, colisión con bancos, dos corredores curvos y el bloqueo del extremo histórico del corredor exterior. Las 1.039 muestras de recorrido no detectan solape bloqueante de la cámara; el brazo llega a reducirse a unos **34,55 cm**, por lo que sigue pendiente valorar personalmente su comodidad en los pasos estrechos.

Las seis vistas de rendimiento de la entrega se miden con D3D12 real, 1920×1080, seis segundos de espera y ocho de registro, sin VSync ni límite de FPS: medias entre **152,6 y 201,6 FPS**, y percentil 95 del intervalo entre **5,50 y 9,09 ms**, en i9-14900HX y RTX 4070 Laptop. Son mediciones del proyecto Development con renderizado fuera de pantalla e iluminación técnica sin sombras; no acreditan el rendimiento del acabado artístico ni de una distribución empaquetada.

El [informe técnico vigente](../../../informes/valhalla/SALA_SUPERCOMPUTADORA_ENTERPRISE_G.md#continuación-v06--quinn-y-entrega-independiente-2-de-noviembre-de-2026) conserva el detalle de cambios, resultados y evidencia identificada. V04E y V05 permanecen conservadas. El siguiente paso es abrir la entrega y probar personalmente los recorridos; la sala no se declara terminada.
