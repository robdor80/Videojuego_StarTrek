# Especies — Star Trek RPG (TNG / DS9 / VOY)

**Índice documental del apartado LORE-01 A.** No se duplican aquí las fichas de biología.

## Fuente de verdad por materia
- `gameplay/species/profiles/` — 25 fichas de especies, más **estado** de asimilación Borg (NO una especie).
- `lore/cultures/profiles/` — culturas aprendidas, múltiples por personaje, jamás impuestas por biología.
- `gameplay/languages/initial_language_catalogue.json` — lenguas documentadas, separadas de competencia lingüística y del traductor.
- `sources/source_registry/source_registry.json` — fuentes trazables y su categoría.
- `lore/species/LORE01_TNG_species_coverage_audit_v0.1.json` — índice de rutas y cobertura, NO nuevo perfil biológico.
- `universe/generation/lore01_tng_content_availability_v0.1.json` — alcance de juego principal frente a futuro DLC.

## Contenido
- **Existentes, conservadas**: humano, vulcano, andoriano, aenar, tellarita, klingon, romulano, cardassiano, bajorano, ferengi, trill, betazoide, cambiante, vorta, jem'hadar.
- **Ampliación principal**: boliano, benzita, el-auriano, breen, pakled.
- **Reserva exclusiva de DLC Cuadrante Delta**: kazon, ocampano, talaxiano, vidiano, hirogen.

Los **el-aurianos sí pueden aparecer en la partida principal** por su diáspora; **los Borg ya existentes no se excluyen** del juego principal. El portal transwarp Borg es una futura idea de acceso, no una ruta ni mecánica creada aquí.

## Reglas
1. Especie no decide cultura, nacionalidad, profesión, personalidad o moralidad.
2. No interpretar fecha de aparición en un episodio como origen biológico, ni imponer sucesos futuros a la campaña.
3. Las especies Delta se documentan para futuro uso, pero **no autorizan generarlas en el juego principal**.
4. No completar la vida media, fisiología ni idioma con números o categorías inventadas. Una lengua no entra en catálogo sin fuente.
5. No inventar cartografía, relaciones diplomáticas, tecnologías, comportamiento de CoreRPG ni integraciones de UE5.

## Auditorías
- `docs/roadmap/lore_01_tng_a_species_cultures_audit_v0.1.md` (auditoría inicial)
- `docs/roadmap/lore_01_tng_a02_existing_species_review_v0.1.md` (revisión del legado)
- `docs/roadmap/lore_01_tng_a_closure_report_v0.1.md` (resultado, pendientes y prueba)

Validación: `python tools/validation/validate_lore01_tng.py` y `python tools/validation/test_lore01_tng.py`.

La disponibilidad Delta se ajusta a la [IDEA-0011](../../ideas/IDEA-0011_dlc_cuadrante_delta_portal_transwarp.md): los Borg **no** cruzan este portal hacia Alfa y el retorno del jugador usa normalmente el mismo enlace (opción C), salvo interrupciones justificadas. Estas son decisiones de **diseño**, no funcionalidades implementadas.
