# Fixtures — Planificación 2, Bloque 4

Casos sintéticos de **referencia**; no hechos canon ni partidas CoreRPG.

- `living_economy_frontier_supply_v0.1.json`: producción, despacho real, tránsito con tres ticks y entrega, sin mercancía duplicada.
- `living_economy_replication_crisis_v0.1.json`: clínica con energía cortada, rechazo de réplica; no ofrece suministros mágicos.

Pruebas: `python -m unittest desarrollo/tools/generation/test_simulate_living_economy.py -v` desde raíz. El fixture usa balances en `latinum_strip` como unidad **local explícita de prueba**; no convierte slip/strip/bar/brick ni impone moneda a la Federación.
