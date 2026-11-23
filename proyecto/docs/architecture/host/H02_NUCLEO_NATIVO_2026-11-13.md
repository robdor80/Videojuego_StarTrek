# H02 — Núcleo nativo del HOST

## Alcance

`TrekHost` es una biblioteca compartida C++20. El encabezado `trek/host/session_owner.h` sirve a los módulos C++ internos del HOST. Acepta una configuración de población por valor, devuelve resultados de ciclo de vida y permite consultar estado y generación. La creación usa `f04_create_population` con ABI 1 y conserva las validaciones de F04. `check_active` es una comprobación de vida ligada a una generación. En el hilo propietario llama a `f04_population_stats` y descarta la salida. La sesión y los códigos numéricos de F04 quedan en la implementación. El código original de dominio se registra en el diagnóstico local del proceso si falla una llamada F04.

La reserva atómica se comparte entre todos los gestores de la biblioteca del proceso. Abarca desde el inicio de la adquisición hasta que la destrucción se confirma. Cada gestor tiene un hilo dedicado, un hueco para apertura, uno para cierre y una cola FIFO de hasta 32 comprobaciones pendientes. Las llamadas C++ retornan futuros. El mutex de admisión queda libre mientras F04 trabaja. El destructor bloquea nuevas admisiones, resuelve peticiones y se reúne con el hilo tras completar la limpieza. El propietario ejecuta llamadas síncronas locales, sin callbacks hacia los productores. El consumidor debe conservar la vida del gestor mientras lo invoca.

## Transiciones H02

| Estado | Transiciones permitidas | Admisión y efecto |
|---|---|---|
| `CLOSED` | `OPENING` | Acepta una apertura con argumentos estructuralmente válidos. Cerrar devuelve éxito idempotente. |
| `OPENING` | `ACTIVE`, `FAILED`, `CLOSING` | Una apertura duplicada devuelve `BUSY_STATE`. Si un cierre se admite antes de publicar `ACTIVE`, se cancela la apertura o se destruye la sesión provisional en el propietario. |
| `ACTIVE` | `CLOSING`, `FAILED` | Acepta comprobaciones de la generación activa. Un fallo de la comprobación nativa invalida la generación y retiene la sesión para cierre. |
| `FAILED` | `CLOSED`, `CLOSING` | Si falla la apertura y se limpian sus recursos, vuelve a `CLOSED`. Si queda una sesión, acepta cierre explícito y rechaza nuevas aperturas. |
| `CLOSING` | `CLOSED`, `FAILED` | Las llamadas concurrentes de cierre comparten el resultado. Un fallo de destrucción conserva el puntero y la reserva hasta un cierre posterior. |
| `SAVING`, `LOADING`, `FAILED_RECOVERABLE` | Reservados | Sin entradas alcanzables ni operaciones de persistencia en H02. |

El resto de transiciones está prohibido en H02. El cierre invalida la generación y resuelve las comprobaciones en cola en el momento de admisión. Una comprobación nativa ya iniciada puede terminar, pero su resultado se descarta si entretanto caduca la generación. La destrucción espera a que termine esa llamada. Una generación antigua devuelve `GENERATION_EXPIRED`, incluso tras reabrir o usar otro gestor. El valor vacío devuelve `SESSION_CLOSED` en `CLOSED`, `INVALID_ARGUMENT` en `ACTIVE` y `BUSY_STATE` en los demás estados. La cola llena devuelve `CAPACITY_LIMIT`.

La generación es un valor efímero opaco, emitido únicamente al publicar `ACTIVE`. Un contador común al proceso evita colisiones entre instancias y rechaza nuevas generaciones antes de desbordarse. Los mecanismos de referencia de F04 siguen en F04. Si falla el cierre durante el destructor, se reintenta una vez en el mismo propietario. Un segundo fallo termina el proceso: con la API F04 actual, un puntero vivo en el hilo correcto debe poder destruirse. El destructor de `NativeSession` verifica que el trabajador haya completado la limpieza.

### Decisiones de implementación respecto a H01 v1.0

- La transición de apertura fallida con limpieza completa vuelve automáticamente de `FAILED` a `CLOSED`. H01 dibuja un cierre explícito tras `FAILED`. Aquí se exige cierre explícito solo si la sesión permanece adquirida.
- Las llamadas tipadas son internas. El sobre de mensajes versionado, la correlación de cliente y las operaciones de dominio se concretarán con los despachadores de fases posteriores. H02 verifica la ABI de creación mediante F04 y el SHA del puente cargado antes de adquirir la sesión.
- HC-06 comprueba admisión incompatible en `OPENING` y `CLOSING` mediante inyección de ciclo de vida. `SAVE` durante `LOAD` queda pendiente de H04. El registro H01 v1.0 conserva su definición.

## Compatibilidad y reproducción

