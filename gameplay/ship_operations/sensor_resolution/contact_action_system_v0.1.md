# Sensores · Contact Action System v0.1

Estado: **CANON OPERATIVO / PROTOTIPO v0.3**

## Objetivo

La estación de Sensores mantiene vigilancia pasiva continua y adquiere contactos automáticamente. La interacción principal del oficial empieza cuando selecciona un contacto y decide qué hacer con él.

La consola no ofrece una botonera fija. El **Core determina de forma determinista qué acciones tienen sentido para el contacto seleccionado** y la UX representa ese estado.

Regla:

**contacto seleccionado → estado/tipo/capacidades → Contact Action Resolver → máximo 8 controles visibles**

Gemini no decide qué botones existen ni qué acciones están permitidas.

## Ubicación UX

La zona de acciones vive inmediatamente **debajo de la solución espacial cenital/perfil** y antes de Comunicaciones.

Formato inicial v0.3:

- máximo **8 huecos**;
- rejilla **4 × 2**;
- dos filas estables;
- los controles cambian sin mover el visor principal;
- las acciones imposibles por naturaleza se ocultan;
- las acciones conceptualmente válidas pero temporalmente imposibles pueden mostrarse deshabilitadas con el motivo.

## Familias de contacto

El resolver distingue, como mínimo:

- contacto no identificado;
- nave civil/identificada;
- nave militar;
- nave hostil confirmada;
- objeto natural;
- objeto artificial / sonda / baliza;
- forma de vida;
- contacto perdido.

La afiliación o especie por sí sola **no implica hostilidad**.

## Acciones primitivas

La v0.3 reutiliza primitivas deterministas del Sensor Core. Las acciones visibles se componen con ellas:

- iniciar/detener seguimiento;
- cambiar prioridad del seguimiento;
- identificación focalizada;
- análisis focalizado;
- escaneo táctico;
- estimación de trayectoria;
- vigilancia de cambios;
- marcar/desmarcar;
- consultar últimos datos;
- readquirir;
- comparar lecturas;
- transferir a Ciencia, Táctica, Puente o Ingeniería.

No todos los contactos reciben todas las acciones.

## Control evolutivo de seguimiento

El seguimiento ocupa **un solo hueco** de la rejilla.

### Sin seguimiento

`SEGUIR`

Activa seguimiento estándar.

### Seguimiento estándar

El mismo hueco se divide mediante una diagonal:

`INTENSIFICAR / DETENER`

- **INTENSIFICAR** aumenta prioridad, coste de recursos y calidad del seguimiento.
- **DETENER** libera el seguimiento.

### Seguimiento intensificado

El hueco pasa a:

`ESTÁNDAR / DETENER`

- **ESTÁNDAR** reduce nuevamente el seguimiento a prioridad normal.
- **DETENER** finaliza el seguimiento.

Si el estado cambia por voz, texto o por otra parte del sistema, el control debe reflejar inmediatamente el estado real del Core.

## Reglas contextuales iniciales

### No identificado

Prioriza:

1. seguimiento;
2. identificar;
3. analizar;
4. trayectoria;
5. vigilancia;
6. marcar;
7. Ciencia;
8. Puente.

### Militar / hostil

Prioriza:

1. seguimiento;
2. escaneo táctico;
3. análisis;
4. trayectoria;
5. vigilancia;
6. comparación si existe historial suficiente;
7. Táctica;
8. Puente.

No se declara hostilidad por ser una nave militar.

### Objeto natural

No ofrece acciones absurdas como armamento o escudos. Prioriza análisis, trayectoria, vigilancia y Ciencia.

### Contacto perdido

No ofrece operaciones en tiempo real. Puede ofrecer:

- últimos datos;
- detener seguimiento residual;
- readquisición solo cuando exista señal físicamente recuperable;
- transferencia del registro a Puente/Ciencia.

## Estado y autoridad

Los botones son una representación del estado, no su propietario.

Ejemplo:

- `tracked=false` → `SEGUIR`;
- `tracked=true && trackingPriority=normal` → `INTENSIFICAR / DETENER`;
- `tracked=true && trackingPriority=priority` → `ESTÁNDAR / DETENER`.

La acción se ejecuta primero en el Core. Después la UX se vuelve a resolver desde el nuevo estado.

## Principio de diseño

**La Computadora reduce opciones irrelevantes; el oficial conserva la decisión operativa.**

La inteligencia de la interfaz consiste en presentar solo las acciones coherentes con el contacto y el estado actual, sin inventar datos ni decisiones.
