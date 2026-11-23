# ASTER_X1 — prueba del propietario en el MSI

1. Actualiza la rama `codex/f06-aster-tres-zonas-20261123` de la PR Draft de implementación, derivada de la especificación #212.
2. Haz doble clic en `desarrollo/integration/f06/INICIAR_PRUEBA_ASTER.cmd`.
3. Espera a que termine la compilación. Se abre Tk con **ASTER_X1 y ×1**; la vigilancia arranca automáticamente. La primera preparación necesita Git, Python con Tk, CMake y Visual Studio C++ x64; descarga el Core fijado si no encuentra una copia compatible. No modifica otra copia de Core.
4. Dedica nueve minutos reales a la guardia. Los marcos son **rojo izquierda / azul centro / verde derecha**. GENERAL muestra el entorno; CONTACTOS incluye todos los objetos. Selecciona Aster IV, pulsa ANÁLISIS y explora sus presiones parciales. La computadora identifica las naves sin pulsar LECTURA.
5. Cuando llegue una nave prioritaria, comprueba que lista, mapa y ficha cambian juntos. **Retomar Aster IV** recupera el estudio y su desplazamiento. **SEGUIR** abre una lista de objetivos marcados y envía automáticamente las nuevas lecturas a Táctica; **Dejar de seguir** termina esa transferencia.
6. **Comunicar por voz** abre un guion QA para que tú lo pronuncies. **Enviar informe** permite elegir capitán/superior, Táctica o Ciencia. La confirmación corresponde a una entrega real a la cola QA; no existe todavía un consumidor NPC final.

| Tiempo real aproximado | Qué comprobar |
|---|---|
| 0:00 | Estrella, seis planetas, cuatro lunas, estación, nebulosa, cinturón y sonda; seis informes científicos Core; carguero inicial identificado |
| 1:00 | Nuevo carguero con transpondedor y ficha automática, sin cambiar la selección del oficial |
| 2:30 | D'deridex sin transpondedor: 8 emisores/3 lanzadores observados frente a 6/2 de catálogo QA; ámbar |
| 3:30 | El segundo carguero incorpora un emisor; cambia la observación y queda el registro anterior |
| 4:00 | Nave de clase no determinada, sin transpondedor, armas y escudos observables; blindaje interno no observable, gris |
| 5:00 | La D'deridex presenta emisión ofensiva activa: rojo, sin asumir afiliación ni intención por su clase |
| 6:00 | Una unidad camuflada QA sigue sin aparecer; tampoco se muestra su número ni su inventario |
| 6:30 | Descamuflaje: nueva ficha automática |
| 7:00 | Cesa la emisión ofensiva y se retira su alerta. Puedes enviar un informe actualizado del mismo contacto |
| 7:00–9:00 | Comprueba guion de voz, elección de destinatario y confirmación de informe. El seguimiento comparte los cambios automáticamente con Táctica |
| 7:30–7:45 | Avería de potencia sensorial real del escenario: pérdida de contactos, aviso de indisponibilidad y recuperación autónoma |

**Colores:** verde = coincidencia con referencia, ámbar = diferencia, rojo = emisión ofensiva realmente medida, gris = sin referencia/no observable. Verde no significa inofensivo. Las cifras de los catálogos y equipos son fixtures QA ficticios, no afirmaciones de canon. Las dos fuentes son independientes: referencia de clase y equipamiento instalado en WorldState.

La zona central conserva el mapa arriba y un resumen corto debajo. La ficha derecha tiene desplazamiento; el inicio se recupera al cambiar de objeto. El análisis normal es inmediato y no utiliza barra de espera. Sus resultados nuevos son cálculos de física sobre mediciones Core: presiones parciales, extensión angular estimada, desplazamiento entre observaciones archivadas y evolución técnica. Si un dominio carece de medidas, se indica su límite. No representa imágenes o modelos inexistentes como cargados.

En **Opciones de prueba**, Guardar/Recuperar conserva el punto en memoria. **Guardar ASTER_X1 en disco / Abrir guardia ASTER_X1** permite cerrar la ventana y restaurar el Core en otro proceso. La restauración queda pausada; pulsa Reanudar. Conserva juntos el archivo `.aster` y su acompañante `.aster.ui.json`: el primero guarda Core y sus entregas; el segundo guarda vistas, selección, análisis solicitados, estudio interrumpido y notas, vinculado al SHA-256 del primero. Tras una pérdida de señal, el seguimiento dedicado queda suspendido para liberar recursos; selecciona el objetivo y pulsa SEGUIR al recuperarse.

El lanzador escribe `latencia-<fecha>.jsonl` junto al build QA local: instantes monotónicos de fuente nativa, recepción Core, publicación F06, recepción y refresco de Tk. `source_to_gui_s` usa el vencimiento real de la aparición, e incluye retrasos del bucle; `realtime` distingue la guardia de pasos manuales. No comparar épocas de reloj C++/Python: cada tramo conserva sus propios instantes y unidades. Una pausa desplaza el origen real; no demuestra tiempo durante la pausa.

Para la regresión histórica, selecciona **1. Guardia normal** en Opciones de prueba y pulsa Iniciar; permite ×15/×30/×60. Dura ocho horas Core. No sustituye esta aceptación ×1. También puede arrancarse con `INICIAR_PRUEBA_ASTER.ps1 -Mode eight-hours`.

**Límites:** Tk es el banco F06, no LCARS/Unreal F07. Las transferencias llegan a colas QA autenticadas en el mismo Core, no a un NPC o una consola final. El perfil instalado es el refit individual de la Enterprise-D, clase Galaxy, Proyecto Valhalla; el armazón F04 sigue siendo Miranda sintética. El camuflaje QA es una máscara física efectiva explícita, no una simulación completa de todas las tecnologías de ocultación. ASTER no es el universo F13 ni una guardia F08 certificada.

El propietario debe anotar incidencias, revisar el log y decidir la aceptación visual. Ninguna prueba de Cloud declara superada la aceptación MSI ni cierra F06.
