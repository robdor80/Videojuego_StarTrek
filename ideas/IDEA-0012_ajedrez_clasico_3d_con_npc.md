# IDEA-0012 — Ajedrez clásico 3D con NPC, aprendizaje y vida social a bordo

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación conceptual:** 24 de octubre de 2026  
**Estado:** **APROBADA CONCEPTUALMENTE; documentación registrada, implementación y pruebas pendientes**  
**Autoridad:** solicitud expresa del autor en conversación de diseño; confirma el ajedrez clásico como alternativa jugable al ajedrez tridimensional característico de Star Trek.  
**Repositorio:** `robdor80/Videojuego_StarTrek`  
**Destino:** `ideas/IDEA-0012_ajedrez_clasico_3d_con_npc.md`  
**Ámbito:** vida a bordo, ocio interactivo, amistad con NPC, tablero y piezas 3D, enseñanza de reglas, Unreal Engine 5, CoreRPG y persistencia.  
**Contexto de uso:** videojuego personal, local, destinado al ordenador del autor, sin publicación ni comercialización prevista.

## 1. Visión aprobada

El jugador podrá **quedar y jugar partidas auténticas de ajedrez clásico** con un amigo o compañero NPC, en espacios adecuados de la Academia, estaciones o naves del universo Star Trek; especialmente en el bar/sala común o en un camarote de la **Clase Valhalla**.

La actividad constituye **vida social jugable real**, no una opción de diálogo que declare «hemos jugado una partida» sin resolverla. Se desea conversar, compartir tiempo de ocio, desarrollar familiaridad y, si las circunstancias/personas lo permiten, profundizar una amistad de forma causal.

**Activos ya descargados por el autor (pendientes de auditoría en MSI):**
- Modelo 3D de un tablero de ajedrez **clásico de madera**, elegido por su belleza visual.
- Modelos 3D de **piezas blancas y negras**.

No se da por acreditada su calidad de importación, dimensiones, rutas ni disponibilidad dentro de UE5 hasta que se revisen los archivos locales.

**Principio rector:** incorporar un minijuego de ajedrez completo y accesible, usando modelos tridimensionales reales, con la mínima complejidad de animación de personajes necesaria.

## 2. Ajedrez clásico, NO ajedrez tridimensional de Star Trek

El autor conoce el **ajedrez tridimensional** característico de Star Trek, con varios tableros/plataformas dispuestos a distintas alturas, pero **no desea tener que aprender esas reglas** para disfrutar del ocio con sus NPC: tampoco conoce todavía las reglas del ajedrez convencional.

**Decisión aprobada:** utilizar un **tablero clásico de 8 × 8 casillas y reglas ordinarias de ajedrez**, presentado como un pasatiempo humano tradicional que los tripulantes pueden disfrutar en la ficción de Star Trek. Funciona como **alternativa jugable y complemento** al ajedrez tridimensional que aparece en las series; no hace falta eliminar del lore o de la decoración la existencia de esa variante.

La posible implementación del ajedrez tridimensional específico de Star Trek queda **fuera del alcance** de esta idea y requeriría un diseño y unas reglas propias en el futuro.

## 3. Experiencia del jugador: cámara centrada en el tablero

**Flujo jugable aprobado:**

