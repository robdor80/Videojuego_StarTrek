# HOST H06 / IA-03B01 — Arquitectura de protagonista S04 v2, PERSON y campaña Academia

**Fecha:** 20-11-2026. **Responsable:** ChatGPT (arquitectura). **Estado:** DISEÑO DE INTEGRACIÓN PROPUESTO / NO IMPLEMENTADO / NO PROBADO EN RUNTIME. **Rama de trabajo:** chatgpt/host-h06-ia03b01-arquitectura-s04-v2-20261120.
**Decisión superior:** DEC-0022, 17-11-2026. **Ámbito:** IA-03B02 (factory candidato) e IA-03B03 (identidad/guardado), y condiciones de entrada de IA-03C; no constituye certificación M1.
**Restricción:** conservar el pin CoreRPG 76a7b7b485616d8c4994f384a90f123bf333591d, los contratos LOCKED v1, F11 y las regresiones históricas.

## 1. Dictamen y precedencia

La ruta de creación libre de IA-03A, fusionada por PR #167, es infraestructura histórica válida para borradores de jugador, pero **no es el nuevo flujo productivo de Star Trek Legends**. DEC-0022 y S04 v2 establecen un único arquetipo fijo: varón híbrido humano-vulcano, 45 años al entrar en la Academia de 2383, madre vulcana, padre humano descendiente de Khan Noonien Singh, cuatro dominios marciales, vocación científica y antecedentes civiles. El jugador cambia **nombre y presentación cosmética autorizada**, no especie, sexo, edad, ascendencia, historia ni aptitudes base.

Un nuevo inicio de campaña materializará **una PERSON distinta y duradera por campaña** a partir del **mismo arquetipo biográfico autoral**. La biografía fija no convierte todas las campañas en una única entidad compartida ni permite múltiples PERSON jugables dentro de la misma campaña.

La prioridad de las fuentes para este corte es: (1) DEC-0022; (2) S04 v2 y su biografía canónica aprobada; (3) reglas de dominio y autoridad F10/CoreRPG y contratos LOCKED que exigen compatibilidad/versionado; (4) contratos de infraestructura HOST H02–H06; (5) referencias históricas del creador libre IA-03A y ensayos de factibilidad. Una norma histórica incompatible NO se sobrescribe: se crea una **ruta v2 explícita** y se conservan regresiones v1.

### Evidencia examinada en main el 20-11-2026

| Fuente real | Hecho comprobado | No demuestra todavía |
| --- | --- | --- |
| sistemas/gameplay/character_creation/s04_fixed_protagonist_contract_v2.json y s04_protagonist_biography_v1.json | Contrato y biografía del arquetipo; datos pendientes etiquetados como desconocidos | PERSON materializada, capacidades Core o aprobación F10 de producto |
| sistemas/gameplay/character_creation/S04_MIGRACION_F10_HOST_v2.md | Migración del creador libre al héroe fijo diseñada | Código F10/IA-03A migrado |
| desarrollo/integration/host/src/f10/biography_validation.cpp y biography_profile_source.h | IA-03A validada con recibo y perfil temporal H03; aún admite tres especies | Elegibilidad de arquetipo fijo ni sustitución de la puerta semántica v1 |
| desarrollo/integration/host/tests/academy_core_feasibility.cpp | El Core fijado permite construir campus, cohorte, PERSON y hecho de candidatura y recuperarlos en un ensayo aislado | Factory de producto; el ID PERSON=4, tick=31 y el catálogo del ensayo son **solo fixtures** |
| desarrollo/integration/host/src/player_bootstrap.h y native_session.h | H03 prepara un sujeto y hoy enlaza vía F05 en campaña de nave | Vínculo legítimo de un candidato de Academia sin F05 |
| desarrollo/integration/host/src/f04_session_bridge.cpp, slot_store.h | H04 restaura mediante una sesión F04 Miranda y comprueba un vínculo F05 | Restore de Academia o guardado compatible sin discriminador nuevo |
| juego/UE5/StarTrekRPG/StarTrekRPG.uproject, PR #186 | Proyecto principal UE 5.8.4 preparado y reparado para autoría; H06 diagnóstico existe | Nueva partida/candidato Core desde UE, escena artística o entrada real Academia |
| PR #185 y README HOST vigente | Servicio IA común sin límite vitalicio de 200, prioridad DIALOGUE y CI ampliada | Llamada LIVE o consumo por NPC/ordenador |

## 2. Responsabilidades y límites

