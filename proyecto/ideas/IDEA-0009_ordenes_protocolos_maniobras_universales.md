# IDEA-0009 — Sistema universal de órdenes, protocolos y maniobras de naves

**Proyecto:** Star Trek RPG 3D  
**Fecha de aprobación conceptual:** 16 de octubre de 2026  
**Estado:** **IDEA-0009 · APROBADA CONCEPTUALMENTE**, pendiente de planificación técnica, pruebas e implementación  
**Destino oficial:** `/ideas/IDEA-0009_ordenes_protocolos_maniobras_universales.md` en `robdor80/Videojuego_StarTrek`  
**Ámbito:** Navegación, maniobras, decisiones operativas, mando, combate y autonomía de naves  
**Motores y arquitectura:** Unreal Engine 5.8.2 (3D, Windows), módulos específicos de Star Trek y CoreRPG genérico según sus contratos

---

## 1. Visión y principio rector

**Star Trek RPG es, ante todo, una experiencia de vida y servicio a bordo de naves estelares, no un simulador de combate de cazas tipo _Top Gun_.**

El jugador pasa gran parte del tiempo en **interiores**: puente, puestos de trabajo, pasillos, ingeniería, camarotes y demás dependencias. Las vistas exteriores deben existir y ser atractivas, especialmente ante planetas, otras naves, maniobras importantes, combates, aproximaciones, atraques y separación del platillo, pero **no son el modo principal de control**.

**Regla central aprobada:** el jugador expresa **qué quiere conseguir**; la tripulación y los sistemas de la nave determinan y ejecutan **cómo hacerlo** dentro de sus atribuciones, capacidades y reglas vigentes.

- El capitán no debe pilotar manualmente cada giro, frenada o corrección de rumbo.
- Timonel, oficial táctico, operaciones y otros puestos ejecutan tareas de su competencia mediante una simulación real, no una simple respuesta narrativa.
- La ejecución debe ser en torno a un **90 % automática** como aspiración de experiencia de juego; no es una métrica técnica fijada.
- El jugador puede intervenir, modificar, cancelar o especificar procedimientos cuando su puesto y autoridad lo permitan.
- Debe existir la posibilidad de pilotaje directo para puestos o situaciones concretas, **sin imponerlo** al capitán como control habitual.

> **Objetivo:** «Timón, establezca órbita estándar alrededor del planeta» debe bastar para que la nave calcule y ejecute la maniobra, sin pedir al jugador que controle seis ejes de movimiento.

## 2. Dos maneras complementarias de impartir órdenes

### 2.1. Órdenes generales por intención

El jugador indica un objetivo operativo y deja iniciativa a los oficiales o al piloto automático:

- «Ataquen esa nave».
- «Mantenga rumbo y velocidad con el contacto».
- «Iguale rumbo y velocidad con esa nave».
- «Persiga al objetivo» / «Dele alcance».
- «Mantenga distancia de seguridad».
- «Acérquese a la estación y solicite atraque».
- «Sitúe la nave en órbita del planeta».
- «Proteja a la nave científica».
- «Retirada táctica».

El sistema elige los **procedimientos más adecuados**, sujeto a la autoridad, reglas de enfrentamiento, información disponible, condiciones de la nave y órdenes superiores.

### 2.2. Órdenes explícitas de protocolo o patrón

El jugador puede elegir un plan operativo concreto:

- «Ejecuten patrón evasivo [nombre]».
- «Ejecuten protocolo defensivo [nombre]».
- «Patrón de ataque [nombre], objetivo [contacto]».
- «Ejecuten procedimiento de escolta [nombre]».

**Los patrones no son animaciones ni recorridos fijos.** Definen **objetivos, prioridades, restricciones, criterios de terminación y situaciones de interrupción**. El timón y los sistemas tácticos calculan una maniobra diferente según geometría actual, distancias, velocidades, obstáculos, daños y conducta del objetivo.

