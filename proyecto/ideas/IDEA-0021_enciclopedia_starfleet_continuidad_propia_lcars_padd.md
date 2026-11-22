# IDEA-0021 — Enciclopedia Starfleet LCARS y PADD de la continuidad propia de Star Trek Legends

**Aprobación expresa:** 23 de noviembre de 2026.  
**Estado:** **APROBADA CONCEPTUALMENTE**; preparación editorial existente en Operación LORE B09; implementación jugable y Android pendientes.  
**Decisión del autor:** «Lo que va a haber en la biblioteca o en la enciclopedia debe ser datos de mi videojuego». **La continuidad aprobada de Star Trek Legends prevalece sobre el canon televisivo cuando difieren.**

## 1. Objeto y base existente

Enciclopedia consultable en la computadora principal de la nave, terminales LCARS y PADD, además del Starfleet PADD Android (IDEA-0019). Especies, tecnología, personajes, instituciones, planetas, historia y expedientes de campaña autorizados.

**No duplicar ni sustituir LORE:** Operación LORE B09 ya aportó **20 entradas editoriales** en `mundo/lore/knowledge/lore_2383_enciclopedia_editorial_v1.json` (`runtime_import_allowed=false`). Reutilizar identificadores y referencias, y auditarlas antes de servirlas al jugador.

## 2. Orden de precedencia irrevocable salvo nueva decisión autoral

1. **Decisiones expresas, vigentes y aprobadas del autor**, junto con el LORE propio ratificado: biografías, edades, nacimientos, destino de personajes, tecnología, identidades de naves, mapas y cronología de **Star Trek Legends**. La decisión más reciente válida sustituye a la previa solo en el ámbito que efectivamente cambie, con trazabilidad.
2. **World State autoritativo de CoreRPG:** resultados y acontecimientos efectivamente ocurridos en la campaña, tiempo de partida, ubicaciones, misiones y descubrimientos. No confundir objetivos futuros del diseño con hechos ya consumados. El estado dinámico no puede inventar una nueva biografía fija.
3. **Canon de pantalla y otras fuentes Star Trek:** recurso de documentación **únicamente en lo compatible con el universo del juego**. `SCREEN_CANON` indica procedencia de una afirmación, **no su autoridad para imponerse** a un cambio aprobado.
4. **Información no decidida, ambigua o contradictoria:** se deja `POR_DEFINIR` o se bloquea para revisión; la IA, un RAG, fuentes externas o una importación automática no pueden rellenarla con canon de TV sin verificar compatibilidad.

**Ejemplo Siete de Nueve:** si para nuestra Siete el autor aprueba un nacimiento/edad diferentes de la serie, la enciclopedia usa **la versión del videojuego**. El año «2400» fue un **ejemplo hipotético**, no una fecha de nacimiento aprobada; esta idea no fija fecha alguna para ella.

**Ejemplo Enterprise-D:** Proyecto Valhalla representa la **USS Enterprise NCC-1701-D restaurada y modernizada por Geordi La Forge**, no la antigua clase Valhalla/Enterprise-G. La reconstrucción y su eventual entrada en servicio se describen conforme a decisiones y World State del juego, no automáticamente conforme a *Picard*.

## 3. Cuatro dimensiones independientes

- **Verdad del juego editorial:** datos estables aprobados y con versiones y procedencia.
- **Estado de campaña:** acontecimientos reales, observaciones, fechas y resultados de una partida concreta.
- **Conocimiento del actor:** lo que el personaje sabe o cree saber, con fiabilidad, fecha, rumores e información incompleta.
- **Derechos de consulta:** acceso por puesto, rol, habilitación, necesidad de conocer, privacidad y contexto.

Una entrada puede estar preparada por LORE y seguir **no visible** para el jugador. Si el expediente secreto no puede revelarse, tampoco mostrar su título. La biblioteca no es un bypass para conocer el futuro, expedientes médicos ajenos o datos exclusivos del capitán.

## 4. Experiencia y presentación

