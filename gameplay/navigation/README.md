# Navegación y control de vuelo

## Bucle jugable

```text
OBJETIVO / DESTINO
      ↓
interpretar orden
      ↓
resolver destino + conocimiento disponible
      ↓
generar rutas candidatas
      ↓
validar nave / velocidad / fronteras / peligros conocidos
      ↓
seleccionar solución
      ↓
ejecutar movimiento
      ↓
seguir posición / ETA / sensores / eventos
      ↓
corregir o completar
```

## Acciones

- fijar rumbo;
- maniobrar;
- velocidad de impulso;
- entrar/salir de warp;
- seleccionar factor warp;
- interceptar;
- mantener formación;
- órbita;
- aproximación;
- atraque;
- evasión;
- navegación de lanzaderas.

## Ruta real, no teletransporte de mapa

Una orden como «Rumbo a Vulcano, warp 6» no cambia la localización de la nave de inmediato.

Genera:
1. una orden estructurada;
2. una solución de navegación;
3. una ruta;
4. una ETA con incertidumbre;
5. progreso persistente por segmentos;
6. posibles eventos durante el trayecto.

## Validación

Una orden de movimiento comprueba:
- propulsión;
- energía;
- navegación;
- sensores mínimos;
- daños;
- límites de clase/configuración;
- peligros conocidos;
- fronteras y permisos conocidos;
- autoridad de mando.

## Velocidad warp

La capacidad máxima pertenece a la clase/configuración y estado de la nave.

No hay un `warp_max` universal para toda Starfleet ni una ecuación única aplicable a todas las eras.

## Jugabilidad

El jugador no introduce ecuaciones orbitales reales.

El personaje prepara la solución según su competencia; el jugador decide:
- ruta;
- riesgo;
- velocidad;
- maniobra;
- prioridad;
- si respeta o viola una restricción conocida.

## Información limitada

Un piloto no puede evitar un peligro que:
- no fue detectado;
- no fue comunicado;
- no figura en sus cartas;
- queda fuera de sus sensores/conocimiento.

El sistema nunca entrega automáticamente la verdad oculta del World State.
