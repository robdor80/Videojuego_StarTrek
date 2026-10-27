# IDEA-0003 — Hangares independientes por clase de nave y transiciones de atraque/despegue

**Proyecto:** Videojuego Star Trek RPG 3D  
**Área:** Naves estelares · Interiores 3D · Lanzaderas · Tránsito interior/exterior · Persistencia  
**Fecha:** 11 de octubre de 2026  
**Estado:** **IDEA-0003 · APROBADA CONCEPTUALMENTE; pendiente de planificación e implementación**  
**Destino:** `/ideas` del repositorio del videojuego Star Trek  
**Prioridad de diseño:** Alta para la inmersión; ejecución incremental según disponibilidad de modelos y sistemas.

---

## 1. Idea principal

Cada nave o clase de nave del juego podrá disponer de **uno o varios hangares interiores tridimensionales diseñados específicamente para ella**, con las dimensiones, distribución, decoración, equipamiento y capacidad que correspondan a su función y tamaño.

**No será obligatorio introducir físicamente esos hangares dentro de la geometría del modelo exterior de la nave.** El exterior y el hangar podrán ser dos escenarios 3D independientes que el videojuego conectará mediante una **transición de atraque o despegue cuidadosamente disimulada**.

El jugador deberá percibir que entra o sale realmente de la nave, aunque técnicamente no exista continuidad geométrica entre el hangar interior y el casco exterior.

Esta solución permite construir hangares propios de gran calidad sin depender de que los modelos 3D descargados de las naves ya los incorporen, ni tener que recortar y reconstruir cascos complejos para insertarlos.

**Principio rector: separación técnica de escenarios, continuidad narrativa y funcional para el jugador.**

## 2. Motivación y problema que resuelve

En el proyecto existen modelos exteriores de distintas clases de naves. Algunos, como la **Sovereign mejorada de la Misión 07**, incorporan un hangar 3D original; otros modelos, como los de las clases **Galaxy** u **Odyssey** actualmente considerados, no incluyen uno aprovechable.

Incrustar un hangar completo en un casco ya terminado implica problemas de topología, escalas, UV, materiales, recortes estructurales, compatibilidad con detalles originales y posibles daños visuales. Además, obliga a limitar el diseño interior a lo que admita el modelo exterior obtenido.

El sistema propuesto evita convertir esa integración geométrica en un requisito para que existan hangares jugables. Los interiores podrán diseñarse **a nuestra manera**, con ambición visual y funcional, mientras el exterior conserva su geometría siempre que sea posible.

No se pretende que todos los hangares sean iguales: **el método técnico será común, pero su diseño, tamaño y equipamiento dependerán de cada clase y, cuando proceda, de cada nave concreta**.

## 3. Libertad para diseñar distintos hangares

El sistema admitirá desde pequeñas bahías para una o dos lanzaderas hasta grandes hangares principales capaces de albergar numerosos vehículos, personal, equipos y zonas operativas.

### Ejemplos de aplicación

- **Clase Galaxy / Enterprise-D:** gran hangar principal independiente, de diseño amplio, curvo o aproximadamente circular según referencias y decisiones artísticas; múltiples plazas de lanzaderas, zonas de movimiento, control de operaciones, personal técnico, pasarelas, almacenes y acceso por turboascensor. Su tamaño y arquitectura no estarán restringidos por la malla exterior descargada.
- **Clase Odyssey / Enterprise-F:** hangar o conjunto de hangares propios, acordes con una nave de gran tamaño, sin necesidad de integrarlos físicamente en el casco exterior.
- **Naves pequeñas o medianas:** bahías compactas, con menos capacidad y circulación simplificada, sin perder funcionalidad.
- **Clase Sovereign:** caso especial que ya dispone de un hangar físicamente modelado en el exterior. Se priorizará conservar y hacer funcional esa integración real, sin impedir que utilice el mismo sistema general de atraque, inventario y persistencia.
- **Otras clases y futuras naves:** podrán utilizar el mismo mecanismo híbrido con interiores específicos, variantes de un módulo base o hangares compartidos entre naves de una misma clase cuando resulte apropiado.

