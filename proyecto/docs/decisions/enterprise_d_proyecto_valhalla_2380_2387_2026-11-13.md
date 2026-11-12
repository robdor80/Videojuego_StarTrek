# DEC-0020 — Enterprise NCC-1701-D, reconstrucción Proyecto Valhalla

**Aprobación del autor:** 13 de noviembre de 2026 · **Estado:** APROBADA EN DISEÑO / GAME_ADDITION · **Ámbito:** LORE-05A, LORE-03, F01, F04, F06, F07, F10, F11, HOST, temporada y dirección artística.  
**No constituye integración CoreRPG/Unreal ni alteración automática de una campaña.**  
**Referencia estructurada:** `mundo/lore/starships/individual_ships/project_valhalla_enterprise_d_v0.1.json`.

## Decisión vigente

1. La nave objetivo de esta campaña es la **USS Enterprise NCC-1701-D**, identidad individual conservada, **clase Galaxy**. No es una clase nueva ni se rebautiza la nave como «Valhalla».
2. **Proyecto Valhalla** designa exclusivamente el programa de **recuperación, reconstrucción y modernización** de la Enterprise-D, bajo la dirección de **Geordi La Forge** en la continuidad propia del videojuego. Se preserva la identidad e historia anterior de la nave.
3. Se mantiene la cronología autoral aprobada en DEC-0013–0016, **reinterpretada como programa de reconstrucción**: gestación institucional **2379**, trabajos **desde 2380**, **2383** Academia/auge de Odyssey con Enterprise-D todavía en obras y objetivo de entrada en servicio **2387**; día, mes, configuración final, fecha efectiva y disponibilidad de plazas permanecen abiertos.
4. Al terminar los cuatro cursos de Academia hacia **2387**, el jugador es alférez; el acceso a la Enterprise-D necesita destino válido, plaza, requisitos y órdenes. **No recibe mando ni plaza de forma automática**. La futura carrera puede conducir a su capitanía mediante las reglas de F11.
5. **Odyssey** está operativa y es la punta de lanza tecnológica en 2383 como `GAME_ADDITION`; la **Enterprise-F individual** no se materializa automáticamente. Los experimentos de **flujo cuántico** en Odyssey desde 2383 **no** se transfieren automáticamente a la Enterprise-D de 2387.
6. El diseño de interiores **Galaxy Refit A2**, separación de secciones, biblioteca arquitectónica, proyecto auxiliar Defiant y otras elecciones técnicas anteriores se conservan como **propuestas específicas sometidas a compatibilidad, instalación y validación**, no como capacidades reales otorgadas por esta acta.

## Canon y divergencia, expresamente separados

- **Canon de pantalla:** la Enterprise-D sufre la pérdida de su sección motriz y el aterrizaje del platillo en **Veridian III (2371)**. El platillo se recupera. En **Star Trek: Picard** se revela que Geordi había reconstruido la nave durante **aproximadamente dos décadas** y que en **2401** estaba con un casco secundario de la **USS Syracuse**. Este resultado **no había sucedido en 2387** en la continuidad televisiva.
- **Aportación del videojuego:** el **nombre Proyecto Valhalla**, su origen institucional en **2379**, comienzo de trabajos en **2380**, dirección del programa por La Forge desde esa fecha como decisión creativa, modernizaciones y **objetivo anticipado de 2387**. Es una divergencia narrativa consciente; no citarla como `SCREEN_CANON`.
- **Sin resolver:** casco secundario/donante de 2387, calendario exacto, grado técnico de avance, recursos, responsabilidades administrativas y fecha real de alta. El casco secundario **Syracuse** queda como hecho de la continuidad de *Picard* hacia 2401, **no** como asignación obligatoria al vehículo de la campaña en 2387. Tampoco atribuir a La Forge en 2380 el puesto/rango que ostenta en *Picard* en 2401.
- La reconstrucción narrada en *Picard* es **referencia de una posible continuidad**. A partir del corte de inicio de campaña 2383, el futuro es emergente: ni 2387 ni 2401 imponen un resultado ya consumado al WorldState.

**Fuentes oficiales editoriales (referencias a la obra, no certificación de visionado escena a escena):**

- [StarTrek.com — Recap Picard 3x09 «Võx»](https://www.startrek.com/news/recap-star-trek-picard-309-vox): platillo recuperado, reconstrucción durante aproximadamente veinte años.
- [StarTrek.com — It's the Enterprise! Starfleet's Finest Flagships](https://www.startrek.com/news/ships/enterprise-starfleets-finest-flagships): 2401 y combinación con casco de Syracuse.
- [StarTrek.com — The Journey from Star Trek Generations to Picard's Final Season](https://www.startrek.com/news/journey-from-generations-to-picard): Veridian III, restauración y Syracuse.

## Precedencia respecto a lo aprobado antes

Esta acta **sustituye exclusivamente la identidad y el propósito** de DEC-0001/DEC-0015 y sus derivados donde consideraban que la **nueva clase Valhalla** sería la nave protagonista de la campaña. **No revoca** por defecto el calendario 2379–2387, Odyssey 2383, investigación cuántica, la filosofía de seguridad, la distribución de tripulación o las ideas aprobadas: cada subsistema se migrará o revisará en su fase propietaria.

La clase histórica `valhalla` del catálogo y el registro `valhalla_tech_decisions_v0.1.json` permanecen por compatibilidad y trazabilidad. **No seleccionarlos como identidad del buque objetivo** y **no eliminar ni renombrar IDs** hasta una migración explícita, con pruebas de consumidores y guardados. La entidad `uss_enterprise_ncc_1701_d` y `class_id=galaxy` son las referencias presentes de esta decisión.  
La plantilla F04 «1.800 Flota + 400 civiles» continúa registrada como **herencia del diseño anterior**, no como dotación ratificada para la Enterprise-D modernizada sin auditoría de capacidad y convivencia.

## Autoridades y puertas

- **Star Trek LORE/decisiones:** identidad, genealogía, canon, programa y referencias documentales.
- **CoreRPG:** fecha real por partida, eventos aceptados, identidad persistente, acciones, guardado y estado de nave. Este documento no escribe WorldState.
- **F04/F06/F07:** dotaciones, sensores, perfil tecnológico y geometría; adaptación por contrato/proyecto individual y pruebas.
- **F10/F11:** Academia, ofertas, sucesiones y oportunidades de acceso sin falsificar vacantes.
- **HOST/UE5/IA:** presentar solo datos autorizados, no declarar lanzamientos ni restauraciones por lenguaje generado.

**Estado administrativo de LORE-05A:** candidata documental hasta CI y fusión verificada. Ni esta acta ni su PR hacen `CONTENT_STATUS.md` COMPLETE antes del cierre.
