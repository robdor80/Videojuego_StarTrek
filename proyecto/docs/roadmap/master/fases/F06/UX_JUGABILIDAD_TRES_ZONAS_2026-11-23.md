# F06 / ASTER — Diseño funcional de la consola jugable de tres zonas
**Fecha:** 23/11/2026 · **Estado:** especificación funcional del propietario para la segunda prueba en MSI. **No es implementación ni aprobación final.**

## 0. Meta del jugador
Que apetezca desempeñar una guardia auténtica como **oficial de Sensores de la USS Enterprise NCC-1701-D, clase Galaxy, modernizada por el Proyecto Valhalla**. La computadora realiza aproximadamente el 95 % de los trabajos rutinarios y vigila 24/7 desde el segundo cero. El oficial **comprende, decide, investiga cuando quiere, informa y vigila objetivos de interés**. Una guardia normal puede transcurrir sin novedades. No generar amenazas para entretener.

**Regla de oro: un dato o texto visible debe aportar información distinta y útil para una decisión.** Eliminar telemetría, IDs del Core, «completado y registrado» sin resultado, recibos numéricos y frases redundantes de la pantalla principal. Información técnica de auditoría solo en registro/diagnóstico.

Este es un banco funcional **Tkinter/CoreRPG de F06**, NO diseño LCARS definitivo de F07, ni puesto UE5/F08, ni universo dinámico F13. Mantener la prueba ASTER_X1 nueve minutos reales ×1 y regresión histórica acelerada independiente.

## 1. Distribución física explícita según imagen anotada del propietario
Tres **marcos permanentes finos y claramente visibles** en toda la consola, exclusivamente para distinguir las zonas de esta prueba:
- **ROJO — lateral IZQUIERDO:** navegación/operaciones y listas contextuales.
- **AZUL — COLUMNA CENTRAL:** área SUPERIOR mapa espacial; área INFERIOR imagen/modelo disponible + resumen contextual.
- **VERDE — lateral DERECHO:** información completa, lecturas especializadas y acciones contextuales.

Proporciones iniciales orientativas ~20 % rojo / ~38 % azul / ~42 % verde; adaptar al espacio disponible, escalado de Windows y redimensionado sin cortar botones, listas o texto. En Tk utilizar bordes perceptibles (~2–3 px), discretos y persistentes, no fondos chillones; no confundir **marco verde de la zona** con verde de conformidad, **marco rojo** con alertas de peligro, etc. Hacer pruebas a 2560×1600 con escalado (MSI) y a resoluciones menores habituales. El pie de estado no debe pisar las zonas.

**No invertir lados:** rojo a izquierda, azul centro y verde derecha, tal y como figura en el croquis del propietario.

## 2. Semántica de las cuatro entradas ROJAS
GENERAL y CONTACTOS = **vistas principales**.
SEGUIMIENTO y ANÁLISIS = **vistas especializadas relativas al contacto elegido**. Pueden mantener listas persistentes de objetivos seguidos o analizados. El mismo objeto puede existir en Contactos, Seguimiento y Análisis sin representar entidades duplicadas.

### GENERAL — «¿Qué hay alrededor?»
- Por defecto sin contacto seleccionado: mapa espacial general con la Enterprise y el entorno observable. Azul inferior: **descripción breve del sistema/zona/cuadrante real** en que se encuentra la nave. Verde: lecturas ambientales relevantes (partículas, interferencias, asteroides, fenómenos, perturbaciones); si el espacio está vacío, mostrar serenamente ausencia de incidencias, no fabricar contenido.
- **Restaurar el ASTER original** en modo ×1: estrella, seis planetas, cuatro lunas y otros cuerpos/estación/fenómenos respaldados por el escenario y por lecturas públicas. No sustituirlo por cinco naves; no filtrar la información secreta de Host.
- La exploración manual de un planeta o cuerpo cambia los paneles según selección, sin apagar vigilancia.

