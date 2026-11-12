# Naves individuales

> **DEC-0020 (13/11/2026):** la nave principal es la **USS Enterprise NCC-1701-D**, `class_id=galaxy`; [Proyecto Valhalla](../../../proyecto/docs/decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md) designa la reconstrucción/modernización por Geordi La Forge, no una clase ni una nueva matrícula. [Datos de identidad documental](project_valhalla_enterprise_d_v0.1.json).

## Identidad

Una nave individual referencia una clase, pero mantiene su propia identidad.

Campos típicos:

```text
ship_id
name
registry
class_id
operator
commissioned
decommissioned
status
assignment
mission
commanding_officer
crew
current_location
refit_state
system_state
damage_state
service_history
```

## Naves canónicas

Se cargan con hechos válidos hasta la fecha de inicio de campaña.

Después, el save puede divergir.

## Naves generadas

Una nave generada se marca como `GAME_ADDITION`, pero una vez creada es una entidad real de esa campaña.

Puede:
- recibir órdenes;
- cambiar de capitán;
- sufrir daños;
- ser transferida;
- desaparecer;
- ser destruida;
- ser reparada;
- recibir un refit.

## Naves famosas

No reciben inmunidad narrativa.

Tampoco son asignadas al jugador por ser "el protagonista".

Deben obedecer:
- disponibilidad temporal;
- situación;
- vacantes;
- cadena de mando;
- estado de campaña.
