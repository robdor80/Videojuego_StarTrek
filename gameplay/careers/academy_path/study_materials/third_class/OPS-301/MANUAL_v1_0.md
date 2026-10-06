# OPS-301 — Operaciones de puente y coordinación

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 3.ª clase · Trimestre 1**

## Finalidad

Participar de forma supervisada en el trabajo real de un puente. OPS-301 ya no se limita a reconocer estaciones: enseña a seguir el flujo de una orden, mantener una imagen operativa común, coordinar varias estaciones y escalar incidencias sin saturar la cadena de mando.

La regla central del curso es:

> **El puente funciona como un sistema de trabajo distribuido: ninguna estación posee por sí sola toda la información, toda la autoridad ni toda la capacidad de actuación.**

---

# OPS-301-U01 — Puente como sistema de trabajo

## 1. Del mapa de puestos al flujo real

**En primer año aprendiste qué estaciones existen.** Ahora debes comprender cómo se relacionan durante una guardia.

Una situación operativa puede pasar por varias estaciones:

> detección → interpretación → decisión → ejecución → resultado → actualización

Por ejemplo:
- Sensores detecta un contacto;
- Ciencia interpreta parte de la lectura;
- Mando decide investigar;
- Conn ajusta rumbo;
- Ops comprueba recursos;
- Ingeniería informa de limitaciones;
- el resultado vuelve a la imagen común.

## 2. Rol y estación

Un rol define responsabilidad profesional. Una estación es una interfaz desde la que se ejercen determinadas funciones.

No son idénticos.

Un oficial puede ocupar una estación distinta temporalmente, tener un rol más amplio que una sola consola o recibir autoridad limitada por una tarea concreta.

## 3. Mando

Mando no debe ejecutar personalmente todas las funciones.

Su trabajo es mantener intención y prioridad, recibir información relevante, asignar tareas, resolver conflictos de prioridad y asumir decisiones que exceden a estaciones individuales.

## 4. Flujo de información

La información útil debe llegar a quien puede actuar, con suficiente contexto, en el momento adecuado y sin llenar el puente de ruido.

No todo dato merece interrumpir al Capitán.

## 5. Observación de guardia

Un cadete debe poder reconstruir quién detectó, quién informó, quién decidió, quién ejecutó y qué resultado se produjo.

### Práctica

Observa una guardia simulada y dibuja el recorrido de tres eventos desde su detección hasta su cierre.

### Autoevaluación

1. ¿Por qué el puente se considera un sistema de trabajo distribuido?
2. Diferencia rol y estación.
3. ¿Qué responsabilidad principal conserva Mando?
4. ¿Qué hace útil un flujo de información?
5. ¿Qué cinco preguntas permiten reconstruir un evento operativo?

---

# OPS-301-U02 — Órdenes y confirmaciones

## 1. Una orden no es solo una frase

**Una orden debe contener suficiente intención para que el destinatario pueda actuar.** Puede incluir acción, objetivo, prioridad, límite, condición o plazo.

## 2. Acuse

El acuse confirma que la orden ha sido recibida. No significa necesariamente que ya esté completada.

Ejemplos:
- “Recibido.”
- “Rumbo fijado.”
- “Barrido configurado, ejecutando.”

## 3. Confirmación de comprensión

Si una orden es ambigua, contradictoria o imposible, el operador no debe inventar.

Debe pedir aclaración, informar de limitación y ofrecer alternativa cuando proceda.

## 4. Ejecución

Durante la ejecución pueden aparecer bloqueo, demora, cambio de situación, imposibilidad física o falta de autoridad.

El operador debe informar si eso altera la intención de mando.

## 5. Reporte de finalización

Completar una tarea exige cerrar el ciclo. Un buen cierre responde qué se hizo, qué resultado hubo, qué anomalías aparecieron y qué queda pendiente.

### Práctica

Ejecuta cuatro órdenes sencillas, una de ellas ambigua y otra técnicamente imposible.

### Autoevaluación

1. ¿Qué diferencia hay entre recibir una orden y completarla?
2. ¿Qué función cumple el acuse?
3. ¿Qué debes hacer ante una orden ambigua?
4. ¿Qué tipos de bloqueo deben reportarse?
5. ¿Qué debe incluir el reporte de finalización?

---

# OPS-301-U03 — Coordinación entre estaciones

## 1. Dependencias

**Muchas tareas requieren más de una estación.**

Ejemplo:
- Sensores necesita más potencia;
- Ops evalúa disponibilidad;
- Ingeniería confirma capacidad;
- Mando aprueba si altera prioridades.

## 2. Peticiones

Una petición interconsola debe indicar qué se necesita, para qué, prioridad, contexto mínimo y cuándo se necesita.

## 3. Prioridades

Dos estaciones pueden solicitar recursos incompatibles. El operador no debe resolver un conflicto de autoridad superior sin permiso.

Debe identificar qué compite, qué impacto tiene, qué prioridad existe y quién puede decidir.

## 4. Bloqueos

Un bloqueo puede ser técnico, energético, operativo, legal, de autorización o de información.

Clasificarlo ayuda a enviarlo al lugar correcto.

## 5. Handoff

