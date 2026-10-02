# Base tecnológica por era

## Objetivo

Este bloque define qué tecnologías puede esperar el juego en cada periodo sin convertir datos generales en especificaciones de una clase concreta.

## Estados

- `standard` — tecnología normal y madura para unidades compatibles.
- `available` — disponible, pero no necesariamente instalada en todas las naves.
- `experimental` — existe de forma limitada; no debe aparecer como equipamiento común.
- `class_specific` — ligada a clases/configuraciones concretas.
- `not_standard` — no forma parte del equipamiento normal de Starfleet en ese periodo.
- `unavailable` — no debe generarse de forma ordinaria en esa fecha.

## Regla

La matriz de era es un **techo/guía de disponibilidad**.

La definición de clase decide qué instala realmente una nave.

Ejemplo:

```text
2371:
quantum_torpedo = available
Intrepid-class = quizá no los instala
Defiant-class = puede instalarlos
```

No confundir "tecnología disponible en Starfleet" con "todas las naves la tienen".
