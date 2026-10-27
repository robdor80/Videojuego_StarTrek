# IDEA-0011 — DLC Cuadrante Delta: portal transwarp de acceso controlado

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación:** 17 de octubre de 2026  
**Estado:** **APROBADA CONCEPTUALMENTE**; diseño técnico, contenido, implementación y pruebas pendientes.  
**Decisión definitiva del autor:** **opción C** — regreso normalmente autorizado mediante el mismo portal, con posibilidad de interrupción temporal por averías, emergencias o misiones especiales.  
**Destino:** `proyecto/ideas/IDEA-0011_dlc_cuadrante_delta_portal_transwarp.md` del repositorio `robdor80/Videojuego_StarTrek`.  
**Áreas:** expansión opcional/DLC, geografía galáctica, tecnología transwarp, exploración, Borg, viajes intercuadrantes, temporadas narrativas, UE5, CoreRPG y persistencia.

## 1. Visión creativa y carácter opcional

Diseñar una **expansión independiente del juego principal** que permita a una nave de la Flota Estelar, incluida la nave del jugador y especialmente la **Clase Valhalla**, acceder al **cuadrante Delta desde el cuadrante Alfa** atravesando un **portal de aspecto hexagonal verde** inspirado en la tecnología de los conductos o nodos transwarp Borg vistos en Star Trek.

El autor **dispone de un modelo 3D** de ese tipo de portal, considerado **activo candidato**, pendiente de localizar, auditar, verificar licencia, escala, materiales, texturas, animaciones y rendimiento. El archivo aún **no está incorporado ni probado en UE5** por registrar esta idea.

La expansión constituye un contenido tipo **DLC opcional**: no es un episodio obligatorio del juego principal, no debe absorber sus temporadas ni convertir en accesible Delta antes de que se active el contenido correspondiente. La activación futura debe ser explícita y reversible dentro de las reglas de compatibilidad/persistencia que se definan.

**Resultado deseado:** disfrutar de nuevas expediciones, exploración, civilizaciones, oportunidades diplomáticas, anomalías, viajes y tramas en Delta, con entrada progresiva en territorios peligrosos y eventual contacto con el espacio Borg, **sin provocar una invasión Borg del Alfa mediante el portal**.

## 2. Principio innegociable: los Borg NO atraviesan este portal hacia Alfa

**DECISIÓN PRIORITARIA DEL AUTOR: los Borg NO pueden utilizar el portal del DLC para entrar en el cuadrante Alfa.** El anillo no constituye una puerta de invasión ni un puente libre de tránsito del Colectivo, independientemente de que el DLC esté instalado o activado.

Restricciones de diseño:

1. **DLC inactivo:** el portal no habilita ninguna ruta jugable operativa entre Alfa y Delta. Puede estar ausente de la escena o ser un elemento inerte si así se define en diseño; su presencia visible no debe activar viajes ni eventos Borg.
2. **DLC activo:** se abre una ruta intercuadrante **controlada** para expediciones autorizadas de la Flota/actor elegible y regreso bajo reglas precisas.
3. **Los Borg no tienen permiso ni posibilidad de atravesar este enlace hacia Alfa**, ni como jugador/NPC simulado, ni por misión emergente, ni por teletransporte narrativo, ni por actuación autónoma de la IA; el controlador debe **impedirlo efectivamente**, no limitarse a escribir «prohibido» en un briefing.
4. **No generar automáticamente** incursiones Borg en Alfa, alertas de invasión, aparición de cubos Borg junto al portal, conquistas o cambios políticos en el juego base por instalar/activar el DLC.
5. **Otros viajes Borg por el universo:** la voluntad expresada por el autor es que, si alguna nave Borg llegara a Alfa en nuestra continuidad propia, fuese por un **viaje convencional prolongado** (se citó «70 años» como imagen narrativa), **no por este portal ni por un atajo transwarp creado por el DLC**. Esa restricción narrativa deberá modelarse como **regla específica del videojuego/continuidad propia**, diferenciada del canon televisivo, donde los Borg poseen tecnología transwarp. No se fija todavía duración exacta ni se modifica silenciosamente toda la tecnología Borg del universo.
6. Las especies y sociedades de Delta pueden seguir existiendo y actuando fuera de cámara; la prohibición de entrada Borg no equivale a que el resto de Delta quede congelado.

**Riesgo a validar:** un portal inspirado visualmente en una infraestructura Borg no puede implicar que el Colectivo conserve control funcional sobre él. La solución narrativa propuesta es **tecnología recuperada/aislada, controlada por la Flota Estelar o sistema compatible de seguridad**, sin conexión operativa Borg a través de este enlace. Las causas concretas de ese aislamiento y su coherencia con época/canon propio quedan por escribir y aprobar; no inventar hechos históricos en una partida ya iniciada.

