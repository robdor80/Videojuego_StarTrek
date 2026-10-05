# INF-401 — Sistemas de información Starfleet

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 4.ª clase · Trimestre 1**

## Finalidad

Dar al cadete autonomía básica para consultar, registrar y manejar información autorizada sin confundir acceso técnico con autoridad, ni una respuesta del ordenador con verdad omnisciente.

INF-401 enseña a utilizar la computadora de Starfleet como servicio de información y control, a trabajar con terminales y PADD, a entender identidad y permisos, a buscar información sin pedir al sistema que invente respuestas, y a reconocer por qué registros, privacidad y trazabilidad importan.

---

# INF-401-U01 — Computadora y terminales

## 1. La computadora no es una consola concreta

La computadora de una nave es un servicio distribuido.

Puede ser accesible, según contexto y era, desde:

- estaciones de puente;
- terminales de pared;
- terminales de Ingeniería;
- alojamientos;
- PADD;
- interfaces de voz;
- sistemas médicos o de seguridad autorizados.

El punto de acceso cambia. La lógica de autoridad no.

## 2. Qué puede hacer

La computadora puede:

- consultar datos;
- calcular;
- correlacionar información;
- recuperar registros autorizados;
- iniciar solicitudes de acción;
- presentar resultados.

Pero no decide por sí sola qué es verdad en el mundo ni ejecuta acciones importantes sin validación.

## 3. Consulta frente a acción

Una consulta pregunta por información.

Ejemplos:
- hora;
- roster de guardia;
- curso;
- ETA;
- estado de un sistema;
- historial autorizado.

Una acción solicita cambiar algo.

Ejemplos:
- contactar un departamento;
- reservar un recurso;
- iniciar un diagnóstico;
- transferir datos;
- cambiar una configuración permitida.

Las acciones requieren validación de autoridad, contexto y estado.

## 4. El ordenador no es omnisciente

Si preguntas:

> “¿Hay naves romulanas en el sistema?”

la computadora solo puede responder con lo que la nave sabe.

> “No se han detectado naves romulanas”

no significa:

> “No existen naves romulanas”.

La primera frase describe conocimiento disponible. La segunda afirmaría una verdad universal que puede estar fuera del alcance de los sensores.

## 5. La IA es una capa de interpretación

Cuando una petición es simple, el sistema debería resolverla por rutas deterministas.

La IA puede intervenir para entender lenguaje complejo o resumir información, pero su resultado debe convertirse en una petición estructurada que después pasa por reglas autoritativas.

### Autoevaluación

1. ¿Por qué la computadora no debe tratarse como una única consola?
2. ¿Qué diferencia existe entre consulta y acción?
3. ¿Por qué “no detectado” no significa “no existe”?
4. ¿Puede una IA cambiar directamente el estado de la nave?
5. Pon dos ejemplos de consulta rutinaria.

---

# INF-401-U02 — PADD y flujo personal

## 1. Qué representa un PADD

En el juego, un PADD es una interfaz portátil para trabajar con información autorizada.

Puede servir para:

- consultar material académico;
- leer documentos;
- realizar anotaciones;
- recibir tareas;
- preparar borradores;
- revisar datos transferidos;
- acceder a servicios personales autorizados.

## 2. El documento no pertenece al dispositivo

La información importante debe persistir como registro o documento del sistema, no como “archivo atrapado” en un PADD concreto.

El PADD es una interfaz.

Esto permite que un cadete pueda comenzar una tarea en una terminal, revisarla después en un PADD y entregarla desde otra interfaz autorizada.

## 3. Sincronización contextual

Sincronizar no significa copiar todo a todas partes.

La disponibilidad depende de:

- identidad;
- acceso;
- contexto;
- conectividad;
- políticas de privacidad;
- tipo de dato.

Un registro médico restringido no debe aparecer en un PADD porque el usuario pueda abrir documentos académicos.

## 4. Trabajo académico

El flujo básico puede ser:

1. abrir tarea;
2. consultar instrucciones;
3. trabajar o tomar notas;
4. guardar borrador;
5. revisar;
6. entregar;
7. conservar referencia en el expediente correspondiente.

## 5. Borrador frente a registro final

Un borrador puede cambiar.

Un registro final o evento autoritativo no debe reescribirse silenciosamente.

Esta diferencia será importante más adelante en logs profesionales.

### Práctica

Abre una tarea académica, crea una anotación, guarda un borrador y prepara una entrega sin modificar la fuente original.

### Autoevaluación

