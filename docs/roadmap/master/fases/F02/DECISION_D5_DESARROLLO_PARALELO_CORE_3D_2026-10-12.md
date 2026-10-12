# DEC-D5 — Desarrollo paralelo de Core RPG y producción 3D Star Trek

**Fecha:** 2026-10-12  
**Autoridad:** dirección técnica delegada expresamente por el autor del videojuego.  
**Estado:** APROBADA COMO ESTRATEGIA DE DESARROLLO. No equivale a aprobar una API Core todavía inexistente ni a abrir las fases F07/F08.  
**Ámbito:** coordinación entre `robdor80/CoreRPG`, `robdor80/Videojuego_StarTrek`, el prototipo UE5/Blender y el consumidor Nimroel.

## Decisión ejecutiva

Dos líneas de trabajo concurrentes, con **integración temprana y puertas funcionales**:

- **Línea A — Core genérico:** terminar primero el mínimo de entidades, estado autoritativo, reglas reproducibles, acciones validadas, conocimiento por observador, tiempo/causalidad, eventos y persistencia requerido por el vertical slice de Sensores. No intentar completar todos los futuros sistemas de Core (IA social completa, población/economía integral, inspector extendido, companion, generación procedural avanzada) para poder jugar una guardia.
- **Línea B — Star Trek 3D:** preparar modelos, Blender/Rob3D, escalas y materiales, pruebas de la Galaxy, separación del platillo, hangares independientes, puentes e interiores; UE5 puede probar importación, colisiones, animación y operación visual con *fixtures de laboratorio declarados no autoritativos*. Prohibido crear un segundo motor de mundo/guardado/permisos para sortear la dependencia.
- **Punto de encuentro:** guardia de Sensores v0.0.1: oficial subordinado, orden válida, operación, detección limitada al conocimiento permitido, informe, evento real, save/load y escena interactiva UE5. Tests y ejecución real en MSI requeridos para llamarla jugable.

## Hasta dónde puede avanzar Core sin que se descompensen las dos líneas

### Tramo C0 — terminar cimentación actual

1. Completar **4.5 Generic World State** en su propia rama, revisar archivos locales de Codex antes de tocarla, PR/CI/merge a `main` cuando sea correcto. Al 2026-10-12 `CoreRPG/main@dcfcb83c` sigue en 4.4 y `feat/generic-world-state@2a3da891` no está fusionada.
2. Probar pronto **dos riesgos de integración** sin esperar al núcleo completo: (a) mini-spike C++ Core/UE5 con un EntityId que sobrevive a destruir su Actor; (b) compilación/ejecución básica Android NDK, porque el Core también servirá a Nimroel Android. Son pruebas técnicas, no F07/F08 finalizadas.

### Tramo C1 — fundamentos de la guardia sin expandir el juego

3. **4.6**: RNG/reglas generales deterministas con solicitudes reproducibles; nada hardcoded de Sensores ni magia.
4. **4.7**: guardado y recuperación mínimos pero reales de identidades, revision, semilla/estado RNG y datos vivos incorporados; garantizar compatibilidad/versionado e integridad.
5. **4.8**: abordar **solo** modelado vivo/tiempo/agenda estrictamente necesario para el escenario cuando los contratos lo requieran; no construir automáticamente economía, generaciones familiares o poblaciones complejas.
6. **4.9**: proyección por observador que oculte contactos desconocidos; pruebas negativas anti-filtración.
7. **4.10**: acción genérica mínima autorizada, un único escritor de WorldState, rechazo/revalidación, idempotencia, reservas/efectos y causalidad de eventos, definidos a partir de una operación real Trek y una verificación de agnosticismo Nimroel.

El orden fino de 4.7–4.10 puede incorporar incrementos verticales, pero **no** saltarse las garantías que un test end-to-end necesita. No declarar cerrada una fase completa si sólo un subconjunto está implementado.

### Tramo C2 — punto de parada obligatorio

