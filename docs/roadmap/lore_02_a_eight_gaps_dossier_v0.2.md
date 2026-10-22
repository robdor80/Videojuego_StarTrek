# LORE-02 A — Dossier transversal de ocho lagunas (investigación v0.2)

> Nota histórica (2026-10-22): este dossier conserva la fotografía de investigación de 20-10-2026. La fase A fue posteriormente cerrada documentalmente y fusionada mediante la PR #31; los estados IN_PROGRESS que aparecen más abajo se refieren a aquel corte, no al estado actual. Ver `CONTENT_STATUS.md` y `docs/roadmap/lore_02_a_cierre_documental_v1.md`.\n\n**Fecha:** 2026-10-20. **Estado:** `RESEARCH_IN_PROGRESS`; documento de evidencia y reglas cualitativas, **no** definición ejecutable, ficha clínica, especificación de clase ni cierre completo de A-G01–A-G08.  
**Cobertura:** motores/maniobra, redes de energía, deflectores, comunicaciones, soporte vital, tecnología no federada, Clase Valhalla y estaciones/industria.  
**Fuente de verdad temporal:** `gameplay/ship_operations/era_technology_matrix.json`. **Fuente de verdad del mundo:** CoreRPG.  
**Tipos de afirmación:** `OFFICIAL_REFERENCE` (artículo en StarTrek.com; no equivale a un episodio visto), `RELIABLE_SECONDARY` (Memory Alpha y referencias técnicas secundarias) y `GAME_ADDITION` (decisiones expresas del juego).

**Límite metodológico:** las referencias oficiales consultadas son artículos web, no una auditoría completa de capítulos. Nunca convertir datos de un buque en regla universal, ni extrapolar rendimientos, fechas, autonomías o cantidades sin clase, estado y fuente. Tampoco inferir ausencia tecnológica de una clave faltante en la matriz.

## A-G01 — Impulso, maniobra y capacidades de separación

