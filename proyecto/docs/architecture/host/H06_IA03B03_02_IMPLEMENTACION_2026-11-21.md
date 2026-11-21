# HOST H06 · IA-03B03-02 · Vínculo de Academia en H03

Entrega para auditoría independiente. La rama de implementación parte de
`5f4b4a417a160af22de0dcaab21b2e0b008bd422`, revisión de arquitectura de la
[PR #190](https://github.com/robdor80/Videojuego_StarTrek/pull/190). El CoreRPG
de todas las composiciones está fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`.

## Vínculo de la PERSON

`AcademyPlayerBinding::bind(SessionOwner&, Generation, const AcademyReceipt&)`
es una entrada C++ privada de TrekHost. La composición nativa llama a B02
para crear la campaña y entrega al vínculo la generación y el recibo opaco
que devuelve el factory. `SessionOwner` comprueba que la generación está
activa y que el recibo es el emitido para el intento, el perfil local y
el identificador de campaña vigentes.

El trabajador coteja el recibo con `AcademyCampaign::inspect()` sobre el
WorldState existente. La inspección valida las definiciones del campus,
la PERSON y el hecho `candidate_created` en el catálogo de producto.
Comprueba que la relación de candidatura apunta al campus y que el hecho
tiene como sujeto únicamente a esa PERSON. También exige una sola PERSON,
un solo hecho de creación y cero plazas de población. La relación de fuente
apunta a una definición del catálogo `starfleet_academy/v2`, construido por
B02 a partir de los documentos aprobados de S04. El HOST coteja su huella,
los IDs de campaña, PERSON y hecho, el hash del nombre, la revisión y el
tick del hecho con el recibo.

El propietario vuelve a comprobar el ámbito al recuperar el mutex y publica
en un solo paso el recibo validado y `BOUND`. La proyección
`current_player(generation)` devuelve el ID de la PERSON de ese recibo y su
generación. La representación académica reside en H03 y reutiliza el recibo
como referencia al Core. La llamada es de solo lectura para el WorldState.

## Autoridad y ciclo de vida

`Dispatch` verifica el tipo de campaña en el trabajador después de comprobar
la generación y el vínculo. En Academia activa con `BOUND`, devuelve
`ACCESS_DENIED` para `query_view`, `submit_order`, `query_order`,
`cancel_order` e `institutional_command` antes de llamar al gateway de
`NativeSession`. La respuesta conserva la correlación y carece de proyecciones
operativas. La PERSON académica sigue siendo candidata y el vínculo le otorga
control de personaje. La apertura y el vínculo navales siguen su ruta H03 por
`PlayerBootstrap` y F05.

La cola serializa ambas solicitudes de vínculo y los reintentos B02. El
mismo recibo conserva el sujeto. Los recibos ajenos, vacíos o de otra
activación se rechazan por ámbito. Una generación cerrada devuelve
`GENERATION_EXPIRED`. El mutex de admisión queda libre durante la validación
Core para que `close()` pueda revocar inmediatamente el ámbito y la cola.
La comprobación posterior al recuperar el mutex impide una publicación
tardía. Un fallo de validación deja el vínculo en su estado anterior.

## Código y verificación

| Archivo | Cambio |
| --- | --- |
| `src/f10/academy_player_binding.h` | Entrada privada H03 basada en el recibo de B02. |
| `src/session_owner.cpp`, `include/trek/host/session_owner.h` | Admisión, cotejo de recibo, publicación, proyección, revocación y puerta naval. |
| `src/f10/academy_campaign.cpp` | Cardinalidad de las relaciones de candidatura y sujeto en Core. |
| `tests/academy_player_tests.cpp`, `CMakeLists.txt` | Casos sobre TrekHost compartido y pruebas deterministas de cierre y fallo en una composición de ensayo. |
| `tests/inspect_product.py`, `.github/workflows/host-h02-native.yml` | Verificación de frontera de Release y ejecución nativa en CI. |

| Caso | CTest `host.academy.*` | Oráculo |
| --- | --- | --- |
| B03T-01 y B03-01 histórico | `b03t_01` | Misma PERSON y generación antes y después de la adquisición del vínculo. |
| B03T-02 y B03-02 histórico | `b03t_02` | Cinco operaciones navales denegadas para Academy `BOUND` y revisión Core intacta. |
| B03T-03a | `b03t_03a` | Mismo recibo y sujeto tras repetir B02 y H03. |
| B03T-03b | `b03t_03b` | Rechazo de recibo vacío o ajeno, incluido un ordinal Core coincidente de otra campaña. |
| B03T-03c | `b03t_03c` | Cierre entre la validación y la publicación. Revocación inmediata del recibo, la cola y la generación. |
| B03T-03d | `b03t_03d` | Proyección H03 válida, denegación institucional y `SAVE_INCOMPATIBLE` en persistencia Academy. |
| B03T-03e | `b03t_03e` | Dos vínculos concurrentes, replay de creación, sustitución del nombre e intento de otro perfil. Una sola PERSON y un solo hecho. |
| Reintento tras fallo | `b03t_bind_retry` | Excepción antes de publicar, estado `UNBOUND` y reintento válido con el mismo recibo. |

### Ejecuciones

La selección GitHub Actions `HOST native H02-H06` incluye Linux y Windows
nativos, Linux ASan/UBSan y Release con `TREK_HOST_TESTS=OFF` en ambas
plataformas. El resultado de esta revisión se registra en la PR Draft.
Las pruebas de Unreal, MSI, OpenAI LIVE y B03T-04 a B03T-22 están `NOT_RUN`.

## Dependencias de B03-03

Academia devuelve `SAVE_INCOMPATIBLE` en B03-02. B03-03 deberá validar un
ancla duradera de perfil, campaña, PERSON, hecho y fuente sobre el mismo
WorldState, y restaurar catálogo e historia de Core en otra ejecución.
Al reabrir deberá reconstruir el vínculo H03 con una generación nueva. El
recibo de B02 de esta subfase tiene vigencia durante la activación local.