Cuando exista una **prueba headless real en C++** que haga *orden→autorización→escaneo/observación→resultado→informe→evento→guardado→recarga* con reproducibilidad, rechazo por permisos y cero filtraciones, junto al spike Core/UE5 de identidad, **congelar expansión funcional del Core** para esa entrega salvo defectos críticos.

Desde ese punto, priorizar su integración real en la guardia UE5. **No iniciar por inercia 4.11 Inspector, 4.12 AI/Context Builder completo, 4.13–4.15 ni sistemas sociales avanzados** sólo para mantener al equipo ocupado. Reabrir alcance de Core únicamente ante una necesidad validada de Star Trek/Nimroel.

## Qué puede hacer el equipo de modelado mientras tanto

- Auditar procedencia y derechos de los recursos *antes de distribución*, no afirmar que un asset es reutilizable por poder abrirlo.
- Conservar originales, versiones/hash; reparar geometría, UV, materiales, colisiones, puertas, escalas y rutas de navegación.
- Galaxy es la **base propuesta por el autor** en la sesión D1, a la espera de la confirmación/acta creativa; no fijar aún nombre final ni fecha de aparición de nueva clase.
- **Puentes candidatos para v0.0.1:** Kelvin (ya probado), y un **tercer puente completo descargado** comunicado por el autor el 12-10-2026; el nuevo recurso tiene apariencia completa **pero su funcionalidad aún no está verificada**. No seleccionar puente definitivo sin revisar licencia/procedencia, malla, texturas, tamaño, transitabilidad, colisiones, accesos, consolas e integración UE5. La Galaxy es la base propuesta para la futura clase protagonista, no una dependencia del primer prototipo.
- Prototipos UE5 pueden usar fixtures simulados únicamente para presentación, nunca como prueba de persistencia, IA, simulación o permisos auténticos.
- El trabajo de Blender externo no implica reactivar formalmente F07/F08: siguen pausadas hasta revisión de las PR del repo.

## Gobernanza y control de deriva

- Un objetivo activo para Core: la **guardia mínima reproducible**, no cerrar la lista completa de features.
- Por cada contrato genérico nuevo, probar al menos un ejemplo de Star Trek y revisar que no estorbe a Nimroel; nada de `if StarTrek` o `if Nimroel` dentro del Core.
- No adelantar sistemas de carrera, economía de naves, relaciones sociales completas o grandes flotas persistentes para desbloquear v0.0.1.
- Cuando **Core avance más rápido** que Blender, detener funciones nuevas en C2 y emplear esfuerzo en tests, portabilidad, defectos y documentación de contratos.
- Cuando **Blender avance más rápido**, aprovechar el tiempo en assets, materiales, accesos, colisiones y validación UE5, sin duplicar reglas de Core.
- Integración no debe esperar al fin de ambas líneas: humo Core↔UE5 temprano tras 4.5 y contratación de APIs a medida que queden verificadas.
- Puertas duras: compile/test Windows/Linux, prueba Android NDK temprana, UE5 smoke en MSI, E2E con WorldState, rechazo y save/load antes de afirmar F08 jugable.
- La IA remota nunca modifica WorldState; el companion/tablet es opcional.

## Registro de alcance

Esta decisión **resuelve D5** del cuestionario del 2026-10-12. 
No resuelve automáticamente las otras decisiones de autor D1, D2, D3, ni fusiona las PR #2–#7. El primer prototipo sigue siendo interno v0.0.1 Sensores; los datos de laboratorio no pasan automáticamente a la campaña.


## Addendum operativo — Codex Cloud y puente alternativo (2026-10-12)

**Aclaración del autor:** tras finalizar **NAP 2.0**, dedicará la capacidad de trabajo disponible de Codex a CoreRPG. Codex Cloud permite solicitar cambios desde móvil o fuera del MSI; ya no se requiere presencia física ante el ordenador para el desarrollo y pruebas que admitan infraestructura cloud. No iniciar este cambio de foco antes de que el autor comunique el cierre de NAP 2.0.

