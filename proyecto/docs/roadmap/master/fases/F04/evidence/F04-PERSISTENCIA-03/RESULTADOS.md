# F04-PERSISTENCIA-03 — Resultados reales y bloqueo

**Entrega parcial. No hay archivado implementado. No se cumplen los criterios
completos de campañas largas.** Base `45f7816c9aa996bfd678b11b4f9fa1a4b9632021`.
[Auditoría y propuesta genérica](../../F04-PERSISTENCIA-03_CAMPANAS_LARGAS.md).

## Resultado de los recorridos

| Clase / objetivo | Días completos publicados | Entidades finales | Bytes del archivo final | Resultado siguiente bloque |
| --- | ---: | ---: | ---: | --- |
| Miranda / 365 | 365 | 41.230 | 12.039.036 | Objetivo de esta muestra alcanzado, sin archivo |
| Intrepid / 365 | 365 | 47.669 | 14.057.612 | Objetivo de esta muestra alcanzado, sin archivo |
| Sovereign / 365 | 112 | 56.042 | 17.386.033 | 112→140 rechazado por F04_CAPACITY |
| Odyssey / 365 | 56 | 62.004 | 19.380.922 | 56→84 rechazado por F04_CAPACITY |
| Valhalla / 365 | 28 | 37.554 | 11.806.157 | 28→56 rechazado por F04_CAPACITY |
| Valhalla / 730 | 28 | 37.554 | 11.806.157 | 28→56 rechazado por F04_CAPACITY |

Son los últimos **bloques completos** de esta prueba, no el máximo número de
días que podría obtenerse probando bloques más pequeños. No se alcanzan 730 días.
Las cifras tras rechazo incluyen su único evento; antes del rechazo Valhalla
tiene 37.553 entidades, Odyssey 62.003 y Sovereign 56.041. La transacción
descartada alcanza el presupuesto F04 y no publica sus entidades; por eso el
estado final no tiene que estar exactamente en 65.536. Todos estos archivos
están por debajo de 64 MiB y de un millón de relaciones.

Se han generado y conservado 26.831 DUTY en Miranda y 32.771 en Intrepid a 365
días; 50.126 en Sovereign, 56.764 en Odyssey y 32.460 en Valhalla en los últimos
horizontes publicados. Hay 8.760 funciones en cada muestra anual pequeña.
Todo sigue siendo estado residente; **cero registros en segmentos históricos**.
No hay mejora antes/después ni tiempos de compactación/archivo/recuperación
segmentada que medir todavía. El contador `entities` incluye historia vencida,
no solo personas o servicios vigentes. Las consultas paginadas existentes pueden
leer ese historial mientras el archivo monolítico quepa.

Cada bloque compara un avance sin interrupción con avance tras cargar el plan,
con igualdad íntegra de bytes; al final otro proceso carga el checkpoint previo
al último bloque y produce el mismo futuro o el mismo rechazo. Se comprueban
ventanas móviles 5/7, descanso >=12 h, un turno diario, IDs, destinos, grupos,
competencias, censo, RNG y reloj. En Valhalla siguen existiendo las mismas 2.200
personas, 1.800 plazas, 90 secciones, 40 navales Defiant, 60 Marines y 400 civiles;
sus registros de identidad/cualificación/grupo/residencia no cambian.

Estos recorridos nuevos son muestras nominales sin incidentes inyectados; las
regresiones existentes ejercen bajas, ausencias, relevos, traslados, deuda,
cancelación y revocación. No se confunden con campañas anuales con todos esos
incidentes ni con consultas de un archivo histórico que no existe todavía.

## Crecimiento medido antes del avance

