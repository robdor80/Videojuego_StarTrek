# Generación de naves de campaña

## Objetivo

Poblar Starfleet con más unidades que las nombradas en pantalla sin inventar tecnología imposible.

## Flujo

```text
fecha de campaña
      ↓
clases válidas
      ↓
rol/necesidad operativa
      ↓
selección de clase
      ↓
identidad individual
      ↓
matrícula no conflictiva
      ↓
dotación + mando
      ↓
World State
```

## Reglas

Una nave generada:
- es `GAME_ADDITION`;
- no altera la definición de clase;
- debe respetar fecha y refit;
- debe evitar nombre/matrícula ya usados en el World State;
- recibe tripulación propia;
- puede persistir durante toda la campaña.

## Matrícula

No usar la regla ingenua:

```text
NCC más alto = nave necesariamente más nueva
```

Las fuentes contienen reutilizaciones, sufijos heredados e inconsistencias.

El generador usará un espacio de matrícula por era/configuración definido por contenido y validará colisiones, sin convertir el número en una fecha.