1. El jugador tiene tiempo libre o encuentra a un NPC disponible para invitarlo a jugar.
2. Pueden acordar una partida en un bar, sala común, camarote u otro lugar con mesa adecuada; también el NPC puede proponerla por iniciativa propia.
3. Ambos personajes se sitúan o se consideran sentados en la mesa; no es necesario implementar una compleja animación corporal de sentarse como requisito del ajedrez. Respetar los sistemas de colocación/sillas cuando existan.
4. Al seleccionar «Iniciar partida», **la cámara pasa a una vista dedicada en primera persona/perspectiva desde los ojos del jugador**, con el **tablero 3D ocupando casi toda la pantalla** y perfectamente legible.
5. El jugador utiliza el **ratón** para seleccionar una de sus piezas y una casilla destino; se pueden iluminar las jugadas legales y, opcionalmente, arrastrar la pieza.
6. El sistema comprueba el movimiento, mueve la **pieza 3D directamente** con una animación suave de desplazamiento y resuelve las capturas/cambios.
7. El **motor de ajedrez** calcula una jugada para el NPC y mueve automáticamente la pieza rival. **No hace falta mostrar brazos, manos ni dedos del NPC tocando físicamente las piezas.**
8. Se repite el proceso hasta fin de partida, aplazamiento o interrupción justificada.
9. Al salir de la cámara dedicada, el jugador vuelve a su vista de vida a bordo con el mismo NPC, localización y continuidad temporal.

**No se exige:** captura de movimiento, IK de manos/dedos, animaciones de agarre, sincronización de extremidades, cámara obligatoria mostrando cuerpos completos, ni simulador físico de piezas sujetadas por personajes.

**Opcional después:** sonidos discretos de madera, sombras/reflejos, animación ligera de captura/promoción, pequeñas reacciones de voz del NPC, orientación de tablero según bando y transición de cámara agradable.

El tablero sigue siendo **3D**: no se sustituye por una interfaz 2D plana como solución final.

## 4. Motor de ajedrez: reutilizar software, no inventar la inteligencia desde cero

El futuro sistema constará de tres responsabilidades separadas:

1. **Reglas y estado de ajedrez:** turnos, movimientos legales, captura, jaque, jaque mate, ahogado, tablas y jugadas especiales. El motor de reglas no depende de mallas UE5 ni de un NPC humanoide.
2. **Oponente ajedrecístico:** componente o motor local que evalúa el tablero y elige una jugada legal según el nivel seleccionado.
3. **Presentación UE5:** representación del tablero/piezas, selección con ratón, animaciones automáticas, HUD/tutorial y cámara dedicada.

Se recomienda evaluar un **motor de ajedrez existente de ejecución local** (por ejemplo Stockfish u otra alternativa) o una biblioteca C++ para reglas y un adversario simplificado para principiantes, según facilidad de integración, compatibilidad con Windows, rendimiento y comportamiento a nivel bajo.

**No requiere conexión a internet, Gemini, IA generativa ni servicios remotos por jugada.** La IA conversacional del NPC solo presenta diálogos o reacciones basados en el resultado real; nunca debe inventar movimientos o resultados que no hayan sido validados.

**No decidir aún un motor/biblioteca definitiva ni afirmar que exista integración UE5.** Es una decisión técnica para implementación posterior.

## 5. Dificultad accesible para quien no sabe jugar

El usuario manifiesta que **parte de nivel cero**. El ajedrez debe poder aprenderse durante la experiencia, sin obligar a estudiar las reglas de antemano ni someterlo a un rival imbatible.

Niveles de diseño propuestos:

| Nivel | Comportamiento y ayudas |
|---|---|
| **Aprendiz absoluto / tutorial** | Explicaciones sencillas en castellano, nombres de piezas, turnos, movimientos permitidos resaltados, ayuda contextual, partidas guiadas y sin reloj. |
| **Principiante** | NPC deliberadamente débil o con errores controlados, sin trampas ni movimientos ilegales; tiempo ilimitado. |
| **Aficionado** | Juego normal con fuerza moderada y ayudas opcionales. |
| **Avanzado** | Estrategia más exigente y menor cantidad de errores. |
| **Experto** | Rival fuerte para quien quiera un desafío. |

En los niveles bajos **no basta con bajar un número de Elo de forma nominal**: probar que la IA realmente resulte ganable y comprensible para una persona que está aprendiendo. Puede ser más conveniente usar decisiones simples/selección restringida de jugadas que un motor profesional mal debilitado.

**Ayudas elegibles:** mostrar casillas válidas, explicar qué es jaque, vista del último movimiento, sugerencia opcional, «por qué no puedo mover aquí», deshacer en partida amistosa cuando se permita, sin cronómetro y opción de elegir color.

