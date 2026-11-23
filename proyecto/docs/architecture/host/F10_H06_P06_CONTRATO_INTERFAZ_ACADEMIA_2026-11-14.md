# F10 ↔ HOST H06-P06 — Contrato de interfaz para la creación de candidato de Academia

**Fecha:** 14-11-2026 · **Corte:** interfaz de diseño y pruebas estáticas.  
**Responsables:** ChatGPT redacta y contrasta; F10 es propietario funcional; Codex implementará el nativo; H03/H04/H06 lo consumirán.  
**Estado:** **PROPUESTO / CONTRATO DE INTEGRACIÓN**, sin ejecución real ni aceptación formal por un módulo F10 en runtime. No equivale a F10 CORE_INTEGRADO, ni a HU-08 PASS, ni a M1 cerrado.  
**Contrato de datos:** [f10_host_candidate_factory_contract_v0.1.json](../../../../sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json).  
**Bloqueos y evidencias:** [PR #147](https://github.com/robdor80/Videojuego_StarTrek/pull/147) y [issue #148](https://github.com/robdor80/Videojuego_StarTrek/issues/148).

## 1. Decisión técnica de esta propuesta

**Ruta A como objetivo de implementación sujeto a prueba de factibilidad:** desarrollar un factory nativo **F10** para una campaña `starfleet_academy` apoyado en las primitivas ya fijadas de CoreRPG. No transformar una campaña de nave `miranda` ni aprovechar el capitán del fixture. El HOST aloja el servicio en el **mismo ciclo de sesión y único hilo propietario**. Se mantienen intactos los módulos históricos F04/F05 y el pin de CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d`. No se crea un servidor, una base de datos paralela ni un WorldState alternativo.

La ruta A debe superar una **prueba de viabilidad nativa mínima** de catálogo, inicialización, persistencia y restauración; si el pin Core hace imposible la historia de Academia sin modificar componentes congelados, se documentará la limitación y se comparará con la ruta B (extensión aditiva consensuada con F04), **antes de modificar archivos**. No prometer compatibilidad hasta haberla probado.

## 2. Arranque real: primero candidato, después cadete

La secuencia **aprobada como diseño de creación** está en `character_creation_contract_v1_0.json`: era/fecha → perfil del jugador → borrador del personaje → validación objetiva y semántica → bloqueo de biografía → acceso a la Academia. Las dos validaciones son obligatorias; la revisión semántica por IA emite **evidencia revisable**, no capacidad de mutar por su cuenta. Si falta cualquiera, el borrador sigue **sin publicar**. El contrato no prescribe un proveedor de IA externo ni presupone que exista en producción.

Proponemos los estados de entrada:

| Estado | PERSON Core | Plaza de cadete | Poder naval / F11 |
|---|---|---|---|
| `DRAFT` local del editor | **No publicada** | Ninguna | Ninguno |
| `candidate` tras validación y commit F10 | **Sí, una PERSON estable** | **Ninguna plaza de cadete** | Ninguno |
| `admitted` por decisión válida del dominio F10 | Misma PERSON | **Una plaza real consumida**, con cohorte registrada | Ninguno |
| `cadet_year_1` tras incorporación | Misma PERSON | **Se conserva la misma plaza** | Ninguno |

F10 no concede admisión porque el cliente envíe un booleano. Los resultados de ACC-01..05, entrevista y revisión holística se incorporarán mediante hechos autorizados cuando exista el dominio jugable. El usuario no queda bloqueado en el desarrollo de su personaje, pero **un candidato no debe figurar matriculado falsamente**. Si la aprobación tarda, permanece en `candidate`.

**Cronología:** existe aprobación del **año 2383** para el acceso del jugador; **el día y el mes no están decididos**. El factory debe recibir/consultar un contexto de campaña aprobado, y no puede codificar silenciosamente una fecha exacta. El inicio desde Academia no implica que la Enterprise-D, Proyecto Valhalla o una nave fija sea ya su destino.

## 3. Superficie conceptual: todavía NO son funciones compiladas

Estas operaciones describen responsabilidad y pre/postcondiciones; Codex debe materializar sus tipos tras verificar Core, ABI, CMake y persistencia, sin exponer un `F04Session*` a UE:

| Operación conceptual | Dueño | Entrada confiable | Resultado interno / regla |
|---|---|---|---|
| `f10_stage_candidate` | F10 | Borrador aportado por usuario, contextos de campaña y validaciones verificadas **fuera del cliente** | Staging, **sin** efectos persistentes. Si falla la revisión, devuelve correcciones sin publicar PERSON |
| `f10_commit_candidate` | F10/Core | Staging admitido, identificador de intento controlado por HOST, generación y revisión vigentes | Crea PERSON **una vez** y hecho de candidatura, con procedencia. Commit atómico; resultado privado |
| `host_bind_candidate` | H03 | Recibo **interno** de creación F10, sesión, principal y generación correctos | Vínculo local del jugador en el mismo Core, no una marca de iniciativa F05. Sin `person_id` elegido desde UI |
| `f10_confirm_admission` | F10/Core | Decisión basada en evidencia de acceso y revisión actual, plaza real de cohorte disponible | Admisión y reserva/consumo de plaza exactamente una vez. No se confunde con graduación o comisión |
| `host_restore_academy` | H04 | Ranura validada, catálogo/versiones correctos, identidad persistente y hechos Core | Restitución escalonada y atómica; nueva generación y nuevo ámbito, invalidando respuestas anteriores |

Para las operaciones que cambian Core, preferir **staging completo del estado** y publicación de un resultado con `idempotency_key` interno, referencia de campaña, sujeto, revisión, y referencia de hecho histórico. Repetir la misma intención debe devolver el mismo efecto; la misma clave con otra biografía se rechaza. No publicar `BOUND` ni un `COMMITTED` de H04 si falta alguna comprobación. Codex determinará los tipos reales y demostrará qué rollback permite el pin fijado.

**Frontera de confianza:** UE y Blueprints pueden enviar solicitudes de perfil, nunca `person_id`, `F04Ref`, revisión Core, marcador `trusted_origin`, identidad/capacidad institucional, `validated_creation_ref`, emisor o plaza asignada. Un recibo interno obtenido del dominio validado no es una cadena que el cliente pueda escribir. Los datos de un PADD, IA o un sitio web tampoco autentican una admisión.

## 4. Identidad: resolver la ambigüedad de nombres sin romper F11

Hay dos momentos diferentes:

1. El personaje `campaign_created` necesita desde su alta una **identidad genérica estable de personaje** y una `PERSON` del WorldState.
2. F11 reserva su **identidad profesional de 128 bits** para la comisión efectiva como oficial (o migración autorizada), respaldada por `commission_event_id`.

**Propuesta de coordinación F10/F11:** documentar ambas como `campaign_character_identity` y `professional_f11_character_id` en las interfaces internas **conceptuales**; conservar la PERSON y unirlas por una relación duradera única cuando F11 confirme la comisión. Ninguna renumeración de la persona ni asignación de rango se produce al ingresar en Academia. **Pendiente de ratificación conjunta** el nombre/formato de persistencia de ese vínculo, la regla de unicidad y su migración. Los campos actuales `character_id` de los contratos existentes **no se renombran aquí**; sería un cambio de dominio que requiere acuerdo explícito.

La ausencia de la identidad F11 **no bloquea que exista un candidato**. Sí bloquea afirmar que ya es oficial comisionado o concluir la aceptación de continuidad profesional CB-24.

## 5. Separación entre H03, F05 y autorización de órdenes

Hoy el puente resuelve el PERSON mediante `f04_handles`/capitán y `f04_person`, y `PlayerBootstrap::bind` usa `f05_bind_player` de forma obligatoria. Ese contrato es válido para un miembro naval previsto por F05, no para un aspirante del campus.

**Cambio autorizado a diseñar:** un vínculo H03 **de jugador** separable de la iniciativa F05; H03 deberá revalidarlo después de carga. F05 permanece intacto para los miembros y operaciones de nave. El sistema no debe fingir una plaza naval, oficial de puente, cualificación ni categoría de tripulante solo para dejar pulsar un botón. En Academia, `SUBMIT_SCAN` debe denegarse en el HOST antes de cualquier llamada F05 y sin efectos sobre Core, salvo en una práctica futura donde F10/F05 acredite competencia y contexto concretos mediante contrato aprobado. Las auditorías `REFUSED` propias de F05 **siguen vigentes** para órdenes realmente presentadas a ese dominio.

## 6. H04: qué hay que guardar y cómo cargar

La partida de Academia preservará en **un estado Core autoritativo**: identificador estable de campaña, PERSON/identidad de personaje, validación de biografía y hecho de creación, situación académica, plaza/cohorte si fue admitido, vínculo de jugador, historial y reloj. Los recursos 3D, paneles Slate y cachés visuales no son identidades ni hechos persistentes.

La ruta histórica `TREKHOST4 1` de F04/F05 **no se reinterpreta** como Academia. H04 especificará un discriminador de producto, catálogo de Academia y versión de esquema; su nombre/formato final queda abierto a la investigación de Codex. Validará en *staging* procedencia, pertenencia del sujeto y estado académico antes de sustituir la sesión viva. Ante catálogo no reconocido, importación alterada o vínculo incompatible: rechazo **sin swap** y sin limpiar la partida anterior. Reabrir genera ámbito y generación nuevos.

## 7. Plan de ejecución y dependencias concretas

**Tarea A — F10 factory nativo mínimo (Codex):** contrato de construcción de `WorldState` de campus y catálogo, biografía validada, PERSON/historia; `candidate` real antes de admisión, y ensayo de plaza bajo autoridad F10 (sin simular ACC-01..05). Demostrar rechazo con cero efectos e idempotencia. Si no es factible con el pin, informar sin modificar Core.

**Tarea B — H03 vínculo pre-F05 (Codex):** estado BOUND del principal local construido únicamente a partir de resultado de F10, verificado en el único hilo propietario, sin exportar set_player arbitrario. Mantener suite naval F05.

**Tarea C — H04 restore Academy (Codex):** persistir y recuperar PERSON/campaña, discriminador/catálogo, sin pérdidas ni migración silenciosa de saves de nave.

**Tarea D — H06 UE y CI (Codex + auditoría ChatGPT):** ampliar ABI de producto solo después del factory; pruebas multi-UWorld/NullRHI/D3D12, fallo cerrado, reserva/edición, admisión y restauración entre procesos. No usar generador `cadet:proc:` o `CORE_HOST_VERIFIED` de referencia como credencial.

**Puerta A→B:** un candidato real persistente de F10. **B→C:** vínculo duradero en mismo Core. **C→D:** restore multiproceso estable y sin regresión. Si A queda bloqueada, se documenta la falta de runtime y no se simula B/C/D para un falso cierre de M1.

## 8. Evidencia y no regresión

- Nueva matriz de referencia: [H06-P06 CB-01..CB-24](H06_P06_MATRIZ_PRUEBAS_2026-11-13.md), inicialmente **22 BLOCKED y 2 NOT_RUN** según #147. El nuevo contrato no altera estados.
- Mantener 239/239 Windows y Linux y 84/84 ASan/UBSan del corte #147; pasar al menos todas las pruebas nuevas de fábrica, vínculo y restauración, Release OFF, y después UE5.8.2 en MSI.
- Un test estático en `desarrollo/tools/validation/test_f10_host_candidate_contract.py` comprobará únicamente coherencia de **este documento JSON con los contratos existentes**, nunca la creación de PERSON ni el funcionamiento de Core/UE.
- No modificar pins, F04/F05/F11 congelados ni tests históricos. No duplicar UE, assets ni descargas. Temporales solo conforme a AGENTS.md; trabajo en rama/PR y resultados versionados de pruebas.

**Criterio de entrega de este documento:** contrato propuesto + prueba estática PASS en GitHub. **No autoriza declaración IMPLEMENTADO del factory**. La implementación requiere Codex y pruebas separadas con los propietarios F10/H03/H04.
