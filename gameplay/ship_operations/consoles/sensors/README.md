# Consola funcional — Sensores

Estado: **DRAFT v0.1 / IN_PROGRESS**

La consola de Sensores permite **detectar, buscar, localizar, medir, seguir y volver a observar** elementos del universo materializado.

No interpreta en profundidad la naturaleza científica de un fenómeno: esa responsabilidad corresponde a Ciencia. Sensores obtiene y organiza observaciones; Ciencia las interpreta.

## Principio de diseño

Una orden verbal debe poder traducirse a una secuencia navegable de menús.

Ejemplo:

> «Alférez, barrido de largo alcance del sector 041. Prioridad a emisiones subespaciales.»

Ruta funcional:

```text
SENSORES
└── BARRIDOS
    └── LARGO ALCANCE
        ├── ÁREA
        │   └── SECTOR
        │       └── 041
        ├── PRIORIDAD
        │   └── SUBESPACIO
        └── EJECUTAR
```

La consola construye una operación estructurada y la entrega al motor de resolución de sensores. El mundo ya existe antes del escaneo.

## Árbol funcional maestro v0.1

```text
SENSORES
│
├── 01. ESTADO DE SENSORES
│   ├── Estado general
│   ├── Matrices disponibles
│   ├── Alcance efectivo
│   ├── Resolución disponible
│   ├── Potencia asignada
│   ├── Integridad / daños
│   ├── Interferencias detectadas
│   └── Operación en curso
│
├── 02. BARRIDOS
│   │
│   ├── Corto alcance
│   ├── Largo alcance
│   ├── Focalizado
│   │
│   └── CONFIGURAR BARRIDO
│       ├── Modo
│       │   ├── Pasivo
│       │   └── Activo
│       │
│       ├── Área / objetivo
│       │   ├── Espacio circundante
│       │   ├── Sector
│       │   ├── Sistema estelar
│       │   ├── Coordenadas
│       │   ├── Vector
│       │   └── Contacto conocido
│       │
│       ├── Resolución
│       │   ├── General
│       │   ├── Estándar
│       │   └── Alta
│       │
│       ├── Filtros
│       │   ├── Todas las firmas
│       │   ├── Electromagnética
│       │   ├── Subespacial
│       │   ├── Gravimétrica
│       │   ├── Térmica
│       │   ├── Radiación ionizante
│       │   ├── Partículas
│       │   ├── Biológica
│       │   ├── Firma warp
│       │   └── Transpondedor artificial
│       │
│       ├── Prioridad
│       │   ├── Ninguna
│       │   └── [una firma seleccionada]
│       │
│       ├── Duración
│       │   ├── Rápida
│       │   ├── Estándar
│       │   ├── Extendida
│       │   └── Personalizada
│       │
│       ├── Revisar configuración
│       ├── EJECUTAR
│       └── CANCELAR
│
├── 03. BÚSQUEDA / LOCALIZACIÓN
│   ├── Nave
│   ├── Lanzadera
│   ├── Sonda / baliza
│   ├── Forma de vida
│   ├── Objeto artificial
│   ├── Fuente de energía
│   ├── Firma warp
│   ├── Emisión subespacial
│   ├── Señal / transpondedor
│   ├── Radiación / partículas
│   └── Firma definida
│       ├── Área de búsqueda
│       ├── Sensibilidad
│       ├── Resolución
│       ├── Criterios
│       └── INICIAR BÚSQUEDA
│
├── 04. CONTACTOS
│   ├── Todos
│   ├── No identificados
│   ├── Identificados
│   ├── Marcados
│   ├── Perdidos recientemente
│   └── [CONTACTO]
│       ├── Posición estimada
│       ├── Distancia
│       ├── Vector
│       ├── Velocidad estimada
│       ├── Firmas detectadas
│       ├── Confianza de lectura
│       ├── Clasificación disponible
│       └── Acciones
│           ├── Barrido focalizado
│           ├── Aumentar resolución
│           ├── Iniciar seguimiento
│           ├── Marcar contacto
│           ├── Comparar lecturas
│           └── Enviar datos a...
│
├── 05. SEGUIMIENTO
│   ├── Contactos seguidos
│   ├── Fijar contacto
│   ├── Seguimiento múltiple
│   ├── Seguir firma concreta
│   ├── Actualizar posición
│   ├── Estimar rumbo
│   ├── Estimar velocidad
│   ├── Predecir trayectoria
│   └── Recuperar contacto perdido
│
├── 06. LECTURA SENSORIAL
│   ├── Intensidad de señal
│   ├── Tipo de firma
│   ├── Banda / frecuencia
│   ├── Firma energética
│   ├── Firma subespacial
│   ├── Masa aproximada
│   ├── Dimensiones aproximadas
│   ├── Vector / velocidad
│   ├── Formas de vida detectables
│   └── Coincidencia con patrones conocidos
│
├── 07. INTERFERENCIAS / COMPENSACIÓN
│   ├── Estado de interferencias
│   ├── Tipo de interferencia
│   ├── Compensación automática
│   ├── Ajuste manual
│   ├── Cambiar banda / frecuencia
│   ├── Aumentar potencia
│   ├── Reducir resolución
│   ├── Prolongar integración
│   └── Intentar recuperar señal
│
├── 08. CONFIGURACIÓN
│   ├── Sensibilidad
│   ├── Resolución predeterminada
│   ├── Potencia de sensores
│   ├── Matriz / conjunto sensor
│   ├── Frecuencia / banda
│   ├── Frecuencia de actualización
│   ├── Filtros predeterminados
│   ├── Prioridades predeterminadas
│   └── Perfiles / preajustes
│
├── 09. RESULTADOS
│   ├── Operación actual
│   ├── Último barrido
│   ├── Resultados recientes
│   ├── Lecturas guardadas
│   ├── Comparar lecturas
│   ├── Repetir operación
│   └── Enviar datos a...
│       ├── Ciencia
│       ├── Táctica
│       ├── Operaciones
│       ├── CONN / Navegación
│       ├── Mando
│       └── Ordenador / Base de datos
│
└── 10. DIAGNÓSTICO
    ├── Autodiagnóstico de sensores
    ├── Estado por matriz
    ├── Calibración
    ├── Rendimiento
    ├── Errores / degradación
    └── Solicitar soporte de Ingeniería
```

