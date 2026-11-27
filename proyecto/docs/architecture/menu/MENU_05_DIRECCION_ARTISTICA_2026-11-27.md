# MENU-05 — Dirección artística y UX aprobada
Fecha: 2026-11-27. Propietario + ChatGPT. Estado: composición y dirección cromática del menú principal APROBADAS por el propietario; especificación documental preparada; acabado visual y ejecución UE pendientes.

## P01 — Referencia visual
Boceto aprobado en conversación MENU-05: composición 16:10, planeta azul con atmósfera en esquina inferior izquierda, espacio negro estrellado, Enterprise-D en centro-izquierda, título metálico frío en superior izquierda, botonera LCARS ámbar/cobre a la derecha. El render conceptual generado en la conversación es referencia artística, no asset de producto ni modelo 3D. No reproducir literalmente su geometría naval, número de botones ni proporciones tipográficas. El PNG original no se incorpora en esta entrega; recuperar de la conversación para cotejo visual.

## P02 — Identidad
Premium, cinematográfico, exploración espacial. Escena tridimensional real, no vídeo ni fondo plano como solución definitiva. Usar exclusivamente el modelo 3D real de la NCC-1701-D del juego (Enterprise-D modernizada) o una referencia temporal explícitamente identificada hasta disponer del asset. No descargar ni sustituir por otra nave sin autorización. Evitar sobrecarga visual y exceso de bloom.

## P03 — Paleta
Decisión aprobada: planeta azul, espacio negro, título plata/blanco/cian, botonera cálida ámbar/cobre. Tokens iniciales ajustables tras ver UE: espacio #02060D; título #E6EDF3, #A1D4E2, #69D6FF; panel #211416; base cobre #C46A36; selección #74332B y #F2B65A; texto #FFF0D9; deshabilitado con contraste comprobado. No teñir planeta ni nave de naranja globalmente. Separar tema UI de iluminación 3D. Una sola implementación con estilos centralizados; temas alternativos seleccionables NO aprobados como requisito, requieren ampliación MENU-02 si se desean.

## P04 — Tipografía
Título STAR TREK en plateado y LEGENDS en cian, estilo futurista y legible; delta de Flota opcional como referencia visual, no obligatorio. Fuente exacta, licencia/archivo disponible y fallback pendientes de selección. Texto español con tildes y Ñ, sin depender de fuentes de sistema ni rasterizar la botonera.

## P05 — Botones e iconografía
LCARS contemporáneo: fondo oscuro, bordes cobre, acento lateral ámbar, esquinas suaves, selección más luminosa con indicador geométrico. Estados normal, hover, focus, pressed, disabled, busy/error con señales no exclusivamente cromáticas. Foco visible independiente del hover. El boceto no sustituye los contratos MENU-01–04: MAIN incluye Continuar, Nueva partida, Cargar partida, Opciones, Enciclopedia/Federación, Extras y Salir según capacidades y guardas; Créditos en Extras según MENU-04. No añadir acciones ficticias. No ocultar Cargar por ausencia en el render. Evitar iconos ambiguos.

## P06 — Composición principal
Referencia MSI 2560×1600 (16:10). Coordenadas normalizadas orientativas: título x 0.03–0.50, y 0.04–0.20; planeta recortado abajo/izquierda x 0–0.48 y 0.60–1; nave x 0.02–0.68 y 0.22–0.64; botonera x 0.69–0.96, y 0.26–0.85. Ajustar encuadre sin invadir título/botones; zonas seguras, tamaños adaptativos. Mapa exclusivo de presentación dentro del proyecto UE existente; cámara fija cinematográfica, esfera planetaria texturizada con capa de nubes y halo; fondo estelar, luces de nave y luz solar. Rotar realmente el planeta de manera continua y dependiente del tiempo de escena, no del reloj de campaña. Nubes a velocidad ligeramente distinta si material y rendimiento lo permiten. Usar materiales/LOD del modelo real o instancias optimizadas sin duplicar originales; no cargar universo jugable ni abrir sesión HOST por ambientación.

## P07 — Submenús
Reutilizar tokens y componentes, mantener título/identidad y foco. Paneles de contenido legibles sobre fondo atenuado; listas virtualizadas si procede. Opciones, partidas, extras, pausa y recuperación conservan contratos anteriores y navegación de regreso. La pausa de juego no carga por defecto la escena orbital ni cambia estado de simulación por motivos visuales.

## P08 — Animación
Entrada desde final Acto II gestionada por MENU-07. Propuesta no vinculante: fundido 0–2 s, título 2–5 s, Enterprise entra 5–12 s; después movimiento ambiental suave sin reiniciar su entrada en bucle. Botones utilizables cuando entrada autorizada y datos listos, sin esperar animación. Rotación continua planeta, nube diferencial opcional; no afirmar que nave orbita físicamente. Reducir movimiento conforme MENU-02, sin afectar navegación; congelar movimiento ambiental/omitir entrada si opción activa. Transiciones breves, cancelables y sin perder foco. No repetir cinemática al regresar de submenú. Política de arranques posteriores corresponde MENU-07.

## P09 — Confirmaciones
Diálogos modales con foco inicial seguro, mensaje explícito, cancelar y confirmar separados, teclado/ratón y Esc según contrato. No anunciar guardado/restauración exitoso antes de confirmación de HOST; no saltar recuperación. Errores conservan lectura y contraste, nunca acción destructiva por animación.

## P10 — Resoluciones
16:10 2560×1600 objetivo; probar 1920×1080, 2560×1440, ventana/borderless/fullscreen y Windows 150% según H07. Anclajes y reglas DPI UMG, tamaños mínimos y ajuste de textos sin recorte; encuadre 3D adapta FOV/posición sin deformar. Pruebas reales MSI en MENU-08. Objetivo orientativo 60 FPS (16.7 ms) a resolución objetivo, no criterio contractual definitivo; medir tiempos, VRAM/RAM y estabilidad y ajustar en MENU-06-P11. Degradación ambiental antes que legibilidad.

## P11 — Prototipos y handoff
Boceto conceptual frío/cálido aprobado; esquema vectorial local de composición en audiovisual/ui/menus/MENU_05_COMPOSICION.svg, no asset final. Codex local debe primero inventariar proyecto Unreal, widgets H08, mapa/flujo y ubicación/formatos del modelo real; preservar diagnóstico H06/H07/H08. MENU-06-P01 infraestructura y ruta de entrada; P02 widgets/estilos; P03 escena y MAIN; P04–P08 submenús y adaptadores; P09 animaciones; P10 resolución; P11 rendimiento. MENU-07 integra audio y Actos. No empezar MENU-06 en esta entrega. No usar Codex ni modificar código/ABI/Core/guardados.

## P12 — Aprobación y límites
Propietario aprobó composición, mezcla de tonos, giro planetario y uso del modelo real de la NCC-1701-D. Quedan como ajustes iterativos fuente exacta, tamaños, velocidades, iluminación y brillo, animaciones, audio, geometría LCARS, políticas de arranque y aceptación presencial. No afirmar asset localizado, disponible/importado o rendimiento verificado. El diseño no desbloquea H09-P02. MENU-05 cerrado en alcance documental/dirección artística; MENU-06/07/08 deben implementar y certificar. Matriz MENU_05_ART_ACCEPTANCE.json: especificación, todos NOT_RUN. Aplican AGENTS.md, no crear proyectos paralelos ni laboratorios permanentes.
