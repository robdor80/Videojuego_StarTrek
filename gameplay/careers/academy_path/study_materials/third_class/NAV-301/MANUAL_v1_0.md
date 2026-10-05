# NAV-301 — Navegación y control de vuelo I

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 3.ª clase · Trimestre 1**

## Finalidad

Pasar de comprender rutas a operar navegación y vuelo básico bajo supervisión. NAV-301 introduce la estación de vuelo, el plotting operativo, maniobras a impulso, preparación y ejecución de curso warp, aproximación y órbita, y respuesta a anomalías de navegación.

La regla central es:

> **La consola no “teletransporta” la nave: transforma una intención de mando en una solución validada de movimiento que progresa dentro del World State.**

---

# NAV-301-U01 — Estación de vuelo

## 1. Qué controla la estación

La estación de vuelo trabaja con:
- rumbo;
- velocidad;
- estado de propulsión;
- solución de navegación;
- maniobra;
- ejecución de órdenes de movimiento.

No decide por sí sola la misión.

## 2. Información mínima

Antes de ejecutar una orden, el operador necesita conocer:
- destino o intención;
- posición actual;
- capacidad de propulsión;
- restricciones;
- estado de ruta;
- autoridad de mando.

## 3. Controles funcionales

La consola deberá permitir, como mínimo:
- fijar rumbo;
- seleccionar velocidad;
- iniciar o modificar una maniobra;
- seleccionar factor warp;
- entrar y salir de warp;
- interceptar;
- entrar en órbita;
- aproximarse;
- atracar cuando proceda;
- abortar o cancelar.

La presentación visual puede variar por era.

## 4. Estado de propulsión

Una orden puede ser válida como intención pero imposible en el estado actual de la nave.

El operador debe distinguir:
- orden válida;
- orden ejecutable;
- orden pendiente de recursos;
- orden imposible.

## 5. Confirmación

El operador confirma la orden, configura lo necesario y reporta ejecución o limitación.

### Práctica

Familiarización con una consola simulada: identificar controles de rumbo, velocidad, propulsión y cancelación.

### Autoevaluación

1. ¿Qué controla la estación de vuelo?
2. ¿Qué información necesita antes de ejecutar?
3. Nombra cuatro acciones funcionales mínimas.
4. ¿Qué diferencia existe entre orden válida y ejecutable?
5. ¿Qué debe hacer el operador si la nave no puede cumplir?

---

# NAV-301-U02 — Plotting operativo

## 1. De destino a ruta

Plotting significa construir una solución de navegación entre origen y destino.

La solución considera:
- waypoints;
- peligros conocidos;
- fronteras;
- restricciones;
- preferencia de ruta;
- capacidad de la nave;
- ETA.

## 2. Waypoints

Un waypoint es un punto intermedio que ayuda a estructurar la ruta.

Puede usarse para:
- evitar una zona;
- pasar por apoyo;
- cumplir una orden;
- dividir una ruta compleja.

## 3. Preferencias

La ruta puede priorizar:
- tiempo;
- seguridad;
- evitar espacio hostil;
- evitar restricciones;
- apoyo de bases;
- bajo contacto.

La opción más corta físicamente no es automáticamente la mejor.

## 4. ETA

La ETA se presenta con la precisión que permita la información.

Si la ruta o condiciones son inciertas, debe usarse un rango.

## 5. Autoridad y legalidad

Una ruta puede ser físicamente posible pero políticamente restringida.

La consola debe advertir de restricciones conocidas sin inventar peligros ocultos.

### Práctica

Preparar un plan de vuelo entre dos sistemas con una frontera y un waypoint opcional.

### Autoevaluación

1. ¿Qué significa plotting?
2. ¿Para qué sirve un waypoint?
3. Nombra tres preferencias de ruta.
4. ¿Por qué la ruta más corta no siempre es mejor?
5. ¿Qué diferencia existe entre posibilidad física y legalidad conocida?

---

# NAV-301-U03 — Maniobra a impulso

## 1. Maniobra local

La maniobra a impulso se utiliza en movimiento subluz y control cercano.

Incluye:
- cambios de rumbo;
- cambios de velocidad;
- aproximación;
- separación;
- formación;
- evasión básica cuando proceda.

## 2. Cambio de rumbo

Un rumbo nuevo debe validarse contra:
- capacidad de maniobra;
- obstáculos;
- trayectoria de otros objetos;
- restricciones;
- estado de propulsión.

## 3. Velocidad

La velocidad no se selecciona aislada del entorno.

Más velocidad puede:
- reducir tiempo;
- disminuir margen de reacción;
- aumentar dificultad de aproximación;
- ser incompatible con seguridad.

## 4. Aproximación y separación

El operador debe mantener márgenes apropiados según:
- objetivo;
- tamaño;
- movimiento relativo;
- misión;
- instrucciones.

