# Planificación 2 — Contratos reforzados y traspaso R6 (19-11-2026)

**Ámbito:** B01–B10, sólo madurez de referencia. **No ejecuta R7 ni implementa F13, CoreRPG, HOST o UE5.**
**Auditoría origen:** [H01–H20](../auditorias/AUDITORIA_PLANIFICACION_2_B01_B10_2026-11-19.md).
**Vista viva de madurez:** [P2_B01_B10_MADUREZ_NORMALIZADA_20261119.json](P2_B01_B10_MADUREZ_NORMALIZADA_20261119.json).
**Cierres 2026-11-12:** históricos, conservados sin reescribir sus resultados originales.

## A. Alcance de la corrección (R1–R5)

1. **B01, H02/H06:** rechazar `population_delta` sin tipo y hecho causal aceptado; migración con débito/crédito emparejados y consumo único de su hecho, pérdidas catastróficas acreditadas; la proyección diplomática de guerra sólo consume un hecho aceptado de B03/Core, nunca declara autónomamente.
2. **B02, H01/H07:** toda fundación consume `settlement_decision` acotada por campaña, civilización, proyecto, mundo, autoridad y revisión; la elegibilidad se calcula **otra vez** (prewarp, acceso, peligros, habitabilidad y derecho de asentamiento). Independencia consume resolución jurisdiccional aceptada y referencia política explícita: ningún `new_polity_ref` implícito.
3. **B03, H03/H04/H05:** identidad única de cada nave en ambos bandos y cotejo de titular/roster en snapshot sintético; daño del casco reduce potencia efectiva en la siguiente operación; máquina de transición con actas, firmantes, tratado, causa, momento y replay idempotente.
4. **B04, H08:** la compraventa coteja delegación del actor, propiedad de los almacenes y carteras, consentimiento por ambas partes, stock, saldos y revisión optimista de la fotografía.
5. **B05, H09:** `known_ids` **no** equivale a conocimiento. Proyección de historia por actor, grant aceptado, fuente anterior, audiencia, caducidad temporal y clearance.
6. **B09:** continuidad de la frontera ya diseñada: intenciones/órdenes del fixture no son ejecución ni autorizaciones reales. No se añade un escritor de misiones.
7. **R3/R4:** validadores offline de ledger interbloque, identidad, contabilidad, causalidad, conocimiento y fotografía multirrevisión; no constituyen adaptadores de producción.
8. **R5:** CI exacta sobre HEAD de PR y posfusión, más acta de resultados reales (sólo cuando estén comprobados).

## B. Modelo de confianza: decisión aceptada no equivale a firma CoreRPG

**Actores y fuentes:** los campos `status: accepted`, `source_domain: CoreRPG`, `authority_ref`, `world_revision` y catálogos `accepted_*` de estas fixtures son **sintéticos**. Los comprobadores Python garantizan estructura, vínculos y coherencia con un catálogo entregado como entrada **pero no autentican su procedencia criptográfica o institucional**.

**Regla futura obligatoria:** CoreRPG es el único escritor de estado, scheduler del tiempo y autoridad de transacciones/guardado. Un *adaptador de sólo lectura* generará contextos con evidencia comprobada; UE5, IA, PADD, HOST y simuladores Python **jamás** podrán fabricar los catálogos de confianza por cuenta propia. HOST sólo gestiona sesiones/servicios conforme a sus contratos; F11 conserva la autoridad de órdenes en su propietario. Ningún hecho se promoverá por una cadena de texto con apariencia de firma.

**Puerta de admisión:** si falta el contexto verificado o una versión actual, se rechaza o queda **REVIEW_REQUIRED / PROPOSAL_ONLY**, sin efectos. La recuperación no está permitida mediante aceptar un booleano de IA ni añadir un permiso por defecto. La Primera Directriz y los derechos de civilizaciones soberanas siguen siendo no eludibles.

## C. Snapshot/revisión/persistencia propuestos (R4; NO implementados)

- **Identidad:** `campaign_id` + `read_token` opaco y exclusivo de una lectura consistente + `read_revision` monotónica + `snapshot_tick` del reloj autorizado CoreRPG. El snapshot debe ser indivisible para las entidades y relaciones consultadas; no combinar vistas de campañas ni de revisiones parciales.
- **Hechos históricos:** conservar `fact_id` estable, `origin_revision` (primera aparición), `version_revision` (última versión), `tick`, `issuer_ref`, estado y audiencia. Una fotografía a revisión N contiene hechos creados en revisiones anteriores (1…N), **sin reescribir todos los hechos a N**. `origin_revision <= version_revision <= read_revision` y `fact.tick <= snapshot_tick`.
- **Optimismo transaccional:** propuesta con `expected_world_revision`, `idempotency_key`, contexto causal y potestad; CoreRPG realiza revalidación atómica justo antes de commit, compara versión y devuelve recibo con `committed_revision`, `fact_ids` y `authority_decision`. **Nunca** convertir una propuesta de B10 en un commit automático.
- **Concurrencia:** si cambia la revisión, no realizar escritura parcial; recuperar nuevo read token, reevaluar elegibilidad, permisos, recursos y reloj, y proponer de nuevo. El mismo `idempotency_key` no debe producir dos consumos.
- **Save/load:** persistir estado, recibos, claves de deduplicación, versión del esquema, reloj, asignaciones y outbox/inbox; restaurar sin duplicación ni pérdida de orden. En migraciones, conservar IDs y revisiones de procedencia. El replay reejecuta **recibos aceptados**, no decisiones estocásticas nuevas.
- **Ramas/LOD/canon:** LOD cercano/lejos/offscreen cambia coste de evaluación y representación, nunca hechos, IDs, titularidad, reloj ni orden causal. El canon sellado no admite reescritura retroactiva y las observaciones clasificadas no se publican por cambio de nivel de detalle.
- **Contrato offline verificable ahora:** `p2_reference_reconciliation.verify_consistent_read`, fixture multirrevisión y negativos de reloj, campaña, duplicación e historia futura. **Sin** demostrar persistencia, recuperación tras crash o rendimiento nativos.

