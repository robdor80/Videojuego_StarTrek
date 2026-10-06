# ENG-301 — Ingeniería y gestión de energía I

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 3.ª clase · Trimestre 1**

## Finalidad

Comprender y operar de forma supervisada los fundamentos de energía, dependencias y diagnóstico básico de una nave. ENG-301 no forma todavía a un ingeniero de guardia completo; enseña a leer capacidad, distribuir recursos dentro de autoridad, reconocer efectos en otros sistemas y comunicar límites técnicos al puente.

La regla central es:

> **Ingeniería no “crea” capacidad por orden verbal: trabaja con recursos, estado, tiempo, riesgo y límites reales de la nave.**

---

# ENG-301-U01 — Producción y reservas

## 1. Estado energético

El operador debe conocer:
- fuentes activas;
- reservas;
- consumo actual;
- margen disponible;
- sistemas prioritarios;
- degradaciones.

## 2. Producción

**Las fuentes proporcionan energía utilizable.** En este nivel no se estudia todavía diseño interno avanzado, sino:
- disponibilidad;
- estabilidad;
- capacidad;
- límites.

## 3. Reservas

Las reservas permiten absorber picos, sostener sistemas o afrontar contingencias.

No son infinitas.

Usarlas ahora puede reducir margen futuro.

## 4. Consumo

El consumo debe entenderse por sistemas:
- propulsión;
- sensores;
- escudos;
- transporte;
- soporte vital;
- laboratorios;
- servicios.

## 5. Margen

El margen es la capacidad disponible antes de comprometer:
- estabilidad;
- reserva;
- otros consumidores;
- seguridad.

### Práctica

Lee un estado energético y decide si existe margen para aumentar consumo de Sensores.

### Autoevaluación

1. ¿Qué datos forman un estado energético básico?
2. ¿Qué función cumplen reservas?
3. ¿Por qué no deben tratarse como infinitas?
4. Nombra cuatro grandes consumidores.
5. ¿Qué significa margen energético?

---

# ENG-301-U02 — Distribución de energía

## 1. Distribuir es priorizar

**La energía debe llegar a cargas concretas.**

La distribución puede:
- mantener;
- aumentar;
- reducir;
- aislar;
- redirigir.

## 2. Prioridades

Una prioridad puede venir de:
- seguridad;
- misión;
- Mando;
- emergencia;
- estado técnico.

Ingeniería no debe modificar prioridades estratégicas sin autoridad.

## 3. Rutas

La energía puede viajar por distintas rutas o buses funcionales según el modelo de nave.

Una ruta dañada puede obligar a:
- aislar;
- reroute;
- usar alternativa;
- degradar capacidad.

## 4. Aislamiento

Aislar protege al resto de la nave cuando una rama:
- falla;
- consume de forma anómala;
- crea riesgo;
- necesita mantenimiento.

## 5. Coste de reasignar

Aumentar un sistema puede reducir otro.

Ejemplo:
> más potencia a Sensores puede exigir reducir un consumidor menos prioritario o pedir autorización.

### Práctica

Asigna energía en un escenario con tres demandas incompatibles.

### Autoevaluación

1. ¿Qué significa distribuir energía?
2. ¿De dónde puede venir una prioridad?
3. ¿Qué ocurre si una ruta está dañada?
4. ¿Para qué sirve aislar?
5. ¿Por qué aumentar un sistema puede afectar a otro?

---

# ENG-301-U03 — Propulsión y energía

## 1. Una orden de vuelo tiene coste técnico

**Impulso y warp necesitan capacidad técnica disponible.**

Ingeniería debe poder responder:
- si es posible;
- durante cuánto tiempo;
- con qué riesgo;
- con qué efecto sobre otros sistemas.

## 2. Demanda de impulso

Una maniobra subluz puede exigir:
- energía;
- capacidad de propulsión;
- control;
- margen térmico o estructural según el modelo.

## 3. Demanda warp

Warp puede depender de:
- capacidad del sistema;
- factor solicitado;
- límite sostenible;
- daños;
- potencia;
- condiciones.

## 4. Máximo y sostenible

Una velocidad máxima puede ser posible durante poco tiempo y no ser sostenible.

Ingeniería debe diferenciar:
- disponible;
- sostenible;
- emergencia;
- imposible.

## 5. Informar al puente

Un informe útil no dice simplemente “no”.

Ejemplo:
> “Warp 8 disponible durante 12 minutos con margen reducido; warp 7 sostenible.”

### Práctica

Relaciona tres órdenes de vuelo con capacidad técnica y prepara una respuesta al puente.

### Autoevaluación

1. ¿Qué debe poder responder Ingeniería ante una orden de vuelo?
2. ¿Por qué máximo y sostenible no son iguales?
3. ¿Qué factores limitan warp?
4. ¿Qué significa capacidad de emergencia?
5. ¿Cómo debe formularse una limitación al puente?

