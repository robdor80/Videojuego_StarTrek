# Sensores · Implementación de referencia en Holocubierta

Estado: **REFERENCE IMPLEMENTATION v1.0**

La especificación autoritativa de Sensores permanece en este repositorio:

- `sensor_menu_tree.json`
- `sensor_context_actions.json`
- `sensor_console_interaction_model.json`
- reglas de configuración, interferencias y contratos interconsola asociados.

La implementación operativa de entrenamiento se mantiene en:

- repositorio: `robdor80/academiaflota`
- ruta: `holodeck/sensors/`
- referencia validada: commit `3d1d1c263f09cb08d870bb30f4f7cd5f1cceb17b`

## Propósito

La Holocubierta funciona como banco de pruebas de la consola antes de disponer del universo jugable completo. Implementa el mismo modelo conceptual:

```text
Consola de Sensores
→ operación estructurada
→ motor de Sensores
→ estado del mundo
→ resultado observado
```

En la Holocubierta, el estado del mundo procede de escenarios de entrenamiento JSON. En el juego, deberá proceder del universo autoritativo de CoreRPG.

## Regla de integración futura

No se debe portar la web como backend del juego. Deben reutilizarse el comportamiento validado, los contratos y las reglas operativas:

- navegación y estados de consola;
- barridos, búsquedas, contactos y tracking;
- lecturas e incertidumbre;
- interferencias y compensación;
- potencia y coordinación con OPS;
- diagnóstico e Ingeniería;
- resultados e historial;
- handoffs interconsola.

La skin visual podrá cambiar por era o nave sin modificar la semántica de las operaciones.

## Formación

La Holocubierta incluye 25 prácticas de instructor en cinco niveles, desde operador básico hasta habilitación integrada. Esto sirve como especificación ejecutable de los flujos humanos esperados.
