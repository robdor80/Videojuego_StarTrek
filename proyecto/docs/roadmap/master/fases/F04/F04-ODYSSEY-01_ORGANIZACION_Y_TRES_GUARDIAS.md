# F04-ODYSSEY-01 — Organización de 1.600 tripulantes y tres guardias

**F04 EN_CURSO. Draft para auditoría independiente, sin fusionar.** Base exacta `c6bfcd7619c442d72afe06c21ee65c1e637f3cb2` (PR #69 y #70 fusionadas). Rama `codex/f04-odyssey-1600-tres-guardias`. Worktree `C:/F04/Odyssey01`; laboratorio `C:/F04/OdysseyBuild`.

## Perfil, cronología y autoridad

`F04_ODYSSEY_MULTIMISSION=4` amplía el registro existente: Miranda=1, Intrepid=2 y Sovereign=3 conservan sus IDs, tablas y funciones. Odyssey es una nave capital de exploración, mando estratégico, diplomacia, investigación y larga duración. Su dotación nominal tiene 1.600 plazas de Flota, siete departamentos y 72 secciones; cero civiles residentes nominales. No es un límite de capacidad física ni una creación automática de naves.

La [decisión aprobada](../../../../decisions/odyssey_valhalla_program_2383_2387_quantum_slipstream.md) y el catálogo vigente sitúan a la clase Odyssey operativa y como punta de lanza en 2383: **GAME_ADDITION**, sin fecha exacta de botadura de un casco ni Enterprise-F automática. Programa Valhalla tras Nemesis en 2379; construcción/desarrollo desde 2380; primera entrada objetivo en 2387. No se modifica esta cronología ni se implementa Valhalla. El perfil registra su época; no crea un motor de calendario alternativo ni desencadena acontecimientos futuros.

CoreRPG conserva todas las personas, plazas, agendas, nombramientos, suplencias, carencias y reloj. La plantilla es definición inmutable de contenido y las consultas son proyecciones. Core F04 permanece en `c147d81ed069da2e09149613ab02cbc3ebe95a4a`, sin modificaciones. No se crean 1.600 Actors: Unreal materializa únicamente las identidades solicitadas.

## Dotación nominal y día de referencia

La fixture completa se crea explícitamente sobre 1.600 personas Core distintas, sin nombres, matrículas, rangos, especies ni biografías inventadas. La clave permanente de plaza es nave / perfil / sección×100+ordinal. El [listado de las 1.600 plazas](F04-ODYSSEY-01_PLANTILLA_1600.md) y [snapshot consultado](evidence/F04-ODYSSEY-01/reference-snapshot.json) contienen cada identidad y asignación. No hay duplicaciones ni personas generadas por el planificador.

| Departamento | Secciones | Total | Alpha | Beta | Gamma | Fuera |
|---|---:|---:|---:|---:|---:|---:|
| Mando y navegación | 10 | 110 | 35 | 22 | 13 | 40 |
| Ingeniería y mantenimiento | 12 | 365 | 117 | 77 | 46 | 125 |
| Ciencias y sensores | 12 | 320 | 109 | 62 | 35 | 114 |
| Operaciones y comunicaciones | 12 | 275 | 85 | 60 | 40 | 90 |
| Seguridad y táctica | 10 | 245 | 65 | 58 | 39 | 83 |
| Lanzaderas y logística | 8 | 185 | 58 | 31 | 17 | 79 |
| Medicina | 8 | 100 | 31 | 20 | 15 | 34 |
| **Total** | **72** | **1600** | **500** | **330** | **205** | **565** |

Las cuatro categorías describen un día exacto, no un patrón semanal repetido. Fuera significa sin servicio ordinario programado ese día; no equivale a baja, vacaciones ni descanso protegido registrado. Estas restricciones se consultan y persisten por separado.

## Las 72 secciones aprobadas

| ID | Departamento | Sección | Total | Alpha | Beta | Gamma | Fuera |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | Mando y navegación | Capitán | 1 | 1 | 0 | 0 | 0 |
| 2 | Mando y navegación | Primer oficial | 1 | 1 | 0 | 0 | 0 |
| 3 | Mando y navegación | Segundo oficial y oficiales de guardia | 16 | 4 | 4 | 3 | 5 |
| 4 | Mando y navegación | Timón y navegación | 22 | 6 | 5 | 4 | 7 |
| 5 | Mando y navegación | Planificación estratégica y misiones | 12 | 5 | 2 | 1 | 4 |
| 6 | Mando y navegación | Enlace y coordinación con Flota | 12 | 4 | 3 | 1 | 4 |
| 7 | Mando y navegación | Diplomacia y protocolo | 12 | 5 | 2 | 0 | 5 |
| 8 | Mando y navegación | Coordinación de expediciones | 10 | 3 | 2 | 1 | 4 |
| 9 | Mando y navegación | Registros y planificación de misiones | 10 | 3 | 2 | 1 | 4 |
| 10 | Mando y navegación | Supervisión de seguridad operacional | 14 | 3 | 2 | 2 | 7 |
| 11 | Ingeniería y mantenimiento | Jefatura y adjuntos | 7 | 2 | 1 | 0 | 4 |
| 12 | Ingeniería y mantenimiento | Propulsión warp | 62 | 18 | 13 | 9 | 22 |
| 13 | Ingeniería y mantenimiento | Impulso y maniobra | 32 | 10 | 7 | 4 | 11 |
| 14 | Ingeniería y mantenimiento | Núcleo warp y antimateria | 45 | 14 | 10 | 6 | 15 |
| 15 | Ingeniería y mantenimiento | Distribución EPS | 45 | 14 | 10 | 5 | 16 |
| 16 | Ingeniería y mantenimiento | Integridad estructural y generadores de escudos | 35 | 11 | 7 | 5 | 12 |
| 17 | Ingeniería y mantenimiento | Soporte vital y control ambiental | 32 | 10 | 7 | 4 | 11 |
| 18 | Ingeniería y mantenimiento | Hardware y núcleos de ordenador | 29 | 9 | 6 | 4 | 10 |
| 19 | Ingeniería y mantenimiento | Deflectores, tractores y emisores | 24 | 8 | 5 | 3 | 8 |
| 20 | Ingeniería y mantenimiento | Mantenimiento y reparaciones | 30 | 12 | 6 | 3 | 9 |
| 21 | Ingeniería y mantenimiento | Control técnico de daños | 14 | 5 | 3 | 2 | 4 |
| 22 | Ingeniería y mantenimiento | Inspecciones y control de calidad | 10 | 4 | 2 | 1 | 3 |
| 23 | Ciencias y sensores | Jefatura científica y adjuntos | 6 | 2 | 1 | 0 | 3 |
| 24 | Ciencias y sensores | Sensores y astrometría | 48 | 15 | 10 | 8 | 15 |
| 25 | Ciencias y sensores | Física y astrofísica | 32 | 11 | 6 | 3 | 12 |
| 26 | Ciencias y sensores | Biología y xenobiología | 32 | 11 | 6 | 2 | 13 |
| 27 | Ciencias y sensores | Geología y planetología | 28 | 10 | 5 | 2 | 11 |
| 28 | Ciencias y sensores | Xenolingüística y antropología | 25 | 10 | 4 | 1 | 10 |
| 29 | Ciencias y sensores | Laboratorios y muestras | 35 | 12 | 7 | 3 | 13 |
| 30 | Ciencias y sensores | Exploración planetaria | 30 | 10 | 6 | 4 | 10 |
| 31 | Ciencias y sensores | Cartografía y expediciones | 28 | 9 | 6 | 3 | 10 |
| 32 | Ciencias y sensores | Análisis de datos científicos | 24 | 8 | 5 | 4 | 7 |
| 33 | Ciencias y sensores | Fenómenos espaciales exóticos | 16 | 6 | 3 | 2 | 5 |
| 34 | Ciencias y sensores | Ecología y ciencias medioambientales | 16 | 5 | 3 | 3 | 5 |
| 35 | Operaciones y comunicaciones | Jefatura y adjuntos | 6 | 2 | 1 | 1 | 2 |
| 36 | Operaciones y comunicaciones | Comunicaciones | 38 | 10 | 10 | 6 | 12 |
| 37 | Operaciones y comunicaciones | Transportadores | 35 | 10 | 8 | 5 | 12 |
| 38 | Operaciones y comunicaciones | Operaciones del puente | 26 | 8 | 5 | 4 | 9 |
| 39 | Operaciones y comunicaciones | Ordenadores y software | 35 | 12 | 7 | 4 | 12 |
| 40 | Operaciones y comunicaciones | Gestión de recursos | 28 | 10 | 6 | 3 | 9 |
| 41 | Operaciones y comunicaciones | Servicios y circulación interna | 25 | 7 | 6 | 4 | 8 |
| 42 | Operaciones y comunicaciones | Holocubiertas y recreación | 18 | 7 | 3 | 2 | 6 |
| 43 | Operaciones y comunicaciones | Enlaces protegidos y cifrado | 17 | 5 | 4 | 3 | 5 |
| 44 | Operaciones y comunicaciones | Sistemas auxiliares y redes internas | 20 | 6 | 5 | 3 | 6 |
| 45 | Operaciones y comunicaciones | Distribución automatizada | 15 | 5 | 3 | 2 | 5 |
| 46 | Operaciones y comunicaciones | Planificación de servicios | 12 | 3 | 2 | 3 | 4 |
| 47 | Seguridad y táctica | Jefatura y adjuntos | 6 | 2 | 1 | 0 | 3 |
| 48 | Seguridad y táctica | Táctica del puente | 36 | 10 | 8 | 6 | 12 |
| 49 | Seguridad y táctica | Armas y municiones | 35 | 9 | 8 | 6 | 12 |
| 50 | Seguridad y táctica | Escudos y contramedidas | 28 | 7 | 7 | 5 | 9 |
| 51 | Seguridad y táctica | Seguridad interior y patrullas | 55 | 13 | 14 | 10 | 18 |
| 52 | Seguridad y táctica | Accesos y custodia | 24 | 7 | 6 | 4 | 7 |
| 53 | Seguridad y táctica | Intervención y abordajes | 22 | 7 | 5 | 3 | 7 |
| 54 | Seguridad y táctica | Protección de misiones exteriores | 16 | 4 | 4 | 2 | 6 |
| 55 | Seguridad y táctica | Investigación de seguridad | 12 | 4 | 2 | 1 | 5 |
| 56 | Seguridad y táctica | Respuesta de emergencia y contención | 11 | 2 | 3 | 2 | 4 |
| 57 | Lanzaderas y logística | Jefatura y adjuntos | 5 | 2 | 1 | 0 | 2 |
| 58 | Lanzaderas y logística | Pilotos de lanzaderas | 32 | 10 | 7 | 4 | 11 |
| 59 | Lanzaderas y logística | Operación de hangares | 30 | 9 | 5 | 2 | 14 |
| 60 | Lanzaderas y logística | Mantenimiento de naves auxiliares | 31 | 10 | 5 | 3 | 13 |
| 61 | Lanzaderas y logística | Almacenes e inventarios | 32 | 10 | 5 | 3 | 14 |
| 62 | Lanzaderas y logística | Aprovisionamiento y reciclaje | 21 | 7 | 3 | 1 | 10 |
| 63 | Lanzaderas y logística | Apoyo logístico a expediciones | 19 | 6 | 3 | 2 | 8 |
| 64 | Lanzaderas y logística | Transportes especiales | 15 | 4 | 2 | 2 | 7 |
| 65 | Medicina | Jefatura médica | 4 | 1 | 1 | 0 | 2 |
| 66 | Medicina | Médicos y urgencias | 20 | 6 | 4 | 4 | 6 |
| 67 | Medicina | Enfermería | 32 | 10 | 7 | 5 | 10 |
| 68 | Medicina | Cirugía y traumatología | 12 | 5 | 2 | 1 | 4 |
| 69 | Medicina | Diagnóstico y biocontención | 10 | 3 | 2 | 2 | 3 |
| 70 | Medicina | Psicología y asesoramiento | 8 | 2 | 2 | 1 | 3 |
| 71 | Medicina | Medicina preventiva y exobiología | 6 | 2 | 1 | 1 | 2 |
| 72 | Medicina | Equipos de respuesta sanitaria | 8 | 2 | 1 | 1 | 4 |

## Guardias, descansos y cadena de mando

Gamma 00:00–08:00, Alpha 08:00–16:00, Beta 16:00–24:00; intervalos semiabiertos en segundos Core. Se reutiliza `plan_watches`, sin otro planificador. Un plan de referencia dura un día. Los planes rotatorios de 1–28 días pueden comenzar con ese día exacto y continúan con selección determinista, rotación semanal de preferencia y reserva de personal habilitado para servicios críticos.

Se aplican máximo cinco guardias ordinarias en cualquier ventana móvil de 168 horas, una por día natural y al menos 12 horas de separación. Se respetan ausencias, descanso protegido, deuda extraordinaria, credenciales y nombramientos vigentes durante la ventana. No se cambian cupos ni reglas para ocultar carencias. Los cupos multisemana son objetivos por departamento; la selección no garantiza los subtotales de cada sección fuera del día de referencia ni demuestra un óptimo global de cobertura no crítica.

Un capitán titular, un primer oficial titular y una persona explícita como segundo oficial (sección 3, ordinal 1). Los otros oficiales pueden ejercer WATCH temporal por ventana cuando estén habilitados. El capitán y el primero descansan y se relevan legítimamente. Los jefes y adjuntos no obtienen mando general por rango; enlace con Flota, diplomacia y supervisión de seguridad operacional tampoco. La supervisión de riesgos no sustituye a Seguridad y Táctica. Mantenimiento de escudos no autoriza empleo táctico ni se añade permiso de armas por ocupar una consola.

El responsable técnico de cada guardia recibe DUTY_HEAD temporal; no exige que el jefe permanente trabaje 24 horas. Medicina mantiene respuesta clínica/enfermería presencial en todas las guardias. COVER_DUTY propone y confirma una persona real habilitada, conserva su plaza nominal y registra origen, intervalo y causa. TRANSFER mantiene su carácter de cambio permanente explícito. Las movilizaciones y ausencias modifican la cobertura real, con historial de carencias aunque una sustitución las resuelva.

## Simulaciones y déficits observados

| Días | Turnos reales | Objetivo | Déficit no crítico | Ventanas críticas verificadas | Máximo móvil 7 días | Mínimo entre turnos | Personas que cambian guardia | Turnos capitán |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1035 | 1035 | 0 | 24/24 | 1 | — | 0 | 1 |
| 7 | 7171 | 7245 | 74 | 168/168 | 5 | 16 h | 1267 | 5 |
| 14 | 14388 | 14490 | 102 | 336/336 | 5 | 16 h | 1535 | 10 |
| 28 | 28459 | 28980 | 521 | 672/672 | 5 | 16 h | 1598 | 19 |

Ocho servicios independientes: mando del puente, timón, sensores, operaciones, comunicaciones, ingeniería, táctica/seguridad y respuesta médica. Cada ventana se comprueba completa, incluyendo límites internos de actividades, nombramientos, bajas y vencimiento de credenciales. Las cifras de cobertura corresponden a la fixture completa sin incidencias. La retirada de las 54 personas habilitadas para sensores (secciones 23 y 24) registra las 21 ventanas críticas imposibles de siete días, sin personal ficticio.

| Departamento | Déficit 7 días | Déficit 14 días | Déficit 28 días |
|---|---:|---:|---:|
| Mando y navegación | 7 | 13 | 48 |
| Ingeniería y mantenimiento | 13 | 13 | 115 |
| Ciencias y sensores | 3 | 3 | 58 |
| Operaciones y comunicaciones | 32 | 44 | 156 |
| Seguridad y táctica | 10 | 15 | 92 |
| Lanzaderas y logística | 0 | 0 | 0 |
| Medicina | 9 | 14 | 52 |

[Cuadrante completo de 28 días](evidence/F04-ODYSSEY-01/roster-28-days.csv), [recuentos diarios](evidence/F04-ODYSSEY-01/daily-counts-28-days.json), [carencias históricas](evidence/F04-ODYSSEY-01/gaps-28-days.json) y [resumen](evidence/F04-ODYSSEY-01/simulations.json). En 28 días hay 16.341 persona-días sin guardia ordinaria. El plan es finito: debe ampliarse con autoridad antes de su fin. La cobertura no se promete después del horizonte ni ante bajas arbitrarias.

## Compatibilidad, persistencia y límites

ABI 1 intacta; se añade únicamente el ID 4 al registro. Instalar la organización usa SCHEMA 3; la planificación de tres guardias migra explícitamente a SCHEMA 4. Se leen SCHEMA 1, 2, 3 y 4 y guardados de las tres clases anteriores. SCHEMA 4 rechaza mezclar el planificador Alpha heredado. La continuación por ventanas, la ejecución en procesos distintos, los handles renovados y el rechazo atómico de corrupción de checksum y campos están probados.

La única adaptación compartida de validación sustituye el techo específico de 700 de una carencia por la dotación nominal del perfil. No cambia el límite de entidades, tamaño de archivo, formatos Core ni reglas de descanso. La ABI ya ofrece consultas paginadas para personas, plazas, deberes, carencias y candidatos.

En 28 días se observan **32.647 entidades** de las 65.536 permitidas por el esquema F04 y **10.157.613 bytes** de los 67.108.864 permitidos por el cargador. Core aplica además sus límites de un millón de relaciones/registros de persistencia. El ensayo acumulado conserva 56 días con 61.919 entidades, 56.764 turnos y 19.364.456 bytes; un tercer bloque hasta el día 84 devuelve CAPACITY sin publicar deberes parciales. No hay compactación ilimitada de historial: una campaña larga necesita una futura política de retención/archivo antes de agotar ese techo. No se elevan límites silenciosamente.

El planificador usa índices descartables por persona y tipo, ligados a la revisión Core. La selección ordena candidatos por guardia y departamento; las comprobaciones de descanso recorren el historial individual y el guardado/carga recorre el estado acumulado. La validación y el historial crecen con el tiempo; no se afirma coste constante ni un benchmark de flota completa. En el horizonte solicitado no se observa un bloqueo que exija cambiar Core.

## Rendimiento local MSI

Medidas puntuales de pared con MSVC Release, sin percentiles ni garantía de latencia. Crear incluye personas, plazas y bootstrap de destinos/cualificaciones. Los tres costes se desglosan en [performance.json](evidence/F04-ODYSSEY-01/performance.json); la mayor parte de creación corresponde a asignar la fixture, no a crear identidades.

| Días | Crear total ms | Manifiesto ms | Plan ms | Cobertura ms | Guardar ms | Cargar ms | Avanzar ms | Archivo bytes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 630.13 | 1.09 | 21.22 | 1.00 | 50.06 | 39.27 | 16.58 | 1252261 |
| 7 | 655.53 | 0.88 | 119.01 | 4.96 | 111.34 | 97.32 | 95.27 | 3244020 |
| 14 | 632.34 | 0.87 | 335.73 | 12.69 | 196.43 | 216.10 | 414.56 | 5585553 |
| 28 | 233.11 | 0.90 | 849.77 | 43.62 | 394.77 | 442.70 | 1256.66 | 10157613 |

El ensayo de enfermedad de un operador tras cargar tarda 21.34 ms; buscar 18 candidatos reales, 1.84 ms; confirmar sustitución legítima, 27.06 ms. Restaura cobertura, conserva 1.600 personas y mantiene el historial de la carencia: [medición](evidence/F04-ODYSSEY-01/incident-performance.json). Es una medición al final de una guardia; las pruebas nativas también cubren sustitución completa y baja interior de ventana.

## Instalaciones y programa experimental

El [contrato de instalaciones](../../../../../../desarrollo/integration/f04/tests/fixtures/odyssey_facilities_contract.json) reutiliza Intrepid/Sovereign: cantidades, capacidades, holocubiertas y equipos médicos dependen del casco. Mismas reglas futuras para NPC y jugador, con Timeline avanzando. Sin reservas ejecutables, entrenamiento, minijuegos ni 3D. EMH es opcional y no cuenta como una de las 100 plazas médicas. Aquarius no se instala por defecto ni crea personas al desplegarse; requiere destinos reales autorizados o futura dotación adicional aprobada. No se fija cantidad de lanzaderas.

El [contrato organizativo experimental](../../../../../../desarrollo/integration/f04/tests/fixtures/odyssey_experimental_program_contract.json) referencia el contrato tecnológico aprobado. Identifica potenciales especialistas de Ingeniería (11,12,14,15,19,21,22), Ciencias (23,24,25,32,33), Navegación (4) y Mando (1,2,3,5,10). Exige cualificación, destino/comisión temporal, autorización y preservación de servicios y descansos. No añade departamento 8 ni sección 73.

Warp convencional permanece operativo. Flujo cuántico solo puede probarse desde 2383 en cascos experimentales expresamente designados; un prototipo no acredita homologación ni fiabilidad. El contrato no instala motores, implementa propulsión, corredores, misiones o resultados futuros. Valhalla 2387 no tiene flujo cuántico garantizado. Flujo cuántico y torpedos cuánticos son distintos. La configuración/estado real futuro sigue bajo CoreRPG; el jugador no está obligado a participar.

## Pruebas y protección

Las [evidencias reproducibles](evidence/F04-ODYSSEY-01/RESULTADOS.md) incluyen organización, referencia exacta, 1/7/14/28 días, descansos, nombramientos, ausencia del capitán/primero, enfermedad, vacaciones, relevo técnico, caducidad, traslado, cancelación, falta total de especialistas, recuperación legítima, persistencia y regresiones.

No se modifican CoreRPG, pins F02/F03, decisiones PR #69, recursos artísticos, Blender, modelos, puentes, materiales, mapas, Valhalla, separación ni copias de seguridad. El inventario externo comprueba rutas, tamaños y mtimes del repositorio principal; no es una auditoría criptográfica del contenido completo. Ninguna PR se fusiona y F04 permanece EN_CURSO.
