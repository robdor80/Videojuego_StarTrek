# Fichas S11–S19 — formalización conceptual

**Ámbito exclusivo:** SISTEMAS · **Fecha:** 19-11-2026 · **Referencias:** [auditoría](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md), decisiones autorales DEC-0020–0024 y acuerdos conversacionales S12–S19.

Son **fichas de definición y límites**, no fases ejecutivas ni certificaciones de UE5. El detalle aprobado del sistema prevalece sobre propuestas técnicas no aprobadas y documentos históricos que contradigan decisiones posteriores.

## S11 — Astrometría 360°

**Objetivo aprobado:** sala holográfica tridimensional 360° de la Enterprise-D modernizada, bella y científicamente útil, con cartas/objetos y exploración interactiva a **cuatro escalas**.

**Funciones:** mapa multiescala de galaxia/zonas/sistemas/cuerpos, zoom, selección, órbitas y comparación de objetos como Tierra/Vulcano; datos reales con fuentes y unidades, conocimiento por observador, filtros de autorización, situación política/temporal procedente y vistas hipotéticas etiquetadas. Puede **proponer** a S08 una ruta con preferencias; no ejecutarla. Controles LCARS/in-world y voz opcional. Renderizar con instancias, LOD, carga bajo demanda y coordenadas relativas sin suponer Z=0 para toda la galaxia.

**Exclusiones:** no construir un segundo universo, inventar planetas o datos, revelar todo el Cuadrante Delta, asignar permisos ni mover la nave desde el holograma. No inventar aún ubicación o puerta de la sala sin diseño S12.

**Autoridad / dependencias:** CoreRPG verdad/conocimiento; S10 sensores, Ciencia interpretación, S08 rutas reales, S18 permisos, S02 input/LCARS, S12 ubicación física, HOST proyección, UE5 visualización Galaxy Refit A2.

**Evidencia/estado:** [DEC-0023](../decisions/s11_astrometria_360_2026-11-18.md), [diseño y contratos](../../../sistemas/gameplay/astrometrics/README.md), status **DESIGN_APPROVED_NOT_RUNTIME**. Ninguna sala holográfica ejecutable o rendimiento certificado.

**Futura comprobación:** cuatro escalas, zoom 360°, comparación Tierra/Vulcano, propuesta de ruta no ejecutable sin orden, datos filtrados y FPS/latencia medidos en UE5.

## S12 — Interiores, desplazamiento y geolocalización

**Objetivo aprobado:** caminar y vivir en la nave como espacio real, con puertas, ascensores y trayectos de jugador/NPC coherentes.

**Funciones:** recorridos transitables por sectores/cubiertas, localización precisa de salas, grafo/mapas LCARS coherentes con mallas y colisiones, desplazamiento NPC realista; **puertas públicas automáticas por proximidad** y **privadas mediante pulsador/timbre**, consultando S18. Turboascensor por destino expresado naturalmente: llegar a la **parada practicable más cercana** y después recorrer a pie hasta la habitación, sin salida mágica frente a la puerta. El puente de batalla está fuera de la geometría principal de cubiertas y su acceso es una **transición virtual válida**, no un corredor inexistente.

**Exclusiones:** S12 no autentica ni autoriza personas (S18), no crea/decora todos los interiores Blender, no materializa conexiones físicas falsas y no sustituye a S05 como planificador social. Un mapa Blender no equivale a nivel UE5 jugable.

**Autoridad / dependencias:** Core posición/identidad/tiempo, S18 política de entrada, S05 agendas, S02 ordenador y rutas, S16 ocio, S19 SFX de puertas/ambientes, Ingeniería daños/energía; UE5 física, colisiones, triggers y navegación. Respetar cubiertas y estilo Galaxy Refit A2 sin editar recursos originales.

**Evidencia/estado:** concepto aprobado; se conoce rama separada de diseño S12 sin fusión acreditada en main, con ajustes recientes del límite S18. Prototipos/corredores y pruebas Sutherland **reportadas**, no integridad UE5 certificada.

**Futura comprobación:** camarote → pasillo → ascensor → parada → tramo a pie al destino, puertas públicas/privadas por actor correcto, movimiento NPC y guardado/carga sin paredes atravesadas ni bloqueos.

## S13 — Exploración de escenarios planetarios

**Objetivo aprobado:** misiones de superficie en **zonas 3D limitadas pero muy bien realizadas**, con ciencia, arqueología, contactos, misterios y descubrimientos.