| Propietario | Responsabilidad en IA-03B | Prohibiciones |
| --- | --- | --- |
| **S04 / autor** | Único arquetipo canónico, campos inmutables y pendientes; personalización permitida | Inventar padres, planeta natal, títulos o genética detallada |
| **F10** | Reconoce fuente autoral versionada, valida elegibilidad y candidatura; gestiona por separado admisión/cohorte | Entregar plaza o aprobar examen por un booleano UI o por narración |
| **CoreRPG** | WorldState único, identidad PERSON, hechos, relaciones, tiempo e historial persistente | Mutaciones provenientes directamente de IA/Blueprint |
| **HOST H02/H03** | Único SessionOwner/hilo propietario, perfil local, activación, vínculo verificado y generación | Confiar en person_id, campaign_id, scope, emisor, rank o flags del cliente |
| **HOST H04** | Slot Academy tipado, publicación segura, restauración escalonada y verificación de identidad | Abrir Miranda y llamarla Academia; convertir slots navales silenciosamente |
| **IA-01/IA-02** | Servicio común y revisión lingüística cuando el contrato requiera realmente contenido libre | Aprobar hechos del mundo, rangos, genealogía o plaza; fuente de procedencia |
| **F05/F11** | Siguen gobernando sus competencias navales y hechos profesionales | Enlazar cadete como capitán F05 o comisionar un aspirante |
| **UE5 / IA-03C** | Intenciones, nombre, cosmética, estados de interfaz e intro | Decidir PERSON, admisión, identidad o permisos |

**No crear** otro servidor, base de datos maestra, WorldState, autenticación remota, emisor F11 o servicio de IA paralelo. Uso exclusivamente local y privado.

## 3. Perfil canónico: datos confiables y huecos auténticamente desconocidos

El archivo S04 v2 **no es** un token de autorización porque su ruta aparezca en un formulario. Un compositor **interno F10**, al iniciar una campaña, selecciona la versión aprobada de la fuente autoral y verifica identidad/versiones/huella de su contenido. La UI únicamente solicita creación y aporta campos editables autorizados.

### Inmutables conocidos

- species_id = human_vulcan_hybrid; presentación/sexo = male; edad de entrada = 45 años terrestres, año de inicio = 2383; nacimiento aproximadamente 2338, sin día/mes impuesto; apariencia humana aproximada de 30 años.
- Madre biológica vulcana y padre humano **descendiente** de Khan Noonien Singh; no afirmar que Khan sea el padre directo ni crear una cadena genealógica inexistente.
- Manifestación extraordinaria individual de rasgos físicos y reflejos, no invulnerabilidad ni poderes telepáticos automáticos.
- Antecedentes civiles; formación marcial en kung-fu, karate, aikido y Suus Mahna; autocontrol emocional aprendido, interés por ciencias/astronomía y música.
- Sin servicio previo Starfleet, sin comisión/rango F11, sin autorización clasificada, sin matrícula académica creada por el formulario; la admisión requiere acto separado F10.

### Campos que permanecen DESCONOCIDOS

Lugar natal, día/mes, nombres y ascendencia detallada de los padres, fechas/maestros de cada disciplina, grados académicos concretos, instrumentos musicales, escalas numéricas de fuerza/habilidades y datos exactos del consejo. Se conservan **ausentes/nulos en el modelo autoral** y NO se rellenan mediante IA ni por Codex. Si un contrato v1 exige una cadena en la representación de transición, F10 v2 debe ofrecer una **representación explícita de desconocido**, con significado neutral y sin crear un planeta, fecha, diploma o pericia. Una cadena de presentación como “no especificado” jamás se materializa como lugar real. Si una regla LOCKED no admite esa representación, crear el contrato v2 aditivo correspondiente antes de publicar PERSON; **no falsificar** un dato esencial solo para pasar el validador.

### Editables autorizados

Nombre diegético y, cuando se habilite, apelativo y ajustes de peinado, barba, rasgos faciales menores y uniforme compatible. El alias del perfil H03 no equivale al nombre del personaje. Validar longitud/formato y límites reales del adaptador; ninguna opción visual puede cambiar especie, sexo, edad, parentesco, competencias o hechos. La persistencia de apariencia final corresponde a IA-03C; B02 conserva como mínimo el nombre sin alterar la ficha.

## 4. Contrato de validación F10 v2 — sin certificados ficticios ni IA redundante

