# F04 — auditoría y arquitectura mínima previa a implementación

Base Trek `c8109216b1467e89e08f7d2d330256e3f0e80559`; Core `c147d81ed069da2e09149613ab02cbc3ebe95a4a`.
Fetch confirmado el 30-10-2026: ninguna base posterior. La referencia F03
`9c53a33787de13d91eb2abe4da07033ee0fa1dc1` permanece reproducible e intacta.

| Capacidad | Clasificación | Resolución mínima |
| --- | --- | --- |
| Identidad, población y pertenencia | REUTILIZABLE | WorldState, materialize_population, relaciones y contención |
| Catálogo y clase | ADAPTACIÓN NECESARIA | Proyección compilada del catálogo JSON existente, sin imponer crew_reference |
| Plazas, manifiesto y cualificaciones | NUEVA CAPACIDAD TREK | Entidades tipadas y relaciones persistentes en WorldState |
| Tiempo y archivo | REUTILIZABLE | Timeline y CampaignPersistence F03, sin cambiar formato |
| Intervalos y cobertura | NUEVA CAPACIDAD TREK | Evaluación [inicio,fin) sobre registros persistentes y reloj Core |
| Nombramientos, delegación y sucesión | NUEVA CAPACIDAD TREK | Reglas de dominio; ninguna autoridad derivada solo del rango |
| Seguridad, aptitud y revisión contextual | ADAPTACIÓN NECESARIA | Contratos existentes convertidos en controles previos a ActionEngine |
| Validadores F04 y Miranda-120 | REUTILIZABLE | Mantener referencia separada de pruebas nativas |
| Actors y UWorld | ADAPTACIÓN NECESARIA | Laboratorio independiente basado en metodología F02/F03 |
| Extensión genérica Core | REUTILIZABLE | No se necesita una nueva API ni PR Core |

Fuentes auditadas: los seis documentos P01–P05/Miranda, contratos de
ship_operations, duty_system, chain_of_command, characters y orders;
generación persistente, catálogo de clases, cualificaciones, sucesión,
aptitud médica y Primera Directriz. Los generadores Python y f04_reference
son referencias: no se importan como autoridad runtime. La muestra de
120 efectivos sigue siendo aritmética e ilustrativa.

## Propiedad y esquema

Core posee **todo** el estado mutable persistente: entidades, definiciones,
relaciones, población, reloj, RNG y archivo. El adaptador Trek no mantiene
otro manifiesto ni mapas mutables de permisos. Sus consultas reconstruyen
proyecciones desde el grafo Core. Las entidades representan nave, personas,
plazas, actividades, nombramientos, delegaciones, restricciones, operaciones
pendientes y registros causales. RelationKind es una etiqueta opaca asignada
por contenido: Trek reserva un espacio versionado para campos de referencia
y campos escalares acotados a 48 bits (campo + valor, relación consigo mismo).
Este convenio pertenece a Trek; Core no interpreta rangos ni guardias.
El lector rechaza etiquetas desconocidas, duplicados y referencias inválidas.

El reloj autoritativo es Timeline; las tareas Trek pendientes son entidades
del mismo WorldState. El host avanza Timeline hasta cada vencimiento, vuelve
a autorizar la tarea con el estado contemporáneo y registra su resultado.
No se encolan acciones privilegiadas con permisos congelados en Timeline.
El hilo propietario serializa accesos; cada petición prepara una copia de la
campaña y publica por swap tras validar. ActionEngine aplica las relaciones.
Las denegaciones de dominio se registran como eventos, sin ejecutar el efecto.
Los límites de memoria/validación conservan la campaña anterior.

## Frontera host y alcance

La ABI es un laboratorio nativo confiable, no un protocolo de autenticación
remota. Handles de sesión invalidan vínculos tras carga. Unreal representa
proyecciones autorizadas y remite intenciones; IA solo puede proponer.
El bootstrap es un escenario sintético pequeño, identificado como prueba,
con personas individualizadas explícitamente; nunca genera reemplazos para
una vacante. No fija canon de Sutherland ni dotación universal Miranda.
No incluye iniciativa NPC ni el sistema completo de órdenes F05, simulación
clínica, desplazamiento por interiores o planificación óptima de toda la flota.
No se modifica ESTADO_GLOBAL ni se declara cierre administrativo.
