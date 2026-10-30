# F04 — dotaciones generales (EN_CURSO)

CoreRPG continúa fijado en `c147d81ed069da2e09149613ab02cbc3ebe95a4a`.
Los individuos son entidades WorldState con relaciones Core, no objetos de una
simulación paralela. El catálogo existente `core_starship_classes.json` contiene
las cifras aprobadas; el generador compila sus IDs y complementos nominales.

| Clase | Flota nominal | Residentes nominales |
|---|---:|---:|
| Miranda | 130 | 0 |
| Intrepid | 160 | 0 |
| Sovereign | 700 | 0 |
| Odyssey | 1600 | 0 |
| Valhalla | 1800 | 400 |

Estas cifras son objetivos de diseño. `maximum=0` significa capacidad física sin
definir; un máximo distinto de cero es una restricción explícita de la instancia,
no una capacidad canónica de clase. Se admite 131 en una Miranda sin máximo.
Pasajeros nunca suman a Flota ni a residentes. Una plaza vacante no genera personas.

## API aditiva y pertenencia

`f04_create_population(1,class_id,&config,&session)` crea una campaña de una nave.
Config contiene identidad de nave no nula, semilla, cantidades reales por categoría
y máximo opcional. Cada individuo recibe un EntityId Core único y persistente.
La identidad completa pertenece a la campaña/nave; los handles incluyen un scope
efímero para impedir reutilizarlos en otra sesión o después de cargar una partida.
El primer individuo recibe un nombramiento explícito de capitán de bootstrap;
los demás no reciben departamentos, rangos ni cualificaciones inventados.

`f04_population_stats` distingue nominal, asignados, presentes, residentes,
pasajeros, bajas históricas y déficit respecto al nominal. Presente excluye una
ausencia temporal activa, pero no el descanso. `f04_stats`, `f04_slots` y
`f04_manifest` existentes conservan su ABI; el manifiesto lista miembros actuales.

Nuevas intenciones autenticadas por el host, con revisión actual y causa:

| Operación | Parámetros | Efecto |
|---|---|---|
| EMBARK | target=0, value=categoría 1/2/3, aux=departamento 0..4 | Nueva identidad, sin cualificación automática |
| EMBARK | target=identidad existente dada de baja, value=categoría | Reincorporación de la misma identidad |
| DEPART | target=persona | Salida/traslado fuera de la nave, conserva identidad e historial |
| CREATE_SLOT | value=departamento 1..4 | Plaza requerida y vacante |

EMBARK/DEPART requieren comandante vigente. Una incorporación duplicada se
rechaza. La salida cancela actividades, nombramientos, delegaciones, tareas y
registros de autoridad emitidos por la persona; libera plazas y elimina su
representación seleccionable. La referencia SHIP histórica permanece junto a
MEMBER=0; no representa pertenencia activa. No se restaura autoridad al volver.
Las operaciones existentes ASSIGN/DUTY/ABSENCE/RELIEF siguen siendo Core.

Una sesión representa una nave, no una flota de campañas compartidas. DEPART
implementa la salida para un traslado; no hay importador entre archivos de
campañas independientes ni duplicación automática de personas en otra nave.
Los IDs numéricos de dos campañas distintas no son identidades intercambiables.

## Consultas y Unreal

`f04_manifest_page(observer,offset,buffer,capacity,&written,&total)` admite páginas
sin copiar el mundo. Capacidad cero consulta el total. `f04_person` consulta una
identidad concreta. Un índice efímero de miembros/actividades se reconstruye al
cambiar la revisión y después de cargar; nunca es autoridad persistente.
Las definiciones tipadas se cachean para evitar parsear IDs en cada búsqueda.

`OpenPopulation` no genera Actors. `Represent` consulta el ID solicitado, y
`Refresh` actualiza solo Actors existentes. `Dematerialize` elimina la proyección,
no la entidad Core. Se preserva aislamiento por UWorld. No se desarrollan multitudes,
vida social, movimiento por interiores, apariencia, animaciones ni F12.

## Persistencia, límites y coste

SCHEMA=1 permanece cargable sin migración destructiva, con sus nueve personas y
handles originales. SCHEMA=2 añade metadatos de dotación y pertenencia. El formato
de archivo Core y ABI 1 no cambian; la nueva biblioteca lee ambos esquemas.
El ejecutable antiguo no tiene por qué leer campañas SCHEMA=2.

Presupuesto técnico: 8192 personas activas y 65536 entidades totales, incluyendo
historial y estados operativos (aproximadamente 29 registros por persona a 2200).
Son controles de memoria/archivo, no capacidades físicas. Cargar sigue acotado a
64 MiB. Se prueba una población de 5000 para superar el antiguo techo de 4096.
El historial no se borra automáticamente; agotar el presupuesto rechaza operaciones.

Las intenciones conservan una copia transaccional por publicación, con validación
del esquema; no se copia por persona, página ni Actor. Se validan solapamientos
agrupando y ordenando intervalos por persona/rol, sin comparar toda la tripulación
por pares. El índice de consultas agrupa también actividades por persona.
No se ha medido todavía un historial con decenas de miles de guardias.
Los límites son presupuestos de seguridad, no una promesa de rendimiento en su extremo.

## Validación ejecutada en MSI, Release, 30/10/2026

64/64 F04 nativas (52 regresiones + 12 de población). Cada clase guarda y recupera
en proceso independiente, preserva asignación/guardia y compara bytes del futuro
tras una alta. Casos adicionales: Miranda 127+2 con déficit 3, vacante sin personas,
altas/bajas/reincorporación de civiles/pasajeros, ausencias, duplicados, scopes,
revisión obsoleta, límites configurados, capitán saliente sin autoridad y 5000 personas.
Se ejecutó también `process_save` con el binario anterior de PR #64 y `process_load`
con el nuevo: PASS, incluido el futuro byte a byte.

Medidas de una ejecución real; no son garantías de latencia. Consulta es manifiesto
completo paginado en lotes de 73. Alta incluye transacción y evento.

| Clase | Personas Core | Crear ms | Consulta ms | Alta ms | Guardar ms | Cargar ms | Archivo bytes | Pico proceso bytes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Miranda | 130 | 0.373 | 0.061 | 0.415 | 1.154 | 0.811 | 31127 | 4894720 |
| Intrepid | 160 | 0.452 | 0.078 | 0.477 | 1.266 | 0.966 | 37938 | 4972544 |
| Sovereign | 700 | 1.736 | 0.320 | 1.841 | 5.372 | 4.105 | 160519 | 6078464 |
| Odyssey | 1600 | 3.910 | 0.773 | 4.541 | 12.620 | 9.725 | 364817 | 7921664 |
| Valhalla | 2200 | 5.591 | 1.201 | 6.207 | 17.115 | 12.704 | 501018 | 9048064 |

Valhalla: 1000 consultas por ID en 0.339 ms. Memoria: PeakWorkingSetSize del proceso
completo de prueba (incluye copias de archivos/transacciones), no bytes exclusivos de Core.
Regresiones ejecutadas: F02 15/15, F03 25/25, Core Windows 447 PASS + 4 omitidas.
Unreal 5.8.2 NullRHI: 18/18, con prueba de Valhalla sin Actors automáticos, ID 2202
en dos UWorld y desmaterialización/recuperación. No equivale a UE5 jugable.
Resultados brutos locales: `C:/F04-scalable/native/Testing/Temporary/LastTest.log`
y reportes `C:/F04-scalable/*-ue-report/index.json`. No se publica arte ni binarios.
