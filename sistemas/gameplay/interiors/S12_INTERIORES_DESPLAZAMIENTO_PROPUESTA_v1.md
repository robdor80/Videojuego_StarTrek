# Sistema 12 — Interiores, tránsito y presencia a bordo

> **ACTUALIZACIÓN AUTORAL 18-11-2026 — PROTOTIPO S12 NO APROBADO:** la identidad/autenticación/permisos de puertas privadas **pertenecen ahora al Sistema 18 (DEC-0024, fusionada en main)**, no a S12. S12 se concentra en puertas mecánicas/automáticas, pulsadores, turboascensores que llegan a la **parada real más próxima**, navegación de NPC y geolocalización/mapas LCARS. **No es un sistema de decoración, texturas ni construcción de recorridos Blender.** Véase S12_FUNCIONAL_PRIORIDADES_ADENDA_2026-11-18.md.

**Versión de trabajo:** 1.0 · **18 de noviembre de 2026**  
**Estado:** PROPUESTA PARA REVISIÓN AUTORAL — **NO APROBADO / NO IMPLEMENTADO**.  
**Nave central:** USS Enterprise NCC-1701-D, clase Galaxy modernizada por Geordi La Forge, **Proyecto Valhalla**. El buque no se denomina clase Valhalla.

## 1. Fantasía jugable

No queremos un menú «Puente / Ingeniería / Camarote», sino poder **vivir dentro de la nave**: salir de un camarote, abrir la puerta hacia el corredor curvo real, cruzar oficiales que van a su guardia, llegar al turbolift, seleccionar Astrometría y acceder a la sala, entrar al comedor, visitar Ingeniería o asistir a una emergencia. La sala y su función existen aunque el jugador no esté allí.

La interfaz debe ofrecer **dos caminos equivalentes**: (a) caminar libremente en 3D por los sectores realmente construidos y (b) elegir destino desde un plano/PADD o pedir indicaciones al ordenador; la asistencia puede trazar ruta y guiar, **sin teleportar al personaje a su voluntad**.

**Principio:** *geografía continua donde realmente hay escenario 3D; conectividad creíble mediante transiciones allí donde las escenas son independientes*. La experiencia del jugador debe resultar una sola nave, aunque UE5 descargue/cargue mapas interiores separados.

## 2. Tres capas que nunca deben confundirse

1. **Topología funcional persistente (CoreRPG):** localidades, puertas, enlaces, sección, cubierta, acceso, ocupación, condiciones de daño, distancia/tiempo, estado de energia, alertas. Es la verdad de dónde se puede estar y circular; se conserva la identidad de nave, habitaciones y tripulantes entre partidas.
2. **Presencia, agenda y viaje (CoreRPG/F12):** quién está realmente dónde, hacia dónde se dirige, si trabaja, duerme, está herido o evacuado; desplazamiento consume tiempo, no puede estar en dos sitios a la vez. NPC no representado en 3D **sigue existiendo**. F12 social no debe rehacer el interior, ni Sistema 12 debe crear su agenda.
3. **Representación y control (HOST/UE5):** mapas, puertas animadas, colisiones, efectos, caminata, transiciones de turbolift, carteles, sonido y versiones de sala dañada/alerta. **La IA no concede acceso ni teletransporta**: verbaliza planes autorizados.

El contrato `interior_navigation_graph_v0.1.schema.json` ya define `location_id`, `links` y tipos `walk/door/stairs/turbolift/virtual_transition`, y existe un enrutador `interior_navigation.py` probado offline. **Se amplía con overlays/escenas mediante contratos nuevos**; no se rompe el v0.1, no se modifican CoreRPG ni rutas de la fase F12 existente.

## 3. Separación de escenarios y escala: preservar geometría real

Regla previa del proyecto Valhalla: los interiores **NO necesitan encajar físicamente dentro del casco externo ni unirse geométricamente entre cubiertas**. Se exige coherencia y recorrido real *dentro de cada sector construido*. Turbolifts y transiciones UE5 conectan los escenarios. Esto evita un único mapa inmanejable y respeta el diseño de Blender ya realizado.

