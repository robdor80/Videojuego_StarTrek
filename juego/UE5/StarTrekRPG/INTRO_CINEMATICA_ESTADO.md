# Estado de la introducción cinematográfica

## Objetivo y protección

Reproducir las diez escenas en el nivel propio de la introducción y conservar la composición de Pike tomada del recurso local del propietario. Las cinco composiciones serán editables en el diseñador UMG.

- Rama de trabajo `feat/intro-cinematic-automation`.
- HEAD inicial `b2a1d2ab63b0467a904a3097d50d7a1e992ffc99`, rama original `codex/f06-aster-tres-zonas-20261123`.
- Copia local `laboratorios/cinematics/intro-cinematic-automation/originales-20261125-031839`. Incluye todo el árbol original `Cinematics` y un inventario `SHA256.csv` comprobado contra los originales. También contiene una copia de los cuatro cambios locales preexistentes del proyecto.
- Recursos protegidos. Nivel, secuencia, controlador, widget original, widget de respaldo, fuentes y texturas de la introducción. Se verificaron 21 paquetes originales y se confirmó que solo cambió el mapa. El MP3 original y los cuatro archivos locales preexistentes conservan su SHA-256.
- Copia de entrega en `laboratorios/cinematics/intro-cinematic-automation/entrega-20261125-033728`, con 27 paquetes y `SHA256.csv` verificado. Las dos copias residen en la unidad local C:, el único volumen de datos disponible en el MSI durante la tarea.
- Unreal Engine 5.8.4 según la asociación local. La configuración del proyecto y los tres archivos de solución/configuración de VS preexistentes quedan fuera de los commits de esta tarea.
- Git excluye los paquetes de Unreal. Los recursos de la introducción están guardados en el proyecto local y respaldados con SHA-256. No se publicó una PR porque la rama remota quedaría sin el nivel, los widgets y el audio.

## Cronología de reproducción

| Plano | Entrada | Opacidad completa | Inicio de salida | Final de salida |
| --- | ---: | ---: | ---: | ---: |
| Enterprise NCC-1701 | 1.000 | 3.000 | 4.500 | 5.500 |
| Pike | 5.500 | 7.500 | 9.000 | 10.000 |
| Enterprise NCC-1701-A | 10.000 | 12.000 | 13.500 | 14.500 |
| Kirk | 14.500 | 16.500 | 18.000 | 19.000 |
| Voyager | 19.000 | 21.000 | 22.500 | 23.500 |
| Janeway | 23.500 | 25.500 | 27.000 | 28.000 |
| Deep Space Nine | 28.000 | 30.000 | 31.500 | 32.500 |
| Sisko | 32.500 | 34.500 | 36.000 | 37.000 |
| Enterprise NCC-1701-D | 37.000 | 39.000 | 42.000 | 43.000 |
| Picard | 43.000 | 45.000 | 53.000 | 56.000 |

Los tiempos están en segundos desde el inicio de la introducción. Cada imagen y sus propios datos usan la misma opacidad durante todo el plano. Las salidas de un segundo terminan justo al inicio del plano siguiente, cuando ambos están a cero. Picard y el homenaje conservan el fundido final de 53 a 56 s. El homenaje aparece entre 47 y 48 s. El Acto I empieza en 0:56.

## Cierre musical

El MP3 original dura 148,323 s. Su frase musical decae de forma natural después de 0:54. La versión de 56 segundos usa el material continuo desde el comienzo del original y conserva el PCM de los primeros 53 segundos. La música se funde con un coseno elevado de 0:53 a 0:56.

Para actualizar una copia local ya preparada, usa FFmpeg y el commandlet de Unreal desde la raíz del repositorio. Elige la carpeta de trabajo en `laboratorios/` y conserva una copia de los paquetes previos.

