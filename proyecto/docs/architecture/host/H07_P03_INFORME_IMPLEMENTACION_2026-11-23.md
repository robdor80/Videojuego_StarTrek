# H07-P03 — Implementación y evidencias de consulta institucional

**Base de trabajo** · PR #203, abierta al iniciar la implementación, en
`94fbd7f593ec3d7d753b753a1200deef40a5f683`. La PR de H07-P03 se apila sobre
esa rama. **CoreRPG** · `76a7b7b485616d8c4994f384a90f123bf333591d`.
[PR #203](https://github.com/robdor80/Videojuego_StarTrek/pull/203)

## Implementación

`SessionOwner` ejecuta las consultas por su cola y el hilo propietario.
`NativeSession` selecciona la sesión naval y el puente comprueba el vínculo
F05 persistido antes de delegar en `trek::f11_host::career` y
`trek::f11_host::promotion`. La vista privada v1 proyecta el rango y el estado
de servicio o el evento de ascenso confirmado. H04 verifica la continuidad
local de la partida para este flujo. La ruta de emisión previamente admitida
sigue devolviendo `SERVICE_UNAVAILABLE`. [Contrato privado v1](H07_P03_CONTRATO_CONSULTA_v1_2026-11-23.md)

## Composición

- `TREK_HOST_F11_READS` selecciona el lector privado y está activo por defecto.
  La opción `OFF` conserva el puente F05/H04 previo y devuelve
  `SERVICE_UNAVAILABLE` en consultas institucionales admitidas.
- HOST conserva la comprobación de composición F05 y sustituye la única
  unidad de traducción de `TrekF04Bridge` por `f04_host_bridge.cpp`. El
  selector privado `F11_HOST_READ_ONLY` activa allí el vocabulario y la
  validación de archivos de F11. Sus guardas de preprocesador excluyen
  `f11_commit_promotion`, sus funciones de escritura y
  `F11_NATIVE_TEST_HOST`. El ensamblaje conserva una sola sesión F04 y un solo
  Core en el puente.
- HOST compila directamente la unidad existente `f11_host_reader.cpp`. Los
  proyectos CMake independientes de F11 y del lector quedan fuera de su
  grafo. El productor de fixtures se ejecuta en el proceso separado de la
  regresión F11 y entrega el archivo Core confirmado y sus metadatos de prueba.
- La inspección de producto comprueba el pin cargado, los símbolos y
  dependencias de HOST y del puente, y las definiciones efectivas de
  `TrekF04Bridge`. `inspect_abi.py` y los consumidores existentes comprueban
  la ABI C publicada.

## Pruebas y trazabilidad

| Cobertura | Comprobación |
| --- | --- |
| H07-07, H07-08 | Producto Release con `TREK_HOST_TESTS=OFF`, inspección de símbolos, dependencias y ABI |
| H07-09, H07-10 | `career`, `promotion` contrastan los campos con las consultas F11 de Core y la revisión original del fixture |
| H07-11, H07-12, H07-16 | `foreign`, `scope` y los casos negativos verifican respuesta vacía y correlación |
| H07-13, H07-14 | `uncommissioned`, `academy` y `capability`, incluida la composición opcional sin lector |
| H07-15 | `repeated` compara bytes Core completos y comprueba el rechazo de emisión en la partida comisionada |
| H07-17, H07-18 | `closed`, `save`, `restore` cubren operaciones en vuelo, estados ocupados, invalidación, continuidad y proceso nuevo |
| H07-19 | `import` comprueba el rechazo de un guardado con datos F11 copiado fuera de su registro local H04 |

El fixture usa la salida de `f11.process_save` de la suite existente. El
ascenso ya está confirmado cuando el ejecutable H07 abre el archivo. El
ejecutable enlaza el puente de lectura y usa un acceso exclusivo de pruebas
para cargar esos bytes antes de vincular al jugador mediante H03/F05. Todas las
consultas y el guardado y restauración se realizan por las rutas nativas
habituales.

Evidencia Cloud en Linux/GCC Release en la primera ejecución completa de P03
local, antes de CI. Los 12 casos nuevos de CTest pasaron, la suite independiente
del lector F11 pasó 17 de 17 y las comprobaciones documentales H07, F11 y H01
pasaron 8 de 8, 15 de 15 y 11 de 11. Los registros locales incluyen el XML
`gcc-h07.xml`, `f11/run.json` y el log de CTest de cada ejecución. La PR
asociada conserva los resultados de GitHub Actions por SHA. [Ejecuciones de la rama](https://github.com/robdor80/Videojuego_StarTrek/actions?query=branch%3Afeat%2Fhost-h07-p03)

Para reproducir la suite, usar el Core limpio en el pin y una carpeta temporal
autorizada por `AGENTS.md` como `LAB`. El prefijo apunta a archivos de fixture
generados fuera de la compilación de HOST.

```sh
python3 desarrollo/integration/f11_host/run_native.py \
  --core-source "$CORE" --output "$LAB/f11"
export TREK_HOST_H07_FIXTURE="$LAB/f11/build/f11/process"
cmake -S desarrollo/integration/host -B "$LAB/host" \
  -DCORERPG_SOURCE_DIR="$CORE" -DTREK_HOST_TESTS=ON -DCMAKE_BUILD_TYPE=Release
cmake --build "$LAB/host" --config Release --target host_h07_query_tests
ctest --test-dir "$LAB/host" -C Release -R '^host\.h07\.p03\.' --no-tests=error --output-on-failure
```

## Riesgos y límites

La regla de esquema F11 vigente sigue validando el marcador histórico de la
raíz de ensayo al cargar ese formato. La admisión de HOST usa en cambio la
procedencia H04, el vínculo y el ámbito activo. La comprobación está acotada al
modelo de confianza local de H04. El emisor de producto sigue siendo una
dependencia de F11 para obtener comisiones nuevas en el juego y para revisar
cualquier evolución de su esquema. Las pruebas positivas utilizan el fixture
aislado de F11 precisamente por esa dependencia.

Los resultados de esta entrega cubren la lectura nativa y sus regresiones.
El consumo en Unreal, la aceptación de H07-P05 y la certificación integral
corresponden a sus fases de revisión. La matriz H07-P04 conserva su estado de
plan de aceptación.
