# Evidencia A02-01 — 11-11-2026

La promoción nativa está demostrada. La aceptación completa de la regresión
queda **bloqueada por un guard de referencias históricas congeladas**. Esta
entrega no cierra F11, no acredita UE5 jugable y no modifica ESTADO_GLOBAL.

Base Trek: `main` **5c6133b402631459a4e345cb35cf45a8812a5ce5**.
Entorno: Codex Cloud Linux, GNU C++ **14.2.0**, CMake **4.4.4**, Release/C++20.
CoreRPG: checkouts limpios, sin cambios de código ni pins.

| Comprobación ejecutada | Resultado | Evidencia |
|---|---|---|
| F11 C++ sobre Core **76a7b7b485616d8c4994f384a90f123bf333591d** | **PASS 13/13** | Ascenso/expediente, negativas, autoridad, identidad, idempotencia, atomicidad, corrupción, legacy, historial, ABI, dos procesos y puente de producto |
| F04 estable sobre **c147d81ed069da2e09149613ab02cbc3ebe95a4a** | **PASS 270/270** | CTest completo, incluidos diagnósticos monolíticos y procesos de persistencia |
| F05 sobre **76a7b7b485616d8c4994f384a90f123bf333591d** | **PASS 134/134** | P01, P02, P03, P04 y P05-A, todos sus casos CTest |
| F04 dentro del build F05/F11, mismo Core 76a7… | **PASS 271; FAIL 1** | Falla `f04.history_reference_contract`; detalle abajo |
| F11 offline | **PASS 340/340** | `unittest discover`, contrato y referencia; no son mutaciones Core |
| Gobernanza del roadmap | **PASS** | 16 fases/80 pasos, estado sin modificar |
| Lector F04 antiguo ante archivo F11 | **PASS** | Rechaza con `F04_SAVE=14`, sin degradación silenciosa |
| Exportaciones del puente de producto | **PASS** | Solo `f11_commit_promotion`, `f11_personnel`, `f11_promotion`; ningún `f11_test_*` |
| Seis `history_campaign_*` de 365/730 días | **SKIP** | Runner exige el pin independiente **89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98**, incompatible con el build F05/F11 |
| MSVC/DLL, UE5 NullRHI/D3D12, interacción en MSI | **SKIP** | Linux sin `cl`, PowerShell ni UnrealEditor; no ejecutadas |

La ejecución combinada F04/F05 terminó con **405 PASS y 1 FAIL de 406**,
en **437,25 s**. La ejecución F04 estable terminó en **398,09 s**. Las 13
pruebas F11 finales terminaron en **0,24 s**. Estos conteos son por ejecución:
no deben sumarse como casos distintos, pues F04 se prueba con dos pins.

## Qué se ha observado en Core

El escenario se crea mediante un emisor de ensayo compilado, separado del
puente de producto, con antecedentes autorizados de bootstrap. Solo dos
personas concretas reciben identidad y comisión; las restantes siguen legacy.
La prueba positiva prepara además una orden F05 real y compara las relaciones
anteriores/posteriores: solo cambian RANK y el puntero de rango del sujeto,
y se añade un único `trek.f04:promotion`. Identidad, comisión, destino, plaza,
departamento, cualificaciones, contención, turnos, órdenes ajenas, RNG y reloj
se conservan. La orden F05 anterior sigue ejecutándose después del ascenso.
El personaje no obtiene mando de nave y una intención BRIDGE se deniega.

Se rechazan rangos legacy y cero, falta de comisión, evaluación de otro sujeto
o tramo, comisión ajena, orden ajena, caducada o revocada, concesión ausente,
capitán/almirante sin concesión, referencias F05, clave conflictiva, revisión
obsoleta, tick distinto del actual y otros ascensos. Las denegaciones F11
conservan **todos los bytes** del guardado previo, incluyendo revisión y RNG.

