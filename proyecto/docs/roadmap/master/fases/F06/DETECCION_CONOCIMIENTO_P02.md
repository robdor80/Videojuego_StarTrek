# F06-P02 — Detección relativa al observador, firmas y conocimiento

## Ruta de ejecución
1. Las entidades y sus firmas ya existen en el mundo antes del escaneo; Sensores **no crea realidad**.
2. La consola construye un sensor_scan_request con origen, ámbito, observador, modo, duración, resolución, filtros y estado sensor.
3. Se rechaza lo imposible: autorización externa no acreditada, puesto desocupado, matriz inoperativa, capacidad ausente, potencia insuficiente o contacto focalizado desconocido.
4. El motor preexistente desarrollo/tools/simulation/resolve_sensor_scan.py determina detección por distancia, firma, capacidad, potencia, integridad, modo, filtros, duración e interferencias.
5. Una evaluación de duración reducida ofrece **snapshot parcial de referencia**, no progreso real por ticks. Otra crea el resultado final.
6. Solo se proyectan campos observables; el ID real de entidad y ground_truth no salen en la respuesta pública. **Tampoco** salen los contadores internos entities_in_scope ni signatures_evaluated: revelarían posibles contactos que aún no se han detectado.
7. En focalizado se exige target_contact_id **conocido** y únicamente se proyecta ese contacto. Core deberá integrar selección/alcance en su motor, no solo en el wrapper.

## Invariantes
- Mundo, petición y contexto intactos; effects_applied=0.
- Contactos estables para un observador y diferentes entre observadores.
- Rastro no equivale a clasificación; información oculta solo tras alcanzar los umbrales legítimos.
- Escanear **el sector equivocado pero válido** se permite y puede devolver cero contactos; es fallo profesional, no técnico.
- Modo activo/pasivo, interferencias, filtros y duración alteran resultados reproducibles.
- Un bloqueo devuelve **cero eventos**, ningún dossier y ningún resultado.
- La duración registrada es un **coste estimado**, no una reserva de recursos.

## Propiedad
Star Trek mantiene catálogo sensorial, reglas de uso y proyección. Core RPG será dueño de reloj, reservas, validación final, concurrencia, identidad y persistencia. UE5 muestra acciones autorizadas. La IA redacta a partir del resultado, sin inventar nada.

**P02:** evaluable por tests independientes; aún no se ha ensayado Core/UE5.
