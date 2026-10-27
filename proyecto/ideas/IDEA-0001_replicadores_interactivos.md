# IDEA-0001 — Sistema de replicadores interactivos

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación:** 2026-10-11  
**Estado editorial:** APROBADA — pendiente de planificación técnica e implementación  
**Decisión del autor:** Aprobada expresamente el 11-10-2026, incluidas las ampliaciones debatidas.  
**Prioridad temporal:** Sin asignar; no desplaza la fase actualmente activa.  
**Áreas:** Ordenador de a bordo, interacción por voz, IA, Core RPG, UE5, vida a bordo, NPC, assets y audio.

## 1. Visión y objetivo

Transformar los replicadores de comida y bebida, actualmente representables por un modelo 3D, en **dispositivos funcionales dentro del mundo jugable**. El jugador se acerca a un replicador, pide de forma natural un alimento o bebida, el sistema interpreta su petición, identifica un artículo **existente en un catálogo autorizado**, comprueba que puede producirse y, si procede, hace aparecer un objeto 3D real en UE5 mediante efectos audiovisuales. Después el jugador puede cogerlo, transportarlo, consumirlo, depositarlo o entregarlo.

Ejemplo emblemático: jugador frente al replicador → «Té, Earl Grey, caliente» → taza con té materializada y disponible para interacción física.

**Alcance aprobado:** arquitectura universal reutilizable para naves, estaciones y otras instalaciones compatibles; peticiones naturales, catálogo de recetas/productos, efectos de replicación, objetos recogibles y participación de NPC. No es un simple menú decorativo ni una escena cinematográfica sin consecuencias.

## 2. Flujo de uso aprobado

1. El jugador entra en el área de interacción del replicador o selecciona explícitamente el dispositivo.
2. El juego ofrece una forma de activar la solicitud: voz mediante pulsar-para-hablar y alternativa manual/textual. La escucha permanente no es obligatoria.
3. La capa de ordenador de a bordo recibe el texto reconocido o escrito, junto al contexto del replicador.
4. Se intenta resolver primero la intención mediante reglas y sinónimos deterministas. Si hace falta, una IA interpreta lenguaje ambiguo o expresiones libres.
5. El intérprete devuelve **una propuesta estructurada** conforme al contrato de petición; no genera objetos ni modifica el mundo.
6. El subsistema autoritativo valida artículo, cantidad, variantes, disponibilidad, capacidad y estado del replicador, además de las demás reglas pertinentes.
7. Si la operación se acepta, se registra la creación del objeto en el estado del mundo, con identidad y atributos válidos. UE5 muestra el efecto de materialización y el sonido correspondiente; el resultado visual debe concordar con el estado real.
8. Al finalizar, el objeto puede recogerse, colocarse, consumirse, entregarse o desecharse. Las acciones y consecuencias se gestionan por reglas del juego.
9. Si existe un problema, el ordenador responde con una aclaración o un rechazo comprensible, sin crear un objeto ficticio.

**Principio:** la IA interpreta; **Core RPG y las reglas específicas de Star Trek autorizan la acción**; **UE5 la representa**.

## 3. Peticiones naturales e interpretación

Ejemplos equivalentes:
- «Té, Earl Grey, caliente».
- «Ponme un Earl Grey bien calentito».
- «Quiero un café con leche».
- «Replica una ración de gagh klingon», siempre que figure en el catálogo habilitado.
- «Lo de siempre», cuando exista una preferencia habitual registrada de manera explícita o inferible de datos válidos.

El ordenador distingue comida/bebida y extrae, si procede, cantidad, temperatura, receta, tamaño u otras variantes admitidas. Si la solicitud no es inequívoca, pregunta en vez de inventar una coincidencia. La respuesta debe ajustarse al carácter sobrio del ordenador de Flota Estelar establecido en el repositorio.

**Ruta eficiente:** comandos frecuentes por interpretación local/determinista; IA por API cuando el lenguaje realmente lo requiera. Evitar que toda petición consuma una llamada de modelo remoto. Permitir una alternativa sin voz y contemplar indisponibilidad de red/API.

### Ejemplo ilustrativo de solicitud estructurada

El ejemplo **no establece todavía una API definitiva**: nombres de campos, versión del contrato y límites serán verificados durante F02 frente a Core RPG.