---

# ENG-301-U04 — Dependencias de sistemas

## 1. Pensar en cadenas

Un sistema puede depender de:
- energía;
- datos;
- refrigeración;
- control;
- hardware;
- autorización.

## 2. Sensores

Sensores depende de:
- matrices;
- potencia;
- integridad;
- procesamiento;
- entorno.

**Si Sensores pide más potencia, Ingeniería y Ops deben distinguir necesidad técnica y prioridad operacional.**

## 3. Escudos

Escudos consumen recursos y pueden competir con otros sistemas en emergencia.

Su disponibilidad no significa uso autorizado.

## 4. Transportadores

Su función depende de:
- energía;
- sistema disponible;
- condiciones;
- objetivo válido;
- autorización.

## 5. Soporte vital

Soporte vital tiene prioridad alta porque sostiene habitabilidad.

Una avería en energía puede convertirse en riesgo de tripulación.

## 6. Efecto cascada

Ejemplo:
> fallo de distribución → sensores degradados → navegación con menos información → mayor incertidumbre de ruta.

### Práctica

Traza dependencias de cuatro sistemas y predice qué ocurre tras perder una rama de distribución.

### Autoevaluación

1. ¿Qué tipos de dependencia puede tener un sistema?
2. ¿De qué depende Sensores?
3. ¿Por qué soporte vital suele tener alta prioridad?
4. ¿Qué limita un transportador?
5. Explica un efecto cascada.

---

# ENG-301-U05 — Mantenimiento y diagnóstico básico

## 1. Síntoma no es causa

**Un síntoma describe lo observado.**

Ejemplo:
> “Matriz de sensores pierde resolución.”

La causa puede ser:
- daño;
- potencia insuficiente;
- calibración;
- interferencia;
- procesamiento;
- conexión.

## 2. Diagnóstico

Un flujo básico:
1. confirmar síntoma;
2. consultar estado;
3. ejecutar prueba;
4. comparar;
5. aislar causa probable;
6. decidir acción o escalado.

## 3. Acciones de Ingeniería

El modelo contempla:
- diagnosticar;
- redirigir energía;
- aislar sistema;
- reiniciar;
- asignar reparación;
- parche temporal;
- sustituir componente;
- modificar configuración;
- ejecutar prueba.

## 4. Límites

Un cadete solo ejecuta tareas dentro de:
- entrenamiento;
- autorización;
- supervisión.

## 5. Escalado

Debe escalarse cuando:
- riesgo supera competencia;
- causa no está clara;
- reparación afecta sistemas críticos;
- se requieren recursos mayores.

### Práctica

Diagnostica un fallo preparado con dos causas plausibles.

### Autoevaluación

1. Diferencia síntoma y causa.
2. ¿Qué pasos sigue un diagnóstico básico?
3. Nombra cuatro acciones de Ingeniería.
4. ¿Qué limita a un cadete?
5. ¿Cuándo debe escalar?

---

# ENG-301-U06 — Informe de Ingeniería

## 1. Informar capacidad, no impresiones

El puente necesita saber:
- estado;
- capacidad;
- riesgo;
- tiempo estimado;
- restricciones.

## 2. Estado

Debe describirse de forma operacional:
- normal;
- degradado;
- limitado;
- crítico;
- fuera de servicio.

## 3. Capacidad

Ejemplo:
> “Impulso disponible al 60% funcional; maniobras de alta aceleración no recomendadas.”

No basta decir:
> “Está mal.”

## 4. Riesgo

El informe debe indicar si una opción:
- es segura;
- aumenta desgaste;
- puede fallar;
- pone en riesgo otro sistema.

## 5. ETA técnica

Cuando sea razonable, Ingeniería puede estimar:
- tiempo de diagnóstico;
- tiempo de reparación;
- tiempo para recuperar capacidad.

**Debe incluir incertidumbre si existe.**

## 6. Recomendación

Puede cerrar con una recomendación:
> “Mantener warp 6 hasta completar reparación.”

La decisión final puede corresponder a Mando.

### Práctica

Emite tres informes al puente: degradación leve, fallo crítico y reparación en curso.

### Autoevaluación

1. ¿Qué necesita saber el puente?
2. ¿Por qué “está mal” no es un informe útil?
3. ¿Qué significa informar capacidad?
4. ¿Qué debe acompañar una ETA técnica incierta?
5. ¿Quién toma la decisión operativa final cuando excede Ingeniería?

---

# Evaluación del curso

ENG-301 evalúa lectura energética, distribución básica, relación con propulsión, dependencias, diagnóstico y comunicación técnica.

# Referencias internas

- `gameplay/engineering/engineering_loop.json`
- `gameplay/ship_operations/interconsole/sensor_to_engineering_support_request.json`
- `gameplay/ship_operations/bridge_station_model.json`
