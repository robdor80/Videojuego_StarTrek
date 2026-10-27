# C05 — Relaciones, veteranos, familias y experiencias compartidas
**Frontera:** ninguna relación, personaje o unidad histórica se crea por escribir este documento.

## Vínculo previo a la campaña
La amistad, rivalidad, obligación, parentesco, mentoría y reconocimiento requieren **referencias de contexto compartido y procedencia**, no proximidad ni coincidencia de especie/organización. Separar (a) verdad de que ocurrió el encuentro, (b) conocimiento que A tiene de B, (c) recuerdo que A conserva y (d) relación A→B, que puede diferir de B→A.

### Cadena para dos veteranos
1. Suceso original identificado: p. ej. `wolf_359_battle` (2367 aproximado), o `dominion_war_begins` (2373).
2. Cada biografía confirma **participación individual válida** y encuentro compartido o comunicación posterior. Haber participado en la misma guerra no demuestra conocerse.
3. `relationship_change_provenance_contract.json` autoriza un estado inicial A→B y B→A; si faltan encuentros verificables no se crea amistad antigua.
4. `character_memory_contract.json` puede contener dos interpretaciones distintas de un mismo encuentro. Reunirse en 2383 no exige que ambos recuerden el nombre, lugar exacto o sentimientos del otro.
5. La relación cambia solo por interacciones representadas, también fuera de escena con comunicaciones y tiempos reales; la IA no la altera para facilitar un diálogo.

### Familias y transmisión
`kinship_family_network_contract.json` conserva vínculos tras separaciones y fallecimientos; `social_knowledge_propagation.json` exige un canal real para heredar *conocimiento*. Un descendiente de desplazados por la ocupación bajorana puede conocer relatos familiares sin tener recuerdos en primera persona de la ocupación. Un silencio familiar no crea conocimiento oculto.

### Pérdidas y duelo
`death_destruction_mourning_continuity_contract.json`: la muerte no borra la identidad ni los registros; el aviso de muerte puede demorarse y las respuestas son personales. No se aplica un reloj universal del duelo, diagnóstico automático ni conducta compulsiva. Un pariente puede ignorar inicialmente lo sucedido aunque CoreRPG lo haya registrado.

### Reconciliación
Puede existir amistad profesional con discrepancias políticas, colaboración entre antiguos adversarios y perdón parcial. Reconciliación no borra historial de conflictos. Las dimensiones confianza, respeto, afecto, miedo y resentimiento son independientes, asimétricas y pueden evolucionar gradualmente.

## Pruebas de rechazo
Se rechaza: «dos cardassianos se conocen por haber servido en la guerra», «toda víctima tiene trauma», «el hijo recuerda haber combatido antes de nacer», «ser familiar concede secretos», «un año transcurrido crea automáticamente mejores amigos», «la muerte elimina toda relación». Escenarios con actor ficticio en `mundo/lore/historical_events/lore03c_memory_casebook_v0.1.json`.
