# IDEA-0015 — Red de turboascensores inteligentes con lenguaje natural y navegación interior

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación conceptual:** 4 de noviembre de 2026  
**Estado:** **APROBADA CONCEPTUALMENTE; documentación registrada; implementación y pruebas pendientes.**  
**Decisión del autor:** «La apruebo», tras debatir y aceptar un sistema de viajes en turboascensor que comprenda destinos expresados libremente y reutilice la cartografía interior estructurada de cada nave.  
**Ámbito:** Valhalla/Enterprise-G y otras naves o instalaciones con red de turboascensores; navegación interior, IA, localizaciones, World State, streaming de escenas UE5, tripulación y tiempos de traslado.

## 1. Visión aprobada

El jugador entra en un **turboascensor real** de una nave y **puede decir inmediatamente, de manera natural, adónde desea ir**, sin memorizar comandos ni pulsar botones de selección de cubierta.

Ejemplos de voz del jugador:
- «Ingeniería».
- «Llévame al reactor warp».
- «Al bar».
- «Quiero ir a mi camarote».
- «Cubierta H».
- «A enfermería».
- «Voy a ver al jefe de máquinas».
- «Llévame a la sala de reuniones».
- «A cubierta G, que he quedado allí».

La **IA**, cuando haga falta, interpreta el significado, pero **el juego consulta su propia cartografía y estado autoritativo**, verifica la ruta y decide qué turboascensor de salida permite llegar al destino. Tras un tránsito coherente, se carga la cubierta o escena correspondiente y las puertas se abren en el **punto accesible más próximo al lugar solicitado**.

**No se exige crear físicamente todos los huecos, ejes y corredores verticales** de una enorme nave: es compatible con la arquitectura de **cubiertas y salas 3D modulares e independientes** decidida para la Valhalla. El traslado entre escenarios se realiza mediante transición controlada, sin duplicar personajes ni alterar el estado persistente por decisión de la IA.

## 2. Experiencia del jugador: flujo de entrada a destino

1. El jugador entra en una cabina de turboascensor disponible por una puerta físicamente existente/accesible; el origen y su turboascensor tienen IDs reales.
2. La entrada **activa automáticamente el modo de petición de destino**. Si la captura de voz es viable y está habilitada, puede escuchar al jugador en ese contexto; siempre habrá alternativa de **texto** y opción de repetir o cancelar. No activar escucha indiscriminada de micrófono fuera de la cabina.
3. El jugador habla/escribe libremente: «Al bar», «Mi camarote», «Cubierta H», «Ingeniería», etc.
4. Primero se intenta resolver la petición con un **catálogo local de alias y destinos**. Solo frases no triviales o ambiguas requieren interpretación de IA (si está disponible).
5. Si se usa IA, recibe **un subconjunto autorizado y suficiente del mapa semántico de la nave**, los nombres/alias compatibles y contexto mínimo de jugador; devuelve destino o candidatos estructurados, sin modificar la partida.
6. El **resolutor de destinos** contrasta el destino con el registro de lugares realmente existente en esa nave y en esa campaña; si no existe, es ambiguo o no se puede resolver, solicita aclaración o informa del motivo.
7. El **planificador de navegación interior** elige el turboascensor de salida **más cercano y accesible**, según conectividad real, rutas a pie, restricciones, disponibilidad de elevadores, daños, sección de nave, condiciones de alerta y permisos.
8. El motor valida el plan, reserva/ejecuta el desplazamiento según contratos efectivos, cierra puertas, calcula y consume **tiempo de viaje coherente**; UE5 reproduce cabina, luces, sonido y una carga de escena disimulada.
9. Tras llegar, aparece **la misma entidad** jugador en el turboascensor elegido, se abren las puertas y puede caminar hasta su destino. No teletransportar directamente al centro de Ingeniería, bar o camarote salvo que otro mecanismo existente lo permita expresamente.
10. La computadora puede indicar llegada o trayecto final si queda un tramo a pie, sin anunciar éxito antes de confirmación autoritativa.

**Regla de diseño:** la IA entiende **adónde** quiere ir el usuario; **el motor** calcula **cómo llegar y si es posible**.

## 3. Cartografía interior de cada nave: JSON como fuente de verdad