## Separación con otras consolas

**Sensores sí hace:** detectar, localizar, medir, seguir, filtrar, mejorar una lectura y entregar datos.

**Sensores no hace:**

- explicar científicamente una anomalía compleja → **Ciencia**;
- disparar o fijar armas → **Táctica**;
- trazar el rumbo de la nave → **CONN / Navegación**;
- reparar físicamente una matriz dañada → **Ingeniería**;
- decidir prioridades generales de recursos de toda la nave → **OPS**.

## Estado de backend

El núcleo de `BARRIDOS` ya puede mapearse al contrato de `sensor_scan_request` y al motor de resolución v0.1.

Las ramas de seguimiento persistente, compensación avanzada, comparación histórica y diagnóstico requerirán extensiones de backend posteriores. Se definen ahora para que la arquitectura de consola no nazca limitada a la v0.0.1.

## Regla UX

Academia y naves operativas deberán exponer este mismo árbol conceptual, pero pueden:

- reorganizar visualmente los controles;
- ocultar funciones no disponibles en esa nave/era;
- añadir accesos rápidos;
- usar etiquetas o agrupaciones diferentes.

La operación subyacente no cambia.


## BARRIDOS v0.1 — decisiones aprobadas

Estas reglas quedan **FIJADAS** para la rama de Barridos:

1. **Valores por defecto:** cada barrido parte de una configuración estándar razonable; el operador modifica solo lo necesario.
2. **Errores humanos permitidos:** una configuración equivocada pero técnicamente válida se ejecuta. Escanear el sector 014 cuando la orden era 041 es un error profesional, no un error de interfaz.
3. **Solo se bloquea lo físicamente imposible:** por ejemplo, usar una matriz destruida o una función no disponible por daños/capacidad.
4. **La duración importa:** rápido, estándar y extendido consumen tiempo de juego y afectan la calidad potencial de la lectura.
5. **El barrido focalizado exige objetivo:** contacto, coordenadas o zona concreta. No existe un focalizado genérico de todo un sector.
6. **Filtros múltiples permitidos:** pueden combinarse varias firmas; una búsqueda más específica obtiene ventaja frente a una búsqueda amplia.
7. **Prioridad y filtro son conceptos distintos:** el filtro define qué firmas se buscan; la prioridad indica a cuál prestar atención preferente sin excluir necesariamente las demás.
8. **Activo/pasivo tiene consecuencias:** el activo mejora la capacidad de detección pero puede hacer perceptible que estamos escaneando.
9. **Resultados inciertos son válidos:** traza, posible contacto, lectura insuficiente, señal intermitente y estados equivalentes forman parte normal del sistema.
10. **Repetir lo mismo no revela mágicamente más:** con la misma configuración y condiciones el resultado debe ser esencialmente equivalente. Para mejorar hay que cambiar resolución, duración, filtro, potencia, posición, condiciones o información disponible.

Estas reglas son vinculantes tanto para la futura UX de Academia como para la de naves operativas.


## BÚSQUEDA / LOCALIZACIÓN v0.1 — decisiones aprobadas

Esta rama queda **FIJADA** con el siguiente comportamiento:

- **Nave:** busca contactos compatibles con una nave por firmas, tamaño, energía, propulsión, warp o transpondedor.
- **Lanzadera:** búsqueda equivalente, optimizada para objetos más pequeños y señales más débiles.
- **Sonda / baliza:** busca dispositivos artificiales, transmisores o sondas, incluso con emisiones débiles o intermitentes.
- **Forma de vida:** prioriza firmas biológicas.
- **Objeto artificial:** busca estructuras, restos o dispositivos construidos aunque no estén identificados.
- **Fuente de energía:** localiza emisiones energéticas sin exigir conocer el objeto que las produce.
- **Firma warp:** busca actividad warp actual o residual.
- **Emisión subespacial:** busca actividad o fenómenos detectables en subespacio.
- **Señal / transpondedor:** busca una transmisión, baliza identificativa o código concreto.
- **Radiación / partículas:** busca fuentes o zonas con emisiones radiativas o de partículas.
- **Firma definida:** permite construir una búsqueda avanzada combinando criterios específicos.

### Parámetros aprobados

- **Área de búsqueda:** delimita dónde buscar.
- **Sensibilidad:** aumenta la posibilidad de detectar señales débiles, pero eleva ruido y posibles falsos positivos.
- **Resolución:** determina cuánto detalle se intenta obtener de los candidatos encontrados.
- **Criterios:** añade condiciones compatibles con el objetivo buscado.
- **Iniciar búsqueda:** ejecuta la operación con la configuración elegida.

### Reglas de comportamiento

1. Una búsqueda devuelve **candidatos compatibles**, no una identificación garantizada.
2. La consola puede mostrar **porcentaje o nivel de coincidencia** cuando haya criterios suficientes para estimarlo.
3. Es válido obtener varios candidatos, ninguno o contactos dudosos.
4. Una búsqueda mal configurada pero técnicamente válida se ejecuta igualmente.
5. La **sensibilidad alta** puede descubrir señales más débiles, pero también aumentar ruido, contactos dudosos y falsos positivos.
6. La búsqueda utiliza el mismo universo autoritativo y las mismas reglas de detección que Barridos; no genera el objetivo al buscarlo.
7. Búsqueda y Barrido son conceptos distintos:
   - **Barrido:** «quiero observar esta zona y ver qué hay».
   - **Búsqueda:** «sé más o menos qué estoy buscando; intenta encontrarlo».


## CONTACTOS v0.1 — decisiones aprobadas

Esta rama queda **FIJADA** con el siguiente comportamiento:

- **Todos:** muestra todos los contactos actualmente conocidos por la nave.
- **No identificados:** contactos detectados cuya naturaleza todavía no puede clasificarse con suficiente confianza.
- **Identificados:** contactos cuya clasificación ha alcanzado el umbral requerido.
- **Marcados:** contactos señalados manualmente o por procedimiento como relevantes.
- **Perdidos recientemente:** contactos cuya señal se ha perdido pero cuya identidad todavía puede recuperarse.

