# F02-P03 — Adaptadores y fronteras propuestos (NO API aprobada)

**Estado:** diseño condicionado. Ningún nombre de método en este documento autoriza implementar una llamada a Core futura sin comprobar el contrato real.

## Diagrama lógico de responsabilidades

```text
Jugador / NPC / interfaz Sensors UE5 / voz
            |
            v
Host Windows UE5: entrada, UI, escena, audio, lifecycle y servicios remotos
            |
            v
Adaptación Star Trek: validar formato, traducir intención a semántica Trek
            |      ^                           ^
            |      |                           |
            v      |                      política Trek:
CoreRPG (autoridad de mundo)              sensores, rangos,
estado/acciones/validación/eventos         órdenes, protocolos
            |                                     
            v
Resultado validado -> proyección por observador -> UI, NPC e IA
```

### A — Adaptador de identidad y ciclo de vida

- **Existente en `main`:** `EntityId`, `WorldState::create_entity/contains/entity_count/revision`.
- **Prueba de concepto posible:** mantener `EntityId` lógico asociado desde el Host a un Actor temporal y quitar el Actor sin destruir la identidad lógica.
- **Prohibido:** crear una segunda entidad persistente como `AActor` o igualar matrícula NCC con `EntityId`.
- **Pendiente:** instanciación de definición, modelo vivo, save/load, contención de 4.5, hilo propietario, lifetime, errores y referencias cross-save. Confirmación del Core antes de declarar interfaz final.

### B — Adaptador de contenido Trek

- **Existente:** `ContentCatalog` de Core con manifest, dependencias, definición y clasificación en `0.1.0`.
- **Pendiente:** representar propiedades de naves, especies, herramientas, personajes y tecnología mediante futuros payloads acordados con el responsable Core. No modificar `schemas/content/0.1.0` unilateralmente ni serializar esos datos dentro del `ResourceKind`.
- **Star Trek mantiene:** canon, tres épocas, clases/tecnología, organigrama y tablas de procedimientos.

### C — Adaptador de órdenes y operaciones de consola

- **Star Trek define:** interpretación, jerarquía, responsabilidades, parametrización de barrido y respuesta formativa.
- **Core futuro ejecuta:** precondiciones comunes, mutaciones y eventos con resultado explícito.
- **No disponible hoy:** dispatcher, acciones generales, transferencias, autorización/delegación, resolución persistente de una guardia.
- Hasta 4.10, `tools/simulation/resolve_sensor_scan.py` es motor de **referencia de Sensores**, no autoritativo de campaña integrada. Evitar duplicarlo como Core en producción.

### D — Adaptador de visibilidad

- Core futuro devuelve o permite construir proyecciones con garantías actor-relativas (4.9).
- Star Trek define firmas, contacto, alcance, experiencia de consola y comunicación sensorial. El Host **no** puede recibir `ground truth` y fiarse de ocultarlo con un widget.
- IA/Academia/Companion reciben únicamente lo autorizado; no hay permiso implícito por estar conectado.

### E — Adaptador de Host UE5

- Propuesta de ubicación: en el proyecto Host o integración Star Trek-UE5, **no** en `CoreRPG/include` ni lógica de gameplay replicada.
- Puntos a demostrar con compilación real (F07): toolchain Windows/UE5, empaquetado librería C++20, CRT/ABI, manejo de errores y excepciones, ownership de objetos, hilos, cancelación y lifecycle de partida, mapeo de IDs a Actor.
- No bloquear la experimentación visual de puente por falta de Core; **etiquetar simulado** hasta integración.

### F — Academia, NAP y servicio de IA

- `academiaflota`: temarios y perfiles educativos web; progreso persistente de partida es otra responsabilidad. No inventar sincronización ni credenciales.
- NAP/Rob3D: importación y procedencia de assets; no modifican World State.
- IA remota: interpretador/redactor con contexto autorizado, salida candidata no confiable, nunca executor; la red y sus credenciales permanecen en Host.

## Puntos de integración que requieren contraparte

| Contrato futuro | Contraparte | Condición de aceptación |
|---|---|---|
| Modelo vivo e identidad | Core 4.5 | API publicada en `main`, tests de invariantes |
| Extensión de reglas Trek | Core 4.6 y consumidora Star Trek | Mecanismo aprobado sin términos Trek en Core |
| Persistencia e IDs | Core 4.7 | save/load de campaña y compatibilidad, test real |
| Proyección de conocimientos | Core 4.9 | prueba anti-filtración por observador |
| Acciones/órdenes/eventos | Core 4.10, Star Trek | ejecución estructurada, autoridad, auditoría, pruebas |
| Contexto IA | Core 4.12, Host | no entrega datos privados ni permite mutaciones |
| Integración UE5 | Core 4.14 / Host Star Trek | compilar/enlazar/jugar prueba de identidad |

**No cerrar P03** antes de concretar al menos las interfaces de la ventana Core realmente publicada y acordar las fronteras con sus responsables.
