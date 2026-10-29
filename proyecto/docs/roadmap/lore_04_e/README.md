# LORE-04E — Auditoría global e integración documental

**Estado:** COMPLETE_DOCUMENTARY_CANDIDATE_PENDING_AUTHOR_MERGE. PR de E dirigida a main ya consolidada con A (#51), B (#52), C (#56) y D (#57); E aún sin merge en este corte documental.

- [E01](E01_integridad_estructura.md) — Integridad del corpus, identidad y estructura
- [E02](E02_canon_cronologia.md) — Canon, procedencia, cronología y campañas divergentes
- [E03](E03_sociedad_economia_logistica.md) — Auditoría de sociedad, economía y logística
- [E04](E04_jurisdiccion.md) — Auditoría de autoridad, derecho y jurisdicciones
- [E05](E05_corerpg_ia_runtime.md) — CoreRPG, WorldState, IA, persistencia y observación
- [E06](E06_storg_f00_f15.md) — Trazabilidad ST-ORG-01, F00–F15 y dependencias
- [E07](E07_validaciones_regresiones.md) — Invariantes, regresiones y pruebas adversariales
- [E08](E08_dictamen_cierre.md) — Dictamen y cierre documental condicionado

- [18 casos de auditoría](lore04e_cases_v0.1.json): negativos y positivos, no ejecutados en CoreRPG.
- Compatible documentalmente con A, LORE-01/02/03, ST-ORG, F00–F15 y patrones CoreRPG. No constituye integración UE5.
- Validación transversal y regressiones en workflow `lore04-e-crossphase.yml`.
- Autorización expresa de fusión secuencial recibida; B/C/D incorporadas. E solo se fusionará tras las verificaciones; `CONTENT_STATUS.md` no se altera sin reconciliación final.

**Protocolo administrativo:** autorización expresa del autor para fusionar fases C, D y E. Las fusiones C/D ya están verificadas; **E sin merge** hasta superar CI. No se borran ramas históricas automáticamente y el cierre administrativo final exige verificar el HEAD de `main`.

- [Acta de reconciliación de PR apiladas](ACTA_RECONCILIACION_FUSIONES_20261029.md).
