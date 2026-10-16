# IDEA-0008 — Sistema modular de entornos espaciales

**Proyecto:** Star Trek RPG (Unreal Engine 5.8.2, Windows)

**Destino oficial:** `/ideas/IDEA-0008_entornos_espaciales_modulares.md`

**Estado:** APROBADA CONCEPTUALMENTE / IDEA-0008, pendiente de planificación, pruebas e implementación. La inclusión en GitHub no acredita un prototipo funcional.

## 1. Concepto

Construir un **sistema universal y reutilizable de escenarios espaciales** que combine fondos astronómicos lejanos con cuerpos celestes y elementos tridimensionales reales. No crear manualmente un escenario nuevo desde cero para cada misión: cada sector o sistema estelar será una **configuración de módulos y activos compartidos**.

La meta es lograr escenas de calidad visual elevada en las que las naves puedan navegar, patrullar, explorar, encontrarse con otras naves y combatir, con una iluminación coherente con el entorno.

**Fórmula de diseño:** fondo estelar y nebulosas + estrella y luz + planetas 3D + lunas y asteroides 3D + naves y estaciones = escenario espacial explorable.

## 2. Estructura del entorno

### A. Fondo de espacio profundo — visual, sin geometría astronómica individual

- Campo estelar lejano mediante *skybox* o *skydome* y material **Unlit/Emissive**.
- Nebulosas y galaxias distantes mediante capas visuales parametrizables.
- Debe dar sensación de inmensidad sin generar colisiones ni simular miles de estrellas físicamente.
- El fondo puede seguir la posición de la cámara, sin copiar necesariamente su rotación, para no crear paralaje artificial ni alcanzar el borde del escenario.

### B. Sistema estelar local — elementos 3D con posición propia

- **Estrella principal:** representación visual del astro y fuente de iluminación direccional coherente para el sector.
- **Planetas:** reutilizar prioritariamente los modelos 3D ya disponibles en la biblioteca de assets, tras comprobar geometría, materiales, texturas, escala y licencias.
- **Lunas y satélites:** objetos tridimensionales con sus propias posiciones y propiedades.
- **Asteroides y cinturones:** modelos 3D instanciados o distribuidos proceduralmente; colisiones y detalle según distancia e importancia jugable.
- **Estaciones, naves y puntos de interés:** actores independientes integrados en el mismo sistema de coordenadas de juego.
- **Fenómenos locales opcionales:** anomalías, gas, polvo y otros efectos, en cantidades moderadas y justificados por el entorno.

**Aclaración:** las “capas” son una separación **lógica y técnica**, no una obligación de superponer varias esferas. Los planetas próximos a los que se navega deben ser modelos 3D, no fotografías colocadas en el cielo.

## 3. Iluminación

- Priorizar **una fuente de luz estelar principal**, coordinando color, intensidad, orientación y sombras sobre naves, planetas y asteroides.
- El cielo espacial no necesita una atmósfera terrestre global (*Sky Atmosphere*) para funcionar. Las atmósferas de planetas concretos serán sistemas locales si se incorporan.
- Ajustar exposición, reflejos y materiales para que las superficies del casco conserven detalle en luces y sombras.
- Contemplar sistemas con varias estrellas como ampliación futura; requerirán una solución de iluminación específica.

## 4. Reutilización y configuración por sector

Proponer un actor o subsistema de UE5, por ejemplo **`BP_SpaceEnvironment`**, y perfiles de datos independientes para variar un mismo sistema visual sin duplicar Blueprints ni geometría.

Ejemplos de perfiles:

| Perfil de escenario | Composición sugerida |
|---|---|
| Espacio profundo | Campo estelar, nebulosa tenue y objetos locales escasos |
| Sistema habitable | Estrella amarilla, planeta terrestre 3D, luna y asteroides dispersos |
| Sistema de gigante gaseoso | Estrella, gigante gaseoso con anillos, lunas y cinturón de asteroides |
| Sistema de enana roja | Luz rojiza, planeta rocoso y entorno oscuro |
| Región nebular | Fondo nebular, visibilidad y efectos locales configurables |

Cada perfil deberá permitir modificar posición/orientación, selección de assets, iluminación, densidad de asteroides y elementos narrativos o jugables.

## 5. Integración con la jugabilidad

- **Navegación libre:** las naves no siguen trayectorias dibujadas previamente en Sequencer; sus rutas se calculan durante la partida.
- **Naves del jugador y NPC:** utilizan el mismo controlador base de navegación y los mismos principios espaciales, con capacidades y decisiones configurables por nave.
- **Sensores:** detectan cuerpos, otras naves, obstáculos y fenómenos de acuerdo con las capacidades y reglas correspondientes.
- **Piloto automático:** puede aproximarse a destinos y evitar obstáculos relevantes.
- **Exploración:** aproximación y órbita de planetas, inspección de anomalías y estaciones.
- **Combate:** maniobras entre naves, utilización de asteroides u otros cuerpos como elementos espaciales, siempre que existan físicamente en la escena.
- **Coherencia visual:** el espacio observado desde los ventanales del puente, desde una lanzadera o desde la cámara exterior debe corresponder al **mismo entorno del juego**.

