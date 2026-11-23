# H06-P01 — Auditoría de prerrequisitos y plan no destructivo de integración Unreal

**Fecha:** 2026-11-13. **Estado:** DOCUMENTADO por ChatGPT, implementación H06 NO INICIADA. **Responsables:** ChatGPT (P01, matriz, auditoría), Codex (P02–P05 C++/UBT/ensayos), usuario (decisión de proyecto Unreal definitivo). **Hito:** M1, integración mínima HOST↔UE5 real, NO certificación global (H13).

## 1. Evidencias comprobadas antes de codificar

- Plan vinculante: `proyecto/docs/architecture/host/PLAN_MAESTRO_HOST_v1.2_2026-11-11.md`, H06-P01..P05. H05 / M0 fusionado mediante [PR #139](https://github.com/robdor80/Videojuego_StarTrek/pull/139), merge `3fb74093278f880e51f1fe37ddaae1e19c54ce7b`, [acta de auditoría](H05_ACTA_AUDITORIA_FUSION_2026-11-13.md). En la inspección, main avanzó a `8775d7ce7c289f90b66a55bca2925619ae67e35c`; Codex revalidará HEAD al iniciar.
- La carpeta versionada `juego/UE5/StarTrekRPG/` contiene **únicamente README.md** que declara ausencia de `StarTrekRPG.uproject`. No puede concluirse que no exista alguna copia local no subida. **Es una puerta de entrada:** inventariar los .uproject locales y su procedencia antes de crear/promover nada. No llamar «juego definitivo» al laboratorio.
- Reutilizables: `desarrollo/integration/host/include/trek/host/session_owner.h` (API C++20 interna, futuros, `SessionOwner`, generación, `open/close/query_view/submit_order/query_order/cancel_order/save/restore/inspect`), `src/player_bootstrap.h` (flujo interno de vinculación), `desarrollo/integration/f02/unreal`, `f04/unreal`, `f05/unreal` (patrones de UBT, UGameInstanceSubsystem y pruebas, **laboratorios y no arquitectura de producto**).
- H05 `SessionOwner` conserva **un solo dueño nativo de Core**. H04 publica/recupera ranuras. F05 `F04_SCAN` produce una tirada Core de fixture, **no detección F06**. La recepción/ejecución de órdenes desde destinatarios es SOLO de pruebas M0, sin API pública de producto. **No desbloquearla desde Blueprint**.
- H03 vincula personaje mediante `PlayerBootstrap` de confianza; la **creación productiva del cadete de Academia no está implementada**. Por tanto, una interfaz Unreal no puede aceptar un `person_id` cualquiera como credencial ni declarar «nuevo juego completo» donde falte el bootstrap aprobado.
- CoreRPG nativo aprobado para H02–H05: `76a7b7b485616d8c4994f384a90f123bf333591d`, checkout limpio. No modificar el pin ni el historial F02/F04/F05/F11.
- Alcance de la inspección ChatGPT: árbol remoto GitHub y documentos; **no** UBT/UHT, editor local, compilación UE, NullRHI ni D3D12. Todos ellos `NOT_RUN` hasta evidencia local de Codex.

## 2. Decisiones y barreras para H06

**Puerta G0 — proyecto UE principal.** Codex inspeccionará equipo local y repositorio (rutas, hashes, EngineAssociation, dependencias, licencias de assets y .uproject) y comparará candidatos. Si no existe uno inequívocamente aprobado, preparará propuesta mínima con estructura `juego/UE5/StarTrekRPG/`, fuente y configuración, **pero no creará ni promoverá como definitivo un .uproject sin aprobación específica del usuario**. Puede preparar código aislado de integración y pruebas nativas antes de obtener esa decisión. No migrar assets/binarios ni duplicar proyectos UE5. El primer paso no es copiar `F02CoreLab.uproject` o `F05OrdersLab.uproject`.
  
**Puerta G1 — ABI Unreal↔HOST.** `SessionOwner` expone C++20 `std::future`, `std::string`, `std::optional` y símbolos C++ a través de DLL. **No dar por segura su ABI binaria con UBT ni pasar STL, excepciones, punteros Core ni objetos Unreal a través de frontera de DLL.** Revisar toolchain/CRT y diseñar un **adaptador estrecho en C de ABI estable** dentro de la composición nativa del HOST, con tipos triviales versionados, handles opacos, tamaños/longitudes explícitos, propiedad de memoria definida y códigos de error. Una C ABI puede evolucionar de modo aditivo; Codex fijará las firmas exactas tras inspeccionar fuentes y necesidades UBT. No crear otra copia de Core.

**Puerta G2 — threading y vida.** El `UGameInstanceSubsystem` del juego es dueño de un handle cliente y mantiene vivo un único `SessionOwner` indirectamente; Core sigue en el hilo propietario de H02. `UWorld` contiene actores/vistas efímeros por mundo, no sesiones ni credenciales. Ninguna llamada Core en Game Thread; no bloquear esperando `future.get()`; pasar resultados de tareas por cola/poll acotados y despachar UObjects SOLO en Game Thread. Cancelar/desvincular operaciones al `Deinitialize`, cambio de nivel, cierre o LOAD; descartar resultados si cambió `session_generation`. Dos UWorld simultáneos no crean dos dueños Core.

**Puerta G3 — identidad y pruebas de juego.** Separa `OPEN` técnico, `BOUND` legítimo y recuperación de ranura. Una sesión sin personaje solo permite diagnósticos inocuos y operaciones permitidas por la política; muestra `PRINCIPAL_UNBOUND` para vistas/órdenes privadas. El bootstrap de un personaje preexistente solo se habilitará mediante el camino interno autorizado H03, **no** con un campo de UI/Blueprint. Si no está disponible el flujo productivo mínimo, declarar bloqueada la prueba de «jugador nuevo y orden» y proponer dependencia; nunca «resolverlo» copiando accesos de fixtures H05.
  
**Puerta G4 — persistencia y decisiones de dominio.** `SAVE/RESTORE` llaman H04, con campaña, raíz privada y generación correctas; sin serializadores paralelos de `UObject` para hechos autoritativos. Solo representar vistas filtradas de H05. F11 institucional permanece `SERVICE_UNAVAILABLE`; H07/F11 proveerán integración futura. No exponer `GatewayTestAccess`, `F04Session*`, actores/issuer arbitrarios, privilegios, historiales crudos ni `WorldState` desde Blueprint.

## 3. Diseño de composición propuesto (no API implementada)

```text
UE5.8.2 juego/UE5/StarTrekRPG (después de G0)
  GameInstanceSubsystem / UI de diagnóstico (Game Thread)
     |  intenciones controladas, datos de vista copiados
     v
  módulo Unreal HOST -> C ABI adaptador nativo con handles opacos
     |  comandos asíncronos + entrega/encuesta de resultados limitada
     v
  TrekHost existente -> SessionOwner (un único hilo propietario)
     |  H03 identidad | H04 slots | H05 órdenes/consultas
     v
  TrekF04Bridge + F05 + CoreRPG (única verdad)
  
  UWorld A/UWorld B: solo representación por mundo, weak refs, invalidables
```

- Al abrir/cargar: obtener y conservar generación vigente. UI solicita lectura filtrada; resultados antiguos no se aplican. Al guardar, reportar `SUCCESS` solo cuando H04 confirma publicación durable.
- El primer interfaz puede ser un panel discreto de diagnóstico: versión/capacidades reales, estado y generación, vista autorizada, operación permitida, guardar, recuperar, cerrar y errores sanitizados. Nada de pantallas artísticas definitivas ni puente institucional.
- El descriptor definitivo, `Source`/`Plugins`, `Build.cs`, empaquetado de DLL/lib y rutas de staging se deciden tras G0 y G1. Nunca referenciar rutas absolutas del equipo ni rutas temporales desde código/configuración de producto.

## 4. Estrategia de ejecución y protección del disco

1. Inventario **de solo lectura** de `.uproject` locales y candidatos. Reportar original, tamaño, EngineAssociation, dependencia, checksum, coste estimado de migración y si está versionado; no copiar modelos ni archivos `.uasset` del laboratorio.
2. Examinar `SessionOwner`, CMake, F02/F04/F05 Unreal y H03 bootstrap. Acordar frontera mínima G1. Preparar adaptador y tests de ABI en la biblioteca HOST sin UE si G0 aún bloquea.
3. Solo tras G0: instalar módulo en el proyecto aprobado y conectar `UGameInstanceSubsystem` y `UWorld`; panel mínimo. Implementar pruebas automatizadas UE.
4. Ensayar editor y arranque de juego en Windows 11 MSI con Unreal 5.8.2: NullRHI y D3D12; guardar, cerrar, recuperar, cambios y multiplicidad UWorld. Probar nativo Linux/Windows en CI y producto `TREK_HOST_TESTS=OFF`.
5. Guardar **informes permanentes pequeños en Git**. Builds/logs/cachés/test data solo en directorios temporales aislados conforme a `AGENTS.md` y `laboratorios/README.md`. Sin copias redundantes de motor Unreal/paquetes Core/3D. Medir bytes por carpeta antes/después, informar cualquier volumen significativo, reutilizar herramienta/compilación cuando sea posible y **dejar cada subdirectorio H06 eliminable en bloque**; retirar solo residuos generados por la tarea actual que se puedan eliminar sin daño. No borrar otros laboratorios sin autorización. Nunca crear dependencias de runtime hacia ellos.

## 5. Cierre H06/M1

Exigir: proyecto `.uproject` realmente aprobado y ejecutado, ABI y dependencias correctamente empaquetadas, una única sesión Core, consultas/órdenes admitidas por el dominio, recuperación H04, UI de diagnóstico, pruebas de vida por mundos y callbacks, evidencia **real** de UE NullRHI y D3D12, regresión nativa y PR auditada. Si faltan proyecto definitivo o bootstrap productivo, **H06/M1 permanece BLOQUEADA o PARCIAL**, aunque el adaptador nativo quede implementado. Ningún PASS está acreditado por este diseño.

Véase `H06_P04_P05_MATRIZ_PRUEBAS_2026-11-13.md` y `H06_ENCARGO_CODEX_2026-11-13.md`.