**Corredores y puertas de las cubiertas anulares** deben poder recorrerse **a pie** dentro del sector cargado. En D los camarotes abren directamente al gran corredor curvo, sin pasillos paralelos inventados; en E predominan espacios de esparcimiento y ventanales Galaxy. Usar módulo de corredor Voyager ya adaptado al estilo Galaxy Refit, sin alterar por sistema ni puertas existentes ni las mallas maestras.

**Reglas físicas de autor preservadas:** ocho designaciones 4-A, 3-B, 2-C, 1-D, −1-E, −2-F, −3-G, −4-H (los valores representan el esquema de proyecto, no alturas UE globales verificadas). D/E usan módulos de 2° y objetivo de altura interior libre 4,00 m. C/F emplean anillos 2,5°, B/G 4°. Para A/H no declarar un anillo completo verificado: A corresponde al puente principal/área superior; **H es el escenario del puente de batalla externo al modelo principal**. Este es un conjunto de referencias del diseño de Blender previo; la **existencia física, dimensiones finales y accesos de cada módulo requieren auditoría local** antes de enlazarla en un mapa jugable.

**Puente de batalla:** el recurso de puente Valkyrie Bridge 3 y su acceso se gestionan como **localización/escenario independiente con transición virtual vía turbolift**, no como una estancia pegada mágicamente al anillo principal. La disponibilidad, la sección correspondiente y su representación al separarse la nave respetarán el estado real de separación; no dar acceso por una puerta de pasillo inventada.

**Conexiones verticales:** no forzar escaleras que atraviesen escenarios que nunca fueron modelados contiguos. Si se construye un conjunto real de escaleras entre cubiertas consecutivas, que las geometrías, accesos y mapeo permitan un trayecto efectivamente continuo; en otros casos, el turbolift con transición simula el enlace y consume tiempo. Los conductos Jefferies pueden ser visitables en zonas realizadas, con tapas, autorizaciones y riesgos, sin obligar a modelar todos los conductos de una nave inmensa.

## 4. Inventario de recintos y prioridad de salas

**Elementos prioritarios dentro de la misma Enterprise-D** (no todas las cubiertas tendrán todo; la distribución exacta la decide la cartografía final, no el menú):

- Puente principal, sala de observación y despacho.
- Corredor maestro modular y conexiones radiales, nudos X/T/Y, accesos a turboascensores, tránsitos verticales autorizados.
- Camarotes personales y de oficiales; en D puertas hacia corredor y continuidad de identidad/cerraduras.
- Ten Forward y espacios comunes de E; comedor/bares; ventanales Galaxy con acabados modernos.
- Ingeniería, núcleo warp de varios niveles, sala de supercomputadora; estas áreas pueden ocupar **volúmenes de varias cubiertas**, según diseño ya existente, sin crear plantas falsas.
- Hangar, lanzaderas y acceso operativo; laboratorios, Astrometría S11, enfermería, transportadores, holocubierta de doble altura y salas de seguridad.
- Puente de batalla externo y sección de combate; estancias de servicio que permitan mantenimiento, alerta, reparación y evacuación.

**Distribución de salas aún por cerrar:** registros históricos sugieren B como camarotes de oficiales, C con hangar/enfermería, D/E con ordenador/holocubierta/cartografía, G con camarotes de alféreces, etc.; **NO se convierten aquí en asignaciones definitivas**. El diseño 3D final y la cartografía aprobada prevalecen. La sala de Astrometría S11 mantiene ubicación sin fijar.

## 5. Navegación y puertas

El jugador **camina por segmentos verificados**. Una puerta se anima si está operativa, permite acceso y existen dos zonas enlazadas; la falta de malla/paso **no se disimula con una puerta que atraviesa un muro**.

