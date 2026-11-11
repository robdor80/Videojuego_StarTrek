# F11-P01 — Escalafón, jerarquía y cadena de mando (v1 de diseño)

**Fecha:** 11-11-2026. **Estado:** borrador técnico verificable para revisión; NO IMPLEMENTADO en CoreRPG/UE5.
**Fase F11:** esta entrega es solo P01 del [plan actualizado](PLAN_F11_ACTUALIZADO_2026-11-11.md). Las oportunidades garantizadas de promoción y sucesión se ejecutarán en P03/P04, no se simulan aquí.
**Norma superior:** una carrera que conduce, si el jugador elige seguirla, a capitanear la USS Enterprise NCC-1701-D modernizada; sin ascensos inmerecidos ni bloqueos interminables por vacantes.

## 1. Separación de conceptos (invariante)

La ficha del personaje conserva campos **independientes**: `rank`, `division`, `department`, `position(s)`, `assignment`, `duty_station`; adicionalmente, `qualifications`, `medical_duty_status`, `duty/watch`, `permissions`, `orders`, `delegations` y `effective_command`. Se reutiliza `proyecto/docs/decisions/personnel_model.md`; no introducir un atributo único de «nivel de mando».

- **Rango:** grado permanente y precedencia militar, útil para candidatos/antigüedad, pero sin conceder por sí solo control del puente, permisos de computadora o capacidad de nombrar oficiales.
- **División:** Mando, Operaciones o Ciencias; no equivale a departamento ni cualificación.
- **Departamento:** Ciencia, Ingeniería, Seguridad, Medicina, Operaciones, etc.
- **Puesto:** función formal, p. ej. `chief_engineering_officer`, `first_officer` o `commanding_officer`. Puede compatibilizarse con otra función si está autorizado.
- **Destino:** nave, estación, Academia u otra unidad; condiciona el ámbito de la autoridad.
- **Estación de guardia:** consola/puesto operativo usado durante turno; no confiere más autoridad que la asignación vigente.
- **Cualificación:** acreditación independiente de rango, incluida `command_qualified`.
- **Mando efectivo:** resultado contextual y temporal de un nombramiento, una guardia, una sucesión o una delegación válida.

Un **comandante jefe de Ingeniería** sigue siendo comandante y jefe de Ingeniería al ascender de rango; no pasa a primer oficial hasta que exista plaza, acto de nombramiento y relevo formal.

## 2. Escalafón jugable

| ID contractual existente | Denominación | Insignia del proyecto | Función esperable, no privilegio automático |
|---|---|---|---|
| `ensign` | Alférez | ● | Servicio supervisado y guardias con atribuciones |
| `lieutenant_junior_grade` | Teniente júnior / grado inferior | ●○ | Mayor autonomía, tutorías y guardias habilitadas |
| `lieutenant` | Teniente | ●● | Oficial experimentado, responsabilidad y supervisión |
| `lieutenant_commander` | Teniente comandante | ●●○ | Candidato habitual a jefatura departamental |
| `commander` | Comandante | ●●● | Puede dirigir departamento o ser primer oficial si es nombrado |
| `captain` | Capitán | ●●●● | Grado compatible con un mando permanente, no la concesión de una nave |

El estatus de **cadete** no es parte del escalafón de oficiales comisionados. Personal alistado/suboficial tiene su propia escala. Comodoro y almirantes se conservan según `universal_rank_insignia.md`; la codificación visual de comodoro es una GAME_ADDITION, no un mandato narrativo de progresión normal. No se exige al jugador continuar más allá de capitán.

**Regla para ofertas:** rango requerido, cualificación, plaza libre y autoridad que nombra se validan por separado. La distinción entre rango de capitán y ocupar el puesto `commanding_officer` se aplica también a NPC.

## 3. Ámbitos de decisión y límites

| Ámbito | Titular habitual | Límite importante |
|---|---|---|
| Política de misión, alerta y mando integral de nave | Oficial al mando legal | Órdenes superiores, normas, aptitud, capacidad material |
| Coordinación general, guardias, implementación de órdenes | Primer oficial | No sustituye al capitán permanente sin habilitación |
| Organización interna y prioridades técnicas | Jefe de departamento | Limitadas al departamento y a política/recursos asignados |
| Ejecución de consola de servicio | Oficial de guardia cualificado | Solo en su ventana y estación/orden |
| Determinación profesional de aptitud médica | Oficial médico competente | No recibe por ello el mando de la nave |
| Promoción, plaza y nombramiento de primer oficial/capitán | Autoridad de personal competente de Flota o facultad delegada verificable | Recomendación del capitán ≠ orden de nombramiento |
| Propuesta narrativa, táctica o administrativa | IA/Computadora | Puede explicar/recomendar; no concede rango, poder ni acceso |

