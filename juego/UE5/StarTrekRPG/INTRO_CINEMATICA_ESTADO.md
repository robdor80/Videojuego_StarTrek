# Estado de la introducción cinematográfica

## Objetivo y protección

Reproducir las diez escenas en el nivel propio de la introducción y conservar la composición de Pike tomada del recurso local del propietario. Las cinco composiciones serán editables en el diseñador UMG.

- Rama de trabajo `feat/intro-cinematic-automation`.
- HEAD inicial `b2a1d2ab63b0467a904a3097d50d7a1e992ffc99`, rama original `codex/f06-aster-tres-zonas-20261123`.
- Copia local `laboratorios/cinematics/intro-cinematic-automation/originales-20261125-031839`. Incluye todo el árbol original `Cinematics` y un inventario `SHA256.csv` comprobado contra los originales. También contiene una copia de los cuatro cambios locales preexistentes del proyecto.
- Recursos protegidos: nivel, secuencia, controlador, widget original, widget de respaldo, fuentes y texturas de la introducción.
- Unreal Engine 5.8 según la asociación local. La configuración del proyecto y los tres archivos de solución/configuración de VS preexistentes quedan fuera de los commits de esta tarea.
- Git excluye los paquetes de Unreal. Los recursos de la introducción se guardarán en el proyecto local dentro de Unreal y los commits recogerán código y documentación.

## Cronología aprobada

| Escena | Imagen | Datos | Opacidad completa |
|---|---:|---:|---:|
| Enterprise NCC-1701 | 1.000 | 2.000 | 3.000 |
| Pike | 5.500 | 6.500 | 7.500 |
| Enterprise NCC-1701-A | 10.000 | 11.000 | 12.000 |
| Kirk | 14.500 | 15.500 | 16.500 |
| Voyager | 19.000 | 20.000 | 21.000 |
| Janeway | 23.500 | 24.500 | 25.500 |
| Deep Space Nine | 28.000 | 29.000 | 30.000 |
| Sisko | 32.500 | 33.500 | 34.500 |
| Enterprise NCC-1701-D | 37.000 | 38.000 | 39.000 |
| Picard | 43.000 | 44.000 | 45.000 |
| Homenaje | — | 47.000 | 48.000 |

Negro y arranque musical en 0.000 s. El inicio de cada imagen activa la salida de dos segundos de la escena anterior. Picard y su homenaje se funden entre 53.000 y 54.000 s.

## Bloques

| Bloque | Estado |
|---|---|
| 0. Seguridad | Validado. Copia verificada y rama creada. |
| 1. Mecanismo | Implementado y validado por compilación de editor y prueba automatizada de cronología. Integración de nivel pendiente. |
| 2. Enterprise y Pike | Validados en paquetes reabiertos. Se compararon jerarquía, orden, anclajes, alineación, posiciones, tamaños, pinceles, colores, textos y tipografía con la plantilla local. |
| 3. Otras parejas | Implementadas. Los cinco Widget Blueprints reabrieron y compilaron sin errores. Pendiente comprobación en el diseñador y reproducción completa. |
| 4. Música y homenaje | Implementados. El MP3 dura 148.323250 s, estéreo, 44.1 kHz, 320 kb/s. Se importó un Sound Wave PCM de 54.000 s con fundido de 53.000 a 54.000 s. |
| 5. Validación | En curso. La primera reproducción en frío reveló una espera de render en los primeros fotogramas. El fondo negro se prepara antes del arranque sincronizado para evitar saltos al cargar. |

Primer bloque funcional en Git: `caab4344`. La integración de los paquetes de Unreal queda guardada en el directorio local del proyecto.

## Arquitectura

`Source/StarTrekRPG/Private/Intro/IntroTimeline.h` define los tiempos absolutos y las curvas de opacidad. Un actor exclusivo del nivel muestrea el reloj monotónico, aplica opacidad a los elementos UMG por nombre y mantiene un fondo negro común. Las composiciones conservan sus propios elementos, jerarquía y escalado. El actor publica `OnIntroFinished` tras fijar el negro y detener el audio.

## Recursos locales y edición

- Nivel `/Game/Cinematics/L_Intro_StarTrekLegends`. Abre el nivel en el explorador de contenido y pulsa **Play**. Para repetir la intro, pulsa **Stop** y vuelve a pulsar **Play**.
- Widgets de composición en `/Game/Cinematics/UI_Intro/`: `WBP_Intro_Pike`, `WBP_Intro_Kirk`, `WBP_Intro_Janeway`, `WBP_Intro_Sisko` y `WBP_Intro_Picard`. Abre cada recurso en **Designer**. Usa el icono de visibilidad del diseñador en **Hierarchy** para aislar la nave o el capitán mientras editas.
- Selecciona un elemento en **Hierarchy**. En **Details > Slot (Canvas Panel Slot)** edita posición, tamaño, anclaje y alineación. En **Appearance** edita pincel, color o fuente. En **Content** edita el texto.
- El homenaje provisional se coloca por encima del retrato para que pueda coexistir con él a plena opacidad. En Picard, selecciona `TXT_HomenajePatrickStewart` o `TXT_FechasPatrickStewart` para editar cada bloque por separado. Conserva los nombres de ambos y de `IMG_FondoNegro`, `IMG_Nave`, `TXT_Matricula`, `IMG_LineaNave`, `TXT_NombreNave`, `IMG_Capitan`, `TXT_RangoCapitan`, `IMG_LineaCapitan` y `TXT_NombreCapitan`. El reproductor localiza esos elementos por nombre.
- Audio local en `/Game/Cinematics/Audio_Intro/SW_Intro_Music`. El fondo negro se muestra durante la preparación. El reloj visual y la orden de reproducción arrancan juntos tras los primeros fotogramas de carga. El fundido de audio está grabado en la muestra y el actor detiene el componente al llegar a 54.000 s.
- El nivel conserva el actor de la secuencia con **Auto Play** desactivado. Se retiró del nivel la instancia de `BP_IntroController`. El Blueprint, el widget original, su copia de respaldo y el recurso de la secuencia se conservaron.

El commandlet de editor `IntroAssetSetup` abre y verifica los paquetes locales. Con `-Apply -MusicWav="ruta-absoluta-del-WAV"` puede reconstruir los cinco widgets a partir de una copia restaurada del contenido original y conectar el nivel. Conserva los widgets y el audio que ya existan. La reconstrucción desde el respaldo original se probó por separado en un laboratorio. La verificación de diseño inicial usa `-CheckInitialLayout`. Omite ese parámetro una vez que ajustes deliberadamente la composición de Pike.