### CONTACTOS — «¿Qué hemos detectado?»
- Rojo: lista de **todos los contactos observables** (categorías agrupadas con sentido, selección legible), no solo avisos recientes. El mapa azul superior los representa y la selección centra/encuadra el elegido; incluir control para mostrar el mapa general.
- Azul inferior: **resumen corto del objeto seleccionado**, con imagen 2D/modelo 3D real si ya está disponible; de lo contrario, etiqueta neutra o silueta honesta, nunca representar un recurso inexistente como cargado. En un planeta: nombre y clase M/H/J/etc. **solo cuando realmente esté observada**. En una nave: nombre, matrícula, modelo/clase, procedencia/misión si se conocen.
- Verde: **datos útiles del objeto seleccionado**; tipo de datos depende de clase de objeto.
  * Planeta: mediciones científicas (atmósfera, temperatura, presión, composición, condiciones, etc., si están justificadas por Core/F06), con acción de transferencia a Ciencia.
  * Nave conocida: clase, diseño, matrícula, transpondedor, origen/destino/misión, tripulación, etc. **solo si disponible por identificación, registros autorizados o mediciones**; no confundir diseño con afiliación actual.
  * Nave desconocida: tipo/clase/facción si deducibles, distancia, desplazamiento, rumbo/velocidad, estado energético, armas realmente medidas, escudos, propulsión y diferencias/ausencias; sin transpondedor también se detectan armas. Nunca reducir la ficha a «contacto desconocido».
- Sin selección de contacto se vuelve a General ambiental (o estado general del modo contactos, sin ficha falsa).

### SEGUIMIENTO — «¿Qué está haciendo ahora?»
- Solo objetivos **marcados por el jugador** para vigilancia exhaustiva. Sigue existiendo la vigilancia pasiva automática del resto.
- Seleccionar SEGUIR activa seguimiento prioritario y **compartición continua automática con Táctica**, por la autoridad/cola CoreRPG disponible. No exigir botones de reenvío cada vez que cambien rumbo, potencia o armas. En QA, recibos reales a cola QA, nunca fingir consumo por NPC.
- Azul superior: mapa centrado en el objetivo, trayectorias y cambios de movimiento que estén respaldados por lecturas.
- Azul inferior: identidad visual y resumen breve del objetivo.
- Verde: **hasta cuatro subzonas contextuales**, ocupadas solo si hay datos: (1) navegación, velocidad, rumbo, distancia, acercamiento/interceptación; (2) armas/escudos/energía; (3) maniobras/cambios de actividad en vivo; (4) incidencias y estado del seguimiento. No cuatro paneles vacíos ni toda la ficha repetida.
- Avisar en tiempo real de incremento de potencia ofensiva, cambios de escudos, aceleración o preparación de curvatura **cuando existan medidas suficientes**. No inferir intenciones/ataque solo por una clase o por cambiar de rumbo.
- Ejemplo de alerta concisa: **«ALERTA · CRUCERO ROMULANO D'DERIDEX — Aumento de energía detectado. La nave está preparando sus armas.»** Este mensaje requiere señal de preparación ofensiva medida, no simple variación genérica. No añadir «Variación observada en los sistemas ofensivos del contacto C-...» si ya se ha dicho lo mismo.

### ANÁLISIS — «¿Qué hemos averiguado en profundidad?»
- Lista de objetivos cuyo análisis detallado ha sido solicitado; al seleccionarlos, verde presenta **solo descubrimientos adicionales y profundos, no copia de la ficha inicial**: tecnología, composición/estructura, armas por tipo y sistemas, escudos y potencia, propulsión, firma energética, tripulación detectada/estimada, modificaciones, anomalías, puntos vulnerables cuando realmente medibles, y para cuerpos celestes ciencia profunda.
- **Tiempo funcional máximo 0–2 s reales en el MSI** para análisis de sensores dentro del modelo QA; resultado aparece directamente. El análisis rutinario completo de sensores no necesita barra artificial ni una operación de veinte segundos que solo devuelva «registrado».
- Si falta un dominio físico para producir nuevas mediciones, **implementar modelo/observación autorizado y pruebas** o indicar de modo honesto «No hay nuevas lecturas verificables»; no inventar información en Python, no convertir datos secretos Host en conocimiento.
- Estudios científicos de otra naturaleza que realmente exijan tiempo se separan y etiquetan explícitamente, nunca bloquean ficha inmediata ni el análisis normal.
- La información básica del contacto existe automáticamente antes de pulsar Análisis; este modo tiene valor solo si aporta **más conocimiento**.

