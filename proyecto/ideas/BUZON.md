# Buzón de ideas — Star Trek RPG

**Estado:** abierto para nuevas propuestas.
**Regla:** registrar primero; analizar y planificar después. No iniciar implementación desde este buzón.

Las ideas se incorporarán aquí por orden de llegada. Cada ficha podrá ampliarse en un archivo propio dentro de `proyecto/ideas/` cuando lo justifique su complejidad.

---

## Ideas capturadas pendientes de clasificar

*Ninguna pendiente de clasificar. Los sistemas y decisiones anteriores permanecen en sus documentos originales; no se duplican aquí.*

<!--
Formato para añadir una propuesta:

### IDEA-XXXX — Título
- Fecha: AAAA-MM-DD
- Estado: CAPTURADA
- Propuesta:
- Motivación:
- Relación con documentación existente: POR REVISAR
- Área responsable: POR CLASIFICAR
- Fase / paso: SIN ASIGNAR
- Decisión del autor: POR DETERMINAR
-->

## Ideas aprobadas pendientes de planificación

### IDEA-0001 — Sistema de replicadores interactivos
- **Fecha de aprobación:** 2026-10-11
- **Estado:** APROBADA (diseño); implementación pendiente.
- **Propuesta:** replicadores de comida y bebida accionables por voz o interfaz alternativa, interpretación determinista/IA, catálogo autorizado, materialización audiovisual y objetos físicos recogibles, consumibles y utilizables por NPC.
- **Motivación:** convertir dispositivos del universo Star Trek en mecánicas reales integradas con vida a bordo y ordenador de la nave.
- **Ficha detallada:** [IDEA-0001_replicadores_interactivos.md](IDEA-0001_replicadores_interactivos.md)
- **Relación con documentación existente:** Starship Computer, Core RPG, UE5 y Plan Maestro F00–F15.
- **Áreas/fases candidatas:** F02, F07, F12 y F14; asignación definitiva pendiente.
- **Decisión del autor:** aprobada expresamente, incluidas las mejoras discutidas y el límite de catálogo existente.
- **Ejecución:** no iniciada; no altera la Guardia de Sensores v0.0.1 ni la fase actual.

### IDEA-0002 — Biblioteca musical personal en los camarotes
- **Fecha de aprobación:** 2026-10-11
- **Estado:** APROBADA (diseño); implementación pendiente.
- **Propuesta:** biblioteca personal MP3/FLAC importada desde el MSI, vinculación de carpetas locales predeterminada y copia local opcional; reproducción por órdenes al ordenador de la nave, controles manuales y sonido espacial en camarotes.
- **Motivación:** convertir el camarote en un espacio habitable con ocio personalizado, sin subir ni distribuir archivos musicales.
- **Ficha detallada:** [IDEA-0002_biblioteca_musical_personal.md](IDEA-0002_biblioteca_musical_personal.md)
- **Relación con documentación existente:** Starship Computer, vida a bordo, Core RPG, UE5 y Plan Maestro F00–F15.
- **Áreas/fases candidatas:** F02, F07, F12 y F14; asignación definitiva pendiente.
- **Decisión del autor:** luz verde expresa a la idea, aclarando importación exclusivamente local desde el MSI y adoptando «Vincular carpeta» como opción predeterminada.
- **Ejecución:** no iniciada; no altera la Guardia de Sensores v0.0.1 ni la fase actual.

### IDEA-0003 — Hangares independientes por clase de nave y atraque simulado
- **Fecha de aprobación conceptual:** 2026-10-11
- **Estado:** APROBADA CONCEPTUALMENTE; planificación e implementación pendientes.
- **Propuesta:** crear hangares 3D propios por clase de nave, independientes del casco exterior cuando convenga, con opciones de integración física, híbrida o simulada y transiciones cinematográficas de salida y atraque.
- **Motivación:** maximizar libertad artística y calidad visual de los hangares sin exigir reconstrucciones destructivas de las mallas exteriores, manteniendo escala, procedimientos y coherencia del universo.
- **Invariante central:** lanzaderas, tripulantes, carga, daños, posiciones y plazas conservan identidad y persistencia; una lanzadera nunca está en dos lugares a la vez.
- **Ficha detallada:** [IDEA-0003_hangares_independientes_atraque_simulado.md](IDEA-0003_hangares_independientes_atraque_simulado.md)
- **Relación con documentación existente:** consola funcional `flight_deck`, Core RPG, UE5 y plan de atraque de instalaciones como referencia, no como contrato ya aplicable a lanzaderas.
- **Áreas/fases candidatas:** F02, F03, F04, F07, F09, F11, F14 y F15; asignación definitiva pendiente.
- **Decisión del autor:** idea aportada mediante documento original declarado aprobado conceptualmente; solicitada su incorporación a `/ideas`.
- **Alcance excluido:** el yate del capitán será una idea/documento distinto.
- **Ejecución:** no iniciada por este registro; no interrumpe la fase activa.

