# H06-P06 — Arquitectura del alta real del cadete y vínculo al HOST

**Fecha:** 13-11-2026. **Autor del análisis:** ChatGPT. **Base examinada:** main 2b666a05466e759066213516d72d60f7d364240a, con H06 PR #142 y acta #145 fusionadas.  
**Estado:** INVENTARIO Y CONTRATO PROPUESTO; NO IMPLEMENTADO, NO PROBADO, NO CERTIFICADO.  
**Alcance:** cerrar HU-08 de H06 sin suplantar la fase F10 ni conceder permisos F05/F11.

## 1. Resultado del inventario real

| Fuente real | Qué existe | Qué NO demuestra |
|---|---|---|
| CoreRPG fijado 76a7b7b485616d8c4994f384a90f123bf333591d, include/corerpg/world_state.hpp | WorldState permite crear entidades, declarar poblaciones y materializarlas de forma atómica en su modelo genérico. | No incluye semántica Starfleet, un alta de cadete F10 ni la asociación autorizada de jugador. |
| desarrollo/integration/f04/include/f04_bridge.h y f04_host_bridge.cpp | f04_create_population crea una población de **clase de nave**; f04_person resuelve PERSON en sesión F04. | No expone una operación productiva para crear un personaje nuevo de Academia ni una campaña de campus. f04_create es escenario sintético. |
| desarrollo/integration/host/src/player_bootstrap.h, session_owner.cpp, native_session.cpp | PlayerBootstrap::prepare/bind es privado y verifica PERSON, ámbito, generación, revisión y f05_bind_player en el trabajador propietario. | El argumento created_person no convierte por sí solo un ID en cadete válido. El vínculo F05 actual pertenece a un contexto de tripulación de nave. |
| desarrollo/integration/host/include/trek/host/host_abi.h y juego/UE5/StarTrekRPG | ABI C 1 con tickets/estado y GameInstanceSubsystem; el OPEN del diagnóstico usa clase miranda y devuelve PRINCIPAL_UNBOUND. | No crea un personaje productivo. No existe operación pública confiable de alta de cadete ni interfaz final. |
| sistemas/gameplay/characters/character_definition_contract.json y character_runtime_model.json | Identidad de personaje campaign_created, biografía validada antes del inicio, continuidad de identidad, capacidades por evidencias. | Son contratos de contenido, no transacciones del WorldState operativo. |
| sistemas/gameplay/careers/academy_path/admission_flow.json y academy_state.json | Proceso candidato/admisión y estados cadet_year_1..4; un cadete admitido ocupa plaza real del registro de población. | Un booleano admission_authorized del cliente no autoriza nada por sí mismo. |
| desarrollo/tools/generation/generate_academy_cadet_step2.py y fixtures Academy Life | Generador determinista para **cadetes procedimentales** de referencia; carácter cadet:proc:... y conservación de plazas en registro JSON. | No es el constructor de un personaje de jugador; no publica una entidad Core ni un vínculo H03. No trasladar su fixture a producto como credencial. |
| proyecto/docs/roadmap/master/fases/F10/README.md y ACTA_P01_P05_REFERENCIA_2026-10-14.md | F10 dispone de trayectoria aspirante→cadete→4 cursos→graduación→alférez y pruebas de referencia. | F10 NO acredita CORE_INTEGRADO o UE5_JUGABLE. La evidencia CORE_HOST_VERIFIED es stub de fixture. |
| proyecto/docs/roadmap/master/fases/F11/F11-P05-A02-00_CONTRATO_IDENTIDAD_RANGOS_AUTORIDAD_2026-11-11.md | Comisión, rango y autoridad institucional requieren hechos reales y emisor propio F11. | Un cadete recién creado no es alférez ni tiene comisión o capacidad de emitir actos F11. |
| desarrollo/integration/host/src/f04_session_bridge.cpp / f05_player_binding.h | H04 identifica/restaura vínculo durable F05; el restore de la composición actual abre un contexto F04 miranda antes de leer historial. | No puede presumirse que un guardado de Academia de nuevo formato sea compatible sin ruta de restore explícita. |

