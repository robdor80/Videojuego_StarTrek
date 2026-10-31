# F04-MIRANDA-01 — Organización de la USS Sutherland

> Actualización 31-10-2026: [F04-GUARDIAS-02](F04-GUARDIAS-02_MIRANDA_INTREPID_TRES_GUARDIAS.md) completa Beta/Gamma con el planificador común y migración explícita SCHEMA 3→4. Las cifras y contratos históricos siguientes conservan su alcance original.

Fecha: 2026-10-30. Estado F04: **EN_CURSO**. Entrega para auditoría mediante PR Draft, sin fusión.

La configuración científica polivalente modernizada de la USS Sutherland dispone de **130 plazas nominales**, distribuidas en **siete departamentos y 32 secciones**. Su Alpha ilustrativa de 08:00 a 16:00 emplea **53 personas distintas**. El perfil se instala explícitamente; crear una Miranda genérica o cualquier otra clase conserva la dotación genérica de la PR #66 y no aplica esta organización.

Clase Miranda, Flota nominal 130, civiles residentes nominales 0. La matrícula está pendiente del autor. Los tipos exactos de equipamiento, cantidad de lanzaderas, capacidad máxima de pasajeros y época concreta no se fijan en este corte. `ship_identity=65001` en las pruebas es un identificador sintético de campaña, nunca una matrícula.

**La distribución por rangos de la tripulación todavía será definida por el autor.** La plantilla y la fixture no inventan nombres, especies, biografías ni rangos; mantienen `rank=0` en el bootstrap general.

## Organización aprobada

Los números departamentales del diseño no se usan para renumerar la ABI: Sensores/Ciencias=1, Ingeniería=2, Mando=3 y Medicina=4 se conservan. Operaciones=5, Seguridad=6 y Logística=7 son adiciones.

| Departamento | Plazas | Alpha |
|---|---:|---:|
| Mando y navegación | 12 | 6 |
| Ingeniería y mantenimiento | 32 | 11 |
| Ciencias y sensores | 30 | 14 |
| Operaciones y comunicaciones | 18 | 6 |
| Seguridad y táctica | 16 | 5 |
| Lanzaderas y logística | 12 | 6 |
| Medicina | 10 | 5 |
| **Total** | **130** | **53** |

