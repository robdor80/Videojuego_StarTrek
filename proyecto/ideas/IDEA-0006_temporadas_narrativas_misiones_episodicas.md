# IDEA-0006 — Sistema de temporadas narrativas y misiones episódicas

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación:** 2026-10-13  
**Estado:** APROBADA (diseño conceptual); planificación técnica e implementación pendientes  
**Decisión del autor:** propuesta discutida y aprobada expresamente («Sí») el 13-10-2026.  
**Numeración:** `IDEA-0005` ya estaba asignada al blindaje ablativo y torpedos transfásicos de Clase Valhalla; se utiliza el siguiente identificador libre, **IDEA-0006**, sin renumerar ideas previas.  
**Áreas:** narrativa, misiones y órdenes, universo persistente, cadena de mando, carrera/destinos, Core RPG, IA, carga externa de contenido.

## 1. Visión aprobada

Incorporar al videojuego el concepto de **TEMPORADAS**: arcos argumentales completos, inspirados en la organización de una temporada televisiva de Star Trek, que agrupan **episodios o misiones relacionados causalmente** y conducen a investigar, afrontar o resolver un conflicto, pregunta u objetivo narrativo central.

Cada episodio debe aportar información o consecuencias coherentes a la trama conjunta. La temporada no implica una secuencia de escenas fijas, un resultado inevitable ni que el jugador sea el protagonista omnipotente del universo.

**Tres requisitos centrales del autor:**

1. **Adecuación a la nave y al destino.** El tipo de misiones depende de capacidades, propósito, época, contexto y preparación reales de la unidad y del papel profesional del jugador. Ejemplo: una **Oberth científica** con un alférez en su primer destino debería participar principalmente en investigación, exploración, cartografía o tareas científicas, **no recibir rutinariamente encargos de enfrentamiento o incursión táctica en la Zona Neutral** para los que no está preparada.
2. **Tiempo libre entre episodios.** La trama no ocupa toda la experiencia. Entre misiones pueden transcurrir guardias ordinarias, viajes, mantenimiento, descanso, relaciones, actividades en camarote, exploración y sucesos emergentes. No forzar un encadenamiento inmediato de capítulos.
3. **Autoría y carga externa.** El autor y ChatGPT podrán diseñar nuevas temporadas fuera del ejecutable, describirlas en **paquetes de datos estructurados**, validarlos e incorporarlos después a una partida compatible. El motor debe poder cargar episodios adicionales sin recompilar por cada historia que use mecánicas, consolas, eventos y recursos **ya implementados**.

Las órdenes que originan las misiones deben proceder de las **autoridades legítimas del mundo de juego**, como el Mando de la Flota Estelar, y seguir la cadena de mando normal.

## 2. Terminología y responsabilidades

- **Temporada:** paquete autoral que contiene premisa, conflicto central, requisitos, episodios, conexiones, posibles ramificaciones, condiciones y consecuencias.
- **Episodio:** unidad de contenido narrativo con objetivos y condiciones de inicio/desarrollo/cierre; puede dar lugar a una o más **misiones** operativas, interacciones, investigación o sucesos contextualizados.
- **Misión:** tarea concreta y autoritativa que ya usa `mission_state`, `mission_objective_state`, órdenes y tareas de servicio existentes. **No crear un sistema paralelo de misiones**.
- **Trama/estado narrativo:** datos persistentes sobre descubrimientos, pistas, decisiones y resultados que ligan los episodios, derivados de acontecimientos realmente resueltos en el mundo.
- **Entre episodios:** intervalo abierto en el que el juego sigue funcionando normalmente y puede haber actividad sin misión argumental activa.
- **Pack de temporada:** contenido importable y versionado, **no código ejecutable arbitrario**; define propuestas y condiciones de activación mediante vocabulario y efectos autorizados por el motor.

Una temporada es una **capa de contenido y orquestación narrativa**, no la entidad propietaria de la verdad del universo. Core RPG sigue siendo autoritativo en materia de estado, acciones, persistencia y eventos genéricos; Star Trek define doctrina, alcance narrativo, capacidades de naves, órdenes e historia; UE5 presenta las acciones, escenas, diálogos y consolas.

