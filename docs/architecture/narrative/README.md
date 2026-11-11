# ST-NAR-00 — Índice de arquitectura narrativa
Responsabilidad técnica en Videojuego_StarTrek. CoreRPG independiente. Diseño y gates offline NO hacen jugable el sistema.
- ST-NAR-00_P02_P03_DIRECTOR.md: decisiones D01–D09, separación de autoridad y contratos de paquetes.
- ST-NAR-00_P04_GCPN.md: exportación de historia real, informes incrementales, catálogo futuro e incorporación de nuevas temporadas.
- ST-NAR-00_P05_VALIDACION.md: comandos, pruebas, bloqueadores y evidencia.
- Contratos: schemas/authoring/st_nar_*.schema.json.
- Fixture sintético: validation/fixtures/seasons/reference_pack (NO PUBLICADO).
- Validador: tools/validation/st_nar_00.py.
- CI: .github/workflows/st-nar-00-reference.yml.
- Temporadas narrativas reales se diseñan en ST-NAR-01 y posteriores junto al autor.
Flujo GitHub: rama feat/st-nar-00 → PR → validación → merge humano → verificación main → borrado rama/pull.