1. ¿Por qué un PADD es una interfaz y no la “propiedad” del documento?
2. ¿Qué factores pueden limitar sincronización o acceso?
3. ¿Qué diferencia existe entre borrador y registro final?
4. ¿Por qué no debe aparecer automáticamente información restringida?
5. Describe un flujo básico de trabajo académico.

---

# INF-401-U03 — Identidad y acceso

## 1. Autenticación y autorización no son lo mismo

**Autenticación** responde:

> ¿Quién eres?

**Autorización** responde:

> ¿Puedes hacer esto?

Un sistema puede saber perfectamente quién eres y aun así negar una acción.

## 2. Señales de identidad

El proyecto puede usar varias señales:

- sesión activa;
- identidad del terminal;
- comunicador;
- voz cuando proceda;
- localización;
- asignación de servicio.

No todas las acciones requieren que el usuario repita credenciales constantemente si su identidad ya está establecida.

## 3. Qué determina el acceso

La autorización puede depender de:

- personaje;
- rango;
- puesto;
- departamento;
- estado de servicio;
- clearance;
- alerta actual;
- ubicación;
- función solicitada;
- autorización temporal;
- override válido.

## 4. El rango no abre todo

Tener mayor rango no concede acceso automático a:

- historiales médicos;
- datos de Seguridad;
- Inteligencia;
- registros privados;
- información clasificada.

La necesidad funcional y la autorización específica también importan.

## 5. Mínimo acceso

El principio práctico es:

> dar acceso suficiente para realizar la función, no acceso universal “por si acaso”.

Esto reduce errores, abusos y exposición innecesaria.

## 6. Acciones sensibles

Algunas funciones pueden exigir:

- confirmación explícita;
- código de autorización;
- doble autorización;
- contexto de emergencia válido.

Los overrides de emergencia deben ser auditables y estar gobernados por reglas, no por improvisación de IA.

### Autoevaluación

1. Diferencia autenticación y autorización.
2. ¿Por qué el rango no concede acceso universal?
3. Nombra cuatro factores que pueden influir en autorización.
4. ¿Qué significa principio de mínimo acceso?
5. ¿Por qué un override de emergencia debe quedar auditado?

---

# INF-401-U04 — Búsqueda de información

## 1. Buscar no es preguntar a un oráculo

Una buena consulta debe expresar:

- qué quieres encontrar;
- sobre qué ámbito;
- con qué filtros;
- dentro de qué fuentes autorizadas.

## 2. Tipos de consulta

La computadora puede buscar, por ejemplo:

- horarios;
- roster;
- estado de sistemas;
- mantenimiento;
- navegación;
- sensores;
- registros;
- base de datos;
- regulaciones autorizadas.

## 3. Fuente y resultado

Un resultado debe conservar su procedencia cuando sea relevante.

No es lo mismo:

- un sensor;
- un log personal;
- un informe de Ingeniería;
- una entrada de base de datos;
- una interpretación generada.

La fuente condiciona qué significa el resultado.

## 4. Resultado frente a interpretación

Un sistema puede devolver:

> “Tres lecturas muestran aumento de radiación.”

Interpretar que:

> “la causa es un arma enemiga”

requiere evidencia adicional.

El sistema no debe rellenar automáticamente el salto lógico.

## 5. Consultas complejas

Una petición como:

> “Resume los eventos relevantes de las últimas seis horas que puedan explicar la pérdida de potencia”

puede necesitar:

1. recuperar fuentes;
2. comprobar permisos;
3. correlacionar;
4. resumir;
5. conservar incertidumbre.

La IA puede ayudar a expresar el resumen, pero no inventar eventos que no existan.

### Práctica

Formula una búsqueda útil para localizar un reglamento, una incidencia técnica y un resultado de sensores sin pedir conclusiones que la fuente no contiene.

### Autoevaluación

1. ¿Qué debe especificar una buena consulta?
2. ¿Por qué importa conocer la fuente?
3. ¿Qué diferencia existe entre resultado e interpretación?
4. ¿Puede un resumen generado incluir hechos no registrados?
5. Pon un ejemplo de búsqueda compleja legítima.

---

# INF-401-U05 — Registros y trazabilidad

## 1. Por qué registrar

Una institución compleja necesita poder reconstruir qué ocurrió.

Los registros permiten:

- continuidad;
- debrief;
- evaluación;
- investigación;
- mantenimiento;
- responsabilidad;
- aprendizaje.

## 2. Dos cosas que no deben confundirse