## 3. Elegibilidad: a cada nave las misiones que le corresponden

Antes de ofrecer o activar contenido se comprobarán filtros y condiciones:

- **Clase/configuración y capacidades reales** de la nave: perfil científico, táctico, exploración, capacidad de transporte, sensores, equipamiento, autonomía, hangares, estado operativo.
- **Destino profesional del jugador, rango, puesto y autoridad vigente.** Un alférez participa desde su estación y no sustituye arbitrariamente al capitán; un oficial superior tiene atribuciones distintas.
- **Era y fecha de campaña**, tecnología disponible, organizaciones existentes y continuidad propia que rige esa partida.
- **Situación actual:** ubicación, tripulación, alistamiento, recursos, amenazas, órdenes vigentes, necesidades de la Flota y apoyo accesible.
- **Condiciones narrativas:** pistas conocidas, episodios resueltos, rutas abiertas, restricciones y consecuencias pendientes.
- **Compatibilidad de assets y mecánicas:** el pack solo se activa en un entorno capaz de representar lo que necesita.

No confundir **compatibilidad de un pack** con **asignación automática de todas sus misiones al jugador**. Puede existir una temporada científica compatible con varias clases (por ejemplo, Oberth y Nova), pero el Mando asignará tareas concretas a unidades idóneas según el estado del mundo.

## 4. Estructura dramática flexible

Las temporadas tendrán un objetivo común identificable y una progresión reconocible, pero sin imponer una única solución.

Se propone gestionar:
- Premisa, ámbito científico/político/cultural/operativo y tema central.
- Introducción, desarrollo, hitos de descubrimiento, posibles giros, crisis y desenlaces.
- Episodios con **dependencias condicionales** (no necesariamente una lista lineal).
- Pistas y hechos descubiertos, con separación entre **verdad del mundo** y **conocimiento permitido al personaje o su mando**.
- Objetivos principales/opcionales por misión y alternativas de solución respaldadas por reglas reales.
- Estados de episodio: no disponible, candidato, autorizado, activo, resuelto, fallido, cancelado, caducado o desplazado, a concretar cuando se defina el contrato.
- Ramificaciones, sustituciones, episodios opcionales, cierre parcial, fracaso y resolución por otras unidades NPC.

**Regla de continuidad:** el episodio siguiente no presupone logros que no hayan ocurrido. Una pérdida, muerte, cambio de nave, orden revocada o decisión inesperada pueden modificar los capítulos disponibles. Un fracaso no obliga a reiniciar ni genera `game over` por defecto.

El objetivo central puede concluir de más de una manera: resuelto, parcialmente resuelto, sin resolver, abandonado o continuado por otras fuerzas, siempre sustentado por la simulación.

## 5. Periodos libres y ritmo de temporada

El jugador conserva el **derecho a vivir la nave** entre misiones argumentales. No se exige estar resolviendo capítulos permanentemente.

Actividades compatibles: guardias normales, informes, relevos, mantenimiento, investigaciones opcionales, prácticas, holocubierta, ocio, replicador, música, amistades, exploración y encargos emergentes.

El ritmo deberá depender de órdenes, tiempo de viaje, ventanas operativas, estado real del universo y decisión de mando. No asignar arbitrariamente un episodio nuevo cada cierto número de minutos para «llenar» la partida.

**Excepción realista:** misiones urgentes o emergencias genuinas pueden imponer plazos y consecuencias; «tiempo libre» no significa congelar el universo, permitir ignorar una orden sin consecuencias ni detener artificialmente los acontecimientos externos.

Las tramas diseñadas coexisten con misiones emergentes y actividades ordinarias. Debe existir política para prioridades, órdenes simultáneas, interrupciones, aplazamientos y relevos, sin romper la cadena de mando.

## 6. Órdenes auténticas del Mando y participación por rango

