# F03-P05 — Validación reproducible de los contratos de continuidad

**Fecha:** 2026-10-11. **Nivel real alcanzable ahora:** referencia estructurada y QA estática. **Nivel objetivo pendiente:** `CORE_INTEGRADO`. Se respetan los bloqueos de F02 PR #3 y F01 PR #2.

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
- **B-03 GOBIERNO:** F01 DEC-0001 y PR #2 sin resolver; F02 PR #3 draft; no modificar estado global de forma que simule cierre de ambas.
- **B-04 ESQUEMAS:** saltos de versionado/almacenamiento y mecanismo de idempotencia requieren contrato formal del Core.

**Resultado de la fase para esta rama:** los cinco pasos tienen entregables inspeccionables, pero **F03 permanece EN_REVISION/BLOQUEADA_CORE**, nunca `CERRADA` ni `CORE_INTEGRADO` hasta pruebas reales.
