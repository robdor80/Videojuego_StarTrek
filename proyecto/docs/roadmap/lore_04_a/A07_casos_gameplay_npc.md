# LORE-04A / A07 — Casos jugables, conocimiento NPC y consecuencias civiles

**Estado:** CANDIDATE_COMPLETE_DOCUMENTARY. **Origen:** anclas LA-E01..E14 y `lore04a_scenarios_v0.1.json`. **Advertencia:** casos `GAME_ADDITION` son **fixtures propuestos**, no sucesos de campaña aprobados ni encuentros obligatorios.

## A07.1 Contrato de comportamiento documental

Cada interacción civil exige: (1) existencia causal del actor/servicio/lugar, (2) autoridad y acceso, (3) agenda y estado físico, (4) conocimiento individual disponible, (5) propuesta permitida de acción y (6) resultado **solo** si CoreRPG lo valida y persiste. La respuesta de IA debe ser coherente con lo que el personaje ve/sabe y no puede crear un nuevo archivo de hechos.

**Separar:** `WorldTruth` (CoreRPG), `Knowledge` (observador), `Dialogue` (interpretación), `Consequences` (evento autorizado). También separar autorización de Flota, jurisdicción civil y soberanía territorial.

## A07.2 Catálogo de interacciones reproducibles

| Caso | Contexto, precondición | Resultado aceptable | Resultado prohibido | Evidencia |
|---|---|---|---|---|
| CIV-01 | docente trabaja en escuela existente, con alumnos | impartir clase, informar solo sobre currículo conocido o indicar indisponibilidad | enseñar sin centro o conocer expedientes secretos | LA-E03, LA-E13 |
| CIV-02 | familiar reside en otro planeta, hay canal de comunicación | conversación condicionada por acceso y horario | aparición instantánea en escena | LA-E01, LA-E04 |
| CIV-03 | civil ferengi atiende comercio autorizado con inventario | negociación con oferta y posterior transacción validada | venta sin bienes; deducir deshonestidad étnica | LA-E07, LA-E12 |
| CIV-04 | klingon de una Casa disputa propiedad con actores competentes | consulta/apertura de controversia | crear norma de sucesión universal a partir de un episodio | LA-E05 |
| CIV-05 | médico/clinica sin suministros por avería real | rechazo, derivación o espera con causa | generar recursos y resolver atención gratis por diálogo | LORE-02C, A03 |
| CIV-06 | propietario/granjero bajorano afectado por infraestructura | discrepancia y solicitud a autoridad existente | concluir derecho universal de expropiación | LA-E06 |
| CIV-07 | adulto cardassiano con trabajo civil en época posguerra | relato condicionado por biografía real | imputar crimen heredado por nacionalidad | LA-E09 |
| CIV-08 | dos ciudadanos participan en deporte | conexión social posible, no obligatoria | amistad automática por tiempo juntos | LA-E08 |
| CIV-09 | romulano civil no autorizado para material clasificado | reserva o ignorancia coherentes | asignarlo a Tal Shiar o filtración de secreto | LORE-01 |
| CIV-10 | líder religioso vs gobierno bajorano | competencias identificadas, incertidumbre donde no constan | convertir Vedek/Kai en gobierno secular por defecto | LA-E03 |
| CIV-11 | estación y autoridad de Flota ante seguridad | acudir al órgano competente si existe | almirante como juez municipal universal | LA-E10 |
| CIV-12 | persona Trill con recuerdos propios y familia | narración según historia y conocimiento | recuerdos de simbionte para no unido | LA-E11 |
| CIV-13 | centro recreativo inoperativo | cancelación y persistencia de condición | reabrir el edificio porque jugador necesita misión | LA-E08 |
| CIV-14 | poblaciones A/B/C, relación tras carga | IDs estables e historia conservada | reroll, población duplicada, memoria creada a posteriori | contratos de población |
| CIV-15 | evento tras corte inicial 2383 | se evalúa solo si sucede causalmente en campaña | forzar política/guerras/sucesos de series futuras | LORE-03D |
| CIV-16 | civil de cultura mixta en mundo miembro | resolver múltiples afiliaciones y vida real | nacionalidad y oficio deducidos de especie | LA-E14 |

Los mismos 16 casos se registran estructuradamente en `lore04a_scenarios_v0.1.json`, con expectativas observables y negaciones para tests de diseño. Los identificadores son **identificadores del fixture**, nunca entidades de mundo.

## A07.3 Respuesta de IA y observador

- Un NPC puede decir «no lo sé» y guardar ambigüedad. Un rumor no es declaración fidedigna del WorldState.
- Si un jugador pregunta por una persona ausente, responder con información conocida y canales disponibles; no crear teletransporte.
- El modelo puede expresar diferencias culturales respaldadas por `culture_refs`, pero no asignarlas por especie.
- Solo los eventos autorizados pueden modificar la agenda, la reputación, el domicilio, el inventario, las relaciones o los derechos.
- Un civil no puede conocer un expediente médico por confianza personal sin base legal/consentimiento.
- Aunque el juego pueda generar un deseo de NPC, el deseo **no** genera empleos, casas, riquezas, escuelas, misiones o hechos pasados.
- Respetar separaciones de relaciones: amistad ≠ confianza ≠ obediencia ≠ parentesco; romance y consentimiento se rigen por el canon de relaciones ya aprobado, sin cambios aquí.

## A07.4 Pruebas de negación y criterio de integración

Cada escenario requiere comprobar tanto una acción **permitida bajo condiciones** como una variante que se **rechaza** por ausencia de causa, autoridad, recurso o conocimiento. Los casos con leyes ambiguas no dan un resultado legal inventado: retornan `UNKNOWN` o requieren datos autoritativos y una decisión de diseño.

La validación documental del fixture solo demuestra que las especificaciones tienen campos, referencias y guardarraíles correctos. Una prueba runtime futura deberá fabricar WorldState, ejecutar CoreRPG, guardar, cargar y comprobar que las acciones cambian la realidad solo por eventos válidos. Esta PR no certifica nada de eso.
