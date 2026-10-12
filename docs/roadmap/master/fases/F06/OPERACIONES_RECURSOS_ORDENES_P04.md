# F06-P04 — Matriz operación → autoridad → recurso → resultado

**Regla fundamental:** visualizar una función en los diez menús no implica que pueda ejecutarse. Las cifras de potencia de la referencia **NO SON CANON**: son umbrales de test configurables y deben negociarse con el balance de Core/Star Trek.

## Puertas comunes (orden de evaluación)
1. Orden o acción intencionada, operador e identidad de nave/estación identificados.
2. Validación **externa** de autoridad, cargo, guardia y ocupación real del puesto (F04/F05/Core); un rango alto por sí solo no concede el uso.
3. Existencia de capacidad en la clase de nave, matriz operativa, potencia disponible y límites del equipo.
4. Objetivo previamente conocido cuando la operación requiere contacto (no consultar IDs ocultos).
5. Reserva y cola atómicas en Core, con duración, idempotencia, cancelación y resultado. La referencia actual **no reserva**.
6. Registro de hechos confirmados, dossier de observaciones y comunicación conforme al canal autorizado.

## Matriz por familia (primera integración)
| Menú / operación | Insumo/autorización | Recurso / tiempo | Bloqueo o fracaso | Responsable y estado |
| --- | --- | --- | --- | --- |
| Estado / consultar matrices | Personal con acceso al puesto | Consulta ligera | Acceso denegado; datos degradados | Core + UI, **pendiente** |
| Barrido corto | Operador autorizado, matriz operativa | Potencia + segundos de barrido | Equipo fuera de servicio; firma no observable | Motor actual + wrapper **referencia** |
| Barrido largo | Operador autorizado y capacidad largo alcance | Mayor exigencia relativa que corto | Potencia insuficiente, interferencia, mal sector | Motor + wrapper **referencia** |
| Barrido focalizado | Contacto conocido y capacidad focal | Potencia/tiempo + selección objetivo | Contacto ausente; sin firma observable | Wrapper **referencia**, foco nativo Core pendiente |
| Búsqueda/localización por tipo | Criterio y ámbito explícitos | Barrido repetido/cola dependiente nave | Falsos negativos, insuficiente sensibilidad | Star Trek/Core **pendiente** |
| Contactos / listar y marcar | Visibilidad de dossier | Memoria y permisos | Contacto inaccesible o perdido | Ship memory Core **pendiente** |
| Seguimiento / recuperar | Contacto reconocido, capacidad tracking | Cuota de pistas y tiempo continuo | Saturación, pérdida/interferencia | Scheduler Core **pendiente** |
| Lectura / medir | Contacto o resultado existente | Resolución/matriz | Ausencia de datos, baja confianza | Readout **parcial** por motor |
| Interferencia / compensación | Configuración permitida y banda | Potencia, tiempo, posible trade-off | Matriz incompatible o compensación ineficaz | Motor de compensación **pendiente** |
| Configuración / recalibrar | Competencia y permisos, matriz adecuada | Potencia, minutos, puede bloquear otras acciones | Perfil no soportado, daño, conflicto de recurso | Core **pendiente** |
| Resultados / comparar | Dos lecturas ya conocidas | Consulta de historia | Fuentes no comparables o datos insuficientes | Core **pendiente** |
| Resultados / enviar a Ciencia | Observación del dossier y destinatario autorizado | Cola de mensajes y latencia | ID ajeno, permisos, Ciencia rechaza datos | Candidato a handoff **referencia** |
| Diagnóstico / autoprueba | Operador habilitado, matriz presente | Tiempo/calibración | Daño impide test, resultado inconcluso | Ingeniería/Core **pendiente** |
| Soporte de Ingeniería / OPS | Motivo y evidencia válidos | Comunicación/cola de tareas | Denegación por prioridad, demora, personal no disponible | F05 + interconsole **pendiente** |

## Umbrales instrumentales de la prueba
F06 sólo exige disponibilidad superior a 0.12 (corto), 0.28 (largo) o 0.35 (focalizado) en **fracción normalizada ficticia de test**; no consume ese recurso y no modifica el balance de la nave. Se prohíbe transportar estos números a la narrativa o UE5 sin decisión formal de diseño y pruebas de Core. El escáner usa duración de la petición para cálculo de confianza; el tiempo real debe reservarse después.

## Integración con el ciclo F05
Solicitud ≠ orden ≠ compromiso ≠ acción ≠ resultado ≠ evento. Un resultado de F05 ALLOW_REFERENCE **no ejecuta** la operación: es solo una precondición prestada en la prueba. La futura API de Core debe volver a verificar autoridad/revisión de orden y recurso al momento de comprometer el estado, rechazar carreras, tramitar expiración/cancelación y registrar de forma causal lo ocurrido. Una LLM no puede decidir ese commit.

**P04:** reglas verificables de barrido y plan explícito de las demás operaciones; **motor temporal, recursos y permisos reales NO_EJECUTADOS**.
