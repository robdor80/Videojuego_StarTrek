# F06 / ASTER — Especificación de terminación y aceptación a tiempo real
**Fecha:** 2026-11-23 · **Responsable funcional:** ChatGPT / propietario del videojuego · **Estatus:** decisiones funcionales aprobadas; implementación, auditoría y aceptación pendientes.

## 0. Propósito y límite
Finalizar **F06 — motor y laboratorio real de sensores ASTER**, NO la consola LCARS bonita ni el puente 3D de la Sutherland (F07), NI la primera guardia integral UE5 (F08), NI el universo persistente F13.

El resultado obligatorio es una **sesión CoreRPG real**, alimentada por un escenario espacial QA controlado, con detección y fichas de contacto inmediatas, mediciones y armamento de cada nave concreta, supervisión automática y una prueba humana de **5–10 minutos reales a ×1** en el MSI. Las pruebas de horas aceleradas serán independientes y no sustituyen esta aceptación.

**Reglas creativas aprobadas:**
- USS Enterprise NCC-1701-D, clase **Galaxy**, modernizada por Geordi La Forge en el **Proyecto Valhalla**; Valhalla NO es una nueva clase de nave.
- La computadora efectúa aproximadamente el 95 % de las operaciones rutinarias: sensores encendidos y barridos continuos desde t=0, detección y clasificación sin intervención; el jugador interpreta, prioriza, comunica y decide transferencias a Táctica/Ciencia.
- Para todo contacto **dentro de alcance, observable, no camuflado, y con sensores operativos**, la adquisición debe ser automática e inmediata, sin probabilidades arbitrarias de fallar. El camuflaje efectivo es una excepción. Interferencias y daños solo afectan cuando están realmente modelados.
- **SLA en la ejecución interactiva a ×1:** detectar en el primer ciclo disponible y presentar la ficha útil de identificación, características y armamento observado en **máximo 3 segundos reales desde la entrada observable** (objetivo habitual 1–3 s); sin esperar 20/120 s por escaneos manuales. Medir de evento fuente → publicación observada → visualización Tk con reloj monotónico, no únicamente ticks simulados. No esconder retrasos tras velocidades de reloj distintas.
- Catálogo y medición no son lo mismo. Si una unidad modificada lleva armas adicionales, se muestra lo observado y se compara con la configuración esperada; si no hay transpondedor se sigue identificando la clase por firma, si es reconocible, y se identifican armas físicamente observables incluso con clase desconocida.
- La ficha no puede inventar datos del mundo oculto. Los sistemas físicos y sus firmas de sensores deben **existir antes de ser descubiertos**. La generación procedural es reproducible y basada en reglas; la lectura por F06 está filtrada por conocimiento/mediciones válidas.

## 1. Situación real comprobada el 23/11/2026
- F06 principal **PR #91 Draft**, base main, rama feat/f06-sensores-core (HEAD 0f67affecbb56c7d70d129b057fa7c50497a3ebd).
- Guardia operativa **PR #96 Draft**, sobre #91, rama feat/f06-guardia-operativa-sensores-20261110 (HEAD df7dcb8850932191c9453a92dbad806ef14e7bbc).
- UX de tres zonas **PR #97 Draft**, sobre #96, rama fix/f06-aster-guardia-ux-ciencia-20261110 (HEAD bbf7f5d5d89cc84b4544a6049a1924ebf9632fde).
- **Atención:** el base_sha de #96 (049a4b...) NO coincide con el HEAD actual de #91 (0f67aff...). Conciliar y revalidar la pila en orden antes de integrar.
- Las #92, #93 y #94 están fusionadas en la rama F06, no equivalen a cierre en main.
- CoreRPG funciona mediante F04Session/F06 nativos y el Host QA materializa snapshots; **NO hay todavía productor espacial F13 autónomo de producción**. ASTER sirve como fuente QA repetible, sin falsificar universo final.
- La GUI existente es **Tkinter Python** (qa/aster_gui.py) y el runner nativo es qa/aster_runner.cpp. Los barridos y la automatización existen; los análisis extensos actuales son operaciones Core con duración. NO rehacer su núcleo.
- En la GUI hay un diccionario NAVAL_CAPABILITIES de **texto por clase**, NO una medición de la configuración instalada de la nave concreta.
- En el fixture heredado, el Vor'cha llega t=3600 s y la D'deridex t=7200 s. El validador build_validation_system.py fuerza ese calendario de 8 h y rechaza starships de clase desconocida. **No alterar ni borrar ese fixture de regresión: añadir un modo QA corto independiente.**
- El perfil de sensores 5 corresponde al refit individual de Enterprise-D; el armazón F04 subyacente de prueba es Miranda sintética. Indicar esta limitación con honestidad; no declarar casco Galaxy físico en ASTER.

