# Investigación operativa transversal — A–H

Documento de síntesis **interpretativa**, vinculado a fuentes y a fichas del catálogo [operational_evidence_v0.1.json](operational_evidence_v0.1.json). Evita reproducir las monografías de A–D. Cuando se cita un episodio, el hecho audiovisual es punto de partida, no prueba de un procedimiento general que la serie no estipula.

## A. Sistemas y territorios: identidad ≠ situación política
**Evidencia:** `OP-A01`–`OP-A04`. La identidad física de un sistema de `mundo/lore/astrography/atlas/` es estable, mientras que jurisdicción, pertenencia, control militar, actividad económica y accesibilidad cambian por acontecimientos políticos. Bajor tras la ocupación es el ejemplo de cómo una misma instalación pasa de explotación cardassiana a centro de reconstrucción federobajorano; no se altera por ello la identidad del planeta ni se declara automáticamente que Bajor sea mundo miembro de la Federación (`DS9_EMISSARY`; `ST_OFFICIAL_STARBASES_FEDERATION`).

**Forma de leer un destino:** preguntar *qué objeto es* (sistema, planeta, instalación o región), *en qué fecha* y continuidad estamos, *qué poder afirma o ejerce control*, *qué presencia se documenta*, *quién informa* y *qué datos permanecen desconocidos*. `sol_system`, `bajor`, `deep_space_9` y `romulan_neutral_zone_near_galorndon` son identidades preexistentes; no crear campos ficticios de población, guarnición, coordenadas, recursos ni perímetro. El atlas distingue sector real o conjetural, espacio político y overlay de mapa de aficionado.

**Advertencia contextual:** un mapa histórico no prueba control actual, un tratado no crea propiedad de suelo por implicación y una fuerza ocupante no equivale siempre al soberano jurídico. Los asentamientos afectados por acuerdos federocardassianos no implican que toda su población se haya unido a los Maquis (`TNG_JOURNEYS_END`, `DS9_THE_MAQUIS_I`). Ver soberanía/control separados en `mundo/lore/diplomacy/geopolitical_layers_v0.1.json` y en el contrato procedural existente.

## B. Circulación, tránsito y acceso: cada caso necesita competencia local
**Evidencia:** `OP-B01`–`OP-B04`. El canon muestra zonas sensibles, escalas y puertos —por ejemplo K-7, DS9 y la Zona Neutral romulana—, pero no ofrece un código migratorio único para todas las potencias ni un listado universal de licencias de vuelo (`TOS_THE_TROUBLE_WITH_TRIBBLES`, `TNG_THE_NEUTRAL_ZONE`, `DS9_EMISSARY`).

**Consulta mínima no normativa:** origen/destino verificados, misión civil/científica/militar, bandera o propietario de la nave, lugar controlado frente a territorio reclamado, relación vigente según partida, instrucciones de misión, comunicaciones posibles, permiso expresamente conocido y riesgo no cuantificado. Si cualquiera es desconocido, contestar «no consta» y elevar a autoridad competente; **no** inventar respuesta de despacho, formulario fronterizo o estacionamiento concedido.

**Excepciones:** emergencia, visita diplomática, conflicto, desmilitarización y tregua pueden modificar criterios, pero sólo si existen fuentes o hechos persistidos. La alianza militar federorromulana desde 2374 no prueba libre acceso general a territorio romulano. El agujero de gusano bajorano es conexión singular Alfa–Gamma, **no** arista warp normal, ni invitación a abrir Delta. La estación de origen y la zona de destino no comparten necesariamente autoridad ni visibilidad.

## C. Comercio y recursos: acuerdos ≠ transacciones
**Evidencia:** `OP-C01`–`OP-C04`. DS9 documenta comercio y agentes privados —Quark es individuo y empresario, no voz automática del Gran Nagus—; el latinum es medio de intercambio observado, no tabla universal de precios (`DS9_THE_NAGUS`, `DS9_RULES_OF_ACQUISITION`). Las restricciones de producción y dependencia del ketracel blanco muestran que la existencia de una sustancia no garantiza disponibilidad para el demandante (`DS9_HIPPOCRATIC_OATH`, `DS9_TO_THE_DEATH`).