La llegada de una misión de temporada reutiliza la secuencia ya definida:

`situación válida del universo → necesidad operativa/orden legítima → selección de unidad apta → orden de misión → informe al mando de la nave → órdenes y tareas por puesto → ejecución → informe/debrief → consecuencias`.

El jugador puede recibir la orden **indirectamente**, a través de capitán, primer oficial o jefe de departamento. El expediente de cada episodio distingue la información a la que tiene acceso el mando de la que recibe un alférez.

Un oficial de Sensores puede contribuir decisivamente sin decidir el rumbo estratégico de toda la nave. El capitán y el resto de NPC conservan autoridad, objetivos y comportamiento persistentes.

El Mando no puede emitir mágicamente órdenes imposibles: caben requerimientos de aclaración, imposibilidad material, apoyo, cambio de misión, renuncia válida o consecuencias disciplinarias, conforme a las reglas existentes.

## 7. Integridad del universo: contenido guionizado sin realidad inventada

**Riesgo arquitectónico más importante:** no contradecir `emergent_mission_from_world_state_contract`, que prohíbe que una misión emerja porque una IA invente una crisis y finja que ya existía.

Solución conceptual:
1. Un pack puede describir **contenido autoral preparado**, incluidos actores, lugares, premisas, condiciones y acontecimientos potenciales, sin declarar por sí mismo que ya son hechos vivos.
2. Al crear/inicializar una campaña o aceptar contenido nuevo, un **proceso de incorporación autorizado** deberá comprobar compatibilidad, conflictos, cronología, disponibilidad y permisos antes de materializar *cualquier* dato nuevo. Registrar procedencia y eventos del pack como contenido del juego, **no como hechos preexistentes descubiertos retroactivamente**.
3. Cada episodio debe activar su posibilidad mediante un hecho/condición verificado del **World State**, una orden permanente/servicio válido, una necesidad operativa o un evento autoral **incorporado legítimamente** conforme a reglas explícitas de campaña. En caso contrario queda inactivo.
4. El AI Director puede seleccionar presentaciones, redactar resúmenes o verbalizar *información autorizada*, pero **no** inventar contactos, naves, asesinatos, víctimas, guerras, pistas o resultados como si ya estuviesen en el mundo.
5. Los cambios de World State provienen exclusivamente de acciones/eventos resueltos por los sistemas autoritativos; no de un texto JSON leído sin validación ni de una respuesta libre de IA.
6. Las unidades NPC pueden encargarse de partes de la trama; no todas las situaciones se generan cerca del jugador.

**Pendiente de diseño:** definir formalmente si la instalación de un pack nuevo permite introducir un escenario argumental ya iniciado en la campaña viva, o si determinados packs se restringirán al inicio de una partida. Esta aprobación **no concede** permiso general para alterar silenciosamente campañas existentes.

La historia canónica anterior al comienzo de la campaña y las decisiones de canon propio se mantienen; nunca se fuerza la repetición del futuro de una serie televisiva.

## 8. Formato externo: Season Pack

Se aprueba **el concepto de cargar temporadas externas estructuradas**. JSON es candidato principal; nombres, esquemas, rutas y manifiestos definitivos se validarán al planificar. Ejemplo de estructura **orientativa**:

```text
Temporada_Oberth_01/
├── manifest.json
├── trama.json
├── episodios/
│   ├── episodio_01.json
│   ├── episodio_02.json
│   └── episodio_03.json
└── dialogos/
    └── conversacion_01.json
```