**Funciones:** entornos seleccionados (ruinas, bosques, cuevas, instalaciones, enclaves científicos) con navegación real, objetos y NPC; desembarco por transportador o lanzadera cinemática, vuelta a nave y continuidad de investigación/objetos/estado. Reutilizar recursos 3D y procedural controlado donde mantenga calidad.

**Exclusiones:** no ofrecer «cualquier planeta íntegramente explorable» ni mundo abierto planetario ilimitado; rover pilotable o lanzadera manual **solo si alcanza calidad muy alta** y como opción posterior, no obligación que bloquee el sistema.

**Autoridad / dependencias:** Core y S03 mundo persistente, S07 misiones, S10/Ciencia, S15 objetos, S05 equipo de desembarco, S18 seguridad, S12 transiciones; UE5 niveles y Blender/NAP assets.

**Evidencia/estado:** **idea aprobada**, recursos y contratos de exploración/expediciones; escenarios 3D jugables E2E **no certificados**.

**Futura comprobación:** zona limitada transitable, investigación real, hallazgo y retorno, sin regenerar planetas ni perder objetos al cargar; calidad visual juzgada en juego.

## S14 — Holocubierta

**Objetivo aprobado:** disfrutar de **mundos holográficos predefinidos, bellos y explorables**, solos o con NPC, para ocio y eventualmente formación.

**Funciones:** programas de playa/oceáno, jardines, bosques, montañas, lagos, cabaña nevada u otros escenarios preparados; paseo, relajación, compañía, sonido y pequeñas interacciones. Entrada/salida con permiso, distinción estricta de holograma y mundo real, simulaciones de entrenamiento sin otorgar mérito por sí solas. Compartir recursos útiles con S13.

**Exclusiones:** no generación visual ilimitada mediante IA, no exigir simuladores de esgrima, vuelo o deportes completos, ni trasladar objetos/PNJ holográficos a inventario real o eventos Starfleet sin validación.

**Autoridad / dependencias:** Core distingue estado REAL/HOLÓGRAFO, S12 recinto y salida, S18 reservas, S05/S06 invitados, S16 ocio, S15 objetos, S19 paisajes sonoros, UE5 escenarios.

**Evidencia/estado:** **idea y experiencia aprobadas**; no runtime certificado de programas ni aislamiento estado real/simulado.

**Futura comprobación:** entrar, explorar, convivir, salir, SAVE/LOAD; ningún objeto simulado se vuelve real y ninguna evaluación falsa produce ascenso.

## S15 — Objetos, equipamiento, capacidades y custodia

**Objetivo aprobado:** objetos 3D que se pueden coger, sujetar, usar, dejar, transferir, guardar, replicar o consumir, con capacidades Star Trek creíbles y persistencia individual.

**Funciones:** catálogo de **tipos** e **instancias** con identificador único, propietario, ubicación, custodia, historial y condición; límites de transporte/equipamiento; tricórders, PADD, fásers, armas, útiles médicos, bebidas, alimentos y artefactos recuperados. Replicador sujeto a patrones, materiales/energía, permisos y reglas del mundo; consumo de comida/bebida retira la instancia con evento registrado. Almacenamiento en armería/laboratorio y cadena de custodia para artefactos científicos/alienígenas.

**Exclusiones:** no inventario Core duplicado, no crear artefactos restringidos arbitrariamente; tricórder no detecta una nave romulana camuflada desde el planeta ni fáser de mano destruye un crucero; las físicas avanzadas de cada objeto distante no son obligatorias.

**Autoridad / dependencias:** Core identidades y transacciones, contrato existente en sistemas/gameplay/inventory/persistent_unique_object_contract.json; S18 permisos, S02/S12 interacción, S10/Ciencia capacidades, S09 combate, S13 hallazgos, S16 replicación/ocio, UE5 modelos y animación.

**Evidencia/estado:** **idea aprobada + contratos de objetos e inventario**; ciclo integral UE5/custodia no certificado.

**Futura comprobación:** equipo replicado autorizado, denegado si restringido; recoger/transferir/consumir/cargar sin clonaciones, capacidades verificadas.

## S16 — Vida a bordo

**Objetivo aprobado:** una nave que sea **hogar y comunidad**, con actividades significativas fuera de servicio en la cubierta E, camarotes, comedores, Ten Forward y otros lugares.