| Sección | Departamento (ABI) | Total | Alpha | Responsabilidades y equipamiento |
|---|---|---:|---:|---|
| 1. Capitán | Mando y navegación (3) | 1 | 1 | Mando de la nave. Equipamiento: Puente. |
| 2. Primer oficial | Mando y navegación (3) | 1 | 1 | Segundo al mando; coordinación operativa y supervisión departamental. Equipamiento: Puente. |
| 3. Oficiales de guardia y mando | Mando y navegación (3) | 3 | 1 | Supervisión rutinaria; relevos y mando delegado. Equipamiento: Puente. |
| 4. Timón y navegación | Mando y navegación (3) | 5 | 2 | Pilotaje de nave principal y navegación. Equipamiento: Timón del puente. |
| 5. Coordinación de misiones | Mando y navegación (3) | 2 | 1 | Planificación y seguimiento operativo. Equipamiento: Puente y comunicaciones. |
| 6. Jefe de ingeniería y adjunto | Ingeniería y mantenimiento (2) | 2 | 1 | Dirección técnica y prioridades de mantenimiento. Equipamiento: Ingeniería. |
| 7. Motores warp e impulso | Ingeniería y mantenimiento (2) | 8 | 3 | Mantenimiento de propulsión. Equipamiento: Propulsión warp e impulso. |
| 8. Reactor y distribución de energía | Ingeniería y mantenimiento (2) | 6 | 2 | Generación y distribución de energía. Equipamiento: Reactor y red energética. |
| 9. Soporte vital e integridad estructural | Ingeniería y mantenimiento (2) | 7 | 2 | Sistemas ambientales y estructurales. Equipamiento: Soporte vital y estructura. |
| 10. Reparaciones y mantenimiento general | Ingeniería y mantenimiento (2) | 9 | 3 | Reparación técnica de sistemas de otros departamentos, sin asumir su operación. Equipamiento: Equipamiento instalado. |
| 11. Jefe científico y adjunto | Ciencias y sensores (1) | 2 | 1 | Dirección científica. Equipamiento: Sensores modernizados y laboratorios polivalentes. |
| 12. Sensores y astrometría | Ciencias y sensores (1) | 8 | 3 | Operación y análisis de sensores; astrometría. Equipamiento: Sensores modernizados. |
| 13. Física y astrofísica | Ciencias y sensores (1) | 6 | 3 | Investigación física y astronómica. Equipamiento: Laboratorios polivalentes. |
| 14. Biología y xenobiología | Ciencias y sensores (1) | 5 | 2 | Estudios biológicos. Equipamiento: Laboratorios polivalentes. |
| 15. Geología y planetología | Ciencias y sensores (1) | 4 | 2 | Estudios geológicos y planetarios. Equipamiento: Laboratorios polivalentes. |
| 16. Laboratorios y análisis de muestras | Ciencias y sensores (1) | 5 | 3 | Análisis instrumental y de muestras. Equipamiento: Laboratorios polivalentes. |
| 17. Jefe de operaciones y adjunto | Operaciones y comunicaciones (5) | 2 | 1 | Coordinación operativa. Equipamiento: Comunicaciones, transportadores y sistemas informáticos. |
| 18. Comunicaciones | Operaciones y comunicaciones (5) | 5 | 2 | Operación de comunicaciones. Equipamiento: Sistemas de comunicaciones. |
| 19. Transportadores | Operaciones y comunicaciones (5) | 5 | 1 | Operación; reparación técnica a cargo de personal habilitado de mantenimiento. Equipamiento: Transportadores. |
| 20. Sistemas informáticos y recursos | Operaciones y comunicaciones (5) | 6 | 2 | Sistemas informáticos y asignación de recursos. Equipamiento: Sistemas informáticos. |
| 21. Jefe de seguridad y adjunto | Seguridad y táctica (6) | 2 | 1 | Dirección de seguridad y táctica; consola táctica si está habilitado. Equipamiento: Fáseres, torpedos, escudos y seguridad. |
| 22. Especialistas tácticos | Seguridad y táctica (6) | 5 | 1 | Operación táctica; apoyo o relevo del jefe de servicio. Equipamiento: Fáseres y torpedos en barra superior; escudos. |
| 23. Seguridad interior | Seguridad y táctica (6) | 6 | 2 | Protección interior. Equipamiento: Instalaciones de seguridad. |
| 24. Respuesta a emergencias y abordajes | Seguridad y táctica (6) | 3 | 1 | Intervención en emergencias y abordajes. Equipamiento: Instalaciones de seguridad. |
| 25. Jefe de sección | Lanzaderas y logística (7) | 1 | 1 | Coordinación de servicios auxiliares. Equipamiento: Hangares posteriores y almacenes. |
| 26. Pilotos de lanzaderas | Lanzaderas y logística (7) | 3 | 1 | Pilotaje de lanzaderas, distinto del pilotaje de nave principal. Equipamiento: Lanzaderas; número configurable. |
| 27. Hangares y mantenimiento | Lanzaderas y logística (7) | 4 | 2 | Preparación y mantenimiento de hangares y naves auxiliares. Equipamiento: Hangares posteriores y lanzaderas. |
| 28. Suministros, almacenes y carga | Lanzaderas y logística (7) | 4 | 2 | Inventarios, suministros y carga. Equipamiento: Almacenes y espacios habitables. |
| 29. Médico jefe | Medicina (4) | 1 | 1 | Dirección sanitaria; no mando general de la nave. Equipamiento: Enfermería. |
| 30. Médicos | Medicina (4) | 2 | 1 | Atención clínica. Equipamiento: Enfermería. |
| 31. Enfermería | Medicina (4) | 5 | 2 | Cuidados de enfermería. Equipamiento: Enfermería. |
| 32. Técnicos sanitarios y diagnóstico | Medicina (4) | 2 | 1 | Diagnóstico y asistencia técnica sanitaria. Equipamiento: Enfermería. |

La [plantilla completa](F04-MIRANDA-01_PLANTILLA_130.md) enumera las 130 plazas con identificador estable, departamento, sección, puesto, cualificaciones iniciales y selección Alpha. Jefes y adjuntos se distinguen por plaza y nombramiento. Las referencias a equipos no añaden instalaciones ni fijan modelos o capacidades no aprobadas.

## Arquitectura y autoridad de los datos