Un mismo protocolo puede tener resultados distintos en dos encuentros diferentes.

## 3. Naturaleza de los protocolos: planes dinámicos, no coreografías

Cada protocolo deberá describir, como mínimo:

| Campo | Descripción |
|---|---|
| Identificador y versión | ID estable, nombre y revisión del protocolo |
| Categoría | Navegación, aproximación, ataque, defensa, evasión, escolta, retirada, atraque… |
| Propósito | Resultado que se busca, no una ruta pregrabada |
| Precondiciones | Sensores, sistemas operativos, autorización, velocidad, espacio disponible, etc. |
| Prioridades | Distancia, protección de aliados, oportunidad de tiro, conservación de escudos, etc. |
| Restricciones | Seguridad, reglamento, objetivos prohibidos, límites de la clase y reglas de combate |
| Distribución funcional | Timón, táctico, operaciones, ingeniería y mando |
| Adaptación | Cómo reevaluar objetivos ante una maniobra enemiga o nuevos acontecimientos |
| Interrupciones | Nueva orden prioritaria, riesgo de colisión, daños, pérdida del blanco, revocación de autorización |
| Criterio de éxito/fracaso | Cuándo termina o informa de que no puede cumplirse |
| Información comunicable | Estado, progreso, alertas, motivos de cambio o imposibilidad |

**Ejemplo de diseño propio, no presentado como canon:** `TACTIC_FLANQUEO_01` puede intentar mantener una posición ofensiva favorable respecto de un blanco, sin suponer que todas las naves tienen un punto débil trasero. Los sensores deben confirmar lo que se conoce y el protocolo debe adaptarse si el adversario cambia de rumbo.

### Familias iniciales propuestas

**Navegación y operaciones:** ir a coordenadas, adoptar rumbo y velocidad, interceptar, seguir, igualar vector de movimiento, mantener formación/distancia, aproximarse, entrar y mantener órbita, atraque, desatraque, aproximación a hangar, separación y reacoplamiento de secciones.

**Táctica:** evaluación de contacto, postura defensiva, ataque autorizado, flanqueo, fuego a distancia favorable, maniobras evasivas, protección de aliados, interceptación de amenazas, ruptura de contacto, retirada y coordinación de varias naves.

**Los nombres concretos, las secuencias y la lista definitiva quedan pendientes de catálogo y validación.**

## 4. Referencias de Star Trek y criterio de fidelidad

La propuesta se inspira en el empleo de **patrones de ataque, maniobras evasivas, protocolos, órdenes al timonel y órdenes al táctico** mostrados en TNG, DS9, Voyager y películas.

- Se revisarán secuencias audiovisuales y fuentes de referencia para describir **cómo se comportan realmente** las distintas clases y cómo se transmiten las órdenes.
- Se distinguirán **nombres y maniobras canónicos** de patrones diseñados específicamente para nuestro juego.
- No se asignarán definiciones supuestamente canónicas a patrones cuyo funcionamiento no esté explicado en pantalla o en referencias fiables.
- El estilo de combate debe reflejar grandes naves estelares con posiciones de tiro, cobertura, intercambio de fuego, retirada, defensa y coordinación, **no dogfights de cazas como regla general**.
- Las tecnologías ficticias de Star Trek —gravedad artificial y amortiguadores de inercia— permiten giros y maniobras sin reproducir sus efectos sobre toda la tripulación mediante una simulación física estricta.

**Criterio visual:** una lanzadera, una nave mediana y una Galaxy/Valhalla deben tener perfiles claramente diferenciados de aceleración, respuesta de giro, frenado y comportamiento; el realismo buscado es **coherencia con la ficción**, no una simulación orbital exhaustiva de la NASA.

## 5. Sistema universal compartido por TODAS las naves

El mismo motor de navegación y ejecución debe servir para:

1. Nave del jugador, sea cual sea su clase, destino o rango.
2. Naves de la Flota Estelar controladas por NPC.
3. Naves neutrales, civiles, amigas o hostiles.
4. Naves enemigas o especiales (p. ej., un Cubo Borg).
5. Secciones independientes de naves separables, cuando aplique.

**La diferencia entre nave jugadora y NPC reside principalmente en quién emite las órdenes, sus autorizaciones y su política de decisiones; no en dos motores de vuelo distintos.**

Cada nave define mediante datos:

- Clase, dimensiones, masa o inercia de diseño, aceleración, frenado y límites de giro.
- Motores y modos de propulsión disponibles.
- Sensores, comunicaciones, armamento, arcos de tiro, escudos y daños.
- Recursos de energía y estado real de subsistemas.
- Tripulación y roles operativos relevantes.
- Doctrina, misión, perfil del comandante, reglas de enfrentamiento y prioridades.
- Capacidades especiales: ocultación, separación de secciones, adaptación defensiva Borg, etc., si proceden.

**No establecer vulnerabilidades ficticias universales por clase** sin datos de diseño concretos y sin la información que permitan los sensores.

## 6. Cadena funcional de decisión y ejecución

**Entrada de la orden → validación → plan → navegación/combate → ejecución UE5 → retroalimentación.**

1. **Orden o evento:** jugador, capitán NPC, mando de flota, protocolo de emergencia o detección de amenaza.
2. **Autoridad y reglas:** comprobar competencia del emisor, autorizaciones, prioridades y reglas de actuación. Distinguir una **orden de atacar** de la **autorización efectiva para abrir fuego**, si procede.
3. **Percepción:** sensores y comunicaciones aportan contactos, incertidumbre, distancias y datos efectivamente conocidos; las naves no son omniscientes.
4. **Planificador:** escoge estrategia/protocolo y objetivos operativos. Puede usar una máquina de estados y puntuación de alternativas (utility AI) junto con reglas y prioridades.
5. **Coordinadores de puesto:** timón, táctico, operaciones y demás sistemas convierten el plan en acciones factibles y coordinadas.
6. **Controlador universal de movimiento:** calcula en tiempo real orientación, velocidades, interpolaciones/limitaciones dinámicas, persecución, evasión y comprobación de obstáculos.
7. **Ejecutor 3D en Unreal:** actualiza transformaciones, colisiones, efectos, armas y representación; nunca requiere una trayectoria fija en el nivel.
8. **Comunicación de resultados:** los NPC informan de progreso, alertas, daños, imposibilidades y solicitudes de autorización cuando corresponda.

La nave debe **reevaluar** las decisiones durante la maniobra, y ser capaz de aceptar nuevas órdenes, interrumpir acciones o volver a un comportamiento de seguridad.

### Simulación independiente de la cámara

Los movimientos y encuentros deben continuar mientras el jugador esté **en el puente, en ingeniería, en su camarote o en otro interior**, no solo cuando active la vista exterior. El estado real debe coincidir para visores, sensores, ventanales y cámara externa.

Las naves que no se estén renderizando pueden necesitar menor detalle gráfico o menor frecuencia de actualización, pero **no deben perder arbitrariamente su estado ni sus órdenes**.

## 7. Conductas de ejemplo por clase

| Clase / función | Tendencia de maniobra inicial propuesta |
|---|---|
| Lanzaderas y naves pequeñas | Aceleración y respuesta ágiles; aproximación precisa; evasión relativamente cerrada |
| Naves medianas (Miranda, Intrepid, etc.) | Perfil equilibrado de respuesta y maniobra |
| Grandes (Galaxy, Sovereign, Odyssey, Valhalla) | Movimientos elegantes y deliberados, giros con sensación de volumen, trayectorias razonables, uso táctico de armamento y protección |
| Pájaro de Presa Romulano | Patrulla, observación, interceptación, ocultación si el modelo concreto la permite, sorpresa y retirada estratégica |
| Cubo Borg | Perfil especial de desplazamiento, resistencia, prioridades de objetivos y adaptación según sus sistemas |