| Clase | Entidades iniciales tras bootstrap | Añadidas 1 día | Añadidas 7 días | Añadidas 28 días | Total 28 días | Bytes 28 días |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Miranda | 315 | 113 | 774 | 3.065 | 3.380 | 986.132 |
| Intrepid | 377 | 131 | 902 | 3.561 | 3.938 | 1.158.923 |
| Sovereign | 1.484 | 507 | 3.428 | 13.668 | 15.152 | 4.671.275 |
| Odyssey | 3.297 | 1.068 | 7.393 | 29.350 | 32.647 | 10.157.613 |
| Valhalla | 4.115 | 1.218 | 8.397 | 33.355 | 37.470 | 11.789.885 |

Promedios añadidos/día dentro del bloque de 28: 109,46; 127,18; 488,14; 1.048,21;
1.191,25 respectivamente. No se extrapolan como una ley lineal: descansos,
déficits, fronteras y eventos cambian el incremento. La muestra de 1 día usa
ROTATING sin semilla de referencia; 7/28 días incluyen la primera jornada de
referencia del contrato vigente. Los recorridos continuos solo la siembran en
el primer bloque. No reinician el contador ni las guardias entre bloques.

Desglose a 28 días de los mayores consumidores:

| Clase | DUTY | Funciones | Nombramientos totales | Carencias |
| --- | ---: | ---: | ---: | ---: |
| Miranda | 2.074 | 672 | 180 | 148 |
| Intrepid | 2.535 | 672 | 180 | 183 |
| Sovereign | 12.648 | 672 | 182 | 177 |
| Odyssey | 28.459 | 672 | 182 | 48 |
| Valhalla | 32.460 | 672 | 181 | 52 |

Las carencias cuentan **registros**, no la suma de servicios faltantes. Los
nombramientos incluyen los permanentes previos al plan. Toda la contabilidad
por tipo, relaciones y muestras de 1/7/28 está en [measurements.json](measurements.json).

## Rendimiento observado

| Clase, 28 días | Plan ms | Save (dos llamadas) ms | Load ms | Working set bytes |
| --- | ---: | ---: | ---: | ---: |
| Miranda | 65,63 | 34,35 | 30,93 | 9.129.984 |
| Intrepid | 81,48 | 40,97 | 35,35 | 10.010.624 |
| Sovereign | 326,66 | 156,16 | 148,81 | 23.764.992 |
| Odyssey | 777,59 | 347,63 | 311,96 | 45.912.064 |
| Valhalla | 917,25 | 391,04 | 363,19 | 50.778.112 |

Working set se observa después de guardar/cargar y de crear el snapshot
diagnóstico; incluye buffers, copias transaccionales y runtime. No es memoria
aislada del motor ni una comparación directa con Python. El pico de proceso
también está en JSON. Picos de las muestras continuas: Miranda 128.577.536 bytes,
Intrepid 149.987.328, Sovereign 184.532.992, Odyssey 207.478.784 y Valhalla
125.972.480. Hubo otras compilaciones/pruebas simultáneas en el MSI; son muestras
puntuales sin percentiles. El segundo intento Valhalla usa otro proceso y su
pico es 130.998.272 bytes.

El plan 28→56 Odyssey tarda 2.030,92 ms y el 84→112 Sovereign 1.952,26 ms. El
336→364 de Miranda tarda 1.835,99 ms e Intrepid 1.654,77 ms: el crecimiento del
trabajo residente afecta también a naves que aún caben. Los tiempos completos
por bloque están en [campaigns.json](campaigns.json). Los `elapsed_ms` del
recorrido incluyen serializaciones, dobles avances de determinismo, auditorías
y pruebas negativas; no son el coste de simulación puro.

## Pruebas ejecutadas

| Suite | Resultado |
| --- | --- |
| Core completo + Content JSON recompilado | 447 superadas, cuatro omitidas, cero fallos |
| F04 anterior completo | 243/243 |
| Diagnósticos de persistencia nuevos | 27/27; reproducen capacidad, no aceptación de archivo |
| F02 / F03 recompiladas con sus pins | 15/15 y 25/25 |
| Unreal 5.8.2 Win64 NullRHI recompilado | 25/25 Success; cero warnings de test |
| Documentales F04/Miranda/F03/F02 | 22+4+26+9 = 61/61 |
| LORE-03 A | 56/56 |
| Fixture autoridad / roadmap | PASS / PASS |
| Referencias globales | 566 incidencias previas idénticas a main; cero nuevas |
| Archivos de la DLL previa, cinco clases | Lectura y continuación al mismo futuro |

