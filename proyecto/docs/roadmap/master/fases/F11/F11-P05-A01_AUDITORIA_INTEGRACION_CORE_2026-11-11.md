# F11-P05-A01 — Auditoría estática para integración de carrera profesional

**Fecha:** 11-11-2026  
**Estado de esta entrega:** auditoría del código y contratos, **no** integración ejecutada.  
**Star Trek auditado:** `main` `f5ffc81a51d3812506257575df7c13165e62933e` (P01–P04 fusionadas).  
**CoreRPG auditado:** `main` `76a7b7b485616d8c4994f384a90f123bf333591d`, que coincide con el pin usado por F05.  
**Normas:** no modificar CoreRPG ni los módulos jugables durante A01; no declarar P05/F11 completadas; no gastar cuota de Codex en esta auditoría.

## 1. Conclusión ejecutiva

**Resultado: A01_AUDITADA_CON_BRECHAS_BLOQUEANTES.** Hay una base real y reutilizable de F04/F05, pero no existe aún una implementación general de **carrera profesional de Flota, promociones autorizadas, sucesiones de NPC y traslados entre unidades**.

**Primer corte A02 recomendado:** operación **atómica e idempotente de promoción de un alférez existente a teniente júnior, sin modificar su destino ni su plaza**, autorizada por personal competente de Flota, con expediente de promoción persistente y pruebas de guardado/carga. Previamente hay que fijar la **identidad profesional estable** y la codificación de grados para que el primer parche no dificulte los traslados posteriores. **No** se recomienda convertir A02 en un parche directo a `F04_RANK` ni otorgar al capitán facultad universal de ascender.

**Dependencia estructural posterior muy importante:** F04 administra **una nave por `F04Session`**. El traslado entre dos naves y el ascenso hasta la Enterprise-D requerirán una **identidad global y un mecanismo autoritativo de Flota** que cubra ambas unidades. Copiar una persona de una sesión a otra, creando otro ID, incumpliría el contrato F11.

## 2. Inventario con trazabilidad a código real

