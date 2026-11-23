# F11-P05-A02-00 — Contrato de identidad, grados y autoridad de Personal de Flota

**Fecha:** 11-11-2026  
**Alcance de este corte:** especificación versionada + pruebas de consistencia **offline**.  
**Próximo corte con C++:** F11-P05-A02-01 (primer ascenso real de alférez a teniente júnior).  
**Estado real:** **CONTRATO**, no `CORE_INTEGRADO`, no `UE5_JUGABLE`.

## 0. Lo que hemos decidido y lo que NO hemos demostrado

Se establece una **identidad permanente de carrera**, una **tabla explícita y versionada de códigos de rango**, un **dominio separado de autoridad de Personal de Flota** y una **operación propuesta** de promoción autoritativa, atómica, idempotente y recuperable tras guardar/cargar.

El contrato ejecutable de datos reside en `sistemas/gameplay/careers/promotions/f11_p05_a02_00_personnel_contract_v0.1.json`. Este documento lo explica y delimita. El código Python asociado **solo comprueba coherencia documental**, no concede un solo rango.

La identidad entre diferentes naves y el coordinador global de Flota seguirán necesitando **implementación y validación real en P05-B3**. Crear un UUID no garantiza por sí solo la atomicidad multiunidad.

## 1. Identidad profesional de una persona

### Identificadores diferentes, usos diferentes

| Identificador | Qué representa | Reutilización prevista |
|---|---|---|
| `F04Ref(scope,id)` | Referencia a entidad dentro de **una sesión F04 viva** | APIs de la nave; **caduca al cargar/cambiar de sesión** |
| `person EntityId` | Identificador numérico Core en **un WorldState** | Referencia local a la persona; no identifica a la persona de otra nave |
| `ship_identity` | Identidad de una nave de campaña | No representa a un oficial |
| **`character_id`** | Identidad profesional permanente y opaca de la persona | Expediente, ascensos, relaciones y **futuros** traslados |
| `rank_event_id` | Hecho histórico que originó el rango actual | Evita usar evaluaciones y órdenes pertenecientes a otro tramo |
| `commission_event_id` | Acto autorizado que comisionó al oficial | Prueba imprescindible de pertenencia al escalafón de oficiales |

**Formato de diseño:** `character_id` de 128 bits, expresado fuera de Core como 32 dígitos hexadecimales minúsculos. Para registrar el valor en los campos numéricos de F04 (máximo **48 bits**), se divide sin pérdida en tres fragmentos de **48 + 48 + 32 bits**. La implementación deberá garantizar que no se truncan, invierten ni mezclan al guardar.

La identidad **se crea una sola vez** desde el Host confiable, en el acto de comisión o en una migración explícita avalada por hechos previos. Queda ligada a la misma persona del `WorldState`. No debe depender de su nombre, nave, plaza, rango, `EntityId`, seed o sesión. El jugador y los NPC comparten esta regla.

**Invariantes:**

1. Un `character_id` no puede corresponder a dos personas dentro del mismo estado.
2. Una persona comisionada no puede tener dos `character_id` distintos.
3. Ausencia de comisión/historial válido = **no se puede promocionar como alférez**.
4. Los identificadores ya presentes en guardados anteriores se **conservan**. Los antiguos personajes sin identidad F11 no se transforman silenciosamente en oficiales de carrera.
5. Los futuros traslados entre naves necesitan una autoridad global que reconcilie identidad, plazas e historia. **No** se copia el NPC como persona nueva de una sesión a otra.

**Límite técnico concreto:** hoy la mayoría de personas de las plantillas F04 nacen con `RANK=0` y sin carrera comisionada. El primer ensayo C++ deberá **crear o importar un oficial realmente comisionado mediante una vía de confianza**. No puede interpretar automáticamente `RANK=0` como alférez.

## 2. Códigos de rango: no mezclar tres escalas distintas

Se han contrastado `mundo/lore/federation/starfleet/ranks/officer_ranks.json`, `rank_insignia_standard.json`, F11-P01/P03 y el código de F04.

