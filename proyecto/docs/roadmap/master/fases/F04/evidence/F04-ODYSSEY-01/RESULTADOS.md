# F04-ODYSSEY-01 — Evidencias de ejecución

Base exacta `c6bfcd7619c442d72afe06c21ee65c1e637f3cb2`, PR #69 y #70 incorporadas. Rama `codex/f04-odyssey-1600-tres-guardias`. F04 EN_CURSO. Draft sin fusionar.

## Resultado local

| Suite | Resultado comprobado |
|---|---|
| F04 CTest | 168/168 entradas: 136 regresiones, 31 Odyssey nativas y una entrada con tres pruebas de contratos |
| F02 / F03 | 15/15 y 25/25 |
| Core + Content JSON | 447 superadas, cuatro omitidas por plataforma, cero fallos |
| Unreal 5.8.2 Win64 NullRHI | 22/22, cero fallos u omisiones; un aviso HTTP externo |
| Cuatro suites documentales F04/Miranda/F03/F02 | 61/61 |
| Cronología y programa tecnológico LORE-03A | 56/56 |
| Contratos específicos Odyssey | 3/3, dentro de CTest |
| Fixture de autoridad / roadmap | PASS / PASS |
| Referencias globales | FAIL previo: 566 incidencias iguales a main; cero nuevas |

`native.xml` conserva cada nombre y salida CTest, incluidas las métricas y el límite acumulado. `core.xml` identifica las cuatro omisiones: permisos de lectura y symlinks no exigibles en esta plataforma; no cuentan como pruebas superadas. Las advertencias de compilador/toolchain no se confunden con las de automatización. La pasada final tiene 21 éxitos limpios y uno con aviso: timeout de la comprobación de conectividad de Unreal a `https://www.google.com/generate_204` durante Sovereign. No es un fallo funcional; se conserva el aviso y no se cuenta como cero advertencias. `unreal.json` conserva el reporte final, con DLL nativa y preparada iguales por SHA-256 en `build-provenance.json`. NullRHI verifica lógica, UWorld, Actors selectivos y persistencia; no acredita una escena artística jugable.

## Evidencias de organización y simulación

- `reference-snapshot.json`: las 72 secciones, 1.600 plazas y personas únicas, 1.035 servicios y ocho coberturas consultados desde la DLL/Core. Se contrasta cada fila con la tabla aprobada `odyssey_approved.tsv`, no con totales inventados desde el resultado.
- `simulations.json`: 1/7/14/28 días; 1.035/7.171/14.388/28.459 turnos. Objetivos 1.035/7.245/14.490/28.980; faltan 0/74/102/521 turnos no críticos.
- `critical-windows-1-days.json`, `critical-windows-7-days.json`, `critical-windows-14-days.json`, `critical-windows-28-days.json`: 24/168/336/672 ventanas individuales comprobadas durante todo su intervalo; cero déficit crítico en la fixture completa sin incidencias.
- `roster-28-days.csv`, `daily-counts-28-days.json`, `gaps-28-days.json`: cuadrante completo y déficits concretos. Máximo móvil cinco guardias y separación mínima observada 16 horas, por encima del mínimo exigido de 12. Un turno ordinario por día; 1.598 personas cambian de guardia en 28 días. Capitán: 5/10/19 turnos en 7/14/28 días; no trabaja indefinidamente.
- `performance.json`: creación de personas, instalación de plazas, bootstrap, manifiesto, planificación, cobertura, guardado, carga y avance para cada horizonte. Medidas puntuales MSI con otras validaciones locales, sin percentiles, Actors masivos ni garantía de latencia.
- `incident-performance.json`: enfermedad tras carga, candidatos reales, sustitución autorizada y cobertura recuperada; 1.600 personas conservadas y carencia histórica retenida.

Los casos nativos incluyen vacaciones, baja del capitán y ausencia del primero, suplencia técnica sin promoción permanente, credenciales caducadas, baja interior de ventana, descanso protegido/deuda, traslado, cancelación y plantilla parcial. Retirar las 54 personas habilitadas de sensores produce 21 carencias críticas en siete días. No se afirma cobertura cuando no existe.

Persistencia: exactitud byte a byte, SCHEMA 1/2/3/4, tres guardias tras carga, continuidad por ventanas y entre procesos distintos, historial de carencias resueltas, checksum y corrupción del vocabulario de dominio. Los handles anteriores a carga dejan de ser válidos. `compatibility.json` acredita guardados de DLL anteriores Miranda/Intrepid/Sovereign recuperados por el nuevo lector y continuados al mismo futuro, además de igualdad de las 20 fuentes F02 y 13 F03 usadas por sus builds originales.

## Límites observados

28 días: 32.647 entidades y 10.157.613 bytes. Sin cambiar 65.536 entidades ni 64 MiB. El caso `odyssey_limits` conserva dos bloques (56 días): 61.919 entidades, 56.764 turnos y 19.364.456 bytes. Solicitar un tercer bloque devuelve CAPACITY y no deja deberes parciales. La retención indefinida de historial necesita trabajo futuro; no se oculta como soporte ilimitado de campaña.

El techo específico de 700 en la validación de una carencia se sustituye por la dotación nominal del perfil. El planificador, las reglas, el formato persistente y Core no se sustituyen ni se modifican. Los planes son finitos y la cobertura no se extiende automáticamente más allá del horizonte.

## Reproducir en MSI

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04/OdysseyBuild/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04/OdysseyBuild/native --config Release --parallel 4
ctest --test-dir C:/F04/OdysseyBuild/native -C Release --output-on-failure --output-junit C:/F04/OdysseyBuild/native.xml
ctest --test-dir C:/F04/core-build -C Release --output-on-failure --output-junit C:/F04/OdysseyBuild/core.xml
ctest --test-dir C:/F04/f02-native -C Release --output-on-failure --output-junit C:/F04/OdysseyBuild/f02.xml
ctest --test-dir C:/F04/f03-native -C Release --output-on-failure --output-junit C:/F04/OdysseyBuild/f03.xml
./desarrollo/integration/f04/run_f04.ps1 -Stage Stage -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/OdysseyBuild -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage Unreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/OdysseyBuild -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage TestUnreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/OdysseyBuild -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native -F02CoreSource C:/F04/core-f02
python desarrollo/integration/f04/collect_odyssey_evidence.py --build-root C:/F04/OdysseyBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-ODYSSEY-01 --roster proyecto/docs/roadmap/master/fases/F04/F04-ODYSSEY-01_PLANTILLA_1600.md
```

Los comandos documentales y sus códigos están en `documentary-results.json`, con salidas individuales. La comparación global está en `references-comparison.json` y conserva ambas salidas completas. Los logs de compilación y archivos binarios quedan en el laboratorio aislado `C:/F04/OdysseyBuild`; las evidencias textuales y cuadrantes se versionan en esta carpeta.

Core F04 permanece limpio en `c147d81ed069da2e09149613ab02cbc3ebe95a4a`. Las dependencias anteriores conservan sus pins. `protection.json` verifica metadatos del repositorio principal (rutas, tamaños y mtimes), sin atribuirle una auditoría de hashes de todo el arte. No se modifican recursos artísticos ni decisiones aprobadas de PR #69. La CI remota no se presenta como superada por estas ejecuciones locales.

[Organización, todas las secciones y límites](../../F04-ODYSSEY-01_ORGANIZACION_Y_TRES_GUARDIAS.md). [1.600 plazas](../../F04-ODYSSEY-01_PLANTILLA_1600.md).
