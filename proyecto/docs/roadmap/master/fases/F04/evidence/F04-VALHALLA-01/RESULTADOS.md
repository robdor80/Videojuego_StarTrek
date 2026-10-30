# F04-VALHALLA-01 — Evidencias locales MSI, 31-10-2026

**Entrega para auditoría; no fusión, no cierre F04, no GUARDIAS-02.**

Base exacta `78fa53f99c384f4111f42d61d71fa2510b56f6b5`; rama
`codex/f04-valhalla-01-gran-nave-2200`; worktree `C:/F04/Valhalla01` y
laboratorio aislado `C:/F04/ValhallaBuild`. GitHub Desktop ejecutó Pull sobre main
antes de crear la rama; se verificaron los merges #67–#73 y main limpio.

## Resultado y recuentos

- 1.800 plazas e identidades de Flota, 400 civiles distintos, 2.200 personas únicas.
- Siete departamentos y 90 secciones exactas; todas las filas contrastadas.
- Referencia 550 Alpha / 380 Beta / 255 Gamma / 615 fuera.
- Defiant: 10+10+6+10+4 = 40 personas incluidas; acoplamiento 15 excluidos.
- Marines: 4+10+10+10+10+6+6+4 = 60, con cadena de mando de destacamento.
- Censo civil: 130+90+65+50+35+30 = 400; identidad, domicilio, presencia y agenda.

Los CSV son exportaciones de consultas reales, no otra base autoritativa:
[plazas](positions-1800.csv), [Defiant](defiant-naval-40.csv),
[Marines](odin-marines-60.csv), [residentes](census-400.csv).
Se describen organización, permisos y límites en
[La gran nave](../../F04-VALHALLA-01_ORGANIZACION_GRAN_NAVE.md).

## Pruebas ejecutadas

| Suite | Resultado | Evidencia |
|---|---|---|
| F04 CTest completo | 187/187, cero fallos/omisiones | [XML](f04.xml), [salida](native.txt) |
| Valhalla dentro de F04 | 18 casos nativos + una entrada con dos contratos Python | CTest `f04.valhalla_*` |
| Capacidad, comprobación reforzada | 1/1 adicional; resto de campaña idéntico byte a byte tras retirar solo auditoría del rechazo | [XML](capacity-atomic.xml), [salida](capacity-atomic.txt) |
| F02 recompilado desde esta rama | 15/15 | [XML](f02.xml) |
| F03 recompilado desde esta rama | 25/25 | [XML](f03.xml) |
| CoreRPG + Content JSON | 447 superadas, cuatro omitidas por plataforma, cero fallos | [XML](core.xml), [salida](core.txt) |
| Unreal 5.8.2 Win64 NullRHI | 23/23 Success, cero fallos y cero warnings asociados a tests | [reporte](unreal-report.json), [log](nullrhi.txt) |
| Documentales F04/Miranda/F03/F02 | 22+4+26+9 = 61/61 | `test_*.txt` |
| Cronología LORE-03 A | 56/56 | [salida](lore03-a-tests.txt) |
| Fixture autoridad F04 | PASS | [salida](authority-fixture.txt) |
| Gobierno roadmap | PASS, F04 EN_CURSO | [salida](roadmap.txt) |
| Referencias globales | FAIL previo: 566 idénticas a main; cero nuevas | [comparación](reference-regression.json), [salida](references.txt) |

Las cuatro omisiones de Core son comprobaciones de permisos/symlinks que esta
plataforma no permite ejecutar. No se cuentan como superadas. El compilador UE
avisa de MSVC posterior al preferido y de APIs obsoletas en cabeceras del motor;
se conserva [el log de compilación](unreal-build.txt). El reporte de automatización
sí tiene cero advertencias de prueba. NullRHI no es validación artística/jugable.

