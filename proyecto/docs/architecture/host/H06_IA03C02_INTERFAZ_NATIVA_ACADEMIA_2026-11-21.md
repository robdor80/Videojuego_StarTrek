# H06 — IA-03C-02 · Interfaz C nativa de Academia

**Fecha:** 21-11-2026. **Estado:** IMPLEMENTADA, pruebas locales PASS; CI pendiente de registrar. Auditoría independiente pendiente. No fusionar.

**Base:** PR Draft #193, rama `chatgpt/host-h06-ia03c01-contratos-unreal-20261121`, SHA `cb633b4ba3097a872c6901fdd6191a5c0e245c0b`. Rama de implementación: `codex/host-h06-ia03c02-academy-native`. La PR y sus ejecuciones identificarán el HEAD comprobado; este informe se actualizará con los resultados finales.

## Interfaz entregada

Cabecera pública `desarrollo/integration/host/include/trek/host/academy_abi.h`. Tres exports aditivos: `trek_host_academy_version`, `trek_host_academy_submit`, `trek_host_academy_poll`. Se resuelven conjuntamente; extensión 1. Se conserva `trek_host_abi_version() == 1`.

| Operación | Entrada | Resultado de lectura |
| --- | --- | --- |
| CREATE | Clave creciente no nula, generación 0, nombre UTF-8 de 1–96 bytes | Campaña UUID, generación, PERSON, hecho de creación, revisión, tick, nombre, digest de fuente S04 y estado candidato; éxito únicamente después de H03 BOUND |
| QUERY | Generación activa exacta | Misma ficha; valida el ancla H03 contra CoreRPG y su checkpoint |
| SLOTS | Generación actual; 0 en CLOSED | Hasta 64 versiones: UUID, ranura, versión, familia, formato, procedencia, compatibilidad, recuperabilidad y motivo de rechazo |

Una ficha no contiene credenciales ni recibos. No se acepta `person_id` como entrada. Especie, edad, biografía, admisión, matrícula, rango, nave y permisos no son campos editables. El nombre se codifica en el payload privado B02 y se valida mediante `academy_display_name`, con la política S04 existente; se rechazan UTF-8 inválido, NUL, controles y entradas fuera del límite.

Secuencia prevista para C-03: crear un cliente v1, negociar la extensión, enviar CREATE y observar con el poll extendido; conservar generación y UUID; consultar con QUERY; guardar con SAVE v1; CLOSE; en otro proceso consultar SLOTS y restaurar mediante RESTORE v1/AUTO; QUERY con la generación nueva. SLOTS es una observación, no una autorización: RESTORE siempre revalida H04.

## Compatibilidad y ejecución

Se eligen nuevos exports frente a una ABI v2 completa: evita duplicar OPEN/SAVE/RESTORE/CLOSE y permite al consumidor anterior seguir resolviendo exactamente sus símbolos. `host_abi.h` permanece intacto. Tamaños v1: request 80, completion 120, status 24 bytes. La extensión fija request 48, ficha 240, fila de catálogo 104 y completion 6696 bytes para plataformas de 64 bits con alineación predeterminada. Ambas cabeceras tienen comprobaciones de layout desde C/C++.

Existe un solo `TrekHostClient`, un solo `SessionOwner`, su trabajador y su Core activo. Las dos fachadas comparten ocho observaciones y la reserva CLOSE. Submit copia entradas acotadas; poll prueba disponibilidad sin esperar. La inspección de disco/Core ocurre en el trabajador. Descartar una observación no cancela la creación ni impide el vínculo. El poll incorrecto para una familia de ticket devuelve ABI_MISMATCH sin consumirlo. Destroy conserva la obligación v1 de ejecutarse fuera del Game Thread y esperar al trabajador antes de descargar las DLL.

El catálogo reutiliza `SlotStore` y el mismo verificador H04 que la inspección nativa anterior, incluida restauración Core aislada. El límite de 64 versiones se aplica antes de validar una versión adicional; el límite histórico de recorrido de directorios y los límites de H04 siguen vigentes. Un desbordamiento devuelve CAPACITY_LIMIT sin filas parciales. Los formatos dañados que se pueden identificar conservan su familia; un formato desconocido se proyecta UNKNOWN, nunca naval por defecto.

## Reintentos, fallos y cierres

El producto mantiene un único registro acotado de reintento en el propietario: clave máxima, payload y referencia débil al intento B02. La misma clave/nombre reutiliza el intento, PERSON y recibo; otro nombre devuelve IDEMPOTENCY_CONFLICT. Una clave superior únicamente empieza en CLOSED. Las claves retiradas no pueden volver a activar una campaña después de CLOSE, OPEN o RESTORE.

CREATE reserva OPENING al admitir el trabajo. En el trabajador compone los handlers B02 CREATE y B03 BIND existentes, con promesas locales que se completan en ese mismo hilo; no espera trabajo encolado ni necesita poll para avanzar. B03 usa exclusivamente el recibo B02 privado. Un fallo de staging deja CLOSED y permite reintentar el mismo intento. Un fallo de vínculo conserva la PERSON y el recibo para reintento; no devuelve ficha BOUND y no permite guardar una campaña sin vínculo. CLOSE puede revocar la generación durante validación, limpia la cola y evita la publicación tardía del vínculo. Las cinco operaciones F05 permanecen denegadas antes del bridge naval.

Una creación sin SAVE no es durable. Un cierre de proceso antes de guardar pierde el mundo en memoria; el proceso siguiente usa Continuar sobre las versiones H04 confirmadas o inicia una nueva campaña explícita. La clave es de vida del cliente, no una credencial durable ni un identificador global. La persistencia, publicación incierta y recuperación de archivos siguen siendo responsabilidad de H04; no se añade otro registro persistente.

## Pruebas y evidencia

- Local Windows, MSVC 19.51 / Visual Studio 18 2026, Release: consumidor C11 y pruebas de producto contra DLL real. Pasan ciclo ABI extendida, ABI v1 histórica, reinicio entre procesos, identidad intacta, catálogo mixto y overflow; tres tests C-02 más `host.abi.lifecycle`.
- Negativos del consumidor C: UTF-8 sobrelargo/surrogates/fuera de Unicode, nombre largo, NUL, entradas reservadas/versiones; replay/conflicto; generación caducada; capacidad compartida y CLOSE reservado; descarte; cierres repetidos y destroy durante creación. H04: COMMITTED alterado, campaña no registrada, pin incorrecto y formato desconocido, con catálogo y RESTORE rechazados.
- Composición aislada con fallos: staging interrumpido antes de publicar, fallo de bind y reintento sobre la misma PERSON, CLOSE durante bind con barrera determinista, una PERSON/un hecho/cero población, revisión e identidad sin mutación, cinco operaciones F05 rechazadas.
- CI requerida: Linux, Windows, ASan/UBSan y Release tests-OFF Linux/Windows, con consumidor C compilado separadamente contra el producto. Resultados y SHA se registrarán al finalizar las ejecuciones.

No se modifica CoreRPG ni el pin `76a7b7b485616d8c4994f384a90f123bf333591d`, F11, contratos históricos LOCKED o fuentes Unreal. No se ejecuta UBT, Unreal, NullRHI, D3D12 ni aceptación MSI. C-03, C-04 y C-05 siguen pendientes; M1 no está certificado.