```powershell
$project = (Resolve-Path 'juego/UE5/StarTrekRPG/StarTrekRPG.uproject').Path
$editor = 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
$source = 'C:/Users/andro/Pictures/Star Trek intro/Star Trek - Michael Giacchino.mp3'
$work = (New-Item -ItemType Directory -Force 'laboratorios/cinematics/actualizar-intro-56').FullName
$wav = Join-Path $work 'SW_Intro_Music.wav'
ffmpeg -nostdin -v error -xerror -i $source -t 56 -af 'afade=t=out:st=53:d=3:curve=hsin' -map_metadata -1 -vn -c:a pcm_s16le -ar 44100 -ac 2 $wav
if ($LASTEXITCODE -ne 0) { throw 'No se pudo generar el WAV de la intro.' }
& $editor $project -run=IntroAssetSetup -RefreshMusic "-MusicWav=$wav" -nullrhi -unattended "-UserDir=$work" "-AbsLog=$work/import.log"
if ($LASTEXITCODE -ne 0) { throw 'No se pudo actualizar el audio de la intro.' }

$timeline = (Resolve-Path 'audiovisual/presentation/guiones/STAR_TREK_LEGENDS_ACTO_I_TIMELINE.json').Path
$assets = 'C:/Users/andro/Pictures/Star Trek Acto 1'
& $editor $project -run=ActOneAssetSetup -Apply "-Timeline=$timeline" "-AssetsRoot=$assets" `
    "-WavRoot=$work" -nullrhi -unattended "-UserDir=$work" "-AbsLog=$work/acto-i.log"
