# DEC-0021 — Doctrina de supremacía de la Enterprise-D Valhalla: sensores y reputación galáctica

**Autor:** decisión expresa del 17-11-2026. **Estado:** APROBADA EN DISEÑO / GAME_ADDITION; runtime todavía no certificado. **Nave:** USS Enterprise NCC-1701-D, `ship_id=uss_enterprise_ncc_1701_d`, clase Galaxy, configuración modernizada Proyecto Valhalla (`galaxy_refit_a2`). No crear clase nueva ni renombrar la nave.

## 1. Intención del autor: «el megalodón de la galaxia»

La Enterprise-D recuperada por Geordi La Forge debe ser la nave insignia de mayor capacidad y prestigio tecnológico de la Flota Estelar en esta continuidad propia. La superioridad **no es solo narrativa**: sensores, cálculo, supervivencia, armamento y desempeño efectivo en CoreRPG deben justificar la fama. No igualar arbitrariamente a un carguero obsoleto, una Miranda o un pirata con la Galaxy modernizada para forzar combate equilibrado.

La Federación no pretende conquistar. La función es exploración, disuasión y defensa contundente cuando sea necesario. Se conservan la autoridad del capitán, la cadena de mando, el derecho, las reglas de enfrentamiento y las consecuencias. Una nave enemiga inferior puede negociar, retirarse o evitar una provocación por reconocer a la Enterprise-D. No imponer miedo universal idéntico ni victoria automática: comandante, misión y contexto siguen contando.

El programa Defiant (camuflaje romulano, centro propio y dotación especializada) y el destacamento de Marines «Hijos de Odín» forman parte del concepto de la nueva Enterprise-D. Sus geometrías, dotaciones, instalación y disponibilidad REAL se certifican en sus propios sistemas; la aprobación de esta doctrina no materializa ni equipa una nave sin un cambio válido en el WorldState. El blindaje ablativo desplegable y los torpedos **transfásicos** (no «transwarp») son capacidades de diseño decisivas que deben contar con instalación y pruebas, nunca bonificadores cosméticos.

## 2. Reputación conocida: no secreta

El Proyecto Valhalla es de conocimiento público y militar **a escala de las potencias con relaciones, noticias y canales galácticos**: Federación y miembros, potencias no miembros y sus estructuras de defensa/inteligencia, incluidos romulanos, klingon, cardassianos, etc. El regreso en servicio de la Enterprise-D modernizada es un acontecimiento mayor y reconocible. La notoriedad del proyecto existe durante su desarrollo; no anticipar como hecho consumado en 2383 una entrada en servicio futura aún condicional (objetivo 2387).

La información pública contiene existencia, identidad histórica NCC-1701-D, reconstrucción, estatus de buque insignia, enorme reputación tecnológica y rendimiento conocido. NO entrega automáticamente especificaciones clasificadas, frecuencias de escudos, inventarios exactos, patrones secretos, códigos, localizaciones encubiertas ni todos los detalles del Proyecto Defiant. Tampoco revela a observadores sin vías de comunicación hechos posteriores a su último informe: mantener fecha y procedencia en el conocimiento.

Las facciones y los comandantes NPC deben consultar un perfil de **reconocimiento de nave individual** (no una regla racial). Al identificar a la Enterprise-D Valhalla, evaluarán sus propias capacidades, órdenes, objetivos, información, riesgo y desventaja. El sistema debe permitir disuasión, retirada, cautela, contacto diplomático o ataque motivado sin fabricar invulnerabilidad ni enemigos suicidas por rutina. Los NPC fuera de pantalla realizan las mismas evaluaciones. El nombre «megalodón» es una metáfora de diseño, no un rango técnico.

## 3. Doctrina sensorial vinculante

**Automático y manual son ambas vías de operación.** La vigilancia, adquisición de contactos y preparación de perfiles suceden de fondo. Cualquier jugador u oficial NPC puede solicitar manualmente `IDENTIFICAR`, `ANÁLISIS TÁCTICO`, `ESCUDOS`, `ARMAMENTO`, `PROPULSIÓN`, `TRAYECTORIA`, `VIDA`, `BARRIDO`, etc.

**Garantía operativa para contactos y fenómenos ordinarios detectables:** una solicitud = informe completo, correcto y utilizable de inmediato. Una nave no camuflada ordinaria dentro del escenario operacional nunca debe devolver «datos insuficientes» sobre armamento, escudos, motores o subsistemas identificables; menos aún un carguero centenario. Un barrido manual no requiere 90 segundos ni cadenas de reintentos, filtros, frecuencias y menús para obtener información elemental. El ordenador prepara por anticipado perfiles completos y soluciones tácticas; la petición manual los presenta o resuelve al instante, tanto para jugador como para NPC. La información esencial debe estar ya preparada antes de la orden de disparo cuando el contacto es ordinario.

