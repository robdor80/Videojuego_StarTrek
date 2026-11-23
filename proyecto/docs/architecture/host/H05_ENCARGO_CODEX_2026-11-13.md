# H05 — Encargo para Codex: pasarela CoreRPG y hito nativo M0

**Modelo recomendado:** GPT-6. **Razonamiento recomendado:** Alto.  
**Proyecto:** HOST Star Trek RPG · **Repositorio:** `robdor80/Videojuego_StarTrek`.  
**Fase:** H05-P01/P02/P04, con proyección mínima H05-P03 conforme al contrato preparado por ChatGPT.  
**Estado de este encargo:** PROPUESTO/DOCUMENTADO, todavía NO EJECUTADO.  
**Base de diseño inspeccionada:** `main` SHA `4889e5b442d56b7a883261c6c51dfb57499ce825` (13/11/2026); comprueba su HEAD al empezar y parte del `main` más reciente que contenga estos documentos.

## INSTRUCCIONES A CODEX (copiar íntegramente como tarea)

Trabaja en el repositorio `robdor80/Videojuego_StarTrek`. **Implementa H05 — Pasarela CoreRPG y primer ciclo funcional nativo M0**. Lee primero `AGENTS.md`, `laboratorios/README.md`, `proyecto/docs/architecture/host/PLAN_MAESTRO_HOST_v1.2_2026-11-11.md` y, de forma obligatoria, los documentos H05:

- `proyecto/docs/architecture/host/H05_P01_P03_CONTRATO_M0_2026-11-13.md`
- `proyecto/docs/architecture/host/H05_P04_MATRIZ_M0_2026-11-13.md`
- `proyecto/docs/architecture/host/H04_ACTA_FUSION_2026-11-13.md`, `H04_PERSISTENCIA_2026-11-13.md`, `H03_IDENTIDAD_NATIVA_2026-11-13.md` y `H01_P02_CONTRATOS_v1.0_2026-11-11.md`

**No comiences suponiendo que las interfaces están terminadas**: inspecciona primero `desarrollo/integration/host`, `desarrollo/integration/f04/include/f04_bridge.h`, `desarrollo/integration/f05/include/f05_orders.h`, `f05_player_binding.h`, sus implementaciones, CMake y CI. El pin de Core actualmente exigido por H02–H04 es `76a7b7b485616d8c4994f384a90f123bf333591d`; confirma limpieza y coincidencia de pin, no lo cambies ni migres otras fases.

### Objetivo de producto

Conseguir un ciclo reproducible sin UE: una partida nativa de `TrekHost` se abre, el flujo interno legítimo vincula un PERSON de la campaña, HOST proporciona una vista filtrada, la intención autorizada del jugador emite una orden de F05, el destinatario real la recibe y ejecuta una vez en Core, se consulta el resultado, se guarda por H04, se cierra y se restaura desde **otro proceso**, verificando la igualdad de hechos, revisión, reloj, RNG e identidad y que la generación antigua ha caducado.

La operación demostrativa compatible es **F05 P01 → F04_SCAN** en el fixture nativo, con `f05_submit`, `f05_receive`, `f05_execute_order` y consultas F05/F04. **No es el motor de sensores F06 ni un escaneo que detecte contactos**. La persona del fixture no es el cadete final de la Academia. Los datos de fixture no sustituyen reglas reales ni son una interfaz de producción.

### Implementación requerida

1. **H05-P01 — composición de producto.** Ampliar `TrekHost` existente de manera aditiva y mínima, conservando `SessionOwner` como único propietario de `F04Session*`, FIFO, threading, H03 y H04. Compilar con F04/F05/Core reales y pin verificado, sin F11 trial. Validar producto Release `TREK_HOST_TESTS=OFF` en Linux/Windows, carga y exportaciones. Mantener y probar configuraciones de tests separadas.
2. **H05-P02 — pasarela tipada de órdenes.** Definir una API interna C++ pequeña en la capa HOST para consulta, emisión de orden, consulta de orden/resultado y manejo de estado, delegando en F05. Hacer revalidación efectiva en el hilo propietario: generación, binding H03, observador/actor derivado del vínculo y revisión vigente. Nunca aceptar un F04Ref/actor inyectado como acreditación por el cliente. Implementar recepción/ejecución con semántica de **destinatario real**: para M0 usar infraestructura interna exclusivamente de prueba para simular la llamada legítima del destinatario, sin publicar en producto un setter de actor o capacidad libre de suplantación. Si una API de producto para receptor requiere H08/H09, dejarla cerrada y expresarlo claramente.
3. **H05-P03 — proyección mínima.** Crear solo la vista de lectura requerida por la demo, ligada a generación y observador admitidos; no serializar mundo ni mantener cache autoritativa. Consultas no mutan Core y fallos devuelven salida vacía. Conservar los nombres reales de tipos y sus invariantes en el informe, contrastados con el contrato propuesto por ChatGPT.
4. **H05-P04 — ciclo E2E real.** Implementar tests nativos de proceso nuevo para SAVE/RESTORE con una orden y un resultado Core auténticos. Comprobar respuesta de F05, estados, idempotencia de key F05 (no `correlation_id`), error por payload distinto, revisiones caducadas, ausencia de vínculo, suplantación, scope/competencia, cierre y restauración, concurrencia y ausencia de efecto parcial ante rechazo. Repetir pruebas históricas pertinentes sin reescribir sus oráculos ni relax de expectations.
5. **Medir almacenamiento después de H05-P04**: bytes y objetos reales por generación y repetición de contenido entre guardados. No optimizar a ciegas; no eliminar generaciones. Dejar propuesta de deduplicación/retención para H12-P04 salvo hallazgo crítico demostrado.

