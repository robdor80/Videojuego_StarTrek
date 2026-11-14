# H06-P06-A5 · Política de antecedentes del personaje inicial — diseño F10

**Fecha:** 14-11-2026 · **Responsables:** ChatGPT (diseño/contratos), Codex (posterior integración nativa). **Estado:** PROPUESTA DE DISEÑO IMPLEMENTADA EN CONTRATO Y REFERENCIA OFFLINE, **NO** autoridad de producto ni certificación. **CoreRPG**: pin `76a7b7b485616d8c4994f384a90f123bf333591d`, intacto.

## 1. Objetivo y hechos comprobados

Permitir al jugador crear una **historia anterior a la Academia** con intereses, formación, lugares, relaciones y experiencias que tengan sentido narrativo, sin exigir documentos imposibles a un personaje que aún no existe en Core. La biografía no concede profesiones, certificaciones, permisos, puntos de habilidad, puestos ni rangos. Los hechos que deban persistir se crearán únicamente en un futuro commit F10 validado por ambas puertas y publicado por Core.

Fuentes bloqueadas inspeccionadas: `character_creation_contract_v1_0.json`, `biography_validation_rules.md`, `prior_activity_model.json`, `species_biology_contract.json` y `character_lifecycle_contract.json`. Contratos aditivos: `f10_species_maturity_policy_v0.1.json` (#153/#154) y `f10_biography_evidence_semantic_boundary_v0.1.json` (#155/#156). El código nativo actual `RegisteredBiographyAuthority` (PR #156) registra fuentes y atestaciones ligadas al borrador/contexto/versiones, pero **aún carece de un emisor autorizado de antecedentes iniciales y de un revisor semántico de producto**.

**Decisión de diseño propuesta en este corte:** aceptar narraciones personales plausibles como *candidatas a antecedentes*, que F10 podrá acreditar internamente tras validar su cronología y procedencia. No son hechos comprobados por declararlos el jugador; tampoco necesitan certificados reales externos. La elección final de qué reglas biológicas dan madurez suficiente y el proveedor de IA siguen pendientes de aprobación.

## 2. Nueve clases de afirmaciones, no nueve fichas nuevas

| Clase | Tratamiento propuesto | Ejemplo |
|---|---|---|
| Afición/práctica personal | Revisión interna F10, sin documento externo | Karate desde los ocho años |
| Interés/objetivo | Revisión interna F10, sin puntos gratis | Le gusta la astronomía |
| Familia/origen personal | Plausibilidad y mundo; no nacionalidad automática | Se crió en una colonia |
| Educación formal | Requiere trayectoria, acceso, institución y duración plausibles | Estudios secundarios |
| Certificación formal | Comprobar ruta/entidad otorgante y versión; no crear un diploma por escribirlo | Primer dan de karate |
| Experiencia profesional civil | Revisar cronología y acceso; no concede permiso institucional | Trabajo en laboratorio civil |
| Ciudadanía/estatus legal | Reglas jurídicas/contexto, no especie | Romulano que declara ciudadanía federada |
| Capacidad especial de especie | Perfil/variación/entrenamiento/alcance; nunca omnisciencia | Vulcano entrenado en fusión mental |
| Rango, mando o autorización de la Flota | Requiere hecho institucional real y autoridad correspondiente | «Fui capitán antes de entrar» |

La clasificación no añade campos al contrato de personaje bloqueado. Solo determina qué fuente es necesaria para la afirmación que aparece en campos existentes. Las contradicciones se muestran al jugador para que las corrija; ninguna IA altera el texto de manera silenciosa.

## 3. Madurez individual: regla necesaria pero aún no autorizada para producto

La edad mínima numérica por especie **es un umbral jugable**, no una prueba automática de adultez biológica. Incluso por encima del umbral se debe tener una regla F10 sustentada en el perfil vital de especie, o la autorización expresa de una política de madurez que incluya evidencia individual. El marcador `adult_equivalent_status=true` aportado por el jugador se interpreta como una **declaración**, no una atestación.

No se pide un expediente clínico ni documentación real al jugador para una criatura ficticia. La fuente F10 de antecedentes iniciales podría comprobar internamente la etapa vital y la coherencia del borrador, **pero todavía no existe ni están aprobados esos criterios concretos por especie**. El estado continuará `REVIEW_REQUIRED` hasta implementar y respaldar esa política. En las tres especies especiales (`changeling`, `jem_hadar`, `vorta`) se mantiene el bloqueo específico. Las cinco especies Delta permanecen fuera de la campaña principal. Los nacimientos que alcanzan el umbral durante 2383 quedan pendientes por no conocerse día/mes de comienzo.

## 4. Flujo previsto (sin IA real ni escritura)

1. El jugador escribe un borrador con los campos existentes: edad, especie, intereses, estudios, experiencia y objetivos.
2. El HOST presenta la propuesta; el precheck y la puerta objetiva F10 determinan incompatibilidades cronológicas, de especie, era o autoridad.
3. Una fuente F10 que haya sido **aprobada e implementada en el futuro** podrá emitir una atestación interna sobre hechos narrativos personales plausibles o datos verificados. Un identificador que envíe el jugador no suple esa fuente; el registro de la PR #156 comprueba su origen y su vínculo al borrador exacto.
4. La segunda puerta semántica asistida por IA evaluará la **misma** biografía. La IA solo propone sugerencias y contradicciones. La decisión corresponde a F10 y, si falta el evaluador, se conserva el estado `REVIEW_UNAVAILABLE`.
5. Solo después de las dos puertas, un recibo privado de F10 podrá permitir que una tarea separada proponga crear **una sola PERSON** en Core. La admisión a la Academia, el vínculo HOST y los rangos F11 se tratarán por separado.

**Atención al orden:** una fuente inicial puede respaldar la *plausibilidad objetiva* para habilitar la revisión semántica, pero no transforma la biografía en hechos del mundo hasta que la segunda puerta se valide y la operación F10 futura complete el commit. No hay círculo de dependencia con un PERSON preexistente.

## 5. Ejemplos de comportamiento deseado

- **Daniel, humano de 20, karate desde los 8:** historial personal plausible que podrá convertirse en origen de antecedente, tras revisión y controles de fecha. Ni experiencia técnica profesional ni cinturón negro automático.
- **Daniel, humano de 20, primer dan:** posible, pero hay que justificar el entrenamiento y una vía de certificación razonable. F10 no exigirá presentar el certificado físico; tampoco lo expedirá porque el jugador lo escriba.
- **Humano de 20, médico especialista y seis años de mando:** títulos y servicio no acreditados, y cronología probablemente inviable. La comprobación de plausibilidad estructural no aprueba tales afirmaciones.
- **Romulano adulto con ciudadanía federada:** la edad no prueba ciudadanía ni acceso a la Academia en 2383; se necesitará contexto legal autorizado.
- **Ocampano de 2 años:** mínimo numérico admitido en diseño, pero no seleccionable para la campaña principal hasta el DLC.
- **Cambiante de cien años:** no se decide madurez por edad ni apariencia, pues no existe la política específica.
- **Protagonista de 20 años que intenta insertar `validated_creation_ref`:** rechazo, nunca se acepta la autorización procedente del cliente.

## 6. Pruebas e interpretación

Archivo contractual permanente: `sistemas/gameplay/character_creation/f10_initial_background_policy_v0.1.json`.

Referencia deliberadamente limitada: `desarrollo/tools/validation/f10_initial_background_reference.py`, recibe ejemplos **estructurados de ensayo** y devuelve únicamente `REVIEW_REQUIRED` o `CHANGES_REQUIRED`. No procesa lenguaje libre, no consume IA, no firma ni emite atestaciones, no crea PERSON y no constituye el validador real. Consulta la política de edades existente, sin copiar 25 umbrales.

Pruebas: `desarrollo/tools/validation/test_f10_initial_background_policy.py`, invocadas con `python -m unittest discover -s desarrollo/tools/validation -p 'test_f10_*.py' -v`. Las regresiones verifican categorías, enlaces a fuentes, ejemplos, límites de edad, frontera 2383, DLC, especies especiales, intento de inyección de autoridad, no privilegios, privacidad y mantenimiento de ambas puertas. **PASS en CI solo demuestra el alcance offline/contractual.**

## 7. Reparto y siguientes decisiones

**ChatGPT:** este corte documental + referencia offline + tests. No modifica reglas bloqueadas ni CoreRPG y no introduce proveedor IA.

**Codex:** siguiente corte C++ tras auditoría, **modelo GPT-6, razonamiento Alto**. Integrar una fuente F10 interna de antecedentes con resultados trazables, faltas de evidencia pendientes y controles negativos. No elegir proveedor IA ni resolver por intuición reglas de madurez biológica. PR separada, regresiones Windows/Linux/ASan, Release y revisión independiente. La integración semántica local será otro corte tras elegir y autorizar un proveedor/modelo.

**Pendientes de producto:** criterio autoral por especie/individuo de la madurez, fecha completa de inicio, especies especiales, proveedor semántico real y publicación posterior de PERSON. H06-P06-A/HU-08/M1 **PARCIALES / NO CERTIFICADOS**. No iniciar H07.
