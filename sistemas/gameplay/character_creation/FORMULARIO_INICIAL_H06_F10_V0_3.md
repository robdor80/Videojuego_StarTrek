# H06/F10 — Formulario inicial v0.3 y personalidad del aspirante

**Fecha:** 2026-11-15. **Estado:** REFERENCIA FUNCIONAL, SIN INTEGRACIÓN UE5/API/CORE AUTORITATIVA.

## Cambios de diseño solicitados

1. **Se elimina el campo de modelo 3D** del proceso biográfico. Solo queda la descripción física que ya acepta F10 (\`appearance_profile\`). La selección, creación o carga de un modelo 3D tendrá lugar **después**, dentro del videojuego, mediante un catálogo UE5 verificado. La malla no modifica especie, aptitud ni biografía.
2. **Separa dos ambiciones:** \`objective\` (área de interés: exploración, ciencias, ingeniería, etc.) y \`career_goal\` (puesto deseado: capitán de nave, primer oficial, jefe de ingeniería, jefe de ciencias, jefe médico, jefe de seguridad, jefe de operaciones, navegación, táctico, instructor, diplomacia, especialista u otro). Son aspiraciones; no anticipan rangos, destinos, acceso ni cualificaciones.
3. **Nueva personalidad autodeclarada:** descripción libre del carácter, valor predominante, estilo de trabajo en equipo y respuesta habitual ante presión. Opcionalmente liderazgo, gestión de conflictos, expresión emocional, hasta tres fortalezas, áreas de mejora y razonamiento ante una situación ética.
4. **Evaluación psicológica institucional separada:** se reserva \`evaluacion_psicologica_institucional:{estado:"NO_REALIZADA",resultado:null}\` como marcador de borrador. La futura evaluación de la Academia **no** nace de marcar cuatro casillas ni de que la IA redacte una etiqueta; debe diseñarse como proceso institucional F10 autorizado, con criterios, testimonios, procedencia, privacidad y evidencias. No usar esta maqueta como test clínico ni inferir diagnósticos.
5. **Importar JSON anterior:** el prototipo puede recuperar un borrador v0.1/v0.2/v0.3 y recuperar nombre, especies, edad, estudios, actividades y biografía. Si la versión anterior carece de objetivo profesional o personalidad, el usuario debe revisarlos y añadirlos; nunca fabricarlos.

## Contratos y autoridad

- \`sistemas/gameplay/character_creation/f10_formulario_inicial_v0.3.json\`: contrato declarativo con etiquetas, opciones, obligatoriedad, condiciones y procedencias.
- \`audiovisual/ui/academy/formulario_cadete_v0.3.html\`: formulario HTML móvil/básico, abrible sin red ni servidor; genera un borrador JSON local.
- \`sistemas/gameplay/character_creation/character_creation_contract_v1_0.json\`: **contrato F10 histórico cerrado; no modificar de forma improvisada**.
- \`sistemas/gameplay/characters/character_definition_contract.json\` ya admite el campo de referencia \`personality_seed\` a futuro. **No convertir la autodescripción en dicho dato autoritativo sin validación y procedencia**.
- \`sistemas/gameplay/character_creation/character_sheet_model_v1_0.json\`: la ficha del personaje y los expedientes Academia/Flota son entidades documentales diferentes.

### Propuesta de estructura de borrador

\`\`\`json
{
  "formulario": "F10/H06 - referencia 0.3",
  "estado": "BORRADOR_PENDIENTE_VALIDACION_F10_Y_REVISION_IA",
  "perfil_jugador_no_autoritativo": {"nickname":"..."},
  "f10_draft": {
    "species_id":"human_vulcan_hybrid",
    "age_or_birth_date":22,
    "initial_long_term_objective":"Área de interés: Ciencias. Objetivo profesional (aspiración, no nombramiento): Capitán/a al mando de una nave. Motivación: ...",
    "prior_experience":[
      "Relato biográfico del aspirante (declaración libre): ...",
      "Autodescripción de personalidad (no evaluación institucional): ..."
    ]
  },
  "personalidad_autodeclarada": {
    "source":"SELF_REPORTED_BY_PLAYER_NOT_STARFLEET",
    "description":"...",
    "values":"curiosity",
    "teamwork_style":"collaborative",
    "stress_style":"analyze",
    "leadership_style":null,
    "conflict_style":null,
    "emotion_style":null,
    "strengths":[],
    "growth_areas":null,
    "ethical_dilemma":null,
    "game_effects":"NONE",
    "institutional_conclusion":null
  },
  "evaluacion_psicologica_institucional":{"estado":"NO_REALIZADA","resultado":null}
}
\`\`\`

El ejemplo enseña los campos nuevos relevantes; **no es un JSON completo apto para enviarlo al HOST**. En la integración, solo \`f10_draft\` se presenta como entrada no fiable a F10. El resto es contexto UI/borrador, nunca una orden de creación.

La autodescripción se copia **temporalmente** como texto narrativo dentro de \`prior_experience\` porque el contrato nativo F10 bloqueado aún no admite \`personality_seed\` como parámetro directo de creación. En la integración real habrá que versionar un enlace de perfil/expediente autorizado, evitar duplicación persistente y distinguir lo **DECLARADO** de lo **OBSERVADO** por acciones posteriores. El HTML no emite un \`validated_creation_ref\` ni certificados.

## Cómo debería influir en el juego

**Fase inicial:** no altera mecánicas, puntuaciones, admisión, rangos o acceso a destinos. Debe conservarse como autodescripción del personaje y ofrecer un punto de comparación futuro.

**Fase narrativa futura, previa autorización:** NPC y profesores podrían reaccionar a un estilo manifestado **siempre que esté corroborado por interacciones del juego**. Un personaje que se describió valiente puede reaccionar con miedo y cambiar; no fijar una personalidad inmutable a partir de respuestas iniciales. La IA solo narra y formula observaciones, no modifica hechos CoreRPG.

**Evaluación institucional durante la Academia:** diseñar por separado escenarios de toma de decisiones, trabajo de equipo, integridad, mando y seguridad bajo presión. Una evaluación ficticia, no un diagnóstico médico. Requerirá contratos F10/F11, validación y autorización de consecuencias si se incorporan, no bastará con una respuesta de modelo.

## Notas de revisión a partir de la ficha de Kazan Rise

- En \`origin\` aparece «Tierra» pero el relato incluye **Vigo**: conviene introducir localidad + planeta si se conoce, sin inventarla cuando no esté declarada.
- Kung-fu intensivo y piano desde los cuatro años son antecedentes **posibles**, no se pueden convertir en maestría sin matices; conservar duración, intensidad y documentación de formación.
- Una licenciatura o grado civil es una **afirmación biográfica** verificable de manera contextual, no un título profesional emitido por el HOST.
- La frase «explotar la Galaxia» aparenta ser una errata por «explorar»; sugerencia de la IA, no fallo de edad ni motivo automático de rechazo.
- «Sin familia» puede querer decir orfandad, ausencia de contacto o falta de datos; no reinterpretar sin la historia del jugador.

## Límites y criterio de cierre

- Prototipo independiente comprobado en navegador con importación del JSON de Kazan Rise, nuevos campos requeridos y descarga de borrador; no hubo error JavaScript en esa ejecución.
- No se ha ejecutado una entrevista Starfleet, ninguna prueba diagnóstica ni una IA de revisión semántica real.
- No modificar CoreRPG, sistema de ascensos F11, datos históricos o motor Unreal; PR Draft hasta auditoría y autorización de fusión.