Funciones requeridas para los packs:
- Identidad única y versión del esquema, versión propia del contenido, idioma principal castellano y metadatos del autor.
- Declaración explícita de dependencias: versión de juego, contratos, mecánicas, consolas, assets disponibles, era, capacidades, destinos y, si procede, mods compatibles.
- Identificadores de temporada, episodios y nodos **estables**; referencias lógicas a definiciones/entidades, no rutas físicas frágiles.
- Estados y condiciones usando un **lenguaje de reglas permitido y limitado**; no JavaScript/Python, DLLs ni funciones arbitrarias ejecutables desde el contenido.
- Resolución segura de referencias, orden de dependencias, ciclos inválidos, nodos inaccesibles y condiciones imposibles.
- Validación de tamaño, formatos, tipos, duplicados, versiones y archivos malformados antes de habilitar el pack.
- Diagnósticos legibles: pack incompatible, recurso ausente, episodio bloqueado por continuidad, conflicto con partida, etc.
- Instalación y activación transaccionales: un paquete fallido no corrompe el catálogo, la partida ni las temporadas instaladas.
- Conservación de la versión/identidad del pack utilizada por una partida; actualizaciones compatibles y migraciones explícitas, **sin reescribir retroactivamente resultados anteriores**.
- Política de borrado/desactivación: no invalidar una partida con temporada activa ni borrar eventos ya ocurridos; resolver con aviso, conservación del contenido necesario o bloqueo seguro hasta migración.
- Proveniencia y derechos de uso de diálogos, música, imágenes y modelos adjuntos.

**Límite aprobado:** una historia puede añadirse sin recompilar el juego **solo si usa comportamientos, operaciones, interfaces y activos que el juego ya sabe ejecutar/cargar**. Si exige una mecánica inédita o un nuevo sistema 3D, primero debe implementarse esa capacidad.

### Ejemplo conceptual mínimo de metadatos

```json
{
  "schema_version": "propuesta-no-definitiva",
  "season_id": "oberth_ecos_del_pasado",
  "title_es": "Ecos del pasado",
  "eligible_ship_roles": ["scientific_research"],
  "supported_play_roles": ["station_or_specialist_officer"],
  "episode_refs": ["episodio_01", "episodio_02", "episodio_03"]
}
```

**Este JSON no es todavía un contrato validado ni una API ejecutable.** Los filtros definitivos deben conectarse a identificadores y capacidades realmente disponibles en Star Trek/Core RPG.

## 9. Autoría, revisión e importación desde el juego

Flujo previsto para nuevas temporadas creadas por el autor con ayuda de ChatGPT:

1. Definir premisa, objetivo final, era, público objetivo, clase/capacidades de naves, participación por puesto, personajes y límites de canon.
2. Construir un mapa de episodios y condiciones de activación; revisar coherencia del arco, riesgos de bloqueo narrativo y desenlaces alternativos.
3. Escribir fichas de episodios: justificación de órdenes, objetivos, información visible/oculta, diálogos, localizaciones, variaciones y consecuencias.
4. Exportar el pack mediante los formatos/esquemas validados, con referencias a las funcionalidades realmente implementadas.
5. Ejecutar un **validador offline** (estructural, semántico, cronológico, de permisos/capacidades, de referencias y de condiciones).
6. Importar o activar el pack desde un gestor de contenido local del juego; informar de incompatibilidades antes de alterar la partida.
7. Probar el pack en una partida de ensayo y revisar jugabilidad, ramificaciones, cancelaciones y persistencia antes de aprobarlo como temporada disponible.

La IA puede colaborar en el guion y redacción, pero la aprobación creativa de cada temporada corresponde al autor, y las reglas de simulación deciden sus consecuencias.

## 10. Ejemplo de temporada científica (no pack aprobado)

**Título provisional:** «Ecos del pasado».  
**Unidad de referencia:** nave científica de clase Oberth; jugador alférez científico en su primer destino.  
**Objetivo común:** descubrir el origen y significado de varias anomalías conectadas.

| Episodio | Encargo coherente | Contribución a la trama |
|---|---|---|
| 1. Señales en la oscuridad | Cartografiar un sistema | Detectar lecturas inusuales y recopilar datos |
| 2. El eco | Investigar una fuente registrada | Comparar resultados e identificar una pauta |
| 3. Fragmentos de una civilización | Estudiar restos y registros | Encontrar indicios que modifican hipótesis |
| 4. Una decisión científica | Evaluar un procedimiento arriesgado | Solicitar apoyo, continuar o suspender con consecuencias |
| 5. El origen | Analizar las evidencias reunidas | Resolver, resolver parcialmente o dejar abierto el misterio según el mundo real |