### Ficha de contacto

Al abrir un contacto se muestran únicamente los datos realmente descubiertos:

- posición estimada;
- distancia;
- vector;
- velocidad estimada;
- firmas detectadas;
- confianza de lectura;
- clasificación disponible;
- historial de observaciones;
- estado del contacto.

La clasificación puede progresar desde una simple traza hasta una identificación concreta, pero cada escalón debe estar sustentado por observaciones reales.

### Acciones aprobadas

- Barrido focalizado.
- Aumentar resolución.
- Iniciar seguimiento.
- Marcar contacto.
- Comparar lecturas.
- Enviar datos a otras consolas/sistemas autorizados.

### Identidad persistente

Un contacto conserva su identidad mientras el sistema pueda justificar razonablemente que sigue siendo el mismo objeto. Si se pierde temporalmente y se recupera con posición, trayectoria y firmas compatibles, se reutiliza el mismo `contact_id`.

### Conocimiento compartido sin omnisciencia

Las distintas consolas pueden trabajar sobre el mismo contacto persistente, pero cada una añade conocimiento según sus capacidades:

- Sensores: firmas, posición, movimiento y clasificación sensorial.
- Táctica: escudos, armamento, postura y datos de combate.
- Ciencia: interpretación física/científica.
- Comunicaciones: transpondedores, canales, señales y autenticación.
- Ordenador/Base de datos: comparación con registros conocidos.

La nave comparte una ficha común, pero cada dato conserva su procedencia y no se mezcla automáticamente como si todas las consolas hubieran sabido siempre lo mismo.

### Memoria de la nave / base de datos

Cada contacto relevante genera o actualiza una **ficha persistente en la memoria de la nave**.

La ficha conserva:

- identidad persistente del contacto;
- primera y última detección;
- historial de observaciones;
- clasificaciones anteriores;
- firmas conocidas;
- cambios de posición, vector y velocidad;
- fuentes de información;
- niveles de confianza;
- marcas/notas operativas;
- estado actual: activo, perdido, archivado o confirmado.

La ficha puede ser consultada posteriormente desde Sensores y desde Ordenador/Base de datos. Un reencuentro futuro puede compararse contra registros anteriores de la propia nave.


## SEGUIMIENTO v0.1 — decisiones aprobadas

Esta rama queda **FIJADA** con el siguiente comportamiento:

- **Contactos seguidos:** lista de contactos con actualización continua.
- **Fijar contacto:** inicia seguimiento prioritario de un contacto concreto.
- **Seguimiento múltiple:** permite mantener varios contactos simultáneamente.
- **Seguir firma concreta:** mantiene la observación sobre una firma específica del contacto.
- **Actualizar posición:** obtiene una nueva estimación de posición.
- **Estimar rumbo:** calcula dirección probable de movimiento.
- **Estimar velocidad:** calcula velocidad actual con la confianza disponible.
- **Predecir trayectoria:** proyecta posición futura con incertidumbre creciente.
- **Recuperar contacto perdido:** usa última posición, trayectoria, velocidad y firmas conocidas para crear un área probable de búsqueda.

### Reglas aprobadas

1. **El seguimiento continuado mejora el conocimiento del movimiento** al acumular observaciones, sin revelar mágicamente la naturaleza del contacto.
2. **La capacidad de seguimiento de la nave es limitada** y depende de sensores, clase, era, estado, potencia e interferencias.
3. Existen **seguimiento normal y prioritario**. El prioritario consume más recursos a cambio de mejor actualización/precisión.
4. **Los contactos pueden perderse y recuperarse**. Una pérdida no borra la ficha; pasa a estado `lost` con última posición, vector, velocidad y firmas conocidas.
5. **Las predicciones nunca son certezas**. La confianza cae cuanto más lejos se proyecta en el tiempo y puede quedar invalidada por maniobras o cambios de firma.
6. El seguimiento múltiple reparte capacidad. La saturación puede reducir frecuencia de actualización, precisión o provocar pérdida de contactos secundarios.
7. Todas las actualizaciones se incorporan a la ficha persistente de contacto de la memoria de la nave.