### IDEA-0005 — Blindaje ablativo desplegable y torpedos transfásicos de Valhalla
- **Fecha de aprobación:** 2026-10-13.
- **Estado:** APROBADA CONCEPTUALMENTE; implementación y pruebas pendientes.
- **Propuesta:** blindaje ablativo desplegable y torpedos transfásicos en la nueva **Clase Valhalla** (inspirada en Galaxy), como adición tecnológica de la continuidad personal del videojuego.
- **Ficha detallada:** [IDEA-0005_blindaje_ablativo_y_torpedos_transfasicos_valhalla.md](IDEA-0005_blindaje_ablativo_y_torpedos_transfasicos_valhalla.md).
- **Decisión del autor:** aprobadas ambas tecnologías; acepta ajustar acontecimientos/fechas del canon de TV. **Año de servicio Valhalla no fijado.** Viabilidad gráfica en Blender/UE5 y reglas de juego aún por estudiar.
- **Áreas candidatas:** Star Trek específico, Core genérico solo para mecanismos comunes, UE5/VFX, Blender/activos y pruebas F07+; sin alterar v0.0.1 Sensores.
- **Ejecución:** NO_INICIADA; no autoriza el cierre de ninguna fase.

### IDEA-0006 — Sistema de temporadas narrativas y misiones episódicas
- **Fecha de aprobación:** 2026-10-13.
- **Estado:** APROBADA (diseño conceptual); planificación técnica e implementación pendientes.
- **Propuesta:** temporadas con episodios/misiones conectadas por una trama común, ramificaciones y consecuencias persistentes; adecuación al tipo/capacidades de nave y al rango/puesto del jugador; órdenes oficiales por cadena de mando y periodos de vida libre entre capítulos.
- **Contenido externo:** diseño de nuevas temporadas por el autor con ChatGPT e importación de **Season Packs** estructurados/versionados, sin recompilar cuando utilicen mecánicas y recursos ya soportados.
- **Coexistencia:** misiones emergentes del universo, guardias ordinarias, ocio, exploración y NPC que actúan fuera de escena; los contenidos narrativos no crean arbitrariamente hechos ni resultados autoritativos.
- **Ficha detallada:** [IDEA-0006_temporadas_narrativas_misiones_episodicas.md](IDEA-0006_temporadas_narrativas_misiones_episodicas.md).
- **Relación con sistemas existentes:** `mission_state`, `mission_objective_state`, `starfleet_mission_tasking_order`, continuidad de campaña, autoridad/participación por rol y misiones emergentes desde World State.
- **Fases candidatas:** F02, F03, F04–F05, F11–F15; principalmente F11 y F13. Asignación definitiva pendiente.
- **Decisión del autor:** aprobada expresamente tras debate el 2026-10-13.
- **Numeración:** registrada como 0006 porque el número 0005 ya pertenece a las tecnologías de la Clase Valhalla.
- **Ejecución:** no iniciada por el registro; no modifica el alcance de la v0.0.1 de Sensores ni abre otra fase.

### IDEA-0007 — Carrera por temporadas, acceso anticipado y mando de Valhalla
- **Fecha de aprobación conceptual:** 2026-10-15.
- **Estado:** APROBADA CONCEPTUALMENTE; implementación y planificación pendientes.
- **Propuesta:** tres etapas (Academia, carrera en distintas naves y vida/mando prolongados en Clase Valhalla), con temporadas conectadas a evaluaciones y oportunidades profesionales sin ascenso automático.
- **Acceso temprano:** opción de destino legítimo en Valhalla ya como teniente; posibilidad de permanecer y ascender allí sin desplazar automáticamente a su capitán NPC.
- **Mando sin edad tardía obligatoria:** ofrecer una oportunidad justificada de capitanear Valhalla **en cuanto el jugador sea apto**, incluso sobre los 35–40 años o antes por trayectoria excepcional; no posponerlo al final de su carrera o cerca de la jubilación.
- **Carreras disponibles:** guiada hacia Valhalla y libre, con posibilidad de ascensos extraordinarios por hechos verdaderamente excepcionales al estilo Kelvin; cualquier rango/nombramiento requiere revisión y decisión válida.
- **Regla:** rango, puesto y mando titular son distintos; varios comandantes pueden servir a bordo. El capitán titular no se elimina ni sustituye sin una sucesión real y justificada.
- **Ficha detallada:** [IDEA-0007_carrera_temporadas_llegada_y_mando_valhalla.md](IDEA-0007_carrera_temporadas_llegada_y_mando_valhalla.md).
- **Vinculación:** [IDEA-0006 — Temporadas narrativas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md); contratos existentes de carrera y ascensos en F11, continuidad, autoridad y Core RPG.
- **Decisión del autor:** confirmada a lo largo de varias intervenciones el 2026-10-15, incluyendo acceso anticipado, promociones extraordinarias y corrección expresa del criterio de edad.
- **Ejecución:** no iniciada; no implica ascensos concedidos, vacantes fabricadas ni modificación de fases.