**Reglas completas por fase de madurez:** enroque, captura al paso, promoción, jaque mate, ahogado y causas normales de tablas. No declarar «ajedrez completo» si faltan reglas esenciales.

## 6. NPC y relación social: el atractivo principal

Se jugará con **personajes persistentes auténticos**, no con «bots genéricos» que reemplazan al NPC al empezar la partida.

- Invitación del jugador al NPC o invitación voluntaria del NPC.
- Disponibilidad real según guardia, descanso, lugar, ánimo, obligaciones y preferencias; el NPC puede **aceptar, rechazar o proponer otro momento**.
- Elección de lugar: bar/sala común o camarote cuando existan y sean accesibles.
- Personalidad y aficiones ajedrecísticas diferentes: NPC más paciente, competitivo, metódico, sociable o pedagógico, independientemente de especie o estereotipos automáticos.
- Dificultad elegida por el jugador como preferencia de **accesibilidad de juego**; no altera arbitrariamente sus talentos profesionales o sus características generales en el World State.
- Comentarios y reacciones del NPC proporcionales al estado/resultado, sin narrar victorias o jugadas que no ocurrieron.
- Persistencia de invitaciones aceptadas, partidas terminadas y resultados reales en el historial común.

**Importante: no se ganan puntos automáticos de amistad simplemente por jugar o vencer.** El proyecto ya distingue **familiaridad, afinidad, confianza, amistad, historia compartida y relaciones profesionales**. Compartir una partida es un **evento social auténtico**, cuya consecuencia dependerá de personalidad, preferencias, trato, contexto, conducta, continuidad y sistema social. Perder o ganar puede influir en el diálogo, pero ni fuerza amistad ni destruye una relación.

Tampoco se fuerza al NPC a jugar por autoridad profesional del jugador: una invitación social sigue siendo voluntaria.

## 7. Interrupciones y guardado de partidas

Se podrá **pausar y continuar la misma partida**, incluyendo cuando la actividad se interrumpa por:
- guardia o llamada al puente;
- alarma, emergencia, misión, lesión o indisponibilidad del espacio;
- decisión voluntaria de guardar/aplazar;
- abandono legítimo del NPC y nueva cita compatible.

La partida tiene **ID único**, referencias persistentes a los dos participantes, tablero y ubicación lógica, bando/turno, historial de movimientos, estado reglamentario, nivel/ayudas elegidas, fecha y motivo de aplazamiento. Considerar representación estándar como **FEN** para una posición y **PGN** o lista de jugadas para el historial, verificando casos no capturados por una sola cadena FEN.

Las entidades no pueden estar a la vez de guardia en el puente y jugando en el bar. **Pausar no congela el resto del universo**: la campaña continúa, cambian turnos/horarios y puede ser necesario acordar una nueva sesión.

Guardar/cargar y reabrir la partida no debe duplicar personajes ni piezas lógicas, cambiar el turno ni regalar victorias. Si un NPC se traslada, desaparece o ya no está disponible, conservar la partida con estado de aplazamiento/abandono resuelto según las reglas sociales, no teleportarlo para jugar.

## 8. Integración con espacios 3D e interfaz

**UE5 deberá**:
- Importar y evaluar tablero de madera y dos juegos de piezas existentes (UV, materiales, pivotes, escala y colisiones/clics), preservando originales.
- Identificar programáticamente las **64 casillas** de un tablero normal; asociar piezas 3D a identidades y posiciones reglamentarias.
- Permitir ratón para seleccionar/arrastrar o seleccionar origen y destino, sin necesidad de controller físico de manos.
- Resaltar jugadas posibles, capturas, último movimiento y jaque cuando proceda, sin tapar la estética del tablero.
- Tener cámara cercana, legible en pantalla de PC; adaptar encuadre, ángulo y sensibilidad a monitor 2560×1600.
- Animar transformaciones de piezas del origen a destino de forma sencilla y determinista, sin requerir agarrarlas.
- Gestionar transiciones hacia y desde la escena de mesa, evitando recargas innecesarias de la nave.
- Ofrecer HUD discreto para nombre del adversario, turno, nivel y acciones de ayuda/abandono/aplazamiento.