Los nombres y episodios son **ejemplo ilustrativo de diseño**, no una primera temporada ya escrita, integrada, obligatoria ni aprobada individualmente.

Entre episodios: guardias, reparaciones, navegación, ocio, conversaciones, descubrimientos y misiones emergentes que pueden afectar recursos y cronología.

## 11. Persistencia, cambios de destino y progreso no lineal

El juego guardará, una vez que exista el sistema:
- Identificador y versión exacta de la temporada; estado general de cada arco.
- Episodios ofrecidos, iniciados, resueltos, fallidos, cancelados o inaccesibles con sus causas.
- Hechos y pistas **efectivamente descubiertos**, fuente, fecha y ámbito de conocimiento.
- Órdenes emitidas y revocadas, unidades asignadas, actores implicados, objetivos y eventos.
- Consecuencias en entidades reales (personal, naves, localizaciones, recursos, diplomacia), como referencias a los estados/eventos autoritativos.
- Estado de capítulos alternativos y posibles continuaciones, sin exigir retorno al guion inicial.

Si el jugador cambia de puesto/nave o asciende, no se resetea la historia. Una trama puede pausarse, reconducirse, continuar con NPC, concluir sin el jugador o quedar inaccesible por causa justificada. El jugador tampoco debe quedar atrapado en la misma nave para completar una temporada.

No prometer siempre un final predeterminado ni una recompensa por XP; las evaluaciones y ascensos siguen sus procesos existentes.

## 12. Responsabilidades por repositorio y sistema

| Sistema | Responsabilidad futura |
|---|---|
| **Core RPG genérico** | Identidad, estado, acciones, eventos, reglas/validación, tiempo, persistencia, carga de definiciones y flujos genéricos **solo donde haya capacidad reutilizable realmente disponible** |
| **Videojuego_StarTrek** | Semántica de temporadas y episodios, doctrina Flota, misiones, restricciones por nave y puesto, guion, contenido, canon propio, condiciones y contratos específicos |
| **UE5** | Interfaz de importación/selección, escenas y diálogos, controles, representación 3D y UX; no decidir verdad ni resultados |
| **IA** | Ayuda de escritura offline, interpretación/narración en runtime bajo límites de información y autoridad; no escritura directa del World State |
| **Validadores de contenido** | Calidad, formato, referencias, consistencia temporal, dependencias, seguridad y compatibilidad antes de instalar |

No se supone que Core RPG ya tenga cargador de packs, editor de misiones, intérprete de reglas narrativas ni APIs para la nueva capa. Esas capacidades se auditarán cuando toque.

## 13. Relación con fases y prioridades

**Asignación provisional**, sin reabrir fases ni bloquear el vertical slice de Sensores:

- **F02 — Arquitectura:** contratos, límites entre contenido, Star Trek, Core/UE5 y validación/versionado del pack.
- **F03 — Mundo/persistencia:** continuidad de misiones y episodios, estado autoritativo y restauración.
- **F04–F05 — Naves/mando/NPC:** elegibilidad de unidades, autoridad, tareas y continuidad sin protagonismo obligatorio.
- **F11 — Carrera y flota:** disponibilidad de temporadas según destino, cualificaciones y progresión.
- **F12 — Vida a bordo:** descanso, periodos entre capítulos, eventos y actividades ordinarias.
- **F13 — Universo dinámico y misiones:** integración central con necesidades operativas, misiones emergentes y hechos válidos del mundo.
- **F14 — Producción:** diálogos, escenas, localizaciones, assets y recursos audiovisuales de packs cuando corresponda.
- **F15 — QA:** carga, compatibilidad, ramificaciones, guardado/carga, migración, seguridad y narración sin contradicciones.

La planificación oficial se hará al llegar a los pasos que correspondan. No introducir contenidos de temporadas dentro de `v0.0.1 Sensores` por el solo hecho de aprobar IDEA-0006.

