# SEN-301 — Sensores y adquisición de situación I

**Material de estudio v1.0 — edición desarrollada**  
**Cadete de 3.ª clase · Trimestre 1**

## Finalidad

Pasar de comprender qué es un sensor a operar las funciones básicas de la consola de Sensores y construir una imagen de situación fiable.

SEN-301 utiliza directamente la especificación funcional aprobada de Sensores. Esto significa que lo aprendido aquí debe corresponder con la futura consola real del juego.

La regla central es:

> **Sensores detecta, busca, localiza, mide, sigue y organiza observaciones. Ciencia interpreta en profundidad.**

---

# SEN-301-U01 — Estado del sistema

## 1. Antes de operar, comprobar

**Un operador no debe iniciar un barrido sin conocer el estado del sistema.**

La consola muestra:
- estado general;
- matrices disponibles;
- alcance efectivo;
- resolución disponible;
- potencia asignada;
- integridad o daños;
- interferencias;
- operación en curso.

## 2. Disponibilidad

Una función puede estar:
- disponible;
- limitada;
- degradada;
- no disponible.

No todas las matrices tienen por qué funcionar al mismo tiempo.

## 3. Cobertura

El alcance nominal no equivale al alcance efectivo.

El efectivo depende de:
- capacidad de la nave;
- potencia;
- integridad;
- interferencias;
- modo;
- entorno.

## 4. Potencia

Sensores administra la potencia ya asignada.

Si necesita más, debe solicitarla a Operaciones. No puede apropiarse unilateralmente de energía de otros sistemas.

## 5. Operación en curso

Antes de iniciar una nueva tarea hay que comprobar:
- si existe otra operación;
- qué recursos consume;
- si puede coexistir;
- si debe cancelarse o esperar.

### Práctica

Completa un checklist de estado y decide qué tipo de barrido es razonable con una matriz degradada.

### Autoevaluación

1. ¿Qué debe comprobarse antes de operar?
2. ¿Por qué alcance nominal y efectivo no son iguales?
3. ¿Qué factores reducen capacidad?
4. ¿Puede Sensores tomar energía de otro sistema directamente?
5. ¿Por qué importa saber si hay una operación en curso?

---

# SEN-301-U02 — Scans básicos

## 1. Tres tipos principales

La consola ofrece:
- corto alcance;
- largo alcance;
- focalizado.

## 2. Configuración

Un barrido puede configurar:
- modo activo/pasivo;
- área u objetivo;
- resolución;
- filtros;
- prioridad;
- duración.

**Los valores por defecto permiten cambiar solo lo necesario.**

## 3. Corto alcance

Es apropiado para observar el espacio cercano con buena sensibilidad dentro de su perfil de alcance.

## 4. Largo alcance

Cubre una región mayor con otras limitaciones y costes.

## 5. Focalizado

Concentra recursos sobre:
- contacto;
- coordenadas;
- zona concreta.

No existe un focalizado genérico “de todo” sin objetivo.

## 6. Resultado

Un barrido puede devolver:
- nada detectado;
- traza;
- contacto sin clasificar;
- parcialmente resuelto;
- resuelto.

No todos los scans producen una identificación completa.

### Práctica

Ejecuta tres barridos estándar cambiando solo un parámetro cada vez.

### Autoevaluación

1. ¿Qué tres tipos de scan existen?
2. ¿Qué parámetros pueden configurarse?
3. ¿Qué exige un focalizado?
4. ¿Por qué un scan puede terminar en “traza”?
5. ¿Qué diferencia existe entre no detectado y resuelto?

---

# SEN-301-U03 — Búsqueda y localización

## 1. Barrer y buscar no son lo mismo

**Barrido:** “quiero observar esta zona y ver qué hay.”

**Búsqueda:** “sé aproximadamente qué quiero encontrar; intenta localizar candidatos compatibles.”

## 2. Objetivos de búsqueda

Puede buscarse:
- nave;
- lanzadera;
- sonda o baliza;
- forma de vida;
- objeto artificial;
- fuente de energía;
- firma warp;
- emisión subespacial;
- señal o transpondedor;
- radiación o partículas;
- firma personalizada.

## 3. Parámetros

La búsqueda utiliza:
- área;
- sensibilidad;
- resolución;
- criterios.

## 4. Sensibilidad

Aumentar sensibilidad puede:
- descubrir señales débiles;
- aumentar ruido;
- producir más candidatos dudosos;
- aumentar falsos positivos.

## 5. Candidatos

**Una búsqueda devuelve candidatos compatibles.**

No garantiza:
- identidad;
- intención;
- clasificación final.

## 6. Error de configuración

Una búsqueda mal configurada pero técnicamente válida se ejecuta.

El sistema no corrige silenciosamente al operador.

### Práctica

Localiza una baliza conocida dentro de una zona con señales débiles y varios candidatos.

### Autoevaluación

1. Diferencia barrido y búsqueda.
2. Nombra cinco objetivos de búsqueda.
3. ¿Qué parámetros utiliza?
4. ¿Qué coste tiene aumentar sensibilidad?
5. ¿Una búsqueda garantiza identidad?

