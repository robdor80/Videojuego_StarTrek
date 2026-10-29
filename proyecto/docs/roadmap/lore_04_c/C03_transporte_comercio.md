# LORE-04C03 — Corredores comerciales, cargueros y transporte de pasajeros

**Estado:** CANDIDATO DOCUMENTAL SIN MERGE NI RUNTIME. **Época:** TNG/DS9/Voyager, continuidad no impuesta posterior al corte de campaña.

## 1. Rutas existentes

`sistemas/universe/generation/traffic_activity_model.json` define origen, destino, propósito, ventana temporal, ruta, actor, contrato y estado de actividad. `sistemas/gameplay/navigation/route_context_model.json`, `route_cost_model.json`, `facility_local_traffic_routing.json`, `sistemas/universe/generation/civilian_commercial_vessel_grammar_v0.1.json` y `population_movement_contract.json` aportan el detalle. El tráfico nace de necesidades, no de un spawn cosmético al observar el espacio.

## 2. Pasaje y comercio

Civiles, científicos, emigrantes, desplazados, turistas, trabajadores y pacientes pueden ser pasajeros cuando la historia, los servicios y la capacidad del operador lo permitan; no se presupone turismo en todos los mundos. Los cargueros pueden satisfacer demanda de abastecimiento y contratos, pero un viaje no garantiza acceso, pago ni éxito. La nave precisa identidad y operador, tripulación real, combustible/sistemas y origen/destino enlazados a ruta.

## 3. Jurisdicción y temporalidad

Fronteras, zonas de exclusión, tratados, cuarentenas y amenaza bélica pueden bloquear o desviar tráfico; la geometría de una ruta no da permiso político. La interrupción modifica el estado solo con un evento y registra efecto en pasajeros, recursos y entrega. No reescribir los itinerarios anteriores al evento, y no suponer que una ventana TNG/DS9/VOY fija las rutas de 2383.

## 4. Ejemplos

INF-04: carguero con necesidades agrícolas va de colonia a estación; su llegada no ocurre antes del tiempo de viaje ni con inventario duplicado. INF-05: pasajero cancelado por bloqueo se queda en origen y mantiene estatus; no aparece simultáneamente en destino. INF-06: itinerario de asistencia sanitaria puede priorizar una nave si existe autorización, nunca crearla de la nada.

**Propiedad de datos:** solo CoreRPG altera WorldState y produce eventos duraderos. Información de fuentes: `mundo/sources/canon_policy.md`; distinción SCREEN_CANON / OFFICIAL_REFERENCE / INFERRED / GAME_ADDITION. `UNKNOWN` para hechos o leyes no acreditados.
