# H04 — Persistencia, recuperación y procedencia

Fecha: 2026-11-13. Estado: IMPLEMENTADO, con evidencia de pruebas separada en
[matriz H04](H04_PRUEBAS_2026-11-13.md). CERTIFICADO: NO. FUSIONADO: NO.
Base sincronizada: `3243105a7e4b09c29e4b9c454f24b74cd4086480`, PR #134 fusionada.
CoreRPG permanece limpio en `76a7b7b485616d8c4994f384a90f123bf333591d`.
No se modifican pins, formatos Core ni oráculos históricos.

## Responsabilidad y composición

`SessionOwner` sigue siendo el único gestor y propietario de la campaña activa.
SAVE y LOAD usan su FIFO de 32 solicitudes y el mismo trabajador de Core.
El mutex protege admisión y publicación; queda libre durante la preparación de IO.
Durante esas operaciones se observan `SAVING` y `LOADING`. Nuevas operaciones
reciben `BUSY_STATE`. Las ya admitidas siguen en orden salvo invalidación por
LOAD o cierre. Dos SAVE admitidos antes de la transición se serializan.

`SlotStore` coordina archivos y metadatos técnicos. No mantiene WorldState,
relojes, RNG, rangos, permisos ni expedientes. Los únicos estados del universo,
incluidos los temporales de validación, los construye Core mediante sus lectores.
Una sesión preparatoria no es una segunda campaña activa. Se crea y destruye
en el hilo que la utiliza, sin acceder desde ella al Core activo.

La composición conserva `TrekF04Bridge`, F05 y el Core de H03. No enlaza
`TrekF11TrialHost`, no activa `F11_ENABLE_PROMOTIONS` y no incorpora Unreal.
La lectura institucional y los canales UI/IA continúan en sus fases posteriores.

## Formato de ranuras v1

El consumidor configura `StorageConfig.root`: directorio absoluto existente,
autorizado, privado y UTF-8. El constructor sin configuración conserva H02/H03;
no habilita almacenamiento implícito en otra ruta. Una campaña nueva obtiene un
identificador aleatorio de 16 bytes, técnico y sin valor de credencial. Se consulta
mediante `campaign_id(generation)`; `campaign_provenance` informa de su origen.

```text
<raíz autorizada>/
  host.lock
  registry/<campaña de 32 hex>                  # constancia local de vínculo
  campaigns/<campaña>/slots/<ranura>/v<N>/
    manifest                                  # sobre técnico versionado
    history/CURRENT                           # raíz Core CRPGROOT
    history/<SHA256>.obj                       # manifiesto/checkpoints/segmentos Core
    history/writer.lock
    COMMITTED                                 # publicación confirmable
  work/<identificador aleatorio>/history/...   # copia operativa aislada de LOAD
```

`prepared` puede existir antes de `COMMITTED`. Su existencia no confirma una
partida. Las versiones nunca se sobrescriben ni se eliminan automáticamente.
Los restos incompletos, versiones anteriores y copias de trabajo se conservan;
la limpieza/retención futura requiere una operación explícita fuera de H04.
El producto no depende de directorios de compilación ni de experimentos.

El manifiesto textual tiene exactamente seis líneas: `TREKHOST4 1`, SHA Core,
ID de campaña, ranura, versión de ranura y tupla técnica del vínculo
`persona hecho_de_vínculo revisión_de_entrada tick_de_vínculo`. `COMMITTED`
contiene el mismo sobre. La constancia de `registry` vive fuera del paquete
movible de campaña; contiene solo esa tupla. Estos IDs permiten contrastar la
continuidad con Core; nunca confieren autoridad. No se replica el contenido
profesional ni se obtiene un vínculo mediante una mutación de restauración.

Límites: nombres de ranura de 1 a 32 caracteres `[a-z0-9_]`, exclusión de nombres
de dispositivo Windows; campaña de 32 hex minúsculos no nulos; rutas de hasta
4096 unidades nativas; metadatos hasta 4096 bytes; cada objeto hasta 64 MiB;
historial hasta 512 MiB y 4096 entradas; versiones hasta 10000. El recorrido de
inspección también tiene un límite de entradas. Se rechazan archivos especiales,
links duros múltiples, symlinks/reparse points y árboles inesperados.

## Procedencia e importación

| Clase | Significado operativo |
|---|---|
| CREATED_LOCALLY | Activación nueva mediante OPEN y flujo H03. |
| KNOWN_LOCAL | Paquete local registrado, compatible y validado por Core, con vínculo coincidente. |
| IMPORTED_UNVERIFIED | Paquete sin constancia en el registro de esta raíz. Se puede inspeccionar; no activar. |
| REJECTED | Incompatible, corrupto, fuera de límites o incoherente. |

