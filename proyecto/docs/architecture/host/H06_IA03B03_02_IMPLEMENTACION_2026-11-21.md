# HOST H06 · IA-03B03-02 · Vínculo de Academia en H03

Entrega para auditoría independiente en la rama
`codex/host-ia03b03-02-vinculo-academy`, desde la revisión de arquitectura
`5f4b4a417a160af22de0dcaab21b2e0b008bd422`. El CoreRPG de todas las
composiciones está fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`.
[PR Draft #191](https://github.com/robdor80/Videojuego_StarTrek/pull/191) · [Base #190](https://github.com/robdor80/Videojuego_StarTrek/pull/190)

## Vínculo de la PERSON

`AcademyPlayerBinding::bind(SessionOwner&, Generation, const AcademyReceipt&)`
es una entrada C++ privada de TrekHost. La composición nativa llama a B02
para crear la campaña y entrega al vínculo la generación y el recibo opaco
que devuelve el factory. `SessionOwner` comprueba que la generación está
activa y que el recibo es el emitido para el intento, el perfil local y
el identificador de campaña vigentes. La PERSON es el protagonista S04 v2
con ascendencia paterna de Khan, cuyo `EntityId` asignó CoreRPG en esa
campaña. El nombre editable del candidato es un dato de la PERSON.

El trabajador coteja el recibo con `AcademyCampaign::inspect()` sobre el
WorldState existente. La inspección valida las definiciones del campus,
la PERSON y el hecho `candidate_created` en el catálogo de producto.
Comprueba que la relación de candidatura apunta al campus y que el hecho
tiene como sujeto únicamente a esa PERSON. También exige una sola PERSON,
un solo hecho de creación y cero plazas de población. La relación de fuente
apunta a una definición del catálogo `starfleet_academy/v2`, construido por
B02 a partir de los documentos aprobados de S04. El HOST coteja su huella,
los IDs de campaña, PERSON y hecho, el hash del nombre, la revisión del
WorldState y el tick del hecho con el recibo.

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

### Codex Cloud

Código probado en `9846bfddb49ae3cc3eeee667c51ca62984576b97` con Linux
x86-64, GCC 14.2.0, CMake 3.31.10 y Ninja.

| Comprobación | Resultado |
| --- | --- |
| Suite nativa Release | PASS 289/289. Incluye 134 HOST, 21 F04, 134 F05 y los ocho casos nuevos de H03. Cero omisiones. |
| Regresión aislada F11 | PASS 17/17 mediante `desarrollo/integration/f11_host/run_native.py`. |
| Linux GCC ASan/UBSan, casos B02 y B03T | PASS 23/23, con detección de fugas activada. |
| Repetición de cierre, concurrencia y reintento | PASS, 100 ejecuciones de cada uno de los tres casos. |
| Contratos H01, factory F10 histórico y S04 | PASS 11/11, 9/9 y 12/12 respectivamente. |
| Linux Release con `TREK_HOST_TESTS=OFF` | PASS de compilación, inspección de dependencias y exportaciones, carga de ABI C 1 y seis casos B03T con un consumidor externo enlazado al TrekHost Release. |
| Entrada al puente F05 desde Academia | PASS. Una sonda Linux interceptó `f05_bind_player` y `f05_player_binding`, la primera llamada de `bridge::dispatch`. El control positivo activó la sonda. Cinco recorridos de Academia, incluido B03T-02, finalizaron sin activarla. |

Para reproducir la suite nativa, configurar `desarrollo/integration/host`
en Release con `CORERPG_SOURCE_DIR` apuntando al checkout limpio fijado y
`TREK_HOST_TESTS=ON`. Compilar los objetivos del workflow y ejecutar la
misma selección con CTest.

```sh
ctest --test-dir "$build" -C Release --no-tests=error --output-on-failure \
  -R '^(host\.|f05\.|f04\.(history_faults|thread|scope|identity|class|buffers|determinism|population_.*|process_save|process_load)$)'
```

Para Release de producto, configurar un directorio de compilación distinto
con `TREK_HOST_TESTS=OFF`, compilar `TrekHost` y ejecutar
`tests/inspect_product.py` y `tests/inspect_abi.py` sobre ese directorio.

### GitHub Actions

La selección `HOST native H02-H06` terminó con **PASS 5/5** para la revisión
de implementación `9846bfddb49ae3cc3eeee667c51ca62984576b97`.
[Ejecución 44869391747](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44869391747)

| Trabajo | Resultado |
| --- | --- |
| Linux nativo HOST/F04/F05, H01 y F11 aislado | PASS |
| Windows MSVC x64 nativo HOST/F04/F05, H01 y F11 aislado | PASS |
| Linux ASan/UBSan, suite HOST | PASS |
| Linux Release con tests deshabilitados, inspección de producto y ABI | PASS |
| Windows x64 Release con tests deshabilitados, inspección de producto y ABI | PASS |

El workflow `HOST H01 — contratos documentales` también pasó.
[Ejecución 44869391752](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/44869391752)

B03T-04 a B03T-22, los casos históricos B03-03 a B03-12 de persistencia,
Unreal, MSI y OpenAI LIVE figuran `NOT_RUN` en esta subfase.

## Dependencias de B03-03

Academia devuelve `SAVE_INCOMPATIBLE` en B03-02. B03-03 deberá validar un
ancla duradera de perfil, campaña, PERSON, hecho y fuente sobre el mismo
WorldState, y restaurar catálogo e historia de Core en otra ejecución.
Al reabrir deberá reconstruir el vínculo H03 con una generación nueva. El
recibo de B02 de esta subfase tiene vigencia durante la activación local.
