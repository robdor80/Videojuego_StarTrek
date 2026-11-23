# F11-P02 — Destinos, departamentos, puestos y ofertas (v1)

**Fecha:** 11-11-2026 · **Madurez de esta entrega:** diseño + referencia offline; NO Core/Host/UE5 jugable.
**Origen:** [plan autoral F11](PLAN_F11_ACTUALIZADO_2026-11-11.md) y [P01: jerarquía](F11-P01_JERARQUIA_CADENA_MANDO_V1.md).

## 1. Qué significa un destino

Un personaje tiene **un destino orgánico principal** (`assignment/unit`), un **puesto profesional** (`position`), una **especialidad** (`department`), **posibles funciones temporales** de guardia y un **expediente persistente**. Moverse de consola no es un traslado; ascender de grado no sustituye un nombramiento; ser segundo oficial no cancela automáticamente otra responsabilidad departamental si ambas están autorizadas.

Un destino puede ser una **nave, estación espacial, base estelar o Academia**. Las normas del servicio activo derivan del estado real de la unidad y de una orden emitida por autoridad competente. El objetivo personal es la **Enterprise NCC-1701-D modernizada** y su capitanía; la aspiración no implica que desde el inicio exista una plaza libre ni autoriza a inventarla.

### Diferenciar plaza, puesto y persona

- **Puesto/Perfil profesional**: jefe científico, primer oficial, médico, oficial de sensores, etc. Es un tipo reutilizable con requisitos y dependencia funcional.
- **Plaza (billet)**: identidad **única y estable dentro de una unidad concreta**; existe antes de ser ocupada y perdura después de un traslado. F04 ya tiene un grafo autoritativo de plazas en Core. P02 no inventa copias paralelas de ellas.
- **Persona**: NPC o jugador con `character_id`, historial, aptitudes y destino; cambia de plaza sin perder identidad o relaciones.
- **Función de guardia**: tarea temporal (por ejemplo, operar Sensores); no es por sí misma otro puesto permanente.

No sustituir el `f04_department_id` numérico de las plantillas F04 por las etiquetas de especialidad del lore de Starfleet. Son dos granularidades distintas y ambas se conservan.

## 2. Las siete grandes áreas de las naves (F04)

| Grupo P02 | ID de F04 | Ejemplos de departamentos/especialidades |
|---|---:|---|
| Ciencias y Sensores | 1 | Ciencias, astrometría, sensores |
| Ingeniería y mantenimiento | 2 | Propulsión, energía, reparaciones |
| Mando y navegación | 3 | Capitán, primer/segundo oficial, timón |
| Medicina | 4 | Enfermería, médicos, consejería |
| Operaciones y comunicaciones | 5 | Sistemas, transporte, comunicaciones, inteligencia |
| Seguridad y táctica | 6 | Seguridad interior, armas, escudos |
| Lanzaderas y logística | 7 | Pilotos, carga, suministros, hangar |

El **catálogo de referencia** incorpora 14 puestos ya presentes en `mundo/lore/federation/starfleet/positions/positions.json` y 9 perfiles operativos junior identificados como **funciones de referencia** (todavía no equivalen a nuevos `position_id` autorizados en Core). Cada uno define banda orientativa de rangos, capacitación y dependencia jerárquica. No se inventa la plantilla ni el número de plazas de la Enterprise-D.

**Ejemplo:** un teniente puede supervisar personal especializado; un teniente comandante o comandante puede optar a una jefatura. Los requisitos concretos pertenecen a **la plaza real** de esa nave y prevalecen sobre preferencias generales del catálogo. Un oficial con rango superior no salta las cualificaciones.

## 3. Estados de plazas: no confundir proyecto con realidad

| Estado | Significado | ¿Puede ofrecerse como vacante efectiva? |
|---|---|---|
| `occupied` | Un tripulante ocupa la plaza | **No** |
| `planned` | Se prepara un relevo futuro; el titular continúa | **No** |
| `reserved` | Plaza separada para un proceso ya autorizado | No para ofertas generales |
| `vacant` | Plaza realmente libre y habilitada | **Sí, tras comprobaciones** |
| `suspended` | Plaza temporalmente deshabilitada | No |
| `decommissioned` | Plaza retirada de servicio | No |

**Caso aprobado:** el primer oficial de la Enterprise-D aspira a capitán. Su candidatura y el eventual traslado pueden aparecer como `planned`, pero su plaza seguirá `occupied` en el mundo real hasta que exista orden, relevo y efecto autoritativo. El planificador P03/P04 preparará esa oportunidad **sin mentirle al sistema de plazas**.

En los documentos narrativos se puede hablar de «vacante prevista». En el motor NO equivale a `vacant`.

## 4. Cómo se asignará el primer destino y cómo se solicita un cambio

1. Una graduación acreditada puede conducir a una **comisión como alférez**, pero el mero cuarto año aprobado no crea destino.
2. Flota examina necesidades del servicio, perfiles, unidades operativas, plazas efectivas, capacidades, méritos y preferencias del personaje.
3. El **cribado** identifica candidaturas posibles. No crea nuevos tripulantes, plazas, destinos ni órdenes.
4. Una autoridad competente **emite oferta** con titular, unidad, plaza, plazo, revisión y causa.
5. El jugador la acepta o rechaza. **Aceptar no transfiere** el destino todavía.
6. La autoridad correspondiente emite **orden formal** y Core debe comprobar nuevamente plaza libre, identidad, cualificación, fecha y revisión antes de aplicar en una operación atómica el cese/incorporación.
7. Se mantienen expediente, relaciones, histórico de puestos, compañeros, antigüedad y efectos sociales. Se regeneran guardias y se aplica relevo, sin duplicar tripulantes.

