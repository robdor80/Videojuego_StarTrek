# Sistema 04 v2 — Migración técnica del creador libre al protagonista único

**Estado:** PLAN DE INTEGRACIÓN; NO IMPLEMENTADO. **Objetivo:** respetar la nueva decisión autoral DEC-0022 sin destruir contratos históricos ni romper el código HOST ya publicado.

## Inventario de compatibilidad a respetar

| Existente | Situación tras DEC-0022 | Acción futura |
|---|---|---|
| `character_creation_contract_v1_0.json` | LOCKED, creó el modelo anterior de fichas biográficas libres | Conservar como v1; **adaptar/introducir v2**, no reemplazar en caliente |
| `f10_initial_player_rules_v0.1.json` | Empotrado/consumido por código nativo IA-03A; admite 3 especies | **No modificar en esta entrega documental**; introducir nueva política/product gate v2 y actualizar embed/tests con Codex |
| `f10_species_maturity_policy_v0.1.json` | Mínimos genéricos históricos 18/25/22 | Conservar para otros contextos, protagonista fijo pasa 22 por tener 45; sin selector inicial |
| `f10_formulario_inicial_v0.3.json` y HTML | Prototipo offline de antiguo formulario | Marcar histórico/no producto, reemplazar UX de nueva partida por panel compacto de identidad |
| `biography_validation_rules.md` | Doble puerta objetiva/semántica en creación libre | Reutilizar controles de coherencia, separar autoría canon versus elección jugador |
| `player_profile_contract.json` | Alias de jugador separado de personaje | Conservar: nombre diegético configurable NO es nickname |
| `character_sheet_model_v1_0.json` | Distintas secciones ficha/academia/servicio | Reutilizar estructura con perfil preestablecido y nombre/visual editables |
| `f10_host_candidate_factory_contract_v0.1.json` | Candidato mediante draft no fiable, sin creación producto completa | Diseñar transición segura a fuente de perfil autoral fijo, manteniendo F10, HOST, PERSON y recibos |
| `desarrollo/integration/host/src/f10` | Validador y política ya parcialmente implementados | Auditar tests/regresiones y programar cambio en una fase con Codex; **no afirmar actualizado** |
| `sistemas/gameplay/characters/character_runtime_model.json` | Persistencia y progresión genérica | Sin alteración de NPC; nuevo protagonista se instancia como personaje de la campaña autorizado |

## Descomposición sugerida para Codex cuando haya cuota

**S04-I01 — Fuente canónica de datos.** Compilar `s04_fixed_protagonist_contract_v2.json` y `s04_protagonist_biography_v1.json` con hashes/versiones; resolver relaciones con referencias aprobadas, distinguir `AUTHOR_DEFINED` de `PLAYER_EDITABLE`; no aceptar selección arbitraria por input ni inyección en JSON.

**S04-I02 — Formulario reducido y avatar.** Quitar selector de especie, sexo, edad y texto libre de biografía; admitir nombre y rasgos permitidos. Mantener alias de perfil aparte y validación de nombres. Guardar apariencia visual persistente sin mutar genealogía, aptitudes ni identidad existente.

**S04-I03 — Validación e ingreso F10.** F10 valida el paquete de antecedentes autorales como fuente registrada y separa examen/decisión institucional del debate creativo; no se debe aceptar un JSON manipulado por cliente que declare «soy descendiente de Khan y capitán». Si historia de intro determina matrícula ya efectiva, generar evento académico autorizado y coherente con el acceso ACC-01–05; no ejecutar paralelamente otro examen de ingreso obligatorio en la misma sesión. Los hechos del relato no sustituyen el mecanismo de creación de PERSON.

**S04-I04 — Competencias reales y equilibrio diegético.** Mapear fuertes rasgos físicos y cuatro maestrías a modelos CoreRPG de habilidades por evidencia y perfiles individuales; diferencias perceptibles y creíbles; probar contra humano convencional, vulcano de referencia y combatiente adiestrado. No convertir por defecto en Security ni asignar fuerzas/victorias mágicas.

**S04-I05 — Introducción y conocimiento NPC.** HOST ensambla secuencia de 2D, voces, UI, datos autorizados; Janeway/Picard han recibido expediente en 2383 y respaldan la evaluación, no encuentro físico; difundir a nadie más el expediente confidencial sin evento. Reproducción saltada/repetida idempotente; relación emocional evoluciona por eventos posteriores.

**S04-I06 — Regresión y migración.** Pruebas de nuevas partidas (siempre mismo arquetipo; nombre/cosmética variable), intentos de especie/sexo/edad no permitidos, registros de origen de habilidades, examen, cache, save/load, rangos F11, relación con Siete, fecha de Sisko; no convertir viejos guardados automáticamente. Mantener exactamente las garantías existentes de identidad/authority F10/HOST.

**S04-I07 — Integración UE5 y aceptación.** Controles cosméticos fluidos, un solo héroe de calidad, avatar consistente, mini-slice intro 2D y acceso Academia; pruebas en Windows MSI, cobertura CI y aceptación por el autor.

## Alcance de este trabajo aprobado ahora

La reescritura **del diseño y los contratos** sí queda terminada; **la migración del código, formulario HTML y runtime queda pendiente de Codex**, sin crear una rama de ejecución paralela con autoridad duplicada. No mezclar este plan con el proyecto autónomo HOST para reimplementar reglas de F10: HOST integra/coordina, **F10 mantiene las reglas**.

No tocar hasta fases correspondientes: F11 ascensos/órdenes, CoreRPG congelado, resto de 16 sistemas, currículo de Academia, elenco LORE-05B. La decisión de protagonista único **no elimina la variedad de especies de NPC**.
