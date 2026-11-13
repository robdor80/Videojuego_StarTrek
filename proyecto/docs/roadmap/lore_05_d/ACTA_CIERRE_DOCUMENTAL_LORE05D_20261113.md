# LORE-05D — Auditoría y acta de cierre documental

**Fecha:** 13-11-2026 · **PR:** [#128](https://github.com/robdor80/Videojuego_StarTrek/pull/128) · **Ámbito:** documental, sin ejecución de simulador.

## Qué se ha cerrado
1. **8 naves individuales** del catálogo canónico existente; pasado histórico, proyecto, clase y estado 2383 separados.
2. **12 instalaciones reservadas** con identidad documental, diseño y posibilidades de escena; no se inventan propietario, operador, personal, inventario, atraque o actividad actual.
3. **8 potencias políticas** enlazadas a sus fuentes; además Gobierno civil de Federación y Flota Estelar representados como instituciones diferentes.
4. **18 casos** de consulta y respuesta esperada (NO ejecución CoreRPG).
5. Guía en castellano, JSON, validador Python, pruebas adversariales y workflow CI independiente.

## Coherencia de canon y decisiones
- USS Enterprise NCC-1701-D: clase Galaxy, misma identidad; Proyecto Valhalla repara/reconstruye ese buque desde 2380 como `GAME_ADDITION`, sin garantizar terminación en 2387. Geordi la Forge dirige el proyecto como decisión autoral.
- USS Defiant NX-74205: destrucción histórica en 2375. USS São Paulo posteriormente rebautizada Defiant **no** es la NX-74205. Aquí no se crea un ID de nave nuevo.
- Odyssey/Sovereign: clases no crean identidades individuales, incluso cuando el juego contempla buques de ellas. No nace automáticamente USS Enterprise-F.
- Los buques del siglo XXIII permanecen como historia, no como naves activas en 2383.
- Una instalación designada no se multiplica por compartir diseño; la situación 2383 depende del estado vivo, no del catálogo.
- Federación civil != Flota Estelar != Bajor u otros gobiernos; el rango militar no sustituye competencias civiles ni la cadena de mando F11.
- Elenco LORE-05B permanece en 12 personajes; no hay cambios en biografías, grados, agendas ni activos 3D.

## Resultado de validación del HEAD previo al acta
`de4f7d1f507c7cf106fab1b0e9b550b4e8be4bc0`:
- [CI LORE-05D #43354375724](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43354375724) **SUCCESS**.
- Validador: **8+12+8+2 identidades y 18 casos** PASS.
- Suite Python: **25/25** PASS.
- Workflows de ese HEAD: **7/7 SUCCESS** (LORE-05D, LORE-05A, LORE-01E, P2-B07/B08/B09/B10).
- Esta evidencia **no** sustituye la CI de la última revisión, posterior al acta y actualización de índices.

## Fronteras de producto no traspasadas
Sin cambios de contratos CoreRPG, estado galáctico P2, F04, F11, HOST, UE5, cartas de navegación, física de las naves, plan de instalaciones, biografías de LORE-05B ni geometría Valhalla. Ninguna misión, inventario, permiso, nueva unidad ni visual se añade al runtime.

## Riesgos y pendientes delegados
- No hay ID individual de São Paulo en el catálogo previo: si una misión lo precisa, abrir expediente de identidad en la fase propietaria; no reciclar el ship_id de Defiant original.
- No hay estado operacional verificable para todos los buques e instalaciones en 2383; consultar WorldState e historia real del save.
- No se fija qué astillero reconstruye Enterprise-D ni la fecha efectiva de alta.
- No se asignan poderes del almirantazgo, del Alto Consejo, Tal Shiar, Consejo Federativo o gobiernos bajorianos por texto narrativo.
- Modelos 3D, interiores y fuentes de imagen deberán comprobar licencias y adaptarse a las fases técnicas.

**Decisión:** contenido de LORE-05D completo en alcance documental y listo para revisión de PR tras validación de HEAD final. El cierre no es una certificación de mundo en marcha.
