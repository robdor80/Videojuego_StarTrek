# H04-AUD-01 — Publicación inicial del registro

Fecha: 2026-11-13. PR #135, Draft, rama `feature/host-h04-persistencia-recuperacion`.
Implementación inicial: `57de710603f4c85e93768de1f582d45da3fe33c7`.
Producto final: `b993efaeede0fcfae801ae0b8217f0e133570494`
(precisa el fallo definitivo de colisión).
Commit final de código/pruebas: `a191d239503cb72ebe7a19384581330da3d018dd`
(usa separadores nativos en la raíz del ensayo de colisión Windows).
Estado: CORREGIDA. Regresión local y suites HOST Windows/Linux en Actions: PASS.
H04 sigue NO CERTIFICADA y NO FUSIONADA.

## Causa

`SlotStore::save` invocaba `write` directamente sobre `registry/<campaña>` cuando
no existía. `write` crea el destino exclusivo y puede ser interrumpida entre dos
escrituras. El archivo definitivo parcial sobrevivía, y el siguiente SAVE intentaba
parsearlo como registro establecido. La identidad legítima no podía reintentarlo.

## Corrección y protocolo

Solo se cambia la publicación inicial del registro. Bajo el lock existente y un
directorio fijado por descriptor/handle, se crea `registry/pending-<id aleatorio>`
con creación exclusiva. Se reutiliza `write`: escritura completa, flush/fsync,
cierre comprobado y sincronización de directorio aplicable. Un temporal parcial
nunca tiene el nombre hexadecimal de una campaña y ningún lector lo admite como
su registro. Los restos se conservan; cada reintento elige un temporal nuevo.

Después se publica sin reemplazo: Linux usa `renameat2` con `RENAME_NOREPLACE`;
Windows usa `MoveFileExW` con `MOVEFILE_WRITE_THROUGH`, sin
`MOVEFILE_REPLACE_EXISTING`. No se reutiliza el helper `publish` de versiones,
porque su rename POSIX permite reemplazo. No hay fallback a rename reemplazante.
Una entrada creada entre comprobación y publicación no se sobrescribe.

Se sincroniza el directorio y se verifica el contenido publicado. La fase incierta
se delimita desde el intento de publicación hasta completar esta confirmación.
Antes del intento, los errores son `PERSISTENCE_FAILED` o el rechazo específico;
durante publicación/confirmación se devuelve conservadoramente
`PUBLICATION_UNCERTAIN`. Una colisión explícita EEXIST/FILE_EXISTS/ALREADY_EXISTS
confirma que no se publicó el temporal y devuelve `PERSISTENCE_FAILED`. Tras confirmación
se restablece la clasificación normal para las operaciones posteriores del SAVE.

Un registro definitivo preexistente se lee y compara con la identidad como antes;
no se regenera ni se repara automáticamente. Un registro antiguo ya corrupto se
conserva y rechaza: esta corrección previene nuevos registros parciales, no intenta
inferir el contenido legítimo de archivos dañados existentes.

## Archivos y funciones

- `desarrollo/integration/host/src/slot_store.cpp`: bloque de registro inicial en
  `SlotStore::save`; reutiliza `write`, `read`, `sync_dir` y cierres comprobados.
- `desarrollo/integration/host/tests/persistence_tests.cpp`: `audit_registry`,
  modos de proceso `aud_crash` y `aud_retry`.
- `desarrollo/integration/host/tests/persistence_process.py`: escenario H04-AUD-01
  integrado en el CTest y workflow Windows/Linux existentes, sin nueva dependencia.

## Prueba específica

Un primer proceso crea, vincula con H03 y guarda mediante el HOST real una campaña
con historial archivado y RNG consumido en una raíz semilla de ensayo. Se utiliza
ese mismo UUID y estado Core en una raíz destino sin registro: esto permite
reanudar el ensayo de una campaña idéntica entre procesos sin añadir al producto
una API para elegir UUID ni inventar identidad tras un crash.

Un segundo proceso inicia el primer SAVE en el destino con el `SlotStore` real y
termina mediante `_Exit(73)` en `partial_write`. El controlador comprueba que no
existe el nombre definitivo. Un tercer proceso reintenta sobre el mismo destino:
confirma el guardado, repite con registro válido, rechaza otra identidad y compara
el registro byte a byte para verificar que no se modifica. Inyecta además una
entrada válida concurrente en `registry_before_publish`: la publicación exclusiva
falla sin reemplazarla. Finalmente recupera con SessionOwner/Core real, contrasta
campaña y personaje y compara el checkpoint Core completo con el del primer
proceso. El callback de snapshot de este ensayo copia el historial semilla completo;
la restauración final usa los validadores reales, nunca carga el checkpoint de
comparación como campaña.

Resultado local Linux/GCC: PASS, 55/55 regresiones HOST, incluido
`host.persistence.process` con H04-AUD-01. Las expectativas históricas no cambian.

## Compatibilidad y riesgos residuales

Se mantienen el pin Core `76a7b7b485616d8c4994f384a90f123bf333591d`, formatos Core,
fuentes históricas, oráculos y frontera F11. Linux requiere soporte de
`renameat2(RENAME_NOREPLACE)` del kernel/filesystem; si falta se rechaza sin usar
una sustitución insegura. Windows conserva las garantías de flush/write-through
existentes y requiere la raíz privada autorizada. No se ensayan cortes eléctricos
físicos. Los temporales incompletos consumen espacio hasta limpieza explícita.
El guard histórico F11 A02-02 sigue siendo un FAIL conocido por alcance congelado;
no se modifica ni se interpreta como certificación de esta corrección.

## Evidencia CI

[HOST run 43453368894](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43453368894),
commit `a191d239503cb72ebe7a19384581330da3d018dd`:

| Verificación | Resultado |
|---|---|
| Linux GCC, HOST y regresiones F04/F05 | PASS, 210/210 |
| Windows x64 MSVC, HOST y regresiones F04/F05 | PASS, 210/210 |
| Linux Clang ASan/UBSan, HOST | PASS, 55/55 |
| Release producto tests OFF, Linux y Windows | PASS |
| H04-AUD-01, procesos y colisión | PASS, incluido en `host.persistence.process` de ambas plataformas |
| Corte eléctrico físico | NOT_RUN |
| Nuevas campañas históricas fuera de la corrección | SKIP, fuentes y oráculos intactos |
| Guard F11 A02-02 | FAIL conocido por alcance congelado, no relajado |

[H01](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43453368798): PASS.
[Guard F11 A02-02](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43453369288):
FAIL de alcance, conservado. La matriz HOST incluye su regresión F11 aislada,
sin enlazar ese emisor con el producto. Las cancelaciones de workflows duplicados
sobre fuentes F04/F05 intactas no se presentan como PASS.

Los resultados previos de H04 no se sustituyen. Esta incidencia corregida no
constituye certificación ni autorización de fusión de H04.
