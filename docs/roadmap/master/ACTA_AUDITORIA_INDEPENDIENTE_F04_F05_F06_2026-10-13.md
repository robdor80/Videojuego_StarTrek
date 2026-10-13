# Acta de endurecimiento independiente — F04 / F05 / F06 (13-10-2026)

**Objeto:** inspección focalizada y ampliación de la regresión de los componentes de **referencia Python** disponibles, sin nuevas APIs, motor paralelo, mutaciones de estado, cambios de canon ni avance de F07/F08. Esta acta no constituye `CORE_INTEGRADO`, `UE5_JUGABLE` ni cierre de fases.

## Lo que esta rama corrige

| Ámbito | Riesgo verificado por inspección de código | Corrección | Tests de regresión |
| --- | --- | --- | --- |
| F04 autoridad | Valores no booleanos como `appointment_active="yes"` / `acting_command="true"` se trataban como verdaderos | Se exige `is True` para nombramiento y mando interino | `test_command_requires_literal_boolean_evidence` |
| F04 delegación | `now=True` podía tratarse como entero `1` | Ticks/intervalos de delegación deben ser `int` literal | `test_delegation_rejects_boolean_tick_as_integer` |
| F04 actividades | Ventanas temporales booleanas; deuda de fatiga `True`, `NaN` o `inf` como justificación de preempción | Tipo entero estricto, revisión de ventana y deuda finita estrictamente positiva | `test_invalid_boolean_window_is_error_not_valid_time`, `test_preemption_requires_finite_numeric_fatigue_not_boolean` |
| F04→F05 | La revisión booleana del contexto podría coincidir con revisión `1` en un comprobante | Revisión `int` literal | `test_reference_binding_rejects_boolean_world_revision` |
| F05 órdenes | Una aprobación del capitán escrita como `"yes"` era `truthy` y podía suplantar la aprobación positiva | Comparación estricta `is True` | `test_textual_approval_does_not_override_captain` |
| F05 delegación | La cadena `"false"` en `within_delegation_scope` era `truthy` | Comprobar `is True` | `test_textual_delegation_scope_does_not_grant_authority` |
| F05 evidencia | `state_revision=True` podía igualar `1` en comprobante F04 | Comprobar tipo entero real | `test_reference_binding_rejects_boolean_revision_as_one` |
| F06 solicitud | IDs no textuales y timestamps no textuales podían aceptarse o alcanzar rutas de hashing | Identidad y metadatos temporales tipados, rechazo seguro | `test_24_nontext_identifiers_are_blocked_before_hashing`, `test_27_nontext_campaign_time_and_ship_are_blocked` |
| F06 autorización | `state_revision=True` podía igualar `1` en comprobante F05 | Revisión de contexto y comprobante `int` estricta | `test_25_boolean_binding_revision_is_not_integer_one` |
| F06 focalizado | `known_contact_ids` como cadena aceptaba coincidencias de subcadena | Exigir colección de IDs de contacto | `test_26_focused_known_contacts_must_be_a_collection` |

Los **comprobantes de referencia F04/F05 siguen siendo simulados, no credenciales emitidas por Core**. Las revisiones de tipo evitan falsos positivos del harness de pruebas, pero no autentican solicitudes.

## Comprobación del PDF (F06-P01)

Véase [REVISION_ARBOL_MANUAL_P01](fases/F06/REVISION_ARBOL_MANUAL_P01.md): texto de 16 páginas contrastado con el árbol de diez ramas; inspección gráfica únicamente de muestra (portada y p. 14); p. 15 sin contenido textual aparte de cabecera/pie. **No se ha obtenido hash del PDF binario de GitHub ni render integral.** Se conserva P01 `EN_REVISION` sin alterar la fuente editorial.

## Evidencias y pendientes fuera del alcance

- La prueba automatizada de esta rama deberá ejecutarse en la CI existente (F04, F05, F06 y QA transversal) y registrar SHA/resultados antes de sugerir merge.
- **F04:** aún faltan generador persistente de tripulación, vacaciones/bajas simultáneas, horarios multisemana, relevos y autoridad del Core; el fixture Miranda-120 solo prueba una semana y seis estaciones.
- **F05:** una propuesta/orden evaluada en referencia no ejecuta efectos reales; faltan autorización, idempotencia y causalidad autoritativas Core/Host.
- **F06:** Sensores no produce eventos confirmados, informe completado ni guardado de mundo; faltan Core/UE5 y prueba end-to-end, además del PDF.
- **F07:** sigue `PLANIFICADA/PAUSADA`. Ningún cambio de esta rama autoriza reactivarla automáticamente.

**Control de estado:** sin cambios en `docs/roadmap/master/ESTADO_GLOBAL.json`; validar hitos pendientes en sus fases responsables.
