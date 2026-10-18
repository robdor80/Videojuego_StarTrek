# LORE-01 C — Auditoría de cartografía y atlas (18-10-2026)
## Estado
**DOCUMENTADO; PENDIENTE DE REVISIÓN Y CI**. Rama aislada, sin fusionar. No integración ejecutable.

## Contexto verificado
La PR #27 de LORE-01 B figura **merged** en `main` mediante `b1c29b6d3ddda36e2b0923372c1053b3df0c181e`; se parte de esa base. Los registros de A y A.1 ya estaban completos y B se regulariza a COMPLETE.

## Hallazgos
| Hallazgo | Respuesta |
|---|---|
| Existían 30 anclajes, 12 regiones y 10 distancias de referencia | Se crea índice documental con claves preexistentes; no se duplican como nuevos destinos. |
| Las cuatro imágenes son bidimensionales, políticas o estilizadas | Coordenadas XYZ = null; no se extrae escala desde tamaño de imagen. |
| Mapa 1 “United Federation of Planets I-IV” | Contexto de territorios y nombres; autor, cronología y derechos no verificados. |
| Mapa 2 “Milky Way Galaxy / Stellar Cartography” | Boceto de cuadrantes, boca de gusano, Voyager y Borg; WWW STinSN visible; distancias rotuladas sin validación primaria. |
| Mapa 3 de sectores coloreados | Excelente referencia de UI, pero sistema sectorial diferente y autoridad no acreditada. |
| Mapa 4 “Shakaar's Alpha/Beta Map v3.3” | Identificado como fan map por referencia pública; se indexan pistas sin convertir fronteras y sistemas en canon. |
| PDF Mandel previo de 42.9 MB en repositorio | No alterado; revisar derechos de redistribución del PDF existente en auditoría legal separada. |
| Capas política y conocimiento separadas en la arquitectura del repo | Las fichas de C no contienen soberanía por sistema y no abren datos secretos para la IA. |
| Delta, Voyager y Borg en esquemas | Solo referencias históricas o DLC reservado, no contenido procedural Delta; IDEA-0011 inactiva. |

## Alcance real
- 30 fichas de anclaje indexadas, no 30 nuevas ubicaciones.
- 4 cuadrantes, 12 regiones de referencia, 11 ejemplos de rutas (incluido el agujero de gusano).
- 25 pistas de investigación selectivas, ninguna aprobada ni importada al juego.
- 11 discrepancias/advertencias registradas, 10 casos de conocimiento/cronología.
- Catálogo de metadatos de 4 imágenes (hash SHA-256 y dimensiones) **sin publicar las imágenes originales**.
- Script validador independiente, regresión automatizada y workflow CI.

## Obstáculos y decisiones abiertas
1. **Permisos** para alojar mapas externos en GitHub público; el usuario puede usarlos como referencias privadas hasta conocer autor/licencia.
2. Resolver evidencia de cada localización secundaria y sus épocas antes de añadirla a `anchor_locations.json`.
3. Validar relaciones distancias/precisión del modelo heredado sin modificarlo aquí: `real_astronomy`, `screen_direct`, `official_map` y cálculos warp requieren tratamientos distintos.
4. En el futuro, escoger el marco de coordenadas 3D del juego con calibración de estrellas; la cuadrícula de Shakaar no da eje Z ni distancia métrica.
5. El repo ya contiene un PDF licenciado completo; analizar legalidad de mantenerlo público **fuera del alcance de esta PR**.
6. No se han revisado páginas/escenas fotograma a fotograma para certificar todas las pistas; ninguna pista asciende de autoridad sin auditoría individual.

## Protección DLC y canon
Un visor puede mostrar la Vía Láctea y la historia de Voyager sin otorgar al jugador conocimiento secreto ni acceso material al cuadrante Delta. La cronología solo inicializa la campaña; desde ese instante manda el estado emergente. No inventar gobiernos, rutas ocultas, límites ni guerras para “rellenar” el mapa.

## Resultados de CI
Rellenar únicamente tras comprobar las ejecuciones de GitHub Actions del HEAD final.

## Criterio de cierre
Revisar los archivos, confirmar que CI y pruebas de A/A.1/B pasan, verificar derechos y fuentes y **fusionar únicamente por decisión del propietario**. No iniciar LORE-01 D en esta rama.
