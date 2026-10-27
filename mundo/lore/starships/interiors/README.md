# Interiores como localizaciones jugables

## Principio

Una nave no es un único escenario llamado "interior".

Cada espacio relevante es una `Location` conectada a otras localizaciones.

## Núcleo común, cuando la clase lo tenga

- Puente
- Sala de observación / briefing
- Despacho del capitán
- Ingeniería principal
- Enfermería
- Laboratorios
- Sala de transportadores
- Hangares
- Bodegas de carga
- Camarotes
- Comedores / salas de descanso
- Pasillos
- Armería / seguridad cuando proceda

## Variación por clase

No todas las naves tienen:
- el mismo número de laboratorios;
- holocubiertas;
- familias/civiles;
- puente de batalla;
- gran hangar;
- instalaciones médicas avanzadas.

La clase y configuración generan el grafo de localizaciones.

## Estados de escena

Una misma localización puede presentarse como:
- normal;
- alerta amarilla;
- alerta roja;
- sin energía;
- dañada;
- evacuada;
- contaminada;
- incendio;
- gravedad reducida;
- sellada.

El World State decide el estado; Presentation decide cómo se ve.