**Contexto verificable.** El sistema de propulsión de impulso es distinto del campo de propulsión warp. Las órdenes de maniobra requieren coordinación con operaciones e ingeniería; a modo de referencia de interacción, el artículo oficial de [Star Trek: Bridge Crew](https://www.startrek.com/news/bridge-crew-teaming-up-on-the-aegis-and-enterprise) explica coordinación entre control del timón y energía de ingeniería para impulso y warp. **Nivel:** OFFICIAL_REFERENCE sobre un videojuego, **no** fuente suficiente para cifras ni instalación canónica.

**Modelo documental mínimo:**
- Identificar **capacidad instalada** de impulso y maniobra para la nave y cada sección; no asumir la misma potencia o respuesta en todas las clases.
- Distinguir maniobra sublumínica, orientación para navegación, control de colisión y maniobra de atraque. El resultado depende de inercia/estado, propulsores disponibles, daños, control y energía; **no especificar cinemática física real todavía**.
- La separación del platillo de Valhalla conserva **impulso solamente**; la sección motriz conserva capacidad warp, conforme al acta F01, con autonomía y tripulaciones separadas.
- Registro de comando: identidad del piloto, autoridad, objetivo, estado de motores, combustible o recurso pertinente, navegación y procedimiento de abortar.

**Casos negativos:** (1) Se ordena `warp` desde platillo separado → denegar como capacidad ausente; (2) un propulsor averiado obliga a degradar/abortar aproximación y evita teletransportar el vehículo a una plaza.

**Aún por contrastar:** diferencias técnicas por era y clase; nombres exactos de propulsores, limitaciones y parámetros, con episodios primarios y equipamiento individual.

## A-G02 — Generación y distribución de energía

**Evidencia:** las referencias secundarias [Warp core](https://memory-alpha.fandom.com/wiki/Warp_core), [Matter–antimatter reaction](https://memory-alpha.fandom.com/wiki/Matter-antimatter_reaction) y [Electro-plasma system (EPS)](https://memory-alpha.fandom.com/wiki/Electro-plasma_system) describen el reactor materia/antimateria en naves y la distribución por conductos de plasma. Se consideran `RELIABLE_SECONDARY`: ilustran arquitectura usual, **no** autorizan un número de reactores, MW ni una red EPS idéntica para todos los operadores. En instalaciones y reactores de impulso pueden existir otras fuentes energéticas.

**Dependencias a documentar como relaciones, no como «barras de vida»:**
```text
fuente/reactor → contención y refrigeración → distribución primaria (EPS o equivalente)
             → convertidores/almacenamiento/reservas → consumidores de a bordo
             ↘ fallos de tubería / incendio / aislamiento / reruta → degradación real
```
- Separar reactor warp principal, generación auxiliar y energía almacenada; perder reactor warp **no** supone automáticamente pérdida instantánea de todas las funciones, pero tampoco habilita warp «con batería».
- Energía presupuestada para escudos, transportadores, impulso, soporte vital, sensores, reparación, tractores y tratamiento médico; prioridad por situación y decisiones del mando.
- Impedir aislamiento ficticio de averías: un fallo de circuito común puede afectar diversos niveles de redundancia.
- La Valhalla aprobó un núcleo principal y generación auxiliar reforzada (`VAL-TEC-02`), **no** dos reactores warp.

**Casos negativos:** pérdida de contención/refrigeración exige emergencia, posible eyección o apagado sujeto a condiciones; intento de transportador + escudos reforzados + máxima maniobra sobre energía insuficiente debe degradar/rechazar servicios coherentemente.

**Pendiente:** diseños de centrales de estaciones de diversas procedencias, baterías concretas y pruebas primarias de contención/despresurización/aislamiento.

## A-G03 — Deflector de navegación frente a escudos defensivos

**Evidencia secundaria:** [Navigational deflector](https://memory-alpha.fandom.com/wiki/Navigational_deflector) recoge barrido de partículas y objetos en ruta; [Deflector shield](https://memory-alpha.fandom.com/wiki/Deflector_shield) describe campos de protección contra amenazas. Los términos se solapan en ciertos diálogos, pero sus **funciones de operación son diferentes**. Las páginas incluyen referencias a episodios que deben comprobarse en investigación primaria.

| Función | Dato documental | Consecuencia |
|---|---|---|
| Deflector de navegación | Protege trayectoria y gestiona partículas/objetos, especialmente a alta velocidad | Falla de deflector ≠ caída automática de los escudos tácticos |
| Escudos defensivos | Protegen secciones y casco ante agresión o ambiente peligroso | Pueden agotar potencia o perder efectividad sin quitar los propulsores |
| Haz tractor | Interactúa con un objetivo concreto para atraer/sujetar/remolcar | No es sustituto universal del deflector ni un rayo ilimitado |

**Casos negativos:** deflector sin potencia obliga a restringir ruta/warp si el riesgo real lo exige; escudos tácticos caídos no implica ceguera de sensores ni ausencia automática de deflector. VAL-TEC-04: tres niveles de escudo es `GAME_ADDITION`, no «estándar Galaxy» canónico.

**Pendiente:** distinguir emisores/haces compartidos de sistemas físicamente redundantes en configuraciones de clase concreta.

## A-G04 — Comunicaciones, propagación y seguridad de señales

**Fuentes oficiales:** [Star Trek 101: What Is Subspace?](https://www.startrek.com/news/star-trek-101-what-is-subspace) como introducción; recapitulación de [SNW «Subspace Rhapsody»](https://www.startrek.com/news/recap-209-subspace-rhapsody-strange-new-worlds) describe red de repetidores, distancia de transmisión y experimento de propagación; [SNW «Terrarium»](https://www.startrek.com/en-un/news/recap-309-terrarium-strange-new-worlds) describe una comunicación bloqueada por un fenómeno espacial. `OFFICIAL_REFERENCE`, episodio reproducible aún pendiente de auditar.

**Distinciones esenciales:** (a) emitir no garantiza recibir; (b) recibir no implica descifrar; (c) descifrar no autoriza conocer; (d) una respuesta depende de que haya transcurrido suficiente tiempo, rutas viables y estado de repetidores. La latencia **no es siempre cero**; no emplear regla «mensaje instantáneo a cualquier punto de la galaxia».

**Modelo cualitativo:** transmisor/receptor, banda/canal, cifrado, potencia, antena, distancia, relés, interferencia, fenómenos locales, integridad del mensaje, titularidad, autoridad, marca temporal, confirmación/reintento.

**Casos negativos:** Valhalla y auxiliar Defiant sin enlace → conocimientos parciales distintos y órdenes remotas no recibidas; relé roto o interferencia → demoras/pérdida/ruido, no datos actualizados al instante.

**Pendiente:** acotar por época/red/ubicación la latencia; política diplomática de frecuencias/códigos y capacidades por potencia.

## A-G05 — Soporte vital, gravedad artificial y control ambiental

**Evidencia secundaria:** [Life support system](https://memory-alpha.fandom.com/wiki/Life_support_system), [Environmental control](https://memory-alpha.fandom.com/wiki/Environmental_control), [Artificial gravity generator](https://memory-alpha.fandom.com/wiki/Artificial_gravity_generator), `RELIABLE_SECONDARY` con anclas a episodios. Atmósfera, temperatura, humedad, presión y gravedad son **subsistemas distinguibles**: apagado de uno no implica siempre caída inmediata y simultánea de los demás.

**Modelo documental:** ambiente por zona/deck, mezclas compatibles con ocupantes, presión, iluminación/temperatura, reciclaje, ventilación, barreras de aislamiento, reservas y alimentación. Establecer alarmas, medidas transitorias, cambios al evacuar o separar secciones, y supervivencia condicionada a ocupantes/entorno/estado. Considerar distintas especies sin atribuir «el mismo aire para todos» ni rasgos universales no verificados.

**Casos negativos:** pérdida de potencia en una cubierta debe afectar servicios reales y desencadenar protocolos, no matar instantáneamente a toda la tripulación; despresurización aislada puede salvar otras cubiertas, pero no sin costes, daños ni bloqueos de acceso.

**Pendiente:** perfiles cuantitativos por instalación, condiciones atmosféricas especiales, estaciones civiles y capacidad de adaptación médica intercultural (LORE-02 C).

## A-G06 — Perfil tecnológico por civilización (no uniformar Starfleet)

**Fuentes oficiales contrastadas:**
- [Klingon D7](https://www.startrek.com/news/inside-the-klingon-d7-class-battle-cruiser): diseño y episodios de intercambio tecnológico/ocultación en contexto del siglo XXIII.
- [Romulan Valdore](https://www.startrek.com/news/inside-the-romulan-warbird-valdore): casco, armamento y dispositivo de ocultación, **no** todos los buques romulanos idénticos.
- [Starships of the Dominion War](https://www.startrek.com/news/the-starships-of-the-dominion-war): plataformas cardassianas, Jem'Hadar y romulanas diferenciadas.
- [Who Are the Breen?](https://www.startrek.com/news/the-breen-explainer): armamento inhibidor de energía y desarrollo de contramedidas durante conflicto.
- [Star Trek 101: The Borg](https://www.startrek.com/news/star-trek-101-the-borg): tecnología asimilativa y adaptación, sin hacerla infalible ni universal.

**Regla de generación:** civilización/operador, **clase/variante**, año, procedencia del casco, refits, capturas, intercambio, tratados, limitaciones y estado instalado se verifican **antes** de asignar tecnología. Compatibilidad no equivale a instalación. Tecnología de camuflaje y su disponibilidad tienen contextos legales y políticos; ver [The Pegasus](https://www.startrek.com/news/a-guide-to-star-treks-bad-admirals).

**Casos negativos:** (1) capturar nave romulana no instala mágicamente camuflaje en toda la Flota; (2) sensor superior/detección excepcional no revela siempre toda la nave enemiga; (3) los Borg no reparan ni se adaptan de forma absolutamente instantánea ante cualquier ataque; (4) tecnología de los Breen no afecta a todos los buques en toda la cronología.

**Pendiente:** perfiles trazables por clase/era de vulcanos, andorianos, klingon, romulanos, cardassianos, ferengi, Dominio, Borg y otros, priorizando naves/estaciones que el generador puede producir. **Los encuentros reservados del DLC Delta siguen deshabilitados**.

## A-G07 — Clase Valhalla, excepciones y nave auxiliar

**Decisión primaria del propio juego:** [VAL-TEC-01–16](../../lore/technology/valhalla_tech_profile_v0.1.md) y [registro de aprobación](../../lore/technology/valhalla_tech_decisions_v0.1.json). La Clase Valhalla es **nueva**, inspirada en Galaxy, con arquitectura equilibrada Sovereign/Intrepid como referencia, no refit oficial.

**Evidencia relevante:** [Star Trek: Voyager «Endgame»] como inspiración **de pantalla pendiente de cotejo escena por escena** de ablativo desplegable y torpedos transfásicos; [fuente oficial sobre la Defiant](https://www.startrek.com/gallery/most-powerful-star-trek-ships-ranked) distingue blindaje ablativo de la Defiant y la ocultación romulana histórica. El juego **aprueba** blindaje desplegable y munición transfásica para Valhalla mediante `GAME_ADDITION`; ello **no** instala esas capacidades en la nave auxiliar IDEA-0010.

**Consolidación:** triple escudo primario/secundario/terciario escalonado y blindaje físico separado; matriz de fáseres, torpedos fotónicos/cuánticos y stock restringido transfásico; único núcleo warp y fusión auxiliar; propulsión avanzada, ciencia, medicina, soporte vital y respuesta a emergencias. Cuando se separan platillo y sección motriz no se copian reactores, emisores, armas o conocimientos.

**Casos negativos:** el platillo separado no dispone de warp; «activar las tres capas + ablativo» no ignora potencia/circuitos dañados; la Defiant no hereda ablativo/transfásicos/camuflaje por ser auxiliar; no se considera operativo ningún sistema sólo por figurar en un documento.

**Pendiente:** **cronología individual**, datos de clase, ubicación y cantidades reales, límites del triple escudo, representación exterior, asignación del acoplamiento Defiant a sección y validación física/UE5.

## A-G08 — Estaciones, astilleros y tecnología industrial/civil

**Fuente oficial:** [Starbases of the Federation: From K-7 to Yorktown](https://www.startrek.com/news/starbases-of-the-federation-from-k-7-to-yorktown) documenta diversidad de funciones de bases y el cambio de misión de Terok Nor a DS9, puesto fronterizo/comercial y **centro de reparaciones** durante la guerra. Una plataforma diseñada para minería puede ser readaptada; **su origen no determina equipamiento futuro sin historial de reformas**.

**Tipos funcionales para investigar, sin inventar capacidades:** relay/antena, pequeña estación científica, puesto fronterizo, astillero/refit, centro médico, centro comercial, estación minera/refinería, complejo de abastecimiento, base militar y estación de tránsito. No deben compartir idénticos reactores ni asumir warp propio.

**Campos necesarios:** clase/operador/año, hábitat, reservas, defensa, atraques/compatibilidad, talleres, repuestos, turnos, equipo médico, telecomunicaciones/relés, capacidad logística, inventario de naves atendidas, gobierno y permisos, dependencias con infraestructura planetaria.

**Casos negativos:** astillero sin piezas no «cura» toda avería instantáneamente; estación sin acomodo adecuado no atraca cualquier nave por tamaño; relé incomunicado no sigue transmitiendo mensajes nuevos; estación sin pacientes/instrumentos no simula hospital completo.

**Pendiente:** perfiles de instalaciones individualizados por civilización y época, alcance real de reparaciones, elementos industriales y procedimientos de carga/descarga.

## Regla común de los ocho ámbitos

Antes de cualquier afirmación operacional o generación de contenido:
1. comprobar **era y evidencia**, sin convertir ausencia de registro en `unavailable`;
2. civilización / clase / refit / instalación y **equipo instalado**;
3. permisos y mando, tripulación, recursos, averías y condiciones locales;
4. conocimiento visible del actor (distinguir detección, clasificación e identificación);
5. simulación autorizada por contratos de Star Trek y ejecución vía **CoreRPG**, no por la IA narrativa;
6. interacción o efecto visual en UE5 posterior a resultado validado;
7. persistencia de errores, daños, transportes y decisiones en continuidad.

**Próxima puerta de cierre:** convertir evidencia por cada sistema en fichas de catálogo validables, con ID de fuente registrado y contrastado con pantalla cuando se afirmen propiedades fuertes; ampliar casos negativos y perfiles no federados/estaciones sin contradecir contratos F00–F15. Hasta entonces **LORE-02 A permanece `IN_PROGRESS`**.

## Tabla de procedencia de consulta de este dossier

| Ámbito | Fuentes consultadas | Clase / cautela |
|---|---|---|
| Impulso | StarTrek.com «Bridge Crew» | Oficial **sobre videojuego**; no especificación de canon |
| Energía | Memory Alpha «Warp core», «Matter-antimatter reaction», «Electro-plasma system» | Secundaria |
| Deflectores | Memory Alpha «Navigational deflector» y «Deflector shield» | Secundaria |
| Comunicaciones | StarTrek.com «Subspace Rhapsody», «Terrarium», «What Is Subspace?» | Oficial; cotejo episodio pendiente |
| Soporte vital | Memory Alpha «Life support system», «Environmental control», «Artificial gravity generator» | Secundaria |
| Civilizaciones | StarTrek.com D7, Valdore, Dominion War, Breen, Borg, «The Pegasus» | Oficial; no extrapolación |
| Valhalla | Decisiones del autor VAL-TEC y IDEA-0005/0010; «Endgame» como referencia a cotejar | **GAME_ADDITION** para equipamiento exclusivo |
| Estaciones | StarTrek.com «Starbases of the Federation» | Oficial; instalaciones individuales pendientes |

El dossier es un **avance verificable de investigación** y una guía de pruebas, no una afirmación de que toda la tecnología galáctica haya quedado documentada.