El **turbolift**:
1. Pedir destino por voz, LCARS o botonera.
2. El sistema comprueba nodo, acceso, disponibilidad, estado de alerta, daño, energía y ruta; puede negar o sugerir alternativa.
3. El jugador entra/activa transición; se simula sonido/movimiento del ascensor y **tiempo de desplazamiento razonable**, sin imponer paseo lento por un pozo físico inexistente.
4. HOST/Core actualizan el tránsito y la localización en el punto legal; UE5 carga la escena de llegada y devuelve control al jugador.
5. Guardar/restaurar durante transición no duplica al personaje, no lo deja flotando, no borra tiempo consumido ni reescribe acceso.

**Rutas no verificadas:** el existente MAP-01 exige `verified=true`. Un portal en diseño debe permanecer **pendiente y no enrutable** hasta auditoría real. Un enlace bloqueado por daños o acceso sigue conocido en la topología pero cambia de disponibilidad temporal, sin borrar la geometría histórica. No convertir transiciones de escena en teletransporte arbitrario.

**Puertas privadas:** ocupación, acceso, timbre/llamada, privacidad y consentimiento siguen F12 y las reglas sociales. Un invitado no entra automáticamente a un camarote porque existe un `DoorActor`. Alarmas/incendios/compartimentación alteran rutas y pueden desencadenar evacuaciones legítimas.

## 6. Presencia creíble de tripulación, sin mil NPC simultáneos

Cada oficial conserva su PERSON, camarote, puesto, guardia, descansos y obligaciones aunque no esté representado. Cerca del jugador se crean actores UE5 visibles y con navegación/collision; a distancia se aplica un LOD de simulación **de F12** sin cambiar identidad, relaciones, tiempo ni memoria. El juego no necesita instanciar visualmente toda la dotación de la Galaxy a la vez.

Al llegar al puente, quien está de guardia **debe** estar allí si su agenda y condiciones lo permiten. Si un oficial está en enfermería o en otro sector, no se duplica para rellenar una silla. La tripulación que circula por corredores tiene destino/tarea plausibles; no se fabrican amistades por un cruce de pasillo.

Visitas a camarote, encuentros con Siete, cenas con otros oficiales y actividad en Ten Forward se regirán por sus agendas, permisos, consecuencias y conocimiento, **no por proximidad geométrica**.

## 7. Estados peligrosos y mundo dinámico dentro de la nave

La misma sala puede estar **normal, en alerta amarilla/roja, sin energía, dañada, sellada, incendiada, contaminada, despresurizada o evacuada**. Los estados provienen de CoreRPG y sistemas de ingeniería/seguridad; UE5 los presenta sin modificar automáticamente el WorldState.

La red de puertas y rutas deberá poder cerrar un compartimento, proponer rutas alternativas, hacer llegar equipos de daños/sanidad y mostrar ausencia de servicio en turbolift. Hay sistemas de emergencia, pero **no saltarse un bloqueo solo porque el jugador pulsó “Ir”**.

En una emergencia, NPC que están fuera de escena realizan tareas según órdenes y tiempo disponible; los actores cercanos actúan en la escena. Un trayecto desde camarote a puente **consume tiempo** y una alarma puede exigir priorizarlo.

## 8. Interfaz y locomoción

- Perspectiva peatonal prioritaria **primera persona** para caminar por camarotes, corredores, salas y grandes espacios; ratón/teclado y mando; tercera persona opcional solo si más adelante se aprueba.
- Interacción in-world con puertas, ascensores, consolas, replicadores y PADD, sin convertir cada tramo en un menú.
- Plano LCARS 2D de nave por sección/cubierta con localizaciones **accesibles/descubiertas**, búsqueda por «Ingeniería», «Astrometría», «Mi camarote» y orientación de ruta, marcador discreto.
- Indicaciones por ordenador: «¿Cómo llego a enfermería?» → señalar camino o turbolift (no transportar automáticamente). Opcional guía/seguir ruta, nunca mover a NPC instantáneamente.
- Accesibilidad y antidesorientación: rótulos de cubierta, puntos de interés, volver a última zona conocida, mapa y alternativas de navegación sin mareo, cámara estable en ascensores.
- Controles y nomenclatura en **castellano**; estilo LCARS azul/cian y acabado Galaxy Refit A2.