La revisión IA-03A v1 fue diseñada para **biografía libre no confiable**, por lo que su doble puerta objetiva/IA-02 era apropiada. Para S04 v2 el pasado completo procede de una **fuente autoral fija**, no de una narración escrita por el jugador: **no hay nada que OpenAI deba volver a inventar, corregir o certificar** en cada nueva partida. La propuesta es una vía F10 v2 determinista de **perfil autoral validado + personalización permitida**, con procedencia y prueba de consistencia; IA-02 queda intacta para biografías libres legacy, futuras entradas realmente libres u otros usos autorizados. No duplicar llamadas de API ni simular una respuesta COHERENT.

**Puerta obligatoria de compatibilidad:** el contrato LOCKED character_creation_contract_v1_0.json y el factory propuesto v0.1 describen revisión semántica para el creador libre. B02 **no debe saltarse** esa puerta dentro de la ruta v1. Debe versionar/documentar **un contrato F10 v2 diferente** para fuente fija antes de implementar la elegibilidad determinista. Si no puede hacerlo sin invalidar autoridad/ABI o pruebas históricas, documentar el bloqueo y detener solo la publicación de candidato: no fabricar recibos IA ni cambiar contratos LOCKED.

**Secuencia F10 de perfil fijo:**
1. HOST inicia un ámbito local y un intento interno (idempotencia), sin aceptar desde UI IDs o huellas autoritativas.
2. F10 carga/selecciona el paquete canónico aprobado (contrato y biografía) **en lado confiable**, verifica su versión/huella y las restricciones de 2383, sexo, especie, edad y ausencia de estatus Starfleet.
3. F10 aplica únicamente las personalizaciones autorizadas y trata los campos desconocidos sin inventar hechos.
4. F10 emite un resultado interno de elegibilidad para **candidatura**, vinculado a arquetipo, versión, huella, contexto H03/generación y el payload editable canónico.
5. CoreRPG solo puede recibir alta a través del factory F10 en el hilo SessionOwner; ninguna respuesta de IA, aprobación visual o texto externo basta.
6. F10 rechaza perfil autoral alterado/desfasado o cambios no autorizados, sin publicar PERSON ni consumir plaza.

Los contenidos biográficos autorales fijos pasan a PERSON como **hechos iniciales reales que las reglas Core/F10 puedan representar**; no se reducen a prompt decorativo. Las traducciones a fuerza, destreza o combate requieren reglas numéricas/sistémicas de dominio **todavía no acordadas**: conservar el antecedente y marcar explícitamente esa dependencia, sin inventar puntos, propiedades imposibles o declarar capacidades jugables ya certificadas.

## 5. Contrato de creación mínima — IA-03B02

### Estados lógicos

- **NO_CAMPAIGN**: sin campaña Academia publicada.
- **STAGED**: catálogo, fuente, identidad e intención comprobados; no existe PERSON visible ni plaza consumida.
- **CANDIDATE**: CoreRPG contiene **exactamente una PERSON** del protagonista, identidad estable, relación/historia de creación F10 y antecedentes conocidos, sin plaza ni rango.
- **BOUND**: además, H03 ha vinculado el perfil local a esa PERSON en la **misma** campaña/generación, sin pasar por f05_bind_player.
- **SAVED**: H04 ha publicado de forma verificable un slot tipado Academia que contiene la identidad, estado, historia y vínculo.
- **ADMITTED / CADET_YEAR_1**: estados académicos **posteriores** por acto formal F10 con plaza/cohorte y prueba autorizada. No son estados que emita B02 solo por crear la PERSON.

Estas etiquetas son **conceptuales** para diseño; Codex elegirá nombres/tipos/errores nativos tras estudiar el pin. No introducir una segunda máquina de estados autoritativa fuera de CoreRPG.

### Operaciones conceptuales (NO existen todavía como API)

| Operación | Dueño | Entrada confiable | Salida/Efecto |
| --- | --- | --- | --- |
| initial_profile_context | HOST H03 | SessionOwner CLOSED, principal local real | ámbito/generación solo internos |
| f10_validate_fixed_profile_v2 | F10 | fuente canónica interna + personalización limitada + contexto | elegibilidad privada vinculada, sin mutación |
| f10_stage_academy_candidate | F10/Core | elegibilidad vigente + catálogo Academy compatible | WorldState preparado, sin publicación |
| f10_commit_academy_candidate | F10/Core sobre owner thread | staging + intento interno y campaña vigente | una PERSON y hecho candidate_created; recibo privado |
| host_bind_academy_player | H03 | recibo privado + PERSON Core revalidada | vínculo único en campaña Academia |
| host_save_academy / host_restore_academy | H04 | campaña tipada, historia, vínculo y slot con procedencia | recuperación segura mismo sujeto, nueva generación |
| f10_admit_candidate | F10 (fase de admisión, fuera de B02) | resultado académico válido + plaza real | mismo sujeto, una plaza consumida, hecho institucional |