## 3. Regreso: opción C aprobada expresamente

**Política base:** la expedición puede regresar **normalmente por la misma infraestructura transwarp**, mediante orden y autorización válida, **si el portal y los sistemas necesarios están operativos**.

**Excepción autorizada:** determinados sucesos **realmente ocurridos y registrados** pueden impedir o demorar el regreso: daños o falta de energía, una interrupción del enlace, bloqueo por seguridad, una investigación de emergencia o un arco narrativo especial.

En esas situaciones, puede activarse una misión de reparación, recuperación, asistencia, identificación de condiciones de seguridad o alternativa de rescate; **no debe fabricarse una avería gratuita porque «toca» un capítulo dramático**.

### Estados operativos propuestos, aún no contrato definitivo

`inactive_without_dlc` · `installed_locked` · `operational_authorized` · `temporarily_unavailable` · `recovery_in_progress` · `restored`.

Todo estado depende de hechos y recursos reales de la campaña, no de un temporizador decorativo. Una vez restauradas las condiciones y validada la autorización de tránsito, se permite el regreso; el juego no fuerza a quedar 70 años abandonado en Delta por el simple hecho de activar el DLC.

**Evitar bloqueos injustificados:** si la trama introduce dificultades de retorno, los autores deben prever rutas jugables de recuperación/continuación, condiciones de fracaso y sus consecuencias. El retorno no se desbloquea mágicamente si la nave está destruida o el portal es físicamente inaccesible, pero tampoco debe haber un *softlock* por diseño incompleto.

## 4. Recorrido del jugador y experiencia de transición

1. DLC instalado y activado de forma válida en una campaña compatible.
2. La Flota anuncia o autoriza una expedición según el puesto, misión y contexto; el jugador no obtiene acceso omnipotente por ser protagonista.
3. La nave se aproxima al portal hexagonal visible en el espacio, con geometría, iluminación verde, efectos y colisiones/plano de tránsito según diseño real de UE5.
4. Se validan permisos, estado del portal, ubicación, seguridad, preparación de la nave y cualquier reserva de tránsito.
5. El timón ejecuta la aproximación bajo [IDEA-0009 — sistema universal de órdenes y maniobras](IDEA-0009_ordenes_protocolos_maniobras_universales.md).
6. Se muestra un **efecto/cinemática transwarp** y se carga el sector de destino, sin mantener en memoria ambos cuadrantes íntegros a la vez.
7. El universo persistente registra **una sola nave**, su tripulación, carga, recursos, daños, órdenes, tiempo y localización resultante. Nada se duplica por el cambio de escenario.
8. El jugador explora Delta mientras su nave/los NPC siguen bajo las reglas ordinarias del juego.
9. Cuando corresponde, podrá solicitar y ejecutar **regreso controlado**; fallos reales/episodios narrativos podrán aplazarlo según la **opción C**, sin conceder acceso de retorno a naves Borg.

**Importante:** no confundir salto espacial con reseteo de campaña. La salida y el regreso pertenecen al mismo `World State` y a la misma partida.

## 5. Contenido del cuadrante Delta

Objetivo: crear una **región jugable extensa y coherente**, no un único nivel alrededor de la salida del portal.

Conforme al periodo temporal de cada campaña y a su historial propio, el contenido candidato incluiría especies y culturas vistas en `Star Trek: Voyager`: Kazon, Ocampa, Talaxianos, Vidiians, Hirogen, Malon, Devore y Borg, además de sistemas estelares, planetas, estaciones, naves, rutas y anomalías compatibles con cada región.

**No situar todas estas especies a poca distancia del punto de entrada.** Definir cartografía, alcance tecnológico, contactos conocidos/desconocidos, zonas fronterizas, tiempos de navegación, amenazas, relaciones y territorios conforme al universo y a la continuidad de la partida.

No repetir obligatoriamente los siete años de episodios de Voyager: las series/películas son historia/canon previo al inicio de partida y **no dictan el futuro de la campaña**. Personajes y eventos de pantalla solo aparecen cuando corresponda a su época, estado real y consecuencias del mundo.

El espacio Borg debe ser peligroso y narrativamente importante; **no empezar el DLC teleportando la Valhalla directamente a una batalla contra un cubo**, salvo que la posición elegida/estado real lo justifiquen y se apruebe expresamente la premisa narrativa.

## 6. Temporadas exclusivas y libertad exploratoria

La expansión podrá ofrecer **temporadas y episodios propios**, diseñados como **Season Packs** compatibles con [IDEA-0006](IDEA-0006_temporadas_narrativas_misiones_episodicas.md).

Ideas ilustrativas, **no guiones aprobados**:
- Primera expedición y comprobación del portal.
- Cartografía de rutas y sistemas de Delta.
- Diplomacia y encuentro con civilizaciones locales.
- Investigación científica de anomalías o restos tecnológicos.
- Primera aproximación a zonas de influencia Borg.
- Emergencia del sistema de retorno, con misión de reparación o rescate (solo cuando se active de manera causal, no obligatoria en cada viaje).

