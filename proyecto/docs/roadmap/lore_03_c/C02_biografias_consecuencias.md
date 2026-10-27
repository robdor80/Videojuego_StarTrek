# C02 — Biografías y consecuencias personales
**Ámbito:** integración editorial; no crea NPC canónicos, traumas, diagnósticos ni equipamiento.

## Enlace causal de una biografía
**Identidad estable** → nacimiento/origen (o desconocido) → acceso real al territorio, institución y tecnología → intervalo del hecho según LORE-03A/B → condición de testigo/participante/receptor de información → referencias de fuentes/servicio → recuerdo y conocimiento separados → consecuencias representadas. No inferir participación por haber nacido en un planeta ni por compartir especie/facción.

Una biografía generada *hipotética* se identifica como `GAME_ADDITION_EXAMPLE_NOT_INSTANTIATED`; puede explicar una posible historia, pero no se concede a una persona materializada sin que el generador y CoreRPG creen y validen las relaciones correspondientes. Los vacíos biográficos son desconocidos, nunca se rellenan con hazañas extraordinarias.

## Reglas de edad, disponibilidad y lugar
- Año de nacimiento menor o igual al año del suceso; si la participación exige adultez/formación, acreditar madurez equivalente **individual y cultural** y tiempo de entrenamiento, no asignar una edad universal para todas las especies.
- Acontecimientos fechados solo por año no autorizan afirmar que un cumpleaños o despliegue ocurrió *antes* del suceso ese mismo año. Resultado: `UNRESOLVED_SAME_YEAR` hasta existir mayor precisión.
- Participación directa requiere evidencia o procedencia explícita de destino, viaje y posición. Un rango o una afiliación no demuestran presencia.
- Un descendiente puede conocer por transmisión familiar un episodio anterior a su nacimiento, nunca recordar haberlo vivido.
- El servicio a bordo de una nave específica exige vinculación autorizada del buque/periodo/destino, no solo que la nave aparezca en el evento.
- Asignaciones, muertes, condecoraciones, promoción, retirada y heridas son sucesos persistentes independientes del recuerdo.
- No dar automáticamente dolor, enfermedad, xenofobia, rencor o heroísmo a supervivientes, refugiados o veteranos. Son consecuencias individuales condicionadas por eventos, atención, cultura y decisiones.

## Efectos, sin automatismo
**Factibles tras evidencia:** cambio de domicilio, familiares desaparecidos, pérdida económica, traslado, nueva vocación, esfuerzo de reconciliación, amistades, desconfianza puntual, reconocimiento de un superior. **No hechos por defecto:** estrés clínico, culpabilidad, conducta anti-Borg, odio anti-cardassiano, afiliación política unánime. Una relación no es la suma de recuerdos del observador; depende de su grafo y causas.

## Ejemplo sin NPC real creado
`case_wolf_survivor`: oficial **ficticio** nacido en 2341, destino previo hipotético y evidencia de participación por aprobar; puede relatar Wolf 359 si se validan su hoja de servicio, disponibilidad temporal y memoria. Quien escuchó el relato no obtiene experiencia en primera persona. No declaramos que esa persona sirvió en USS Saratoga; la afirmación exigiría prueba individual de destino.

## Dependencias
`sistemas/gameplay/character_creation/biography_validation_rules.md`, `character_definition_contract.json`, `generated_character_rules.json`, `service_record_model.json`, `relationship_change_provenance_contract.json`, `character_memory_lifecycle_contract.json`. Preservar edad e identidad al cambiar LOD/guardar.
