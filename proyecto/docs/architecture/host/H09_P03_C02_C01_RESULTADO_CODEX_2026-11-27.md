# HOST H09-P03-C02 — Ubicación, carta conocida y propuesta de ruta

**Fecha** 27 de noviembre de 2026. **Base** `main` en `9c8ee562eadce391f09866ca6020f3dcd91d72de`, tras la fusión de la PR #233. **Código funcional probado** `12f36f91bb7b1682dcc876c79b63972e9427bca3`. **Composición aislada** `90f1f7ddea0a45a0025218cc13397d258a75cecd`. **CoreRPG** `76a7b7b485616d8c4994f384a90f123bf333591d`.

## Capacidad nativa

- `SessionOwner::open_naval` recibe un `NavalBootstrap` de autoría de confianza. La identidad de la nave se resuelve con `f04_handles`. F04 registra un lugar tipado y la contención nave→lugar en el mismo `WorldState`. `open` y el arranque por ABI C conservan el origen desconocido. La campaña normal necesita que su autor suministre explícitamente el origen, la versión de carta y los permisos de sus observadores.
- El catálogo de referencia se compila a partir de `anchor_route_graph.json`, `initial_reference_distance_edges.json`, `anchor_locations.json` y `route_cost_model.json`. El arranque debe seleccionar el identificador exacto de publicación. La campaña conserva el sello SHA-256, los registros de carta, lugares y aristas, y los permisos por tripulante en Core. Se puede publicar una carta sin determinar el origen físico.
- `query_navigation` comprueba el H03/F05 vinculado y la membresía F04 en el hilo dueño. `Visibility::project` y los permisos vigentes determinan cada dato visible. La memoria del lugar y la del hecho de estar allí son comprobaciones distintas. Una arista requiere permiso, memoria y ambos extremos visibles. El embarque posterior no recupera permisos revocados en una baja. La vista lleva referencias de autoría visibles y omite dependencias de lugares, fuentes de sensores y estado político.
- `propose_route` compara el vector de revisión y resuelve un ID exacto o un nombre visible. Los homónimos se devuelven como candidatos visibles. Para los cinco perfiles de autoría, la búsqueda pondera saltos y la incertidumbre documentada de los tramos. La respuesta indica que faltan datos para optimizar tiempo, peligros, exposición y apoyo. Los tramos conservan procedencia, confianza y relación de distancia. El total se calcula únicamente con estimaciones puntuales publicadas en todos los tramos. La ETA queda nula porque faltan costes de propulsión. Se excluye la travesía especial por el agujero de gusano.
- `validate_route` vuelve a comprobar el observador, la generación y el contexto actual. Posición y conocimiento usan la revisión global del Core fijado. Las referencias caducan al cambiar esa revisión, la carta o el tick Core, o al tramitar SAVE, RESTORE o CLOSE. El HOST conserva hasta 64 referencias recientes de la activación en memoria. Cualquier uso posterior depende de una revalidación, y la propuesta carece de autoridad para emitir una orden.

La costura de persistencia usa el formato Core existente. El catálogo F04 admite las definiciones adicionales solo en la composición HOST. `schema` comprueba tipos, cardinalidad, contención, sello y concesiones, y el esquema de conocimiento de F05 acepta únicamente los hechos navales respaldados por dichas concesiones. `HistoryPersistence` verifica el archivo y restaura en una campaña candidata antes del intercambio. La composición naval no registra acciones de navegación en Timeline ni añade un reloj.

La primera ejecución de Actions detectó una dependencia de compilación. Los workflows históricos F04 y F05 validan el hash exacto de `f04_bridge.cpp` antes de ejecutar sus campañas. C02 devuelve ese archivo a los bytes de `main` y aplica la extensión solo a una copia generada para HOST. `compose_f04_bridge.py` aplica un parche contextual a un candidato temporal y publica la copia únicamente si el parche encaja. El resultado coincide byte por byte con la unidad previamente probada, y las otras composiciones siguen compilando el original con sus oráculos intactos. [Primera ejecución F04](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/46037794609)

