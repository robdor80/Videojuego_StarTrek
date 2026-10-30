# F04-INTREPID-01 — Resultados ejecutados

Fecha: 2026-10-30. F04 **EN_CURSO**. Base `main`/`origin/main` verificada en `9e5f46eb1ff364f66e41d913cb64ce5ce232b4c2`. Rama `codex/f04-intrepid-organizacion`. Entrega PR Draft, sin fusión; SHA final y número de PR en el informe de entrega y la PR.

| Validación | Resultado |
|---|---|
| F04 nativo, MSVC Release, Core real | **107/107**, cero fallos y omisiones: 87 regresiones y 20 casos Intrepid |
| F02 nativo, dependencia original | **15/15** |
| F03 nativo, dependencia original | **25/25** |
| Core completo, Content JSON activo | **447 superadas, 4 omitidas, 0 fallos**, 451 registradas |
| Unreal 5.8.2, Win64 Development, NullRHI | **20/20**, cero fallos, advertencias de test u omisiones |
| Referencias F04 / Miranda-120 / F03 / F02 | **22 + 4 + 26 + 9 = 61**, todas superadas |
| Fixture de autoridad F04 y roadmap | **PASS** |
| Snapshot Alpha consultado a la DLL | **160 plazas, 160 personas distintas, 7 departamentos, 34 secciones, 64 trabajadores distintos, déficit cero** |
| Archivos antiguos SCHEMA=1/2 | Regresión de carga/guardado idéntico byte a byte superada |
| Archivo Sutherland SCHEMA=3 de DLL anterior | Carga/guardado idéntico y futuro determinista superados con ejecutable nuevo |
| Instalaciones holocubierta | JSON y referencias existentes verificados; **solo contrato mínimo**, ejecución de reservas/instalaciones no implementada |

Los cuatro casos Core omitidos son las condiciones de manifiesto ilegible y enlaces simbólicos dependientes de plataforma; sus nombres exactos constan en `results.json` y `core.xml`. **No se contabilizan como superados**. NullRHI acredita integración lógica, UWorld y Actors, sin demostrar una escena gráficamente jugable completa.

## Correspondencia con las comprobaciones solicitadas

| Nº | Comprobación | Evidencia ejecutada |
|---:|---|---|
| 1–4 | 160 plazas, 7 departamentos, 34 grupos y subtotales | `f04.intrepid_structure`, `alpha-snapshot.json`, [listado completo](../../F04-INTREPID-01_PLANTILLA_160.md) |
| 5–6 | 64 personas Alpha distintas, sin duplicados | `f04.intrepid_alpha`, `structure`, snapshot |
| 7–9 | Asignación, liberación, vacantes y traslados | `assignment`, `vacant`, `partial`, `transfer`, `lifecycle` |
| 10 | Persistencia de secciones y responsabilidades | `roundtrip`, `process_save`, `process_load` |
| 11 | Guardias y relevos | `beta_gamma`, `patterns`, `deficit_relief`, `rest`; regresiones anteriores 3×8/4×6 |
| 12 | Capitán, primer oficial y guardia | `authority`, `watch_fallback`; `f04.organization_authority_boundary` de Miranda |
| 13 | Jefe de seguridad con función táctica | `functions`, `alpha`, `authority`, Unreal Intrepid |
| 14 | Operador distinto de mantenedor | `qualifications`: sensores, científicos, transportadores, ordenadores y recursos sin reparación implícita; Ingeniería repara deflectores |
| 15 | EMH fuera de las 160 personas | `structure`, contrato de capacidades, snapshot sin identidad EMH |
| 16 | Holocubiertas sin 3D | Contrato mínimo permitido por alcance; sintaxis, referencias e inicialización no disponible verificadas; **sin prueba de ejecución runtime** |
| 17 | Independencia de jugador | Pruebas nativas sin jugador; Unreal `IntrepidOrganizationOffscreen` sin Actors automáticos y futuro idéntico tras desmaterializar |
| 18 | Guardado y carga | `roundtrip`, `corrupt`, `process_save/load`, fixtures SCHEMA=1/2 y archivo previo SCHEMA=3 |
| 19 | Regresión Miranda | Todos los casos `f04.organization_*`, población y muestra anteriores, Unreal Sutherland, comparación con DLL previa |
| 20 | Regresión F02/F03/F04 | JUnit completos y referencias documentales |
| 21 | CoreRPG real | Compilación de la DLL contra Core fijado; suite Core completa con JSON |
| 22 | Unreal 5.8.2 | Compilación real y 20 automatizaciones F02/F03/F04 con UWorld/Actors |

Los nombres abreviados en las filas corresponden a `f04.intrepid_<nombre>`. Beta/Gamma son ejemplos finitos con siete personas de servicio y un médico localizado diferente por ventana; no se aprueban cifras definitivas, descansos ni cobertura garantizada 24/7. Al terminar se exponen los déficits reales; `coverage_validated=0` permanece explícito.

