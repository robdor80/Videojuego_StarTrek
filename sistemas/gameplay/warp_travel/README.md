# Viaje warp

Este directorio contiene las reglas runtime para convertir una orden de navegación en desplazamiento persistente del World State.

## Principio central

```text
FACTOR WARP != FÓRMULA UNIVERSAL DE DISTANCIA
```

Star Trek presenta escalas, prestaciones y tiempos de viaje que varían por época, nave, fuente y contexto. El juego no fuerza una única ecuación global para hacer encajar todo.

El Core separa:

```text
factor solicitado
+ perfil de escala warp de la era/configuración
+ capacidad de la nave
+ potencia disponible
+ daños
+ condiciones de subespacio
= velocidad efectiva del segmento
```

## Gameplay

Una ruta se ejecuta por segmentos. Esto permite:
- interrupciones;
- encuentros;
- averías;
- cambios de frontera;
- nuevos peligros;
- correcciones de rumbo;
- cambios de velocidad;
- órdenes de detenerse;
- desvíos.

La ETA se expresa normalmente como intervalo y se recalcula cuando cambian las condiciones.

## Autoridad

Core controla posición, tiempo transcurrido, consumo/estado y progreso.

La IA puede:
- interpretar la orden;
- explicar opciones;
- informar de ETA y riesgos conocidos;
- representar al oficial de navegación.

La IA no puede mover la nave directamente.