- Base Star Trek de la rama `a8604a21fd9f606ecbe48a884bb96698b87dae38`. Incluye H01 por la [PR #112](https://github.com/robdor80/Videojuego_StarTrek/pull/112). La puerta HG-01 se verificó mediante [ruleset activo para main](https://github.com/robdor80/Videojuego_StarTrek/rules/27170774), que exige PR y bloquea borrado y force-push, con lista de bypass vacía.
- CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d`, árbol limpio. H02 reutiliza la composición F05, con `F05_ENABLE_ORDERS=ON`, `F04_ENABLE_HISTORY=ON`, `F11_ENABLE_PROMOTIONS=OFF` y `CORERPG_BUILD_CONTENT_JSON=OFF`. El configure registra los defines heredados del puente, incluido `F04_HISTORY_TESTING`. Los pines históricos se conservan.
- Configurar con `cmake -S desarrollo/integration/host -B <build> -DCORERPG_SOURCE_DIR=<CoreRPG-limpio> -DTREK_HOST_TESTS=ON -DCMAKE_BUILD_TYPE=Release`. Construir con `cmake --build <build> --config Release --target host_native_tests host_fault_tests` y ejecutar `ctest --test-dir <build> -C Release -L h02 --no-tests=error --output-on-failure`. El target de producto es `TrekHost`, con `TREK_HOST_TESTS=OFF` por defecto.
- El workflow H02 publica los SHA, configuración, compilador, JUnit y logs por plataforma. La regresión F11 ejecuta el lector histórico en una compilación independiente. La prueba de frontera H02 inspecciona los símbolos del puente cargado por HOST. La selección de regresiones F05 que escribe historiales requiere una salida nueva por ejecución.

## Evidencia local del 13 de noviembre de 2026

Árbol de código y pruebas `3204d525467898b336fbcc79bb2cfde68e660b71`, CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d`, Windows 11 25H2 x64 (26200.9711), MSVC 19.51.36256.0, SDK 10.0.26100.0, CMake 4.4.3, Python 3.10.11. Generador Visual Studio 18 2026, arquitectura x64, configuración Release. La repetición limpia de CTest reutilizó el checkout limpio de jsoncons en el pin de F05 `bcb44594c50c495ee1e690602cdd71455942ad0e`.

| Comprobación | Resultado local | Evidencia |
|---|---|---|
| H02 con puente real | 9 PASS | `native.xml` y `tests.log` de la ejecución limpia, grupo `host.native` |
| H02 con inyección de ciclo de vida | 6 PASS | Mismo JUnit, grupo `host.fault` |
| F04 con el candidato F05 | 20 PASS | Mismo JUnit, grupo `f04`, población, hilos, scopes, buffers, identidad, clases, determinismo y persistencia entre procesos |
| F05 | 134 PASS | Mismo JUnit, grupo `f05` |
| F11 y lector nativo | 17 PASS | Compilación aislada con el mismo Core, `tests.xml` y `run.json` del ejecutor F11 histórico |
| H01 documental | 11 PASS | `h01.log` |
| AddressSanitizer Windows | 15 PASS | JUnit separado, `/fsanitize=address`, `/INCREMENTAL:NO`, `halt_on_error=1`, sin incidencias ASan |

El primer reintento en un directorio de build reutilizado dejó `f05.p05a_I_process_save` en FAIL por exigir una salida de historial nueva y su caso dependiente en SKIP. La ejecución limpia pasó ambos. MSVC emitió C4805 y C4838 en pruebas históricas F05. En la compilación con ASan avisó de la ausencia de información de depuración completa (C5072 y LNK4302). ASan de Windows no aportó comprobación de fugas. Quedan fuera de esta ejecución local el detector de fugas de Linux, ThreadSanitizer, las campañas históricas largas, los builds en los pines históricos, la persistencia H04 y Unreal. Las comprobaciones de hilos de H02 ejercitan el rechazo propio de F04 y el doble de ciclo de vida registra el hilo de cada llamada.

## Inventario de cambios

| Ruta | Motivo |
|---|---|
| `desarrollo/integration/host/include/trek/host/session_owner.h` | Interfaz C++ interna con configuración, resultados, estados y generación opaca. |
| `desarrollo/integration/host/src/native_session.{h,cpp}` y `src/f04_session_bridge.cpp` | Propiedad exclusiva, verificación del puente, mapeo de errores y adaptación a F04. |
| `desarrollo/integration/host/src/session_owner.cpp` | Hilo propietario, admisión, cola, invalidación y cierre. |
| `desarrollo/integration/host/CMakeLists.txt` | Biblioteca y ensamblaje del puente existente, controles de pin y flags y registro CTest. |
| `desarrollo/integration/host/tests/native_tests.cpp` | Integración con el puente real, concurrencia, reaperturas, apagado y símbolos. |
| `desarrollo/integration/host/tests/fault_tests.cpp` y `test_support.h` | Fallos de ciclo de vida reproducibles y aserciones de apoyo. |
| `.github/workflows/host-h02-native.yml` | CI Windows/Linux, diagnósticos y regresiones. |
| `proyecto/docs/architecture/host/H02_NUCLEO_NATIVO_2026-11-13.md` | Invariantes, transiciones, decisiones de contrato e inventario de auditoría. |
