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
| 2. Enterprise y Pike | Pendiente. |
| 3. Otras parejas | Pendiente. |
| 4. Música y homenaje | MP3 verificado con ffprobe: 148.323250 s, estéreo, 44.1 kHz, 320 kb/s. Se utilizarán los primeros 54 s. |
| 5. Validación | Pendiente. |

Primer bloque funcional: commit `feat(intro): implementar reloj y fundidos de la introducción`.

## Arquitectura

`Source/StarTrekRPG/Private/Intro/IntroTimeline.h` define los tiempos absolutos y las curvas de opacidad. Un actor exclusivo del nivel muestrea el reloj monotónico, aplica opacidad a los elementos UMG por nombre y mantiene un fondo negro común. Las composiciones conservan sus propios elementos, jerarquía y escalado. El actor publica `OnIntroFinished` tras fijar el negro y detener el audio.
