# Encargo para Codex — F11-P05-A02-03, emisor institucional de producto

**Modelo recomendado:** GPT-6, pensamiento **ALTO** (o la opción de mayor razonamiento disponible en Codex, si esa denominación difiere).
**Momento:** próxima sesión, con cuota disponible.
**Estado actual:** punto 1 ya fusionado (#108 y #109). Este encargo no representa una implementación completada.

## Prompt listo para pegar

> Repositorio `robdor80/Videojuego_StarTrek`, rama base `main`. Te autorizo a ejecutar la fase **F11-P05-A02-03, punto 2 — emisor institucional REAL** solo en una rama y PR **Draft** independientes, con enfoque de seguridad por defecto, revisión y pruebas nativas. NO fusiones sin mi autorización. Si encuentras una frontera de confianza irresoluble, **para la parte mutadora** y documenta el bloqueo; no fabriques una bandera `verified` ni copies fixtures de prueba a producción.
>
> **Primero LEE** `AGENTS.md`, `proyecto/docs/decisions/F11-P05-A02-03_EMISOR_INSTITUCIONAL_PREIMPLEMENTACION_2026-11-11.md`, `proyecto/docs/decisions/F11-P05-A02-03_MATRIZ_PRUEBAS_EMISOR_v0.1.json`, contrato de PR #108 y lector C++ de PR #109. Recorre el código real, especialmente:
>
> - `desarrollo/integration/f04/src/f04_bridge.cpp` (session, schema, save/load, scopes, workstate) y `desarrollo/integration/f04/unreal/F04CampaignSubsystem.cpp`.
> - `desarrollo/integration/f11/src/f11_schema.inc`, `f11_promotions.inc`, `f11_trial_host.inc`, `include/f11_promotions.h`, `CMakeLists.txt`.
> - `desarrollo/integration/f11_host/` (lector de producto, 17 pruebas por plataforma, runner y aislamiento).
> - `juego/UE5/StarTrekRPG/README.md`: comprobar si aún falta el proyecto principal real.
> - `desarrollo/integration/f05/core-revision.txt` (`76a7b7b485616d8c4994f384a90f123bf333591d`) y `desarrollo/integration/f04/core-history-revision.txt` (`89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`).
>
> **Primer entregable obligatorio — amenaza y arquitectura:** identifica qué módulo posee la sesión, cómo se establece principal/partida autenticados y de dónde sale una autoridad institucional competente. Distingue integridad de gameplay offline de seguridad resistente a un cliente que controle el ejecutable. No presentes `f04_load`, un checksum, `CAUSE=110501` ni `F04Ref` como autenticación. Si no existe una fuente de confianza real, deja el emisor fail-closed y plantea la decisión necesaria sin inventar un servidor, cifrado o credencial dentro del cliente.
>
> **Segundo entregable — implementación solo si la frontera está resuelta:** crea un servicio **privado nativo del Host** capaz de emitir hechos legítimos de graduación, orden de comisión, comisión, concesión de Personal, evaluación, causa y orden institucional en el mismo `CoreRPG.WorldState`, nunca en sidecar, y autorizando únicamente la primera transición `1101 -> 1102`. No permitir APIs `issue_grant(actor_id, verified=true)`, rutas Blueprint, LLM, NPC, GUI o PADD con facultad de autorizar. El capitán o el oficial de guardia no heredan esta facultad por rango. Conservar la semántica de `f11_commit_promotion` y el lector C++ fusionado. Debe funcionar por **staging completo + schema + revalidación + commit atómico**, sin cambios parciales en rechazos.
>
> **Reglas estrictas de compatibilidad:** no reutilices como credencial la raíz de ensayo `CAUSE=110501`; protege los expedientes previos con migración/versionado explícitos. No modifiques por comodidad los 13 casos F11, las 4 pruebas Host, A02-02, F04/F05, los 6 históricos ni sus oráculos; ningún `SKIP` o green artificial. No cambies CoreRPG ni pins. No alteres `ESTADO_GLOBAL.json`. No crees el proyecto Unreal definitivo ni traslades assets: esa integración necesita su propio paso verificable.
>
> **Pruebas:** utiliza los 33 escenarios `TRUST-xx`, `COMMISSION-xx`, `GRANT-xx`, `PROMOTION-xx`, `REPLAY-xx`, `REGRESSION-xx` y `UNREAL-xx` de la matriz; enlaza cada uno a prueba real, evidencia y estado (PASS, FAIL o BLOCKED con motivo). Prioriza denegación por suplantación, archivo falsificado y checksum correcto, ventana caducada, revocación antes de commit incluso en el mismo tick, error de referencias, repetición exacta, clave con payload distinto, rollback completo, otro proceso y seis campañas históricas. Ejecuta Linux GNU y Windows MSVC contra el binario de producto y el Core pin exacto. Para Unreal, no afirmar `NullRHI`/`D3D12` ni `UE5_JUGABLE` sin ejecución real en MSI y un `.uproject` existente.
>
> **Ubicación de trabajo:** respeta `AGENTS.md`: todo producto nuevo en rutas definitivas aprobadas; cualquier artefacto temporal dentro de la zona ignorada de laboratorios del propio repositorio, desechable, nunca commiteado ni necesario para producción. No borres experimentos previos.
>
> **Entrega:** PR Draft con lista de archivos tocados, contratos/versiones, compiladores, comandos verificables, pruebas por plataforma, huellas de oráculos, denegaciones observadas y riesgos residuales. Si alguna condición de seguridad o la fuente de autoridad queda sin resolver, informa y mantén la PR en Draft y el emisor desactivado. **No fusionar.**

## Criterio de revisión humana posterior

Al terminar Codex: verificar de forma independiente que no se exportó el emisor de ensayo, que la autoridad no procede de parámetros inventados por el cliente, que los guardados no se autentican con el checksum del Core, que la nueva raíz productiva no se confunde con `110501`, que el pin y los históricos siguen intactos, y que ninguna prueba pendiente ha sido declarada verde. Solo entonces debatir la fusión.
