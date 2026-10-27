# F09 — Preparación autónoma P01–P05 (sin sustituir Core/UE5)

**13-10-2026 · Alcance:** contrato de referencia y validador de **transferencia de datos**, no consolas 3D funcionales. **La fase global permanece PLANIFICADA (runtime) y el objetivo UE5_JUGABLE no se ha alcanzado.** F02 es la única fase principal EN_CURSO.

## F09-P01 · Prioridad de consola

Orden propuesto para implementar después de Sensores: **Ciencia**, **Navegación**, **CONN**, **Operaciones**. Están conectadas con acciones ya definidas (lecturas, análisis, ruta, ejecución de vuelo y solicitudes de potencia), sin inventar un motor paralelo.

| Familia | Entrada aprobada o reutilizada | Resultado de referencia (aún no ejecutable) |
|---|---|---|
| Ciencia | sensor_to_science_analysis_handoff.json y incoming_analysis_task_contract.json | Tarea interpretable, hipótesis con procedencia; solicita nuevos datos sin inventar hechos |
| Navegación | sistemas/gameplay/navigation/navigation_order_contract.json | Solución/rumbo validable; datos observados de Sensores y cartas reales |
| CONN | sistemas/gameplay/navigation/navigation_state.json y bridge_station_model.json | Ejecución de maniobras solo tras solución, autoridad, recursos y seguridad |
| Operaciones | power_allocation_model.json y sensor_to_operations_power_request.json | Evaluación de prioridad y recursos; solicitud ≠ concesión |

No declarar que las funciones sean botones ya conectados a UE5. La autoridad decisoria recae en el dominio correspondiente y las reglas de mando.

## F09-P02 · Avería, combate, seguridad y canales

**Ingeniería** valida daños/reparaciones, **Táctica** evalúa objetivos con reglas de enfrentamiento, **Seguridad** administra incidentes y acceso, **Comunicaciones** gestiona canales, retardo y destinatario. **No** se deduce un éxito porque el paquete haya llegado. Referencias preexistentes: `sistemas/gameplay/engineering/engineering_loop.json`, `sistemas/gameplay/tactical/tactical_state.json`, `sistemas/gameplay/security/`, `sistemas/gameplay/communications/subspace_communication_contract.json`. Exigir resultados y restricciones de cada subsistema.

## F09-P03 · Resto de dominios

**Mando** (orden válida, delegación, alertas), **Misiones** (tareas y contexto), **Transportador** (fijación, interferencias, escudos y traslado real), **Médica** (privacidad, cuidados y triaje), **Ambiental** (soporte vital, fallos y cargas), **Hangar** (capacidad, tráfico, plaza de lanzadera, control), **Ordenador** (consulta permitida, respuestas con procedencia y IA únicamente propositiva).

Son **familias funcionales**, no 15 modelos físicos nuevos. La estación de puente y las capacidades por clase siguen en `sistemas/gameplay/ship_operations/bridge_station_model.json`; la UI y los materiales son responsabilidad UE5/NAP.

La matriz `sistemas/gameplay/ship_operations/consoles/f09_reference_matrix_v0.1.json` registra las 16 familias, la prioridad, fuentes reales, operaciones sugeridas y rutas de **datos**, sin cambiar los modelos originales.

## F09-P04 · Ensayo seguro entre consolas

**Ruta de datos:** Sensores → Ciencia → Ordenador/Mando, o Navegación → CONN, con referencias conocidas y comprobación de permisos.

La implementación pura `desarrollo/tools/validation/f09_interconsole_reference.py` acepta un paquete según `interconsole_data_package_contract.json` y una **instantánea confiable emitida por Core/Host** que delimita los datos conocidos y rutas autorizadas. Nunca se debe poblar esa instantánea con valores del paquete, con un formulario de usuario ni con la IA remota. Resultado `ACCEPT_DATA_ONLY`: únicamente admite metadatos para eventual entrega, **no crea una tarea, no muta el World State ni certifica que el receptor haya actuado**.

Los valores antiguos `conn_navigation` y `computer_database` del contrato de intercambio son **ambiguos respecto a las familias canónicas**. Se devuelve `CLARIFY_TARGET` para que el adaptador resuelva la familia concreta; no se reescribe ni invalida el contrato histórico. Los campos nuevos no aprobados y datos completos inline se rechazan. Esta referencia **no autentica** identidad ni implementa funciones de Core.

## F09-P05 · Escenarios a completar

| Escenario | Validación local posible | Bloqueo final |
|---|---|---|
| Avería de Sensores → Ingeniería → Operaciones | Transferencia de diagnóstico observado; denegación de referencias ocultas | Reparación, consumo y efectos reales Core, display UE5 |
| Combate → Táctica → CONN/Mando | Ruta y autorización contextual de datos | Reglas combate, blancos, daños, fuego y UE5 |
| Misión → Comunicaciones/Misiones/Transportador | Rutas permitidas, privacidad y ausencia de filtraciones | Latencia, ejecución de misión y transporte autoritativo |
| Orden multitarea de Capitán → varios departamentos | Catálogo y rechazo de transferencia no autorizada | Delegación, simultaneidad, eventos y save/load Core |
| Medicina → Mando en incidente | Denegación sin autorización | Filtrado médico real y roles Core |
| Diferentes clases de nave | Catálogo desacoplado de puestos físicos | Capacidades concretas Oberth/Miranda/Intrepid/Valhalla y pruebas en UE5 |

**Criterio de no regresión:** los 16 nombres, la línea Sensores→Ciencia, el origen de los datos, la privacidad y la separación de autoridad se conservan. No crear un sistema universal de órdenes en Star Trek. Ninguna ruta por sí misma ejecuta energía, movimiento, disparo, sanación o transporte.

## Evidencias y ejecución

Se incluyen [22 casos P05 solo de metadatos](../../../../../../desarrollo/validation/fixtures/f09/f09_interconsole_scenarios_v0.1.json) (avería, combate, misión, orden multitarea y privacidad), `desarrollo/tools/validation/test_f09_interconsole_reference.py` y `.github/workflows/f09-console-reference.yml` para QA automatizada de catálogo y escenarios negativos. **Las pruebas de CI, si pasan, acreditan solo la referencia Python y rutas de archivos.** Sin conexión real CoreRPG/UE5 ni pruebas MSI: **NO_EJECUTADO** para P01–P05 a nivel jugable. Para cerrar F09 se necesitarán SHA/versión de Core, pruebas de acciones reales autorizadas, persistencia, recursos/daños y test de la escena UE5 de cada dominio.


## Límite de compatibilidad heredada

El contrato fijo `interconsole_data_package_contract.json` todavía enumera valores agrupados `conn_navigation` y `computer_database`, pero **no** todas las 16 etiquetas canónicas (`sensors`, `navigation`, `conn`, `computer`) como receptor. La matriz F09 es una **propuesta de normalización**; no puede conectarse al contrato fijo sin una migración aditiva acordada y pruebas de compatibilidad. Las 22 situaciones son intercambios de **metadatos**, no ensayos reales de reparaciones, fuego, transporte ni ejecución de órdenes.