**Funciones:** rutina de guardia, descanso, alimentación, higiene y ocio sin micromantenimiento obligatorio; charlas, citas, paseos, convivencia y cenas con NPC. Replicadores de bebidas/comidas mediante S15, seleccionables en interfaz y consumibles. Música reproducible en camarote desde biblioteca propia (MP3 y FLAC locales, soporte USB/importación por estudiar, Spotify solo hipótesis sin promesa); piano 3D en Ten Forward con gesto sentado/manos y melodías pregrabadas, **sin animación individual de dedos**. Juegos S17 y holocubierta S14 como actividades integradas. Continuidad de agenda/bienestar/interrupciones.

**Exclusiones:** no barras survival tediosas, no duplicar el motor de relaciones, minijuegos, audio o inventario; no obligar al jugador a jugar al póquer o escuchar música para progresar.

**Autoridad / dependencias:** Core bienestar/tiempo/eventos; S05 NPC y turnos, S06 relaciones, S12 cubiertas, S14 holo, S15 objetos, S17 reglas de juego, S18 privacidad, S19 audio, S02 controles. IDEA-0002 gobierna biblioteca local.

**Evidencia/estado:** **idea aprobada**, contratos y catálogo en sistemas/gameplay/ship_operations/shipboard_life_state_contract.json y off_duty_activity_catalog_v0.1.json. No experiencia de ocio UE5 completa certificada.

**Futura comprobación:** de guardia a ocio y vuelta, invitación o consumo físico real, música espacial y piano si se seleccionan, interrupción por alerta y SAVE/LOAD; experiencia placentera sin rutinas vacías.

## S17 — Minijuegos

**Objetivo aprobado:** partidas recreativas reales contra NPC, conectadas a vida social y no una colección de interfaces falsas.

**Catálogo objetivo para empezar a jugar:** **ajedrez clásico, damas, póquer y mus**. **Pocha y tute** son candidatos a actualizaciones posteriores, no compromisos del lanzamiento. No se aprueban billar/dardos/deportes como parte obligatoria.

**Funciones:** plataforma común para iniciar, configurar niveles, turnos, guardar/interrumpir/reanudar y resolver partidas, con motores de reglas **por juego**. Ajedrez para principiantes con ayudas y dificultad regulable; damas auténticas; póquer con modalidad por confirmar (Five-Card Stud como preferencia de coherencia TNG); mus español por parejas con descartes, grande/chica/pares/juego, envites, órdagos, señas y compañero/rivales con información limitada y personalidad. Evaluar motor existente frente a portar o desarrollar: Stockfish, PokerTH, go_trumpcards, PC Mus/Mus 2000 son **referencias a analizar**, no elección de implementación sellada.

**Presentación:** NPC sentados, miradas, reparto/cogida de cartas mediante animaciones y cambio dirigido de malla/posición, cámaras de mesa legibles; no simular físicamente cada carta ni animar dedos uno a uno. Pack de Fab para animaciones es candidato, sin compra acordada.

**Exclusiones:** no llamadas IA por movimiento ni árbitro LLM, no apuestas de dinero real, no convertir un minijuego en proyecto de meses ni reclamar motores integrados sin prueba. Si portar un motor Go a C++ desperdicia cuota Codex, escoger otra solución viable.

**Autoridad / dependencias:** reglas locales deterministas con eventos Core; S05/S06 NPC sociales, S12/S16 lugar/ocasión, S15 props, S19 audio, S02 interfaz, UE5 representación.

**Evidencia/estado:** **idea aprobada**, estudios y candidatos; ninguna partida completa UE5 integrada/certificada por esta revisión.

**Futura comprobación:** cuatro juegos completos, reglas correctas, bots que «den el pego», niveles razonables, interrupción y carga sin trampas ni consumo de API para decidir cada jugada. La modalidad exacta de póquer, variantes de damas/mus y elección de motores se deciden al desarrollar.

## S18 — Identidad, autenticación y control de accesos

**Objetivo aprobado DEC-0024:** saber qué personaje realmente solicita un acceso y si dispone de derecho vigente, sin crear cuentas reales o duplicar identidad de Core.

**Funciones:** resolución confiable de actor desde sesión y PERSON, verificación de credenciales diegéticas cuando corresponda y política determinista de acceso a camarotes, despachos, laboratorios, zonas restringidas. Residentes/corresidentes, invitaciones, expiración, revocación, escoltas, mantenimiento autorizado, emergencia/evacuación con causa verificable. Privacidad: ser capitán **no abre automáticamente todos los camarotes**; uniforme, mera voz o proximidad no autentican por sí solos. Si S18 autoriza, S12 aún puede reportar imposibilidad física por avería, falta de energía o bloqueo.

