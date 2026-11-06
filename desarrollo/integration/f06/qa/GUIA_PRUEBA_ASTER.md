# F06 — Guardia autónoma del Sistema Aster (banco de pruebas)

**Estado:** banco de pruebas F06 preparado en PR #94 sobre F06 Draft #91; no sustituye aceptación UE5 ni las consolas F07.

## Qué comprobará el jugador

La computadora de la nave mantiene vigilancia pasiva continua, prioriza **contactos detectados de verdad** y, sin intervención del oficial, puede reservar un barrido focal temporal, ejecutarlo cuando avance el reloj de CoreRPG, guardar la observación y mostrar el resultado. Dos análisis focales como máximo coinciden en el tiempo (junto a las operaciones manuales). Si los sensores están averiados, reconoce el fallo; si hay interferencias, no inventa detecciones.

No hay nave enemiga improvisada, planetas engendrados por una consola ni resultados científicos falsos. **El escenario es la fixture Aster de 20 entidades y cinco momentos de cambio; no es el universo F13 en funcionamiento.** El escenario de pruebas usa una sesión sintética Miranda con **perfil de sensores refit Enterprise-D 5**. Es una instalación de laboratorio, **no es una Galaxy físicamente jugable**.

## Cómo abrirlo en el MSI

1. En **GitHub Desktop**, seleccionar la rama `feat/f06-sensores-core` una vez integrada PR #94, y usar **Fetch/Pull**. Esto no requiere fusionar F06 con `main`.
2. Abrir la carpeta `desarrollo/integration/f06` y hacer **doble clic en `INICIAR_PRUEBA_ASTER.cmd`**. No hay que copiar comandos ni abrir Unreal. Alternativa por PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\INICIAR_PRUEBA_ASTER.ps1`.

3. Se compila el ejecutable nativo y se abre la ventana. El script usa CoreRPG en la **revisión exacta aprobada**; si no hay una copia compatible, descarga otra dentro de `laboratorios/f06/qa/deps`. Todo lo descargado y compilado queda bajo `laboratorios`, fuera del control de versiones y sin modificar los assets 3D.

El generador CMake por defecto es `Visual Studio 18 2026`, el mismo previsto por el script F06 existente. Si el MSI tiene Visual Studio 2022, indicar `-Generator 'Visual Studio 17 2022'`. Requiere Python 3 con Tkinter, CMake, Git, compilador C++ y acceso a GitHub para la descarga inicial de dependencias. Una compilación previa se reutiliza en siguientes aperturas; no se realizan comprobaciones interminables en cada uso.

## Lo único que debe hacer el jugador

- Pulsar **Iniciar**. A velocidad **×30**, ocho horas de guardia tardan **16 minutos reales**. Se puede cambiar a ×15 o ×60, y pausar cuando algo llame la atención.
- **Prueba 1. Guardia normal:** observar qué detecta, cómo lo estudia y si avisa lo suficiente.
- **Prueba 2. Repetición idéntica:** mismo Sistema Aster, mismas condiciones y mismo reloj; el comportamiento debe coincidir con la prueba 1 si la cadencia de avance es idéntica.
- **Prueba 3. Interferencias:** el Host introduce un entorno EM adverso a la hora 1 y lo retira a la hora 2.
- **Prueba 4. Avería y recuperación:** se corta la alimentación de sensores a la hora 2 y se restaura a las 2 h 30 min.
- **Guardar punto / Recuperar punto** usa `f04_save/f04_load` sobre la misma sesión de CoreRPG (punto de prueba en memoria, no archivo definitivo).
- Escribir comentarios en **Tus impresiones** y pulsar **Exportar informe**. Adjuntar ese TXT a ChatGPT permite ajustar comportamiento, mensajes y prioridades con evidencia real.

### Vocabulario en lenguaje corriente

Un **barrido focalizado** no es más que observar con más detalle una señal determinada; la computadora puede iniciarlo por sí sola. **Contacto perdido** significa que dejamos de verlo, no que la nave haya sido destruida o saltado a warp. **Análisis completado** significa observación de sensores, **no** que Ciencia haya identificado automáticamente toda la vida, composición o historia de un planeta. Para eso se necesita equipo científico legítimo y observaciones adicionales.

### Qué muestra la ventana (y qué no)

La ventana solo contiene estado general, avisos importantes, pausa, velocidad, selección de escenario y controles mínimos de prueba. Los IDs, magnitudes de sensores y detalles del backend se procesan internamente. Esta ventana usa **Tkinter como interfaz temporal fuera de Unreal**, pero está conectada a un **ejecutable C++ que ejecuta CoreRPG real**. No se presenta como una consola LCARS jugable, ni como certificación del puente, FPS, Unreal D3D12, audio o tripulación. La integración UE5/LCARS y la aceptación visual quedan pendientes para fases posteriores.

## Entregables técnicos

- `include/f06_autonomy.h`, `src/f06_autonomy.inc`: estado y avisos de la computadora, prioridad basada en observaciones, trabajos focales temporizados de propiedad **computer**, y regeneración tras readquisición real. No usa modelos de lenguaje ni permisos humanos ficticios.
- `src/f06_bis.inc`, `src/f06_runtime.inc`, `src/f06_schema.inc`: actualización de reloj, soporte a observaciones computer-owned, eventos semánticos, datos persistentes y validación al guardar/cargar.
- `qa/aster_runner.cpp`: fuente de escenario autorizada del Host, pasos de reloj del Core, cuatro variantes y protocolo de estado compacto de una línea JSON; solo emite datos públicos de sensores.
- `qa/aster_gui.py`: interfaz rudimentaria en castellano para la prueba humana.
- `qa/test_aster_runner.py`: prueba sin pantalla de resultados del protocolo (Windows y Linux).
- `INICIAR_PRUEBA_ASTER.ps1`: compilación segura y arranque en MSI, exclusivamente dentro de `laboratorios`.
- `tests/f06_tests.cpp`: cuatro escenarios nuevos del supervisor y todos los tests anteriores F06/F05.

## Criterio de aprobación

1. CI nativa completa en Windows y Ubuntu, incluyendo casos de automatización y protocolo de la GUI, sin regenerar las auditorías históricas F04/F05.
2. Usuario puede observar las cuatro guardias con cambios de escenario sin instalar una consola definitiva.
3. Detección y análisis iniciados por ordenador; nunca adivinación de ciencia oculta; avisos breves; contacto perdido/reaparecido preserva identidad; fallo o interrupción hacen ruido razonable.
4. Recoger comentarios en informe y corregir lo observado. La aceptación nativa **no cierra la integración en Unreal** ni la fuente viva de F13.

**La prueba de rendimiento del MSI es independiente de este banco F06: no debe tocarse ni sustituirse con estas métricas de CoreRPG.**
