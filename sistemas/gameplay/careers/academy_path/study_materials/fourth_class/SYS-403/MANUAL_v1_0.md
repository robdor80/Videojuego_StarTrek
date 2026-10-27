# SYS-403 — Sistemas fundamentales de una nave estelar

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 4.ª clase · Trimestre 3**

## Finalidad

Comprender la función general y las dependencias de los principales sistemas de una nave estelar sin convertir al cadete en ingeniero.

SYS-403 enseña a pensar en una nave como una **red de sistemas interdependientes**. El objetivo es reconocer qué sistema permite una función, qué necesita para operar y qué consecuencias puede producir su degradación.

---

# SYS-403-U01 — Arquitectura de sistemas y energía

## 1. Una nave es una red

**Los sistemas de una nave no funcionan de forma aislada.**

Propulsión, sensores, soporte vital, comunicaciones, defensas, transporte y servicios comparten recursos y dependen unos de otros.

## 2. Fuentes

Una fuente proporciona energía utilizable por la nave.

En este nivel no se exige ingeniería interna detallada. Se aprende que la disponibilidad energética condiciona qué sistemas pueden funcionar y con qué prioridad.

## 3. Distribución

La energía debe llegar desde una fuente hasta los consumidores.

Una distribución puede:

- priorizar;
- limitar;
- aislar;
- redirigir;
- degradarse.

## 4. Cargas

Una carga es un sistema o función que consume recursos energéticos.

Ejemplos conceptuales:

- sensores;
- propulsión;
- escudos;
- servicios;
- laboratorios;
- transportadores.

## 5. Dependencias

Un sistema puede depender de varios recursos.

Por ejemplo, una consola puede estar intacta físicamente pero no funcionar si:

- no recibe energía;
- su red de datos está caída;
- el sistema remoto que controla está dañado;
- la autorización necesaria no está disponible.

## 6. Prioridad

No siempre puede mantenerse todo al máximo.

En una emergencia, la nave puede priorizar:

- vida;
- control;
- propulsión;
- comunicaciones;
- defensa;
- recuperación.

La prioridad concreta depende del contexto y de la autoridad competente.

### Práctica

Sigue un diagrama funcional sencillo desde fuente de energía hasta tres consumidores y predice qué ocurre si se pierde una rama.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SYS-403-U02 — Propulsión de impulso

## 1. Función general

**La propulsión de impulso permite el movimiento normal de la nave en régimen subluz.**

A nivel de 4.ª clase, el cadete debe entender:

- cuándo se utiliza;
- qué función cumple;
- qué limitaciones generales puede tener;
- cómo se relaciona con Navegación y Mando.

## 2. Subluz

“Subluz” significa operar por debajo de la velocidad de la luz dentro del modelo del juego.

Las maniobras locales, aproximaciones y gran parte del control cercano se resuelven en este régimen.

## 3. Estado de propulsión

Un operador puede recibir estados como:

- disponible;
- degradado;
- limitado;
- no disponible.

La velocidad solicitada debe respetar la capacidad real de la nave en ese momento.

## 4. Navegación y control

Propulsión no decide el destino.

Navegación/Conn interpreta órdenes de movimiento y utiliza la capacidad disponible para ejecutar una solución válida.

## 5. Limitaciones generales

La operación puede verse afectada por:

- daño;
- energía;
- maniobra;
- seguridad;
- condiciones locales;
- restricciones de misión.

### Práctica

Interpreta un estado básico de propulsión y decide qué órdenes simples siguen siendo ejecutables.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SYS-403-U03 — Propulsión warp

## 1. Función general

**La propulsión warp permite el viaje superlumínico dentro del universo de Star Trek.**

En este nivel se estudia como **capacidad de navegación interestelar**, no como ingeniería de campo avanzada.

## 2. Campo warp

El sistema warp genera las condiciones necesarias para que la nave viaje a velocidades efectivas superiores a la luz según la tecnología del universo.

El cadete no necesita todavía calcular la física interna del campo.

## 3. Factor de curvatura

El factor warp expresa una selección de régimen de velocidad.

Pero el proyecto establece una regla importante:

> **No existe una conversión única, universal e inmutable de factor warp a velocidad para todas las eras, naves y condiciones.**

La capacidad real depende de:

- clase;
- configuración;
- estado;
- potencia;
- límites sostenibles;
- condiciones locales.

## 4. Máximo no significa sostenible

Una nave puede tener una capacidad máxima superior a la que puede mantener durante largo tiempo.

Por eso Navegación trabaja con:

- velocidad solicitada;
- capacidad disponible;
- límite sostenible;
- ETA resultante.

## 5. Riesgos generales

Una transición o viaje warp puede verse condicionado por:

