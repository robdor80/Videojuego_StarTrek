# IDEA-0004 — Yate del capitán: acceso interior, desacople simulado y vehículo auxiliar persistente

**Proyecto:** Videojuego Star Trek RPG 3D  
**Área:** Naves capitales · Vehículos auxiliares · Puente/interiores · Vuelo espacial · Transiciones · Persistencia  
**Fecha:** 11 de octubre de 2026  
**Estado vigente (17-10-2026):** **DESCARTADA / SUSTITUIDA por IDEA-0010**. La documentación antigua se conserva como archivo histórico y no constituye una propuesta activa de yate para ninguna nave.  
**Destino:** `/ideas` del repositorio del videojuego Star Trek  
**Nave de referencia inicial:** Clase **Sovereign**, basada en la Sovereign con hangar mejorada en M07.  
**Actualización de continuidad (2026-10-13):** la nueva Gran Dama es **Clase Valhalla**, inspirada en **Galaxy**, y **no** una evolución de la Sovereign M07. Este yate nació como concepto para Sovereign; podrá evaluarse para Valhalla por separado, **sin confirmar** que ya exista un alojamiento de yate compatible.

---

## 1. Idea principal

Incorporar al RPG un **yate del capitán** (*Captain's Yacht*): una embarcación auxiliar exclusiva, diferenciada de las lanzaderas convencionales, que el jugador pueda utilizar para visitas oficiales, desplazamientos, misiones diplomáticas, exploración y otras situaciones adecuadas.

El concepto inicial del yate se ha preparado para la **clase Sovereign** y el modelo M07. La **Clase Valhalla es otra clase nueva, inspirada en Galaxy**; el sistema genérico del yate podrá adaptarse a esa nave u otras compatibles **si se aprueba y se comprueba su integración**, sin rehacer la persistencia y el control de accesos.

**No será necesario modelar desde el principio una operación físicamente continua de desacople o acople entre el yate y el casco exterior de la nave nodriza.** Igual que con los hangares independientes, podremos representar el proceso mediante **acceso interior + secuencia cinematográfica + transición controlada al escenario espacial**.

El jugador debe percibir que ha embarcado en una nave auxiliar real y ha partido desde su nave nodriza, aunque no contemple el recorrido geométrico completo a través de la sección de acoplamiento.

**Principio rector: un vehículo persistente y funcional, con una transición visual convincente; el desacople físico detallado es una mejora futura, no un bloqueo de la jugabilidad.**

## 2. Origen de la idea y referencia estética

El concepto parte del **yate del capitán de la Enterprise-E**, asociado a la clase Sovereign, que inspira un vehículo pequeño frente a una nave capital, pero mucho más refinado y representativo que una lanzadera de servicio.

La intención artística es que el jugador sienta que viaja en **la embarcación personal/oficial del mando**, con una presentación elegante y un carácter propio. Podrá tomarse como referencia el yate **Cousteau**, sin obligarnos a reproducir un modelo concreto si no encontramos un activo 3D de calidad suficiente.

**Nota de precisión:** la referencia recordada a una excursión planetaria con un vehículo todoterreno procede de recuerdos de una película y **no se utiliza como requisito canónico de esta idea**. El sistema debe definirse por su función jugable, no por atribuir sin verificación esa secuencia al yate.

No se considera aprobada todavía una malla, matrícula, configuración interior o diseño final del vehículo.

## 3. Motivo para usar un desacople simulado

El modelo Sovereign M07 conserva en la zona ventral del platillo una estructura que visualmente **podría corresponder a la zona del yate del capitán**. Esa identificación y la posibilidad de utilizarla mecánicamente todavía deben verificarse sobre la geometría real.

Convertir directamente esa zona del casco en un mecanismo físico exigiría, entre otras tareas:

- Identificar y separar con precisión las partes correspondientes al yate y a su alojamiento.
- Reconstruir superficies ocultas, puntos de acople y mecanismos de apertura.
- Preparar pivotes, animaciones y colisiones evitando atravesar el casco.
- Garantizar escalas y posiciones compatibles entre el yate exterior y la nave nodriza.
- Coordinar entrada/salida del jugador, despegue y vuelo relativo a una nave que puede estar moviéndose.

Nada de ello es imposible, pero **no justifica paralizar el desarrollo del sistema de viaje en yate** hasta completar una intervención geométrica de alto riesgo.

La solución híbrida permite trabajar antes en el propio vehículo, sus funciones y su presentación, manteniendo intacta la Sovereign que ya hemos conseguido mejorar.

## 4. Experiencia del jugador: embarque y salida

Ejemplo: el jugador se encuentra a bordo de nuestra Sovereign y tiene autorización para utilizar el yate.

1. **Decisión de viaje.** Desde el puente, el camarote o cualquier área comunicada con los accesos internos, el jugador decide embarcar en el yate.
2. **Acceso mediante turboascensor.** Selecciona el destino **«Yate del capitán»** o la denominación final del área de embarque.
3. **Zona de acceso exclusiva.** Aparece en una antesala o módulo específico que representa el acceso al yate. En una primera versión podría bastar una transición directa al puesto de control; una versión avanzada dispondrá de interior 3D explorable.
4. **Embarque real en el sistema de juego.** El estado persistente registra qué yate utiliza, ocupantes, tripulación autorizada, carga y condiciones del vehículo.
5. **Preparación de salida.** Se solicitan comprobaciones y autorización de desacople. La computadora o control de vuelo informa de la disponibilidad.
6. **Inicio de secuencia.** Sonidos de liberación de amarres, pequeñas vibraciones, iluminación de cabina, vista de una compuerta o un plano cinematográfico breve disimulan el salto entre escenarios.
7. **Transición al exterior.** El yate aparece **junto al punto del casco donde razonablemente estaría acoplado**, con orientación, distancia de seguridad y velocidad relativa coherentes.
8. **Separación suave.** El piloto automático completa una maniobra de alejamiento controlado. A continuación el jugador puede asumir el mando, mantener el automático o pasar a su interfaz de vuelo.

**Lo que no se muestra necesariamente es el instante físico exacto en que el vehículo se libera del alojamiento del casco.** Todo lo anterior y posterior debe mantener continuidad narrativa y espacial.

### Presentación opcional más avanzada

Cuando tengamos geometría de calidad suficiente podremos mostrar una cubierta de acceso, un interior de lujo o un breve plano exterior de desacople. Estos recursos enriquecerán la escena **sin cambiar las reglas ni la identidad persistente del yate**.

## 5. Experiencia del jugador: regreso y acoplamiento

1. El yate se aproxima a la nave nodriza, respetando las escalas reales adoptadas para ambos vehículos.
2. El jugador solicita permiso de acoplamiento o activa una aproximación autorizada.
3. El piloto automático alinea el vehículo con una **zona de atraque propia del yate**, distinta de las puertas de los hangares convencionales.
4. Si existe un mecanismo exterior representable, se muestra su activación; si no, se utilizan cámara, oclusión del casco, sonido y una transición cinematográfica breve.
5. En el punto adecuado se cambia desde la escena espacial al estado **yate acoplado / acceso interior**.
6. El jugador puede desembarcar por la antesala o volver a otra cubierta mediante turboascensor.
7. El simulador confirma el acoplamiento, actualiza la disponibilidad del yate y mantiene la información de ocupantes, carga, daños y mantenimiento.

El regreso debe ser **reversible y coherente**, sin apariciones arbitrarias ni pérdida de estado. No es necesario enseñar el contacto mecánico exacto entre ambas mallas si todavía no está preparado.

## 6. Tres niveles posibles de realización

| Nivel | Qué se representa | Uso |
|---|---|---|
| **A — Simulación básica** | Acceso narrativo o por turboascensor, breve transición y yate controlable en el espacio. Regreso equivalente. | Primera versión funcional, con el menor riesgo artístico y técnico. |
| **B — Presentación híbrida** | Antesala o interior 3D parcial, efectos de desacople y zona exterior de acoplamiento visualmente preparada, ocultando el cruce físico. | **Objetivo visual recomendado** a medio plazo. |
| **C — Desacople físico completo** | Yate extraíble, alojamiento real en el casco, puertas/paneles animados y trayectoria continua. | Posible mejora futura, únicamente si la geometría y el esfuerzo lo justifican. |

La modalidad elegida **no debe cambiar el vehículo que existe en la simulación**: es una diferencia de presentación y de interacción visual.

## 7. Modelo 3D del yate: selección o construcción

Antes de crear el vehículo desde cero se buscará **un modelo 3D existente de Star Trek** que pueda dar el pego como yate de la Sovereign y, posteriormente, de nuestra nueva clase.

Criterios de selección:

- **Silueta elegante y distinguible**, no simplemente otra lanzadera de carga.
- **Coherencia estilística** con la Sovereign y con el acabado final del juego.
- **Escala plausible** frente al casco, las cubiertas y los personajes; dimensiones a validar, no inventadas.
- Buenas mallas, UV, texturas y materiales PBR.
- Posibilidad de limpiar matrículas y personalizar nombre e identidad.
- Preferentemente con interior o elementos desmontables, aunque **no será obligatorio para la primera versión**.
- Formatos manejables por Blender y exportables a Unreal Engine 5.
- Procedencia y **licencia de uso** documentadas.

Si encontramos un exterior excelente sin interior, podrá utilizarse igualmente. No debemos sacrificar el acabado visual por intentar mostrar una cabina insuficientemente trabajada.

**La selección del modelo queda pendiente.** No se aprueba automáticamente ningún activo descargado.

## 8. Interior del yate: aspiración artística, no condición inicial

Se desea que el yate llegue a transmitir un ambiente **más lujoso, cómodo y exclusivo** que una lanzadera normal. Según el vehículo elegido y las dimensiones disponibles, podría incluir:

- Dos o más puestos de pilotaje o navegación.
- Consolas de vuelo, comunicaciones y sensores.
- Asientos de pasajeros o zona de reunión.
- Materiales de calidad, superficies limpias, iluminación suave y pantallas funcionales.
- Acceso interior, puertas y otros elementos coherentes con su volumen exterior.

**No se construirán de golpe interiores completos sin validación visual.** Se seguirá el método modular que estamos adoptando para Blender: volumen base → accesos → mobiliario grande → consolas → materiales PBR → iluminación → detalles → interacción.

Si no conseguimos un interior satisfactorio en una fase temprana, el yate seguirá siendo totalmente utilizable mediante:

- **Cámara exterior en tercera persona**.
- **Interfaz de pilotaje** con visión exterior, sensores, navegación y comunicaciones.
- Transiciones de embarque y desembarque sin mostrar una cabina de baja calidad.

Un eventual interior 3D completo será una ampliación artística; la lógica de vuelo y las misiones no deberán depender de él.

## 9. Rol del yate frente a las lanzaderas convencionales

El yate debe tener una **identidad y un propósito diferenciados**, sin volverse mágicamente superior en todos los aspectos.

Usos posibles:

- Viajes oficiales del capitán o personal autorizado.
- Misiones diplomáticas y transporte de representantes o visitantes importantes.
- Visitas a planetas, bases y estaciones.
- Desplazamientos en misiones de representación o exploración adecuada a sus capacidades.
- Ocasiones narrativas especiales vinculadas al mando de una nave capital.

No se asume que disponga por defecto de más armamento, más velocidad o mejores sensores que cualquier lanzadera. Sus características reales deberán definirse al seleccionar o diseñar el vehículo.

El sistema no debe conceder automáticamente al jugador **rango de capitán ni acceso irrestricto** al yate: eso dependerá de su puesto, sus autorizaciones y las decisiones de mando dentro de la carrera RPG.

## 10. Persistencia: una sola entidad, esté donde esté

Este apartado es **obligatorio** y comparte principios con la idea de los hangares independientes.

Cada yate será una **entidad única y persistente**, no un elemento decorativo que aparece siempre que entramos en el turboascensor.

El juego conservará como mínimo:

- Identificador del yate y nave a la que está asignado.
- Estado lógico: acoplado, preparándose, desacoplando, en vuelo, aterrizado, estacionado, averiado, perdido o destruido, según el catálogo final.
- Ubicación actual, incluida la zona de acoplamiento exacta o el lugar exterior en el que se encuentra.
- Piloto, pasajeros, tripulación a bordo, autorizaciones y responsables.
- Carga, suministros y equipamiento.
- Energía, daños, reparación y cualquier otra propiedad de vehículos auxiliares que se establezca.
- Orden o misión activa, si procede.

**Regla innegociable: el yate no puede estar a la vez acoplado a la Sovereign y volando por el espacio.**

Si el capitán lo utiliza para viajar a un planeta, seguirá allí hasta que exista una razón simulada para su retorno: por ejemplo, que lo pilote un NPC autorizado, que pueda regresar en automático, que se recupere posteriormente o que quede abandonado. Si el jugador muere, es transportado a otra nave o cambia de destino, **el yate no debe teletransportarse gratuitamente a su punto de origen**.

### Coherencia con el modelo visual del casco

Si el modelo exterior de la Sovereign incluye una forma que representa el yate permanentemente acoplado, hay que **evitar que parezca existir otro yate idéntico a la vez en el espacio**.

Posibles soluciones escalables:

1. Separar o controlar visualmente esa pieza de la nave nodriza cuando resulte viable.
2. Preparar una variante o máscara para estados acoplado/desacoplado sin dañar el casco.
3. En una primera etapa, utilizar encuadres y presentación que no exhiban una contradicción evidente mientras se prepara la mejora geométrica.

No se modificará la zona ventral M07 sin un análisis específico: **el yate funcional debe existir en la simulación aunque su alojamiento físico todavía no esté animado**.

## 11. Escala, acoplamiento y vuelo alrededor de la nave

El yate deberá respetar la **escala física coherente** con la Sovereign y con la futura clase derivada. La cercanía a una nave capital debe transmitir su tamaño real, igual que acordamos para las lanzaderas.

- El punto de desacople será un **anclaje relativo al casco**, no una coordenada fija del mundo.
- La posición, orientación y velocidad de salida deberán calcularse teniendo en cuenta el movimiento de la nave nodriza.
- El piloto automático deberá separar al yate de la nave con una trayectoria libre de obstáculos.
- La maniobra de regreso tendrá un punto de espera, alineación y un volumen de seguridad.
- Si el yate está acoplado, permanecerá asociado a la nave cuando esta viaje, maniobre o cambie de escena.
- Si no está disponible, averiado o ya está fuera, el turboascensor o el punto de embarque no podrá ofrecerlo como si estuviera acoplado.

Puede existir una secuencia de aproximación visual especialmente cuidada para contemplar el tamaño de la Sovereign, pero no debe imponerse en todos los viajes. Se permitirá una transición abreviada cuando corresponda.

## 12. Integración con el RPG y Unreal Engine 5

Se propone separar tres responsabilidades:

**A. Simulación y persistencia (CoreRPG + reglas Star Trek).** Autoridad para determinar disponibilidad del yate, permisos de acceso, ubicación, ocupantes, daños y resultados de las maniobras.

**B. Representación 3D (Unreal Engine 5).** Casco exterior, modelo del yate, posible interior, antesala, materiales, iluminación, efectos, cámaras y animaciones.

**C. Controlador de transición de acople/desacople.** Coordina autorización, preparación, sonidos, encuadres, cambio entre escenario interior/exterior, posicionamiento relativo y confirmación del estado persistente.

**Reutilizar el mismo principio técnico del sistema de hangares independientes**, pero con reglas propias del acoplamiento del yate. No debe tratarse el yate como una lanzadera estacionada en una plaza normal salvo que su diseño y la nave lo permitan explícitamente.

Esta es una **arquitectura conceptual**. Su encaje concreto con los módulos ya desarrollados de CoreRPG y Unreal se analizará durante las fases de implementación correspondientes; la aprobación de la idea no significa que esas funciones existan actualmente.

## 13. Compatibilidad con Valhalla (decisión creativa del 13-10-2026)

La Sovereign M07 es una **referencia artística propia de este proyecto de yate**, no la base de la nueva Gran Dama. La nave principal futura será de **Clase Valhalla**, clase nueva inspirada en Galaxy. **No está aprobada todavía la implantación de un yate en la Valhalla**, pero el sistema deberá ser adaptable si más adelante se decide incluirlo.

Si se incorpora el yate a Valhalla u otra clase:

- El sistema del yate deberá seguir siendo utilizable.
- El punto de acoplamiento y el aspecto del compartimento podrán cambiar.
- Podrá mantenerse el yate inicial, rediseñarse o sustituirse por otro vehículo compatible con la nueva clase.
- La identidad, autorizaciones y persistencia no dependerán del nombre de la clase ni de una matrícula específica.
- La evolución artística de la nave no debe obligarnos a reprogramar desde cero el sistema de desacople.

**El nombre de clase Valhalla ya está decidido.** Siguen pendientes el diseño definitivo de su alojamiento de yate, el nombre/matrícula de una nave individual y las comprobaciones en Blender/UE5.

## 14. Riesgos y límites

| Riesgo | Medida prevista |
|---|---|
| El yate descargado tiene buen exterior pero mal interior | Usar cámara exterior o consola de vuelo hasta conseguir una cabina satisfactoria. |
| El casco de la Sovereign no permite un desacople geométrico sencillo | Utilizar transición cinematográfica; no forzar modificaciones de alto riesgo. |
| El yate aparece duplicado por una pieza visible en la zona ventral | Gestionar estado visual de acoplado/desacoplado o evitar mostrar una contradicción mientras se prepara la variante de casco. |
| Desajustes de escala o orientación al salir | Validar dimensiones, punto de anclaje, rumbo y desplazamiento relativo. |
| Un acoplamiento automático atraviesa geometría | Validar recorridos, distancias, colisiones y cancelación segura de maniobra. |
| La transición revela cortes, cambios de iluminación o cargas | Utilizar encuadres, sonido, ocultación del umbral y precarga cuando sea posible; no prometer continuidad perfecta de antemano. |
| El jugador pierde el yate por muerte o cambio de escena | Mantener su entidad persistente y resolver su destino mediante reglas del RPG, no por reinicio decorativo. |
| Un personaje sin autoridad utiliza el vehículo | Respetar rango, permisos y situaciones narrativas excepcionales. |
| El diseño nuevo de la clase sucesora altera la posición del acople | Configurar puntos de anclaje y presentación por clase/nave, sin modificar las reglas del vehículo. |

## 15. Desarrollo incremental propuesto

**Etapa 1 — Auditoría y elección del activo.** Confirmar qué representa la estructura ventral de M07, localizar modelos 3D candidatos del yate, estudiar licencias, calidad, dimensiones y posibles interiores. No modificar todavía la nave maestra.

**Etapa 2 — Vehículo independiente y escala.** Preparar en Blender una copia limpia del modelo elegido, sus materiales PBR y una escala coherente. Exportarlo para inspección en Rob3D y posteriormente Unreal.

**Etapa 3 — Desacople/acoplamiento simulado.** Prototipar acceso interior, salida con transición al espacio y regreso reversible, aunque el yate no tenga todavía cabina 3D completa.

**Etapa 4 — Persistencia y autorizaciones.** Integrar estado de acoplamiento, ubicación, tripulantes, permisos, disponibilidad y comportamiento ante cambios de misión, muerte o abandono.

**Etapa 5 — Presentación cinematográfica.** Refinar sonido, cámaras, trayectorias automáticas, efecto de liberación, zona de acople y aproximación suave a la nave nodriza.

**Etapa 6 — Interior artístico del yate, si supera la revisión.** Construcción modular en Blender con aprobación visual de cada parte; panel de vuelo o tercera persona como alternativa válida.

**Etapa 7 — Integración avanzada opcional.** Estudiar variante de casco con pieza móvil y verdadero desacople físico si el valor visual compensa su dificultad.

La Misión 08 ya reservada para la Sovereign corresponde a **las puertas del hangar de lanzaderas**, no a este sistema del yate. Esta idea tendrá su propia planificación cuando se priorice.

## 16. Criterios de aceptación

Se considerará funcional la primera versión de la idea cuando:

1. Exista un modelo de yate independiente, apropiado visualmente y con escala validada.
2. El jugador autorizado pueda acceder a él desde una zona interior de la nave.
3. Pueda salir al espacio mediante una transición convincente, aunque no exista desacople geométrico continuo.
4. Pueda regresar a la zona de acoplamiento mediante aproximación manual o automática, según implementación.
5. El modelo espacial aparezca en la posición y orientación correctas respecto a la nave nodriza.
6. El estado del yate persista al cambiar de escena, misión o personaje.
7. El yate no se duplique ni aparezca simultáneamente acoplado y en vuelo como vehículo activo.
8. Sus ocupantes, carga, autorizaciones, daños y estado operativo no se pierdan durante las transiciones.
9. La experiencia pueda disfrutarse sin interior 3D completo, mediante cámara exterior o interfaz de vuelo.
10. Las mejoras artísticas de Sovereign M07 o una eventual adaptación a Valhalla puedan incorporarse sin rehacer la lógica central.

El interior de lujo completamente transitable y el desacople físico real **son objetivos opcionales de evolución**, no requisitos para declarar funcional el primer sistema.

## 17. Relación con otras ideas y trabajos

- **Idea relacionada:** [IDEA-0003 — Hangares independientes](IDEA-0003_hangares_independientes_atraque_simulado.md). Comparte el principio de separar escenarios, ocultar transiciones y mantener vehículos persistentes.
- **Sovereign M07:** base visual conservada; no modificar directamente el archivo aprobado sin trabajar sobre derivadas.
- **Misión 08 Sovereign:** puertas del hangar de lanzaderas; trabajo independiente del yate del capitán.
- **Sistema de carrera y mando del RPG:** determina quién puede autorizar, utilizar o mandar el yate.
- **Clase Valhalla (base Galaxy):** candidata independiente a incorporar un yate si posteriormente se valida alojamiento, acceso, proporciones y diseño; no se da por aprobada la geometría.

## 18. Decisión de diseño

**Se aprueba conceptualmente introducir un yate del capitán inicialmente vinculado a la clase Sovereign M07, con arquitectura reutilizable para otras clases si corresponde.** La nueva **Clase Valhalla**, derivada artísticamente de Galaxy, **no** nace de Sovereign; su eventual yate exige decisión y estudio propios.

El jugador podrá embarcar desde el interior de la nave y realizar viajes con él mediante **desacople/acoplamiento simulado**, transiciones cinematográficas controladas y un vehículo 3D exterior independiente. No será obligatorio reconstruir ni animar desde el principio toda la sección de acoplamiento del casco.

El yate tendrá **identidad única, ubicación y estado persistentes**, con reglas de disponibilidad y autorización coherentes con el RPG. Se buscará un modelo descargable de calidad antes de considerar modelarlo por completo, y su interior lujoso será una aspiración a desarrollar paso a paso sin sacrificar el estándar artístico del juego.

**Resultado buscado:** sentir que disponemos de una embarcación exclusiva del capitán, que realmente pertenece a nuestra nave, sale de ella, cumple misiones y regresa, aunque por debajo utilicemos dos escenarios separados y una transición visual breve.

**Pendiente de implementación. No altera aún archivos, modelos, código ni repositorios.**

---

## 19. Registro, encaje técnico y trazabilidad (anotación al archivar)

**Registro:** `IDEA-0004` · 2026-10-11 · aprobada conceptualmente según el documento aportado por el autor y su solicitud de archivarla como idea número 4. Los apartados 1–18 conservan la propuesta original; esta sección añade exclusivamente coordinación con el repositorio actual.

### Compatibilidad y reutilización

- [IDEA-0003 — Hangares independientes y atraque simulado](IDEA-0003_hangares_independientes_atraque_simulado.md): comparte transiciones visuales, persistencia, control de maniobra y separación entre el vehículo lógico y su representación; **el yate usa una estación de acoplamiento específica**, no una plaza ordinaria de hangar por defecto.
- [Familias funcionales de consola](../../sistemas/gameplay/ship_operations/consoles/README.md): reutilizar los sistemas de vuelo, navegación, comunicaciones y `flight_deck` que correspondan; no crear un segundo simulador de naves.
- [F02 — Arquitectura e integración](../docs/roadmap/master/fases/F02/README.md) y [F03 — Mundo y persistencia](../docs/roadmap/master/fases/F03/README.md): definir contratos de solicitud/autorización, identidad única, localización, estados y eventos, sin atribuir al Core RPG APIs no verificadas.
- [F04 — Dotación y autoridad](../docs/roadmap/master/fases/F04/README.md): el rango, destino y autorización real gobiernan el acceso al yate.
- [F07 — Pipeline 3D](../docs/roadmap/master/fases/F07/README.md): auditoría de modelos, escala, zona ventral de la Sovereign M07 y transición UE5, siempre sobre derivadas de la malla maestra.
- [F09 — Resto de consolas](../docs/roadmap/master/fases/F09/README.md): reutilización funcional de control de vuelo, sistemas de a bordo y coordinación.
- [F11 — Carrera y flota](../docs/roadmap/master/fases/F11/README.md): elegibilidad, asignación a nave, misiones oficiales, mando y continuidad tras cambios de destino.
- [F14 — Recursos audiovisuales](../docs/roadmap/master/fases/F14/README.md): activos licenciados, sonido, cámaras, efectos y eventual interior de calidad.
- [F15 — QA y distribución](../docs/roadmap/master/fases/F15/README.md): pruebas de transiciones reversibles, save/load, recuperación, presencia visual única, posiciones relativas y no duplicación.
- [Plan Maestro](../docs/roadmap/master/PLAN_MAESTRO.md) y [Buzón de ideas](BUZON.md).

### Observación de canon y estado de la nave base

**Histórico:** al aportar esta idea, su borrador daba por elegida a la Sovereign M07 como base de una clase nueva. **Decisión autoral posterior (12–13-10-2026): la base elegida es Galaxy/Enterprise-D y la clase nueva se llama Valhalla.** Por tanto, toda mención de «futura sucesora de Sovereign» en anotaciones artísticas anteriores es histórica, no un requisito vigente. La ficha Sovereign M07 sigue siendo útil para desarrollar **su propio yate**; adaptar el sistema a Valhalla requiere estudiar su arquitectura por separado. La F01 PR #2 recoge la decisión en su acta.

La identificación de la estructura ventral M07, los supuestos de geometría desmontable, los activos candidatos y el estado de la Misión 08 son antecedentes facilitados en el texto original, **no verificaciones técnicas nuevas realizadas al archivarlo**.

### Reglas de implementación y criterios de seguridad

1. **Una entidad, una localización lógica:** el yate no puede existir simultáneamente como vehículo en vuelo y acoplado, incluso cuando el modelo exterior integre una silueta fija representativa.
2. **La escena 3D no es la autoridad:** el controlador de transición representa lo que autorizan los sistemas de estado/persistencia; gestionar cancelaciones e interrupciones con recuperación segura.
3. **Anclajes relativos a nave nodriza:** evaluar rumbo, velocidad, colisiones, zonas de espera y distancias seguras antes de ofrecer acople/desacople asistido.
4. **Sin atribución automática de mando:** la exclusividad estética del yate no da al jugador permisos de capitán por ser protagonista.
5. **MVP independiente del interior completo:** cámara exterior y consola de vuelo pueden permitir jugabilidad sin mallas interiores de baja calidad.
6. **Sin implementación anticipada:** registrar esta propuesta no modifica automáticamente Core RPG, UE5, modelos de Blender, ni la planificación de fases.

**Estado final:** IDEA-0004 registrada como aprobada conceptualmente, **no implementada** y pendiente de planificación.

---

## 20. CIERRE DE IDEA-0004 — Descartada y sustituida (2026-10-17)

**Decisión posterior y expresa del autor:** «descarta esa idea e implementa en su lugar esta del desafiante». Queda **sin efecto** la elección del **yate clásico del capitán**, tanto como equipamiento de la Clase Valhalla como propuesta de desarrollo activo general.

**Sustitución aprobada:** [IDEA-0010 — Nave auxiliar táctica y furtiva de Valhalla](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md), nave de identidad original inspirada en Defiant y desarrollada a partir de los modelos 3D exterior y puente disponibles, pendientes de auditoría.

Los 19 apartados previos quedan conservados para **trazabilidad histórica y aprovechamiento de principios técnicos generales** (identidad única del vehículo, transiciones, persistencia, autorizaciones y anclajes relativos), pero **NO** significan que el yate sea una opción viva a desarrollar por defecto en Sovereign o Valhalla. La eventual reapertura de un yate tradicional requerirá una nueva decisión del autor.

**No confundir esta decisión documental con ejecución en Blender/UE5/CoreRPG:** no se ha modelado, sustituido físicamente ni instalado todavía la nave nueva.