**El recibo interno de creación** no es un valor que UE pueda inventar; debe transportar la relación exacta entre campaña persistente, generación/ámbito, identidad local H03, PERSON creada por Core, revisión y fuente/versiones F10, huella de datos, identidad del intento y referencia del hecho de candidatura. La forma binaria/estructura final será propuesta por Codex y verificada con sus capacidades reales. Un número de entidad mostrado en pantalla es solo una proyección, nunca autoridad.

### Publicación e idempotencia

- Preparar catálogo, persona, relaciones, hechos y vínculo **antes de exponer éxito**. Si no se puede garantizar que vínculo y alta se publiquen de forma atómica con el pin, implantar staging/copias y rollback **demostrados**. Nunca dejar una campaña activa a medio vincular tras un error.
- Una clave de intención **interna al HOST y persistible por campaña** se vincula al arquetipo, huella autorizada y nombre aceptado. Repetir el mismo intento devuelve el mismo resultado; misma clave con datos diferentes = CONFLICT sin efectos.
- No crear segunda PERSON en el mismo inicio ni al pulsar de nuevo, reproducir intro, reabrir vista, recuperar una ranura o repetir solicitud tras timeout.
- La estabilidad se exige dentro de la campaña: **nueva campaña** = nueva PERSON e identidad Core, **misma campaña** = misma PERSON. Sin identificador global de usuario/persona elegido en UI.
- No afirmar durabilidad ante corte eléctrico **antes de que H04 haya publicado un slot**. B02 garantiza atomicidad de sesión y reintentos; B03 garantizará recuperación entre procesos tras guardado confirmado.

## 6. Identidad H03 y persistencia H04 — IA-03B03

**Problema verificado:** PlayerBootstrap::bind termina en f05_bind_player y el puente H04 actual restaura con f04_create("miranda"). Es correcto para el producto naval anterior, **no para Academia**.

**Solución de integración propuesta, sin tocar el carril naval:**
- Extender con discriminador de tipo de campaña en la composición de SessionOwner/NativeSession; aceptar ACADEMY solo a través de un creador/lector F10 validado. Mantener una única sesión activa y un único hilo dueño.
- Añadir vínculo académico H03 ligado a identidad de campaña y PERSON real; no generar hecho de tripulante F05 ni introducir una cuenta/tabla autoritativa paralela.
- Establecer sobre duradero de ranura Academy con tipo, versión, referencia de catálogo/hash, campaña, identidad local, PERSON y comprobación de hecho de creación; conservar formato TREKHOST4 1 como naval, sin reinterpretación silenciosa.
- En LOAD, leer metadatos/catálogo permitidos, construir WorldState **en staging**, comprobar PERSON única, rol candidato/admitido según hechos, vínculo y procedencia, y **solo entonces** sustituir la sesión activa y renovar generación, invalidando tickets/vistas anteriores.
- Rechazar un slot naval por ruta Academy y viceversa, versión desconocida, alteración de identidad, catalogo incompatible, revisión/huella inconsistente y enlace a persona inexistente. Importaciones sin procedencia confiable no activan campaña.
- H04 guarda hechos y referencias una sola vez, no 20 copias de la misma biografía; archivos 3D, audio, imágenes y texturas pertenecen a contenido, no a la ficha o historial.
- No fusionar B03 como “guardado Academy probado” si el restore real depende aún de f04_create("miranda").

### Frontera de admisión e intro

DEC-0022 pretende que el prólogo concluya en ingreso y que el juego empiece como cadete, pero **el apoyo del consejo y el discurso de Picard no son por sí mismos un acto académico válido**. B02 puede entregar CANDIDATE; B03 puede guardar/restaurar CANDIDATE. El alta ADMITTED/CADET_YEAR_1 y la plaza real requieren una operación F10 independiente con evidencia de admisión, cuya implementación se coordinará con H06-P06/IA-03C sin reexaminar artificialmente al jugador ni inventar aprobados. Se almacenará la referencia del acto para que saltar o repetir la cinemática no lo duplique. Si tal acto no existe aún, la interfaz mostrará CANDIDATE; **no afirmar Academia jugable M1**.

## 7. Reparto en tareas y puertas de integración

