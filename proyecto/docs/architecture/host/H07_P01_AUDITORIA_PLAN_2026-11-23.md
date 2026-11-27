# H07 — Auditoría inicial, dependencias y plan de integración institucional HOST ↔ F11

**Fecha:** 23-11-2026 · **Base examinada:** main en d0cae3f9a4165710501ff4a2f4e488fd6a0fa0ac.
**Estado de este documento:** H07-P01 DOCUMENTADO para revisión en PR; P02–P05 PLANIFICADAS. No se declaran pruebas nuevas de C++/Unreal ni certificación H07.
**Responsables:** ChatGPT: arquitectura, revisión, documentación y matriz. Codex: cambios C++/composición y Unreal. Usuario: decisiones sustanciales y fusión.
**Frontera vigente:** H01/Plan Maestro v1.2 y decisión F11-P05-A02-03: la competencia institucional pertenece a F11, CoreRPG es fuente autoritativa, HOST no legisla ni emite.

## 1. Evidencia directamente inspeccionada en main

| Activo | Lo que existe realmente | Estado de la capacidad | Condición / límite |
|---|---|---|---|
| H06 / M1 | Acta H06_IA03C05_ACTA_CERTIFICACION_M1_2026-11-23.md; PR #200 y #201 fusionadas | M1 CERTIFICADO LIMITADO | Pantalla completa aceptada; incidencia M1-UX-WINDOWED-2560 abierta; no acredita F11 |
| H02/H03 | SessionOwner, Generation, único vínculo, hilo propietario, current_player; SessionOwner::Impl | IMPLEMENTADO y probado históricamente; H06 lo reutiliza | Academy crea PERSON candidata, no oficial comisionado |
| H04 | SlotStore, procedencia CREATED_LOCALLY / KNOWN_LOCAL, staging y recuperación, nueva generación | IMPLEMENTADO y probado; reutilizado por M1 | Procedencia local no es firma institucional ni autenticación fuerte frente al propietario del equipo |
| H05 | gateway_bridge.cpp (F05) y NativeSession::dispatch | IMPLEMENTADO, probado y fusionado en H05 | Solo dominio F04/F05; consulta y orden no implican competencia F11 |
| H06 | juego/UE5/StarTrekRPG/StarTrekRPG.uproject y menú Slate Academy | IMPLEMENTADO, certificado en alcance M1 | AcademyCampaign propia, no se debe reinterpretar como F04Session de oficial |
| F11 / producto | f11_promotions.h: f11_personnel, f11_promotion, f11_commit_promotion; schema y proyecciones Core | IMPLEMENTADO y probado en incrementos F11, no conectado a TrekHost | Solo primer ascenso 1101→1102; el commit exige antecedentes institucionales reales |
| F11 / lector | f11_host_reader.h/.cpp: trek::f11_host::career y promotion | IMPLEMENTADO, probado históricamente con 4 casos lectores + 13 F11 | Biblioteca separada, no admisión/autorización de sesión integrada en HOST |
| F11 / emisión | f11_trial_host.inc solo bajo F11_NATIVE_TEST_HOST en TrekF11TrialHost | IMPLEMENTADO SOLO PARA ENSAYO | **No existe** emisor de comisiones/concesiones/evaluaciones/órdenes de producto |
| F11 / preparación | PR #108 y #109 fusionadas, PR #110 abierta en Draft | #110 SOLO DOCUMENTADO, 33 escenarios NOT_RUN | La matriz #110 vive en rama Draft, no debe confundirse con main ni con pruebas PASS |

**Comprobaciones de código:** desarrollo/integration/host/CMakeLists.txt mantiene F11 fuera del grafo del HOST, comprueba que F11_ENABLE_PROMOTIONS no esté activo y sustituye la única unidad del puente F04 por f04_host_bridge.cpp. No enlaza TrekF11HostReader. desarrollo/integration/f11_host/CMakeLists.txt incluye todo el subproyecto ../f11, que define TrekF11TrialHost en su grafo de pruebas; **no incorporar ese CMake directamente en la composición de producto sin separar de forma segura los targets de ensayo**. f04_bridge.cpp incluye f11_schema.inc y f11_promotions.inc solo con F11_ENABLE_PROMOTIONS. f11_schema.inc reconoce el marcador de ensayo CAUSE=110501: nunca usarlo como certificado de procedencia ni desbloquear por su presencia.