`desarrollo/integration/f04/src/f04_templates.h` contiene definiciones inmutables de perfil y secciones. Los selectores del perfil incluyen clase, configuración, equipamiento requerido, misión, época configurable, nominal y cobertura por sección. Solo se registra el perfil 1 de Sutherland. Otras clases conservan sus nominales aprobados y requieren distribuciones futuras propias; no se incluyen distribuciones Intrepid, Sovereign, Odyssey ni Valhalla.

La instancia operativa vive enteramente en **WorldState de CoreRPG**: nave → entidades departamento → entidades sección → entidades plaza → referencia PERSON → agendas y nombramientos. El módulo Trek interpreta esas relaciones y aplica sus reglas mediante ActionEngine; CampaignPersistence guarda el grafo completo, RNG y Timeline. Las copias transaccionales y los índices de consulta son temporales, sin otro almacén autoritativo de tripulantes.

Cada plaza tiene EntityId Core, clave estable `sección*100+ordinal` dentro de su perfil/nave, requisitos de cualificación, responsabilidad, referencias funcionales a estaciones/sistemas, condición de cobertura y selección Alpha. Su ocupante puede ser nulo. Se conserva la plaza cuando alguien sale, se traslada o cambia de guardia.

La ampliación aditiva mantiene ABI 1 y los tamaños de los tipos antiguos. Los tipos y funciones nuevos están en `f04_bridge.h`; no es necesario reinterpretar un F04Slot antiguo como F04Position. Las cualificaciones 1–4 conservan su sentido, se añaden los ámbitos 5–7 y especialidades 8–30. Los pilotos de nave principal y de lanzaderas tienen requisitos distintos; operación de transportadores no implica reparación general. Sensores y astrometría exige ambas competencias explícitas. El rango no interviene en esas comprobaciones.

## Instalación y operaciones

El host nativo autentica al actor y aporta revisión y evidencia (`cause`); no es una API de permisos abierta a NPC/IA. Todas estas mutaciones pasan por `f04_execute`, preparan una copia y se publican solo tras validar el esquema. Las denegaciones registran el motivo sin aplicar la intención.

| Intención nueva | Uso |
|---|---|
| INSTALL_TEMPLATE | `value=F04_SUTHERLAND_SCIENCE`, `aux=F04_SUTHERLAND_EQUIPMENT`. Comandante; población SCHEMA=2 de clase compatible y sin plazas previas. Migra explícitamente a esquema 3 y crea únicamente departamentos, secciones y plazas vacantes. |
| BOOTSTRAP_TEMPLATE | Fixture sintética explícita, una sola vez. Reutiliza hasta 130 miembros existentes, ordenados por ID, con el capitán existente primero; rechaza datos personales/competencias ya configurados. Asigna solo las competencias del puesto inicial, sin crear personas. Admite dotación parcial con vacantes reales. |
| CREDENTIAL | Comandante, persona existente, máscara explícita de cualificaciones y caducidad, causa documental. Certificaciones importadas por el host; no es simulación de formación F11. |
| TRANSFER | Comandante, plaza destino vacante y persona ya existente con competencias válidas. Cancela guardias y funciones anteriores, libera la plaza anterior y actualiza departamento; cancela nombramientos departamentales anteriores. Conserva identidad. |
| FUNCTION | Persona y plaza nominal ya asignadas, una estación compatible y ventana. Requiere guardia, habilitación y ámbito del comandante/jefe correspondiente. No crea una segunda plaza o persona ni concede mando. |
| PLAN_ALPHA | Ventana de un solo día `[08:00,16:00)`, patrón 3×8. Programa solo ocupantes válidos de las 53 plazas seleccionadas; omite vacantes o incompatibles y expone el déficit. `aux=1` permite nombrar WATCH al primer oficial; si no está disponible se considera al oficial de guardia programado. Programa la función táctica del jefe de seguridad habilitado. |

Estas operaciones devuelven un EntityId en `F04Result.record`, como la ABI existente: instalación, bootstrap y planificación devuelven la nave 1. Los recuentos se consultan por separado, no se codifican como identificadores de registro.

