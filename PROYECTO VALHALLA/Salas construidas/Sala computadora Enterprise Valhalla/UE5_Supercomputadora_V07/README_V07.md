# USS Enterprise NCC-1701-D — V07, cierre práctico

Proyecto Galaxia. Se conservan los nombres históricos de carpetas `Valhalla`.
La aceptación personal y el cierre formal corresponden a la auditoría posterior.

## Abrir y jugar

Abrir con **Unreal Engine 5.8.2**:

`PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V07/ValhallaComputer.uproject`

Mapa inicial: `/Game/ValhallaV07/Maps/L_Supercomputadora_V07`.
Play, WASD, ratón y Espacio; Esc termina Play. Se conserva Quinn oficial,
Enhanced Input, cápsula de 35/90 cm y cámara en tercera persona.

- **D01:** automática habilitada, conserva el mecanismo V06.
- **D02–D04:** mecanismos conservados; cerradas por destinos sin construir.
- **MEM_C01–MEM_C06:** se conservan los cierres estáticos originales. Los seis
  rótulos exteriores no demuestran seis parejas de hojas independientes. No se
  recortan mamparos ni se mueven bancos para convertirlos en pasos. No son
  necesarios para recorrer el interior terminado.
- **Escaleras:** tres entradas permanecen abiertas a los peldaños existentes.
  B05–B07 conservan la protección de las salidas a cubiertas incompletas. B08
  cierra el hueco bajo el tramo superior sur donde se reprodujo una caída; B09
  cierra preventivamente la boca bajo la rampa norte en el nivel inferior.
  Ninguno añade suelo ni modifica peldaños.
- **B01–B04:** se conservan los cuatro cierres de extremos de corredor V06.

El inventario registra **22 puntos de control**, con categorías distintas:
cuatro puertas, seis candidatas señalizadas de memoria, ocho bocas de escalera
y cuatro extremos de corredor. **No significa 22 puertas.** Tres pasos de
escalera quedan abiertos sin hojas, D01 permite paso automático y 18 puntos
quedan cerrados intencionadamente, incluidos los tres mecanismos bloqueados.
El número artístico de posibles hojas integradas no se certifica ni condiciona
esta solución práctica.

Para probar D02–D04 con Quinn sin abrir destinos incompletos, usar el mapa
permanente `/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion`.
Para habilitarlas en otra fase será necesario construir y validar primero el
destino, y después cambiar `DestinationConstructed` y `SecurityLocked`.

Consultar el [inventario](Scripts/v07_door_inventory.json) y el
[informe técnico](../../../informes/valhalla/V07_PUERTAS_ESTADO_TECNICO.md).
La iluminación sigue siendo técnica y la comodidad de cámara en escaleras
requiere valoración personal. No se inicia V08.

## Reconstrucción

Trabajar en una copia nueva dentro de la ubicación temporal autorizada por el
AGENTS de la raíz. Las variables siguientes son rutas proporcionadas por quien
ejecute la receta; no quedan incorporadas como dependencias del juego.

1. `prepare_v07.py --source-project "$SourceV06" --target "$Target"` copia V06,
   incorpora el código y selecciona el mapa V07. Rechaza destinos existentes.
2. Exportar V04E con `exportar_v04e_ue.py` y ejecutar Blender con
   `export_doors_v07.py --source "$V04E" --reference "$ExportV04E" --output "$Manifest"`.
   Conservar estas exportaciones únicamente como evidencia temporal.
3. Compilar el proyecto nuevo:

```powershell
& "$UEInstall/Engine/Build/BatchFiles/Build.bat" ValhallaComputerEditor Win64 Development "$Target/ValhallaComputer.uproject" -WaitMutex -NoHotReloadFromIDE "-Log=$Logs/build.log"
```

4. Ejecutar `author_v07.py` en dos procesos separados, primero con
   `VH_V07_STAGE=copy`, después con `VH_V07_STAGE=author` y `VH_SOURCE_FILE=$Manifest`.
   Cada ejecución necesita un `VH_EVIDENCE_DIR` nuevo. Estos dos pasos conservan
   el resultado histórico de cuatro mecanismos; todavía falta el cierre práctico.
5. Ejecutar **`author_v07_closure.py`**, también con evidencia nueva. Añade B08/B09
   desde `v07_closures.json`; rechaza duplicados y compara las propiedades de
   puertas, arquitectura instanciada y límites V06 antes y después.
6. Crear el recinto auxiliar con `author_v07_rig.py`, el mismo manifiesto,
   evidencia nueva y `VH_V07_RIG_MAP=/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion`.
7. Reabrir en otro proceso con RHI real y `audit_v07.py`.

Ejemplo de invocación de autoría o reapertura:

```powershell
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$Target/ValhallaComputer.uproject" "-ExecutePythonScript=$Target/Scripts/author_v07_closure.py" -unattended -RenderOffscreen -nosound "-Abslog=$Logs/closure.log"
```

Comprobar el JSON de cada ejecución, además del código de salida. La autoría
no sustituye la validación de juego ni concede el cierre formal.

## Repetir las pruebas

- `v07_validation_plan.json`: 49 casos heredados del mapa, sin alterar.
- `v07_rig_plan.json`: 27 casos de D02–D04, incluidos doce ciclos completos por puerta.
- `v07_closure_plan.json`: 18 casos nuevos de memoria y B08, con aproximaciones y saltos.
- `check_v07_closure_report.py <report.json>`: exige todos los casos y comprueba
  que las muestras de Quinn quedan ante el plano protegido de B08. Tras saltar,
  la consulta final puede apuntar al marco; se exige contacto observado con B08
  y la posición segura, además del bloqueo y suelo final.

```powershell
& "$UEInstall/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$Target/ValhallaComputer.uproject" /Game/ValhallaV07/Maps/L_Supercomputadora_V07 -game -unattended -RenderOffscreen -nosound "-VH06Plan=$Target/Scripts/v07_closure_plan.json" "-VH06Report=$ClosureReport" "-Abslog=$Logs/closure-runtime.log" -ExecCmds="t.MaxFPS 60"
python "$Target/Scripts/check_v07_closure_report.py" "$ClosureReport"
```

Para los demás planes, cambiar el archivo de plan y, para el recinto auxiliar,
el mapa. Examinar todos los campos `passed` y los ciclos completos; salir con
código cero no basta. NullRHI no acredita apariencia ni rendimiento.

Los modelos, recursos UE, imágenes, binarios y datos brutos permanecen locales
según la política del repositorio. Git publica código, planes, inventario e
informe. La PR #80 sigue en Draft y depende de V06; no fusionar ni modificar #79.
