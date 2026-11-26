# Acto I — La decisión del Consejo

## Reproducción en el MSI

1. Abre `juego/UE5/StarTrekRPG/StarTrekRPG.uproject` con Unreal Engine 5.8.4. Comprueba que Windows está a 2560 × 1600 y al 150 %.
2. En el navegador de contenido abre `/Game/Cinematics/L_Intro_StarTrekLegends`. Pulsa **Play**. La introducción dura 54 segundos y el Acto I comienza automáticamente. Desde el inicio de la intro, el recorrido completo dura 9:04.
3. Tras el fundido final, pulsa **Stop** para salir de PIE. Pulsa **Play** de nuevo para repetir la secuencia.

Para revisar el viewport nativo a pantalla completa desde PowerShell, ejecuta desde la raíz del repositorio:

```powershell
$project = (Resolve-Path 'juego/UE5/StarTrekRPG/StarTrekRPG.uproject').Path
$editor = 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe'
& $editor $project /Game/Cinematics/L_Intro_StarTrekLegends -game -d3d12 -fullscreen -ForceRes -ResX=2560 -ResY=1600
```

Para modo ventana, sustituye los cuatro últimos parámetros por `-windowed -ForceRes -ResX=1440 -ResY=900`. Cierra la ventana para salir.

## Recursos e importación

Git excluye los paquetes de Unreal de esta producción. En el MSI se instalan en `/Game/Cinematics/Act_One` y el nivel original los detecta al cargar. Para reproducir el montaje en otra copia, restaura primero los paquetes de la introducción validada y compila `StarTrekRPGEditor` siguiendo la preparación del proyecto. Con FFmpeg en el PATH, ejecuta desde la raíz:

```powershell
& 'juego/UE5/StarTrekRPG/Build/Import-ActOne.ps1' `
    -AssetsRoot 'C:/Users/andro/Pictures/Star Trek Acto 1' `
    -EditorCmd 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
```

El importador usa las dos maestras y las 25 imágenes de intervención, incluidas las tres variantes adicionales de V7. Conserva el área completa de cada PNG. Produce 27 texturas, tres Sound Waves PCM, cuatro clases de sonido y `DA_ActOneTimeline`. La segunda ejecución del commandlet vuelve a abrir los paquetes y comprueba dimensiones, referencias y cronología. Los WAV intermedios se eliminan al cerrar el importador.

La fuente de títulos y nombres procede de `TXT_NombreCapitan` en `WBP_Intro_Pike` y corresponde a `/Game/Cinematics/Fonts_Intro/Federation_Wide_Font.Federation_Wide_Font`. El cuerpo usa `/Engine/EngineFonts/Roboto.Roboto`. Slate resuelve las grafías ausentes en la fuente importada mediante su fuente de respaldo.

## Edición y continuidad

[Manifiesto de cronología](STAR_TREK_LEGENDS_ACTO_I_TIMELINE.json) · [Guion aprobado V2](STAR_TREK_LEGENDS_GUION_CONSEJO_ACTO_I_V2.md)

El manifiesto contiene los tiempos absolutos, las rutas de los 27 archivos, sus dimensiones, los lados, las 22 intervenciones, los 68 bloques, las pausas y los marcadores. El Data Asset permite editar esos campos en Unreal. Edita el manifiesto para versionar cambios reproducibles. Tras importar de nuevo, las asignaciones de voz, la prerreproducción del siguiente acto y los controles de mezcla permanecen en el Data Asset local.

El mismo actor, reloj monotónico y fondo negro de la introducción gobiernan la presentación. Los tiempos del Acto I se calculan desde el final exacto de la intro. La capa utiliza los equivalentes Slate de `ScaleBox → SizeBox → Canvas` en el mismo overlay de viewport. Centra un lienzo de 2560 × 1600 y ajusta cada imagen proporcionalmente a su área. Los retratos alternan hasta V21. Los cuatro planos de V7 conservan el lado y el interlocutor. V22 emplea la panorámica y los bloques centrados en una zona inferior protegida por degradado.

| Tiempo del acto | Reproducción |
| --- | --- |
| 0:00–0:03 | Negro, localización y London Calling |
| 0:03–0:07 | Exterior de la sede |
| 0:07–0:10 | Sala, rótulo del Consejo y entrada ambiental |
| 0:10–1:56 | V1–V6 |
| 1:56–2:10 | V7, recuerdo de Picard y frase a 2:01,1 |
| 2:10–2:18 | V7.1, Locutus, entrada de Ode y reducción del ambiente |
| 2:18–2:27 | V7.2, Enterprise-D y cubo Borg |
| 2:27–2:56 | V7.3, Picard y regreso del ambiente |
| 2:56–5:28 | V8–V16 |
| 5:28–7:09 | V17–V20. Crescendo de Myers a 6:40 |
| 7:09–7:31 | V21. Preparación a 7:10 y voto visible a 7:30 |
| 7:31–8:05 | V22. Resolución, acta, reflexión, clímax a 7:55 y cierre |
| 8:05–8:10 | Fundido de imagen y audio hacia negro |
| 8:10 | Negro sostenido y evento `OnActOneFinished` |

## Mezcla y doblaje

Las canciones conservan sus grabaciones por separado y sus velocidades originales. Comienzan en los segundos 0 y 130 del acto. Se equilibran en Unreal con ganancias iniciales de 0,76 y 0,27. Ode comienza con un factor adicional de 0,92, que sube suavemente a 1,0 durante el tramo del voto y la resolución. El fundido final usa la misma ventana de cinco segundos que la imagen. El ambiente usa una ganancia de 0,85 y un bucle de 29,7 s con 300 ms de fundido entre los extremos. Desciende al 22 % de su nivel habitual en el recuerdo y se recupera durante V7.3.

Las clases `SC_MUSIC`, `SC_AMBIENCE`, `SC_VOICE` y `SC_SFX` son independientes. Cada intervención tiene un campo opcional `Voice`; su reproducción parte de la misma línea temporal que sus bloques. El factor `VoiceDuck` inicial es 0,50 y solo se aplica mientras haya voz. Para sincronizar un doblaje futuro, asigna la onda de la intervención y ajusta los tiempos de sus bloques y pausas. Los campos de voz quedan vacíos.

`NextActPreroll` admite el futuro ambiente de la bahía antes de `OnActOneFinished`. El acto actual libera las pistas y conserva el overlay negro al concluir. Para un eventual empaquetado, incluye el mapa de la introducción y el directorio `/Game/Cinematics/Act_One` en el conjunto de cocción, dado que el actor resuelve el Data Asset por ruta.

## Verificación

La prueba `StarTrekRPG.Intro.ActOne.Timeline` valida el montaje importado, los hitos prioritarios, la alternancia, la continuidad estructural del ambiente y las clases de mezcla. Las pruebas de intro cubren su cronología, los cinco diseñadores UMG y el reinicio consecutivo de PIE.

La escucha y la aceptación artística corresponden al propietario. El doblaje, las escenas del Acto II y el empaquetado de distribución quedan fuera de esta entrega.