Las regresiones cubren Miranda, Intrepid, Sovereign y Odyssey. Se han producido
archivos con la DLL anterior a Valhalla y cargado/continuado en procesos de los
nuevos lectores, con el mismo futuro para las cuatro clases:
[compatibilidad y hashes](compatibility.json). SCHEMA 1/2 se prueban también en
las fixtures heredadas; SCHEMA 3→4 conserva el archivo previo y migra explícitamente.
No se exige que una DLL vieja interprete un perfil nuevo que no conoce.

## Cuadrantes y cobertura

| Días | Reales / objetivo | Déficit no crítico | Críticas verificadas | Máximo móvil 7 días | Descanso mínimo observado |
|---:|---:|---:|---:|---:|---:|
| 1 | 1.185 / 1.185 | 0 | 24/24 | 1 | No aplica |
| 7 | 8.176 / 8.295 | 119 | 168/168 | 5 | 16 h |
| 14 | 16.421 / 16.590 | 169 | 336/336 | 5 | 16 h |
| 28 | 32.460 / 33.180 | 720 | 672/672 | 5 | 16 h |

Se prueba cada ventana completa de ocho servicios por tres turnos, no únicamente
su comienzo. Los proveedores son operadores Valhalla, sin usar civiles, Marines
o personal especializado Defiant. Una guardia ordinaria por persona/día y al
menos doce horas de descanso. Los JSON `critical-windows-*-days.json` contienen
proveedor y primer hueco; [simulaciones](simulations.json),
[cuadrante completo](roster-28-days.csv) y [déficits](gaps-28-days.json).

La demanda diaria multisemana es un objetivo, no prueba de optimalidad. Los
déficits quedan persistidos por departamento/intervalo, sin sustitutos ficticios.
La baja de sensores pierde cobertura y el relevo legítimo la recupera, manteniendo
destinos y huecos históricos: [medición del incidente](incident-performance.json).
La ausencia de todos los habilitados de sensores produce 21 huecos en siete días.

Negativas Valhalla: un Marine no recibe timón/naval Defiant ni plaza naval aunque
esté vacante; ni Marine ni naval Defiant reciben mando Valhalla; un civil no
recibe plaza, guardia o maniobra; un jefe de Seguridad no manda por su jefatura;
la restricción técnica no anulable sigue rechazando al capitán. Ningún Actor
confiere autoridad. La corrupción con checksum Core válido también se rechaza.

## Rendimiento y límite persistente

[Mediciones completas](performance.json): una ejecución puntual MSI MSVC Release,
sin percentiles. Se miden creación de 2.200 identidades, instalación de plazas,
bootstrap, manifiesto paginado, planificación, cobertura, serialización, carga,
avance y memoria. Los archivos `.f04` se escriben realmente en el laboratorio;
`persistent_file_bytes` es el tamaño devuelto por el sistema de archivos y
coincide con el archivo serializado. No se incorporan binarios de campaña a Git.

En 28 días: 37.470 entidades tras planificar; archivo 11.789.885 bytes. Después
de avanzar, 37.553 entidades y 11.805.987 bytes, con cambios de mando históricos.
El bloque adicional 28→56 días devuelve F04_CAPACITY antes de publicarse. Quedan
32.460 guardias originales y las 2.200 personas; solo se añade un evento de rechazo:
37.554 entidades y 11.806.157 bytes. [Detalle](capacity.json).

El test reforzado deserializa antes/después, exige exactamente ese único evento,
normaliza su creación y revisión y obtiene el archivo previo byte a byte: estado,
RNG, Timeline, plazas, personas, actividades y relaciones intactos. No se suben
límites ni se elimina historial para pasar la prueba. No se ha buscado el día
exacto de saturación entre 28 y 56, ni se ha certificado un año de campaña.
**Deuda explícita F04-PERSISTENCIA-03.**

La memoria reportada es Working Set y Peak Working Set del proceso de medición
Python/ctypes, incluyendo transacciones temporales y buffers, no el heap aislado
de Core ni los 2.200 Actors. El experimento UE comprueba cero Actors automáticos,
proyección selectiva de un civil y continuidad determinista tras desmaterializar.

## Comandos reproducibles