### Reglas de seguridad y alcance

- **CoreRPG sigue siendo fuente de verdad** y F04/F05 deciden competencia, transacciones, hechos y códigos de rechazo. No copiar reglas a HOST, no mantener historial, orden ni RNG paralelo. No escribir en otro formato de partida: usar el mecanismo H04 que valida snapshots Core.
- **F11 es ajeno a H05**. No implementar emisor, ascensos, permisos, expedientes, rangos, F11-P05-A02-03, `f11_trial_host.inc`, ni enlazar `TrekF11TrialHost`. Las solicitudes institucionales quedan indisponibles hasta H07 + API aprobada por el proyecto principal.
- Sin UE, UObjects, Blueprints, pantallas, servicios de red, login remoto, autenticación desproporcionada o nuevo repositorio. No crear un segundo propietario de sesiones ni hilo que toque Core por fuera de `SessionOwner`.
- Las operaciones con `expected_core_revision` stale se rechazan: nunca recomputar y ejecutarlas automáticamente. Si hay un timeout, consultar orden antes de actuar; no duplicar ejecución. No convertir un éxito en Core en confirmación durable de guardado.
- No modificar `main` directamente, pins históricos, esquemas originales Core, fuentes de certificación de F11, pruebas congeladas, proyectos UE o binarios/assets. Respetar `AGENTS.md`: **todos** los builds, logs, snapshots temporales y JUnit local en `laboratorios/host/h05/`, aislados, sin borrar laboratorios existentes y sin forzar su inclusión en Git. Los archivos definitivos de producto y las suites sí van en los árboles existentes de `desarrollo/integration/host` y workflows si hace falta.
- Trabaja en rama `feature/host-h05-pasarela-m0` (o nueva variante si existe), prepara **una Pull Request Draft hacia main**; no la fusiones. Mantén el alcance pequeño y registra cualquier cambio aditivo a H01/H02/H03/H04 claramente.

### Pruebas obligatorias y clasificación

Utiliza la matriz `H05_P04_MATRIZ_M0_2026-11-13.md`. Implementa sus HM-ID según corresponda, con casos positivos y negativos. CI como mínimo: Linux GCC y Windows MSVC nativos, Linux Clang ASan/UBSan, producto Release tests OFF ambos sistemas y regresión de H02–H04, F04/F05 y F11 aislada (sin enlazar F11 a HOST). Reporta cada resultado **PASS / FAIL / SKIP / NOT_RUN** honestamente, con SHA exactos, comandos, recuentos y enlace a Actions. Si no puedes ejecutar MSI/UE, no afirmes que se probaron.

Incluye dos informes **permanentes, versionados y COMMITIDOS en tu rama/PR** (no solo mensaje de chat, no solo artefacto efímero ni solo `laboratorios/`):

1. `proyecto/docs/architecture/host/H05_INFORME_IMPLEMENTACION_2026-11-13.md`: inventario por archivo, arquitectura final y diferencias frente a contrato, decisiones de confianza, manejo de revisión/idempotencia/errores, pin y repos SHA, resultados HM-ID, limitaciones, riesgos, tamaño de guardados real y clasificación IMPLEMENTADO/PROBADO/NO CERTIFICADO/NO FUSIONADO.
2. `proyecto/docs/architecture/host/H05_RESULTADOS_M0_2026-11-13.md`: instrucciones reproducibles, tabla por plataforma y suite, JUnit/resúmenes con PASS/FAIL/SKIP, URLs de GitHub Actions, prueba entre procesos, evidencia de carga producto y oráculos de integridad; declarar cualquier RUN no realizado.

No sustituyas resultados de tests por frases genéricas como «todo PASS». Los logs crudos quedan en `laboratorios/host/h05/`, pero **los informes MD deben estar en GitHub** para que ChatGPT pueda acceder y auditar sin tu entorno local. Al terminar, responde con enlace a la PR Draft, HEAD SHA, enlaces directos a ambos informes y bloqueos pendientes. No marques H05 CERTIFICADA: M0 probado es un hito parcial; la certificación integral corresponde a H13.

**Criterio de éxito:** M0 completamente trazable y probado en Core real (con las limitaciones declaradas) y ningún bypass de identidad, permiso o persistencia. Si falta una API imprescindible, deja la parte bloqueada con evidencia reproducible: nunca simules falsamente que M0 se ha alcanzado.