En **F04 histórico**, el arranque de una partida sintética incluye `RANK=8` para el capitán de ejemplo, `RANK=10` para otro personaje de ejemplo y `RANK=1` para varios tripulantes; además, otras plantillas usan `RANK=0` como pendiente de autoría. Esos números **no están certificados como un mapa completo del escalafón de oficiales**. Por su parte, `officer_ranks.json` utiliza `order=8` para **contraalmirante**. Traducir el campo numérico por posición en el catálogo sería un error grave.

**Decisión del contrato F11:** reservar un espacio nuevo y explícito para oficiales comisionados **v1**, sin reinterpretar valores antiguos:

| ID semántico canónico | Grado | Nuevo valor del campo `RANK` | Insignia |
|---|---|---:|---|
| `ensign` | Alférez | **1101** | ● |
| `lieutenant_junior_grade` | Teniente júnior | **1102** | ●○ |
| `lieutenant` | Teniente | **1103** | ●● |
| `lieutenant_commander` | Teniente comandante | **1104** | ●●○ |
| `commander` | Comandante | **1105** | ●●● |
| `captain` | Capitán | **1106** | ●●●● |

**El nuevo código solo tiene significado profesional F11 si aparece unido a un `commission_event_id` autorizado, `character_id` válido y un `rank_event_id` histórico.** Un valor `1101` introducido manualmente por un cliente, una importación incompleta o una modificación de un archivo de guardado no comisiona a nadie.

La escala de cadetes y la de alistados/suboficiales son independientes. Los grados de comodoro, almirantes y capitán de Flota se preservan como IDs del lore, pero **no se asignan nuevos códigos F11 en A02**, donde solo se prueba el primer ascenso.

**Nunca usar `rank+1` como autorización:** que los seis códigos sean consecutivos facilita leerlos, pero la validez de una promoción la impone el **par exacto** de grados permitido en el contrato, no una suma.

**Compatibilidad:** el cargador debe aceptar y conservar guardados legacy sin forzar conversión. Valores 0/1/8/10 y cualquier valor antiguo sin procedencia verificada se **tratan como legacy/no mapeados para promoción F11**; no se convierten automáticamente. Si una partida antigua necesita integrarse con F11, se exigirá migración autoritativa explícita, con copia de seguridad y auditoría.

## 3. Quién tiene derecho a ascender oficiales

La regla vigente de F11-P01 es **rango ≠ puesto ≠ autoridad de Personal de Flota**. Lo mantenemos también durante el ascenso.

- **Capitán de nave:** recomienda, evalúa profesionalmente cuando corresponda, informa y comunica ceremonias. **No** concede una promoción de Flota por su puesto de mando.
- **Almirante por rango:** no tiene automáticamente autorización para alterar expedientes; debe estar destinado o expresamente habilitado en la autoridad institucional pertinente.
- **Oficina de Personal de Flota:** órgano con ámbito de promoción, manifestado mediante **concesión de autoridad viva y verificable**.
- **Delegado de Personal de Flota:** únicamente si existe una delegación formal vigente del mismo ámbito; no sirve la simple delegación táctica de F04/F05.
- **IA, jugador, PADD, Blueprint, consola:** pueden solicitar o presentar resultados, nunca autenticar órdenes de personal.

### Cadena de confianza obligatoria

1. El **Host nativo confiable** identifica la autoridad emisora (persona u órgano legítimo), con una raíz de confianza establecida por bootstrap autorizado.
2. El sistema conserva en el mismo `WorldState` una **concesión institucional de Personal de Flota** cuyo origen, titular, ámbito, ventana temporal y revocación se pueden comprobar. No se acepta un booleano `verified=true` enviado por cliente.
3. Una **orden de Personal de Flota** válida referencia la concesión, al oficial, al grado anterior y al nuevo, a la evaluación y a la causa. Su identidad y aprobación se verifican en Core/Host.
4. **En el instante de confirmación** se comprueban de nuevo concesión, orden, comisión, evaluación, rango anterior, reloj, alcance y revisión del mundo.
5. Solo entonces se publica conjuntamente el nuevo grado y el evento histórico.

**Separación de F05:** F05 reutiliza la misma sesión F04 y sus mecanismos de idempotencia/historia, pero su orden actual solo ejecuta `F04_SCAN`. **No** se cambia esa orden ni se finge que una instrucción de Sensores es una orden de promoción. Se propone una vía nativa de personal F11 **dentro de la sesión existente**, con un contrato propio de autorización y deduplicación.

