# ENCARGO CODEX — H06-P06: bootstrap productivo del cadete, no emisor

**Fecha:** 13-11-2026. **Modelo:** GPT-6. **Razonamiento:** ALTO (High).  
**Repositorio:** robdor80/Videojuego_StarTrek, misma rama principal main. **Base:** main que incluya las tres fuentes documentales H06-P06 de ChatGPT.  
**Responsable:** Codex para C++/Core/UE e integración de persistencia; ChatGPT audita; F10 es propietario de admisión/ciclo académico; el usuario autoriza decisiones significativas y fusiones.  
**Estado de entrada:** H06 diagnóstico fusionado por PR #142, M1 parcial; issue #144 de seguimiento. NO hay creación real de cadete comprobada.

## Lee antes de editar

1. AGENTS.md, laboratorios/README.md, .gitignore y plan maestro HOST.
2. proyecto/docs/architecture/host/H06_P06_CONTRATO_BOOTSTRAP_CADETE_2026-11-13.md.
3. proyecto/docs/architecture/host/H06_P06_MATRIZ_PRUEBAS_2026-11-13.md.
4. H03_P01_IDENTIDAD_CONTRATO_v1.0_2026-11-13.md, H03_IDENTIDAD_NATIVA_2026-11-13.md, H06_RESULTADOS_2026-11-13.md y H06_ACTA_AUDITORIA_FUSION_PARCIAL_2026-11-13.md.
5. F10/README.md, F10/ACTA_P01_P05_REFERENCIA_2026-10-14.md, sistemas/gameplay/careers/academy_path/{README.md,admission_flow.json,academy_state.json}; character_definition_contract.json y character_runtime_model.json; generador de cadetes step2 y pruebas.
6. F11-P05-A02-00_CONTRATO_IDENTIDAD_RANGOS_AUTORIDAD_2026-11-11.md para mantener separada la comisión institucional.
7. Código real de HOST PlayerBootstrap, SessionOwner, bridge H04/F05, host_abi.h, subsystem UE, F04/CMake, y **pin CoreRPG 76a7b7b485616d8c4994f384a90f123bf333591d**; no sustituir Core fijado.

## Objetivo y condición previa

El jugador debe poder comenzar una **campaña legítima de candidato/cadete de Academia**, con PERSON autoritativa única y vínculo interno seguro al HOST, conservarla tras SAVE/RESTORE entre procesos y verla desde Unreal. **Esto no se consigue reutilizando el capitán/alférez del fixture ni abriendo miranda y llamándola Academia.** Una campaña nacida sin identidad sigue denegada hasta resolución legítima.

**Primera tarea obligatoria (sin codificar):** elaborar un diagnóstico de factibilidad con referencias exactas a APIs y fuentes reales. Responder explícitamente: 
- ¿Existe hoy un factory de producto en F10/Core para una campaña con escenario Academia, población, plaza y PERSON de jugador?
- ¿Puede resolverse una persona de Academia en el mismo SessionOwner y restaurarse por H04, cuando el restore actual crea miranda como contenedor?
- ¿Es válido f05_bind_player para un cadete sin puesto naval? ¿Es preciso desacoplar identidad de jugador de autoridad de órdenes F05?
- ¿Qué semántica de character_id precomisión y character_id profesional F11 se debe acordar con el propietario F10/F11?

**Regla de parada:** si cualquiera de estas rutas carece de contrato seguro y la reparación exige cambiar una API histórica F04/F05, el Core pin, F10 o la regla institucional F11, **NO improvises**. Entrega informe técnico con 2 alternativas concretas, impacto, criterios de compatibilidad y tarea desbloqueante; implementa únicamente los adaptadores/tests no mutadores e independientes que tengan contrato real. No crear un falso PASS ni una ruta insegura para cumplir el hito.

## Implementación permitida si la ruta real está soportada

**P06-A: creación interna de producto de F10/Core.** Proponer e implementar solo el corte mínimo aprobado por fuentes existentes: perfil campaign_created validado, condición CANDIDATE/ADMISIÓN que determine el dominio, cohorte y plaza real, PERSON una sola vez con identidad estable y procedencia. No resolver artificialmente todos los exámenes/4 años de F10. Mantener un único WorldState y la semántica de materialización genérica. No aceptar IDs, rango, autoridad, credenciales o admission_authorized del cliente como hechos.

