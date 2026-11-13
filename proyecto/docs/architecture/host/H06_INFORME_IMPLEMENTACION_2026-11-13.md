# H06 — Implementación del adaptador HOST para Unreal

Fecha: 2026-11-13. Rama `feature/host-h06-ue-m1`. Base `5f12d9c152dd0003a6d971068d693184f45b213e` (PR #141). Código `2b68bd16a6200a86b43d5b66d535e97a28c4eb9d`. Configuración CI final `517b5adcb8d99a93dfa7ce81c698a74abfd5d6e2`. CoreRPG limpio y fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`. [PR #142 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/142).

**M1 parcial y bloqueado.** Está implementado el adaptador nativo; quedan pendientes el proyecto Unreal autorizado, su módulo y panel, el bootstrap productivo del cadete y la validación UE. [Decisión G0](H06_DECISION_PROYECTO_UE_2026-11-13.md) · [Resultados y matriz](H06_RESULTADOS_2026-11-13.md).

## Cambios

| Archivo | Cambio |
|---|---|
| `desarrollo/integration/host/include/trek/host/host_abi.h` | Contrato C v1, funciones `trek_host_*`, entrada/salida trivial, generaciones y tickets. |
| `src/host_abi.cpp` | Traducción de solicitudes y errores, poll y proyecciones mínimas dentro de TrekHost. |
| `src/abi_admission.h`, `src/session_owner.cpp`, `include/trek/host/session_owner.h` | Admisión inmediata sobre el mismo mutex recursivo; lectura interna de generación e ID H04 bajo guardia. El trabajador conserva su cola, estados y transiciones. |
| `CMakeLists.txt` de HOST | Compila el consumidor C11 y mantiene una sola composición Core/F04. OFF excluye dos exportaciones de ensayo heredadas de F04. |
| `tests/host_abi_tests.c`, `tests/abi_fixture.py`, `tests/inspect_abi.py` | CTest de producto y fixture H04/F05, negociación y carga del producto OFF. |
| `.github/workflows/host-h02-native.yml` | Incorpora consumidor C, sanitizadores C/C++, inspección de ABI en Release OFF y artefactos H06. |
| Tres informes H06 en `proyecto/docs/architecture/host/` | Decisión reservada, arquitectura, ejecución y trazabilidad. |

El pin, fuentes Core/F04/F05/F11, guardado H04 y oráculos históricos conservan su implementación. Ningún descriptor, mapa, asset o fuente Unreal cambió.

## ABI real

- `trek_host_abi_version` y `trek_host_create` negocian versión 1. Los tamaños exactos en x64 con alineación por defecto son 16 bytes para `TrekHostText`, 80 para la solicitud, 24 para el estado y 120 para el resultado. Se comprueban en C y C++. Los números públicos tienen ancho fijo. Win64 usa C linkage y `__cdecl`. La biblioteca controla la vida del handle; el llamador posee buffers de entrada y salida. Las cadenas con longitud se copian en la llamada. Excepciones y objetos STL se confinan a TrekHost.
- `trek_host_status` copia estado H02, generación y estado de identidad H03. La capacidad institucional publica `SERVICE_UNAVAILABLE`. Los diagnósticos crudos de dominio, paths y referencias Core quedan en nativo. El C ABI deja fuera el bootstrap, la ejecución por destinatario, las mutaciones institucionales y cualquier identidad seleccionada por cliente. Los exports C++ históricos siguen siendo internos y el futuro módulo UE solo usará el header C.
- `trek_host_submit` admite OPEN, CLOSE, QUERY_VIEW, SUBMIT_SCAN, QUERY_ORDER, CANCEL_ORDER, SAVE y RESTORE. Distingue el resultado de transporte del de dominio. El ticket es de entrega y correlación; F05 conserva su key de idempotencia. SUBMIT_SCAN traduce una intención tipada a F04_SCAN. F05 decide revisión, autoridad, estación, destinatario y plazo. Los resultados de dominio se traducen explícitamente. La proyección C de consulta incluye los datos mínimos de campaña y orden, con resultado de tirada si existe.
- `trek_host_poll` consulta el futuro a cero espera y consume el resultado una vez. Hasta ocho observaciones simultáneas y una ranura reservada para CLOSE. `trek_host_discard` libera la observación; una intención ya admitida sigue su curso en el trabajador. La adquisición del mutex con `try_lock` devuelve `RETRY` cuando está ocupado. El adaptador serializa admisión y validación de generación usando el mismo mutex de SessionOwner. Las llamadas sobre el mismo cliente se serializan por contrato del llamador. La capa C no programa tareas Core ni crea otro trabajador.
- La comparación de generación se hace en admisión y en poll. Un resultado pendiente de entrega, aunque el trabajador ya lo haya producido, devuelve `GENERATION_EXPIRED` si un CLOSE o un LOAD válido revocó su generación. El consumidor debe revalidar el resultado entregado si se difiere su aplicación. El descarte de un resultado no implica rollback de una operación que Core o H04 ya confirmó.
- `trek_host_destroy` libera el handle y hace join del trabajador nativo. Se deben detener las llamadas del consumidor y ejecutar el join fuera del Game Thread. Conservar ambas DLL hasta que terminen las destrucciones; el futuro módulo debe administrar también el orden de descarga.

## Composición Unreal pendiente de G0

```text
Game Thread: GameInstanceSubsystem -> handle C -> poll acotado por tick
                |                                  |
      UWorld A / UWorld B: vistas débiles      TrekHost -> SessionOwner
                                                      -> único trabajador Core
```

Un handle por GameInstance. Las proyecciones por UWorld se identifican por mundo y generación; comprobar weak references en Game Thread justo antes de aplicar cada resultado. Durante world cleanup y map travel se desregistran las proyecciones/tickets de ese mundo, y el nuevo mapa se suscribe a la sesión del mismo GameInstance. Tras LOAD/CLOSE se invalidan también las proyecciones de generación anterior. En Deinitialize se dejan de recibir resultados, se invalida el contexto UE y se transfiere el handle para destrucción fuera de Game Thread. El dueño del módulo retiene las DLL durante ese drenaje. El consumidor C ya comprueba exclusividad nativa; la vida real de UWorld y UObject requiere automatización UE.

Propuesta de staging Win64 tras G0: Build.cs con include público C, import lib `TrekHost.lib`, carga controlada de `TrekF04Bridge.dll` y `TrekHost.dll` y `RuntimeDependencies` relativas a proyecto o módulo. `TrekF04Bridge` sigue siendo dependencia privada; ningún consumidor Unreal enlaza Core directamente. Verificar el CRT del producto, carga desde staging y juego cocinado en equipo limpio. El build nativo usa la misma biblioteca para el C ABI, preserva la ABI C++ histórica para consumidores nativos y aísla de ella a Unreal. UBT/UHT y la ruta de empaquetado quedan sin validar.

## Identidad y guardado

OPEN técnico crea una población F04 sin vincular un cadete. El estado `PRINCIPAL_UNBOUND` permite diagnosticar y cerrar; las consultas privadas, órdenes y SAVE conservan las precondiciones de H03/H04/H05. RESTORE usa dirección de campaña/ranura y raíz privada autorizada por la aplicación. H04 valida registro, compatibilidad, ruta y vínculo persistido; la ABI copia la identidad únicamente cuando la pasarela la autoriza. La raíz de almacenamiento procede de configuración privada y H03 resuelve la identidad. La decisión para el futuro panel es mostrar OPEN/CLOSE, estado de identidad, capacidades, errores y vistas autorizadas, con SAVE/RESTORE sujetos a H04 y SUBMIT solo con vínculo y competencia real. El capitán de ensayo se vincula exclusivamente al preparar un fixture en otro proceso.

## Puertas

| Puerta | Estado |
|---|---|
| G0 | Inventario y propuesta entregados. Bloqueada por aprobación de proyecto principal. |
| G1 | ABI C y carga Release OFF en alcance nativo. Compatibilidad UBT y staging UE pendientes de G0. |
| G2 | Tickets, capacidad, exclusividad y revocación verificados en nativo. Integración GameInstance/UWorld pendiente de G0. |
| G3 | Denegación unbound y recuperación de vínculo H04 verificadas en nativo. UI y bootstrap productivo del cadete pendientes. |
| G4 | H04/F05 ejercitados con Core fijado y fixture identificado. F11 permanece SERVICE_UNAVAILABLE. Falta ejecución de editor/juego. |

## Disco y laboratorios

La raíz de trabajo fue el checkout exigido por AGENTS, `C:/Users/andro/Documents/GitHub/Videojuego_StarTrek`. Se partió de `origin/main` en una rama nueva, desde el checkout limpio de la rama H03. Se reutilizaron el motor instalado, el checkout limpio existente de CoreRPG y la misma descarga jsoncons para los builds locales. El build OFF es independiente para comprobar el grafo de producto. Las regresiones Windows/Linux y ASan se ejecutaron en runners desechables de Actions.

Medición inicial en bytes lógicos: `laboratorios/` 111 120 157 391, H06 inexistente, C: 337 702 273 024 bytes libres. Las cinco carpetas mayores fueron `valhalla` (81 116 120 197), `f05` (16 346 639 383), `Enterprise_G` (8 450 867 006), `F04` (1 845 442 528) y `galaxia` (1 216 505 407).

Medición al cierre de las pruebas: `laboratorios/` 111 545 966 751 bytes lógicos, C: 335 436 910 592 bytes libres. H06 ocupa 400 576 052 bytes en 6 227 archivos, incluidos 360 680 772 bytes del build nativo y sus ensayos y 34 362 836 bytes del build Release OFF. El total del volumen también refleja actividad ajena a H06; el tamaño propio se midió directamente.

`laboratorios/host/h06/` contiene builds, logs, JUnit, guardados de ensayo y temporales. Está ignorada y es eliminable en bloque tras conservar las evidencias deseadas. Los builds se regeneran desde Git y Core, con el destino temporal a elección del operador. Se conservaron laboratorios previos y originales. La evidencia permanente de las ejecuciones se enlaza en el informe de resultados.
