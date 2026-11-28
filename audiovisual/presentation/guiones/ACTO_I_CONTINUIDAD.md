# Acto I — La decisión del Consejo

## Reproducción en el MSI

1. Abre `juego/UE5/StarTrekRPG/StarTrekRPG.uproject` con Unreal Engine 5.8.4. Comprueba que Windows está a 2560 × 1600 y al 150 %.
2. En el navegador de contenido abre `/Game/Cinematics/L_Intro_StarTrekLegends`. Pulsa **Play**. La introducción dura 56 segundos y el Acto I comienza automáticamente. El Acto I dura 8:08, con tres segundos de negro inicial. Desde el inicio de la intro, el recorrido completo dura 9:04.
3. Tras el fundido final, pulsa **Stop** para salir de PIE. Pulsa **Play** de nuevo para repetir la secuencia.

Para reproducir a pantalla completa en D3D12 a 2560 × 1600 al 150 % de Windows, ejecuta desde la raíz del repositorio:

```powershell
$project = (Resolve-Path 'juego/UE5/StarTrekRPG/StarTrekRPG.uproject').Path
$editor = 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe'
$previousDpi = $env:__COMPAT_LAYER
try {
    $env:__COMPAT_LAYER = 'HIGHDPIAWARE'
    & $editor $project /Game/Cinematics/L_Intro_StarTrekLegends -game -d3d12 -fullscreen -ForceRes -ResX=2560 -ResY=1600 `
        '-ini:Engine:[/Script/Engine.UserInterfaceSettings]:bAllowHighDPIInGameMode=True'
} finally {
    $env:__COMPAT_LAYER = $previousDpi
}
```

La compatibilidad DPI del proceso evita que Windows reduzca el búfer de pantalla completa y conserva el escalado del sistema. Usa Alt+F4 para salir.

## Recursos e importación

Git excluye los paquetes de Unreal de esta producción. En el MSI se instalan en `/Game/Cinematics/Act_One` y el nivel original los detecta al cargar. Para reproducir el montaje en otra copia, restaura primero los paquetes de la introducción validada y compila `StarTrekRPGEditor` siguiendo la preparación del proyecto. Con FFmpeg en el PATH, ejecuta desde la raíz:

```powershell
& 'juego/UE5/StarTrekRPG/Build/Import-ActOne.ps1' `
    -AssetsRoot 'C:/Users/andro/Pictures/Star Trek Acto 1' `
    -EditorCmd 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
