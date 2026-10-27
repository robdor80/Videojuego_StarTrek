# Modelo de consulta documental — Sin comportamiento ejecutable

## Flujo de preguntas
Una petición, como «quiero entrar en espacio romulano», debe conectarse con ocho piezas documentales, pero ninguna por sí sola expide un pase:

1. Identidad de destino. Buscar `location_id` en LORE-01 C. No inferir pertenencia política por coordenadas no calibradas.
2. Época y continuidad. Separar fecha, eventos **realmente sucedidos antes del arranque** y futuros que pueden divergir.
3. Gobierno y instituciones. Buscar `civilization_id` de B y su `classification`, no tratar red clandestina como Estado.
4. Relaciones y acuerdos. Consultar D por `relation_id`, evento exacto y sujetos jurídicos.
5. Contexto cultural. Enlazar perfiles de A/A.1 solo si se trata de interlocutores concretos y sin estereotipos.
6. Información de observador. Distinguir lo que sabe el jugador, la tripulación y una organización del hecho del universo. La obtención y la confidencialidad se resolverán por el Core.
7. Capacidad/autorización. Consultar misión, puesto, órdenes, permisos, recursos, restricciones y condiciones actuales: *el texto de E no habilita acciones*.
8. Respuesta al jugador. Comunicar comprobado, desconocido, inferido y propuesta de remisión al mando cuando proceda. Toda modificación del mundo requerirá acción validada exclusivamente por CoreRPG.

## Contratos de procedencia
`source_refs` referencia identificadores del registro del proyecto; no son directamente permisos ni diagnósticos de sensor. `not_before_event_id` es un filtro **necesario pero no suficiente**: aunque el evento haya ocurrido, el receptor debe conocerlo. Las relaciones históricas son ejemplos de contexto, no un autómata de la historia canónica.

### Ejemplo: petición de tránsito romulano
- Pregunta correcta del alférez: «¿Cuál es la última información verificada de ruta y restricciones que **mi puesto** puede ver?».
- Informe correcto: localización con precisión declarada; si existe una advertencia documental sobre Zona Neutral; relación histórica aplicable a la fecha/continuidad; no constancia de permiso salvo dato acreditado.
- Propuesta correcta: solicitar confirmación al mando/autoridad competente, sin emitir una autorización ficticia.
- Respuesta incorrecta: «Se autoriza el paso porque los romulanos fueron aliados contra el Dominio», especialmente antes de los hechos de 2374.
- Resultado de la operación: **indeterminado en documentación**; será consecuencia de estado real y orden autorizada.

### Ejemplo: orden supuestamente emitida por Sección 31
No entregar archivos clasificados ni ejecutar detenciones por una simple afirmación de identidad. Registrar la alegación, comprobar cadena de autoridad y comunicación según los contratos operativos existentes. Tampoco adjudicar automáticamente falsedad: el actor puede disponer de documentos, ser impostor o estar desinformado. E no decide el desenlace.

### Ejemplo: atención médica urgente a civilización prewarp
La petición de ayuda, riesgo físico y deber de no interferencia pueden entrar en conflicto. No fabricar un permiso absoluto ni bloquear de antemano toda decisión narrativa. Obtener hechos, autoridad, alternativas, exposición cultural y consecuencias posibles; la acción final debe quedar ligada a las reglas/estado de campaña ya existentes.

## Por qué hay una frontera técnica
CoreRPG `4.9` aporta conocimiento; `4.10` acciones y simulación; `4.11` inspector; `4.12` builder de contexto autorizado, comprobado en `main` durante la preparación. No significa que estos JSON estén consumidos ni que exista el adaptador de consulta de Star Trek. La capa de presentación de UE5 debe mostrar solamente la proyección autorizada que reciba, con información de procedencia cuando corresponda.

**No es una API, JSON Schema de contenido ejecutable, orden, función de autorización ni plan de integración aprobado.**
