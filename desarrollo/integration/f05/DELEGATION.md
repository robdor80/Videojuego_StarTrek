# F05-P02: delegación efectiva sobre F04/CoreRPG

Incremento nativo para auditoría independiente. Depende de P01 PR #81,
HEAD base `854aa5720ec8681d6e5eccc7fe4ed80ac0c65d9b`; PR apilada contra
`codex/f05-p01-orders`. No modifica #81/#78, sus ramas ni el estado global.
CoreRPG main permanece fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`.
No fue necesario modificar Core ni crear una PR en ese repositorio.

## Contrato ejecutable

La API aditiva [f05_delegation.h](include/f05_delegation.h) conserva la ABI P01.
`f05_delegate` crea una entidad **`trek.f04:delegation`**, el mismo tipo de F04;
el vocabulario opcional P02 identifica ámbito Sensores, permiso de emitir
`F04_SCAN`, una estación y un ejecutor. No concede cualificaciones, puestos,
presencia física, mando de nave ni permisos de `F04_POLICY`.
Las delegaciones F04 antiguas de política siguen sus reglas originales.
Todos los cambios de relaciones pasan por `ActionEngine`; toda persistencia
usa `CampaignPersistence` o `HistoryPersistence` con el mismo `F04Session`.
Core posee los hechos; Trek interpreta la autoridad de la Flota Estelar.
No se atribuye a Core un ACL de Star Trek incorporado ni existe almacén lateral.

El delegante debe ser el **mando efectivo contemporáneo** que devuelve F04,
disponible, cualificado y con el nombramiento de origen aún vigente. Puede
ser el capitán o el sucesor que F04 realmente habilite. El rango no interviene.
El receptor debe ser militar de la nave primaria, cualificado en mando y tener
un nombramiento admitido vigente (mando/XO/sucesión/guardia o jefatura Sensores).
Se fija ese nombramiento concreto. Un oficial de guardia requiere además
servicio real; en SCHEMA4 también se comprueba servicio del receptor.

La duración no puede exceder ninguno de los dos nombramientos de origen ni
las credenciales actuales de mando. La pertenencia, disponibilidad, cualificación,
nombramientos y mando del delegante se vuelven a comprobar al usar el mandato.
El plazo de cada orden tampoco puede exceder el de la delegación.
La subdelegación con `parent != 0` devuelve `F05_UNSUPPORTED`; ser delegado
no permite crear otro mandato como si se fuese capitán.

## Ciclo persistente y modos

`f05_delegate` crea `draft`, sin autoridad. `f05_change_delegation` activa,
suspende, revoca o registra caducidad. `revoked` y `expired` son terminales.
La reactivación de `suspended` es una operación explícita del mando actual,
con nueva revisión y todas las comprobaciones de origen. No hay reactivación
implícita. Cambiar el modo también crea un evento persistente.
Cada evento guarda actor, causa, revisión de entrada, tick Core y evento anterior.
El registro no reescribe eventos anteriores. `f05_delegations_page` permite
recuperar el inventario desde Core después de cargar; las consultas solo muestran
mandatos propios o accesibles al mando actual.

`effective_code` separa el estado administrativo de la habilitación actual:
un mandato activo puede estar inhabilitado por tiempo, relevo, ausencia médica,
baja de la nave o pérdida de autoridad. La caducidad es efectiva exactamente
en `end`, aunque el Host todavía no haya solicitado el evento `expired`.
La pérdida de autoridad conserva el evento causal F04 y el resultado fallido
de la orden; no fabrica una revocación administrativa automática.
La API F04_REVOKE devuelve `F04_REVIEW` para mandatos enriquecidos: usar la
transición P02 para conservar su cadena de eventos. F04_REVOKE mantiene su
comportamiento para las delegaciones antiguas de política.

- `manual`: el delegante decide explícitamente cada orden con `f05_approve_order`.
- `proposal_requires_approval`: la propuesta permanece `issued` sin tarea ni efecto;
  recibirla devuelve `F04_REVIEW` hasta que el delegante actual aprueba.
- `delegated_autonomous`: puede aceptarse y ejecutarse dentro del mandato activo.

Una aprobación es otra entidad causal Core vinculada a la orden y a la delegación;
no elimina las comprobaciones posteriores. Cambiar un mandato aceptado a un modo
que requiera aprobación provoca fallo de ejecución `F04_REVIEW` si no existe
aprobación. Debe emitirse otra orden para solicitar aprobación; no hay reintento
oculto ni modificación de la orden ya cerrada. No se desarrollan IA ni iniciativa.

## Orden pendiente y efecto real

`f05_submit_delegated` fija el mandato en la petición P01, incluso si el oficial
adquiere después otro cargo. Recepción y ejecución revalidan ese mandato.
No se sustituye silenciosamente por autoridad independiente del emisor.
Una revocación entre aceptación y ejecución crea un intento/resultado P01 fallido,
`performed=0`; no se llama a la tirada Core. Una orden completada antes conserva
su resultado y todos sus eventos. No hay reversión de efectos confirmados.

El único efecto operativo admitido sigue siendo el `F04_SCAN` real de P01:
`ActionEngine::process(StreamRollAction{0xF0401,1,100})`. No hay contactos F06,
reservas de recursos ficticias ni cambios de turnos simulados como efecto real.
La estación, cualificación Sensores, servicio, presencia, identidad, disponibilidad,
revisión del mundo y plazo del ejecutor siguen comprobándose por F04/P01.

## Persistencia, repetición y límites

Se conserva la transacción por copia F04/P01: un fallo no publica media mutación.
La creación y los cambios comparten un espacio P02 de keys por campaña; P01
conserva su espacio de solicitudes de órdenes. Mismo key y payload devuelve el
estado actual sin otro evento; payload diferente produce `F05_IDEMPOTENCY_CONFLICT`.
Cada orden incluye el mandato en su payload idempotente. Las aprobaciones se
repiten por orden y payload de aprobación. La restauración verifica formas,
referencias, límites y cadenas de eventos antes de sustituir la sesión viva.
Los scopes se renuevan al cargar. La publicación durable sigue siendo explícita.

Máximos: 256 mandatos P02, 4096 eventos de delegación y las 512 órdenes P01
existentes. Se conservan tombstones y dependencias residentes para repetición
segura. No hay retención escalable nueva, servidor multihilo ni autenticación de red.
La ABI es de Host nativo de confianza. Un permiso de emitir órdenes no impide
que un Host privilegiado solicite por separado operaciones F04 que ya tenía.

El build P02 carga archivos F04/P01 anteriores. Los builds antiguos rechazan
las nuevas definiciones o relaciones desconocidas; no existe migración inversa.
Los seis oráculos históricos F04 y su procedencia se mantienen byte a byte;
solo se actualiza la huella del puente y se conserva expresamente la previa.
Las seis campañas de regresión usan sus pins y oráculos originales, mientras
P02 prueba su persistencia histórica con el Core fijado por P01.

## Reproducir

Mismos requisitos y comandos de compilación que [README](README.md).
`OUTPUT` y `CORE_SOURCE` son rutas del operador a un directorio temporal permitido
y al checkout Core fijado, respectivamente; no son dependencias permanentes.

```sh
cmake -S desarrollo/integration/f05 -B "$OUTPUT" -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR="$CORE_SOURCE"
cmake --build "$OUTPUT" --config Release --parallel 4
ctest --test-dir "$OUTPUT" -C Release -R '^f05\.' --no-tests=error --output-on-failure
ctest --test-dir "$OUTPUT" -C Release -E 'history_campaign_|persistence_baseline_|persistence_resume_' --no-tests=error --output-on-failure
```

Los tests `f05.p02_*` incluyen casos de mandato válido, ámbito, autoridad, receptor,
revocación, suspensión, caducidad, relevo, origen, incapacidad médica, subdelegación,
modos/aprobación, cambio de modo, idempotencia, causalidad corrupta, población F04,
inventario/restauración y persistencia monolítica/histórica entre procesos.