**Localizaciones candidatas:** bar, salas recreativas, camarote propio o camarote de un compañero donde se permita entrar, Academia y otras naves/estaciones con zona de ocio. No limitarlo a Valhalla ni colocar una mesa inexistente en todos los buques.

## 9. Relación con sistemas y contratos ya presentes en el repositorio

### Referencias documentales existentes, verificadas al registrar

- [Catálogo de ocio a bordo](../gameplay/ship_operations/off_duty_activity_catalog_v0.1.json): **ya tiene** la actividad `games_cards_chess` con requisito de espacio social o privado y familia `recreation`. IDEA-0012 es su **versión interactiva real**, no un catálogo paralelo.
- [Vida a bordo](../gameplay/ship_operations/shipboard_life_state_contract.json): el ocio consume tiempo, espacio y disponibilidad y puede interrumpirse por alertas.
- [Agenda de actividades](../gameplay/characters/activity_schedule_model.json): invitaciones, reuniones y continuación requieren horarios compatibles, sin NPC teletransportados.
- [Reglas de eventos sociales](../gameplay/social/social_event_rules.json) y [simulación social](../gameplay/social/README.md): `social_invitation`, `social_activity`, eventos persistentes y progresión multidimensional de relaciones; evitar puntos de amistad automáticos.
- [F12 — Vida a bordo, NPC y relaciones](../docs/roadmap/master/fases/F12/README.md): ámbito principal de la futura integración social y continuidad.
- [IDEA-0006 — Temporadas narrativas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md): ocio real entre episodios, sin obligación de convertir cada partida en misión.
- [Buzón oficial de ideas](BUZON.md): registro y planificación, sin implementación automática.

### Responsabilidades

| Módulo | Qué le corresponde |
|---|---|
| **Juego Star Trek** | Reglas concretas de actividad social/ajedrez en contexto de Academia, naves, NPC, ocio y requisitos por lugar. |
| **Módulo de ajedrez local** | Tablero lógico, reglas, movimientos legales, decisión del rival, dificultad y serialización de partida. Sin lógica de Flota Estelar incrustada. |
| **CoreRPG genérico** | Identidades, reloj, permisos, agendas, eventos, persistencia y relaciones cuando los contratos realmente disponibles así lo permitan. No introducir ajedrez específico como obligación del núcleo RPG común. |
| **Unreal Engine 5** | Actores 3D, tablero/piezas, cámara, clics, materiales, animación visual y UI. |
| **IA conversacional** | Invitaciones y diálogo contextual sobre hechos autorizados; no calcula ni confirma movimientos arbitrarios. |

## 10. Implementación incremental propuesta — CHESS-01 a CHESS-07

1. **CHESS-01 — Inventario y prototipo visual:** auditar tablero/piezas descargadas; identificar pieza/casilla, pivotes, materiales, dimensiones; crear escena de mesa 3D de prueba sin alterar modelos originales.
2. **CHESS-02 — Reglas y turnos:** integrar biblioteca/reglas de ajedrez; pruebas de todos los movimientos, finales y posiciones especiales.
3. **CHESS-03 — Interacción 3D:** selección de pieza con ratón, destino legal, movimientos/capturas animados mediante transformación, cámara ampliada estable.
4. **CHESS-04 — Rival y niveles:** motor local o IA simple con varios niveles, en especial **principiante real** y ayuda/tutoría; partidas con NPC sin animaciones corporales obligatorias.
5. **CHESS-05 — Persistencia de partida:** guardar/cargar y continuar partida aplazada, turnos e historial correctos, compatibilidad con cambios de escena/cámara.
6. **CHESS-06 — Vida social y agenda NPC:** invitaciones, encuentro en lugares válidos, horarios, respuestas NPC, resultados verdaderos e influencia social causal según reglas existentes.
7. **CHESS-07 — QA e integración:** pruebas UE5 en MSI, rendimiento, UX del modo aprendizaje, interrupciones por alerta, naves/bares/camarotes, guardados, NPC con agenda incompatible y campaña persistente.