if ($LASTEXITCODE -ne 0) { throw 'No se pudo actualizar el Data Asset del Acto I.' }
```

La actualización del Data Asset reutiliza las ondas instaladas. Los tiempos relativos y el comando de reproducción están en la [guía de continuidad del Acto I](../../../audiovisual/presentation/guiones/ACTO_I_CONTINUIDAD.md).

## Bloques de la versión anterior

| Bloque | Estado |
|---|---|
| 0. Seguridad | Validado. Copia verificada y rama creada. |
| 1. Mecanismo | Validado. Compilación Win64 de editor y prueba automatizada de cronología. Un único actor inicia la reproducción del nivel. |
| 2. Enterprise y Pike | Validados en paquetes reabiertos. Se compararon jerarquía, orden, anclajes, alineación, posiciones, tamaños, pinceles, colores, textos y tipografía con la plantilla local. |
| 3. Otras parejas | Validadas. Los cinco Widget Blueprints compilaron sin errores y abrieron en sus editores UMG. Las diez escenas se comprobaron en capturas de la ejecución. |
| 4. Música y homenaje | Validados técnicamente. MP3 de 148.323250 s, estéreo, 44.1 kHz, 320 kb/s. Sound Wave PCM de 54.000 s, sin bucle, con fundido de 53.000 a 54.000 s. Homenaje visible junto a Picard. |
| 5. Validación | Validado en el MSI a 2560 × 1600 y en dos arranques consecutivos en PIE. Pendientes la escucha humana y la aceptación artística del propietario. |

Último commit funcional del reproductor `73fc2b4b`. La integración reproducible de los paquetes está en `8ede64a3` y los paquetes guardados están en el proyecto local.

## Arquitectura

`Source/StarTrekRPG/Private/Intro/IntroTimeline.h` define los tiempos absolutos y las curvas de opacidad. Un actor exclusivo del nivel muestrea el reloj monotónico, aplica opacidad a los elementos UMG por nombre y mantiene un fondo negro común. Las composiciones conservan sus propios elementos, jerarquía y escalado. El actor publica `OnIntroFinished` tras fijar el negro y detener el audio.

## Recursos locales y edición

- Nivel `/Game/Cinematics/L_Intro_StarTrekLegends`. Abre el nivel en el explorador de contenido y pulsa **Play**. Para repetir la intro, pulsa **Stop** y vuelve a pulsar **Play**.
- Widgets de composición en `/Game/Cinematics/UI_Intro/`: `WBP_Intro_Pike`, `WBP_Intro_Kirk`, `WBP_Intro_Janeway`, `WBP_Intro_Sisko` y `WBP_Intro_Picard`. Abre cada recurso en **Designer**. Usa el icono de visibilidad del diseñador en **Hierarchy** para aislar la nave o el capitán mientras editas.
- Selecciona un elemento en **Hierarchy**. En **Details > Slot (Canvas Panel Slot)** edita posición, tamaño, anclaje y alineación. En **Appearance** edita pincel, color o fuente. En **Content** edita el texto.
- El homenaje provisional se coloca por encima del retrato para que pueda coexistir con él a plena opacidad. En Picard, selecciona `TXT_HomenajePatrickStewart` o `TXT_FechasPatrickStewart` para editar cada bloque por separado. Conserva los nombres de ambos y de `IMG_FondoNegro`, `IMG_Nave`, `TXT_Matricula`, `IMG_LineaNave`, `TXT_NombreNave`, `IMG_Capitan`, `TXT_RangoCapitan`, `IMG_LineaCapitan` y `TXT_NombreCapitan`. El reproductor localiza esos elementos por nombre.
- Audio local en `/Game/Cinematics/Audio_Intro/SW_Intro_Music`. El fondo negro se muestra durante la preparación. El reloj visual y la orden de reproducción arrancan juntos tras los primeros fotogramas de carga. El fundido de audio está grabado en la muestra y el actor detiene el componente al llegar a 56.000 s.
- El nivel conserva el actor de la secuencia con **Auto Play** desactivado. Se retiró del nivel la instancia de `BP_IntroController`. El Blueprint, el widget original, su copia de respaldo y el recurso de la secuencia se conservaron.

El commandlet de editor `IntroAssetSetup` abre y verifica los paquetes locales. Con `-Apply -MusicWav="ruta-absoluta-del-WAV"` puede reconstruir los cinco widgets a partir de una copia restaurada del contenido original y conectar el nivel. Conserva los widgets y el audio que ya existan, salvo el reemplazo explícito mediante `-RefreshMusic`. La reconstrucción desde el respaldo original se probó por separado en un laboratorio. La verificación de diseño inicial usa `-CheckInitialLayout`. Omite ese parámetro una vez que ajustes deliberadamente la composición de Pike.

## Resultados y tolerancias de la versión de 54 segundos

| Prueba | Resultado |
|---|---|
| Unreal 5.8.4, Win64 Development Editor | Compilación correcta y cinco Widget Blueprints compilados al reabrir los paquetes. Reconstrucción desde una copia del original con 0 errores. |
| `StarTrekRPG.Intro.Timeline` | Superada. Horarios absolutos, rampas de imagen y datos, salidas completas, homenaje y negro a 54.000 s. |
| `StarTrekRPG.Intro.Designers` | Superada. Los cinco editores de Widget Blueprint abrieron. |
| `StarTrekRPG.Intro.PIERestart` | Superada. Dos arranques PIE en la misma sesión con un único reproductor activo en cada uno. |
| D3D12, 2560 × 1600 en el MSI | Negro inicial y final verificados píxel a píxel. Capturas de las diez escenas, transición Enterprise–Pike, Picard con homenaje y fundido final. |
| Cronología durante la reproducción | 35 hitos registrados. Máximo retraso de muestreo de 3.434 ms. Negro final y orden de parada del audio en 54.003017 s. |
| Salida de audio del MSI | Una orden de inicio y una de parada. Primera confirmación del mezclador a 30.388 ms. El monitor de salida de Windows registró caída a cero después del fundido, con una última lectura superior a 0.0001 en 54.068 s. La salida incorpora el búfer del mezclador y del dispositivo. |

El primer ensayo en frío reveló una espera larga del motor en sus primeros fotogramas. El reproductor prepara el fondo negro antes de iniciar el reloj y el audio. Durante la reproducción, Unreal aplica las opacidades en el primer fotograma disponible a partir de cada hito. El archivo de audio contiene exactamente 54.000 s de muestras.

La fuente Federation recurre al glifo de sustitución de Slate para algunos caracteres acentuados. Se conservaron la fuente y los textos solicitados. Los avisos de carga de ajustes de compresión de animación de ACL son del entorno existente. Queda pendiente la revisión artística de las cuatro parejas provisionales y del homenaje, así como la escucha humana. Las capturas, registros y medición del dispositivo están en el laboratorio de la tarea.
