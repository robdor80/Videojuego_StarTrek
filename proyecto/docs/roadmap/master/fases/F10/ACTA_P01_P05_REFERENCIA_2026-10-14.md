# F10 — Acta de preparación P01–P05 · 14-10-2026

**Rama:** feat/f10-academy-continuity-reference-20261014  
**Nivel acreditable:** REFERENCIA_PROBADA para auditoría, contratos y trayectoria simulada.  
**No alcanzados:** CORE_INTEGRADO, UE5_JUGABLE ni ACEPTACION_SUPERADA.

**La fase F10 global NO queda cerrada por esta acta.** Falta jugabilidad real en UE5, el adaptador CoreRPG y la prueba de guardado/carga de una partida en el MSI.

## P01 — Currículo y academiaflota

Se conservan las fuentes aprobadas de sistemas/gameplay/careers/academy_path y los bancos, manuales y guías existentes. La auditoría estática verifica **4 años, 12 trimestres, 60 asignaturas y 7 ramas**. Los manifiestos declaran 501 unidades diseñadas y 67 manuales, 67 bancos de evaluación y 67 guías: las declaraciones editoriales no prueban clases ya impartidas en UE5. Los identificadores y su orden se contrastan con academiaflota en SHA 0a46971059950bb234ec6fd5114cee03cb2c5984.

**No verificados:** Google Auth, Firestore, perfiles reales y contenido web actualizado después de dicho SHA.

## P02 — Separación de autoridad

La web sirve para consultar y practicar; puede remitir **propuestas** de evidencia, pero nunca dar aprobados, rango, ascenso ni destino oficiales. CoreRPG con host autenticado será el dueño de reglas, mutaciones, expediente y persistencia; UE5 representará acciones y escenas; la IA solo explica y dialoga.

El validador f10_academy_reference.py deja la evidencia web nueva en REQUIRES_CORE_REVIEW sin aplicar efectos. La cadena CORE_HOST_VERIFIED de los fixtures **NO autentica** a un usuario: es exclusivamente un stub de pruebas.

## P03 — Vida académica y expediente

Se reutilizan en lugar de duplicarlos:
- Academy Life paso 5: generate_academy_schedule_step5.py (horarios y trayectos).
- Paso 12: resolve_academy_mentors_instructors_step12.py (docencia y tutorías; sin notas automáticas).
- Paso 18: resolve_academy_year_progression_step18.py (ascenso de curso por evidencias).
- Paso 19: integrate_academy_record_step19.py (expediente append-only con proveniencia).
- Las veinte suites preexistentes Academy Life.

f10_academy_continuity.py reproduce clases, eventos sociales de solo traza, prácticas, selección personal de especialidad, progresión, graduación y carrera. **No conecta todavía NPC, clases ni calendarios a un mundo UE5.**

## P04 — Sensores, Kobayashi Maru y ceremonia

Hay dos prácticas de referencia: sensors_training y kobayashi_maru. Ambas consumen resultados ya confirmados por el fixture y nunca generan automáticamente notas. Kobayashi está restringido al cuarto curso y no interpreta vencer como requisito del escenario imposible. Cuarto curso terminado => graduation_pending; después se confirman por separado graduación, comisión de Alférez y primer destino.

**No probado:** consola de Sensores operativa en UE5, holocubierta real, Kobayashi jugable, profesor 3D, ceremonia y transiciones de escenario. La V001 usará el puente Sutherland cuando esté preparado; el Kelvin se reserva para otro uso.

## P05 — Continuidad y persistencia de prueba

Fixture: desarrollo/validation/fixtures/f10/f10_academy_lifecycle_offline_v0.1.json. **16 eventos** trazan la trayectoria aspirante→cadete→cuatro cursos→graduación→alférez→destino. Las pruebas niegan ingresos y aprobados falsos, imposición de especialidad, saltos de curso, comisión prematura, destino sin orden/vacante, IDs duplicados y alteración de saves.

La serialización JSON + SHA-256 comprueba corrupción y restauración **offline**; no es guardado transaccional CoreRPG ni firma segura.

## Evidencias reproducibles

CI: .github/workflows/f10-academy-reference.yml. Revisa datos académicos, versión fijada de academiaflota, 20 suites Academy Life, replay de los cuatro años y todos los test_f10_*.py. Adjunta el artefacto temporal f10-academy-offline-snapshot (NO partida).

Comandos:

    python desarrollo/tools/generation/run_academy_life_suite.py
    python desarrollo/tools/validation/f10_academy_continuity.py --scenario desarrollo/validation/fixtures/f10/f10_academy_lifecycle_offline_v0.1.json --output desarrollo/validation/results/f10_academy_lifecycle_snapshot.json
    python -m unittest discover -s desarrollo/tools/validation -p 'test_f10_*.py' -v

El enlace y SHA de CI figuran en la PR. CI verde solo acredita la referencia Python.

## Puertas pendientes para F10 CERRADA

1. Adaptador CoreRPG autenticado con versión fija y persistencia/eventos oficiales.
2. Academy Life realmente conectada a NPC persistentes, horarios, aulas y evaluaciones en UE5.
3. Consola Sensores, Kobayashi y ceremonia realmente operativos en el MSI.
4. Save/load real entre cursos y después de destinarse a una nave, preservando expediente y vínculos.
5. Evidencias de aceptación jugable, rendimiento, no regresión y actualización del estado maestro.

**Dictamen:** preparación autónoma F10 terminada en su alcance de referencia; fase global aún abierta por integración CoreRPG y UE5.
