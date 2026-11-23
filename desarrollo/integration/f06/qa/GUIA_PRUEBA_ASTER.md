# ASTER_X1 — prueba del propietario en el MSI

1. Actualiza la rama `plan/f06-aster-aceptacion-x1-20261123` de la PR Draft #206.
2. Haz doble clic en `desarrollo/integration/f06/INICIAR_PRUEBA_ASTER.cmd`.
3. Espera a que termine la compilación. Se abre Tk con **ASTER_X1 y ×1**; la vigilancia arranca automáticamente. La primera preparación necesita Git, Python con Tk, CMake y Visual Studio C++ x64; descarga el Core fijado si no encuentra una copia compatible. No modifica otra copia de Core.
4. Dedica nueve minutos reales a la guardia. No pulses LECTURA ni ANÁLISIS para identificar naves. El resumen central cambia con cada nueva ficha; selecciona contactos para consultar el resumen operativo y el detalle desplazable.

| Tiempo real aproximado | Qué comprobar |
|---|---|
| 0:00 | Carguero inicial identificado, sensores automáticos, ficha verde frente al catálogo QA |
| 1:00 | Nuevo carguero con transpondedor y ficha automática, sin cambiar la selección del oficial |
| 2:30 | D'deridex sin transpondedor: 8 emisores/3 lanzadores observados frente a 6/2 de catálogo QA; ámbar |
| 3:30 | El segundo carguero incorpora un emisor; cambia la observación y queda el registro anterior |
| 4:00 | Nave de clase no determinada, sin transpondedor, armas y escudos observables; blindaje interno no observable, gris |
| 5:00 | La D'deridex presenta emisión ofensiva activa: rojo, sin asumir afiliación ni intención por su clase |
| 6:00 | Una unidad camuflada QA sigue sin aparecer; tampoco se muestra su número ni su inventario |
| 6:30 | Descamuflaje: nueva ficha automática |
| 7:00–9:00 | Elige COMUNICAR, TRANSFERIR A TÁCTICA o TRANSFERIR A CIENCIA. Debe aparecer un recibo vinculado a una observación Core, sin envío automático |
| 7:30–7:45 | Avería de potencia sensorial real del escenario: pérdida de contactos, aviso de indisponibilidad y recuperación autónoma |

**Colores:** verde = coincidencia con referencia, ámbar = diferencia, rojo = emisión ofensiva realmente medida, gris = sin referencia/no observable. Verde no significa inofensivo. Las cifras de los catálogos y equipos son fixtures QA ficticios, no afirmaciones de canon. Las dos fuentes son independientes: referencia de clase y equipamiento instalado en WorldState.

El encabezado operativo mantiene visibles las cantidades esenciales, defensas y propulsión incluso en 1150×700. El resto de las lecturas tiene scroll. Se conservan las tres zonas y el mapa de observaciones. Las órdenes de lectura y análisis son opcionales.

En **Opciones de prueba**, Guardar/Recuperar conserva el punto en memoria. **Guardar ASTER_X1 en disco / Abrir guardia ASTER_X1** permite cerrar la ventana y restaurar el Core en otro proceso. La restauración queda pausada para poder revisarla; pulsa Reanudar. Las entregas y observaciones son persistentes, las preferencias de navegación de Tk no se serializan en el archivo Core.

El lanzador escribe `latencia-<fecha>.jsonl` junto al build QA local: instantes monotónicos de fuente nativa, recepción Core, publicación F06, recepción y refresco de Tk. `source_to_gui_s` usa el vencimiento real de la aparición, e incluye retrasos del bucle; `realtime` distingue la guardia de pasos manuales. No comparar épocas de reloj C++/Python: cada tramo conserva sus propios instantes y unidades. Una pausa desplaza el origen real; no demuestra tiempo durante la pausa.

Para la regresión histórica, selecciona **1. Guardia normal** en Opciones de prueba y pulsa Iniciar; permite ×15/×30/×60. Dura ocho horas Core. No sustituye esta aceptación ×1. También puede arrancarse con `INICIAR_PRUEBA_ASTER.ps1 -Mode eight-hours`.

**Límites:** Tk es el banco F06, no LCARS/Unreal F07. Las transferencias llegan a colas QA autenticadas en el mismo Core, no a un NPC o una consola final. El perfil instalado es el refit individual de la Enterprise-D, clase Galaxy, Proyecto Valhalla; el armazón F04 sigue siendo Miranda sintética. El camuflaje QA es una máscara física efectiva explícita, no una simulación completa de todas las tecnologías de ocultación. ASTER no es el universo F13 ni una guardia F08 certificada.

El propietario debe anotar incidencias, revisar el log y decidir la aceptación visual. Ninguna prueba de Cloud declara superada la aceptación MSI ni cierra F06.