Las cuatro omisiones Core son permisos/symlinks no exigibles en esta plataforma;
no se cuentan como éxitos. Se conservan los avisos de toolchain/compilador Unreal
en el log. NullRHI no certifica escenas 3D. [Resumen](test-summary.json),
[Core](core.xml), [F04 anteriores](f04-existing.xml),
[diagnósticos](persistence.xml), [Unreal](unreal-report.json),
[compatibilidad](compatibility.json), [referencias](reference-regression.json).

Las cinco muestras continuas rechazan truncado, magic inválido, checksum,
versión desconocida e intervalo F04 manipulado con checksum Core válido. Cada
rechazo conserva la partida anterior byte a byte y los handles anteriores.
En los rechazos por capacidad se verifica el código auditado y se elimina
exclusivamente ese evento del snapshot de comparación: el resto completo
coincide con la partida anterior. No se afirma tolerancia ante escritura rota
en disco ni fallos de consolidación: no hay publicación segmentada implementada.
Los casos pendientes de fallo/recuperación están en el diseño y en
[acceptance.json](acceptance.json).

## Trazabilidad y reproducción en PowerShell

Los archivos de campaña/checkpoint/futuro se escriben fuera del checkout;
[sus hashes y tamaños](campaign-file-hashes.json) permiten comparar una repetición.
Los logs y XML contienen nombres de casos y resultados. CTest truncó parte del
stdout en JUnit a 1.024 bytes; [persistence-full.txt](persistence-full.txt) conserva
la salida completa de los 27 casos, y el colector usa sus líneas JSON completas.
No se regeneraron resultados para suplir el truncado. El colector normaliza
codificación UTF-8, finales de línea y
espacios al final de las líneas para su revisión en Git.
Los timestamps de logs corresponden al MSI; la fecha de entrega es
31-10-2026 Europe/Madrid.

`provenance.json` comprueba pins limpios, hashes de fuentes compiladas y DLL
nativa/staged idénticas. Todas las fuentes productivas F02/F03/F04 son iguales a
la base, normalizando CRLF/LF. La diferencia productiva es cero; únicamente se
añaden diagnósticos, su registro CMake, documentación y evidencias. No se hace
una afirmación de inventario/hash de recursos externos no examinados.

