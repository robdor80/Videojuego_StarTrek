# F06 — Sensores nativos Star Trek sobre CoreRPG

**Estado:** implementación nativa ampliada en PR Draft; última CI y MSI por verificar. F06 NO cerrada. Véase [auditoría P02–P04 y Enterprise-D](INTEGRACION_UNIVERSO_OPERACIONES_GALAXY_2026-11-06.md).

## Arquitectura real

- `desarrollo/integration/f04/src/f04_bridge.cpp` continúa siendo la **única** sesión de CoreRPG. F06 se habilita solo con `F06_ENABLE_SENSORS`; compilaciones originales F04/F05 permanecen apagadas por defecto.
- Los `f06_signal` representan **firmas reales materializadas por el Host de mundo** como entidades Core. Solo el puerto nativo privilegiado `f06_host_signal` puede incorporarlas o actualizarlas; la interfaz LCARS o un LLM NO pueden hacerlo.
- Los `f06_contact` son observaciones del sensor sobre esas firmas, **no** objetos que generen contactos del universo. Su estado, IDs públicos, última lectura y clasificación validada son relaciones en WorldState y se conservan mediante el guardado/carga original.
- En cada `f04_advance`, incluso fuera de cámara, F06 resuelve de nuevo la vigilancia pasiva corta/larga y compara cambios. No crea incidentes, naves ni un bucle por fotograma.
- Una orden F05 `F04_SCAN` ejecutada tras revalidación desencadena además una evaluación activa en la **misma transacción Core**. Los recibos F05 conservan su semántica previa de tirada Core; su resultado no es un dossier sensorial nuevo ni contiene identidad oculta.
- Una solicitud directa de focalización exige un contacto **actualmente activo** y un operador F04 cualificado, de guardia y físicamente en su consola.
- El resultado público nunca expone el ID de firma real, propiedades de `ground_truth` ni censos de firmas no detectadas. El ID público de contacto no coincide con `EntityId` Core.
- Los avisos significativos son eventos Core de F04 (`OP=6001..6005`) que pueden entrar en la política de archivo de historial existente; no se crean miles de registros por cada barrido.

## Contratos de referencia que se reutilizan

- `sistemas/gameplay/duty_system/sensor_watchstanding_protocol_v0.1.md`
- `sistemas/gameplay/ship_operations/consoles/sensors/` (10 menús)
- `sistemas/gameplay/ship_operations/sensor_resolution/sensor_detection_rules.json` (umbrales inspiradores, **no** ecuación canónica)
- `desarrollo/tools/simulation/resolve_sensor_scan.py` y `f06_reference.py` (suites de referencia, que NO escriben Core)
- `desarrollo/integration/f05/include/f05_orders.h` (órdenes y autorización)

La primera integración nativa usa **puntuaciones enteras normalizadas y milésimas de UA** a modo de prueba determinista, sin presentarlas como potencia o alcance canon del universo. El Host debe aportar posición relativa, firma, camuflaje/interferencia y transpondedor provenientes de su World State y de las reglas físicas disponibles.

## P01 — Auditoría y experiencia

El árbol, manual Markdown, protocolos de guardia, contratos y suite de referencia han sido revisados para construir el corte nativo. La revisión visual del manual PDF anterior sigue pendiente y **no puede darse por aprobada por una lectura de texto**.

El objetivo de los diez menús permanece: Estado; Barridos; Búsqueda/localización; Contactos; Seguimiento; Lecturas; Interferencia; Configuración; Resultados; Diagnósticos. La API nativa inicial **no implementa todavía todas las acciones** de esos menús, ni sustituye la interfaz final LCARS que corresponde a F07.

## P02 — Vigilancia

- Tick determinista según tiempo de Core, sin RNG.
- Evaluación de dos alcances pasivos y focalización activa de contacto conocido.
- Identificación solo al alcanzar resolución suficiente.
- Interferencia/rango y pérdidas distinguidas sin atribuir automáticamente destrucción, camuflaje ni salto warp.
- Estado real de matrices, potencia e integridad incorporado como entidad opcional en Core mediante un puerto privilegiado del Host. Una pérdida por matriz sin alimentación se señala como avería conocida, no como anomalía misteriosa.
- No se crea nada cuando no existen firmas en Core.

## P03 — Memoria y catálogo 3D