**Conclusión de arquitectura:** los tres elementos críticos no son equivalentes: (1) creación/matriculación del personaje Academy en el dominio F10/Core, (2) vinculación del jugador a ese sujeto en HOST/H03/H04 y (3) facultades institucionales F11 o de órdenes F05. P06 debe conectar (1) y (2) sin falsificar (3).

## 2. Fronteras de propiedad (obligatorias)

- **F10 / sistema de Academia:** elegibilidad, perfil inicial validado, admisión, plaza real de cohorte, condición de cadete, historia y transición de cursos. Debe resolver la semántica del dominio y sus contratos, utilizando CoreRPG como almacén autoritativo. H06 no puede inventar curriculum, plazas ni aprobados.
- **CoreRPG:** único WorldState, ID de entidad, relaciones, tiempo, historial y mutación publicada. No alterar el pin ni las pruebas históricas para lograr un caso verde.
- **HOST H03/H04/H06:** control exclusivo de sesión, principal local, ligadura a un único sujeto válido, generación, procedencia, frontera de interfaz y guardado/carga. La UI puede solicitar datos de biografía, nunca escoger ID Core, F04Ref, marca de admisión, categoría, rango, permiso o emisor.
- **F05:** valida permisos y órdenes de operaciones de nave **cuando exista una competencia legítima**. Separar ser el personaje jugable de estar autorizado a emitir una orden. No modificar el contrato f05_bind_player o la emisión histórica sin coordinación y regresión.
- **F11/H07:** rango, comisión, autoridad de Personal de Flota y emisor. Ningún acto de matrícula, bootstrap o vínculo H03 equivale a comisión o ascenso.

**Cuestión contractual para F10/F11:** el modelo genérico de personajes exige character_id estable desde creación, mientras el contrato de identidad profesional F11 describe su creación al comisionar. Hasta acordar si son una misma identidad continuada o dos identificadores con relación inmutable, no asignar un character_id F11 mediante un campo elegido por UE ni al matricular; conservar identidad del candidato como persona precomisión y garantizar una transición documentada a F11. Esto NO bloquea la definición de candidato, pero sí cualquier fusión que presuponga identidad profesional.

## 3. Secuencia productiva deseada, sujeta a implementación del dominio

### P06-A — Perfil y candidatura

1. El jugador solicita NUEVA PARTIDA en Unreal y aporta elecciones de biografía/persona admitidas por el contrato de personajes; por defecto, **campaña con inicio en 2383**, con día/mes todavía no fijados por la decisión de lore. No fijar una fecha inventada.
2. El servicio confiable de F10 valida opciones, perfil, contexto canónico y elegibilidad. Una petición de cliente no acredita aprobación de acceso; conservar candidato como CANDIDATE si la admisión aún no está resuelta. No se requiere resolver toda F10 en H06.
3. Preparar una única campaña Core de Academia con población, cohorte y plaza propias cuando exista un factory de producto de F10. Un escenario de Miranda de pruebas NO sustituye la Academia. Reservar identidad y plaza; no materializar un segundo cadete por reintento.

### P06-B — Alta autoritativa