ASSIGN, DUTY, REST, ONCALL, ABSENCE, RELIEF, APPOINT, REVOKE, EMBARK y DEPART siguen usando las mismas entidades Core. ASSIGN conserva el departamento; TRANSFER permite cambiarlo explícitamente y valida cualificaciones. Una persona no puede ocupar dos plazas nominales. En un relevo se libera primero la plaza nominal del entrante; F04Position expone `duty_record` para relevar una actividad Alpha incluso si su ocupante está enfermo. Se conserva el déficit de la plaza que deja vacante el entrante.

La salida libera la plaza y cancela agendas, funciones y autoridad de la persona. EMBARK con su ID histórico reincorpora la misma identidad, sin restaurar nombramientos ni guardias canceladas. Los cambios de puesto no conceden automáticamente nuevos nombramientos. Reponer un jefe exige nombrarlo explícitamente.

Las consultas nuevas proyectan datos Core: `f04_organization_stats`, `f04_positions_page`, `f04_functions`, `f04_person_credentials`. `f04_template_spec` y `f04_template_sections` consultan únicamente las definiciones estáticas. La paginación permite dimensionar buffers, valida ámbitos y no modifica la campaña.

## Mando, puestos y funciones

Capitán, primer oficial, oficial de guardia, jefes, adjuntos y médico jefe conservan **nombramientos independientes** de sus plazas y de su rango. DEPUTY es un rol añadido por departamento; no hereda el mando general ni suplanta automáticamente a HEAD. El médico jefe posee autoridad sanitaria y gestión del propio servicio, sin mando de la nave.

La cadena existente selecciona capitán, primer oficial, segundo y sucesor según nombramientos, competencias y disponibilidad. WATCH es temporal y no sustituye permanentemente al capitán. En Alpha, primer oficial y WATCH pueden ser la misma persona; el oficial adicional de la sección de guardias permanece en tareas auxiliares o relevo sin otro nombramiento WATCH. El capitán sigue siendo una sola identidad aunque supervise operaciones.

El jefe de seguridad habilitado añade una relación FUNCTION táctica a su **misma plaza e identidad**. El especialista táctico Alpha queda como apoyo/relevo. La función se invalida operativamente con ausencia, falta de guardia, salida o pérdida de competencia y puede revocarse; no otorga política de guardias, mando del puente ni autorización de fuego. No se implementan órdenes ni disparos de F05. La autorización de operaciones sigue pasando por las reglas de mando existentes, nunca por ocupar una consola.

La guardia no equivale a presencia física ante una consola: los 53 trabajan en áreas distintas. Las referencias STATIONS son referencias funcionales de equipos; la ubicación diagnóstica y las proyecciones de Unreal se consultan aparte. FUNCTION solo representa una estación principal por persona y evita solapar ocupantes de la misma estación.

## Alpha, Beta, Gamma y déficits

La fixture completa demuestra 53 personas distintas en DUTY a tick 28800, cero déficit Alpha, 130 identidades y cero duplicados. Al llegar a tick 57600 se terminan esas actividades. Fuera de Alpha, `alpha_present`/`alpha_deficit` comparan las plazas de referencia con su servicio actual; no son una exigencia de repetir 53 personas en otros turnos. `vacant` significa plaza nominal sin ocupante; `on_duty` significa servicio efectivo. Los antiguos F04Stats.vacancies cuentan plazas no cubiertas de servicio y no deben confundirse con vacantes nominales.

No se etiqueta automáticamente como descanso a las otras 77 personas: están sin DUTY en ese instante. REST exige una actividad explícita. Ausencias, descansos protegidos, localización y presencia ante consola conservan su significado separado en Core.

La prueba `organization_beta_gamma` programa un ejemplo finito con las API operativas existentes:

| Servicio | Beta 16:00–24:00 (sección/ordinal) | Gamma siguiente 00:00–08:00 (sección/ordinal) |
|---|---|---|
| Guardia de puente, con nombramiento WATCH | 3/2 | 3/3 |
| Timón principal | 4/3 | 4/4 |
| Sensores | 12/4 | 12/5 |
| Comunicaciones/operaciones | 18/3 | 18/4 |
| Ingeniería de guardia | 6/2 | 7/4 |
| Seguridad/táctica | 22/2 | 22/3 |
| Respuesta sanitaria ilustrativa localizada | 30/2 | 30/2 |

