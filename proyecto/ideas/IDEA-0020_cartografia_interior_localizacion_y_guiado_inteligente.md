# IDEA-0020 — Cartografía interior de la Enterprise-D, localización de tripulantes y guiado inteligente

**Aprobación expresa:** 2026-11-06.  
**Estado:** APROBADA; **implementación autorizada por el autor**, progresiva y dependiente de que se finalicen las cubiertas. No declarar completado el mapa real sin datos geométricos verificados ni pruebas UE5.  
**Nave de referencia:** USS Enterprise NCC-1701-D restaurada y modernizada por Geordi La Forge (**Proyecto Valhalla**). El mapa **no** representa la distribución canónica de la Enterprise-D de televisión: debe describir **la configuración jugable realmente construida**.

## Experiencia requerida

- «Computadora, ¿dónde está el primer oficial?» → consulta a identidad, rol vigente, permisos y localización autoritativa del NPC; respuesta precisa solo si la computadora puede conocerla y el solicitante está autorizado.
- «Guíame hasta él» → resolver destino y ruta desde la posición actual del jugador, indicando corredores, puertas, escaleras, turboascensores y transiciones entre escenas. Si el NPC cambia de ubicación, recalcular cuando haya nueva información válida.
- «¿Cómo llego a Ingeniería?» → itinerario hablado y/o plano LCARS con ruta resaltada, por cubierta, con pasos comprensibles y alternativas.
- Camarotes asignados, habitaciones del capitán, puestos de oficiales, laboratorios, zonas civiles, enfermería, ingeniería y todos los espacios aprobados se identifican por **ID estable**, nunca por un número de habitación inferido.
- No inventar ubicación de NPC, acceso a salas, puertas, recorridos, plantas ni distancias que no consten en la nave jugable. Responder «ubicación desconocida», «sin acceso» o «ruta no disponible» cuando proceda.

## Arquitectura

**Fuente espacial única:** `sistemas/gameplay/ship_operations/interior_location_model.json` ya describe campos `location_id`, `deck_or_section`, `connections`, `access_level` y ocupantes. Ampliar por contratos compatibles, sin sustituir ni duplicar el modelo. Cada nave/instalación puede aportar su propia instancia de grafo.

1. **Inventario espacial estático versionado:** habitaciones, pasillos, puntos de entrada/salida, puertas, turboascensores, escaleras, escenas, conectores virtuales y coordenadas del plano por cubierta. ID estable y correspondencia verificable con Blender/UE5.
2. **Grafo navegable:** nodos de tránsito y aristas con tipo (caminar, puerta, turboascensor, escalera, transición), dirección, tiempo/coste si se mide, accesibilidad y restricciones. Un camino visual sobre el plano no demuestra conexión física: las aristas deben estar verificadas.
3. **Estado dinámico autoritativo:** posición actual o última ubicación conocida del jugador y NPC, puertas, peligros, alertas, zonas restringidas, asignaciones de camarote y ocupantes. Distinguir domicilio/puesto asignado/ubicación actual; no teletransportar actores por resolver rutas.
4. **Servicio de consultas:** `locate(entity)`, `resolve_destination(alias)`, `route(from,to,actor,world_state)`, `describe_route(route)`. Filtrar permisos, privacidad, información y frescura; comprobar acceso en cada tramo. El planificador no modifica World State.
5. **Computadora universal:** `sistemas/ai/command_interpretation/starship_computer_system.md` traduce voz/texto a intención; CoreRPG/Star Trek responde con datos validados; IA solo verbaliza o pide aclaración. Reutilizar IDEA-0015 (turboascensores) e IDEA-0016 (insignias/comunicaciones).
6. **UE5/LCARS:** exportación desde escenas reales, planos esquemáticos legibles, indicaciones paso a paso, resaltado de rutas y actualización ante bloqueos o cambios legítimos de ubicación. La escena 3D cargada es una representación, no la única fuente de ubicación.
7. **IDEA-0019 PADD:** posible consumo de planos autorizados y versión estática de rutas del último guardado, **sin localizar NPC en tiempo real ni avanzar el juego cerrado**.

## Orden de desarrollo autorizado

- **MAP-01:** contrato y validador de grafo, identificadores, conectores, accesos y errores; usar fixture sintético de pruebas, **no fingir un plano de la Enterprise-D**.
- **MAP-02:** inventario de cubiertas/salas definitivas y mapeo de IDs ↔ geometría UE5; trabajo iterativo según construcción.
- **MAP-03:** generador/exportador de mapa por cubierta desde datos verificados de la nave jugable, con control de versiones y pruebas de cobertura.
- **MAP-04:** resolver rutas accesibles y detectar desconexiones, bloqueos, accesos no autorizados y conectores virtuales.
- **MAP-05:** integración con localización autoritativa de jugador/NPC, permisos y privacidad; distinguir ubicación conocida y desconocida.
- **MAP-06:** interfaz de consultas de la computadora, insignia y turboascensores; respuestas progresivas sin inventar hechos.
- **MAP-07:** plano LCARS y guía visual/voz dentro de UE5, incluida actualización de rutas.
- **MAP-08:** QA MSI/UE5: recorrer destinos reales, salas inaccesibles, cambios de escena, replanificación, save/load y rendimiento.

**Dependencias:** F03 estado persistente, F04 dotación y espacios, F05 autoridad, F07 geometría/escenas, F12 horarios NPC, F14 interfaz y F15 QA. La definición y validación del formato pueden comenzar antes del cierre de cubiertas; la cartografía final exige las salas/puertas/conexiones definitivas.

## Reglas de aceptación

- El jugador no puede recibir una ruta a través de una pared, puerta inexistente, cubierta equivocada o acceso no autorizado.
- Una escena independiente conectada por turboascensor o transición narrativa tiene conexión **virtual explícita**, no se inventa una escalera física.
- El primer oficial puede tener camarote asignado y estar en Ingeniería; ambas ubicaciones son hechos distintos.
- Los NPC fuera de escena siguen localizables solo según su World State y la capacidad/autorización de seguimiento de la nave.
- Un bloqueo, alerta o cambio de destino obliga a revalidar la ruta; una ruta obsoleta no se presenta como segura.
- La cartografía se obtiene de la **Enterprise-D modernizada construida**, no de planos de fans ni del casco original sin adaptar.
- La idea y su implementación no alteran automáticamente el estado de F05, ni declaran F07/F12/F15 cerradas.

**Relaciones:** IDEA-0015, IDEA-0016, IDEA-0019 y contratos de `ship_operations`, computadora de la nave y World State.
