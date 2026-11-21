# H06 — IA-03C-02 · Interfaz C nativa de Academia

**Fecha:** 21-11-2026. **Estado:** corrección de paginación solicitada por auditoría IMPLEMENTADA Y PROBADA; CI Linux/Windows/ASan-UBSan y producto Release tests-OFF PASS. Auditoría independiente pendiente de cierre. No fusionar.

**Base:** PR Draft #193, rama `chatgpt/host-h06-ia03c01-contratos-unreal-20261121`, SHA `cb633b4ba3097a872c6901fdd6191a5c0e245c0b`. Entrega: [PR Draft #194](https://github.com/robdor80/Videojuego_StarTrek/pull/194), rama `codex/host-h06-ia03c02-academy-native`. Auditoría del HEAD `29609e5125fbdcff2d8dd0281c2598eed46c756e`: [dictamen condicionado](https://github.com/robdor80/Videojuego_StarTrek/pull/194#pullrequestreview-6003856271). Esta corrección continúa C-02 en la misma PR; no crea otra subfase. El HEAD final queda identificado por el historial y la PR.

## Interfaz entregada

Cabecera pública `desarrollo/integration/host/include/trek/host/academy_abi.h`. Tres exports aditivos: `trek_host_academy_version`, `trek_host_academy_submit`, `trek_host_academy_poll`. Se resuelven conjuntamente; extensión Academy **2**. Se conserva `trek_host_abi_version() == 1`. El protocolo Academy Draft 1 se rechaza explícitamente con ABI_MISMATCH; ningún tamaño cambia: `slot_cursor` es alias de `creation_key` para SLOTS, y `next_cursor` ocupa la anterior palabra reservada del catálogo. La ABI naval v1 y su consumidor histórico permanecen intactos.

| Operación | Entrada | Resultado de lectura |
| --- | --- | --- |
| CREATE | Clave creciente no nula, generación 0, nombre UTF-8 de 1–96 bytes | Campaña UUID, generación, PERSON, hecho de creación, revisión, tick, nombre, digest de fuente S04 y estado candidato; éxito únicamente después de H03 BOUND |
| QUERY | Generación activa exacta | Misma ficha; valida el ancla H03 contra CoreRPG y su checkpoint |
| SLOTS | Generación actual; 0 en CLOSED. `slot_cursor=0` inicia; luego se devuelve `next_cursor` como entrada | Hasta 64 filas por página: UUID, ranura, versión, familia, formato, procedencia, compatibilidad, recuperabilidad y motivo de rechazo. `next_cursor=0` termina |

Una ficha no contiene credenciales ni recibos. No se acepta `person_id` como entrada. Especie, edad, biografía, admisión, matrícula, rango, nave y permisos no son campos editables. El nombre se codifica en el payload privado B02 y se valida mediante `academy_display_name`, con la política S04 existente; se rechazan UTF-8 inválido, NUL, controles y entradas fuera del límite.

Secuencia prevista para C-03: crear un cliente v1, negociar la extensión, enviar CREATE y observar con el poll extendido; conservar generación y UUID; consultar con QUERY; guardar con SAVE v1; CLOSE; en otro proceso consultar SLOTS y restaurar mediante RESTORE v1/AUTO; QUERY con la generación nueva. SLOTS es una observación, no una autorización: RESTORE siempre revalida H04.

El staging actual de Unreal (`Prepare-Host.ps1`) copia únicamente `host_abi.h`, y `HostRuntime` resuelve únicamente los exports v1. C-03 deberá incorporar `academy_abi.h` al SDK staged y negociar los tres exports extendidos. C-02 entrega la biblioteca y su cabecera pública; no modifica ese consumidor ni declara integración UE ejecutada.

## Compatibilidad y ejecución

Se eligen nuevos exports frente a una ABI v2 completa: evita duplicar OPEN/SAVE/RESTORE/CLOSE y permite al consumidor anterior seguir resolviendo exactamente sus símbolos. `host_abi.h` permanece intacto. Tamaños v1: request 80, completion 120, status 24 bytes. La extensión fija request 48, ficha 240, fila de catálogo 104 y completion 6696 bytes para plataformas de 64 bits con alineación predeterminada. Ambas cabeceras tienen comprobaciones de layout desde C/C++.

