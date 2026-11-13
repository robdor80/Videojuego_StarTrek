# H06 — Integración del HOST en StarTrekRPG

Fecha: 2026-11-13. Rama `feature/host-h06-ue-m1`. Base `5f12d9c152dd0003a6d971068d693184f45b213e` (PR #141). Adaptador nativo `2b68bd16a6200a86b43d5b66d535e97a28c4eb9d`; código Unreal ensayado `216e2cecd0dc5c21647e8f2fd33e0862023f333d`. CoreRPG limpio y fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`. [PR #142 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/142).

**Integración mínima de diagnóstico ejecutada en el proyecto principal.** M1 permanece parcial por el bootstrap productivo del cadete y el flujo de órdenes del jugador. [Decisión G0](H06_DECISION_PROYECTO_UE_2026-11-13.md) · [Resultados HU-01–HU-25](H06_RESULTADOS_2026-11-13.md).

## Inventario

| Ruta | Entrega |
|---|---|
| `desarrollo/integration/host/include/trek/host/host_abi.h`, `src/host_abi.cpp`, `src/abi_admission.h` | ABI C v1, handles opacos, tickets, proyecciones mínimas y admisión inmediata sobre SessionOwner. |
| `desarrollo/integration/host/src/session_owner.cpp`, `include/trek/host/session_owner.h`, `CMakeLists.txt` | Misma cola, trabajador y transiciones con un mutex recursivo compartido por la admisión C. Release OFF excluye los dos exports F04 heredados de ensayo. |
| `desarrollo/integration/host/tests/{host_abi_tests.c,abi_fixture.py,inspect_abi.py}`, `.github/workflows/host-h02-native.yml` | CTest de consumidor C y fixture H04/F05, carga Release OFF, Windows/Linux y sanitizadores. |
| `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`, `Source/*.Target.cs`, `Config/` | Proyecto Win64 limpio, asociación 5.8, targets Editor y Game, mapa predeterminado, perfil D3D12 y cook local. |
| `Build/Prepare-Host.ps1`, `Source/StarTrekRPG/StarTrekRPG.Build.cs`, `Private/HostRuntime.*` | Build CMake Release OFF y staging de header C y las dos DLL. Carga y negociación del módulo, recibo UBT y empaquetado NonUFS. |
| `Private/HostSessionSubsystem.*` | Un handle por GameInstance, poll por tick, proyección por UWorld, revocación y retirada del handle. |
| `Private/HostDiagnosticGameMode.*`, `Private/HostDiagnosticMapCommandlet.*` | Panel Slate, mapa regenerable con punto de entrada y GameMode propio. La generación del mapa solo se ejecuta en Editor. |
| `Private/HostAutomation.cpp`, `README.md` del proyecto | Automatización con botones reales, modos limpio y fixture, reconstrucción desde fuentes. |

Se reutilizan CoreRPG, TrekF04Bridge, H04 y la pasarela H05. El proyecto no incorpora assets artísticos, acceso directo a Core, fuente de autoridad adicional ni dependencias de laboratorios históricos.

## Frontera y vida

```text
Slate / UWorldSubsystem  <── proyecciones débiles y efímeras
           |                             ↑
           v                             | Game Thread
UGameInstanceSubsystem ─── ABI C ─── TrekHost ─── SessionOwner ─── CoreRPG/F04/F05
       un handle           tickets                         trabajador propietario
```

La ABI C tiene versión negociada, tipos de ancho fijo y tamaños x64 comprobados en CMake y UBT. Copia entradas y salidas, mantiene propiedad del handle y confina las excepciones a TrekHost. Las operaciones OPEN, CLOSE, VIEW, SAVE y RESTORE del panel llaman al adaptador C. El código C también ofrece SUBMIT_SCAN, QUERY_ORDER y CANCEL_ORDER por la pasarela H05. La UI actual mantiene deshabilitadas las órdenes de jugador hasta disponer de la procedencia y competencia productivas.

La capa UE permite hasta ocho observaciones y CLOSE conserva una ranura reservada en la ABI. `PENDING` y `RETRY` se reevalúan por tick. El Game Thread no espera futuros ni ejecuta IO de H04. La operación de cierre o carga cancela la entrega de observaciones anteriores; cada resultado consumido se vuelve a validar con un estado y una generación frescos antes de llegar a la proyección. El descarte de la entrega no revierte una operación que H04 o Core ya confirmaron. El cambio de mundo retira la proyección anterior y su panel, preserva el handle y conserva en el GameInstance la transición de sesión en curso. `Deinitialize` retira el ticker y las observaciones y transfiere el handle a un trabajo de destrucción fuera del Game Thread. La descarga final del módulo espera a que terminen esas destrucciones antes de liberar las DLL. El módulo deshabilita la recarga dinámica.

El cargador usa rutas relativas al proyecto, abre TrekF04Bridge y luego TrekHost, resuelve únicamente los símbolos C de HOST y exige ABI 1. La carga de producto y el pin de la biblioteca adyacente se comprobaron con inspección Release OFF; OPEN y RESTORE vuelven a contrastar el pin dentro del HOST nativo. UBT prepara las DLL como NonUFS para que se resuelvan también desde el ejecutable cocinado. Se usa MSVC Release y CRT de Windows. El MSI compiló ambos targets con MSVC 14.51.36256 y SDK 10.0.26100.0. UBT avisó que 14.50.35717 es su versión preferida. Se eligió `NoPCHs` para este módulo pequeño tras observar más de 4,68 GB de PCH regenerables con las opciones iniciales.

## Identidad y siguiente dependencia

OPEN abre una población técnica y deja `PRINCIPAL_UNBOUND`. La UI recibe únicamente el ID técnico de campaña, que carece de autoridad, y muestra estado, disponibilidad, error y campos filtrados si H03/H05 autorizan la vista. La raíz normal procede del directorio de aplicaciones del usuario. Las ranuras se recuperan con el vínculo persistido y el registro local de H04. H04 valida ruta, integridad y procedencia. SAVE confirma éxito tras COMMITTED. F11 permanece `SERVICE_UNAVAILABLE`.

Para nueva campaña de producto se propone que un flujo nativo de Academia cree y valide la entidad de cadete conforme a su contrato. Su resultado interno alimentará `PlayerBootstrap::prepare` y `bind` en el mismo `SessionOwner`, con generación y revisión vigentes. UI recogerá opciones de creación y consumirá el resultado, sin seleccionar una entidad Core como credencial. H04 conservará la vinculación para el siguiente arranque. La capacidad de emitir una orden deberá derivarse del dominio F05; el panel no otorgará competencia ni comisión. Se propone probar primero continuidad de identidad y guardado entre dos procesos y luego una emisión legítima con el mismo personaje. La identidad del fixture H05 solo se usa en la batería automatizada mediante una ranura local ya registrada.

## Puertas

| Puerta | Estado |
|---|---|
| G0 | PASS. Aprobación expresa y proyecto principal creado. |
| G1 | PASS para Win64 Development. UBT/UHT, ABI 1, pin y carga de ambas DLL en juego empaquetado. |
| G2 | PASS en el diagnóstico. Dos UWorld, recarga de mapa y caducidad de vistas tras RESTORE/CLOSE en ambos RHI. |
| G3 | PARCIAL. Denegación productiva sin identidad y recuperación de fixture verificadas. Pendiente bootstrap del cadete y habilitación de órdenes. |
| G4 | PASS en el alcance de diagnóstico H04 y regresión nativa. F05 interactivo de jugador depende de G3. |

## Disco y reconstrucción

Inicio de la continuación: C: 333 794 549 760 bytes libres; laboratorio H06 400 576 052 bytes. Las cinco carpetas mayores medidas fueron `valhalla` (81 116 120 197), `f05` (16 346 639 383), `Enterprise_G` (8 450 867 006), `F04` (1 845 442 528) y `host` (1 292 196 195). Al cierre de las pruebas, el conjunto de laboratorios registró 113 426 260 750 bytes lógicos y C: 343 843 880 960 bytes libres. El H06 completo quedó en aproximadamente 2,28 GB, incluidos 363 470 317 bytes del único paquete Win64, 290 366 233 bytes de DDC local y 257 834 776 bytes de cook. Se conservaron salidas de diagnóstico y un juego anterior de binarios regenerados, con 708 095 404 bytes. Se retiraron los dos PCH propios de las primeras compilaciones y se apartaron los cachés de proyecto. Una revisión automática rechazó la limpieza recursiva de la salida propia supersedida; esa carpeta queda conservada dentro de H06. Las carpetas históricas y los originales se conservaron.

UBT creó temporalmente `Binaries` e `Intermediate` en el proyecto, y UBT/UAT escribieron también su traza o log de herramienta en rutas propias del motor o de usuario. Los binarios reconstruidos de uso local ocupan 459 124 607 bytes bajo `Binaries`, ignorados. Los informes de aceptación, cook, stage, DDC y archivos de ensayo se concentran en H06. Sus carpetas se pueden retirar sin afectar las fuentes o los binarios listos para abrir el proyecto; las instrucciones reconstruyen los componentes desde el checkout y el motor instalados. No se duplicó el motor ni el checkout Core. Se comprobó la reconstrucción apartando `Binaries`, `Intermediate`, `Saved` y el mapa, regenerando ambos targets y el mapa y arrancando una raíz H04 vacía. Git contiene exclusivamente el descriptor, la configuración, el generador, el código y las instrucciones.