Los interiores se crearán modularmente, **pieza a pieza**, siguiendo el método acordado para Blender: arquitectura básica, puertas, plataformas, zonas de atraque, pasarelas, consolas, mobiliario, materiales PBR, luces y detalles operativos. Cada etapa deberá poder revisarse visualmente antes de seguir.

## 4. Tres modalidades de integración

Las tres opciones deben coexistir bajo una misma lógica de juego y persistencia:

| Modalidad | Descripción | Uso previsto |
|---|---|---|
| **A — Integración física** | Hangar situado geométricamente dentro del modelo exterior, con entrada y salida continuas si el activo lo permite. | Sovereign con hangar original y futuras naves preparadas expresamente. |
| **B — Integración híbrida** | Hangar interior 3D independiente y acceso exterior representado mediante puertas, marco o un pequeño tramo de profundidad. La transición se oculta en el umbral. | **Opción recomendada para Galaxy, Odyssey y otras naves sin hangar integrado.** |
| **C — Atraque simulado** | La secuencia aproxima la lanzadera a una zona exterior coherente y realiza el cambio a un hangar interior sin mostrar un paso físico por las puertas. | Modelos donde modificar el casco no compense, prototipos o naves secundarias. |

**No debe exigirse reconstruir todo el casco para ofrecer una experiencia de embarque y desembarque convincente.** La modalidad puede mejorar con el tiempo sin rehacer el funcionamiento de las lanzaderas.

## 5. Experiencia del jugador: salida del hangar

Ejemplo: el jugador está a bordo de la Enterprise-D y decide utilizar una lanzadera.

1. **Acceso interior.** Desde el puente, camarote u otra dependencia utiliza el turboascensor y selecciona el hangar que corresponda.
2. **Llegada al hangar.** Accede a un espacio 3D completo, explorable, con lanzaderas estacionadas, técnicos, elementos operativos e iluminación propia.
3. **Selección de lanzadera.** Embarca en una unidad realmente disponible; se registra quién la utiliza y con qué autorización.
4. **Preparación.** Se confirma la ruta, el estado de puertas, la autorización de control de vuelo y la disponibilidad del pasillo de salida.
5. **Apertura interior.** La compuerta del hangar se abre y se muestra la maniobra de aproximación a la salida. Si el interior tiene un tramo de acceso, podrá aprovecharse para crear profundidad.
6. **Transición disimulada.** Justo cuando la lanzadera atraviesa la zona del umbral, una combinación de cámara, encuadre, iluminación o corte cinematográfico breve permite cargar o activar la escena espacial y colocar el vehículo en su posición exterior correcta.
7. **Continuación exterior.** La misma lanzadera aparece junto al casco, cerca de la posición donde estaría la puerta real, manteniendo rumbo y velocidad de forma visualmente coherente. El jugador puede tomar el control o continuar en automático.

**Lo único que se oculta es el cruce físico entre dos escenarios que no están conectados geométricamente.** La experiencia anterior y posterior a ese instante debe resultar continua y creíble.

## 6. Experiencia del jugador: regreso y atraque

1. La lanzadera se aproxima a la nave a **escala física coherente**; la diferencia de tamaño entre un pequeño vehículo auxiliar y una nave capital debe resultar impresionante.
2. Se solicita permiso de atraque. Control de vuelo comprueba autorización, estado de la bahía y plazas disponibles.
3. El piloto automático, si se utiliza, dirige la lanzadera hacia el acceso exterior correspondiente mediante puntos definidos **relativamente a la nave nodriza**, incluso si esta se desplaza o gira.
4. Las puertas exteriores podrán **simular su apertura**. Cuando sea viable, se mostrará un pequeño vestíbulo, túnel o tramo iluminado de entrada, sin necesidad de construir el hangar completo detrás.
5. En el momento de atravesar visualmente el umbral, se efectúa una **transición cinematográfica encubierta**: cambio controlado de cámara, corte breve, oclusión por el marco/compuerta o recurso equivalente.
6. El vehículo aparece **ya entrando en el hangar interior independiente**, no necesariamente estacionado: podrá continuar un tramo de vuelo lento, alinearse y aterrizar suavemente en su plaza.
7. Finalizado el atraque, se cierran las puertas, se confirma la ocupación de la plaza y el jugador puede desembarcar y desplazarse al resto de la nave.

