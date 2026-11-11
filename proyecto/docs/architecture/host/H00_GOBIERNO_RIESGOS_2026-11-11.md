# H00-P03/P04 — Decisiones, gobierno y riesgos

**Fecha:** 2026-11-11. **Alcance:** auditoría documental, no configuración ni ejecución del HOST.

## Decisión aprobada y obligatoria HOST ↔ F11

1. **F11/Star Trek + CoreRPG** son dueños de las reglas de ascensos, puestos/cadena de mando, evaluaciones, autorizaciones institucionales, creación/revocación de hechos y efectos persistentes. El emisor institucional **F11-P05-A02-03 se desarrolla y certifica en el proyecto principal Star Trek RPG**.
2. **HOST** es dueño de sesión, acceso operativo, principal vinculado a personaje, contexto de confianza local, comunicación, peticiones controladas, correlación de respuestas y gestión de guardado. No concede rangos, no inventa méritos, no autentica mediante `F04Ref` o `CAUSE=110501`, no reimplementa reglas F11 y no crea un emisor paralelo.
3. HOST define la envoltura operativa de la llamada; **F11 define su API de negocio y conserva la revalidación de autoridad**. Los contratos se versionarán y coordinarán; si no existe emisor productivo, denegación segura.
4. F11 certifica lógica/evidencia institucional; HOST certifica acceso, encaminamiento, sesión y manejo de respuestas. Una prueba de HOST **no certifica** F11, y viceversa.
5. Prohibido copiar `f11_trial_host.inc` o exponer un endpoint de emisión por Blueprint, LLM, NPC o consola; no mantener expedientes/rangos laterales.

## Reconciliación propuesta con el juego, sin alterar sus documentos históricos

- En `proyecto/docs/roadmap/master/fases/F11/README.md` y `PLAN_F11_ACTUALIZADO_2026-11-11.md` se documenta la decisión creativa **USS Enterprise NCC-1701-D modernizada**. Es la decisión vigente para la campaña, aunque el plan maestro general del juego contenga todavía lenguaje histórico sobre una nueva clase Valhalla.
- El catálogo F04 `F04_VALHALLA_FLAGSHIP` es una referencia técnica histórica de dotación. **No** se renombra ni reinterpreta automáticamente como identidad del objetivo narrativo Enterprise-D.
- `proyecto/docs/roadmap/master/ESTADO_GLOBAL.json` indica fecha 2026-11-03; no debe tratarse como actualización automática de la fase HOST ni editarse para simular certificaciones.
- Propuesta a gestionar en planificación general F11 (no en esta H00): reconciliar el texto introductorio del Plan Maestro F00–F15 con la última decisión, preservando actas históricas y revisando referencias de uso.

## Política de trabajo del HOST

- Un repositorio: `robdor80/Videojuego_StarTrek`. Fases H00–H13 en documentación `proyecto/docs/architecture/host/`; implementación futura en rutas definitivas pertinentes tras H01.
- Rama específica + PR por entrega. **Ninguna fusión sin autorización expresa del usuario.** No escribir directamente en `main`, no forzar push ni modificar pruebas fijadas para hacerlas pasar.
- Leer `AGENTS.md` y `laboratorios/README.md` antes de ejecutar trabajos. Resultados temporales de builds, diagnósticos, logs y pruebas únicamente en `laboratorios/<area>/<tarea>/`, ignorados por Git y eliminables sin romper producción; no borrar anteriores sin autorización. Ninguna dependencia definitiva hacia laboratorios.
- Conservar CoreRPG, sus pins, manifests, fixtures, oráculos y certificados históricos. Cambios que los afecten requerirán tarea explícita, justificación, tests y aprobación aparte.
- Definir en cada subfase `PLANIFICADO/IMPLEMENTADO/PROBADO/CERTIFICADO/FUSIONADO` con ámbito de evidencia. Un documento fusionado no acredita un runtime.
- ChatGPT: arquitectura, contratos, documentación, auditoría, validadores no invasivos. Codex: núcleo, persistencia, integración UE/Core y operaciones delicadas. Cada encargo a Codex indicará modelo y razonamiento; recomendación inicial en trabajo crítico: GPT-6 Alto.

## Revisión de protección GitHub

**Observado mediante GitHub API a fecha 2026-11-11:**

- `GET /repos/robdor80/Videojuego_StarTrek/branches/main` → `protected: false`.
- `GET /repos/robdor80/Videojuego_StarTrek/rulesets` → `[]`.
- Lectura de `branches/main/protection` desde la conexión GitHub → 403 por permisos de la integración. La información pública disponible indica que **no se ve una protección activa**; no permite inspeccionar detalles restringidos.
- No se han cambiado ajustes de GitHub, permisos, bypass o reglas.

**Propuesta que requiere revisión/aplicación por el propietario** en *GitHub → repositorio → Settings → Rules → Rulesets* (o la sección de Branches disponible): crear una regla para `main` que impida borrado y force-push y requiera PR antes de integrar, sin bloquear la cuenta única con requisitos de aprobación imposibles. Configurar checks exigidos **solo después de determinar los nombres estables y su ejecución real**; nunca fijar un check inexistente. Mantener posibilidad de reparación administrativa controlada. Verificar posteriormente `protected: true`/ruleset activo y hacer una comprobación no destructiva.

**Importante:** proponer reglas no equivale a activarlas. La activación no forma parte de esta PR documental y queda como riesgo pendiente de gestión, prioritario antes de modificar código crítico en H02.

## Registro de riesgos

| ID | Prioridad | Riesgo | Mitigación / responsable | Estado |
|---|---|---|---|---|
| HG-01 | ALTA | `main` sin protección visible | Propuesta de Ruleset; activación y comprobación por propietario | **ABIERTO** |
| HG-02 | ALTA | Confundir laboratorios UE con juego definitivo | Registrar ausencia de `.uproject`, separar H06 | CONTROL DOCUMENTAL |
| HG-03 | CRÍTICA PARA F11 | HOST usurpe emisor o validaciones F11 | Restricción explícita y contrato entre responsables | CONTROL DOCUMENTAL; verificar en H01/H07 |
| HG-04 | ALTA | Guardado Core válido pero procedencia no confiable | Política de confianza local y pruebas negativas en H01/H04 | ABIERTO |
| HG-05 | ALTA | Unificar pins o cambiar oráculos históricos inadvertidamente | Inventario de SHA y prohibición de cambio implícito | CONTROL DOCUMENTAL |
| HG-06 | MEDIA | Roadmap general desactualizado respecto a Enterprise-D | Reconciliación futura en proyecto juego, sin borrar histórico | ABIERTO |
| HG-07 | ALTA | Declarar nativo/CI de laboratorios como UE5 jugable | Criterios de madurez independientes por alcance | CONTROL DOCUMENTAL |
| HG-08 | MEDIA | Pretender IA, sensores o scheduler genérico ya implementados | Alcance exacto F05/F06 y adaptación por etapas | CONTROL DOCUMENTAL |

## Puerta para iniciar H01

H01 puede comenzar con estas restricciones documentadas. **No** se programarán servicios críticos ni se considerará `main` protegida hasta resolver HG-01. La fusión de la PR de H00 y la aceptación administrativa quedan a decisión del usuario.
