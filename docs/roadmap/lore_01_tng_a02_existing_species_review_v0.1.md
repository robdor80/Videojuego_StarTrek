# LORE-01 A02 — Auditoría de especies preexistentes (TNG)
**Estado:** Revisadas documentalmente; sin editar ni invalidar perfiles aprobados.
**Alcance:** 15 especies + 1 estado Borg; referencias vigentes a archivos originales.
**Política:** `sources/canon_policy.md`, `sources/provenance_policy.md`.
## Hallazgos transversales
- `gameplay/species/profiles/` es la fuente actual de perfiles de biología, no `lore/species/`. Mantener sus IDs.
- 12 perfiles culturales de profundidad en `lore/cultures/profiles/`; asociación contextual **nunca adjunción automática**.
- Existe variación en secciones (`physiology`, `biology`, `lifecycle`, `joining`), conforme a contratos de autoría ya existentes. No intentar migración masiva incompatible.
- Falta evidencia puntual para algunas afirmaciones; **no elevar por etiqueta general el nivel de confianza**.
- Las referencias a ENT de Andorian, Aenar y Tellarite están en archivos preexistentes. Dado que `sources/canon_policy.md` delimita obras retenidas, tratarlas como **legado extramuros de selección** en este paquete, mantenerlas materialmente sin cambios y no presentarlas como evidencia TNG/DS9/VOY. Requieren revisión caso a caso antes de extraer nuevos hechos para el juego.
## Matriz de auditoría
| Perfil | Cultura preexistente | Riesgo específico / trabajo de autor |
|---|---|---|
| human | HUMAN_FEDERATION_CULTURAL_COMPOSITION | No presumir ciudadanía de Federación ni cultura terrestre común. |
| vulcan | VULCAN | TOS y VOY apoyan capacidades; pon farr/telepatía dependen del individuo y privacidad. |
| andorian | ANDORIAN_AENAR | Evidencia de anatomía ligada a ENT no retenida: conservar **marcada para contraste**; no inventar uso de antenas. |
| aenar | ANDORIAN_AENAR | Condición de población diferenciada y evidencia ENT; no extrapolar telepatía idéntica a Andorian. |
| tellarite | TELLARITE | Normas de discusión proceden en parte de ENT: confirmar con material retenido antes de atribuirlas universalmente. |
| klingon | KLINGON | Honor, Casa, profesión, ciudadanía y mentalidad separadas. |
| romulan | ROMULAN | El Tal Shiar no representa a todos los individuos; estado político depende de fecha. |
| cardassian | CARDASSIAN | No imputar militancia ni responsabilidad por ocupación de Bajor a cada personaje. |
| bajoran | BAJORAN | Fe individual y vínculos con Resistencia no son automáticos. |
| ferengi | FERENGI | Reglas de Adquisición y negocios no imponen carácter ni profesión. |
| trill | TRILL | Hospedador unido, sin unir y simbionte tienen identidades/estados diferenciados. |
| betazoid | BETAZOID | Solo `MA_BETAZOID` en ficha individual: buscar evidencias TNG para capacidades y limitaciones; no telepatía omnisciente. |
| changeling | DOMINION | Imitar aspecto no concede recuerdos ni autorizaciones. |
| vorta | DOMINION | Ingeniería genética y función institucional no equivalen a obediencia perfecta de todo individuo. |
| jem_hadar | DOMINION | Dependencia de ketracel-white es estado médico/operativo, no juicio de carácter. |
| borg_assimilated_character | ninguno automático | Transformación con especie original conservada; Borg **no es especie biológica de origen**. |
## Dictamen de compatibilidad
- **No se detecta necesidad de migrar los contratos existentes** para añadir el nuevo catálogo: las fichas enriquecen contenido, no mutan resolución de acciones.
- Restricción de no generación: las nuevas especies Delta se mantienen como datos **DLC únicamente**, y el Borg ya existente en el juego principal **no queda prohibido** por ello.
- Las fichas nuevas no se transforman en estados de CoreRPG por existir en GitHub; validación documental y runtime son puertas distintas.
## Evidencia adicional a revisar en iteraciones
- TNG: "Haven", "The Price", "The Loss" y otros episodios con Betazoides/Deanna para respaldar límites telepáticos (no son revisiones automáticas de la ficha).
- Andorian/Aenar/Tellarite: usar exclusivamente datos del corpus seleccionado al redactar material nuevo; mantener `NEEDS_REVIEW` donde el dato conocido solo proceda de ENT.
- Datos numéricos no avalados (vida media universal, reproducción, medicina), en blanco/null con política `unknown`.
