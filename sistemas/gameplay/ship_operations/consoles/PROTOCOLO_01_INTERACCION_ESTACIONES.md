# Protocolo n.º 1 — Interacción física con estaciones de la Flota Estelar

**Aprobación de diseño:** 10 de noviembre de 2026  
**Versión:** 0.1 — concepto aprobado; valores de cámara, controles y escalado pendientes de pruebas UE5/MSI.  
**Aplicación:** estaciones técnicas de las naves jugables; primer laboratorio, USS Sutherland (F07); destino principal, USS Enterprise NCC-1701-D modernizada.  
**Estado del código:** este documento no autoriza a fusionar F07 ni modifica F04/F05/F06 ni recursos 3D.

## Principios

1. **Las consolas son objetos físicos de la nave.** No reemplazarlas por ventanas artificiales para el uso habitual. El operador permanece en la misma posición ante la estación; los cambios de vista son cambios de cámara/mirada.
2. **Las pantallas y controles deben tener utilidad.** Cualquier dato mostrado corresponde a una observación, estado o función autorizada. Evitar decoración que aparente datos reales y botones sin operación.
3. **Automatización predominante:** el computador ejecuta aproximadamente el 90–95 % del trabajo cotidiano de vigilancia (objetivo de experiencia, no porcentaje técnico garantizado). El oficial supervisa, consulta, decide y comunica; los avisos críticos son visibles desde la posición habitual.
4. **Control por ratón y teclado.** En la estación no se presupone voz, gamepad, pantalla táctil ni interacción constante.
5. **Una estación, varias superficies, un estado CoreRPG.** Las visualizaciones superior e inferior comparten selección, contactos, avisos, permisos y revisión. El cambio de encuadre no cambia de puesto, actor o mundo.
6. **Sin revelaciones indebidas:** F06/Core controla permisos, detección, identificación y resultados; las pantallas no inventan contactos, identidad ni modelos 3D.

## Cuatro modalidades de uso aprobadas

| Modalidad | Activación a definir | Resultado |
|---|---|---|
| Mirada inferior / trabajo | Vista habitual al ocupar la estación | Se ve y opera la consola inclinada inferior. |
| Vista rápida superior | Mantener pulsada una tecla | Levanta la mirada a la pantalla superior, **sin interactuar**, y vuelve abajo al soltar. |
| Vista superior interactiva | Pulsación de otra tecla | Mantiene la mirada arriba; permite interactuar con la pantalla superior. La misma tecla devuelve abajo. |
| Lectura inmersiva | Tecla específica | Presenta una versión ampliada y legible de información real de esa misma estación, sin sustituir la interacción física habitual. Al salir, restaura estado y encuadre. |

**No incluir miniatura contextual de la pantalla superior en la consola inferior.** Esa solución ha sido expresamente descartada por introducir una superficie no existente en la nave.

## Adaptación a geometrías distintas

### USS Sutherland, laboratorio de F07

- Consola alargada horizontalmente: **proporción de ejemplo cercana a 6:1**; los 120 × 20 cm fueron ilustrativos y no medidas verificadas.
- El visor del MSI es 2560 × 1600 (16:10). Al mostrar una superficie 6:1 completa, esta ocuparía aproximadamente 2560 × 427 píxeles, **27 % de la altura** del visor, antes de aplicar perspectiva, marcos o márgenes adicionales. Caber no implica poder leer cada elemento.
- Ofrecer **encuadre físico completo** para contexto y **encuadre de trabajo cercano** para legibilidad, con paneo o cambio de mirada si la geometría lo exige. Nunca deformar la imagen LCARS por estiramiento.
- El modo inmersivo sirve para lecturas extensas o precisión. La versión F07 de navegador es banco de presentación y no acredita todavía interacción en UE.

### USS Enterprise-D modernizada, destino final

- Estaciones técnicas traseras con **gran pantalla vertical superior** y **panel inferior horizontal inclinado**.
- **Abajo** se concentran mandos y operaciones puntuales; **arriba** radar, contactos, resultados y recursos 3D certificados.
- En la vista superior ofrecer **encuadre completo** para percibir toda la gran pantalla vertical con su proporción real, y **detalle/zoom físico** cuando los textos o controles se vean demasiado pequeños. Aceptar márgenes laterales en el visor del MSI: no deformar la pantalla.
- Mantener dos superficies coordinadas de una misma estación y el mismo estado de CoreRPG; cualquier selección o acción autorizada debe reflejarse en ambas.
- Las alertas relevantes llegarán también al panel inferior para que la persona no tenga que mirar arriba continuamente.

## Propuesta inicial de controles, NO bloqueada

- **E:** ocupar/abandonar la estación.
- **Vista rápida:** mantener tecla por asignar (retorno al soltar).
- **Vista superior estable:** alternar tecla por asignar.
- **Lectura inmersiva:** tecla por asignar.
- **Esc:** cerrar lectura o salir del modo de interacción correspondiente.

Antes de fijar las teclas, auditar conflictos con movimiento de personaje, atajos internos de la LCARS y teclado de UE.

## Requisitos de integración y pruebas

1. **Condición previa:** superar aceptación de F06/CoreRPG antes de integración jugable F07.
2. Medir en UE5 la geometría, UVs, superficie visible, posición del usuario, perspectiva, tamaño de textos y resolución real de los widgets físicos.
3. Validar cámara completa y de trabajo en la Sutherland sin clipping, estiramientos ni fuente ilegible. La cámara ajustará distancia, orientación o FOV según sea necesario; no se presupone una única solución.
4. Validar mantener/soltar tecla, modo interactivo persistente y retorno exacto a la vista previa; controlar foco de ratón/teclado, sin clicks accidentales durante movimientos.
5. Probar la pantalla vertical de la Enterprise-D con encuadre completo y detalle, y preservar legibilidad en MSI.
6. Verificar que los comandos realmente atraviesan las autorizaciones de F04/F06 y que la computadora autónoma continúa trabajando durante los cambios de vista.
7. La aceptación visual y de jugabilidad requiere prueba real en MSI/UE5; automatizaciones y maquetas no la sustituyen.

## Evolución y cambios

Este protocolo está **aprobado como dirección**, no congelado. Los tiempos de transición, la elección concreta de teclas, límites de zoom, layouts y tratamiento de pantallas de proporción extrema se ajustarán tras las primeras pruebas. Todo cambio deberá justificar mejora de legibilidad, ergonomía, inmersión o comportamiento y documentar su revisión aquí.
