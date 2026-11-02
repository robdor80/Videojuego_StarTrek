# Supercomputadora Enterprise-G — V07 PARCIAL

**V07 no está terminada. El inventario exhaustivo sigue abierto.** Se han identificado cuatro puertas con hojas originales, implementado sus mecanismos y conservado las tres salidas nuevas bloqueadas por destinos sin construir. Los seis accesos señalizados de memoria y la atribución de hojas junto a las escaleras siguen pendientes. No interpretar cuatro mecanismos como el total de puertas de la arquitectura.

## Prueba personal

Abrir con **Unreal Engine 5.8.2**:

`PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V07/ValhallaComputer.uproject`

El mapa inicial es `L_Supercomputadora_V07`. Play, WASD, ratón, Espacio; Esc termina Play. D01 conserva su funcionamiento V06. D02 está en el vestíbulo oeste; D03 y D04 son las dos puertas naranjas de los laterales del corredor este. Estas tres quedan cerradas por seguridad: sus destinos no están construidos. Para habilitarlas en una fase futura deberán verificarse primero suelo, continuidad, límites y recorridos, y después establecer `DestinationConstructed=true` y `SecurityLocked=false` en el actor correspondiente. No basta con quitar el bloqueo.

Para probar sus mecanismos con Quinn, abrir **`/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion`**. Es un mapa auxiliar permanente de validación: plataforma con límites físicos, marcos originales y tres puertas habilitadas, en orden D02, D03, D04 a lo largo del eje X. Permite aproximación por ambos lados, paso, ocupación, cierre y reapertura. Su suelo pertenece exclusivamente a este recinto auxiliar; no repara ni amplía los suelos de la sala.

Los modelos Blender/SketchUp, V04E, V05 y la entrega V06 se conservan aparte. No hay cambios en CoreRPG ni en Sutherland. Se mantiene la iluminación técnica V06; no se realiza una fase artística o PBR.

## Mecanismo y límites

Se reutiliza `AVHAutomaticDoor`. D01 conserva el recorrido original. D02–D04 separan primero las hojas 20 cm del marco, las deslizan lateralmente y realizan el retorno inverso. D04 se retrae hacia el lado exterior opuesto para evitar un panel del corredor. Los dos segmentos se barren con colisión; se mantiene la protección por ocupación y la inversión del cierre ante obstáculos.

La partición conserva todas las superficies, UV, normales y materiales originales. En `#58` se divide la moldura que cruzaba la junta entre hojas, interpolando los atributos de los puntos nuevos. No se recortan marcos ni paredes para abrir carriles. Las colisiones privadas de las hojas tienen un margen de 1 cm en D02 y 3,2 cm en D03/D04. La medida del hueco original de estas últimas, aproximadamente 178,5 cm, es menor que sus 184 cm de geometría visible; el margen retira colisión de zonas que el propio marco oculta. La cápsula de Quinn mantiene 35/90 cm.

La sonda heredada ahora selecciona `door_id`, restaura las políticas originales en cada caso y modifica únicamente la puerta solicitada. Un identificador inexistente produce un caso fallido. El contador `min_closed_cycles` exige aperturas y cierres completos observados; recorrer los puntos no basta para acreditar ciclos.

Consultar el [inventario abierto](Scripts/v07_door_inventory.json) y el [informe técnico V07](../../../informes/valhalla/V07_PUERTAS_ESTADO_TECNICO.md). El inventario expresa `total_real_doors: null` e `inventory_exhaustive: false` deliberadamente.

## Reconstrucción independiente

Trabajar siempre en una copia nueva y en la ubicación temporal autorizada por el AGENTS de la raíz. Asignar `$SourceV06`, `$Target`, `$UEInstall`, `$Logs`, `$Manifest` y directorios de evidencia nuevos. No ejecutar autoría sobre una entrega existente. Todos los registros, cachés y datos generados deben dirigirse a la ubicación autorizada; no son dependencias del proyecto entregado.

1. `prepare_v07.py --source-project "$SourceV06" --target "$Target"` copia el contenido y la configuración V06, incorpora el código vigente y selecciona el mapa V07. Rechaza destinos existentes.
2. Exportar V04E con `exportar_v04e_ue.py` y después ejecutar Blender con `export_doors_v07.py --source "$V04E" --reference "$ExportV04E" --output "$Manifest"`. Ambas salidas son datos temporales. El exportador exige la firma V04E verificada y no guarda el Blender original.
3. Compilar antes de abrir el proyecto:

```powershell
& "$UEInstall/Engine/Build/BatchFiles/Build.bat" ValhallaComputerEditor Win64 Development "$Target/ValhallaComputer.uproject" -WaitMutex -NoHotReloadFromIDE "-Log=$Logs/build.log"
```

Ejecutar `author_v07.py` en **dos procesos separados**, primero con `VH_V07_STAGE=copy` y después con `VH_V07_STAGE=author`. Cada proceso requiere un `VH_EVIDENCE_DIR` nuevo; el segundo requiere `VH_SOURCE_FILE=$Manifest`:

```powershell
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$Target/ValhallaComputer.uproject" "-ExecutePythonScript=$Target/Scripts/author_v07.py" -unattended -RenderOffscreen -nosound "-Abslog=$Logs/author.log"
```

Comprobar el JSON y el código de salida de cada ejecución. `ok=true` acredita autoría técnica, **no finalización de V07**. La separación de procesos evita retener mundos duplicados durante la carga. Reabrir con RHI real y `audit_v07.py`, usando otra evidencia y otro registro nuevos.

Para generar el mapa auxiliar, ejecutar `author_v07_rig.py` con el mismo manifiesto, otra evidencia nueva y `VH_V07_RIG_MAP=/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion`. También rechaza mapas existentes.

## Repetir las pruebas

El [plan del mapa](Scripts/v07_validation_plan.json) contiene 49 casos: los 43 V06 y seis comprobaciones de bloqueo/destino de D02–D04. El [plan del recinto auxiliar](Scripts/v07_rig_plan.json) contiene nueve casos por puerta, con doce ciclos completos por cada una.

```powershell
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$Target/ValhallaComputer.uproject" /Game/ValhallaV07/Maps/L_Supercomputadora_V07 -game -unattended -nullrhi -nosound "-VH06Plan=$Target/Scripts/v07_validation_plan.json" "-VH06Report=$MapReport" "-Abslog=$Logs/map.log" -ExecCmds="t.MaxFPS 60"
```

Para el recinto auxiliar, sustituir el mapa por `/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion` y el plan por `v07_rig_plan.json`. Examinar todos los campos `passed` y `completed_close_cycles`; no basta con una salida de proceso cero. NullRHI verifica movimiento y colisiones, no apariencia ni FPS. Para rendimiento se conserva el protocolo V06: D3D12 real, 1920×1080, seis segundos de espera y ocho de medida en seis vistas, sin VSync ni límite de FPS.

Los recursos UE, modelos, imágenes y binarios de la entrega permanecen locales según la política del repositorio. Git publica código, planes, inventario e informe. La PR V07 depende de la rama V06 y permanece Draft. No fusionar. El apagado automático no corresponde mientras el objetivo completo siga pendiente.