Cuando otra estación asume parte del problema, debe recibir suficientes datos para actuar sin repetir todo desde cero.

Un handoff útil conserva contexto, datos, procedencia, prioridad y estado actual.

### Práctica

Resuelve una tarea que necesita Sensores, Ops e Ingeniería con una restricción de potencia.

### Autoevaluación

1. ¿Qué es una dependencia entre estaciones?
2. ¿Qué debe contener una petición interconsola?
3. ¿Quién debe resolver un conflicto de prioridad superior?
4. Nombra tres tipos de bloqueo.
5. ¿Qué información debe conservar un handoff?

---

# OPS-301-U04 — Imagen operativa común

## 1. Qué significa “situación”

**La imagen operativa común es un resumen compartido de lo relevante para la misión.**

Puede incluir estado de nave, misión actual, contactos, riesgos, tareas activas, restricciones e incidencias.

No es una copia de todos los datos disponibles.

## 2. Estado de nave

Debe distinguir normal, degradado, limitado, crítico o desconocido cuando falte información.

## 3. Contactos

Un contacto debe aparecer según conocimiento real: identificado, provisional, no identificado, perdido y con confianza asociada.

No debe elevarse una hipótesis a certeza solo para “rellenar” el resumen.

## 4. Misión

La orden de misión puede contener autoridad, objetivo, prioridad, área o destino, restricciones y requisitos de informe.

Una orden puede limitar objetivos sin dictar cada decisión táctica.

## 5. Riesgos

La imagen común solo puede incluir riesgos conocidos e incertidumbre conocida.

Los peligros ocultos del World State no aparecen porque sí.

## 6. Actualización

La imagen debe cambiar cuando cambian sensores, daño, órdenes, contactos, política o recursos.

### Práctica

Mantén un resumen de situación durante una simulación con tres cambios relevantes.

### Autoevaluación

1. ¿Qué es una imagen operativa común?
2. ¿Por qué no debe incluir todos los datos?
3. ¿Cómo se representa un contacto incierto?
4. ¿Qué puede contener una orden de misión?
5. ¿Por qué un riesgo oculto no debe aparecer en el resumen?

---

# OPS-301-U05 — Escalado de incidencias

## 1. Resolver localmente

**Un operador puede resolver localmente cuando está dentro de su función, tiene autoridad, el riesgo es controlable y no altera prioridades mayores.**

## 2. Informar

Debe informar cuando cambia el estado relevante, afecta a otra estación, puede afectar a misión o seguridad, crea una restricción o requiere seguimiento.

## 3. Escalar

Debe escalar cuando excede autoridad, exige recursos en conflicto, implica riesgo significativo, cruza departamentos, puede cambiar misión o requiere decisión de mando.

## 4. Urgencia

Urgencia no equivale a gravedad absoluta.

Un problema menor puede ser urgente si el tiempo es crítico. Un problema grave puede no requerir interrupción instantánea si ya está contenido y supervisado.

## 5. Saturación

Escalar todo produce ruido, retraso, dependencia excesiva y pérdida de atención del mando.

No escalar nada produce decisiones fuera de autoridad, riesgos ocultos y sorpresas tardías.

### Práctica

Clasifica diez incidencias como resolver, informar o escalar.

### Autoevaluación

1. ¿Cuándo puede resolverse una incidencia localmente?
2. ¿Cuándo debe informarse?
3. ¿Qué condiciones obligan a escalar?
4. Diferencia urgencia y gravedad.
5. ¿Qué problemas causa escalar demasiado o demasiado poco?

---

# OPS-301-U06 — Guardia de puente supervisada

## 1. Integración

**La guardia combina rutina, órdenes, contactos, coordinación, incidente y relevo.**

## 2. Rutina

El cadete debe mantener atención, registro, tareas periódicas y comunicación proporcional.

## 3. Evento

El instructor puede introducir un contacto nuevo, degradación, cambio de misión, petición externa o restricción.

No existe un único “camino correcto” si varias respuestas son profesionalmente defendibles.

## 4. Coordinación

Se evalúa si el cadete informa a quien corresponde, pide ayuda cuando toca, no invade otras funciones y conserva contexto.

## 5. Relevo

La guardia termina con un handoff que debe incluir estado, pendientes, órdenes, incidencias y restricciones.

## 6. Evidencia

La evaluación no se reduce a “ganó/perdió”. Se observa precisión, juicio, comunicación, disciplina, teamwork y ejecución.

### Práctica

Turno corto en simulador con rutina, un evento inesperado y relevo final.

### Autoevaluación

1. ¿Qué elementos integra una guardia supervisada?
2. ¿Por qué no siempre existe una única respuesta correcta?
3. ¿Qué conductas muestran buena coordinación?
4. ¿Qué debe incluir el relevo?
5. ¿Qué ejes se evalúan además del resultado final?

---

# Evaluación del curso

OPS-301 evalúa la capacidad de participar en el flujo de un puente, no de mandar la nave.

# Referencias internas

- `gameplay/ship_operations/bridge_station_model.json`
- `gameplay/ship_operations/operational_event_log/README.md`
- `gameplay/orders/starfleet_mission_tasking_order.json`
- `gameplay/careers/academy_path/course_resolution.md`