Estos son **perfiles de diseño pendientes de parametrización y contraste audiovisual**, no comportamientos fijos ni hechos canónicos absolutos. La situación táctica, daños, misión y capitán pueden alterarlos.

## 8. Alcance práctico y ejemplo de uso

### Encuentro habitual — dos naves

**Primer banco de pruebas:** Enterprise-D (Galaxy) + **Pájaro de Presa Romulano NPC**.

- Ambas vuelan con el mismo controlador universal.
- Se detectan únicamente cuando lo permiten sus sensores y circunstancias.
- La Galaxy recibe una orden como «Mantenga distancia» o «Intercepte el contacto».
- El romulano ejecuta su propia misión y responde a las maniobras según sus reglas.
- Ninguna de las dos sigue una coreografía preparada en Sequencer.
- Pueden realizar seguimiento, evasión, comunicación, ataque autorizado, defensa o retirada.

### Escenario excepcional — combate de grupo

**Valhalla + Sovereign + Odyssey frente a un Cubo Borg**: prueba posterior para validar coordinación entre capitanes, roles, ataques, apoyo, retirada, objetivos cambiantes y comportamiento Borg.

Lo habitual serán **encuentros de dos naves**; los enfrentamientos de varias se reservan para situaciones especiales. **No fijar un límite de dos** en la arquitectura: diseñar para múltiples entidades y medir rendimiento.

## 9. Arquitectura y límites de responsabilidad

- **CoreRPG (C++ genérico):** gestiona los contratos genéricos que correspondan a reglas, estados, entidades, capacidades, autoridad/iniciativa y consecuencias. Evitar duplicar o anticipar interfaces no integradas.
- **Módulo específico Star Trek:** define clases de nave, doctrina, patrones, protocolos, armamento, sensores, órdenes y reglas de misión propias de este universo.
- **Unreal Engine 5.8.2:** control del movimiento tridimensional y la escena, componentes de navegación, colisiones, renderizado y efectos. Considerar C++ para el núcleo reusable y Blueprints/Data Assets para configuración e integración.
- **Tripulación NPC:** representa los puestos y emite informes/acciones vinculadas a estados reales de la simulación; debe respetar cadena de mando.
- **Gemini u otra IA generativa:** opcional para entender órdenes en lenguaje natural y diálogos, **nunca necesaria** para calcular cada giro o disparo en tiempo real.
- **Codex:** herramienta de desarrollo, implementación y pruebas, bajo revisión técnica y validación en el MSI.

La arquitectura ha de permitir también órdenes emitidas mediante botones o consolas, para no depender del reconocimiento de voz ni de servicios externos.

**No programar un controlador exclusivo de la Galaxy** que luego haya que reconstruir para las otras naves.

## 10. Relación con trabajos ya realizados

- **M09:** modelo exterior Galaxy con platillo y sección de batalla diferenciados.
- **M10C:** prototipo Blender de desacople/reacoplamiento con geometría visual M09 preservada y trayectoria guiada.
- **M11:** importación visual aceptable del GLB en un proyecto UE5 configurado para calidad máxima; prueba manual de separación y prueba de animación mediante Sequencer realizadas.

**Importante:** la animación de Sequencer es un **prototipo visual**, no la solución definitiva. El desacople y el reacoplamiento para el videojuego deberán calcularse respecto a la **posición/orientación actuales** de la nave, tener comprobaciones de seguridad y permitir que cada sección opere de forma independiente cuando corresponda.

## 11. Implementación propuesta por etapas