## 5. Cancelación

Toda maniobra debe poder cancelarse o modificarse si el estado cambia.

### Práctica

Ejecutar una secuencia de cambio de rumbo, velocidad, aproximación y separación.

### Autoevaluación

1. ¿Qué tareas pertenecen a maniobra a impulso?
2. ¿Qué valida un cambio de rumbo?
3. ¿Qué efecto puede tener aumentar velocidad?
4. ¿De qué dependen los márgenes de aproximación?
5. ¿Por qué debe existir cancelación?

---

# NAV-301-U04 — Curso warp

## 1. Preparación

Entrar en warp requiere una ruta y condiciones válidas.

Debe comprobarse:
- destino;
- ruta;
- factor solicitado;
- capacidad sostenible;
- energía;
- daño;
- restricciones;
- autorización.

## 2. Entrada

La entrada en warp inicia una travesía persistente.

No completa el viaje de inmediato.

## 3. Monitorización

Durante el trayecto se sigue:
- posición;
- progreso;
- ETA;
- estado de propulsión;
- condiciones;
- cambios de ruta;
- nuevos peligros conocidos.

## 4. Salida

Salir de warp puede ser:
- planificado;
- por llegada;
- por orden;
- por peligro;
- por fallo;
- por necesidad táctica.

## 5. Replanificación

Un cambio en daño, energía, subespacio, frontera o misión puede obligar a recalcular.

### Práctica

Preparar y ejecutar un salto supervisado con una modificación de ETA en ruta.

### Autoevaluación

1. ¿Qué se comprueba antes de entrar en warp?
2. ¿Por qué entrar en warp no completa el viaje?
3. ¿Qué se monitoriza durante tránsito?
4. Nombra tres causas de salida no planificada.
5. ¿Qué cambios pueden obligar a replanificar?

---

# NAV-301-U05 — Aproximación y órbita

## 1. Interceptación

Interceptar significa calcular una trayectoria para encontrarse con un objetivo móvil.

Se necesita:
- contacto válido;
- posición;
- vector;
- velocidad estimada;
- capacidad propia.

## 2. Aproximación

Una aproximación debe controlar:
- velocidad relativa;
- separación;
- orientación;
- tráfico;
- instrucciones del destino.

## 3. Órbita

Entrar en órbita requiere:
- cuerpo objetivo;
- solución disponible;
- capacidad de control;
- perfil apropiado.

El jugador no necesita calcular mecánica orbital real manualmente.

## 4. Acoplamiento

Atracar añade condiciones:
- instalación válida;
- puerto asignado cuando proceda;
- aproximación segura;
- autorización.

## 5. Márgenes

Un margen permite absorber:
- incertidumbre;
- movimiento;
- error;
- demora.

### Práctica

Simulación de llegada: interceptación, aproximación y entrada en órbita.

### Autoevaluación

1. ¿Qué datos requiere interceptar?
2. ¿Qué controla una aproximación?
3. ¿Qué necesita una orden de órbita?
4. ¿Qué añade el acoplamiento?
5. ¿Para qué sirven los márgenes?

---

# NAV-301-U06 — Anomalías de navegación

## 1. Desviación

Una desviación aparece cuando la nave no sigue la solución prevista o cuando la ruta deja de ser válida.

Puede deberse a:
- daño;
- error;
- nueva información;
- cambio de condiciones;
- obstáculo;
- orden modificada.

## 2. Datos incompletos

Si la información es insuficiente:
- se reduce confianza;
- se amplía margen;
- se solicita información;
- se evita fingir precisión.

## 3. Obstáculos

Un obstáculo conocido debe evaluarse según:
- distancia;
- trayectoria;
- capacidad de maniobra;
- tiempo;
- riesgo.

## 4. Abort

Abortar una maniobra es una acción profesional válida cuando continuar deja de ser seguro o autorizado.

No debe verse como “fracaso” si protege misión y tripulación.

## 5. Reporte

Ante anomalía, el operador debe comunicar:
- qué cambió;
- impacto;
- opción segura;
- ETA o ruta revisada.

### Práctica

Resolver una desviación provocada por una nueva zona de peligro.

### Autoevaluación

1. ¿Qué puede causar una desviación?
2. ¿Cómo se trabaja con datos incompletos?
3. ¿Qué factores se consideran ante un obstáculo?
4. ¿Cuándo es correcto abortar?
5. ¿Qué debe incluir el reporte de anomalía?

---

# Evaluación del curso

NAV-301 evalúa manejo básico, plotting, maniobra, control warp, aproximación y juicio ante anomalías.

# Referencias internas

- `gameplay/navigation/navigation_order_contract.json`
- `gameplay/navigation/route_cost_model.json`
- `gameplay/warp_travel/route_planning_model.json`
- `gameplay/warp_travel/eta_resolution_model.json`