~~~json
{
  "action": "replicator.request",
  "item_id": "tea_earl_grey",
  "category": "beverage",
  "temperature": "hot",
  "quantity": 1
}
~~~

La interpretación se valida contra un catálogo y esquemas cerrados. Una respuesta de IA no es una autorización para ejecutar funciones arbitrarias, inventar identificadores o modificar rutas de archivos.

## 4. Catálogo autorizado y recursos 3D

Cada artículo replicable se define mediante una **identidad estable** y metadatos separados del nombre comercial visible. Campos previstos, sujetos a validación de diseño:
- Identificador único, nombre localizado, categoría, sinónimos y clasificación cultural (incluidos platos del universo Star Trek y comidas/bebidas generales).
- Receta o definición de producto, variantes permitidas, cantidad/ración, envase/recipiente compatible y temperatura admisible.
- Referencias a los modelos 3D necesarios: alimento, bebida, recipiente y accesorios; materiales/instancias variantes y animaciones si corresponden.
- Reglas de uso, consumo, efectos de bienestar y permisos/capacidades si son necesarios.
- Referencias de procedencia, licencia y versión de los assets.

**No es obligatorio un modelo 3D por variante:** una taza reutilizable puede combinarse con distintos líquidos, materiales, colores y vapor. Un artículo no puede darse por materializado solo porque el nombre exista en el catálogo: debe disponer de representación validada o de una alternativa visual previamente definida y aprobada.

Los modelos descargados por el autor, incluido su replicador 3D funcional ya disponible, son **candidatos de integración**, no prueba automática de compatibilidad UE5. Han de revisarse licencia de distribución/uso, escala, formato, UV/materiales PBR, colisiones, puntos de agarre, pivotes, optimización, LOD y funcionamiento.

Usar nombres de archivo consistentes, pero desacoplar identificadores lógicos de rutas físicas. Propuesta inicial de ID: tea_earl_grey. La localización efectiva de assets se definirá mediante el pipeline de producción aprobado, sin inventar carpetas definitivas.

## 5. Materialización audiovisual y objeto físico

Implementar en UE5 una presentación inspirada en los replicadores de Star Trek mediante:
- Efecto de materialización visible y gradual (candidatos técnicos: Niagara/materiales).
- Efecto sonoro sincronizado (sistema de audio de UE5).
- Aparición en un punto de salida adecuado con orientación correcta y prevención de colisiones.
- Transferencia a un objeto interactivo real: coger, llevar, dejar, entregar, consumir o eliminar por vías admitidas.
- Manejo de cancelación, error de colocación, interrupción del proceso y restauración de partida sin duplicaciones.

Los efectos visuales y sonoros deberán producirse con recursos legítimamente utilizables y distribuidos según sus licencias. No se presupone autorización para extraer y redistribuir sonidos o modelos protegidos de otras obras.

**Invariante:** el efecto visual no puede crear entidades ajenas a las validadas. El objeto representado tiene identidad en el estado del mundo y su presencia debe conservarse conforme a las políticas de persistencia vigentes.

## 6. Consecuencias de juego y vida a bordo

La interacción debe enlazar con los sistemas reales de hambre, sed, necesidades, bienestar, hábitos y relaciones, conforme se implementen. No fijar aquí cifras, penalizaciones ni efectos médicos: pertenecen a las reglas correspondientes.

- El jugador puede consumir alimentos y bebidas, mover objetos o dárselos a otros personajes.
- Los NPC pueden realizar pedidos, recogerlos y comer/beber de acuerdo con horarios, ubicación y necesidades simuladas; **no exige tener a todos los NPC representados en 3D simultáneamente**.
- El ordenador puede gestionar preferencias («lo de siempre») si existen datos coherentes y accesibles; no debe atribuir memorias inventadas al personaje.
- Debe haber comportamiento definido para productos no disponibles, nombres ambiguos, pedidos imposibles, dispositivos averiados, falta de capacidad y autorizaciones especiales.
- Evitar que comida, tazas y residuos abandonados crezcan sin límite: definir reglas de reciclaje, despawn justificado, persistencia y rendimiento sin borrar arbitrariamente objetos relevantes.

## 7. Límites y decisiones de arquitectura

