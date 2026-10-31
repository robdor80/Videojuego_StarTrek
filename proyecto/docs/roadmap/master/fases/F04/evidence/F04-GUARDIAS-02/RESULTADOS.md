# F04-GUARDIAS-02 — Resultados y reproducción local

31-10-2026. Base `4436bb444bcfae17941edc84d856d756ac5f6929`.
Rama `codex/f04-guardias-02-miranda-intrepid`. Worktree `C:/F04/Guardias02`;
laboratorio aislado `C:/F04/GuardiasBuild`. Entrega Draft, sin fusión ni cierre F04.

[Diseño completo, las 66 secciones, viabilidad y rendimiento](../../F04-GUARDIAS-02_MIRANDA_INTREPID_TRES_GUARDIAS.md).

## Resultado

| Nave | Nominal / secciones | Referencia Alpha / Beta / Gamma / Fuera | Cobertura crítica 28 días | Déficit no crítico 28 días |
|---|---|---|---|---:|
| Miranda | 130 / 32 | 53 / 18 / 13 / 46 | 672/672 | 278 |
| Intrepid | 160 / 34 | 64 / 23 / 16 / 57 | 672/672 | 349 |

Máximo ordinario móvil siete días: cinco. Una guardia por día natural. Descanso
mínimo observado: 16 h, superior a las 12 h exigidas. Alpha preservada por sección
en el día de referencia. Las carencias posteriores se conservan por departamento
y ventana. No se alteran personas, competencias, destinos ni nominales.

## Validación real

| Suite | Resultado | Evidencia |
|---|---|---|
| F04 completo, cinco clases | 243/243: 187 anteriores + 56 nuevas, cero omitidas | [XML](f04.xml), [salida](native.txt) |
| F02 recompilado desde esta rama | 15/15 | [XML](f02.xml) |
| F03 recompilado desde esta rama | 25/25 | [XML](f03.xml) |
| CoreRPG completo + Content JSON | 447 PASS, 4 omitidas, cero fallos | [XML](core.xml), [salida](core.txt) |
| UE 5.8.2 Win64 NullRHI | 25/25 Success, cero advertencias asociadas a tests | [reporte](unreal-report.json), [log](nullrhi.txt) |
| F04/Miranda/F03/F02 documentales | 22+4+26+9=61/61 | `test_*.txt` |
| LORE-03 A | 56/56 | [salida](lore03-a-tests.txt) |
| Fixture autoridad / roadmap | PASS / PASS | [fixture](authority-fixture.txt), [roadmap](roadmap.txt) |
| Referencias globales | FAIL previo: 566 idénticas a main, cero nuevas | [comparación](reference-regression.json), [salida](references.txt) |
| Guardados producidos por la DLL anterior, cinco clases | Mismo futuro en todos los casos | [compatibilidad y hashes](compatibility.json) |

Las cuatro omisiones Core son permisos y symlinks no soportados por esta plataforma;
no se cuentan como superadas. La compilación UE conserva advertencias de cabeceras
del motor y MSVC posterior al preferido: [log de compilación](unreal-build.txt).
NullRHI comprueba UWorld, proyección selectiva, persistencia y simulación lógica;
no acredita nave 3D jugable. Cero Actors automáticos de dotación.

La regresión Valhalla conserva 1.800 Flota, 400 civiles, 40 navales Defiant y 60
Marines, estos dos últimos incluidos en Flota. Mantiene las tres guardias, 90
secciones, separación de competencias y rechazo atómico al acumular más historial.
Sovereign y Odyssey mantienen sus tablas exactas. Los archivos de contenido
protegidos y el ABI público se comparan con la base: [protección](protection.json).

Nuevos casos por perfil: referencia exacta, 7/14/28 días, 28 sin sembrar referencia,
autoridad/sucesión, baja, cancelación, cancelación intermedia, revocación antes de
cancelar, suplencia, carencia total de sensores, descanso protegido de mando,
insuficiencia real de mando, medicina, descanso, vacaciones, deuda, dotación parcial,
caducidad, migración, roundtrip, Alpha heredado con continuidad, ampliación tras
cargar, corrupción semántica, solicitudes inválidas y dos procesos guardar/cargar.

## Proyecciones y rendimiento

Cada subcarpeta [Miranda](miranda/simulations.json) e
[Intrepid](intrepid/simulations.json) contiene:

- `positions.csv`: plazas y personas Core originales con guardia del día de referencia.
- `qualified-capacity.json`: efectivos habilitados y cotas semanales por servicio.
- `critical-windows-{1,7,14,28}-days.json`: cada ventana completa, proveedor y primer hueco.
- `roster-28-days.csv` y `gaps-28-days.json`: actividades y carencias reales.
- `performance.json`: planificación, creación, instalación, bootstrap, manifiesto,
  cobertura, guardado, carga, avance, Working Set y Peak Working Set del proceso.
- `incident-performance.json`: baja tras cargar, candidatos y sustitución autorizada;
  recuperación de cobertura y conservación de destinos e historial.
- `dll-provenance.json`: SHA-256 de la DLL medida.

En 28 días, Miranda: 2.074 actividades DUTY, 3.380 entidades, archivo 986.132 bytes.
Intrepid: 2.535 actividades DUTY, 3.938 entidades, archivo 1.158.923 bytes. Los
`.f04` reales quedan en el laboratorio; se verifica su tamaño en disco.
Memoria incluye Python/ctypes, buffers y copias transaccionales, no heap Core aislado.
Medidas puntuales con validaciones concurrentes, sin percentiles ni garantías.