```

El importador usa las dos maestras y las 25 imágenes de intervención, incluidas las tres variantes adicionales de V7. Conserva el área completa de cada PNG. Produce 27 texturas, tres Sound Waves PCM, cuatro clases de sonido y `DA_ActOneTimeline`. La segunda ejecución del commandlet vuelve a abrir los paquetes y comprueba dimensiones, referencias y cronología. Los WAV intermedios se eliminan al cerrar el importador. Si ya tienes los paquetes del montaje anterior, sigue la [guía de actualización de la introducción](../../../juego/UE5/StarTrekRPG/INTRO_CINEMATICA_ESTADO.md) para actualizar su audio y el Data Asset con los recursos ya instalados. Si necesitas regenerar las tres ondas desde los originales, añade `-RefreshAudio` a la orden.

La fuente de títulos y nombres procede de `TXT_NombreCapitan` en `WBP_Intro_Pike` y corresponde a `/Game/Cinematics/Fonts_Intro/Federation_Wide_Font.Federation_Wide_Font`. El cuerpo usa `/Engine/EngineFonts/Roboto.Roboto`. Slate resuelve las grafías ausentes en la fuente importada mediante su fuente de respaldo.

## Edición y continuidad

[Manifiesto de cronología](STAR_TREK_LEGENDS_ACTO_I_TIMELINE.json) · [Guion aprobado V2](STAR_TREK_LEGENDS_GUION_CONSEJO_ACTO_I_V2.md)

El manifiesto mide los tiempos desde el comienzo del Acto I y contiene las rutas de los 27 archivos, sus dimensiones, los lados, las 22 intervenciones, los 68 bloques, las pausas y los marcadores. El Data Asset permite editar esos campos en Unreal. Edita el manifiesto para versionar cambios reproducibles. Tras importar de nuevo, las asignaciones de voz, la prerreproducción del siguiente acto y los controles de mezcla permanecen en el Data Asset local.

El mismo actor, reloj monotónico y fondo negro de la introducción gobiernan la presentación. Los tiempos relativos del Acto I se calculan desde 0:56. El negro termina a 0:03 del acto, en 0:59 del reloj global. A partir de ahí, cada hito conserva su instante en el reloj global. La capa utiliza los equivalentes Slate de `ScaleBox → SizeBox → Canvas` en el mismo overlay de viewport. Centra un lienzo de 2560 × 1600 y ajusta cada imagen proporcionalmente a su área. Los retratos alternan hasta V21. Los cuatro planos de V7 conservan el lado y el interlocutor. V22 emplea la panorámica y los bloques centrados en una zona inferior protegida por degradado.

| Tiempo del acto | Reloj global | Reproducción |
| --- | --- | --- |
| 0:00–0:03 | 0:56–0:59 | Negro absoluto y silencio |
| 0:03–0:06 | 0:59–1:02 | San Francisco y Cuartel General sobre negro |
| 0:06–0:10 | 1:02–1:06 | Exterior de la sede con los dos rótulos |
| 0:10–0:14 | 1:06–1:10 | Sala del Consejo con los dos rótulos y el del Alto Consejo |
| 0:13 | 1:09 | Entrada de London Calling |
| 0:14–0:35 | 1:10–1:31 | V1. Picard abre la sesión |
| 0:35–1:54 | 1:31–2:50 | V2–V6 |
| 1:54–2:08 | 2:50–3:04 | V7, recuerdo de Picard y frase a 1:59,1 |
| 2:08–2:16 | 3:04–3:12 | V7.1, Locutus, entrada de Ode y comienzo del fundido de London |
| 2:16–2:25 | 3:12–3:21 | V7.2, Enterprise-D y cubo Borg. London alcanza el silencio a 2:23 |
| 2:25–2:54 | 3:21–3:50 | V7.3, regreso a Picard |
| 2:54–5:26 | 3:50–6:22 | V8–V16 |
| 5:26–7:07 | 6:22–8:03 | V17–V20. Crescendo de Myers a 6:38 |
| 7:07–7:29 | 8:03–8:25 | V21. Preparación a 7:08, entrada del texto del voto a 7:25,850 (8:21,850 global) y marcador a 7:28 (8:24 global) |
| 7:29–8:03 | 8:25–8:59 | V22. Resolución, acta, reflexión, clímax a 7:53 (8:49 global) y cierre |
| 8:03–8:08 | 8:59–9:04 | Fundido de imagen y audio hacia negro |
| 8:08 | 9:04 | Negro sostenido y evento `OnActOneFinished` |

Los rótulos de la apertura se dibujan directamente sobre negro y sobre las maestras, con sus sombras tipográficas. La capa anterior de 28 bandas superpuestas oscurecía la foto a intervalos regulares y generaba líneas horizontales. El degradado de contraste de la panorámica final sigue reservado para los diálogos de V22.

V1 presenta sus cuatro bloques a 0:14,35, 0:16,15, 0:21,30 y 0:29,35. El último termina a 0:34,55 y V2 comienza a 0:35 (1:31 global).

## Encuadre de retratos verticales

Los 23 retratos, incluidas las excepciones V2 y V4, ocupan un marco 3:4 de 1104 × 1472 px lógicos, con radio de 24 px y márgenes verticales de 64 px. El marco izquierdo está en (103, 64) y el derecho en (1353, 64). El recorte usa una sola escala para los dos ejes y aplica el marco con el escalado existente del lienzo. V7.2, V22 y las dos maestras conservan su ajuste previo.

La alineación se aplica al excedente de cada eje. 0 % toma el borde inicial, 50 % centra el recorte y 100 % toma el borde final. Cuando un eje encaja exactamente, su alineación carece de efecto.

| Plano | Alineación horizontal | Alineación vertical | Criterio |
| --- | ---: | ---: | --- |
| V2 | 70 % | 50 % | Conserva el rostro y la mano levantada |
| V3 | 15 % | 50 % | Prioriza la mano extendida a la izquierda. La mano apoyada queda parcialmente fuera del marco. |
| V4 | 75 % | 50 % | Prioriza la cabeza, los galones y la mano extendida |
| V5 | 66 % | 50 % | Deja margen al gesto del lado derecho |
| V7.1 | 50 % | 15 % | Conserva la cabeza y los implantes de Locutus |
| V10 | 62 % | 50 % | Conserva la mano levantada |
| V11 | 50 % | 38 % | Conserva el pelo y el gesto de T’Vaen |
| V13 | 43 % | 50 % | Da margen a la mano del lado izquierdo |
| V14 | 66 % | 50 % | Conserva el gesto de Rourke |
| V19 | 50 % | 36 % | Conserva la cabeza y el apoyo de las manos |
| V20 | 50 % | 26 % | Conserva la cabeza y las manos entrelazadas |

V1, V6, V7, V7.3, V8, V9, V12, V15, V16, V17, V18 y V21 usan 50 % en ambos ejes.

## Mezcla y doblaje

Las canciones conservan sus grabaciones por separado y sus velocidades originales. London Calling comienza a 0:13 y Ode to Harrison a 2:08. El solapamiento va de 2:08 a 2:23. En ese tramo se oyen London desde 1:55 de su grabación y Ode desde 0:00. Se equilibran en Unreal con ganancias efectivas iniciales de 0,76 y 0,27 respecto a las señales decodificadas. El MP3 de Ode alcanza +1,73 dBFS al decodificarlo en flotante. La conversión reserva margen con un factor lineal fijo de 0,80 antes de escribir PCM y Unreal compensa ese factor en reproducción. Se conservan picos, dinámica y archivos originales. Ode comienza con un factor adicional de 0,92, que sube suavemente a 1,0 durante el tramo del voto y la resolución. El fundido final usa la misma ventana de cinco segundos que la imagen.

El Acto I se reproduce únicamente con London Calling y Ode to Harrison. **Enable Council Ambience** está desactivado por defecto en el apartado **Audio** de `DA_ActOneTimeline`. Al activarlo se recupera la mezcla ambiental anterior. El bucle de 29,7 s, con un fundido de 300 ms entre sus extremos, entra a 0:13, alcanza su ganancia habitual de 0,85 a 0:15 y desciende al 22 % durante el recuerdo de Locutus. Se recupera durante V7.3. `NextActPreroll` funciona de manera independiente.

El fundido de London se aplica a su propio componente de audio, con interpolación cúbica. Su curva `LondonFade` se puede editar en el apartado **Audio** de `DA_ActOneTimeline`. El eje horizontal de la curva se mide en segundos desde la entrada de Ode. El valor predeterminado de `LondonFade` restituye los puntos aprobados. La versión aprobada usa estos puntos:

| Tiempo del acto | Ganancia relativa de London | Factor adicional aplicado a Ode |
| --- | ---: | ---: |
| 2:08 | 100 % | 100 % |
| 2:11 | 90 % | 100 % |
| 2:13 | 75 % | 100 % |
| 2:16 | 50 % | 100 % |
| 2:18 | 30 % | 100 % |
| 2:21 | 10 % | 100 % |
| 2:23 | 0 % | 100 % |

Las clases `SC_MUSIC`, `SC_AMBIENCE`, `SC_VOICE` y `SC_SFX` son independientes. Cada intervención tiene un campo opcional `Voice`; su reproducción parte de la misma línea temporal que sus bloques. El factor `VoiceDuck` inicial es 0,50 y solo se aplica mientras haya voz. Los actos I y II se conciben sin voces por ahora. En el Acto I, la opción **Enable Voices** del Data Asset queda desactivada. Para incorporar doblaje más adelante, asigna la onda de la intervención, ajusta los tiempos de sus bloques y pausas, y activa esa opción.

`NextActPreroll` admite el futuro ambiente de la bahía antes de `OnActOneFinished`. El acto actual libera las pistas y conserva el overlay negro al concluir. Para un eventual empaquetado, incluye el mapa de la introducción y el directorio `/Game/Cinematics/Act_One` en el conjunto de cocción, dado que el actor resuelve el Data Asset por ruta.

## Verificación

Las cuatro pruebas de Unreal pasaron. El muestreo D3D12 a pantalla completa del MSI, a 2560 × 1600 y con Windows al 150 %, verificó los 21 marcos 3:4 y los rótulos del exterior y del Consejo. La comparación con la referencia dio coincidencia píxel a píxel en V2, V4, V7.2 y V22. Los 62 paquetes audiovisuales, el manifiesto y el código de mezcla coincidieron con la referencia.

En la revisión de 56 segundos pasaron la compilación, la reapertura de ambos paquetes y las cuatro pruebas de Unreal. La comparación confirmó los 334 tiempos absolutos del manifiesto. En D3D12 a pantalla completa se obtuvieron 24 capturas a 2560 × 1600 con Windows al 150 %. La pasada verificó el fundido de la introducción, el negro a 0:56, los rótulos a 0:59, London a 1:09 y el comienzo de V1. Los hitos posteriores se verificaron mediante las pruebas y la comparación de cronologías.

Los resultados siguientes corresponden a las revisiones anteriores con la intro de 54 segundos.

En la revisión sin ambiente pasaron la compilación Win64 Development Editor, la reimportación y la prueba de cronología del Acto I. La pasada técnica D3D12 con WASAPI llegó a 2:25. La traza registró el componente del Consejo detenido y confirmó las entradas de London y Ode, los niveles de la mezcla y los 15 segundos de solapamiento. Los 62 paquetes de la cinemática coincidieron con la referencia.

La prueba `StarTrekRPG.Intro.ActOne.Timeline` valida el montaje importado, los hitos prioritarios, la alternancia, el ambiente desactivado por defecto y su curva opcional, las cuatro clases de mezcla y el formato y margen del PCM de Ode. Las pruebas de intro cubren su cronología, los cinco diseñadores UMG y el reinicio consecutivo de PIE.

| Comprobación | Resultado en el MSI |
| --- | --- |
| Win64 Development Editor e importación NullRHI | Compilación correcta. Reabiertas 27 texturas, tres ondas y cuatro clases. |
| Guion V2 | Blob idéntico al de `25edd8a352dc83880c428d1ec59aa3278c3d1edf`. Los bloques reproducen las 760 palabras y excluyen las acotaciones. |
| Pruebas NullRHI | Superadas `StarTrekRPG.Intro.ActOne.Timeline`, `Designers`, `PIERestart` y `Timeline`. |
| D3D12 a 2560 × 1600 y Windows al 150 % | Recorrido completo en ventana, con 12 capturas. Revisados la localización, el exterior, el Consejo, V1, V2, V6, V7.1, V7.2, V21, V22 y el negro final. |
| D3D12 a pantalla completa | Recorrido completo a 1707 × 1067 efectivos al 150 %. |
| Cronología de la pasada de 2560 × 1600 | Intro 54,002 s. Orden de Ode a 130,005 s. Bloques del voto y el clímax visibles a 450,000 y 475,005 s. Negro total y pistas detenidas a 490,006 s. |
| Continuidad del material | SHA-256 intacto en los 27 paquetes de la intro y los archivos de origen. El salto máximo del bucle de ambiente en su unión fue de 2 unidades PCM16. |

La comprobación de imagen a resolución nativa usó la primera copia del audio del laboratorio. Tras corregir el margen de PCM, se reabrieron los paquetes, se comprobaron las muestras de la onda final y se repitió el arranque hasta Locutus en D3D12. En esa pasada, la orden de Ode llegó a 130,002 s y el mezclador confirmó su inicio a 130,019 s. El dispositivo de salida registró señal durante la transición. La escucha y la aceptación artística corresponden al propietario. El doblaje, las escenas del Acto II y el empaquetado de distribución quedan fuera de esta entrega.

El ajuste de London se comprobó en D3D12 con salida WASAPI en el MSI. En el tramo 1:50–2:35, Unreal ordenó el inicio de London a 15,006 s y el de Ode a 130,005 s. London se detuvo a 145,006 s, tras 15,000 s de solapamiento. La ganancia de Ode durante el tramo coincidió con la automatización anterior. La suma conservadora de los picos PCM de las dos canciones quedó en −6,5 dBFS, y la salida registró señal antes, durante y después del solapamiento. Las cuatro pruebas de Unreal confirmaron los puntos de la curva y los marcadores posteriores.

La revisión de la apertura se comprobó en el MSI durante los primeros 45 segundos del acto, en D3D12 a 2560 × 1600 con Windows al 150 %. Las capturas verificaron el negro inicial, los rótulos, las dos maestras y los cuatro bloques de V1. La captura de V2 a 0:40,20 coincidió píxel a píxel con la referencia. Unreal solicitó London y el ambiente a 15,002 s. El mezclador confirmó ambas entradas y la salida WASAPI registró silencio antes de ellas. Pasaron las cuatro pruebas de intro. La comparación del manifiesto confirmó equivalencia exacta de V2–V22.