En una emergencia se puede actuar con autonomía **dentro** de órdenes, competencias y límites aplicables. No interpretar que todo lo extraordinario concede una excepción universal.

El comandante con rango más alto a bordo **no** desplaza automáticamente al capitán legítimo. Un médico puede apartar del servicio a un oficial declarado no apto en su ámbito; la **sucesión de mando**, no la medicina, selecciona al sustituto.

## 4. Cadena de mando por destino

La fuente existente es `mundo/lore/federation/starfleet/command_structure/succession_rules.json`:

`commanding_officer → first_officer → second_officer → designated_qualified_successor`.

Se resuelve por **unidad**, **instante**, **alcance** y **causa de indisponibilidad**. Un titular incapacitado, ausente sin delegación o relevado legalmente activa evaluación de sucesión; una mera presencia del XO no sustituye automáticamente al CO.

Precondiciones mínimas: identidad del sucesor, destino en la misma unidad, puesto reconocido o designación válida, cualificación de mando según época/función, aptitud médica, disponibilidad, órdenes/registro de guardia y ausencia de revocación o designación preferente superior.

**Sustitución temporal**: evento de inicio con causa + alcance + identificador de mandato + instante + revisión; evento de fin con retorno del titular, relevo o nuevo nombramiento. No modifica rango, especialidad, destino permanente ni convierte al sustituto en capitán de grado. Si nadie es elegible, la política es `REQUIRES_AUTHORIZED_RESOLUTION`, no elegir por azar.

**Mando de guardia** no es lo mismo que comandante permanente. Un oficial competente puede dirigir la guardia y reportar al capitán; las decisiones reservadas al CO se escalan si exceden órdenes permanentes.

## 5. Delegación, órdenes y caducidad

Reutilizar `command_decision_delegation_state_v0.1.json`, `captain_operational_decision_authority_contract_v0.1.json`, F04-P03 y F05.

Tres modos compatibles: `manual`, `proposal_requires_approval`, `delegated_autonomous`. Se almacena quién delega, a quién, dominio, limitaciones, fuente/orden, `effective_at`, `expires_at`, `revoked_at` y revisión. Una delegación no concede una capacidad fuera del poder del concedente.

Toda evaluación de una acción mutadora verifica su **vigencia en el instante de ejecución**, no únicamente cuando el NPC o IA la propuso. Cambios de guardia, revisión del World State, orden superior o revocación invalidan las propuestas anteriormente autorizables.

El capitán puede aceptar, modificar, delegar o rechazar propuestas dentro de sus competencias; jamás se le reemplaza silenciosamente su decisión porque una IA prefiera otra solución.

## 6. Resolución autorizativa: contrato de entrada y salida

**Entrada conceptual** (no representa una API implementada):

`actor_id, unit_id, action_id, decision_domain, evaluation_time, world_revision, actor_rank, actor_positions, actor_assignment, duty_window, duty_station, qualifications, medical_status, valid_orders, active_delegations, succession_state, professional_scope, resources_and_safety_constraints`.

Estos campos son **referencias a hechos verificados por Host/Core**, no booleans o textos inventados por el cliente. Una aplicación web, el PADD, un archivo JSON o una respuesta de IA no son fuentes de autoridad.

**Salida de referencia:** `ALLOW_REFERENCE`, `DENY_REFERENCE` o `REVIEW_REQUIRED`, con `reason_codes`, límites y procedencia. Ninguna salida de P01 equivale a una autorización efectiva. Solo Core/Host, con revisión actual y evento auditado, podrá ejecutar la operación correspondiente.

Orden conceptual de comprobación:
1. Validez de identidad, revisión y origen del contexto; faltan pruebas → negar.
2. Pertenencia a destino/ámbito; aptitud y cualificaciones.
3. Puesto titular, sucesión o delegación formal vigente para el dominio solicitado.
4. Guardia y estación cuando se exige servicio efectivo.
5. Órdenes superiores, competencias profesionales, reglas duras de seguridad y recursos.
6. Concesión delimitada o denegación con razones; revalidación y registro antes de mutar.

