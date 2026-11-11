# PLAN MAESTRO DEL HOST — STAR TREK RPG

**Versión de planificación:** 1.2 (11-11-2026; H00 auditada y documentada, decisión HOST/F11 vigente)  
**Estado:** H00 DOCUMENTADA y ENTREGADA PARA REVISIÓN (PR #111 Draft, sin fusionar); H01–H13 PLANIFICADAS. No se ha programado, ejecutado ni certificado un HOST nuevo.  
**Repositorio único de producto:** `robdor80/Videojuego_StarTrek` (`main` verificada en `816e72b2b6e2057c47b84473e616a6feda096016`).  
**Relación con el plan general:** fases propias `H00–H13`, independientes de `F00–F15` y trazadas a ellas.  
**Propiedad del cierre y fusiones:** usuario. **Arquitectura y revisión:** ChatGPT. **Integraciones críticas:** Codex.  
**Decisión vinculante:** separación HOST/F11 — el emisor institucional y las reglas F11 se desarrollan y certifican exclusivamente en el proyecto principal Star Trek RPG; HOST solo aporta infraestructura y consume sus contratos.

## ACTUALIZACIÓN H00 — 11-11-2026 (v1.2)

**Trabajo documental de H00 realizado por ChatGPT.** Se han verificado la estructura, las cabeceras, los pins de CoreRPG, las PR precedentes, el estado del juego Unreal y los límites de los laboratorios. Resultado publicado en la rama `docs/host-h00-auditoria-gobierno-20261111`, PR **#111**, abierta en Draft:

- [PR #111 — HOST H00: auditoría y gobierno](https://github.com/robdor80/Videojuego_StarTrek/pull/111)
- [Inventario y dependencias](https://github.com/robdor80/Videojuego_StarTrek/blob/docs/host-h00-auditoria-gobierno-20261111/proyecto/docs/architecture/host/H00_INVENTARIO_DEPENDENCIAS_2026-11-11.md)
- [Gobierno, separación HOST/F11 y riesgos](https://github.com/robdor80/Videojuego_StarTrek/blob/docs/host-h00-auditoria-gobierno-20261111/proyecto/docs/architecture/host/H00_GOBIERNO_RIESGOS_2026-11-11.md)
- [Acta de H00](https://github.com/robdor80/Videojuego_StarTrek/blob/docs/host-h00-auditoria-gobierno-20261111/proyecto/docs/architecture/host/H00_ACTA_2026-11-11.md)

**Comprobación de cambios:** la comparación con `main` muestra exactamente cuatro archivos `.md` nuevos, sin modificaciones en código, CoreRPG, Unreal, CMake, pruebas, pins, oráculos, historial ni `ESTADO_GLOBAL.json`. No se han ejecutado nuevas suites C++/Unreal: esta entrega posee madurez exclusivamente **DOCUMENTACION_AUDITADA**.

**Pendientes de gobierno:** `main` figura `protected:false` y sin rulesets; la configuración protectora está propuesta, pero NO aplicada. La PR #111 permanece abierta y no está fusionada. La conciliación del roadmap general con Enterprise-D se ha propuesto sin tocar el histórico. Estos pendientes no autorizan afirmar que el HOST esté implementado.

**Siguiente conversación:** H01 — Arquitectura y contratos del HOST (ChatGPT). H02 y las modificaciones críticas de producto quedan reservadas a Codex, después de validar los contratos y asegurar suficientemente la rama principal.

---

## 0. DECISIÓN ARQUITECTÓNICA OBLIGATORIA — FRONTERA HOST / F11

**Estado:** APROBADA POR EL USUARIO · **Fecha:** 11-11-2026 · **Carácter:** RESTRICCIÓN VINCULANTE para H00–H13, contratos, encargos a Codex, pruebas y criterios de cierre.

1. **F11 / capa de reglas Star Trek sobre CoreRPG** posee y desarrolla las reglas de ascenso, la cadena de mando, los requisitos, las validaciones institucionales, las decisiones de concesión/revocación y el registro autoritativo de hechos profesionales en CoreRPG. **F11-P05-A02-03, incluido su emisor institucional, se implementa, prueba y certifica en el proyecto principal Star Trek RPG**, no como tarea de construcción del HOST.
2. **HOST** posee el ciclo de sesiones, vínculo del jugador con el personaje, contexto de procedencia y confianza local proporcional, control de acceso a interfaces, encaminamiento de solicitudes, coordinación de respuestas/eventos, guardado/recuperación y conexión con Unreal. **No decide** si corresponde una comisión, un ascenso, una evaluación, una autorización institucional o un destino: presenta la solicitud a la API aprobada de F11/CoreRPG y devuelve su resultado sin reinterpretarlo.
3. **Prohibido en HOST:** implementar un segundo emisor, crear concesiones/órdenes de Personal por cuenta propia, mantener expedientes o rangos paralelos, copiar `f11_trial_host.inc`, duplicar validadores de negocio F11, fabricar credenciales institucionales o exponer una vía de mutación por Blueprint, UI, LLM o NPC al margen de F11.
4. **Contrato coordinado, dos responsables:** el proyecto F11 define la API institucional, semántica, operaciones y precondiciones; HOST define el sobre de transporte local (partida, principal verificado, sujeto, revisión, procedencia, identificador de solicitud, trazabilidad y errores) y verifica que el consumidor está autorizado a usar esa API. Ningún dato del sobre sustituye las validaciones propias de F11. Los campos finales se pactarán contra cabeceras reales y serán versionados, no se inventan endpoints productivos.
5. **Dos certificaciones independientes:** F11 certifica emisor, normativa y efecto Core. HOST certifica propiedad de sesión, identidad, control de acceso, tránsito íntegro de la petición, manejo de denegaciones, reintentos y entrega de hechos ya confirmados. Las regresiones F11 son *dependencias y evidencias externas* de la integración, **no certificados emitidos por HOST**. Si F11 no expone todavía un emisor de producto, el HOST debe denegar/desactivar esa operación (fail-closed), sin sustituirlo por un simulador.
6. **Gobierno:** toda propuesta que altere esta frontera requiere decisión expresa del usuario y coordinación con la planificación F11. Esta decisión corrige y prevalece sobre los alcances iniciales de H07, H11 y H13 de la versión 1.0.

**Ejemplo operativo:** un evento de ascenso confirmado por F11/CoreRPG puede llegar mediante HOST a la interfaz del jugador. HOST no calcula el mérito, no crea la orden institucional, no cambia el rango y no genera una segunda fuente de verdad. La ceremonia o presentación diegética pertenece al desarrollo narrativo/F11; HOST únicamente comunica y conserva el contexto técnico necesario.

## 1. Conclusión de la auditoría

Existe una base técnica sólida, **no un HOST de producto ya terminado**. La aplicación principal `juego/UE5/StarTrekRPG/` contiene un README que declara la ausencia de un `.uproject` definitivo. Los laboratorios de F02/F03/F04/F05 sí incluyen proyectos Unreal aislados y puentes funcionales, pero no equivalen al videojuego final.

Inventario comprobado:

| Procedencia | Activo real | Capacidad reutilizable | Precaución |
|---|---|---|---|
| F02: `desarrollo/integration/f02/` | `TrekF02Bridge`, ABI C; GameInstanceSubsystem y simulación de observadores | Patrón de ownership, scopes efímeros, hilo propietario, proyección por observador, integración nativa/Unreal | Fixture de tres entidades; no es gestor de partidas de producto |
| F03: `desarrollo/integration/f03/` | Campaña sintética Core con eventos, tiempo, identidad y conocimiento | Ciclo autoritativo de mundo, LOD, visibilidad, guardado y reanudación | Navegación/época de fixture, no mundo galáctico final |
| F04: `desarrollo/integration/f04/` | `TrekF04Bridge`, `F04Session`, dotación, autoridad, horarios, población, historial | Núcleo de campaña; IO host, `f04_save/load`, historial y consultas; perfiles Miranda/Intrepid/Sovereign/Odyssey/Valhalla histórico | No duplicar `WorldState` ni afirmar juego final; historial tiene pins/modos precisos |
| F05: `desarrollo/integration/f05/` | Órdenes, delegación, iniciativa, IA opcional | `f05_submit/receive/execute`, revocaciones, idempotencia, `f05_bind_player`, lectura de contexto, provider | P01 solo ejecuta `F04_SCAN` como tirada; no hace detección F06 ni scheduler genérico |
| F06: `desarrollo/tools/simulation/resolve_sensor_scan.py` y contratos | Motor de sensores de referencia | Semántica de barrido y conocimiento, fixtures y pruebas | No confirma hechos Core: integración autoritativa pendiente |
| F11: `desarrollo/integration/f11/`, `f11_host/` | `f11_commit_promotion` y lector `TrekF11HostReader` de producto | Ascenso 1101→1102, expediente y proyecciones de hechos confirmados | El emisor solo existe para ensayo; no copiar `f11_trial_host.inc` a producto |
| Infraestructura | CMake, CTest, Python, Actions, matrices de tests | Regresiones multiplataforma, evidencias, oráculos históricos | Cada resultado se aplica a su commit/alcance, no al HOST nuevo |

**PR #108 y #109:** fusionadas. **PR #110:** abierta, Draft, únicamente documentación y 33 escenarios propuestos en estado `NOT_RUN`.  
**Riesgo de gobierno:** API de GitHub devuelve `protected: false` para `main`; revisar protecciones/rulesets efectivos antes de desarrollos críticos.  
**Desalineación de roadmap:** `PLAN_MAESTRO.md` general y `ESTADO_GLOBAL.json` (fecha 03-11) contienen contexto histórico; F11 documenta la decisión creativa vigente **USS Enterprise NCC-1701-D modernizada**. Reconciliar sin borrar lo histórico.

Referencias auditadas: [reglas AGENTS](https://github.com/robdor80/Videojuego_StarTrek/blob/main/AGENTS.md), [README de repositorio](https://github.com/robdor80/Videojuego_StarTrek/blob/main/README.md), [F02](https://github.com/robdor80/Videojuego_StarTrek/tree/main/desarrollo/integration/f02), [F04](https://github.com/robdor80/Videojuego_StarTrek/tree/main/desarrollo/integration/f04), [F05](https://github.com/robdor80/Videojuego_StarTrek/tree/main/desarrollo/integration/f05), [F11 Host](https://github.com/robdor80/Videojuego_StarTrek/tree/main/desarrollo/integration/f11_host), [frontera institucional](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/decisions/f11_p05_a02_03_host_boundary_2026-11-11.md), [PR #110](https://github.com/robdor80/Videojuego_StarTrek/pull/110) y [proyecto Unreal principal](https://github.com/robdor80/Videojuego_StarTrek/blob/main/juego/UE5/StarTrekRPG/README.md).

## 2. Arquitectura aprobable (propuesta, no implementada)

```text
          UNREAL 5.8.2 (UI / mundo 3D / LCARS / input)
                 │ intenciones tipadas / vistas filtradas
                 ▼
   HOST nativo de producto (una partida local activa)
   ├─ ciclo de sesión y propiedad de hilo
   ├─ principal local, personaje y ámbito de campaña
   ├─ política de guardado/carga y procedencia
   ├─ orquestador de operaciones F04/F05/F11
   ├─ cola de eventos, tareas y notificaciones (sin verdad paralela)
   ├─ pasarela autorizada hacia la API institucional de F11 (SIN emisor propio)
   ├─ adaptador opcional de IA, sin autoridad
   └─ diagnósticos, errores, límites y pruebas
                 │ contratos existentes, ningún Core duplicado
                 ▼
      TrekF04Bridge + extensiones F05/F11
                 │
                 ▼
   CoreRPG: WorldState, Timeline, Actions, Knowledge,
            RandomStreams y persistencia AUTORITATIVOS
```

**Principios invariantes:** solo CoreRPG contiene estado del universo; F11 aplica sus propias reglas específicas de Star Trek y registra sus hechos en CoreRPG; el HOST tiene estado operativo efímero y metadatos mínimos de gestión de archivos, nunca otro expediente ni otro reloj de campaña. Toda acción nace como intención; F11/Core la valida conforme a su dominio, sin validadores institucionales duplicados en HOST. El actor, identificadores de entidad, `F04Ref`, texto IA y `CAUSE` no son credenciales. No mezclar `UObject`, excepciones o STL a través de la ABI C. Llamadas Core únicamente en hilo propietario; trabajos externos no acceden a `WorldState`. Las vistas se filtran por observador. Tras cargar, scopes y actores anteriores quedan invalidados. No introducir red, servidor ni arquitectura distribuida para un solo jugador.

**Contrato conceptual mínimo** (nombres de diseño, no APIs ya existentes): abrir/cerrar campaña; vincular jugador-personaje; avanzar reloj; consultar proyección por observador; emitir intención F04/F05; leer el resultado y sus eventos; guardar; restaurar; suscribirse a notificaciones filtradas. El emisor institucional pertenece a F11 (proyecto principal), no al HOST; el HOST únicamente consume su interfaz interna autorizada y la mantiene fuera de Blueprint/IA/PADD.

**Modelo de amenaza proporcional:** garantizar separación de permisos durante el juego, coherencia del historial, carga controlada y rechazo de ficheros externos no confiables para conferir autoridad. No confundir CRC/checksum con autenticación; no prometer antifalsificación fuerte frente a quien altera libremente el ejecutable local. Una exigencia futura de confianza externa requerirá decisión separada y probablemente una raíz ajena al cliente.

## 3. Fases y subfases

**Leyenda:** **C** = ChatGPT ejecuta directamente diseño, documentación, herramientas aisladas o comprobaciones seguras; **X** = Codex ejecuta la implementación crítica; **U** = decisión/aprobación del usuario. Un trabajo marcado C no habilita mutaciones críticas por su cuenta. Cada cambio de código irá en rama y PR; nunca fusión automática.

### H00 — Auditoría de base, trazabilidad y gobierno

**Objetivo:** fijar una línea base reproducible antes de programar. **Dependencias:** ninguna. **Responsable:** C; U para políticas de GitHub. **Riesgos:** confundir laboratorios y producto, documentación histórica desactualizada, protección insuficiente de `main`. **Entregables:** inventario con rutas/SHA/PR, mapa de dependencias y riesgos, protocolo de ramas/CI. **Pruebas:** lectura verificable de árbol, archivos y estados; comprobaciones de coherencia documental sin alterar fuentes. **Cierre:** ningún componente catalogado como producto sin evidencia, riesgos aceptados y baseline identificada.

- **H00-P01 [C]** Auditar interfaces F02/F03/F04/F05/F11 y capacidades efectivas.
- **H00-P02 [C]** Catalogar pins Core, modos CMake, suites y límites; separar resultado de referencia/producto.
- **H00-P03 [C]** Reconciliar por propuesta el roadmap F11/Enterprise-D y registrar la decisión vinculante de separación HOST/F11, sin reescribir actas históricas.
- **H00-P04 [C+U]** Revisar `AGENTS.md`, `.gitignore`, branch protection/rulesets y criterios de fusión.

### H01 — Diseño de arquitectura, contratos y seguridad básica

**Objetivo:** convertir la arquitectura en especificación implementable. **Dependencias:** H00. **Responsable:** C, revisión de viabilidad X en cambios delicados. **Riesgos:** duplicar autoridad o abrir APIs inseguras; versiones/pins incompatibles. **Entregables:** diagramas de componentes, interfaces, mapa de propiedad y matriz de errores. **Pruebas:** casos contractuales de sesión, revisión, scopes, accesos, idempotencia y rollback; revisión cruzada con CMake y cabeceras reales. **Cierre:** contratos coherentes y versionados con responsables; sin introducir APIs Core inexistentes.

- **H01-P01 [C]** Diseño de componentes y dependencias nativas; interfaz HOST↔UE↔Core.
- **H01-P02 [C]** Contratos de comandos, lecturas, resultados, eventos, revisión y error, con anexo de integración HOST↔F11 cuyo dueño funcional es F11.
- **H01-P03 [C]** Modelo de confianza offline del HOST: principal, procedencia del guardado y acceso a interfaces privadas F11, sin crear autoridad institucional.
- **H01-P04 [C]** Plan de integración/adopción de versiones Core y estrategia de no duplicación.

### H02 — Núcleo del HOST y gestor de sesiones

**Objetivo:** dar a un componente nativo único la propiedad de la partida y del acceso a Core. **Dependencias:** H01. **Responsable:** X; C prepara contratos/pruebas. **Riesgos:** doble dueño de `F04Session`, punteros obsoletos, uso desde otro hilo, destrucción incompleta. **Entregables:** biblioteca nativa de HOST local, gestor de sesiones y estados `CLOSED/OPENING/ACTIVE/SAVING/LOADING/FAILED/CLOSING`. **Pruebas:** crear-cerrar-reabrir, dobles cierres, errores de inicialización, fuga de recursos, hilo incorrecto y scopes caducados. **Cierre:** ciclo de vida reproducible sin UE y sin fugas ni cambios parciales.

- **H02-P01 [X]** Diseñar/implementar propiedad única de sesión sobre el puente de producto.
- **H02-P02 [X]** Estados, transiciones, invariantes y serialización de acceso a Core.
- **H02-P03 [C]** Matriz de pruebas y comprobadores de interfaces, sin mutación de producto.
- **H02-P04 [X]** Tests nativos y CI del ciclo de vida; revisión independiente C.

### H03 — Identidad del jugador, personaje y partida

**Objetivo:** vincular principal local, campaña y personaje sin confundir entidad Core con credencial y sin emitir ni reinterpretar la identidad profesional F11. **Dependencias:** H02. **Responsable:** C contratos; X implementación. **Riesgos:** suplantación desde cliente, cambio de jugador silencioso, identidad duplicada entre campañas. **Entregables:** vínculo principal↔campaña↔personaje, política de nuevo juego/continuación y acceso por sujeto. **Pruebas:** continuidad entre cargas, jugador único, pertenencia correcta, denegación de referencias ajenas, `f05_bind_player` controlado. **Cierre:** nunca se concede acceso solo por un ID numérico o campo declarado por cliente.

- **H03-P01 [C]** Especificar identidad local y distinción jugador/personaje/oficial/persona Core; los identificadores y hechos profesionales de F11 solo se consultan, no se emiten en HOST.
- **H03-P02 [X]** Enlazar sujeto autenticado a sesión y campaña; renovar referencias en carga.
- **H03-P03 [X]** Integrar binding F05 sin exponer una API de cambio de identidad.
- **H03-P04 [C+X]** Casos adversarios y pruebas de persistencia de identidad.

### H04 — Guardado, recuperación y procedencia

**Objetivo:** un único mecanismo host para IO durable usando el formato y las validaciones Core. **Dependencias:** H02–H03. **Responsable:** X; C diseña política y auditorías. **Riesgos:** corrupción, reconocimiento prematuro de éxito, directorios incompletos, archivos falsificados, pérdida de estado tras corte. **Entregables:** gestión segura de ranuras, publicación atómica/recuperación, validación, metadatos mínimos y compatibilidad. **Pruebas:** guardado/carga entre procesos, ficheros truncados, versiones antiguas, crash antes/después de publicación, revocación, RNG/reloj idénticos, recuperación sin sobrescribir partida válida. **Cierre:** errores no destruyen sesión buena ni archivos anteriores; durabilidad declarada solo cuando se comprueba.

- **H04-P01 [C]** Política de ranuras, procedencia, importación, backups y versionado de formatos.
- **H04-P02 [X]** Integrar `CampaignPersistence`/`HistoryPersistence` por rutas ya autorizadas.
- **H04-P03 [X]** Recuperación, publicación atómica, errores inciertos y validación pre-swap.
- **H04-P04 [C+X]** Inspección no mutadora de partidas y baterías de fallo/roundtrip.

### H05 — Pasarela CoreRPG y primer ciclo funcional nativo

**Objetivo:** ejecutar un ciclo completo autenticado y reproducible de consulta→intención→resultado→guardado; los comandos institucionales F11 quedan reservados a la API de producto que F11 publique. **Dependencias:** H02–H04. **Responsable:** X pasarela/transacciones; C modelos de lectura/test. **Riesgos:** compilar pins equivocados, saltarse validación F04/F05, presentar un `F04_SCAN` como sensor real. **Entregables:** composición de `TrekF04Bridge` con extensiones F05, despacho tipado, proyección y demostración headless. **Pruebas:** mandato legítimo/denegado/revocado, revisión caducada, orden idempotente, ninguna mutación ante rechazo, save/load tras resultado. **Cierre: HITO M0, HOST NATIVO MÍNIMO FUNCIONAL** demostrado sin UE.

- **H05-P01 [X]** Ensamblar binarios de producto contra el Core pin apropiado, sin alterar pins históricos.
- **H05-P02 [X]** Adaptador de operaciones F04/F05 y resultados sin segundo motor de reglas; preparación no mutadora de extensión F11, pendiente de contrato institucional aprobado por F11.
- **H05-P03 [C]** Proyecciones de solo lectura/validadores de contrato de bajo riesgo, si su interfaz queda estable.
- **H05-P04 [X]** Test end-to-end nativo de una campaña mínima con una orden y recuperación.

### H06 — Integración real con Unreal Engine 5

**Objetivo:** insertar el HOST en el proyecto final, sin tratar el laboratorio como producto. **Dependencias:** H05 y existencia verificada de un `.uproject` principal. **Responsable:** X integración C++/UBT; C guía de instalación/UX; U aprueba creación del proyecto si sigue ausente. **Riesgos:** plugin incorrecto, referencias a laboratorios, ciclos de vida entre `UGameInstance`/`UWorld`, bloqueos del Game Thread. **Entregables:** proyecto UE real, módulo/servicio de HOST, una interfaz de diagnóstico mínima e interacción validada. **Pruebas:** UE 5.8.2 NullRHI y D3D12 MSI, múltiples UWorld, abrir/cerrar/cargar, interacción y órdenes reales; no filtros de conocimiento omitidos. **Cierre: HITO M1, HOST INTEGRADO MÍNIMO EN UE** con proyecto realmente ejecutado.

- **H06-P01 [C]** Verificar prerequisitos y preparar plan de integración no destructivo del proyecto UE.
- **H06-P02 [X+U]** Crear/confirmar `.uproject` definitivo con respaldo de recursos y módulo Host.
- **H06-P03 [X]** Conectar GameInstanceSubsystem, ownership de hilo, callbacks y actores efímeros.
- **H06-P04 [C+X]** Interfaz de prueba discreta y flujo primera sesión/guardar/recuperar.
- **H06-P05 [X]** Ensayos locales MSI y evidencias NullRHI/D3D12, revisadas por C.

### H07 — Integración HOST↔F11: identidad, acceso y comunicación (SIN emisor)

**Objetivo:** proporcionar el contexto de sesión, identidad y acceso que necesita F11/CoreRPG y conectar el HOST con las interfaces F11 **sin implementar ni certificar el emisor institucional ni las reglas de negocio**. **Dependencias:** H01, H03–H05; integración interactiva depende de H06 y una API institucional de producto aprobada por F11. **Responsable:** C arquitectura, contratos y matrices; X adaptación nativa de integración y pruebas propias del HOST; **F11/Codex del proyecto principal** implementa el emisor, sus reglas y su certificación fuera de H07. **Riesgos:** reproducir código F11, equiparar `F04Ref`/checksum/`CAUSE=110501` con acreditación, conferir autoridad por datos de entrada, integración prematura con el fixture. **Entregables HOST:** contrato coordinado HOST↔F11, adaptador de sesión y acceso, consumo de `TrekF11HostReader`, enrutamiento de solicitudes autorizadas y entrega de resultados/eventos confirmados; gestión de operación no disponible si F11 todavía no publica un emisor. **Pruebas HOST:** acceso denegado, sujeto ajeno, scopes/revisión inválidos, respuesta negativa sin efectos, idempotencia de encaminamiento, save/load y retransmisión sin inventar hechos; integración Linux/MSVC/UE cuando esté disponible. **Cierre:** transporte y controles del HOST probados contra la API F11 aprobada, o estado **BLOQUEADO POR DEPENDENCIA F11** en las operaciones institucionales aún inexistentes. La certificación normativa/emisora F11 se decide únicamente en F11 y no es entregable H07.

- **H07-P01 [C]** Acuerdo de frontera y contrato: F11 declara operaciones/validaciones; HOST declara principal, sesión, procedencia, control de acceso y errores de enlace.
- **H07-P02 [X]** Adaptador **no emisor** de solicitudes F11: comprobar contexto y encaminar a API F11 privada *solo cuando exista y esté aprobada*; denegar si no está disponible.
- **H07-P03 [X]** Integrar lectura con `TrekF11HostReader` y entregar eventos ya confirmados; no calcular ni conceder rangos, comisiones, evaluaciones o permisos F11.
- **H07-P04 [C]** Matriz de interfaz HOST/F11 y trazabilidad de las 7 puertas `HOST_01–HOST_07` y los 33 escenarios de PR #110: distinguir pruebas **F11 externas** de pruebas propias HOST sin dar por ejecutadas las primeras.
- **H07-P05 [X]** Pruebas de integración del HOST (acceso, fallo cerrado, transmisión, respuestas, cargas y eventos); C audita. Las pruebas de emisión, revocación institucional y reglas de ascenso se ejecutan y certifican **en F11**, no aquí.

### H08 — Coordinación de eventos, servicios y reloj

**Objetivo:** orquestar notificaciones, tareas y vida de juego desde hechos Core, no desde un bus con verdad propia. **Dependencias:** H05, H06 para presentación. **Responsable:** C contratos; X ciclo y dispatcher. **Riesgos:** eventos duplicados, cambios de orden, reloj paralelo, reintentos con efectos repetidos. **Entregables:** taxonomía, dispatcher en hilo propietario, plan de entregas y acuses de UI. **Pruebas:** orden causal, repetición tras carga, eventos pendientes, no filtración entre observadores, estados terminales, avances de reloj reproducibles. **Cierre:** cada notificación deriva de hechos Core autorizados y puede reconstruirse tras recarga.

- **H08-P01 [C]** Contrato de eventos, deduplicación, precedencia, visibilidad y mensajes.
- **H08-P02 [X]** Dispatcher/cola local sin mutación lateral del mundo.
- **H08-P03 [X]** Integración del reloj Core, budget y trabajos acotados de la campaña.
- **H08-P04 [C]** Formateadores y pruebas de proyecciones/notificaciones no mutadores; eventos F11 solo tras confirmación en Core, sin generar actos institucionales.

### H09 — Operaciones de naves, sensores y navegación

**Objetivo:** incorporar progresivamente capacidades operativas reales usando F04/F05 y F06 como referencia. **Dependencias:** H06/H08 y contratos propios F06/F09. **Responsable:** C catálogos/pruebas; X integración nativa/UE. **Riesgos:** confundir tirada F04 con detección F06, inventar conocimiento, dos ubicaciones, física y permisos inconsistentes. **Entregables:** flujos autorizados de consola Sensores, comunicaciones, navegación y operaciones de nave. **Pruebas:** contacto oculto y visible, informes, orden revocada, búsqueda sin filtración, avance de posición/tiempo, carga en mitad de maniobra, cruzar naves/secciones. **Cierre:** operaciones probadas contra Core y UE, no únicamente Python.

- **H09-P01 [C]** Inventario de capacidades, operaciones y permisos; contrato de consola limpia.
- **H09-P02 [X]** Integración Core real de barrido F06 y reportes observador-relativos.
- **H09-P03 [X]** Navegación, órdenes de timón y cronología de viaje según fase general correspondiente.
- **H09-P04 [X]** Encaminar coordinación entre naves/secciones y consumir la autoridad delegada que validen F04/F11; no recalcular jerarquías ni atribuciones de mando en HOST.
- **H09-P05 [C+X]** Mensajería LCARS de puente y pruebas cruzadas Sensores→Ciencia→Mando.

### H10 — NPC, IA y computadora de a bordo

**Objetivo:** coordinar autonomía NPC primero determinista y después conversación opcional sin ceder autoridad. **Dependencias:** H08/H09; F05 ya proporciona las bases. **Responsable:** C reglas, contratos y mensajes; X ejecución y proveedor. **Riesgos:** NPC omnisciente, órdenes inventadas, latencias IA, bloqueo de hilo, reintentos desfasados. **Entregables:** gestor de decisiones acotadas, adaptador de proveedor IA y computadora contextual. **Pruebas:** jugador operador/capitán, órdenes NPC→NPC, datos desconocidos, IA caída/lenta, cambio de autoridad durante respuesta, recuperación sin IA, memoria tras carga. **Cierre:** el bucle jugable funciona desconectado; ninguna propuesta IA altera Core sin nueva validación.

- **H10-P01 [C]** Matriz de consumo de competencias y conocimiento por observador: las reglas de cadena de mando se consultan a F04/F11, nunca se replican en HOST.
- **H10-P02 [X]** Orquestación de evaluaciones P03 y tareas con budget por tick.
- **H10-P03 [X]** Adaptación P04 a proveedor real opcional, colas y cancelación.
- **H10-P04 [C+X]** Contratos/respuestas breves y presentación de la computadora de a bordo.
- **H10-P05 [C]** Pruebas de privacidad y semántica del diálogo; X CI nativa de regresión.

### H11 — Misiones, temporadas y comunicaciones narrativas

**Objetivo:** coordinar activadores y consumo de hechos narrativos autoritativos independientemente del rango y nave del jugador, sin asumir los servicios de comunicación institucional de F11. **Dependencias:** H08–H10, reglas generales F10–F13. **Responsable:** C diseño narrativo y fixtures; X integración del controlador. **Riesgos:** misión dependiente de una nave concreta, escena que cambia hechos sin permiso, progreso que se pierde al cargar. **Entregables:** contrato de disparadores/condiciones/consecuencias, temporadas y adaptadores para entregar a Unreal los mensajes narrativos producidos por sus sistemas dueños (incluido F11). **Pruebas:** mismo incidente como alférez y capitán, partidas con distintos destinos, persistencia y no repetición de recompensas/eventos. **Cierre:** demostración transversal desde dos puestos/rangos, con hechos confirmados exclusivamente por Core.

- **H11-P01 [C]** Arquitectura de temporadas y disparadores independientes de destino.
- **H11-P02 [C]** Historias y guiones de ensayo con condiciones/ramificaciones comprobables.
- **H11-P03 [X]** Dispatcher de misión, estado persistente Core y consecuencias autorizadas.
- **H11-P04 [C+X]** Adaptar el canal de entrega, acuse y consulta para presentaciones F11 ya aprobadas; el contenido, disparadores institucionales y certificación de ceremonias siguen en F11/proyecto principal.

### H12 — Diagnósticos, rendimiento, estabilidad y mantenimiento

**Objetivo:** convertir la integración en un sistema operable y medible en Windows local. **Dependencias:** H02–H11 según capacidad. **Responsable:** C matriz/métricas y herramientas seguras; X optimización crítica. **Riesgos:** crecimientos históricos y topes F04/F05, bloqueos Game Thread, logs que filtran secretos, regresiones encubiertas. **Entregables:** diagnósticos categorizados, trazas de operaciones, reportes de carga y presupuesto de CPU/memoria/latencia. **Pruebas:** sesiones prolongadas, 1/7/28 días, campañas extensas, reanudación, fallos de proveedor y archivos, stress de órdenes/eventos, plataformas. **Cierre:** límites documentados, fallos claros, sin bloqueantes ni cambios de comportamiento no aprobados.

- **H12-P01 [C]** Esquema de métricas e informes sin datos secretos ni sidecars autoritativos.
- **H12-P02 [X]** Instrumentación y watchdog/cooperación de hilo donde sea necesario.
- **H12-P03 [C]** Scripts de comparación de logs y reportes de rendimiento, ejecutados en laboratorio.
- **H12-P04 [X]** Ajustes medidos y regresión tras cada optimización.

### H13 — Certificación integral y autorización de cierre

**Objetivo:** certificar el HOST real para el alcance acordado; no certificar Unreal/IA/narrativa no realizados. **Dependencias:** todas las capacidades objetivo, H12, proyecto UE ejecutable. **Responsable:** C auditoría independiente, X ejecución técnica, U aceptación/fusiones. **Riesgos:** confundir CI documental con ejecución, romper evidencia congelada o aceptar SKIP sin justificar. **Entregables:** matriz de trazabilidad, evidencias por commit/entorno, acta con límites y certificación final del HOST. **Pruebas:** GNU/MSVC, Core pins exactos, regresiones F02–F05 y consumo del contrato F11, seis campañas cuando aplican, UE NullRHI/D3D12 MSI, E2E guardar/cargar, negativas de acceso del HOST, inicio/cierre/reanudación; la certificación de reglas/autoridad institucional F11 se acredita como dependencia externa, sin duplicarla. **Cierre:** todas las puertas obligatorias PASS, excepciones documentadas y aprobación expresa del usuario; solo entonces `CERTIFICADO`.

- **H13-P01 [C]** Matriz completa de requisitos HOST→pruebas→evidencia→SHA, separando claramente certificados F11 externos.
- **H13-P02 [X]** CI nativa multi-SO e integración con suites existentes sin alterar oráculos.
- **H13-P03 [X+U]** Pruebas finales sobre MSI/UE y aceptación interactiva.
- **H13-P04 [C]** Reauditoría independiente de seguridad, compatibilidad y documentación.
- **H13-P05 [U]** Acta y autorización de fusión/cierre; actualización de estados por alcance.

## 4. Camino crítico e hitos

- **A:** H00 → H01 → H02 → H03 → H04 → H05 = **M0, HOST nativo funcional**. Se considera funcional solo tras ejecutar pruebas reales, no por diseño.
- **B:** H05 + `.uproject` verificado → H06 = **M1, HOST mínimo funcionando en UE5**.
- **C:** H03–H05 + política de confianza + **contrato institucional implementado y certificado en F11** → H07 = **pasarela HOST/F11 integrada**; aceptación UE requiere además H06. Si F11 aún no está preparada, las operaciones F11 permanecen deshabilitadas y no bloquean M0/M1.
- **D:** H08 → H09 → H10 → H11, consumiendo H07 cuando se deban presentar hechos F11 ya confirmados por su sistema propietario.
- **E:** H12 transversal → H13 = **HOST certificado** para el alcance probado.

Si el juego principal Unreal todavía no existe, **el camino A no se bloquea**: se certificará solo su corte nativo. H06 esperará a proyecto de producto real. H07 (solo contrato y adaptación no emisora) y las herramientas documentales de H08/H11 pueden progresar en paralelo, siempre sin declarar `UE5_JUGABLE` ni atribuir al HOST la certificación F11.

## 5. Reparto y uso de cuota de Codex

ChatGPT asume auditoría y plan, contratos, evaluadores puros, pruebas offline y matrices, scripts de informes, documentación, interfaces de lectura simples cuando no invadan la frontera crítica, revisión de cada PR y evidencias. Codex asume dueño de sesión nativo, identidad de sesión y control de acceso, persistencia, transacciones de orquestación, pasarela F04/F05 y consumidor no emisor de F11, UBT/UE, coordinación de eventos y pruebas profundas. El equipo F11 del proyecto principal conserva por separado el desarrollo y certificación del emisor y las reglas institucionales. Usuario conserva decisiones significativas y fusiones.

**Recomendación por encargo cuando llegue el momento:**

| Encargo complejo futuro | Modelo Codex | Razonamiento |
|---|---|---|
| H02 ciclo de sesión | GPT-6 | Alto |
| H03 identidad y vínculo F05 | GPT-6 | Alto |
| H04 persistencia/procedencia | GPT-6 | Alto |
| H05 composición y operaciones Core | GPT-6 | Alto |
| H06 módulo Unreal/UBT | GPT-6 | Alto |
| H07 pasarela HOST↔F11 (no emisora) | GPT-6 | Alto por frontera de confianza; Medio para lecturas aisladas |
| H08 dispatcher/scheduler | GPT-6 | Alto |
| H09 sensores/navegación autoritativos | GPT-6 | Alto |
| H10 proveedor IA/gestor NPC | GPT-6 | Medio para adaptadores; Alto para mutaciones/concurrencia |
| H11 ejecución narrativa | GPT-6 | Alto si toca estado persistente |
| H12 optimización y H13 CI | GPT-6 | Medio para CI aislada; Alto para cambios críticos |

La recomendación se repetirá expresamente en **cada prompt real**, ajustada al riesgo concreto; no se enviarán tareas complejas si ChatGPT puede resolverlas con seguridad mediante análisis o trabajo no mutador.

## 6. Reglas de gobierno y estados

- Un solo repositorio: `robdor80/Videojuego_StarTrek`; no crear repositorio HOST separado. La separación HOST/F11 es de módulos, propietarios y certificaciones, no de repositorios.
- Rama y PR Draft por corte, CI y revisión; sin fusiones ni cambios importantes en `main` sin permiso.
- No cambiar CoreRPG, sus pins, auditorías históricas ni pruebas congeladas sin autorización y procedimiento de migración independiente. No introducir en HOST un segundo emisor institucional, autoridad, tablas de rangos o validadores de negocio F11.
- Material temporal exclusivamente `laboratorios/<area>/<tarea>/`, ignorado por Git; jamás borrar laboratorios anteriores sin permiso.
- Código final dentro de una ubicación propuesta y aprobada en `desarrollo/` y, cuando exista, módulo UE bajo el proyecto principal `juego/UE5/StarTrekRPG/`.
- No declarar **IMPLEMENTADO**, **PROBADO**, **CERTIFICADO**, **FUSIONADO** como sinónimos. Un mismo corte puede estar `IMPLEMENTADO` en Draft y no estar `PROBADO` ni `FUSIONADO`.
- El cierre de fase incluye objetivo, deps resueltas, propietario, riesgos residuales, entregables, pruebas repetibles, commit/PR y firma de aceptación cuando corresponda.

## 7. Primer paquete seguro, sin programación

1. **H00-P01/02:** inventario definitivo de símbolos, rutas, pins, CI y proyecto UE; estado histórico por SHA.
2. **H00-P03:** documento de reconciliación Enterprise-D frente al roadmap histórico sin sobrescribir el canon histórico.
3. **H00-P04:** propuesta de protección `main` y política de PR/revisión antes de cambios críticos; activación bajo aprobación del usuario.
4. **H01-P01/02/03:** contratos/diagramas y amenaza offline con pruebas de ejemplo; todo documental.
5. **H01-P04:** compatibilidad y estrategia de ensamblaje F04/F05 y lectura F11 que Codex auditará antes de tocar el ciclo de sesión; el emisor F11 depende de su proyecto principal.

**Primer encargo de código futuro:** H02, después de cerrar la arquitectura. **No ejecutado en este documento.**

## 8. Correspondencia con las fases del videojuego

| HOST | Fases generales que habilita o consume | Límite de responsabilidad |
|---|---|---|
| H00–H01 | F00–F05 y F11 | Inventario y contratos; sin reabrir certificados históricos |
| H02–H05 | F02–F05 y lectura F11 | Núcleo nativo de sesiones y Core; no emite hechos institucionales ni demuestra juego UE |
| H06 | F02, F07–F08, F15 | Integración con proyecto UE real, sin reemplazar interfaces visuales |
| H07 | F11-P05 (dependencia externa) | Solo identidad de sesión, acceso y pasarela hacia F11; **emisor y reglas/certificación pertenecen íntegramente a F11** |
| H08 | F03–F05, F12–F13 | Coordinar tiempo y eventos ya reconocidos por Core |
| H09 | F04, F06, F08–F09 | Operación de nave y sensores, siempre con la cadena de mando existente |
| H10 | F05, F09, F12 | NPC y computadora; proponer no equivale a autorizar |
| H11 | F10–F13, eventos F11 | Misiones/temporadas y entrega de eventos; F11 conserva el contenido y reglas de ceremonias profesionales |
| H12–H13 | F15 y regresiones F02–F14 | Certificación del HOST por alcance; certificaciones F11 se incorporan solo como evidencia externa |

En particular, la futura **Enterprise-D modernizada** condiciona el contenido, el mapa de cubiertas y los puestos de juego, pero **no** la identidad, los permisos, la persistencia ni los contratos generales del HOST. Por ello se puede comenzar el HOST antes de finalizar la geometría de la nave.

## 9. Registro de cambios de la versión 1.1

- Incorporada como vinculante la **DECISIÓN ARQUITECTÓNICA — Separación HOST / F11** del usuario (11-11-2026).
- H07 redefinida por completo: **integración no emisora**, sin crear concesiones, comisiones, evaluaciones, órdenes institucionales ni reglas de ascenso.
- Afinadas H01, H03, H05, H08 y H11 para respetar la titularidad de F11; la ceremonia y el emisor se desarrollan allí.
- H13 certificará **solo el HOST**; F11 es requisito interoperable con su propia aprobación y evidencias.
- Camino crítico y recomendaciones a Codex actualizados. **Sin cambios de código, GitHub, CoreRPG o documentación del proyecto principal.**