---

# SEN-301-U04 — Contactos

## 1. Qué es un contacto

**Un contacto es una ficha observacional persistente de algo detectado.**

La nave no expone al jugador el identificador oculto de la entidad real.

## 2. Estados

Puede aparecer como:
- no identificado;
- identificado;
- marcado;
- perdido recientemente;
- activo;
- archivado.

## 3. Ficha

Solo se muestran datos realmente descubiertos:
- posición;
- distancia;
- vector;
- velocidad;
- firmas;
- confianza;
- clasificación disponible;
- historial.

## 4. Identidad persistente

Si un contacto se pierde y se recupera con posición, trayectoria y firmas compatibles, puede mantener el mismo contact_id.

No debe crearse un “objeto nuevo” cada vez que desaparece temporalmente.

## 5. Actualización

Cada nueva observación puede:
- aumentar confianza;
- cambiar clasificación;
- modificar trayectoria;
- contradecir datos anteriores.

## 6. Pérdida

Perder un contacto no borra su historia.

Se conserva:
- última posición;
- rumbo;
- velocidad;
- firmas;
- hora de pérdida.

### Práctica

Gestiona cinco contactos: dos identificados, uno dudoso, uno perdido y uno recién detectado.

### Autoevaluación

1. ¿Qué representa un contacto?
2. ¿Qué datos puede contener?
3. ¿Por qué la identidad puede persistir tras una pérdida?
4. ¿Qué ocurre con la historia cuando se pierde?
5. ¿Puede una nueva observación contradecir una clasificación anterior?

---

# SEN-301-U05 — Tracking y readout

## 1. Tracking

El seguimiento acumula observaciones para actualizar:
- posición;
- rumbo;
- velocidad;
- trayectoria probable.

**No revela automáticamente qué es el objeto.**

## 2. Capacidad finita

La nave no puede seguir un número infinito de contactos con máxima calidad.

La capacidad depende de:
- clase;
- era;
- matrices;
- potencia;
- daños;
- interferencias.

## 3. Seguimiento prioritario

Un contacto prioritario puede recibir más recursos y mejor actualización.

Eso reduce recursos disponibles para otros.

## 4. Readout

La lectura sensorial puede incluir:
- intensidad;
- firma;
- banda;
- energía;
- subespacio;
- masa aproximada;
- dimensiones;
- vector;
- velocidad;
- formas de vida detectables;
- coincidencia con patrones.

## 5. Calidad

Cada dato debe conservar:
- procedencia;
- hora;
- confianza;
- margen.

## 6. Predicción

Predecir trayectoria produce una estimación cuya confianza cae con el tiempo y puede invalidarse si el contacto maniobra.

### Práctica

Mantén seguimiento de tres contactos y emite un readout breve de uno prioritario.

### Autoevaluación

1. ¿Qué mejora tracking?
2. ¿Por qué la capacidad es finita?
3. ¿Qué coste tiene priorizar un contacto?
4. ¿Qué debe conservar cada dato?
5. ¿Por qué una trayectoria predicha no es certeza?

---

# SEN-301-U06 — Interferencia básica

## 1. Interferencia

**La interferencia degrada la relación entre señal y lectura.**

Puede ser:
- ambiental;
- deliberada.

## 2. Ejemplos ambientales

- partículas;
- radiación;
- ruido subespacial;
- actividad electromagnética;
- turbulencia gravimétrica.

## 3. Ejemplos deliberados

- jamming;
- enmascaramiento;
- contramedidas;
- reducción intencionada de emisiones.

Sensores puede observar patrones de degradación sin conocer siempre la causa real.

## 4. Compensación

Opciones básicas:
- automática;
- cambiar banda;
- aumentar potencia;
- reducir resolución;
- prolongar integración;
- intentar recuperar señal.

## 5. Costes

Toda compensación tiene algún coste:
- energía;
- tiempo;
- resolución;
- cobertura;
- capacidad de tracking.

## 6. Límites

Compensar no elimina la causa física.

Puede reducir su efecto.

### Práctica

Repite una búsqueda bajo interferencia y compara dos estrategias de compensación.

### Autoevaluación

1. ¿Qué diferencia existe entre interferencia ambiental y deliberada?
2. ¿Puede Sensores conocer siempre la causa?
3. Nombra cuatro opciones de compensación.
4. ¿Qué costes puede tener?
5. ¿Por qué compensar no equivale a eliminar la causa?

---

# Evaluación del curso

SEN-301 evalúa operación real de estado, scans, búsqueda, contactos, tracking, readout e interferencia básica.

# Relación con v0.0.1

Este curso utiliza directamente el árbol funcional aprobado de la consola de Sensores y es prioritario para el vertical slice.

# Referencias internas

- `gameplay/ship_operations/consoles/sensors/README.md`
- `gameplay/ship_operations/consoles/sensors/sensor_menu_tree.json`
- `gameplay/ship_operations/sensor_resolution/sensor_detection_rules.json`
- `gameplay/careers/academy_path/study_materials/sensors/SENSORS_OPERATOR_MANUAL_v0.1.md`
