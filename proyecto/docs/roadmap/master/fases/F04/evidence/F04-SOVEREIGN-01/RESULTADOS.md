# F04-SOVEREIGN-01 — Evidencias de ejecución

Base: `ff975c8b9d4b02ba8fe2a3f36d2b184f95a6ecee`. Rama `codex/f04-sovereign-organizacion-tres-guardias`. F04 EN_CURSO; entrega Draft sin fusión.

- `native.xml`: 136/136 (107 regresiones y 29 Sovereign).
- `f02.xml`, `f03.xml`: 15/15 y 25/25.
- `core.xml`: 447 superadas, 4 omitidas por plataforma, cero fallos; nombres en `test-results.json`.
- `unreal.json`: 21/21, cero advertencias de automatización, errores u omisiones. Win64/NullRHI, motor 5.8.2. Las advertencias de toolchain y de cabeceras Epic en la compilación no son advertencias de automatización.
- Cuatro suites documentales: 61/61. Fixture de autoridad y roadmap: PASS.
- `references.txt` y `references-base.txt`: mismo fallo previo, 566 incidencias; no superado y sin modificaciones ajenas para ocultarlo.
- `compatibility.json`: igualdad de las 20 fuentes F02 y 13 F03 con las utilizadas por sus builds; archivos SCHEMA 3 producidos por las DLL previas de Miranda/Intrepid recuperados y continuados por el nuevo lector. Los fixtures SCHEMA 1/2 siguen en las regresiones.
- `reference-snapshot.json`: secciones, 700 plazas/identidades, 480 asignaciones de las tres guardias y cobertura consultadas desde Core.
- `simulations.json`: comprobaciones independientes sobre los registros consultados para 1/7/14/28 días.
- `roster-28-days.csv`, `daily-counts-28-days.json`, `gaps-28-days.json`: cuadrante y carencias reales del plan, sin atribuir al algoritmo una demostración de óptimo global.
- `performance.json`: medidas puntuales en MSI, sin Actors masivos; no percentiles ni garantía de latencia.
- `build-provenance.json`: fuentes, dependencias Core y huellas de las DLL nativa y preparada en Unreal. Los logs y archivos binarios completos permanecen en `C:/F04/SovereignBuild`.

## Reproducir

Desde la raíz de esta rama, con las dependencias Core indicadas en los archivos `core-revision.txt`:

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04/SovereignBuild/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04/SovereignBuild/native --config Release --parallel 4
ctest --test-dir C:/F04/SovereignBuild/native -C Release --output-on-failure --output-junit C:/F04/SovereignBuild/native.xml
ctest --test-dir C:/F04/core-build -C Release --output-on-failure --output-junit C:/F04/SovereignBuild/core.xml
ctest --test-dir C:/F04/f02-native -C Release --output-on-failure --output-junit C:/F04/SovereignBuild/f02.xml
ctest --test-dir C:/F04/f03-native -C Release --output-on-failure --output-junit C:/F04/SovereignBuild/f03.xml
./desarrollo/integration/f04/run_f04.ps1 -Stage Stage -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/SovereignBuild -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage Unreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/SovereignBuild -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage TestUnreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/SovereignBuild -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02
python desarrollo/integration/f04/collect_sovereign_evidence.py --build-root C:/F04/SovereignBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-SOVEREIGN-01 --roster proyecto/docs/roadmap/master/fases/F04/F04-SOVEREIGN-01_PLANTILLA_700.md
```

Los comandos documentales son los del workflow `.github/workflows/f04-native-integration.yml`; sus salidas se conservan individualmente. El validador global adicional se ejecutó sobre esta rama y sobre main y produjo texto idéntico. No se modifica su alcance ni se silencia su fallo.

## Alcance de lo verificado

La tabla de referencia se contrasta con `sovereign_approved.tsv`, transcripción independiente del encargo. Se auditan los 59 subtotales y personas únicas, y los registros reales de deberes y cobertura. Los tests multisemana comprueban cada ventana crítica y cada par de servicios de cada persona, no solo el estado inicial/final.

Los incidentes se registran, las propuestas se calculan sobre personas reales y la suplencia se confirma con autoridad. El test de baja de sensores comprueba carencia efectiva y registro persistente; el de inviabilidad mantiene 21 servicios descubiertos al retirar las 32 personas cualificadas. El historial de una carencia resuelta permanece como evidencia; la cobertura actual se consulta por separado.

Hay persistencia entre procesos y continuidad al avanzar el mismo horizonte de una vez o por guardias. Se rechaza corrupción de checksum y del vocabulario de campos con checksum Core válido. Un nuevo scope invalida handles anteriores.

No se acreditan reservas de holocubierta ejecutables, vida social autónoma, recuperación de fatiga, una escena artística jugable ni cobertura después del horizonte. Las instalaciones solo tienen contrato mínimo compartido. Las cifras de carencias no prueban inviabilidad matemática de todas las posibles políticas. Las simulaciones usan la política de juego documentada y no una normativa laboral canónica.