**No confundir acceso a información con autoridad para ordenar:** incluso un capitán consulta datos conforme a su conocimiento adquirido y permisos. El PADD externo nunca recibe secretos solo por el rango.

## 7. Casos de aceptación de P01

| ID | Situación | Resultado esperado |
|---|---|---|
| A01 | Alférez de Sensores en guardia, formado, pide lectura ordinaria de su consola | Elegible en ese dominio |
| A02 | Ese alférez intenta modificar el destino de la nave | Denegar salvo orden/delegación explícita válida |
| A03 | Teniente comandante jefe de Ingeniería asigna trabajo técnico a su equipo | Elegible dentro de su departamento |
| A04 | Ese jefe cambia unilateralmente una misión diplomática | Denegar |
| A05 | Comandante con mayor rango que el XO pretende ocupar la plaza de XO sin nombramiento | Denegar |
| A06 | XO asume mando temporal tras incapacidad verificada del CO, apto y cualificado | Elegible dentro de la ventana de sucesión |
| A07 | Vuelve el CO válido; XO continúa ordenando como CO por la sucesión ya cerrada | Denegar |
| A08 | CO delega planificación de guardias con plazo y dominio concreto | Elegible dentro de límites |
| A09 | Delegación revocada o vencida ejecuta una propuesta antigua | Denegar |
| A10 | Oficial médico competente declara CO no apto por razón clínica legítima | Restringir servicio; sucesión separada |
| A11 | Médico sin puesto de mando intenta tomar control permanente por su dictamen | Denegar |
| A12 | Capitán ordena activar recurso inexistente | Denegar ejecución material |
| A13 | IA recomienda promover a comandante a XO con plaza ocupada | No mutar; solo proponer revisión |
| A14 | Capitán recomienda a su sucesor sin facultad formal de nombrar | La recomendación no cambia la plaza |
| A15 | Un NPC recibe promoción y traslado; todavía no se produjo relevo | Conserva su puesto hasta orden/efecto |
| A16 | Actor alega una orden de Flota sin prueba verificable | Denegar por falta de evidencia |
| A17 | Oficial cualificado manda temporalmente una guardia, sin ser capitán de grado | Permitido en el alcance de guardia; rango intacto |
| A18 | Capitán intenta consultar datos clasificados desconocidos sin permiso aplicable | No revelar información |
| A19 | Nueva revisión de mundo entre propuesta y ejecución | Revalidar; no ejecutar decisión obsoleta |
| A20 | Médico competente, por dictamen de aptitud, ordena cambio de objetivo de misión | No autorizado fuera de su ámbito |

Son **escenarios de especificación**, no pruebas de runtime ya ejecutadas. Los fixtures/contratos de referencia permitirán automatizarlos; las puertas reales requieren pruebas de integración.

## 8. Vínculo con la progresión garantizada

P01 no fabrica promociones. Define el límite que impide que la garantía de progresión de P03/P04 altere retrospectivamente hechos del mundo:

- El planificador puede preparar oferta a un NPC actual primer oficial para que pase a capitán de **otra nave**.
- Debe existir dicha oportunidad y registrarse su aceptación/orden y su fecha efectiva.
- Solo entonces queda vacante `first_officer` en la Enterprise-D y puede iniciarse una propuesta/selección para el jugador.
- El capitán puede recomendar a un candidato y, **solo si la política efectiva le concede esa facultad**, efectuar el nombramiento; en otro caso, lo valida el Mando de Flota.
- Si una ruta falla, se prepara otra verosímil; nunca una usurpación por decreto técnico.

La dirección narrativa puede garantizar la futura oportunidad, no falsificar las autorizaciones del presente.

## 9. Propiedad y alcance de implementación

| Propiedad | Dueño |
|---|---|
| Rangos/puestos/jerarquía Starfleet, criterios de vacantes, reglas por unidad | Contenido y reglas Star Trek |
| Identidad/tiempo/revisión/eventos/persistencia y validación definitiva | CoreRPG/Host |
| Consola, conversación, interfaz, ceremonia, presentación de órdenes | UE5 |
| Variación de diálogo y sugerencias | IA sin facultad mutadora |
| Preparación causal de ascensos y traslados | F11-P03/P04 (planificador) con eventos Core confirmados |

**Aceptación actual:** este documento + contrato de referencia coherente con F04/F05. **No se declara** CoreRPG integrado, jugabilidad UE5, garantía ya ejecutada ni F11 cerrada. Deben realizarse pruebas positivas/negativas y de persistencia real más adelante, con SHAs y evidencias.
