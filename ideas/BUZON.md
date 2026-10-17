# Buzón de ideas — Star Trek RPG

**Estado:** abierto para nuevas propuestas.
**Regla:** registrar primero; analizar y planificar después. No iniciar implementación desde este buzón.

Las ideas se incorporarán aquí por orden de llegada. Cada ficha podrá ampliarse en un archivo propio dentro de `ideas/` cuando lo justifique su complejidad.

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
