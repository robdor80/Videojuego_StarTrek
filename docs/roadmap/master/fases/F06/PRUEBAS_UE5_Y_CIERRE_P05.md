# F06-P05 — Pruebas independientes y puerta de integración UE5

## Referencia implementada
- Motor original de Sensores reutilizado y **endurecido** en esta PR: tools/simulation/resolve_sensor_scan.py (supresión de censos internos no observados y validación defensiva). No es un World State de producción.
- Orquestador **no autoritativo**: tools/simulation/f06_reference.py.
- Suite: tools/simulation/test_f06_reference.py (**23 pruebas verificadas en el corte del 12-10-2026; se revalidarán tras sincronizar con F04/F05**).
- Regresión del motor: tools/simulation/test_sensor_detection_v0_1.py (**8 pruebas preexistentes**).
- Test de cadena F04→F05→F06: tools/simulation/test_f04_f05_f06_cross_phase.py (**3 casos obligatorios** tras fusionar PR #4/#5/#6).
- Workflow: .github/workflows/f06-sensors-reference.yml, Python 3.12 sin dependencias externas; ejecuta además la regresión de referencia F03/F04/F05 ya fusionadas.

## Ejecución reproducible
En raíz del repositorio:

    python -m py_compile tools/simulation/resolve_sensor_scan.py tools/simulation/f06_reference.py tools/simulation/test_f06_reference.py
    python -m unittest discover -s tools/simulation -p 'test_sensor_detection_v0_1.py' -v
    python -m unittest discover -s tools/simulation -p 'test_f06_reference.py' -v
    python -m unittest discover -s tools/simulation -p 'test_f04_f05_f06_cross_phase.py' -v

Las **23 pruebas** F06 (revisadas el 12-10-2026) abarcan: diez ramas y tres modos, motor anterior, no mutación, determinismo, no filtración de verdad oculta, identidad por observador, resultados parciales, sector equivocado permitido, filtro erróneo, interferencia/modo, focalizado limitado al contacto conocido, daños y falta de recursos, autorización, parámetros inválidos, cadena causal de eventos, procedencia de dossier, paquete a Ciencia y compatibilidad de contratos, blindaje contra la filtración de recuentos de entidades ocultas y rechazo defensivo de entradas inválidas.

## Evidencia y cautela
**No confundir** una suite incorporada con una suite ejecutada. **Evidencia inicial:** [Actions 38179039670](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38179039670), 8/8 regresión y 18/18 F06. **Evidencia posterior** (12-10-2026): [Actions 38228217392](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38228217392), 8/8 regresión y **23/23 F06**, con tres pruebas interphase OMITIDAS entonces. **Desde el 13-10-2026 esas tres pruebas se exigen en CI** y deben constar como ejecutadas, sin skips; consultar la ejecución más reciente para acreditar su resultado. Archivo de evidencia histórica: EVIDENCIA_P05.json. Los eventos/dossiers/paquetes de referencia son propuestas sin commit, y no prueban consola jugable, latencia, memoria persistente o IA conectada. Los eventos/dossiers/paquetes de referencia son propuestas sin commit; no prueban consola jugable, latencia, memoria persistente o IA conectada.

## Entrega a la F07/F08 (interfaz del puesto)
La pantalla/puente UE5 debe consumir datos confirmados del Core; **no llamar al módulo de referencia como autoridad**. Adaptador conceptual requerido:

| Intercambio | Campos Star Trek | Origen legítimo |
| --- | --- | --- |
| Configurar | console_id, request, prefill, operator_id | UI, sin autoejecución |
| Solicitar acción | order_id opcional, operation_id, observer_id, requisitos de recurso | Core autorizado |
| Cambio de estado | queued/running/partial/completed/failed/cancelled y hora de campaña | Scheduler/World State Core |
| Observar | detecciones con confidence, contact_id, provenance, observaciones | Proyección Core por observador |
| Conservar | observation_id, dossier_id, result_id, eventos append-only | Persistencia Core |
| Enviar a Ciencia | handoff_id, included_observation_ids, receptor, estado | Transporte y permisos Core |

**No son firmas ABI, RPC ni métodos existentes**; solo un acuerdo de semántica que deberán adoptar los componentes reales.

## Pruebas de aceptación **pendientes**
1. Una nave y tripulación reales ocupan el puesto; una orden de capitán NPC llega al alférez por F05.
2. Ejecutar barrido con demora, estado intermedio y coste **real**, bloquear matriz destruida.
3. Confirmar observación visible sin revelar entidad oculta; comparar otra nave/observador.
4. Guardar, salir, cargar; recuperar idénticos mundo, contacto, eventos y progreso.
5. Transferencia a Ciencia entregada/aceptada; conclusión científica posterior con fuentes.
6. Fallo de alimentación, interrupción, órdenes revocadas y actor ausente con efectos coherentes.
7. Probar consola UE5 en el MSI y registrar build, FPS y resultado.

**Propietarios:** Core RPG para reloj, autoridad, persistencia y evento; Star Trek para reglas y casos de juego; UE5 para interacción; Academia para materiales de formación (web independiente).

## Dependencias
**Actualización 13-10-2026:** PR #2–#6 **fusionadas**; la aceptación global F06 continúa supeditada a Core RPG y a F07/F08. Esta PR integra **solo referencia y pruebas**, sin modificar ESTADO_GLOBAL.json ni declarar F06 CERRADA. Se revisará y fusionará tras CI satisfactoria; la fusión no equivale a integración UE5.