## Procedencia y compatibilidad

F04 y Unreal se compilaron en `C:/F04-Intrepid01` desde esta rama. F02 y F03 reutilizan sus builds previos, con **todas sus fuentes comparadas por SHA-256** contra las de esta rama antes de volver a ejecutar sus suites. `build-provenance.json` registra esa comparación, los pins Core y las huellas de DLL. La DLL F04 usada por Unreal coincide por SHA-256 con la validada nativamente y con la del snapshot final.

Core F04: `c147d81ed069da2e09149613ab02cbc3ebe95a4a`. F02 conserva `4f282863737bcd8f5add401202a9e1064c133672`; F03 conserva `9c53a33787de13d91eb2abe4da07033ee0fa1dc1`. No se cambia Core ni sus fuentes.

El archivo previo Sutherland procede del ejecutable y DLL ya existentes en `C:/F04-Miranda01/native/Release`, sin recompilarlos con Intrepid. Se ejecutó su `process_save` y el `process_load` nuevo sobre sus bytes y su futuro. El archivo tiene 95.346 bytes, SHA-256 `74293b73a94c0823b2ac43a9db1e17afef2156213f0a48df038a6514ca5f9738`; el futuro tiene SHA-256 `55e78d943d68b1afaaf3d080f9c0bd09d9b1e2bec21d205f93d37ea890b69955`. Las huellas del productor constan en la procedencia. Los archivos binarios locales se mantienen fuera de Git; los fixtures históricos SCHEMA=1/2 ya estaban versionados y sus pruebas se repiten.

La primera compilación detectó que la extracción del helper de pruebas había arrastrado una función dependiente de `F04_FIXTURE_DIR` al ejecutable Intrepid. Se devolvió esa función a las pruebas Miranda; la compilación final y todos los casos pasan. Las advertencias del compilador de Unreal sobre cabeceras de Epic/toolchain no se contabilizan como advertencias de test; el informe final tiene cero advertencias de automatización.

## Comandos principales

Desde la raíz del repositorio:

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04-Intrepid01/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04-Intrepid01/native --config Release --parallel 4
ctest --test-dir C:/F04-Intrepid01/native -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Intrepid01/evidence/native.xml
ctest --test-dir C:/F04/core-build -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Intrepid01/evidence/core.xml
ctest --test-dir C:/F04/f02-native -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Intrepid01/evidence/f02.xml
ctest --test-dir C:/F04/f03-native -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Intrepid01/evidence/f03.xml
```

Se ejecutó `desarrollo/integration/f04/run_f04.ps1` en las etapas `Stage`, `Unreal` y `TestUnreal` con `-CoreSource C:/F04/CoreRPG -BuildRoot C:/F04-Intrepid01 -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02`. El runner exige exactamente 20 éxitos. Tras la última compilación nativa se volvió a preparar y comprobar Unreal para asegurar la misma DLL.

Las cuatro suites documentales, fixture de autoridad y roadmap se ejecutaron con los comandos del workflow `.github/workflows/f04-native-integration.yml`. Sus salidas están versionadas aquí.

Recogida reproducible de resultados y listado de plazas, desde la DLL real:

```powershell
python desarrollo/integration/f04/collect_intrepid_evidence.py --build-root C:/F04-Intrepid01 --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-INTREPID-01 --roster proyecto/docs/roadmap/master/fases/F04/F04-INTREPID-01_PLANTILLA_160.md
```

## Archivos, protección y límites

Se modifican únicamente integración F04 y documentación F04. El motor compartido de organización/persistencia queda intacto; se añade el perfil y su identificador, pruebas, contrato mínimo y evidencias. El helper de pruebas Miranda se extrae a `organization_lab.h` para reutilizarlo sin duplicarlo; su comportamiento y aserciones permanecen. El runner y README actualizan el recuento de pruebas Unreal. No se modifican arte, Blender, modelos, texturas, puentes, respaldos, exclusiones, dotaciones de otras clases ni estados globales de fase. La comprobación de alcance se basa en el diff Git; no se presenta como un inventario hash de todos los recursos artísticos.

Los archivos `f04.xml`, `f02.xml`, `f03.xml`, `core.xml`, `unreal.json`, `results.json`, `build-provenance.json` y `alpha-snapshot.json` contienen resultados y procedencia. Los nombres y estados completos de los 20 casos Unreal constan en `unreal.json`. Los logs de compilación y campañas binarias se conservan localmente en `C:/F04-Intrepid01`.

Pendientes: rangos, configuración individual de instalaciones/aforos/vehículos, validación de descansos y suplencias, modalidad sanitaria nocturna, ejecución futura de reservas y vida cotidiana, auditoría independiente e integración posterior. Las holocubiertas no se publicitan como funcionalidad runtime ya ejecutable. No se fusiona la rama y F04 sigue **EN_CURSO**.