Son seis trabajadores distintos por ventana y un médico localizado, sin duplicar identidades ni agendarlo como séptimo trabajador presencial. La continuidad se estudia por seis grupos funcionales, no exigiendo que toda plaza marcada como candidata tenga servicio continuo. Las actividades científicas, administrativas y logísticas de día no se convierten en turnos nocturnos obligatorios. La modalidad de urgencia sanitaria **sigue pendiente de validación**; esta es una posibilidad técnica de prueba.

`continuous_required=6` y `continuous_covered` reflejan la cobertura actual de esos grupos. `urgent_response=0/1/2` distingue ninguna respuesta, actividad sanitaria presencial o médico localizado. `coverage_validated=0` permanece siempre: ninguna consulta certifica descansos, vacaciones, reservas, equidad semanal ni cobertura garantizada 24/7. Al terminar el ejemplo a la mañana siguiente se registran cero trabajadores programados y seis grupos sin cobertura; no se inventa personal ni se prolongan horarios. Una ausencia reduce inmediatamente la cobertura real. Un relevo usa otra identidad existente y deja visibles las vacantes resultantes.

Se preservan las ventanas 3×8 y 4×6. Cambiar patrón conserva las comprobaciones previas y, para esta organización, exige cobertura real del siguiente ciclo para los seis grupos, comprobando límites de agendas, nombramientos y caducidad de credenciales. Eso sigue sin validar un régimen de descanso. PLAN_ALPHA exige 3×8 porque su ejemplo aprobado es 08:00–16:00; las actividades manuales siguen admitiendo otras ventanas.

## Persistencia y compatibilidad

CoreRPG sigue fijado, sin modificaciones, en `c147d81ed069da2e09149613ab02cbc3ebe95a4a`. SCHEMA es la versión del vocabulario de relaciones Trek, no un cambio al formato binario de Core:

- SCHEMA=1 conserva muestra histórica, identidades, ABI y agendas.
- SCHEMA=2 conserva dotación general de la PR #66 y sus cinco nominales.
- SCHEMA=3 añade el perfil instalado, equipos, departamentos, secciones, plazas enriquecidas y funciones. Solo se produce mediante instalación explícita.

Las referencias 1–7 y escalares 1–27 no se renumeran; se añaden referencias DEPARTMENT=8 y SECTION=9 y escalares 28–40. El cargador valida tipos, campos obligatorios, exclusividad de personas/roles/estaciones y la correspondencia exacta del perfil (claves, secciones, recuentos, competencias y condiciones). Rechaza grafos Core válidos pero incoherentes para Trek sin sustituir la campaña activa.

Los archivos de prueba históricos fueron producidos con la DLL anterior de PR #66, no reescritos por este código. Se guardan como hex textual en `tests/fixtures` con procedencia y SHA-256. Se demuestra carga/guardado idéntico byte a byte, migración explícita desde esquema 2, persistencia completa del esquema 3 y continuación determinista entre procesos separados.

## Validación y entrega

Los resultados y comandos reales de esta entrega se registran en [evidence/F04-MIRANDA-01/RESULTADOS.md](evidence/F04-MIRANDA-01/RESULTADOS.md). La suite nueva incluye totales exactos, vacantes, perfiles incompatibles, competencias, mando/medicina, primer oficial WATCH, jefe táctico, Alpha con bajas, relevos, traslados, reincorporación, descansos, corrupción semántica, archivos previos y recuperación entre procesos. Se ejecutan también todas las pruebas nativas F04 anteriores, F02/F03, Core con JSON, referencias documentales y roadmap.

Unreal 5.8.2 se compila y prueba en `C:/F04-Miranda01/ue`, fuera del repositorio y de los proyectos artísticos. El subsistema instala y consulta la organización Core; **no genera automáticamente 130 Actors**. La prueba nueva comprueba cero Actors tras el bootstrap/Alpha, materialización selectiva, primer oficial WATCH, denegación de mando al jefe táctico, persistencia y recuperación en otro UWorld. NullRHI acredita integración lógica y ciclo de Actors, **no jugabilidad gráfica completa**.

Permanecen pendientes la distribución por rangos, matrícula, detalles de equipos, validación de descanso/cobertura y modalidad sanitaria, UI de organización, simulación científica y clínica completas. La segunda silla del primer oficial queda como requisito futuro del puente artístico. No se modifican Blender, puente, materiales, texturas, mapas, activos Unreal, respaldos ni exclusiones locales. No se implementan F05, F11 ni F12 ni se cierra F04.