Existe un solo `TrekHostClient`, un solo `SessionOwner`, su trabajador y su Core activo. Las dos fachadas comparten ocho observaciones y la reserva CLOSE. Submit copia entradas acotadas; poll prueba disponibilidad sin esperar. La inspección de disco/Core ocurre en el trabajador. Descartar una observación no cancela la creación ni impide el vínculo. El poll incorrecto para una familia de ticket devuelve ABI_MISMATCH sin consumirlo. Destroy conserva la obligación v1 de ejecutarse fuera del Game Thread y esperar al trabajador antes de descargar las DLL.

El catálogo reutiliza `SlotStore` y el mismo verificador H04 que la inspección nativa anterior, incluida restauración Core aislada. `inspect_version` comparte exactamente la validación de manifiesto, COMMITTED, registro, árbol, hash e identidad Core entre ambas consultas; SAVE/RESTORE, sus formatos y sus límites no cambian. Los formatos dañados que se pueden identificar conservan su familia; un formato desconocido se proyecta UNKNOWN, nunca naval por defecto.

## Corrección de auditoría: catálogo paginado

El límite anterior contaba versiones agregadas y devolvía cero filas desde la 65. Se sustituye por paginación de clave: campaña ASCII ascendente, ranura ASCII ascendente y versión numérica descendente. No se usa el orden de `directory_iterator` para ordenar la salida ni se guarda el catálogo completo en memoria. No hay límite agregado de 64 versiones ni el antiguo presupuesto agregado de 10.000 nodos de `inspect` en el camino paginado; la inspección C++ histórica conserva su contrato anterior.

Cada petición verifica como máximo 64 versiones y avanza como máximo 128 directorios de campaña/ranura. Se mantienen guardas por directorio de hasta 10.000 entradas, coherentes con la guarda H04 de versiones, sin cambiar el límite H04 de 10.000 versiones por ranura. La enumeración ordenada tiene memoria acotada por esas guardas; los datos Core solo se validan para la página solicitada. Al agotarse el presupuesto de recorrido puede haber páginas vacías con continuación, por ejemplo al encontrar miles de ranuras vacías: el consumidor continúa hasta `next_cursor=0`, no hasta `count=0`.

Los cursores son referencias opacas de lectura, no credenciales. El propietario retiene hasta 32 posiciones, emite tokens de 32 bits sin reutilización dentro del proceso y devuelve GENERATION_EXPIRED para cursores ajenos, expulsados o retirados. Al agotarse el espacio de tokens falla CAPACITY_LIMIT sin reciclarlos. Repetir una posición retenida revalida la misma clave de inicio; descartar una observación no la consume. SAVE admitido, OPEN, CREATE, RESTORE y CLOSE retiran posiciones y observaciones anteriores mediante un epoch privado, además de la comprobación de generación. Incluye CLOSE desde CLOSED y SAVE sin cambio de generación.

Se trata de un recorrido vivo, sin retener locks de almacenamiento entre peticiones. Cada fila se valida al leerla. Si otro proceso modifica el árbol entre páginas, pueden incorporarse filas posteriores al cursor; para incluir nuevas filas que ordenan antes de él se reinicia en cero. Esto no ofrece un snapshot de disco ni atribuye autoridad a metadatos: RESTORE siempre vuelve a validar H04. Los fallos de integridad de una versión se devuelven en su fila y no eliminan otras campañas del catálogo; los errores estructurales de ruta/recorrido siguen fallando de forma cerrada.

## Reintentos, fallos y cierres

El producto mantiene un único registro acotado de reintento en el propietario: clave máxima, payload y referencia débil al intento B02. La misma clave/nombre reutiliza el intento, PERSON y recibo; otro nombre devuelve IDEMPOTENCY_CONFLICT. Una clave superior únicamente empieza en CLOSED. Las claves retiradas no pueden volver a activar una campaña después de CLOSE, OPEN o RESTORE.