### Formas de cambio

- **Primer destino** tras comisión.
- **Cambio de puesto dentro de una misma unidad**, con cargo y responsabilidad nueva, incluso manteniendo el rango.
- **Traslado a otra nave/base**, a petición propia o por necesidades del servicio.
- **Comisión temporal**, conservando la adscripción original cuando una orden válida lo establezca; no equivale a abandonar la plaza de origen.
- **Ascenso sin traslado** o **traslado sin ascenso**.
- **Reorientación profesional**, si existe formación/cualificación y autorización; los años en Ingeniería no otorgan automáticamente un puesto médico.

Las solicitudes informales pueden registrarse sin plaza libre; las **ofertas efectivas** y órdenes requieren vacante real y expediente válido.

## 5. Oferta profesional: ciclo de vida propuesto

`draft → screened → offered → accepted → orders_issued → effective`.

Alternativas auditables: `declined`, `withdrawn`, `expired`, `cancelled`. Cada transición registra actor, autoridad, causa, ventana temporal y revisión. `accepted` **no** cambia aún `current_assignment`, `current_position` ni `occupant_id`.

Cuando dos aspirantes compiten por la misma plaza, el primer expediente en llegar a Core no obtiene un derecho arbitrario: se requiere resolución/selección de Flota. Tras la selección, **una sola orden** podrá convertirse en nombramiento efectivo, usando comprobaciones y revisión de estado atómica. La detección de versiones obsoletas evita que la aceptación tardía de otro candidato duplique el puesto.

En P02 el cribado es deliberadamente **solo de referencia**. Las entradas JSON `verified` son simulaciones; jamás sustituyen la autenticación CoreRPG/Host.

## 6. Reglas del catálogo de 23 perfiles

- **14 puestos formales** reutilizan identificadores existentes; el catálogo NO redefine su autoridad operativa (F11-P01).
- **9 funciones especializadas** (Ciencias, Sensores, Ingeniería, Seguridad, Táctica, Medicina, Lanzaderas, Logística y Guardia de Puente) no se declaran puestos formales existentes, solo tipos de servicio para cartografiar más adelante sobre plazas F04.
- `accepted_ranks` son requisitos de diseño de **los perfiles**, no correspondencias canónicas rígidas de cada nave. Las plazas reales pueden ser más restrictivas.
- `required_qualifications` son **referencias a cualificaciones** que deben existir/verificarse en Core/Host; el contrato no concede certificados ni entrena al personaje.
- Un ascenso no produce una jefatura ni un destino por sí mismo; un cambio de puesto tampoco concede un grado.
- El oficial supervisor debe ser **un cargo ocupado por otra identidad adecuada**, no una relación inventada por el usuario.
- Una misma persona puede simultanear **funciones** compatibles si está habilitada, pero no puede ocupar dos plazas permanentes incompatibles ni duplicar una persona entre dos unidades.
- La disponibilidad temporal de una clase y una nave concreta se verifican separadamente. Referencias históricas a nueva clase Valhalla **no** activan una nave ni fuerzan su disponibilidad.

## 7. Alcance actual y referencias reales

**Herramienta:** `desarrollo/tools/validation/f11_p02_assignments_reference.py`. Criba perfiles, unidades, plazas y operaciones de oferta a partir de una instantánea ficticia, sin mutar el mundo. El `test_f11_p02_assignments_reference.py` debe cubrir negativos (ocupado, previsto, reservado, rango, título, certificados, destitución implícita, unidad fuera de época, duplicación, orden no válida, revisión caducada) y positivos (primer destino, cambios, oferta, renuncia, relevo).

**Conservar:** `sistemas/gameplay/careers/assignments/assignment_transition.json`, `academy_path/first_assignment_model.json`, `sistemas/gameplay/careers/service_record/`, `mundo/lore/federation/starfleet/assignments/transfer_model.json`, `sistemas/gameplay/chain_of_command/`, F04 (dotaciones), F05 (órdenes), F10 (graduación).

**Frontera:** CoreRPG tiene la única verdad de plazas/personas/vacantes/tiempo/órdenes; las siete categorías y perfiles son semántica Trek; Unreal representa los destinos y comunicaciones; IA puede proponer narrativas pero no concede plazas ni rangos.

## 8. Lo que queda para P03 y P04

P02 **no garantiza todavía la promoción** ni crea vacantes. Expone una diferencia que necesita P03/P04: «no hay plaza hoy» **no** significa «nunca habrá plaza». El director de oportunidades preparará con antelación eventos verosímiles de NPC hasta que una plaza realmente quede vacante, y entonces P02 permite verificar la candidatura y emitir la oferta correspondiente.

Debe poder demostrarse en campaña que el jugador que sigue la ruta de mando consigue **oportunidades repetibles y coherentes** de ser teniente, jefe de departamento, comandante, primer oficial, capitán en otra nave y finalmente capitán de la Enterprise-D, sin muertes/decretos artificiosos. Se implementará y probará después, no se considera satisfecho por el catálogo P02.

## 9. Puerta de aceptación P02

- [ ] Contrato catálogo con grupos F04 sin conflictos de identidad, jerarquía o cifras.
- [ ] Cribado referencia de primer destino/cambio/traslado con entradas verificables conceptuales.
- [ ] Denegaciones y diferimiento de plazas ocupadas/planificadas; no vacantes ficticias.
- [ ] Máquina de estados de oferta sin mutar hasta orden y revalidación.
- [ ] Suite CI verde de pruebas P02 y regresión F11-P01/existente.
- [ ] Declaración expresa de **referencia solamente**, no Core ni UE5; F11 no cerrada.