**Protección existente y verificable:** SessionOwner::institutional_command encola GatewayOp::INSTITUTIONAL; NativeSession::dispatch devuelve Error::SERVICE_UNAVAILABLE antes de bridge::dispatch. La ABI C actual expone OPEN/CLOSE/VIEW/F05/SAVE/RESTORE, **no una operación de emisión institucional**. En Academy, Dispatch rechaza por ACCESS_DENIED antes de usar F04/F05. Los ensayos H05 previos incluyen host.m0.institutional y comprobación de ausencia de cambio de bytes; este análisis no reejecuta ese test.

**GitHub:** PR #108/#109 fusionadas y #110 Draft no fusionada a la fecha. La rama main indica protected=true en metadata, pero su objeto protection declara enabled=false y required_status_checks enforcement_level=off: no inferir que todas las protecciones exigibles estén activas. Respetar PR y no modificar main directamente.

## 2. Decisiones para H07 (no alteran F11)

1. **Solo consumo y encaminamiento.** Una petición institucional es intención tipada; HOST valida sesión/generación/canal/identidad/procedencia y delega toda regla normativa a F11. Nunca modificar RANK, relaciones, expedientes o evaluar méritos dentro del HOST.
2. **Lecturas primero.** Se puede integrar el lector de hechos F11 ya confirmados en Core mediante un adaptador privado, siempre que exista F04Session F11 habilitada, sujeto F11 comisionado y vínculo legítimo en esa misma campaña. Un cadete Academy sin comisión no produce expediente de oficial: respuesta vacía y código semántico apropiado, no rango inventado.
3. **Emisión cerrada.** Mantener SERVICE_UNAVAILABLE para toda solicitud de comisión, concesión, evaluación, orden institucional o ascenso que dependa del emisor F11 aún inexistente. No usar el trial ni activar un emisor con campos aportados por Blueprint/LLM/NPC.
4. **Compatibilidad rigurosa.** La composición del puente HOST y F11 es una intervención C++ de alto riesgo: resolverla con Codex, preservando H02/H04/H05/H06, ABI C existente, Core pin 76a7b7b485616d8c4994f384a90f123bf333591d, regresión y negativos. No activar F11 con un cambio ciego de flags ni actualizar oráculos históricos.
5. **Eventos limitados.** H07 podrá consultar y proyectar un evento F11 ya confirmado, sin cola durable nueva, acuse narrativo ni campo presented_at. Dispatcher/eventos general en H08; carrera, emisor y ceremonia en F11/narrativa.
6. **Privado y local.** No añadir servidor, token remoto ni antitrampas criptográfico ficticio. Un manifest/hash de guardado no constituye acreditación institucional.
7. **Conservación de identidad.** No unir arbitrariamente AcademyCampaign y F04Session ni asignar comisión al candidato para satisfacer una prueba. El tránsito real Academia→oficial dependerá del flujo de graduación F11 y de la planificación del juego.

## 3. Subfases definitivas de H07

**Se adoptan cinco subfases H07-P01–P05**, conservando la granularidad y numeración conceptual del Plan Maestro. No crear extensiones por cada defecto menor; reparar dentro de la misma PR o mediante PR correctiva vinculada.

### H07-P01 — Auditoría, frontera y contrato de integración