**Primeras naves de prueba propuestas:** Enterprise-D (Galaxy) y Pájaro de Presa Romulano (NPC). La arquitectura no debe depender de estas dos clases.

## 6. Rendimiento y escala

El prototipo se desarrollará en el MSI Raider (RTX 4070 Laptop, 8 GB de VRAM). Debe priorizar calidad sin cargar recursos innecesarios.

- Usar **LOD/HLOD, instanciación y culling** cuando proceda para planetas, asteroides y objetos de escena.
- Separar **representación visual lejana** de objetos que necesitan posición, físicas, sensores o interacción real.
- No mantener todos los sistemas estelares del universo cargados ni simulados en 3D simultáneamente.
- Diseñar la transición entre distancias astronómicas y escenas locales; verificar **precisión de coordenadas, escala y origen** en UE5 antes de fijar distancias reales.
- Medir consumo de VRAM, FPS, tiempo de carga, calidad de texturas y coste de iluminación en el MSI.
- Mantener persistencia y simulación simplificada de acontecimientos fuera de la zona activa cuando el diseño general lo requiera.

## 7. Arquitectura y responsabilidades

- **Unreal Engine 5:** renderizado de escenarios, streaming, movimiento 3D, colisiones, iluminación, efectos y presentación espacial.
- **Lógica de navegación/decisiones:** componentes reutilizables para naves del jugador y NPC; maniobras y decisiones no dependen de una IA generativa en cada fotograma.
- **CoreRPG:** solamente reglas genéricas, estados, capacidades, autoridad o persistencia que sean parte de su contrato reutilizable; evitar trasladar a CoreRPG la implementación gráfica específica de Star Trek.
- **Contenido Star Trek:** definiciones de sectores, planetas, naves, facciones, misiones y configuraciones visuales, preferentemente mediante datos editables.

## 8. Propuesta de implementación por etapas

1. **Entorno espacial mínimo:** estrellas y nebulosa parametrizables, sin modificar la Galaxy M09 original.
2. **Estrella e iluminación:** luz direccional y exposición ajustadas; verificar materiales y legibilidad de las naves.
3. **Primer planeta 3D:** importar un asset existente, validar materiales y escala, permitir aproximación y órbita simplificada.
4. **Asteroides:** añadir un pequeño conjunto real con colisiones y después convertirlo en campo modular eficiente.
5. **Navegación:** probar movimiento y piloto automático de la Enterprise-D dentro del entorno.
6. **Interacción entre naves:** añadir el Pájaro de Presa Romulano y verificar detección, reacción y maniobras básicas.
7. **Segundo perfil espacial:** cambiar estrellas, planetas, fondo e iluminación **sin duplicar el sistema**, para demostrar la reutilización.

Cada etapa debe tener una prueba visual y funcional concreta antes de avanzar.

## 9. Criterios de aceptación iniciales

- Los modelos 3D conservan una calidad visual comparable a la aprobada en Blender tras su importación a UE5.
- El fondo estelar no interfiere con la navegación ni presenta bordes visibles o movimientos falsos evidentes.
- Los planetas y asteroides relevantes son elementos 3D independientes, con posiciones consistentes.
- La iluminación del casco corresponde a la estrella principal del escenario.
- El mismo sistema configura al menos **dos escenarios diferentes** sin duplicar su arquitectura.
- Las naves pueden moverse dinámicamente dentro del entorno; ninguna depende de una trayectoria Sequencer pregrabada para su navegación ordinaria.
- El rendimiento se comprueba en el equipo objetivo, registrando datos antes de declarar la fase aprobada.

## 10. Cuestiones por decidir

- ¿Las naves podrán entrar en las atmósferas planetarias o, inicialmente, solo navegar y permanecer en órbita?
- ¿Qué escala espacial utilizaremos para representar órbitas y distancias entre planetas sin perder precisión ni jugabilidad?
- ¿Qué nivel de simulación orbital/rotacional se necesita y qué movimientos serán aproximaciones visuales?
- ¿Qué modelos concretos de planetas y asteroides de la biblioteca actual resultan válidos y con qué licencias?
- ¿Qué funcionalidades mínimas exigir a los sensores y al piloto automático para las pruebas iniciales?

## 11. Límites de esta idea

Este documento describe un **diseño propuesto**, no sistemas ya desarrollados. La importación visual satisfactoria de la Galaxy en un proyecto UE5 con calidad Maximum y la prueba manual de separación del platillo son antecedentes útiles, pero **no demuestran todavía** navegación autónoma, combate, iluminación astronómica, simulación planetaria ni reutilización efectiva del entorno.