### IDEA-0008 — Sistema modular de entornos espaciales
- **Fecha de incorporación:** 2026-10-16.
- **Estado:** APROBADA CONCEPTUALMENTE; implementación, validaciones y planificación pendientes.
- **Propuesta:** escenarios espaciales universales y reutilizables por perfiles de sector: campo estelar/nebulosas de fondo, estrella e iluminación, planetas/lunas/asteroides 3D y naves/estaciones reales.
- **Experiencia:** navegación dinámica común a nave del jugador y NPC, piloto automático, sensores, aproximación/orbita simplificada, combates y vistas coherentes desde puentes y cámaras exteriores.
- **Rendimiento:** perfiles gráficos modulares, LOD/instanciación/culling, streaming, precisión y escala espacial; medir FPS, VRAM y materiales en MSI RTX 4070 Laptop 8 GB.
- **Prototipo propuesto:** Enterprise-D (Galaxy) y Pájaro de Presa Romulano; demostrar al menos dos entornos sin duplicar su arquitectura. Modelos de planetas locales a auditar antes de usar.
- **Ficha detallada:** [IDEA-0008_entornos_espaciales_modulares.md](IDEA-0008_entornos_espaciales_modulares.md).
- **Relación con sistemas existentes:** F02, F03, F07, F09, F13, F14 y F15; universo persistente/CoreRPG, UE5 y [IDEA-0006 — Temporadas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md). Asignación definitiva pendiente.
- **Decisión del autor:** solicitada su incorporación desde un documento Markdown aportado el 2026-10-16.
- **Exclusiones:** no se aprueban por esta ficha vuelos atmosféricos, física orbital completa ni nueva lógica de Core RPG; el sistema no está implementado.
- **Ejecución:** no iniciada por este registro, sin interferir en las fases activas.

### IDEA-0009 — Sistema universal de órdenes, protocolos y maniobras de naves
- **Fecha de aprobación conceptual y registro:** 2026-10-16.
- **Estado:** APROBADA CONCEPTUALMENTE; planificación, implementación y pruebas pendientes.
- **Propuesta:** control de naves mediante órdenes de intención («orbite», «intercepte», «mantenga distancia») o protocolos explícitos de navegación, ataque, defensa y evasión, resueltos mediante planes dinámicos, nunca coreografías predeterminadas.
- **Experiencia:** juego principalmente desde el interior de las naves; oficiales y sistemas ejecutan maniobras de forma autónoma según autoridad, información, clase, capacidades, recursos y situación; posibilidad de intervenir, cancelar o pilotar manualmente cuando corresponda.
- **Universalidad:** mismo sistema de maniobra para naves del jugador, NPC, civiles, hostiles, lanzaderas y secciones separadas; perfiles por clase y sin simuladores duplicados por nave.
- **Banco de pruebas propuesto:** primero Enterprise-D/Galaxy y Pájaro de Presa Romulano NPC; más adelante combate coordinado Valhalla + Sovereign + Odyssey contra Cubo Borg, sin asumir pruebas reales completadas.
- **Implementación por etapas:** NAV-01 a NAV-10 en documento, con verificación de control universal, interpretación de órdenes, sensores, tácticas, maniobras de servicio, separación, coordinación y persistencia.
- **Ficha detallada:** [IDEA-0009_ordenes_protocolos_maniobras_universales.md](IDEA-0009_ordenes_protocolos_maniobras_universales.md).
- **Vinculaciones:** [IDEA-0008 — Entornos espaciales](IDEA-0008_entornos_espaciales_modulares.md), [IDEA-0003 — Hangares](IDEA-0003_hangares_independientes_atraque_simulado.md), [IDEA-0004 — Yate](IDEA-0004_yate_del_capitan_desacople_simulado.md), contratos actuales de órdenes, navegación, táctica, sensores y autoridad de mando.
- **Fases candidatas:** F02–F07, F09, F13–F15; por planificar. CoreRPG solo para responsabilidad genérica, Star Trek para reglas concretas y UE5 para navegación/visualización.
- **Decisión del autor:** archivo Markdown original aportado el 16-10-2026 con aprobación conceptual expresa y solicitud de incorporación como nueva idea.
- **Ejecución:** NO INICIADA por este registro; no implica código UE5, CoreRPG, clases ni protocolos probados.

