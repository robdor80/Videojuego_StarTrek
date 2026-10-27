# Dotación y tripulación

## Separación

La clase puede indicar una **dotación de referencia**.

La nave individual posee la tripulación real.

## Manifest

Una tripulación real incluye:
- personaje;
- rango;
- división/departamento;
- puesto;
- turno;
- puesto de servicio;
- estado de servicio;
- localización actual.

## Turnos

El mismo puesto funcional puede estar cubierto por personas distintas según guardia.

Ejemplo:

```text
Táctica — turno Alpha → Teniente A
Táctica — turno Beta → Alférez B
Táctica — turno Gamma → Teniente C
```

## Vacantes

Una vacante es estado real del mundo y puede afectar:
- primer destino del jugador;
- traslados;
- carga de trabajo;
- ascensos;
- necesidad de sustituciones;
- seguridad de la nave.

## Civiles/familias

No se presupone que todas las naves transporten civiles.

Cuando una clase/época/misión lo permita, se modelan como manifest separado de la dotación de Starfleet.