**Decisión técnica y frontera:** la raíz de confianza y la concesión se exponen **solo mediante bootstrap nativo privado**, nunca como operación pública de F04 que un NPC/usuario pueda simular. A02-01 implementará y probará el mecanismo real; su forma concreta de representación Trek (entidad, relaciones y comprobaciones estrictas) deberá ajustarse al validador existente sin añadir otro almacén de estado.

## 4. La primera operación que implementará Codex en A02-01

**Nombre provisional de la API C:** `f11_commit_promotion` sobre **`F04Session*`**, con `F11PromotionRequest` y `F11PromotionReceipt`. No es todavía una función existente; definir su ABI exacta y compatible será parte del cambio C++.

**Alcance deliberadamente mínimo:** promoción **alférez (1101) → teniente júnior (1102)** de una persona existente, comisionada, en servicio, con evaluación y autorización legítimas. En esta primera operación **no hay traslado ni cambio de plaza**.

### Entrada conceptual obligatoria

`session_scope_ref, expected_world_revision, idempotency_key, subject_character_id, subject_local_ref, issuer_authority_grant_id, approved_personnel_order_id, verified_evaluation_event_id, commission_event_id, expected_rank_event_id, expected_from_rank_id, requested_to_rank_id, effective_tick, cause_event_id`.

Los campos acabados en `_id` de autoridad/orden/evento son **referencias a hechos que ya existen y pueden verificarse** en el estado autoritativo; **no son tokens, cadenas o afirmaciones del cliente**. El usuario no puede acreditarlos rellenando una estructura arbitraria.

**Reglas:** la revisión debe coincidir con el `WorldState` actual; el tiempo efectivo corresponde al instante de campaña de la ejecución (en A02 no programamos futuras promociones); el grado previo debe coincidir tanto con la proyección actual como con el evento histórico; la evaluación debe pertenecer al mismo tramo profesional y a la misma identidad.

### Salida y efectos

**Si se aprueba:**

- Cambia únicamente el **grado** de la persona; no cambia su unidad, plaza, departamento, nombre, competencias, turno ni permisos.
- Se añade **un único evento `promotion`** al expediente append-only, vinculado a comisión, evaluación, acto de autoridad, orden, grado anterior y nuevo, fecha y causa.
- El `rank_event_id` actual pasa a identificar ese evento. La proyección `f04_person` devuelve **1102** tras confirmar el commit.
- La transacción se aplica sobre una **copia validada de la campaña**, siguiendo el patrón F04. El mundo original no puede observar o guardar «grado nuevo sin expediente» ni «expediente sin grado».
- Se genera un recibo persistente con identidad de promoción, sin prometer un traslado o un puesto.

**Si se rechaza:** ningún cambio en rango, expediente, concesiones, plazas o RNG por esa operación. Si se desea una auditoría de denegación, debe mantenerse separada de la transacción de promoción y justificar por qué no viola «sin efectos»; no equivale a ascenso.

### Reintentos

| Caso | Contrato |
|---|---|
| Primera orden válida | Aplicar y registrar una promoción |
| Misma clave + misma petición tras variar revisión | Recuperar recibo original; **sin nueva promoción** |
| Misma clave + petición distinta | **Conflicto**; no modificar |
| Reintento después de guardar/cargar | Idéntico resultado de expediente, sin segundo evento |
| Error/fallo inyectado a mitad de preparación | No publicar ni rango ni evento |
| Clave repetida con autorización ya revocada después del primer commit | Consultar **recibo pasado** no otorga una nueva autoridad |
| Estado antiguo o ya promocionado y clave nueva | Denegar; no volver a promover |

La deduplicación se basa en identificadores profesionales y el contenido semántico de la orden, **nunca únicamente en el `F04Ref` local** porque cambia al recargar.

## 5. Datos exactos que deberán guardarse en Core

El expediente `service_record_model.json` ya declara `promotion` con `event_id, date, event_type, authority_id, assignment_id, position_id, rank_id, reason, source_event_id, notes_structured`. **Reutilizar ese esquema conceptual**, añadiendo referencias de relación a la misma identidad, evaluación, comisión, orden y rango anterior. No abrir un JSON o SQLite paralelo con la «verdad» de la carrera.