Entre capítulos seguirá habiendo turnos, ocio, vida a bordo, navegación normal, exploración libre y misiones emergentes independientes.

La presencia de tecnología Borg en el argumento **no otorga al Colectivo acceso al portal**.

## 7. DLC, activación y guardados

**Modelo conceptual de producto/contenido:** expansión opcional instalada/activada por el jugador. No se ha definido distribución comercial, tienda, monetización ni empaquetado exacto; «DLC» significa **módulo de expansión desacoplado del juego base**.

Prever:
- Identificador y versión del pack, dependencias de versión del juego, contratos y assets.
- Instalación y comprobación local de contenido compatible (sectores, perfiles, especies, escenas, objetos y Season Packs).
- Portal **bloqueado/inactivo** sin pack válido y sin autorización.
- Activación con una **transición causal y segura en el estado del mundo**, sin afirmar que un artefacto tecnológico apareció retrospectivamente sin justificación.
- Estado de activación/ubicación/paso/regreso persistente en el guardado.
- **No desactivar o desinstalar el DLC en caliente si hay nave, personajes o hechos cuya restauración depende del contenido de Delta**; requerir retorno seguro, migración explícita, conservación de dependencias u otra política aprobada.
- No alterar automáticamente partidas existentes, fronteras, distribución Borg o hechos de la historia básica al activar el pack.
- Validación antes de transición; rollback o recuperación segura si falla una carga.
- Explicar claramente al jugador cuándo Delta está disponible, cuándo el regreso se encuentra temporalmente bloqueado y por qué.

La compatibilidad de **instalación en una partida ya empezada** y los detalles de cómo se incorpora el portal al World State son aspectos por decidir; **no** se aprueba ninguna inyección retroactiva arbitraria de hechos.

## 8. Diseño técnico y reparto de responsabilidades

| Sistema | Responsabilidad futura |
|---|---|
| **CoreRPG genérico** | Entidades, eventos, reglas genéricas, persistencia, recursos, tiempo/orden y transición de estados cuando los contratos reales lo permitan. No codificar Borg, Alfa/Delta ni portal específico en el núcleo genérico. |
| **Star Trek específico** | Definiciones del cuadrante Delta, especies, cartografía, permisos de tránsito, doctrina Flota, bloqueo Borg, canon propio, misiones y condiciones de activación. |
| **UE5** | Modelo 3D de portal hexagonal verde, iluminación, efectos y sonidos, transición de escenas, streaming, posiciones visibles y HUD. No es autoridad sobre concesión de tránsito/estado persistente. |
| **IA/Director narrativo** | Interpretar órdenes y narrar exclusivamente hechos/conocimientos legítimos; no abrir a voluntad el portal, inventar una incursión Borg ni violar restricciones. |
| **Validación de packs** | Comprobar dependencias, estado de instalación, IDs, recursos, compatibilidad y política de guardados antes de habilitar. |

Relación con otras ideas:
- [IDEA-0008 — Entornos espaciales modulares](IDEA-0008_entornos_espaciales_modulares.md): reutilizar el mismo sistema visual/posicional con perfiles de cuadrante y streaming.
- [IDEA-0009 — Órdenes, protocolos y maniobras](IDEA-0009_ordenes_protocolos_maniobras_universales.md): aproximación, tránsito, órdenes al timón y abortos seguros.
- [IDEA-0006 — Temporadas narrativas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md): misiones y arcos Delta como contenido modular cargado externamente.
- [IDEA-0007 — Carrera y mando de Valhalla](IDEA-0007_carrera_temporadas_llegada_y_mando_valhalla.md): la expansión no otorga capitanía ni acceso a Valhalla; mantiene el puesto real y las órdenes del jugador.

Documentación de base:
- [Continuidad de campaña](../docs/decisions/campaign_continuity.md).
- [Estado de navegación](../../sistemas/gameplay/navigation/navigation_state.json).
- [Modelo de ubicación estratégica](../../sistemas/gameplay/navigation/strategic_location_model.json).
- [F13 — Universo dinámico y exploración](../docs/roadmap/master/fases/F13/README.md).

## 9. Hoja de ruta candidata (NO iniciada)

