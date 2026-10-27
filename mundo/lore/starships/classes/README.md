# Clases de nave

## Qué es una clase

Una clase es una definición de diseño compartida por varias naves.

## Datos de autoría

Cada definición podrá incluir:

- `class_id`
- nombre visible;
- facción/operador;
- año de introducción;
- periodo de servicio conocido;
- clasificaciones/roles;
- dimensiones;
- cubiertas;
- dotación típica;
- velocidad/capacidad warp;
- propulsión de impulso;
- generación de energía;
- sensores;
- comunicaciones;
- escudos;
- armamento;
- transportadores;
- hangares/naves auxiliares;
- instalaciones científicas;
- instalaciones médicas;
- capacidades especiales;
- variantes;
- refits;
- procedencia/confianza.

## No meter estado vivo aquí

Incorrecto:

```text
Galaxy-class:
  shields = 42%
  captain = Jean-Luc Picard
```

Correcto:

```text
Galaxy-class:
  shield_system = defined capability

USS Enterprise-D:
  class_id = galaxy
  shield_state = 42%
  commanding_officer = ...
```

## Fechas

Una clase debe tener disponibilidad temporal suficiente para impedir:
- Galaxy en la era Kirk;
- Intrepid antes de su introducción;
- refits antes de existir.

Las fechas pueden ser exactas o aproximadas según evidencia.