**P06-B: vínculo H03.** Tras creación confirmada, flujo interno privado por worker de SessionOwner (como PlayerBootstrap::prepare/bind): un único personaje por campaña, comprobación de principal/campaña/scope/generación/revisión e idempotencia. Si hay que separar vínculo de jugador de binding de iniciativa F05, acordar y documentar extensión aditiva segura; NUNCA tocar F05 histórico sin plan autorizado. UE/ABI C recibe peticiones y vistas tipadas, no capacidad de elegir persona arbitraria ni puntero Core. No exponer API pública de bind con person_id libre; test hooks no se compilan en producto OFF.

**P06-C: persistencia y visualización.** H04 conserva identidad y hechos Core, NEW/LOAD/CLOSE gestionan generaciones/tickets y UWorld efímeros. Pruebas de recuperación entre procesos con la misma persona sin pérdida/duplicación de plaza. Interfaz sencilla es suficiente; no migrar assets artísticos ni crear otra plataforma. Un cadete sin competencia debe seguir sin órdenes de puente. F11 SERVICE_UNAVAILABLE, sin comisiones, rango 1101 o emisor por defecto.

## Pruebas, evidencias y ramas

- Ejecutar al menos la matriz CB-01..CB-24 en lo que proceda; PASS solo con resultados reales. Cubrir errores y fault injection transaccional, repetición/conflicto, SAVE/RESTORE entre procesos, denegación de importación alterada, caducidad por LOAD/CLOSE y exclusividad. Demostrar cero efectos parciales, no solo resultados UI.
- Repetir CTest Windows y Linux y ASan/UBSan, Release OFF sin símbolos/hooks de ensayo, pin Core intacto; después UBT/UHT Win64 Editor/Game y UE 5.8.2 NullRHI/D3D12 en MSI cuando el flujo esté implementado. No inventar pruebas de Unreal si no las ejecutas.
- Crear una rama nueva desde main (nunca sobre HEAD anterior de PR #142 ya fusionada) y PR **Draft**, no fusionarla. No reescribir versiones/suites históricas ni añadir files bajo laboratorios/ a Git.
- Informes **permanentes y versionados**:
  - proyecto/docs/architecture/host/H06_P06_INFORME_FACTIBILIDAD_2026-11-13.md
  - proyecto/docs/architecture/host/H06_P06_INFORME_IMPLEMENTACION_2026-11-13.md
  - proyecto/docs/architecture/host/H06_P06_RESULTADOS_2026-11-13.md
  Incluye commit SHA final, rutas, decisiones técnicas, evidencias, matriz CB-01..CB-24, resultados PASS/FAIL/BLOCKED/NOT_RUN, límites, dependencias externas, pruebas y reproducibilidad.
- **Disco y limpieza concurrente:** proteger los trabajos activos H06 y terceros; no borrar, mover ni limpiar laboratorios previos. Temporales nuevos exclusivamente laboratorios/host/h06-p06/ bajo checkout existente, evitar repetir descargas y builds enormes. No duplicar motor, Core ni los assets. Medir uso y confirmar qué es regenerable; no borrar sin autorización.
- Final: enlace PR Draft, HEAD, informes, resultados ejecutados y bloqueos. ChatGPT realizará auditoría independiente. **No declarar H06/M1 certificados ni terminados por una implementación parcial.**

### Distribución y economía de cuota

Este encargo requiere **GPT-6 / ALTO** por la frontera Core/H03/F05/H04, concurrencia y persistencia. Evitar procesos masivos de Unreal mientras falte la ruta productiva validada; hacer primero el estudio de factibilidad y los tests nativos del corte aprobado. Si la ruta exige una decisión de F10 o F11 no aprobada, documentar y detener solo esa parte.

**Prohibiciones claras:** no usar cadet:proc de referencia como sujeto autenticado, no fabricar una admisión con CORE_HOST_VERIFIED, no dar rangos de oficial sin comisión, no inyectar person_id desde Blueprint/IA, no habilitar f05_submit antes de competencia real, no mutar CoreRPG fijado ni promocionar F02/F05 como proyecto principal, no duplicar fuentes de verdad ni borrar laboratorios.
