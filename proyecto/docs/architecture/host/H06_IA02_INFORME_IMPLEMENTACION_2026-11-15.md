# H06 / IA-02 — Motor semántico de biografía F10

Entrega permanente, trabajo **2 de 3**, 15/11/2026. Responsable: Codex.
Base: `42196e4e0858eb2fc4ada3be93eb124226eec9f6` (PR #164 fusionada).
Rama: `codex/h06-ia02-f10-openai`. [PR Draft #165](https://github.com/robdor80/Videojuego_StarTrek/pull/165), sin fusionar.
HEAD exacto de implementación: `adcfb9fc11fc9ec113562e55d8f9b943880c04fc`. El HEAD de entrega se registra en la PR;
los commits posteriores exclusivamente documentales se distinguen del código probado.

## Arquitectura y composición interna

`OpenAiBiographyEvaluator` es final y consume la instancia compartida de
`trek::host::ai::Service`; no crea cliente HTTP ni trabajador. La composición HOST de confianza
crea el servicio, el adaptador y `RegisteredBiographyAuthority(sources, evidence, adapter)`,
y después `BiographyValidator(authority)`. El constructor productivo solo admite ese adaptador
concreto; el constructor histórico que admite evaluadores/autoridades arbitrarios sigue
compilándose exclusivamente en el ejecutable histórico de tests.

Cada sesión/borrador tiene un adaptador, usado desde un único hilo propietario. El HOST mantiene
el servicio compartido vivo durante las revisiones y lo destruye en su trabajador de cierre,
como IA-01 exige; no destruir la última referencia al servicio en Game Thread. No se añade ABI
Unreal, formulario, bootstrap definitivo, persistencia, PERSON, matrícula ni vínculo F05.

Se reutilizan `evaluate`, `eligible`, `SemanticEvaluator::review`, `BiographyAuthority::verify`,
`ReviewBinding`, `ReviewEvidence` y el registro de evidencias objetivas. La primera puerta no
cambia: si existe rechazo no se consulta IA; si hay evidencia pendiente no se consulta IA.
El constructor sin adaptador mantiene el comportamiento histórico de indisponibilidad.
El evaluador concreto se conecta explícitamente desde la composición interna futura del HOST.

## Datos, prompt y Structured Outputs

La política nueva `f10_openai_semantic_policy_v0.1.json` registra la precedencia autoral de
15/11/2026 sobre las restricciones locales de los contratos históricos. **No se sobrescriben**
las versiones históricas bloqueadas ni sus pruebas. La política de edad sigue siendo
`f10_species_playable_maturity_policy/0.1.2`, sin prueba individual de madurez. Año 2383,
sin inventar día/mes. El generador incorpora la política nueva al digest de fuentes y a
`ReviewBinding.policy`; conserva la versión objetiva `/5`, pues las reglas objetivas no cambian.
Una revisión anterior tiene distinta política y huella y no sirve para esta implementación.
Huella SHA-256 de fuentes embebidas verificada: `5845a0fbe0aeacdcb0277d8af57b9b54b7fb6667ea4dc8ed15a09696ca037360`.

El prompt de confianza está separado del mensaje de datos. Los textos del jugador no se
interpolan en instrucciones. Se envían el borrador canónico, escenario/era/año autorizados,
restricciones de madurez de la especie seleccionada, una proyección pública de su perfil
(fisiología, capacidades, cultura, límites de IA; se omiten estado médico y ciclo vital),
y versiones. Los IDs de campaña/perfil y la generación se vinculan localmente y no se envían.
No se consultan expedientes ajenos ni secretos de la partida.

`FAST_LANGUAGE` es habitual. `EXPLICIT_COMPLEX` selecciona `REASONING_LANGUAGE` expresamente,
sin escalada ni reintentos automáticos. Se respetan modelos/rutas configurados en IA-01.
El esquema estricto exige `verdict` (`COHERENT`/`CHANGES_REQUIRED`) e `issues` (máximo 16).
Cada observación exige campo canónico permitido, tipo `CONTRADICTION`/`SUGGESTION`, razón y
orientación en castellano (hasta 512 caracteres cada una). Todos los objetos prohíben extras.
IA-01 aplica `strict:true` y valida el JSON contra el esquema; F10 comprueba además coherencia
entre veredicto y presencia de contradicciones, texto no vacío y campos/tipos admitidos.
La salida se acota a 32768 bytes. Una respuesta inconsistente se considera indisponible.

La opción aditiva `Request::require_model_identity` de IA-01 exige que `response.model` coincida
con el modelo de la ruta inmutable; F10 la activa. Si el proveedor devuelve un identificador de
snapshot diferente, hay que configurar explícitamente ese modelo: se rechaza la discrepancia.
`route_model` permite conocer la expectativa sin copiar configuración en el consumidor.
Los consumidores anteriores conservan su comportamiento (opción desactivada por defecto).

## Procedencia, verificación y autoridad

El adaptador conserva **un solo registro privado** por sesión: borrador canónico exacto,
contexto completo con generación, binding de hashes/reglas/política, identidad y versión del
evaluador, resultado completado y observaciones. Solo la lectura de un futuro realmente
completado de IA-01 puede producir un registro completo. No existe método para importar un
resultado, registrar una aprobación o sustituir un evaluador simulado en producción.
La prueba de transporte de IA-01 sigue siendo una dependencia inyectable deliberada del HOST;
solo composición C++ de confianza puede suministrarla, nunca el formulario o el jugador.
No se pretende proteger el proceso contra código nativo malicioso ejecutado dentro del HOST.

`RegisteredBiographyAuthority::verify` recalcula las huellas del borrador/contexto y la política
vigente, y consulta el registro privado del adaptador esperado. Exige igualdad íntegra de la
evidencia, incluida referencia, versión, finalización y observaciones. Una cadena de aprobación,
una huella o un `ReviewEvidence` sin registro no bastan. El modelo esperado se comprueba tanto
en la respuesta técnica como contra la configuración inmutable del servicio.

F10 valida estructura, procedencia, vínculo y tipos; `CORRECTIONS` exige observaciones de
contradicción admitidas. No se transforma el razonamiento del modelo en hechos del universo:
las observaciones siguen siendo propuestas y ninguna concede rangos, habilidades o permisos.
Con solo sugerencias puede emitirse recibo si ambas puertas son válidas. `feedback` conserva
razón/orientación para el jugador, sin reescribir el borrador ni registrar textos en logs.
Un recibo privado no es PERSON ni autorización institucional. `eligible` vuelve a consultar
la procedencia vigente: cancelar o reemplazar el registro invalida también recibos ya emitidos.

## Asincronía y vigencia

Primera evaluación válida objetivamente: se copian canónico/contexto/binding antes de encolar;
`review` devuelve `PENDING` y F10 devuelve `REVIEW_REQUIRED`, sin recibo. Una evaluación posterior
consulta `wait_for(0)`; solo llama a `get()` cuando está listo. No mantiene vistas prestadas.
La revisión completada o el fallo se conservan sin volver a consumir API durante los sondeos.
Un reintento explícito requiere cancelar y volver a evaluar.

El dueño debe llamar `cancel()` al editar/cambiar contexto, cerrar sesión, cancelar operación
o recargar política, y dejar de sondear al cerrar/cancelar. La evaluación también cancela al
detectar entrada inválida, evidencia objetiva pendiente o un vínculo diferente. Una nueva
evaluación después de cancelación es una nueva solicitud; nunca recupera la operación cancelada.
La generación/contexto actuales se pasan de nuevo a `evaluate` y a `eligible`. No hay callbacks
sobre Unreal ni referencias a objetos del juego en el trabajador de IA-01.

## Archivos y contratos

- Nuevos: `src/f10/openai_biography.{h,cpp}`, `tests/biography_ai_tests.cpp` y la política semántica.
- Modificados: `biography_validation.{h,cpp}`, `biography_evidence.h`, generador de reglas,
  `ai/service.cpp`, `include/trek/host/ai/service.h`, CMake HOST y workflow HOST.
- Reutilizados: contratos de creación, reglas biográficas, interfaz y frontera de evidencia,
  política de antecedentes y de edades, contratos de campaña/candidato H06-P06 e IA-01.
- CoreRPG y su pin `76a7b7b485616d8c4994f384a90f123bf333591d`: sin cambios.

## Pruebas y resultados

Las pruebas nuevas compilan las fuentes productivas **sin** `TREK_F10_BIOGRAPHY_TESTING`.
Usan el servicio IA-01 real con transporte/credencial simulados. Las fuentes objetivas de las
fixtures son datos de ensayo, **no evidencias aprobadas para un personaje real**.

Casos: coherencia; cronología objetiva imposible; edad mínima antes de IA; afición legítima;
certificación pendiente; contradicción institucional y de estudios/experiencia; sugerencias
sin edición; JSON malformado, extras, campos inválidos y veredicto inconsistente; respuesta
incompleta/rechazo; falta de clave; 401/429/500/503; timeout/cancelación; cambio de borrador,
especie, campaña, perfil y generación; modelo diferente/ausente; versiones/bindings falsificados;
registro inexistente/cancelado; recibo obsoleto; selección explícita Sol y privacidad del payload.
Las aserciones de compilación rechazan sustitución por `SemanticEvaluator` genérico y el
constructor privilegiado histórico. No hay API para insertar registros completos.

Matriz de comprobación del encargo (las respuestas semánticas son controladas):

| Casos | Comprobación |
|---|---|
| 1, 4 | `coherent` y `findings`: humano 20, karate y astronomía; solo recibo privado |
| 2, 3 | `objective`: inicio posterior a edad y menor de especie, cero HTTP |
| 5 | `objective`: certificación sin fuente queda pendiente, cero HTTP |
| 6, 7 | `findings`: contradicción temporal/institucional y sugerencia; borrador intacto |
| 8, 9, 10 | `failures`: formato, extras, enum/campo, veredicto inconsistente, incompletitud y refusal |
| 11, 12, 13 | `failures`/`stale`: clave ausente, 401/429/500/503, timeout y cancelación |
| 14, 15 | `replacement`/`stale`: borrador, especie, campaña, perfil, generación y cierre |
| 16, 17, 18 | `failures`/`provenance`: modelo/versión, bindings/observaciones falsos, registro ausente/cancelado |
| 19 | Diff y checkout limpio del Core fijado; inspección de producto carga el pin real |
| 20 | Payload sin clave ni IDs privados; diagnósticos fijos, sin logger nuevo ni impresión de biografías |

Resultados locales en Linux, GCC 14.2 y CMake 4.4.5, HEAD de implementación indicado:

- Regresión nativa HOST/F10/F04/F05: **265/265 PASS** (33,61 s).
- F10 Python de referencia: **163/163 PASS**. H01 documental: **11/11 PASS**.
- Batería F10/IA aislada: **25/25 PASS**, antes de ejecutar la regresión completa.
- No se modifican pruebas históricas para obtener estos resultados. La primera ejecución nueva
  detectó un timeout de fixture inferior al mínimo de IA-01 (30 frente a 100 ms); se corrigió
  únicamente esa fixture nueva. No se cambiaron límites ni políticas de producto para ello.
- Compilaciones/inspecciones Release con tests OFF: **PASS Linux y Windows x64 en CI**.

CI del HEAD de implementación `adcfb9fc11fc9ec113562e55d8f9b943880c04fc`:
[ejecución 43730271106, cinco trabajos correctos](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271106).

| Verificación real | Resultado |
|---|---|
| Linux nativo (GNU) HOST/F10/F04/F05 | 265/265 PASS |
| Windows x64 nativo (MSVC) HOST/F10/F04/F05 | 265/265 PASS |
| Linux Clang ASan/UBSan, detección de fugas activa | 110/110 PASS |
| F11 aislado con producto real, Linux y Windows | 17/17 PASS por plataforma |
| Release tests OFF Linux y Windows x64 | PASS: compilación, carga, exports, pin y ABI C 1 |

[H01 documental en CI](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271105): PASS.
También pasó la regresión documental F09 activada por el cambio HOST. Los logs completos de
los cinco trabajos se inspeccionaron; el resultado F11 identifica GNU y MSVC respectivamente.

Artefactos de evidencia de esa ejecución:
[Windows nativo](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271106/artifacts/14168153483),
[Linux nativo](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271106/artifacts/14168187886),
[ASan/UBSan](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271106/artifacts/14167849341),
[producto Windows](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271106/artifacts/14168580011),
[producto Linux](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43730271106/artifacts/14167923618).
Este cierre documental posterior no cambia código, políticas ni huellas respecto al HEAD probado.
OpenAI real: **NOT_RUN**; el entorno Cloud declara ausencia de secretos. No se realiza una
llamada pagable. Las simulaciones no demuestran una revisión real de Luna ni calidad semántica.

## Limitaciones objetivas reales y cierre

Una biografía ordinaria (Daniel, humano de 20 años, karate desde los ocho) supera edad y puede
superar la actividad personal comprobable. Siguen faltando fuentes aprobadas concretas para:
`origin` (`ORIGIN_EVIDENCE_REQUIRED`), `citizenship_context` (`CITIZENSHIP_EVIDENCE_REQUIRED`),
`prior_education` (`EDUCATION_EVIDENCE_REQUIRED`), `prior_experience`
(`EXPERIENCE_EVIDENCE_REQUIRED`) y perfil propietario (`PROFILE_EVIDENCE_REQUIRED`). Una
certificación añade `CERTIFICATION_EVIDENCE_REQUIRED`; actividades solapadas o no comprobables
pueden añadir `ACTIVITY_BUDGET_REVIEW`. Se conservan las políticas especiales/DLC existentes.
No se generan atestaciones ficticias para resolver estas carencias: **REVIEW_REQUIRED, sin IA
ni recibo** hasta disponer de fuentes auténticas. El adaptador no define esas fuentes nuevas.

No se ha verificado el circuito posterior de creación real F10/Core. No se declara un personaje
creable ni certificación H06/M1. Entrega limitada a IA-02, PR Draft sin fusionar para auditoría
independiente de ChatGPT; trabajo 3, UI y operaciones institucionales permanecen fuera.
