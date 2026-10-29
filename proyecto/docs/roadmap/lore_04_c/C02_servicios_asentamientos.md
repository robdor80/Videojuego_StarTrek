# LORE-04C02 — Servicios civiles, ciudades, estaciones y asentamientos

**Estado:** CANDIDATO DOCUMENTAL SIN MERGE NI RUNTIME. **Época:** TNG/DS9/Voyager, continuidad no impuesta posterior al corte de campaña.

## 1. Cadena servicio-capacidad

Un asentamiento contiene servicio solo si lo permite la base de recursos, población, tecnología y función, con localización, operador, personal/agenda, infraestructura física y prioridad de uso. Reutilizar `facility_service_node_model.json`, `facility_service_queue.json`, `facility_service_berth_throughput_generation_contract_v0.1.json` y `settlement_infrastructure_contract.json`. Los servicios pueden estar suspendidos por daños o falta de suministros.

## 2. Espacios diferenciados

Ciudad, puesto científico, estación diplomática, colonia minera, asentamiento agrario, espacio de tránsito, puerto orbital, astillero, almacén, centro educativo, clínica y zona residencial son **roles**, no etiquetas que conceden funciones automáticamente. Una zona puede tener servicios mixtos o delegados a operadores, y una colonia joven puede carecer de ellos sin ser un error gráfico.

## 3. Capacidad en tiempos de crisis

Aforo máximo, muelles compatibles, personal, energía, repuestos, ventilación, evacuación y rutas de emergencia son restricciones. Priorizar un paciente o nave cambia el orden si hay reglas de prioridad, no multiplica camas, profesionales, muelles ni cargadores. La carga de una estación no es un stock infinito de la Federación.

## 4. Escenarios

INF-01: puesto médico sin cama libre → espera/derivación, no cama nueva. INF-02: puesto de comunicaciones sin antena/suministro → no establece enlace a kilómetros de distancia. INF-03: nave mercante solicita atraque → requiere tamaño compatible, muelle y política local; no aparece una dársena adicional.

**Propiedad de datos:** solo CoreRPG altera WorldState y produce eventos duraderos. Información de fuentes: `mundo/sources/canon_policy.md`; distinción SCREEN_CANON / OFFICIAL_REFERENCE / INFERRED / GAME_ADDITION. `UNKNOWN` para hechos o leyes no acreditados.
