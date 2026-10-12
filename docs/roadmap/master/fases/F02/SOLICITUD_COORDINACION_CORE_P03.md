# F02-P03 — Handoff para coordinación con responsables CoreRPG y Host UE5

**Estado:** solicitud técnica documentada, **sin aceptación ni compromiso de implementación por la contraparte**. No se ha modificado el repositorio CoreRPG. Corte: Core `main@dcfcb83`; rama `feat/generic-world-state@2a3da89`.

## Contexto mínimo verificable

- Consumidor: Star Trek RPG 3D para Windows, Host UE5; **v0.0.1 = prueba interna de guardia de Sensores**.
- Core es biblioteca C++20 y debe seguir independiente de UE5 y Star Trek. Se compila con CMake; aún no hay ABI estable ni Host UE5 integrado.
- CoreRPG/main tiene identidad y catálogo mínimos; no tiene mundo completo, acciones, guardado, conocimiento o simulación.
- Star Trek ya posee contratos de nave/tripulación, sensores, órdenes, bitácora y fixtures; **son especificaciones de dominio**, no interfaces aceptadas por Core.
- [ADR-0001 multiuniverso](https://github.com/robdor80/CoreRPG/blob/dcfcb83c9853e005b5450bd39e0ba693cb91e257/docs/adr/0001-multi-universe-architecture.md) y [ADR-0002 Hosts](https://github.com/robdor80/CoreRPG/blob/dcfcb83c9853e005b5450bd39e0ba693cb91e257/docs/adr/0002-platforms-presentation-companion.md) gobiernan la distribución de responsabilidades.

## Preguntas concretas a Core; sin imponer soluciones

| ID | Pregunta para acordar y registrar | Fase Core | Evidencia mínima antes de cerrar |
|---|---|---|---|
| **Q01** | ¿Cuál es la primera API integrada en `main` para entidades vivas y vínculo posterior de datos de dominio? ¿Cómo modelar alias Trek sin hacer `EntityId` global? | 4.5/4.8 | Header público/versión/CI, semántica de mundo y ejemplo |
| **Q02** | ¿Qué modelo aprobado enlaza `DefinitionId` con instanciación viva y propiedades Trek sin ampliar arbitrariamente JSON 0.1.0? | después de 4.5 | Caso de uso Star Trek y Nimroel, contrato versionado |
| **Q03** | ¿Cómo se expondrá tiempo autoritativo (timestamp, precisión, orden causal) y compatibilidad de agenda sin convertir la contención en ubicación? | 4.8–4.10 | Estados/tipos y prueba de coherencia |
| **Q04** | ¿Qué frontera entre validaciones universales y reglas Trek acepta Core para una orden de capitán o alférez, con autoridad y delegación temporal? | 4.6/4.10 | Acción validada y rechazo en código, sin términos Trek en Core |
| **Q05** | ¿Dónde se aplica la proyección por observador ANTES del Host/IA, y cómo se impide filtrar `authoritative_entity_id`/verdad oculta en Sensores? | 4.9 | Prueba negativa anti-filtración |
| **Q06** | ¿Cómo conservar causalidad entre orden, scan, resultado, informe y eventos append-only sin hacer logging redundante en Star Trek? | 4.7/4.10 | Event IDs/relaciones probadas y alcance de visibilidad |
| **Q07** | ¿Qué garantías tendrá save/load atómico respecto de `EntityId`, semillas, agenda, conocimiento y eventos? ¿Cómo se versionarán migraciones? | 4.7 | Roundtrip real, rechazo de estado incompatible |
| **Q08** | ¿Qué política de aplicación/revalidación/reintento después de timeout permite no ejecutar duplicados, sin asumir un command bus universal? | 4.10/4.12 | Casos revocación, repetición, respuesta IA tardía |

## Preguntas concretas al responsable del Host UE5

| ID | Pregunta | Prueba pendiente |
|---|---|---|
| **H01** | ¿Qué toolchain UE5/Windows y forma de enlazar biblioteca C++20 funciona realmente con el target `CoreRPG` y sus dependencias aisladas? | Compilación y link reales en MSI |
| **H02** | ¿Quién posee instancia lógica, referencias y hilo de mutación mientras vive el Host? | Actor creado→descargado→recreado, mismo `EntityId` |
| **H03** | ¿Qué política conserva entrada por teclado/ratón y consola operativa sin IA/Companion? | Guardias de Sensores offline de servicios IA |
| **H04** | ¿Cómo se evita que Game Thread, callbacks asíncronos y Blueprint muten directamente WorldState sin validación? | Pruebas de errores/reentrancia/hilos |

## Prioridad de respuestas y próximos entregables

1. **Ahora:** terminar Core 4.5 en rama/PR/CI/merge; no introducir cambios en su árbol local pendiente desde Star Trek.
2. **En Core 4.6–4.10:** pactar mínimos de solicitudes/resultados/eventos/visibilidad/persistencia con **ambos consumidores reales** (Star Trek/Nimroel), sin ampliar el núcleo con normativa de Flota Estelar.
3. **En F07 UE5:** spike acotado de identidad y Actor temporal; es admisible una interfaz de prueba estrictamente etiquetada, nunca simular que es el juego persistente.
4. **En F08:** guardia Sensores end-to-end cuando las capacidades estén integradas y probadas, con guardado/carga, informes, rechazo por permiso y continuidad off-screen.

## Política de cierre formal

Para cada Q/H resuelta: adjuntar **SHA de Core**, cabecera y versión/compatibilidad, decisión aceptada por responsable, tests/CI y prueba del consumidor. Una reunión informal o una respuesta del modelo no constituye por sí sola una API de producción.

**Fuera de este handoff:** elección de Dama Imperator (DEC-0001, F01), PWA web Academia, activos 3D y licencias, implementación de un `UniversalCommandSystem` genérico no aprobado, políticas futuras Companion/Android.
