# LORE-04C05 — Persistencia, LOD espacial y coherencia fuera de pantalla

**Estado:** CANDIDATO DOCUMENTAL SIN MERGE NI RUNTIME. **Época:** TNG/DS9/Voyager, continuidad no impuesta posterior al corte de campaña.

## 1. Existencia física e identidad

Las instalaciones que reciben identidad propia persisten fuera del campo de visión; LOD cambia detalle gráfico y frecuencia de cálculo, no sus existencias, cargas, trabajadores ni posición material. Reutilizar `sistemas/universe/generation/ship_facility_offscreen_simulation_contract.json`, `sistemas/gameplay/facilities/facility_traffic_state.json`, `sistemas/universe/generation/persistent_population_materialization_rules.json`. Una estación destruida no reaparece al volver el jugador si no hubo reconstrucción histórica.

## 2. Relación con A y B

Los habitantes (04A) mantienen agenda y domicilio; las mercancías y recursos (04B) requieren proveedores y causa de transmisión. El nivel de detalle no borra pasajeros, contratistas, inventario ni acuerdos ya persistidos. La observación de un mapa o consola no crea una ruta, sino que muestra una vista autorizada de la realidad existente.

## 3. Escenarios de carga

INF-10: el jugador viaja mientras existe un convoy lejano; al regresar, su estado ha evolucionado solo por reglas deterministas y eventos posibles, sin spawn por proximidad. INF-11: población de estación no aumenta al hacer materialización de visitante. INF-12: incidente logístico no divulgado no es conocido por todos los NPC ni altera rumores sin canal.

## 4. Límite de runtime

Estas son especificaciones para el contenido y la validación del videojuego, **no** un planificador de economía o transporte ejecutable. CoreRPG controla reloj, eventos, persistencia y mutaciones. Los visuales NAP/UE5 consumen topología y niveles de detalle, no crean nuevas instalaciones por escena.

**Propiedad de datos:** solo CoreRPG altera WorldState y produce eventos duraderos. Información de fuentes: `mundo/sources/canon_policy.md`; distinción SCREEN_CANON / OFFICIAL_REFERENCE / INFERRED / GAME_ADDITION. `UNKNOWN` para hechos o leyes no acreditados.