### IDEA-0010 — Nave auxiliar táctica y furtiva integrada en Valhalla (tipo Defiant)
- **Fecha de aprobación:** 2026-10-17.
- **Estado:** APROBADA CONCEPTUALMENTE; sustituye de forma expresa a la IDEA-0004, ahora descartada. **No implementada**.
- **Propuesta:** nave auxiliar original inspirada en Defiant, con exterior y puente 3D ya disponibles como activos candidatos, para infiltración, exploración discreta, incursiones, rescates y apoyo táctico junto a Valhalla.
- **Decisión definitiva de alojamiento:** **NO físico**. Al igual que las cubiertas y el gran hangar, el interior de la auxiliar es una escena independiente. **Acceso directo desde el puente principal de Valhalla mediante turboascensor** con destino «Nave auxiliar táctica», sin corredores/hangares físicos de conexión.
- **Maniobra de salida:** desacople y regreso representados por transición simulada y anclaje exterior virtual, manteniendo escala visual, autorización y entidad/ocupantes persistentes. El acceso desde Valhalla se bloquea mientras la nave vuela separada.
- **Sistemas a estudiar:** furtividad y posible camuflaje bajo reglas de época/canon propio, blindaje ablativo, dotación operativa reducida pero coherente, armamento y autonomía equilibrados.
- **Documentación oficial:** [IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md).
- **Vinculaciones:** [IDEA-0003 — Hangares/atraque simulado](IDEA-0003_hangares_independientes_atraque_simulado.md), [IDEA-0008 — Entornos espaciales](IDEA-0008_entornos_espaciales_modulares.md), [IDEA-0009 — Maniobras](IDEA-0009_ordenes_protocolos_maniobras_universales.md), [IDEA-0006 — Temporadas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md).
- **Hitos candidatos:** AUX-01–AUX-08; futura auditoría Blender/UE5 y CoreRPG. La aprobación del concepto no declara jugabilidad ya existente.

### IDEA-0011 — DLC Cuadrante Delta: portal transwarp de acceso controlado
- **Fecha de aprobación expresa:** 2026-10-17.
- **Estado:** APROBADA CONCEPTUALMENTE; diseño técnico, contenido, integración y pruebas pendientes.
- **Propuesta:** expansión/DLC opcional e independiente del juego base que permite a las naves autorizadas viajar desde el cuadrante Alfa hasta el Delta mediante un portal hexagonal verde de inspiración Borg. El autor dispone de un modelo 3D candidato, aún sin auditar ni integrar en UE5.
- **Exploración:** nuevos sectores, civilizaciones de `Star Trek: Voyager`, expediciones y temporadas narrativas, con acercamiento progresivo al espacio Borg y continuidad de partida.
- **Restricción Borg innegociable:** **ninguna nave Borg puede cruzar este portal hacia el cuadrante Alfa**, ni el DLC crea incursiones Borg automáticas en el juego principal. Cualquier llegada Borg futura a Alfa debe diseñarse aparte y sin este atajo.
- **Regreso elegido por el autor — Opción C:** normalmente se vuelve **por el mismo portal con autorización**, pero daños, averías o sucesos narrativos reales pueden bloquearlo temporalmente y requerir misiones especiales para recuperar el acceso.
- **DLC desactivado:** portal inoperativo/no accesible; el juego base y sus guardados no se alteran arbitrariamente. Se estudiará la instalación/activación y la compatibilidad de partidas.
- **Ficha completa:** [IDEA-0011_dlc_cuadrante_delta_portal_transwarp.md](IDEA-0011_dlc_cuadrante_delta_portal_transwarp.md).
- **Vínculos:** [IDEA-0006 — Temporadas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md), [IDEA-0008 — Entornos espaciales](IDEA-0008_entornos_espaciales_modulares.md), [IDEA-0009 — Maniobras](IDEA-0009_ordenes_protocolos_maniobras_universales.md), persistencia/World State, UE5 y CoreRPG genérico.
- **Etapas candidatas:** DELTA-01–DELTA-08 en la ficha; fases F02/F03, F07/F09, F11, F13–F15. Planificación pendiente.
- **Decisión del autor:** elige y aprueba expresamente opción C y solicita registrar IDEA-0011.
- **Ejecución:** NO INICIADA por este registro. No existe aún DLC, portal operativo ni cuadrante Delta jugable.

