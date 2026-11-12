# Planificación 2 · Bloque 5 — Historia procedural y grandes acontecimientos

**Estado:** EN_VALIDACION_REFERENCIA (2026-11-12). **Alcance:** contratos, generador de propuestas de referencia, registro determinista, fixtures, pruebas y auditoría; no CoreRPG/UE5/HOST ejecutable.

## Propósito
Convertir **hechos aceptados y causalmente verificados** de B1 (evolución), B2 (colonización), B3 (conflicto) y B4 (economía) en registros históricos persistentes, sin inventar sucesos por conveniencia narrativa. La historia de cada campaña diverge después de su corte temporal. La Flota Estelar conoce sólo lo comunicado y permitido.

## Paquetes
| Código | Entregable | Criterio |
|---|---|---|
| PH001 | Autoridad y separación CoreRPG/Star Trek | Sin doble motor del mundo |
| PH002 | Historia histórica previa y corte de campaña | Prefijo anterior a D protegido |
| PH003 | Identidades, causalidad y cronología | Fuentes aceptadas, ticks coherentes |
| PH004 | Evolución civilizatoria | Se registra la decisión ya adoptada por B1 |
| PH005 | Expansiones y legado colonial | No inventa soberanía ni colonias |
| PH006 | Guerra, paz y consecuencias | No declara guerras, tratados ni bajas |
| PH007 | Economía e infraestructura | B4 es la fuente, no un mercado paralelo |
| PH008 | Grandes acontecimientos | Alcance de impacto sustentado por evidencias |
| PH009 | Historias locales y galácticas | Escalas distintas, identidades estables |
| PH010 | Anotaciones, rectificaciones y versiones | Append-only, sin borrar el pasado |
| PH011 | Rumores, noticias y conocimientos | Observador y clearance independientes |
| PH012 | Variación por campaña y perspectiva | Sin dependencia de nave o rango |
| PH013 | Determinismo, idempotencia, LOD y recarga | Reproducción exacta a misma versión |
| PH014 | Fixture positivo/negativo y pruebas | Rechazos atómicos y no regresiones |
| PH015 | Auditoría de fronteras B6–B10 | Sin descubrimientos/crisis/misiones/scheduler |
| PH016 | Acta, registro y traspaso a Bloque 6 | Cerrar sólo el nivel probado |

## Contrato de verdad
1. **Canon anterior al corte D** se incorpora como prefijo histórico de referencia, sellado. El año 2383 propuesto no se convierte en día/mes exacto sin decisión del autor.
2. **Después del corte**, no hay sucesos televisivos obligatorios. Rómulo en 2387, por ejemplo, no se destruye por calendario; sólo una secuencia de causas autorizadas podría producir un resultado propio de campaña.
3. El registro necesita `campaign_id`, `event_id`, tiempo efectivo, fuentes aceptadas, entidades afectadas preexistentes, actor/autoridad, procedencia, escala y visibilidad. Idempotencia y conflicto de ID se verifican.
4. Un hecho nuevo de historia **no muta por sí mismo el inventario, la soberanía, la diplomacia, un personaje o una guerra**. B1–B4 generan los cambios reales, B5 reconoce su importancia, los conecta y registra. CoreRPG es el único dueño de WorldState, eventos, relojes, guardado y transacciones.
5. Un suceso mayor requiere evidencia explícita de escala y al menos dos entidades afectadas preexistentes; esta es una **regla del adaptador de referencia**, no un umbral definitivo de producción.
6. Las rectificaciones añaden un segundo acontecimiento que apunta al anterior: ni una IA ni una revisión pueden reescribir clandestinamente el historial.
7. La visibilidad pública no significa conocimiento instantáneo. Acceso y comunicación con marcas temporales separan verdad, rumor y observación. PADD, recapitulaciones y diálogos reciben proyecciones filtradas.
8. Las semillas para nuevos IDs incluyen campaña, versión, tipo, causas, entidades afectadas y ordinal estable. No incluyen distancia de cámara, rango, nave ni presencia del jugador.
9. Un dato desconocido sigue sin resolver. No se inventa fecha, autoridad, rumor confirmado ni resultado para completar un arco dramático.
10. No se fusionan historias de campañas ni se reescriben saves antiguos al actualizar versiones del generador.

## Reutilización y límites
Fuentes: `sistemas/universe/generation/civilization_economy_governance_history_contract.json`, `proyecto/docs/roadmap/lore_03_d/D07_historia_por_partida.md`, `proyecto/docs/roadmap/lore_03_e/E05_universo_dinamico.md`, `proyecto/docs/roadmap/lore_03_b/B05_horizonte_2383_consecuencias.md`, `sistemas/universe/chronology/master_timeline/MASTER_TIMELINE_v0.1.md`, B1–B4 y F13.

B5 **no** desarrolla: B6 investigación y progreso científico; B7 anomalías y arqueología; B8 generadores de crisis; B9 generación de misiones; B10 planificación automática de la galaxia. Los arcos de temporadas son otra capa narrativa que **consume** la historia, sin determinar qué sucede al mundo.

## Diseño de referencia probado
- `sistemas/universe/generation/procedural_history_major_events_reference_contract_v0.1.json`: frontera y familias.
- `desarrollo/tools/generation/simulate_procedural_history.py`: propuesta ID estable, aceptación inmutable, replay y proyección observada.
- `desarrollo/validation/fixtures/procedural_history/procedural_history_reconstruction_v0.1.json`: caso sintético de reconstrucción posconflicto (no canon).
- `desarrollo/tools/generation/test_simulate_procedural_history.py`: pruebas positivas/negativas.
- `.github/workflows/p2-b05-procedural-history.yml`: CI, incluyendo regresión B1–B4 y F13.

**No está implementado:** precarga histórica completa desde canon, ejecución periódica de nuevos acontecimientos sin jugador, persistencia real de campañas, autorización viva por WorldState, comunicaciones intersistémicas, simulación local/galáctica ni integración con CoreRPG/HOST/UE5. Eso exige tareas de runtime posteriores y validación explícita. La referencia acepta **candidatos históricos ya causalmente sustentados**, no descubre causas por sí sola.
