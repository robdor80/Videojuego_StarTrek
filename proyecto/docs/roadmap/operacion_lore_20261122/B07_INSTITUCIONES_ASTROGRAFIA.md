# B07 — Federación, potencias, jurisdicciones y cartografía temporal

**Alcance:** procesos 07 y 08. Reutiliza LORE-01 B/C/D, LORE-04D y LORE-05C/D; no abre una segunda geografía ni un motor político.

## 1. Mapa de instituciones de 2383

| Actor | Naturaleza | Qué puede determinar | Lo que no se deduce |
|---|---|---|---|
| Federación Unida de Planetas | gobierno civil multi-mundo | política federada conforme competencias válidas; relaciones diplomáticas | que Starfleet legisle toda vida civil |
| Flota Estelar | servicio de exploración, defensa y ciencia | disciplina, buques, órdenes, misiones e ingreso militar/científico conforme norma | que un almirante modifique leyes civiles por voluntad propia |
| Consejo Estratégico de Starfleet | **GAME_ADDITION** institucional, presidido por Picard según LORE-05B | debate y recomendaciones de alto nivel | que resuelva formalmente sin F10 la admisión de un cadete |
| Gobierno de Bajor | soberanía bajorana | política, territorio y autoridades propios | que DS9 transfiera soberanía a la Federación |
| Administración de DS9 | instalación con gobernanza/mandos concretos | acceso a muelles, servicios y zona de operaciones habilitados | existencia de suministros infinitos o jurisdicción universal |
| Imperio Klingon | potencia interestelar | diplomacia y política según cargos y autoridad real | homogeneidad conductual de sus ciudadanos |
| Imperio Estelar Romulano | potencia interestelar | sus fronteras, restricciones y relaciones en fecha | desaparición forzosa en 2387 |
| Cardassia | civilización y estructuras políticas posguerra | reconstrucción y decisiones propias | un gobierno definitivo impuesto sin eventos |
| Dominio | poder del Cuadrante Gamma | decisiones sobre sus territorios y estructuras | que la derrota de 2375 signifique inexistencia |
| Colectivo Borg | red/organización tecnológicamente singular | acciones causalmente simuladas y observables | encuentros automáticos o conocimiento compartido con toda la Flota |
| Ferengi y operadores comerciales | estructuras culturales/económicas diversas | intercambios según contratos, recursos y relaciones | una economía universal uniforme |

**Reglas de competencia:** grado militar ≠ nombramiento ≠ permiso sobre instalación ≠ jurisdicción sobre planeta. Un capitán designado para una nave no es automáticamente presidente de una institución. Las directrices de confidencialidad, Primera Directriz, diplomacia, salud y seguridad se consultan por tiempo y por caso, no como permisos globales.

## 2. Fotografía de relaciones de 2383

La Federación mantiene su historia de cooperación y tensiones con Klingon, Romulanos, Bajor y Cardassia; las alianzas y tratados de la Guerra del Dominio proporcionan **antecedentes**, no un grafo que permanezca congelado. Una afirmación diplomática necesita fecha, órgano emisor, ámbito, consentimiento cuando corresponda y estado de vigencia. Diferenciar `relationship`, `treaty`, `current_access` y `rumor`.

El acceso a Delta y Gamma requiere rutas, contexto, autorización y validación; el proyecto no desbloquea el **portal Borg hexagonal** ni futuros idiomas/encuentros Delta por mencionar esos territorios.

## 3. Atlas de posiciones y rutas

| Lugar | Referencia / tipo | Límite de navegación y acceso |
|---|---|---|
| Tierra/Sol | sistema de origen institucional, ancla física | no fijar cuadrante Alfa/Beta universal sin respaldo |
| Vulcano | mundo de cultura vulcana; ancla histórica | coordenadas 40 Eridani no se afirman como pantalla sin fuente |
| Bajor y Deep Space Nine | mundo soberano + instalación orbital / geografía dinámica | tránsito DS9 sujeto a seguridad, jurisdicción y muelles disponibles |
| Agujero de gusano bajorano | corredor especial Alfa↔Gamma | conectar por condición del fenómeno, **no** por distancia warp euclidiana |
| Cardassia Prime | centro cardassiano, contexto posguerra | soberanía y estado de servicios independientes del catálogo |
| Qo'noS | mundo klingon | carta de acceso según gobierno/actor y fecha |
| Romulus | mundo romulano en corte 2383 | 2387 televisivo externo no se ejecuta automáticamente |
| Veridian III | lugar histórico de caída Enterprise-D | recuperación autorizada del platillo, no buque operativo en superficie |
| Wolf 359 | lugar histórico de batalla | su memorial no garantiza restos físicos ni misiones |
| Nebulosa Omarion | lugar vinculado a crisis de 2371 | información histórica, no coordenadas siempre reveladas |
| Localizaciones Voyager Delta | pasado documentado de la nave | no viaje/portal ni conocimiento global por lectura |

**Fuentes principales:** `mundo/lore/astrography/atlas/README.md`, `mundo/lore/astrography/systems/anchor_locations.json` (30 anclajes), `mundo/lore/astrography/spatial_regions/gameplay_regions.json` (12 regiones), `sistemas/gameplay/navigation/anchor_route_graph.json` (17 nodos/13 aristas), `sistemas/gameplay/navigation/initial_reference_distance_edges.json` (10 distancias de procedencia mixta), `political_space_state_anchors.json` y LORE-05C (16 entradas).

**No crear XYZ.** Un mapa de referencia visual, una mención en diálogo, una instancia física, una ruta transitable y un permiso de aterrizaje son cinco cosas diferentes. Lo procedural debe mantener `generated_identity`, semilla, existencia previa, procedencia, `discovery_state`, soberanía temporal y condiciones causales; no insertar mundos por necesidad de misión.

## 4. Reglas comprobables de generación

- Prohibido crear planetas ya ocupados por un ancla de identidad.
- Prohibido declarar una frontera precisa a partir de una etiqueta de mapa no contrastada.
- Prohibido inventar rutas seguras a través de anomalía por omisión de datos.
- No existe «descubierto para todos» cuando lo observa una nave.
- No existe «estación operativa» sin recursos, titular, empleados y estado temporal.
- El conocimiento del PADD del jugador **no excede** el permitido para ese observador; revocaciones también cuentan.
