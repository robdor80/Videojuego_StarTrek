# LORE-04A / A02 — Marco inicial de sociedad y vida cotidiana

**Estado:** `COMPLETE_DOCUMENTARY_CANDIDATE_IN_DRAFT`, no canon nuevo aprobado ni implementación. **Ámbito:** sociedad civil durante TNG/DS9/Voyager y continuidad abierta. **Procedencia:** referencias al canon existente, perfiles de LORE-01 y contratos ya vigentes. Lo desconocido permanece `UNKNOWN`.

## 1. Qué existe antes de que llegue el jugador

Un asentamiento tiene población, hogares, actividades y servicios con **causas**: emplazamiento, recursos, producción, historia, instituciones y transporte. Un individuo importante procede de un puesto/espacio de población existente; una vez materializado persiste con `character_id`, domicilio, relaciones, historia, empleo/función y presencia compatible con su agenda. Las poblaciones latentes se representan agregadas. La presencia del jugador no autoriza materializar vecinos arbitrarios, abrir un servicio inexistente ni mover gente por teletransporte narrativo.

Reutilizar directamente `persistent_population_materialization_rules.json`, `social_simulation_lod.json`, `relationship_graph_model.json` y `sistemas/universe/generation/settlement_infrastructure_contract.json`.

## 2. Dimensiones documentales por comunidad

| Dimensión | Preguntas del juego | Restricciones |
|---|---|---|
| Hogar y parentesco | ¿Dónde vive? ¿Con quién convive? ¿Qué obligaciones y apoyos tiene? | Familia, convivencia, especie, ciudadanía y afiliación política son ejes **distintos**; vínculos referenciados, no presupuestos |
| Educación y aprendizaje | ¿Quién ofrece formación? ¿Qué acceso tiene esta persona? | Academia de Flota no equivale a educación civil universal; no inventar currículos obligatorios |
| Oficios y actividades | ¿Qué función presta y por qué existe? ¿Quién administra su puesto? | No asumir salarios, equivalencias monetarias ni oficio por especie; servicios con personal/capacidad real |
| Atención y necesidades | ¿Qué servicios existen y quién tiene acceso? | Cuidado, salud, suministro, vivienda y reparación dependen de jurisdicción y disponibilidad; no replicadores milagrosos |
| Ocio y comunidad | ¿Qué lugares están abiertos, con qué aforo y horarios? | Preferencias y tradiciones personales no determinan automáticamente rutina; privacidad y consentimiento conservados |
| Movilidad cotidiana | ¿Cómo llega a su destino? | Desplazamiento consume tiempo; restricciones de ruta, puesto y jurisdicción |
| Conocimiento social | ¿Qué sabe de sucesos/personas? | Se distingue verdad del mundo, recuerdo, rumor y observación; la IA solo verbaliza lo conocido |

La vida civil puede tener festividades, rituales y horarios diferentes, pero ninguna fecha, obligatoriedad o distribución social se añadirá a canon sin una fuente concreta o autorización `GAME_ADDITION`.

## 3. Contextos sociales: diferencias sin estereotipos

- **Federación / Tierra / mundos miembros:** ciudadanía y cultura no equivalen a servicio en Flota. Coexistencia multicultural, hogares, ciencia, cuidado, hostelería y artes son **categorías plausibles para estudiar**, no distribución estadística canónica. Ninguna norma económica universal para todos los miembros; gobiernos planetarios y Federación no se sustituyen.
- **Klingon:** Casas, honor, reputación, artes, servicio y familia pueden afectar expectativas situadas; civiles y profesionales no combatientes deben ser posibles. Un klingon no nace guerrero ni su ocupación se deriva de su especie. Perfil base: `KLINGON_CULTURAL_PROFILE_v0.1.json`.
- **Romulano:** instituciones y cultura de seguridad pueden afectar información pública y privada, pero ciudadanía no implica pertenencia a Tal Shiar, deslealtad o engaño. Perfil: `ROMULAN_CULTURAL_PROFILE_v0.1.json`.
- **Cardassiano:** instituciones, legado de la ocupación y la reconstrucción pueden alterar la vida familiar y laboral **según época y localidad**; nadie hereda automáticamente culpabilidad o ideología. Perfil: `CARDASSIAN_CULTURAL_PROFILE_v0.1.json`.
- **Ferengi:** comercio, contratos y latinio son relevantes para muchos entornos; no todos son mercaderes, ni se atribuye fraude. No anticipar ni congelar reglas sociales de cada época tras los cambios mostrados en DS9. Perfil: `FERENGI_CULTURAL_PROFILE_v0.1.json`.
- **Bajorano:** memoria de ocupación, soberanía, agricultura y tradiciones religiosas pueden influir en los contextos, pero no todos practican una misma fe ni fueron resistentes. Gobierno, Milicia e instituciones religiosas tienen autoridades separadas. Perfil `BAJORAN_CULTURAL_PROFILE_v0.1.json`.
- **Vulcano, andoriano, tellarita, trill, betazoide y otros:** reutilizar sus perfiles de LORE-01 y fichas territoriales; no componer «carácter de especie» a partir de biología.