- **Objetivo y componente:** baseline de F11/HOST, contrato de identidad/procedencia/visibilidad, mapa de dependencias y casos de cierre; documentación permanente en este directorio.
- **Dependencias:** H01–H06, lectura de AGENTS.md, decisiones F11, PR #108–#110 y acta M1.
- **Reutilización:** H01_P02_CONTRATOS, H01_P03_CONFIANZA, H05_P01_P03_CONTRATO_M0, frontera F11-P05-A02-03, código y cabeceras reales.
- **Responsable / modelo:** ChatGPT exclusivamente; Codex no necesario.
- **Riesgos:** confundir el ensayo con producto, introducir expectativas no disponibles, asumir que Academy es un oficial.
- **Entregables:** este plan auditado, contrato de frontera H07 y registro de escenarios.
- **Pruebas:** contraste estático de cabeceras, CMake, clases de sesión, estados PR, acta M1 y matriz F11; validar enlaces/rutas e identificadores, sin ejecutar CTest ficticio.
- **Cierre objetivo:** inventario sin funciones inventadas, mapa de responsabilidades y contrato sin emisor; revisión de la PR documental. Un documento escrito no se convierte en certificación.
- **Entorno:** GitHub/Cloud; no necesita MSI ni Unreal en ejecución.
- **Estado al inicio de la PR:** DOCUMENTADO; pendiente revisión/fusión.

### H07-P02 — Admisión y pasarela institucional privada (sin emisor)

- **Objetivo y componente:** fijar en SessionOwner/NativeSession la frontera tipada de solicitudes institucionales, versión de capacidad y rechazo explícito si la API F11 aprobada no está disponible. No escribir autoridad.
- **Dependencias:** P01; H02/H03/H04/H05; aprobaciones normativas F11 solo para mutaciones futuras.
- **Reutilización:** Generation, Binding, Provenance, Dispatch, SERVICE_UNAVAILABLE y ABI H05. El rechazo actual ya existe y NO debe refactorizarse sin beneficio probado.
- **Responsable / modelo:** Codex **GPT-6, razonamiento Alto** para modificaciones de núcleo/hilo/ABI; ChatGPT revisa. Si basta con documentar y ampliar pruebas seguras, ChatGPT las hace sin consumo Codex.
- **Riesgos:** TOCTOU entre admisión y ejecución, estado after-load, exponer permisos por ABI, confundir 'canal autorizado' con competencia institucional.
- **Entregables:** pasarela privada mínima/aditiva o evidencia de que la existente basta; pruebas negativas de rechazo y guía de adaptación futura a emisor F11 real. No publicar un endpoint institucional para clientes.
- **Pruebas:** sin binding, generación caducada, Academy, ruta falsa, callback de restauración, canal no autorizado, petición sin emisor, buffers vacíos, ausencia de mutación Core/bytes y repetición.
- **Cierre objetivo:** SERVICE_UNAVAILABLE sin efectos en rutas no disponibles y ninguna nueva superficie de emisión; resultados CTest Linux/Windows y revisión de ABI según cambios.
- **Entorno:** Codex Cloud para código/CI; MSI no imprescindible salvo que se modifique interfaz UE, lo que no se prevé.

### H07-P03 — Consulta nativa y proyección F11 de solo lectura

- **Objetivo y componente:** hacer accesibles al HOST las operaciones de expediente y evento F11 confirmados, con observador resuelto por HOST y salida vacía al denegar; sin duplicar TrekF11HostReader.
- **Dependencias:** P01 y frontera P02; F11 reader #109, puente con F11 realmente habilitado, campaña F04 válida con comisionado legítimo. No depende del emisor para leer hechos de expedientes existentes, pero **sí para producir oficiales nuevos de producto**.
- **Reutilización:** f11_personnel, f11_promotion, trek::f11_host::career/promotion, F04Ref/Scope, hilo propietario, SessionOwner, H04 staging y snapshot.
- **Responsable / modelo:** Codex **GPT-6, razonamiento Alto** para CMake/C++/composición y runtime; ChatGPT diseña vistas y audita.
- **Riesgos:** chocar con el guard H02 que excluye F11, enlazar accidentalmente TrekF11TrialHost, romper pins/historial y ABI, filtrar expediente de otro sujeto, proyectar datos de una generación anterior.
- **Entregables:** adaptador interno de lectura integrado en TrekHost, contrato de vista versión 1, posibilidad controlada de consumo para interfaz sin acceso bruto a F04Session, sin crear registro lateral. Mantener fuera cualquier ceremonia/presented_at.
- **Pruebas:** expediente válido cargado de prueba ya confirmado; ajeno, no comisionado, scope viejo, doble consulta inmutable, salida borrada, cambio de generación y SAVE/RESTORE en otro proceso; inspección de símbolos del binario producto para impedir bootstrap experimental.
- **Cierre objetivo:** cliente autorizado obtiene hechos idénticos a Core; cliente no autorizado no obtiene datos; consultas no cambian WorldState, RNG, revisión ni historial; build/CTest Linux y MSVC PASS en el SHA inspeccionado.
- **Entorno:** Codex Cloud/CI primero; integración de vista UE y aceptación real se reserva a P05 en MSI.

