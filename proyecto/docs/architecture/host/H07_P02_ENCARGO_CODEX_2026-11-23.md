# ENCARGO CODEX — H07-P02 · Admisión institucional privada y cierre seguro

**Modelo recomendado: GPT-6. Nivel de razonamiento: ALTO.**
**Proyecto:** robdor80/Videojuego_StarTrek, rama de trabajo propia desde main actualizado.
**Estado:** PROMPT PREPARADO; no ejecutado. Comenzar SOLO cuando H07-P01 haya sido revisada y la dependencia de documentación esté disponible en la rama base.
**Entorno primario:** Codex Cloud (Linux/Windows CI); no requiere MSI para esta subfase.

## Contexto que debes leer ANTES de modificar

1. AGENTS.md y laboratorios/README.md.
2. proyecto/docs/architecture/host/H07_P01_AUDITORIA_PLAN_2026-11-23.md, H07_P01_CONTRATO_FRONTERA_v0.1_2026-11-23.md y H07_P04_MATRIZ_ACEPTACION_v0.1_2026-11-23.json.
3. Plan Maestro HOST v1.2 y H01_P02/H01_P03; H05 M0, H06 acta M1, decisión F11-P05-A02-03.
4. desarrollo/integration/host/{CMakeLists.txt,src/native_session.cpp,src/session_owner.cpp,src/gateway_bridge.cpp,src/host_abi.cpp,include/trek/host/{session_owner.h,host_abi.h},tests/m0_tests.cpp}.
5. desarrollo/integration/f11/include/f11_promotions.h y desarrollo/integration/f11_host/include/f11_host_reader.h. No tocar ni reutilizar el emisor trial.
6. Confirmar PR #108/#109 fusionadas y #110 Draft; no absorber el código o documentos de esta última sin revisión.

## Misión estricta P02

Auditar si la protección ya implementada en SessionOwner::institutional_command y NativeSession::dispatch cumple el cierre seguro exigido por H07 **sin cambiar nada**. Su implementación actual devuelve SERVICE_UNAVAILABLE antes de bridge::dispatch. Prioriza **reutilizar** la implementación existente y ampliar pruebas negativas donde falten. Solo si detectas un fallo reproducible y relevante, realiza el cambio mínimo y aditivo.

Comprobar que una intención institucional sin emisor F11 de producto no puede:
- acceder a la biblioteca trial o a un setter de grants/rank;
- seleccionar principal, F04Ref, sujeto institucional, permiso o verified desde UI/LLM/Blueprint;
- sortear binding, generación, cierre/restore y estado Academy;
- reintentar tras carga como si el correlation_id fuera autorización;
- mutar el WorldState, RNG, reloj, historia ni archivo de guardado ante la denegación.

Mantener los códigos HOST adecuados: SESSION_CLOSED, PRINCIPAL_UNBOUND, ACCESS_DENIED, GENERATION_EXPIRED, BUSY_STATE y SERVICE_UNAVAILABLE según contexto real. No cambiar los tipos o valores de la ABI C por estética. No exponer una nueva operación de emisión. No simular servicios F11 ni insertar hechos profesionales artificiales.

## Diseño y límites de ejecución

- Capa institucional **F11** decide requisitos, comisiones, órdenes, concesiones, promociones y revocaciones; esta tarea **NO** implementa ninguna de esas reglas.
- CoreRPG mantiene autoridad persistente; no tocar CoreRPG, pins, oráculos, tests históricos ni sus manifiestos.
- No convertir AcademyCampaign de H06 en F04Session, no comisionar automáticamente al protagonista ni usar CAUSE=110501 como autorización.
- No añadir arquitectura de servidores, tokens remotos, cifrado ficticio ni persistencia paralela.
- Si el guard ya es suficiente, entregar un informe de inspección y pruebas; ningún refactor es necesario. Codex no debe gastar cambios en una función que ya cumple.
- Mantener pruebas o implementaciones realmente temporales únicamente en laboratorios/host/h07/p02/; no versionar esta carpeta.
- No empezar P03 composición F11 reader en esta PR. P03 vendrá después de auditar P02.

## Pruebas y evidencia requeridas

1. Tests del HOST para sesión cerrada, identidad ausente, Academy, generación antigua, cambio de generación por LOAD, alcance/permiso y servicio ausente.
2. Medición estricta de estado Core antes/después de un rechazo: comparar bytes o equivalencia completa auditable; no declarar atomicidad solo por error_code.
3. Repetir con distintas correlaciones: ninguna emisión, ninguna cola de efecto institucional.
4. Verificar test previo host.m0.institutional y los demás H02–H06/F04/F05 pertinentes en Linux y Windows/MSVC con Core pin exacto. No asumir PASS por el estado de otra PR.
5. Guardar en informe commit exacto, comandos, suites ejecutadas, conteo real, fallos, SKIP y enlaces de Actions. Indicar si una prueba requiere MSI o si esta fase no lo necesita.
6. Si es relevante, comprobar que la ABI productiva no exporta rutas F11 de emisión ni el trial; no mezclar la certificación F11 de terceros.
7. Actualizar únicamente estados **realmente ejecutados** de la matriz H07 en su propia rama, conservando los 33 escenarios F11 externos como NOT_RUN salvo evidencia externa trazada (nunca contarlos como tests HOST).

## Entrega

- Rama propuesta: feature/host-h07-p02-admision-institucional.
- PR **Draft** hacia main, sin fusionar.
- Informe permanente: proyecto/docs/architecture/host/H07_P02_RESULTADOS_2026-11-23.md (adaptar fecha real al día de ejecución).
- Cambios nativos mínimos solo si hay defecto demostrado; pruebas negativas añadidas cuando aporten cobertura nueva.
- Resultado que distinga IMPLEMENTADO heredado, PROBADO en HEAD, DEFECTO REPARADO, BLOQUEADO POR F11 y NO EJECUTADO.
- No avanzar a H07-P03, no autorizar generación de hechos F11, no cerrar H07 global.

**Criterio de cierre P02:** cierre institucional seguro probado en una versión concreta del HOST, sin emisor propio, sin nuevas vías de autoridad y con regresiones pertinentes en verde. Si falta infraestructura externa para los tests, documentarlo como bloqueo verificable, no como PASS.