CREATE reserva OPENING al admitir el trabajo. En el trabajador compone los handlers B02 CREATE y B03 BIND existentes, con promesas locales que se completan en ese mismo hilo; no espera trabajo encolado ni necesita poll para avanzar. B03 usa exclusivamente el recibo B02 privado. Un fallo de staging deja CLOSED y permite reintentar el mismo intento. Un fallo de vínculo conserva la PERSON y el recibo para reintento; no devuelve ficha BOUND y no permite guardar una campaña sin vínculo. CLOSE puede revocar la generación durante validación, limpia la cola y evita la publicación tardía del vínculo. Las cinco operaciones F05 permanecen denegadas antes del bridge naval.

Una creación sin SAVE no es durable. Un cierre de proceso antes de guardar pierde el mundo en memoria; el proceso siguiente usa Continuar sobre las versiones H04 confirmadas o inicia una nueva campaña explícita. La clave es de vida del cliente, no una credencial durable ni un identificador global. La persistencia, publicación incierta y recuperación de archivos siguen siendo responsabilidad de H04; no se añade otro registro persistente.

## Pruebas y evidencia anterior a la corrección

- Local Windows, MSVC 19.51 / Visual Studio 18 2026, Release: consumidor C11 y pruebas de producto contra DLL real. Pasan ciclo ABI extendida, ABI v1 histórica, reinicio entre procesos, identidad intacta, catálogo mixto y overflow; tres tests C-02 más `host.abi.lifecycle`.
- Regresión local ampliada: **114/114 PASS**, selección `^host\.(native|fault|persistence|m0|abi|academy\.(abi_|b0|persistence_))`, incluidos roundtrip naval C v1, casos H03, negativos y cierres H04/B03. El código de producto es el del SHA inicial; el consumidor C incluye además las comprobaciones de entradas reservadas, dos CREATE admitidos antes de observar, referencias de otro cliente y catálogo caducado después de RESTORE.
- Negativos del consumidor C: UTF-8 sobrelargo/surrogates/fuera de Unicode, nombre largo, NUL, entradas reservadas/versiones; replay/conflicto; generación caducada; capacidad compartida y CLOSE reservado; descarte; cierres repetidos y destroy durante creación. H04: COMMITTED alterado, campaña no registrada, pin incorrecto y formato desconocido, con catálogo y RESTORE rechazados.
- Composición aislada con fallos: staging interrumpido antes de publicar, fallo de bind y reintento sobre la misma PERSON, CLOSE durante bind con barrera determinista, una PERSON/un hecho/cero población, revisión e identidad sin mutación, cinco operaciones F05 rechazadas.
- CI histórica del commit de implementación/pruebas `60a390dc1ea97060f996f5c8588cb8607582666d`: [ejecución 44879265924](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44879265924). Su código de producto coincide con `79bc00c5032e9ad690b32273d90c1481f3d7e198`; el cierre documental de esa iteración fue `29609e5125fbdcff2d8dd0281c2598eed46c756e`, objeto de la auditoría que solicitó paginación.

| Comprobación CI | Resultado comprobado | Evidencia |
| --- | --- | --- |
| Linux nativo Release | **296/296 PASS**; contratos H01 y regresión F11 aislada PASS | [job 136770737571](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44879265924/job/136770737571) |
| Windows nativo Release | **296/296 PASS**; contratos H01 y regresión F11 aislada PASS | [job 136770737558](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44879265924/job/136770737558) |
| Linux Clang ASan/UBSan | **141/141 PASS**, detección de fugas habilitada y halt-on-error; sin errores de sanitizadores | [job 136770737303](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44879265924/job/136770737303) |
| Linux Release, tests OFF | **4/4 consumidores PASS**, exports y dependencias inspeccionados | [job 136770737537](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44879265924/job/136770737537) |
| Windows Release, tests OFF | **4/4 consumidores PASS**, DLL cargada, exports y dependencias inspeccionados | [job 136770737614](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44879265924/job/136770737614) |

Los cuatro tests del consumidor independiente son: binario C v1 histórico, ciclo de la extensión C, persistencia/catálogo/negativos/límite a través de C en procesos separados y persistencia nativa B03. Las builds tests-OFF carecen de hooks de pruebas/F11 trial y conservan el pin Core validado en tiempo de carga. Los logs y resultados JUnit se publican como artefactos del workflow.