El autor propone dar a la IA un `.json` o `.md` con la distribución interior de la nave al entrar en la cabina. **Se aprueba el propósito, con una mejora técnica:**

- Mantener la **representación estructurada y validable en JSON/datos tipados** de la nave como fuente de verdad, asociada a clase, variante, nave concreta y cambios de configuración.
- Conservar **Markdown como documentación humana opcional**, no como segunda cartografía autoritativa cuya sincronización pudiera fallar.
- El catálogo debe describir **cubiertas existentes, estancias reales, nombres visibles, alias, destinos relativos, turboascensores, puntos de entrada/salida, conexiones, tiempos/costes de recorrido y restricciones**.
- El juego puede buscar localmente la mayoría de destinos, sin API.
- **No enviar por API el JSON completo de centenares de habitaciones en cada viaje**: construir, cuando haga falta, una vista semántica de **candidatos accesibles**, filtrada por el contexto/los permisos y versionada por nave. Evitar además enviar detalles confidenciales o ubicaciones sensibles a un modelo que el personaje no debería conocer.
- Los nombres conocidos deben registrarse con alias en castellano, pero permitir expresiones coloquiales que la IA vincule a objetos o lugares válidos; **la IA no inventará un destino porque suene plausible**.
- La ubicación de cada escena UE5 ha de referenciar **IDs de lugar y turboascensor** persistentes, no depender exclusivamente de una ruta de fichero o del nombre visible.

### Ejemplo ilustrativo, NO contrato ni mapa definitivo

```json
{
  "ship_instance_id": "enterprise_g_ejemplo",
  "interior_map_version": "borrador",
  "locations": [
    {
      "location_id": "main_engineering",
      "display_es": "Ingeniería principal",
      "deck_id": "por_definir",
      "aliases_es": ["ingeniería", "sala de máquinas", "reactor warp"]
    }
  ],
  "turbolifts": [
    {
      "turbolift_id": "TL_ING_EJEMPLO",
      "serves_location_ids": ["main_engineering"],
      "scene_entry_id": "TL_ING_EJEMPLO_ENTRY"
    }
  ],
  "connections_and_access": "grafo de rutas por definir"
}
```

**Importante:** `deck_id=por_definir` es deliberado. El diseño de cubiertas de la Valhalla continúa evolucionando; este registro **no asigna Ingeniería a una cubierta inventada** ni da por dibujada la red física. El ejemplo simplifica los datos: el grafo completo debe especificar conexiones realmente válidas y puntos de salida.

## 4. Resolución híbrida: catálogo determinista + IA cuando haga falta

### Camino rápido sin API

Para destinos exactos y alias claros, resolver localmente:
- «Ingeniería» → ubicación `main_engineering` si existe en la nave.
- «Enfermería» → enfermería válida de esa configuración.
- «Cubierta H» → validar que la cubierta H **existe en esa nave** y qué desembarco permite; preguntar por punto/sector si hay múltiples opciones no equivalentes.

### Camino de lenguaje libre con IA

Para expresiones complejas o indirectas:
- «Quiero ir donde trabaja el ingeniero jefe» → consultar ubicación profesional **real y conocida**, y resolver el tipo de petición.
- «Me apetece ir a tomar algo» → candidatos de bar/sala social; la IA propone el propósito, no inventa un bar.
- «Llévame al laboratorio donde trabaja mi amiga» → resolver persona y lugar solo cuando existe referencia válida, acceso y conocimiento adecuado.

**Salida propuesta del intérprete** (identificadores aún no implementados, compatibles en espíritu con el contrato existente de interpretación de órdenes):

```json
{
  "intent": "TURBOLIFT_TRAVEL",
  "destination_ref": "main_engineering",
  "clarification_required": false,
  "clarification_question": null
}
```

La petición no ejecuta un cambio de mapa por sí sola. Debe pasar por **validación de esquema, identidad del lugar, permisos, ruta, integridad de la nave y presencia de un punto de salida utilizable**.

Si el texto permite más de una interpretación, el sistema **pregunta antes de moverse**. Una confianza estadística no equivale a autorización.

## 5. Destinos contextuales: «mi camarote», «al bar», «cubierta H»

### «A mi camarote»