### H07-P04 — Matriz de conformidad y pruebas estáticas

- **Objetivo y componente:** matriz HOST propia y correspondencia con las 7 puertas HOST_01–HOST_07 y los 33 casos F11 previstos en PR #110; definir pruebas negativas, evidencia y límites de autoridad.
- **Dependencias:** P01; lectura del contrato F11/PR #110. **Puede realizarse en paralelo con P02/P03** siempre que no marque tests como PASS.
- **Reutilización:** test_f11_p05_a02_03_host_boundary.py (15 guards existentes), matriz #110 Draft, H05 M0, pruebas unitarias/CTest existentes y documentación M1.
- **Responsable / modelo:** ChatGPT exclusivamente; sin Codex.
- **Riesgos:** mezclar suite F11 externa con suite propia del HOST, atribuir hechos confirmados a una simulación, contar CI estática como UE/MSI.
- **Entregables:** matriz H07 versionada y mapeo de escenarios a CTest/CI/MSI, inicialmente NOT_RUN; revisiones de especificación.
- **Pruebas:** comprobar unicidad/cobertura de IDs, que 33 casos externos no aparecen implementados por una PR documental y que ninguna vía de emisión de ensayo se confunde con producto.
- **Cierre objetivo:** cobertura especificada y verificable, cada escenario con dueño, fuente de verdad y criterio binario; no equivale a ejecución.
- **Entorno:** GitHub/Cloud, sin MSI.

### H07-P05 — Integración UE, regresiones y acta de cierre acotado

- **Objetivo y componente:** conectar una visualización institucional mínima autorizada a la capa Unreal existente y ejecutar pruebas de extremo a extremo; preparar acta H07 sin anticipar F11-C/D ni H08.
- **Dependencias:** P02/P03/P04, H06 certificado limitado; una campaña/guardado F11 válido y conocido para prueba de consulta. Para mutaciones reales, **emisor de producto F11-P05-A02-03 aún pendiente**; no fabricarlo aquí.
- **Reutilización:** UE 5.8.4, inicialización/dll HOST de H06, automatizaciones NullRHI/D3D12, H04, CTest F11 reader, logs y matriz.
- **Responsable / modelo:** Codex **GPT-6, razonamiento Alto** para Unreal/UBT/ABI y pruebas; ChatGPT dirige auditoría, verificación GitHub Actions y acta; usuario valida UX.
- **Riesgos:** atribuir al usuario real un fixture de oficial, modificar assets fuera del alcance, confundir visualización con orden institucional, no distinguir prueba Cloud de ejecución MSI.
- **Entregables:** pantalla/vista mínima sin creación de rangos, informes Linux/MSVC y MSI, matrices con estados realmente ejecutados, diagnóstico de limitaciones y acta condicionada.
- **Pruebas:** UE UBT Editor/Game, NullRHI y D3D12, consulta permitida y denegada, session generation tras restauración, guardado/carga, UI sin datos de otra persona, cero cambios de Core en solo lectura, F04/F05/H02–H06, escenarios de F11 pertinentes, inventario de exports y no-trial.
- **Cierre objetivo:** evidencia fechada por SHA de versiones/componentes y pruebas reproducibles; certificado **solo de lectura/denegación** si el emisor sigue ausente; ningún cierre integral de mutaciones sin F11 de producto y pruebas propias.
- **Entorno:** Codex Cloud para C++ y CI; **Codex en MSI obligatorio** para la validación Unreal real. Revisión/aceptación del usuario para experiencia final.