## Compatibilidad de guardados

| Caso | Resultado |
| --- | --- |
| Guardado anterior a C02 | Se restaura con ubicación y carta desconocidas. |
| Campaña nueva sin origen aprobado | Ubicación nula. Una carta publicada y visible sigue consultable. |
| Campaña con ubicación y carta explícitas | Se recuperan el lugar Core y la proyección autorizada de la carta, con una generación nueva. |
| Carta retirada al observador | Su carta deja de mostrarse, la propuesta caduca y la revocación se conserva al restaurar. |
| Revisión de publicación distinta o sello inválido | El arranque rechaza una publicación desconocida. RESTORE rechaza atómicamente un archivo que reclama una publicación incompatible. Para distribuir una revisión nueva y seguir leyendo las partidas C02, el producto deberá conservar la definición versionada que se guardó. |
| Observador ajeno o que salió de la tripulación | La vista queda limitada a sus propios permisos o se deniega si perdió la membresía. |

## Pruebas nativas

| Caso | Resultado local y evidencia |
| --- | --- |
| CN2-01 | **PASS**. Guardado sin dominio naval y campaña con carta explícita sin origen conservan ubicación nula. |
| CN2-02 | **PASS**. Lugar explícito en contención Core. Lectura autorizada sin carta y recuperación desde HistoryPersistence. |
| CN2-03 | **PASS**. Publicación versionada, subconjunto conocido y arista filtrada por su extremo oculto. Recuperación del subconjunto. |
| CN2-04 | **PASS**. Aislamiento de dos observadores, revocación Core persistente, baja de tripulación y validación obsoleta. |
| CN2-05 | **PASS**. El resolvedor nativo desambigua un homónimo introducido solo en una proyección de prueba. La carta publicada carece de homónimos en sus nombres actuales. |
| CN2-06 | **PASS**. Destino oculto e inexistente devuelven el mismo estado y ninguna proyección. |
| CN2-07 | **PASS**. Los cinco perfiles aceptados, perfil inválido rechazado y ruta de dos tramos conocidos. |
| CN2-08 | **PASS**. Destino visible sin conexión autorizada y travesía especial excluida de la búsqueda ordinaria. |
| CN2-09 | **PASS**. Distancia, Z y ETA conservan nulos cuando faltan datos. |
| CN2-10 | **PASS**. Bytes canónicos Core idénticos tras lectura, propuesta, revalidación y rechazo. |
| CN2-11 | **PASS**. Publicación desconocida y revisión distinta rechazadas. Avanzar el reloj Core invalida la referencia. |
| CN2-12 | **PASS**. SAVE, RESTORE y CLOSE retiran referencias. El arranque de otra nave y otro observador no admite la referencia anterior. |
| CN2-13 | **PASS**. Se rechazan un snapshot Core válido con sello de carta incompleto y un archivo HistoryPersistence dañado. Ambos conservan la campaña activa. El snapshot sano recupera bytes canónicos idénticos. |
| CN2-14 | **PASS**. El principal sin vínculo no obtiene la vista. Una propuesta mantiene lugar, revisión, tick y bytes canónicos. |

**Relación con P03.** CN2 aporta evidencia de N3-01 a N3-06 y N3-10, y de la parte de propuestas de N3-12 y N3-14. N3-07 requiere una fuente de advertencias fronterizas autorizadas en campaña. N3-08 y N3-09 quedan pendientes del contrato de entrega y del receptor autorizado de S11/CONN. N3-11, N3-13 y las partes de órdenes de N3-12/N3-14 pertenecen a la autorización y ejecución de CONN. El diseño histórico y sus pruebas documentales conservan su estado original.

## Reproducción y regresiones

Entorno Debian 13 x86-64, GCC 14.2.0, CMake 4.4.5, Ninja 1.13.2, Python 3.12.14, Git 2.52.0 y libcurl 8.14.1. Usar directorios de salida y temporales aislados conforme a `AGENTS.md`. `$core` es un checkout limpio del pin indicado.

