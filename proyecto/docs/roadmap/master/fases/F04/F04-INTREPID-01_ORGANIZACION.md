# F04-INTREPID-01 — Organización de clase Intrepid

Fecha: 2026-10-30. F04 permanece **EN_CURSO**. Implementación para auditoría independiente mediante **PR Draft contra main**, sin fusionar.

Base verificada después de `git fetch origin`: `main` y `origin/main` en `9e5f46eb1ff364f66e41d913cb64ce5ce232b4c2`, fusión de F04-MIRANDA-01 (PR #67). Rama exclusiva: `codex/f04-intrepid-organizacion`.

La plantilla explícita `F04_INTREPID_EXPLORATION=2` aporta **160 plazas de Flota Estelar, cero civiles residentes nominales, siete departamentos y 34 grupos/secciones**. Es un perfil reutilizable de exploración científica de largo alcance posterior a Nemesis, con patrulla, respuesta rápida y operaciones independientes. Crear una población Intrepid no instala automáticamente este perfil ni inventa personas para cubrirlo.

| Departamento | Total | Alpha 08:00–16:00 |
|---|---:|---:|
| Mando y navegación | 16 | 7 |
| Ingeniería y mantenimiento | 36 | 13 |
| Ciencias y sensores | 34 | 14 |
| Operaciones y comunicaciones | 25 | 10 |
| Seguridad y táctica | 18 | 7 |
| Lanzaderas y logística | 17 | 7 |
| Medicina | 14 | 6 |
| **Total** | **160** | **64** |

[La plantilla completa](F04-INTREPID-01_PLANTILLA_160.md) enumera los 34 subtotales y las 160 plazas con claves estables. La identidad completa de una plaza incluye nave, perfil y clave `sección*100+ordinal`; no se confunde una plaza Intrepid con la misma clave local de Miranda. Las personas son referencias a identidades Core existentes. Nombres, biografías, especies, rangos y jerarquía exacta siguen pendientes del autor; la fixture sintética mantiene rango cero.

## Motor compartido y configuración de nave

Se añade únicamente la definición inmutable de Intrepid al registro `trek_templates::Profile`, con sus secciones, máscaras de cualificación, responsabilidades y grupos de cobertura. **No se modifica el motor** `f04_bridge.cpp` / `f04_organization.inc`, CoreRPG, la tabla de 130 plazas de Miranda ni los nominales de Sovereign, Odyssey y Valhalla. Las definiciones ABI de departamentos 1–7 y especialidades 8–30 se reutilizan sin renumerar.

La organización usa las API existentes: `INSTALL_TEMPLATE`, `BOOTSTRAP_TEMPLATE`, `ASSIGN`, `TRANSFER`, `CREDENTIAL`, `DUTY`, `REST`, `ONCALL`, `ABSENCE`, `RELIEF`, `APPOINT`, `FUNCTION`, `DEPART` y `EMBARK`. Todas las mutaciones pasan por las intenciones autenticadas del host, revisión vigente, ActionEngine y validación transaccional. No se añade otro motor de autoridad, persistencia o planificación.

Para instalar, el host crea o carga una población de clase compatible y ejecuta `INSTALL_TEMPLATE` con `value=F04_INTREPID_EXPLORATION`, `aux=F04_INTREPID_EQUIPMENT` y causa documental. Se crean 160 plazas vacantes sin nuevas personas. El bootstrap es una fixture sintética explícita y única sobre personas todavía no configuradas, nunca un generador de personajes del juego. Una campaña real asigna sus personas existentes con sus competencias y nombramientos. La plantilla admite población parcial: 157 personas dejan tres vacantes reales.

El perfil nominal permanece inmutable; cada nave conserva su identidad, dotación real, competencias, destinos, ocupación de plazas, ausencias, agendas y nombramientos en Core. Puede liberar plazas, trasladar personas y configurar equipamiento adicional mediante el campo existente. `required_equipment=8191` identifica referencias funcionales a sistemas del motor previo: no codifica cantidades de salas ni modelos tecnológicos. Un cambio de distribución nominal requiere otro perfil aprobado, evitando alterar el significado de archivos guardados existentes.

Los mecanismos de barquillas de geometría variable pertenecen a Propulsión. Ingeniería repara deflectores; Ciencias no recibe habilitación de reparación por operarlos. Operadores de transportadores y especialistas bioneurales tampoco obtienen reparación general automáticamente. Sistemas bioneurales y ordenadores se coordinan con Ingeniería. Pilotaje principal y pilotaje de lanzaderas usan cualificaciones diferentes; una doble certificación no crea otra plaza.

La configuración de nave puede contemplar diferentes salas de transportadores y vehículos auxiliares, sin fijar cantidades no aprobadas. No se añade Delta Flyer ni la sala de astrometría modificada de Voyager. La capacidad de aterrizaje requiere procedimientos y cualificaciones posteriores, sin otro departamento. No se copian personajes ni historia de Voyager.

## Guardia Alpha y cadena de mando

`PLAN_ALPHA` programa 08:00–16:00 del día indicado sobre las 64 plazas seleccionadas, omitiendo vacantes y personas incompatibles. `alpha_present`, `alpha_deficit`, `on_duty` y `vacant` conservan significados separados. No tener DUTY no implica descansar: REST requiere una actividad explícita.

La referencia completa ejecutada presenta **64 personas distintas, déficit Alpha cero**, cobertura en mando, timón, sensores, operaciones, comunicaciones, ingeniería y táctica, y respuesta médica presencial. Los siete grupos continuos se comprueban por separado, más `urgent_response` para sanidad. Operaciones usa la referencia funcional COMPUTER, diferenciada de COMMUNICATIONS; eso no exige que todo personal de Operaciones esté ante una consola. Tampoco obliga a que las 64 personas estén en el puente.

El primer oficial puede recibir WATCH sobre su misma plaza e identidad. El capitán conserva la autoridad superior; solo existe un nombramiento WATCH efectivo por ventana. El oficial adicional Alpha puede planificar, coordinar o preparar relevos. Si el primer oficial está vacante, se programa al oficial de guardia disponible y se expone el déficit de personal. Timón tiene tres personas Alpha, sensores cuatro: sus tareas pueden distribuirse entre consola principal, análisis, laboratorios y preparación de relevos, sin triplicar consolas físicas.

El jefe de seguridad cualificado recibe una función táctica sobre su misma plaza. Los dos especialistas tácticos Alpha son apoyo o relevo. La función depende de disponibilidad, servicio y competencias; no concede mando ni autorización para abrir fuego. No se implementan disparos ni reglas de combate de F05. El médico jefe mantiene autoridad sanitaria, sin mando general. Jefes y adjuntos tienen plazas y nombramientos distintos; rango y nombramiento no se confunden.

Los traslados cancelan el servicio y las funciones anteriores, conservan identidad y actualizan departamento; los nombramientos departamentales anteriores se cancelan. Salir del destino libera plaza y autoridad. Reincorporarse con el mismo ID no restaura nombramientos cancelados. Un relevo usa otra persona real y deja visible la plaza que esa persona ha liberado.

## Propuesta limitada Beta y Gamma

Este ejemplo ejecutado valida ventanas, identidades, competencias y cobertura puntual. **No aprueba una dotación nocturna definitiva ni un régimen de descansos, vacaciones, suplencias o continuidad semanal**. `coverage_validated=0` permanece explícito.

| Servicio | Beta 16:00–24:00 (sección/ordinal) | Gamma 00:00–08:00 siguiente (sección/ordinal) |
|---|---|---|
| Mando de guardia, WATCH temporal | 3/2 | 3/3 |
| Timón principal | 4/4 | 4/5 |
| Sensores | 13/5 | 13/6 |
| Operaciones/ordenadores | 21/4 | 21/5 |
| Comunicaciones | 19/3 | 19/4 |
| Ingeniería | 6/2 | 7/4 |
| Táctica/seguridad | 24/3 | 24/4 |
| Respuesta sanitaria localizada | 32/2 | 32/3 |

Hay siete personas de servicio y un médico localizado distinto por ventana, todos fuera de la selección Alpha. La disponibilidad sanitaria localizada es una posibilidad técnica pendiente de validación profesional del diseño; no se cuenta como presencia física. Una ausencia en Operaciones reduce la cobertura aunque siga habiendo Comunicaciones. Al acabar el ejemplo, el servicio cae a cero y las carencias quedan visibles. No se añaden efectivos ni se extienden agendas automáticamente.

Se conservan los patrones 3×8 y 4×6. Una prueba específica programa cuatro equipos distintos de seis horas mediante las API existentes y verifica el cambio de patrón con cobertura; no valida descansos. `PLAN_ALPHA` sigue exigiendo 3×8 por su ventana ilustrativa aprobada.

## Holocubiertas y EMH

La búsqueda en integración nativa y contratos de gameplay encuentra catálogos declarativos de actividad y solicitudes al ordenador, pero ningún servicio nativo ejecutable de reservas compatible. Se entrega por ello el [contrato mínimo de datos](../../../../../../desarrollo/integration/f04/tests/fixtures/intrepid_facilities_contract.json), conforme a la alternativa autorizada en F04. Reutiliza las referencias de actividad, tecnología y acciones del ordenador existentes.

El contrato contempla dos holocubiertas como referencia configurable, con claves por nave, ubicación lógica, estado operativo, disponibilidad, ocupantes, capacidad, limitaciones y actividad asociada. Sus valores iniciales son **sin configurar y no disponibles**, con capacidad pendiente: no declara instalaciones operativas ni inventa aforo. La nave concreta debe vincular identidad y configuración. No existen escenarios 3D ni un almacén paralelo de estado mutable.

Quedan definidos los campos futuros de reserva, ventana `[start,end)`, duración, participantes, actividad, cancelación/interrupción y referencia al evento de emergencia. Una sesión de dos horas significa `end=start+7200` sobre **CoreRPG Timeline**. El universo y los eventos externos continúan avanzando; no se añade otro reloj ni una condición de presencia del jugador. Los NPC tendrán el mismo contrato de uso. La futura ejecución deberá comprobar aforo, exclusividad, agendas, autoridad y emergencias, y persistir en Core. **La ejecución de instalaciones y reservas no está implementada ni se contabiliza como prueba funcional superada.** Se difieren actividades sociales, deportes, misiones holográficas, entrenamiento y XP a sus fases, especialmente F12/F11.

EMH queda como capacidad tecnológica configurable, sin persona automática y sin ocupar una de las 160 plazas. Los tres técnicos sanitarios incluyen soporte operativo EMH. No se atribuye identidad ni historia del Doctor de Voyager. Una eventual identidad holográfica reconocida deberá pasar por los contratos de identidad persistente y las reglas específicas futuras, sin crear ahora una persona 161.

## Persistencia, simulación y validación

Se conserva ABI 1 y SCHEMA=3 de Miranda; solo se añade el ID de perfil 2. No se añaden etiquetas relacionales ni cambia el formato de CampaignPersistence. SCHEMA=1/2 siguen cargando sin migración automática y mantienen sus bytes. SCHEMA=3 de Sutherland también se carga exactamente con la DLL nueva y reproduce el mismo futuro que la DLL anterior. Intrepid persiste plazas, personas, secciones, responsabilidades, competencias, servicio y funciones; la restauración entre procesos es determinista. Los archivos incoherentes se rechazan sin sustituir la campaña activa.

CoreRPG permanece fijado a `c147d81ed069da2e09149613ab02cbc3ebe95a4a`. La tripulación reside en WorldState, y las agendas se evalúan sobre el reloj Core aunque no exista jugador ni Actor. Unreal 5.8.2 solo representa personas solicitadas explícitamente. La prueba Intrepid verifica cero Actors automáticos, representación selectiva, desmaterialización sin cambiar el guardado y recuperación en otra sesión/UWorld con el mismo futuro.

Resultados, comandos, procedencia, omisiones y límites: [evidence/F04-INTREPID-01/RESULTADOS.md](evidence/F04-INTREPID-01/RESULTADOS.md). No se adelantan F05, F11 o F12, ni se declara completada F04. Pendientes: jerarquía por rangos, ajustes concretos de cada nave, validación de descansos/suplencias y urgencias 24/7, ejecución futura de instalaciones y auditoría independiente antes de integrar.