## 4. Orden, paralelismos y bloqueos

- **Secuencia preferente:** P01 → P02 → P03 → P05. **P04 puede ejecutarse desde P01 en paralelo** con P02/P03 y debe estar completada antes de P05.
- **Trabajo ChatGPT ejecutable ya:** P01 y P04 documentales, revisión de matrices, rutas, comprobaciones estáticas, PR de documentación y Actions. No usar Codex para esto.
- **Trabajo Codex Cloud:** P02 solo si requiere código, P03 composición C++ y pruebas, preparación P05 C++/CI.
- **Trabajo Codex MSI:** P05 UE 5.8.4, UBT, NullRHI/D3D12, funcionalidad UI y validación final.
- **Bloqueo F11 independiente:** servicio de emisión institucional productiva, graduación/comisión/concesión/evaluación/orden reales, otros ascensos y permisos. Es F11, no H07. **No desactivar el bloqueo por copiar f11_trial_host.inc, cambiar CAUSE=110501 o activar una bandera CMake sin auditoría.**
- **Dependencias posteriores fuera de alcance:** H08 bus/notificaciones, F11-P05 B/C/D/E para progresión, evaluaciones, ceremonias y traslados, narrativa del tutorial, UX final, S18 si se aprueba evolución de autenticación. No bloquear el lector actual por estos elementos futuros.

## 5. Criterio de aceptación y semántica de estados

**H07 de lectura verificable:** puede declararse IMPLEMENTADA/PROBADA/FUSIONADA solo tras P02–P05 con evidencias reales. Una posible certificación **LIMITADA a consulta y denegación** requiere acta explícita, con operaciones de emisión todavía SERVICE_UNAVAILABLE. Nunca declarar que HOST ha certificado la emisión F11.

**H07 institucional plena:** no se considera CERTIFICADA mientras los comandos institucionales de producto no puedan encaminarse a una API F11 aprobada y probada en el ámbito definido. El proyecto principal debe certificar independientemente el emisor; la revalidación HOST de esas operaciones se hará entonces en una entrega delimitada, sin duplicar F11.

Ningún documento PREPARADO/PLANIFICADO implica IMPLEMENTADO, PROBADO, CERTIFICADO ni FUSIONADO. Ninguna PR Draft se considera parte de main.

## 6. Fuentes primarias y trazabilidad

- Reglas: AGENTS.md, laboratorios/README.md.
- H06: proyecto/docs/architecture/host/H06_IA03C05_ACTA_CERTIFICACION_M1_2026-11-23.md; PR #200 y #201.
- H01/H05: proyecto/docs/architecture/host/H01_P02_CONTRATOS_v1.0_2026-11-11.md; H01_P03_CONFIANZA_v1.0_2026-11-11.md; H05_P01_P03_CONTRATO_M0_2026-11-13.md.
- HOST: desarrollo/integration/host/{CMakeLists.txt,src/native_session.cpp,src/session_owner.cpp,src/gateway_bridge.cpp,include/trek/host/session_owner.h,include/trek/host/host_abi.h}.
- F11: desarrollo/integration/f11/{README.md,include/f11_promotions.h,src/f11_schema.inc,src/f11_promotions.inc,CMakeLists.txt}; desarrollo/integration/f11_host/{CMakeLists.txt,include/f11_host_reader.h,src/f11_host_reader.cpp,README.md}.
- Frontera: proyecto/docs/decisions/f11_p05_a02_03_host_boundary_2026-11-11.md; sistemas/gameplay/careers/promotions/f11_p05_a02_03_host_boundary_v0.1.json.
- PRs: #108 y #109 fusionadas; #110 Draft abierta (matriz externa de 33 casos NOT_RUN; no está fusionada). Los compromisos F11 posteriores requieren su propia auditoría.