Fuentes técnicas prioritarias:
- desarrollo/integration/f06/include/f06_sensors.h
- desarrollo/integration/f06/src/f06_runtime.inc y f06_autonomy.inc
- desarrollo/integration/f06/qa/aster_runner.cpp y aster_gui.py
- desarrollo/integration/f06/fixtures/aster_f06_qa.json
- desarrollo/integration/f06/build_validation_system.py
- desarrollo/integration/f06/qa/test_aster_runner.py y test_aster_gui_layout.py
- sistemas/gameplay/ship_operations/consoles/sensors/ship_class_registry.json
- proyecto/docs/roadmap/master/fases/F06/R2_ESTADO_PR_F06_Y_GATE_PENDIENTE_2026-11-19.md (PR #179 en revisión)
- proyecto/docs/auditorias/AUDITORIA_PLANIFICACION_1_F00_F15_2026-11-19.md

## 2. Fuente de verdad, contratos y separación
1. **Generación del dominio/Host QA:** crea por reglas y semilla estable un mundo de prueba, inventario de unidades, **equipamiento instalado realmente** (tipos, montajes, número, energía/estado, modificaciones), transpondedor cuando existe, firmas físicas observables y acontecimientos temporizados. Datos privados con procedencia y validación. No escribir resultados de sensores prefabricados.
2. **CoreRPG:** única autoridad para WorldState, reloj, identidades, autorización F05/F04, observaciones, cambios y save/load. El Host entrega la fuente espacial versionada, no recalcula contactos ni desbloquea datos por su cuenta.
3. **F06:** detecta objetos por su firma en el universo materializado y produce **observaciones públicas autorizadas**: clase inferida, atributos físicos medidos, armamento detectado y discrepancias frente al catálogo permitido. No leer ni revelar de modo directo campos host-only del JSON o IDs secretos. Medición basada en señal/materialización y reglas verificables, con estado de certeza y procedencia.
4. **Catálogo:** referencia técnica de clases y equipos *habituales*; el catálogo NO sustituye la medición de una unidad concreta ni prueba identidad/afiliación. El transpondedor, si existe, aporta identidad declarada; sin él la detección y análisis siguen operativos.
5. **GUI Tk:** visualiza únicamente la proyección autorizada de Core/F06 y permite las órdenes legítimas del oficial. NO calcula armas, inventa campos, hace informes de Ciencia por su cuenta ni actúa como segundo motor.

**Compatibilidad:** mantener ABI C, F04 pin y datos históricos sin romperlos. Si se requieren campos de equipamiento/señal, usar extensión opt-in versionada, o un API nuevo, con negativos contra filtración y guardado. Revisar colisiones de class_id=0 (nave desconocida), identificadores opacos, revisiones, reintentos y autorización. NO introducir dependencia obligatoria de una IA externa ni de red.

## 3. Ficha naval que ASTER debe entregar automáticamente
**Datos prioritarios (sin exigir abrir menús):** tipo/identidad cuando conocida, clase o “Clase no determinada”, transpondedor/ausencia, procedencia o afiliación solo si acreditada, posición/distancia/rumbo observable, tamaño/estructura, propulsión, defensas y **armamento de la unidad observada**. Mantener una ficha corta útil y “Datos técnicos” ampliables, sin logs de depuración ni relleno.

**Bloque ARMAMENTO Y DEFENSAS:**
- **Configuración esperada:** catálogo versionado y identificado por clase cuando exista.
- **Configuración detectada:** cada banco/emisor/lanzador medible de la unidad concreta, categoría, recuento, estado cuando sea medible, instante/fiabilidad y procedencia de la lectura.
- **Comparación visual:** VERDE = coincide con lo conocido; ÁMBAR = dispositivo extra, ausente o anómalo; ROJO = amenaza ofensiva activa que realmente conste; GRIS = sin referencia/no verificable. Nunca usar verde como sinónimo de “sin peligro”.
- **Nave totalmente desconocida y sin transpondedor:** NO exigir class_id distinto de cero para detectar inventario físico. Describir equipos observables (ej. “6 emisores energéticos ofensivos; 2 lanzadores”), no suponer nombre de clase ni inventar cantidades.
- **Modificaciones reales:** simular al menos una nave de clase conocida cuyo inventario instalado difiera del catálogo. La discrepancia se obtiene de dos fuentes independientes; no es un texto fijo ni un simple ‘if contact_id == X’ en Tk.
- **Actualizaciones:** un nuevo barrido vuelve a medir cambios reales sin duplicar avisos; cambios permanecen coherentes en histórico y tras save/load.
- Opcionalidad 3D: reservar identificador de recurso, pero no incorporar modelos ficticios ni bloquear F06 por el visor de F07.

Si el catálogo no conoce el número exacto de armas de alguna clase, **crear entradas QA explícitamente ficticias/no canónicas, documentadas como tales**; no atribuir cifras inventadas al canon. Los detalles internos de baja observabilidad requieren un modelo físico en el juego para su lectura; no revelar campos secretos sin observación.

## 4. Guardia corta obligatoria (modo ASTER_X1, sin reloj acelerado)
**Un segundo de simulación = un segundo real; tiempo transcurrido real objetivo total 5–10 min.** El modo debe ser seleccionable desde el lanzador/GUI y arrancar preferentemente en ×1. No hacer pasar un escenario reproducible guionado por un universo F13 dinámico.

Cronograma mínimo reproducible sugerido (modificable ± segundos por razones técnicas, sin superar 10 min):
- **t=0:** inicia Core + F06, vigilancia pasiva automática desde el primer tick, inventario observable del sistema, interfaz sin bloqueos. El carguero preexistente, si lo hay, está identificado.
- **t≈60 s:** entra/aparece un **nuevo carguero conocido con transpondedor**. Se detecta y publica su ficha técnica automáticamente en ≤3 s reales, sin escaneo manual; aviso discreto sin interrumpir la guardia.
- **t≈150 s:** aparece una **D'deridex romulana visible y sin transpondedor, con modificaciones ofensivas**. Se identifica clase por firma; enumera armamento observado y compara contra referencia; anomalía visible en ámbar. Alerta relevante pero decisión de informar/transmitir reservada al jugador.
- **t≈240 s:** aparece una **nave completamente desconocida** (clase no catalogada, transpondedor 0, firma observable). Los sensores caracterizan sistemas ofensivos/defensivos de esa unidad sin inventar nombre ni filtrar host-only.
- **t≈360 s:** **negativo de camuflaje**: contacto efectivamente camuflado no aparece ni filtra número/identidad; al descamuflarse, se detecta y analiza como los demás, con SLA. Si el motor no tiene camuflaje físico, modelar un caso QA claro y no fingir su implementación final.
- **t≈420–540 s:** el oficial consulta fichas, solicita transferencia Táctica/Ciencia de un contacto y un informe superior cuando decida; se reciben confirmaciones reales, se comprueba seguimiento, histórico y guardado/restauración. Sin acciones manuales para mantener vigilancia.

Los tiempos de 60/150/240 s son **acontecimientos de entrada, no temporizadores de identificación**. El usuario NO necesita activar FOCUS/SCAN para que la ficha básica y el armamento observable aparezcan. Los estudios profundos que realmente demanden tiempo existen como operaciones OPCIONALES, nunca bloquean la información esencial.

## 5. Automatización, notificaciones y flujo entre consolas
- Vigilancia 24/7 desde t=0, sin necesidad de oficial humano ni pulsaciones repetidas. Auto-lectura/identificación/seguimiento básico, tolerante a save/load.
- Sin inventar contactos por entretenimiento. Una guardia puede transcurrir sin incidencias.
- Contactos rutinarios (p. ej. carguero civil): alta, ficha, registro discreto. Amenaza o característica anómala: aviso destacado y acceso directo; sin enviar un parte oficial automáticamente ni asumir hostilidad solo por acercamiento.
- Las acciones humanas **COMUNICAR**, **TRANSFERIR A TÁCTICA** y **TRANSFERIR A CIENCIA** deben usar contratos y recibos reales de Core/HOST donde estén disponibles. Si no existe un consumidor final, registrar entrega de datos autenticada a una cola/lectura compartida claramente de QA; NUNCA representar un botón demostrativo como entrega efectiva a NPC o consola definitiva.
- Preservar flujo de tres zonas izquierda/centro/derecha y mapa actual, pero la selección nunca debe ocultar la ficha principal ni exigir una cadena de menús.

## 6. Pruebas automáticas obligatorias antes del MSI
**T01** ×1: lectura del mundo inicial desde Core + auto ON sin órdenes del usuario.
**T02** carguero a 60s: identificación, identidad transpondedor y ficha automática.
**T03** D'deridex sin transpondedor: clase inferida y catálogo vs loadout instalado distinto, discrepancia ámbar; nunca datos hardcoded de GUI.
**T04** clase desconocida + transpondedor 0: inventario real medido, sin class_id prestado ni alias engañoso.
**T05** nave conocida sin modificaciones: coincidencias VERDE con pruebas cruzadas de datos.
**T06** clase conocida modificada después de t=0: actualización de armamento y aviso sin duplicados.
**T07** ocultación/descamuflaje + no filtración de secretos; contacto no observable no aparece tampoco en buscar/archivos/avisos.
**T08** medición de tiempo: evento fuente, recepción Core, publicación F06 y refresco GUI, objetivo SLA ≤3s; CI puede verificar ticks y plumbing sin fingir medición de reloj real del MSI. Log monotónico local para aceptación humana.
**T09** SAVE/LOAD (idealmente nueva instancia de proceso), continuidad de identidades/observaciones/equipamiento/avisos; sin repeticiones ni cambios de las fichas al restaurar.
**T10** rol, revisión caducada, request duplicada, ID inventado, permisos, formato malicioso, regresión F04/F05/F06.
**T11** interfaz de 3 zonas sin controles tapados, navegación, scroll, ficha técnica, modo ×1 y botones accionables con respuestas de backend.
**T12** determinismo de misma semilla + suficiente diversidad en otras semillas, datos no canónicos etiquetados, integridad de catálogos.
**T13** transferencia a Ciencia/Táctica y comunicación con acuse real/QA trazable, no “toast” ornamental.
**T14** diferencias entre equipo dañado/no disponible y nave visible: avisos veraces y degradación física modelada, sin contradicción con detección garantizada en condiciones nominales.
**T15** suite acelerada de **8 horas** separada (×15/×30/×60), mismas reglas/salvaguardas, sin usarla como prueba de latencia ×1.

Pruebas C++/CTest + Python + GitHub Actions Linux y Windows; comparaciones antes/después con HEAD/SHA, memoria, errores, log de comandos, casos de fallo negativos y resumen pass/fail. No reemplazar pruebas genuinas por mocks del GUI ni considerar 100 % PASS prueba de aceptación visual.

## 7. Orden de ejecución para Codex Cloud
1. Congelar inventario del estado actual y auditar diferencias, base SHA, tests y dependencias #91→#96→#97; comprobar **actualidad respecto a main y F05**. NO fusionar ni cerrar nada hasta resolver deuda, verificar CI y aceptar el MSI.
2. Trabajar en una **rama aislada basada en #97**, conservando esta especificación y la historia; usar PR Draft apilada si procede, sin tocar a ciegas #91/#96. Ante desalineamiento #96/#91, resolver/ensayar secuencialmente y documentar.
3. Implementar **catálogo técnico versionado + equipamiento instalado procedural QA + firmas observables + medición Core F06**. Elegir interfaces compatibles: extender sin romper ABI/guardados legados y asegurar secreto Host.
4. Añadir modo corto ×1 y calendario propio; mantener intacta la regresión de 8 h. Reducir automatización manual innecesaria y garantizar primera ficha sin FOCUS/SCAN.
5. Integrar ficha de armas y discrepancias en Tk, transferencia y comunicación con recibos reales/QA bien etiquetados, y telemetría de latencias.
6. Ejecutar T01–T15 y regresiones F05/F04/F03 existentes donde corresponda; comprobar flujos Core multi-proceso y limitaciones; no declarar PASS a partir de resultados sin ejecución.
7. Entregar PR Draft con SHA exactos, matriz de aceptación, rutas, comandos MSI (doble clic, no instrucciones complejas), logs/CI y un **informe de qué está implementado vs qué queda fuera**.
8. Después el propietario ejecutará una **prueba visual real 5–10 min en MSI** y aprobará o pedirá cambios. Solo entonces discutir aceptación formal F06/P01 y requisitos cruzados con F05/F07; no marcar F06 CERRADA por el mero hecho de probar ASTER.

**Prohibido:** rehacer CoreRPG entero; atribuir a F06 el universo F13; declarar una consola UE5 F07 terminada; inventar armamento desde Tk o hacer que el clasificador lea datos secretos en vez de observaciones; forzar resultados desde scripts de demo; introducir integración IA/red obligatoria; alterar la identidad Enterprise-D/Galaxy; borrar historial; romper los escenarios acelerados.

## 8. Evidencia y entrega para revisión
- PR Draft y árbol actualizado con resumen de commits, base, HEAD y dependencias.
- Tabla T01–T15 con resultados verificables, entorno (Cloud CI vs MSI), SHA, logs y no-ejecutados explícitos.
- Guía nueva “INICIAR_PRUEBA_ASTER.cmd” + selección modo ×1 con cronómetro/telemetría; separar 8 horas aceleradas.
- Descripción de la política de conocimiento/armamento y esquema/procedencia real; prueba de nave desconocida.
- Lista literal de bloqueos pendientes de F05/manual PDF/UE5 que **impidan cierre administrativo**, sin rebajar inadvertidamente las puertas del roadmap.

**Modelo sugerido para implementación Codex:** GPT-6 / esfuerzo Alto. Desarrollo en Cloud; **MSI no necesario para escribir código**, sí para la aceptación visual del propietario.
