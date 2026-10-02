# Sistemas de nave

## Objetivo

Los sistemas no se modelan como texto decorativo.

Son componentes que pueden:
- consumir energía;
- tener capacidad;
- sufrir daño;
- degradarse;
- fallar;
- ser reparados;
- ser aislados;
- recibir prioridad;
- afectar otros sistemas.

## Familias iniciales

### Propulsión
- motor warp;
- impulso;
- maniobra/control de reacción cuando proceda.

### Energía
- fuente principal;
- sistemas auxiliares;
- reservas/emergencia;
- distribución de energía.

### Defensa y táctica
- escudos;
- phasers/armamento energético;
- torpedos/armamento de proyectiles;
- control táctico.

### Sensores y navegación
- sensores;
- navegación;
- deflector;
- sondas.

### Comunicaciones y computación
- comunicaciones;
- ordenadores;
- bases de datos;
- interfaces.

### Transporte y soporte
- transportadores;
- tractores;
- hangares/naves auxiliares;
- soporte vital.

### Estructura
- casco;
- integridad estructural cuando corresponda;
- control de daños.

## Dependencias

Ejemplos:

```text
energía insuficiente
→ escudos reducidos

sensores dañados
→ adquisición táctica peor

soporte vital crítico
→ riesgo para tripulación

warp offline
→ no viaje warp
```

Las dependencias concretas pertenecen a reglas y a cada configuración de nave.
