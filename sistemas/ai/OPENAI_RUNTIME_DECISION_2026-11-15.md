# Decisión de producto — servicio OpenAI compartido para Star Trek RPG

**15 de noviembre de 2026.** **Estado:** diseño autoral aprobado; conexión API aún **NO IMPLEMENTADA ni probada en vivo**.

## Qué queremos y por qué

**Una conexión real con la API de OpenAI**, dentro del HOST, que atienda varias funciones del videojuego sin crear una integración independiente por función.

El primer consumidor es **F10**: comprueba la coherencia de la biografía antes de crear el personaje. Después, la misma conexión servirá a diálogos de NPC, computadora de a bordo y otras necesidades cuando lleguen sus fases. Esto **reutiliza** las rutas existentes de `sistemas/ai/runtime_orchestration.md`: `FAST_LANGUAGE`, `REASONING_LANGUAGE`, `DIALOGUE`, `COMPUTER_ANALYSIS` y otras. No desarrollar ahora toda H10 ni un servidor nuevo.

**Modelos elegidos por el autor:** `gpt-6-luna` para conversaciones/revisiones corrientes y `gpt-6.1-sol` para consultas complejas, sin escalar cada petición por defecto. Identificadores contrastados con la documentación oficial de OpenAI de 15-11-2026. Usar **Responses API**; F10 recibe resultados estructurados con `text.format=json_schema` y `strict=true`.

## Ejemplo claro de F10

El jugador crea a Daniel Torres, humano de 20 años, y cuenta que practicó karate desde los ocho años y le gusta la astronomía.

1. **F10 comprueba primero lo objetivo:** especie y edad mínima, fechas claramente imposibles y campos ilegales. Edad declarada suficiente = **edad correcta**, sin evidencia médica ni de madurez (PR #160).
2. **HOST pide una revisión semántica a OpenAI:** F10 proporciona la biografía y solo reglas/canon necesarios; los textos del jugador se tratan como datos, nunca como instrucciones para el modelo.
3. **OpenAI devuelve un JSON limitado** indicando `COHERENT` o `CHANGES_REQUIRED`, y, en su caso, campo afectado, tipo de problema y sugerencia legible. Ejemplo inválido: «tengo 20 años y fui capitán durante 15» por incoherencia temporal e institucional.
4. **F10 comprueba la respuesta** usando los puertos `SemanticEvaluator::review`, `BiographyAuthority::verify` y `BiographyValidator::eligible` existentes. La IA **no** es fuente de verdad ni crea PERSON, permiso, rango o matrícula. Sus sugerencias no reescriben automáticamente el texto del jugador.
5. Solo tras superar las puertas previstas, la futura operación F10/Core puede crear una PERSON de candidato real. La admisión a cadete sigue separada.

**Si falla OpenAI o falta la clave:** conservar el borrador y explicar que la revisión no está disponible, sin aprobar ficticiamente nada. El funcionamiento determinista del resto de la partida no depende de llamadas a IA cuando no hacen falta. Esta decisión mantiene la revisión semántica **obligatoria para crear una biografía nueva**, conforme al contrato F10.

## Qué no debemos construir

- Ningún segundo HOST ni sistema paralelo de memoria/persistencia, autoridad o catálogo de personajes.
- Ningún servidor web/backend para este primer despliegue local de un solo jugador.
- Ningún registro nuevo de «pruebas de adultez» ni atestaciones ficticias.
- Ningún proveedor autónomo por NPC, por consola o por tarea.
- Ningún acceso directo de Blueprint/NPC/CoreRPG a la clave API.
- No usar el modelo para resolver hechos que CoreRPG ya conoce (hora, permiso, sensores o inventario).

## La clave API: integración real, sin prohibiciones absurdas

El usuario **ya posee clave API y modelos elegidos**. Codex **puede y debe** conectar la API con una configuración segura, por ejemplo mediante `OPENAI_API_KEY` en el entorno de ejecución o almacenamiento de credenciales del sistema Windows. Si Codex trabaja en la nube, la clave se proporciona mediante el mecanismo de **secretos del entorno**, no como texto en una PR, commit, script rastreado, captura o log. No se necesita añadir una clave real a este contrato.

**Una precisión práctica:** en una instalación local personal el proceso del juego puede leer la clave del entorno del usuario. Si el juego se distribuye algún día con una clave compartida embebida, esa clave se podría extraer. Esa futura distribución exigiría un método distinto de credenciales, pero **no se introduce un servidor ahora**.

Las llamadas usan HTTPS, tiempo de espera acotado, tratamiento de cuotas/errores, `store:false` y contexto mínimo. Nunca deben bloquear el Game Thread. Las biografías se envían a OpenAI para revisarlas: hay que mostrar al jugador ese uso de datos cuando llegue la interfaz final. El uso de API se factura por consumo con independencia de la suscripción ChatGPT.

## Compatibilidad con contratos que ya existen

- `sistemas/ai/README.md` y `runtime_orchestration.md` siguen siendo la arquitectura y la frontera de autoridad: la IA interpreta, **CoreRPG decide hechos**.
- `sistemas/gameplay/character_creation/biography_validation_rules.md` sigue exigiendo la doble puerta objetiva + semántica; **no hay que quitarla**.
- `sistemas/gameplay/character_creation/f10_biography_evidence_semantic_boundary_v0.1.json` describía un proveedor local y prohibía red exterior. **Esa restricción de diseño se sustituye ahora por la autorización explícita de OpenAI**. La implementación de Codex debe armonizar política y huellas de versión sin editar silenciosamente contratos cerrados.
- `sistemas/ai/command_interpretation/starship_computer_system.md` refleja una política anterior de Gemini en un prototipo Holodeck. No borrarla ni convertirla en proveedor obligatorio del producto; la elección de producción actual es OpenAI.
- `sistemas/gameplay/character_creation/f10_individual_maturity_policy_v0.1.json` queda histórico por PR #160. No rescatarlo.

**Contrato pequeño y sin secretos:** `sistemas/ai/openai_runtime_v0.1.json`. No es un SDK ni asegura llamadas reales.

## Orden de implementación y prueba

**Primera entrega Codex:** transporte OpenAI compartido + adaptador semántico F10 **real** + tests. Debe reutilizar puertos nativos y no modificar CoreRPG. Debe comprobar JSON estricto, refusals, respuestas incompletas, datos obsoletos, cancelación, fallos HTTP, rate limits y costes acotados. Mock HTTP en CI, y una prueba de humo real bajo configuración segura con la clave del usuario. **No afirmar que se ha probado la API real si no se ha llamado a ella.**

**Después:** aprovechar el mismo servicio para una primera línea NPC, pero su integración profunda y gestión de conocimiento pertenecen a H10. La creación de PERSON/alta Academia/vínculo/guardado pertenece al cierre H06-P06 ya preparado, no a esta conexión.

**Responsables:** ChatGPT el contrato y auditoría; Codex el código crítico C++ y sus pruebas (**modelo recomendado GPT-6.1 Sol, razonamiento Alto**); usuario la clave y las decisiones de gameplay. PR Draft separada para auditoría, sin fusionar hasta verificar resultados.