**Orden de ejecución ajustable** si conviene probar primero el motor aislado del UE5. Estas etapas son hitos candidatos, **no fases ejecutadas** ni autorización para abrir trabajos 3D en medio de prioridades superiores.

## 11. Criterios de aceptación futuros

1. Tablero **8×8 de ajedrez clásico** y modelos 3D de madera/piezas del autor visibles e interactivos.
2. El jugador puede iniciar una partida con NPC presente y disponible, encuadrar el tablero y mover piezas con el ratón sin animar sus brazos.
3. El NPC responde con movimientos válidos sin animación de manos/cuerpo, con niveles que realmente permitan empezar desde cero.
4. El tutorial explica reglas en castellano, ofrece sugerencias/casillas válidas y permite jugar sin reloj.
5. El motor aplica correctamente todas las reglas, incluyendo situaciones de jaque, tablas, enroque, paso y promoción.
6. El resultado proviene del módulo de ajedrez, no de diálogos inventados por IA.
7. La partida se guarda y puede reanudarse sin perder turno/posición, incluso tras interrupciones o guardar/cargar.
8. La invitación no anula disponibilidad, obligaciones ni autonomía del NPC.
9. La interacción puede producir historia compartida y eventualmente mejorar afinidad/amistad, **pero no mediante un aumento numérico fijo ni obligatorio**.
10. No necesita tablero tridimensional de Star Trek, conexión externa, reconocimiento de voz ni personaje animado manipulando piezas.
11. La actividad no inventa instalaciones en naves que no tienen el espacio, ni modifica el estado autoritativo desde UE5 sin validación.
12. Las pruebas de aceptación se ejecutan realmente en el MSI y las etapas cerradas tienen evidencias reproducibles.

## 12. Decisiones cerradas y asuntos pendientes

### Aprobado expresamente por el autor
- **IDEA-0012** como nuevo diseño del proyecto.
- **Ajedrez convencional** como alternativa práctica al ajedrez tridimensional tradicional de Star Trek.
- Tablero de madera y fichas/piezas 3D blancas y negras ya descargadas.
- Partidas **jugables** contra un NPC amigo o compañero, en bar, camarote u otro entorno adecuado.
- Cámara de tablero en primer plano/desde la perspectiva del jugador; manejo con **ratón**.
- Piezas que se mueven automáticamente; **sin obligación de manos, brazos ni agarre real**.
- Niveles de dificultad y accesibilidad para quien empieza desde cero.
- Ocio capaz de generar convivencia e historia social, con eventual desarrollo de amistad coherente con reglas existentes.

### Propuestas de diseño que requieren afinamiento técnico posterior
- Elección de biblioteca/motor ajedrecístico y arquitectura final de integración UE5.
- Niveles efectivos y tutoría exacta, ayudas, parámetros de deshacer.
- Interrupción/reanudación, almacenamiento FEN/PGN y forma de tratar una partida cuyo NPC ya no está disponible.
- Selección de mesas/espacios por clase de nave, ritual de invitación, diálogo, reacciones y animación mínima de sentarse.
- Interfaces/cámaras definitivas e importación de los modelos reales en MSI.
- Perfil personal del NPC ajedrecista y relación de resultados con reglas sociales, sin puntuación automática.
- Compatibilidad con carga de escenas, guardados, episodios y rendimiento.

**Resultado administrativo:** IDEA-0012 **APROBADA Y REGISTRADA COMO DISEÑO**. **NO IMPLEMENTADA EN UNREAL ENGINE NI COREGPG**, y no se certifican pruebas de gameplay ni assets importados por el hecho de registrarla.