- Dossiers actuales Core, contactos activos y perdidos; recuperación con ID estable.
- Alertas por adquisición, clasificación, pérdida y recuperación.
- `sistemas/gameplay/ship_operations/consoles/sensors/ship_class_registry.json` fija el vocabulario numérico para vincular clases.
- `ships_visual_catalog.json` conserva los **25 modelos** incluidos en las fichas de metadatos del repositorio, como candidatos NO validados; `build_ship_visual_catalog.py --check <catalog.json>` detecta desajustes.
- Los archivos `.glb` no se han descargado, importado ni subido; ningún modelo está certificado para Unreal.
- **En la PR:** existe una cola real `f06_handoff` de solicitudes a Ciencia en Core; cada solicitud incorpora una instantánea inmutable de los datos observados, prioridad, clase de análisis, emisor F04 autorizado y clave idempotente. Una solicitud en estado `queued` es un hecho persistente, **no** implica que Ciencia la haya aceptado, estudiado o emitido hallazgos. **Pendiente:** registros individuales de observación con procedencia detallada, aceptación/procesamiento por consola Ciencia y correlaciones históricas profundas.

## P04 — Operación y delegación

- F05 revalida las órdenes escaneadas antes de que el motor F06 realice detección activa.
- F06 focal exige ocupación real de Sensores y rechaza un contacto perdido.
- **Implementación nueva:** seguimiento con cupos, zonas de búsqueda, configuración con intercambios de sensibilidad/resolución/compensación, búsqueda por tipo y clase realmente observados, autodiagnósticos y resultados focalizados persistentes y comparables. **Pendiente:** asignación física de potencia, bandas espectrales específicas, cuotas temporales completas y rutinas de separación por secciones. No atribuir autorización a parámetros booleanos suministrados por la UI.

## P05 — Pruebas, rendimiento y cierre

Compilación del incremento, usando el pin verificado de Core de F05:

```sh
cmake -S desarrollo/integration/f06 -B laboratorios/f06/local/build -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR=/ruta/a/CoreRPG
cmake --build laboratorios/f06/local/build --parallel 3
ctest --test-dir laboratorios/f06/local/build -C Release -R '^f06\\.' --no-tests=error --output-on-failure
```

Las pruebas cubren guardia vacía de ocho horas, detección, clasificación parcial sin filtrado de verdad, pérdida inexplicada, recuperación, focalización y puesto, revisión obsoleta, lectura por observador, guardado/carga y avance temporal determinista. CI en Linux y Windows: `.github/workflows/f06-sensors-native.yml`.

**Para cerrar F06** faltará ejecutar/validar los escenarios con Unreal Engine 5.8.2 en el MSI, los diez menús funcionales, transferencias reales y la cobertura de capacidades/recursos propia de la Enterprise-D modernizada. Ningún check de referencia o compilación aislada es certificado de fase completa.

## Cursores y paginación de alertas

Los identificadores y cursores de avisos son opacos; no representan ID de
entidades CoreRPG. Un cursor de aviso desconocido se rechaza. El historial de
avisos conserva el orden y los duplicados de eventos significativos, no cada
barrido periódico. No revelar firmas no detectadas por los paginadores.

## Límites operativos expresos

1. La API `f06_host_signal` es un puerto exclusivo del servicio nativo fiable; no debe estar expuesto como función accesible por jugadores, web, IA ni Blueprints.
2. La geometría de las firmas se expresa por posición relativa al observador; el Host debe resolver movimientos auténticos y llamar al puerto solo cuando cambie la realidad. Todavía no existe simulador orbital completo conectado.
3. La adquisición manual es inmediata en este incremento; duración, colas de recursos, cancelación, fallo de matrices y prioridad avanzada deben integrarse antes de certificar P04.
4. No alterar CoreRPG compartido para resolver reglas específicas de Star Trek.
5. No fusionar una PR con fallos CI, ni utilizar el resultado como base para marcar F06 global CERRADA.

## P04 — Solicitudes de potencia a Operaciones

Sensor cualificado puede registrar peticiones de potencia en WorldState con
clave idempotente, fecha límite y estado. Solo mando efectivo o jefatura de
Operaciones pueden aprobar/rechazar. El reloj Core caduca pendientes. La
aprobación NO modifica potencia material: el Host fiable de Ingeniería/
Operaciones debe aplicar asignación real tras verificar presupuesto energético.
Nunca permitir al operador de Sensores seleccionar subsistema donante.

## Prueba cruzada F05–F06

El escenario nativo `f06.f05_order` ejecuta el flujo completo
emisión → aceptación → ejecución F05 sobre una firma que los sensores pasivos
no podían resolver. Comprueba que solo la ejecución autorizada produce un
contacto observable, sin revelar clase/transpondedor ni duplicar el barrido
en reintentos de una orden terminada.