La reentrada **no tiene por qué resolverse con una teletransportación visible ni con una pantalla de carga explícita**. La calidad de la ilusión depende de encadenar bien posiciones, orientación, sonido, cámaras, luces y ritmo. No se promete ausencia absoluta de cargas: deberá evaluarse técnicamente en Unreal Engine 5.

### Variantes de presentación

- **Secuencia completa automática:** desde solicitud de atraque hasta aterrizaje.
- **Aproximación manual + acoplamiento asistido:** el jugador vuela hasta un volumen de entrada seguro y el sistema toma el control en la maniobra delicada.
- **Transición abreviada:** opción para evitar repetir secuencias largas después de muchas misiones.
- **Cámara exterior o interior:** el sistema no debe depender de que la lanzadera tenga una cabina 3D detallada. Se podrá utilizar cámara exterior o interfaz de vuelo si el interior todavía no existe o no alcanza la calidad deseada.

## 7. Puertas y fachada exterior del hangar

Para las modalidades híbrida y simulada **no hace falta abrir un hueco completamente transitable en el casco exterior**.

Cuando merezca la pena, se construirá un **módulo exterior de acceso** adaptado a cada clase de nave: compuerta, marco, luces de guía y una profundidad aparente suficiente para que la transición no resulte brusca. Esta fachada podrá ser una modificación localizada y controlada del exterior, sin modelar todo el interior detrás.

Si el casco exterior carece de un hueco apropiado o abrirlo genera demasiado riesgo, se elegirá un encuadre o transición que evite mostrar una abertura imposible. **No se debe fingir que unas puertas se abren físicamente si el modelo continúa siendo un casco sólido detrás de ellas y el fallo resulta visible.**

Las puertas deberán respetar estados operativos: cerradas, abriéndose, abiertas, cerrándose, bloqueadas o averiadas. La lógica de acceso debe impedir entradas cuando la bahía no esté disponible.

En la **Sovereign M07**, la preparación de unas puertas reales y operativas en el hangar ya integrado se reserva a la **Misión 08**, en copia del modelo, protegiendo la arquitectura existente.

## 8. Persistencia absoluta de lanzaderas, tripulantes y carga

La separación visual entre escenarios **no permite duplicar vehículos ni alterar su estado**.

Cada lanzadera será una entidad persistente con identidad única y datos propios. El simulador del RPG conservará, como mínimo:

- Identificador de la lanzadera y nave propietaria o asignación actual.
- Ubicación lógica: hangar concreto y plaza, espacio exterior, estación, planeta, otro vehículo o estado de tránsito.
- Estado operativo: disponible, en preparación, en vuelo, aterrizando, acoplada, dañada, inmovilizada, desaparecida o destruida, según los estados definitivos del sistema.
- Piloto, pasajeros, tripulación, carga y equipamiento.
- Combustible/energía, daños, mantenimiento y demás atributos que se definan para los vehículos auxiliares.
- Reserva u ocupación de plaza y permisos de salida/entrada.

**Regla innegociable: una lanzadera no puede estar en dos lugares a la vez.** Si ha salido de la Enterprise-D, su plaza queda libre y no debe seguir apareciendo como objeto estacionado en el hangar. Si atraca, deberá encontrarse allí cuando el jugador regrese caminando.

El cambio de escenario debe trasladar **la representación visual**, no crear un vehículo nuevo. Las transiciones de estado se consolidarán únicamente cuando la maniobra alcance el punto correspondiente, con mecanismos de recuperación ante interrupciones o errores.

### Ejemplo de continuidad narrativa

Si el jugador parte en lanzadera hacia un planeta y después muere, es capturado o abandona el vehículo, **el juego no debe devolverla automáticamente al hangar sin justificación**. Su destino dependerá de las reglas de simulación y de lo que realmente suceda: puede quedar en el planeta, recuperarla un NPC, regresar mediante pilotaje automático si sus sistemas y circunstancias lo permiten, requerir una misión de rescate o considerarse perdida.

