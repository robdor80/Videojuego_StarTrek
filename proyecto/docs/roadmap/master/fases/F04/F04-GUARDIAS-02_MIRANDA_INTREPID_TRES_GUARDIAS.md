# F04-GUARDIAS-02 — Miranda e Intrepid: tres guardias

31-10-2026. **Entrega para auditoría independiente en PR Draft; F04 EN_CURSO.**
Base exacta `4436bb444bcfae17941edc84d856d756ac5f6929` (PR #74 incluida).
Rama `codex/f04-guardias-02-miranda-intrepid`; worktree `C:/F04/Guardias02`;
laboratorio `C:/F04/GuardiasBuild`. Main limpio y origin/main coincidentes tras fetch.

Miranda conserva 130 plazas, siete departamentos, 32 secciones y Alpha=53.
Intrepid conserva 160 plazas, siete departamentos, 34 secciones y Alpha=64.
No cambian identidades, nombres, IDs, rangos, destinos, competencias ni nombramientos
nominales. Solo se añaden demandas Beta/Gamma/Fuera al registro del mismo planificador
Sovereign/Odyssey/Valhalla. Las personas de la prueba son la fixture sintética explícita
ya existente; planificar y relevar nunca crean personas ni certificaciones.

## Viabilidad antes de fijar cupos

Un servicio continuo necesita 3×7=21 guardias por semana. Con máximo cinco por
persona, el límite necesario es ceil(21/5)=5 personas habilitadas. No basta dividir
el total nominal: importa la especialidad y la disponibilidad en cada intervalo.
Los grupos distintos de esta fixture no compiten por una misma identidad para dos
servicios simultáneos. La capacidad siguiente es una cota necesaria, no una promesa
ante bajas arbitrarias. Las simulaciones completas comprueban la suficiencia real.

| Servicio crítico | Habilitados Miranda | Capacidad semanal Miranda | Habilitados Intrepid | Capacidad semanal Intrepid | Necesidad semanal |
|---|---:|---:|---:|---:|---:|
| Mando de puente | 5 | 25 | 6 | 30 | 21 |
| Timón principal | 5 | 25 | 7 | 35 | 21 |
| Sensores | 10 | 50 | 12 | 60 | 21 |
| Operaciones/ordenadores | 8 | 40 | 13 | 65 | 21 |
| Comunicaciones | 5 | 25 | 6 | 30 | 21 |
| Ingeniería de guardia | 32 | 160 | 36 | 180 | 21 |
| Táctica/seguridad | 7 | 35 | 7 | 35 | 21 |
| Respuesta sanitaria | 8 | 40 | 11 | 55 | 21 |

Miranda tiene margen de solo cuatro guardias por semana en mando, timón y
comunicaciones. Si pierde un habilitado completo durante siete días en un grupo
de cinco, 4×5=20<21: al menos una ventana queda descubierta. Se prueba esta
inviabilidad en mando; Intrepid pierde dos de seis para reproducir el mismo límite.
Retirar todos los habilitados de sensores registra exactamente 21 carencias por nave.
Proteger el descanso de todos los oficiales de guardia deja solo capitán y primero:
capacidad 10<21, al menos 11 carencias reales. El planificador no revoca ese descanso.

Sanidad conserva la definición F04 de respuesta presencial clínica **o enfermería
habilitada**. No se asigna competencia clínica a enfermería, diagnóstico o EMH para
obtener cobertura. Miranda tiene tres médicos incluyendo jefatura; Intrepid cuatro:
15 y 20 guardias semanales no permiten prometer un médico presencial en las 21
ventanas. La cobertura de respuesta sanitaria incluye cuidados de enfermería;
no certifica médico/cirugía permanente ni una simulación clínica completa.

Se preserva íntegramente Alpha el día de referencia. Para las noches se reservan
primero las ocho funciones críticas; se mantienen mantenimiento técnico, operación
de sistemas y seguridad, y se reduce investigación de laboratorio, planificación,
vuelos auxiliares y gestión de almacenes. Los cupos son compromisos de actividad
por función, sujetos al presupuesto semanal de cada departamento. No son proporciones
escaladas de las naves grandes. Se eligen 84 servicios/día en Miranda y 103 en
Intrepid, por debajo de 130×5/7=92,86 y 160×5/7=114,29. Ese margen no vuelve
intercambiables las especialidades ni elimina déficits departamentales.

En Miranda, Mando dispone de 12×5=60 guardias/semana frente a 10×7=70 si se
repitiera la referencia completa: es imposible repetirla sin reducir actividad.
Esto **no impide** preservar su Alpha de seis personas en el día aprobado; la
rotación posterior reduce tareas auxiliares y conserva mando/timón. Capitán y
primero no trabajan todos los días. Se registran además las reducciones debidas
a reservas de relevos y distribución temporal; no se afirma un óptimo global.

## Matrices definitivas del día de referencia

Gamma 00:00–08:00; Alpha 08:00–16:00; Beta 16:00–00:00, intervalos semiabiertos
sobre Timeline Core. En cada sección se eligen ordinales consecutivos: Alpha,
después Beta, después Gamma, resto Fuera. Fuera significa sin guardia ordinaria
ese día; REST, baja, vacaciones y deuda de descanso son estados separados.
Estas matrices fijan el día de referencia; en días posteriores el motor compartido
usa objetivos **departamentales**, sin prometer el mismo subtotal por sección.

### Miranda

| Departamento | Plazas | Alpha | Beta | Gamma | Fuera | Cota 5N/7 por día |
|---|---:|---:|---:|---:|---:|---:|
| Mando y navegación | 12 | 6 | 2 | 2 | 2 | 8.57 |
| Ingeniería y mantenimiento | 32 | 11 | 6 | 4 | 11 | 22.86 |
| Ciencias y sensores | 30 | 14 | 3 | 1 | 12 | 21.43 |
| Operaciones y comunicaciones | 18 | 6 | 3 | 3 | 6 | 12.86 |
| Seguridad y táctica | 16 | 5 | 2 | 2 | 7 | 11.43 |
| Lanzaderas y logística | 12 | 6 | 1 | 0 | 5 | 8.57 |
| Medicina | 10 | 5 | 1 | 1 | 3 | 7.14 |
| **Total** | 130 | 53 | 18 | 13 | 46 | 92.86 |

| ID | Departamento ABI | Sección original | Total | Alpha | Beta | Gamma | Fuera |
|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | 3 | Capitán | 1 | 1 | 0 | 0 | 0 |
| 2 | 3 | Primer oficial | 1 | 1 | 0 | 0 | 0 |
| 3 | 3 | Oficiales de guardia y mando | 3 | 1 | 1 | 1 | 0 |
| 4 | 3 | Timón y navegación | 5 | 2 | 1 | 1 | 1 |
| 5 | 3 | Coordinación de misiones | 2 | 1 | 0 | 0 | 1 |
| 6 | 2 | Jefe de ingeniería y adjunto | 2 | 1 | 0 | 0 | 1 |
| 7 | 2 | Motores warp e impulso | 8 | 3 | 2 | 1 | 2 |
| 8 | 2 | Reactor y distribución de energía | 6 | 2 | 1 | 1 | 2 |
| 9 | 2 | Soporte vital e integridad estructural | 7 | 2 | 1 | 1 | 3 |
| 10 | 2 | Reparaciones y mantenimiento general | 9 | 3 | 2 | 1 | 3 |
| 11 | 1 | Jefe científico y adjunto | 2 | 1 | 0 | 0 | 1 |
| 12 | 1 | Sensores y astrometría | 8 | 3 | 1 | 1 | 3 |
| 13 | 1 | Física y astrofísica | 6 | 3 | 1 | 0 | 2 |
| 14 | 1 | Biología y xenobiología | 5 | 2 | 1 | 0 | 2 |
| 15 | 1 | Geología y planetología | 4 | 2 | 0 | 0 | 2 |
| 16 | 1 | Laboratorios y análisis de muestras | 5 | 3 | 0 | 0 | 2 |
| 17 | 5 | Jefe de operaciones y adjunto | 2 | 1 | 0 | 0 | 1 |
| 18 | 5 | Comunicaciones | 5 | 2 | 1 | 1 | 1 |
| 19 | 5 | Transportadores | 5 | 1 | 1 | 1 | 2 |
| 20 | 5 | Sistemas informáticos y recursos | 6 | 2 | 1 | 1 | 2 |
| 21 | 6 | Jefe de seguridad y adjunto | 2 | 1 | 0 | 0 | 1 |
| 22 | 6 | Especialistas tácticos | 5 | 1 | 1 | 1 | 2 |
| 23 | 6 | Seguridad interior | 6 | 2 | 1 | 1 | 2 |
| 24 | 6 | Respuesta a emergencias y abordajes | 3 | 1 | 0 | 0 | 2 |
| 25 | 7 | Jefe de sección | 1 | 1 | 0 | 0 | 0 |
| 26 | 7 | Pilotos de lanzaderas | 3 | 1 | 0 | 0 | 2 |
| 27 | 7 | Hangares y mantenimiento | 4 | 2 | 0 | 0 | 2 |
| 28 | 7 | Suministros, almacenes y carga | 4 | 2 | 1 | 0 | 1 |
| 29 | 4 | Médico jefe | 1 | 1 | 0 | 0 | 0 |
| 30 | 4 | Médicos | 2 | 1 | 0 | 0 | 1 |
| 31 | 4 | Enfermería | 5 | 2 | 1 | 1 | 1 |
| 32 | 4 | Técnicos sanitarios y diagnóstico | 2 | 1 | 0 | 0 | 1 |

[Plazas e identidades consultadas](evidence/F04-GUARDIAS-02/miranda/positions.csv).

### Intrepid

| Departamento | Plazas | Alpha | Beta | Gamma | Fuera | Cota 5N/7 por día |
|---|---:|---:|---:|---:|---:|---:|
| Mando y navegación | 16 | 7 | 2 | 2 | 5 | 11.43 |
| Ingeniería y mantenimiento | 36 | 13 | 7 | 5 | 11 | 25.71 |
| Ciencias y sensores | 34 | 14 | 4 | 1 | 15 | 24.29 |
| Operaciones y comunicaciones | 25 | 10 | 4 | 3 | 8 | 17.86 |
| Seguridad y táctica | 18 | 7 | 2 | 2 | 7 | 12.86 |
| Lanzaderas y logística | 17 | 7 | 2 | 1 | 7 | 12.14 |
| Medicina | 14 | 6 | 2 | 2 | 4 | 10.00 |
| **Total** | 160 | 64 | 23 | 16 | 57 | 114.29 |

| ID | Departamento ABI | Sección original | Total | Alpha | Beta | Gamma | Fuera |
|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | 3 | Capitán | 1 | 1 | 0 | 0 | 0 |
| 2 | 3 | Primer oficial | 1 | 1 | 0 | 0 | 0 |
| 3 | 3 | Oficiales de guardia y mando | 4 | 1 | 1 | 1 | 1 |
| 4 | 3 | Timón y navegación | 7 | 3 | 1 | 1 | 2 |
| 5 | 3 | Coordinación de misiones | 3 | 1 | 0 | 0 | 2 |
| 6 | 2 | Jefe de ingeniería y adjunto | 2 | 1 | 0 | 0 | 1 |
| 7 | 2 | Motores warp, impulso y geometría variable | 9 | 3 | 2 | 2 | 2 |
| 8 | 2 | Núcleo warp y distribución energética | 8 | 3 | 2 | 1 | 2 |
| 9 | 2 | Soporte vital e integridad estructural | 6 | 2 | 1 | 1 | 2 |
| 10 | 2 | Reparaciones y mantenimiento general | 7 | 3 | 1 | 1 | 2 |
| 11 | 2 | Deflectores y emisores técnicos | 4 | 1 | 1 | 0 | 2 |
| 12 | 1 | Jefe científico y adjunto | 2 | 1 | 0 | 0 | 1 |
| 13 | 1 | Sensores y astrometría | 10 | 4 | 2 | 1 | 3 |
| 14 | 1 | Física y astrofísica | 7 | 3 | 1 | 0 | 3 |
| 15 | 1 | Biología y xenobiología | 6 | 2 | 1 | 0 | 3 |
| 16 | 1 | Geología y planetología | 4 | 2 | 0 | 0 | 2 |
| 17 | 1 | Laboratorios y datos científicos | 5 | 2 | 0 | 0 | 3 |
| 18 | 5 | Jefe de operaciones y adjunto | 2 | 1 | 0 | 0 | 1 |
| 19 | 5 | Comunicaciones | 6 | 2 | 1 | 1 | 2 |
| 20 | 5 | Transportadores | 6 | 2 | 1 | 1 | 2 |
| 21 | 5 | Sistemas bioneurales y ordenadores | 7 | 3 | 1 | 1 | 2 |
| 22 | 5 | Coordinación de recursos y holocubiertas | 4 | 2 | 1 | 0 | 1 |
| 23 | 6 | Jefe de seguridad y adjunto | 2 | 1 | 0 | 0 | 1 |
| 24 | 6 | Especialistas tácticos | 5 | 2 | 1 | 1 | 1 |
| 25 | 6 | Seguridad interior | 8 | 3 | 1 | 1 | 3 |
| 26 | 6 | Respuesta a emergencias y abordajes | 3 | 1 | 0 | 0 | 2 |
| 27 | 7 | Jefe de sección | 1 | 1 | 0 | 0 | 0 |
| 28 | 7 | Pilotos de lanzaderas | 4 | 2 | 0 | 0 | 2 |
| 29 | 7 | Hangares y mantenimiento | 7 | 2 | 1 | 1 | 3 |
| 30 | 7 | Suministros, almacenes y carga | 5 | 2 | 1 | 0 | 2 |
| 31 | 4 | Médico jefe | 1 | 1 | 0 | 0 | 0 |
| 32 | 4 | Médicos | 3 | 1 | 1 | 1 | 0 |
| 33 | 4 | Enfermería | 7 | 3 | 1 | 1 | 2 |
| 34 | 4 | Técnicos sanitarios, diagnóstico y soporte EMH | 3 | 1 | 0 | 0 | 2 |

[Plazas e identidades consultadas](evidence/F04-GUARDIAS-02/intrepid/positions.csv).

## Planificación, autoridad y descansos

Se reutiliza `plan_watches`, sin otro motor. Se conservan selección determinista,
reservas críticas, una guardia ordinaria por día, máximo cinco inicios en cualquier
ventana móvil de 168 horas y mínimo doce horas entre fin e inicio. Ausencias,
francos protegidos, deuda, credenciales completas y nombramientos siguen limitando
cada candidato. WATCH y DUTY_HEAD son funciones temporales legítimas sobre
identidades y destinos existentes. Ningún rango, jefatura táctica o médica concede
mando general. No se inventa un segundo oficial nominal donde no estaba aprobado.

Una corrección común considera candidatos legalmente disponibles cuando el
reparto preferente de francos dejaría un servicio crítico vacío. Respeta REST,
ABSENCE, deuda y límites ordinarios; no cancela descansos protegidos. En la primera
simulación Miranda perdía la ventana de mando del día 23 por esa preferencia,
aunque había candidatos legales; la prueba de 28 días verifica su recuperación.

El relevo tras CANCEL_DUTY recupera la función vinculada a la actividad cancelada,
al inicio o a mitad del turno, mediante su historial Core existente. Consulta de
candidatos y confirmación usan el mismo criterio. Una función revocada
expresamente no se resucita. El pasado y los déficits resueltos siguen registrados;
la sustitución temporal conserva todas las plazas nominales. No se añaden campos,
se suben límites ni se cambia el esquema para esta corrección.

## Simulaciones verificadas

| Nave | Días | Guardias reales / objetivo | Déficit no crítico | Ventanas críticas | Máximo móvil 7 días | Descanso mínimo | Turnos capitán |
|---|---:|---:|---:|---:|---:|---|---:|
| Miranda | 1 | 84 / 84 | 0 | 24/24 | 1 | — | 1 |
| Miranda | 7 | 532 / 588 | 56 | 168/168 | 5 | 16 h | 3 |
| Miranda | 14 | 1051 / 1176 | 125 | 336/336 | 5 | 16 h | 6 |
| Miranda | 28 | 2074 / 2352 | 278 | 672/672 | 5 | 16 h | 13 |
| Intrepid | 1 | 103 / 103 | 0 | 24/24 | 1 | — | 1 |
| Intrepid | 7 | 651 / 721 | 70 | 168/168 | 5 | 16 h | 2 |
| Intrepid | 14 | 1283 / 1442 | 159 | 336/336 | 5 | 16 h | 4 |
| Intrepid | 28 | 2535 / 2884 | 349 | 672/672 | 5 | 16 h | 6 |

Cada servicio se consulta sobre la ventana **completa**, incluyendo límites de
agendas, ausencias y vencimientos; no basta comprobar el inicio. Las cifras son
para la fixture completa sin incidencias. Los casos negativos mantienen déficits.
En 28 días cambian de guardia 109 personas Miranda y 150 Intrepid. Capitán y primero
tienen días sin guardia; una prueba independiente recorre cada agenda y ventana móvil.

| Departamento | Carencia Miranda 28 días | Carencia Intrepid 28 días |
|---|---:|---:|
| Mando y navegación | 70 | 79 |
| Ingeniería y mantenimiento | 44 | 83 |
| Ciencias y sensores | 16 | 0 |
| Operaciones y comunicaciones | 69 | 93 |
| Seguridad y táctica | 7 | 15 |
| Lanzaderas y logística | 0 | 0 |
| Medicina | 72 | 79 |

Los [cuadrantes Miranda](evidence/F04-GUARDIAS-02/miranda/roster-28-days.csv) e
[Intrepid](evidence/F04-GUARDIAS-02/intrepid/roster-28-days.csv) y los JSON de
carencias contienen actividades, persona, destino, intervalos, causa y plan.
Los archivos son exportaciones descartables de Core, nunca otra autoridad.

## Compatibilidad y regresión

ABI 1 y vocabulario SCHEMA 4 existentes. Instalación/bootstrap siguen produciendo
SCHEMA 3; PLAN_WATCHES migra explícitamente 3→4. Las listas históricas de seis
servicios Miranda y siete Intrepid se conservan para SCHEMA 3; solo SCHEMA 4 usa
las ocho funciones de guardia. Las definiciones originales de plaza, máscaras,
responsabilidades y cobertura declarativa no se alteran, por lo que los guardados
anteriores siguen siendo válidos y se conservan byte a byte.

Se prueban lectura SCHEMA 1/2, SCHEMA 3 sin modificación automática, continuación
tras un Alpha heredado, ampliación de planes después de cargar, determinismo entre
procesos, avance directo/escalonado, identidades/destinos, cancelaciones/ausencias
persistentes, caducidad interior y rechazo atómico de corrupción semántica con
checksum Core válido. La DLL anterior a esta rama produce guardados de las cinco
clases que el nuevo lector carga y continúa al mismo futuro. Sus hashes y tamaños
están en [compatibilidad](evidence/F04-GUARDIAS-02/compatibility.json).

F04: **243/243** (187 previas + 56 GUARDIAS-02); F02 **15/15**; F03 **25/25**.
Core completo + Content JSON: **447 superadas, cuatro omitidas por plataforma,
cero fallos**. Unreal **5.8.2**, Win64 NullRHI: **25/25**, sin warnings de test;
las dos nuevas pruebas simulan 28 días Miranda/Intrepid, cero Actors automáticos,
proyección selectiva, otro UWorld/sesión, archivo exacto y el mismo futuro.
El compilador conserva avisos del motor por APIs obsoletas y MSVC posterior al
preferido. NullRHI valida integración lógica, no una nave 3D jugable.

Regresión de las cinco clases: estructura, identidad, Alpha/referencia exacta,
1/7/14/28 días y cobertura, incidentes, mando, descanso y guardados. Valhalla conserva
1.800 Flota + 400 civiles; sus 40 navales Defiant y 60 Marines están incluidos en
Flota y mantienen competencias separadas. Sus tablas y las de Sovereign/Odyssey
son idénticas a la base. Se conserva el rechazo atómico de capacidad acumulada
Valhalla y el historial prolongado de Odyssey; no se compacta ni elimina nada.

Contratos documentales F04/Miranda/F03/F02: **61/61**; LORE-03 A: **56/56**;
fixture de autoridad y roadmap: PASS. Referencias globales: fallo previo con
**566 incidencias idénticas a main, cero nuevas**. No se presenta como PASS.

## Rendimiento y límites

Medición puntual MSI/MSVC Release, con otras validaciones en ejecución, sin
percentiles ni garantía de latencia. Guardar incluye consulta de tamaño y
serialización; cargar valida Core y dominio. Actividades equivale aquí a guardias
DUTY del plan; las demás entidades se muestran en el total Core.

| Nave | Días | Plan ms | Guardar ms | Cargar ms | Actividades DUTY | Entidades tras plan | Archivo bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| Miranda | 1 | 2.14 | 4.32 | 3.27 | 84 | 432 | 116258 |
| Miranda | 7 | 11.16 | 11.37 | 9.36 | 532 | 1089 | 310341 |
| Miranda | 14 | 26.09 | 19.51 | 16.58 | 1051 | 1857 | 537009 |
| Miranda | 28 | 67.77 | 36.82 | 30.75 | 2074 | 3380 | 986132 |
| Intrepid | 1 | 2.69 | 5.12 | 4.09 | 103 | 513 | 139450 |
| Intrepid | 7 | 14.10 | 13.37 | 11.34 | 651 | 1279 | 367672 |
| Intrepid | 14 | 31.63 | 22.87 | 19.66 | 1283 | 2169 | 632600 |
| Intrepid | 28 | 82.81 | 42.17 | 36.71 | 2535 | 3938 | 1158923 |

Los `performance.json` desglosan creación, instalación, bootstrap, manifiesto,
cobertura, avance y memoria Working Set/Peak Working Set del proceso Python/ctypes,
con transacciones y buffers: no es memoria aislada de Core. Los `.f04` escritos
realmente en el laboratorio coinciden en tamaño con la serialización. Los
`incident-performance.json` miden baja, búsqueda y sustitución real después de
cargar, verificando destinos y cobertura recuperada con historial de carencia.

Persisten 65.536 entidades y 64 MiB como límites operativos. Las dos naves caben
con margen en 28 días; no se certifican campañas indefinidas ni un año. El límite
de historial prolongado queda en **F04-PERSISTENCIA-03**, sin iniciarlo ni cambiar
el formato. Los planes son finitos y deben ampliarse con autoridad antes de agotar
el horizonte. Las bajas pueden volver inviables los servicios; se conservan sus
carencias. No se garantiza equidad global ni simulación biológica por especie.
La autoridad de host nativo y los nombramientos siguen siendo necesarios para
confirmar cualquier sustitución; la consulta de candidatos no la aplica por sí sola.

## Evidencias y alcance

[Resultados, comandos y procedencia](evidence/F04-GUARDIAS-02/RESULTADOS.md).
No se modifica CoreRPG genérico, ABI pública, formato Core ni pins. No se tocan
modelos 3D, Blender, texturas, puentes, mapas o recursos artísticos. Todo se ejecuta
por terminal y herramientas de programación, sin Computer Use. No se fusiona,
no se cierra F04 ni se ejecutan PERSISTENCIA-03/INTEGRACION-04.