- **Core RPG:** acciones, validación genérica, identidad de entidades, eventos y persistencia cuando sus capacidades reales estén disponibles; no duplicar un segundo motor autoritativo.
- **Star Trek:** vocabulario, catálogo replicable, reglas propias de replicadores, ordenador de a bordo, canon y capacidades por tecnología/nave/civilización.
- **UE5:** interacción espacial, representación 3D, interfaces, sonido, físicas y efectos.
- **IA/STT:** transcripción e interpretación estructurada con permisos mínimos; ninguna escritura directa del World State.

La aprobación de la idea **no significa** que ya existan estos endpoints, contratos de Core, blueprints o assets preparados. Tampoco autoriza generar en tiempo real cualquier modelo 3D pedido por el usuario. **Regla inicial aprobada:** únicamente se replica un artículo con definición válida en el catálogo autorizado y recursos de representación previstos.

## 8. Entrega incremental recomendada (no calendarizada)

**Prueba técnica aislada:** replicador 3D aportado por el autor, tres artículos de muestra (por ejemplo Earl Grey, café con leche y un plato sólido), entrada por texto y voz si es viable, resolución de catálogo, efecto, aparición y recogida. Esta prueba no altera el alcance de la v0.0.1 de Guardia de Sensores.

**Integración posterior:** contrato real Core/Star Trek/UE5, persistencia, errores, consumo, gestión de preferencias, objetos transportables y uso NPC.

**Escalado:** catálogo más amplio, recursos Star Trek y cotidianos, variantes de recipientes, tecnologías y tipos de replicador donde proceda, optimización y QA.

## 9. Criterios de aceptación futuros

- Un pedido de «té, Earl Grey, caliente» produce exactamente un objeto correcto, físico y recogible cuando el replicador puede atenderlo.
- Una formulación alternativa equivalente resuelve el mismo artículo sin generar una receta nueva.
- Una intención desconocida o ambigua no produce ningún objeto y da una respuesta útil.
- Peticiones duplicadas, fallos de API, sonido, materiales o spawn no generan objetos fantasma ni duplicaciones persistentes.
- Es posible depositar, entregar y consumir el objeto; el estado del mundo se mantiene consistente al guardar/cargar.
- La interacción funciona por un canal alternativo cuando no se utiliza micrófono o IA remota.
- Un NPC puede hacer un pedido simulado coherente con su posición y agenda; su presencia 3D solo se requiere si la escena debe representarse.
- Rendimiento, limpieza/reciclaje de objetos y licencias de assets se validan antes de considerar la función lista para distribución.

Estos son **criterios propuestos**, no pruebas ya ejecutadas.

## 10. Relación con el Plan Maestro y fuentes existentes

Asignación preliminar, **sin abrir ni cerrar ninguna fase**:

| Fase | Relación |
|---|---|
| F02 — Arquitectura e integración | Contrato de peticiones, interfaz con Core, fallback de IA, validación y errores |
| F07 — Pipeline 3D y puente piloto | Replicador físico, puntos de interacción, objeto recogible en UE5 |
| F12 — Vida a bordo y relaciones | Consumo, bienestar, hábitos, uso NPC y objetos persistentes |
| F14 — Recursos audiovisuales y NAP | Modelos, licencias, sonido, VFX, optimización y trazabilidad |

Referencias existentes a reutilizar:
- [Plan Maestro F00–F15](../docs/roadmap/master/PLAN_MAESTRO.md).
- [Buzón oficial de ideas](BUZON.md).
- [Starship Computer](../../sistemas/gameplay/ship_operations/ship_computer/README.md).
- [F02 — Arquitectura](../docs/roadmap/master/fases/F02/README.md).
- [F12 — Vida a bordo](../docs/roadmap/master/fases/F12/README.md).
- [F14 — Recursos audiovisuales](../docs/roadmap/master/fases/F14/README.md).

## 11. Estado de decisión

**APROBADO por el autor (11-10-2026)**: concepto, alcance funcional, ampliaciones sobre consumo, NPC, preferencias y límite de catálogo controlado.

**Por concretar al planificar:** contrato JSON versionado definitivo, representación de cada receta, assets aprobados, lista inicial de productos, modelo de físicas e inventario, estado y reciclaje de objetos, integración con Core RPG y evidencias de pruebas.

**No implementado. No asignado a un sprint. No altera las prioridades de F01 ni el objetivo v0.0.1 de Sensores.**
