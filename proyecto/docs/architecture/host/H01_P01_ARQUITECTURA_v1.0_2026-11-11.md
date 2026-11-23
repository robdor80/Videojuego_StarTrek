# H01-P01 — Arquitectura del HOST v1.0

Fecha: 11-11-2026. Estado: DISEÑADO, NO IMPLEMENTADO. Baseline Star Trek main@07f226248220c18c0527d38cf4cdfaf1c93cbb31. Dependencia: H00 (PR #111 fusionada).

## Decisión principal

El HOST es una biblioteca nativa incrustada en el proceso del juego, inicialmente local, de un jugador y con UNA campaña activa. Coordina la sesión, los permisos de acceso al canal, los mensajes, la carga y la entrega de vistas. No es otro motor de reglas, otro WorldState, un backend de red ni un emisor institucional de F11.

~~~text
Unreal 5.8.2: UI, LCARS, input y mundo 3D
          | intenciones tipadas / vistas filtradas
          v
Adaptador UE de producto [H06, pendiente de .uproject]
          |
          v
HOST nativo de producto [H02-H05]
  - SessionOwner: única F04Session y hilo dueño
  - PrincipalBinder: jugador/campaña/personaje
  - CommandDispatcher: solicitudes y revisiones
  - ProjectionService: vistas por observador
  - SaveCoordinator: ranuras, procedencia, IO
  - EventDelivery: avisos derivados (H08)
  - OptionalAiAdapter: propuestas no autoritativas (H10)
          | APIs privadas existentes de cada dominio
          v
TrekF04Bridge + extensiones F05/F11
          |
          v
CoreRPG (WorldState, knowledge, reloj, RNG, historia)
~~~

El lector TrekF11HostReader consume hechos F11 ya confirmados. El emisor institucional que falta pertenece únicamente a F11 del proyecto principal. No existe puente de emisión por Blueprint/LLM/NPC/PADD. Si no hay API institucional de producto certificada, fallo cerrado.

## Componentes, propietario y reutilización

| Componente propuesto | Dueño de la responsabilidad | Apoyo real |
|---|---|---|
| SessionOwner (H02) | HOST: creación, destrucción, estados y generación de sesión | F04Session, f04_create_population, f04_destroy |
| PrincipalBinder (H03) | HOST: vínculo local y resolución de sujeto | f05_bind_player; la profesión sigue en F11 |
| CommandDispatcher (H05) | HOST: estado, canal, correlación, serialización | f04_execute, f05_submit/receive/execute |
| ProjectionService (H05/H07) | HOST: acceso, observador y limpieza de buffers | f04_person/manifest_page, f05_order, lector F11 |
| SaveCoordinator (H04) | HOST: ruta, ranuras, admisión, publicación y recuperación | Core persistence, f04_history_* |
| EventDelivery (H08) | HOST: entrega/deduplicación de notificaciones | hechos y eventos confirmados de Core |
| UeHostAdapter (H06) | Unreal: presentación y traducción de input | GameInstanceSubsystem, no laboratorios como producto |
| OptionalAiAdapter (H10) | HOST: proveedor asíncrono y cancelación | F05AiContext y trek::ai::Provider |

CoreRPG posee los hechos, cronología, knowledge y persistencia; F04/F05 poseen reglas operativas; F11 posee identidad profesional, comisiones, competencias, rangos, ascensos y actos institucionales; el HOST posee únicamente coordinación y estado operacional efímero. No hay un reloj paralelo de campaña, un expediente redundante ni un conjunto de permisos copiado.

## Vida, hilos e invalidación

1. Una única F04Session viva. F02/F03 son modelos de diseño, NO segundas sesiones runtime.
2. Toda invocación F04/F05/F11, incluso lecturas, destrucción y guardado, se ejecuta en el hilo propietario. Otros hilos entregan mensajes a la cola HOST sin punteros Core.
3. Cada apertura/restauración incrementa session_generation operacional y revoca F04Ref, callbacks, contextos IA, proyecciones y peticiones de la generación anterior.
4. El HOST resuelve actor/observador auténtico contra campaña vinculada; las referencias numéricas recibidas no son credenciales.
5. Toda mutación de dominio valida expected_revision al ejecutarse, no al dibujar la interfaz. Un rechazo no genera reintentos automáticos.
6. Una proyección por observador es copia efímera. No dar f04_stats ni lecturas de diagnóstico a pantalla pública o IA.
7. Separar relojes: Core tick autoritativo, monotonic_ms de transporte IA y tiempo de presentación visual.

## Máquina de estados prevista

~~~text
CLOSED -> OPENING -> ACTIVE -> SAVING -> ACTIVE
                 |         -> LOADING -> ACTIVE (con nueva generación)
                 |                       -> ACTIVE (si carga falla, sin swap)
                 +-> FAILED -> CLOSING -> CLOSED
ACTIVE ---------------------> CLOSING -> CLOSED
SAVING/LOADING -> FAILED_RECOVERABLE -> ACTIVE/CLOSING
~~~

Cada transición y error es especificación para Codex H02/H04; no existe aún esta API. Durante SAVING, LOADING y CLOSING no se admiten mutaciones. Una carga fallida conserva el último estado válido; si la API no garantiza rollback, H04 crea y valida un candidato aislado y solo conmuta tras éxito. Cierre cancela proveedores y invalida vistas antes de destruir la sesión.

## Dependencias y fronteras verificadas

- desarrollo/integration/f04/include/f04_bridge.h: F04Session, F04Ref scope/id, F04Request revision, f04_advance, f04_save/load y history_migrate/open/publish.
- desarrollo/integration/f05/include/f05_orders.h: misma F04Session, key/cause por campaña y estados independientes de emisión, recepción y ejecución.
- desarrollo/integration/f05/include/f05_ai_provider.h: transporte no bloqueante; reloj monotónico no es tick Core.
- desarrollo/integration/f11_host/include/f11_host_reader.h: C++ de solo lectura, exige autenticación previa al lector.
- juego/UE5/StarTrekRPG/README.md: todavía falta StarTrekRPG.uproject; H06 queda condicionado.
- AGENTS.md: temporales exclusivamente en laboratorios/ dentro del repositorio, nunca dependencias de producto.

## Decisiones de implementación diferidas

Los puertos conceptuales OpenCampaign, CloseCampaign, ResolvePrincipal, DispatchCommand, QueryView, AdvanceCampaign, SaveSlot, RestoreSlot y PollEvents NO son símbolos exportados. H02/H05 definirán firmas reales adaptadas a la ABI C existente. No pasan UObjects, STL, excepciones ni punteros Core por esa ABI. No inventar endpoint de emisor F11 ni declarar F04_SCAN sensor real F06.