```sh
cmake -S desarrollo/integration/host -B "$host_build" -G Ninja \
  -DTREK_HOST_TESTS=ON -DCORERPG_SOURCE_DIR="$core" -DCMAKE_BUILD_TYPE=Release
cmake --build "$host_build" -j 3 --target host_navigation_tests
ctest --test-dir "$host_build" -j 3 --no-tests=error --output-on-failure -R '^host\.navigation\.'

python3 desarrollo/integration/f11_host/run_native.py --core-source "$core" --output "$f11_build" --parallel 2
cmake --build "$host_build" -j 3
TREK_HOST_H07_FIXTURE="$f11_build/build/f11/process" \
  ctest --test-dir "$host_build" -j 3 --no-tests=error --output-on-failure \
  -R '^(host\.|f05\.|f04\.(history_faults|thread|scope|identity|class|buffers|determinism|population_.*|process_save|process_load)$)'

cmake -S "$core" -B "$core_build" -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_TESTING=ON -DCORERPG_BUILD_CONTENT_JSON=ON
cmake --build "$core_build" -j 3
ctest --test-dir "$core_build" -j 3 --no-tests=error --output-on-failure
```

| Verificación | Resultado |
| --- | --- |
| Navegación nativa HOST | **PASS 14/14**, 0,33 s de CTest. |
| CoreRPG con backend JSON | **PASS 483/483**, 1,56 s de CTest. |
| H09-C02, H09-P03, H09-P01, H01, S11, F04 referencia y Miranda | **PASS 94/94** documentales y de referencia (15 + 15 + 11 + 11 + 16 + 22 + 4). |
| Regresión nativa HOST/F04/F05 | **PASS 389/389** en 30,13 s con el código funcional. La composición aislada recompilada dio **PASS 292/292** en 23,08 s, con 137 HOST (incluidos los 14 CN2), 21 F04 y 134 F05. |
| Fixture aislado F11 para los lectores históricos del HOST | **PASS 17/17**. |
| Costura de compilación y oráculos históricos | **PASS**. `cmp` entre la copia generada y la unidad funcional, 21/21 hashes de `contract_files` y 6/6 oráculos verificados con `history_reference.py`. `f04.history_reference_contract` pasó con el comparador nativo. El generador rechazó una copia con contexto alterado sin publicar salida. |
| Guardado generado por el binario de la base | **PASS**. `host_m0_tests write` de la base generó una ranura con una orden F05 ejecutada. Un proceso de C02 enlazado a `TrekHost` llamó a `restore`, `query_navigation` y `save`. Recuperó ubicación nula y carta vacía, y guardó en una ranura nueva. |

Las advertencias de GCC sobre inicializadores de Core y enlace interno de F04 permitieron completar la compilación.

La matriz de Actions ejecuta CN2 en Linux, Windows y ASan/UBSan. El estado por SHA y los artefactos están en los checks de la rama. [GitHub Actions](https://github.com/robdor80/Videojuego_StarTrek/actions?query=branch%3Acodex%2Fhost-h09-p03-c02-navegacion)

## Limpieza

El laboratorio propio `laboratorios/HOST/H09-P03-C02/` reunió los checkouts de verificación, compilaciones, guardados, herramientas y registros. La medición inmediatamente anterior al borrado fue de 560.833.160 bytes de tamaño aparente (`du -sb`). Las pruebas y la compilación se regeneran desde el código y las fuentes versionadas.

Se eliminó por completo el primer laboratorio. La comprobación de la composición aislada reutilizó esa ruta. La nueva medición antes de limpiar fue de 266.360.960 bytes aparentes. Las pruebas no requieren archivos de ese directorio tras compilar desde las fuentes versionadas.

El segundo laboratorio también se eliminó por completo. La ruta quedó ausente y ningún artefacto propio quedó retenido.
