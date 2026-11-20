# Valhalla — rendimiento V08/V09: conservación de estadísticas Unreal Insights
Fecha: 13/11/2026. Estado: **estadísticas recuperadas; originales .utrace todavía no autorizados para borrado**.

## Procedencia y alcance
- Fuente: \`StarTrek_Rendimiento_14_Capturas.zip\` (ZIP original de 2.723.788 bytes; SHA-256: \`1a152c1199b67ed29c2a8bec0c879db228d0b1127c5b72d19a52bbbedfac5828\`).
- Capturas fuente: **14 .utrace**, **13,016 GiB** acumulados, agrupados en V08 (4), V09-P01 (3) y V09-P01B (7).
- Extracción local con \`C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealInsights.exe\`, comandos \`TimingInsights.ExportTimerStatistics\`, \`TimingInsights.ExportTimers\`, \`TimingInsights.ExportThreads\`.
- Resultados: **56 CSV** (estadísticas agregadas, filtrado GPU, temporizadores e hilos); 14 manifiestos y 14 registros de herramienta. Cada uno terminó con \`codigo_salida=0\` y muestra datos tabulares.
- Copia íntegra de los 56 CSV y los manifiestos: **guardar ZIP original fuera de laboratorios**. Este documento y el CSV de resumen se versionan; el ZIP completo de los datos fuente se conserva localmente de momento.
- Los valores \`I.Avg\` del exportador están en segundos; aquí se multiplican por 1000 para mostrar **milisegundos por invocación**.
- Con nombres duplicados de temporizador se selecciona la fila con mayor \`Count\`. En \`Frame\` hay varias pistas; esto **NO** equivale automáticamente al tiempo total de fotograma o a FPS de juego.

## Resultados (medias de temporizador, milisegundos)
| Etapa | Variante | Frame (pista principal) | SceneRender | DeferredLighting | LumenScreenProbeGather | ShadowDepths | DLSS (recuento) |
|---|---|---:|---:|---:|---:|---:|---:|
| V08 | native_sw | 10,83 | 11,02 | 6,08 | 3,96 | 1,11 | 34,06 (2) |
| V08 | native_sw_p4096 | 11,18 | 11,43 | 6,15 | 3,82 | 1,26 | 36,81 (2) |
| V08 | quality_sw | 8,46 | 8,54 | 2,98 | 1,93 | 0,96 | 1,86 (9073) |
| V08 | quality_sw_p4096 | 9,10 | 8,99 | 2,90 | 1,84 | 1,63 | 1,85 (8490) |
| V09-P01 | base_sw_p4096 | 8,70 | 8,76 | 2,91 | 1,85 | 1,33 | 1,86 (8155) |
| V09-P01 | exp1_sw_p4096 | 9,04 | 9,06 | 2,91 | 1,87 | 1,68 | 1,85 (7829) |
| V09-P01 | exp2_sw_p4096 | 8,40 | 8,44 | 2,94 | 1,90 | 0,95 | 1,89 (8503) |
| V09-P01B | base_sw_p4096 | 9,23 | 9,11 | 2,98 | 2,11 | 1,24 | 1,86 (15742) |
| V09-P01B | clean_sw_p4096 | 8,73 | 8,75 | 2,93 | 2,07 | 1,00 | 1,83 (16395) |
| V09-P01B | exp1_sw_p4096 | 8,83 | 8,64 | 2,60 | 2,05 | 1,19 | 1,87 (16516) |
| V09-P01B | exp2_sw_p4096 | 9,88 | 9,61 | 2,41 | 1,84 | 2,36 | 1,91 (14512) |
| V09-P01B | locked_base_sw_p4096 | 8,82 | 8,85 | 2,93 | 2,00 | 0,99 | 1,84 (10409) |
| V09-P01B | locked_clean_sw_p4096 | 8,85 | 8,90 | 2,98 | 2,11 | 0,99 | 1,84 (10363) |
| V09-P01B | locked_final_sw_p4096 | 8,43 | 8,44 | 2,62 | 2,07 | 0,92 | 1,90 (10909) |

Para leer los datos con precisión, el CSV \`VALHALLA_14_CAPTURAS_RESUMEN.csv\` guarda conteos y otras medidas.

## Lecturas comparativas preliminares
- En V09-P01, \`exp1\` frente a \`base\`: Frame **+3,9 %** y SceneRender **+3,4 %**; \`exp2\` frente a \`base\`: Frame **−3,4 %** y SceneRender **−3,6 %**.
- En V09-P01B, \`clean\` frente a \`base\`: Frame **−5,4 %** y SceneRender **−3,9 %**.
- En V09-P01B, \`exp2\` frente a \`base\`: Frame **+7,1 %** y SceneRender **+5,5 %**; contrapartida destacable: \`ShadowDepths\` 2,36 ms frente a 1,24 ms.
- Comparación preferente bajo nombre de prueba \`locked\`: \`locked_final\` frente a \`locked_base\`: Frame **8,430 ms frente a 8,816 ms (−4,4 %)**; SceneRender **8,437 ms frente a 8,848 ms (−4,6 %)**. Son diferencias de temporizador, no prueba de un incremento equivalente de FPS.
- En V08, \`native\` y \`quality\` difieren notablemente en DLSS y número de invocaciones: en \`native\`, DLSS se ejecutó solo **2 veces**, de modo que sus medias altas **no son coste estable por fotograma**. No interpretar la diferencia V08 como una comparación aislada de una sola variable.

**Limitaciones:** no se han comprobado aquí equivalencia de escena, resolución interna, cámara, configuración gráfica, periodos de calentamiento ni distribución temporal de cada variante. Las duraciones de captura varían. No se pueden demostrar mejoras causales o FPS reales con estas tablas aisladas. Los temporizadores anidados no se suman.

## Restricción de borrado
Las exportaciones son estadísticas agregadas y no conservan la cronología exacta de eventos ni todos los canales de trace. **No se deben borrar automáticamente los 14 .utrace antes de aceptar expresamente la pérdida del detalle temporal**, una vez preservados los 56 CSV originales y la documentación de pruebas.

Los artefactos regenerables de compilación (\`.pch\`, ciertos \`.pdb\`, \`.obj\` de compilación, \`Intermediate\`, cachés Zen/DDC) se pueden auditar y limpiar por separado, con Unreal y Visual Studio cerrados. **No borrar por extensión archivos 3D fuente, assets Unreal, escenas ni datos únicos**.

Pendiente: auditar \`C:\F04\`, que está fuera de la raíz oficial del repositorio; no se ha inspeccionado ni modificado.
