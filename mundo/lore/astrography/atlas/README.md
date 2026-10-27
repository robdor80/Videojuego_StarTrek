# LORE-01 C — Atlas galáctico de consulta (TNG / DS9 / VOY)
**Fecha de autoría:** 18-10-2026 · **Estado:** documentación pendiente de revisión y aprobación.

## Objetivo
Aprovechar las cuatro cartografías facilitadas por el usuario **sin sustituir** las estructuras ya existentes de navegación, localizaciones, fronteras y conocimiento. Esta carpeta sirve de índice documental y trazabilidad; **NO** crea coordenadas, mundos, rutas, fronteras, misiones o contenidos ejecutables.

## Inventario comprobado en main
- `mundo/lore/astrography/systems/anchor_locations.json`: 30 anclajes, tipos y sectores seleccionados.
- `mundo/lore/astrography/spatial_regions/gameplay_regions.json`: 12 regiones.
- `sistemas/gameplay/navigation/anchor_route_graph.json`: 17 nodos y 13 aristas/relaciones del grafo original.
- `sistemas/gameplay/navigation/initial_reference_distance_edges.json`: 10 distancias de procedencia heterogénea; se mantienen intactas.
- `sistemas/gameplay/navigation/political_space_state_anchors.json`: estados fronterizos fechados; no se reemplazan por polígonos fan.
- `sistemas/gameplay/navigation/star_charts_sector_reference_scheme.json`: referencia licenciada de cubos nominales de 20 años luz, **no** escala impuesta al universo.
- `sistemas/gameplay/exploration/astrographic_knowledge_state.json`: conocimiento de persona/nave/organización independiente de la verdad física.
- `assets/otros/cartografia/reference/star_charts_geoffrey_mandel/`: atlas licenciado previo; **su presencia en el repo no significa que la redistribución esté autorizada**.

## Documentos nuevos
| Archivo | Uso |
|---|---|
| `map_reference_manifest_v0.1.json` | Metadatos y huellas SHA-256 de las 4 imágenes, sin subir binarios protegidos. |
| `anchor_atlas_v0.1.json` | 30 fichas trazables de anclajes, con cuadrantes dudosos y XYZ nulos. |
| `quadrants_regions_v0.1.json` | Cuadrantes y regiones indexadas; geografía separada de soberanía. |
| `route_reference_cases_v0.1.json` | Lectura documental de aristas preexistentes y atajo Alfa/Gamma. |
| `cartographic_research_leads_v0.1.json` | Etiquetas visuales pendientes de contraste, *no* destinos importables. |
| `map_discrepancy_ledger_v0.1.json` | Contradicciones, representación dimensional, anacronismos y derechos. |
| `knowledge_era_cases_v0.1.json` | Filtros de época, conocimiento y DLC aplicados a ejemplos. |

## Regla de autoridad y extracción
1. Pantalla retenida en proyecto TNG/DS9/VOY cuando avala un hecho concreto.
2. `STAR_CHARTS_2002` (Mandel / Pocket Books): referencia licenciada, secundaria a la pantalla.
3. Las cuatro imágenes del usuario sirven como **pistas de investigación y comparativas**, nunca prueba automática de sector, XYZ, rutas o fronteras.
4. Shakaar Alpha/Beta v3.3 es un mapa de aficionados (ver https://brilliantmaps.com/star-trek-map/). Los otros mapas tienen procedencia/derechos pendientes de confirmar.
5. Una etiqueta legible no implica posición validada ni licencia de copia. No se ha realizado transcripción exhaustiva por OCR o inspección píxel a píxel; las pistas son **selectivas y potencialmente falibles**.
6. No se inventan sistemas en producción a partir de píxeles. Para admitir una ubicación nueva: episodio/fuente, identidad, cronología, geometría opcional, permisos de conocimiento, validación.

## Separación de capas
```text
Identidad física (localizaciones)     — sin dueños
      + referencia astrográfica       — fuentes, esquemas, XYZ nullable
      + política temporal             — tratados, fronteras, jurisdicción
      + conocimiento disponible       — nave / personaje / época
      + rutas y riesgos validados     — grafo / CoreRPG futuro
      = respuesta segura de consola y narrativa
```

### Ejemplos de decisiones difíciles
- **Sol**: el límite Alfa/Beta del diagrama no permite elegir cuadrante exacto universal. Se deja nulo.
- **Vulcano / 40 Eridani**: hipótesis no pantalla señalada ya por las distancias del repo. No se promueve.
- **Bajor–Gamma**: dos bocas de gusano, conexión especial; no trayecto warp euclidiano, ni acceso retroactivo pre-2369.
- **Borg**: incursiones en Alfa documentadas sin apertura de la futura puerta del DLC Delta.
- **Shakaar**: múltiples estados, nombres y fronteras interesantes, pero no son canon por figurar en un mapa.

## Límites / traspaso
No modificar CoreRPG, UE5, `sistemas/gameplay/navigation/**` ni `sistemas/gameplay/exploration/**` en esta fase. La navegación real, el visor 3D, las coordenadas y las consultas de computadora quedan para integración autorizada futura. Nunca se crean fronteras eternas ni se revelan al jugador secretos globales. El contenido `DELTA_RESERVED_REFERENCE_ONLY` no se genera ni se vuelve accesible; IDEA-0011 sigue inactiva.

## Auditoría
Ver `proyecto/docs/roadmap/lore_01_c_cartographic_audit_v0.1.md`. Ejecutar:
```shell
python desarrollo/tools/validation/validate_lore01_c.py
python desarrollo/tools/validation/test_lore01_c.py
```
