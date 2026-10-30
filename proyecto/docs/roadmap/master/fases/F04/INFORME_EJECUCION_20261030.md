# F04 — entrega técnica para auditoría independiente

Fecha: 30-10-2026. PR Draft: [Star Trek #64](https://github.com/robdor80/Videojuego_StarTrek/pull/64).
Rama: `codex/f04-ship-operations-20261030`, basada en
`c8109216b1467e89e08f7d2d330256e3f0e80559`.
Código y scripts validados: `96d37c6697623085c1f711ada2d39cc017439705`.
El HEAD de entrega es la cabecera de esta PR; los commits posteriores al código
pueden añadir únicamente evidencias/documentación. No se ha fusionado nada.

## 1. Implementación y reutilización

El alcance realizado se detalla en `MATRIZ_IMPLEMENTACION_20261030.md` y
`ARQUITECTURA_IMPLEMENTACION_20261030.md`. P01–P05 forman un corte operativo
ejecutable sobre Core real: identidad/clase/manifiesto; plazas y vacantes;
agendas y guardias; cuatro roles distintos; nombramientos, delegación y
sucesión; límites médicos/técnicos; revisión contextual; avance sin Actors;
guardado y restauración en una sesión y proceso nuevos.

Las operaciones positivas tienen consecuencias Core: el alférez realiza una
operación diagnóstica de sensores con RNG persistente; el jefe modifica la
asignación de su departamento; el oficial de guardia cambia la alerta de la
nave; el capitán decide una política de turnos con cobertura comprobada.
Los actores ajenos al ámbito reciben motivos de denegación auditables.
Un rango superior visitante solo puede emitir una orden dentro del mandato
externo explícito importado en esta muestra, sin adquirir el mando de la nave.

Reutilizado sin modificar: identidad/población, relaciones, catálogo, motor
de acciones, RNG, Timeline y archivo de campaña Core; contratos y escenarios
Trek F04; metodología de laboratorio F02/F03. Nuevos componentes exclusivamente
Trek: esquema relacional, autorización, agenda, ABI C, proyecciones Unreal,
tests y workflow. No existe un manifiesto alternativo mutable dentro de UE.

F04 abre una campaña nueva con esquema Trek propio sobre el mismo formato
genérico Core. No importa ni migra implícitamente el contenido del fixture F03;
los archivos F03 siguen cargándose con su adaptador original sin modificar.
Una campaña ajena al esquema F04 se rechaza de forma atómica. Una migración
explícita de campañas entre muestras queda fuera de este laboratorio.

La muestra es sintética: siete miembros de dotación, un civil y un almirante
visitante como pasajero, tres plazas y déficit reconocido. No es una nueva
dotación canónica de Sutherland ni el ejemplo Miranda-120.

## 2. Pruebas locales finales

| Suite | Definidas | Superadas | Fallidas | Omitidas |
| --- | ---: | ---: | ---: | ---: |
| CoreRPG completa, Content JSON activado, Windows Release | 451 | 447 | 0 | 4 |
| F04 nativa, Core real | 52 | 52 | 0 | 0 |
| F03 nativa, SHA original | 25 | 25 | 0 | 0 |
| F02 nativa, SHA original | 15 | 15 | 0 | 0 |
| Unreal 5.8.2, Actors/UWorld, NullRHI | 17 | 17 | 0 | 0 |
| Referencia F04 Python | 22 | 22 | 0 | 0 |
| Miranda-120 Python | 4 | 4 | 0 | 0 |
| Referencia F03 Python | 26 | 26 | 0 | 0 |
| Contratos F02 Python | 9 | 9 | 0 | 0 |
| Escenarios F04 existentes | 39 | 39 | 0 | 0 |

El checkout actual contiene **22** tests de referencia F04, no 17; se ejecutó
la suite completa presente, conservando los 39 escenarios. Estos escenarios
también son comprobados por un unittest; no se deben sumar como pruebas
nativas independientes.

Las cuatro omisiones Core Windows son: archivo ilegible por permisos y tres
casos de symlinks no disponibles en este entorno. Sus nombres y motivos
figuran en `evidence/20261030/core.xml`. Unreal se desglosa en F02 6, F03 6,
F04 5; no hubo advertencias de test ni pruebas pendientes. La compilación
Unreal emitió un aviso de API obsoleta procedente del propio motor.

Los tests F04 cubren guardado/carga entre procesos, identidad única, ausencia
sin reemplazo artificial, cualificación caducada al ejecutar, delegación
revocada, revocación del nombramiento de origen seguida de nuevo nombramiento,
solapamiento y adyacencia, sucesión al saltar intervalos completos, archivo
corrupto o semánticamente inválido, hilo ajeno, handles obsoletos y presupuesto
temporal reanudable. Se compara el futuro de campaña byte a byte.

Validadores de gobierno, contratos F02, traspaso F02-P05 y contrato F03: PASS.
Validador general de referencias: **FAIL, 564 incidencias preexistentes**;
repetido en `c810921...` limpio con salida byte a byte idéntica. Se incluyen
ambas salidas. No se presenta esta comprobación como superada ni se altera
documentación ajena para ocultar la deuda.

## 3. Fallos originales y recuperación

Se conservan los logs íntegros localmente en `C:/F04/evidence` y extractos con
hashes en `original-failures.json`. La primera compilación encontró colisión
del identificador DOMAIN con una macro de MSVC; se renombró. El primer CTest
sin ejecutable dejó 44 casos sin ejecutar: no se contabilizan como pruebas
realmente corridas. Dos ejecuciones posteriores dieron 43/44: el generador del
archivo alterado debía ordenar relaciones e incrementar revisión Core para
alcanzar la validación Trek. Otro ensayo dio 44/46 al hacer caducar demasiado
pronto la habilitación de relevo respecto de su guardia; se corrigió el fixture.
Las ejecuciones finales indicadas arriba pasan y los originales no se borraron.

## 4. Reproducción y evidencias

Instrucciones completas: `desarrollo/integration/f04/README.md` y
`run_f04.ps1`. Builds y laboratorio solo en `C:/F04`. Windows 11, MSVC
19.51.36256.0, UE 5.8.2, changelist 56702186. Las pruebas no abren ni modifican
proyectos artísticos existentes. Las pruebas nativas y la CI no requieren UE.

Resultados públicos: `evidence/20261030/results.json`, XML Core/F02/F03/F04,
`unreal.json`, logs documentales y listado de fuentes auditadas con SHA256.
El colector elimina rutas de perfil personal. No se publican modelos, texturas,
campañas binarias, inventarios artísticos detallados ni builds.

## 5. Revisiones y dependencias

| Repositorio/uso | SHA exacto |
| --- | --- |
| Trek base y checkout principal preservado | `c8109216b1467e89e08f7d2d330256e3f0e80559` |
| Trek código del corte F04 validado localmente | `96d37c6697623085c1f711ada2d39cc017439705` |
| Core F04, main ya fusionado | `c147d81ed069da2e09149613ab02cbc3ebe95a4a` |
| Core F03, referencia original sin cambiar | `9c53a33787de13d91eb2abe4da07033ee0fa1dc1` |
| Core F02, referencia original sin cambiar | `4f282863737bcd8f5add401202a9e1064c133672` |

No se necesita PR Core. Su worktree F04 está en detached HEAD limpio; no se
creó una rama Core con cambios inexistentes. PR Trek #64 depende únicamente
del Core ya integrado. Orden recomendado: auditoría independiente del esquema
y autorizaciones; revisión de limitaciones; decisión de ChatGPT sobre la única
PR Trek. No hay fusión autorizada dentro de esta ejecución.

## 6. Protección local

41.827 archivos inventariados antes y después: **0 ausentes, 0 modificados,
0 nuevos en ubicaciones protegidas**. Método: ruta, tamaño y mtime_ns; no es
una auditoría criptográfica de cada archivo. Incluye checkout principal,
laboratorios/worktrees F02/F03 y `C:/F03`, archivos ignorados y backups.

Trek principal conserva main y su HEAD original, 2.342 archivos sin seguimiento
y 14.814 ignorados; Core principal conserva main/HEAD, 0 sin seguimiento y
4.759 ignorados. Los estados Git completos son idénticos a los iniciales.
`main-checkouts.json` contiene el resumen sin rutas privadas. Los archivos
nuevos versionados de esta PR son código, documentación y evidencias F04;
no pertenecen al inventario artístico anterior.

No se ejecutaron reset/clean, borrados, merges, podas de worktrees, cierres de
Blender/Unreal artísticos ni sincronizaciones de los checkouts principales.
El worktree antiguo marcado por Git como prunable se dejó intacto.

## 7. Límites y dictamen

Pendientes: régimen biológico de descanso/fatiga; planificación multisemanal
real de 120 personas; viajes físicos y duración de relevo; traspaso completo
de conocimiento; editor de destinos y cualificaciones; rotaciones arbitrarias;
normativa y sistemas técnicos completos; órdenes e iniciativa NPC F05; escena
gráficamente jugable. Son límites expresos del mínimo vertical, no éxitos
atribuidos a los tests de referencia.

**Preparada para auditoría independiente del corte P01–P05**, con estos límites
y la deuda general de referencias visibles. No acredita UE5_JUGABLE, aceptación
final ni cierre de F04. `ESTADO_GLOBAL.json` y las entregas F02/F03 permanecen
intactos. El control de fusiones y cierre administrativo sigue en ChatGPT.

## 8. GitHub Actions

Código `96d37c6697623085c1f711ada2d39cc017439705`: tres workflows SUCCESS.

| Workflow | Ejecución verificada |
| --- | --- |
| F04 authoritative ship operations | [41049813307](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41049813307) |
| F04 reference contracts | [41049813117](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41049813117) |
| Roadmap governance | [41049813133](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41049813133) |

En Ubuntu: Core 451/451, F04 52/52, F02 15/15, F03 25/25; cero fallos y
omisiones. Referencias Python: 22 + 4 + 26 + 9, y 39 escenarios F04, todos
superados. Los logs resumidos con SHA/run/job se conservan en
`github-actions-code.json`. UE se validó localmente, no en el runner Linux.
Los commits posteriores a ese código añaden solo informe/evidencias; los
checks de la cabecera documental final se comprueban también en la PR.
