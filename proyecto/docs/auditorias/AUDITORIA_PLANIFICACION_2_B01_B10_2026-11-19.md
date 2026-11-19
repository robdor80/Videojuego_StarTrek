# AUDITORÍA INDEPENDIENTE — PLANIFICACIÓN 2 (B01–B10)
## Universo Dinámico · Videojuego Star Trek Legends · 19 de noviembre de 2026 · Informe 1.0

**DICTAMEN:** La **secuencia Planificación 2 está cerrada en madurez de referencia** (10/10 bloques, 177/177 paquetes declarados completos en sus respectivos alcances). **No está cerrada como universo dinámico jugable, autoritativo o integrado**. Existen defectos concretos de validación en los primeros simuladores, debilidades de confianza transversal y una importante deuda de pruebas entre bloques. Conviene reparar la referencia **sin iniciar todavía la implementación de F13 ni crear nuevos bloques**.

**Repositorio:** https://github.com/robdor80/Videojuego_StarTrek  
**Fotografía:** rama main, SHA 51f8aa33999fa1ded65b4052ce9bb2d5dda689ed (PR #174 fusionada), consultada el 19-11-2026.  
**Objeto:** Planificación 2, B01–B10; planes y estados, diez simuladores de referencia, suites, fixtures, contratos, actas B04–B10, workflows, frontera F13, CoreRPG/HOST/F11, canon y sistemas S01–S19 sólo en lo que afectan a P2.  
**Método y limitación:** inspección remota del código y documentos mediante GitHub, contraste de metadatos de rama/PR y evidencias CI declaradas. **No se han ejecutado en esta auditoría los 383 tests, CoreRPG, HOST, Unreal ni benchmarks en el MSI.** «Confirmado por lectura» significa condición observable en el código, no fallo reproducido en una nueva ejecución. Los resultados GitHub Actions se atribuyen a los commits exactos documentados, no a cualquier HEAD posterior.

**Disciplina:** esta auditoría NO modifica contratos, reglas, código, workflows, estados, assets ni otros proyectos. No cambia canon ni abre fases F13. Propone un plan de saneamiento para la conversación responsable de Planificación 2; las fronteras externas deben remitirse a las auditorías de sus propietarios. El juego tiene uso exclusivamente privado: no se requiere ni se presupone distribución.

---

## 1. Resumen ejecutivo y respuesta «¿qué falta?»

1. **Bloques de referencia pendientes de crear: CERO.** B01–B03 figuran como COMPLETE en el plan y sus manifiestos; B04–B06 como COMPLETE_REFERENCE / REFERENCE_COMPLETE según documento; B07–B10 como REFERENCE_COMPLETE. Los diez simuladores están presentes.
2. **Paquetes declarados cerrados: 177/177**, suma documental 15+16+18+16+16+18+18+20+20+20. No equivale a 177 funcionalidades dentro de UE5.
3. **Última suite global P2 certificada históricamente:** 383/383 pruebas B01–B10 (incluye todos los bloques), 30/30 F13 y 9/9 Academia, en el HEAD endurecido B10 7cbc4631b4cea44e7657c9115716872ad29a55a0; PR #122 fusionada en e3ae738d9ae14f949982b49ef3b2786dfcdf18db con 26/26 workflows previos y 21/21 posteriores según acta B10. [Acta B10](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/P2_B10_ACTA_CIERRE_REFERENCIA_20261112.md).
4. **Madurez real:** CONTRATO + SIMULADOR + FIXTURES + CI OFFLINE. No existe una cadena B01–B10 conectada a WorldState auténtico, scheduler nativo, commit transaccional, reloj persistido, órdenes F11/HOST, save/load de la galaxia ni escenas UE5 jugables.
5. **F13 global:** PLANIFICADA. Capas procedurales 001–118 se declaran completas en su *alcance de referencia*, 119 PARTIAL, 120 BLOCKED_RUNTIME. No promocionarlas por completar P2.
6. **Deuda previa al cierre saneado de referencia:** corregir defectos H01–H07; reforzar reglas de confianza H08–H14 y cobertura cruzada H15–H20. No se puede dar porcentaje de progreso del runtime: no hay una base de aceptación nativa que permita calcularlo.
7. **Decisión propuesta:** mantener P2_B01_TO_B10_REFERENCE_CLOSED_RUNTIME_PENDING; introducir una distinción adicional «AUDIT_REMEDIATION_OPEN» en *un informe de reconciliación*, nunca degradar sin prueba los diez cierres históricos. Terminar QA de P2 por fases de reparación R0–R5 y dejar integración futura R6–R7 para F13.

### 1.1 Criterio de estados

- **DISEÑO:** reglas e invariantes descritos.
- **CONTRATO:** entradas/salidas y autoridad identificadas.
- **REFERENCIA_PROBADA:** simulador aislado y pruebas offline.
- **REFERENCIA_RECONCILIADA:** nivel anterior con hallazgos de esta auditoría cerrados, negativos nuevos y CI.
- **CORE_INTEGRADO:** hechos y órdenes validados sobre CoreRPG real, transacciones/persistencia/replay nativos.
- **HOST_INTEGRADO / UE5_JUGABLE:** servicios y representación de partida real.
- **ACEPTACIÓN FINAL:** pruebas de continuidad, rendimiento y experiencia autorizadas.

No sustituir los estados del Plan Maestro por estas etiquetas sin migrar sus validadores. PR fusionada y «test PASS» no prueban automáticamente una galaxia operativa.

---

## 2. Matriz de los diez bloques

| Bloque | Dominio | Paquetes | Estado de referencia | Material verificable | Pendiente principal |
|---|---|---:|---|---|---|
| B01 | Civilizaciones y relaciones | 15/15 | COMPLETE histórico, sólo referencia | Contratos + simulador + 9 tests | Conciliar población y autoridad sobre guerra |
| B02 | Colonización y fronteras | 16/16 | COMPLETE histórico, sólo referencia | Contratos + simulador + 10 tests | Vincular elegibilidad/prewarp con fundación |
| B03 | Conflictos y guerras | 18/18 | COMPLETE histórico, sólo referencia | Contratos + simulador + 13 tests | Unicidad de fuerzas, estados y daño |
| B04 | Economía viva | 16/16 | COMPLETE_REFERENCE | Contrato, fixture, 30 tests y CI #113 | Autoridad transaccional y titulares de recursos |
| B05 | Historia procedural | 16/16 | COMPLETE_REFERENCE | Contrato, fixture, 36 tests y PR #114 | Acreditación real de fuentes/conocimiento |
| B06 | Ciencia/descubrimiento | 18/18 | COMPLETE_REFERENCE | Contrato, fixture, 54 tests y PR #115 | Ensayo/instalación con hechos y permisos reales |
| B07 | Fenómenos/arqueología | 18/18 | REFERENCE_COMPLETE | Contrato, fixture, 56 tests y PR #116 | Custodia, sensores y materialización real |
| B08 | Crisis sistémicas | 20/20 | REFERENCE_COMPLETE | Contrato, fixture, 56 tests y PR #118 | Del riesgo previsto a hechos aceptados externos |
| B09 | Misiones emergentes | 20/20 | REFERENCE_COMPLETE | Contrato, fixture, 65 tests y PR #120 | Órdenes/reservas/resultado externos y jugadores/NPC |
| B10 | Evolución galáctica offscreen | 20/20 | REFERENCE_COMPLETE | Contrato, fixture, 54 tests y PR #122 | Scheduler/cola/reloj real, persistencia, escala |
| **TOTAL** | **10 bloques** | **177/177** | **100 % cobertura de referencia declarada** | **383 pruebas globales históricas** | **Integración F13 posterior, no P2 actual** |

**Contabilidad de tests:** B01 9; B02 10; B03 13; B04 30; B05 36; B06 54; B07 56; B08 56; B09 65; B10 54. Suma = 383; la cifra es coherente con el acta B10. La suite B10 descubre todos los archivos test_simulate_*.py, más F13 y Academia, pero no es un ensayo de integración entre salidas de B01–B09 ni un benchmark nativo.

### 2.1 Cadena de dependencias y frontera de autoridad

- B01 población/diplomacia → B02 fundaciones/fronteras → B03 fuerzas/control → B04 recursos/rutas → B05 registro histórico → B06 investigación → B07 fenómenos → B08 riesgos/crisis → B09 necesidades/misiones → B10 arbitraje temporal.
- Esa flecha expresa **dependencia conceptual**, no un pipeline ejecutable completo. B10 trabaja con intenciones de fixture ya aceptadas, no invoca ni certifica los nueve simuladores de dominio.
- **CoreRPG** debe ser el único escritor de WorldState, autoridad de reloj/transacciones/persistencia; **Star Trek** suministra reglas de dominio; **HOST** coordina servicios/sesión/autorizaciones de su ámbito y solicitudes F11 sin reimplementar F11; **UE5** presenta e interactúa; **IA** propone/explica sin escribir hechos. El PADD y las noticias no conocen nada por defecto.
- Canon en época TNG/DS9/VOY y campaña 2383: protección de canon anterior al corte, Primera Directriz, reservas de sujetos extraordinarios y ausencia de avance tecnológico por conveniencia del guion siguen vigentes. No inventar hechos futuros del canon ni una tecnología genérica de viaje temporal.

---

## 3. Hallazgos por prioridad

**Convención:** P0 = bloqueante para conectar producción de forma segura; P1 = defecto o riesgo material que debe sanearse en la referencia; P2 = deuda documental, cobertura o planificación. **[CÓDIGO]** constatado directamente al leer la función; **[CONTRATO/CI]** constatado documentalmente; **[RIESGO]** requiere una prueba nueva y no se afirma como bug reproducido.

### H01 — B02: la fundación no consume obligatoriamente la decisión de elegibilidad [P1, CÓDIGO]

[simulate_colonization_expansion.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_colonization_expansion.py): evaluate_candidate() sí rechaza mundo prewarp/protegido, pero simulate_project() empieza validando los colonos de origen y materializando la colonia sin usar esa decisión ni una prueba externa de derecho de asentamiento. Son dos operaciones públicas separadas. **Impacto:** un consumidor podría llamar directamente a la fundación y saltarse la protección que figura en el plan.

**Corrección:** exigir al crear el proyecto un resultado de elegibilidad vinculante, ligado a campaña, objetivo, autoridad, instante y restricciones medioambientales/Primera Directriz; comprobarlo antes de mover población. No reimplementar la autoridad legal Core. **Prueba:** fundar directamente en mundo prewarp, soberano sin tratado o inaccesible debe fallar atómicamente; el caso autorizado conserva población y derechos.

### H02 — B01: cambios de población sin contabilidad causal de origen/destino [P1, CÓDIGO]

[simulate_civilization_evolution.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_civilization_evolution.py): population_delta se suma/resta al total con límite inferior 0. El validador comprueba no negatividad, **no** exige movimiento emparejado entre origen y destino, hecho de nacimiento/defunción ni conciliación con B02/B08. **Impacto:** se puede duplicar o perder población agregada sin reflejo causal, pese a la regla escrita «population is conserved across movement».

**Corrección:** tipar la clase de delta y requerir fuentes externas emparejadas; distinguir crecimiento vital de migración y pérdidas, con doble entrada y reconciliación interdominio. **Prueba:** un mismo lote de 1.000 migrantes no puede aumentar destino sin disminuir origen ni repetirse tras replay.

### H03 — B03: unidades militares duplicadas pueden pasar el control de identidad [P1, CÓDIGO]

[simulate_conflict_war.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_conflict_war.py): effective_force() suma todas las filas de units; validate_operation() compara conjuntos de unit_id antes/después. **Un mismo unit_id repetido en la lista suma potencia dos veces y los conjuntos ocultan el duplicado**. Tampoco se demuestra por esa comparación la disyunción de identidad entre bandos.

**Corrección:** validar unicidad intraejército e interejércitos *antes* del cálculo, existencia/campaña y estado del inventario de fuerzas del dueño. **Prueba:** duplicar una nave con el mismo ID debe rechazar operación, sin alterar ningún resultado.

### H04 — B03: daño material sin reducción demostrada de potencia futura [P1, CÓDIGO]

En el mismo simulador, resolve_operation() reduce integrity y cambia status, mientras effective_force() pondera combat_power, readiness y logistics e ignora integrity salvo status == destroyed. Una unidad dañada o heavily_damaged puede conservar la misma potencia efectiva en el encuentro siguiente. **Riesgo funcional:** las pérdidas persistentes no repercuten necesariamente en combates posteriores.

**Corrección:** acordar una fórmula o contrato con el sistema táctico/material real; validar cómo daño, averías, reparaciones y tripulación afectan capacidad. **Prueba:** dos operaciones sucesivas con la misma unidad dañada reflejan pérdida objetiva de capacidad, salvo una reparación aceptada.

### H05 — B03: transición de guerra/paz excesivamente permisiva [P1, CÓDIGO]

apply_conflict_event() comprueba que una declaración tenga cadenas cause_refs/war_objective_refs/authority_ref, pero no autentica las referencias; concede ceasefire, armistice o peace_settlement con un booleano en effects sin validar estado anterior, firmantes, tratado ni fecha. **No se acredita con ello una máquina de estados diplomática legal**.

**Corrección:** matriz de transiciones y evidencias aceptadas por dueño jurídico/militar B03/F11/Core, con idempotencia y rechazo de paz sin conflicto o armisticio sin condiciones. **Pruebas:** eventos fuera de secuencia y autoridad inexistente se rechazan; la paz conserva daños, víctimas y obligaciones.

### H06 — B01/B03: posible invasión de autoridad al marcar guerras [P1, CÓDIGO/RIESGO]

En B01, el efecto war_declared puede cambiar directamente la relación a estado de guerra. El diseño reserva la declaración/resolución bélica a B03. **Matiz:** consumir un hecho de guerra **previamente aceptado por B03** es legítimo; lo que no está probado es esa vinculación obligatoria. **Corrección:** admitir sólo referencia validada de B03/Core y proyección B01 de ese hecho; nunca una declaración autónoma B01. **Prueba:** evento B01 sin autorización/commit B03 no altera guerra.

### H07 — B02: independencia reconocida sin validación fuerte de autoridad [P1, CÓDIGO]

En simulate_project(), un efecto independence_recognized puede cambiar governance_status a independent_polity y generar incluso un nuevo polity_ref por defecto. El validador comprueba causa no vacía para el hito, pero no aprobación institucional, jurisdicción ni preexistencia/creación autorizada de la nueva entidad política. **Corrección:** exigir resolución aceptada, sujeto y régimen de creación, trazabilidad B01/LORE y nunca sustituir una ausencia de polity_ref por una autorización implícita. **Prueba:** booleano sin resolución válida debe ser insuficiente.

### H08 — B04: aceptación de transacciones por referencias declaradas, sin titularidad acreditada [P1, CÓDIGO/CONTRATO]

[simulate_living_economy.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_living_economy.py): apply_event() exige authority_ref como texto; _trade() recibe wallet IDs y aceptaciones por texto pero no coteja por sí solo la titularidad/comprobación de poder de cada cuenta o actor. El acta B04 admite esta limitación.

**Corrección:** puerta de transacción que consulte propietario, delegación, consentimiento, saldo/inventario y versión del WorldState; CoreRPG decide/commitea. **Prueba:** intentar pagar con cartera de tercero sin facultades debe fallar.

### H09 — B05: visibilidad histórica confía en grants suministrados por el llamante [P1, CÓDIGO/RIESGO]

[simulate_procedural_history.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_procedural_history.py): visible_history(state, known_ids, at_tick, clearance) filtra IDs, tiempo y clasificación, pero recibe known_ids sin demostrar quién autorizó la adquisición. **No es necesariamente bug de la función de referencia**: exige un productor real de grants con procedencia y audiencia.

**Corrección:** contrato del registro actor-específico de conocimiento, sin aceptar una lista arbitraria de cliente UE5/IA/PADD. **Prueba:** usuario con clasificación suficiente pero sin entrega acreditada no ve el acontecimiento.

### H10 — B06/B07: evidencia científica, sensores y custodia no están autenticados por el runtime [P0 para integración, CONTRATO]

Las [actas B06](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/P2_B06_ACTA_CIERRE_REFERENCIA_20261112.md) y [B07](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/P2_B07_ACTA_CIERRE_REFERENCIA_20261112.md) especifican que los hechos «accepted» son sintéticos. La cadena sensor → observación → aprobación → instalación en nave o excavación/custodia no consume sensores F06, inventarios, autorizaciones ni instalaciones Core reales.

**Corrección futura de F13:** adaptador lector de hechos aceptados y pruebas con dos observadores, discrepancias, autorizaciones, instalación individual y secreto; **no implementar aquí** ni convertir Python en segundo dueño de estado.

### H11 — B08: previsiones de crisis y efectos materiales siguen separados [P0 para integración, CONTRATO]

El evaluador de crisis proyecta exposición, contención y recuperación, pero **deliberadamente no aplica** escasez, víctimas, cambios de ruta, evacuaciones o destrucción. Este diseño de frontera es correcto: el problema sería anunciar que las crisis ya afectan a la galaxia jugable. **Corrección futura:** flujos con B02/B03/B04/B05 y compromisos efectivos de Core, ensayando propagación y rollback.

### H12 — B09: misiones no tienen autoridad de ejecución real [P0 para integración, CONTRATO]

[simulate_emergent_missions.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_emergent_missions.py) valida órdenes, reservas, excepciones de Primera Directriz y reportes **de un fixture**; no firma hechos Core, ejecuta NPC, consume combustible ni asigna misiones de producto. **Corrección futura:** integrar órdenes F11 y sesiones HOST conservando reglas en los dueños, uso de recursos real y comprobación causal al cerrar. Acreditar que NPC resuelve necesidad sin jugador.

### H13 — B10: el scheduler no alimenta ni verifica los motores propietarios [P0 para integración, CÓDIGO/CONTRATO]

[simulate_background_galactic_evolution.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/generation/simulate_background_galactic_evolution.py) valida intenciones externas y emite propuestas PROPOSAL_ONLY. El fixture incluye seis intenciones «accepted» de varios bloques, **no salidas ejecutadas de B01–B09**. No existe despacho real B10 → dueño → transacción Core → recibo → continuidad de mundo.

**Corrección futura:** interfaz de integración tipada por dominio, outbox/inbox durable, reconciliación de versión, idempotencia en cada dueño, reintento/crash recovery y prohibición de doble escritor. **No adelantar este runtime en la remediación actual.**

### H14 — B10: semántica de world_revision a contrastar al migrar [P1, RIESGO]

validate() exige que todos los hechos relevantes del snapshot pertenezcan a la misma world_revision que el estado de B10. Esto es correcto como restricción de fotografía sintética, pero una partida persistente contendrá hechos históricos de múltiples revisiones. **No se ha demostrado** cómo se autentican y proyectan sucesivos hechos sin expulsar los anteriores o depender de reescritura del historial.

**Corrección:** especificar snapshot consistente, token de lectura, historial de origen y política de versionado/migración. **Prueba futura:** reanudar catch-up tras commits y guardados sucesivos; no tratar este punto como bug confirmado de referencia.

### H15 — Ausencia de regresión causal de extremos entre los diez bloques [P1, CONTRATO/CI]

La suite B10 suma 383 tests de diez módulos y F13, pero eso **no demuestra un caso que encadene salidas reales** B01→B02→B03→B04→B05→B06/B07→B08→B09→B10, ni invariantes compartidos sobre los mismos IDs, recursos, épocas y agentes. El escenario B10 usa entradas sintéticas ya declaradas.

**Corrección en P2:** crear pruebas offline de *compatibilidad y trazabilidad* entre contratos, sin simular ejecución de Core inexistente. **Gate:** detectar un evento que duplica población, inventario o unidad militar al cruzar bloques; rechazar información no entregada y retrocesos temporales.

### H16 — Ausencia de pruebas reales de coste, escala y fallos de larga duración [P0 para integración, CONTRATO/CI]

El estado B10 reconoce real_cpu_benchmarks=false y real_offscreen_workers=false. Hay topes de presupuesto/ventana en fixture, pero **no** memoria, CPU, latencia, catch-up de años, millones de IDs, tamaño de save, fairness en largos horizontes, cierres inesperados y reanudación nativa. Un PASS de cuota lógica no equivale a rendimiento real.

**Corrección futura:** presupuesto de rendimiento medible para MSI i9/RTX 4070 y campañas prolongadas, primero simulación nativa sin 3D, luego UE5; no inventar FPS ni costes antes de medir. **Gate:** reproducir años virtuales con consumo acotado y guardado/restauración sin perder trabajo.

### H17 — B01–B03 poseen manifiestos de estado incompatibles con B04–B10 [P2, CÓDIGO/DOCUMENTO]

Los tres primeros tienen summary.complete y runtime_boundary textual, **sin** campos status ni runtime_implemented; B04–B06 usan COMPLETE_REFERENCE y otros campos; B07–B10 usan REFERENCE_COMPLETE, booleano false y evidencia CI más explícita. El plan maestro escribe COMPLETE para B01–B03 aunque sus simuladores sólo son de referencia. **No invalida sus cierres**, pero un agregador puede confundir COMPLETE con integración nativa.

**Corrección:** crear una vista/registro normalizado de madurez documental sin reescribir el pasado; schema version y campos comunes, fuente de verdad y migración para validadores.

### H18 — La documentación histórica muestra muchas «siguientes fases» desfasadas [P2, DOCUMENTO]

[Plan maestro P2](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md) y [README F13](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/fases/F13/README.md) conservan instantáneas fechadas que indican B04, B06, B08 o B10 como siguiente, aunque ahora 10/10 están cerrados a nivel referencia. El propio texto suele advertir que son históricos, pero su lectura aislada puede abrir trabajo duplicado.

**Corrección:** encabezado de estado vivo y enlace único al último manifiesto P2; conservar apéndices históricos sin falsificar fechas. Prohibir «siguiente bloque» sin fecha o corte.

### H19 — Cobertura adversarial desigual en B01–B03 [P1, CI]

B01 tiene 9 tests, B02 10 y B03 13, frente a 30–65 en los bloques modernos. Los casos H01–H07 evidencian que faltan negativos explícitos: fundación por bypass, doble entrada de migrantes, ID militar duplicado, daño/reoperación, paz sin guerra, jurisdicción de independencia y guerra B01 no autorizada. **No se concluye que los tests actuales fallen:** concluye que no ejercitan dichas puertas.

**Corrección:** ampliar primero las pruebas de los tres bloques históricos, con fixture adversarial y CI; no aceptar una revisión basada sólo en pruebas positivas.

### H20 — Evidencia y control de CI deben anclarse al commit exacto [P2, CI]

La PR #122 y sus runs previos/posfusión están documentados. La consulta de runs en main muestra también P2-B08/B09/B10 SUCCESS sobre el commit 8991e5332b70bfdc1999f610560131e82d3b41ff del 18-11-2026; la fotografía main para esta auditoría es 51f8aa... del 19-11. **No se puede afirmar que se haya ejecutado la suite P2 sobre este último SHA sólo por existir runs anteriores.**

**Corrección:** para el cierre posterior a remediación, registrar SHA exacto, test counts, CI relevante del HEAD definitivo y, cuando proceda, posfusión. No exigir que cada modificación puramente documental dispare benchmarks; sí una certificación reproducible del código reparado.

---

## 4. Lo que NO debe interpretarse como un error

1. **B08 no altera inventarios**: por diseño, una previsión no es un daño ni una baja aceptada. Imponer mutaciones directas a B08 sería peor que el límite actual.
2. **B10 no escribe WorldState**: correcto; convertir el scheduler Python en un CoreRPG paralelo sería una regresión arquitectónica.
3. **El jugador no es imprescindible para que sucedan misiones o historia**: principio correcto, documentado y probado de forma sintética; falta demostrarlo en runtime.
4. **La Primera Directriz bloquea la intervención automática** en culturas prewarp: conservar revisión contextual e independencia institucional; no resolverla con un booleano manejado por la IA.
5. **Canon y anomalías especiales no se generan indiscriminadamente**: conservar el agujero de gusano bajorano, Omega y las excepciones narrativas bajo decisión de autor; no abrir viajes temporales jugables.
6. **F13 PLANIFICADA con P2 de referencia completo es coherente**; no marcarla CERRADA para mejorar métricas.
7. **El histórico documental no debe borrarse**: añadir una foto actual de mando en lugar de manipular actas antiguas.

---

## 5. Reconciliación y ruta R0–R7

| Ruta | Trabajo / responsable | Naturaleza | Criterio de salida |
|---|---|---|---|
| **R0** | Fijar informe, SHA, matriz y dueño de cada hallazgo — ChatGPT | Auditoría; ahora | Informe publicado, cero cambios funcionales |
| **R1** | B01–B03: H01–H07 + H19 — conversación P2 + Codex | **Corrección referencia**, no F13 | Nuevas pruebas negativas PASS; conservación, autoridad y estados coherentes |
| **R2** | B04/B05/B09: H08–H09 y contratos de confianza — P2 + Codex | Endurecer límites de referencia | Rechazo de titularidad y conocimiento falsos; sin fingir Core real |
| **R3** | Matriz causal transbloque H15 + H17–H18 — ChatGPT/Codex | Reconciliación + tests offline | Compatibilidad de IDs, canon, recursos, LOD, tiempos y docs viva |
| **R4** | Política de snapshots/revisiones H14 y trazabilidad — P2/arquitectura Core *como propuesta* | Especificación de frontera, sin runtime | Contrato escrito y prueba de referencia con secuencia de revisiones |
| **R5** | Reejecutar suites y CI de HEAD definitivo H20 — Codex + revisión ChatGPT | Certificación de referencia | B01–B10, F13 y Academia sin regresiones; evidencias SHA; acta «REFERENCIA_RECONCILIADA» |
| **R6** | Especificación para futura implementación H10–H13 — coordinación con CoreRPG/HOST/F11/LORE | **Solo traspaso** | Matriz productor/consumidor, autoridad, recibo, fracaso, replay, permisos |
| **R7** | F13/Corrida galáctica real H10–H16 — *fase futura, no autorizada por esta auditoría* | Implementación posterior | Core/HOST/UE5 y pruebas larga duración, rendimiento, save/load, partida real |

**Orden recomendado hoy:** R0 → R1 → R2 → R3 → R4 → R5. Preparar R6 sólo como especificación de frontera; **no ejecutar R7 ahora**. La conversación de Planificación 1 mantiene F13, la de HOST mantiene sus servicios, los Sistemas S01–S19 sus fichas, y LORE sus hechos/canon. No «arreglarlos» unilateralmente desde P2.

### 5.1 Pruebas mínimas de cierre R5

- **B01:** sin creación espontánea de población por migración y sin guerra sin hecho B03.
- **B02:** prohibida fundación prewarp y soberana no autorizada, con reversión íntegra.
- **B03:** IDs militares únicos, daño operativo persistente y transiciones diplomáticas legales.
- **B04:** titularidad real comprobable como precondición de referencia, con transacción no aceptada ante datos ajenos.
- **B05:** ID conocido y clasificado no se revela sin grant auditable.
- **B06:** una investigación no instala automáticamente tecnología en toda la Flota.
- **B07:** ruinas, canon y custodia respetados; observadores disienten sin inventar certeza.
- **B08:** proyección no crea víctimas reales; mitigación exige causa/permiso.
- **B09:** necesidad previa, reserva, orden independiente, resultado acreditado; NPC sin jugador.
- **B10:** prioridad, fairness, cuota, backpressure, reintentos/idempotencia, clock externo, clasificación y revisiones.
- **Transversal:** mismo historial/identidades/recursos en replay y LOD; datos «accepted» del fixture jamás etiquetados como firmas Core.

### 5.2 Evidencia que falta PARA el cierre jugable futuro (no exigible a R5)

- Adaptadores reales para WorldState versionado, autoridad, lectura/escritura transaccional y reconciliación CoreRPG.
- Reloj/catch-up desde el tiempo del juego, con pausas, reinicios, replay y límites de CPU/RAM.
- Corrida galáctica NPC real (producir, viajar, investigar, perder fuerzas, responder a crisis) sin visita del jugador.
- Notificaciones, sensores, mapa/astrometría y PADD con límites de conocimiento y permisos.
- F11/HOST: órdenes y reservas de misión con audiencias/autorizaciones válidas, sin reimplementar sus reglas.
- Guardado/restauración y migraciones de campañas de larga duración.
- Pruebas de estrés, aceptación Unreal, efecto en campañas y evaluación de experiencia.

---

## 6. Dictamen final

**Planificación 2 no necesita otro bloque 11 ni empezar otra «Planificación 2» de implementación.** Está concluida documentalmente como **10/10 bloques de referencia**, con una base técnica real y valiosa. **Lo que necesita ahora es saneamiento puntual** de las lagunas de B01–B03, unificación de autoridad/trazabilidad, pruebas negativas y una matriz interbloque que no confunda diez simuladores independientes con una galaxia operativa.

**Hasta R5:** mantener «REFERENCE_COMPLETE (histórico) / AUDIT_REMEDIATION_OPEN» y no proclamar una nueva certificación. **Después de R5:** cerrar la auditoría de P2 con su acta de reconciliación. **La implementación persistente/jugable** seguirá siendo un trabajo diferente, dependiente de F13/CoreRPG/HOST/UE5, con sus propios criterios de cierre.

**Sin modificación automática de otros proyectos o fases.** Las decisiones de autor se preservan. La hoja de ruta separa inequívocamente reparación y desarrollo futuro.
