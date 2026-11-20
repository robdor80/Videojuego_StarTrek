# HOST H06 · IA-03B02 · Protagonista canónico S04 v2

Fecha 2026-11-20. Entrega para auditoría independiente. La rama B02 parte de
`799c23eaaea8d3785af88d48add3c3348ccfd66a`, HEAD de la PR #188 de arquitectura
B01, abierta en Draft al iniciar el trabajo. La PR B02 apunta a esa rama.
El Core de todas las composiciones se fija en
`76a7b7b485616d8c4994f384a90f123bf333591d`.

## Arquitectura

El punto de entrada C++ privado `AcademyCandidateFactory` vive en el HOST.
`begin` emite un intento opaco para el perfil local de `SessionOwner`, con
identidad de campaña generada por el HOST y generación reservada. `create`
admite un objeto JSON con un único `display_name`. El máximo es 1024 bytes
para el objeto y 96 bytes de UTF-8 para el nombre decodificado. Se rechazan
campos duplicados o adicionales, nombres vacíos, espacios en los extremos,
controles, caracteres invisibles seleccionados y codificación inválida.
La identidad del nombre usa sus bytes decodificados, incluida la distinción
entre formas Unicode canónicamente equivalentes. Las variantes de escape
JSON del mismo nombre conservan la identidad.

La cola del dueño ejecuta F10 en su hilo de Core. F10 valida la fuente y
construye en memoria un catálogo `startrek.academy` 2.0.0 con el esquema de
contenido Core 0.1.0. El escenario de producto es `starfleet_academy/v2` y
sitúa la candidatura en 2383. El calendario exacto sigue pendiente. El tick
`0` del hecho es tiempo relativo de la campaña.

`AcademyCampaign` crea el campus y pide a `WorldState::create_entity` el
identificador de la PERSON. Asocia la definición `person`, la relaciona con
el campus como candidata y genera la entidad de hecho `candidate_created`,
con ella como sujeto. Especie, parentesco, antecedentes y fuente quedan
en definiciones ligadas y relaciones de Core. Las referencias a la madre y
al padre describen sus especies. La referencia histórica identifica el linaje
paterno de Khan. La campaña contiene una sola PERSON y carece de población
de cadetes. Campaña y nombre se codifican en relaciones persistibles de bytes
ordenados porque el pin carece de un campo de texto libre por entidad.

La identidad estable es la pareja **ID de campaña, EntityId de Core**.
`EntityId` pertenece al WorldState, por lo que dos campañas pueden usar el
mismo ordinal para personas distintas. La campaña queda activa únicamente al
publicar la PERSON, el hecho y la procedencia juntos. El titular local sigue
sin vínculo jugable H03 en B02.

## Procedencia y validación

| Entrada empotrada | Identidad y versión | SHA-256 de UTF-8 con finales LF |
| --- | --- | --- |
| Contrato de ejecución F10 | `f10_fixed_candidate_factory` 2.0.0 | `df7f7a564cb1cb8dd989b5e70672db8d14ac0e7f9e8587c8d5a49afd3769a27b` |
| Contrato autoral S04 | `s04_fixed_player_protagonist` 2.0.0 | `e2a61bc3984df99123edd9072eae3b6755e24267dd0fa5c2bd727f45b84d90ba` |
| Biografía autoral | `s04_player_khan_vulcan_male` 1.0.0 | `abb04e51348a906433028b5585e1a0cc9c5386725f2e5557dc8d8857a3fc47d9` |

La generación de CMake verifica los dos archivos autorales. En ejecución el
factory vuelve a verificar las huellas contra la política fijada, los
identificadores, las versiones y las invariantes de los documentos aprobados.
La definición fuente incorpora las versiones y la huella
`19317d97ef8f8e14483e544f0f7babab5c312f8c6f64c832ad47fb4936d35bc8`, obtenida
con SHA-256 sobre la concatenación de las tres huellas hexadecimales de la tabla
en ese orden. La fuente y la autoridad se seleccionan internamente. F10 v2
usa procedencia determinista y la ruta de biografías libres conserva su puerta
semántica de IA-03A v1.

La fuente conserva explícitamente los valores nulos o pendientes. El WorldState
omite afirmaciones sobre el lugar y la fecha exacta de nacimiento, los nombres
de los padres, la cadena genealógica, maestros, instrumentos, títulos y
certificados cuando carecen de dato aprobado. Fuerza, reflejos, resistencia y
las cuatro maestrías quedan como antecedentes cualitativos. Su traducción a
capacidades de juego requiere reglas de dominio posteriores.