Desde la raíz del worktree; rutas de laboratorio externas a fuentes:

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04/ValhallaBuild/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04/ValhallaBuild/native --config Release --parallel 4
ctest --test-dir C:/F04/ValhallaBuild/native -C Release --no-tests=error --output-on-failure -j 4 --output-junit C:/F04/ValhallaBuild/f04.xml
ctest --test-dir C:/F04/ValhallaBuild/native -C Release -R valhalla_limits --output-on-failure --output-junit C:/F04/ValhallaBuild/capacity-atomic.xml
ctest --test-dir C:/F04/core-build -C Release --no-tests=error --output-on-failure -j 4 --output-junit C:/F04/ValhallaBuild/core.xml
```

F02/F03 se configuraron y compilaron en `ValhallaBuild/f02` y `ValhallaBuild/f03`,
con `CORERPG_SOURCE_DIR=C:/F04/core-f02` y `C:/F04/core-f03` respectivamente;
CTest con `-C Release --no-tests=error --output-on-failure --output-junit` produjo
los XML entregados. Pins originales: F02 `4f282863737bcd8f5add401202a9e1064c133672`,
F03 `9c53a33787de13d91eb2abe4da07033ee0fa1dc1`.

```powershell
./desarrollo/integration/f04/run_f04.ps1 -Stage Stage -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/ValhallaBuild -F02NativeBuild C:/F04/ValhallaBuild/f02 -F03NativeBuild C:/F04/ValhallaBuild/f03 -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage Unreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/ValhallaBuild -F02NativeBuild C:/F04/ValhallaBuild/f02 -F03NativeBuild C:/F04/ValhallaBuild/f03 -F02CoreSource C:/F04/core-f02
./desarrollo/integration/f04/run_f04.ps1 -Stage TestUnreal -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04/ValhallaBuild -F02NativeBuild C:/F04/ValhallaBuild/f02 -F03NativeBuild C:/F04/ValhallaBuild/f03 -F02CoreSource C:/F04/core-f02
python desarrollo/integration/f04/collect_valhalla_evidence.py --build-root C:/F04/ValhallaBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-VALHALLA-01
python desarrollo/integration/f04/check_valhalla_compatibility.py --previous-build C:/F04/OdysseyBuild/native --new-build C:/F04/ValhallaBuild/native --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-VALHALLA-01/compatibility.json
python desarrollo/integration/f04/package_valhalla_evidence.py --build-root C:/F04/ValhallaBuild --output proyecto/docs/roadmap/master/fases/F04/evidence/F04-VALHALLA-01
python desarrollo/tools/validation/validate_roadmap_state.py
```

Documentales: `python -m unittest discover -s desarrollo/tools/validation -p`
para `test_f04_reference.py`, `test_f04_miranda_example.py`, `test_f03_reference.py`
y `test_validate_f02_contracts.py`; `python desarrollo/tools/validation/test_lore03_a.py`;
fixture `f04_reference.py --fixture desarrollo/validation/fixtures/f04/authority_watch_acceptance_v0.1.json`.
El validador `validate_internal_references.py` se ejecutó tanto en main como en
esta rama, comparando las listas completas de errores, no solo su número.

## Procedencia y protección

[Procedencia](build-provenance.json) contiene SHA de los tres Core limpios,
versión UE, compilador, hashes de fuentes y DLL. La DLL nativa y la de Unreal
coinciden SHA-256. Todos los cambios versionados están en integración F04 y
documentación/evidencias F04. Main queda limpio; no se modificaron arte, Blender,
modelos, texturas, materiales, ignorados originales, copias de seguridad ni Core.
Esta verificación de alcance Git no equivale a un hash completo de todos los
recursos artísticos externos.

Pendiente INTEGRACION-04: reparto y autoridad al separar secciones, transferencias
físicas, embarque/desembarque, mando y cobertura independiente Defiant, anclaje y
misiones conjuntas. Pendiente F12: simulación civil completa. No hay camuflaje o
combate ejecutables, escenas nuevas, propulsión cuántica instalada ni cierre F04.
