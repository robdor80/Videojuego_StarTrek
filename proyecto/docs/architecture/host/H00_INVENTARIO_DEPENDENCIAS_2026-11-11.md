# H00-P01/P02 — Inventario y dependencias de HOST

**Fecha de auditoría:** 2026-11-11  
**Star Trek:** `robdor80/Videojuego_StarTrek`, `main@816e72b2b6e2057c47b84473e616a6feda096016`.  
**CoreRPG:** `robdor80/CoreRPG`, `main@76a7b7b485616d8c4994f384a90f123bf333591d` (consulta de rama en la misma fecha).  
**Método:** lectura de árbol, cabeceras, CMake, README, documentación de fases, registro de PR y configuración accesible de GitHub. **No compilación ni ejecución nueva.**

## Inventario comprobado

| Origen | Código/contrato verificado | Reutilización prevista | Lo que no demuestra |
|---|---|---|---|
| **F02** | `desarrollo/integration/f02/include/f02_bridge.h`; `src/f02_bridge.cpp`; `unreal/F02CoreLab.uproject`; `CMakeLists.txt`. | ABI C entre UE y Core, propiedad de sesión, hilo propietario, scopes efímeros, proyecciones por observador y patrón `UGameInstanceSubsystem`. | Un HOST definitivo; fixture limitado, no partida completa. |
| **F03** | `desarrollo/integration/f03/include/f03_bridge.h`, `unreal/`, `README.md`. | Identidad/campaña autoritativa, reloj y conocimiento observable, acciones causales y reanudación. | Vuelo warp ni universo final; escenario sintético. |
| **F04** | `desarrollo/integration/f04/include/f04_bridge.h`, `src/f04_bridge.cpp`, `unreal/F04CampaignSubsystem.*`. | `F04Session`, sesiones Core compartidas, `f04_save/load`, `f04_advance`, guardias, dotaciones, mando, instalaciones y recuperación/historial. | Autenticación de archivo externo; el subsistema UE es de laboratorio y admite bytes aportados por el llamador. |
| **F05** | `desarrollo/integration/f05/include/f05_orders.h`, `f05_delegation.h`, `f05_initiative.h`, `f05_ai.h`, `f05_ai_provider.h`. | Órdenes/recepción/ejecución, delegaciones, iniciativa determinista y propuestas IA revisadas contra Core. | Planificador global o contactos F06 reales: el efecto P01 `F04_SCAN` es una tirada de ActionEngine. |
| **F06** | `desarrollo/tools/simulation/resolve_sensor_scan.py`, `f06_reference.py` y contratos `sistemas/gameplay/ship_operations/`. | Contratos de detección y conocimiento para H09, después de tener HOST funcional. | Mutación de sensores autoritativa y consola UE final. |
| **F11** | `desarrollo/integration/f11/include/f11_promotions.h`, `src/f11_promotions.inc`, `src/f11_trial_host.inc`, `desarrollo/integration/f11_host/include/f11_host_reader.h`, `src/f11_host_reader.cpp`. | Lectura privada de expediente/eventos confirmados y futura pasarela hacia la API institucional de F11. | **El emisor de ensayo no es el emisor del producto. El HOST no puede trasladarlo ni duplicarlo.** |
| **Pruebas y CI** | `desarrollo/integration/*/tests/`, `.github/workflows/f02-*`, `f04-*`, `f05-*`, `f11-*`. | Reutilizar regresiones nativas, oráculos históricos y validaciones UE de laboratorio, sin reescribirlas. | CI pasada para un commit previo no acredita HOST final. |

**Unreal definitivo:** `juego/UE5/StarTrekRPG/README.md` declara que el directorio aún **no contiene `StarTrekRPG.uproject`**. Los proyectos `F02CoreLab` y `F05OrdersLab` no deben promoverse automáticamente a proyecto principal.

**Compatibilidad crítica:** F04/F05/F11 comparten `F04Session`, y el HOST debe poseer su vida útil sin crear otro `WorldState`. Las consultas deben usar ámbitos válidos y perspectivas de observador, y las mutaciones solo las APIs propias de cada dominio. Un `F04Ref` no acredita identidad humana ni competencia institucional.

## Pines reales de CoreRPG

| Integración | Archivo/constante | Pin verificado |
|---|---|---|
| F02 | `desarrollo/integration/f02/CMakeLists.txt` | `4f282863737bcd8f5add401202a9e1064c133672` |
| F03 | `desarrollo/integration/f03/core-revision.txt` | `9c53a33787de13d91eb2abe4da07033ee0fa1dc1` |
| F04 estable | `desarrollo/integration/f04/core-revision.txt` | `c147d81ed069da2e09149613ab02cbc3ebe95a4a` |
| F04 historial separado | `desarrollo/integration/f04/core-history-revision.txt` | `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98` |
| F05/F11 | `desarrollo/integration/f05/core-revision.txt` | `76a7b7b485616d8c4994f384a90f123bf333591d` |

**No unificar automáticamente estos pins.** Los diferentes cortes fueron auditados por separado. La selección de versión objetivo y la matriz de compatibilidad binaria pertenecen a H01/H05, con revisión de dependencias antes de compilar.

## Evidencia histórica reutilizable, no repetida en H00

- PR [#60](https://github.com/robdor80/Videojuego_StarTrek/pull/60) F02: fusionada, laboratorio nativo/UE.
- PR [#62](https://github.com/robdor80/Videojuego_StarTrek/pull/62) F03: fusionada, corte de mundo/persistencia.
- PR [#76](https://github.com/robdor80/Videojuego_StarTrek/pull/76) F04: fusionada, historial y campañas largas conforme a su acta.
- PR [#89](https://github.com/robdor80/Videojuego_StarTrek/pull/89) F05: fusionada; informe histórico `F05-P05B_CERTIFICACION_INTEGRAL_MSI_20261105.md` detalla dos repeticiones, 395/395 nativas y 12/12 NullRHI y D3D12 en laboratorios; **no es ejecución de HOST final**.
- PR [#106](https://github.com/robdor80/Videojuego_StarTrek/pull/106) y [#107](https://github.com/robdor80/Videojuego_StarTrek/pull/107): fusionadas, primer ascenso F11 y certificación delimitada.
- PR [#108](https://github.com/robdor80/Videojuego_StarTrek/pull/108) y [#109](https://github.com/robdor80/Videojuego_StarTrek/pull/109): fusionadas, contrato de frontera y lector C++ de producto. El README del lector describe **17 casos nativos**, no reejecutados aquí.
- PR [#110](https://github.com/robdor80/Videojuego_StarTrek/pull/110): abierta en Draft; tres documentos de preparación y 33 escenarios **NOT_RUN** del emisor de F11.

## Carencias para H01/H02 y siguientes

1. **No hay HOST de producto** dueño de la campaña y sus recursos.
2. No hay vínculo de principal de partida/jugador/personaje respaldado por el HOST final; `f05_bind_player` no lo sustituye.
3. La política de admisión, procedencia y recuperación de guardados requiere diseño y pruebas propias.
4. El proyecto Unreal definitivo necesita creación y verificación aparte.
5. F11 todavía necesita su emisor institucional de **producto dentro del proyecto F11**; HOST solo consumirá el contrato cuando esté disponible.
6. No existe planificador de eventos universal ni sensores/navegación autoritativos listos para el juego completo.

**Conclusión:** reutilización posible, pero integración incremental. H00 no modifica código, Core, Unreal, pins, pruebas históricas ni oráculos.
