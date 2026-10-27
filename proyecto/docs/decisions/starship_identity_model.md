# Modelo de identidad de naves estelares

Status: **APPROVED GAME DESIGN**

## Regla fundamental

El juego separa tres conceptos:

```text
CLASIFICACIÓN / ROL
        ≠
CLASE DE NAVE
        ≠
NAVE INDIVIDUAL
```

Ejemplo:

```text
Clasificación: Explorador
Clase: Galaxy
Nave: USS Enterprise NCC-1701-D
```

## Clasificación

Describe de forma general la función, tamaño o rol de una nave.

Ejemplos:
- exploración;
- ciencia;
- escolta;
- transporte;
- apoyo;
- médico.

No define por sí sola la construcción exacta de la nave.

## Clase

Una clase es un diseño compartido por varias naves.

La definición de clase contiene capacidades y límites de diseño:
- época;
- dimensiones cuando estén establecidas;
- sistemas;
- prestaciones;
- dotación típica;
- variantes/refits;
- roles habituales.

La clase **no** contiene daños, tripulación actual ni historia de campaña de una nave concreta.

## Nave individual

Una nave individual es una entidad histórica y/o viva del mundo.

Contiene:
- nombre;
- matrícula;
- clase;
- estado de servicio;
- localización;
- misión/destino;
- Oficial al mando;
- tripulación;
- daños;
- nivel de combustible/consumibles cuando proceda;
- sistemas actuales;
- modificaciones;
- historial;
- consecuencias de campaña.

## Canon y campaña

Una nave canónica se inicializa con su historia válida hasta la fecha de comienzo.

Desde ese momento, su estado vivo pertenece a la campaña.

Ejemplo:

```text
USS Enterprise-D
canon válido hasta fecha D
        ↓
inicio de campaña
        ↓
daño / reparación / cambio de capitán / destrucción / supervivencia
según la partida
```

El juego no fuerza su futuro televisivo.

## Naves generadas

El juego puede crear naves individuales nuevas como `GAME_ADDITION`.

Una nave generada debe:
- usar una clase válida para la fecha;
- respetar tecnología y capacidades de clase;
- recibir una identidad/matrícula no conflictiva;
- generar dotación y mando compatibles;
- entrar en el World State como cualquier otra nave.

## Matrículas

La matrícula es un identificador, no un reloj.

El juego **no inferirá automáticamente una fecha exacta a partir del número NCC**.

Las matrículas conocidas se conservan tal cual. Para naves generadas, el sistema de generación deberá evitar colisiones y seguir convenciones de la época sin asumir una secuencia histórica perfecta.
