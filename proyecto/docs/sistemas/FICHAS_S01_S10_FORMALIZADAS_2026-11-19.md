# Fichas S01–S10 — formalización conceptual

**Ámbito exclusivo:** SISTEMAS · **Fecha:** 19-11-2026 · **Referencia:** [auditoría independiente](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md), aprobaciones conversacionales y DEC-0020–0024.

Las fichas no autorizan programación ni reemplazan contratos técnicos. «Evidencia» identifica solo el alcance que consta en fuentes; **no hay certificación global de ninguno de estos sistemas Core + HOST + UE5** en esta revisión.

## S01 — IA central

**Objetivo aprobado:** servicio único de IA para lenguaje, diálogos y análisis necesarios en el juego, sin un acceso API diferente por NPC, consola o tarea.

**Funciones:**
- Encaminamiento compartido **por HOST** hacia OpenAI, con rutas lógicas según complejidad y configuración común de modelos, clave, límites y contexto.
- Conversaciones NPC, interpretación de peticiones complejas, ordenador de la nave y resúmenes sobre información **permitida y verificable**, con prioridad razonable de peticiones y rechazo/cancelación de trabajo obsoleto.
- Salida segura sin acceso: texto manual/acciones deterministas siguen disponibles; sin aprobar un permiso por fallo o respuesta del proveedor.
- Política de costes por sesión y función a concretar en HOST; contador de llamadas **no** equivale a euros de API. No utilizar ChatGPT Plus como supuesto presupuesto API.
- Preferencia de voces locales gratuitas CPU/RAM y uso no invasivo de VRAM; la síntesis y reproducción sonora se presentan mediante S19.

**Exclusiones:** no decidir hechos Core, permisos S18, rangos F11, física/combate/sensores, ni crear otro servicio IA. Las consultas simples del ordenador (hora, inventario, puerta, estado autorizado) no necesitan LLM.

**Autoridad / dependencias:** HOST transporta, prioriza y cancela; CoreRPG y reglas Star Trek suministran verdad y contexto; S18/visibilidad filtran; S02, S05, S06, S07, S10, S16 y S19 consumen solo cuando haga falta.

**Evidencia/estado:** **idea aprobada + código de servicio compartido parcial** documentado en [HOST IA-01](../../../sistemas/ai/HOST_AI_SERVICE_IA01.md), sin consumidores E2E ni certificación de conexión general en juego. Decisión [OpenAI](../../../sistemas/ai/OPENAI_RUNTIME_DECISION_2026-11-15.md), con ejemplos F10 antiguos sujetos a DEC-0022.

**Futura comprobación:** dos diálogos y un resumen no bloquean Game Thread, cancelan tras LOAD, no filtran conocimiento y las operaciones físicas comunes requieren cero llamadas API.

## S02 — Interacción e interfaces

**Objetivo aprobado:** experiencias LCARS y 3D cómodas para órdenes, consolas, PADD, comunicador, ordenador, texto y voz opcional en castellano.

**Funciones:** una **intención lógica común** para botón, voz o texto con actor/origen/destino; navegación por interfaz, feedback y denegaciones; acceso manual permanente, subtítulos, legibilidad y controles ratón/teclado/mando. UE5 puede presentar una consola en mundo o pantalla completa sin lógica duplicada. Ordenador de la nave común a instalaciones, no chatbot universal ni «otra IA».

**Exclusiones:** S02 no autoriza rutas, puertas, ascensos, objetos ni lectura clasificada. La voz no prueba identidad; un doble clic o reenvío no puede generar dos efectos.

**Autoridad / dependencias:** Core/Fxx validan y ejecutan, S18 decide permisos, HOST enruta, S01 interpreta lenguaje excepcional, UE5 representa; S08/S09/S10/S11/S12/S15/S16 son consumidores de controles.

**Evidencia/estado:** **concepto y documentación de interacción y Starship Computer**, integración uniforme entre formatos no certificada; referencias en sistemas/ai/command_interpretation/ y sistemas/gameplay/ship_operations/ship_computer/.

**Futura comprobación:** orden por botón/voz/texto produce mismo resultado autorizado y un solo efecto; sin micrófono/API las tareas básicas se completan.

## S03 — Universo Vivo

**Objetivo aprobado:** universo persistente y causal que sigue evolucionando aun cuando el jugador no esté presente.

**Funciones:** evolución de facciones, ciencia, colonias, diplomacia, conflictos, crisis y economía con causa/fecha/procedencia. Tres escalas de ejecución conceptual: NPC visible de alta fidelidad, región activa resumida y galaxia lejana por eventos agregados. Reconciliar saltos largos, cambios de sector y SAVE/LOAD sin duplicar sucesos; comunicar solo lo legítimamente observado.

**Exclusiones:** no una segunda base del universo, no «IA generativa por planeta», no un universo UE5 permanentemente renderizado, no encargar a S07 que fabrique hechos para una misión.