**Seis distinciones:** mercancía conocida ≠ stock presente; capacidad técnica ≠ producción local; interés comercial ≠ derecho de importación; transacción privada ≠ tratado interestatal; ruta que existe ≠ ruta segura; moneda usada ≠ cambio fijado. La información sobre minería forzada en Terok Nor durante la ocupación no autoriza extrapolar precios, volúmenes o permisos comerciales contemporáneos.

**Encaje futuro:** los contratos ya existentes `sistemas/gameplay/economy/`, `sistemas/universe/generation/procedural_civilization_economy_resource_trade_grammar_v0.1.json` y las invariantes de tráfico/conservación/stock son los dueños de decisiones técnicas. Esta fase no añade arbitraje, generación de convoyes, aranceles, embargo automático ni economía paralela.

## D. Ley, seguridad y jurisdicción: cargo ≠ competencia ilimitada
**Evidencia:** `OP-D01`–`OP-D04`. El mando operativo de una nave o de DS9 no implica potestad legislativa, jurisdicción penal extraterritorial, reconocimiento diplomático ilimitado ni detención sin base. La naturaleza de DS9 demanda distinguir autoridad civil bajorana, administración de Starfleet, autoridad funcional del oficial de servicio y condiciones concretas del acuerdo vigente (`DS9_EMISSARY`).

**Categorías no intercambiables:** ley local/federal, reglamento profesional de Starfleet, orden de mando válida, fuerza militar extranjera, servicio de inteligencia, autoridad provisional, organización clandestina y persona particular. La pertenencia a Maquis o Sección 31 no legitima ni condena automáticamente a un individuo por mera asociación. Separar sospecha, indicio, testimonio, propaganda y hecho judicialmente establecido (`DS9_THE_MAQUIS_I`, `DS9_INQUISITION`).

**Límites:** no se presume extradición, convenio penal, inmunidad diplomática, poder de abordaje, derecho a registrar equipajes ni jurisdicción marítima extrapolada del presente terrestre. En guerra u ocupación, competencia y cadena de mando pueden variar: el registro histórico no resuelve la autorización de un capitán para su situación concreta.

## E. Comunicaciones y conocimiento: transmisión ≠ recepción ≠ verdad
**Evidencia:** `OP-E01`–`OP-E04`. La red subespacial permite comunicación extensa, pero el canon no justifica instantaneidad incondicional ni cifras fijas para toda distancia, daño o interferencia. Un informe puede tener emisor falso, retraso, interceptación, secreto, interpretación errónea o destinatario restringido (`MA_SUBSPACE_COMMUNICATION`, `DS9_IN_THE_PALE_MOONLIGHT`).

**Distinguir siete capas:** acontecimiento real → medición observable → registro/versión → mensaje transmitido → mensaje recibido → comprensión o creencia personal → autorización para revelar/actuar. Un informe visualizable en un terminal no concede los derechos de acceso de otros terminales ni la autoridad de mando del emisor.

**Defensa contra omnisciencia:** el canal de conocimiento de un civil, un alférez y un almirante puede ser distinto, también entre miembros de una misma especie o gobierno. El contexto para IA debe proceder de proyecciones autorizadas del Core; no adjuntar toda la base histórica a una respuesta NPC. Un actor puede equivocarse o mentir sin que la base de hechos cambie.

## F. Ciencia y tecnologías: saber ≠ construir ≠ utilizar
**Evidencia:** `OP-F01`–`OP-F04`. La disponibilidad de dispositivos (teletransporte, ocultación, sensores, comunicaciones, tratamiento médico o tecnologías Borg) varía por cultura, nave, fecha, jurisdicción, energía, materiales, formación y situación táctica. El catálogo de clases y `sistemas/gameplay/ship_operations/era_technology_matrix.json` contiene tecnología de la Flota y no debe duplicarse aquí.