## 3. Reglas de presentación comunes
- La zona AZUL responde a «¿qué estoy observando?»; la VERDE a «¿qué sabemos y qué cambia?»; la ROJA a «¿qué quiero hacer?».
- No repetir grandes títulos, tablas o descripciones entre zonas. Escalas y nombres en castellano natural. ID interno C-XXX solo mientras no existe identificación mejor o es necesario desambiguar dos objetivos equivalentes.
- Interfaz **contextual**: botones sencillos, exclusivamente pertinentes al objeto y modo. «Seguir», «Analizar», «Enviar a Táctica», «Enviar a Ciencia», «Comunicar por voz», «Enviar informe» según contexto; no una botonera inmóvil llena de controles imposibles.
- Mostrar diferencias de armamento conocido vs observado con verde/ámbar/rojo/gris de **estado técnico**; estos colores no dependen de los marcos de zona. Mostrar de forma legible tipos de armas y escudos y recuentos cuando físicamente observables.
- Datos **confirmados**, **estimados** y **no observables** con señalización discreta. Core es autoritativo sobre WorldState; GUI no puede inventar tripulación, destino, clase, intención, nombre ni equipamiento.
- No bloquear o recortar fichas extensas, mapas, botones ni desplazamiento. Al cambiar de selección volver al inicio del detalle; mantener selección consistente entre rojo/azul/verde. Accesibilidad de alto contraste e indicadores no basados solo en color.

## 4. Prioridades, interrupciones y recuperación
- Contacto civil normal = registrar y actualizar mapa sin cambiar vistas ni interrumpir.
- Nave **desconocida** u objeto espacial crítico = alerta prioritaria, la computadora interrumpe exploración rutinaria, centra mapa, muestra ficha inmediata y permite actuar.
- Contacto Borg/amenaza grave/armas activándose = máxima prioridad y alerta inequívoca.
- **Al interrumpir, conservar** planeta, pestaña, desplazamiento lógico y trabajo anterior; ofrecer retorno visible a «Retomar estudio de Aster IV». No perder resultados, no borrar seguimiento ni análisis.
- Cuando una situación deja de ser crítica, bajar o retirar la alerta activa; no dejar rojo permanentemente tras cesar su causa. No ocultar información por múltiples alertas; clasificación, ciclo de vida y prioridad.
- Mensajes cortos sin repeticiones. Enviar información relevante al jugador, no cientos de logs. Ante falta de medición, «Trayectoria aún no determinada», no afirmar interceptación.

## 5. Comunicaciones y flujo de mando
- El oficial decide si/ cuándo informa al capitán o superior, salvo transferencia automática a Táctica al ordenar seguimiento activo.
- **COMUNICAR POR VOZ:** preparar un guion breve y preciso con la ficha viva, para que el jugador lo pronuncie libremente por canal de puente cuando exista sistema de voz. En F06 QA mostrar guion y simular apertura del canal solo como vista/contrato etiquetado de pruebas; **no fingir conversación NPC/voz real**.
- **ENVIAR INFORME:** permitir elegir destinatario y entregar observación/situación autorizada a la cola Core QA con recibo real (en producción se enlazará al mando).
- «Datos transferidos a Táctica» / «Informe enviado al capitán», no IDs gigantes de recibo en pantalla principal. Historial técnico auditable aparte.
- **Nueva observación importante** sobre contacto ya informado habilita actualización al superior y a Táctica; evitar duplicados idénticos pero no bloquear la segunda comunicación de un incidente distinto.
- Si se inicia SEGUIR, Táctica debe recibir automáticamente información actualizada; no pedir además «Transferir a Táctica» por cada cambio.