Lo mismo se aplica si el jugador es transportado desde otro lugar, cambia de nave o deja a un compañero al mando de la lanzadera. El hangar debe reflejar la situación real del universo persistente, no una decoración fija.

## 9. Escala, navegación y seguridad

La espectacularidad de la aproximación depende de respetar **las dimensiones y proporciones reales adoptadas para cada clase de nave y vehículo**. No se debe escalar una lanzadera para que «quepa» visualmente a costa de romper la coherencia del universo.

Antes de preparar el vuelo jugable se comprobarán:

- Escala validada de casco exterior, acceso, hangar, lanzadera y personajes.
- Tamaño útil de la abertura o del corredor visual que represente el acceso.
- Puntos de espera, aproximación, cruce de umbral y estacionamiento.
- Colisiones, obstáculos, movimiento de puertas y trayectorias seguras.
- Número real de plazas y su ocupación.
- Comportamiento si la nave nodriza está moviéndose, maniobrando o sufriendo una emergencia.
- Posibilidad de cancelar una maniobra y retornar a una posición segura.

El piloto automático no deberá atravesar geometría por comodidad ni conceder permisos de atraque cuando la puerta, plaza o bahía no estén disponibles.

## 10. Arquitectura técnica prevista

La implementación deberá mantener separadas, pero coordinadas, tres responsabilidades:

**A. Simulación persistente (CoreRPG y reglas Star Trek).** Decide dónde está cada vehículo, quién lo ocupa, qué autorizaciones tiene, si puede volar o aterrizar y cuál es el resultado de cada maniobra. La persistencia es independiente de que el hangar esté cargado visualmente.

**B. Escenarios 3D (Unreal Engine 5).** Representa el exterior de la nave, los interiores de sus hangares, las lanzaderas y la iluminación. Puede activar, cargar o descargar los escenarios que correspondan según la situación.

**C. Controlador de transición de atraque/despegue.** Coordina animaciones de puertas, rutas de aproximación, cámaras, efectos, sincronización entre escenarios, posición relativa a la nave nodriza y confirmación de los cambios de estado.

Se recomienda que el **sistema de atraque sea común para todas las clases** y que cada clase proporcione sus propios datos de presentación: modelo de hangar, accesos, plazas, puertas, rutas, reglas y modalidades disponibles.

Esta es una **arquitectura conceptual**, no un diseño de API aprobado ni una afirmación de que CoreRPG ya dispone de todos los componentes necesarios. Su encaje exacto deberá revisarse cuando corresponda en las fases de Actions/Simulation y en la planificación del juego.

## 11. Reutilización sin perder la identidad de cada nave

El objetivo no es crear manualmente un sistema de vuelo nuevo por cada hangar, sino **crear hangares distintos que funcionen mediante reglas comunes**.

- Las naves de una misma clase pueden reutilizar la arquitectura de hangar base con variaciones de señalización, plazas, equipamiento y estado.
- Clases distintas podrán utilizar tamaños y distribuciones completamente diferentes.
- Una nave concreta podrá tener un hangar modificado o una configuración especial sin alterar el modelo de datos del resto de la flota.
- Lanzaderas y otros vehículos auxiliares serán **activos 3D independientes**. Su presencia en el hangar dependerá de la simulación, no de geometría decorativa fija.
- Los interiores podrán mejorarse progresivamente —arquitectura, PBR, luces, consolas, personal, animación— sin rehacer el sistema de atraque.

Este criterio también admite hangares de estaciones espaciales si sus requisitos son compatibles, aunque el alcance inicial se centra en naves estelares.

## 12. Riesgos y límites reconocidos

1. **Desajustes visuales entre exterior e interior:** resolver mediante compuertas, marcos, tramo de transición, encuadre y puntos de referencia coherentes.
2. **Saltos de posición o cámara:** comprobar alineación, rumbo, velocidad aparente, escala, iluminación y sonido durante el cambio de escenario.
3. **Cargas perceptibles:** estudiar precarga/streaming y mantener una transición cinematográfica breve si fuera necesario.
4. **Colisiones y plazas incompatibles:** validar dimensiones y circulación antes de ofrecer maniobras automáticas.
5. **Pérdida o duplicación de vehículos:** centralizar la entidad y sus estados; no asociar la existencia del vehículo a que esté visible en una escena.
6. **Trabajo artístico descontrolado:** construir interiores por módulos y aprobar visualmente cada etapa.
7. **Modelo exterior sin puerta real:** utilizar un acceso visual limitado o transición totalmente simulada, sin prometer continuidad geométrica inexistente.