**Autoridad / dependencias:** CoreRPG simula y persiste; Planificación 2 define reglas de dominios, HOST coordina calendario/reconciliación, S05/S06/S07/S08/S10/S11/S16 consumen consecuencias, UE5 solo visualiza el fragmento presente.

**Evidencia/estado:** **Planificación 2 B01–B10 documentada con contratos/referencias**; **simulación galáctica real E2E no certificada**. Los detalles de P2 esperan su propia auditoría.

**Futura comprobación:** avance semanas/años y retorno al mismo sector mantienen cronología, identidades, conocimiento y resultados sin clonados; CPU/RAM medidos.

## S04 — Protagonista y carrera

**Objetivo aprobado vigente (DEC-0022):** **único protagonista varón híbrido humano-vulcano**, padre descendiente de Khan, madre vulcana, 45 años en la Academia en **2383**, con biografía, aptitudes marciales/científicas y carácter inicial fijados por el autor. Nombre y cosmética sí configurables; **sin selector libre de especie, sexo, edad o biografía**.

**Funciones:** representar ficha canónica estable y apariencia autorizada; admisión académica mediante autoridad F10 real (la intro institucional con Janeway y Picard **presenta**, no crea plaza); cuatro cursos de Academia hacia 2387 y carrera posterior alférez → teniente junior → teniente → teniente comandante → comandante → capitán, mediante evidencia institucional. Capacidades mejoradas excepcionales pero finitas y consecuencias reales; libertad ética/afectiva/profesional tras origen. Picard impone personalmente galones al alcanzar legítimamente capitán.

**Exclusiones:** no mantener el editor multiespecie como nueva UX, no reescribir contratos LOCKED, no dar destinos/ascensos por genes, prólogo ni guion; la Enterprise-D no se concede automáticamente ni tiene clase Valhalla.

**Autoridad / dependencias:** [DEC-0022](../decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md), F10/F11 y Lore; Core identidad/carrera; HOST coordina; S05/S06/S07/S12/S18 aportan escenas, relaciones y accesos.

**Evidencia/estado:** [S04 v2](../../../sistemas/gameplay/character_creation/S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md) **aprobado en diseño**; antiguo formulario y código F10/H06 parcialmente implementados; **migración v2 no realizada/certificada**. No tocarlos desde SISTEMAS.

**Futura comprobación:** partida nueva tiene ficha fija; guardado antiguo se migra conscientemente; ningún acceso/rango inventado; salto de intro no duplica matrícula.

## S05 — NPC y tripulación

**Objetivo aprobado:** tripulación realmente activa, con guardias, tareas, iniciativa, personalidad y persistencia, no figurantes inmóviles.

**Funciones:** identidad y localización estables; agendas de servicio, descanso y tareas; iniciativa profesional y órdenes/delegación válidas; niveles de detalle por presencia y relevancia. Oficiales NPC se desplazan y cumplen operaciones sin tener al jugador detrás. Lenguaje bajo demanda sin consulta periódica por cada NPC.

**Exclusiones:** no duplifica relación social S06, universo distante S03 ni rangos F11; no crea posiciones simultáneas o acceso automático por atravesar puertas.

**Autoridad / dependencias:** Core y Fxx para rol/orden/tiempo; S03 offscreen; S06 memoria/vínculo; S12 rutas, S18 permisos; S01 diálogo, S19 audio.

**Evidencia/estado:** **contratos, reglas y referencias F04/F05 disponibles**, NPC autónomos integrados en entorno UE5 no certificados de extremo a extremo.

**Futura comprobación:** guardia → relevo → trayecto → actividad independiente → LOAD, misma identidad/posición/acceso y sin dependencia IA para rutinas.

## S06 — Relaciones sociales

**Objetivo aprobado:** amistades, romances posibles, disputas y confianza construidos mediante hechos, tiempo, diálogo y consentimiento del NPC.

**Funciones:** relaciones multidimensionales, preferencias y límites; memoria solo de eventos vividos/observados o comunicados; invitaciones, citas, colaboración, rechazos y evolución real de la relación. Siete de Nueve y los legendarios conservan personalidad, autonomía, agenda y privacidad, sin romance ni amistad garantizados.

**Exclusiones:** no «medidor de cariño» como único decisor, no recuerdos inventados por IA, no divulgar expedientes privados, no forzar aceptación de propuestas ni emitir rangos.

**Autoridad / dependencias:** Core eventos/memorias; S05 agenda, S16 ocio, S12 presencia, S18 privacidad, S02/S01 diálogos, S07 hechos de trama.

**Evidencia/estado:** contratos documentados en sistemas/gameplay/social/, sistemas/gameplay/relationships/ y sistemas/ai/memory/; **experiencia social integral aún no certificada**.

**Futura comprobación:** una conversación privada no circula sin fuente; negativa respetada; cambio de vínculo se registra solo tras hecho válido.

## S07 — Misiones y narrativa

**Objetivo aprobado:** historias, temporadas y emergencias nacidas de un universo real y una vida de a bordo predominantemente tranquila.