**Operational Event Log**  
Conserva hechos operativos autoritativos.

**Logs escritos por personas o instituciones**  
Conservan lo que alguien decidió registrar sobre esos hechos.

La diferencia es fundamental.

## 3. Ejemplo

El Operational Event Log puede registrar:

- orden recibida;
- barrido iniciado;
- resultado creado;
- informe emitido.

Un log personal puede decir:

> “Pensé que el contacto era hostil.”

Eso es una interpretación del personaje, no un hecho objetivo.

## 4. Historia append-only

Los eventos registrados no deben editarse silenciosamente.

Si una información anterior era incorrecta:

- se registra la corrección;
- no se borra el pasado.

Esto permite auditar cómo evolucionó el conocimiento.

## 5. Autoría y marca temporal

Un registro debe poder conservar:

- quién lo creó;
- cuándo;
- qué tipo de registro es;
- a qué hechos o documentos hace referencia;
- qué permisos lo protegen.

### Práctica

Distingue qué elementos de una situación pertenecen al Event Log y cuáles a un log personal o de departamento.

### Autoevaluación

1. ¿Para qué sirve la trazabilidad?
2. Diferencia Operational Event Log y log personal.
3. ¿Debe borrarse un registro antiguo cuando aparece una corrección?
4. ¿Por qué importa conservar autoría y hora?
5. ¿Puede una opinión personal convertirse automáticamente en verdad operativa?

---

# INF-401-U06 — Privacidad y uso responsable

## 1. Poder consultar no significa tener derecho a consultar

El acceso técnico y la autorización son cosas distintas.

Un cadete puede encontrarse ante información que el sistema sabe que existe pero que no tiene permiso para leer.

## 2. Datos restringidos

Pueden requerir protección especial:

- información médica;
- Seguridad;
- Inteligencia;
- datos clasificados;
- logs personales;
- expedientes sensibles.

La computadora debe evitar incluso filtrar contenido protegido a través de mensajes de error o fragmentos de búsqueda.

## 3. Curiosidad no es necesidad de servicio

Un acceso no se justifica porque:

- sea interesante;
- el usuario tenga mayor rango;
- el dato “pueda resultar útil algún día”.

Debe existir una base de autorización coherente.

## 4. Auditoría

Los accesos sensibles pueden quedar registrados.

Esto permite revisar:

- quién accedió;
- cuándo;
- desde dónde;
- a qué función;
- bajo qué autorización.

## 5. IA y privacidad

La IA no puede usar su capacidad lingüística para saltarse reglas de acceso.

No puede:

- reconstruir contenido restringido;
- revelar un secreto desde otra fuente no autorizada;
- publicar un borrador sin aprobación;
- convertir información privada de un NPC en conocimiento universal.

### Caso

Un cadete sabe que existe un log personal de un instructor y tiene curiosidad por una conversación mencionada allí.

El hecho de saber que el log existe no concede acceso al contenido.

### Autoevaluación

1. ¿Qué diferencia existe entre acceso técnico y autorización?
2. Nombra cuatro tipos de información que pueden estar restringidos.
3. ¿Por qué un mensaje de acceso denegado no debe filtrar contenido?
4. ¿Para qué sirve auditar accesos?
5. ¿Puede la IA reconstruir información privada para “ayudar” al usuario?

---

# Evaluación del curso

INF-401 evalúa:

- comprensión del papel de la computadora;
- uso responsable de terminales y PADD;
- autenticación y autorización;
- búsqueda con procedencia;
- distinción entre hechos e interpretación;
- registros y trazabilidad;
- privacidad.

No exige:
- programación;
- administración avanzada;
- arquitectura informática profunda;
- memorizar comandos de interfaz específicos de una sola era.

# Tratamiento por era

Cambian interfaces, dispositivos y presentación.

Permanece estable la lógica de:

- identidad;
- autorización;
- procedencia;
- trazabilidad;
- privacidad;
- autoridad del estado de juego.

# Referencias internas

- `gameplay/ship_operations/ship_computer/README.md`
- `gameplay/ship_operations/ship_computer/access_control_rules.json`
- `gameplay/ship_operations/ship_computer/computer_query_action_catalog.json`
- `gameplay/records_and_logs/README.md`
- `gameplay/ship_operations/operational_event_log/README.md`
- `gameplay/careers/academy_path/course_resolution.md`

Estas referencias constriñen la semántica. Interfaces concretas y ejercicios pedagógicos pueden variar por era.