- **DELTA-01 — Auditoría de contenidos:** localizar archivo 3D del portal, licencia, materiales, proporciones, pivotes, integración UE5; inventariar geografía y especies candidatas por época/canon propio.
- **DELTA-02 — Contrato de expansión:** definir instalación, activación, compatibilidad, navegación entre cuadrantes, restricciones Borg y gestión segura de DLC en guardados.
- **DELTA-03 — Representación UE5:** montar portal inerte y luego prueba visual de apertura, aproximación, efecto transwarp y transición de mapa.
- **DELTA-04 — Prueba de viaje bidireccional:** nave del jugador autorizada cruza a Delta y vuelve por el mismo acceso, con entidad única, tripulación y daño persistentes.
- **DELTA-05 — Bloqueo Borg verificable:** pruebas negativas con naves Borg y misiones emergentes intentando utilizar el portal desde ambos lados; **ninguna debe desembocar en Alfa**.
- **DELTA-06 — Opción C:** introducir avería o bloqueo de prueba registrado en World State; impedir regreso mientras exista, permitir reparación y posterior tránsito, respetando causas/autoridades.
- **DELTA-07 — Sectores y primeras misiones:** exploración limitada de Delta con una pequeña selección verificada de sistemas/especies y al menos un arco narrativo corto, sin extrapolar que todo el cuadrante está implementado.
- **DELTA-08 — QA y compatibilidad:** carga y guardado antes/durante/después de tránsito, viajes repetidos, rendimiento en MSI, instalación/actualización/desactivación segura y continuidad de NPC sin duplicaciones.

**Fases candidatas:** F02/F03 (arquitectura/persistencia), F07/F14 (activo 3D/UE5), F09 (navegación y órdenes), F11/F13 (misiones, regiones y exploración), F15 (validación/QA). La asignación exacta se fijará al planificar, sin dar por cerradas fases por archivar esta propuesta.

## 10. Criterios mínimos de aceptación futura

1. DLC desactivado/inexistente → portal no utilizable ni ruta Delta; Alfa no recibe eventos automáticos Borg derivados del DLC.
2. Activado y autorizado → nave compatible atraviesa Alfa → Delta de forma segura y coherente.
3. Regreso normal Delta → Alfa con el **mismo portal**, autorización válida y estado operativo (**opción C**).
4. Una avería/evento real puede bloquear temporalmente el retorno; el motivo se informa y una resolución verificable permite restaurarlo si se cumplen los requisitos.
5. **Ningún barco/nave Borg cruza hacia Alfa por el portal**, ni por órdenes, IA, rutas automáticas, misiones guionizadas o simulación fuera de cámara. Las vías de entrada Borg a Alfa no se crean con este contenido.
6. El jugador mantiene la identidad de nave/personajes, rango, misión, daños, recursos y estado al cruzar y volver; guardados y recargas no duplican entidades.
7. Los territorios Borg y de otras especies están localizados según cartografía/época; no son todos vecinos inmediatos de la salida del portal.
8. Un pack narrativo de Delta no cambia el pasado de una campaña ni obliga a reproducir episodios de Voyager.
9. La desactivación con entidades dependientes en Delta se gestiona sin destruir guardados ni dejarlos imposibles de cargar.
10. El rendimiento de portal, modelos y escenarios se mide en MSI; no se declara que un quadrante entero sea jugable tras probar solo la transición.

## 11. Decisiones cerradas y pendientes

**APROBADO:**
- Expansión opcional/cuadrante Delta separada del juego principal.
- Portal hexagonal verde inspirado en infraestructura transwarp Borg y basado, si es viable, en modelo 3D que posee el autor.
- Acceso desde Alfa a Delta para naves autorizadas y exploración de especies/regiones conocidas de `Voyager`, incluido riesgo de espacio Borg.
- **Los Borg NO atraviesan el portal hacia Alfa ni lo utilizan para invadir el juego base.**
- **Opción C:** regreso normal autorizado por el mismo portal, con posibilidad de dificultades/emergencias/misiones especiales de retorno.
- Continuidad de partida, estado persistente y coexistencia con temporadas narrativas y exploración libre.
- Aislamiento narrativo de Alfa frente a incursiones Borg generadas por el DLC; cualquier llegada Borg futura a Alfa deberá obedecer a una decisión autoral independiente, sin utilizar este portal.

**POR DEFINIR:**
- Ubicación exacta de la entrada Alfa y salida Delta, fecha y estado histórico del dispositivo.
- Quién lo construyó, recuperó o controla; justificación tecnológica de la exclusión Borg y requisitos de tránsito autorizado.
- Diseño final del flujo de instalación/desinstalación y seguridad de campañas ya activas.
- Lista concreta de especies, regiones/sectores, NPC, temporadas y primeras misiones implementables.
- Posibles naves autorizadas además de Valhalla, limitaciones de carrera y permisos.
- Política exacta de desplazamiento Borg por otras rutas en esta continuidad propia y cualquier divergencia con tecnología canónica.
- Integración del modelo 3D disponible, escalas, colisiones, efectos, audio, rendimiento y licencia.

**NO IMPLEMENTADA.** El presente archivo registra el diseño aprobado; no construye portales UE5, sectores, NPC, DLC operativo ni una conexión real Alfa/Delta.
