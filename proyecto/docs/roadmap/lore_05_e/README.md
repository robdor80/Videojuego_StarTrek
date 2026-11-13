# LORE-05E — Idiomas, comunicación y exploración (2383)
**Fecha:** 13/11/2026 · **Estado:** documentación candidata a validación, no runtime. 

## Entregables
- [Superposición de reglas y ocho asociaciones lingüísticas preexistentes](../../../../mundo/lore/languages/lore05e_reference_overlay_v0.1.json) — no define nuevos idiomas jugables.
- [Guía de traducción, diálogo y comunicaciones](../../../../mundo/lore/languages/LORE05E_TRADUCCION_Y_COMUNICACION_20261113.md).
- [Guía de exploración y primer contacto](../../../../mundo/lore/exploration/LORE05E_EXPLORACION_Y_PRIMER_CONTACTO_20261113.md).
- [24 casos adversariales documentales](../../../../mundo/lore/exploration/lore05e_acceptance_cases_v0.1.json).
- `desarrollo/tools/validation/validate_lore05_e.py` y `test_lore05_e.py`; CI independiente `.github/workflows/lore05-e-documentary.yml`.

## E01–E08: trazabilidad
E01 inventario de contratos existente; E02 lenguas sin generalizaciones por especie; E03 traductor y ambigüedad; E04 transmisión, autenticación y privacidad; E05 descubrimientos observables; E06 primer contacto, consentimiento y Primera Directriz; E07 casos y validación reproducible; E08 auditoría y cierre documental después de CI final y fusión.

## Límites
Canon de pantalla y evidencia no se mezclan con `GAME_ADDITION`. Reutilización en lugar de duplicación; cero variaciones de contratos de sistemas. CoreRPG escribe WorldState; HOST sirve y no sustituye la cadena de mando F11. La IA se limita al conocimiento disponible. No se desbloquea Delta, no hay misiones automáticas, ni escenarios reales en UE5, ni PADD con secretos, ni nuevo elenco legendario. La Enterprise-D es Galaxy en reconstrucción bajo Proyecto Valhalla, no nueva clase ni plaza garantizada.

**Puerta de salida:** verificar IDs, 24 casos y mutaciones negativas; CI del HEAD definitivo y regresiones, inspección de diff; fusionar si procede y **solo después** actualizar el índice administrativo como `COMPLETE_DOCUMENTARY`.