**Exclusiones:** S18 no crea personajes, cargos, residencias ni autoriza órdenes tácticas fuera de ámbito; no mueve personaje, no anima hoja de puerta ni abre automáticamente un privado por trigger; no depende de IA para cada decisión.

**Autoridad / dependencias:** Core identidad/permisos/tiempo, dominios F11/Seguridad/Medicina/Ingeniería, HOST canal, S02/S05 petición, S12 mecanismo, S15/S16 acceso a pertenencias y camarotes.

**Evidencia/estado:** [DEC-0024](../decisions/s18_identidad_autenticacion_control_accesos_2026-11-18.md), [diseño y contratos](../../../sistemas/gameplay/access_control/README.md); status técnico dice **runtime no implementado**. S12 no lo certifica.

**Futura comprobación:** pública automática/privada manual, invitado válido y caducado, revocación, denegación sin revelar intimidad, emergencia trazada, actor NPC correcto, fallo mecánico y SAVE/LOAD.

## S19 — Audio, música y ambientación dinámica

**Objetivo aprobado 19-11-2026:** una coordinación sonora única, no un reproductor por sistema. **Prioridad de efectos sonoros sobre la música** y umbral de calidad absoluto: si la música ambiental no queda bien, no se introduce hasta resolverlo.

**Funciones:** eventos válidos → efectos de puertas, fásers, torpedos, transportadores, motores, LCARS y alertas; ambientes por lugar; voces/comunicaciones con prioridad de inteligibilidad; reproducción/detención, mezcla, espacialización, atenuación/oclusión y transiciones contextualizadas. Música de fondo **opcional y condicionada a calidad**, no requisito para declarar satisfactorio el bloque de efectos. Diferenciar banda sonora, música localizada en camarote, piano en Ten Forward y efectos. Soportar conceptualmente biblioteca personal local MP3/FLAC por vinculación de carpetas sin duplicar archivos (IDEA-0002), sin subir audios a la API, GitHub o nube; decodificación runtime en build pendiente de comprobar. TTS de NPC gratuito/local CPU/RAM si viable, sin impacto significativo en VRAM ni obligación de clonar voces.

**Exclusiones:** S19 no genera hechos ni decide si empieza un combate, no desarrolla un nuevo mezclador que UE5 ya ofrece, no proporciona automáticamente bandas sonoras profesionales ni música de Spotify, no inventa emociones por reproducir pistas.

**Autoridad / dependencias:** Core/S03–S18 emiten eventos con contexto; S02 entrada; S01 lenguaje cuando proceda; S05 diálogos, S12 espacios y puertas, S16 ocio; HOST coordinación de eventos; UE5 Audio Mixer/MetaSounds/emisores. F14 prepara activos audiovisuales en otro pilar, sin alteración aquí.

**Evidencia/estado:** **idea aprobada** y [ficha dedicada](S19_AUDIO_MUSICA_AMBIENTACION_DINAMICA_2026-11-19.md); [IDEA-0002](../../ideas/IDEA-0002_biblioteca_musical_personal.md) documentada. No gestor general de sonido integrado/certificado.

**Futura comprobación:** SFX funcional de puerta/alarma/disparo con posición real y prioridades de voz; música solo si es buena; biblioteca privada sin subidas; mediciones CPU/GPU/VRAM y pruebas en build. No usar la ausencia de música opcional para fingir que SFX no tiene valor.

---

## Reglas de formalización comunes

- **CoreRPG es la verdad**, reglas específicas de Star Trek/Fxx son dueñas de permisos y efectos según dominio, **HOST coordina**, **UE5 presenta**. Las entradas se validan una sola vez y no mutan por el texto de una IA.
- Estado de estos 19: **conceptos aprobados; diseños, contratos y componentes parciales de madurez variable**. Este documento no certifica integración.
- Las «futuras comprobaciones» son criterios conceptuales para cuando se implementen, no una petición de escribir suites ahora.
- El lenguaje de planificación técnica detallada, prioridades de Fxx y cambios de Lore/HOST/P2 quedan fuera de esta conversación y se transmiten mediante la [matriz de dependencias](MATRIZ_TRANSVERSAL_Y_PENDIENTES_S01_S19_2026-11-19.md).