4. Con la condición apropiada de admisión **confirmada por el dominio** (o como candidato antes de ingresar), crear/materalizar una PERSON real en el WorldState de esa misma campaña, con origen/slot y biografía validada. La creación debe ser atómica a nivel de efectos visibles y no consumar cambios parciales ante error.
5. Emitir un resultado **interno y no falsificable por cliente** que vincule campaña/generación y persona recién creada a la operación de alta validada. Un ID de texto, el ID de entidad y un booleano trusted=true no bastan. La idempotencia y reintentos deben recuperar la misma persona.
6. H03 resuelve la PERSON real en el hilo propietario, valida ámbito, generación y revisión, y establece el único vínculo de jugador. Revisar la dependencia actual f05_bind_player, ya que el cadete no es necesariamente tripulante apto para órdenes F05: **no forzar un bind F05 de capitán/ensign de laboratorio para obtener BOUND**. Si se necesita una extensión separada de vínculo de jugador para campañas Academia, diseñarla explícitamente y en Core sin duplicar fuentes de verdad.
7. Publicar una vista mínima de personaje solo después del éxito: estado de identidad/campaña, id de sujeto autorizado en su scope vigente, condición de candidato/cadete y estado de matriculación filtrados. La UI no recibe F04Session ni token utilizable como permiso.

### P06-C — Continuidad

8. H04 guarda la campaña y su vínculo (no un perfil decorativo paralelo). En restauración, verificar procedencia local, identidad de personaje, estado académico y hechos Core; renovar scope/generación; rechazar importación no confiable o identidad incompatible.
9. Tras LOAD/CLOSE, invalidar tickets y proyecciones UWorld; tras error de alta, mantener UNBOUND y no dejar plaza, PERSON, expediente o ranura publicada a medias.
10. H06-P07 solo después de comprobar jugador real: activar interfaz de peticiones F05 **únicamente en contextos donde el personaje tenga competencia real**, rechazando la orden de nave del cadete no habilitado. La vida académica no exige poseer permisos de puente.

## 4. Decisiones técnicas que debe resolver Codex antes de editar

- Identificar una ruta de materialización Academia válida sin cambiar CoreRPG pinned y sin alterar el comportamiento histórico de F04/F05. Si no existe, presentar opciones A/B con coste y dependencia y ejecutar solo el tramo no invasivo. **Prohibido promover un fixture o abrir miranda y llamarla Academia.**
- Determinar dónde reside el vínculo persistente de jugador en una campaña pre-F05: extensión aditiva al dominio/compilación de producto, no segundo registro autoritativo. Compatibilidad H04 con saves existentes; no reutilizar f05_player_binding para afirmar una matrícula ficticia.
- Resolver si la admisión se ejecuta ya en tiempo de juego o se parte de un estado inicial **admitted validado por F10**, sin falsear la evaluación ACC-01..05 ni convertir un parámetro público en autorización. Sin decisión aprobada, continuar hasta CANDIDATE.
- Contrastar que la creación de PERSON no altera sin permiso ids canónicos ni campos reservados F11; la etiqueta campaign_created y su procedencia son de partida, no autoridad profesional.
- Planificar recuperación de energía/fallo después de crear pero antes del vínculo, incluyendo reintentos y compatibilidad entre procesos.

## 5. Cierre y exclusiones

**HU-08 solo PASS cuando** exista partida nueva realmente jugable de candidato/cadete en UE, creación única autoritativa en Core, vínculo H03 propio, SAVE/RESTORE H04 en proceso nuevo y denegaciones de identidad incompatibles, con evidencia CTest Windows/Linux/ASan y ejecución UE NullRHI/D3D12. Hasta entonces: BLOCKED por dependencia F10/Core y adaptador H03.

Excluido de P06: desarrollo completo de la Academia, cursos, notas, profesores, evaluación de acceso completa, primer ascenso oficial, elección de departamento final, modificación de las reglas F11 o creación artificial de órdenes F05. La aceptación visual manual corresponde a P08.

**Disco:** no borrar ni modificar laboratorios existentes durante limpieza concurrente; usar únicamente temporales ignorados en la ubicación prevista por AGENTS.md, reversibles y sin dependencias desde el producto. No duplicar motores/checkout Core. Git alberga únicamente código definitivo, contratos, pruebas fuente e informes pequeños.

**Siguiente encargo:** H06_P06_ENCARGO_CODEX_2026-11-13.md. Matriz de oráculos: H06_P06_MATRIZ_PRUEBAS_2026-11-13.md.
