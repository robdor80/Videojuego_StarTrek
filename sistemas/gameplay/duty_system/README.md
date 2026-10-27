# Sistema de servicio y guardias

El sistema de guardias convierte la vida a bordo en estado jugable continuo.

## Principio

```text
RANGO ≠ PUESTO ≠ ESTACIÓN ≠ GUARDIA ACTUAL
```

Un personaje puede conservar su rango y puesto permanente mientras, durante una guardia concreta:
- ocupa una estación;
- releva a otro oficial;
- ejerce como oficial de guardia;
- queda temporalmente fuera de servicio;
- recibe una responsabilidad de emergencia.

## Relevo

El relevo debe transferir lo que la guardia saliente **sabe**:
- misión y órdenes vigentes;
- posición/ruta;
- contactos;
- peligros;
- averías;
- restricciones médicas o de personal;
- comunicaciones pendientes;
- tareas sin cerrar.

No transfiere conocimiento omnisciente.

## Gameplay

Las guardias permiten que durante un viaje aparentemente tranquilo sigan existiendo:
- trabajo de puente;
- mantenimiento;
- vigilancia de sensores;
- conversaciones;
- informes;
- relevos;
- errores u omisiones;
- decisiones rutinarias que pueden volverse importantes más tarde.


## Generación de guardias por nave

La capa de profundidad vive en:

- `shipboard_watch_generation_contract_v0.1.json`
- `../ship_operations/off_watch_obligation_model_v0.1.json`
- `../ship_operations/off_duty_activity_catalog_v0.1.json`
- `../../lore/starships/classes/shipboard_life/SHIPBOARD_LIFE_PROFILE_CATALOG_v0.1.json`

### Regla

```text
DOTACIÓN DE REFERENCIA ≠ MANIFIESTO REAL ≠ PERSONAL ACTIVO EN ESTA GUARDIA
```

La nave genera primero sus puestos y cobertura necesaria. Después se asignan guardias, personal diurno, relevos, reservas y especialistas localizados.

En Starfleet, el modelo soporta tres guardias de 8 h o cuatro guardias de 6 h como regla de simulación compatible con el canon. La hora exacta de inicio pertenece a cada nave concreta. Otras organizaciones usan guardias locales/personalizadas salvo que exista evidencia canónica de su terminología.

Fuera de turno, un tripulante puede seguir ocupado con relevo, informes, entrenamiento, mantenimiento, guardia localizada, controles médicos, comida, descanso, ocio o compromisos privados. El jugador no puede volver disponible a un NPC simplemente iniciando una conversación.


## Guardia de Sensores

La estación de Sensores mantiene vigilancia pasiva continua incluso sin órdenes directas. La automatización de la nave realiza adquisición, actualización y control rutinario; el oficial supervisa, investiga, prioriza y reporta.

Regla de simulación:

**vigilancia continua ≠ eventos continuos**

Una guardia completa puede terminar sin novedades. La Computer no crea contactos, anomalías ni crisis para llenar tiempo.

Contrato específico:
- `sensor_watchstanding_protocol_v0.1.md`
- `sensor_watchstanding_state_v0.1.json`

La estación informa normalmente al oficial que tenga el mando del puente; el capitán solo recibe escalado cuando corresponda por presencia, órdenes permanentes, decisión del mando o gravedad.