## LECTURA SENSORIAL v0.1 — decisiones aprobadas

Esta rama queda **FIJADA**.

La lectura sensorial muestra únicamente datos medidos, estimados o comparados a partir de observaciones reales:

- intensidad de señal;
- tipo de firma;
- banda / frecuencia;
- firma energética;
- firma subespacial;
- masa aproximada;
- dimensiones aproximadas;
- vector / velocidad;
- formas de vida detectables;
- coincidencias con patrones conocidos.

### Reglas aprobadas

1. **Sensores mide; Ciencia interpreta.**
2. Las lecturas pueden mostrar **incertidumbre explícita**, márgenes de error y confianza.
3. Cada dato conserva **procedencia**, momento de observación y nivel de confianza.
4. Sensores puede comparar una lectura con la base de datos de la nave, pero una coincidencia no equivale automáticamente a certeza.
5. Sensores no formula causas científicas complejas salvo que exista una identificación sustentada por conocimiento previo válido.
6. La lectura nunca revela propiedades autoritativas del mundo que no hayan sido realmente observadas.

## Pipeline Sensores → Ciencia v0.1 — aprobado

Desde una ficha de contacto, lectura o resultado de Sensores, el operador puede usar **ENVIAR DATOS A → CIENCIA**.

El flujo funcional queda fijado:

```text
SENSORES
→ seleccionar contacto/lecturas
→ ENVIAR DATOS A CIENCIA
→ elegir prioridad
→ indicar análisis solicitado
→ confirmar envío
→ tarea pendiente en CIENCIA
→ análisis por personal/sistema científico autorizado
→ resultado científico
→ actualización de la ficha común del contacto
```

### Reglas

- El paquete solo contiene datos que la nave conoce realmente.
- Incluye observaciones, confianza, procedencia, hora y operador cuando proceda.
- Ciencia puede aceptar, analizar, devolver **NECESITA MÁS DATOS**, completar o cancelar la tarea.
- Si Ciencia necesita más datos, puede solicitar a Sensores un nuevo barrido o una configuración concreta.
- Los hallazgos científicos se incorporan a la misma ficha persistente del contacto con `source_system = science`.
- La interpretación científica no sustituye ni borra las lecturas originales de Sensores.
- Este patrón se reutilizará para futuros envíos a otras consolas, respetando siempre el ámbito funcional de cada una.


## INTERFERENCIAS / COMPENSACIÓN v0.1 — decisiones aprobadas

Esta rama queda **FIJADA** con el siguiente comportamiento:

- **Estado de interferencias:** indica si la lectura está limpia, degradada o comprometida y cuánto afecta al rendimiento.
- **Tipo de interferencia:** intenta clasificar la causa observable del ruido o degradación.
- **Compensación automática:** aplica ajustes rápidos y seguros con criterios del sistema; no garantiza la mejor solución.
- **Ajuste manual:** permite al operador seleccionar estrategias de compensación específicas.
- **Cambiar banda / frecuencia:** desplaza la observación hacia bandas menos afectadas.
- **Aumentar potencia:** mejora la capacidad de atravesar ruido a cambio de recursos energéticos.
- **Reducir resolución:** sacrifica detalle para estabilizar o conservar el contacto.
- **Prolongar integración:** acumula datos durante más tiempo para separar señal y ruido.
- **Intentar recuperar señal:** usa historial, última posición, trayectoria y firmas conocidas para reacquirir un contacto degradado o perdido.

### Reglas aprobadas

