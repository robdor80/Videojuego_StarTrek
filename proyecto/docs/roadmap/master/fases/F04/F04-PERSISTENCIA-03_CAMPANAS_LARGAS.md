# F04-PERSISTENCIA-03 — Persistencia de campañas largas

Fecha: 31-10-2026. **INCOMPLETA: bloqueo de arquitectura pendiente de autorización
para ampliar CoreRPG genérico.** Esta entrega diagnostica el problema y añade
pruebas reproducibles; no implementa archivo, compactación ni campañas ilimitadas.
No inicia INTEGRACION-04 ni CIERRE-05. F04 permanece EN_CURSO.

Base exacta: `45f7816c9aa996bfd678b11b4f9fa1a4b9632021` (PR #75 incorporada).
Rama: `codex/f04-persistencia-03-campanas-largas`.
Repositorio: `robdor80/Videojuego_StarTrek`.

## 1. Precondiciones y aislamiento

Se actualizó main mediante fetch y fast-forward a la base obligatoria. El checkout
principal **no estaba limpio**: dos bajas en
`assets/interiores/shipboard/ten_forward_tng/` y un directorio nuevo
`assets/interiores/ten_forward_tng/`, cambios ajenos a F04. Se conservaron y se
usó un worktree nuevo y limpio `C:/F04/Persistencia03`. No se restauraron ni
incluyeron esos recursos en commits. Laboratorio externo: `C:/F04/PersistenciaBuild`.

Pins comprobados, sin modificarlos:

| Integración | CoreRPG |
| --- | --- |
| F04 | `c147d81ed069da2e09149613ab02cbc3ebe95a4a` |
| F03 | `9c53a33787de13d91eb2abe4da07033ee0fa1dc1` |
| F02 | `4f282863737bcd8f5add401202a9e1064c133672` |

`Engine/Build/Build.version` local confirma Unreal **5.8.2**, changelist
56702186. Se revisaron las entregas de Odyssey, Valhalla y GUARDIAS-02, sus
límites y el código vigente. No se usa Computer Use ni se modifica otro proyecto,
el repositorio CoreRPG, fuentes Unreal, recursos artísticos o archivos ignorados
del checkout. Las compilaciones y partidas sintéticas se generan fuera de él.

## 2. Auditoría del modelo y causa exacta

Core `WorldState` representa todas las identidades emitidas mediante el intervalo
denso `[1,last_entity_id]`. `contains(id)` comprueba ese intervalo;
`entity_count()` devuelve el máximo emitido, no un recuento de registros vigentes.
`create_entity()` incrementa identidad y revisión. No existen borrado de entidad,
desvinculación de definición, archivo, localizador de entidades externas ni
consulta de segmentos. Las definiciones quedan asociadas de forma inmutable.
Las relaciones, contenciones, poblaciones, membresías y conocimiento son tablas
canónicas residentes. Quitar relaciones no libera identidades.

**65.536 es el presupuesto explícito de F04**, en `make()` y `schema()` de
`src/f04_bridge.cpp`; no es el máximo nativo de IDs de CoreRPG. Core utiliza IDs
de 64 bits. Su `PersistenceLimits` predeterminado impone **64 MiB** y otros límites
independientes: un millón de relaciones, definiciones, enlaces, etc. Ningún límite
se cambia en esta entrega. Los escenarios de capacidad observados tropiezan con
F04_CAPACITY antes de agotar 64 MiB; no deben confundirse ambos techos.

Los generadores `RandomStreams`, su semilla y cada estado se capturan con el
mundo. `CampaignPersistence` incluye el reloj y registros Timeline. F04 guarda
tareas/eventos en WorldState; su validador exige Timeline sin registros. El techo
genérico Timeline de 4.096 registros no es la causa de este fallo F04.

### Registros generados y estado presente

| Hecho F04 | Representación actual | Dependencia que impide descartarlo sin más |
| --- | --- | --- |
| Plan por solicitud | `roster_plan`, nave, emisor, causa, intervalo, modo | Referencias de actividades y carencias; exclusión de planes |
| Servicio ordinario | `activity` DUTY por persona/turno | Persona, plaza, emisor, PLAN, causa, intervalo, STOP, suplencia |
| Cobertura crítica | Ocho `function` por turno cuando hay proveedores | Proveedor real, plaza, responsable, intervalo y estación |
| Mando/ingeniería de guardia | Dos `appointment` por turno si cubiertos | Sucesión y autoridad temporal |
| Carencia crítica/no crítica | `roster_gap` por departamento/estación/intervalo | Déficit original e incidencias posteriores, incluso resueltas |
| Descanso/franco protegido | `activity` REST | Intervalo y deuda tras RECALL; no se elimina al vencer |
| Ausencia/vacaciones/baja | `activity` ABSENCE, código y causa | Disponibilidad, recuperación por fin de intervalo, causalidad |
| Suplencia/cancelación | Nueva DUTY con ACTIVITY origen, STOP y cambios de estado; funciones/nombramientos | Referencias entre IDs y funciones revocadas explícitamente |
| Nombramiento/revocación | `appointment`, estado y evento | No restaurar autoridad cancelada |
| Cambio de mando | `event` op 100 al cruzar fronteras temporales | Responsable previo, destino, causa y tick |
| Traslado/salida | Persona y plaza existentes modificadas, actividades canceladas y evento | MEMBER, destino y continuidad de identidad |
| Incidente/orden/revisión/tarea | Actividad y/o `event`, `order`, `review`, `task`, `delegation`, `mandate` | Resultado, causa, emisor, origen y vencimiento |
| Censo/agenda civil | Campos y referencias en la persona; no DUTY diaria militar | Domicilio, categoría, contacto, presencia y reserva de agenda |

El mayor crecimiento es DUTY; hay además 24 funciones y seis nombramientos por
día, carencias y eventos. El reloj no convierte automáticamente el pasado en
registros pequeños: los intervalos vencidos siguen presentes con sus relaciones.
No hay una simulación clínica completa de muerte/secuelas/méritos en este corte;
no se atribuye a estas pruebas una capacidad narrativa futura inexistente.

### Transacciones e integridad existentes

`f04_execute` prepara una copia de Campaign, aplica operaciones y valida el
grafo antes del swap. Ante denegación descarta la copia y añade un evento sobre
el estado anterior. En la saturación reproducida queda espacio para ese evento;
no se promete registrar rechazos si ya no queda ni una entidad. `f04_advance`
también prepara copia. Una carga se publica solo después de validación Core y
F04 y renueva el scope. Un fallo deja la sesión previa intacta.

Core valida estructura, orden canónico, referencias, RNG y Timeline y usa
checksum contra corrupción accidental. **No tiene autenticación criptográfica
contra un atacante que regenere checksums.** Los validadores F04 rechazan algunas
alteraciones semánticas con checksum correcto, no toda falsificación histórica.
`f04_save` devuelve bytes; no implementa escritura atómica al sistema de archivos.
La integridad de un conjunto de segmentos no puede obtenerse envolviendo estos
bytes con un índice externo sin validación y autoridad adicional del motor.

## 3. Medición y reproducción

Los resultados completos están en [evidencias](evidence/F04-PERSISTENCIA-03/RESULTADOS.md).
Se miden perfiles completos en 1, 7 y 28 días, con estados tipados, relaciones,
tamaño serializado, planificación, guardado/carga y memoria del proceso.
Los tiempos de save incluyen sus dos llamadas ABI (tamaño y escritura).
Las mediciones son muestras locales, no percentiles ni garantías de latencia.
Memoria significa working set de todo el proceso, incluyendo copias y buffers.

Un recorrido adicional intenta 365 días por clase y 730 en Valhalla mediante
bloques de hasta 28 días, con actividades reales, avance y recarga periódica.
Al fallar un bloque se conserva el último horizonte completo y se informa del
rechazo. Un diagnóstico que pasa al reproducir F04_CAPACITY **no equivale a que
la campaña haya alcanzado el horizonte solicitado**. El historial se mantiene
íntegro en memoria activa: en esta entrega el historial archivado es cero.

## 4. Alternativas evaluadas

| Alternativa | Evaluación con las APIs/pins actuales | Decisión |
| --- | --- | --- |
| A. Compactación autoritativa | Quitar payload no disminuye `entity_count`; el binding es inmutable. Reutilizar una entidad cambia el significado de IDs publicados. Un resumen con hash pierde quién hizo qué. | No resuelve el techo manteniendo contratos |
| B. Segmentos temporales | Se pueden guardar snapshots completos independientes, pero Core no valida un manifiesto conjunto, pertenencia, referencias cruzadas, precedencias ni publicación multisegmento. | Requiere ampliación genérica |
| C. Ventana activa + archivo | Adecuada si Core administra ambos. Con el motor actual se perdería información o el adaptador tendría que ser autoridad de segmentos y referencias. | Arquitectura propuesta, no implementada |
| D. Intervalos/referencias compartidas | Reducen duplicación y bytes, pero la selección diaria de personas cambia y existen suplencias, cancelaciones y causas distintas. Bajo límites fijos solo aplazan la saturación si toda la historia sigue residente. | Optimización complementaria futura |

Modificar snapshots públicos no abre una excepción: retirar un registro interior
de sus tablas deja la identidad existente; reducir `last_entity_id` trunca el
mundo y vuelve a emitir IDs históricos. El test `persistence_core_boundary`
demuestra ambos comportamientos. Reconstruir un mundo renumerando entidades rompe
IDs de actividades, planes y referencias externas. Guardar snapshots completos
como exportaciones es válido; usarlos como una campaña segmentada exige definir
y validar esa nueva frontera autoritativa en Core.

Ni el simple aumento de límites ni comprimir el archivo de salida reduce el
grafo residente y sus copias transaccionales. Codificar indefinidamente hechos
en RelationKind también termina en el millón de relaciones/64 MiB y exige un
nuevo contrato de consulta. No se declara imposible cualquier optimización
finita; falta la capacidad estructural para una retención escalable sin descarte.

## 5. Ampliación genérica mínima propuesta — PENDIENTE DE AUTORIZACIÓN

**Elegida para proponer:** archivo inmutable de entidades operativas cerradas,
con ventana activa y localización histórica gestionadas por CoreRPG. No hay
código genérico modificado ni prototipo que actúe como segunda autoridad.
El motor no conocerá naves, rangos ni guardias. F04 decide qué registros han
terminado y qué hechos deben permanecer íntegros; Core valida identidad,
referencias, temporalidad declarada, integridad y atomicidad del conjunto.

### Capacidades y contratos que faltan

1. Separar máximo de identidad emitida, existencia lógica y registros residentes.
   IDs globales de campaña de 64 bits, monotónicos y **nunca reutilizados**.
   Localizador persistente que distinga activo/archivado/inexistente y permita
   referencias entre ubicaciones. Archivar no equivale a borrar una persona.
2. Segmentos genéricos inmutables, acotados por bytes/registros e intervalo
   `[inicio,fin)`, con UUID de campaña, secuencia, versión, longitud, hash fuerte,
   vínculo al segmento previo e índice de ID/tipo/tiempo/participantes.
   Los índices deben derivarse y comprobarse contra los registros originales.
3. Manifiesto autoritativo con checkpoint activo, high-water mark, revisión,
   semilla/streams, Timeline, frontera de consolidación y descriptores de todos
   los segmentos. Validar conjunto completo y dependencias antes de publicar.
   Hashes verifican integridad; no sustituyen el payload consultable ni garantizan
   autenticidad si un atacante puede sustituir también la raíz confiable.
4. Preparar/validar/publicar consolidación sin cambiar hechos ni orden de IDs.
   Prohibir solapamientos, IDs duplicados, referencias rotas y modificación de
   segmentos confirmados. Un fallo de preparación no altera mundo ni manifiesto.
5. Consultas históricas paginadas que resuelvan IDs sin reactivar actividades ni
   copiar toda la historia al mundo activo. Un fallo de lectura se informa como
   error de integridad; nunca se interpreta como ausencia de servicio/persona.
6. Nuevo contenedor **optativo y versionado**, conservando lectores SAVE v1/v2/v3
   y CRPGTIME v1. APIs anteriores mantienen sus garantías en modo monolítico;
   la semántica residente/archivada usa APIs nuevas explícitas. No cambiar en
   silencio `definition_of` o `contains` para aparentar que un archivo no existe.
   Diseñar y revisar por separado ABI y adaptación de consumidores genéricos.

El detalle binario y firmas C++ se fijarán con la aprobación y revisión de Core;
no se presenta un formato público nuevo como ya aprobado. El alcance mínimo es
identidad/localización, persistencia conjunta, transacción y lectura histórica:
un borrado de entidades aislado no basta.

### Retención y determinismo F04 previstos

Conservar activos presente, futuro, siete días operativos anteriores y cualquier
REST/ABSENCE/deuda, suplencia, orden, incidente o referencia que aún pueda influir.
Antes de consolidar, comprobar cierre temporal y dependencias causales; no asumir
que todo dato viejo ha terminado. El margen de siete días cubre las ventanas de
168 h y 12 h; deudas y ausencias abiertas no vencen por antigüedad.

La equidad del planificador también usa **`p.work.size()` de toda la vida**, además
de ventanas recientes. No basta conservar siete días: se necesita un acumulador
autoritativo por persona equivalente al número exacto de DUTY anteriores que el
algoritmo cuenta, incluidos STOP y suplencias según el contrato actual. La
consolidación debe derivarlo de hechos verificables, preservar su revisión y
compararlo con una ejecución íntegra. Cambiar la puntuación cambiaría el futuro.

Conservar íntegros persona, nave, plaza, emisor/autoridad, intervalo efectivo,
actividad, causa, PLAN, ACTIVITY origen, cancelaciones, suplencias, funciones,
nombramientos/revocaciones, carencias y sus resoluciones. No regenerar turnos
pasados desde una semilla. Solo eliminar redundancia sintáctica demostrable:
diccionarios e intervalos compartidos con equivalencia exacta. Un hecho relevante
para misiones conserva sus relaciones completas. Marines, navales Defiant y
civiles mantienen sus IDs, competencias, residencia y cadena de mando.

### Publicación en disco y recuperación previstas

El host realiza E/S a petición de Core; no decide cuál versión del mundo manda.
Preparar nuevos segmentos/checkpoint temporales; cerrar, sincronizar y comprobar
lectura íntegra; preparar manifiesto generación N+1; publicar por reemplazo
atómico del puntero de generación tras asegurar durabilidad. Conservar N y sus
archivos hasta confirmar N+1. El protocolo debe especificar fsync/FlushFileBuffers,
reemplazo y barreras de directorio por plataforma; no asumir garantías de rename
uniformes. Recuperación elige una generación **completa y validada**, nunca mezcla
checkpoints, RNG o segmentos de generaciones distintas. Huérfanos temporales se
ignoran y se limpian solo después de validar referencias. Sin borrado automático
de una campaña válida durante recuperación.

## 6. Migración y compatibilidad

Esta PR no migra ni reescribe partidas, no cambia SCHEMA 3/4, ABI 1, pins, formato
Core ni contratos productivos F04. La migración futura será explícita: leer el
original sin alterarlo, validar, producir un conjunto nuevo, verificar equivalencia
de hechos/IDs/RNG/reloj y futuro, y conservar el original para rollback. El
contenedor tendrá versión propia; solo se propondrá SCHEMA 5 si cambian los
campos semánticos F04 (por ejemplo acumuladores), con justificación y conversión
reproducible. Un lector antiguo debe rechazar el contenedor nuevo claramente;
no se promete lectura inversa de archivos segmentados por DLL antiguas.

## 7. Pruebas existentes, nuevas y pendientes

`tests/persistence_audit.cpp` usa las APIs de producción sin alterarlas. Añade
27 entradas CTest: 15 medidas, cinco recorridos hasta 365 días o rechazo, cinco
continuaciones en proceso distinto, una reproducción 730 Valhalla y la prueba
de límite de identidad. Mantiene las 243 entradas F04 anteriores.

En cada bloque publicado se comparan el futuro sin interrupción y el obtenido
tras cargar, **byte a byte**, con RNG/reloj incluidos; se validan 5/7, una
guardia/día, descanso y referencias de personas/plazas. Se compara el grafo
estático de identidades, competencias, grupos y censo contra el original.
El último checkpoint se continúa en un ejecutable distinto y se compara con el
futuro de A. El rechazo por capacidad se normaliza quitando exclusivamente su
evento y revisión y se exige igualdad de todos los bytes previos.

Las cargas negativas ejercen truncado, magic, checksum, versión desconocida y
un intervalo F04 corrupto dentro de un contenedor Core válido; conservan estado
y handles existentes. Las regresiones existentes cubren bajas, relevos, deuda,
salidas, revocaciones, corrupciones de competencias Marine y migración 3→4.

**Pendiente de implementación genérica:** fallos antes de iniciar archivo,
durante preparación, antes de publicación, entre escritura y confirmación y
durante recuperación; segmento faltante/truncado/reordenado, ID duplicado,
dependencia cruzada inválida, manipulación, manifiesto desconocido, fallo de
durabilidad y rollback. Esos casos son contratos previstos, no pruebas superadas.
Los [vectores de contrato](../../../../../../desarrollo/integration/f04/tests/fixtures/persistence_contract_vectors.json)
enumeran precondiciones, inyecciones y resultados esperados y llevan el estado
`PROPOSED_NOT_IMPLEMENTED_NOT_EXECUTED`; no están registrados como éxitos CTest.
Tampoco se certifica recuperación de historial consolidado, ausente todavía.

Tras autorizar e implementar, exigir 365 días completos por las cinco clases y
730 Valhalla con actividades reales, incidentes, cargas/cierre entre procesos,
consultas antiguas y ventana residente acotada. Comparar hechos y futuro contra
la referencia sin consolidación, además de bytes cuando coincida el formato.
Medir archivos acumulados, consulta, recuperación, archivo y memoria. Las
medidas de consolidación/segmentación actuales son **no aplicables**, no cero ms.

## 8. Unreal y riesgos pendientes

Se conserva Unreal como proyección. Las 25 pruebas Win64 NullRHI verifican el
contrato actual; no hay APIs ni escenas nuevas de archivo. Una integración
futura deberá exponer lectura histórica paginada con errores claros sin Actors
históricos ni cargas gráficas masivas. No hay validación artística nueva.

Riesgos a resolver en Core: referencias cíclicas entre archivo y activo,
conocimiento de observadores, dependencias Timeline, caches, conservación de
revocaciones y transferencias, determinismo de acumuladores, retención de
identidades a décadas y coste del índice de segmentos. El almacenamiento
histórico total seguirá creciendo; el requisito es acotar residencia y trabajo
por operación, conservando la información. No se cifra ni autentica todo el
universo por añadir hashes. Fases clínicas, narrativas y misiones futuras no se
implementan en esta subfase.

**Autorización requerida:** modificar CoreRPG genérico para las capacidades
enumeradas en el apartado 5 y sus pruebas/migración, manteniendo el contenido
Star Trek en F04. Hasta entonces no se cumplen los criterios A–H de aceptación
completa ni se declara terminada PERSISTENCIA-03.
