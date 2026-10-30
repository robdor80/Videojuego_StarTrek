# USS Sutherland — Corrección exclusiva de puertas

28/10/2026, Europe/Madrid. **Intervención de puertas terminada y verificada tras reabrir.** No se han iniciado otras fases ni continuado la auditoría general de integración.

## Proyecto utilizado

`C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Unreal\SutherlandPlayable01.uproject`

Mapa: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`. Se reutilizó la misma copia de trabajo, derivada de VISUAL_02. No se creó otro proyecto.

## Causa y reparación

Las colisiones importadas de las hojas incluían la parte visual oculta bajo el suelo. En D02 y D04 llegaban a Z=-2,3589 cm. En ejecución, el barrido de D04 comenzaba penetrando `SM_COLL_Circle_0_05` y `SM_COLL_P03G_D04_RightLowerReturn_01`: el código existente recibía un impacto y dejaba la puerta obstruida. No faltaban el Blueprint, los permisos ni la solicitud de Quinn.

Se recortó **solo la colisión inferior de las ocho hojas**, hasta 0,2 cm sobre su suelo local (0,3 cm en D04, cuyo suelo de cabina está a 0,1 cm). Se retuvo un hull convexo por hoja y su extremo superior. La parte dibujada bajo el suelo permanece intacta. No se movieron ni reescalaron las hojas, no se importó de nuevo el puente y no se cambiaron suelo, retornos, marcos o colisiones generales.

| Puerta UE | Suelo Z, cm | Límite inferior del collider Z, cm | Resultado mecánico |
|---|---:|---:|---|
| 001 | 60.0 | 60.2 | Dos hojas; 3 ciclos mecánicos correctos |
| 002 | 0.0 | 0.2 | Dos hojas; 3 ciclos mecánicos correctos |
| 003 | 60.0 | 60.2 | Dos hojas; 3 ciclos mecánicos correctos |
| 004 | 0.1 | 0.30000000000000004 | Dos hojas; 3 ciclos mecánicos correctos |

Se modificaron únicamente los `BodySetup` de ocho StaticMesh ya usados por `LeftLeaf` y `RightLeaf` de `P03FG_D001`–`P03FG_D004`, en `/Game/F07COLL01/Ergonomia03/Leaves/`. Rutas y hashes exactos: `Data/doors_20261028_fix.json` y `doors_20261028_final_integrity.json`.

## Mecanismos reutilizados

Blueprint conservado: `/Game/F07P03FG/Blueprints/BP_ST_AutomaticDoor_Sutherland`.
Clase/plugin conservados: `STAutomaticDoor` / `STAutomaticDoors`, de VISUAL_02. Se reutilizan las dos hojas, sus posiciones cerradas, recorridos, sensores de aproximación/ocupación, intención de paso, autorización, apertura, cierre y protecciones existentes.

**Cero cambios en Blueprints, código C++, binarios o configuración de Quinn.** No se creó un nuevo mecanismo. Los perfiles de colisión y los componentes móviles originales se mantienen.

## Pruebas realmente ejecutadas

- Diagnóstico en PIE, con barridos reales de las hojas: contacto inicial contra suelo y retorno inferior identificado. `doors_20261028_runtime_diagnosis.json`. Los contactos de D01/D03 recogidos en ese diagnóstico preliminar se produjeron por un error del guion al acumular la referencia de posición; no se utilizan como prueba de fallo de sus guías. La validación posterior usa copias de coordenadas y el recorrido correcto.
- Las ocho hojas completaron recorrido horizontal en sentidos opuestos y retorno, con barridos activos y sin impactos contra marcos. Se verificaron tanto posición de cierre como desplazamiento del collider unido a la hoja, tolerancia 0,001 cm.
- **Tres ciclos mecánicos consecutivos para cada una de las cuatro puertas**, ambas hojas: 12 rondas de mecanismo / 24 ciclos de hoja, sin bloqueos ni deriva. `doors_20261028_repeat_validation.json`: 3/3 comprobaciones y todas las rondas correctas.
- **Quinn real y poseído** activó D04 por aproximación desde el puente, caminando con la entrada W a través de su PlayerController. D04 abrió por completo y cerró automáticamente en **tres ciclos consecutivos**. `doors_20261028_validation.json`: 18/18 comprobaciones.
- Quinn entró caminando en la cabina existente y regresó al puente; se verificó apoyo en el suelo de cabina. Solo la posición inicial del escenario se preparó de forma controlada; no se presenta esta prueba como auditoría completa de circulación.
- Tres carriles de sonda de cápsula (Y=-25, 0, +25 cm) contra las hojas: bloquean cerradas y dejan paso abiertas. Se repitió durante los ciclos; no quedó la antigua barrera de hoja en la posición cerrada.
- Reapertura en otro proceso: ocho hulls correctos, perfiles activos y límites inferiores nuevos. Digest de vértices, índices, normales, tangentes, UV y materiales **idéntico** al anterior en las ocho mallas visibles. `doors_20261028_saved_verification.json`.

## Seguridad y límites

D04 es la puerta con cabina disponible y apertura automática validada con Quinn. D01–D03 conservan los tres bloqueos de destino no construido; sus mecanismos se probaron de forma controlada, sin habilitar circulación ni cambiar los permisos guardados. No se ha inventado suelo, habitación, corredor o destino. No hay transporte entre cubiertas.

Esta intervención no certifica todas las colisiones del puente, ergonomía o rendimiento. Pies suspendidos y la incidencia VSM quedan como antecedentes sin intervenir. Las seis sillas laterales, el capitán, las consolas, las cámaras y demás sistemas permanecen como estaban.

## Protección y recuperación

- Antes de modificar: respaldo del mapa y de cada uno de los ocho paquetes, con SHA-256, en `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Backups\Puertas_20261028`.
- Resultado validado, ocho paquetes y mapa de referencia: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Backups\Puertas_20261028\Resultado_validado`.
- Mapa activo sin cambios: SHA-256 `cff10a2af8d8926d85951834d63b31117d0fe3420bb50007ae24ed8be9792d29`.
- Rehash final de 2821 archivos del proyecto histórico y 7 Blender originales: sin diferencias.
- Verificados 1837 archivos previos no regenerables de la copia y los 90 assets derivados. Únicas modificaciones de assets: **las ocho hojas autorizadas**; los otros 82 derivados y el contenido previo del proyecto permanecen intactos.
- Las seis sillas (15 piezas móviles cada una), actores visuales adjuntos, Quinn y GameMode coinciden con la línea base al reabrir. La silla del capitán y sus marcadores no se cambiaron en esta intervención; el mapa es idéntico.
- Sin commit, push, PR, borrado de históricos ni cambios en proyectos originales.

## Reanudación

Abrir `Abrir_Editor.cmd` o el .uproject indicado. `Jugar_Standalone.cmd` inicia el juego normal. No repetir `15_fix_door_collisions.py`: se protege frente a una segunda aplicación. Los datos válidos son los cuatro JSON de fix, validation, repeat_validation y saved_verification, todos con `ok=true`; los intentos preliminares se conservan por separado.

Para restaurar, cerrar Unreal y recuperar **solo los ocho paquetes de hojas** desde el respaldo anterior o desde Resultado_validado, manteniendo sus rutas Content en esta copia de trabajo. El mapa no necesita restauración para esta corrección, pues no cambió.

La intervención termina aquí. Cualquier continuación de integración o fases posteriores requiere una nueva instrucción; no se inicia automáticamente.
