# F04-VALHALLA-01 — La gran nave

**31-10-2026. Implementación para auditoría independiente. F04 permanece EN_CURSO.**
Base: `78fa53f99c384f4111f42d61d71fa2510b56f6b5` (PR #67–#73 integradas).
Rama: `codex/f04-valhalla-01-gran-nave-2200`. No cerrar F04 ni avanzar a GUARDIAS-02.

## Organización verificable

Perfil aditivo `F04_VALHALLA_FLAGSHIP=5`, ABI 1 y vocabulario Trek SCHEMA 3→4
al planificar. Miranda=1, Intrepid=2, Sovereign=3 y Odyssey=4 conservan sus
tablas. CoreRPG F04 sigue fijado en `c147d81ed069da2e09149613ab02cbc3ebe95a4a`,
sin cambios en su repositorio ni en sus formatos.

Se crean 1.800 personas de Flota y 400 residentes distintos en WorldState, con
1.800 plazas estables, siete departamentos y 90 secciones. Las cantidades y
las 90 filas proceden de la [plantilla aprobada](F04-VALHALLA-01_PLANTILLA_1800_Y_CIVILES_400.md).
El generador compila esa fuente; una prueba documental compara archivo generado,
fixture y autoridad. Las pruebas nativas contrastan cada fila con las consultas.

| Departamento | Plazas | Alpha | Beta | Gamma | Fuera |
|---|---:|---:|---:|---:|---:|
| Mando y navegación | 130 | 40 | 25 | 15 | 50 |
| Ingeniería y mantenimiento | 405 | 125 | 85 | 61 | 134 |
| Ciencias y sensores | 300 | 110 | 60 | 36 | 94 |
| Operaciones y comunicaciones | 310 | 95 | 70 | 45 | 100 |
| Seguridad, táctica y Marines | 300 | 85 | 65 | 49 | 101 |
| Lanzaderas y logística | 215 | 60 | 45 | 25 | 85 |
| Medicina | 140 | 35 | 30 | 24 | 51 |
| **TOTAL** | **1.800** | **550** | **380** | **255** | **615** |

[Las 1.800 plazas individuales](evidence/F04-VALHALLA-01/positions-1800.csv)
incluyen persona Core, sección, ordinal, clave estable, competencias,
responsabilidad y guardia de referencia. La clave se interpreta con identidad
de nave y perfil 5; una misma persona puede asumir una función temporal sin
convertirse en otra identidad. Capitán y primero tienen nombramientos; el
oficial WATCH y el responsable técnico DUTY_HEAD reciben funciones por ventana.
Una jefatura departamental no concede mando general.

La población es una **fixture sintética explícita** del host, como las clases
anteriores. No se asignan nombres, especies, rangos personales, biografías ni
matrículas inventadas. Instalar el perfil crea plazas vacantes; bootstrap solo
asigna personas ya existentes y rechaza sobrescribir una organización escrita.
El caso de 25 personas conserva 1.775 vacantes y registra carencias.

## Defiant: 40 operadores navales incluidos

| Sección | Especialidad | Plazas |
|---:|---|---:|
| 12 | Puente y navegación | 10 |
| 26 | Ingeniería y propulsión | 10 |
| 51 | Comunicaciones y sensores | 6 |
| 62 | Táctica naval | 10 |
| 90 | Atención médica | 4 |

[Manifiesto de las 40 personas](evidence/F04-VALHALLA-01/defiant-naval-40.csv).
Sus plazas administrativas siguen en Valhalla; su adscripción operativa apunta
a una única entidad Core `auxiliary_defiant`, persistente y acoplada. La identidad
es lógica de campaña, sin nombre ni NCC canónicos. No se genera personal al
activar esa adscripción.

Las cualificaciones 36–40 son propias de la auxiliar y no alias de las estaciones
Valhalla. Los 15 técnicos de acoplamiento (sección 79) pertenecen a Valhalla y
no figuran entre esos 40. El planificador registra obligaciones ordinarias y
disponibilidad de los especialistas sin usarlos para cobertura crítica Valhalla.
No se certifican aquí mínimos independientes de operación ni guardias críticas
de la Defiant en vuelo: corresponden a INTEGRACION-04.

`operational_ship` expresa adscripción funcional, no una transferencia física.
La auxiliar está acoplada; no hay desacoplamiento, movimiento entre naves ni
modificación del contenedor físico para simular un embarque aún no implementado.

## Hijos de Odín: 60 Marines incluidos

Mando 4; equipos Alpha, Beta, Gamma y Delta 10 cada uno; inteligencia 6;
soporte técnico de misión 6; apoyo y recuperación 4. Las ocho secciones 63–70
y las [60 identidades](evidence/F04-VALHALLA-01/odin-marines-60.csv) conservan
cualificaciones 41–45 de operaciones especiales. El primer integrante del mando
es la raíz de una cadena explícita; los responsables de unidad dependen del
mando y sus integrantes del responsable de unidad. Son responsabilidades de
destacamento, sin inventar rangos ni otorgar autoridad naval.

Los nombres Alpha/Beta/Gamma de los equipos son independientes de la etiqueta
horaria. Los integrantes rotan por disponibilidad y descanso; no se fija un
equipo entero a la guardia de igual nombre. No existe dualidad Marine/piloto.
Se rechazan credenciales de timón o Defiant, asignación a navegación Valhalla,
transferencia a una plaza naval Defiant vacante y nombramiento de mando naval.
La carga rechaza incluso un archivo con checksum válido que adultera esa
separación. Ser transportado en una misión no modifica estas competencias.

## Comunidad civil: 400 residentes

[Censo completo](evidence/F04-VALHALLA-01/census-400.csv): 130 familiares y
convivientes adultos, 90 menores/estudiantes, 65 investigadores/especialistas,
50 profesionales comunitarios, docentes y salud civil, 35 servicios/comercio y
30 representación/administración. La categoría primaria es exclusiva.

Cada identidad conserva una residencia lógica individual `100001`–`100400` en
el área platillo, presencia/ausencia y una reserva diaria mínima opcional de
dos horas con desfase individual. La categoría familiar recibe actividad
comunitaria, sin presumir empleo; estudiantes reciben actividad educativa.
Son datos de agenda inicial, no un turno militar ni una profesión completa.
La consulta deriva actividad vigente de Timeline sin crear Actors ni eventos
por cada jornada civil.

Los estudiantes tienen un enlace ilustrativo a un contacto adulto de la fixture;
no afirma parentesco biológico ni una familia canónica. `related_person` admite
una relación Core, sin una base social paralela. Relaciones y profesiones
completas, escuela, comercio, economía e IA social quedan para F12.

`F04_CIVIL_PRESENCE` registra ausencia y retorno bajo el host autorizado; la
ausencia persiste al guardar. Un residente ausente conserva identidad, residencia
y categoría, y su agenda deja de estar activa. Esta consulta civil distingue
presencia de `F04Person.available`, que sigue significando aptitud militar.
Visitantes de categoría pasajero no entran en el censo. No se permite asignar
civiles a plazas, guardias o maniobras; tampoco se convierten en Flota al volver
de una salida. No hay Actors masivos.

## Guardias, descansos, incidentes y cobertura

Se reutiliza el planificador Sovereign/Odyssey: Gamma 00–08, Alpha 08–16 y
Beta 16–24, intervalos semiabiertos. El día de referencia cumple cada sección;
los horizontes restantes empiezan con esa referencia y rotan según restricciones.

| Días | Turnos reales | Objetivo | Carencias no críticas | Ventanas críticas |
|---:|---:|---:|---:|---:|
| 1 | 1.185 | 1.185 | 0 | 24/24 |
| 7 | 8.176 | 8.295 | 119 | 168/168 |
| 14 | 16.421 | 16.590 | 169 | 336/336 |
| 28 | 32.460 | 33.180 | 720 | 672/672 |

Máximo observado cinco guardias por cualquier ventana móvil de 168 horas;
una por día natural y descanso mínimo observado 16 horas, frente a las 12
exigidas. El capitán trabaja 1/4/9/19 turnos en esos horizontes. En 28 días,
1.791 personas cambian de guardia. La heurística no demuestra optimalidad global;
los déficits de demanda son resultados reales y no se fuerzan con gente ficticia.

Se verifica el intervalo entero de ocho servicios: mando, timón, sensores,
operaciones, comunicaciones, ingeniería, seguridad/táctica y urgencias. Los
proveedores pertenecen a Valhalla; ni Marines, ni navales Defiant, ni residentes
se usan para completar su cobertura. Los JSON de ventanas contienen identidad
del proveedor y primer hueco. [Cuadrante de 28 días](evidence/F04-VALHALLA-01/roster-28-days.csv)
y [carencias exactas](evidence/F04-VALHALLA-01/gaps-28-days.json).

Se ensayan baja real, descanso protegido y relevo cualificado de una identidad
existente, sin traslado permanente. Los huecos históricos quedan guardados aunque
se recupere el servicio. Retirar los 52 habilitados de sensores registra las 21
ventanas imposibles de siete días. El capitán no puede superar una restricción
técnica no anulable. Las regresiones heredadas cubren vacaciones, caducidad,
nombramientos, cancelación, transferencia, fatiga, sucesión y corrupción.

## Separación, continuidad y alcance

El [contrato de áreas](../../../../../../desarrollo/integration/f04/tests/fixtures/valhalla_areas_contract.json)
prepara platillo, sección motriz, servicios compartidos, Defiant y destacamento.
Las referencias de equipamiento de las secciones distinguen hangar del platillo,
hangares de batalla, warp/integridad y servicios comunes. Las áreas requieren
mando y cobertura propios al separarse; no clonan plazas ni personas. El anclaje
Defiant y el reparto final de recursos siguen pendientes de INTEGRACION-04.

Se conserva nueva clase inspirada en Galaxy, programa posterior a Nemesis,
desarrollo desde 2380 y primer servicio objetivo 2387. Ablativo desplegable,
transfásicos y camuflaje romulano individual Defiant son diseño aprobado, sin
armas o camuflaje ejecutables. Flujo cuántico sigue como candidato tras pruebas,
sin instalación de serie en 2387. No se escriben velocidades o potencias.

## Persistencia, rendimiento y deuda

[Resultados y comandos](evidence/F04-VALHALLA-01/RESULTADOS.md),
[mediciones](evidence/F04-VALHALLA-01/performance.json) y
[capacidad](evidence/F04-VALHALLA-01/capacity.json). En 28 días se planifican
37.470 entidades y el archivo ocupa 11.789.885 bytes. Tras avanzar al final,
37.553 entidades y 11.805.987 bytes incluyen el historial de cambios de mando.
El segundo bloque hasta día 56 devuelve CAPACITY: se conserva el bloque original,
solo se añade un evento de rechazo. Una prueba normaliza exclusivamente ese
evento y revisión y compara byte a byte el resto de campaña, RNG y Timeline.

No se elevan 65.536 entidades ni 64 MiB, no se borra historial y no se ocultan
carencias. No se ha medido el último día acumulable exacto entre 28 y 56 ni se
prometen campañas indefinidas. PERSISTENCIA-03 debe resolver esa retención;
no bloquea la entrega nominal de Valhalla. Las mediciones son una ejecución MSI,
con memoria del proceso Python/ctypes y transacciones temporales, no memoria
aislada de Core ni percentiles. NullRHI acredita integración lógica y proyección
selectiva; no acredita una nave 3D jugable.
