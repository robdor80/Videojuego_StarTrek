# Encargo Codex — H06-P06-A · Validación productiva de la biografía

**Fecha:** 14-11-2026. **Modelo recomendado: GPT-6. Nivel de razonamiento: Alto (High).**  
**Repositorio:** `robdor80/Videojuego_StarTrek`, partiendo de `main` tras la fusión de los documentos H06-P06-A.  
**Salida:** rama propia y **PR Draft**, sin fusionar. ChatGPT auditará.  
**Alcance:** exclusivamente puerta de validación **F10** de la biografía inicial de Academia. **NO** implantar H06-P06-B/H03/H04, admitir cadetes, modificar F05/F11 ni ejecutar Unreal salvo necesidad puntual demostrada. **NO** modificar CoreRPG fijado.

## Lectura obligatoria y auditoría previa

1. `AGENTS.md` y las reglas vigentes sobre temporales, [informe de factibilidad Core #150](F10_H06_P06_FACTIBILIDAD_NATIVA_2026-11-14.md) y [contrato de alta](F10_H06_P06_CONTRATO_INTERFAZ_ACADEMIA_2026-11-14.md).
2. [Contrato del presente corte](H06_P06_A_CONTRATO_VALIDACION_BIOGRAFIA_2026-11-14.md), `sistemas/gameplay/character_creation/f10_biography_validation_interface_v0.1.json`, y las referencias `desarrollo/tools/validation/f10_biography_precheck.py` + `test_f10_biography_precheck.py`.
3. Reglas bloqueadas `character_creation_contract_v1_0.json`, `biography_validation_rules.md`, `prior_activity_model.json`, `player_profile_contract.json`, `character_affiliation_citizenship_contract.json`, `species_biology_contract.json` y perfiles versionados de especie.
4. F10 (`admission_flow.json`, reglas de Academia, QA de referencia) y HOST `SessionOwner`, puente Core fijado `76a7b7b485616d8c4994f384a90f123bf333591d`.

## Meta técnica exacta

**Construir las dos puertas de F10, con separación de confianza**, para que en el futuro pueda publicarse una PERSON solo tras validación de biografía. No implementar el commit ni fingir que un validador Python offline otorga autoridad.

### Corte A1 — reglas objetivas nativas

- Conservar el orden y campos del contrato bloqueado, sin inventar niveles/puntos de habilidad, calendario exacto de 2383, ciudadanía por especie, rango de Flota, permisos o cualificaciones automáticas.
- Convertir a reglas **ejecutables** todas las comprobaciones cuya fuente versionada sea suficiente: sintaxis, campos, especie/catálogo, año de nacimiento, evidencias y referencias autorizadas, cronología y restricciones temporales. Para las reglas sin datos (por ejemplo, umbrales de madurez de especies), emitir `REVIEW_REQUIRED` **sin aprobar**, e inventariar decisiones que corresponden al autor/F10. El hecho de que un borrador declare `adult_equivalent_status=true` no valida la madurez.
- Evitar falsos rechazos por suponer que todas las especies maduran como humanos o que un hobby concede una titulación. Un texto libre plausible puede seguir pendiente de revisión, no otorgar un `VALID`.
- Guardar el resultado como objeto interno de F10 con origen verificable por el proceso, vinculado a biografía, contexto de campaña y versión del ruleset. Solo un código de producto confiable puede confirmar `OBJECTIVE_VALID`; el cliente no introduce el veredicto.

### Corte A2 — revisión semántica asistida por IA

- Diseñar e implementar el **puerto interno del verificador**, separado de la interfaz pública y del motor Core. La salida IA son hallazgos y sugerencias **no autoritativos**; F10 comprueba correspondencia del borrador exacto, política, versión, respuesta y trazabilidad.
- La revisión semántica asistida por IA es **obligatoria** según los contratos existentes. No imponer un proveedor de pago, un servidor externo ni un modelo que el repositorio no incorpore. Si no hay proveedor local ya configurado y aprobado, implementar el puerto y su prueba con un **doble control de ensayo explícito** pero dejar el veredicto de producción `REVIEW_UNAVAILABLE` y la publicación bloqueada. No convertir un fixture en credencial ni afirmar integración real.
- Cambios de nombre, especie, edad, estudios, experiencia, fecha o versión de reglas invalidan la revisión; no se reescribe una biografía silenciosamente. Informar correcciones al usuario, con código y campo; no enviar biografías privadas a logs o telemetría.
- Los hashes canónicos son identificadores de contenido, **no autorizaciones ni firmas**. El recibo de aprobación futura queda dentro del ámbito F10/HOST de confianza y no se admite desde Blueprint, UI, PADD ni IA.

### Corte A3 — verificación conjunta

- Probar que **solo** la conjunción de reglas objetivas `OBJECTIVE_VALID`, revisión semántica auténtica sobre el mismo borrador y contexto y generación/identidad de campaña vigentes habilitaría la fase de commit **posterior**. Esta fase A no publica ninguna PERSON.
- Probar casos de rechazo y fallos: campo obligatorio ausente, especie desconocida, biografía alterada tras revisión, credenciales introducidas por el cliente, versión obsoleta, caso ambiguo de madurez, reconocimiento de certificados sin pruebas, IA caída, revisión contradictoria, falla de servicio y retries sin mutación. Preservar las 19 pruebas Python de precheck y referencias F10.
- Usar interfaces pequeñas; evitar bibliotecas externas, nuevos servicios persistentes, archivos enormes o cachés de UE. La carga principal de la PR debe ser validadores, su contrato y pruebas.

### Puertas de bloqueo / límites

Si falta una decisión normativa indispensable (fecha de inicio día/mes, madurez contextual, tecnología, reglas concretas de ciudadanía o evaluador IA), **no inventar un valor**. Completar las comprobaciones seguras y marcar solo ese caso como pendiente. Es válido terminar H06-P06-A como PARCIAL con evidencia real.

- No emitir `validated_creation_ref` a partir de un booleano, de un texto de IA, de `CORE_HOST_VERIFIED` de fixtures o de un SHA-256 de entrada.
- No tocar el registro/cupo de Academia, la matrícula, rango, carrera, H03, H04, F05, CoreRPG fijado, ABI pública ni `StarTrekRPG.uproject` para desbloquear por fuerza la prueba.
- No crear laboratorios permanentes ni borrar worktrees históricos. Reutilizar fuentes y cachés; temporales solo según AGENTS.md; evítese recompilar Unreal si no hay cambios UE.

## Evidencia y entrega

- Publicar tres documentos definitivos en `proyecto/docs/architecture/host/` con prefijo `H06_P06_A` y tema **FACTIBILIDAD**, **IMPLEMENTACION**, **RESULTADOS** (fecha 14-11-2026). Describir todas las decisiones pendientes y modelo de autoridad real.
- Tests nativos de módulo si se ha compilado C++, tests negativos, regresiones F10 Python y suites HOST relevantes; declarar **NOT_RUN** para aquello no ejecutado. Mantener 240/240 Windows/Linux y 85/85 sanitizers **como umbral histórico**; los nuevos casos incrementarán el total si se registran. Release OFF no debe incluir ejecutables de ensayo.
- La evidencia offline solo acredita su alcance, no la creación de un cadete ni el cierre CB/HU-08/M1; no declarar CERTIFICADO si falta proveedor IA/autoridad.
- Comunicar **PR Draft, HEAD, implementación real, pruebas efectivamente ejecutadas y bloqueos**, guardando informes permanentes para auditoría posterior.

**Modelo: GPT-6. Razonamiento: Alto (High).**  
**No comenzar H06-P06-B ni H07 como parte de este encargo.**
