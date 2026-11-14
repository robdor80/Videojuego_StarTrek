# Encargo a Codex — F10-P03 / H06-P06: primer corte nativo de candidato Academia

**Fecha:** 14-11-2026. **Modelo recomendado: GPT-6. Razonamiento: ALTO (High).**  
**Repositorio:** `robdor80/Videojuego_StarTrek`. **Crear rama propia desde main** que incluya el contrato de interfaz y prueba estática de 14-11-2026. **PR en Draft**; no fusionar.  
**Responsables:** Codex (implementación C++ compleja), ChatGPT (contratos, auditoría); F10 define admisión; F11 define comisión profesional.  
**Objetivo:** superar de forma real y verificable la primera dependencia de [issue #148](https://github.com/robdor80/Videojuego_StarTrek/issues/148) y después desbloquear [#144](https://github.com/robdor80/Videojuego_StarTrek/issues/144). H06-P06/M1 siguen parciales.

## 0. Documentación obligatoria

Leer completos:
- `AGENTS.md`, `laboratorios/README.md`, el plan maestro H00–H13, y el contrato [F10_H06_P06_CONTRATO_INTERFAZ_ACADEMIA_2026-11-14.md](F10_H06_P06_CONTRATO_INTERFAZ_ACADEMIA_2026-11-14.md).
- `sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json` y su test estático `desarrollo/tools/validation/test_f10_host_candidate_contract.py`.
- `H06_P06_INFORME_FACTIBILIDAD_2026-11-13.md`, `H06_P06_MATRIZ_PRUEBAS_2026-11-13.md`, `H03_IDENTIDAD_NATIVA_2026-11-13.md`, implementación H04, `F10/README.md`, `F10/ACTA_P01_P05_REFERENCIA_2026-10-14.md`, los contratos `character_creation` y F11.
- Código actual de `SessionOwner`, `PlayerBootstrap`, `NativeSession`, `host_abi`, F04, F05, `juego/UE5/StarTrekRPG` y las APIs CoreRPG **fijadas** en `76a7b7b485616d8c4994f384a90f123bf333591d`.

## 1. Gate de factibilidad obligatorio, antes de tocar producto

En un documento del repositorio, identificar exactamente cómo crear un WorldState de campus Academia con catálogo/schema/historia y PERSON real **sin modificar CoreRPG fijado ni disfrazar `f04_create_population` como Academia**. Probar, mediante código pequeño de spike nativo, si las APIs genéricas `create_entity`, `declare_population`, `materialize_population`, `bind_definition`, `add_relation` y persistencia del pin permiten un escenario `starfleet_academy` legítimo con guardado/restauración transaccionales.

**Si no se puede garantizar el modelo de catalogación, persistencia o rollback con el pin**, NO introducir atajos: detener solamente el tramo afectado, documentar por qué no cabe la ruta A y ofrecer ruta B aditiva de F04 con impacto de compatibilidad y decisión necesaria. No hacer un cambio del pin o API histórica de forma silenciosa. La prueba de C11 `OPEN academy` debe seguir protegiendo la ABI naval actual mientras no se apruebe el endpoint Academy.

## 2. Implementación incremental cuando gate permite continuar

**F10-A. Factory privado mínimo:** crear campaña Academia para candidato con biografía `campaign_created` validada por **reglas objetivas y revisión semántica**, separando perfil de jugador y personaje. No aceptar `trusted_origin`, `validated_creation_ref`, `admission_authorized`, `person_id`, rango, permisos o F11 desde UI. La validación semántica debe aportar una revisión verificable por el dominio; si falta proveedor/flujo aprobado, mantener borrador sin PERSON y reportar dependencia; no falsificar una aprobación. Fecha aprobada: año 2383, **sin mes/día fijados**. No fabricar admisión automática.

**F10-B. Commit candidato:** crear exactamente una `PERSON`, `candidate`, identidad de campaña, biografía e historial aprobados, en un solo estado autoritativo. Misma intención reintentada produce mismo candidato; clave igual con biografía distinta se rechaza; fault injection no deja PERSON ni historial parcial ni consume RNG. Admitir es **operación separada F10**, con prueba de plaza/cohorte real cuando exista evidencia auténtica; `candidate` no consume plaza. Evitar nuevo sistema de población paralelo a Core.

**HOST-C. H03 en mismo owner:** vincular al sujeto mediante recibo interno de F10, sin `f05_bind_player` para el candidato. Vínculo operativamente exclusivo y durable en Core. Proyección de `BOUND` no concede ninguna orden naval. Un ID arbitrario enviado por cliente no puede activar jugador. Compatible con H03/F05 anteriores.

**HOST-D. H04 persistencia:** soporte explícito de escenario/catalogo Academy y versión de guardado, sin reinterpretar `TREKHOST4 1` de nave. Probar SAVE/RESTORE en procesos distintos, misma PERSON y biografía, generación renovada, nunca swap de partida ante importación incompatible. No alterar el historial F04/F05 validado.

**HOST-E. Unreal, después de lo anterior:** nueva operación por ABI compatible con UE5 y GameInstanceSubsystem, vista de candidato. No exponer setters de autoridad/IDs. UBT/UHT y tests NullRHI/D3D12 MSI; panel simple sin assets pesados. Si falta fase previa, marcar NOT_RUN en lugar de simular éxito.

## 3. Matriz y evidencia de cierre

Ejecutar casos pertinentes CB-01..CB-24, con estados honestos. Incorporar nuevos tests de replay, conflicto, rollback, plaza, importación, scope/generación, no permiso F05 y persistencia entre procesos. Mantener regresiones mínimas **239/239 Windows y Linux, 84/84 ASan/UBSan** del HEAD #147 más los casos nuevos, Release tests OFF en ambos OS, pin CoreRPG sin modificación y las suites F10/Academy Life. No declarar PASS por tests offline de referencia.

Todos los resultados brutos de CMake/UBT/pytest/logs van a la zona **ignorada** de `laboratorios/` conforme a AGENTS.md. Evitar duplicar motor UE5, checkout Core, grandes assets o paquetes, y **no borrar ni mover laboratorios existentes**; hay una limpieza concurrente. Ojo: Codex dejó un **worktree Git registrado** en su laboratorio H06-P06 anterior, no eliminar directorio sin `git worktree` y sin autorización de limpieza.

## 4. Entregables obligatorios

PR **Draft** sin fusión. Informes versionados y permanentes:
1. `proyecto/docs/architecture/host/F10_H06_P06_FACTIBILIDAD_NATIVA_2026-11-14.md`: existencia de catálogo, APIs, esquema, perfil validable, persistencia y límites.
2. `proyecto/docs/architecture/host/F10_H06_P06_IMPLEMENTACION_2026-11-14.md`: archivos, decisiones, fuentes y rutas.
3. `proyecto/docs/architecture/host/F10_H06_P06_RESULTADOS_2026-11-14.md`: SHA, comandos, CI/MSI, pruebas CB con PASS/FAIL/BLOCKED/NOT_RUN, evidencias.

Para terminar, comunicar **PR, HEAD, qué está IMPLEMENTADO, qué está PROBADO y qué permanece BLOQUEADO**. ChatGPT auditará; el usuario mantiene decisión sobre ampliaciones de alcance. Ni F10 ni H06/M1 ni H13 pueden declararse cerrados por un spike o tests de referencia.

**Modelo: GPT-6. Razonamiento: Alto (High).**