La auditoría posterior detectó el fallo funcional del catálogo pese a esta CI verde. La prueba anterior de overflow acreditaba el límite, pero su oráculo era insuficiente para Continuar. Ese oráculo se reemplaza por acceso a las versiones 65 y anteriores mediante páginas exitosas.

## Validación de la corrección de paginación

- Consumidor C11 contra DLL real: **5/5 pruebas locales PASS**, incluida ABI naval v1. Nuevo caso `host.academy.abi_pagination`, también `product.academy.c_pagination` contra Release tests-OFF.
- Regresión local ampliada de la corrección: **115/115 PASS**, incluidos H03/H04, B02/B03, F05 y roundtrip naval C v1.
- Fixture con **145 versiones H04 reales de cuatro campañas y varias ranuras** (tres Academy con 65, 70 y 9 versiones, la tercera repartida entre alpha/beta, más una naval): cobertura exacta, sin duplicados, orden determinista y repetible entre procesos, recuperación de versiones 1/2/64/65/70 y del histórico beta con la misma PERSON y bloqueo F05 intacto.
- COMMITTED manipulado en una fila posterior a la primera página: la fila conserva su error y quedan consultables las otras 144 versiones. Reintentos/descarte de páginas, cursor extranjero/inexistente/fuera de rango, caducidad por CLOSE desde CLOSED, RESTORE y SAVE en la misma generación.
- 4.200 ranuras vacías: progreso por páginas vacías y expulsión segura de cursores tras más de 32 posiciones, sin bucles ni crecimiento del registro de cursores.
- Implementación de paginación: `4e85bb7ca0e080cef185667a6e1a861345936adb`. Fixture final de pruebas: `7e2208692df87484ee08bb966e96d5610bc1b7b5`. [CI de la corrección, run 44882238947](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44882238947). La ejecución intermedia 44882003402 se canceló al ampliar el fixture de varias ranuras; fue sustituida por esta matriz sobre el commit actualizado, sin diagnosticar un fallo de código.

| Comprobación de la corrección | Resultado | Evidencia |
| --- | --- | --- |
| Linux nativo Release | **297/297 PASS**, H01 y regresión aislada F11 PASS | [job 136779829935](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44882238947/job/136779829935) |
| Windows nativo Release | **297/297 PASS**, H01 y regresión aislada F11 PASS | [job 136779829797](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44882238947/job/136779829797) |
| Linux Clang ASan/UBSan | **142/142 PASS**, sin errores de sanitizadores, detección de fugas habilitada | [job 136779829719](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44882238947/job/136779829719) |
| Linux Release, tests OFF | **5/5 PASS**, carga y exports inspeccionados | [job 136779829671](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44882238947/job/136779829671) |
| Windows Release, tests OFF | **5/5 PASS**, carga y exports inspeccionados | [job 136779829796](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44882238947/job/136779829796) |

Los cinco consumidores incluyen los cuatro anteriores y la paginación con varias campañas/ranuras. Los resultados anteriores a la corrección se conservan como evidencia histórica y no se atribuyen a este nuevo código.

**Resultado de la corrección:** ninguna compilación ni prueba fallida en la matriz completa del SHA `7e2208692df87484ee08bb966e96d5610bc1b7b5`. El commit posterior de cierre modifica únicamente este informe y el tablero, con código y tests idénticos; el HEAD final y su CI asociada se verifican en la PR antes de la entrega. El dictamen de auditoría sigue pendiente de revisión independiente; no se declara fusionado ni certificado M1.

La duración de disco/Core depende del sistema de archivos, con trabajo acotado y ejecutado fuera del hilo llamador. Una campaña sin SAVE confirmado no sobrevive al proceso, conforme a H04.

La ejecución de este chat es Windows local con CI remota, sin ejecutor Cloud conectado. Todos los builds y registros locales se aíslan en el laboratorio C-02 del repositorio conforme a AGENTS.md; no se publican en Git ni constituyen dependencias del producto.

No se modifica CoreRPG ni el pin `76a7b7b485616d8c4994f384a90f123bf333591d`, F11, contratos históricos LOCKED o fuentes Unreal. No se ejecuta UBT, Unreal, NullRHI, D3D12 ni aceptación MSI. C-03, C-04 y C-05 siguen pendientes; M1 no está certificado.