Resolver mediante **la asignación de residencia real y vigente del personaje** en esa instancia de nave/campaña. Si se cambia de camarote, rango, destino o nave, la frase seguirá funcionando sin reprogramar el alias.

El turboascensor desembarca en el **acceso más cercano permitido al camarote**, **no dentro de un espacio privado**. El tramo final se recorre caminando y conserva reglas de puertas, acceso e intercomunicación de [IDEA-0014](IDEA-0014_intercomunicadores_inteligentes_camarotes.md).

Si no existe camarote asignado en esa nave o la información es insuficiente, informar o pedir aclaración, no suponer uno.

### «Al bar»

Si hay **varios bares**, y ninguno está inequívocamente seleccionado por contexto o preferencia legítima, la computadora pregunta: «¿Nine Forward o Ten Forward?» (los nombres son **ejemplos**, no garantía de ambas salas en la versión jugable).

Una preferencia aprendida puede servir para resolver, pero no vencer restricciones de acceso ni alterar la información de identidad o la arquitectura de la nave.

### «Cubierta H»

Primero validar si existe como cubierta en **esa nave concreta**. Después seleccionar la salida conectada al sector requerido o, si no se identifica sector y hay destinos relevantes, elegir una salida principal definida y documentada, o pedir precisión. No fabricar geometría/numeración de cubiertas que el jugador no puede visitar.

### Destinos inexistentes o desconocidos

Ejemplos: un bar aún no construido, un camarote de otro NPC desconocido, una sala que ya no existe tras una reforma, o un espacio que la computadora no puede localizar con legitimidad. Responder con explicación o candidatos cercanos, **sin inventar coordenadas ni cambiar al azar de mapa**.

## 6. Red de turboascensores, restricciones y secciones separadas

El resolutor no elige necesariamente el ascensor **más próximo en distancia euclidiana**, sino la **salida más conveniente dentro del grafo de recorrido accesible**.

Aspectos a modelar:
- conexiones reales entre cubierta, pasillo, cabina y localización objetivo;
- escaleras u otras transferencias solo cuando **existan** y estén autorizadas;
- requisitos de acceso, puertas cerradas, áreas de seguridad, bloqueos de emergencia;
- daños, energía, ascensores fuera de servicio, peligros o incomunicación;
- secciones de platillo y cuerpo de batalla **desacopladas** en Valhalla: nunca conectar por turboascensor dos secciones separadas sin una unión legítima;
- roles de transbordo o **accesos especiales simulados** ya aprobados en otras ideas (p. ej. nave auxiliar tipo Defiant accesible desde el puente por turboascensor virtual), solo cuando su estado y permiso lo permitan;
- coherencia con el estado de ocupación y la capacidad real de la cabina.

Si el destino no es alcanzable, el juego responde por qué y, si existe, ofrece una alternativa válida. **No teleportar al jugador por comodidad de la IA**.

Los NPC usan la **misma lógica de tránsito interior**, aunque la simulación fuera de cámara use LOD y no reproduzca continuamente animaciones o streaming 3D. Un personaje no debe figurar simultáneamente en el turboascensor y en el puente.

## 7. Viaje, tiempo, transición de escenas y persistencia

**Objetivo:** crear una transición convincente entre cubiertas 3D independientes, manteniendo una única campaña continua.

- Una vez aprobada la ruta, cerrar puertas y cambiar a un **estado de viaje** autoritativo, con origen, destino, punto de llegada y participantes.
- Calcular **duración razonable** a partir de datos de red, distancia/recorrido o perfil de nave, sin fingir dimensiones o velocidades que aún no se han definido.
- Reproducir sonido de movimiento, luz y diálogo breve de la computadora, y **aprovechar ese intervalo para preparar la escena UE5 de destino**.
- Si hay un incidente, bloqueo o cancelación, resolverlo sin abandonar al jugador en coordenadas inválidas.
- Actualizar ubicación, calendario, disponibilidad y estado tras completar una transición válida; mantener guardado/carga, rollback seguro, idempotencia y trazabilidad.
- Al abrir puertas, el jugador ocupa **el turboascensor de salida accesible más cercano**, no un punto arbitrario del escenario.
- Mantener la cámara y los comandos de voz/texto sin transiciones bruscas o pérdida de control.