| Subfase | Responsable | Entrega y criterio mínimo |
| --- | --- | --- |
| **B01 — presente** | **ChatGPT** | arquitectura, contrato conceptual, matriz de pruebas y encargo B02; documentación en PR Draft |
| **B02 — factory F10/Core** | **Codex GPT-6, Alto** | fuente fija v2 + prueba de validación/autoridad + PERSON candidato real, idempotencia y rollback; PR Draft; sin H04/Unreal |
| **B03 — H03/H04 Academy** | **Codex GPT-6, Alto** | identidad académica duradera, slot tipado y restore multiproceso; regresión naval; PR Draft separado tras B02 |
| **B04 — auditoría** | **ChatGPT** | auditoría del código, tests, CI y acta por alcance; nunca certificar lo no probado |
| **IA-03C** | **Codex + ChatGPT** | ABI/UE 5.8.4, nombre/cosmética, inicio/intro y pruebas NullRHI/D3D12 en MSI; no introducir en B02 |

**Puertas:** B02 no se considera terminada con el fixture de factibilidad; B03 no comienza como producto sin PERSON real de B02; IA-03C no simula un cadete ni consume un candidato fake para “cerrar” M1. No actualizar pines ni contratos LOCKED por comodidad.

## 8. Riesgos que B02 debe comprobar antes de codificar

1. **P0 — Contrato semántico v1 frente al nuevo perfil fijo.** Resolver mediante ruta F10 v2 explícita con fuentes autorales; nunca fingir IA-02 COHERENT ni relajar v1.
2. **P0 — Factory Core Academy sigue siendo un ensayo.** Probar catálogo y materialización en módulo productivo, idempotencia y fallo de publicación sobre el pin.
3. **P0 — H03/H04 son navales.** No enlazar candidato con F05 ni restaurar un barco como Academia; dejar B03 como dependencia visible.
4. **P1 — Huecos del canon.** Preservar null/unknown reales; no fabricar planeta, padres, títulos o día exacto para pasar los contratos.
5. **P1 — Capacidades S04.** Antecedentes verdaderos, sin cifras ni efectos de juego falsamente declarados; coordinación de dominio para mecánicas reales más adelante.
6. **P1 — Narrativa de admisión.** Separar CANDIDATE de ADMITTED, hechos de Picard/Janeway y su conocimiento de la comisión F11.
7. **P1 — Compatibilidad.** Pruebas legacy IA-03A, F04/F05/H03/H04, F11 y saves navales; no degradar el servicio IA central PR #185.
8. **P2 — Escenario de uso exclusivamente privado.** Evitar servidores, DRM, burocracia de certificados y seguridad frente al dueño del equipo fuera de amenaza real.

## 9. Evidencia y aceptación del diseño B01

Documentos de esta entrega:
- H06_IA03B01_ARQUITECTURA_S04_PERSON_ACADEMIA_2026-11-20.md (este informe).
- H06_IA03B01_CONTRATO_INTEGRACION_v0.1.json (contrato legible por máquina, **propuesto**).
- H06_IA03B01_MATRIZ_ACEPTACION_2026-11-20.md (oráculos **aún no ejecutados**).
- H06_IA03B02_ENCARGO_CODEX_2026-11-20.md (handoff enfocado a B02, sin gastar cuota ahora).

**B01 cerrable documentalmente** si las fuentes, estados, campos y restricciones son coherentes, el contrato JSON es válido y se mantiene la separación CANDIDATE / ADMITTED / CADET_YEAR_1. No declarar IA-03B implementada/probada/certificada por publicar documentos. Ningún cambio runtime, ningún CTest/UE5/OpenAI LIVE ejecutado en B01.

## 10. Referencias verificadas

- proyecto/docs/decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md (DEC-0022).
- sistemas/gameplay/character_creation/S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md; S04_MIGRACION_F10_HOST_v2.md; s04_fixed_protagonist_contract_v2.json; s04_protagonist_biography_v1.json.
- sistemas/gameplay/careers/academy_path/f10_host_candidate_factory_contract_v0.1.json; academy_state.json; admission_flow.json.
- desarrollo/integration/host/tests/academy_core_feasibility.cpp; src/native_session.h; src/f04_session_bridge.cpp; src/player_bootstrap.h; src/slot_store.h; src/f10/biography_validation.h; src/biography_profile_source.h.
- proyecto/docs/architecture/host/F10_H06_P06_CONTRATO_INTERFAZ_ACADEMIA_2026-11-14.md; F10_H06_P06_FACTIBILIDAD_NATIVA_2026-11-14.md; H04_PERSISTENCIA_2026-11-13.md; H06_P06_CIERRE_FUNCIONAL_MINIMO_2026-11-14.md.
- PR #167 (IA-03A), #185 (IA/CI), #186 (UE 5.8.4), auditoría HOST PR #183 **Draft y no fusionada** en el momento de esta preparación.
