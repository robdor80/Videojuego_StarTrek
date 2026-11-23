# H06 — Corrección técnica M1-UX-WINDOWED-2560

**Estado:** corregida y comprobada técnicamente en MSI; aceptación visual y funcional humana pendiente. No amplía por sí sola la certificación M1 ni certifica H07. Código de la corrección: `2e75db5998151719f47933904a8729d9916cbde7`, separado del commit H07 `61d03ce760eadb7e1db4b58061ee2a3f16960e02`. PR [#205](https://github.com/robdor80/Videojuego_StarTrek/pull/205), apilada sobre #204, sin fusionar.

## Causa demostrada

Se ejecutó una **copia aislada del binario M1 anterior** (DLL Unreal SHA-256 `9ef719b88bbef94d51c3b2e265b2ad63722071a6f3a99801bc7cc1137aaf0d2a`) y su configuración original, con el mapa mínimo generado, solicitando `-windowed -ForceRes -ResX=2560 -ResY=1600`, **sin -unattended**. No se modificó el laboratorio previo ni el proyecto original.

Las mediciones Win32 se tomaron desde un contexto de lectura per-monitor-v2 para evitar virtualizar los rectángulos físicos: monitor 2560×1600; área de trabajo 2560×1528; factor Windows 150 %; ventana del juego DPI-unaware (awareness 0), DPI 96. El cliente físico resultante era **3840×2400**, y el rectángulo exterior `(-12,-47)-(3852,2412)`. La captura remota del escritorio estaba bloqueada; estos valores proceden de las API de ventana, no de una imagen escalada en el chat.

La configuración original no activaba `bAllowHighDPIInGameMode`. Windows virtualizaba las coordenadas y ampliaba el cliente solicitado por 1,5. La primera instrumentación interna observó, además, monitor lógico 1707×1067, viewport nominal 2560×1600 y un panel de anchura local 856: no se atribuye el fallo a esa anchura. La geometría Slate se calculaba para una superficie mayor que la visible. La referencia pública de Epic describe la relación entre DPI awareness y resoluciones incorrectas en [UE-310825](https://issues.unrealengine.com/issue/UE-310825); el diagnóstico de este equipo se apoya en las mediciones anteriores, no en dar por idénticas dos versiones del motor.

Una ventana con cliente físico 2560×1600 tampoco cabe íntegra en este escritorio: la barra de tareas y las decoraciones ocupan espacio real. Activar DPI awareness por sí solo no resuelve esa imposibilidad geométrica.

## Corrección

- `DefaultEngine.ini` activa `bAllowHighDPIInGameMode=True` para crear la ventana de juego con DPI awareness. La ejecución normal comprobó awareness 2, DPI 144 y Slate DPI 1,5.
- `FitHostAcademyWindow` consulta el monitor de la ventana y su área de trabajo, mide las decoraciones reales y limita únicamente el cliente que no cabe. Conserva modo ventana. No aplica porcentajes DPI fijos ni cambia resolución o escalado de Windows.
- SWindow recibe un tamaño cliente en píxeles ya escalados. El desplazamiento se aplica como diferencia respecto de su posición actual, porque el origen de SWindow y el rectángulo exterior nativo no coinciden. Se reevalúa tras redimensionar y volver desde pantalla completa. Las ventanas minimizadas o maximizadas quedan a cargo del sistema.
- Se conservan composición Slate, centrado, navegación y comandos de Academia. El único cambio de widget para diagnóstico es una etiqueta de la superficie, sin rediseño artístico.

Medición de este MSI: decoraciones **22×56**; área de trabajo **2560×1528**. Por tanto, cliente máximo **(2560−22)×(1528−56) = 2538×1472**. La ventana final ocupa `(0,0)-(2560,1528)` y su origen cliente es `(11,45)`. El panel ocupa aproximadamente X=696,65..1863,35 dentro de ese cliente, centrado por Slate. Los números dependen del monitor y decoraciones; el código los vuelve a calcular.

## Verificación real en MSI

UE 5.8.4, CL 58902052; Windows 11; RTX 4070 Laptop. Suite `StarTrek.H06.AcademyMenu.Geometry`, D3D12 real, con proceso nuevo y UserDir aislado en cada ejecución:

| Ejecución | Resultado técnico |
|---|---|
| Ventana 1920×1080, sin ForceRes | PASS: cliente 1920×1080, ventana y controles contenidos; menú principal y Continuar |
| Ventana solicitada 2560×1600, ForceRes, Windows 150 % | PASS: cliente efectivo 2538×1472; ventana exterior dentro del área de trabajo; controles contenidos en ambas vistas |
| Pantalla completa 2560×1600 | PASS: cliente/viewport 2560×1600; ambas vistas dentro del cliente |
| Ventana → pantalla completa → ventana | PASS: seis muestras, menú principal y Continuar en cada modo; el cliente recuperado vuelve a 2538×1472 |

La pantalla completa observada fue **WindowedFullscreen (modo 1, sin bordes)**; no se afirma haber probado fullscreen exclusivo. Las transiciones invocaron `UGameViewportClient::HandleToggleFullscreenCommand`, el comando del motor utilizado por Alt+Intro. No se afirma una pulsación física de Alt+Intro desde el escritorio bloqueado.

La suite registra monitor físico, área de trabajo, DPI awareness, rectángulos exterior/cliente, viewport, tamaño local, origen y escala acumulada de la geometría Slate, y límites de los widgets. Comprueba que el rectángulo exterior cabe y que la superficie y botones están contenidos. También solicita PNG de la superficie renderizada por Unreal; el índice de captura identifica la solicitud, y su contenido debe revisarse al auditar porque la captura se resuelve en un frame posterior.

## Límites y aceptación pendiente

`-unattended` produjo DPI-unaware en esta instalación incluso con el ajuste de juego activado. Las mediciones de aceptación geométrica se repitieron **sin ese parámetro**; no se usan las ejecuciones unattended como evidencia de la ventana normal al 150 %.

Computer Use encontró la pantalla de bloqueo del MSI y se detuvo. Las imágenes generadas directamente por el viewport muestran la interfaz y permiten inspección técnica, pero no acreditan interacción física con ratón, foco, Escape, Alt+F4 ni aceptación humana. Las automatizaciones de navegación, creación, guardado y continuación se registran por separado en el informe H07-P05: pares Seed/Resume, navegación y fallo real de guardado pasan en NullRHI y D3D12; el paquete también pasa geometría/transiciones y continuación en proceso nuevo. Una captura adicional solicitada al arrancar el proceso muestra un frame aún incompleto y no se utiliza como aceptación visual del título; las capturas tardías de Continuar y las medidas por widget son las evidencias útiles. No se interpreta el escritorio bloqueado como superficie del juego.

Para aceptar la incidencia: desbloquear el MSI, lanzar la copia de laboratorio con UserDir aislado, revisar menú principal/Continuar en los tres tamaños anteriores, recorrer botones con teclado y ratón, comprobar Escape, Alt+F4 y Alt+Intro físicos, crear/continuar una partida de ensayo y confirmar ausencia de recortes. Usuario y ChatGPT decidirán el cierre visual; este informe no sustituye esa decisión.
