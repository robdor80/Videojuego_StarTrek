# SCI-403 — Ciencia, sensores y método científico I

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 4.ª clase · Trimestre 3**

## Finalidad

Aprender a observar sin confundir observación con explicación.

SCI-403 introduce el método científico, la incertidumbre y el funcionamiento conceptual de los sensores. También sirve como primera preparación directa para la consola de Sensores del juego.

La regla central es:

> **El mundo existe primero. Sensores obtiene información. Ciencia interpreta.**

El sistema nunca crea una anomalía porque el jugador la busque, ni revela automáticamente la verdad oculta porque el jugador pulse “scan”.

---

# SCI-403-U01 — Método científico

## 1. Observar antes de explicar

**Una observación describe algo detectado o medido.**

Ejemplo:

> “La intensidad de radiación aumenta al acercarnos al objeto.”

Eso no explica todavía la causa.

## 2. Pregunta

Una pregunta convierte la observación en un problema investigable.

Ejemplo:

> “¿Qué está produciendo el aumento de radiación?”

## 3. Hipótesis

Una hipótesis es una explicación provisional que debe poder contrastarse.

Una buena hipótesis ayuda a decidir:

- qué buscar;
- qué medir;
- qué resultado la apoyaría;
- qué resultado la debilitaría.

## 4. Evidencia

La evidencia puede:

- apoyar;
- debilitar;
- contradecir;
- dejar abierta una hipótesis.

Una sola lectura rara vez convierte una explicación compleja en certeza.

## 5. Revisión

Si la evidencia cambia, la explicación debe cambiar.

El objetivo no es “tener razón a la primera”, sino construir una conclusión que siga siendo compatible con los datos.

### Ejemplo

Observación:
> Un contacto emite una firma energética intermitente.

Hipótesis A:
> Es un fallo técnico.

Hipótesis B:
> Es una señal deliberada.

La siguiente observación debe buscar información que ayude a distinguirlas.

### Práctica

Recibe una observación sencilla, formula dos hipótesis y propone una medición que permita diferenciarlas.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SCI-403-U02 — Medición e incertidumbre

## 1. Medir no significa conocer con exactitud perfecta

**Toda medición tiene límites.**

El cadete debe aprender a leer:

- valor;
- calidad;
- confianza;
- incertidumbre;
- condiciones de observación.

## 2. Precisión

La precisión describe cuánto detalle o estabilidad posee una medición.

Más precisión puede exigir:

- más tiempo;
- más potencia;
- mejor resolución;
- menos interferencia.

## 3. Ruido

Ruido es información no deseada que dificulta distinguir la señal útil.

Puede provenir de:

- entorno;
- otras emisiones;
- daño;
- condiciones de observación;
- interferencia deliberada.

## 4. Error

“Error” no significa necesariamente equivocación humana.

Puede describir el margen de incertidumbre asociado a una medición.

Ejemplo:

> distancia estimada: 12.000 km ± margen de lectura.

## 5. Límite de detección

Una señal puede existir y ser demasiado débil para ser detectada con la configuración disponible.

Por eso:

> **no detectado ≠ inexistente**

## 6. Calidad de lectura

El proyecto admite estados de conocimiento como:

- confirmado;
- alta confianza;
- estimado;
- hipótesis;
- desconocido;
- contradictorio.

La interfaz debe comunicar estos niveles en lugar de convertir todo en “verdadero/falso”.

### Práctica

Compara tres lecturas del mismo fenómeno con distinta interferencia y decide cuál permite una conclusión más fuerte.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SCI-403-U03 — Qué es un sensor

## 1. Función general

**Un sensor detecta y mide propiedades observables.**

Puede ayudar a determinar:

- que existe una señal;
- de dónde procede;
- cómo cambia;
- qué firmas presenta;
- con qué confianza se ha medido.

## 2. Detección

El motor de sensores puede producir estados como:

1. no detectado;
2. traza detectada;
3. detectado sin clasificar;
4. parcialmente resuelto;
5. resuelto.

Cada nivel depende de observaciones reales y capacidad disponible.

## 3. Firma

Una firma es un patrón observable asociado a una fuente o fenómeno.

La consola puede trabajar con categorías como:

- electromagnética;
- subespacial;
- gravimétrica;
- térmica;
- radiación;
- partículas;
- biológica;
- warp;
- transpondedor artificial.

## 4. Medición y clasificación

Detectar una firma no equivale automáticamente a identificar el objeto.

Ejemplo:

> “Firma warp compatible con una nave”

no significa:

> “Es definitivamente una nave concreta.”

## 5. Canales y filtros

El operador puede elegir qué firmas buscar o priorizar.

Un filtro más específico puede ayudar a aislar información, pero también puede ignorar señales fuera del criterio seleccionado.

### Práctica

Relaciona cinco fenómenos de entrenamiento con el tipo de firma que podría proporcionar información útil.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SCI-403-U04 — Activo y pasivo

## 1. Dos formas generales de observar

### Pasivo

**El sistema observa señales disponibles sin emitir una búsqueda equivalente dirigida al entorno.**