### IDEA-0012 — Ajedrez clásico 3D con NPC, aprendizaje y vida social
- **Fecha de aprobación expresa:** 2026-10-24.
- **Estado:** APROBADA CONCEPTUALMENTE; diseño documental registrado, implementación UE5/CoreRPG y pruebas pendientes.
- **Propuesta:** minijuego funcional de ajedrez **clásico 8×8** para jugar con NPC amigos o compañeros en bar, camarote o espacio compatible de Academia, estaciones y naves, especialmente Valhalla.
- **Referente Star Trek:** alternativa práctica al ajedrez tridimensional de varios tableros de las series; **no se obliga al jugador a aprender esa variante** ni se borra su existencia cultural del universo.
- **Activos:** el autor ha descargado un **tablero de madera 3D** y modelos de **piezas blancas y negras 3D** para futura auditoría e importación al MSI/UE5.
- **Interacción aprobada:** acercarse a NPC, quedar y sentarse si procede, activar cámara de primer plano casi a pantalla completa desde la perspectiva del jugador, seleccionar/mover piezas con ratón; el motor mueve las piezas del NPC automáticamente **sin animaciones de manos/brazos obligatorias**.
- **Accesibilidad:** tutorial desde cero, niveles de dificultad realmente suaves, casillas legales resaltadas, ayudas y juego sin límite de tiempo; motor de ajedrez local reutilizable a seleccionar.
- **Convivencia y amistad:** actividad con agenda, lugar, personajes y resultados persistentes; puede reforzar historia compartida, afinidad y amistad **solo según las reglas sociales existentes**, no por ganar ni sumar puntos fijos automáticos.
- **Persistencia:** partida aplazable y reanudable, incluso tras emergencia/cambio de guardia; estado del tablero y turnos coherentes con guardado y carga.
- **Ficha detallada:** [IDEA-0012_ajedrez_clasico_3d_con_npc.md](IDEA-0012_ajedrez_clasico_3d_con_npc.md).
- **Integración existente:** actividad `games_cards_chess` ya contemplada en `sistemas/gameplay/ship_operations/off_duty_activity_catalog_v0.1.json`, reglas sociales, calendarios de NPC y F12; visualización F07/F14 y pruebas F15. No se creará un sistema social paralelo.
- **Hitos candidatos:** CHESS-01–CHESS-07, del inventario 3D al tablero, rival, dificultades, persistencia y juego social.
- **Decisión del autor:** inscripción solicitada expresamente después de discutir la viabilidad técnica y precisar el uso exclusivamente personal del juego y la simplificación de las animaciones corporales.
- **Ejecución:** no iniciada por este registro; la aprobación conceptual no certifica ajedrez funcional ya programado.

### IDEA-0013 — Homenaje a Sir Patrick Stewart y Jean-Luc Picard eterno
- **Fecha de aprobación expresa:** 2026-10-29.
- **Estado:** APROBADA CONCEPTUALMENTE; planificación, integración y pruebas pendientes.
- **Origen:** fallecimiento de **Sir Patrick Stewart (1940–2026)** el 28-10-2026, anunciado el 29-10-2026; el autor desea rendir homenaje a quien interpretó a su personaje favorito.
- **Compromiso A — Homenaje general del videojuego:** dedicatoria permanente y discreta al actor, visible en presentación y/o créditos. La muerte real del actor no afecta al destino ficticio de Picard.
- **Compromiso B — Sala de reuniones de Valhalla:** retrato, placa e información interactiva opcional sobre **el legado de Jean-Luc Picard**, visitables dentro de una sala que sigue siendo funcional; homenaje a su trayectoria, **no funeral del personaje**.
- **Compromiso C — PICARD ETERNO:** el almirante Picard continúa **vivo y presente** en el canon propio; nunca morirá ni desaparecerá automáticamente por edad, acontecimientos aleatorios, simulación, canon televisivo ni por la muerte de Patrick Stewart. La protección solo podrá revisarse por nueva decisión expresa del autor.
- **Límites narrativos:** continuidad y ubicación coherentes, sin convertir al NPC en omnisciente, omnipresente ni cambiar arbitrariamente el rango o destino de otros personajes.
- **Ficha detallada:** [IDEA-0013_homenaje_sir_patrick_stewart_picard_eterno.md](IDEA-0013_homenaje_sir_patrick_stewart_picard_eterno.md).
- **Integración:** presentación y créditos, diseño de la sala de reuniones, lore de personajes, World State y pruebas de protección narrativa. Se conserva la separación entre CoreRPG genérico y reglas particulares Star Trek.
- **Hitos candidatos:** PICARD-01–PICARD-07; ejecución UE5/Blender/CoreRPG/QA aún no iniciada.
- **Decisión del autor:** aprueba expresamente las tres propuestas (general, sala de reuniones y Picard eterno) el 29-10-2026.
- **Ejecución:** NO INICIADA por este registro; no se confunde documentación con elemento jugable ya implementado.

