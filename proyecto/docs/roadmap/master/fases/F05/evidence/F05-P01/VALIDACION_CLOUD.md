# Validación Cloud F05-P01

Código probado: `855bb6e1eb3a5e225f2279b7bef5bc85c2901dbf`.
[PR Draft #81](https://github.com/robdor80/Videojuego_StarTrek/pull/81).
La descripción de esa PR recoge las conclusiones finales de Actions para el
HEAD publicado; este registro conserva la evidencia local y el corte de CI
conocido al confirmar los documentos. No atribuye éxito a trabajos en curso.

| Prueba | Resultado Cloud | Evidencia |
| --- | --- | --- |
| CoreRPG main completo, con JSON | 483/483 | `core-linux.xml` |
| F02 con su pin original | 15/15 | `f02-linux.xml` |
| F03 con su pin original | 25/25 | `f03-linux.xml` |
| F04 sin opción P01, pin original | 270/270 | `f04-original-linux.xml` |
| F04 + P01 con Core main | 280/280 (261 F04 + 19 P01 del corte previo al test adicional) | `f04-f05-linux.xml` |
| P01 final, fallo de publicación y recuperación entre procesos incluidos | 20/20 | `f05-final-linux.xml` |
| Referencia F05 | 22 unit + 48 fixture; cero fallos | `documentales-linux.txt` |
| Referencias F02/F03/F04 y transversal F04→F05→F06 | 9 + 26 + 22 + 4 + 3 unit; gobierno y sintaxis PASS | `documentales-linux.txt` |

No sumar los XML superpuestos. Las campañas `persistence_baseline_*` de la
suite F04 original son diagnósticos, con límites expresos; no reemplazan la
aceptación de guardias reales de 365/730 días. Esa aceptación se ejecuta en el
workflow histórico F04 contra los seis oráculos congelados.

La compilación usa GCC 14.2.0, CMake 4.4.4, Python 3.12.14, Release C++20.
Las advertencias heredadas de Core no se modifican. No hubo UE ni Blender.
Los datos brutos temporales se guardan en el laboratorio de la tarea; los
archivos de esta carpeta son una copia permanente de evidencia autorizada,
sin dependencia de ejecución desde los temporales.

## Comandos ejecutados

Los directorios `$BUILD_*` representan salidas temporales diferentes, y
`$CORE_*` checkouts limpios de los pins respectivos:

```sh
cmake -S "$CORE_MAIN" -B "$BUILD_CORE" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCORERPG_BUILD_CONTENT_JSON=ON -DBUILD_TESTING=ON
cmake --build "$BUILD_CORE" --parallel 4
ctest --test-dir "$BUILD_CORE" --output-on-failure --output-junit core.xml -j 2

# Repetido para f02, f03 y f04, con sus pins originales:
cmake -S desarrollo/integration/$PHASE -B "$BUILD_PHASE" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR="$CORE_PHASE"
cmake --build "$BUILD_PHASE" --parallel 4
ctest --test-dir "$BUILD_PHASE" --output-on-failure --output-junit phase.xml -j 2

cmake -S desarrollo/integration/f05 -B "$BUILD_P01" -G Ninja -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR="$CORE_MAIN"
cmake --build "$BUILD_P01" --parallel 4
ctest --test-dir "$BUILD_P01" -E 'history_campaign_|persistence_baseline_|persistence_resume_' --no-tests=error --output-on-failure --output-junit f04-f05.xml -j 2
ctest --test-dir "$BUILD_P01" -R '^f05\.' --no-tests=error --output-on-failure --output-junit f05.xml -j 2
```

Se declararon `TMPDIR`, cachés Python y `F04_TEST_TEMP_ROOT` dentro del directorio
temporal permitido. La suite documental se ejecutó con unittest, los fixtures
F04/F05 y `validate_roadmap_state.py`; su salida completa está adjunta.

## Traza real y comprobaciones

`escenario-linux.txt`: capitán 3 → operador 5, petición 25, orden 26, tarea 28,
intento 30, resultado 32, evento final 33. Core devuelve stream **984065**
(`0xF0401`), valor **99**. Se compara contra F04 y contra ActionEngine real,
con igualdad del estado RNG. No se genera un contacto de sensores ficticio.

Las pruebas cubren rechazo de autoridad, cualificación, destinatario/puesto,
operación no soportada, referencias ajenas y acceso indebido; revisión obsoleta,
enfermedad, revocación de nombramiento, plazo, cancelación, transiciones,
duplicados y conflictos sin filtrar recibos ajenos. Comprueban bytes idénticos
al reanudar en otro proceso, recuperación de historial Core y el bloqueo tras
un fallo inyectado después de publicar, seguido de replay sin segundo efecto.

## Incidencias encontradas y corregidas

- La primera comparación directa cargaba sin catálogo: Core la rechazó
  correctamente. La prueba ahora construye un catálogo declarativo independiente.
- La primera selección de historial no declaró `F04_TEST_TEMP_ROOT`; la suite
  rechazó ejecutarse. Los runners local/CI/MSI lo declaran explícitamente.
- Las huellas congeladas detectaron la ampliación de fuente F04. Solo se
  actualizaron las huellas de los dos archivos cambiados, conservando las
  anteriores y exigiendo comparación actual de las seis campañas. No se
  reescribieron oráculos ni acceptance históricos.
- Dos drivers históricos asumían sufijo `.exe`; ahora eligen según plataforma.

Las ejecuciones iniciales rojas permanecen en GitHub, con sus fallos de montaje
y contrato; no son la evidencia de aprobación del código final. Consultar los
checks finales de #81. MSI/UE permanece pendiente según
[VALIDACIONES_PENDIENTES_MSI.md](../../VALIDACIONES_PENDIENTES_MSI.md).

`RESULTADOS.json` fija pins, comandos/resúmenes, huellas de fuentes y evidencia.
**Ninguna PR fusionada. P02–P05 fuera del alcance.**
