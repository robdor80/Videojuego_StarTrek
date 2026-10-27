# F04-P03 — Autoridad por destino, guardia, nombramiento y sustitución (11-10-2026)

**Fuentes:** `mundo/lore/federation/starfleet/positions/positions.json`; `command_structure/succession_rules.json`; `qualifications/command_qualification.json`; `sistemas/gameplay/chain_of_command/captain_operational_decision_authority_contract_v0.1.json`; `sistemas/gameplay/duty_system/duty_assignment_model.json`; `sistemas/gameplay/orders/`.

## Regla de autorización

`rango ≠ destino ≠ puesto ≠ cualificación ≠ habilitación de consola ≠ autoridad vigente`.

Decidir a partir de identidad/destino, ventana de guardia, nombramientos formales, cualificaciones, estado médico, cadena de sucesión, dominio de decisión, órdenes externas válidas, delegaciones vigentes y estado real de sistemas. Ante datos incompletos → **rechazar o solicitar aclaración, sin elevar privilegios**.

| Actor | Permitido por defecto | No permitido por mera graduación/rango |
|---|---|---|
| Alférez de Sensores, de guardia | Operar sensores dentro de cualificación y controles; reportar a puente | Cambiar guardias, misión o diplomacia, comandar la nave |
| Jefe departamental | Organizar deberes y emitir instrucciones **en su departamento**, dentro de órdenes y competencias | Apropiarse de poderes del capitán sobre misión/nave |
| Oficial de guardia del puente | Ejecutar guardia, tareas de navegación/alerta delegadas, reportar y decidir dentro de órdenes permanentes | Sustituir indefinidamente al capitán ni asumir todos sus dominios |
| Oficial al mando legal (sea NPC/jugador) | Revisar/aceptar/modificar decisiones propias, delegar, revocar y emitir órdenes lícitas | Crear recursos, ignorar limitaciones físicas, médica o normativas por ser capitán |

## Sucesión y delegación

1. **Mando permanente:** cargo `commanding_officer` vinculado a destino; un mero rango superior a bordo no lo suplanta.
2. **Mando de guardia:** autoridad operativa temporal; permanece el titular del mando de la nave.
3. **Sucesión:** titular indisponible → primer oficial → segundo oficial → sucesor designado **cualificado**, con registro del motivo, comienzo, alcance y cese. No cambia el rango permanente.
4. **Delegación:** referencia al titular, receptor, dominio, ventana, estado y límites explícitos; revocación/caducidad detiene autorizaciones futuras. La delegación no puede extenderse más allá del poder de origen.
5. **Modos:** `manual` nunca ejecuta política reservada sin aprobación; `proposal_requires_approval` exige acto positivo; `delegated_autonomous` admite ejecución rutinaria dentro de órdenes permanentes. La propuesta IA/XO no es permiso.
6. **Orden superior:** si es válida y aplicable, constriñe decisión de misión; una decisión conflictiva registra desobediencia/disputa y consecuencias, no altera la orden superior en silencio.
7. **Auditoría:** registrar actor, rol efectivo, intervalo, origen, norma, orden, recursos, autorización/denegación, razón y referencia causal. Retrasar una respuesta IA requiere revalidar autoridad al ejecutarla.

## Fronteras

CoreRPG aporta checks de actor/acción/tiempo y eventos genéricos **cuando existan**; Star Trek determina puestos y la matriz normativa; UE5 muestra mando/estaciones; IA no concede permisos. **No** se define aquí una API universal ni se anticipa F05 (gestión completa de órdenes e iniciativa). Pruebas de P05 verifican cambios de rol, caducidad y denegaciones por rango solo.
