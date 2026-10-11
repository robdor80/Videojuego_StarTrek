# F01-P02 — Auditoría de épocas y canon

Fecha: 2026-10-11. Estado: CONFORME (auditoría documental).

## Fuentes revisadas
- `docs/decisions/playable_eras.md`
- `docs/decisions/campaign_continuity.md`
- `sources/canon_policy.md` y `sources/provenance_policy.md`
- `lore/starships/classes/core_catalog.md` y `core_starship_classes.json`
- `docs/decisions/starship_identity_model.md`
- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`

## Resultado verificable
Tres perfiles aprobados, sin cambios: `pike` (SNW); `kirk` (TOS y películas originales); `tng_ds9_voyager` (un periodo compartido). Se excluyen del ámbito jugable las series Picard, Discovery y Enterprise; sus personajes no quedan automáticamente excluidos cuando figuran en obras retenidas. Sovereign existe en el catálogo como extensión cinematográfica tardía explícita y no debe eliminarse. Las épocas no constituyen universos independientes.

Canon válido hasta fecha D de inicio; desde D las campañas tienen historia propia, sin reproducir eventos de pantalla futuros de forma obligatoria. Los hechos se registran con origen y grado de confianza; `GAME_ADDITION` no se hace pasar por `SCREEN_CANON`.

## Riesgos detectados, sin alterar canon
1. Odyssey / Enterprise-F no consta en el catálogo `core_starship_classes.json`; no asumir su fecha/capacidades ni su presencia en 2372.
2. Imperator todavía no tiene clase ni fecha de entrada definidas; su existencia depende de decisión autoral.
3. El fixture de Sensores usa 2372-03-14, seed `fixture_sensor_v0_0_1`. Es escenario de prueba, no base obligatoria de la saga.
4. Puente prototipo 3D y Dama definitiva son decisiones diferentes.
5. Una malla de terceros exige validación de licencia y pipeline en F07/F14.

## Reglas de no regresión
No introducir una cuarta época de forma tácita; no importar tecnología futura a campañas pasadas; no garantizar acontecimientos televisivos futuros; distinguir clasificación, clase e identidad individual; conservar historia por partida. Toda excepción autoral requiere registro de decisión y compatibilidad temporal.

Verificación: lectura e inspección cruzada de las fuentes mencionadas. NO_EJECUTADO: Core RPG, UE5 y pruebas funcionales. La conformidad aquí es documental.
