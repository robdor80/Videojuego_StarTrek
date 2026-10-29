# LORE-04A — Sociedad y vida cotidiana

**Estado:** CANDIDATE_COMPLETE_DOCUMENTARY — ocho paquetes desarrollados en la PR Draft #51; revisión y fusión reservadas al autor. **Fecha:** 2026-10-29. **Base:** LORE-03 cerrada mediante PR #50.

## Navegación

- `A01_auditoria_reutilizacion.md` — contratos y huecos reales; fuente de verdad original no duplicada.
- `A02_vida_civil_base_y_casos.md` — hogar, relación, comunidad y ejemplos base.
- `A03_educacion_profesiones_servicios.md` — funciones civiles y educación no militar.
- `A04_ocio_comunidades_rutinas_cotidianas.md` — cultura de ocio, calendarios y desplazamientos.
- `A05_matriz_sociedades_y_diversidad.md` — diferencias culturales, conflictos temporales y variación individual.
- `A06_lod_rutinas_persistencia.md` — mapeo de rutina, off-screen, LOD y autoridad (NO motor nuevo).
- `A07_casos_gameplay_npc.md` — fichas de jugabilidad, casos negativos, conocimiento y consecuencias.
- `A08_auditoria_pruebas_cierre.md` — auditoría, regresiones, incertidumbres y dictamen.

## Artefactos auxiliares

- `lore04a_evidence_ledger_v0.1.json`: evidencia por afirmación con episodios registrados y referencias oficiales, **minutajes pendientes**.
- `lore04a_scenarios_v0.1.json`: supuestos positivos/negativos documentales, **no** ejecución de CoreRPG.
- `desarrollo/validation/consistency/lore04a_civil_society_invariants_v0.1.json`: invariantes de diseño.
- `desarrollo/tools/validation/validate_lore04_a.py`, `test_lore04_a.py` y workflow de CI: verificación de estructura, procedencia y reservas.
- `proyecto/docs/roadmap/lore_04_master_plan_v0.1.md`: plan transversal 04A–E.

## Protocolo de clasificación

`SCREEN_CANON` = ancla audiovisual identificada; `OFFICIAL_REFERENCE` = apoyo editorial oficial, **no** prueba de una escena por sí sola; `INFERRED` = inferencia explícita; `GAME_ADDITION` = caso de juego propuesto; `UNKNOWN` = información no establecida. Toda nueva institución o norma obligatoria requiere autorización de autor.

El cierre significa preparación documental evaluada; **no** `WorldState` integrado ni NPCs ejecutando rutinas. CoreRPG conserva la autoridad; no se marca `CONTENT_STATUS.md` como COMPLETE sin autor y fusión.