No existe una operación que importe y conceda confianza. Copiar una campaña a
`campaigns` no crea su entrada en `registry`. SAVE requiere una identidad H03
ligada en Core; LOAD de un importado permanece cerrado. No se autentica al
propietario del equipo ni se otorgan competencias por hashes o campos del sobre.
Una copia legítima de toda la raíz conserva su procedencia local técnica;
no equivale a una firma institucional. El usuario que modifica ejecutable,
registro y archivos puede falsificar su instalación local: H01 no promete
resistencia criptográfica frente a ese adversario.

## Persistencia real de Core

F05 fuerza la compilación de historial F04, pero una campaña recién abierta puede
estar aún en modo monolítico. `f04_save/load` sirven para ese modo y rechazan una
proyección segmentada. `f04_history_export_active` solo se usa como diagnóstico
comparativo en pruebas: nunca alimenta una recuperación de producto.

Se añaden APIs nativas aditivas en la composición de producto del adaptador
existente. `f04_host_bridge.cpp` incluye una sola vez el puente histórico intacto y
las extensiones H04 de persistencia y lectura F05. CMake del HOST sustituye
exclusivamente su unidad de compilación original, comprobando que era la única.
Las otras composiciones F04/F05/F11 conservan sus fuentes y contratos congelados;
no se altera el manifiesto del oráculo para admitir la extensión. Las declaraciones
nuevas están en `f04_host_persistence.h` y `f05_player_binding.h`:


- `f05_player_binding`: consulta de solo lectura del hecho F05, persona,
  revisión inicial y tick. Salida vacía si no hay vínculo o si se rechaza la lectura.
  Valida el hilo y la persona mediante el observador F05 existente.
- `f04_history_identity`: lee el UUID autoritativo del archivo Core ya abierto.
- `f04_history_snapshot`: destino nuevo. Si el Core activo es monolítico,
  compone `HistoryPersistence::migrate` con las mismas reglas F04. Si ya tiene
  historial, copia sus objetos completos, los abre con `recover` y publica
  sobre esa copia el estado vivo mediante `HistoryPersistence::publish`.
  Finalmente vuelve a recuperar el conjunto completo para verificarlo.

Estas operaciones no alteran el Core activo ni reinventan serialización,
selección histórica, reducciones, RNG o validadores F05. El adaptador reutiliza
`workload_rule`, `schema` y las primitivas Core. Conserva originales archivados,
relaciones, decisiones y cronología; no regenera hechos desde una semilla.

`f04_history_migrate`, `open`, `consolidate`, `publish` y `stats` conservan sus
contratos. H04 no decide cuándo consolidar ni cambia la retención de siete días.
Acepta y conserva historiales previamente consolidados. No publica directamente
sobre la versión confirmada ni convierte silenciosamente una sesión viva a otro
modo de persistencia. El coste de esta separación es una copia completa por
snapshot/LOAD; los objetos antiguos también cuentan para los límites.

## Publicación y durabilidad

1. Validar generación activa, vínculo H03, persona Core, campaña y ranura.
2. Bajo exclusión de almacenamiento, crear una versión nueva. La anterior sigue
   completa y accesible. Preparar el snapshot Core sin mutar la sesión viva.
3. Comprobar nombres/límites y recuperar en Core aislado todo el historial.
   Contrastar UUID y hecho exacto del vínculo con el registro local y el sobre.
4. Sincronizar todos los archivos del snapshot, escribir y sincronizar manifiesto
   y `prepared`, y asegurar los directorios implicados donde existe esa primitiva.
5. Publicar `prepared` como `COMMITTED`. Verificarlo, completar sincronización
   de namespace y únicamente entonces devolver `OK`.

Linux usa escrituras completas, `fsync` de archivos, rename en el mismo directorio
y `fsync` de directorios; se comprueba cada resultado. Windows usa handles de
archivo con escritura directa, `FlushFileBuffers` y `MoveFileExW` con
`MOVEFILE_WRITE_THROUGH`, sin sustituir versiones anteriores. No se equipara
rename por sí solo con durabilidad. Las garantías declaradas son las operaciones
que el SO confirma sobre almacenamiento local que respete flush/write-through.
No se certifican cortes eléctricos reales, controladores que ignoren barreras,
filesystems remotos ni semánticas de almacenamiento no ensayadas.

Antes de intentar la publicación, un error devuelve `PERSISTENCE_FAILED` o su
rechazo específico. Si el intento de publicación o su confirmación no permiten
establecer el resultado durable, devuelve `PUBLICATION_UNCERTAIN`. La aplicación
debe inspeccionar/reabrir la ranura; nunca asumir que no se guardó y sobrescribirla.
La incertidumbre de un snapshot aislado no bloquea el Core activo.
Un cierre concurrente invalida la generación inmediatamente: la respuesta tardía
puede ser `GENERATION_EXPIRED` aunque el snapshot haya llegado a disco.

