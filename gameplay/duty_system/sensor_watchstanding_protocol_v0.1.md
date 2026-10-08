# Protocolo de guardia de Sensores v0.1

Estado: **FOUNDATION FIXED**

## Principio

La estación de Sensores no espera órdenes para empezar a observar el espacio.

SENSORES / COMPUTADORA → vigilancia pasiva continua → actualización de la situación → detección de cambios reales del World State → aviso solo si algo merece atención → oficial investiga / prioriza / informa.

La vigilancia continua **no crea acontecimientos**. Si el espacio está tranquilo, una guardia completa puede terminar sin novedad.

La vigilancia es una responsabilidad del **runtime de la nave**, no de la pantalla de la consola. Debe existir durante todo el tiempo simulado en que la nave esté operativa, aunque el jugador no esté sentado en Sensores. Al reanudar una nave tras tiempo fuera de pantalla, el Core debe resolver el catch-up del World State y reconstruir la imagen sensorial coherente antes de presentar novedades al jugador.

## Separación de responsabilidades

### Automatización de la nave

En condiciones normales, el subsistema de Sensores y la Computadora mantienen de forma automática:

- vigilancia pasiva de corto y largo alcance dentro de las capacidades de la nave;
- actualización periódica de contactos ya conocidos;
- adquisición de contactos que el World State hace físicamente detectables;
- comparación con lecturas anteriores;
- correlación básica de firmas y transpondedores;
- mantenimiento de seguimientos ya autorizados mientras haya capacidad;
- control de integridad/calibración/disponibilidad de matrices;
- control de interferencias y degradación de calidad;
- registro temporal de observaciones;
- evaluación de umbrales y órdenes permanentes;
- generación de avisos cuando aparece una novedad significativa;
- clasificación de nuevos contactos como identificados, no identificados o de identidad incierta;
- reconocimiento automático de transpondedores válidos cuando el World State lo permita;
- detección de pérdidas anómalas de contactos previamente estables.

Estas rutinas son deterministas y no requieren una llamada LLM.

### Obligaciones normales del oficial de Sensores

Aunque la computadora haga el trabajo repetitivo, el oficial de guardia sigue siendo responsable de:

- supervisar que la imagen de sensores sea coherente;
- revisar avisos y lecturas de baja confianza;
- investigar contactos o firmas ambiguas;
- ordenar barridos focalizados o análisis adicionales dentro de su autoridad;
- ajustar filtros, sensibilidad y prioridades cuando la situación lo requiera;
- mantener una imagen de contactos útil para el puente;
- detectar y comunicar degradaciones del sistema;
- mantener registros y preparar el relevo;
- informar de novedades relevantes al oficial que tenga el mando del puente.

El oficial no necesita una orden superior para cada actuación técnica rutinaria propia de su puesto.

## Acciones que normalmente requieren orden, autorización o una regla previa

Dependiendo de doctrina, misión y órdenes permanentes, pueden requerir autoridad superior:

- usar emisiones activas si pueden revelar la posición de la nave;
- pedir o reasignar potencia fuera de la asignación ordinaria;
- abandonar un seguimiento protegido para liberar recursos;
- ejecutar exploraciones intrusivas o políticamente sensibles;
- alterar prioridades tácticas o de misión;
- adoptar decisiones que correspondan al mando.

La Computer puede proponer; no sustituye a la autoridad humana.

## Calma operativa

**Una guardia sin incidentes es un resultado válido.**

La rutina automática no genera enemigos, anomalías, llamadas de socorro ni contactos para entretener al jugador, y no altera el World State para producir gameplay.

Si el World State no cambia y no hay ninguna condición relevante, la Computer permanece silenciosa salvo consultas del oficial.

## Adquisición automática de contactos

La vigilancia pasiva 24/7 mantiene dos capas simultáneas: corto alcance y largo alcance.

Cuando un contacto entra en detectabilidad:

- si existe un transpondedor reconocido o una correlación suficiente, la Computer lo incorpora como **contacto identificado** y muestra los datos disponibles;
- si no existe identificación suficiente, lo incorpora como **nuevo contacto desconocido/no identificado**;
- los contactos desconocidos nuevos deben quedar visualmente resaltados hasta que el oficial los revise, seleccione o investigue;
- el hecho de que un contacto sea visible no autoriza a la Computer a inventar su identidad, intención o afiliación.

