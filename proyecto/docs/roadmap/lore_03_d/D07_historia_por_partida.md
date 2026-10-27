# D07 — Historia propia de cada campaña, guardados y reconstrucción

## 1. Separación lógica (responsabilidad CoreRPG)
La partida posee identificador exclusivo `campaign_id`, un `start_cutoff` verificable y una referencia/versión del prefijo histórico **congelado**. El registro de acontecimientos de campaña es append-only y ordenado según tiempo efectivo/causalidad; `event_id` no colisiona entre campañas. Un registro de estado guarda identidades, relaciones y referencias de consecuencia, memoria, conocimiento y servicio. **Esto es una política de interoperabilidad, no un esquema alternativo de guardado**: CoreRPG decide la representación concreta.

## 2. Invariantes de persistencia
1. Guardar/cargar el mismo punto no añade sucesos ni provoca segundo impacto (idempotencia por evento).
2. A igualdad de versión, prefijo de historia, estado e inputs, recuperación y catch-up dan la misma historia aceptada, sin necesidad de reproducir cada animación.
3. Un `campaign_id` no puede leer/escribir memorias, muertes, daños, tecnología o tratados de otro.
4. Un cambio de nave del jugador altera punto de vista y asignación, **no** borra acontecimientos externos.
5. LOD A/B/C y `dormant_catch_up` preservan prefijo histórico, identidades, asignaciones y eventos mayores; no se generan historias heroicas para justificar un presente nuevo.
6. Migraciones de reglas/versiones son explícitas, auditables y reversibles/fallidas de modo seguro; no sobrescribir silenciosamente.
7. Presentación, recaps y diálogo se reconstruyen desde eventos y proyecciones de conocimiento permitidas, nunca desde futuro de TV ni de un save ajeno.
8. Una corrección administrativa posterior se registra como rectificación con causalidad/procedencia, sin reescritura oculta del hecho registrado.

## 3. Capas conceptuales, no clases nuevas
- `Historical reference`: canon/contexto previo, compartido como **datos inmutables de lectura**.
- `Authoritative campaign ledger`: solo CoreRPG; eventos aceptados de esa partida y deltas.
- `Actor knowledge / memory`: persistente por actor, filtrado por acceso y cronología.
- `Derived recap / UI / IA`: vistas descartables basadas en las tres capas; narración sin autoridad.

Un rumor corregido se recuerda, cuando procede, como rumor y corrección; no se elimina la afirmación del pasado ni se cambia la verdad. Fechas de comunicación distintas impiden memoria precoz.

## 4. Ejemplo de bifurcación documental
`S1`: alertas científicas justificadas y decisiones posteriores evitan un daño en 2387. `S2`: esos mismos recursos no se destinan a investigación y ocurre otro desenlace conforme a causas comprobadas. `S3`: no se produce el candidato de crisis. Los tres comparten la historia hasta `D`, pero ninguno recibe automáticamente un evento de "destrucción de Rómulo 2387". Tras reabrir cada save, NPC, noticias y mapas muestran **solo** resultados autorizados en su historia.

## 5. Contrato de rechazo y restauración
Ante save corrupto, referencias cruzadas rotas, salto temporal negativo, evento duplicado, versión no migrable o procedencia desconocida, **fallar de forma segura**, no rellenar con IA ni regenerar identidades. Toda recuperación deja traza para auditoría y no modifica el pasado de otras campañas.