### IDEA-0014 — Intercomunicadores inteligentes en puertas de camarotes
- **Fecha de aprobación expresa y registro:** 2026-11-04.
- **Estado:** APROBADA CONCEPTUALMENTE; planificación, implementación UE5/IA y pruebas pendientes.
- **Propuesta:** botón de intercomunicador junto a **cada puerta de camarote**, con aviso sonoro de estilo Star Trek en el interior y respuesta creíble según presencia, disponibilidad, privacidad y personalidad de los ocupantes.
- **Bidireccional:** **jugador→NPC** (llama y espera respuesta del residente) y **NPC→jugador** (aviso en el camarote del jugador, quien responde libremente por voz o texto).
- **IA:** interpreta respuestas coloquiales («¿Quién es?», «Adelante», «Espere un momento», «Ahora no», «¿Qué necesita?» y frases compuestas) y propone **intenciones estructuradas**, sin ejecutar directamente ni modificar el World State.
- **Autoridad:** el motor valida identidad, permisos, ocupación, estado de puerta, seguridad, alerta y solicitudes vigentes; únicamente entonces abre, mantiene cerrada, solicita identificación, registra espera o deniega entrada.
- **Experiencia:** sonido y botón interactivos, diálogo natural, transiciones de interior compatibles con escenarios modulares, subtítulos y alternativa escrita a micrófono.
- **Reglas sociales:** sin teletransportar NPC desde otros lugares, conceder acceso por rango/amistad ni inventar disponibilidad o confianza; las emergencias autorizadas siguen procedimientos específicos.
- **Ficha detallada:** [IDEA-0014_intercomunicadores_inteligentes_camarotes.md](IDEA-0014_intercomunicadores_inteligentes_camarotes.md).
- **Vínculos técnicos:** `sistemas/ai/command_interpretation/starship_command_contract.md`, `sistemas/gameplay/ship_operations/shipboard_life_state_contract.json`, `sistemas/gameplay/ship_operations/interior_location_model.json`, agendas de NPC, reglas sociales, F10 y F12.
- **Desarrollo candidato:** ICOM-01–ICOM-08; primero contratos, botón/sonido, máquina de estados, después ambas direcciones de llamada, IA, persistencia y QA.
- **Decisión del autor:** aprobada expresamente tras debatir el funcionamiento del sistema.
- **Ejecución:** NO INICIADA por el registro; no implica que las puertas o intercomunicadores ya funcionen en UE5.

### IDEA-0015 — Turboascensores inteligentes con lenguaje natural y navegación interior
- **Fecha de aprobación expresa:** 2026-11-04.
- **Estado:** APROBADA CONCEPTUALMENTE; planificación, implementación y pruebas pendientes.
- **Propuesta:** al **entrar en un turboascensor**, se activa automáticamente la petición de destino. El jugador puede expresarse libremente («Ingeniería», «al bar», «a mi camarote», «cubierta H» y frases coloquiales) por voz o texto, sin aprender comandos.
- **Cartografía:** distribución interior de cada nave/instancia documentada en **JSON estructurado**, con cubiertas, habitaciones, nombres y alias, ascensores, puntos de acceso, conexiones y restricciones. Markdown opcional solo como documentación.
- **Resolución híbrida:** consulta **local** de nombres claros; la **IA interpreta** expresiones complejas usando solo un contexto autorizado/filtrado, devuelve destino candidato estructurado y solicita aclaraciones cuando existen varios destinos posibles.
- **Autoridad del motor:** valida existencia, permisos, estado de la red y rutas; elige **el turboascensor de salida accesible más cercano**, ejecuta el desplazamiento y carga la cubierta/escena UE5 correspondiente. La IA nunca teletransporta personajes ni inventa salas.
- **Casos especiales:** «mi camarote» consulta la asignación vigente; varios bares requieren elección/preferencia válida; una cubierta inexistente no se inventa; daños, alertas y separación de platillo/cuerpo impiden rutas incompatibles.
- **Persistencia:** el viaje consume tiempo razonable y conserva identidad, ubicación, agendas y World State, incluyendo NPC fuera de cámara; cabina/transición visual sin necesidad de modelar todos los ejes físicos.
- **Ficha detallada:** [IDEA-0015_turboascensores_inteligentes_lenguaje_natural.md](IDEA-0015_turboascensores_inteligentes_lenguaje_natural.md).
- **Integración:** `sistemas/gameplay/ship_operations/interior_location_model.json`, `sistemas/ai/command_interpretation/starship_command_contract.md`, [IDEA-0014 — Intercomunicadores](IDEA-0014_intercomunicadores_inteligentes_camarotes.md), [IDEA-0010 — Nave auxiliar](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md), CoreRPG, F10/F12 y UE5.
- **Hitos candidatos:** TL-01–TL-08: auditoría de mapa, catálogo, cabina, interpretación local/IA, rutas/permisos, streaming, pruebas de destinos y QA.
- **Decisión del autor:** aprobación expresa de la propuesta y de las dos mejoras técnicas (JSON fuente principal y resolución local+IA).
- **Ejecución:** NO INICIADA por este registro; no representa mapa completo, red de turboascensores jugable ni pruebas UE5 superadas.

