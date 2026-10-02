# Contrato IA — interpretación de órdenes de nave

## La IA puede

- interpretar lenguaje natural;
- extraer intención;
- identificar destinatario probable;
- convertir una orden a estructura;
- pedir aclaración;
- generar confirmación/diálogo;
- explicar por qué una orden no puede ejecutarse si el personaje lo sabe.

## La IA no puede

- elevar escudos por sí misma;
- quitar energía de un sistema;
- causar daño;
- disparar un arma;
- cambiar rumbo;
- declarar una reparación terminada;
- inventar permisos;
- saltarse la cadena de mando;
- inventar información de sensores.

## Ejemplos

```text
«Rumbo 173 marca 4, warp 6»
→ navigate(course=173/4, speed=warp_6)

«Fuego a discreción»
→ tactical_fire(mode=weapons_free, target=current_hostile_set)

«Saquen toda la potencia que puedan y denla a los escudos»
→ transfer_power(destination=shields, amount=max_safe_available)
```

El resultado final depende siempre de las reglas y del estado real.
