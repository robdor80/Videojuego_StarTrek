# F04-MIRANDA-01 — Resultados reales (2026-10-30)

F04 permanece **EN_CURSO**. Base `main` y `origin/main`, sincronizadas al inicio
y tras fetch final: `c214910eb7e2f9c9c9ad258c98fdee5b45783e21`.
Rama: `codex/f04-miranda-organizacion-20261030`.
Worktree aislado: `C:/F04/Miranda01`; compilaciones: `C:/F04-Miranda01`.

| Validación | Resultado |
|---|---|
| F04 nativo, MSVC Release | **86/86**, sin fallos ni omisiones: 64 regresiones y 22 casos nuevos |
| F02 nativo | **15/15**, sin fallos |
| F03 nativo | **25/25**, sin fallos |
| CoreRPG completo con Content JSON | **447 superadas, 4 omitidas, 0 fallos**, 451 registradas |
| Unreal 5.8.2, Win64 Development, NullRHI | **19/19**, 0 fallos, 0 casos con advertencias de test, 0 pendientes |
| Referencias unitarias F04 / Miranda-120 / F03 / F02 | **22 + 4 + 26 + 9 = 61**, todas superadas |
| Fixture de autoridad F04 y validador de roadmap | **PASS** |
| Snapshot operativo de Alpha | **130 plazas asignadas, 7 departamentos, 32 secciones, 53 personas de servicio**, déficit Alpha 0 |
| Compatibilidad SCHEMA=1 y SCHEMA=2 anterior | Carga/guardado idénticos byte a byte; fixtures creadas con DLL previa |
| Compatibilidad SCHEMA=3 | Organización, agendas, funciones, relevos y autoridad conservados; futuro determinista entre procesos |

Los cuatro casos omitidos por Core son los de manifiesto ilegible y tres de
enlaces simbólicos cuando la plataforma no aplica sus condiciones. Sus nombres
exactos constan en `results.json` y `core.xml`. No se contabilizan como superados.

F04 y Unreal se recompilaron desde esta rama. F02/F03 reutilizaron sus builds
existentes sin cambios y se ejecutaron de nuevo; `build-provenance.json` compara
sus directorios fuente con los de esta rama y consulta los SHA Core de las DLL.
F02 conserva Core `4f282863737bcd8f5add401202a9e1064c133672`, F03 conserva
`9c53a33787de13d91eb2abe4da07033ee0fa1dc1` y F04 conserva
`c147d81ed069da2e09149613ab02cbc3ebe95a4a`.

La primera pasada F04 tuvo una aserción fallida en el caso Alpha vacío: el campo
`record` estaba siendo usado como recuento aunque la ABI lo define como EntityId.
Se corrigió para devolver la nave y consultar los recuentos por separado. Las
pasadas finales reflejadas en los JUnit están completamente superadas.

El ejemplo Beta/Gamma usa seis personas de servicio por ventana y un médico
localizado, con agendas y nombramientos Core reales. No valida descansos,
vacaciones ni continuidad semanal. Al terminar, el déficit vuelve a ser visible.
`coverage_validated=0` permanece explícito. NullRHI no acredita jugabilidad
gráfica completa. El compilador instalado MSVC 14.51.36256 es posterior a la
versión preferida por Unreal 5.8; el laboratorio compila y pasa sus pruebas.

## Comandos ejecutados

```powershell
cmake -S C:/F04/Miranda01/desarrollo/integration/f04 -B C:/F04-Miranda01/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04-Miranda01/native --config Release --parallel 4
ctest --test-dir C:/F04-Miranda01/native -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Miranda01/evidence/f04.xml
ctest --test-dir C:/F04/core-build -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Miranda01/evidence/core.xml
ctest --test-dir C:/F04/f02-native -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Miranda01/evidence/f02.xml
ctest --test-dir C:/F04/f03-native -C Release --no-tests=error --output-on-failure --output-junit C:/F04-Miranda01/evidence/f03.xml
```

Desde la raíz del worktree se ejecutó `run_f04.ps1` en las etapas `Stage`,
`Unreal` y `TestUnreal`, con `-CoreSource C:/F04/CoreRPG`,
`-BuildRoot C:/F04-Miranda01`, `-F02NativeBuild C:/F04/f02-native`,
`-F03NativeBuild C:/F04/f03-native`, `-F02CoreSource C:/F04/core-f02`.
El runner valida que el informe Unreal contenga exactamente 19 éxitos.

También se ejecutaron los comandos documentales del workflow
`.github/workflows/f04-native-integration.yml`: unittest de F04, Miranda-120,
F03 y contratos F02; fixture `authority_watch_acceptance_v0.1.json`;
`validate_roadmap_state.py`. Los logs textuales se incluyen aquí.

## Evidencia y protección

`f04.xml`, `f02.xml`, `f03.xml` y `core.xml` contienen los resultados CTest.
`results.json` contiene los 19 nombres y estados de Unreal, sus contadores y
el informe local completo de origen. `alpha-snapshot.json` proyecta desde la
DLL final los 130 ID de plaza, persona, sección, departamento, requisitos,
guardia efectiva y función. No contiene personajes inventados.

Los **20.051 archivos existentes** inventariados en el checkout principal y
Core conservaron ruta, tamaño y mtime; no hubo modificaciones ni desapariciones.
Esta comparación es de metadatos, no un hash exhaustivo del contenido. El SHA-256
de `.git/info/exclude` permanece idéntico. Ambos árboles tracked quedaron limpios.

Durante la tarea se observaron diez archivos nuevos de texturas en el respaldo
original TABULA RASA, fuera de las rutas de escritura de este trabajo. Se dejaron
intactos y se registran aparte en `results.json`; no se incorporan a la PR ni se
atribuyen a la implementación. La PR solo modifica integración y documentación
F04. No cambia CoreRPG, recursos artísticos, mapas, respaldos ni exclusiones.

Pendiente de autor/validación: rangos, matrícula, detalles de equipos y cantidades
no aprobadas, modalidad de urgencias y régimen de descansos. No se implementan
F05/F11/F12, no se fusiona la PR y no se cierra F04.
