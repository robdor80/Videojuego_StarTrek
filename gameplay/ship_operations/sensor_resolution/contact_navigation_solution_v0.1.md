# Solución espacial de contactos de Sensores v0.1

Estado: **FOUNDATION FIXED**

## Principio

Un contacto no debe representar con un único campo ambiguo datos distintos como posición relativa y curso.

Cada solución de contacto separa:

- **Distancia**: separación actual respecto a la nave propia.
- **Marcación**: ángulo horizontal relativo a la nave propia.
- **Elevación**: ángulo vertical relativo al plano de referencia de la nave propia.
- **Curso**: dirección de desplazamiento del contacto, separada de su posición.
- **Velocidad**: magnitud de movimiento.
- **Movimiento relativo**: aproximándose, alejándose, cruce lateral, estable o sin resolver.
- **CPA**: máxima aproximación prevista / closest point of approach.
- **TCPA**: tiempo estimado hasta CPA cuando pueda calcularse de forma fiable.

## Regla UX

La consola presenta estos datos en filas separadas. No debe mostrar `316 / -04` bajo la etiqueta «rumbo».

Ejemplo:

```text
IKS Vornak
Distancia: 78.000 km
Marcación: 316°
Elevación: -4°
Curso: 142° / +1°
Velocidad: 0,17c
Movimiento relativo: aproximándose
Máxima aproximación prevista: 12.400 km
```

## Regla de datos

Campos recomendados:

- `distanceKm`
- `bearingDeg`
- `elevationDeg`
- `courseBearingDeg`
- `courseElevationDeg`
- `velocity`
- `relativeMotion`
- `closestApproachKm`
- `tcpaMinutes`

El antiguo campo `vector` se considera legado de prototipo y solo puede usarse para migración/compatibilidad. No debe emplearse como sinónimo de curso.

## Automatización

La Computer puede resumir operacionalmente la solución, por ejemplo «aproximándose» o «curso compatible con intercepción», siempre que derive de datos deterministas del World State/Sensor Core. El LLM no inventa posición, curso, CPA ni intención.

## Pérdida de contacto

Cuando un contacto se pierde, la alerta conserva la última solución conocida separando posición y curso. La causa de la pérdida sigue siendo independiente de esos datos.