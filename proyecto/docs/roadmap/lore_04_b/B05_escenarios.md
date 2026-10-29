# LORE-04B05 — Escenarios económicos, diplomacia, comercio y consecuencias

**Estado:** DOCUMENTACIÓN CANDIDATA — pendiente de revisión y fusión expresa; no implementación. **Fecha:** 2026-10-29.

## 1. Cadena causal mínima

(1) necesidad y demanda verificables → (2) oferta real y operador → (3) inventario/infraestructura/ruta → (4) jurisdicción/autorización/política → (5) contrato o acuerdo → (6) propuesta de acción → (7) resolución de CoreRPG → (8) persistencia y conocimiento restringido. Ningún paso autoriza a saltar los anteriores por interés dramático.

## 2. Casos positivos

**ECO-01:** colonia solicita repuestos porque falló instalación: proveedor con stock y ruta accesible; entrega válida produce evento. **ECO-02:** transportista opera una ruta con pasajeros y energía disponible, origen y destino persistentes. **ECO-03:** intercambio ferengi con denominación compatible, sin tarifa universal. **ECO-04:** científico terrestre entrega trabajo sin salario fijado: servicio legítimo posible.

## 3. Casos negativos

**ECO-05:** vendedor no tiene inventario → rechazo. **ECO-06:** replicador sin energía → rechazo. **ECO-07:** bloqueo de frontera → no entrega remota sin tránsito autorizado. **ECO-08:** rumor de escasez → no modifica stock real. **ECO-09:** oficial de Flota proclama arancel local sin competencia → invalidez. **ECO-10:** política futura post-2383 se ejecuta porque un guion externo así lo dice → rechazo.

## 4. Conocimiento NPC

La percepción de un vendedor sobre precios no es un precio global; reputación individual, espionaje, documentos y secretos comerciales requieren canales de conocimiento. Los diálogos nunca alteran oferta, stock o riesgo sin un evento. El silencio del actor no prueba inexistencia del bien.

## 5. Dependencia

Estos escenarios son **fixtures de diseño**, no triggers de economía viva. La economía procedural de Bloque 4 aún deberá implementar la causalidad interplanetaria en su propia fase y CoreRPG resolver ejecución; LORE-04B no cambia su estado `READY_TO_RESUME`.

---
**Referencias transversales:** `proyecto/docs/roadmap/lore_04_master_plan_v0.1.md`, `mundo/sources/canon_policy.md`, `mundo/sources/provenance_policy.md`, `desarrollo/validation/consistency/movement_logistics_economy_diplomacy_invariants_v0.1.json`. **Autoridad:** CoreRPG WorldState. **No se valida simulación runtime**.