## Recuperación controlada e identidad H03

LOAD admite una dirección técnica, nunca un jugador elegido por cliente.
`version=0` selecciona la versión más nueva con marcador `COMMITTED`. Ignora
preparaciones sin confirmar; no vuelve silenciosamente a una versión antigua
si una confirmada está corrupta. El llamante puede pedir expresamente una versión
anterior tras inspección.

Se valida el sobre y el registro, se copia el historial a un área operativa
independiente y se llama a `f04_history_open` en una sesión preparatoria.
Core comprueba manifiesto, checkpoint, segmentos originales, reducciones y esquema.
Se compara su UUID con la campaña admitida y su vínculo F05 con el hecho exacto
esperado. Se exige una persona actual admitida por F05. El ID numérico aislado
nunca basta: otra campaña con los mismos IDs se rechaza por UUID y un vínculo
sustituido/ausente se rechaza por su hecho persistente y persona.

Antes del swap se preparan el marcador opaco H03, el ámbito nuevo de F04 y una
generación H02 nueva. Tras superar las comprobaciones, el mismo propietario
publica la sesión, invalida las solicitudes pendientes de la generación anterior
y revoca selecciones y referencias antiguas. El cierre tiene precedencia si se
admitió durante preparación. Cualquier error anterior al swap conserva la sesión
válida y permite reintentar. No se llama a `f05_bind_player` para restaurar.

Los estados `FAILED` y `FAILED_RECOVERABLE` previos no habilitan operaciones
por sí mismos. Los fallos de preparación H04 vuelven a `ACTIVE` si había campaña,
o a `CLOSED` si no la había; el error normalizado conserva la causa operativa.
El cierre y las comprobaciones de vida mantienen los estados de fallo H02.

## Seguridad de rutas e inspección

En Linux se abren todos los componentes con `openat`, `O_DIRECTORY` y
`O_NOFOLLOW`; los accesos posteriores usan el descriptor fijado en `/proc/self/fd`.
Los descriptores se conservan mientras Core necesita su historial. La raíz debe
pertenecer al usuario y no permitir escritura de grupo/otros; las carpetas nuevas
se crean con modo 0700. Esto requiere Linux con procfs montado.

Windows mantiene abiertos los componentes con handles sin `FILE_SHARE_DELETE`,
rechaza reparse points, utiliza rutas locales extendidas y excluye UNC. La raíz
autorizada debe tener ACL privada de usuario; no se administra la seguridad de
cuentas del SO desde HOST. Ambos sistemas abren archivos sin seguir links,
comprueban tipo y número de enlaces, y excluyen escritores HOST con un lock del SO
que se libera al morir el proceso. La protección presupone un SO y usuario local
legítimos; un proceso del mismo usuario con control del ejecutable queda dentro
del riesgo residual offline de H01.

`SessionOwner::inspect` no escribe ni abre una campaña activa. Devuelve direcciones,
formato, compatibilidad, procedencia, recuperabilidad y un `Error` normalizado.
Valida Core en sesiones transitorias de solo lectura, creadas y destruidas en el
hilo de inspección. No reutiliza el Core activo ni devuelve contenido bruto,
identidades profesionales o conocimiento. `compatible` indica que el sobre H04 y
el pin declarado son compatibles; `recoverable` exige además validación completa
de Core y del vínculo. F04 devuelve `F04_SAVE` tanto ante corrupción como ante
algunos esquemas Core no admitidos: se conserva como `SAVE_CORRUPT` sin inventar
una distinción que la ABI no proporciona. El sobre o pin incompatibles sí devuelven
`SAVE_INCOMPATIBLE`. Sus resultados son una observación;
LOAD vuelve a validar una copia aislada y no confía en una inspección anterior.

## Uso interno y límites de alcance

```cpp
SessionOwner host(StorageConfig{authorized_private_root});
auto opened = host.open(config).get();
// Flujo nativo H03: prepare + bind del personaje legítimo.
auto campaign = host.campaign_id(opened.generation);
auto saved = host.save(opened.generation, "principal").get();
host.close().get();
auto resumed = host.restore({}, {campaign, "principal", 0}).get();
```

H05 sigue siendo responsable de la pasarela de juego; H07, de divulgación y
operaciones institucionales; H10, de callbacks UI/IA. H04 no implementa esas
superficies ni certifica HI-17/HI-18 completos. La comparación de RNG/cronología
se realiza sobre Core real, sin presentar poblaciones de ensayo como creación
definitiva del cadete o integración final de Unreal.