Desde la raíz de la rama, con los tres checkouts Core en los pins anteriores:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
cmake -S desarrollo/integration/f04 -B C:/F04/PersistenciaBuild/native -G 'Visual Studio 18 2026' -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04/PersistenciaBuild/native --config Release --parallel 4
ctest --test-dir C:/F04/PersistenciaBuild/native -C Release -E 'f04.persistence' --no-tests=error --output-on-failure --output-junit C:/F04/PersistenciaBuild/f04-existing.xml
ctest --test-dir C:/F04/PersistenciaBuild/native -C Release -R 'f04.persistence' --no-tests=error --output-on-failure --test-output-size-passed 65536 --output-junit C:/F04/PersistenciaBuild/persistence.xml
Copy-Item -LiteralPath C:/F04/PersistenciaBuild/native/Testing/Temporary/LastTest.log -Destination C:/F04/PersistenciaBuild/persistence-full.txt
```

Guardar además las salidas de esos comandos como `f04-existing.txt`,
`persistence-tests.txt`, `native-build.txt` con redirección PowerShell si se desea
reconstruir el paquete. No ejecutar dos CTest sobre el mismo directorio cuando
se quiera preservar `LastTest.log` de cada ejecución. Para Core y regresiones:

```powershell
cmake -S C:/F04/CoreRPG -B C:/F04/core-build -G 'Visual Studio 18 2026' -A x64 -DBUILD_TESTING=ON -DCORERPG_BUILD_CONTENT_JSON=ON
cmake --build C:/F04/core-build --config Release --parallel 4
ctest --test-dir C:/F04/core-build -C Release --output-on-failure --output-junit C:/F04/PersistenciaBuild/core.xml > C:/F04/PersistenciaBuild/core-tests.txt
foreach($Phase in @('f02','f03')) {
 cmake -S ('desarrollo/integration/'+$Phase) -B ('C:/F04/PersistenciaBuild/'+$Phase) -G 'Visual Studio 18 2026' -A x64 ('-DCORERPG_SOURCE_DIR=C:/F04/core-'+$Phase)
 cmake --build ('C:/F04/PersistenciaBuild/'+$Phase) --config Release --parallel 4
 ctest --test-dir ('C:/F04/PersistenciaBuild/'+$Phase) -C Release --output-on-failure --output-junit ('C:/F04/PersistenciaBuild/'+$Phase+'.xml') > ('C:/F04/PersistenciaBuild/'+$Phase+'-tests.txt')
}
foreach($Stage in @('Stage','Unreal','TestUnreal')) {
 ./desarrollo/integration/f04/run_f04.ps1 -Stage $Stage -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/PersistenciaBuild -F02NativeBuild C:/F04/PersistenciaBuild/f02 -F03NativeBuild C:/F04/PersistenciaBuild/f03 -F02CoreSource C:/F04/core-f02 *> ('C:/F04/PersistenciaBuild/unreal-'+$Stage+'.txt')
}
```

Los validadores se reproducen con `python -m unittest discover -s
desarrollo/tools/validation -p <nombre> -v`, usando `test_f04_reference.py`,
`test_f04_miranda_example.py`, `test_f03_reference.py`,
`test_validate_f02_contracts.py` y `test_lore03_a.py`. Ejecutar además
`f04_reference.py --fixture desarrollo/validation/fixtures/f04/authority_watch_acceptance_v0.1.json`,
`validate_roadmap_state.py` y `validate_internal_references.py` desde
`desarrollo/tools/validation/` con la ruta de script relativa a la raíz.
El de referencias devuelve 1 por las incidencias históricas conocidas.

Compatibilidad (procesos distintos, DLL de GUARDIAS-02 y lector recién compilado):

```powershell
python desarrollo/integration/f04/check_guardias_compatibility.py --previous-build C:/F04/GuardiasBuild/native --new-build C:/F04/PersistenciaBuild/native --output C:/F04/PersistenciaBuild/compatibility.json
python desarrollo/tools/validation/validate_internal_references.py > C:/F04/PersistenciaBuild/references-current.txt
python C:/Users/andro/Documents/GitHub/Videojuego_StarTrek/desarrollo/tools/validation/validate_internal_references.py > C:/F04/PersistenciaBuild/references-base.txt
python desarrollo/integration/f04/collect_persistence_audit.py --build-root C:/F04/PersistenciaBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-PERSISTENCIA-03
```

El colector requiere los logs con los nombres de esta carpeta (`*-tests.txt`,
`unreal-tests.txt`, `unreal-build.txt`, `test_*.txt`, `authority.txt`, `roadmap.txt`);
conservar/renombrar las salidas del laboratorio según esos nombres. Su contenido
es evidencia diagnóstica, nunca otra fuente del estado del mundo. La CI existente
registra automáticamente las 270 entradas F04 por CTest; las medidas de memoria
solo se emiten en Windows. Las campañas generadas grandes no se suben a Git.

## Decisión pendiente

Se solicita autorización para desarrollar y probar en **CoreRPG genérico** la
separación identidad/residencia, manifiesto y segmentos inmutables validados,
consulta paginada histórica y consolidación transaccional descritas en el diseño.
No se solicita una subida de límites. Esta PR debe permanecer Draft sin fusionar.
