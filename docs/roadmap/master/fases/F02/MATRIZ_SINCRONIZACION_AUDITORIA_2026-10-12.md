# F02 — Matriz de sincronización tras auditoría (2026-10-12)

> **Actualización de gobierno 2026-10-13:** todas las PR #2–#7 se han **fusionado**; la cadena F04→F05→F06 ya se ejecutó sin skips en [CI integrada](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38321712021). El texto inferior documenta el **corte histórico previo** y no describe el estado actual. [Acta vigente](../../ACTA_RECONCILIACION_F00_F06_2026-10-13.md): F01 cerrada en diseño, F02 activa, F03–F06 en revisión con Core/UE5 pendientes.

**Estado:** plan de coordinación, NO aprobación de APIs nuevas ni `CORE_INTEGRADO`.
**Estado al auditar (12-10-2026):** las PR #2–#7 estaban en borrador. **Actualización 13-10-2026:** PR #2 (F01) **fusionada**, PR #3 (F02) marcada **Ready for review** y sin conflicto con `main` en la comprobación; PR #4–#7 todavía requieren revisión y tratamiento secuencial.

## Línea base comprobada

- Star Trek `main@6069f6aa`, conserva acuerdos F00; los commits posteriores del buzón son ideas, no runtime.
- CoreRPG `main@dcfcb83c` = 4.4; la rama 4.5 `feat/generic-world-state@2a3da891` está **fuera de main** y ha divergido (2 commits por delante, 1 por detrás). Su CI no implica aceptación API.
- Core RFC NPC en `docs/npc-initiative-authority-roadmap-20261011`: **propuesta documental**, no ActionEngine universal ni implementación 4.10.

## Correspondencia de contratos de referencia

| Fuente | Emite / verifica | Consume / condición | Prohibición |
| --- | --- | --- | --- |
| F04 — `issue_reference_binding` | Solo tras `evaluate=ALLOW`; actor/acción/puesto/revisión y plazo | F05 `authorization_binding` con `source=F04_REFERENCE` | Un diccionario de Python NO es una credencial auténtica |
| F05 — `assess` | Revalidación explícita, entrada incompleta denegada | F06 necesita decisión real de Core; en tests acepta un binding F05 de referencia | `ALLOW_REFERENCE` no aplica efectos ni garantiza ejecución |
| F06 — `authorization_binding_valid` | Comprueba actor/operación/puesto/nave/revisión/plazo de la propuesta | Core debe revalidar al reservar recursos y producir eventos reales | Ninguna UI/LLM puede inventar autorización |
| F06 — `resolve_sensor_scan` | Devuelve contactos observados sin censos de no detectados | La proyección autorizada hacia UI, IA y Ciencia | Prohibido usar métricas de verdad oculta |
| F06 — `event_candidates` | Solo intenciones estructuradas y resultado estimado | Core confirma inicio, resultado, informe por separado | `events=[]` hasta commit; no inventar `REPORT_MADE` |

**Importante:** estas formas internas de Python existen para comprobar coherencia entre fases, **no** se deben estandarizar como ABI/API pública Core. El diseño definitivo debe proceder de Q01–Q08, host H01–H04 y un ejemplo ejecutable de ambos universos.

## Contratos y preguntas aún bloqueadas

1. **Core 4.5**: confirmar identidad, revision, contención y garantías; contención no significa turno, ubicación ni destino.
2. **4.6/4.10**: acordar quién convierte una intención en una acción autorizada. F04 es política Trek; Core conserva mutación técnica.
3. **4.7**: guardado/restauración de semilla, IDs, órdenes, conocimiento, tareas, eventos y progreso de la guardia.
4. **4.9**: visibilidad por observador, secretos y anti-filtración antes de exponer datos al Host.
5. **4.10/4.12**: idempotencia, revocación, concurrencia y evaluación de una respuesta IA tardía. El proveedor IA nunca es una autoridad.
6. **UE5/MSI**: compilar y enlazar Core C++20 en Host y demostrar que descargar el Actor no destruye el NPC.
7. **Manual PDF F06-P01**: inspección visual pendiente y obligatoria antes del cierre.
8. **Licencias de planos e imágenes**: clasificación obligatoria de recursos externos antes de su distribución; no mover/borrar/convertir binarios en esta auditoría.
9. **F01 / DEC-0001 — RESUELTA:** el autor eligió **Galaxy/Enterprise-D** como referencia artística de una **nueva Clase Valhalla**, no Imperator. Fecha de servicio no fijada. La decisión no bloquea el prototipo interno de Sensores ni valida por sí sola ningún puente UE5.

## Orden de revisión y pruebas posterior a las PR

- Comprobar SHA de cada rama y `main`, sin asumir que estados o informes antiguos estén actualizados.
- Revisar y fusionar **secuencialmente** PR #3→#7 tras la PR #2 ya fusionada. **No** inferir cierre formal F01 o integración Core/UE5 por el mero merge de documentación.
- F02: ejecutar sus validadores documental y 9 tests; F03: 26; F04: 39 casos/17 unit; F05: 48 casos/19 unit; F06: 8 legados/23 unit.
- En **main integrado**: ejecutar `test_f04_f05_f06_cross_phase.py`; sus **tres** casos aparecen SKIPPED en PR #7 aislada, y deben pasar efectivamente con F04/F05 integradas.
- Demostrar después el slice real capitán NPC→orden→Sensores→Ciencia→eventos→save/load→UE5. Hasta entonces **NO-GO para F08 jugable**.
- Actualizar `ESTADO_GLOBAL.json` por madurez verdadera de cada tarea, sin convertir referencia Python en juego funcional.
- Las PR pasan de DRAFT a revisión individual cuando se autoriza y comprueba su preparación; F07/F08 permanecen formalmente aparcadas hasta la sesión de integración acordada.

## Seguimiento de incidencias auditadas

A-01 F05 valores permisivos **corregido en PR #6**. A-02 vínculo estructurado referencial **corregido en PR #5–#7; sin credencial Core**.
A-03 filtración de recuentos directos **corregido en PR #7**.
A-04 validación finita y mundo inválido **corregido en PR #7**.
A-05 CI de contratos **ampliado en PR #7**.
A-06 hechos no confirmados **separados como candidatos en PR #7**.
A-07 Core pendiente; A-08 pruebas cruzadas preparadas (ejecución pos-merge pendiente);
A-09 Dama **resuelta mediante DEC-0001 (Galaxy → Valhalla)**; A-10 PDF pendiente; A-11 derechos/licencias pendiente;
A-12 suite transversal se ejecutará tras integrar, no certificada anticipadamente.

Ninguna de las modificaciones modifica `robdor80/CoreRPG` ni decide APIs 4.5–4.12.