1. **La compensación reduce los efectos de la interferencia; no elimina mágicamente la causa física.**
2. **Toda compensación tiene un coste o sacrificio** en energía, tiempo, resolución, cobertura o capacidad disponible.
3. **Automático = cómodo y robusto; manual = potencialmente mejor**, pero exige decisiones correctas del operador.
4. **Las interferencias afectan de forma distinta a distintas firmas y bandas.**
5. Se distingue entre **interferencia ambiental** y **contramedidas deliberadas**, pero Sensores no siempre puede conocer inmediatamente cuál es la causa.
6. **Recuperar señal utiliza el historial persistente del contacto** y no crea una nueva identidad si la reidentificación es suficientemente sólida.
7. **Las compensaciones dependen del entorno actual**; una solución que funcionaba puede dejar de ser válida si cambian las condiciones.

### Interferencia ambiental vs deliberada

Ejemplos ambientales:
- ruido subespacial;
- partículas cargadas;
- turbulencia gravimétrica;
- radiación;
- actividad electromagnética natural.

Ejemplos deliberados:
- jamming;
- enmascaramiento de firmas;
- contramedidas electrónicas;
- reducción o alteración intencionada de emisiones;
- tecnologías de ocultación cuando sean válidas para era/clase.

Sensores puede informar de la degradación y de patrones observables. La atribución causal compleja puede requerir Ciencia, Táctica u otra consola especializada.


## CONFIGURACIÓN v0.1 — decisiones aprobadas

Esta rama queda **FIJADA**.

La configuración define cómo trabaja normalmente la consola de Sensores. No ejecuta por sí misma un barrido, búsqueda o seguimiento.

### Ajustes disponibles

- sensibilidad;
- resolución predeterminada;
- potencia utilizable por Sensores;
- matriz / conjunto sensor;
- banda / frecuencia;
- frecuencia de actualización;
- filtros predeterminados;
- prioridades predeterminadas;
- perfiles / preajustes.

### Jerarquía de configuración

```text
ESTÁNDAR DE LA NAVE
        ↓
PERFIL DEL OPERADOR
        ↓
CONFIGURACIÓN TEMPORAL DE OPERACIÓN
```

La capa inferior puede sobrescribir temporalmente a la superior sin modificarla de forma permanente.

### Reglas aprobadas

1. **Configuración establece valores base; no ejecuta operaciones.**
2. Una operación concreta puede **sobrescribir temporalmente** valores sin modificar los predeterminados.
3. Ningún ajuste puede superar las capacidades reales de la nave, era, matrices disponibles, potencia autorizada o estado de daños.
4. Sensores solo administra la potencia que tiene asignada. Si necesita más, debe **solicitar potencia adicional a OPS**.
5. Sensibilidad, resolución, frecuencia de actualización y potencia tienen costes reales; no pueden maximizarse gratis.
6. Los perfiles son **conjuntos de ajustes**, no bonificaciones ocultas.
7. Puede haber perfiles estándar de la Flota y perfiles personalizados del operador.
8. Los ajustes y perfiles pertinentes pueden persistir en la memoria de la nave.
9. Los errores humanos siguen siendo posibles: una banda, filtro o prioridad técnicamente válidos pero mal escogidos se aplican igualmente.
10. Debe existir **RESTAURAR CONFIGURACIÓN ESTÁNDAR** para volver al baseline autorizado de la nave.

### Potencia y frontera con OPS

Sensores puede distribuir y consumir la potencia que ya tiene asignada. No puede apropiarse unilateralmente de energía de otros sistemas. Una necesidad superior genera una solicitud operativa a OPS.

### Matrices sensoras

Las matrices disponibles dependen de la definición real de cada nave. Pueden existir matrices principales, laterales, de largo alcance, auxiliares u otras válidas para la clase y era. El daño puede degradar o inutilizar una matriz.

### Perfiles

Los perfiles pueden incluir valores como sensibilidad, resolución, actualización, filtros, prioridades, matriz y banda. Un perfil solo automatiza la configuración.

Ejemplos de perfiles estándar posibles:

- Estándar;
- Navegación;
- Búsqueda y rescate;
- Ciencia;
- Seguimiento;
- Bajo ruido;
- Largo alcance.

Los operadores pueden guardar perfiles personales siempre que los ajustes sean técnicamente válidos para la nave.

### Academia

Esta rama es materia válida de entrenamiento y examen práctico: el cadete puede recibir una situación y tener que preparar correctamente la consola antes de ejecutar una operación.
