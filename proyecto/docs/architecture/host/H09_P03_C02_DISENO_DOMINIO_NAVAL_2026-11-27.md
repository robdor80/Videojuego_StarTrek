# HOST H09-P03-C02 — Diseño de dominio naval mínimo (ubicación, carta y propuesta)

**Fecha:** 27-11-2026. **Responsable preparación:** ChatGPT. **Responsable de implementación nativa futura:** Codex Cloud (Sol 6.2, Medium).  
**Estado:** DISEÑADO, NO IMPLEMENTADO, NO PROBADO EN CORE, NO CERTIFICADO.  
**Base:** PR #231 fusionada en \`main\` (\`c65c0a32c4130d9fcf32da1101b975cf8f9c6b26\`). Pin CoreRPG: \`76a7b7b485616d8c4994f384a90f123bf333591d\`.  
**Alcance autorizado:** preparar y evaluar la **opción 1** del informe C01, sin modificar CoreRPG ni su pin, ni aceptar implícitamente ampliaciones de F04/F05.  
**Fuente:** [Factibilidad C01](H09_P03_C01_FACTIBILIDAD_CORE_2026-11-27.md), [contrato P03](H09_P03_CONTRATO_NAVEGACION_CONN_v1.json), [registro P01](H09_P01_REGISTRO_CONSOLAS_v1.json).

## 1. Decisión de arquitectura propuesta y puertas