Todos estos puntos son **reglas de aplicación** de perfiles existentes, no afirmaciones sobre el porcentaje de población que sigue cada tradición.

## 4. Tres ejemplos documentales no canonizados

**Caso CIV-01, poblado federado con centro de formación.** Un docente civil presta servicio en horario derivado de un centro existente, convive con personas persistentes y puede no estar disponible cuando el jugador llega. El diálogo conoce solo hechos observados; no obtiene instantáneamente detalles privados de un cadete.

**Caso CIV-02, enclave comercial ferengi.** Una persona que administra un local puede aceptar un pago/canje solo si jurisdicción, inventario, medio de intercambio, acceso y autorizaciones lo permiten. Un personaje ferengi que no trabaja como comerciante es igualmente válido. Las operaciones no consumadas no transfieren bienes.

**Caso CIV-03, estación bajorana.** Un litigio local se canaliza hacia una competencia civil o judicial real, si está definida. La presencia de personal de Flota no otorga jurisdicción civil universal. La Milicia no es lo mismo que una autoridad religiosa.

Estos casos son `GAME_ADDITION` **propuesta de escenarios de prueba**, sin nombres propios, lugares canonizados, suceso obligatorio ni contratos nuevos.

## 5. Frontera de integración

**Entradas:** `campaign_date`, `location_id`, `civilization/polity`, `culture_refs` documentadas, `entity_id`, horarios/roles/relaciones ya materializados, recursos/servicios, jurisdicción, conocimiento del observador.
**Efecto permitido en esta fase:** restricciones para interpretación, presentación y futuros fixtures. **No** emisión en vivo de acciones, ticks, mutaciones, inventario, NPCs ni calendarios autónomos.
**Futuro runtime:** CoreRPG valida disponibilidad, tiempo, autoridad, legalidad, recursos y transición; produce evento persistente; los NPC/IA/UE5 reciben la observación filtrada. No autorizar una segunda fuente de verdad.

## 6. Fuentes de verificación y pendientes

- Canónicos a contrastar en episodios/películas: *Star Trek: First Contact* (conversación de Picard sobre dinero en su sociedad), escenas de bar/latinio y vida civil en *Deep Space Nine*, episodios TNG/DS9 sobre familias y gobiernos. **No atribuir a esas escenas detalles no pronunciados**.
- Apoyo editorial verificado (no `SCREEN_CANON` por sí solo): `L04A_ST_LATINUM` (https://www.startrek.com/news/star-trek-101-latinum); `L04A_ST_FAMILY` (https://www.startrek.com/news/your-ultimate-star-trek-picard-watch-guide); `L04A_ST_SCHOOL` (https://www.startrek.com/news/deep-space-nine-modern-balance-science-religion).
- Pendientes de A03–A07: fichas por servicio y jurisdicción, fuentes audiovisuales granulares, escenarios de ausencia/inaccesibilidad, educación civil fuera de Academia, métricas de densidad social sin cifras inventadas, cobertura de otras culturas.
- **Gate del autor:** no fijar todavía moneda/ingreso universal, derecho de vivienda, ritual obligatorio, oficio único o modelo constitucional no acreditado.

## 7. Criterios de cierre de A02

La capa es una **base documental inicial**, no el cierre de toda A. Se revisarán los escenarios contra A01, la política de canon y los invariantes de `lore04a_civil_society_invariants_v0.1.json` antes de elevar cualquier estado a `COMPLETE_DOCUMENTARY`.

## 8. Evidencia contrastada y cierre de paquete

Las afirmaciones y sus restricciones están trazadas en `lore04a_evidence_ledger_v0.1.json`: LA-E01 (familia Picard), LA-E02 (bodas y ocio), LA-E03 (educación de Keiko), LA-E05 (Casas klingon), LA-E07 (cambios sociales ferengi), LA-E09 (responsabilidad cardassiana). Las referencias de StarTrek.com corroboran el contexto de los episodios, **sin certificar su minutaje ni justificar normas sociológicas universales**. La distinción `SCREEN_CANON` / `OFFICIAL_REFERENCE` / `INFERRED` / `GAME_ADDITION` es obligatoria.

El documento, con el resto de A01–A08, queda **preparado como candidato documental**. No se extiende el motor de relaciones, ni la Academia, ni la economía de Bloque 4, ni se declara la simulación ejecutada. La revisión del autor y la fusión siguen pendientes.
