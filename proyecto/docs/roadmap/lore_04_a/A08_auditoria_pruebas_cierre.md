# LORE-04A / A08 — Auditoría integral, regresiones y dictamen documental

**Fecha de preparación:** 2026-10-29. **Situación:** `DOCUMENTARY_CLOSURE_CANDIDATE_IN_DRAFT`. Este texto **no declara fusión** ni decisión creativa final del autor. **PR:** #51 Draft, sin merge, rama independiente. **Base:** `289a1074b9b2767692823bfe5b8b94662af72a98` (LORE-03 #50).

## A08.1 Lista de comprobación de contenido

| Paquete | Entregable | Criterio verificado por diseño | Reserva |
|---|---|---|---|
| A01 | `A01_auditoria_reutilizacion.md` | inventario de contratos/áreas de verdad y alcance | runtime CoreRPG no re-auditado ejecutivamente |
| A02 | `A02_vida_civil_base_y_casos.md` | hogares, individuo, contextos y 3 escenas hipotéticas | leyes, salarios y cronología exacta no inventados |
| A03 | `A03_educacion_profesiones_servicios.md` | servicios civiles y enseñanza no confunden Academia | modelos de acceso y financiación `UNKNOWN` |
| A04 | `A04_ocio_comunidades_rutinas_cotidianas.md` | ocio, horarios y movilidad causales, no universalizados | sin calendario universal |
| A05 | `A05_matriz_sociedades_y_diversidad.md` | distinción de 11 ámbitos, no esencialismo | legislación y grados de aceptación no fijados |
| A06 | `A06_lod_rutinas_persistencia.md` | separación población/LOD, identidad, agendas, off-screen | ningún scheduler implementado |
| A07 | `A07_casos_gameplay_npc.md` | 16 escenarios con aceptación y rechazo | fixtures no materializados |
| A08 | presente acta y herramientas | consistencia, trazabilidad, riesgo y pruebas | merge y cierre administrativos pendientes |

## A08.2 Matriz de coherencia transversal

- **LORE-01:** no se alteran perfiles culturales, especies o gobiernos; `cultural_profile_contract_v0.1.json` sigue propietario.
- **LORE-02:** replicación, medicina y tecnología no son mágicas; recursos, autorización, tratamientos y energía se consultan a contratos anteriores.
- **LORE-03:** memoria, cronología pre-corte y futuro abierto. Ningún evento futuro se impone; el año inicial 2383 sigue propuesto sin día/mes.
- **ST-ORG-01:** organización de Flota ≠ gobierno civil ni jurisdicción universal. No se modifica contrato de mando.
- **F00–F15:** autoridad, identidad, órdenes, sensores, carrera, consola, vida de nave y universo dinámico se consumen por referencia, sin reajustar funcionalidades aprobadas.
- **Academy Life:** 20/20 contratos y referencia; campus no se copia como modelo civil universal.
- **Universo procedural:** 15/15 instalaciones, 18/18 asentamientos, LOD/población/gobierno/logística; no crear segundo motor.
- **Bloque Dynamic Universe 4:** `READY_TO_RESUME`, no iniciado; LORE-04A **no** puede marcar economía viva como finalizada.
- **CoreRPG:** WorldState, persistencia, transiciones, ejecución off-screen y scheduler son propietarios exclusivos; sin integración ni tests ejecutables del juego acreditados.
- **IA/UE5/NAP:** presentadores/consumidores, jamás autores de la verdad material.

## A08.3 Pruebas documentales y alcance exacto

**Artefactos de prueba:** `desarrollo/validation/consistency/lore04a_civil_society_invariants_v0.1.json`; `lore04a_scenarios_v0.1.json`; validador `validate_lore04_a.py`; pruebas de mutación `test_lore04_a.py`; workflow `.github/workflows/lore04-a-civil-life.yml`.

Las pruebas deberán comprobar:
1. Integridad A01–A08 y fuentes de verdad; referencias y registro de episodios.
2. Clasificación `SCREEN_CANON` / `OFFICIAL_REFERENCE` / `INFERRED` / `GAME_ADDITION` sin promoción automática.
3. Documentación de las 16 variantes positivas y negativas; cada caso con contexto y veto.
4. Autoridad exclusiva CoreRPG y distinción de LOD, población, identidad y relaciones.
5. Rechazo de atribución de profesión/persona por especie, religión por raza, ley inventada y moneda universal.
6. Rechazo de eventos futuros obligatorios, de confirmación ficticia del 2383 exacto y de «runtime funciona» sin prueba.
7. Las regresiones LORE-03 / LORE-01/02 existentes no deben alterarse por la PR.

**La ejecución de CI y sus resultados se documentan en la conversación de PR mediante comentario con SHA exacto y enlaces a los runs.** No escribir `PASS` sin evidencia. Las verificaciones locales de sintaxis no equivalen a ejecución en UE5.

## A08.4 Incertidumbres, deuda técnica y decisiones reservadas

| Prioridad | Cuestión | Tratamiento |
|---|---|---|
| Evidencia | minutería y secuencia exacta de episodios usados | `lore04a_evidence_ledger_v0.1.json`: anclas corroboradas editorialmente; no inventar minutajes |
| Autor | sistema monetario o salariales obligatorios en la Federación | diferir a 04B sin decidir |
| Autor | competencias legales y leyes de ficción sin prueba en canon | diferir a 04D sin decidir |
| Autor | fecha exacta de entrada 2383 | no fijar sin autorización |
| Técnicos | CoreRPG integración y simulación real | `BLOCKED_RUNTIME` hasta prueba separada; no bloquea documento |
| Contenido | mayor densidad etnográfica en civilizaciones con datos escasos | usar `UNKNOWN`, no rellenar con estereotipos |
| Producto | expedientes personales/privacidad y consecuencia de decisiones | no dar omnisciencia al diálogo; usar contratos de conocimiento |

## A08.5 Dictamen

A01–A08 **preparados como corpus documental**, pendientes de una validación automática con el HEAD publicado y de revisión del autor. **Si la CI y regresiones resultan satisfactorias, el estado justificable es `COMPLETE_DOCUMENTARY_PENDING_AUTHOR_MERGE`**, no `GAMEPLAY_IMPLEMENTED`. Si fallan, el estado permanece `IN_REVIEW`.

**Queda terminantemente prohibido:** modificar `main`, fusionar PR #51, eliminar rama o marcar administrativamente LORE-04A como cerrada antes de la autorización expresa de Roberto y verificación posfusión.

## A08.6 Traspaso a LORE-04B

Investigar economía, propiedad, producción/replicación, comercio, latinio y pluralidad monetaria; reutilizar `civilian_trade_operator_contract.json`, `replicator_post_scarcity_contract.json` y el Bloque 4 como propietario de economía dinámica. A no especifica la moneda que cobra un docente, ni crea transacciones nuevas.
