# F03-P05 — Validación reproducible de los contratos de continuidad

**Fecha de auditoría:** 2026-10-11; **actualización de dependencias documentales:** 2026-10-13. **Nivel real alcanzado:** referencia estructurada y QA estática. **Nivel objetivo pendiente:** `CORE_INTEGRADO`. F01 PR #2 y F02 PR #3 ya están fusionadas, sin que eso acredite integración Core/Host.

## Artefactos

- `validation/fixtures/f03/continuity_reference_v0.1.json`: escenario **inerte**, fechado 2372-03-14, dos entidades preexistentes, tres plazas (dos NPC B, una C), dos observadores con contactos distintos, seis eventos originales enlazados, una orden completada y otra pendiente.
- `tools/validation/validate_f03_reference.py`: validador **de fixture**, sin alterar datos, llamar a Core ni generar mundos. Lee además **8 fuentes originales**, `sensor_result_contract.json`, `persistent_state_roundtrip_contract.json` y los 13 invariantes originales del fixture de Sensores.
- `tools/validation/test_f03_reference.py`: 26 pruebas herméticas (incluyen corrupción, duplicación, contacto ajeno, filtración en campos anidados, cronología, causalidad y tareas solapadas).
- `.github/workflows/f03-reference-contracts.yml`: checkout y Python 3.12, validador y batería `unittest` en CI al cambiar estos archivos. El workflow **no compila Core ni UE5**.

## Ejecución reproducible

Desde la raíz del repositorio:

```bash
python tools/validation/validate_f03_reference.py
python -m unittest discover -s tools/validation -p 'test_f03_reference.py' -v
```

Los comandos son requisitos de ejecución y no evidencia de haber pasado. **Evidencia: consultar GitHub Actions del PR de F03 y registrar estado y enlace de run.** Si está pendiente o falla, no declarar `REFERENCIA_PROBADA` hasta observar resultado.

## Cobertura real vs pruebas de integración previstas

| Grupo | Comprueba el validador/fixture | Lo que sigue pendiente en Core/Host |
|---|---|---|
| P01 `F03-T01..T05` | Seed/era/timestamp presentes; IDs/slots no duplicados; materialización anterior a observación | Ejecutar dos generaciones idénticas; C→B real; descarga/carga Actor |
| P02 `F03-T06..T11` | Dos observadores, IDs relativos, ocultación por nivel, secreto y referencias privadas separados | API Knowledge por actor/rol, redacción end-to-end y negativa de acceso |
| P03 `F03-T12..T16` | Exclusividad de agenda, orden temporal y causalidad de la bitácora existente | Avance de reloj, gastos/recursos, tránsito y catch-up auténticos fuera de escena |
| P04 `F03-T17..T22` | JSON fixture estable tras serialización Python, detección de corrupción de estructura, versión desconocida e idempotency keys únicas | Save/load transaccional Core, migración real, recuperación de fallos, orden in-flight |
| P05 QA | 26 pruebas de validador y 8 referencias verificadas | Suite E2E Core/UE5 y 13/13 criterios ejecutados del fixture original |

**Advertencia de terminología:** un `json.dumps / json.loads` demuestra únicamente que el JSON del fixture puede serializarse; NO demuestra la persistencia de un videojuego. Las claves de idempotencia únicas **no demuestran** ejecución exactamente una vez. Una cadena de eventos estática **no prueba** que el NPC esté actuando. Mismo fixture textual **no acredita** determinismo de un generador.

## Protocolo de pruebas de integración cuando se desbloquee Core

1. Registrar SHA y versión exacta de Core`main`, ABI usada en Host, versión del paquete Trek, rama/commit y sistema operativo.
2. Repetir generación con idéntica semilla/configuración/versiones; comparar identidad y semántica persistidas, también con contexto distinto y tras añadir generador ajeno.
3. Ejecutar observación con dos naves, permiso autorizado y denegado, contacto parcial, UI/IA filtrada; comprobar que la verdad no varía ni aparece en telemetría de presentación.
4. Forzar descarga/reload de Actor, NPC en jornada fuera de escena, órdenes completadas e in-flight, cambios de puesto, reparación y reasignación real de lanzadera.
5. Guardar, matar proceso, restaurar, migrar un schema soportado, probar corruptos/futuros/reintento de timeout; comparar IDs, slots, prefijo histórico, cursor, permisos y efectos duplicados.
6. Ejecutar los 13 `must_pass` de `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json` con pruebas positivas y negativas; archivar logs de ejecución y fallos.
7. Sólo si se verifican límites con Core integrado, negociar cierre técnico de F03 y registrar PR y evidencia: `CORE_INTEGRADO` **no se reclama en esta PR**.

## Bloqueos y escalado

- **B-01 CORE:** `CoreRPG/main@dcfcb83c` no integra aún 4.5 ni funcionalidades posteriores de persistencia, conocimiento, acciones/simulación. Reconsultar al integrar.
- **B-02 HOST:** no hay prueba de UE5 Windows/EntityId↔Actor frente a API real.
- **B-03 GOBIERNO — ACTUALIZADO:** F01 DEC-0001 resuelta (Galaxy → nueva Clase Valhalla) y PR #2/#3 fusionadas. Persiste la obligación de conciliar madurez real y cierre formal; no modificar estado global fingiendo que F03 está integrada en Core.
- **B-04 ESQUEMAS:** saltos de versionado/almacenamiento y mecanismo de idempotencia requieren contrato formal del Core.

**Resultado de la fase para esta rama:** los cinco pasos tienen entregables inspeccionables, pero **F03 permanece EN_REVISION/BLOQUEADA_CORE**, nunca `CERRADA` ni `CORE_INTEGRADO` hasta pruebas reales.


## Acta de QA estática ejecutada (GitHub Actions — 11-10-2026)

**Evidencia real observada**, tras checkout de la rama en GitHub Actions:
- [Push run 38153741443](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38153741443): `completed/success` en `a360e2cd96fbf7d2c2b45ff60fd6a624fd8a9d2e`.
- [PR run 38153764549](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38153764549): `completed/success` para la [PR #4](https://github.com/robdor80/Videojuego_StarTrek/pull/4) sobre el mismo head SHA.
- Entorno verificado en logs de push: Ubuntu GitHub-hosted, CPython **3.12.15**, código de la rama `docs/f03-world-knowledge-persistence`.
- Validador: **PASS**; 2 entidades, 2 proyecciones, 6 eventos, 2 órdenes, 3 plazas; 8 fuentes de referencia y los 13 invariantes originales de Sensores verificados estructuralmente.
- `unittest`: **26/26 tests OK** (0 errores, 0 fallos), conforme al log del job `static-reference-checks`.
- Enlace del job push y registro: [workflow run](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38153741443). Auditoría de enlaces internos de los seis Markdown F03 realizada sobre árbol de rama: **0 enlaces relativos rotos**.

**Conclusión comprobada:** `REFERENCIA_PROBADA` **sólo del validador y fixture estático P05**. Integración de Core/Host, prueba de migración real, persistencia real, generación determinista real, clock/catch-up y UE5 = **NO_EJECUTADOS/BLOQUEADOS**. F03 completa NO se declara cerrada.
