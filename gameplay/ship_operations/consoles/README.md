# Consolas funcionales de nave

## Catálogo maestro v0.1

Este directorio fija las familias funcionales de consola del juego.

Reglas base:

- una consola funcional no equivale necesariamente a una estación física;
- cada clase/configuración de nave decide desde qué estaciones físicas se exponen estas funciones;
- Academia y naves operativas comparten el mismo modelo funcional, aunque la UX cambie;
- la presentación visual y LCARS pertenece a `ui/`, no a este directorio;
- no se crea una nueva familia si la función encaja de forma coherente en una de las existentes.

Familias fijadas:

1. `command` — Mando
2. `conn` — Control de vuelo
3. `navigation` — Navegación / Astrometría
4. `operations` — Operaciones
5. `sensors` — Sensores
6. `science` — Ciencia
7. `tactical` — Táctica
8. `security` — Seguridad
9. `engineering` — Ingeniería
10. `communications` — Comunicaciones
11. `mission_ops` — Operaciones de misión
12. `transporter` — Transportador
13. `medical` — Médica
14. `environmental` — Soporte vital / Ambiental
15. `flight_deck` — Hangar / Lanzaderas
16. `computer` — Ordenador / Base de datos

Estado: catálogo fijado para diseño incremental. Los árboles de menús y operaciones se definirán consola por consola.
