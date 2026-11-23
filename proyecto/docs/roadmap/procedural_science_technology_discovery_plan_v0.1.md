# Planificación 2 · Bloque 6 — Ciencia, tecnología y descubrimientos

**Nivel de cierre objetivo:** `COMPLETE_REFERENCE` exclusivamente documental, contrato y simulación offline. **No se entrega runtime CoreRPG/HOST/UE5.**
**Secuencia:** Bloques 1–3 COMPLETE de referencia; 4 y 5 REFERENCE_COMPLETE, PR #113 y #114 fusionadas. Se habilita B06, sin comenzar B07–B10.

## Propósito

Dar continuidad científica real a las civilizaciones y organizaciones de cada campaña: observar un fenómeno preexistente, contrastar hipótesis con instrumentos reales, desarrollar conocimiento, superar filtros institucionales y, cuando proceda, transformar ese hallazgo en un proyecto tecnológico de ingeniería para **una nave concreta**. El resultado no depende de la nave, rango, presencia ni agenda del jugador; una misma investigación puede ser desarrollada por NPC. Sólo hechos aceptados por el motor autoritativo podrán alterar la verdad del universo.

## Reutilización obligatoria

- `proyecto/docs/decisions/lore_02_d_author_decisions_v0.1.md` y `mundo/lore/science/lore02_d_scientific_legacy_policy_v0.1.json`: política autoral aprobada y los **ocho pasos** de investigación→astillero→adopción.
- `mundo/lore/science/scientific_domain_contract.json` y `sistemas/gameplay/science/sensor_analysis_model.json`: método, observación, incertidumbre.
- `mundo/lore/technology/`: capacidades según fecha/operador/plataforma, nunca instalación universal.
- B01: maduración de capacidades sin desbloqueo automático; B04: presupuesto preexistente; B05: historia causal sin alterar fuentes; F06: sensores y sus lecturas.
- LORE-01 astrogeografía para rutas reales; F11 para credenciales y cadena de mando; proyecto HOST para validación de sesión/órdenes; CoreRPG como única verdad.
- El concepto de la Enterprise-D modernizada o de «Sensores Rise» **no instala nada de forma anticipada** ni declara canon nuevas capacidades.

## Paquetes de B06

| Código | Entregable | Prueba de referencia |
|---|---|---|
| ST001 | Autoridad, separación Star Trek/CoreRPG/HOST/UE5/IA | Ausencia de escritor paralelo |
| ST002 | Ciencia por época, organización y contexto, no especie | Entradas verificables, sin progreso predeterminado |
| ST003 | Identidades, versiones y semillas deterministas | Estables por campaña, independientes de LOD |
| ST004 | Instituciones, investigadores y permisos | Acciones sin facultad se rechazan |
| ST005 | Sujetos y fenómenos preexistentes | No generar anomalías de B07 |
| ST006 | Instrumentos, alcance, calibración y recursos | No detectar con instrumental inexistente |
| ST007 | Observaciones y procedencia verificable | Fuente aceptada, fecha, instrumento y autor |
| ST008 | Hipótesis rivales, errores y contradicciones | No validar evidencia contradictoria |
| ST009 | Investigación sostenida y coste finito | No aparecen recursos gratuitos |
| ST010 | Revisión independiente y descubrimiento | Dos observadores e instrumentos independientes |
| ST011 | Evaluación científica/institucional y seguridad | Rechazo/espera antes de diseño |
| ST012 | Transferencia a ingeniería y compatibilidad de era | Sin desbloqueo genérico, Omega ni viaje temporal |
| ST013 | Reforma real, astillero y trabajos | Presupuesto, tiempo y nave concretos |
| ST014 | Pruebas, activación y difusión gradual | Instalada no equivale a activa |
| ST015 | Autoría, créditos compartidos y legado histórico | Nunca nombrar o robar crédito automáticamente |
| ST016 | Conocimiento y proyección para IA/PADD/NPC | Comunicación y clearance independientes |
| ST017 | LOD, replay, idempotencia, migración y pruebas negativas | Inmutabilidad/campañas aisladas |
| ST018 | Auditoría, estado, CI y frontera secuencial B07 | Sólo nivel demostrado |

## Decisiones operativas de referencia