- Enciclopedia navegable y buscable en **castellano**, con categorías, artículos, cronologías, esquemas, imágenes autorizadas y referencias cruzadas.
- Lectura desde LCARS de la nave y terminales personales; peticiones por texto o voz mediante la computadora compartida, con respuestas verificadas.
- Capacidad de consultar **expedientes de campaña**, como planetas explorados o anomalías investigadas, sin convertir lo observado en un hecho editorial universal de todas las partidas.
- Android/IDEA-0019: biblioteca estática versionada compatible con el juego y **último snapshot autorizado** de la campaña, opcionalmente offline; nunca datos en directo si el juego está cerrado.
- Cualquiera de las interfaces puede responder «no consta», «todavía desconocido», «clasificado» o «información contradictoria» en lugar de fabricar respuestas.

## 5. Arquitectura y documentos responsables

- **Fuente estable:** `mundo/lore/` y decisiones ratificadas del proyecto.
- **Proveniencia:** `mundo/sources/provenance_policy.md`; conservar la distinción `SCREEN_CANON` frente a `GAME_ADDITION`, pero evaluar siempre compatibilidad con la versión del videojuego.
- **Índice inicial:** `mundo/lore/knowledge/lore_2383_enciclopedia_editorial_v1.json`, 20 entradas en estado editorial NO RUNTIME.
- **B09:** `proyecto/docs/roadmap/operacion_lore_20261122/B09_ENCICLOPEDIA_PADD.md`.
- **Conocimiento:** `sistemas/gameplay/knowledge/character_knowledge_state.json`; el indexador no sustituye a CoreRPG.
- **Consultas:** computadora principal y aplicaciones LCARS/IDEA-0019 como proyecciones de lectura, nunca autoridades paralelas.

Separar siempre `entry_id` editorial de `entity_id` persistente, marcar versión de continuidad y revisar enlaces/fechas cuando una decisión nueva invalide parte de un artículo.

## 6. Trabajos candidatos ENC-01–ENC-07

- **ENC-01:** auditar las 20 entradas B09 frente a las decisiones del juego; clasificar compatibles, corregibles, divergentes y pendientes. **No publicar todavía entradas no verificadas**.
- **ENC-02:** contrato de fuentes/precedencia, versionado, validez temporal, enlaces e invalidación de hechos canónicos desplazados.
- **ENC-03:** índice y búsqueda en castellano, sin duplicar todas las fichas LORE.
- **ENC-04:** filtros de conocimiento, accesos, privacidad, World State, cronología y observaciones; pruebas de no filtración.
- **ENC-05:** visualizador LCARS y consulta por computadora vía voz/texto, sin inventar contenido.
- **ENC-06:** integración del PADD Android con fichas estáticas compatibles y copia de consulta de la última partida.
- **ENC-07:** QA de contradicciones, cambios de decisión, permisos, partidas divergentes y lectura sin mutaciones.

**Fases relacionadas:** LORE B09; F02–F05 (autoridad/conocimiento), F11–F12 (carrera/personajes/vida a bordo), F14 (LCARS) y F15 (QA). No abrir nueva fase principal ni cambiar el estado administrativo de F05 por aprobar la idea.

## 7. Invariantes de aceptación

1. Si la TV dice una cosa y una decisión vigente de *Star Trek Legends* dice otra, **el artículo y la respuesta muestran la del juego**.
2. El uso de `SCREEN_CANON` conserva trazabilidad, **no obliga a copiar ese dato en la versión del juego**.
3. No fijar biografías o fechas no aprobadas, incluidas las de Siete, para encajar con el canon.
4. Leer un artículo **no crea misiones, descubre planetas, desbloquea sucesos, cambia relaciones, ejecuta órdenes ni modifica World State**.
5. La fecha de juego, el conocimiento real, los permisos y el contenido editorial deben concordar; si no, restringir la respuesta.
6. PADD Android es de consulta y muestra únicamente la última información autorizada sincronizada.
7. Una ficha «editorial completa» no implica que haya sido auditada para continuidad de juego, indexada, implementada ni certificada en UE5.
