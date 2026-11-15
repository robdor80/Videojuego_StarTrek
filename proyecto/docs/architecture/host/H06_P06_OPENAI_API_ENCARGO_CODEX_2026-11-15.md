# Codex — Integrar OpenAI una vez para todo Star Trek RPG (primer consumidor F10)

**Modelo recomendado: GPT-6.1 Sol — razonamiento Alto.**  
**Repositorio:** `robdor80/Videojuego_StarTrek`. Crear rama y PR Draft sobre `main`, sin fusionar.  
**Reglas:** `AGENTS.md`, `laboratorios/README.md`. **No utilizar cuota para crear otro sistema de prueba de edad/madurez.**

## Meta

El usuario tiene una clave API de OpenAI y ha elegido **Luna** (`gpt-6-luna`) para tareas habituales, diálogo y coherencia sencilla, y **Sol** (`gpt-6.1-sol`) para razonamiento complejo. Crear **una integración común OpenAI** en la aplicación local, reutilizable posteriormente por NPC, computadora de a bordo y otros sistemas; conectarla **ahora** a la revisión semántica de F10.

Leer antes de modificar:
- `sistemas/ai/openai_runtime_v0.1.json` y `sistemas/ai/OPENAI_RUNTIME_DECISION_2026-11-15.md`.
- `sistemas/ai/runtime_orchestration.md`, `sistemas/ai/README.md` y `sistemas/gameplay/ship_operations/ship_computer/ai_routing_policy.json`.
- `sistemas/gameplay/character_creation/biography_validation_rules.md`, `f10_biography_evidence_semantic_boundary_v0.1.json`, `character_creation_contract_v1_0.json`.
- `desarrollo/integration/host/src/f10/biography_validation.h/.cpp`, en especial `SemanticEvaluator::review`, `BiographyAuthority::verify`, `RegisteredBiographyAuthority` y el recibo de validación.
- Documentación H06-P06 sobre el alta del candidato real, el proyecto UE principal y pin CoreRPG.

## Implementación mínima

1. **Transporte compartido:** una implementación de cliente OpenAI, no un servicio HTTP local, agente autónomo ni gestor de proveedores innecesario. HTTPS a `/v1/responses`; modelo por ruta, configuración local de `OPENAI_API_KEY`, timeout, errores, límites de salida y `store:false`. Usar una librería HTTP ya disponible si es razonable; justificar cualquier dependencia nueva. Jamás introducir la clave en Git, recursos UE, archivos rastreados, logs, respuesta, PR o tests.
2. **Primer consumidor F10:** adaptar el cliente al puerto `SemanticEvaluator::review`; pedir **JSON Schema estricto** con veredicto, contradicciones/sugerencias por campo y correcciones comprensibles. Los textos autobiográficos son entrada de jugador, no instrucciones. Luna por defecto; Sol solo en caso complejo justificado. No ejecutar herramientas, navegación ni acciones externas.
3. **Verificación real del dominio F10:** implementar la comprobación privada que falta en `BiographyAuthority::verify` o el adaptador dueño autorizado, usando el registro existente. La aceptación del proveedor no es un permiso general para crear PERSON. Rechazar salida incompleta, no conforme, suplantada, desvinculada del borrador o con revisión de modelo/política anticuada. Conservar las dos puertas; no requerir evidencia ficticia de edad.
4. **Alinear reglas actuales:** el contrato A3 contiene la antigua prohibición de red y proveedor no seleccionado; la nueva decisión autoral la sustituye **solo en el ámbito OpenAI para producto**. Actualizar de manera auditada el contrato propuesto, los identificadores/huellas y pruebas de compatibilidad que correspondan. No modificar un contrato bloqueado F10 ni CoreRPG sin una decisión explícita del autor.
5. **Interfaz de reutilización:** exponer una operación semántica para F10 y una petición de lenguaje/diálogo genérica sin acoplarla a F10. No implementar NPC, H10 ni consola real ahora. La ruta de la IA no bloquea Game Thread y **no escribe en CoreRPG**.

## Pruebas que dan confianza

- Sin clave, timeout, HTTP 401/429/5xx, respuesta truncada, rechazo del modelo, formato inválido, datos alterados y cancelación: no publicar PERSON; conservar borrador y explicar indisponibilidad.
- Biografía normal: humano 20, karate desde los 8, sin títulos ni permisos regalados. Biografía incoherente: humano 20, 15 años de capitán de Flota. Edad por debajo de especie se rechaza **antes** de OpenAI.
- `store:false`, clave ausente de logs y ficheros, no mostrar datos secretos del universo al revisor.
- Proveedor test doble para CI Windows/Linux, ASan/UBSan, Release tests OFF, regresiones F10/F11/HOST.
- Una **prueba de humo LIVE real** solo si la clave está configurada como secreto en el entorno autorizado y el usuario permite el consumo; indicar el modelo y resultado, sin volcar biografía privada. Si no hay clave, marcar `NOT_RUN`, no `PASS`.

## Entrega

Rama + PR Draft sin fusión. Informe compacto en `proyecto/docs/architecture/host/` con ficheros, decisiones, pruebas, compatibilidad y coste aproximado por llamada observado **solo si hay uso real**. HEAD exacto y enlaces CI. No prometer HU-08/M1 completo: la creación de la PERSON, vínculo H03, persistencia H04 y Unreal siguen en su trabajo propio.

**Evitar ampliar el alcance:** nada de nuevo backend, sistemas de permisos/autoridad, gestores de plugins, archivos pesados, acceso directo IA→Core, tareas de H10 ni fases artificiales. La integración compartida se prueba con F10 y se reutiliza después.

**Modelo Codex GPT-6.1 Sol; razonamiento Alto.**