**Método de ejecución coordinado:**

1. Una unidad/PR de Core por objetivo verificable; partir del estado real de GitHub, comprobar cambios locales pendientes de Codex para 4.5 antes de reescribirlos.
2. Codex Cloud crea código, tests, documentación y commits en ramas controladas; CI debe pasar antes de integrar. Al volver al MSI, sincronizar explícitamente ramas/commits, **sin machacar archivos locales de Blender/UE5 ni trabajo sin subir**.
3. La construcción/enlace real de Core con el proyecto Unreal, la inspección de geometrías 3D y las mediciones del MSI **siguen necesitando pruebas en ese entorno**; una CI verde en cloud no las sustituye.
4. La dirección técnica compara el avance por **capacidades demostradas**, no por cantidad de commits o fases iniciadas. Detiene el desarrollo de nuevas funciones de Core al alcanzar el umbral C2 y lo comunica expresamente al autor; antes, prioriza defectos, portabilidad y pruebas si una línea se adelanta.
5. El prototipo **v0.0.1 no depende de terminar el puente Galaxy ni de rehacer Kelvin**: se elegirá el puente ya modelado que supere antes la auditoría de licencia y transitabilidad, haciendo las adaptaciones mínimas para operar la consola de Sensores.
6. No confundir "aparentemente entero" con "jugable": son puertas distintas (inspección de asset, importación, navegación/colisiones, superficies interactivas, rendimiento y test de guardia).

**Sin cambios de autorización:** F07/F08 continúan pausadas formalmente y las PR se revisarán una a una; este addendum no ejecuta ni adelanta esos trabajos.


## Identificación del tercer puente candidato — USS Sutherland (actualización 2026-10-12)

**Fuente identificada por captura del autor:**
[Star Trek: Sutherland Bridge](https://sketchfab.com/3d-models/star-trek-sutherland-bridge-7dcbb60473164f36a0a4f39df11b34c1), Sketchfab, perfil visible **Andrew Perdzock**.
El modelo representado en Rob3D figura como `star_trek_sutherland_bridge_Validado_....glb`, sin que este documento certifique hash ni identidad bit a bit del fichero exportado.

**Inspección visual comparada:** las capturas de Sketchfab muestran un puente de geometría aparentemente íntegra, con pasillos laterales, consolas simétricas, sillas, plataforma central, barandillas, puertas de turboascensor, pantalla principal y una pared de puestos LCARS. En Rob3D las texturas de pantallas están visibles pero los muros y techos se ven mucho más planos; **investigar iluminación, ambient occlusion, normales y materiales PBR antes de inferir pérdida de geometría**. No confundir captura renderizada con test UE5.

**Proveniencia y licencia:** una fuente secundaria externa atribuye el activo a Andrew Perdzock con **Creative Commons Attribution** (https://www.outerspace-software.com/community/15436/work-in-progress). La página de Sketchfab no pudo verificarse automáticamente: **LICENCIA_ORIGINAL_PENDIENTE_DE_VERIFICAR**. Antes de publicar o redistribuir, obtener copia de la licencia exacta y los créditos; el fanart basado en Star Trek añade derechos de la franquicia que la licencia del artista no sustituye.

**Siguiente puerta de revisión:** auditar GLB/mallas/materiales/orientación/medidas/colisiones y licencia; importar en UE5 con una cápsula de primera persona, caminar de la entrada a una consola lateral y examinar si cabe una interacción de Sensores. Si supera la prueba, puede sustituir al Kelvin como **escenario piloto de v0.0.1**, sin afectar a la futura nave Galaxy ni declarar F07/F08 iniciadas.

**Estado:** IDENTIFICADO_VISUALMENTE · CANDIDATO · NO_VERIFICADO_FUNCIONALMENTE.