### IDEA-0016 — Insignias Starfleet y sistema universal de comunicaciones inteligentes
- **Fecha de aprobación conceptual:** 2026-11-04.
- **Estado:** APROBADA CONCEPTUALMENTE; **respuesta progresiva y enmascaramiento de latencia aprobados expresamente**; implementación y pruebas pendientes.
- **Idea central:** jugador y NPC de Flota Estelar llevan insignias 3D personales en el pecho con símbolo de rama inspirado en **Star Trek: Strange New Worlds** y función de comunicador de la era Picard; civiles y otros NPC conservan su identidad y equipamiento legítimo.
- **Activación:** tocar insignia mediante tecla o botón del mando, tono de comunicación, solicitud libre por voz o texto, opción de cerrar el canal o pulsar para hablar. Llamadas entrantes y salientes.
- **Peticiones:** hablar con computadora, nave, un NPC/departamento, consultar lugares y tripulantes, preguntar datos autorizados y emitir instrucciones/órdenes validadas. Respuesta natural, aclaración de destinatarios y continuidad de conversación.
- **Arquitectura:** resoluciones sencillas **locales**, intérprete IA para lenguaje complejo, distribuidor de **intenciones estructuradas** y ejecución exclusivamente autoritativa en juego/CoreRPG. Reutilizar `sistemas/ai/command_interpretation/starship_computer_system.md` y `sistemas/gameplay/communications/README.md`, no crear una IA por dispositivo.
- **Comunicaciones reales:** disponibilidad, horarios, privacidad, rango, canales, interferencias, distancia, subespacio, imposibilidad técnica y autonomía NPC; no se inventan respuestas, conocimiento ni éxito de órdenes.
- **Mejora aprobada expresamente — latencia:** **respuestas progresivas**. La computadora comienza a pronunciar una introducción con **hechos ya comprobados** mientras consulta la información pendiente; añade el resultado tras validarlo. Para órdenes rápidas evita relleno, y ante demoras informa de que sigue consultando, sin fingir datos o acciones.
- **Rendimiento:** objetivos orientativos de respuesta local casi inmediata y respuesta inicial por IA con mínima espera; medir de verdad en MSI `fin de voz → primer audio` y `fin de voz → resultado validado`; sin prometer segundos fijos.
- **Ficha completa:** [IDEA-0016_insignias_starfleet_comunicaciones_universales.md](IDEA-0016_insignias_starfleet_comunicaciones_universales.md).
- **Vínculos:** [IDEA-0014 — Intercomunicadores](IDEA-0014_intercomunicadores_inteligentes_camarotes.md), [IDEA-0015 — Turboascensores](IDEA-0015_turboascensores_inteligentes_lenguaje_natural.md), contratos actuales de computadora, comunicaciones, identidad NPC, permisos y vida a bordo.
- **Etapas candidatas:** BADGE-01–BADGE-09: insignias/ramas, controles, enrutador, computadora, llamadas NPC, órdenes, respuestas progresivas y QA en MSI/UE5.
- **Decisión del autor:** propone expresamente este sistema universal de insignias, desarrolla la optimización para ganar tiempo mediante locución y la aprueba («Aprobado»).
- **Ejecución:** **NO INICIADA** por el registro; los objetos 3D, las llamadas y la voz progresiva aún no son funcionalidades jugables.

### IDEA-0017 — Vida personal, relaciones sentimentales, matrimonio y familia
- **Fecha de aprobación expresa:** 2026-11-04.
- **Estado:** APROBADA CONCEPTUALMENTE; implementación y QA pendientes.
- **Nave protagonista vigente:** **Proyecto Valhalla = USS Enterprise NCC-1701-D (Galaxy) restaurada y modernizada por Geordi La Forge**. Preservar la identidad Enterprise-D y los espacios civiles/familiares reales de esta configuración; **la antigua Enterprise-G/clase Valhalla se ha descartado**.
- **Vida personal opcional:** puedes permanecer soltero sin restricciones, ser un **soltero picaflor y mujeriego**, coquetear y tener citas/relaciones informales consentidas o iniciar una pareja estable. No imponer progreso ni boda/hijos como condición de juego.
- **Compromiso:** pareja consolidada, convivencia, matrimonio y ceremonias persistentes, con aceptación mutua, memoria causal, acuerdos y autonomía de NPC.
- **Familia:** posibilidad de tener hijos, gestación/nacimiento cuando proceda, parentesco, crianza, crecimiento infantil, educación y vida doméstica; nuevos niños como **personajes persistentes reales**.
- **Consecuencias de vida y carrera:** guardias, tiempo familiar, cambios de nave, permisos, residencias, traslados, comunicaciones a distancia y restricciones de alojamiento; sin teleportar familiares ni inventar servicios.
- **Reglas sociales:** reutilizar `sistemas/gameplay/social/social_event_rules.json`, `sistemas/gameplay/social/README.md` y los contratos de vida a bordo; **respetar el canon autoral adulto vigente**. Consentimiento, reciprocidad y ausencia de coerción; ser soltero o vivir relaciones consensuadas informales no causa penalización moral automática.
- **IA/Core:** diálogo, emociones y memoria narrativa sí; IA no inventa matrimonio, embarazos, hijos, decisiones de voluntad ni cambios de World State. Core/Star Trek validan y persisten.
- **Ficha detallada:** [IDEA-0017_vida_personal_pareja_matrimonio_familia.md](IDEA-0017_vida_personal_pareja_matrimonio_familia.md).
- **Etapas candidatas:** LIFE-01–LIFE-09, desde ampliación de relaciones hasta vida familiar y continuidad durante años de campaña.
- **Decisión del autor:** aprobado expresamente tras ampliar la propuesta para incluir soltería y vida de picaflor/mujeriego.
- **Ejecución:** NO INICIADA por registrar la idea; ni matrimonios ni hijos jugables declarados implementados.

