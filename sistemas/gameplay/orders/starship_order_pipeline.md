# Flujo de órdenes a bordo

## Principio

Una frase del jugador **no modifica directamente el World State**.

Flujo:

```text
Jugador habla / escribe
        ↓
interpretación de intención
        ↓
orden estructurada
        ↓
validación de autoridad + capacidades + estado
        ↓
aceptación / duda / rechazo
        ↓
ejecución por estación/personaje
        ↓
cambio autoritativo de estado
        ↓
feedback visual + sonoro + diálogo
```

## Ejemplo: «Levanten escudos»

Interpretación:

```text
action = set_shields
target = own_ship
mode = raise
```

Validación:
- ¿el actor tiene autoridad?
- ¿la nave posee escudos?
- ¿el sistema está operativo?
- ¿hay energía?
- ¿existe alguna restricción de estado?

Ejecución:
- Táctica/Operaciones actúa;
- el sistema pasa a energizarse;
- consume potencia;
- cuando se completa, cambia el estado.

Feedback:
- HUD;
- escena de puente;
- sonido;
- confirmación del oficial.

## Ejemplo: «Alerta roja»

No es solo una línea de diálogo.

Puede producir:
- alert state → red;
- personal a puestos de combate;
- cambio de iluminación/sonido;
- priorización de sistemas;
- cierre/aseguramiento de áreas según clase;
- NPCs reaccionando.

## Ejemplo: «Potencia auxiliar a escudos»

Es una redistribución de energía.

El sistema debe indicar de dónde sale la energía si esa decisión afecta otros subsistemas.

## Tiempo

Las órdenes pueden ser:
- instantáneas;
- rápidas;
- temporizadas;
- trabajos prolongados.

Reparar un sistema no ocurre al terminar la frase.

## Ambigüedad

Si una orden carece de datos necesarios, el oficial puede:
- pedir aclaración;
- inferir un valor seguro si su doctrina/rol lo permite;
- rechazarla si no puede ejecutarse de forma responsable.

## Desobediencia

Una orden válida puede ser:
- ejecutada;
- cuestionada;
- rechazada por imposibilidad;
- rechazada por autoridad/regulación;
- desobedecida por un NPC en circunstancias narrativamente válidas.

Eso debe quedar en el estado/historial cuando tenga consecuencias.
