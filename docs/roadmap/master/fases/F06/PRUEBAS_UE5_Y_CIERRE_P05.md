# F06-P05 — Pruebas independientes y puerta de integración UE5

## Referencia implementada
- Motor previo reutilizado sin cambios: tools/simulation/resolve_sensor_scan.py.
- Orquestador **no autoritativo**: tools/simulation/f06_reference.py.
- Suite: tools/simulation/test_f06_reference.py (**16 pruebas definidas**).
- Regresión del motor: tools/simulation/test_sensor_detection_v0_1.py (**8 pruebas preexistentes**).
- Workflow: .github/workflows/f06-sensors-reference.yml, Python 3.12 sin dependencias externas.

## Ejecución reproducible
En raíz del repositorio:

    python -m py_compile tools/simulation/resolve_sensor_scan.py tools/simulation/f06_reference.py tools/simulation/test_f06_reference.py
    python -m unittest discover -s tools/simulation -p 'test_sensor_detection_v0_1.py' -v
    python -m unittest discover -s tools/simulation -p 'test_f06_reference.py' -v

Las pruebas F06 abarcan: diez ramas y tres modos, motor anterior, no mutación, determinismo, no filtración de verdad oculta, identidad por observador, resultados parciales, sector equivocado permitido, filtro erróneo, interferencia/modo, focalizado limitado al contacto conocido, daños y falta de recursos, autorización, parámetros inválidos, cadena causal de eventos, procedencia de dossier, paquete a Ciencia y compatibilidad de contratos.

## Evidencia y cautela
**No confundir** una suite incorporada con una suite ejecutada. La evidencia de una ejecución se registra solo al disponer de estado y logs observables de GitHub Actions. Los eventos/dossiers/paquetes de referencia son propuestas sin commit; no prueban consola jugable, latencia, memoria persistente o IA conectada.

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
PR #2–#6 abiertas; la aceptación global F06 se aplaza a la coordinación de Core y a la futura F07/F08. La rama F06 se propone **en borrador**, sin mover ESTADO_GLOBAL.json ni proclamar la fase como CERRADA.
