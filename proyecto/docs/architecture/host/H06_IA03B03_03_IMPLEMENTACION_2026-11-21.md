# HOST H06 · IA-03B03-03 · Persistencia de Academia en H04

Entrega para auditoría B03-04 en
`codex/host-ia03b03-03-persistencia-academy`. La rama parte de `main` en
`91d5759a9c7e242f8870a8ab1539ebe0835f37eb`, con las PR #188 a #191 fusionadas.
CoreRPG se compila desde `76a7b7b485616d8c4994f384a90f123bf333591d`.
La integración sigue el diseño y los oráculos de B03-01.
[PR Draft #192](https://github.com/robdor80/Videojuego_StarTrek/pull/192) · [Arquitectura](H06_IA03B03_01_ARQUITECTURA_VINCULO_PERSISTENCIA_2026-11-20.md) · [Matriz](H06_IA03B03_01_MATRIZ_ACEPTACION_2026-11-20.md)

## Formato de ranura

H04 usa la raíz local autorizada, el mismo `host.lock` y los mismos directorios
`registry`, `campaigns` y `work` de H04. El sobre Academy tiene once líneas
ASCII con terminación LF, tanto en `manifest` como en `prepared` y
`COMMITTED`. El marcador confirmado debe coincidir con el sobre completo.

| Línea | Campo |
| --- | --- |
| 1–2 | `TREKHOST4 2` y `ACADEMY` |
| 3–6 | SHA del pin CoreRPG, campaña de 32 hex, ranura y versión decimal |
| 7 | `startrek.academy:starfleet_academy/v2 2.0.0` y hash SHA-256 del catálogo |
| 8 | `s04_fixed_player_protagonist/2.0.0/s04_player_khan_vulcan_male/1.0.0` y hash SHA-256 combinado de la fuente aprobada por B02 |
| 9 | ID Core de PERSON, ID del hecho `candidate_created`, perfil local opaco y SHA-256 del nombre UTF-8 de B02 |
| 10 | Revisión del WorldState y tick de Timeline del snapshot |
| 11 | SHA-256 de los bytes de `history/CURRENT`, que referencia el manifiesto Core por hash |

El hash del catálogo cubre su identidad y versión, el esquema Core 0.1.0
y el inventario ordenado de IDs y tipos resuelto por el catálogo de producto.
La entrada local `registry/<campaña>` usa `TREKHOST4 ACADEMY REGISTRY 1`,
seguido de la campaña y las líneas 7 a 9. La raíz autorizada es el ámbito
local de confianza. El perfil proviene del vínculo B02/H03 y se recupera
desde ese registro. El cliente aporta campaña, ranura y versión como dirección.
La revisión y el tick de la línea 10 son propiedades de cada snapshot. El
hash del nombre fija el nombre elegido en B02 sin replicar el texto en H04.

`TREKHOST4 1` conserva el sobre de seis líneas y el registro F05 histórico.
Los lectores se seleccionan por formato. En C++ nativo se puede imponer
`CampaignKind::NAVAL` o `CampaignKind::ACADEMY` en `SlotAddress`; el valor
`AUTO` selecciona el lector por el sobre. La ABI C existente mantiene
sus firmas y usa esa selección automática. La inspección informa el formato,
el tipo, la procedencia, la compatibilidad y la recuperabilidad.

## SAVE

El trabajador de `SessionOwner` coteja el sujeto H03 con la PERSON, el hecho,
el nombre y la fuente observados en el Core de la campaña activa. Con una
raíz configurada, SAVE exige un vínculo `BOUND`. La decisión y escritura
se realizan en el hilo propietario.

Una activación creada por B02 usa `HistoryPersistence::migrate` para crear
una foto completa `CRPGROOT` en cada versión hasta que se restaure desde un
archivo. El checkpoint Core incluye el WorldState
real, sus referencias canónicas, RandomStreams y Timeline. B02 crea los hechos
autoritativos de candidatura en ese WorldState. Al volver a guardar una
campaña recuperada, H04 copia su historial validado a la versión nueva y
`HistoryPersistence::publish` extiende la copia. Así conserva segmentos
`CRPGSEG1` y su frontera, junto con el nuevo checkpoint. Cada versión tiene
su propio árbol físico y Core mantiene una representación lógica por hecho.

El escritor reutiliza el bloqueo H04, la reserva de versión, las rutas
ancladas, las cotas de archivos y la comprobación de enlaces y árbol.
Después de generar el historial, se sincronizan sus archivos y el lector
real de Academia reconstruye y valida la foto en una instancia aislada.
H04 sincroniza el sobre y `prepared`, publica `COMMITTED` y confirma
la publicación antes de devolver `OK`. Una publicación cuyo resultado
durable resulte ambiguo devuelve `PUBLICATION_UNCERTAIN`.

## RESTORE

Para Academia se requiere un HOST cerrado. Un HOST con Academia activa
devuelve `BUSY_STATE` si tiene almacenamiento configurado. Un HOST naval
activo conserva la sustitución naval validada de H04 y rechaza la carga de
Academia. Una versión explícita permite seleccionar una partida anterior.
La selección automática se detiene ante corrupción de la última confirmada.

H04 coteja dirección, marcador, registro y resumen de `CURRENT`, y crea
una copia operativa de historial en `work`. Sin constancia local el slot
queda `IMPORTED_UNVERIFIED`. El lector de Academia recrea el catálogo de
producto y pide a CoreRPG que recupere el checkpoint y valide los segmentos.
Busca campus, PERSON y hecho por sus definiciones en el grafo recuperado.
Verifica su unicidad y relaciones, la huella S04, todos los antecedentes
canónicos, el nombre, el tick de creación, la revisión y el reloj. Una
candidatura válida tiene cero plazas. El lector rechaza candidatos adicionales,
entidades profesionales incompatibles y sustituciones por un ordinal igual de
otra campaña.

El propietario coteja ese resultado con el ancla durable del registro y publica
la campaña y el vínculo H03 juntos. La generación H02 usa un punto de partida
aleatorio por proceso y un contador local. El propietario emite una generación
nueva al activar la restauración. Los recibos B02 siguen ligados a sus
activaciones de origen. La PERSON recuperada pasa directamente a `BOUND` y
el gateway de Academia continúa denegando las cinco operaciones navales antes
del puente F05. Un cierre admitido durante la preparación revoca la solicitud
antes de que pueda activar el Core. La ruta naval mantiene sus comprobaciones
F04/F05.

## Inventario

| Archivos | Cambio |
| --- | --- |
| `src/slot_store.{h,cpp}`, `src/f10/academy_identity.h` | Sobre v2, registro Academy, hash de la raíz Core y reutilización del almacenamiento H04. |
| `src/f10/academy_campaign.{h,cpp}`, `src/f10/academy_candidate_factory.h` | Checkpoint, recuperación Core y proyección verificada de Academia. |
| `src/session_owner.cpp`, `include/trek/host/session_owner.h`, `src/f10/academy_player_binding.h` | SAVE/LOAD, tipo de ranura, reconstrucción H03 y generación H02. |
| `src/f04_session_bridge.cpp` | Verificación de que el lector naval recibe su tupla v1 antes de abrir F04. |
| `tests/academy_persistence_tests.cpp`, `tests/academy_persistence_process.py` | Procesos reales, regresión mixta, archivos alterados, evolución autenticada en Core y fallos de publicación. |
| `CMakeLists.txt`, `tests/product_consumer/CMakeLists.txt`, `tests/inspect_product.py`, `.github/workflows/host-h02-native.yml` | Pruebas nativas y consumidor separado de las bibliotecas Release tests-OFF. |

## Matrices y evidencia

| Casos | Evidencia nativa |
| --- | --- |
| B03T-04, 05, 06, 10, 16, 17 y 19; B03-03, 05, 06, 08, 10 y 12 históricos | `host.academy.persistence_process`. Procesos independientes escriben, reanudan, vuelven a guardar y leen una versión anterior. Compara los campos de identidad, la proyección biográfica y el SHA-256 del checkpoint Core completo. Verifica generaciones, recibos caducados, recuperación H03, lista mixta y bloqueo F05. |
| B03T-07, 08, 11, 12, 13, 14, 15 y 22; B03-04, 07 y 11 históricos | `host.academy.persistence_negative`. Corrupción de marcadores y objetos, enlaces, registro ajeno, pin y fuentes incompatibles y archivos Core válidos cuyo grafo es incompatible. Incluye candidato v1 y una definición de admisión sin autorización de dominio. |
| B03T-20 | `host.academy.persistence_advanced`. Una copia de ensayo avanza Timeline a 31, consume un flujo RNG y consolida un hecho Core neutral. El producto reanuda y guarda `alpha/v2`. Se comparan el checkpoint completo, los bytes del segmento y el registro intacto. |
| B03T-09 y 18; B03-09 histórico | `host.academy.persistence_interruptions`. Fallos de snapshot, copia, sincronización y manifiesto, incertidumbre durante publicación o confirmación de `COMMITTED`, salida abrupta, reintentos y cierre durante la preparación de LOAD. |
| B03T-21 y parte de B03T-10/16 | Las reanudaciones nativas conservan la única PERSON y el único hecho. La interacción de introducción se registra como `NOT_RUN` por pertenecer a IA-03C. |

La prueba fundamental arranca un ejecutable consumidor, crea y vincula en
TrekHost y sale después de SAVE. El controlador verifica `COMMITTED` antes
de lanzar otro proceso desde cero. Los casos de alteración y avance usan un
ejecutable separado para construir archivos de control con CoreRPG. El
consumidor que los restaura enlaza la biblioteca de producto.

### Codex Cloud

Código probado en `3544d89eeb18701ae4716dbd6a44c2c7ba9b6f3f` con Linux
x86-64, GCC 14.2.0, CMake 3.31.10 y Ninja.

| Comprobación | Resultado |
| --- | --- |
| Selección nativa Release | PASS 293/293, con 138 HOST, 21 F04 y 134 F05. Incluye las cuatro pruebas multiproceso de esta fase y las regresiones históricas H02, H03, H04, H05 y Academia. |
| F11 aislado | PASS 17/17 con `desarrollo/integration/f11_host/run_native.py`. |
| GCC ASan/UBSan de Academia | PASS 27/27, con detección de fugas y los cuatro recorridos multiproceso. |
| Contratos H01, factory F10 histórico y S04 | PASS 11/11, 9/9 y 12/12, respectivamente. |
| Producto Linux Release con `TREK_HOST_TESTS=OFF` | PASS de carga ABI C 1, inspección de binarios y dependencias, y ciclo multiproceso del consumidor externo `product.academy.process`. |
| Ausencia de llamadas F05 desde Academia | PASS. Una sonda interpuesta interceptó la entrada F05 en un control positivo. La creación, el vínculo, SAVE y la restauración independiente, incluidas las cinco negativas de operación naval, completaron el recorrido sin invocarla. |

En una ejecución local, el nuevo caso de copia se encontró con el binario de
inyección anterior a ese punto y falló. Se recompiló, se conservaron las salidas
previas por separado y se repitió la suite completa. La ejecución final tuvo
cero fallos y cero omisiones.
Los 27 casos de Academia se repitieron con y sin sanitizadores sobre
`31a63d64790e5bef7a238c7b5ef4ab167a925f58`, que acorta la ruta de escritura
de los archivos de ensayo. Ambas selecciones pasaron.

En Linux Release, la campaña `f41b5dc5e418a406219254290a2de009` recuperó la
PERSON `2`, el hecho `3`, la revisión `176` y el mismo checkpoint
`c6196068443dddd4fcd4712621d2da6542a2a3e4de8c5cc02e7423d550a472ec` en
los tres procesos de lectura. Los cuatro procesos usaron generaciones
distintas. En el caso de avance se conservó el segmento Core
`6ebc6a7f6b524923e267d67f30dc69ed6356c8ce7e4b9e0b1bc834c57b95bb06.obj`
y el checkpoint nuevo con tick 31. Las pruebas extraen los IDs del Core de
cada campaña y comparan todos los campos en ejecución.

Para reproducir la selección nativa, compilar los objetivos del workflow
`HOST native H02-H06` con `TREK_HOST_TESTS=ON` y el checkout fijado.

```sh
ctest --test-dir "$build" -C Release --no-tests=error --output-on-failure \
  -R '^(host\.|f05\.|f04\.(history_faults|thread|scope|identity|class|buffers|determinism|population_.*|process_save|process_load)$)'
```

Para reproducir el consumidor, compilar `TrekHost` con `TREK_HOST_TESTS=OFF`
y configurar `desarrollo/integration/host/tests/product_consumer` con
`TREK_HOST_RUNTIME` y, en Windows, `TREK_HOST_LIBRARY`. Ejecutar
`product.academy.process` con CTest desde la compilación del consumidor.

### GitHub Actions

El workflow `HOST native H02-H06` ejecuta Linux y Windows nativos,
F11 aislado, ASan/UBSan y el consumidor multiproceso sobre las bibliotecas
Release de producto. La primera ejecución corresponde a
`662e757a37c7c8b9fdaadc509e4126c053ad4ec0`.
[Matriz de implementación](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44873688459)

| Trabajo | Primera ejecución |
| --- | --- |
| Linux nativo HOST/F04/F05, H01 y F11 aislado | PASS |
| Windows MSVC x64 nativo HOST/F04/F05 | FAIL inicial en el generador del archivo negativo `missing-person`, con 292/293 casos aprobados. |
| H01 y F11 aislado dentro del trabajo Windows | PASS, incluidos 17/17 casos F11. |
| Linux ASan/UBSan, suite HOST | PASS |
| Linux Release tests-OFF, ABI y consumidor Academy multiproceso | PASS |
| Windows x64 Release tests-OFF, ABI y consumidor Academy multiproceso | PASS |
| Workflow H01 de contratos documentales | PASS |

El generador de archivos negativos de la primera ejecución utilizaba una ruta
Win32 ordinaria. El nombre temporal de un objeto Core podía superar 260
caracteres. El ensayo ahora genera esos objetos en una ruta corta de la misma
ejecución y mueve el archivo completo a la ranura antes de probar el lector.
Las verificaciones del HEAD de la Draft incluyen esa corrección y los casos
adicionales de copia, sincronización y corrupción de segmentos.
[Controles de la Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/192/checks) · [H01 inicial](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44873688446)

## Límites

Unreal, MSI, OpenAI LIVE y restauración de un estado legítimamente admitido
figuran `NOT_RUN`. El dominio de esta fase conserva el estado candidato.
Las copias de trabajo y versiones previas siguen la política H04 de retención.
Las garantías durables corresponden a las primitivas confirmadas por el SO
sobre un volumen local autorizado. La auditoría B03-04 y el consumo Unreal
corresponden a las fases siguientes.