---

**Resumen:** construir un único sistema modular de entornos espaciales para Star Trek RPG, compuesto por fondos lejanos de estrellas y nebulosas y objetos astronómicos tridimensionales reutilizables —estrella, planetas, lunas y asteroides—, con iluminación coherente, navegación dinámica, perfiles por sector y rendimiento escalable.

---

## 12. Registro administrativo e integración técnica (añadido al incorporar IDEA-0008)

**Fecha de registro:** 16 de octubre de 2026. **Decisión del autor:** inclusión expresamente solicitada como nueva idea del proyecto. **Alcance:** conservar la propuesta del archivo adjunto en sus apartados 1–11; las notas de este apartado son aclaraciones técnicas para futura planificación, no afirmaciones de implementación.

### Dependencias y reutilización

- **F02 — Arquitectura:** separar los perfiles descriptivos de sectores, estado autoritativo y representación UE5; revisar interfaces sin inventar APIs de CoreRPG.
- **F03 — Mundo/persistencia:** posición, identidad y propiedades de cuerpos y naves reales; el hecho de que un sistema no esté cargado visualmente no hace desaparecer sus entidades ni eventos.
- **F07 — Pipeline 3D:** auditoría de materiales, escala, licencias, calidad visual de importación, sistemas de coordenadas y escena piloto UE5; verificar en el MSI, no considerar pruebas Blender equivalentes a pruebas UE5.
- **F09 — Consolas:** navegación, sensores, operaciones y maniobras; el controlador de vuelo dinámico debe ser reutilizable por jugador/NPC, pero no duplica la lógica de decisión/autoridad.
- **F13 — Universo dinámico y exploración:** elegir perfiles/activos compatibles con sectores y sistemas estelares realmente existentes, evitando que un entorno visual genere hechos astronómicos falsos por sí solo.
- **F14 — Recursos audiovisuales:** fondos, nebulosas, star lighting, planetas/asteroides, materiales, efectos, rendimiento gráfico y niveles de detalle.
- **F15 — QA:** medición de FPS/VRAM/tiempos de carga, pruebas de dos perfiles diferentes, navegación y consistencia espacial; sin cerrar fase por simples capturas o fixtures.
- **[IDEA-0006 — Temporadas narrativas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md):** los packs narrativos podrán referenciar perfiles espaciales ya soportados, sin tener que redefinir el sistema de entorno para cada misión.

### Separación de responsabilidades e invariantes

1. **Estado del universo frente a representación:** `CoreRPG`/reglas de Star Trek mantienen identidad, hechos, posiciones y consecuencias que les competen; UE5 construye y presenta el entorno espacial visible. Un perfil gráfico no inventa un planeta, contacto o nave detectada.
2. **Un solo espacio lógico:** vistas exteriores, ventanales e interfaces deben consultar la misma ubicación/identidades del escenario, con representaciones de detalle distintas si el rendimiento lo exige.
3. **Navegación dinámica:** trayectorias y reacciones se calculan conforme al estado y reglas del juego; Sequencer puede usarse para planos no interactivos, no como sustituto de navegación operativa autónoma.
4. **Escalas y streaming:** confirmar límites de precisión, distancias, físicas y origen en la versión UE5 elegida. No declarar resuelto un mundo astronómico continuo por disponer de un skybox.
5. **Activos:** los modelos 3D de planetas ya poseídos son candidatos a auditar. Antes de emplearlos en una build, verificar licencia, geometría, escala, texturas y comportamiento a diferentes distancias.
6. **Pruebas de las dos naves propuestas:** Enterprise-D (Galaxy) como referencia de control y Pájaro de Presa Romulano como NPC; la implementación común no deberá codificar dependencias exclusivas de esas clases. Esta propuesta no fuerza la elección de la Enterprise-D como la Valhalla ni modifica los modelos originales.
7. **Límites de la idea:** no autoriza entrada atmosférica, órbitas físicas de alta fidelidad ni simulación simultánea de todos los sistemas estelares. Son decisiones pendientes explícitas del documento.

### Material existente a consultar

- [Buzón de ideas](BUZON.md).
- [F07 — Pipeline UE5 y activos](../docs/roadmap/master/fases/F07/README.md).
- [F13 — Universo dinámico](../docs/roadmap/master/fases/F13/README.md).
- [Consola de Navegación/Astrometría](../gameplay/ship_operations/consoles/navigation/README.md).
- [Sistema de misiones emergentes desde World State](../gameplay/missions/emergent_mission_from_world_state_contract.json).

**Estado final de archivo:** IDEA-0008 registrada y aprobada como concepto; **NO IMPLEMENTADA**. No modifica por sí sola proyectos UE5/Blender, maniobras autónomas ni fases de desarrollo.
