# LORE-04A / A04 — Ocio, comunidades, ritmos de vida y movilidad cotidiana

**Estado:** CANDIDATE_COMPLETE_DOCUMENTARY. **Evidencia:** LA-E01, E02, E04, E08, E11; `sistemas/gameplay/social/social_event_rules.json`, `social_knowledge_propagation.json`, `social_simulation_lod.json`; `sistemas/universe/generation/population_movement_contract.json`.

## A04.1 Comunidades y espacios

Espacios civiles **posibles, no universales**: hogares/espacios comunes, bibliotecas, áreas de reunión, comedores, establecimientos, instalaciones deportivas, lugares de culto, talleres, jardines, escuelas, espacios comerciales, centros sociales y zonas de tránsito. Deben responder a una necesidad y a operadores reales; no se materializan por la proximidad del jugador.

El espacio tiene `location_id`, `operator_ref`, `jurisdiction_ref`, `capacity`, `available_at`, accesibilidad y condición actual **solo cuando el sistema propietario dispone de esos datos**. Son campos de consulta orientativos, no schema nuevo. Prohibido introducir tarifas u horarios canónicos no documentados.

**Anclas:** en *Data's Day* (LA-E02) observamos matrimonio y actividades de preparación social; el partido de *Take Me Out to the Holosuite* (LA-E08) muestra deporte y cooperación; *Family* (LA-E01) presenta reunión doméstica y agricultura familiar. Ningún ejemplo establece un programa de ocio obligatorio, estándar de propiedad o presencia semanal.

## A04.2 Actividades y vínculo social

Reutilizar las familias `social_invitation`, `social_activity`, `promise`, `conflict`, `apology`, `mentoring_session` del contrato de eventos existente; no diseñar nuevas métricas de amistad. Una actividad compartida puede aumentar familiaridad sin crear amistad, y la respuesta de un participante no determina la de otro. La pertenencia a un club o institución no crea confianza automática. La IA puede interpretar y ofrecer propuestas que CoreRPG evalúe.

**Ejemplo CIV-A04-01:** jugadores y vecinos se encuentran en una liga deportiva realmente organizada. Si falta una persona porque trabaja, su plaza queda vacante o se sustituye conforme a reglas ya representadas. No forzar «jugador invitado especial» ni añadir logros sociales por tiempo transcurrido.

**Ejemplo CIV-A04-02:** taller de cerámica o de escritura en una colonia; la actividad solo existe cuando hay instalación, personal, demanda y recursos. Participar no otorga rango de Flota ni convierte automáticamente la amistad en relación íntima.

**Ejemplo CIV-A04-03:** convivencia en vivienda multiespecie. La lengua, creencias, hábitos o dieta dependen de individuos y culturas realmente adjuntas; nadie conoce conversaciones privadas por compartir edificio.

## A04.3 Calendario, fiestas, horarios y desplazamiento

No existen un «día laboral galáctico» ni una «semana de siete días» aplicables por defecto a todos los planetas. El reloj de campaña y las convenciones locales, que puede que sigan pendientes, condicionan la presentación. Las festividades requieren procedencia: evento canónico o adición autorizada; no se generan fiestas automáticamente según especie.

Política de comprobación:
1. Agenda individual y ocupación sin incompatibilidades temporales.
2. Desplazamiento físicamente posible con medio, tiempo y autorización.
3. Acceso al lugar dependiente de apertura, aforo, seguridad y restricciones locales.
4. Consecuencias de cancelación, trabajo urgente o crisis coherentes con WorldState.
5. Tradiciones individuales, familiares, de organización y del mundo pueden divergir.
6. Toda escena social observa el instante y conocimiento permitidos, no crea un estado fuera de cámara a posteriori.

Una persona que vive en una estación puede tener familia en otro planeta, mantener contacto a distancia y esperar un transporte real; ello **no** la teletransporta ni concede comunicación subespacial sin infraestructura. Contratos de transporte, comunicaciones y de población existentes tienen prioridad.

## A04.4 Casos negativos obligatorios

- Anfitrión «siempre disponible» porque un jugador quiere conversación, aunque su agenda esté ocupada.
- Evento deportivo en centro destruido/no construido.
- Vacaciones instantáneas sin viaje ni autorización.
- Cobro automático de entrada en todos los mundos federados.
- Suposición de que un vulcano nunca practica deporte, o que un klingon siempre debe asistir a un rito.
- Rumor íntimo compartido con toda una ciudad sin canal de difusión ni incertidumbre.
- Romance o compromiso social derivados automáticamente de asistencia a una actividad. Los vínculos románticos se rigen exclusivamente por el canon de relaciones vigente, no se modifica en LORE-04A.

## A04.5 Observabilidad y reutilización

Las vistas de NPC/IA deben consumir `social_knowledge_propagation.json` (observación directa, declaración, rumor, informe autorizado), `social_event_rules.json`, `social_simulation_lod.json`. El LOD cambia profundidad, no existencia ni causalidad. El diseñador de eventos podrá consultar esta ficha para ofrecer ocio plausible, pero **no** para instanciar eventos runtime desde el diálogo. Estado de A04: trabajo documental concluido y sujeto a pruebas A08.
