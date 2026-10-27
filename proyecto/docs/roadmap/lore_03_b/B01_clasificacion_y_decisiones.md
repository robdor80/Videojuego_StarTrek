# B01 — Taxonomía, principios y decisiones editoriales

**Base documental: main@a5f76737; integración sobre main@9cc9c240` · **Estado:** propuesta completa para validación del autor, sin activar sistemas.

## Separación estricta de conceptos

| Etiqueta conceptual | Qué requiere | Qué NO presupone |
|---|---|---|
| Protesta o litigio diplomático | Reivindicación y respuesta política | Guerra ni ruptura de relaciones |
| Crisis fronteriza | Posiciones rivales, amenazas o incidente | Beligerancia declarada |
| Incidente armado | Uso localizado de fuerza con protagonistas identificables | Guerra entre Estados |
| Incursión / amenaza existencial | Ataque externo, peligro masivo, defensa reactiva | Tratado o diplomacia convencional (p. ej. Borg) |
| Ocupación | Control efectivo impuesto y resistencia posible | Soberanía legítima o reconocimiento |
| Insurgencia | Grupo armado no estatal con objetivos y apoyos | Estado soberano o ciudadanía uniforme |
| Guerra civil | Facciones armadas internas y campaña de hostilidades | Simple disidencia o golpe fallido |
| Guerra interestatal | Estados beligerantes, autoridad y conflicto sostenido | Que todas sus especies apoyen la guerra |
| Guerra multilateral | Coaliciones cambiantes y operaciones relacionadas | Igualdad de fechas de ingreso entre aliados |
| Coerción / espionaje | Amenazas, infiltración, sabotaje, sanciones | Guerra automática ni pruebas públicas fiables |
| Alto el fuego | Restricción acotada de hostilidades | Armisticio, tratado de paz ni cierre de agravios |
| Armisticio | Suspensión organizada de combate | Solución de disputas estructurales |
| Paz / acuerdo | Mandato y términos explícitos | Olvido de pérdidas, libre tránsito universal |

## Reglas B-D01 a B-D08 propuestas para aprobación editorial

- **B-D01**: una misma guerra tiene un ID principal; las campañas, batallas y subconflictos se vinculan por referencia, no se suman como guerras independientes.
- **B-D02**: fecha D propuesta 2383, mes/día sin fijar; un evento del mismo año no entra al pasado garantizado sin orden temporal probado.
- **B-D03**: un hecho anterior a D puede inicializar contexto; nunca se ejecuta por calendario después de D.
- **B-D04**: guerra emergente requiere causas verificadas, capacidad, autoridad, objetivos y consecuencias compatibles con WorldState.
- **B-D05**: solución diplomática válida, y en muchos casos preferente; la existencia de tensión no fuerza evolución.
- **B-D06**: facción/política institucional no asigna agresividad genética o unanimidad a una especie.
- **B-D07**: consecuencias persistentes; pérdidas, desplazamientos y acuerdos no se resetean tras la paz.
- **B-D08**: distinguir SCREEN_CANON, OFFICIAL_REFERENCE, INFERRED y GAME_ADDITION. Ninguna interpretación se promociona a canon silenciosamente.

## Exigencias de evidencia

Diferenciar **fuente narrativa** (episodio/película), **registro documental de fuente**, **inferencia** y **gancho de juego**. Registrar grado de precisión; no inventar fuerzas, cifras, colonias, comandantes, frentes o tratados.

La documentación no supone reconocimiento de todas las afirmaciones episodio por episodio. Antes de importar como dataset de ejecución se revisarán los pasajes dudosos contra material audiovisual. Se seguirá `mundo/sources/canon_policy.md`.

## Autoridad

Contratos de historial en `mundo/lore/conflicts/` = contexto. Contratos `sistemas/gameplay/conflict/` = referencia estratégica ya existente. Eventos y cambios reales = CoreRPG solamente; IA propone/narra, UE5 visualiza.