Ventajas posibles:

- menor exposición;
- menor interferencia provocada;
- discreción.

Limitaciones posibles:

- menos información;
- dependencia de emisiones existentes;
- menor capacidad de detección en ciertas condiciones.

### Activo

El sistema utiliza una emisión o interacción deliberada para mejorar capacidad de observación.

Ventajas posibles:

- detección mejorada;
- mejor resolución en determinadas condiciones.

Costes posibles:

- consumo;
- tiempo;
- mayor detectabilidad de la propia actividad.

## 2. No existe un modo universalmente mejor

La elección depende de:

- misión;
- riesgo;
- distancia;
- interferencia;
- discreción;
- necesidad de detalle.

## 3. Activo tiene consecuencias

El proyecto fija una regla:

> un barrido activo puede hacer perceptible que estamos escaneando.

No significa que siempre seamos detectados, pero el coste debe existir en el modelo.

## 4. Malas decisiones válidas

Si el operador elige un modo técnicamente válido pero inapropiado, el sistema puede ejecutarlo.

Eso es un error profesional, no un error de interfaz.

### Práctica

Elige activo o pasivo en cuatro escenarios: exploración tranquila, búsqueda de señal débil, vigilancia discreta y emergencia.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SCI-403-U05 — Contacto, lectura e interpretación

## 1. Contacto

**Un contacto es una representación persistente de algo que la nave ha detectado.**

No es una copia de la entidad oculta del World State.

Por eso utiliza una identidad observacional propia.

## 2. Ficha de contacto

Puede incluir, cuando haya sido realmente descubierto:

- posición estimada;
- distancia;
- vector;
- velocidad estimada;
- firmas;
- confianza;
- clasificación;
- historial de observaciones.

## 3. Tracking inicial

Seguir un contacto significa actualizar su conocimiento a lo largo del tiempo.

Puede mejorar:

- posición;
- rumbo estimado;
- velocidad;
- trayectoria probable.

No revela mágicamente su naturaleza.

## 4. Readout

La lectura sensorial presenta datos medidos o estimados.

Debe conservar:

- procedencia;
- momento;
- confianza;
- incertidumbre.

## 5. Ciencia interpreta

Sensores puede decir:

> “Masa aproximada, firma térmica, emisión subespacial y vector.”

Ciencia puede recibir esos datos y plantear:

> “El patrón es compatible con un fenómeno de tipo X.”

La interpretación no borra ni modifica la lectura original.

## 6. Conocimiento compartido sin omnisciencia

Varias estaciones pueden trabajar sobre el mismo contacto:

- Sensores: posición y firmas;
- Ciencia: interpretación;
- Táctica: postura y capacidad de combate;
- Comunicaciones: señales y autenticación;
- Ordenador: comparación con registros.

Cada dato conserva su fuente.

### Práctica

Recibe una ficha de contacto y separa:
- datos observados;
- estimaciones;
- clasificación;
- hipótesis científica.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SCI-403-U06 — Barrido básico

## 1. El primer procedimiento real de consola

**Esta unidad conecta directamente con la consola funcional de Sensores.**

Un barrido básico sigue la lógica:

> **tipo → modo → área/objetivo → resolución → filtros → prioridad → duración → revisar → ejecutar**

Los valores por defecto permiten cambiar solo lo necesario.

## 2. Tipo

La consola contempla:

- corto alcance;
- largo alcance;
- focalizado.

Un barrido focalizado necesita un objetivo concreto.

## 3. Área u objetivo

Puede ser:

- espacio circundante;
- sector;
- sistema;
- coordenadas;
- vector;
- contacto conocido.

## 4. Resolución

Puede elegirse un nivel de detalle.

Más resolución puede implicar:

- más tiempo;
- más potencia;
- menor cobertura.

## 5. Filtros y prioridad

**Filtro**  
Define qué firmas interesan.

**Prioridad**  
Indica qué firma recibe atención preferente sin excluir necesariamente las demás.

No son el mismo concepto.

## 6. Duración

La duración importa.

Un barrido puede ser:

- rápido;
- estándar;
- extendido;
- personalizado.

Más tiempo puede mejorar la calidad potencial si las condiciones lo permiten.

## 7. Resultados inciertos

Son resultados válidos:

- traza;
- posible contacto;
- señal intermitente;
- lectura insuficiente;
- detectado sin clasificar.

El sistema no tiene obligación de entregar una respuesta completa.

## 8. Repetir lo mismo

Repetir exactamente la misma operación bajo las mismas condiciones no debe revelar mágicamente más.

Para mejorar puede ser necesario cambiar:

- resolución;
- duración;
- filtros;
- potencia;
- posición;
- condiciones.

## 9. Error humano

Si la orden era:

> “sector 041”

y el cadete configura:

> “sector 014”

la consola puede ejecutar el barrido si es técnicamente válido.

El error pertenece al operador.

### Práctica

Ejecuta un barrido guiado en la consola real cuando esté disponible, revisando configuración antes de confirmar.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

