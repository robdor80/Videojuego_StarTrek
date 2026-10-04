# Manual de Operador de Sensores - Flota Estelar

Estado: **APPROVED v0.1**
Uso: **Academia / PADD de estudio / Ordenador de a bordo**
Fuente funcional: `gameplay/ship_operations/consoles/sensors/`

> Este manual enseña procedimientos jugables. No es una wiki de Star Trek: cada concepto debe corresponder a una operación real del sistema.

## 00. Misión y filosofía

Sensores detecta, busca, localiza, mide, sigue y vuelve a observar el universo ya materializado.

Principios:

- primero existe la realidad y después se observa;
- Sensores solo presenta información obtenida legítimamente por la nave;
- alcance, resolución, potencia, daños, interferencia, duración y configuración importan;
- una configuración equivocada pero técnicamente válida se ejecuta;
- Sensores mide; Ciencia interpreta;
- Táctica evalúa amenaza y armamento;
- CONN/Navegación decide el movimiento de la nave;
- Ingeniería repara hardware;
- OPS administra prioridades globales de recursos.

## 01. Estado de sensores

Antes de operar, revisar:

- estado general;
- matrices disponibles;
- alcance efectivo;
- resolución disponible;
- potencia asignada;
- integridad / daños;
- interferencias;
- operación en curso.

El estado muestra capacidad real actual, no prestaciones ideales de catálogo.

## 02. Barridos

Un barrido responde: **«quiero observar esta zona y ver qué hay»**.

Tipos:

- corto alcance;
- largo alcance;
- focalizado.

Configuración:

- modo pasivo / activo;
- área u objetivo;
- resolución general / estándar / alta;
- filtros múltiples;
- prioridad;
- duración rápida / estándar / extendida / personalizada.

Reglas:

1. El barrido parte de valores por defecto razonables.
2. Solo se bloquea lo físicamente imposible.
3. El activo mejora detección pero puede delatar el escaneo.
4. El focalizado exige contacto, coordenadas o zona concreta.
5. Filtro y prioridad son conceptos distintos.
6. Repetir lo mismo en las mismas condiciones no revela mágicamente más.

### Ejemplo

Orden: «Barrido de largo alcance del sector 041. Prioridad a emisiones subespaciales.»

Ruta:

```text
SENSORES
-> BARRIDOS
-> LARGO ALCANCE
-> ÁREA: SECTOR 041
-> PRIORIDAD: SUBESPACIO
-> REVISAR
-> EJECUTAR
```

## 03. Búsqueda / localización

Una búsqueda responde: **«sé más o menos qué busco; intenta encontrarlo»**.

Objetivos:

- nave;
- lanzadera;
- sonda / baliza;
- forma de vida;
- objeto artificial;
- fuente de energía;
- firma warp;
- emisión subespacial;
- señal / transpondedor;
- radiación / partículas;
- firma definida.

Parámetros:

- área de búsqueda;
- sensibilidad;
- resolución;
- criterios.

La búsqueda devuelve candidatos compatibles, no identificación garantizada. Sensibilidad alta ayuda con señales débiles, pero aumenta ruido, contactos dudosos y falsos positivos. Un falso positivo es un artefacto de observación, no una entidad nueva del mundo.

## 04. Contactos y memoria de la nave

Un contacto es una ficha observacional persistente, no una afirmación de identidad perfecta.

Vistas:

- todos;
- no identificados;
- identificados;
- marcados;
- perdidos recientemente.

La ficha conserva:

- posición y distancia;
- vector y velocidad;
- firmas detectadas;
- confianza;
- clasificación disponible;
- historial;
- primera y última detección;
- fuentes de información;
- estado actual.

La identidad del contacto persiste si posición, trayectoria, firmas y continuidad temporal permiten justificar que sigue siendo el mismo objeto.

Las distintas consolas aportan conocimiento a la misma ficha, conservando procedencia:

- Sensores: firmas, posición y movimiento;
- Táctica: escudos, armas y postura;
- Ciencia: interpretación científica;
- Comunicaciones: señales y transpondedores;
- Ordenador: coincidencias históricas.

## 05. Seguimiento

Seguimiento mantiene contactos bajo observación.

Funciones:

- contactos seguidos;
- fijar contacto;
- seguimiento múltiple;
- seguir una firma concreta;
- actualizar posición;
- estimar rumbo y velocidad;
- predecir trayectoria;
- recuperar contacto perdido.

Reglas:

- el seguimiento continuado mejora el conocimiento del movimiento;
- la capacidad es finita;
- seguimiento prioritario consume más recursos;
- saturar seguimiento degrada actualización o precisión;
- perder un contacto no borra su ficha;
- la predicción tiene incertidumbre creciente.

## 06. Lectura sensorial

Puede mostrar:

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

Toda estimación puede llevar confianza o margen de error.

### Sensores -> Ciencia

Desde un contacto, lectura o resultado:

```text
ENVIAR DATOS A
-> CIENCIA
-> prioridad
-> análisis solicitado
-> confirmar
```

Ciencia recibe únicamente datos conocidos por la nave, con procedencia y confianza. Puede completar el análisis o responder **NECESITA MÁS DATOS** y solicitar un nuevo trabajo a Sensores.

## 07. Interferencias / compensación

Funciones:

- estado y tipo de interferencia;
- compensación automática;
- ajuste manual;
- cambio de banda;
- aumento de potencia;
- reducción de resolución;
- integración más larga;
- recuperación de señal.

Toda compensación tiene coste: potencia, tiempo, resolución, cobertura o capacidad.

La interferencia puede ser ambiental o deliberada. Sensores no siempre puede atribuir inmediatamente su causa.

## 08. Configuración

Jerarquía:

```text
ESTÁNDAR DE LA NAVE
-> PERFIL DEL OPERADOR
-> OVERRIDE TEMPORAL DE OPERACIÓN
```

Ajustes:

- sensibilidad;
- resolución predeterminada;
- potencia;
- matriz;
- banda / frecuencia;
- actualización;
- filtros;
- prioridades;
- perfiles.

Sensores solo utiliza la potencia asignada. Si necesita más, solicita a OPS.

Los perfiles son conjuntos de ajustes, no bonificaciones. Puede haber perfiles estándar de Flota y perfiles personales. Debe existir **RESTAURAR CONFIGURACIÓN ESTÁNDAR**.

## 09. Resultados

Resultados conserva el producto sensorial:

- operación actual;
- último barrido;
- resultados recientes;
- lecturas guardadas;
- comparar lecturas;
- repetir operación.

Cada resultado es una instantánea histórica con hora, configuración, procedencia y confianza. No se reescribe retroactivamente.

**Repetir operación** copia la configuración, pero ejecuta una operación nueva contra el estado actual del mundo.

Los resultados parciales pueden conservarse, siempre marcados como parciales.

Los datos pueden enviarse a Ciencia, Táctica, Operaciones, CONN/Navegación, Mando u Ordenador mediante paquetes estructurados.

## 10. Diagnóstico

Diagnóstico examina el sistema sensor, no el universo exterior.

Funciones:

- autodiagnóstico;
- estado por matriz;
- calibración;
- rendimiento;
- errores / degradación;
- solicitar soporte de Ingeniería.

Distinguir:

- funcionamiento nominal;
- degradación;
- descalibración;
- daño físico;
- offline.

Sensores puede recalibrar. Ingeniería realiza reparaciones físicas.

Un diagnóstico nominal puede descartar fallos conocidos del equipo, pero no demuestra que la interpretación de una señal externa sea correcta.

## 11. Procedimientos operativos estándar

### SOP-01 - Inicio de guardia

1. Revisar estado, matrices, potencia e interferencias.
2. Cargar perfil autorizado.
3. Ejecutar barrido pasivo de corto alcance.
4. Revisar contactos y trazas.
5. Informar desviaciones.

### SOP-02 - Contacto desconocido

1. Abrir ficha.
2. Revisar confianza y firmas.
3. Iniciar seguimiento.
4. Ejecutar focalizado si procede.
5. Comparar patrones.
6. Enviar a Ciencia/Táctica si la pregunta excede Sensores.

### SOP-03 - Búsqueda y rescate

1. Definir última posición y ventana temporal.
2. Seleccionar objetivo correcto.
3. Ajustar sensibilidad y criterios.
4. Priorizar firmas relevantes.
5. Revisar candidatos y falsos positivos.
6. Marcar y seguir candidatos relevantes.

### SOP-04 - Interferencia intensa

1. Identificar bandas afectadas.
2. Probar compensación.
3. Ajustar banda, potencia, resolución o integración.
4. Valorar el coste.
5. Enviar a Ciencia/Táctica si puede haber contramedida deliberada.

### SOP-05 - Fallo de sensor

1. Ejecutar autodiagnóstico.
2. Aislar componente.
3. Recalibrar si procede.
4. Cambiar de matriz si es posible.
5. Solicitar Ingeniería ante daño físico.

## 12. Lenguaje de informe

Informar lo que se sabe, no lo que se supone.

Ejemplos:

- «Traza subespacial intermitente, baja confianza.»
- «Posible nave, coincidencia 72 %, sin transpondedor detectado.»
- «Entre 48 y 63 formas de vida detectables; confianza 71 %.»
- «Posición estimada a +30 s, confianza 82 %.»
- «Autodiagnóstico nominal; no se detecta fallo conocido que explique la lectura.»

Nunca convertir «compatible con» en «es», «no detectado» en «no existe» o una predicción en certeza.

## 13. Errores comunes

- escanear el sector equivocado;
- usar filtros demasiado estrechos;
- confundir prioridad y filtro;
- maximizar sensibilidad sin considerar ruido;
- saturar seguimiento;
- atribuir una causa científica desde Sensores;
- repetir el mismo barrido esperando una mejora gratuita;
- ignorar calibración/daños;
- tomar potencia adicional sin pasar por OPS;
- intentar reparar hardware desde Sensores;
- olvidar conservar y comparar lecturas históricas.

## 14. Ejercicios de Academia

- **E-01:** barrido de largo alcance del sector 041 con prioridad subespacial.
- **E-02:** localizar una lanzadera desaparecida con interferencia moderada.
- **E-03:** recuperar Contacto 07 tras una pérdida.
- **E-04:** enviar una emisión desconocida a Ciencia para análisis.
- **E-05:** diagnosticar una matriz lateral con lecturas incoherentes.
- **E-06:** gestionar capacidad limitada de seguimiento ante un nuevo contacto prioritario.

Los ejercicios deben usar el backend real de Sensores. La UX de Academia guía; no sustituye la operación.

## 15. Referencia rápida

| Necesidad | Ruta |
|---|---|
| Ver qué hay | BARRIDOS |
| Encontrar algo por características | BÚSQUEDA / LOCALIZACIÓN |
| Abrir una ficha | CONTACTOS |
| Mantener observación | SEGUIMIENTO |
| Ver medidas | LECTURA SENSORIAL |
| Limpiar señal | INTERFERENCIAS / COMPENSACIÓN |
| Cambiar valores base | CONFIGURACIÓN |
| Revisar / guardar / comparar | RESULTADOS |
| Comprobar el equipo | DIAGNÓSTICO |

**Mantra:** Detecta. Mide. Conserva la incertidumbre. Comparte los datos. No inventes la conclusión.
