# H06-P04/P05 — Matriz de verificación HOST ↔ Unreal Engine 5

**Fecha:** 2026-11-13. **Estado:** DISEÑADA, TODAS las pruebas `NOT_RUN` en esta fase. No confundir las pruebas nativas H05 (M0) con ejecución UE H06 (M1). **Responsable:** ChatGPT (oráculos y auditoría), Codex (implementación y ejecución local). UE esperado: 5.8.2 en Windows 11 x64/MSI. **No inventar resultados o métricas.**

## Puertas técnicas (G0–G4)

| ID | Comprobación | Cierre obligatorio |
|---|---|---|
| G0 | Inventario real de proyectos `.uproject` y decisión de proyecto principal | Proyecto UE definitivo elegido/aprobado. Sin elección, PROYECTO BLOQUEADO, no promover laboratorios |
| G1 | Compatibilidad binaria UE↔DLL HOST | ABI estable con memoria/tipos controlados, carga y packaging `TREK_HOST_TESTS=OFF` sin STL/exception/ptr Core cruzando |
| G2 | Ciclo de vida, Game Thread, hilo propietario de Core | Ninguna espera bloqueante en Game Thread; revalidación de generación y limpieza |
| G3 | Identidad/autoridad | Cero actor/issuer arbitario desde UI; personaje legítimo vinculado por H03 o escenario marcado BLOQUEADO |
| G4 | Core/H04/F05/F11 | Guardados H04; reglas Core y F05; F11 sin emisor local; no tests-only hooks en producto |

## Casos HU-01..HU-25

**Oráculos:** pruebas positivas usan únicamente la API y el dominio reales; un test de fixture solo es válido si está rotulado como tal. Capturar versión UE, modo RHI, SHA de Git y Core, comando, estado, duración, memoria y enlace a evidencia.

| Caso | Prueba | Oráculo / resultado exigido | Capa |
|---|---|---|---|
| HU-01 | Inventario de `.uproject`, rutas y origen | Sin supuestos; README principal coincide con inventario; aprobación G0 registrada | inspección |
| HU-02 | No promover F02/F05 labs ni modificar originales | Diff solo de producto autorizado; no pérdidas de recursos | inspección |
| HU-03 | UBT/UHT real del módulo de producto | Build Win64 Editor y juego PASS, sin hacks de copia ni símbolos no resueltos | Windows/UE |
| HU-04 | Carga de DLL producto con tests OFF | `TrekHost` + `TrekF04Bridge`, dependencias resueltas, Core pin esperado | Windows/UE |
| HU-05 | ABI bajo compilación UE y CMake independientes | Tipos triviales, longitudes, memory ownership, errores, versión; no cruce STL/UObject/Core | nativo/UE |
| HU-06 | Abrir campaña una vez | Una instancia de `SessionOwner`, transición y generación correctas | UE |
| HU-07 | Inicio sin identidad legítima | `PRINCIPAL_UNBOUND` o denegación; sin exponer PERSON ajeno | UE |
| HU-08 | Vinculación de personaje | Camino H03 de confianza, no elegir ID/actor en UI; si falta, BLOCKED documentado | UE |
| HU-09 | Consulta de vista válida | Datos filtrados/copiados, sin WorldState ni RNG; lectura no muta | UE/Core |
| HU-10 | Emisión F05 por actor autorizado | Solo si G3 disponible; estado ISSUED real y número/key correctos | UE/Core |
| HU-11 | No exponer receptor/ejecutor M0 | Test-only `GatewayTestAccess` ausente de producto y Blueprint | estático/UE |
| HU-12 | Rechazo F05 de revisión/competencia | Código de dominio coherente, UI no auto-reintenta ni inventa privilegios | UE/Core |
| HU-13 | SAVE H04 y persistencia durable | UI no afirma guardado antes de confirmación H04 | UE/disco |
| HU-14 | RESTORE de la misma campaña | Nueva generación; identidad, revisión, reloj y resultados Core conservados | UE/Core |
| HU-15 | Callback tardío después de RESTORE | No actualizar HUD ni mutar con generación anterior | UE |
| HU-16 | Callback tardío después de cerrar | No acceso a UObject destruido; no false success ni deadlock | UE |
| HU-17 | Dos UWorld simultáneos | Proyecciones/Actors separados; una sola sesión/identidad Core | UE |
| HU-18 | Cambio de mapa / world travel | Representaciones previas caducadas sin destrucción de partida por error | UE |
| HU-19 | Denegación de ruta/save inválido | H04 conserva ranura y sesión sanas, no lectura parcial ni traversal | UE/disco |
| HU-20 | F11 institucional no disponible | `SERVICE_UNAVAILABLE`, sin librería ni trial host de emisión | producto |
| HU-21 | UMG/diagnóstico en Game Thread | Resultado y errores accesibles; sin `.get()` bloqueante | UE |
| HU-22 | Pruebas `-nullrhi` | Automation nativa UE y juego sin render, evidencia ejecutada | MSI/UE |
| HU-23 | Pruebas D3D12 | Arranque gráfico, interacción, cierre/recovery sin bloqueos, evidencia ejecutada | MSI/UE |
| HU-24 | Regressions H02–H05 y dependencias | CTest Windows/Linux/ASan cuando proceda y producto OFF, sin cambiar oráculos | CI |
| HU-25 | Higiene de laboratorios | Tamaño real antes/después, no duplicados masivos, artefactos finales independientes, carpeta temporal H06 eliminable | local/inspección |

## Clasificación y evidencia

- Tabla de estados de cada caso: `PASS`, `FAIL`, `SKIP`, `NOT_RUN` o `BLOCKED` (bloqueo de prerrequisito). Cada uno con SHA, dispositivo/modo, comando ejecutado, ruta relativa del informe y una breve prueba del oráculo; `SKIP` no cuenta como `PASS`.
- Ejecutar en un `StarTrekRPG.uproject` verificado, no en una copia de laboratorio, para declarar HU-03, HU-06..HU-23. Ejecutar `-nullrhi` no sustituye una pasada D3D12, ni una preparación estática `check_unreal_preparation.py` sustituye UBT/UHT.
- Para `HU-10` no fingir una orden real cuando no hay bootstrap productivo de personaje. Se permite prueba independiente limitada del adaptador nativo, expresamente `FIXTURE`, que **no cierra M1**.
- H05 ya documentó 236/236 nativos en Windows y Linux, 81/81 sanitizers en su HEAD; esas cifras son históricas y **no son resultados H06**. Reportar recuentos nuevos sobre SHA H06.
- Inspeccionar y medir los datos temporales tras cada pasada; los resúmenes permanentes y reproducibles se registran en `proyecto/docs/architecture/host/H06_RESULTADOS_2026-11-13.md` con SHA y enlaces de Actions si existen. Dejar `laboratorios/host/h06/` prescindible en bloque; no borrar contenido previo ajeno.
- El módulo de Unreal no debe referenciar rutas absolutas ni `laboratorios/` en archivos definitivos, ni copiar assets artísticos originales ni crear paquetes grandes inútiles.

**Cierre M1:** G0–G4 superadas, HU-01..HU-25 comprobados según alcance de producto y evidencia ejecutada en editor/juego; cualquier bloqueante necesario mantiene H06 `PARCIAL/BLOCKED`. **La certificación integral es H13.**