**Advertencia B10/H14:** el validador B10 actual exige revisiones iguales en sus hechos de una sola fotografía sintética; se conserva su semántica y sus 54 tests. El contrato multirrevisión de R4 es **propuesta de interfaz futura**, no una migración silenciosa de B10 ni permiso para cambiar datos históricos.

## D. Matriz R6 de entrega a propietarios futuros (sin ejecutarla)

| Bloque | Produce / consulta (referencia) | Autoridad futura del hecho y comprobación | Fallo / replay |
|---|---|---|---|
| B01 | Demografía, gobierno, relaciones; hechos de guerra consumidos | CoreRPG + reglas del dominio B01; guerras aceptadas por B03; B02/B08 para transferencias/pérdidas | Rechazar migración sin doble asiento y duplicación de fact |
| B02 | Elegibilidad, fundación, derechos, frontera, independencia | CoreRPG + F11/autoridad jurídica correspondiente; B01 proyecta polity | Negar prewarp, soberano sin tratado, control implícito y cambio de jurisdicción |
| B03 | Fuerzas, daño, conflicto, armisticio, paz | Registro de inventario y autoridad militar/jurídica de Core + dueño B03/F11 | Rechazar roster duplicado, unidad ajena, transición ilícita, replay |
| B04 | Stores, carteras, rutas, transacciones y envíos | Core valida propietario, poderes, saldo, ruta, revisión y commit indivisible | CAS/revisión, rollback, recibo único |
| B05 | Registro histórico y entregas de conocimiento | Core registra hechos y grants actor-específicos; B05 sólo propone historial | Sin grant no ver ni en PADD ni en UI ni para IA |
| B06 | Observación, descubrimiento, prototipo/instalación | F06 sensores; Core instrumentos, permisos, casco concreto y hechos aceptados | Dos observadores, contradicción, ensayo fallido sin instalar tecnología global |
| B07 | Fenómenos, ruinas, custodia y prohibiciones | F06 sensores + Core inventarios, custodia, acceso y canon/LORE | Observación ≠ certeza, acceso no autorizado denegado |
| B08 | Riesgo/mitigación como **pronóstico**, no víctimas reales | B02/B03/B04/Core aplican consecuencias sólo por hechos separados | Crisis prevista jamás crea pérdidas por sí sola |
| B09 | Necesidad→candidato→reserva/orden→resultado | Core y F11/HOST según contratos propios, recursos e identidades NPC | Necesidad real, autorización, no ordenar dos veces; NPC actúa sin jugador |
| B10 | Priorizar propuestas y presupuestos temporales | **CoreRPG** reloj, cola durable, commit, replay; B10 no escribe WorldState | Backpressure, fairness, retry, crash recovery con idempotencia |

### Interfaz futura mínima (F13, propietario externo)

**Entrada:** snapshot CoreRPG validado + token/revisión + reloj + facts/grants según permisos + intents de dominios por dueños. **Salida B10:** `PROPOSAL_ONLY`, `dispatch_id` y causa. **Aceptación:** dueño del dominio verifica la propuesta; Core ejecuta transacción con CAS y emite recibo durable aceptado/rechazado. **Difusión:** HOST/UE5/PADD/IA sólo ven proyecciones autorizadas, nunca el archivo de hechos completo. **Replay:** leer journal/receipts Core, deduplicar, restaurar cola y tiempo sin re-generar hechos. **Fallo:** revisión stale, permisos nulos, falta de stock, mundo protegido, crash o TTL vencido → rechazo reintentable o revisión humana, no escritura silenciosa.

### Puertas de aceptación futuras, NO exigibles para cerrar P2

1. Casos Core→B01–B09→B10→Core con hechos reales y transacciones atómicas.
2. Orden F11/HOST, reserva, consumo y resultado de NPC independientes del jugador.
3. Sensor F06 real, discrepancia, secreto y custodia B06–B07.
4. Campañas con snapshots y commits de varias revisiones, save/load y crash recovery.
5. Estrés CPU/RAM y memoria de campañas largas, cuotas y fairness en MSI + aceptación en Unreal.
6. Cambios sugeridos a Planificación 1/F13, HOST, LORE y S01–S19 sólo como **traspaso**, a tratar por sus conversaciones propietarias.

## E. Criterio para cerrar el saneamiento P2

Se podrá escribir **REFERENCIA_RECONCILIADA** cuando la suite nueva y la histórica B01–B10, F13 y Academia pasen sobre el **mismo HEAD de PR**, la CI esté verde, no queden defectos conocidos de referencia y haya un acta con commits/resultados exactos. Sigue significando **sólo contratos, simuladores, fixtures, validadores y pruebas offline**. La integración real seguirá abierta en F13/R7.