| Etapa | Entregable verificable |
|---|---|
| **NAV-01 — Control universal básico** | Galaxy avanza, gira, acelera y frena en tiempo real; sin Sequencer y con límites por clase |
| **NAV-02 — Segunda clase** | Pájaro de Presa Romulano usa **el mismo controlador**, con parámetros propios |
| **NAV-03 — Órdenes de navegación** | Ir a coordenadas, adoptar rumbo y velocidad, aproximar, igualar vector, seguimiento e interceptación |
| **NAV-04 — Sensores y conocimiento** | Detección mutua, pérdida de contacto, incertidumbre y comunicaciones; sin conocimiento mágico |
| **NAV-05 — Protocolos operativos** | Órdenes generales y patrones seleccionables, prioridades, cancelación y avisos a tripulación |
| **NAV-06 — Reacciones defensivas y combate** | Evasión, postura defensiva, ataques autorizados, respuestas a daños, retirada y protección |
| **NAV-07 — Maniobras de servicio** | Órbita, aproximaciones, atraque/desatraque y operaciones relacionadas con hangares |
| **NAV-08 — Separación dinámica** | Desacople, vuelo independiente y reacoplamiento con referencias y restricciones dinámicas |
| **NAV-09 — Coordinación multi-nave** | Escoltas, formaciones y escenarios de grupo, con prueba posterior frente a Cubo Borg |
| **NAV-10 — Integración** | Autoridad y persistencia mediante contratos reales de CoreRPG; funcionamiento desde interiores y sin cámara externa |

El orden exacto se revisará al comenzar la implementación. Las etapas no equivalen a fases ya ejecutadas ni comprometen plazos.

## 12. Criterios de aceptación

Antes de declarar aprobado el sistema deberá verificarse que:

1. La misma orden produce movimientos **coherentes pero no idénticos** en clases con capacidades distintas.
2. La orden «Acérquese» o «Iguale rumbo y velocidad» se ejecuta sin instrucciones de joystick del jugador.
3. «Ataquen esa nave» selecciona un plan adecuado **solo si está autorizado**; «Patrón X» impone el protocolo concreto mientras sea viable.
4. Las naves pueden reaccionar a cambios de rumbo, aproximación, ataques, daños, pérdida de sensores y nuevas órdenes durante la ejecución.
5. El controlador no utiliza secuencias fijas de posición para la navegación habitual.
6. El mismo código sirve para nave de jugador y NPC, con diferencias dadas por datos, permisos y emisor de órdenes.
7. La simulación continúa durante el juego en interiores y al cambiar entre cámaras.
8. Hay pruebas repetibles de seguridad, colisiones y evitación de maniobras imposibles; se miden rendimiento y estabilidad en el MSI.
9. Se comprueba que los oficiales comunican resultados reales, no relatos desconectados de la simulación.
10. El diseño preserva una posible integración con CoreRPG sin introducir dependencias de Unreal en el núcleo genérico.

## 13. Decisiones aprobadas, propuestas y asuntos abiertos

### Aprobado conceptualmente

- Predominio del juego interior y mando mediante órdenes; pilotaje directo no obligatorio.
- Navegación normal, maniobras de servicio y combate **automáticos o semiautomáticos**.
- Órdenes generales y protocolos explícitos coexistentes.
- Protocolos dinámicos, no coreografías fijas.
- Mismo sistema de navegación y reacción para todas las naves, jugables y NPC.
- Comportamiento dependiente de clase, equipamiento, misión, daños, conocimiento, comandante y autoridad.
- Encuentros habituales entre dos naves, sin limitar la arquitectura a dos.
- Primera prueba con **Enterprise-D y Pájaro de Presa Romulano**; batalla Valhalla/Sovereign/Odyssey contra Cubo Borg como escenario posterior.

### Pendiente de decidir o investigar

- Catálogo de nombres canónicos y diseños propios; validación de maniobras vistas en las series/películas.
- Modelo exacto de movimiento por clase, unidades, aceleraciones, giros, frenadas y tolerancias.
- Criterios de iniciativa de cada puesto y reglas de enfrentamiento por rango/orden.
- Estrategias de planificación, control y detección de obstáculos en 3D.
- Catálogo y serialización de protocolos (Data Assets/JSON u otra solución compatible).
- Coordinación del movimiento espacial exterior con interiores transitables y personajes.
- Integración final con CoreRPG cuando sus interfaces estén disponibles.
- Pruebas del comportamiento Borg y control de rendimiento en escenarios de varias naves.

