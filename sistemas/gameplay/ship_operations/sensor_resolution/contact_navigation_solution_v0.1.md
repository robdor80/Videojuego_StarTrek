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

## Idea UX futura · visor espacial del contacto seleccionado

Reservar en la zona central de la consola de Sensores un visor espacial del **contacto seleccionado**, usando blueprints/siluetas de la nave propia como referencia.

### Vista superior

- Nave propia centrada y orientada de forma fija, con proa a 000°.
- Espacio/anillo de 360° alrededor.
- El contacto seleccionado se representa como un punto en su marcación real.
- Una línea discreta une nave propia y contacto para facilitar lectura inmediata.
- Mostrar distancia asociada.
- Desde el punto del contacto sale una **flecha de curso** que muestra hacia dónde se desplaza, separando visualmente posición y movimiento.

### Vista lateral

- Nave propia de perfil y orientación fija.
- Plano horizontal de referencia marcado como 0°.
- El mismo contacto se representa arriba o abajo según su elevación positiva o negativa.
- Puede mostrarse también la flecha de curso cuando aporte información útil.

### Datos asociados

El visor acompaña, sin sustituirlos, a los datos textuales: distancia, marcación, elevación, curso, velocidad, movimiento relativo, CPA y TCPA cuando exista.

### Reglas visuales

- Un solo contacto seleccionado en este visor para evitar saturación.
- Orientación de las vistas siempre fija; no rotar la nave por motivos estéticos.
- Contacto normal: neutro; desconocido/prioritario: resaltado; hostil confirmado: rojo según reglas tácticas.
- Un contacto perdido desaparece del visor actual tras su transición visual; si se consulta desde históricos, mostrar solo su **última posición conocida** con tratamiento claramente histórico/discontinuo.
- La silueta de referencia debe adaptarse a la clase de nave del jugador (Galaxy, Miranda, Constitution, etc.) aprovechando los blueprints disponibles.

Esta idea queda reservada para la fase de UX final; no forma parte de la implementación funcional actual de la Holocubierta.


## UX futura · consola sin scroll global

La consola de Sensores debe permanecer estable dentro del viewport: **la página completa no debe desplazarse** durante la guardia.

La zona central de comunicaciones tampoco debe convertirse en una conversación infinita con scroll. Debe mostrar únicamente las comunicaciones recientes necesarias para el contexto inmediato; las anteriores se conservan en historial/log consultable.

Esta regla reserva espacio estable para el futuro visor espacial basado en blueprints (vista superior, vista lateral, marcación, elevación y flecha de curso) sin que nuevas alertas o respuestas desplacen la instrumentación fuera de pantalla.