## 6. Prueba humana y criterios de aceptación
**Obligatoria:** ASTER_X1, nueve minutos reales a velocidad ×1, sin acelerar; contactos 60 s carguero rutinario, 150 s D'deridex modificada, 210 s modificación carguero, 240 s clase desconocida, 300 s actividad ofensiva, 360 s camuflaje efectivo invisible, 390 s descamuflaje, 450–465 s fallo/recuperación; escenario de ocho horas separado.
- Sistema Aster se ve **completo** y se pueden seleccionar cuerpos celestes desde el minuto cero; General muestra ciencia ambiental respaldada por observación.
- Un contacto rutinario no interrumpe; uno prioritario sí, sin perder contexto; mapa/ficha verde/nombre coherentes.
- Una nave visible sin transpondedor muestra identidad por firma si se conoce y equipamiento observado, incluidas discrepancias, antes de 3 segundos desde aparición. Nave desconocida muestra lecturas reales sin clase fabricada.
- Seguir presenta datos cambiantes, **compartidos automáticamente con Táctica**, más las alertas energéticas que se detecten.
- Análisis devuelve **nueva información**, verificable y útil, en ≤2 s de tiempo real; si no hay nuevas medidas no mentir.
- Selección de planeta despliega clase, visual y ciencia disponibles; en modo General, lecturas ambientales, sin llenar espacio de basura.
- Comunicación por voz tiene guion QA; envío de informe tiene destinatario/acuse Core; nueva observación permite actualización.
- Bordes **ROJO, AZUL y VERDE** claramente visibles, correctos y persistentes en el MSI. Controles legibles y utilizables con escalado Windows.
- El usuario debe poder comprender qué está pasando y actuar **sin interpretar mensajes técnicos ni hacer navegación confusa**. Esta aceptación jugable/visual es independiente de los tests automatizados.
- Save/load de Core en otro proceso, restauración de contexto UI cuando se acuerde y prueba de regresión. Verificar casos de pérdida de contacto y degradación.
- Tests Core/QA C++, Python/Tk, Windows/Linux Actions, 9 min reales y 8 h aceleradas separadas. Documentar mediciones, evidencia y límites, sin declarar MSI superado por CI.

## 7. Observaciones de la primera aceptación MSI (INC01–INC07)
1. ASTER_X1 omitió estrella, planetas, lunas y resto del sistema; «Todo el sistema» mostraba solo naves.
2. ANÁLISIS tardaba demasiado (20s Core).
3. ANÁLISIS acababa con «completado y registrado» sin ampliar información.
4. Contactos civiles rutinarios cambiaban de modo y molestaban.
5. Al llegar la D'deridex, el aviso correspondía a ella pero el panel derecho seguía mostrando el carguero anterior; scroll sin reset.
6. Números enormes de recibos/observaciones en fichas, lenguaje burocrático.
7. Posible bloqueo de nueva comunicación cuando ya se avisó al superior y surgió actividad ofensiva nueva. Verificar y corregir si procede.
Además: alerta roja persistente al finalizar; comprobar si el estado de alerta se actualiza correctamente.

**No resuelto deliberadamente ahora:** estética LCARS premium, holografía, NPC y diálogo de voz real (F07/F08), universo F13 y producción UE5. No inventar esas piezas. Los modelos e imágenes 3D se mostrarán cuando existan assets reales.

## 8. Instrucciones de implementación
Punto de partida verificado PR Draft #206: rama `plan/f06-aster-aceptacion-x1-20261123`, SHA `433096fbfdb2a1f4f50953440fdc9d7243760fe8`, base `main`. Esta especificación está en rama documental derivada de ese SHA; verificar la rama actual antes de codificar, sin reescribir trabajos concurrentes.

Codex Cloud debe conservar CoreRPG, F04/F05, las interfaces, permisos, historial, observación auténtica y tests. Modificar la GUI y **solo el Core/Host/fixtures necesario para soportar datos científicos/operativos reales**, sin resultados prefabricados. Crear PR Draft de implementación (no fusionar main ni cerrar F06 sin aceptación MSI), ejecutar pruebas y explicar límites con claridad.

**Orden recomendado:** auditar contra branch real; restaurar mundo Aster; redefinir modelo de estado de vistas y selección; implementar presentación azul/verde contextual y 4 modos rojos; mejorar análisis/seguimiento/mensajes/comunicaciones; probar escenarios y regressiones; entregar MSI launcher de doble clic y guía muy corta.

**Modelo recomendado:** Codex Sol 6.1, esfuerzo Alto.
