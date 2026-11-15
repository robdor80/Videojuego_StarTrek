# HOST H06 / IA-03A — Implementación de reglas iniciales F10

Fecha: 15/11/2026. Base: `11193316dc83b5e967fcc9adaccf581292054c8c` (PR #166). Entrega para auditoría independiente, sin fusión. No certifica H06, Unreal, PERSON ni OpenAI LIVE.

## Alcance y precedencia

Se implementan las seis decisiones autorales definitivas de `H06_IA03A_AUDITORIA_DISENO_REGLAS_F10_2026-11-15.md`. La política nueva `sistemas/gameplay/character_creation/f10_initial_player_rules_v0.1.json` es aditiva y prevalece en la composición de creación inicial sobre las cláusulas históricas de ciudadanía, expedientes y obligatoriedad. No se editan contratos LOCKED, el formulario histórico v0.3, la política de madurez de 26 especies, CoreRPG (`76a7b7b485616d8c4994f384a90f123bf333591d`) ni F11.

La ruta utilizada es el validador C++ existente, su registro de evidencias y el adaptador IA-02. Los programas Python/formularios web son referencias offline históricas; no son la autoridad nativa. `BiographyValidator{}` conserva la composición histórica acotada, útil para políticas y pruebas de las otras especies. La composición productiva **de jugador inicial** se obtiene explícitamente con `RegisteredBiographyAuthority::for_initial_player`; esta restringe la selección a humano/vulcano/híbrido. La API pública C del HOST sigue sin abrir una campaña Academia ni crear candidatos: esto no se presenta como integración IA-03B/IA-03C.

## Archivos y motivos

| Archivos | Cambio |
|---|---|
| `src/f10/biography_validation.cpp`, `.h` (bajo `desarrollo/integration/host/`) | Normalización inicial, evaluadores por incidencia, restricción de selección, ciudadanía automática, clasificación institucional, comprobaciones temporales mixtas, coexistencia de actividades y elegibilidad con perfil vigente. Ruleset nativo `/6`. |
| `src/f10/biography_evidence.h` | Composición interna inicial con dos fuentes nativas; conserva registro, vinculaciones y precedencia de contradicciones/revocaciones. |
| `src/biography_profile_source.h`, `src/session_owner.cpp`, `include/trek/host/session_owner.h` | Proyección privada del perfil local y activación de creación emitidas por el propietario HOST. Caducan al renovar, cerrar, abrir, restaurar o destruir el propietario. Sin ABI nueva ni operaciones PERSON. |
| `sistemas/gameplay/character_creation/f10_initial_player_rules_v0.1.json` | Decisiones versionadas, campos neutrales, alcance de especies, clasificación y complemento de instrucciones semánticas. |
| `src/f10/embed_biography_rules.py`, `CMakeLists.txt` | Empotrado y huella de la política nueva, dependencias de reconstrucción y prueba nativa nueva. Sin lectura de laboratorios en producto. |
| `src/f10/openai_biography.cpp` | Complemento de instrucciones exclusivamente para el ruleset inicial. Necesidad: las instrucciones históricas IA-02 dicen no inferir ciudadanía por especie; la decisión posterior exige que F10 la asigne sin revisión. No cambian servicio, transporte, modelos, verificación ni contrato de respuesta IA-02. |
| `tests/initial_biography_tests.cpp` | Regresiones con constructores productivos, propietario HOST real y solo transporte OpenAI simulado; sin fabricar fuentes SUPPORTED. |
| `tests/biography_tests.cpp`, `tests/biography_rules_generation.py`, `desarrollo/tools/validation/test_f10_species_maturity_policy.py` | Oráculo de coexistencia actualizado, versión `/6` y prueba de invalidación por cambio del contenido de la política nueva. |
| `.github/workflows/host-h02-native.yml` | Incluye el ejecutable nuevo en Windows/Linux y sanitizadores existentes. |
| Este informe | Evidencia permanente, límites y entrega a fases posteriores. |

## Reglas y normalización

- Selección inicial: `human`, `vulcan`, `human_vulcan_hybrid`. Mínimos 18/25/22, leídos de la política de madurez empotrada existente. Otras especies conservan sus políticas históricas y no pasan la selección inicial, incluidos los casos especiales y DLC.
- Ciudadanía: F10 asigna `Federación Unida de Planetas` a las tres especies, independientemente del lugar. No hay petición de documentos ni validación IA de ciudadanía. Las cadenas canónicas federadas o neutrales se normalizan; una estructura de autoridad o una afirmación legal distinta no se descarta silenciosamente para conseguir aceptación.
- Esenciales: nombre, especie, edad/fecha, condición adulta, origen, apariencia y objetivo conservan las comprobaciones existentes. Los campos canónicos complementarios omitidos `culture_context`, `prior_education`, `prior_experience`, `prior_activities_and_hobbies` reciben `No declarado`. Los demás opcionales permanecen ausentes. No se inventa educación general, familia, empleo ni afición. El borrador del llamante no se modifica.
- Origen: libre, incluso estación/nave/colonia inventada; no se consulta catálogo ni se publica un lugar en CoreRPG. La IA sigue revisando coherencia del relato con 2383.
- Formación/experiencia/certificaciones: admite cadenas narrativas y colecciones/objetos personales reconocidos, sin diplomas ni expedientes previos. Cada colección se evalúa completa. Las fechas y edades estructuradas contradictorias se rechazan antes de IA. El doctorado civil de un personaje de 30 años puede llegar a revisión semántica y conservarse íntegro en el borrador canónico del recibo. No se convierte en texto decorativo ni en puntos numéricos.
- Aficiones: se comprueban sus periodos individuales; el solapamiento o la cantidad por sí solos no prueban incompatibilidad. Karate desde 8, piano desde 10, natación desde 12 y astronomía desde 15 con edad 25 pasan la puerta objetiva. La plausibilidad de la carga y logros queda en la revisión semántica obligatoria.
- Instituciones: afirmaciones explícitas de capitanía/servicio/permisos y roles estructurados institucionales quedan pendientes sin llamada a IA ni recibo. La aspiración futura a ser capitán sí llega a IA. Mencionar una nave Starfleet o un familiar capitán no atribuye rango al jugador. No se crean hechos institucionales por ningún resultado F10/IA.

Las comprobaciones de fechas mixtas usan intervalos conservadores de año cuando solo se conoce la edad. Rechazan un periodo antes de cualquier nacimiento posible o un final inequívocamente anterior al inicio, sin inventar el día/mes de campaña. Se mantiene pendiente el cumpleaños en el umbral histórico no decidido.

## Fuentes internas y seguridad

`BiographyProfileSource::begin(SessionOwner&)` es una entrada **privada C++ del HOST**, no UI, Blueprint, ABI ni IA. Requiere propietario CLOSED y genera dentro del HOST identidad opaca de perfil local, ámbito de creación y generación no nula mediante las utilidades existentes. Reutiliza la identidad local dentro del mismo propietario; renovar la activación cambia ámbito/generación y caduca la anterior. Su capacidad débil solo vive mientras el propietario mantiene la activación. No abre Core, crea cuentas, servidores o autenticación, ni usa una PERSON como perfil.

Esta proyección cubre la etapa **anterior a PERSON**; no es un perfil persistido ni un vínculo de campaña H03. La continuidad duradera de identidad y el traslado del ámbito de creación a una campaña real deberán ser autorizados por IA-03B. No reutilizar su identificador de ámbito como si ya fuera una campaña persistida.

Composición interna prevista:

```cpp
auto profile = trek::host::detail::BiographyProfileSource::begin(owner);
auto authority = RegisteredBiographyAuthority::for_initial_player(profile, openai_adapter);
BiographyValidator validator(authority);
auto result = validator.evaluate(draft, profile->context());
```

El adaptador es el `OpenAiBiographyEvaluator` real sobre el servicio IA-01 compartido. Si `begin` no devuelve perfil válido, el consumidor debe tratarlo como no disponible; aun componiendo sin perfil el validador mantiene pendiente `PROFILE_EVIDENCE_REQUIRED`.

Las fuentes registradas son `f10_initial_player_rules/0.1.0` (F10, `VALIDATED_INITIAL_BACKGROUND`) y `host-h03-local-profile/ia03a.1` (HOST, `APPROVED_RULE`). F10 emite una atestación por incidencia solo tras comprobar sus condiciones; el perfil solo se respalda si coincide todo el contexto y sigue viva la activación. No se importan fuentes ni registros del formulario o de OpenAI. Las instantáneas positivas no pueden sustituir la evaluación de las fuentes nativas; sí se aplican contradicciones/revocaciones registradas para el mismo binding. Las fuentes/instantáneas son inmutables: una modificación requiere reemplazar autoridad y validador, como exige el puerto existente; sus recibos no cruzan emisores.

Cada atestación se vincula a borrador **normalizado canónico**, contexto completo (perfil, ámbito, generación, escenario, era, fecha), ruleset, hash de fuentes y política. El sufijo `initial-player/0.1.0` separa esta composición de la histórica. Cambiar contenido de política cambia el hash aunque se conserve su versión nominal. Los recibos privados conservan el contenido biográfico y la revisión con procedencia verificable para IA-03B; no contienen permisos de alta.

Se rechazan claves de autoridad, incluso anidadas, antes de normalizar ciudadanía para impedir que una sustitución oculte una inyección. Un `evidence_ref` narrativo no resuelve ni acredita nada. Una contradicción objetiva cancela la revisión anterior y evita solicitar otra. La revisión semántica fallida, incompleta, sin clave o no registrada no produce recibo. `eligible` revalida además la activación local y la procedencia IA-02; cierre/destrucción/renovación invalidan el recibo.

La clasificación léxica es una defensa objetiva acotada para afirmaciones explícitas y roles estructurados; no constituye comprensión completa del lenguaje natural. Paráfrasis, ironía, ambigüedad, plausibilidad del doctorado y contradicciones expresadas solo en prosa requieren IA-02. Ni la fuente F10 ni una respuesta COHERENT otorgan hechos globales, rango, plaza o permisos.

## Pruebas y resultados

Los resultados de compilación nativa y CI se completarán tras la ejecución en curso. No se consideran PASS por estar descritos.

Resultados locales ejecutados hasta esta revisión:

| Suite | Resultado |
|---|---|
| Python F10 (`unittest discover ... -p 'test_f10*.py'`) | 163/163 PASS |
| Python HOST H01 | 11/11 PASS |
| Python F04/F05 referencia | 22/22 + 22/22 PASS |
| Python F11 | 355/355 PASS |
| Ejecutable IA-03A, primera ejecución | PASS; fuentes productivas y transporte simulado |
| OpenAI LIVE | NOT_RUN; no se acredita comportamiento real del modelo |

El primer pase histórico detectó oráculos de versión `/5` que se actualizaron a `/6`; la coexistencia antes bloqueada también tiene nuevo oráculo. No se presenta el transporte simulado como LIVE.

### Matriz A01–A18 aplicada

| Caso | Cobertura reproducible |
|---|---|
| A01 | `initial_player`: humano 20, campos complementarios ausentes, origen inventado, ciudadanía automática, revisión IA-02 y recibo verificado. |
| A02 | `initial_player` sin clave, y `openai` con errores HTTP, timeout e incompletos: sin recibo. |
| A03–A05 | `initial_player`: humano 17, vulcano 24, híbrido 21 y actividades posteriores a edad; cero solicitudes. |
| A06 | `initial_player`: humano 20, vulcano 25, híbrido 22, ciudadanía automática. El oráculo antiguo andoriano/tellarita se sustituye: no seleccionables inicialmente. |
| A07 | Oráculo histórico corregido: doctorado/certificación ficticios plausibles sí llegan a IA; no se exige expediente. Evidencias falsas/estructuras desconocidas siguen sin resolver. |
| A08 | `initial_player`: pasado institucional pendiente y sin solicitudes; experiencia de investigador civil aceptable sin rango. |
| A09–A10 | `initial_player`, `registered_sources`, `evidence_policy`, `openai`: identidad/contexto falsos, claves anidadas, emisores o evidencias no pueden elevar autoridad. |
| A11–A12 | `initial_player`, `evidence_stale`, `evidence_conflicts`, `background_provenance`, `rules_generation`: cambio de campos, contexto, fuentes/política, contradicción/revocación y recibo de otro emisor. |
| A13–A14 | `initial_player`: especiales/DLC no seleccionables. Las suites históricas conservan sus oráculos de madurez pendiente/DLC y políticas intactas. |
| A15 | `initial_player`: cuatro aficiones simultáneas, incluida certificación marcial, pasan objetivo y necesitan semántica; `personal_background` actualiza el veto antiguo al solapamiento. |
| A16 | `initial_player`: aspiración futura válida frente a capitanía pasada no acreditada. Mención a familiares/naves no se convierte en servicio del jugador. |
| A17 | `openai`, `provenance`: COHERENT/procedencia manipulada no verificable no crea recibo. |
| A18 | `initial_player`, `stale`, `openai`: edición/contexto/generación/renovación/cierre/restauración impiden reutilizar recibo. |

## Riesgos, limitaciones y fases siguientes

- No hay prueba OpenAI LIVE ni certificación de su calidad semántica. Se necesita una ejecución LIVE controlada antes de certificar el recorrido real completo.
- Los objetos estructurados fuera del vocabulario reconocido quedan pendientes; no se firma cualquier JSON. IA-03C debe mapear su formulario a los campos canónicos y representar ausencias con el adaptador inicial; no enviar el wrapper v0.3 con claves de perfil/persona al validador.
- IA-03B deberá consumir el recibo vigente y volver a comprobar elegibilidad/propietario, crear exactamente una PERSON, fijar antecedentes validados como hechos reales, vincular H03 y persistir H04 de manera autorizada. Ninguna de esas operaciones se implementa aquí. La fuente local es efímera hasta esa integración.
- Capacidades, efectos de titulaciones y conocimiento/reacciones de NPC corresponden a sus dominios posteriores; no existen puntos de habilidad, diálogos asistidos o simulaciones de esos efectos en IA-03A.
- IA-03C conserva pendiente toda interfaz Unreal y la proyección visual del formulario. El prototipo histórico no se altera ni se declara productivo.
- F11, admisión a Academia y autoridad CoreRPG no cambian.

## Laboratorio y eliminación

Por instrucción expresa de entrega se documenta la ruta temporal: `laboratorios/host/ia03a/`. Contiene checkout limpio del Core fijado, herramientas locales, compilaciones, registros y resultados de pruebas. Está ignorado y no se incluye en commits. No se borran ni modifican laboratorios históricos. El código definitivo, contratos, CMake y pruebas no leen ese laboratorio ni dependen de sus binarios o scripts; los directorios de compilación y checkout Core se suministran como entradas de prueba. Se puede eliminar el laboratorio completo cuando el propietario lo autorice. Este informe conserva resultados, no lo convierte en dependencia.