**Regla de persistencia:** no basta con cargar visualmente «la cubierta H» si CoreRPG/World State sigue diciendo que el jugador está en el puente. El sistema lógico y la representación UE5 han de coincidir.

## 8. Integración con arquitectura ya documentada

El repositorio dispone de elementos que conviene aprovechar antes de escribir código nuevo:

- [Modelo de ubicaciones interiores](../../sistemas/gameplay/ship_operations/interior_location_model.json): ya contempla `location_id`, `deck_or_section`, `connections`, `access_level`, `pov_profiles`, `access_state` y `occupants`. **Extender/reutilizar**, no duplicar.
- [Estado de vida a bordo](../../sistemas/gameplay/ship_operations/shipboard_life_state_contract.json): ubicación de personajes, servicios, privacidad y daños.
- [Inventario de tripulación](../../sistemas/gameplay/ship_operations/crew_manifest_model.json): identidad y asignaciones; la residencia real deberá consultarse donde esté efectivamente registrada, no inferirse del manifiesto.
- [Interpretación IA de órdenes](../../sistemas/ai/command_interpretation/starship_command_contract.md): principio **«AI interprets. Core executes.»**; el turboascensor debe tener su propio dominio de destino/desplazamiento sin convertirlo artificialmente en orden de timón.
- [IDEA-0014 — Intercomunicadores de camarotes](IDEA-0014_intercomunicadores_inteligentes_camarotes.md): reutilizar la infraestructura común de comprensión de lenguaje natural y de acceso/privacidad, sin confundir solicitudes de puerta con navegación interior.
- [IDEA-0010 — Nave auxiliar táctica](IDEA-0010_nave_auxiliar_tactica_furtiva_valhalla.md): acceso simulado por turboascensor desde Valhalla a una escena separada; reglas específicas de conexión y disponibilidad.
- [F12 — Vida a bordo y NPC](../docs/roadmap/master/fases/F12/README.md): integración con personajes, horarios y desplazamientos; otros hitos UE5/IA/navegación deben planificarse respetando su estado real.

### Separación de responsabilidades

| Componente | Responsabilidad |
|---|---|
| **JSON de nave / Star Trek** | Cartografía interior, alias, cubiertas, turboascensores, conexiones y restricciones por clase/instancia. |
| **Intérprete local / IA de lenguaje natural** | Convertir expresiones a candidatos de destino e indicar ambigüedad; **sin decidir cambios de estado**. |
| **Resolver de rutas / reglas del juego** | Comprobar destinos, permisos, capacidad, conectividad, tiempo y seleccionador del mejor punto de desembarco. |
| **CoreRPG / estado autoritativo** | Entidades, ubicación, tiempo, trayecto, eventos y persistencia según contratos existentes; no codificar taxonomía Star Trek específica dentro del núcleo genérico. |
| **Unreal Engine 5** | Cabina, puertas, audio, interfaz, cámaras, transición, streaming y representación final coherente con el estado aceptado. |

## 9. Etapas propuestas (NO iniciadas)

1. **TL-01 — Auditoría de cartografía:** localizar datos de cubierta/ubicación, escenas UE5, puntos de turboascensor y conexiones de la Valhalla; identificar faltantes, especialmente accesos virtuales.
2. **TL-02 — Contrato de destinos:** definir JSON canónico/alias, resolutores contextuales (`mi camarote`, `al bar`), permisos y estados por nave, sin fijar cubiertas no decididas.
3. **TL-03 — Prototipo de turboascensor:** cabina real con entrada automática de destino, alternativa por texto, sonidos y confirmación accesible.
4. **TL-04 — Interpretación híbrida:** búsqueda local sin API para alias claros; IA para lenguaje natural difícil y mecanismo de aclaración en múltiples destinos.
5. **TL-05 — Planificador de rutas y permisos:** grafo interior, salida más cercana accesible, continuidad entre secciones, interrupciones, daños y acceso de NPC.
6. **TL-06 — Streaming UE5 y tiempo:** transición de cabina a punto de salida, carga de escena, sincronización de reloj, eventos y World State.
7. **TL-07 — Casos reales:** Ingeniería, bar ambiguo, camarote asignado, cubierta concreta, destino inaccesible por separación de platillo y acceso virtual a nave auxiliar cuando proceda.
8. **TL-08 — QA MSI / regresiones:** voz y texto, idioma castellano y sinónimos, ausencia de alucinaciones, save/load, reintentos y latencia, múltiples NPC, versiones de mapas y pruebas negativas de acceso.