---

**Resumen en una frase:** _El capitán ordena; sus oficiales y sistemas ejecutan de manera autónoma, competente y verificable, mediante protocolos dinámicos compartidos por todas las naves del universo Star Trek._


---

## 14. Registro oficial, compatibilidad y trazabilidad (añadido al archivar)

**Fecha de registro:** 16 de octubre de 2026. **Identificador:** IDEA-0009. **Decisión del autor:** analizar el archivo y registrarlo como una nueva idea del proyecto. Se conservan los 13 apartados del documento original; este apartado añade referencias a contratos ya existentes, límites y comprobaciones futuras sin alterar sus decisiones creativas.

### Relación con documentación ya existente

- **[IDEA-0008 — Entornos espaciales modulares](IDEA-0008_entornos_espaciales_modulares.md):** aporta escenario, posiciones y geometría espacial para las maniobras. IDEA-0009 aporta el sistema de *órdenes, protocolos y movimiento*; ninguna de las dos por sí sola acredita navegación UE5 funcional. La referencia de prueba a Enterprise-D y Pájaro de Presa Romulano aparece en ambas, para reutilizar un único banco de pruebas y evitar trabajo duplicado.
- **[IDEA-0003 — Hangares independientes](IDEA-0003_hangares_independientes_atraque_simulado.md):** aproximación, reserva/autorización de plaza, entrada/salida y transiciones requieren maniobras coherentes con órdenes y estado persistente.
- **[IDEA-0004 — Yate del capitán](IDEA-0004_yate_del_capitan_desacople_simulado.md):** desacople, separación controlada y reencuentro aplican los mismos principios universales y anclajes relativos, con reglas de acoplamiento propias.
- **[IDEA-0006 — Temporadas y misiones](IDEA-0006_temporadas_narrativas_misiones_episodicas.md):** el sistema de protocolos y órdenes será reutilizable por capítulos narrativos, misiones emergentes y actividades de vida a bordo; un pack no debe inventar capacidades navales.
- **[Flujo de órdenes](../../sistemas/gameplay/orders/starship_order_pipeline.md)** y **[contrato de orden](../../sistemas/gameplay/orders/starship_order_contract.json):** ya describen intérprete → validación → estación → evento autoritativo → retroalimentación. IDEA-0009 especializa la ejecución de *maniobras*, sin reemplazar el contrato existente.
- **[Contrato de órdenes de navegación](../../sistemas/gameplay/navigation/navigation_order_contract.json)** y **[estado de navegación](../../sistemas/gameplay/navigation/navigation_state.json):** intención, rumbo, warp, interceptación, órbita, atraque y evasión ya figuran **a nivel de contrato**; falta validar el ejecutor espacial compartido.
- **[Estado táctico](../../sistemas/gameplay/tactical/tactical_state.json):** las soluciones de tiro y autorizaciones son distintas de las órdenes de maniobra; «ataquen» nunca implica permiso automático para disparar cuando no exista.
- **[Interpretación IA de órdenes](../../sistemas/ai/command_interpretation/starship_command_contract.md):** la IA produce un plan estructurado, **no mueve naves ni dispara armas** directamente. Mantener entrada manual/teclado/consola como alternativa a voz.
- **[Autoridad operativa del capitán](../../sistemas/gameplay/chain_of_command/captain_operational_decision_authority_contract_v0.1.json)** y **[registro de decisiones automáticas](../../sistemas/gameplay/chain_of_command/automatic_command_decision_registry_v0.1.json):** las decisiones nuevas que pertenezcan al capitán deben documentar responsable, modos de delegación, límites duros y posibilidad de revisar o revocar. **90 % automático es aspiración UX**, no autorización general para desobedecer/omitir consentimiento requerido.
- **Consolas `conn`, `navigation` y `tactical`:** su definición funcional detallada continúa pendiente; se ampliarán reutilizando las familias existentes, no añadiendo un motor exclusivo para cada clase.