### IDEA-0019 — Starfleet PADD: terminal Android de consulta de la última partida
- **Fecha de aprobación expresa:** 2026-11-06.
- **Estado:** APROBADA CONCEPTUALMENTE; implementación pendiente.
- **Propuesta:** app Android LCARS para móvil y tablet que muestra el estado **de la última partida guardada**, con expediente del jugador, retrato, departamento, dotación, turnos, órdenes, bitácora, planos reales de la nave y registros de mando autorizados.
- **Permisos:** rango, puesto, destino, autoridad, habilitación y conocimiento reales; un teniente jefe de Sensores, primer oficial y capitán ven información distinta. Los documentos clasificados y datos privados se filtran **antes** de exportar.
- **Arquitectura candidata:** CoreRPG/Star Trek → snapshot JSON filtrado y versionado → Firebase Auth + Firestore/Storage → aplicación Kotlin/Compose LCARS; lectura offline con fecha de última sincronización. GitHub no se usará para exponer información privada de partidas.
- **Invariante:** **solo consulta**. Android no cambia la partida, no da órdenes y no avanza el tiempo mientras el juego está cerrado.
- **Ficha detallada:** [IDEA-0019_starfleet_padd_consulta_android_partida.md](IDEA-0019_starfleet_padd_consulta_android_partida.md).
- **Etapas candidatas:** PADD-01–PADD-06. Dependencias F02–F07, F09, F11–F12, F14–F15; planificación definitiva pendiente.
- **Decisión del autor:** «guárdala como nueva idea».
- **Ejecución:** NO INICIADA; no altera F05 ni el Plan Maestro.

### IDEA-0020 — Cartografía interior real, localización y guiado inteligente
- **Fecha de aprobación expresa:** 2026-11-06.
- **Estado:** APROBADA; **implementación autorizada y progresiva**, pendiente de geometría y pruebas integradas.
- **Propuesta:** cartografía de **nuestra Enterprise-D modernizada**, no de la original; cada sala, puerta, camarote, pasillo y turboascensor tiene identidad y conexiones verificadas. La computadora conoce la posición autorizada del jugador y de NPC según World State y ofrece rutas habladas o LCARS.
- **Seguridad y coherencia:** accesos, bloqueos, privacidad, localización desconocida, conectores virtuales entre escenas y replanificación; no inventar rutas, ocupantes ni conocimiento.
- **Ficha detallada:** [IDEA-0020_cartografia_interior_localizacion_y_guiado_inteligente.md](IDEA-0020_cartografia_interior_localizacion_y_guiado_inteligente.md).
- **Relación:** [IDEA-0015 — Turboascensores](IDEA-0015_turboascensores_inteligentes_lenguaje_natural.md), [IDEA-0016 — Insignias](IDEA-0016_insignias_starfleet_comunicaciones_universales.md), [IDEA-0019 — Starfleet PADD](IDEA-0019_starfleet_padd_consulta_android_partida.md), CoreRPG, F03–F05, F07, F12, F14–F15.
- **Etapas candidatas:** MAP-01–MAP-08. Empezar por contrato/validador, completar planos solo cuando existan salas y conexiones reales.
- **Decisión del autor:** «esta ... también ... implémentala».
- **Ejecución:** autorizada; el registro por sí solo no significa cartografía UE5 terminada.

## Ideas planificadas

*Todavía ninguna: pendiente de acordar el plan maestro.*

## Ideas integradas, aplazadas o descartadas

### IDEA-0004 — Yate del capitán [DESCARTADA / SUSTITUIDA]
- **Fecha de descarte:** 2026-10-17.
- **Estado:** DESCARTADA / SUSTITUIDA por [IDEA-0010 — Nave auxiliar táctica y furtiva de Valhalla](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md).
- **Decisión expresa del autor:** no incorporar yate tradicional del capitán a Valhalla ni mantenerlo como propuesta activa general; se prefiere una nave tipo Defiant con puente 3D, misiones de infiltración y apoyo táctico.
- **Documento histórico preservado:** [IDEA-0004_yate_del_capitan_desacople_simulado.md](IDEA-0004_yate_del_capitan_desacople_simulado.md).
- **Reutilización:** persistencia, maniobras y transiciones se reaprovechan mediante IDEA-0003 e IDEA-0010, no como un yate vigente.
- **Ejecución:** nunca implementada; no requiere desinstalación ni cambios en modelos 3D.
