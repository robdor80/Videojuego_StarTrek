# H06-P06-A · Resultados de validación nativa F10

**Fecha** 14-11-2026. **Base** `470aab8258eb07e4cabc4e3035bade7f71b43f5a` (PR #151). **Revisión técnica probada** [`e8d7e67c7571128bf1d74e364f6d1ca668339c52`](https://github.com/robdor80/Videojuego_StarTrek/commit/e8d7e67c7571128bf1d74e364f6d1ca668339c52). **CoreRPG** `76a7b7b485616d8c4994f384a90f123bf333591d`. El commit de entrega añade este informe. [PR #152 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/152), [Factibilidad](H06_P06_A_FACTIBILIDAD_2026-11-14.md), [Implementación](H06_P06_A_IMPLEMENTACION_2026-11-14.md).

## Verificación por entorno

| Entorno | Resultado | Evidencia |
|---|---|---|
| MSI, Windows x64, MSVC 19.51.36256.0, SDK 10.0.26100.0, CMake 4.4.3, Release ON | **253/253 PASS**. Incluye 13 casos nuevos y la regresión C11. | JUnit y logs locales, selección debajo. |
| MSI, Windows x64, Release OFF | **PASS**. Carga, pin y ABI 1 verificados. | Inspección local de archivos, exportaciones y ABI. |
| GitHub Actions, Windows x64, Release ON | **253/253 PASS**, 0 fallos y 0 omitidos. | [JUnit y logs Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626647/artifacts/14092326182). |
| GitHub Actions, Ubuntu, Release ON | **253/253 PASS**, 0 fallos y 0 omitidos. | [JUnit y logs Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626647/artifacts/14091962039). |
| GitHub Actions, Ubuntu Clang, ASan/UBSan, Release ON | **98/98 PASS**, 0 fallos y 0 omitidos. | [JUnit y flags ASan/UBSan](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626647/artifacts/14091667181). |
| GitHub Actions, Windows y Ubuntu, Release OFF | **PASS** en ambos. ABI y exportaciones verificadas. Ausencia de binario y constructores de ensayo en el producto. | [Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626647/artifacts/14091726428), [Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626647/artifacts/14092086435). |
| Contratos H01 y regresión F11 aislada | **11/11 H01** y **17/17 F11** en Windows y Linux. | [H01](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626648), [HOST](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540626647). |
| F10 Python | **78/78 PASS** en MSI (Python 3.10.11) y **78/78 PASS** en CI. El código fusionado de referencia enumera 20 casos de precheck y la ejecución conserva todos. La ejecución de CI de referencia se hizo en `aee8f37f`; el cambio posterior se limita al código y la prueba C++ de vigencia. | [F10 referencia](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540341767). |
| Academy Life | **20/20 scripts PASS** en MSI, manifiesto de 482 casos definidos. Auditoría, puente dinámico y suites PASS en CI. | [Academy Life CI](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43540346003). |
| Proveedor semántico y emisor de evidencia reales | **BLOCKED**. Sin configuración aprobada de F10. El resultado de producto `REVIEW_UNAVAILABLE` está probado y la conjunción positiva se ejecuta solo con los controles de ensayo. | Casos `production`, `conjunction`, `review`. |
| Candidato, admisión y aceptación Unreal | **NOT_RUN**. Corresponden a fases posteriores y no hubo cambios UE. | [Matriz de producto existente](F10_H06_P06_RESULTADOS_2026-11-14.md). |

SHA-256 de los JUnit CI: Windows `58fed65f1f7fdcf3dac1538bbc0ce23a2631cc277ddb32a9cbc9373b2fc8ea47`, Linux `7c6f0dabe0525c26848517e88415bb20b3c2f1a8b98696a44b0b821845d75954` y ASan/UBSan `d57cc56b16859dd663d36271df4f43db7a542042eba7e1b08cc939d5346d5bb4`.

## Casos nativos de H06-P06-A

El prefijo de CTest es `host.biography.`. Los controles tienen BIO y campaña ficticias y se limitan a la memoria del proceso de prueba.

| Caso | Oráculo |
|---|---|
| `production` | **PASS**. Composición por defecto, borrador pendiente y revisión indisponible, sin recibo. Declarar adultez no la acredita. |
| `fields` | **PASS**. Campo requerido ausente, apodo/identidad y escalado de autoridad en la raíz o en objetos internos. El evaluador no recibe el borrador rechazado. |
| `species` | **PASS**. Especies con perfil válido quedan pendientes de madurez, sin valor por defecto. Se rechazan IDs desconocidos, estados presentados como especies y la declaración de no adultez. |
| `chronology` | **PASS**. Nacimientos imposibles o posteriores a 2383, actividades anteriores al nacimiento, edades fuera de secuencia y hechos que dependen del día/mes de campaña. |
| `evidence` | **PASS**. Ciudadanía y certificaciones alegadas, incluida la asociada a una actividad, requieren evidencia. La restricción publicada de tecnología naval se aplica en el perfil y período explícitos. Alegar excepción abre revisión. |
| `context` | **PASS**. Se rechazan año distinto, fecha exacta de campaña sin decisión y generación vacía. |
| `malformed` | **PASS**. No-objeto, claves duplicadas incluso vía escape, comentarios, coma final, datos adicionales, UTF-8 inválido, exceso de tamaño y profundidad. |
| `conjunction` | **PASS**. Se exige evidencia objetiva y una decisión autenticable por el dominio. Una respuesta completa del evaluador de ensayo por sí sola no emite recibo. |
| `review` | **PASS**. Contradicción impide aprobar. Sugerencia con campo controlado deja el texto intacto. Correcciones exigidas por el dominio impiden el recibo. |
| `stale` | **PASS**. Cambios de nombre, especie, edad, educación, experiencia o precisión decimal invalidan el recibo. Se rechazan contexto, campaña, perfil, generación e instancia diferentes. Un resultado que vuelve tras renovar la activación queda ligado a la anterior. |
| `evidence_stale` | **PASS**. Se rechazan huellas, evaluador, versión de reglas y política discrepantes antes de pedir la decisión F10. |
| `failure` | **PASS**. Indisponibilidad, respuesta parcial y excepciones mantienen la puerta cerrada. El reintento usa la misma asociación sin consumir intención ni estado Core. |
| `privacy` | **PASS**. Los errores devuelven solo campos controlados y códigos. Claves de usuario, texto de respuesta y excepciones privadas no se proyectan. |

La validación opera en memoria y carece de acceso a una sesión Core, PERSON, RNG, disco, matrícula o registro de plazas. El positivo de la prueba demuestra la conjunción y vigencia requeridas para el consumidor futuro. Los casos CB-01–CB-24 conservan el resultado de producto del corte anterior (**22 BLOCKED, 2 NOT_RUN**). HU-08 sigue bloqueada. H06-P06 y M1 siguen parciales.

## Reproducción

Usar un checkout Core limpio en el pin, la composición HOST versionada y un directorio de compilación en la zona temporal ignorada. Redirigir `TMP`, `TEMP`, `TMPDIR` y `F04_TEST_TEMP_ROOT` a esa zona. En Linux omitir `-A x64` y añadir `-DCMAKE_BUILD_TYPE=Release`. El [workflow HOST](../../../../.github/workflows/host-h02-native.yml) contiene los targets de la regresión completa, flags de sanitizadores y comandos de inspección Release OFF.

```powershell
cmake -S desarrollo/integration/host -B "$build" -A x64 "-DCORERPG_SOURCE_DIR=$core" -DTREK_HOST_TESTS=ON
cmake --build "$build" --config Release --target host_biography_tests host_abi_tests
ctest --test-dir "$build" -C Release -R '^(host[.]biography[.]|host[.]abi[.]unsupported_academy_open$)' --no-tests=error --output-on-failure
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m unittest discover -s desarrollo/tools/validation -p 'test_f10_*.py' -v
python desarrollo/tools/generation/run_academy_life_suite.py
```

La compilación MSI reutilizó las fuentes de jsoncons en el pin `bcb44594c50c495ee1e690602cdd71455942ad0e` en modo de solo lectura. En el primer ensayo local se corrigió el tratamiento de etiquetas de cadena del parser y se deshabilitaron sus comentarios por defecto. Los reintentos de la suite dirigida verificaron la corrección. Una repetición local de la regresión sobre el mismo build encontró un archivo previo en la prueba histórica F05 de escritura entre procesos. Se repitió la batería en un build limpio para conservar los artefactos anteriores y respetar su precondición de salida nueva. Los resultados brutos y las compilaciones permanecen en el laboratorio ignorado. Se registró en la PR la exclusión del worktree bloqueado de la limpieza concurrente.