Cinco fallos nativos cubren antes de crear el expediente, después del evento,
después de cambiar el grado, después de validar staging y antes del swap. No
se publica nada; cargar el estado previo y reintentar produce un solo ascenso.

Dos procesos CTest distintos guardan/cargan antes y después del ascenso. El
futuro generado desde el guardado previo coincide byte a byte con el futuro
original. Reintentar desde el guardado posterior conserva el mismo evento,
identidad, fecha, grado y revisión original. También pasa con revisión
refrescada, tras revocación de autoridad y después de recuperar una generación
segmentada consolidada ocho días después del efecto legal.

Otro ejecutable enlaza **TrekF04Bridge de producto** y reproduce esos mismos
bytes y recibo; no enlaza la biblioteca del emisor de ensayo. Los fixtures
legacy SCHEMA 1/2 se conservan byte a byte bajo el lector F11.

## FAIL real: referencia histórica congelada

El primer intento del guard carecía de `F04_TEST_TEMP_ROOT`. Repetido con esa
variable y `PYTHONPYCACHEPREFIX` dirigidas al directorio temporal autorizado,
se reproduce el fallo de procedencia:

```text
Incompatible source/contract: desarrollo/integration/f04/src/f04_bridge.cpp;
regenerate and audit reference
Ran 17 tests ... FAILED (failures=5, errors=8)
```

Es **un caso CTest fallido** que agrupa esos 17 checks Python; no se declara
superado. El manifiesto `f04/tests/fixtures/history_reference_v1.json` congela
SHA-256 de `f04_bridge.cpp`, `f04_history.inc` y `f04/CMakeLists.txt`. Las tres
huellas coinciden con `main` previo y cambian con los hooks aditivos F11.
El guard exige reauditar cualquier cambio de esos archivos, aunque sea opt-in.
El comparador nativo de divergencia incluido en el guard sí pasó en el reintento.

Se conservan **intactos** el manifiesto, los oráculos, los archivos de aceptación
anteriores y sus hashes. Actualizar solo las huellas declararía una nueva
compatibilidad sin la auditoría que el propio contrato exige.

**Propuesta para cerrar este bloqueo:** PR de reauditoría histórica Trek,
manteniendo el pin independiente 89a0…, ejecutar las seis campañas 365/730 con
el comparador de originales completos, verificar pasado/futuro y procedencia,
publicar evidencia nueva y versionar las referencias antes de actualizar su
compatibilidad. No requiere alterar Core genérico ni adoptar otro pin para
F05/F11. Hasta entonces este guard permanece FAIL y las seis campañas SKIP.

## Reproducibilidad y límites

Los comandos están en [README.md](README.md). Para incluir los diagnósticos
monolíticos usados en esta ejecución:

```sh
ctest --test-dir "$OUTPUT" --parallel 2 \
  -E '^f11\.|history_campaign_' --output-on-failure
F04_TEST_TEMP_ROOT="$SCRATCH" ctest --test-dir "$OUTPUT" \
  -R '^f04.history_reference_contract$' --output-on-failure
```

Los diagnósticos monolíticos de 365/730 días permiten terminar por CAPACITY:
su PASS demuestra diagnóstico, rechazo atómico y reproducción del checkpoint;
**no demuestra una campaña larga aceptada**.

Los logs y builds son temporales, ignorados por Git y eliminables; ninguna
fuente depende de ellos. El único fallo del harness F11 durante una repetición
fue un destino de historial ya existente; se corrigió usando un destino nuevo
por ejecución, sin borrar resultados previos, y las 13 pruebas volvieron a pasar.

La raíz de confianza sigue siendo el Host nativo y su almacenamiento. La
autenticación de archivos hostiles completos, la emisión institucional de
campaña fuera del escenario de ensayo, la evaluación jugable, la coordinación
entre naves B3 y la comunicación narrativa C/D/E no están acreditadas por estas
pruebas. El evento conserva los datos exigidos por la issue #104, que permanece
abierta. No se ha ejecutado ni construido una interfaz Unreal de promociones.
