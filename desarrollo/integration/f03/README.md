# F03 — campaña autoritativa real

Implementación del mínimo vertical P01–P05, con CoreRPG real. Depende de la
[PR Draft Core #12](https://github.com/robdor80/CoreRPG/pull/12), SHA exacto en
`core-revision.txt`. No equivale a integración en `main` ni cierre oficial F03.

## Repetir

Requisitos verificados: Windows 11/MSI, UE **5.8.2 CL 56702186**,
Visual Studio Community 2026 / MSBuild 18.9.1, MSVC 19.51.36256,
SDK 10.0.26100.0, CMake 4.4.3, Python 3.10.11, Git 2.52.0.
Primero obtener checkouts/worktrees limpios: Core F02 en `4f282863737bcd8f5add401202a9e1064c133672`
y Core F03 en la revisión fijada, sin tocar proyectos originales.

```powershell
# Desde la raíz Star Trek. Elegir rutas ASCII externas y nuevas para cada ejecución.
./desarrollo/integration/f02/run_f02.ps1 -Stage All -CoreSource <CoreF02> -BuildRoot C:/F03_repro/f02
./desarrollo/integration/f03/run_f03.ps1 -Stage All -CoreSource <CoreF03> -BuildRoot C:/F03_repro/f03 -F02CoreSource <CoreF02> -F02NativeBuild C:/F03_repro/f02/native

# Suite completa Core, independiente del Host:
cmake -S <CoreF03> -B C:/F03_repro/core -G 'Visual Studio 18 2026' -A x64 -DBUILD_TESTING=ON -DCORERPG_BUILD_CONTENT_JSON=ON
cmake --build C:/F03_repro/core --config Release --parallel 4
ctest --test-dir C:/F03_repro/core -C Release --no-tests=error --output-on-failure --parallel 4
```

Solo nativo (también Linux):

```sh
cmake -S desarrollo/integration/f03 -B /tmp/f03 -DCORERPG_SOURCE_DIR=/path/to/pinned/CoreRPG
cmake --build /tmp/f03 --config Release --parallel 4
ctest --test-dir /tmp/f03 -C Release --no-tests=error --output-on-failure
```

El runner conserva cada log con fecha. `All` compila y prueba 25 casos nativos,
prepara el laboratorio externo y ejecuta 12 tests UE (6 F02 + 6 F03). Rechaza un
laboratorio preexistente sin su marcador. No ejecutarlo concurrentemente contra
el mismo BuildRoot. El proyecto staged mantiene el nombre técnico F02CoreLab;
el overlay añade los subsistemas/tests F03 sin editar las fuentes F02.

## Escenario ejecutado

Ocho IDs Core: dos naves Starfleet, nave romulana oculta, dos sectores, un grupo
de tres plazas y dos individuos materializados de ese grupo. Queda una plaza
latente, sin inventar población. Las dos ubicaciones iniciales de tripulantes
se eligen con `RandomStreams::stream(0xF0301)`. IDs, definiciones, conocimiento y
ubicaciones residen en Core; no hay un mundo paralelo Trek.

La ruta fija de la segunda nave autoriza cuatro acciones: salida t=10, llegada
t=20, tirada t=21 y regreso t=40; cada acción depende causalmente de la anterior.
La ubicación es contención en sectores discretos: no es un modelo de vuelo warp,
distancias, combustible o física. La ruta es una actividad sintética de integración.
El tiempo es exacto en segundos desde **2372-03-14T10:42:00**. La época es parte
del fixture Trek 0.1.0, no configurable en este incremento. `f03_calendar` deriva
calendario y desplazamiento estelar de 1000 unidades/año de calendario; no inventa
un ancla absoluta de fecha estelar. Se rechaza fuera de rango gregoriano hasta 9999.

Antes de la llegada ninguno conoce la nave romulana. La observación directa
legítima requiere nave secundaria y objetivo en el segundo sector. Adquiere
existencia, definición y ubicación mediante `WorldState::learn_fact`. El informe
autorizado a la primera nave solo transmite existencia. Consultar no adquiere
conocimiento ni actualiza recuerdos. Dos observers producen vistas distintas;
`ContextBuilder` recibe exclusivamente `ObserverView`.

## Frontera, persistencia y seguridad

La DLL C ABI 1 admite registros/buffers del llamador, sin STL, excepciones ni
UObjects a través de la frontera. Todas las llamadas de sesión requieren hilo
propietario; UE exige Game Thread. `F03Ref` añade un scope efímero renovado en cada
carga correcta. Se rechazan refs de otra sesión, bindings caducados y observers
inventados. La revocación Host bloquea nuevas consultas/acciones; no elimina
memorias legítimas. El control es de laboratorio, no una autenticación de red.

`f03_view` exporta contactos relativos al observador, clasificación solo conocida
y referencias ya filtradas. `f03_stats`, handles, save y marker_state son APIs
**privilegiadas de diagnóstico**; no son endpoints de UI/IA ni resultados de
Sensores. Ningún Actor puede pedir una entidad oculta por su ID. El historial Core
y la totalidad del save tampoco se entregan a un consumidor no autorizado.

`CampaignPersistence` guarda mundo, RNG, conocimiento, reloj, agenda y resultados
en un archivo Core `CRPGTIME` v1 con payload SAVE v1–v3 y CRC32C. Trek añade
validación de alcance (catálogo, población, observers y ruta exacta) y publica una
sesión candidata únicamente tras validarla. Un fallo conserva campaña y bindings.
El permiso Host vive fuera del save y cargar no lo eleva.

IO pertenece al Host. Los archivos de prueba usan ubicaciones aisladas; Unreal
rechaza sobrescribir saves existentes. No se afirma durabilidad frente a pérdida
eléctrica ni escritura concurrente; el test entre procesos termina el escritor y
abre un lector distinto. No se mata ni se modifica un proceso/proyecto del usuario.
No hay migración automática de F02 al archivo nuevo: se rechazan formatos ajenos
o versiones futuras. El Core antiguo conserva sus formatos y tests anteriores.

## Resultados y límites

[Auditoría técnica](../../../proyecto/docs/roadmap/master/fases/F03/AUDITORIA_TECNICA_2026-10-30.md)
· [Informe para auditoría independiente](../../../proyecto/docs/roadmap/master/fases/F03/INFORME_EJECUCION_2026-10-30.md).

No implementa consola de Sensores, IA conversacional, memoria psicológica, simulador
galáctico, jerarquía de autorizaciones de Flota, cancelación/revocación de órdenes
ya autorizadas, compactación del historial ni fichas completas de producción.
La agenda genérica conserva hasta 4096 registros. El alcance logrado es el corte
integrado en ramas para auditoría; integración final depende de Core y revisión.