**Preguntas correctas:** ¿conoce el actor que existe esa tecnología?, ¿se ha descubierto en la campaña?, ¿la entidad dispone realmente de ella?, ¿su instalación es compatible?, ¿hay personal, alimentación y recursos?, ¿puede su titular utilizarla legalmente?, ¿qué riesgos son solo hipotéticos? Las naves romulanas con ocultación no implican ocultación de todas las naves romulanas, ni su empleo por cualquier aliado (`TNG_THE_ENEMY`). El ketracel es ejemplo de recurso médico sensible que no pasa a ser de libre obtención por ser conocido.

**Límite temporal mayor:** una solución aprendida por Voyager en Delta o por encuentros Borg posteriores no aparece en retrospectiva en la consola de una nave Alfa anterior. Los descubrimientos que suceden *después* de arrancar partida no ocurren automáticamente en la campaña.

## G. Primer contacto e interacción intercultural: culturas no son scripts
**Evidencia:** `OP-G01`–`OP-G04`. Mintaka demuestra los daños de una observación clandestina expuesta; Malcor enseña que un encuentro institucional no implica aceptación social. La Primera Directriz es una obligación real contextual, no un gatillo «warp alcanzado = contacto automático» (`TNG_WHO_WATCHES_THE_WATCHERS`, `TNG_FIRST_CONTACT`).

**Protocolos de lectura, no mecánicas:** identidad y mandato de quien acude; percepción del otro interlocutor; traductor y margen de ambigüedad; consentimiento; normas y compromisos documentados; historia de exposición externa; impacto cultural y evaluación de riesgo. El traductor convierte lenguaje, no crea un tratado ni garantiza que se comprendan conceptos jurídicos.

**Individualidad:** una persona bajorana puede ser religiosa, crítica, indiferente o disidente; un romulano puede desafiar a su gobierno; una figura ferengi puede trabajar por valores distintos a los de Quark. Los perfiles de A y A.1 son referencias para un NPC único, junto a experiencia, objetivos, rol y memoria, nunca tablas de gestos obligatorios.

## H. Ciencia civil y respuesta humanitaria: urgencia no materializa infraestructura
**Evidencia:** `OP-H01`–`OP-H04`. Starfleet participa en exploración, defensa y ayuda; DS9 sirve a la recuperación de Bajor. Las misiones de rescate y las preocupaciones no intervencionistas coexisten: `TNG_HOMEWARD` no concede una exención sistemática ante toda emergencia (`ST_OFFICIAL_STARBASES_FEDERATION`, `TNG_HOMEWARD`).

**Condiciones documentales a reunir:** situación y petición, gobierno/contacto competente, ubicación y acceso, gravedad observada, formación y recursos reales, capacidad de evacuación, riesgos de contagio o contaminación cultural, cadena de mando y registro de consecuencias. Un científico civil no recibe capacidad militar por título; un médico puede conocer un tratamiento sin materiales, acceso o consentimiento.

**Escenarios futuros sin implementarlos:** exploraciones, arqueología, rescate, evacuaciones, viajeros, asentamientos, hospitales y convoyes son contextos posibles sólo si las capas de estado (gente, equipo, instalaciones, comunicaciones, recursos y autoridad) los sostienen. La emergencia debe originar decisiones, no crear de la nada un centro logístico.

## Régimen de confianza y lagunas

Cada ejemplo enlaza sus fuentes en el catálogo y mantiene `confidence` separada de `provenance_class`. La observación en pantalla puede ser sólida y la interpretación institucional seguir siendo **INFERRED**. Muchos permisos, tarifas y competencias carecen de detalle canónico; quedan **UNKNOWN** antes que una simulación pretendidamente canónica.

La investigación es un puente de consulta. **No** se garantiza exhaustividad de leyes, economías, sistemas, hospitales, negociaciones o capacidades de todas las civilizaciones de Star Trek.