## 9. UE5, recursos y estrategia para no destruir lo existente

**Inventario ya registrado en repo:** `assets/arbol_modelos3d.txt` muestra corredores, salas de cartografía, centro de ingeniería, sala de núcleo, holocubierta, camarotes, modelos Galaxy, puentes y recursos reutilizables. **Son referencias de inventario histórico, NO prueba de que el .blend esté montado/con colisiones y funcionando en Unreal**. Los binarios 3D locales siguen bajo su política de almacenamiento.

Importar cada conjunto Blender/SketchUp como **subescena/sector UE5** con:
- escala y orientación auditadas, origen, pivotes y coordenadas locales;
- conectores/entradas con ID estable y evidencia de apertura;
- colisiones sencillas con perfiles correctos, NavMesh de NPC y pruebas de paso;
- puertas que respeten el vano original, su marco y dimensiones;
- PBR estilo Refit A2 sin retopología destructiva;
- Level Instance / streaming por sector y carga anticipada durante transición de turbolift;
- un registro de escena que vincula `location_id` Core a `scene_asset_ref`, portal y posición segura de entrada.

**No** meter todas las cubiertas a la vez en memoria, ni trasladar toda la simulación social a Blueprints, ni usar miles de `Tick` individuales. Mantener personal visible cerca del jugador y LOD fuera de pantalla.

**Modo degrado/fallback:** si una sala todavía no tiene representación 3D acabada, mantener el lugar funcional a nivel Core y poder mostrar una representación simplificada/2D **marcada como provisional**, sin crear una puerta funcional hacia vacío o declarar que esa sala fue construida.

## 10. Casos narrativos que debería soportar

- De camarote D a Ten Forward E, a pie hasta turbolift y transición autorizada; posibilidad de conversación en corredor sin obligar a concluirla.
- De Ten Forward a Astrometría S11, para entrar en holograma 360°; si aún no existe sala/modelo se accede a la funcionalidad remota autorizada, **no a un escenario inventado**.
- Alerta roja mientras el jugador descansa: aviso, ruta viable hacia puesto de guardia, puertas cerradas por compartimentación; pueden aparecer bloqueos reales.
- Encuentro programado con oficial/NPC en sala de observación: comprobar presencia y horarios; si falta, avisar, reprogramar o esperar, sin teletransportar.
- Acceso a puente de batalla solo si existe la transición virtual y el estado de nave lo permite; al separar secciones, el mapa no abre un portal imposible.
- Visita a sala de ingeniería/núcleo, con áreas restringidas, peligro y asistencia de personal real.

## 11. Ámbitos no decididos (no rellenar por intuición)

1. **Posición definitiva de todas las habitaciones** y de Astrometría S11 (necesita asignación basada en escenarios locales).
2. Escaleras reales continuas en qué cubiertas, sectorización final D/E/C/F/B/G, número de turboascensores operativos y rutas exactas.
3. Qué recursos Blender locales ya superaron escala, colisiones y export FBX/glTF/UE5; inventario no sustituye auditoría.
4. Anchuras de corredores, umbrales de acceso, aforo real y distancias funcionales no medidos.
5. Cámara 3.ª persona, desplazamiento automático opcional y política de velocidad de paso/tiempo, a validar con primer prototipo.

## 12. Criterios de cierre de diseño y ejecución

**Propuesta documental:** tabla de cubiertas que no muta geometría, contrato de transiciones, pruebas previstas, matriz F12/UE5/HOST y vertical slice. **Pendiente ratificación del autor**.

**Cierre de implementación:** al menos un recorrido real desde camarote a corredor; una puerta con permisos; un turbolift entre dos mapas; acceso a sala funcional; un NPC con agenda y ruta; bloqueo por emergencia; save/load en tránsito; colisiones, NavMesh, LOD, FPS/VRAM medidos en MSI RTX 4070. El documento no demuestra nada de eso por sí solo.

**No se fusionará esta propuesta con las reglas vigentes como decisión aprobada sin evaluación del autor.**