El oficial puede continuar usando la consola para otras tareas mientras esta adquisición automática sigue funcionando.

## Pérdida de contacto y desaparición anómala

La Computer debe distinguir entre una pérdida **explicable** y una pérdida **anómala**.

Pérdidas explicables incluyen, cuando el estado lo justifique, salida de alcance, interferencia conocida, oclusión conocida, entrada en sombra sensorial o una partida a curvatura detectada.

Si un contacto que estaba estable y con confianza suficiente desaparece súbitamente sin una explicación sensorial conocida, la Computer debe generar una alerta inmediata de **pérdida anómala de contacto**.

La alerta debe informar solo de hechos observados:

- contacto afectado;
- última confianza;
- última distancia;
- último rumbo/vector;
- última velocidad;
- hora de última observación;
- causa: no determinada.

La Computer **no debe decir que el contacto explotó, fue destruido, se camufló o saltó a curvatura** salvo que exista evidencia suficiente para esa conclusión.

## Avisos de rutina

La Computer debe interrumpir al oficial solo cuando exista una condición que cruce un umbral o una orden permanente, por ejemplo:

- nuevo contacto detectable;
- contacto perdido;
- pérdida súbita anómala de un contacto previamente estable;
- cambio significativo de vector/velocidad;
- cambio material de confianza o clasificación;
- firma que coincide con una vigilancia activa;
- degradación de matriz o interferencia fuera de tolerancia;
- señal de socorro o transpondedor relevante;
- condición incluida en órdenes permanentes.

Los cambios mínimos o ruido normal pueden registrarse sin aviso de voz/UI.

## Cadena de información en el puente

La estación informa al **oficial que tenga el mando del puente en ese momento**.

SENSORES → OFICIAL AL MANDO DEL PUENTE / OFICIAL DE GUARDIA → CAPITÁN, si corresponde.

El capitán recibe el informe directamente cuando está personalmente al mando del puente, una orden permanente exige avisarle, el oficial al mando decide escalar o la gravedad activa un protocolo de notificación/recall.

No se despierta ni se interrumpe al capitán por cada contacto rutinario.

## Regla de implementación

La vigilancia de Sensores debe ser **event-driven + comprobación periódica**, nunca un generador aleatorio de aventuras.

World State cambia → Sensor Core evalúa detectabilidad → estado observado cambia → Routine Watch compara con baseline → si cruza criterio: ALERTA → si no: silencio.

Las acciones del propio jugador actualizan el baseline después de ejecutarse para evitar alertas duplicadas sobre algo que el oficial acaba de ordenar.

En la Holocubierta web, un temporizador local aproxima este comportamiento mientras el prototipo está abierto. En el juego final, la vigilancia pertenece al Core de la nave y debe continuar 24/7 en tiempo simulado, independiente de la UI concreta de Sensores.

## Relación con IA

La vigilancia automática no depende de Gemini. Core detecta y calcula; la Computer local decide si el cambio cruza un umbral de aviso; Gemini puede interpretar una orden natural del oficial; el LLM no crea el contacto ni decide que debe pasar algo.

## Objetivo de simulación

La estación debe permitir una guardia auténticamente tranquila: relevo, comprobación de estado, vigilancia pasiva, alguna consulta o ajuste rutinario si el oficial quiere, registro/relevo y fin de guardia sin novedad. También debe reaccionar de inmediato si el World State realmente cambia.

## Presentación visual de pérdida de contacto

- Pérdida normal explicable: tres pulsos amarillos y después el contacto pasa a CONTACTOS PERDIDOS.
- Pérdida de una amenaza hostil confirmada o estado táctico crítico: tres pulsos rojos y después pasa a CONTACTOS PERDIDOS.
- Pérdida anómala sin causa conocida: tres pulsos rojos y después pasa a CONTACTOS PERDIDOS.
- La afiliación, especie, clase militar o prioridad alta no bastan por sí solas para considerar un contacto hostil.
- El registro conserva la última solución conocida del contacto perdido.


### UX final de contactos perdidos

Los contactos perdidos no deben ocupar permanentemente la lista principal de contactos activos. Después de cualquier transición visual de pérdida, el contacto se archiva en un apartado consultable **CONTACTOS PERDIDOS**, con su última solución conocida, hora de pérdida y causa confirmada o no determinada. La lista principal queda reservada para contactos actualmente detectables. La Holocubierta puede mantener temporalmente una representación simplificada hasta la fase de UX final.
