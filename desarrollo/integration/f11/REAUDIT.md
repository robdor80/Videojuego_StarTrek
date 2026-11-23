# Segunda revisión A02-01 — reauditoría auténtica, 11-11-2026

Esta evidencia complementa y supera el bloqueo descrito en `VALIDATION.md`,
que se conserva como registro de la primera entrega. No cierra F11 ni acredita
UE5. El emisor institucional del producto sigue pendiente y fuera del alcance.

Se ha atendido la [revisión técnica de PR #106](https://github.com/robdor80/Videojuego_StarTrek/pull/106#pullrequestreview-5856950219).

## Seis campañas completas, antes de versionar las huellas

Build independiente F04 histórico, **CoreRPG
89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98**, checkout limpio, GNU 14.2.0,
Release. F05 y F11 desactivados en ese build, conforme a sus opciones opt-in.
Los pins del producto y de las fases anteriores no se han alterado.

| Campaña | Días | Bloques comparados | Hechos emitidos reconstruidos | Futuro en proceso nuevo | Resultado |
|---|---:|---:|---:|---:|---|
| Miranda | 365 | 53 | 41.123 | día 372 | PASS |
| Intrepid | 365 | 53 | 47.500 | día 372 | PASS |
| Sovereign | 365 | 53 | 177.697 | día 372 | PASS |
| Odyssey | 365 | 53 | 382.087 | día 372 | PASS |
| Valhalla | 365 | 53 | 433.616 | día 372 | PASS |
| Valhalla | 730 | 105 | 866.849 | día 737 | PASS |

Son **370 bloques y 1.948.872 hechos emitidos**, reconstruidos desde los
segmentos y el checkpoint activo. No son diagnósticos monolíticos que puedan
terminar por CAPACITY. Cada campaña alcanzó su horizonte completo, comparó
todos los bloques de serialización canónica con el oráculo anterior, verificó
el esquema global al terminar y después del futuro, recuperó el checkpoint
y reprodujo el futuro en otro proceso. El auditor independiente reconstruyó
todos los payloads originales, incluidos campos y vínculos causales, y comparó
sus hashes de bytes completos. También se mantuvo la identidad estática durante
cada bloque. Las duraciones individuales fueron 14,49; 17,10; 103,82; 256,16;
315,79 y 675,34 segundos, respectivamente.

La evidencia permanente está en
[`F11-P05-A02-01-REAUDIT`](../../../proyecto/docs/roadmap/master/fases/F11/evidence/F11-P05-A02-01-REAUDIT):
`transition.json`, entorno de compilación y, por campaña, logs de ejecución,
recuperación y auditoría, resultado estructurado y metadata nativa del futuro.
Los directorios de generación Core permanecen temporales; no son dependencias
de los lectores ni de los tests definitivos.

## Procedimiento y nueva protección

`f04/tests/reaudit_history.py` reconstruyó desde Git el contrato anterior en
`5c6133b402631459a4e345cb35cf45a8812a5ce5`. Antes de ejecutar el candidato:

1. Verificó el manifiesto v1, sus fuentes congeladas, procedencia, seis oráculos
   y seis acceptance con el verificador estricto original.
2. Limitó las diferencias candidatas a `f04_bridge.cpp`, `f04_history.inc` y
   `f04/CMakeLists.txt`, sin modificar las huellas publicadas.
3. Ejecutó los tres programas nativos de campaña, continuación y auditoría.
4. Revalidó al finalizar las fuentes, los binarios ejecutados y las evidencias
   anteriores para detectar cambios durante el ensayo.

Solo tras finalizar **las seis** campañas se emitió el registro de transición
y se creó `history_reference_v2.json`. El archivo v1, los oráculos, acceptance
y procedencias anteriores se conservan byte a byte. V2 mantiene el formato
JSON schema 1 y declara explícitamente `manifest_version=2`.

El guard normal ahora utiliza v2 y mantiene la comparación estricta de fuentes,
pins, hashes de oráculos y procedencia. Además valida el enlace entre las nuevas
huellas y la evidencia completa de transición: seis campañas distintas, bloques,
payloads, logs y digest congelado del futuro. No existe opción CLI de omitir el
guard. La API interna permite verificar v1 solo con sus propias fuentes exactas;
el candidato actual sigue siendo rechazado contra las huellas v1.

`history_reference_contract` vuelve a PASS con **22 checks**, incluidos cinco
casos nuevos que rechazan transición ausente, campaña omitida, protección
desactivada, fuentes diferentes o futuro falsificado, incluso si alguien vuelve
a calcular el hash del informe alterado. Las nuevas evidencias tienen política
de bytes sin conversión de finales de línea, y los manifiestos conservan LF en
Linux y Windows.

## Revocación en el instante exacto

Las 13 pruebas nativas F11 pasan en Linux con Core
**76a7b7b485616d8c4994f384a90f123bf333591d**. El caso `f11.authority` ahora
revoca por separado concesión y orden en los ticks **0, 1 y 99**, y llama a
la promoción en ese mismo tick, sin avance de reloj. Comprueba el tick guardado
de revocación, la denegación inmediata y la ausencia de cambios parciales,
también después de guardar/cargar. El tick 99 es el último anterior al fin
exclusivo 100 de las ventanas del escenario.

También prueba el orden inverso: commit y revocación en el mismo tick 99.
El replay devuelve el hecho anterior sin cambios; la concesión revocada no
permite ascender al segundo candidato aún alférez. Revocar una orden individual
no revoca la orden distinta del otro oficial.

No fue necesario cambiar la autorización: `window()` exige `STATE=ACTIVE`
en la ejecución y de nuevo al confirmar. El predicado inclusivo
`f11_history_live_at()` solo reconstruye legalidad histórica; permite conservar
un commit que ocurrió antes de revocar dentro del mismo tick. Nunca autoriza
una promoción nueva. Esto se documenta en el código y se prueba explícitamente.

## CI nativa F11

El workflow `f11-native-promotions.yml` ejecuta Linux y Windows con el mismo
pin F05/F11. `run_native.py` exige exactamente los **13 casos distintos**, sin
SKIP, y en Windows comprueba `CMAKE_CXX_COMPILER_ID=MSVC`. Conserva compilador,
logs, JUnit, recibo de ensayo y guardados antes/después como artifacts.

La prueba del puente de producto ahora inspecciona el módulo realmente cargado
con `dlsym` o `GetProcAddress`: exige la operación de promoción y rechaza las
exportaciones de bootstrap, revocación e inyección de fallos de ensayo. Luego
ejecuta promoción, carga y replay contra ese puente de producto.

La ejecución [43003893957](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43003893957)
ha terminado con **SUCCESS** en ambas plataformas sobre el commit de
implementación **1d26889fe5ea5b3390f7ba129c1fb7441c8881e8**:

| Validación terminada | Resultado |
|---|---|
| [F11 Linux/GNU](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43003893957/job/130466472304) | PASS 13/13 |
| [F11 Windows/MSVC](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43003893957/job/130466472326) | PASS 13/13 |
| F04 histórico local, selección de regresión compatible | PASS 261/261 |
| F04/F05 local, selección completa recomendada por F05 | PASS 395/395 |
| F11 offline local | PASS 340/340 |
| Gobernanza local | PASS |

Los logs reales de los jobs confirman respectivamente
`{"result": "PASS", "tests": 13, "compiler": "GNU"}` y
`{"result": "PASS", "tests": 13, "compiler": "MSVC"}`. No son éxitos inferidos
de las pruebas F05: son los 13 casos F11, incluidos puente de producto y
persistencia. Los IDs y el commit están en `CI_EVIDENCE.json`; los artifacts
contienen JUnit, versión del compilador, logs y los guardados de ambos procesos.

La primera repetición local F05 intentó reutilizar un destino previo y su guard
la rechazó con `fresh history output required`. Se conservaron esos resultados
y se ejecutó de nuevo la suite completa en un destino nuevo: **395/395 PASS**.
El guard de referencias también pasó dentro de esta nueva ejecución.

## Reproducir

Usar directorios nuevos dentro del destino temporal autorizado del encargo.
`OUTPUT`, `AUDIT`, `CORE_SOURCE` y `SCRATCH` son rutas suministradas por el Host;
el repo debe conservar el objeto Git de la revisión base indicada arriba.

```sh
cmake -S desarrollo/integration/f04 -B "$OUTPUT" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR="$CORE_SOURCE" -DF04_ENABLE_HISTORY=ON
cmake --build "$OUTPUT" --target f04_history_campaign f04_history_audit --parallel 3
python desarrollo/integration/f04/tests/reaudit_history.py --bin "$OUTPUT" \
  --core-source "$CORE_SOURCE" --output "$AUDIT" --jobs 2
F04_TEST_TEMP_ROOT="$SCRATCH" ctest --test-dir "$OUTPUT" \
  -R '^f04.history_reference_contract$' --output-on-failure
```

Para F11 utilizar otro checkout limpio del pin 76a7… y un OUTPUT nuevo:

```sh
python desarrollo/integration/f11/run_native.py \
  --core-source "$CORE_SOURCE" --output "$OUTPUT" --parallel 3
```

MSVC se valida mediante GitHub Actions. Unreal, NullRHI/D3D12 e interacción MSI
siguen fuera del alcance y no se declaran ejecutados.