## 13. Desarrollo incremental propuesto

**Etapa 1 — Definir el sistema común.** Documentar estados, reglas de disponibilidad, estructura de hangares, plazas, puntos de acceso y modalidades de transición.

**Etapa 2 — Prototipo con una nave y una lanzadera.** Crear un hangar interior separado sencillo, una escena exterior y una transición reversible. Comprobar que la misma entidad entra, sale y conserva su ubicación.

**Etapa 3 — Refinar la ilusión.** Añadir autorización de control de vuelo, piloto automático básico, puertas visuales, sonido, cámaras y aterrizaje suave.

**Etapa 4 — Primer gran hangar artístico.** Construir modularmente el hangar principal de la **Galaxy / Enterprise-D**, con el nivel de detalle que se vaya aprobando.

**Etapa 5 — Extensión por clases.** Incorporar Odyssey y otros diseños, ajustando escala, tamaño, capacidad y accesos, reutilizando los sistemas ya probados.

**En paralelo:** la Sovereign con hangar original podrá evolucionar hacia integración física real, comenzando por la Misión 08 de puertas. Ambos caminos deben compartir la misma persistencia y lógica de operaciones.

Ninguna de estas etapas se considera ejecutada por la aprobación de esta idea.

## 14. Criterios para dar la idea por implementada

- El jugador puede llegar a un hangar interior 3D propio de su nave y encontrar los vehículos que realmente están asignados y presentes.
- Una lanzadera puede despegar y aparecer fuera de la nave mediante una transición visual coherente, sin exigir un hangar geométricamente integrado.
- Puede regresar desde el exterior y completar una maniobra de aterrizaje dentro del hangar independiente.
- Las puertas, autorizaciones y rutas presentan un comportamiento creíble, aunque algunos accesos sean simulados.
- La escala de las naves y lanzaderas se mantiene consistente.
- La lanzadera conserva su identidad, posición lógica, tripulación, carga, daños y demás estados durante las transiciones.
- No se producen duplicados ni vehículos que reaparezcan mágicamente.
- El sistema admite hangares grandes, medianos y pequeños sin implementar otro controlador específico desde cero.
- La modalidad integrada de la Sovereign y la modalidad híbrida de la Galaxy pueden coexistir.
- El aspecto visual mantiene un nivel de calidad suficiente para que el corte de escenario no rompa la inmersión.

## 15. Decisión de diseño

**Se aprueba conceptualmente la creación de hangares 3D independientes, adaptados a cada clase o nave, con maniobras simuladas de entrada y salida mediante transiciones cinematográficas.**

La integración física del hangar en el modelo exterior **será una mejora opcional, no una condición necesaria para la jugabilidad**.

Este enfoque libera el diseño artístico de los hangares, permite utilizar modelos exteriores de naves que carecen de interiores, reduce el riesgo de modificar geometría compleja y conserva los elementos esenciales del RPG: escala, inmersión, procedimientos de vuelo y persistencia real de vehículos y tripulación.

**Idea relacionada, pero separada:** acceso y desacople simulado del *yate del capitán* mediante una transición equivalente; deberá documentarse como propuesta propia, no confundirse con el sistema de hangares convencionales.


---

## 16. Registro en el Plan Maestro y compatibilidad técnica (auditoría al archivar)

**Fecha de registro:** 2026-10-11. **Identificador:** `IDEA-0003`. El documento original del autor se conserva en los apartados 1–15; este apartado solo agrega trazabilidad y dependencias de planificación.

