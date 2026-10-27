# Turnos y guardias

## Concepto

Una nave o estación funciona de forma continua mediante turnos/guardias.

El jugador puede:
- tener un turno asignado,
- ocupar un puesto de servicio durante ese turno,
- ser Oficial de Guardia,
- cambiar temporalmente de turno,
- cubrir ausencias,
- realizar guardias extraordinarias.

## Evidencia por era

### Pike / Strange New Worlds

La era de Pike usa terminología de turno diurno/nocturno en pantalla.

El proyecto **no fija todavía una duración universal** para esos turnos si el canon no la establece de forma suficiente para una unidad concreta.

### Kirk / TOS + películas

En la etapa tardía del siglo XXIII aparecen rotaciones de tres turnos y nombres Alpha/Beta/Gamma.

### TNG + DS9 + Voyager

Tres turnos son comunes, pero no obligatorios.

Ejemplos canónicos:
- Enterprise-D operaba normalmente con tres turnos.
- Jellico ordenó temporalmente una rotación de cuatro.
- DS9 pasó de tres a cuatro turnos.
- Voyager muestra oficiales jóvenes mandando la guardia nocturna.

## Regla del proyecto

El número de turnos pertenece al **estado de la unidad**, no a la definición universal de Starfleet.

```text
unit.shift_pattern = 3_shift | 4_shift | custom
```

Esto permite:
- decisiones del capitán,
- fatiga,
- emergencias,
- guerra,
- falta de personal,
- cambios de organización.

## Oficial de Guardia

Cada guardia puede tener un oficial responsable del puente/centro de operaciones.

Ser Oficial de Guardia:
- otorga autoridad operativa durante ese turno,
- no cambia el rango,
- requiere cualificación adecuada,
- forma parte de la progresión profesional.

## Diseño de carrera

Las guardias serán una vía natural para que el jugador practique mando antes de alcanzar puestos superiores.
