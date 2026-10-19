# LORE-01 D — Auditoría documental inicial

Fecha de preparación: 2026-10-19. Estado: pendiente de revisión humana y CI.

## Base y dependencia
- main verificado: 577fd1bfda89205f5d8a95e27cde13cadc46f04d (merge LORE-01 C, PR #28).
- 16 identidades de LORE-01 B sin fabricar Estados a partir de redes ni organismos.
- Se conserva el baseline ya establecido de gameplay/diplomacy/major_faction_catalogue.json, federation_relation_anchors.json, gameplay/conflict/ y gameplay/navigation/political_space_state_anchors.json.
- Se corrige estado C = COMPLETE en CONTENT_STATUS.md.

## Alcance entregado
- 27 expedientes de relaciones, 40 hitos históricos documentales, 7 acuerdos, 5 conflictos de referencia, 6 lecturas de capa territorial, 10 escenarios y 12 incertidumbres.
- Evidencia por source_refs procedente del catálogo existente, sin alegar revisión escena a escena de cada enunciado.
- No hay ejecución automática de los datos, ni cambios en CoreRPG, Unreal o contratos ya activos.

## Riesgos conocidos
- Fuentes secundarias oficiales ayudan a ubicar pactos sin certificar texto/fecha de firma. Contrastar contra escenas en revisión futura.
- Anclas de año sin fecha de episodio: no deben aplicarse en bloque a principio de año.
- Pacto y alianza no equivalen a libre tránsito, cesión territorial ni aceptación social.
- Los rumores del supuesto golpe tzenkethi no son hechos del mundo.
- El Dominio dispone de fases temporales diferentes: historia previa, contactos, guerra, rendición.
- Delta sigue clausurado; IDEA-0011 no ejecutable; solo contacto Borg Alfa respaldado TNG.

## Auditoría automatizada prevista
python tools/validation/validate_lore01_d.py
python tools/validation/test_lore01_d.py
más regresión A, A.1, B y C en GitHub Actions.

## Sin presumir validación
La integridad estructural se verifica programáticamente en la escritura inicial; resultados reales de CI y pruebas Python sólo se declararán tras ejecución. Esta auditoría no constituye prueba del motor de juego ni de exactitud total del canon escena por escena.

## Pendientes no bloqueantes
- Fechar con resolución de episodio/escena los cambios dentro de 2373/2375.
- Revisión de términos jurídicos y fuentes primarias completas de algunos pactos.
- Identificar acuerdos comerciales adicionales si los acredita el canon.
- LORE-01 E no iniciada.

## Resultado CI tras correcciones (19-10-2026)

Verificado sobre commit `dd5c3bf2eefbcbd27de10015475d84955a563cc6`, con cuatro workflows completados correctamente:

- LORE-01 — catálogo especies y culturas: run #39296526526 — success.
- LORE-01 B — civilizaciones: run #39296526528 — success.
- LORE-01 C — atlas: run #39296526580 — success.
- LORE-01 D — diplomacia + regresiones: run #39296526597 — success.

- El validador nuevo informó 27 relaciones, 40 hitos, 7 acuerdos, 5 conflictos y 10 casos.
- Las 15 pruebas unitarias de D resultaron satisfactorias; las regresiones A/A.1/B/C incluidas en workflow D también pasaron.
- Se corrigió una aserción textual frágil de Bajor y se amplió el validador documental de C para admitir su cierre y posterior comienzo de D. No se modificaron contratos operativos.
- Los resultados son de documentación/CI; no constituyen validación de UE5, ejecución en CoreRPG ni auditoría escena por escena de la serie.