## Comandos reproducibles

Desde la raíz del worktree, con checkout Core limpio en cada pin:

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04/GuardiasBuild/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04/GuardiasBuild/native --config Release --parallel 4
ctest --test-dir C:/F04/GuardiasBuild/native -C Release --no-tests=error --output-on-failure -j 4 --output-junit C:/F04/GuardiasBuild/f04.xml
cmake -S desarrollo/integration/f02 -B C:/F04/GuardiasBuild/f02 -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/core-f02
cmake --build C:/F04/GuardiasBuild/f02 --config Release --parallel 4
ctest --test-dir C:/F04/GuardiasBuild/f02 -C Release --no-tests=error --output-on-failure --output-junit C:/F04/GuardiasBuild/f02.xml
cmake -S desarrollo/integration/f03 -B C:/F04/GuardiasBuild/f03 -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/core-f03
cmake --build C:/F04/GuardiasBuild/f03 --config Release --parallel 4
ctest --test-dir C:/F04/GuardiasBuild/f03 -C Release --no-tests=error --output-on-failure --output-junit C:/F04/GuardiasBuild/f03.xml
ctest --test-dir C:/F04/core-build -C Release --no-tests=error --output-on-failure -j 4 --output-junit C:/F04/GuardiasBuild/core.xml
```

Core completo usa el build existente con Content JSON habilitado. Pins limpios:
F04 `c147d81ed069da2e09149613ab02cbc3ebe95a4a`;
F03 `9c53a33787de13d91eb2abe4da07033ee0fa1dc1`;
F02 `4f282863737bcd8f5add401202a9e1064c133672`.

```powershell
./desarrollo/integration/f04/run_f04.ps1 -Stage Stage -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/GuardiasBuild -F02NativeBuild C:/F04/GuardiasBuild/f02 -F03NativeBuild C:/F04/GuardiasBuild/f03 -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage Unreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/GuardiasBuild -F02NativeBuild C:/F04/GuardiasBuild/f02 -F03NativeBuild C:/F04/GuardiasBuild/f03 -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage TestUnreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/GuardiasBuild -F02NativeBuild C:/F04/GuardiasBuild/f02 -F03NativeBuild C:/F04/GuardiasBuild/f03 -F02CoreSource C:/F04/core-f02
python desarrollo/integration/f04/collect_guardias_evidence.py --build-root C:/F04/GuardiasBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-GUARDIAS-02/miranda --profile 1
python desarrollo/integration/f04/collect_guardias_evidence.py --build-root C:/F04/GuardiasBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-GUARDIAS-02/intrepid --profile 2
python desarrollo/integration/f04/check_guardias_compatibility.py --previous-build C:/F04/ValhallaBuild/native --new-build C:/F04/GuardiasBuild/native --output C:/F04/GuardiasBuild/compatibility.json
python desarrollo/integration/f04/package_guardias_evidence.py --build-root C:/F04/GuardiasBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-GUARDIAS-02
```

Los logs `f04-tests.txt`, `core-tests.txt`, `unreal-tests.txt`, `native-build.txt`
y `references-{base,current}.txt` se conservan en BuildRoot. El empaquetador copia
los resultados, verifica hashes de DLL nativa/staged, pins y ausencia de regresión.
Los comandos documentales usan `python -m unittest discover -s desarrollo/tools/validation -p`
para `test_f04_reference.py`, `test_f04_miranda_example.py`, `test_f03_reference.py`
y `test_validate_f02_contracts.py`; también `test_lore03_a.py`,
`f04_reference.py --fixture desarrollo/validation/fixtures/f04/authority_watch_acceptance_v0.1.json`,
`validate_roadmap_state.py` y `validate_internal_references.py`. Este último se ejecuta
tanto en main/base como en la rama y se comparan las 566 líneas completas de error.

## Persistencia y límites abiertos

ABI 1/SCHEMA 4 reutilizados; SCHEMA 3→4 explícito. Los archivos históricos no se
reescriben al cargar. Las listas anteriores de cobertura se conservan en SCHEMA 3.
No cambia formato, límites Core ni organización nominal. Se prueba recuperación
tras Alpha antiguo y ampliación de guardias tras carga, y la conservación de bajas,
cancelaciones, historia resuelta y destinos. Los bytes de campañas completas y su
futuro coinciden entre procesos y con los productores anteriores.

Los planes siguen siendo finitos, con 1–28 días por llamada. Las ocho coberturas
no significan médico cirujano permanente, funcionamiento de todas las tareas de
cada sección, ni tolerancia a bajas ilimitadas. Las noches reducen funciones no
críticas, sin considerarlas fallos críticos. No se afirma un óptimo global.

El límite de historial acumulado permanece asignado a **F04-PERSISTENCIA-03**.
No se inicia esa subfase ni se eleva el techo de 65.536 entidades/64 MiB. No se
certifican campañas de un año. Tampoco se cierra F04 ni se ejecuta INTEGRACION-04.
No hay modificaciones de CoreRPG genérico, Blender, modelos, puentes, texturas,
mapas, respaldos o recursos artísticos. Sin Computer Use ni control de ratón/teclado.

[Procedencia de fuentes, Core, compilador y DLL](build-provenance.json).
[Listado completo de archivos cambiados](files-changed.txt).