**Funciones:** seleccionar oportunidades narrativas según hechos/órdenes/rango/conocimiento y presentar investigaciones, aventuras, episodios y arcos. Mantener crisis y combates excepcionales, no crisis constantes. Borg, Siete y exploración Delta son **contenido**, Directiva Omega es incidente raro y **Q/Continuo Q queda excluido** conforme a las decisiones vigentes. Órdenes de Flota llegan por comunicaciones y autoridad legítimas.

**Exclusiones:** no mutación retroactiva de entidades, no director que conceda poderes, no duplicar simulación S03 ni generar tragedias artificiales por calendario.

**Autoridad / dependencias:** Core causalidad/persistencia; S03 hechos, Fxx/F11 cadena institucional; S05/S06 reparto, S08/S09/S10/S13 experiencias, S01 lenguaje, HOST entrega, UE5 representación.

**Evidencia/estado:** arcos y contratos documentados; **director narrativo jugable integrado no certificado**.

**Futura comprobación:** misión pospuesta no crea hechos incompatibles ni ignora permisos; sucesos extraordinarios no interrumpen escenas sin causa.

## S08 — Vuelo y navegación

**Objetivo aprobado:** viajar como oficial en nave Starfleet y coordinar pilotos NPC sin convertir operaciones cotidianas en minijuegos obligatorios.

**Funciones:** rutas, ETA, riesgos, maniobras, impulso/warp y ejecución autorizada conforme a capacidades de nave, cartografía y órdenes; pilotos NPC profesionales; persistencia del tránsito. S11 puede proponer una ruta y S08 valida/canaliza su ejecución.

**Exclusiones:** no otro mapa galáctico, no movimiento por pulsación sin autoridad, no reglas redundantes de propulsión/órdenes.

**Autoridad / dependencias:** Core estado/movimiento; Trek Fxx navegación/propulsión y F11 mandos; S02 controla entrada, S10 observa, S11 propone, S05 pilotos, HOST coordina.

**Evidencia/estado:** contratos y referencias de navegación/órdenes; **operación completa UE5 no certificada**.

**Futura comprobación:** un cadete propone ruta sin mover nave; orden válida activa tránsito; cancelación/LOAD mantienen coherencia.

## S09 — Combate espacial

**Objetivo aprobado:** encuentros tácticos con defensas, daño y disuasión, sin degradar arbitrariamente la Enterprise-D refit ni hacerla inmortal.

**Funciones:** táctica naval, escudos, armamento, torpedos, reglas de enfrentamiento, retirada y negociación; conducta NPC según riesgo/objetivos/reputación; daños que afectan sistemas reales. La **superioridad DEC-0021** y prestigio de la Enterprise-D se aplican solo si la configuración consta realmente operativa; adversarios pueden temerla o atacarla por motivos coherentes.

**Exclusiones:** no disparar por clic sin permiso, no segundo núcleo de combate, no cargueros convertidos en iguales de un buque insignia por balance artificial ni enemigos suicidas por obligación.

**Autoridad / dependencias:** Core y reglas Star Trek para combate/daños; F11 autoridad, S08 maniobra, S10 contactos, S05 tripulación, S07 motivación narrativa, S19 alertas y SFX.

**Evidencia/estado:** diseño y contratos de seguridad/táctica/daños; **combate espacial UE5 completo no certificado**.

**Futura comprobación:** retirada razonable, disparo denegado sin autoridad y daño persistente con sensores coherentes.

## S10 — Sensores y exploración

**Objetivo aprobado y corrección vinculante DEC-0021:** en la **USS Enterprise NCC-1701-D reconstruida**, cuando el refit de sensores está instalado/operativo y un objetivo es ordinario y detectable, **una petición manual o automática basta para informe completo, correcto y prácticamente inmediato**, no una sucesión artificial de filtros, temporizadores o barridos fallidos.

**Funciones:** vigilancia automática, clasificación/identificación, solicitudes manuales de escudos, armamento, sistemas, trayectorias y barridos científicos dentro de conocimiento observable; perfiles precalculados y consulta a WorldState; registro de observación/procedencia. Fenómenos extraordinarios, camuflaje o daño real sí pueden limitar resultados.

**Exclusiones:** no probabilidades de «0,1 % de fallo» aplicadas a cada lectura, no análisis trivial de 90 segundos, no inventar información vía LLM, no convertir mapas S11 ni conocimiento universal en sensores.

**Autoridad / dependencias:** Core hechos y conocimiento, capacidad/estado de sensores, Ciencia especializada; S02 interfaz, S08 navegación, S09 táctico, S11 visualiza, S01 solo redacta si necesario.

**Evidencia/estado:** [DEC-0021](../decisions/enterprise_d_valhalla_superioridad_sensores_reputacion_2026-11-17.md), F06/contratos/prototipos acotados; **doctrina de refit completa no certificada**.

**Futura comprobación:** contacto ordinario detectable ofrece informe completo en solicitud única (objetivo orientativo ~1 s, a medir), mientras anomalía genuina indica limitación fundada; no filtra secreto.
