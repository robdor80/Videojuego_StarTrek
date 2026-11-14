# H06-P06-A — Validación de biografía antes del alta de Academia

**Fecha:** 14-11-2026 · **Propiedad:** F10 (dominio y reglas); HOST (orquestación y entrega); CoreRPG (hechos).  
**Estado de este corte:** **IMPLEMENTADA solo precomprobación Python de referencia, con pruebas pendientes de CI en el momento de redacción**. **NO** es la validación objetiva completa de F10, **NO** hay revisión semántica de producto ni candidato real. F10/H06-P06/HU-08/M1 permanecen abiertos.  
**Contrato añadido:** [f10_biography_validation_interface_v0.1.json](../../../../sistemas/gameplay/character_creation/f10_biography_validation_interface_v0.1.json).  
**Referencia ejecutable:** [f10_biography_precheck.py](../../../../desarrollo/tools/validation/f10_biography_precheck.py) y [sus pruebas](../../../../desarrollo/tools/validation/test_f10_biography_precheck.py).

## 1. Fuentes auditadas (no se alteran)

- `sistemas/gameplay/character_creation/character_creation_contract_v1_0.json`: orden de creación, campos obligatorios/opcionales, biografía bloqueada y ausencia de puntos de habilidades.
- `sistemas/gameplay/character_creation/biography_validation_rules.md`: **dos puertas obligatorias** (reglas objetivas y revisión semántica asistida por IA); ninguna puede anular a la otra.
- `sistemas/gameplay/character_creation/player_profile_contract.json`: el usuario, su apodo y su personaje son identidades diferentes.
- `sistemas/gameplay/character_creation/prior_activity_model.json`: aficiones, formación y certificaciones requieren tiempo y evidencia; no equivalen a capacidades profesionales gratuitas.
- `sistemas/gameplay/species/species_biology_contract.json` y perfiles `species/profiles/*`: los umbrales de madurez exactos **no están fijados para todas las especies**. No asumir 18 años para humanos o para todas las especies, ni madurez solo porque un cliente envíe `adult_equivalent_status=true`.
- `sistemas/gameplay/organizations/character_affiliation_citizenship_contract.json`: especie, origen, ciudadanía, pertenencia, cultura y lealtad son hechos diferentes.
- `F10_H06_P06_FACTIBILIDAD_NATIVA_2026-11-14.md` (PR #150 fusionada): el pin de Core permite guardar y restaurar una PERSON **de ensayo**, no aprobar biografías ni crear un candidato real.

**Año aprobado de la campaña:** 2383. **Día y mes:** sin fijar. No resolver por intuición la edad exacta de un nacimiento próximo a la fecha de inicio.

## 2. Flujo de producto que debe permitir la implementación futura

| Etapa | Entrada | Resultado admisible | ¿Publica PERSON? |
|---|---|---|---|
| 0. Edición | Borrador de personaje, perfil de jugador separado | Borrador modificable | No |
| 1. Precomprobación | Borrador no confiable | `CHANGES_REQUIRED` o `REVIEW_REQUIRED`, sin efectos | **No** |
| 2. Objetiva autoritativa F10 | Borrador canónico + especie, contexto, regla, cronología y evidencias | `OBJECTIVE_VALID`, correcciones o revisión pendiente | No |
| 3. Coherencia semántica F10 asistida por IA | La **misma** biografía congelada, evaluación objetiva y política de revisión | Evidencia de revisión vinculada a borrador/contexto/reglas y verificada por F10 | No |
| 4. Commit F10 privado | Dos puertas válidas, campaña/generación vigentes, intento único HOST | PERSON candidata y hecho de origen atómicos | **Sí, una sola** |
| 5. Admisión F10 | Pruebas de acceso y decisión auténtica, plaza/cohorte disponible | Admisión y plaza de cadete | Mantener la misma PERSON |

Ningún paso de precomprobación, IA o interfaz de usuario puede emitir por sí solo una credencial `validated_creation_ref`, `person_id`, admisión, plaza o comisión profesional. No se aceptan `trusted=true`, nombres de modelo, mensajes de chat o firmas suministradas por el cliente como prueba de autoridad.

**Resultado de ejemplo:** personaje humano de 20 años que comenzó karate a los 8 → `REVIEW_REQUIRED`, no aprobación automática. Si declara haber nacido en 2384, ser menor de edad o haber empezado una actividad a los 21 teniendo 20 → `CHANGES_REQUIRED`, sin cambios en Core.

## 3. Lo que hace hoy la referencia Python

`f10_biography_precheck.evaluate(draft, campaign_year=2383)` es una función pura que:

- Comprueba presencia de los campos de creación sin alterar el contrato bloqueado, detecta campos extra y rechaza campos de autoridad visibles u ocultos dentro de estructuras.
- Comprueba que el identificador de especie remite a un perfil versionado conocido; **no** deduce adultez, cultura, personalidad ni ciudadanía de esa especie.
- Rechaza edades negativas, fechas inexistentes, nacimientos posteriores al **año** de campaña y contradicciones cronológicas evidentes en actividades con edades numéricas.
- Calcula una huella SHA-256 canónica **informativa**, que sirve para detectar modificaciones de una propuesta, pero **no prueba procedencia**, no contiene aprobación ni sustituye el recibo nativo.
- Devuelve exclusivamente `CHANGES_REQUIRED` o `REVIEW_REQUIRED`, `person_created=false`, `world_state_mutated=false`, `validated_creation_ref=null`. No llama al CoreRPG, UE5, servicios externos ni IA, y no escribe archivos.

Los datos que carecen de soporte semántico o de una regla objetiva vigente quedan **pendientes de revisión**, no se inventan. El precheck no determina que una carrera universitaria o certificación sea plausible solo por la forma del JSON. Un resultado `REVIEW_REQUIRED` **no habilita publicar una PERSON**. Por tanto, aunque las pruebas offline pasen, la validación de producto sigue bloqueada.

### Precauciones de persistencia y privacidad

La biografía, sus posibles datos familiares o médicos y las observaciones de una IA no se registran en logs de diagnóstico sin necesidad y consentimiento; los informes de error solo mencionan campo y código. Para guardar una biografía real en Core, F10 tendrá que versionar una representación canónica con codificación UTF-8, límites e integridad; **no adoptar** la codificación de relaciones por byte del ensayo #150 sin auditoría.

## 4. La segunda puerta: contrato del verificador semántico

Se propone una interfaz **interna** F10, sin proveedor impuesto (no contratar nube ni levantar servidores solo para esto). El flujo exacto del proveedor deberá validarse antes de conectarlo.

El verificador F10 no confía en una respuesta de IA por su texto. Conserva o genera de manera privada evidencia ligada a:
- la huella **exacta** del borrador y del contexto de campaña;
- versiones del catálogo, reglas objetivas y política semántica;
- la identidad/versión del evaluador y las conclusiones, distinguiendo observaciones y contradicciones comprobables;
- la decisión adoptada por el dominio después de evaluar evidencias y reglas, con un origen que un Blueprint o PADD no pueda simular.

Si cambia el nombre, edad, especie, experiencia, contexto, reglas o política, el dictamen anterior **caduca**. Una sugerencia de IA nunca modifica silenciosamente la biografía; el usuario verá contradicciones y podrá corregirlas antes de solicitar nueva revisión. Si el evaluador no está disponible, el estado sigue `REVIEW_REQUIRED` o `REVIEW_UNAVAILABLE`, sin publicación. **La revisión asistida por IA sigue siendo obligatoria**, pero no implica que la IA sea autoridad ni que exista un proveedor funcional hoy.

La implementación nativa decidirá la representación de recibo privado más simple compatible con el único HOST local; hashes y cadenas no son privilegios. No introducir certificados, infraestructura remota ni autenticaciones de red desproporcionadas.

## 5. Qué queda por implementar (Codex)

**P06-A1:** objetivar con F10 reglas ejecutables: fuente de edades de madurez por especie/contexto, acceso, cronología, tecnología disponible, estudios y certificaciones. Donde no haya datos aprobar una política explícita o devolver pendiente; **no** fijar arbitrariamente edades o poderes.

**P06-A2:** interfaz de revisión semántica asistida por IA, optando por una vía compatible con el juego local y una política verificable de F10. Un proveedor no disponible no puede generar resultados positivos de mentira.

**P06-A3:** comprobar la misma biografía en ambas puertas y materializar un recibo interno no falsificable desde el cliente, invalidado por cambios. Solo entonces la siguiente tarea H06-P06-B implementará el commit de la PERSON candidata y el vínculo H03.

**P06-A4:** tests de conflicto, campos prohibidos, biografía alterada, revisión caducada, rechazo por regla, indisponibilidad de IA, no mutación de Core y regresiones de F10/HOST.

**Evidencias de este corte:** los tests Python nuevos son **offline**, no entregan un nuevo PASS de CB-01..CB-24. Estos casos siguen con **22 BLOCKED y 2 NOT_RUN**; HU-08/H06-P06/M1 parciales. No iniciar Unreal, trabajo de nave, F11 o H07 como consecuencia automática.

## 6. Coordinación y recursos

- Arquitectura y referencia de bajo riesgo: **ChatGPT**.
- Núcleo C++ de F10, integración de IA y puentes de autoridad: **Codex, GPT-6, razonamiento Alto** con su propia PR Draft.
- CoreRPG sigue fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`. No tocar pruebas históricas ni revertir F04/F05; no fusionar PR grandes sin auditoría.
- Ejecutar CI F10 mediante la suite existente. El precheck Python forma parte del código versionado de validación, no de una compilación Unreal ni de un laboratorio permanente.
- Evitar generar cachés grandes o duplicar engines. Consultar AGENTS.md para temporales y no borrar worktrees Git activos en la limpieza concurrente.

**Cierre posible de H06-P06-A:** la prueba de referencia y el contrato quedan PROBADOS en su alcance; solo la implementación futura con entradas reales, validadores objetivos y semánticos y pruebas negativas podrá declararse **VALIDACIÓN DE PRODUCTO PROBADA**.