| Capacidad | Clasificación A01 | Evidencia y consecuencia |
|---|---|---|
| Entidades, relaciones, revisiones, validación genérica | **REUTILIZAR** | CoreRPG [`WorldState`](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/include/corerpg/world_state.hpp) permite entidades/relaciones genéricas, sin entender «ascensos» |
| Reloj de campaña y acciones futuras | **REUTILIZAR/AMPLIAR EN HOST** | Core `Timeline`; F04 [`f04_advance`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L779) avanza reloj y procesos existentes, **no** planifica revisiones profesionales por sí mismo |
| Identidad de personal en una sesión | **REUTILIZAR/AMPLIAR** | F04 [`person`, `F04Person`, `f04_person`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/include/f04_bridge.h#L77) distinguen individuos; falta identidad **global** estable al cambiar de nave |
| Atributo de rango actual | **REUTILIZAR CAMPO/CREAR OPERACIÓN** | F04 almacena el escalar `RANK` y `F04Person.rank`; [bootstrap de tripulación](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L301) deja `RANK=0` para la mayoría. No se identificó una operación pública de ascenso con autoridad profesional, eventos y control de adyacencia |
| Codificación canónica de grados | **ADAPTAR** | F11 usa IDs semánticos `ensign` → `lieutenant_junior_grade`; F04 usa números de dominio y algunos datos sintéticos (p. ej. capitán de muestra con otro valor). **No asumir** `rank+1` ni usar `RANK=0` como alférez; establecer mapa versionado y reglas de comisión |
| Posiciones/plazas ocupadas | **REUTILIZAR CON VALIDACIÓN NUEVA** | [`f04_positions_page`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L897) muestra `F04Position.person` (titular real) y `on_duty` separadamente; solo `person==0` indica plaza sin ocupante |
| Cobertura de guardias y `F04Stats.vacancies` | **NO USAR COMO VACANTE PROFESIONAL** | [`f04_stats`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L760) suma «vacancies» por ausencia de `duty(...,now)`: una plaza ocupada fuera de guardia puede contarse ahí. Usar titular de plaza + autoridad, no cobertura |
| Reasignación dentro de una nave | **REUTILIZAR CON GUARDAS** | [`F04_TRANSFER`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L475) comprueba plaza libre/mismo ocupante, cualificaciones y limpia tareas antiguas; **no** es transferencia entre dos naves/F04Session distintas |
| Asignación directa `F04_ASSIGN` | **RIESGO: NO LLAMAR DIRECTAMENTE PARA SUCESIONES F11** | [`F04_ASSIGN`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L554) puede sustituir al ocupante de una plaza tras cancelar su puesto, según las reglas existentes. F11 exige **rechazar una plaza ocupada** hasta el cese real; añadir comprobación específica en la operación profesional |
| Desembarco `F04_DEPART` | **REUTILIZAR PARCIALMENTE** | [`F04_DEPART`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L539) quita adscripción y cancela actividad local; **no** confirma que el NPC haya sido dado de alta en otra nave ni una transacción de dos destinos |
| Nombramientos y sucesión operativa | **REUTILIZAR/ADAPTAR** | [`F04_APPOINT`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L611) crea cargos/roles en la nave bajo mando actual; **no es** una orden de Flota para nombrar/comisionar o cambiar grados |
| Órdenes F05, idempotencia y registro | **REUTILIZAR MECANISMO; OPERACIÓN NUEVA** | [`F05OrderRequest`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f05/include/f05_orders.h) y [`f05_submit`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f05/src/f05_orders.inc#L61) ya fijan revision, clave, recepción/resultado; **`f05_validate` exige `F04_SCAN`** y no procesa promociones |
| Autorización de personal de Flota | **NO IMPLEMENTADA** | La autoridad de F04/F05 es mando de nave/departamento, además de mandatos especiales de otro ámbito; **no** equivale a una autoridad de Flota que aprueba promociones o nombramientos entre unidades |
| Evaluaciones profesionales autoritativas | **NUEVO MODELO RUNTIME** | F11-P03 contiene [contrato y Python](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/tools/validation/f11_p03_progression_reference.py); no hay eventos F11-P03 firmados y validados dentro de F04 |
| Director de carrera de NPC y liberación causal | **NUEVO MODELO RUNTIME** | F11-P04 [directorio de referencia](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/tools/validation/f11_p04_succession_reference.py) **no modifica** Core; falta estado profesional persistente y decisiones NPC verificadas |
| Expediente histórico | **ADAPTAR** | [`service_record_model.json`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/sistemas/gameplay/careers/service_record/service_record_model.json) define `promotion`, `transfer`, `commendation` etc. como contrato; falta materialización de hechos de personal dentro de `WorldState` |
| Transacción y guardado/carga en una sesión | **REUTILIZAR/AMPLIAR** | [`f04_execute`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L768) valida sobre copia y publica al completar; Core [`CampaignPersistence`](https://github.com/robdor80/CoreRPG/blob/76a7b7b485616d8c4994f384a90f123bf333591d/include/corerpg/campaign_persistence.hpp) conserva campaña y reloj. Los **nuevos** registros deben quedar en esa misma autoridad y ser compatibles con historia segmentada |
| Campañas largas con historial segmentado | **REUTILIZAR CON PRUEBAS** | F04 tiene [`HistoryPersistence`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/HISTORY.md); F05 activa el modo de historia. Ningún registro nuevo de carrera debe archivarse por error mientras esté activo su plan, su orden, su obligación o su identidad |
| Identidad de Enterprise-D refit | **NUEVA INSTANCIA, NO REUTILIZAR «VALHALLA» AUTOMÁTICAMENTE** | [Catálogo de clases](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/mundo/lore/starships/classes/core_starship_classes.json) contiene Galaxy; F04 tiene plantilla de **nueva clase Valhalla**, distinta de la Enterprise NCC-1701-D modernizada. Se precisan identidad, dotación y puesto de capitán auténticos |
| Representación Unreal | **REUTILIZAR PATRÓN/AMPLIAR** | [`F04CampaignSubsystem`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/unreal/F04CampaignSubsystem.h) y F05 UE de laboratorio; todavía no se ofrecen UI ni interacciones finales para progresión de F11 |

**Clasificación de madurez:** «REUTILIZAR» significa API o contrato auditado **por lectura de fuentes**, no que A01 haya vuelto a compilarlo ni probado su comportamiento en MSI. El estado de F05 y sus evidencias previas no se atribuyen como nueva validación de F11.

## 3. Tres riesgos de integración que deben resolverse antes de la carrera completa

### R1 — Alcance de identidad y transacciones entre naves (BLOQUEANTE para campaña completa)

Actualmente se crea una unidad de nave como entidad 1 de una `F04Session`, y [`f04_initialize_population`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/src/f04_bridge.cpp#L293) añade personas vinculadas a `SHIP=1`. `F04_TRANSFER` solo transfiere entre plazas de la **misma sesión**.

La carrera hasta la Enterprise-D **no debe** simular un traslado haciendo `DEPART` en una nave y `EMBARK` como persona nueva en otra, ya que fragmentaría la identidad del oficial, sus relaciones y el historial. Antes de habilitar traslados, adoptar una de dos arquitecturas y probarla:

- **Opción preferente a estudiar:** único `WorldState` autoritativo de Flota, con múltiples unidades y plazas, y transacciones que incluyan ambas naves; exige adaptar la proyección mononave de F04 y revisar rendimientos/esquemas.
- **Alternativa solo si se acredita compatibilidad:** coordinador de Flota con identidad global e historial autoritativo común, capaz de confirmar o revertir atómicamente el cambio entre sesiones sin duplicar personas ni mezclar generaciones de guardado. **No** usar JSON/SQLite paralelo como segundo dueño del mismo estado.

La primera promoción local de A02 puede desarrollarse **sin transferir todavía a nadie**, pero debe usar una identidad persistente preparada para esa decisión futura. No aprobar traslados inter-nave hasta cerrar R1.

### R2 — Autoridad de promoción y conflicto con F05 (BLOQUEANTE A02)

El [código F05](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f05/src/f05_orders.inc#L16) rechaza cualquier orden distinta de `F04_SCAN` en su dominio actual. Un capitán con autoridad operativa F04 no tiene automáticamente autoridad institucional de **Personal de Flota**.

Definir un contrato **nuevo y explícito** de autoridad profesional (identidad/competencia del emisor, grado anterior/siguiente, expediente, revisión, causa, caducidad y clave de idempotencia). El Host autentica al actor y Core/Trek lo valida. **No** reinterpretar `F04_SCAN`, no hacer pasar una propuesta de IA por una orden y no permitir que una casilla booleana del cliente acredite una firma.

### R3 — Semántica de vacante, rango y estado guardado (BLOQUEANTE A02/B)

- `F04Stats.vacancies` refleja cobertura de guardias: no utilizarlo para promociones.
- `F04_ASSIGN` es válido para otras operaciones de la nave, pero puede sustituir un ocupante; F11 debe requerir titular libre y orden de relevo.
- Los rangos F11 usan **IDs de cadena**, mientras que F04 utiliza escalares de dominio; hace falta correspondencia versionada **que no cambie significados históricos**.
- En los perfiles de plantilla el personal puede comenzar con `RANK=0`: no promover un oficial no comisionado por tratar `0` como alférez.
- Los contratos F11 actuales solo generan propuestas offline. `ready_since_month`, `plan_id`, `rank_event_id`, evaluaciones y propuestas NPC **no** viven aún en Core; si se mantuvieran únicamente en un proceso Python, se perderían al cargar.

## 4. Plan aprobado para el primer incremento técnico F11-P05-A02

### A02-00 — Contrato de identidad y rango (antes de tocar mutaciones)

1. Fijar `character_id` estable de carrera, `current_rank_id` y `rank_event_id` con origen en el mundo autoritativo. Precisar la equivalencia entre el rango de F04 y el ID Starfleet sin modificar archivos de guardado antiguos.
2. Fijar autoridad legítima de Personal de Flota y cómo se referencia desde la misma sesión, sin confundirla con `F04_CAPTAIN`. Si hay un mandato/servicio externo, acreditar su fuente y alcance.
3. Fijar el registro inmutable de promoción vinculado a hechos previos de evaluación y al evento de rango; prohibir emisión por nombre, cliente o LLM.
4. Auditar si se necesitan **nuevos tipos Trek dentro de WorldState**, con validador de esquema, sin ampliar la API genérica de CoreRPG salvo necesidad demostrada.
5. Definir migración reversible por guardados legados, flags opt-in y ruta de laboratorio, **sin editar imágenes ni fuentes originales del usuario**.

### A02-01 — Primera promoción real, deliberadamente estrecha

**Entrada de ensayo:** oficial humano existente en una sesión F04, **comisionado previamente como alférez** por evento válido, evaluación y cualificación verificadas; petición de Personal Flota para `ensign → lieutenant_junior_grade`.

**Resultado que sí debe existir:** Core refleja **grado teniente júnior** y registra una promoción única autorizada; mismo `character_id`, misma `unit_id`, `billet_id`, departamento, cualificaciones y órdenes no relacionadas. No adquiere mando, no ocupa otra plaza ni cambia de nave.

**Límites innegociables:**
- No saltos `ensign → captain`; no rango por XP, contador de meses o medalla aislada.
- Verificación de actor/autoridad, revisión del mundo, validez de evaluación, escalafón y causa **en el instante de confirmar**.
- **Clave de idempotencia**: reintentar idéntica petición no crea otro ascenso/evento; misma clave con datos diferentes debe devolver conflicto.
- **Transacción única**: rango y evento de expediente se confirman juntos, sin estado intermedio persistible.
- Rechazar misma sesión ajena, grado 0/no comisionado, autoridad falsa, evaluación inventada, solicitud caducada, rango ya cambiado y errores de carga.
- La consulta `f04_person` y la proyección Host deben ver el rango nuevo **después** de confirmar; no mediante un valor local de interfaz.

### A02-02 — Persistencia y pruebas de regresión del primer ascenso

1. Guardar antes, ascender, guardar después y cargar en otro proceso; identidad, cargo, grado y evento se mantienen.
2. Guardar ante un fallo inyectado; no debe aparecer grado nuevo sin evento ni evento sin grado.
3. Repetir tras una carga: misma key, ningún nuevo evento.
4. El modo de historial segmentado F04/F05 conserva identidad, hechos y futuro; validar en el Core real en sus SHAs fijados, con comparación de campañas repetibles.
5. Ejecutar F04/F05 nativo íntegro sin alterar su API, test de rangos y regresión de Unreal **cuando proceda**.
6. En el MSI, pruebas NullRHI y D3D12 **solo después de integrar la capacidad**, no se consideran aprobadas desde A01.

**Regla de cierre del incremento:** `A02-01` **no** supera aceptación si solo pasa el Python de P01–P04, si el grado aparece en una ventana de UE o si el evento vive en un archivo lateral. Debe existir dentro del `WorldState` autoritativo y sobrevivir a recuperar una partida.

## 5. Secuencia posterior para P05 sin desbordar A02

| Bloque | Objetivo real | Requiere |
|---|---|---|
| **A02** | Comisión/primer ascenso interno autorizado, histórico e identidad | Resolver R2 y R3; delimitar contrato R1 |
| **P05-B1** | Evaluaciones, méritos, sanciones y revisiones reales + planificador P03 persistente | A02 |
| **P05-B2** | Vacantes y nombramientos P02/P01 a bordo **sin desalojar** NPC | A02 y contrato de autoridad |
| **P05-B3** | Flota multiunidad: transferencias atómicas o equivalentes verificadas entre naves | **R1 cerrado** |
| **P05-B4** | Director P04 de sucesión NPC y oportunidades limitadas temporalmente, con alternativas y rechazo | B1–B3 |
| **P05-C** | Persistencia, migración, idempotencia y recuperación integral durante relevo | B1–B4 |
| **P05-D** | Unreal 5.8.2: proyecciones sin autoridad, ofertas, ceremonia y permisos que reflejan puesto real | B y C |
| **P05-E** | Carrera **end-to-end** hasta capitán Enterprise-D, campañas con varias semillas y negativas | Todo lo anterior |

La **Enterprise-D** necesita instancia funcional legítima de clase Galaxy refit en el mundo, con capitán NPC, XO NPC, plazas e historia previa, **sin** reutilizar sin más la plantilla histórica de nueva clase Valhalla. Deben definirse sus requisitos organizativos y comprobar su compatibilidad de época.

## 6. Pruebas de vida profesional larga: propiedades de seguridad y progreso

**Seguridad (siempre):**
- Nunca dos titulares efectivos de una misma plaza, ni un mismo personaje duplicado entre destinos.
- Nunca un ascenso sin autorización/evaluación; nunca un relevo antes de la fecha efectiva.
- Nunca un nuevo capitán por **rango** sin puesto, orden de nombramiento y unidad concreta.
- NPC conserva identidad, rango, relaciones y memoria de la oferta rechazada.
- Los registros son históricos de solo adición; guardar/cargar y repetir mensajes no crea efectos múltiples.

**Progreso (bajo condiciones explícitas):**
- Si el jugador sigue voluntariamente la ruta de mando, está habilitado y los hechos avanzan, no queda bloqueado para siempre por un resultado azaroso de vacantes.
- P03 mantiene ancla y fecha límite; P04 debe disponer de mecanismos profesionales **causales y verificables** para generar rutas alternativas.
- Una cadena infructuosa se registra como **deuda de oportunidad pendiente**, no como «ascenso completado».
- Probar campañas repetidas y adversas: NPC rechaza, varias plazas ocupadas, cambio de mando, partida guardada a mitad de traslado, dos aspirantes compitiendo, jugador pospone.
- **Prueba final de aceptación:** un único jugador con identidad persistente llega a ocupar el puesto `commanding_officer` de la instancia autoritativa `USS Enterprise NCC-1701-D` con rango `captain`, conservando cronología y expediente, y la partida continúa después.

**Precisión matemática:** la «garantía» exige una condición de vivacidad o *liveness*, pero no puede acreditarse si el universo permite un estado imposible sin ninguna alternativa legítima. P05-E debe **refutar esa posibilidad por diseño** mediante vías reales de Flota, o fallar la prueba y registrar qué invariantes impidieron progresar. No se solucionará el fallo falsificando consentimiento, órdenes o historia.

## 7. Entorno, dependencias y protecciones de A02

- F04 pin sin historia opt-in: `c147d81ed069da2e09149613ab02cbc3ebe95a4a`; F05 activa historia y usa CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d`. [CMake F04](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f04/CMakeLists.txt) verifica SHA y limpieza. **No actualizar pins de F02–F05 en bloque**; compilar el incremento contra el pin exacto de la ruta F05, preservar el arranque por defecto y documentar compatibilidad.
- F05 tiene una sola biblioteca puente F04 y **una única sesión**, según [CMake F05](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/desarrollo/integration/f05/CMakeLists.txt); no añadir otro `WorldState` persistente solo para F11.
- Desarrollar en rama específica del repositorio Trek; si CoreRPG necesitase una función **genérica**, abrir PR independiente en Core y compatibilizarla explícitamente antes de adoptar el pin.
- Laboratorios temporales en `laboratorios/f11/p05-a02-<tarea>/`, ignorados por Git y completamente desechables. No tocar originales Blender, modelos PBR ni proyectos UE artísticos; no borrar laboratorios anteriores. [`AGENTS.md`](https://github.com/robdor80/Videojuego_StarTrek/blob/f5ffc81a51d3812506257575df7c13165e62933e/AGENTS.md).
- A01 **solo leyó fuentes remotas** y elaboró informe. **No** compila C++, no ejecuta suite Core/F04/F05, no entra en UE, no prueba una partida en el MSI y **no** consume cuota Codex.
- Antes de aprobar cualquier PR nativa: pruebas C++ + Core compatibles, persistencia/recuperación, legacy saves, condiciones de carrera, autoridad y escenarios de regresión; distinguir `REFERENCIA_PROBADA` de `CORE_INTEGRADO` y `UE5_JUGABLE`.

## 8. Decisión recomendada para la siguiente entrega

**A02 debe arrancar con el contrato A02-00 y una única operación de promoción local A02-01**, no con la carrera completa ni con un sistema de Flota global improvisado.

**Recomiendo usar Codex solo para la modificación C++ real** (modelo GPT-6, pensamiento **alto**) después de fijar el contrato, con intervención limitada en el puente Trek y tests. El usuario/ChatGPT pueden preparar casos, criterios y revisión documental sin gastar cuota.

### Puerta de aceptación A01

- [x] Identificados mecanismos reales Core/Timeline/WorldState y F04/F05.
- [x] Separados puesto, grado, mando, orden y plaza realmente vacante.
- [x] Identificados bloqueos: rango, autoridad de Flota, identidad multiunidad, persistencia de planes.
- [x] Definido corte mínimo A02 y sus pruebas de éxito/fracaso.
- [x] Especificada ruta de validación de campañas hasta Enterprise-D.
- [ ] **Pruebas nativas de ejecución**: pendientes de A02/P05; fuera de alcance A01.
- [ ] **Decisión final sobre arquitectura de Flota multiunidad**: pendiente de diseño previo a B3.