- Persona: identidad persistente F11, comisión y referencia al evento vigente de grado.
- Autoridad: concesión verificable, cadena de procedencia, ámbito y revocación.
- Orden: propuesta/aprobación y llave idempotente, vinculadas a autoridad y beneficiario.
- Promoción: evento histórico inmutable, con grado anterior/nuevo y fecha.
- Histórico segmentado: retener identidad, concesiones relevantes, evento actual de rango y **tombstones de deduplicación** aunque se consoliden hechos antiguos.

**Compatibilidad de guardados:** los archivos anteriores siguen cargando. La extensión de F11 es **opt-in y versionada**; no reescribe un fichero legacy durante una mera lectura. Los archivos nuevos que contengan hechos F11 podrán requerir un lector actualizado; nunca realizar una conversión silenciosa descendente que elimine autoridad o expediente.

**Reserva en esquema F04:** la implementación tiene que incorporar explícitamente cualquier nuevo campo de persona y cualquier clase de registro F11 al validador estricto de `f04_bridge.cpp`. No basta con que CoreRPG acepte una relación genérica: F04 rechaza campos/relaciones desconocidos. No tocar las enumeraciones antiguas en su numeración; añadir símbolos y límites de extensión con tests de ABI.

## 6. Validación A02-00 (sin ejecutar un ascenso)

Las pruebas offline de este contrato comprobarán:

- Rango, orden y seis insignias coinciden con los catálogos aprobados F11/P01/P03.
- Códigos F11 únicos, distantes de los valores antiguos observados, y `1101 → 1102` es el único cambio autorizado en A02.
- Un rango no equivale a un cargo F04 y un mandato de F05 no equivale a Personal de Flota.
- Identidad F11 de 128 bits: fragmentos 48+48+32; ninguna `F04Ref` se acepta como identidad global.
- Expediente e identidad tienen fuente de comisionamiento y relaciones de eventos.
- Autoridad de Flota no puede proceder de cliente/IA; recomendación del capitán no otorga grado.
- Reintentos, guardados, revisiones obsoletas, estados legacy y promociones indebidamente saltadas **figuran como denegaciones obligatorias**.
- La configuración del contrato no declara que exista aún C++ o UE5.

**La CI de A02-00 puede demostrar coherencia del contrato y ausencia de regresiones en las 292 pruebas de referencia. No demuestra un solo ascenso real ni compila CoreRPG.**

## 7. Puerta exacta A02-01 (ya preparada para Codex)

La tarea de Codex deberá quedar acotada a **un único cambio C++ nativo y sus pruebas**, compatible con los SHAs fijados de F04/F05 y el CoreRPG actual. Orden de desarrollo:

1. Implementar identidad/commission en WorldState **sin falsificar graduaciones**. Crear fixture de oficial comisionado mediante entrada confiable, no con `RANK=0` reinterpretado.
2. Crear ruta privada de autoridad de Personal de Flota autenticada y contrato de orden/suceso verificable.
3. Ejecutar la operación `ensign 1101 → lieutenant_junior_grade 1102`, con staging, historial y deduplicación en Core.
4. Verificar conservación de destino/puesto y comportamiento del capitán actual.
5. Probar errores, repetición de key, cambios de revisión, fallos inyectados, reconstrucción tras carga y compatibilidad de archivos viejos.
6. Pasar las regresiones F04/F05 actuales y las suites F11. Para artefactos temporales usar **`laboratorios/f11/p05-a02-01/`**, ignorado y eliminable. No editar Core salvo que se demuestre imprescindible; si sucede, PR independiente.

**Modelo recomendado para esa implementación:** Codex GPT-6, **pensamiento Alto**, no Instant. No lanzar Codex automáticamente por aprobar la especificación A02-00.

**Aceptación de A02-01:** un oficial realmente comisionado obtiene un ascenso que sobrevive al guardado/carga, con una orden de Personal de Flota válida, sin perder identidad ni plaza y sin efectos colaterales. **A02-00 termina cuando se fusionan contrato y pruebas documentales; A02-01 sigue pendiente.**