1. **Lo observado no nace cuando llega el jugador.** La fuente de observación debe existir en el estado previo, estar aceptada y tener instrumento/autor/fecha. `accepted` es una **afirmación del fixture**; el adaptador real exigirá atestación CoreRPG.
2. Un sensor averiado, no instalado o no calibrado no produce evidencia confiable. Una hipótesis es provisional. En este adaptador, descubrir una relación corroborada requiere al menos **dos observaciones positivas utilizables, con dos instrumentos y dos investigadores distintos**; es una regla de pruebas conservadora, no fórmula universal de la física Trek.
3. Una contradicción utilizable impide certificar el hallazgo hasta resolverla expresamente; una lectura degradada no suma como corroboración. El fracaso y la ausencia de respuesta son resultados legítimos.
4. El proyecto necesita investigador autorizado, laboratorio existente, sujeto existente y una asignación de recursos aprobada y no reclamada. Los costes de referencia son sintéticos. B04/CoreRPG gestionarán los recursos reales.
5. Una revisión institucional puede aprobar o rechazar. Sólo una revisión aprobada permite estudiar un proyecto de ingeniería. El diseño precisa autorización de época, seguridad y clases **explícitamente compatibles**.
6. La autorización para fabricar un diseño **no** cambia `technology_band` de una civilización, no lo distribuye a todas las naves y no crea componentes ni armamento. Para utilizarlo: astillero activo, nave compatible, presupuesto y duración de obra, instalación, ensayo positivo y activación individual.
7. Un proyecto puede ser iniciado por el jugador, un científico NPC, una institución o un equipo; la capa de eventos nunca utiliza proximidad, cámara, nivel de detalle o rango del jugador como generadores de resultados.
8. La atribución científica recoge **todos los participantes reales**. Un nombre honorífico requiere una acción institucional específica; un ascenso o cambio de destino no elimina el mérito. «Sensores Rise» es una posibilidad ilustrativa, no mejora ya concedida.
9. Ser capitán **no exige física académica**: autorizar medios/prioridades, leer informes entendibles y decidir sobre riesgos. El jugador científico puede investigar opcionalmente con instrumentos, hipótesis y equipos.
10. Un informe puede ser verdadero y desconocido para un personaje. Los mensajes, la IA, las bitácoras y el PADD externo sólo reciben datos comunicados, conocidos y permitidos.
11. **Omega** conserva protocolo especial, confidencialidad y reserva de una misión de autor posterior. **Nada de viajes temporales jugables.** Los agujeros de gusano pueden estudiarse, pero sus rutas requieren ancla astrográfica real y las crea su dominio, no B06.
12. B06 no crea fenómenos (B07), crisis (B08), misiones (B09), historia retroactiva (B05) ni motor galáctico de trabajo en segundo plano (B10). Sólo procesa una secuencia de acciones previamente aportadas y produce un resultado de **referencia**.
13. `start_cutoff`, historia previa y reservas canónicas se respetan. Nunca insertar acontecimientos televisivos futuros obligatorios ni compartir resultados entre partidas.
14. Un evento tiene ID, tick, autor, tipo, causa, contenido y hash; repetición idéntica no duplica efectos, uso de ID conflictivo se rechaza y errores no alteran el input. Las migraciones de versión serán explícitas, no reinterpretación silenciosa.

## Datos y transición futura

El fixture de laboratorio/astillero es **sintético y no canónico**. El `snapshot` y su `events` no constituyen guardado operativo. El adaptador futuro deberá leer IDs/WorldState y hechos aceptados desde CoreRPG, revalidar autoridad a través de HOST, producir propuestas de transición para Core, registrar créditos con conocimiento real y representar su consumo en UE5. Si el núcleo no acredita los hechos, la operación debe fallar cerrada.

B06 entrega a B05 únicamente una **posible interfaz futura** de hitos científicos aceptados; B05 no se modifica ni se le hace reconocer un nuevo tipo sin su contrato actualizado. La instalación en una nave es independiente de la existencia de la definición de diseño; el catálogo LORE no prueba que la pieza esté allí.

## Evidencias

- Contrato: `sistemas/universe/generation/science_technology_discovery_reference_contract_v0.1.json`.
- Referencia: `desarrollo/tools/generation/simulate_science_discovery.py`.
- Fixture: `desarrollo/validation/fixtures/science_discovery/science_discovery_refit_v0.1.json`.
- Pruebas: `desarrollo/tools/generation/test_simulate_science_discovery.py`.
- Workflow: `.github/workflows/p2-b06-science-discovery.yml`.
- Acta: `proyecto/docs/roadmap/P2_B06_ACTA_CIERRE_REFERENCIA_20261112.md`.

**Cierre limitado:** tras tests y CI verde, contrato, prueba local de replay y documentación se marcarán `COMPLETE_REFERENCE`. No `CORE_INTEGRADO`, `UE5_JUGABLE` ni `HOST_IMPLEMENTED`. **Siguiente bloque:** B07, fenómenos, anomalías y arqueología, sólo cuando B06 esté fusionado y verificado.