## 14. Pruebas de aceptación propuestas (no ejecutadas)

1. Un pack científico autorizado puede ser importado en una instalación compatible y rechazado de forma comprensible en otra incompatible.
2. Una nave sin capacidad o habilitación necesaria **no recibe** la misión aunque la temporada esté instalada.
3. Una misión recibida llega por la cadena de mando y genera tareas relevantes para el puesto real del jugador.
4. Las misiones de una temporada contribuyen causalmente a su objetivo central y no contradicen pistas/resultados anteriores.
5. Es posible vivir **periodos amplios sin episodios de temporada activos** mientras guardias, NPC y mundo siguen evolucionando.
6. Las misiones emergentes pueden coexistir; las urgencias no desaparecen porque la temporada esté en marcha.
7. Una misión fallida, una decisión alternativa o una transferencia de nave modifica el recorrido sin forzar un éxito inexistente.
8. Cada episodio respeta la diferencia entre verdad del mundo, información del mando y conocimiento del jugador.
9. Guardar/cargar mantiene estado de temporada, misiones, pistas y eventos; no duplica episodios ni hechos.
10. Importar una actualización del pack no reescribe resultados anteriores; rechazar un pack dañado no altera el mundo.
11. Un NPC puede resolver o afectar una trama fuera de escena si la simulación y sus capacidades lo justifican.
12. Una temporada nueva que emplea únicamente acciones y recursos ya soportados puede instalarse sin recompilar la build; las funcionalidades inéditas se señalan como dependencias nuevas.

## 15. Documentación existente a reutilizar

- [Buzón de ideas](BUZON.md).
- [Plan Maestro](../docs/roadmap/master/PLAN_MAESTRO.md).
- [Continuidad de campaña](../docs/decisions/campaign_continuity.md).
- [Estado de misión](../../sistemas/gameplay/command/mission_state.json).
- [Estado de objetivos](../../sistemas/gameplay/command/mission_objective_state.json).
- [Participación por rol](../../sistemas/gameplay/command/mission_participation_by_role.json).
- [Briefings](../../sistemas/gameplay/command/mission_briefing_model.json).
- [Órdenes del Mando de la Flota](../../sistemas/gameplay/orders/starfleet_mission_tasking_order.json).
- [Necesidades operativas](../../sistemas/gameplay/command/operational_need_model.json).
- [Misiones emergentes desde World State](../../sistemas/gameplay/missions/emergent_mission_from_world_state_contract.json).
- [Restricciones del director IA](../../sistemas/ai/director/operational_need_guardrails.md).
- [Viabilidad logística](../../sistemas/gameplay/logistics/mission_feasibility_model.json).
- [Tareas de servicio por misión](../../sistemas/gameplay/duty_system/mission_duty_task_model.json).
- [Acceso a información de misión](../../sistemas/gameplay/knowledge/mission_information_access.json).
- [F11 — Carrera y flota](../docs/roadmap/master/fases/F11/README.md).
- [F13 — Universo dinámico y misiones](../docs/roadmap/master/fases/F13/README.md).

## 16. Decisión y estado final

**APROBADO por el autor el 2026-10-13:** temporadas narrativas compuestas de episodios/misiones coherentes y conectados, adecuación por nave/destino/rol, encargos oficiales por el Mando, intervalos libres de vida a bordo, desarrollo de temporadas fuera del juego y carga como paquetes estructurados, ramificación basada en consecuencias, coexistencia con misiones emergentes y continuidad entre destinos.

**PENDIENTE de diseño formal:** esquema y formato versionado definitivo de los Season Packs, mecanismo de activación e introducción legítima de premisas argumentales en el World State, validación, infraestructura de mods/contenido, migración de partidas, UX, primera temporada completa y pruebas de integración.

**No implementado.** Este archivo documenta una decisión creativa, **no declara que existan cargadores funcionales, temporadas terminadas ni Core/UE5 integrado**. No altera las fases actualmente en desarrollo.