**Fases candidatas para futura planificación:** F03/F05 (persistencia/acciones), F07/F09 (navegación interior/UE5), F10 (IA), F12 (vida a bordo), F14 (presentación/audio) y F15 (QA). No asignar cierre ni alterar planificación actual por registrar la idea.

## 10. Criterios mínimos de aceptación futura

1. Entrar en un turboascensor habilita automáticamente solicitud de destino, con voz donde esté disponible y **texto siempre funcional**.
2. El jugador puede pedir destinos normales y coloquiales sin usar comandos rígidos: «Ingeniería», «al bar», «a mi camarote», «cubierta H».
3. La cartografía interior de esa nave está descrita mediante datos estructurados, validables y enlazados a ubicaciones/escenas.
4. La IA o resolver local produce **un ID de destino válido o una aclaración**, nunca una posición inventada.
5. `mi camarote` corresponde a la residencia **asignada y vigente** en esa partida; no se abre ni se entra automáticamente en ella.
6. Múltiples bares o zonas equivalentes desencadenan aclaración o preferencia previamente definida y legítima.
7. El planificador elige **el punto de desembarco más cercano que realmente sea accesible**, no solo visualmente próximo.
8. Separación de secciones, puertas restringidas, daños y ausencia de energía bloquean la ruta cuando corresponde; no existe teleportación arbitraria entre cubiertas.
9. El traslado consume **tiempo coherente**, carga el escenario adecuado y preserva identidad, posición, agendas y estado del jugador/NPC.
10. El sistema permite el acceso especial mediante turboascensor a la nave auxiliar de IDEA-0010 solo cuando esté presente y autorizado.
11. Fallo o retardo de API, respuesta tardía, cancelación y save/load no causan movimiento duplicado ni estados inconsistentes.
12. El juego **no confunde una confirmación en pantalla con un viaje completado**; se verificará trayecto real en MSI antes de declarar el sistema implementado.

## 11. Decisiones cerradas y abiertas

### APROBADAS
- Turboascensor activado al entrar: petición de destino **inmediata y natural**.
- Reconocimiento de destinos **expresados libremente**, por ejemplo «Ingeniería», «al bar», «mi camarote» o una cubierta.
- Disponibilidad para IA de la **distribución interior estructurada de cada nave** y contexto suficiente, sin obligarla a calcular la ruta real.
- **JSON estructurado como fuente principal**; Markdown solo como documentación opcional.
- **Búsqueda local primero, IA cuando sea útil**, para ahorrar tokens y reducir latencia.
- Devolución de una **intención estructurada** al juego y ejecución por el motor.
- Viaje hasta **el turboascensor accesible más próximo al destino**, con traslado y carga de escenario.
- Solicitud de aclaraciones, controles de permiso/estado, restricciones por secciones separadas y tiempo de viaje coherente.
- Reutilización de mapa interior, World State e interpretación general de IA ya previstos para el proyecto.

### PENDIENTES DE DISEÑO E IMPLEMENTACIÓN
- Mapa real de la Valhalla con todas sus cubiertas, salas, turboascensores y conexiones.
- JSON/schema definitivo, costes/rutas, estados temporales y gestión de variantes de naves.
- Modelo de entrada de voz y activación de micrófono en el ejecutable UE5.
- Política detallada de preferencia por bar/cubierta y aclaración.
- Velocidades y duración exactas de trayectos, animaciones de cabina y sonidos concretos.
- Contratos y ejecutores reales de viaje, autorización y cambio de escenas.
- Estrategias de ahorro de latencia/API, recuperación tras fallos y pruebas con NPC.

**Resultado administrativo:** IDEA-0015 **APROBADA CONCEPTUALMENTE Y REGISTRADA COMO DOCUMENTACIÓN**. Esta aprobación no implica que existan ya turboascensores inteligentes, una cartografía completa de la Valhalla, clases UE5 ni rutas de viaje probadas.
