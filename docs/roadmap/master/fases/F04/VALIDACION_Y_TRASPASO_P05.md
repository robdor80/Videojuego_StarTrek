# F04-P05 — Matriz de aceptación ejecutable y traspaso a F05 (11-10-2026)

**Alcance:** probar **reglas Star Trek de referencia** con ejemplos observables; no simular un Core ni declarar jugabilidad UE5.

## Activos de prueba

- `tools/validation/f04_reference.py`: evaluador **referencial aislado** de autoridad, coberturas y exclusividad temporal; no es API Core ni sistema de órdenes de producción.
- `tools/validation/test_f04_reference.py`: pruebas unitarias que contrastan invariantes y cinco documentos canónicos existentes.
- `validation/fixtures/f04/authority_watch_acceptance_v0.1.json`: **39 casos** (26 autoridad, 7 dotación, 6 agenda).
- `.github/workflows/f04-reference-contracts.yml`: unittest + validación de fixture + compilación de Python sin terceros.

## Cuatro papeles jugables y casos que deben pasar

| Papel | Autorización positiva | Denegación obligatoria |
|---|---|---|
| Alférez recién incorporado a Sensores | Escaneo cualificado, en consola y guardia, reporte | Mando o política de guardias por el mero rango |
| Responsable de departamento | Ajustar asignaciones de su departamento, si es titular habilitado | Control de departamentos ajenos |
| Oficial de guardia de puente | Dar órdenes acotadas por guardia y órdenes permanentes | Decisiones de mando fuera de guardia |
| Capitán legal, jugador o NPC | Configurar rotación, aceptar/rechazar propuesta, nombrar sucesión/delegación lícita | Ignorar seguridad no anulable, crear personal y saltarse aptitud médica |

Coberturas: vacante sin NPC ficticio; civiles no cuentan como tripulación; una persona no ocupa dos plazas del mismo instante; personas ausentes no cubren guardia. Agendas: [inicio,fin), descanso incompatible, excepción solo con emergencia trazada/deuda; actividad localizada no equivale a dos puestos. Autoridad: cargo efectivo y vigencia, delegación acotada y revocada, relevo médico sin adjudicación del mando, Primera Directriz como evaluación no bloqueo duro universal y conflicto con orden superior explícito.

## Ejecución reproducible

```bash
python -m unittest discover -s tools/validation -p 'test_f04_reference.py' -v
python tools/validation/f04_reference.py --fixture validation/fixtures/f04/authority_watch_acceptance_v0.1.json
```

`REVIEW` es estado **sin ejecución automática** hasta revisión/decisión; `ALLOW` significa únicamente que el caso de *política de referencia* autoriza esa operación, no que se ejecutó una acción real. El test del código fuente garantiza solamente concordancia con modelos existentes.

## Orden de integración pendiente

1. **F03/Core:** proveer identidad/agenda/aptitud/nombramientos autoritativos y pruebas de persistencia en versión identificada.
2. **F04 ↔ Core:** traducir entradas y salidas con interfaces **aprobadas**, ejecutar negativos sobre World State y verificar exclusión concurrente.
3. **F05:** registrar orden/delegación/revocación, actualizaciones y consecuencias; no alterar autoridad desde IA.
4. **F06/F08/UE5:** consola Sensores y guardia interactiva; proveer evidencias E2E para alférez, mando de guardia y capitán.
5. Revalidar con `F01` (DEC-0001) y `F02` antes de cualquier merge de estado global.

## Puerta de cierre y evidencias

- `DISENO_VALIDADO`/referencia ejecutada solo tras confirmar CI de esta rama y fixture.
- `REFERENCIA_PROBADA` **limitado** a las reglas cubiertas por el simulador; no prueba spawn/persistencia ni sistema completo de órdenes.
- `CORE_INTEGRADO` / `UE5_JUGABLE` / `ACEPTACION_SUPERADA`: **NO_EJECUTADO**; requieren SHA, versión, tests reales, trazas y ausencia de incidencias bloqueantes.
- El `ESTADO_GLOBAL.json` se mantiene sin cambios mientras F01/02/03 continúen abiertas; F04 **no** se marca CERRADA en el registro central.

**No decidir:** Dama Imperator, canon/épocas nuevas, reglas definitivas Core, gestión completa F05 de órdenes ni primera guardia jugable. Proseguir F05 a nivel de diseño una vez revisado este contrato.

## Evidencia CI — 11-10-2026

La revisión inicial detectó dos errores de código de referencia (cierre de paréntesis y acceso a campos opcionales sin guardas); fueron corregidos en commits posteriores sin alterar fuentes de juego. GitHub Actions [run 38156353372](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38156353372) terminó **SUCCESS**: compilación Python, 16 tests unitarios y fixture de 38 escenarios. El negativo número 39 (médico sin nombramiento vigente) está incluido y **confirmado** en el [run 38156511824](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38156511824): **SUCCESS**, 16 pruebas unitarias y 39 escenarios de fixture; tampoco acredita Core/UE5. **No** acredita Core/UE5.
