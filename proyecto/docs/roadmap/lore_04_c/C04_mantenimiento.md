# LORE-04C04 — Mantenimiento, suministros, industria y fallos

**Estado:** CANDIDATO DOCUMENTAL SIN MERGE NI RUNTIME. **Época:** TNG/DS9/Voyager, continuidad no impuesta posterior al corte de campaña.

## 1. Contratos propietarios

`sistemas/gameplay/logistics/maintenance_state_model.json`, `resupply_job_model.json`, `resource_inventory_state.json`, `facility_transfer_job.json`, `support_request_model.json`, `sistemas/gameplay/facilities/facility_operational_state.json` y `facility_support_effects.json`. La tecnología y disponibilidad en LORE-02 condiciona equipos, no aporta los recursos faltantes por sí misma.

## 2. Causalidad de reparación

Avería→diagnóstico válido→pieza/habilidad/equipo→solicitud y traslado→acceso→trabajo→validación de reparación por CoreRPG→cambio de capacidad. La aceptación de una misión de reparación no arregla instalaciones. El material entrante sale del inventario del origen y solo llega al destino tras traslado; el mismo recurso no puede estar en dos lugares.

## 3. Economía y servicios

La demanda de suministros puede causar comercio, prioridades o ayuda comunitaria; la naturaleza del pago depende de LORE-04B, no de este paquete. Una colonización genera carga y tráfico si existían necesidad, acuerdos y ruta. Una estación no puede ofrecer refit, astilleros ni reparación pesada sin muelles, técnicos y tecnología ya justificados.

## 4. Casos

INF-07: pieza averiada sin repuesto disponible: reparación fallida o aplazada, sin inventario ficticio. INF-08: convoy interrumpido causa falta de suministros después del evento; no se retropropaga ficticiamente al pasado. INF-09: petición de ayuda médica se registra sin garantizar hospital, personal ni transportador.

**Propiedad de datos:** solo CoreRPG altera WorldState y produce eventos duraderos. Información de fuentes: `mundo/sources/canon_policy.md`; distinción SCREEN_CANON / OFFICIAL_REFERENCE / INFERRED / GAME_ADDITION. `UNKNOWN` para hechos o leyes no acreditados.