## Idempotencia y publicación

El HOST conserva un solo intento por campaña y el recibo privado queda ligado
al intento, perfil local, generación, campaña, fuente, huella del nombre,
PERSON, hecho, tick y revisión de Core. La misma solicitud devuelve el mismo
recibo. Un nombre distinto con el mismo intento devuelve
`IDEMPOTENCY_CONFLICT`. La lectura verifica el recibo vigente y confronta sus
datos con el WorldState y el catálogo en el hilo propietario. La API de lectura
tiene como entrada el recibo emitido por el HOST y devuelve una proyección.

Antes del commit se valida un checkpoint Core en memoria. La reserva exclusiva
que ya usa H02 impide publicar dos campañas activas. El último paso bajo el
mutex mueve el WorldState ya construido y publica la generación, el ID y el
recibo. Ante una excepción, un cierre durante la preparación o una reserva
ocupada se destruye el estado preparatorio y el recibo queda sin publicar. Al
cerrar caducan intento y recibo. El flujo naval requiere su vínculo F05 y el
guardado o la carga naval ante una Academia activa se rechazan por
incompatibilidad. B02 termina en candidatura, con cero plazas, rangos y
concesiones navales.

## Archivos

- `sistemas/gameplay/careers/academy_path/f10_fixed_candidate_factory_contract_v2.json`
  define la política aditiva de producto.
- `desarrollo/integration/host/src/f10/{embed_fixed_candidate.py,academy_campaign.h,academy_campaign.cpp,academy_candidate_factory.h}`
  empotra y verifica la fuente, compone el catálogo y construye la campaña.
- `desarrollo/integration/host/{include/trek/host/session_owner.h,src/session_owner.cpp,src/native_session.h,src/native_session.cpp}`
  integran la cola, la autoridad, el ciclo de vida y la publicación.
- `desarrollo/integration/host/{CMakeLists.txt,tests/academy_candidate_tests.cpp,tests/inspect_product.py}`
  integran producción, aceptación, fallos aislados e inspección de Release.
- `.github/workflows/host-h02-native.yml` incluye B02 en la matriz nativa
  y comprueba el artefacto de producción.
- Este informe registra las decisiones y la evidencia de entrega.

## Matriz B02 y ejecuciones

La mayoría de los casos ejecutan el C++ privado de la misma biblioteca
`TrekHost` que compone el producto. B02-07, B02-11 legado y B02-12 usan una
compilación separada de las mismas fuentes con inyección de fallos. La
composición de fallos comprueba también serialización y recarga en memoria del
WorldState real con el catálogo de producto. B02-14 usa las suites históricas.

| Casos de la matriz | Evidencia | Estado |
| --- | --- | --- |
| B02-01 a B02-10 | `host.academy.b02_01` a `host.academy.b02_10` | Pendiente |
| B02-11 | `host.academy.b02_11` y `host.academy.b02_11_legacy` | Pendiente |
| B02-12 y B02-13 | `host.academy.b02_12`, `host.academy.b02_13`, regresión F11 | Pendiente |
| B02-14 | `host.biography.*` y rechazos de B02-05 | Pendiente |
| B02-15 | `host.academy.b02_15` | Pendiente |

### GitHub Actions

El workflow `HOST native H02-H06` cubre Linux y Windows nativos, Linux
ASan/UBSan y compilaciones Linux/Windows Release con tests deshabilitados.
El informe se actualizará con las ejecuciones del código de entrega.

## Dependencias para B03

B03 debe autorizar el vínculo académico del perfil a la PERSON verificada,
definir el slot tipado Academy y restaurar catálogo, hechos, identidad e
idempotencia con renovación de generación. Hasta ese guardado, la garantía de
B02 abarca la sesión en memoria. La transición de admisión, la matrícula y
la integración Unreal pertenecen a fases posteriores. MSI, Unreal y OpenAI
LIVE quedan en estado NOT_RUN para este encargo.

Las compilaciones locales, el Core limpio, los logs y las herramientas de
verificación son temporales. El código y los tests se construyen directamente
desde el repositorio con un checkout de Core en cualquier ruta autorizada.
