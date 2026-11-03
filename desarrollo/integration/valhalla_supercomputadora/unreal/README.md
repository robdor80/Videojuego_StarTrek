# Supercomputadora Valhalla — V05 y V06

**Entrega actual V06:** [Quinn, correcciones de escaleras y límites, instrucciones y reproducción](README_V06.md). Pendiente de aprobación personal; PR #79 en Draft. Los apartados V05 siguientes documentan la entrega histórica conservada.

Código permanente para UE 5.8.2. El proyecto local entregado con sus recursos está en `PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V05/`. Esta plantilla versionada contiene código y configuración; los recursos privados se restauran desde la entrega local y no se publican en Git.

V04E es la base geométrica validada. V05 implementa **una puerta exterior D01 con dos hojas**; los ocho módulos acristalados #206 son estáticos. La sala continúa pendiente de la prueba personal con Quinn en V06. No se crean materiales PBR nuevos ni hay dependencia de CoreRPG.

## Mecanismo y seguridad

`AVHAutomaticDoor` consulta cápsulas de `APawn` desde ambos lados, excluye espectadores, separa las hojas mediante barridos de colisión y mantiene el paso abierto mientras exista ocupación. Una nueva aproximación o una obstrucción interrumpe el cierre. Los estados son `Closed`, `Opening`, `Open`, `Closing` y `Blocked`; los cambios emiten `OnDoorStateChanged`. Los colisionadores de hoja son convexos y conservan 2 mm de margen sobre el suelo. Esa modificación afecta exclusivamente a la colisión; la firma de superficies, normales y UV se verifica antes y después.

Las funciones `RequestOpen`, `RequestClose`, `SetSecurityLocked`, `SetDestinationConstructed` y `SetExternalAccessAllowed` permiten conectar un adaptador de órdenes. `CanActorUseDoor` puede especializarse en Blueprint. `SetEmergencyHoldOpen(true)` es la orden explícita de evacuación: abre y mantiene abierta la puerta por encima de las restricciones de acceso. Solo se abre hacia un destino construido; no vence las protecciones de ocupación o colisión. Liberarla restituye las restricciones previas. Un cierre o bloqueo nunca vence la protección del ocupante. No se define aquí autoridad de estados del videojuego.

El código de proximidad y movimiento deriva del mecanismo interno STAutomaticDoors del prototipo Sutherland, adaptado en una copia independiente; aquel proyecto no se modifica. La evaluación opcional de intención permanece desactivada en D01.

## Coordenadas y datos

La exportación usa centímetros: `UE = (100·Blender.X, −100·Blender.Y, 100·Blender.Z)`. Se transforman normales, orientación triangular y reflexiones explícitamente. Las reflexiones arquitectónicas se hornean en variantes privadas de malla con transformaciones positivas. Los materiales conservan sus ranuras, colores, alpha, imágenes originales y UV; el acabado y la iluminación artística siguen pendientes. Los anversos/reversos se conservan con materiales de una cara y colisión estática de dos caras, evitando activar simultáneamente ambas superficies en el rasterizado.

Las posiciones cerradas y abiertas proceden de las claves V04B 20/60, conservadas en V04E. La raíz de D01 en UE es aproximadamente `(3121,5833; 248,1314; 37,0000)` cm. Las dos hojas recorren unos `90,7618` cm, cada una hacia su bolsillo. El tiempo de apertura es 0,8 s; el cierre espera 1,5 s sin demanda ni ocupación.

## Reproducir

Trabajar siempre en una copia nueva y aislada, siguiendo el `AGENTS.md` de la raíz para todas las salidas temporales. No ejecutar autoría sobre el proyecto original ni sobre una entrega anterior. Modelos, recursos y evidencias no se añaden a Git.

1. Exportar la V04E cuyo SHA-256 es `e55df3cf537365ac8e145b9a7cd96605f5b0edaa5537473a734f090f931a8670`:

   `blender --background --factory-startup --python-exit-code 1 --python Scripts/exportar_v04e_ue.py -- --input V04E.blend --output-dir NUEVA_EXPORTACION`

2. Copiar esta plantilla al directorio temporal autorizado y compilar `ValhallaComputerEditor Win64 Development` con `Engine/Build/BatchFiles/Build.bat`. Redirigir los registros de compilación y de UE a la evidencia autorizada.
3. Definir `VH_SOURCE_FILE` con el JSON exportado y `VH_EVIDENCE_DIR` con un directorio nuevo. Ejecutar `UnrealEditor-Cmd PROYECTO.uproject -ExecutePythonScript=Scripts/author_scene.py -unattended -nullrhi -nosound`. El script rechaza una escena ya creada, aplica el margen del colisionador y guarda el mapa.
4. Cerrar y reabrir UE. Con otro directorio nuevo de evidencia, ejecutar `Scripts/audit_scene.py` de la misma manera. Comprueba las 297 mallas, 16.302 colocaciones, ranuras, UV y normales, además de 22 casos funcionales con Chaos. Las consultas inmediatas durante la autoría no sustituyen a esta prueba de reapertura.
5. Ejecutar el mapa en mundo de juego:

   `UnrealEditor-Cmd PROYECTO.uproject /Game/Valhalla/Maps/L_Supercomputadora_V05 -game -unattended -nullrhi -nosound -VHRunValidation -VHValidationReport=RUTA_AUTORIZADA/informe.json -Abslog=RUTA_AUTORIZADA/runtime.log`

   `AVHFunctionalProbe` utiliza el `Tick` real de la puerta y escribe 31 comprobaciones. Sin esas opciones queda inactivo. El informe declara explícitamente que V06 no está completada. Esta prueba usa una cápsula de 70 × 180 cm; no simula la animación de Quinn.

## Prueba personal y Quinn

Abrir la entrega local `ValhallaComputer.uproject` con UE 5.8.2 y el mapa `L_Supercomputadora_V05`. **Play** usa un personaje provisional con cápsula física de 70 × 180 cm: WASD y ratón. El `PlayerStart` está junto a D01. Acercarse, pasar, quedarse en el umbral, salir, volver durante el cierre y repetir desde el otro lado. Comprobar los estados de D01 en sus propiedades durante la ejecución.

Para V06, incorporar el contenido oficial de Quinn y crear un GameMode Blueprint con su personaje como `DefaultPawnClass`; asignarlo en World Settings y mantener el PlayerStart de referencia. Confirmar las dimensiones reales de su cápsula y repetir las pruebas de paso, suelo, cámara, animaciones y seguridad con esas dimensiones. Las rutas certificadas para la cápsula provisional no acreditan automáticamente la cápsula de Quinn. La iluminación y los materiales definitivos se revisan después.

No fusionar la PR de esta entrega sin autorización.
