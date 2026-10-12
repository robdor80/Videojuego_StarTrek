# F01-P02 — Auditoría de épocas y canon

Fecha de auditoría: 2026-10-11. Actualización de decisiones autorales: 2026-10-13. Estado: CONFORME (auditoría documental con política de continuidad propia explícita).

## Fuentes revisadas
- `docs/decisions/playable_eras.md`
- `docs/decisions/campaign_continuity.md`
- `sources/canon_policy.md` y `sources/provenance_policy.md`
- `lore/starships/classes/core_catalog.md` y `core_starship_classes.json`
- `docs/decisions/starship_identity_model.md`
- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`

## Resultado verificable
Tres perfiles aprobados, sin cambios: `pike` (SNW); `kirk` (TOS y películas originales); `tng_ds9_voyager` (un periodo compartido). Se excluyen del ámbito jugable las series Picard, Discovery y Enterprise; sus personajes no quedan automáticamente excluidos cuando figuran en obras retenidas. Sovereign existe en el catálogo como extensión cinematográfica tardía explícita y no debe eliminarse. Las épocas no constituyen universos independientes.

**Regla general:** canon válido hasta fecha D de inicio; después, historia emergente por partida. **Excepción aprobada por el autor:** este videojuego personal puede modificar expresamente acontecimientos o fechas del canon televisivo, incluso antes de D, para introducir tecnología y contenido propios. Tales cambios son **continuidad de juego propia**, registrados como `GAME_ADDITION`, nunca suplantando a `SCREEN_CANON`. Siguen existiendo tres épocas jugables; las excepciones deben fijar disponibilidad coherente por fecha/partida antes de activarse.

## Riesgos detectados, sin alterar canon
1. Odyssey / Enterprise-F no consta en el catálogo `core_starship_classes.json`; no asumir su fecha/capacidades ni su presencia en 2372.
2. **La nueva Clase Valhalla ya está elegida**, con Galaxy como inspiración; su **fecha de entrada en servicio aún NO está fijada**. No confundir con la Enterprise-D ni presumir disponibilidad en 2372.
3. El fixture de Sensores usa 2372-03-14, seed `fixture_sensor_v0_0_1`. Es escenario de prueba, no base obligatoria de la saga.
4. Puente prototipo 3D y Dama definitiva son decisiones diferentes.
5. Una malla de terceros exige validación de licencia y pipeline en F07/F14.

## Reglas de no regresión
No introducir una cuarta época tácita; **no incorporar tecnología de otra fecha automáticamente**, pero permitir **excepciones autorales expresas registradas** para la cronología alternativa propia. No garantizar acontecimientos televisivos futuros; distinguir clasificación, clase e identidad individual; conservar historia por partida. La tecnología de «Endgame» aprobada para Valhalla —blindaje ablativo desplegable y torpedos transfásicos— **no implica** que toda la flota la tenga en 2372 o en épocas Pike/Kirk.

Verificación: lectura e inspección cruzada de las fuentes mencionadas. NO_EJECUTADO: Core RPG, UE5 y pruebas funcionales. La conformidad aquí es documental.

**Documento de autoridad posterior:** [Acta creativa de la Clase Valhalla](ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md). Las tres épocas y el fixture de Sensores permanecen sin cambio.
