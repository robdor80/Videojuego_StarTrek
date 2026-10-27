# LORE-01 A.1 — Comportamiento cultural para NPC relevantes e IA

**Estado:** paquete de autoría y guías de uso pendiente de fusión. **Ámbito de pantalla:** TNG, DS9, VOY, con anclajes históricos retenidos y límites explícitos. **No** es un simulador psicológico, reentrenamiento de modelo o actualización de CoreRPG.

## Qué aporta y para qué

Las 25 guías `profiles/<species_id>_behavior_v0.1.json` completan un repertorio de **normas culturales condicionales**: maneras de comunicarse, de expresar emociones, de resolver desacuerdos, de interpretar autoridad y de formar relaciones. Cada guía contiene advertencias de estereotipos, fuentes, épocas, ejes de variación y **dos ejemplos de individuos distintos compatibles**.

No es correcto decir «es un Klingon, por tanto es agresivo». Sí puede decirse «este oficial fue educado en una Casa donde el honor tiene importancia; cuando se enfrente a un reproche, podría interpretar la dignidad de proteger a civiles como una respuesta honorable, salvo que su historia personal o la escena señalen otra cosa».

## Orden de aplicación (esencial)

1. **Especie**: fisiología y consulta bibliográfica, no personalidad.
2. **Procedencia cultural acreditada**: hogar, tutores, comunidad, escuela, instituciones y afiliación; cero/varias culturas.
3. **Personalidad persistente del individuo**: objetivos, carácter, valores, capacidad emocional, aversiones y biografía; tiene preferencia sobre recomendaciones culturales.
4. **Circunstancias**: jerarquía real, relaciones, obligaciones, enfermedad, estrés, contexto de la conversación, conocimiento permitido y fecha.
5. **Expresión por IA**: tono, matiz y propuesta de reacción, sin atribuirse autoridad sobre el estado del mundo.
6. **Resolución por CoreRPG** de cualquier intención que deba crear consecuencias reales; la IA narra solo lo validado.

La guía de contexto cultural **nunca se adjunta automáticamente al NPC por `species_id`**. El ID sirve para localizar investigación. El motor de creación debe usar `culture_refs` o procedencia social justificada. El estado final de un personaje puede ser contrario a valores de origen, y eso no es un error.

## Alcance y calidad de las fuentes

Los perfiles se apoyan en expedientes `mundo/lore/species/evidence/*_v0.2.json` y perfiles culturales `mundo/lore/cultures/profiles/*`. Los anclajes son por episodio/fuente **no visionado completo de cada escena**. Una interpretación cultural es un posible contexto, no una estadística de comportamiento de toda la población.

- `STRONG_CONTEXTUAL_NORMS` / `CONTEXTUAL_NORMS`: valores relevantes en culturas determinadas, nunca acciones ni porcentajes garantizados.
- `LIMITED_CONTEXTUAL`: evidencia parcial; estilo neutro/individual por defecto.
- `UNKNOWN_NO_DEFAULT`: **ninguna pauta colectiva deducible**.
- `NO_SPECIES_PRIOR`: no existe cultura general de especie homogénea, como en el caso humano.

En especial, andorianos, tellaritas y aenar requieren cuidado: parte del material heredado alude a **Enterprise**, fuera de este corpus TNG/DS9/VOY. No reafirmar aquellas conductas como canon TNG solo porque aparezcan en archivos antiguos. Los breen y pakled tampoco están bien documentados en su vida civil.

## Qué significa para la IA

Los perfiles proporcionan **opciones de comportamiento y contexto**, no un prompt de voz fijo. La IA no escribe ni altera nombres de Casas, genealogía, credenciales, cargos, enfermedades, recuerdos o poderes. Tampoco puede fabricar una obligación cultural para forzar una escena.

La personalidad individual, las relaciones, la memoria y las consecuencias pertenecen al estado persistente y a CoreRPG. Si un NPC aprende otro modo de resolver conflictos, su desarrollo se representa por experiencias y cambios autorizados, no sobrescribiendo su ficha porque «los klingon son así».

## DLC y límites de integración

Kazon, ocampanos, talaxianos, vidianos e hirogen están documentados para **DLC Delta futuro**. No aparece ninguno por generación ordinaria del juego principal. La diáspora el-auriana y presencia Borg canónica de TNG son excepciones expresas: **Borg no es especie**, la asimilación es estado de personaje. El portal de IDEA-0011 sigue sin implementar; jamás se habilita como entrada Borg a Alfa.

Se incluyen índices, contrato, nueve casos de prueba editoriales y validación estructural. A.1 **no modifica** los archivos operativos de especie anteriores, CoreRPG, Unreal, runtime de IA ni tasas de generación. La prueba de runtime y el comportamiento de conversaciones reales siguen pendientes de su fase técnica correspondiente.

## Mapa de archivos

- `behavior_context_contract_v0.1.json` — prioridad, condicionantes, prohibiciones y gates.
- `species_behavior_index_v0.1.json` — 25 perfiles, 20 principales / 5 Delta.
- `profiles/*.json` — 25 guías culturales contextuales.
- `npc_dialogue_context_examples_v0.1.json` — escenarios editoriales positivos y negativos.
- `desarrollo/tools/validation/validate_lore01_a1.py` — integridad documental, fuentes y reglas.
- `desarrollo/tools/validation/test_lore01_a1.py` — regresiones del validador.

**Puerta de fase:** aprobar y fusionar esta PR, verificar `main`, borrar rama y entonces decidir cuándo iniciar LORE-01 B.
