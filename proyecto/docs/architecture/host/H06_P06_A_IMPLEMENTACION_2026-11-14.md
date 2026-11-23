# H06-P06-A · Implementación del validador F10

**Fecha** 14-11-2026. **Estado** Parcial. Comprobaciones nativas y puerto interno implementados. La configuración de producto devuelve `REVIEW_UNAVAILABLE` para un borrador que supera los rechazos deterministas.

## Superficie y autoridad

- `BiographyValidator::evaluate` recibe JSON no confiable y un `BiographyContext` de composición interna, con escenario, era, año, fecha si la política la autoriza, campaña, generación y perfil. El flujo de producto actual requiere fecha de inicio vacía. La biografía no lleva apodo, identificador de perfil, veredictos ni ámbitos. El validador acepta texto Unicode y estructuras acotadas y devuelve códigos con nombres de campo del contrato, evitando reproducir claves desconocidas, biografías y texto de proveedor.
- La evaluación objetiva devuelve un objeto interno que asocia el estado a las huellas de borrador y contexto y a la versión de reglas y política. Cualquier infracción determinista se resuelve antes de invocar un revisor. Las brechas de información producen `REVIEW_REQUIRED`. `BiographyAuthority::resolves` define el puerto futuro para verificar hechos concretos, incluidos el perfil y las referencias alegadas, sin permitir que se resuelva por esa vía una infracción ya demostrada.
- `SemanticEvaluator` recibe una vista del borrador canónico y su asociación exacta. El resultado contiene completitud, versión, identificador de revisión y hallazgos con código y campo. F10 comprueba asociación, identidad del evaluador fijada por composición, versión, formato y tamaño y delega la verificación de procedencia y hallazgos a `BiographyAuthority::verify`. Una revisión incompleta, contradictoria, obsoleta o inaccesible impide un resultado positivo. Los fallos de servicio se convierten en estado de revisión sin exponer excepciones.
- El caso positivo requiere `OBJECTIVE_VALID` y decisión F10 verificada. El recibo privado y movible conserva la evidencia, el borrador canónico y el contexto exactos. Su construcción depende de una instancia interna; `eligible` comprueba vigencia de instancia, versiones y contexto, y compara el borrador canónico de nuevo. Los SHA-256 correlacionan contenido. El recibo y las comprobaciones en memoria implementan la frontera. No hay ruta que reciba un recibo serializado o una cadena `validated_creation_ref` del cliente.
- El único constructor que inyecta los dos controles se compila con `TREK_F10_BIOGRAPHY_TESTING` en el ejecutable de ensayo. La DLL de producto compila el módulo con el constructor cerrado. Para habilitar un flujo real, F10 deberá revisar otra composición privada que configure sus fuentes y evaluador, y HOST deberá suministrar la activación actualmente vigente. Este corte no conecta un editor o un comando a la validación.

## Datos y representación

El generador toma las listas de campos y perfiles de fuentes versionadas, incorpora la matriz de tecnología existente y obtiene un SHA-256 de las fuentes canónicas. El identificador de reglas combina `f10-biography/1` con ese SHA-256. La política usa la identidad y versión del contrato H06-P06-A. Se debe actualizar la versión nativa al cambiar sus semánticas. El compilado usa estos datos embebidos, sin lecturas de contenido o servicios durante la evaluación.

En el borrador, los textos se conservan y el orden de las listas es significativo. El módulo usa la representación ordenada de jsoncons, sin espacios de formato y preservando precisión decimal. No intenta igualar la huella informativa del precheck Python. Para hechos de historia estructurados usa `started_at_or_age` y `ended_at_or_current` (edades enteras, fechas ISO o texto pendiente de revisión, con `current` permitido para un término abierto). `evidence_ref`, `technology_ref` y `technology_profile_ref` son referencias declaradas, no credenciales. Las reglas de fecha y disponibilidad solo se aplican cuando hay datos comparables. El límite de entrada es 65 536 bytes, profundidad 12. Los identificadores técnicos usan hasta 128 caracteres ASCII alfanuméricos, punto, guion, guion bajo y dos puntos. Máximo 32 hallazgos por revisión. Son decisiones técnicas del corte para acotar entradas y errores.

## Archivos

| Ruta | Función |
|---|---|
| [biography_validation.h](../../../../desarrollo/integration/host/src/f10/biography_validation.h) | Contrato privado, estados, puertos y recibo opaco. |
| [biography_validation.cpp](../../../../desarrollo/integration/host/src/f10/biography_validation.cpp) | Validación objetiva, asociación de revisión y comprobación de vigencia. |
| [embed_biography_rules.py](../../../../desarrollo/integration/host/src/f10/embed_biography_rules.py) | Proyecta y versiona las fuentes del validador en la compilación. |
| [biography_tests.cpp](../../../../desarrollo/integration/host/tests/biography_tests.cpp) | Entradas adversarias, doble control de ensayo, cambios tras revisión, privacidad y fallos. |
| [CMake HOST](../../../../desarrollo/integration/host/CMakeLists.txt) y [CI HOST](../../../../.github/workflows/host-h02-native.yml) | Compilan el módulo, registran los 13 casos y verifican la composición Release. |

La fase B, el alta de una PERSON, la vinculación H03, el guardado H04, la admisión y las pruebas Unreal están fuera del alcance del corte.
