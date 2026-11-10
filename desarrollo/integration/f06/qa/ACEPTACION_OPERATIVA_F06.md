# F06 — Aceptación operativa: guardia de Sensores (sin LCARS F07)

## Objetivo del jugador
En segundos, reconocer el sistema *observable* y consultar el inventario obtenido. La computadora permanece vigilante en segundo plano, no narra acciones rutinarias y escala únicamente contactos o incidencias relevantes. El oficial puede seleccionar un contacto y ordenar operaciones sobre el estado auténtico de CoreRPG.

## Integración experimental preparada en esta rama
- Un único F04Session/CoreRPG, un reloj, datos de contacto autenticados de F06.
- Barrido panorámico al entrar: recuento **solo de contactos observados** (no se revela la entidad romulana sin emisión o el klingon fuera de alcance).
- Datos observados de cada contacto: categoría, clase naval si está confirmada, transpondedor si resuelto, distancia, confianza, última observación, causa de pérdida si está acreditada.
- Informe planetario de un instrumento de **Host QA** basado en el Aster físico generado. Publicación *solo si pasan* el enfoque autorizado, la observación, el handoff a Ciencia y `f06_host_complete_science`. Se consulta posteriormente mediante `f06_science_reports_page`. Nunca se muestra al oficial directamente `science_truth` ni la clasificación privada original del JSON.
- El informe inicial agrupa clasificaciones planetarias **provisionales**, diferenciándolas de identidades navales confirmadas. No se infiere vida inteligente ni clase espectral estelar si no existe una medición publicable.
- Selección, observación focalizada, estudio detallado de dos minutos y seguimiento prioritario envían `FOCUS`, `SCAN` y `PRIORITY` al ejecutable nativo; no se simulan en Python. Los estudios temporizados requieren equipos disponibles y generan resultados solo al avanzar el reloj auténtico de Core.
- Configuraciones Estándar / Alta resolución / Antinterferencias / Máxima detección se aplican mediante `f06_configure` con el operador habilitado; `DIAG` ejecuta un autodiagnóstico de hardware auténtico de CoreRPG.
- La designación Aster I–VI se **deriva de las posiciones de los contactos observados respecto a la estrella**, no de los `key` de la verdad privada. Conserva identificadores al perder temporalmente el contacto.
- El validador científico F06-BIS y el esquema persistido admiten temperaturas >=20 K para reconocer planetas exteriores criogénicos reales (como Aster VI). Se conserva la exigencia de observación, instrumento autorizado y coherencia física. Los 6 planetas deben quedar publicados en el ensayo inicial o la CI falla.
- Aunque la clasificación provisional muestre M, nunca se supone una atmósfera respirable si la presión u oxígeno observado no lo justifican; indicios biológicos no equivalen a civilización confirmada.
- Mensajes rutinarios de trabajos automáticos quedan en backend. Avisos de nuevo contacto, identificación, recuperación, pérdidas, interferencias y avería se muestran con los datos disponibles.
- Exportación incluye eventos, contactos observados, informes científicos devueltos por Core y notas del jugador.

## Límites que NO deben ocultarse
1. **Aster es una fuente QA repetible**: la geometría, emisiones y mediciones de laboratorio se generan desde la ficha física del Host. No constituye el universo persistente F13. Las observaciones y los informes publicados sí atraviesan operaciones nativas de CoreRPG.
2. El barrido inicial y el enfoque inmediato utilizan las operaciones existentes, cuya escala temporal detallada todavía requiere calibración. No se ha validado que una Galaxy real complete espectroscopia de seis planetas en un tiempo concreto; la fase de ensayos debe hacerlo antes de declarar la simulación equilibrada.
3. El `f06_aster_science_generated.h` está compilado **solo** como instrumento QA autorizado, nunca como origen de conocimiento del jugador. Para sustituir Aster por F13 será necesario que su Host de mundo/instrumentos emita **lecturas reales** equivalentes, con revisiones y trazabilidad, en vez de usar el fixture.
4. La descripción espectral de estrellas, una civilización precurvatura, biosignaturas confirmadas, incidentes científicos avanzados y diagnóstico causal completo de fallos de identificación **no están implementados en esta prueba**; no se deben fabricar. Para hacerlos jugables se requiere ampliar los modelos/instrumentos F06 y la fuente F13 y comprobar el proceso completo.
5. Esta pantalla Tkinter no es LCARS, no es UE5 y no certifica F07. El motor de unificación continúa viviendo en el repositorio del videojuego; por el momento no hay motivo demostrado para modificar las estructuras genéricas del repositorio independiente CoreRPG.

## Aceptación mínima antes de utilizar en MSI
- CI Windows/Linux: C++ compila, 40+ escenarios F06 y regresión F05 pasan.
- `test_aster_runner.py`: informes Core de los seis planetas (M provisional, gigante J y criogénico), clases de nave no filtradas por truth privado, enfoque inmediato, estudios temporizados, diagnóstico/configuración, interferencias y guardado/carga deterministas.
- Revisión humana: informe panorámico útil, identificación naval concreta cuando se conoce, nada de ruido rutinario; selección y acciones responden.
- Verificación específica de que las mediciones científicas iniciales no vulneran tiempo, recursos ni autorizaciones. Hasta entonces se consideran una **integración QA candidata**, no una versión final jugable.