La doctrina también cubre navegación y exploración ordinarias: datos de órbitas, trayectorias, cuerpos celestes, señales y características relevantes disponibles en cuanto son operativamente solicitados. El universo sigue siendo autoritativo; una lectura **consulta/deriva** datos reales del WorldState, no genera entidades o poderes por IA. La precisión garantizada se obtiene diseñando un perfil tecnológico superior y un motor resolutorio capaz de producir esos datos, no fingiendo que una señal «falló» para prolongar la acción.

**Excepciones extraordinarias:** solo en circunstancias narrativas explícitas, rarísimas y justificadas (orientación aproximada 0,1 % del contenido, NO probabilidad de fallo de una lectura). Nunca introducir fallos aleatorios recurrentes o degradaciones a escondidas para crear tensión. Una anomalía excepcional tiene causa en WorldState, trazabilidad y tratamiento específico; un evento ordinario no puede declarar indisponible la información prevista. Si el casco está verdaderamente averiado o una tecnología singular excede la capacidad real, gestionar la situación como incidente mayor explícito, no como comportamiento habitual. La regla no obliga a revelar secretos narrativos aún no existentes en los datos.

## 4. Interfaz y desempeño

- **Respuesta instantánea de jugabilidad:** presentar la lectura en el mismo flujo interactivo, sin barras de progreso inventadas ni esperas largas. Objetivo de aceptación <= 1 s para informe táctico ordinario en máquina objetivo, a partir de datos precalculados y resolución determinista; medir en UE5 real, no afirmar que ya se cumple.
- **Informe único completo:** identidad/clase, sistemas de armas y su ubicación, defensas/escudos, propulsión, trayectoria, vulnerabilidades tácticas y características relevantes para el contacto. Evitar cascadas de «analizando...» y consultas sucesivas.
- **Consolas operativas de 1–2 acciones frecuentes:** mantener árbol avanzado de referencia cuando proceda, pero controles contextuales de acceso directo; no exigir al jugador múltiples menús para una orden urgente.
- **Capitanes NPC:** disponen de los mismos informes y emiten órdenes de forma autónoma. Oficiales NPC ejecutan tareas; el jugador subordinado solo realiza su parte. Sin acceso obligatorio a OpenAI para resolver lecturas, disparos o estados.
- **Autoridad:** automatizar adquisición y preparación; los escaneos intrusivos, decisiones de mando y disparos siguen exigiendo autorizaciones aplicables. El ordenador no inventa derechos de mando.

## 5. Alcance temporal y precedencia

Esta decisión se aplica a la **Enterprise-D modernizada cuando su perfil autorizado está activo**. No reescribe las capacidades genéricas de una Miranda, una Galaxy clásica u otras naves, ni implica que los prototipos antiguos implementen ya este comportamiento. Los contratos generales pueden conservar sus reglas de incertidumbre para otras plataformas, pero el perfil Valhalla es vinculante cuando el buque está equipado y operativo.

**Precedencia:** esta decisión autoral posterior complementa DEC-0020 y prevalece sobre requisitos anteriores de retrasos habituales, lectura rutinaria incierta o bloqueos de subsistemas ordinarios, **solo para la Enterprise-D Proyecto Valhalla**. Conserva la regla «verdad del mundo antes que observación» de `authoritative_observable_universe.md` y el carácter genérico de CoreRPG.

## 6. Contratos y criterio de cierre

- `sistemas/gameplay/ship_operations/sensor_resolution/enterprise_d_valhalla_sensor_superiority_v0.1.json`
- `sistemas/gameplay/reputation/enterprise_d_valhalla_ship_reputation_v0.1.json`
- `sistemas/gameplay/conflict/enterprise_d_valhalla_threat_recognition_v0.1.json`
- `sistemas/gameplay/ship_operations/sensor_resolution/enterprise_d_valhalla_acceptance_cases_v0.1.json`

**No confundir:** aprobación de diseño, contratos y pruebas de coherencia estática **NO son integración** CoreRPG/HOST/UE5. Antes de declarar «perfectos» los sensores o activa la reputación, exigir escenarios reales de observación manual/automática, órdenes NPC, rendimiento en MSI, estado de la flota y reacción de facciones, con CI y evidencia de ejecución.