- **F02 — Arquitectura e integración:** definir interfaces entre Core RPG (estado y acciones), reglas de Star Trek (hangar, permisos, plazas y lanzaderas) y UE5 (renderizado y transiciones), validando capacidades realmente disponibles sin suponer APIs terminadas.
- **F03 — Mundo y persistencia:** asegurar identidad de la lanzadera, localización única, ocupantes, carga, estado de maniobra y consistencia al guardar/cargar, incluidos fallos o interrupciones a mitad de una transición.
- **F04 — Naves y dotaciones:** integrar capacidades de hangares y tripulación a los perfiles de nave que corresponda; verificar qué plazas, vehículos, servicios y personal existen en cada instancia de nave.
- **F07 — Pipeline 3D/UE5:** mallas, escala, accesos, puertas, interiores, streaming de niveles, cámaras, colisiones y pruebas de transición. La prioridad del puente piloto no cambia por esta idea.
- **F09 — Consolas:** reutilizar la familia funcional `flight_deck` ya catalogada; desarrollar sus procedimientos de salida/entrada cuando llegue su fase.
- **F11 — Flota jugable:** asignar capacidades de bahía por clase/configuración y conservar la continuidad de vehículos al cambiar de destino o nave.
- **F14 — Producción audiovisual:** modularidad Blender, materiales PBR, efectos, sonidos, optimización y procedencia/licencias de modelos.
- **F15 — QA:** cubrir pruebas de reversibilidad, cancelación, carga/guardado, saturación de plazas, nave nodriza en movimiento y ausencia de duplicación.

### Material del repositorio a reutilizar

- [Plan Maestro F00–F15](../docs/roadmap/master/PLAN_MAESTRO.md).
- [Familias de consolas: `flight_deck`](../../sistemas/gameplay/ship_operations/consoles/README.md).
- [Hangar/Lanzaderas — estado actual](../../sistemas/gameplay/ship_operations/consoles/flight_deck/README.md) (detalle funcional pendiente).
- [Flujo de atraque de instalaciones](../../sistemas/gameplay/facilities/docking_service_flow.json): referencia de secuencias/seguridad **que requiere adaptación**, no sustituye al flujo específico de lanzaderas.
- [Validaciones de atraque y soporte](../../desarrollo/validation/consistency/docking_maintenance_support_rules.md).
- [F07 — Pipeline 3D](../docs/roadmap/master/fases/F07/README.md).
- [F11 — Carrera y flota](../docs/roadmap/master/fases/F11/README.md).
- [Buzón de ideas](BUZON.md).

### Comprobaciones pendientes antes de implementar

1. **Modelos y versiones:** confirmar en los activos Blender/UE5 correspondientes el estado real del hangar de la Sovereign M07 y la planificación M08; el archivo adjunto los da como antecedentes, **no como comprobaciones de ejecución realizadas en esta auditoría**.
2. **Geometría y escala:** mantener dimensiones físicas, acceso aparente, plazas y maniobras compatibles con la clase, sin forzar la inclusión geométrica del hangar en el casco exterior.
3. **Consistencia transaccional:** separar `vehículo persistente` de `actor visual`; fijar puntos de confirmación y recuperación de maniobras interrumpidas antes de construir la secuencia definitiva.
4. **Continuidad de tripulantes y cargas:** la transición visual no debe crear, borrar ni trasladar arbitrariamente entidades fuera de lo decidido por el sistema autoritativo.
5. **Alcance:** el yate del capitán queda expresamente **fuera** de IDEA-0003 y deberá registrarse como idea independiente cuando se gestione.

**Registro administrativo, no implementación:** IDEA-0003 aprobada conceptualmente. No se abren fases nuevas ni se altera el alcance de la Guardia de Sensores v0.0.1.

## Actualización de dependencia — 2026-10-17

La [IDEA-0004 — Yate del capitán](IDEA-0004_yate_del_capitan_desacople_simulado.md) está **DESCARTADA**. Su sustituta para Valhalla es [IDEA-0010 — Nave auxiliar táctica furtiva](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md), que reutiliza **este sistema de transición simulada**: no necesita cavidad física ni hangar real y se accede directamente desde el puente principal de Valhalla mediante turboascensor al interior 3D independiente de la nave tipo Defiant. La salida/reacoplamiento se representan por anclaje virtual con continuidad/persistencia, sin mezclar identidades de vehículos.