- daño;
- energía;
- navegación;
- condiciones subespaciales;
- peligros;
- restricciones de ruta.

### Práctica

Compara dos rutas donde una es más corta pero exige una velocidad menos sostenible y otra es más larga pero más segura.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SYS-403-U04 — Habitabilidad y servicios

## 1. Mantener una tripulación viva

**Una nave necesita sistemas que no “mueven” la misión pero hacen posible que exista.**

## 2. Soporte vital

El soporte vital mantiene condiciones habitables.

A nivel introductorio incluye la idea de controlar:

- atmósfera;
- temperatura;
- condiciones ambientales básicas.

Un fallo de soporte vital puede convertir un problema técnico en una emergencia para la tripulación.

## 3. Síntesis de alimentos y replicación

El proyecto distingue por era:

### Siglo XXIII

Puede utilizarse síntesis de alimentos y tecnologías de producción a bordo.

No se trata automáticamente todo sistema de comida como un replicador molecular del siglo XXIV.

### Siglo XXIV

Los replicadores son tecnología madura para:

- alimentos;
- muchos objetos;
- reciclaje de materia según capacidad y contexto.

Su uso depende de:

- energía;
- patrones autorizados;
- reservas;
- restricciones.

## 4. Transportadores

El transportador es un sistema de movimiento de personas o materia.

En 4.ª clase se estudia su **función y dependencia**, no operación avanzada ni mantenimiento.

Su disponibilidad puede depender de:

- estado;
- energía;
- condiciones;
- autorización;
- objetivo válido.

## 5. Computer service

La computadora de la nave conecta información y acciones autorizadas entre múltiples interfaces.

No es un sistema omnipotente.

### Práctica

Relaciona cada necesidad con el sistema que principalmente la soporta: alimento, traslado, consulta de datos, habitabilidad o acceso a servicios.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SYS-403-U05 — Defensa y entorno de misión

## 1. Sistemas defensivos

La defensa de una nave puede incluir sistemas como:

- escudos;
- armamento;
- sensores;
- maniobra;
- comunicaciones;
- control de daños.

**En 4.ª clase se estudian funciones y dependencias, no doctrina táctica avanzada.**

## 2. Escudos

Los escudos protegen la nave frente a amenazas o fenómenos compatibles con sus capacidades.

Su disponibilidad depende del estado real de la nave y de recursos.

## 3. Armamento

El armamento permite aplicar fuerza cuando existe autoridad y contexto para ello.

Tener un sistema disponible no equivale a tener permiso para usarlo.

## 4. Sensores como proveedor y consumidor

Sensores:

- consume energía y capacidad;
- produce conocimiento;
- alimenta Navegación, Ciencia, Táctica, Mando y otros sistemas.

Una defensa sin información puede tomar decisiones peores.

## 5. Holodeck cuando proceda

El holodeck es una capacidad propia de determinadas eras y naves.

No debe retrotraerse automáticamente a Pike o Kirk.

Puede utilizarse para:

- entrenamiento;
- simulación;
- recreo

cuando la nave y era lo permitan.

### Práctica

Analiza una situación donde aumentar recursos a sensores mejora conocimiento pero reduce recursos disponibles para otra función.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

# SYS-403-U06 — Fallos y dependencias

## 1. Degradación

Un sistema degradado puede seguir funcionando con:

- menos capacidad;
- menor precisión;
- menor velocidad;
- restricciones;
- riesgo adicional.

**“Funciona” y “funciona al cien por cien” no son lo mismo.**

## 2. Primario y secundario

Una función puede disponer de:

- sistema primario;
- respaldo;
- alternativa parcial.

El respaldo no siempre ofrece la misma capacidad.

## 3. Efecto cascada

Un fallo puede afectar a sistemas dependientes.

Ejemplo conceptual:

> pérdida de energía → menos sensores → menor conocimiento → navegación más incierta.

El problema inicial puede producir consecuencias operativas indirectas.

## 4. Prioridad

En una avería, la tripulación decide qué restaurar primero según:

- vidas;
- misión;
- peligro;
- capacidad restante;
- tiempo;
- recursos.

## 5. Diagnóstico frente a suposición

No debe asumirse la causa solo por el síntoma.

Una misma pérdida de función puede tener causas distintas.

Ingeniería diagnostica; otras estaciones informan de los efectos que observan.

### Práctica

Sigue una avería sencilla desde el sistema afectado hasta dos consecuencias secundarias y propone qué información debe enviarse a Ingeniería.

### Repaso interactivo

Las preguntas de esta unidad se generan desde conceptos evaluables del curso. El repaso teórico utiliza test de cuatro opciones y respuestas cortas autocorregibles; las competencias complejas se valoran en prácticas y simulaciones.

