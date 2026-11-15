# H06 bis / F10 — Formulario básico de creación de personaje

**Versión:** 0.1.0 · **Fecha:** 2026-11-15
**Alcance:** diseño, opciones y referencia HTML funcional local. **No es una pantalla UE5 ni un adaptador CoreRPG.**
**Propietario de reglas:** F10. **HOST:** coordina la solicitud de evaluación. **CoreRPG:** valida hechos autoritativos y crea PERSON solo tras autorización.

## Entregables

- Contrato de campos, textos, etiquetas y opciones: \`sistemas/gameplay/character_creation/f10_formulario_inicial_v0.1.json\`.
- Formulario ejecutable **sin instalación, sin servidor, sin red**: \`audiovisual/ui/academy/formulario_cadete_v0.1.html\`; abrir el archivo con el navegador. Incluye una copia JSON idéntica del contrato para funcionar con \`file://\`.
- Pruebas de referencia: \`desarrollo/tools/validation/test_f10_character_form_v0_1.py\`.
- Biografías de referencia: HUM-01, VUL-01 y HVA-01, sin sustituir sus matices ni convertir costumbres en requisitos.

## 1. Qué verá el jugador

1. **Identidad:** alias del jugador, nombre del personaje, especie y edad declarada al inicio (2383).
2. **Origen:** lugar de nacimiento, lugares de crianza, ciudadanía declarada (no acreditada), lenguas y familia opcional.
3. **Cultura:** tipo de crianza según especie; humanos sin exigencia ritual, vulcanos e híbridos con campos opcionales para disciplina emocional, Kahs-wan, Tal'oth, Kolinahr, contacto telepático y costumbres familiares.
4. **Aspecto:** descripción visual, más campo de modelo 3D **desactivado** y señalado como pendiente de catálogo.
5. **Formación:** estudios, conocimientos y habilidades **explicados en texto libre**, experiencia civil, certificaciones opcionales. Nunca escoger nivel global ni puntos de habilidades.
6. **Actividades:** una o varias (hasta 10 para mantener el prototipo manejable), con nombre, categoría, edad de inicio, fecha de fin o «continúa» y frecuencia.
7. **Objetivo e historia:** aspiración, motivación para Starfleet y biografía libre.

Los campos opcionales nunca invalidan una ficha por no contestar. No se pregunta al jugador por pon farr, estado médico íntimo ni pareja predestinada. La práctica de Kolinahr solo se trata como extraordinaria cuando el jugador declara haberla completado y exige una explicación narrativa para enviar el borrador.

## 2. Diferencias condicionales

| Especie | Edad mínima | Crianza elegible | Ritos |
| --- | ---: | --- | --- |
| Humano | 18 | Tierra urbana/rural, colonia, nave civil, hogar intercultural u otra | No se muestra lista vulcana por defecto; cultura vulcana aprendida puede describirse en texto |
| Vulcano | 25 | Vulcano tradicional, heterodoxo, otros hábitos en Vulcano o fuera de Vulcano | Kahs-wan, Tal'oth y Kolinahr opcionales, con grados de práctica |
| Híbrido humano-vulcano | **22** | Predominio vulcano, terrestre, mixto u otro | Mismas preguntas opcionales que vulcano, pero **no obligatorias** independientemente del hogar |

**Regla central:** especie biológica no determina ciudadanía, cultura, educación, personalidad, emociones, telepatía o rituales realizados.

## 3. Control objetivo local de la pantalla

La página comprueba únicamente:
- Campos obligatorios presentes y longitud máxima indicada.
- Especie dentro del conjunto de tres; edad entera >= mínimo de especie; no inventar fecha exacta de campaña (se usa edad, no fecha de nacimiento).
- Tipo de crianza compatible con el selector de especie.
- Al menos una actividad y no más de diez; edad de inicio y finalización compatible con la edad actual; categoría y frecuencia conocidas.
- Si se declara Kolinahr **completado**, un breve contexto de formación, sin conceder ni denegar maestría.
- No genera ni entrega identidades Core, permisos, aprobación semántica, matrícula, rangos ni habilidades.

**No realiza:** verificación institucional de estudios/certificaciones, comprobación completa de cronología, revisión de plausibilidad con Sol, emisión F11, creación de PERSON o persistencia de partida. Esas comprobaciones pertenecen a F10/servicio común OpenAI/CORE y requieren sus contratos y credenciales; la maqueta no las finge.

## 4. Construcción del borrador y frontera de autoridad

El prototipo genera un documento **JSON local**, con estas piezas separadas:

\`\`\`json
{
  "formulario": "F10/H06 – referencia 0.1",
  "estado": "BORRADOR_PENDIENTE_VALIDACION_F10_Y_REVISION_IA",
  "perfil_jugador_no_autoritativo": {"nickname": "<alias declarado>"},
  "f10_draft": {
    "display_name": "<nombre>",
    "species_id": "human_vulcan_hybrid",
    "age_or_birth_date": 22,
    "adult_equivalent_status": true,
    "origin": "<nacimiento y crianza>",
    "citizenship_context": "<declaración no acreditada>",
    "culture_context": "<crianza, ritos, educación emocional>",
    "appearance_profile": "<descripción>",
    "prior_education": ["<formación previa>"],
    "prior_activities_and_hobbies": [
      {"name": "Astronomía", "category": "academic_interest", "started_at_or_age": 10,
       "ended_at_or_current": "current", "typical_frequency": "regular"}
    ],
    "prior_experience": ["<habilidades declaradas>", "<experiencia civil>", "<biografía libre>"],
    "initial_long_term_objective": "<aspiración y motivación>"
  },
  "presentacion_no_autoritativa": {"modelo_3d_ref": null, "estado": "PENDIENTE_CATALOGO_UE5"}
}
\`\`\`

**Importante:** el código de producción NO debe enviar el objeto de envoltura a F10. Solo \`f10_draft\` contiene los campos del contrato nativo vigente, y es un **borrador no fiable**. El alias es un dato separado de perfil H03. El aspecto descriptivo sí está dentro de \`appearance_profile\`, pero \`modelo_3d_ref\` **no forma parte de la identidad, genealogía, biología ni de las reglas de personaje**.

El contrato nativo F10 no admite hoy un campo libre llamado \`biography\`; se conserva la narración del jugador como declaración legible dentro de \`prior_experience\`, y las actividades se registran aparte, para no insertar un campo que el motor rechazaría como \`UNEXPECTED_FIELD\`. Esta adaptación es explícita y deberá revisarse en la integración final por si conviene formalizar un campo narrativo nuevo de forma versionada.

## 5. Flujo futuro que deberá integrar Codex cuando corresponda

\`\`\`
Unreal — formularios/cambios de campos
     -> HOST entrega borrador al dominio F10
     -> F10 valida identidad, edad y compatibilidad objetiva
     -> HOST solicita revisión semántica al servicio común OpenAI
     -> F10 verifica respuesta, versión y procedencia
     -> CoreRPG crea PERSON + expediente candidato de forma autorizada
     -> HOST H03 vincula al jugador; H04 conserva estado
     -> F10 tramita separadamente el ingreso como cadete
\`\`\`

La API no está integrada en este HTML. Ningún botón puede fingir que Sol «ha aprobado» una ficha. Si una futura revisión falla por proveedor inaccesible, el borrador no debe perderse ni obtener una validación ficticia.

## 6. Decisión sobre modelo 3D

**Sí al campo visible; no a la carga de un archivo 3D en esta fase.** El valor se mantiene **sin asignar** y no se exporta como un hecho CoreRPG. Cuando existan modelos y un proyecto UE5 verificado, el menú podrá cargar un **identificador de un catálogo de recursos aprobado** (preset humano, vulcano, híbrido, variantes físicas), con previsualización y referencias de asset validadas. No se permitirá introducir rutas de disco, archivos arbitrarios ni inferir capacidades por la malla elegida.

Beneficios: evita dependencias prematuras de assets inexistentes; permite cambiar la representación sin reescribir un personaje validado; impide que una malla humana convierta por error a un híbrido en humano a nivel de reglas.

## 7. Pruebas y límites

- Pruebas puras del ensamblador/validador del borrador ejecutadas en construcción del prototipo: humano 18, vulcano 25, híbrido 22, rechazo de 17/24/21, límites de actividades, Kolinahr, claves F10 permitidas, separación de alias y modelo.
- Pruebas de contrato Python incorporadas a la suite \`test_f10_*.py\`, ejecutables desde checkout.
- No confundir estas referencias con aprobación de IA real, aceptación de UX en navegador, compilación UE5 o emisión de un personaje autoritativo.

**Cierre de esta entrega:** referencia de formulario implementada, con datos y textos disponibles. **Integración UE5/CORE/API: PENDIENTE.**