La extensión mínima pertenece a la **composición naval de producto**, no a un segundo mundo del HOST. Reutilizar la única campaña \`F04Session\`, \`WorldState\` y tick Core; acceder a la sesión mediante su hilo propietario. Tres funciones lógicas internas —\`read_own_location\`, \`read_authorized_chart\` y \`propose_known_route\`— preceden a cualquier API pública o integración UE.

Las tres operaciones se especifican aquí **como contrato de futuro**, no como firmas C++ implementadas. La operación ya registrada en H09-P01 sigue siendo \`NAVIGATION_ROUTE_PROPOSE\` y permanece indisponible. \`CONN_MANEUVER_ORDER\` sigue indisponible: no se añade un simulador warp, entrada en órbita ni órdenes F05.

**Puerta P0 (bloqueante para código de dominio):** el implementador debe demostrar una costura de producto capaz de representar, validar, publicar y recuperar hechos de ubicación/carta en el único WorldState, compatible con el esquema cerrado F04 y \`HistoryPersistence\`. Si ello exige cambiar CoreRPG, mover su pin, modificar formatos históricos o alterar el emisor institucional F11, **detener esa parte y presentar propuesta específica para decisión del propietario**. No eludirlo con caché HOST autoritativa, JSON cargado fuera de campaña o emulación.

## 2. Identidad y ubicación de la nave

- Resolver la identidad real de la nave en el HOST, nunca aceptar \`ship_id\` aportado por UE/IA como prueba de autoridad. El hecho de que la nave principal se cree con ID Core 1 en un arranque actual no autoriza a fijar 1 en el contrato.
- **Modelo candidato para evaluar:** entidad de lugar discreto tipada y relación de contención nave→lugar en \`WorldState\`. Es hipótesis de representación, no afirmación de soporte actual: verificar colisiones con contención de personas/puestos, unicidad, ciclos, catálogo F04, bootstrap, guardado y restauración. Un lugar discreto **no equivale a coordenadas 3D ni a trayecto warp**.
- \`current_location\` proviene únicamente de un hecho Core de campaña validado; si no existe, devolver \`UNKNOWN\` y \`location_ref=null\`. No asignar Tierra, San Francisco, estrella ni sector por defecto. No deducir la ubicación de la cámara UE, el mapa artístico o nombres del grafo.
- Definir fuente y procedencia del bootstrap de campañas nuevas como dato de autoría **explícitamente aprobado**, versionado y validado antes de publicar. Si carecemos de origen aprobado, la partida nace con ubicación desconocida; C02 no decide un lugar narrativo.
- Un guardado anterior a la extensión debe poder cargarse conservando \`UNKNOWN\` sin reconstruir falsamente un estado. Rechazar migraciones que reescriban silenciosamente archivos previos.

## 3. Carta autorizada y conocimiento por observador

Separar (a) **definiciones de referencia de contenido** —\`anchor_route_graph.json\`, \`astrography_location_model.json\`, \`navigation_distance_edge_model.json\` y \`route_cost_model.json\`—, (b) publicación versionada de carta a una campaña concreta, y (c) **conocimiento concedido al observador** por Core. El material de referencia no se convierte automáticamente en carta visible ni en verdad conocida.

- \`chart_ref\` y \`chart_revision\` identifican una publicación aprobada con procedencia; \`knowledge_revision\` representa el alcance observable; la publicación deberá definir semántica de identidad estable y tratamiento de cambios de contenido. No presentar nodos del catálogo no publicados como destinos conocidos.
- La lectura solo devuelve una **proyección** de lugares, aristas, restricciones, riesgos y fuentes autorizadas. Ni el WorldState completo ni hechos de sensores o riesgos ocultos. Un \`parent_location_id\`, \`source_refs\` o índice de búsqueda también puede filtrar lugares ocultos: filtrarlos antes de resolver nombres, rutas y estadísticas.
- Una localización físicamente existente y una localización conocida **son cosas distintas**. Para nombres homónimos, aclarar solo entre candidatos visibles. Los destinos ocultos y los inexistentes producen una misma respuesta pública de desconocido/no accesible para no permitir enumeración.
- Las aristas con \`distance_ly=null\` pueden indicar adyacencia conocida, **no ETA numérica** ni velocidad implícita. \`z_ly=null\` permanece \`null\`; no se establece plano Z=0. Cruzar un agujero de gusano requiere mecánica propia, jamás tratarlo como warp normal.
- Los cinco perfiles existentes (\`fastest\`, \`safest\`, \`avoid_hostile_space\`, \`prefer_starbase_support\`, \`silent_or_low_contact\`) son preferencias de búsqueda, **no resultados garantizados**. Sin datos suficientes se indica incertidumbre; no usar peligros secretos para puntuar.

## 4. Contratos de solo lectura y propuesta

| Operación lógica interna | Entrada de confianza | Salida prevista | Prohibiciones |
| --- | --- | --- | --- |
| \`read_own_location\` | Campaña y nave resueltas en hilo dueño, observador autorizado, generación | \`KNOWN / UNKNOWN / UNAVAILABLE\`, lugar tipado o nulo, revisiones y procedencia filtrada | No escribir lugar, tick, historial ni inferir posición a partir de UE |
| \`read_authorized_chart\` | Sesión, nave, observador y publicación aprobada | Carta recortada por conocimiento y permisos, revisiones Core/carta/conocimiento, procedencia visible | No exponer catálogo global, ni hechos desconocidos, ni datos de otro observador |
| \`propose_known_route\` | Destino visible, perfil existente, snapshot autorizado de lugar/carta/conocimiento | \`proposal_ref\` efímera o rechazo/ambigüedad; tramos conocidos, incertidumbre, distancias/ETA opcionales | Nunca mover nave, reservar recursos, ejecutar CONN, consumir RNG o agenda |

La propuesta exige origen conocido **y** carta publicada/visible. Una ruta sin tramos conocidos no debe fabricarse ni confundirse con ausencia física de conexión: responder \`NO_KNOWN_ROUTE\`, no «imposible viajar». Un punto de origen \`UNKNOWN\` bloquea propuesta (\`LOCATION_UNKNOWN\`), aunque se permitan consultas de carta autorizada.

El \`proposal_ref\` no es un permiso, un recibo de mando ni un identificador Core global: se vincula a campaña, sesión, generación, nave, observador/autorización, revisión Core, ubicación, carta y conocimiento. Validar esos elementos en cada consumo. Invalidar referencias al guardar, restaurar, cerrar sesión, cambiar nave/observador o revocar permisos; \`SAVE\` no cambia necesariamente generación pero sí invalida propuestas según contrato P03. Los fallos y rechazos **no** modifican posición, tick, RNG, recursos, eventos ni bytes canónicos persistidos. No volver a intentar solicitudes automáticamente.

**Respuestas:** \`SERVICE_UNAVAILABLE\` si la capacidad aún no existe; \`NOT_AUTHORIZED\` si no existe admisión/visibilidad; \`LOCATION_UNKNOWN\` si falta origen; \`DESTINATION_UNKNOWN_OR_REDACTED\` para no enumerar verdad oculta; \`CLARIFICATION_REQUIRED\` solo sobre homónimos visibles; \`NO_KNOWN_ROUTE\` para falta de ruta en la proyección; \`STALE_CONTEXT\` al invalidarse revisiones/permiso/generación; \`INVALID_PROFILE\`; \`INVALID_CHART\`. Son códigos de **diseño**, no ampliaciones del enum ABI actual; mapearlos a errores existentes sin filtrar datos hasta aprobar una interfaz.

## 5. Compatibilidad y propiedad de los datos

| Pieza | Dueño | Persistencia y regla |
| --- | --- | --- |
| Localización discreta de nave | Campaña \`WorldState\` Core | Hecho tipado validado; formato y esquema F04 sujetos a P0 |
| Relación observable de ubicación | Vista autorizada del dominio Core | Leer únicamente bajo identidad resuelta y permisos; ausencia → desconocido |
| Definiciones de carta | Autoría/versionado de producto | No son hechos en campaña hasta publicación aprobada |
| Alcance cartográfico conocido | Conocimiento por observador en Core y publicación de carta | No almacenar verdad visible en una caché paralela |
| Propuesta efímera y correlación | HOST, **no autoritativo** | Invalidar por ciclo de vida y revisión; no guardar como hecho de movimiento |
| Maniobras, consumos, progreso, reloj | Futuro ejecutor naval Core + F04/F05 | **FUERA DE C02**: no usar \`F04_MOVE\` ni \`Timeline::schedule\` como atajos |

Preflight de implementación: identificar exactamente el generador de catálogo F04, inicialización de campaña naval, \`schema\`, snapshot y validación de restauración, así como el mecanismo de observador. Presentar matriz de compatibilidad **campaña antigua sin lugar / campaña nueva sin origen aprobado / campaña con ubicación y carta autorizadas / carta modificada o despublicada / observador revocado**. No introducir migración destructiva ni cambio de pin sin autorización diferenciada.

## 6. Plan de trabajo y responsables

1. **C02-A — ChatGPT:** especificación de fronteras, contrato JSON, matriz de aceptación, pruebas documentales y encargo nativo. Entregables en esta PR.
2. **C02-B — Codex, Sol 6.2 Medium:** P0 sobre composición/guardado; informe exacto de cambio mínimo y coste de compatibilidad. Sin CoreRPG ni cambio de pin.
3. **C02-C — Codex, solo si P0 aprobado y compatible:** extensión de lectura de ubicación y carta publicada, caso de origen \`UNKNOWN\` y aislamiento de observador; pruebas reales de carga/recuperación.
4. **C02-D — Codex, tras C:** resolvedor de propuestas sobre rutas **conocidas**, sin movimiento; validación de revisiones, lifecycle, inmutabilidad y handoff S11 de datos si procede.
5. **C02-E — ChatGPT:** auditoría independiente, revisión de CI y recomendación de fusión. El propietario autoriza fusiones relevantes.

La aceptación de C02-B **no** aprueba automáticamente cambios de esquema, bootstrap, F04/F05, API pública o CoreRPG en C02-C. Si P0 falla, resultado válido es informe de bloqueo y petición concreta de autorización; nunca un motor alternativo.

## 7. Matriz de aceptación futura y cierre

La matriz \`H09_P03_C02_CONTRATO_DOMINIO_NAVAL_v1.json\` identifica los **14 casos CN2-01…CN2-14**, todos \`NOT_RUN\`. Incluye: campaña sin origen, fuente Core, catálogo/carta visible, aislamiento por observador, homónimos, rutas conocidas/desconocidas, distancia y coordenada nula, inmutabilidad del estado, cambio de revisión, invalidación SAVE/RESTORE/CLOSE, compatibilidad guardados antiguos y ausencia de ejecutor CONN. Mapear después los casos N3-01…N3-14 del contrato P03; **no** marcarlos PASS por completar este documento.

**Cierre C02-A:** documentos y validadores estáticos coherentes, GitHub Actions verde sobre la PR y entrega del encargo; no certifican Core ni navegación.  
**Cierre C02 funcional futuro:** código nativo con pin Core intacto (o autorización específica de cambio), carga/restauración real, aislamiento, oráculos de inmutabilidad, Linux y Windows, auditoría y PR independientes.  
**No desbloquear:** F06/H09-P02 pendientes de aceptación MSI, H09-P03-E (CONN y vuelo) sin ejecutor/autorización F04/F05, H09-P03-F UE/MSI y H09-P04 sin iniciar.