### Planificación técnica candidata (sin abrir fases ni ejecutar trabajos)

- **F02 / F04 / F05:** separar autoridad, delegación, conocimientos, decisiones NPC, interpretación de órdenes y ejecución; registrar los dominios de decisión automática realmente incorporados.
- **F06 / F09:** integrar datos de sensores, timón, navegación, operaciones y táctica, con los límites de información y permisos de cada puesto.
- **F07 / F14:** preparar y probar en UE5 el controlador universal de movimiento, mallas, clases de nave, efectos/animaciones y escena de entorno espacial modular.
- **F03 / F13:** estados espaciales autoritativos, simulación persistente al no renderizar naves, consecuencias y misiones dinámicas.
- **F15:** pruebas en MSI de maniobras seguras, clases diferentes, cambio interior/exterior, desacople y reacoplamiento, interrupciones, carga/guardado y coste en FPS/VRAM.

Las **etapas NAV-01 a NAV-10 del documento original** son una propuesta de desarrollo incremental, no fases del Plan Maestro ejecutadas ni PR ya existentes.

### Riesgos y decisiones pendientes de validación

1. **Simulación sin cámara exterior:** comprobar que cambiar al puente/camarote no altera los resultados del movimiento, los sensores ni la posición; usar representación/simulación simplificada fuera de escena cuando se justifique, nunca borrar el estado.
2. **Coherencia CoreRPG / Star Trek / UE5:** confirmar contratos de persistencia, autoridad, física local, datos de navegación y sincronización antes de fijar la implementación. El carácter genérico del CoreRPG prohíbe introducir allí clases, doctrinas y nombres específicos de Star Trek.
3. **Planes adaptativos:** definir vocabulario, IDs estables, condiciones, prioridades, interrupciones y efectos de cada protocolo. La ejecución no debe depender de trayectorias `Sequencer` pregrabadas ni de que Gemini tome decisiones por fotograma.
4. **Movimiento y precisión:** seleccionar unidades, perfiles de aceleración y giro, distancias de seguridad, colisiones, seguimiento/interceptación y comportamiento cuando la nave nodriza se desplaza. Evitar reglas ficticias de puntos débiles sin información confirmada.
5. **Control y permisos:** diseñar sustitución de órdenes, cancelación, emergencia, iniciativas de puestos y *rules of engagement* sin suplantar al capitán ni impedir correcciones legítimas.
6. **Diferencias de clases:** probar **dos vehículos muy distintos con el mismo controlador** y parámetros independientes; la configuración no debe forzar idénticas aceleraciones ni giros para lanzaderas, cruceros y Cubo Borg.
7. **Antecedentes de mallas:** los hitos Blender/UE5 **M09, M10C y M11** figuran en el documento aportado como contexto técnico del autor; esta auditoría de ideas **no certifica** sus archivos locales, pruebas UE5 o estado de integración.
8. **Nombres y canon:** verificar las denominaciones de patrones, tipos concretos de nave y fuentes audiovisuales antes de presentarlas como canon. Los protocolos originales del videojuego se etiquetarán como diseño propio.
9. **Rendimiento:** medir un enfrentamiento común de dos naves y, después, encuentros con varias; no asumir que toda la flota necesita estar instanciada en 3D ni fijar un límite arquitectónico de dos.

**Resultado administrativo:** IDEA-0009 aprobada y documentada, **NO IMPLEMENTADA**. No modifica modelos, Unreal Engine, CoreRPG, fases, contratos ni la Guardia de Sensores por el solo hecho de registrarse.

**Actualización 17-10-2026:** IDEA-0004 descartada y sustituida por [IDEA-0010](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md). Acceso a la auxiliar por turboascensor desde puente Valhalla, alojamiento/maniobra simulados.
