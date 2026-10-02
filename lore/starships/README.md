# Naves estelares — modelo del juego

Este árbol documenta definiciones de diseño y datos históricos que alimentan el sistema jugable de naves.

## Separación

- `classifications/` — roles/categorías funcionales;
- `classes/` — diseños de nave;
- `individual_ships/` — naves concretas;
- `ship_systems/` — sistemas reutilizables;
- `interiors/` — espacios/localizaciones;
- `bridge_stations/` — puestos operativos;
- `crew_complements/` — dotaciones;
- `refits/` — cambios de configuración;
- `service_history/` — hechos históricos;
- `operational_doctrine/` — uso operativo.

## Regla runtime

El lore define la nave.

El World State define **cómo está ahora**.

Una clase puede existir en datos sin que ninguna nave concreta de esa clase esté actualmente disponible en una campaña.

Una nave puede estar:
- activa;
- en reparación;
- en reserva;
- desaparecida;
- destruida;
- retirada.

Ese estado pertenece a la entidad individual.
