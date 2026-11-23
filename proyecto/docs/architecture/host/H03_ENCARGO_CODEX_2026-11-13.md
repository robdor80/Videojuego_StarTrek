# H03 — Encargo de implementación para Codex (después de revisión documental)

**Modelo recomendado:** GPT-6 (si está disponible en Codex).  
**Nivel de razonamiento recomendado:** Alto.  
**Estado del encargo:** PREPARADO, **NO EJECUTADO**.  
**Repo:** `robdor80/Videojuego_StarTrek`. **Fase:** HOST H03-P02/P03/P04.  
**Base de integración:** `main` posterior a la fusión de H02, [PR #132](https://github.com/robdor80/Videojuego_StarTrek/pull/132).

## Tarea

Implementa únicamente el vínculo local de identidad del jugador con **una única** campaña Core y un sujeto PERSON real dentro de la biblioteca nativa `TrekHost` existente. Parte de los contratos `H03_P01_IDENTIDAD_CONTRATO_v1.0_2026-11-13.md` y `H03_P04_MATRIZ_PRUEBAS_v1.0_2026-11-13.md`. Consulta `AGENTS.md`, H01, H02 y los headers reales antes de editar.

El HOST es local, un jugador, offline; no introduzcas servidor, cuentas, OAuth, criptografía vacía, antitrampas ni otro motor de reglas. CoreRPG conserva los hechos; F11 conserva identidad profesional, permisos y la emisión de ascensos. No tocar F11-P05-A02-03, no copiar ningún emisor de ensayo y no habilitar mutaciones privilegiadas desde UI/IA/NPC.

## Pasos de trabajo

1. Audita el C++ H02 real: `SessionOwner`, `NativeSession`, hilo propietario, admisión, cierre, generación, y la composición actual CMake de F04/F05. Comprueba los SHA y las flags sin actualizar pins de forma implícita.
2. Inspecciona la ABI F04 `F04Ref`, `f04_person`, `f04_handles`, `f04_stats` y la ABI F05 `f05_bind_player`. Examina su semántica real: mismo sujeto es idempotente; diferente sujeto es conflicto; primera vinculación exige revisión. No deduzcas que existen métodos de carga o lectores de vínculo que no están exportados.
3. Diseña una extensión **interna** de `TrekHost` que reuse la misma `F04Session` y su hilo propietario, sin segundo dueño, guardando un contexto mínimo principal/campaña/sujeto/generación para acceso. Distingue `ACTIVE` de `BOUND`. No usar `ship_identity`, `F04Ref`, causa, rank ni entity ID como credenciales.
4. Implementa vinculación inicial **solo por flujo de bootstrap confiable**: resuelve en Core la entidad PERSON real, comprueba pertenencia a campaña, scope y generación; pasa al `f05_bind_player` existente solo en el hilo propietario; no publica `BOUND` ante fallo. Cuando se vuelva a solicitar el mismo vínculo no crees un segundo registro F05.
5. Protege concurrencia, cierre/admisión, errores de revisión y generación; nunca regreses al estado `BOUND` después de cerrar. Garantiza salida vacía en denegación y ausencia de APIs de «cambiar actor» libres. No alteres los invariantes H02. Mantén ABI C sin STL/exception/UObject.
6. Implementa pruebas nativas reales para HI-01 a HI-13 y HI-19 en la medida que las APIs permitan, y pruebas negativas de suplantación. Los escenarios HI-15..HI-18 dependen de H04/H07/H10 y se reportan PENDIENTES, **no PASS**. Si una cobertura requiere un futuro componente no existente, registra SKIP justificado.
7. Ejecución: Windows/MSVC y Linux/GCC o Clang en CI si dispone de los jobs; regresiones H02, F04 y F05. No anuncies certificación UE, H04 ni F11. Documenta comandos reproducibles, HEAD, Core SHA, flags, resultados y límites.
8. Publica los cambios en una **rama distinta** de la rama de documentación y abre una PR Draft contra `main`. No fusionar sin autorización del usuario.

## Bloqueantes y límites explícitos

- Si no hay flujo de creación final para el cadete de la Academia, usa un fixture nativo controlado para comprobar el vínculo y etiqueta claramente esa cobertura. No conviertas un fixture de F04 en el personaje final del juego ni inventes el flujo de Academia.
- Si la recuperación segura de un `f05_player` anterior requiere una lectura inexistente, **no toques estructuras privadas Core desde HOST**. Documenta la necesidad de una API read-only propiedad de F05 para discusión con el proyecto principal; deja recuperación durable a H04.
- No implementes guardado, importaciones, reconstrucción de scopes tras LOAD ni pruebas de durabilidad todavía: pertenecen a H04. No crees un segundo fichero de identidad paralelo con autoridad.
- Los posibles cambios en API F04/F05 o pin Core requerirán propuesta y autorización previa; no ejecutes refactorización amplia por iniciativa propia.
- Trabaja solo mediante PR; deja `main`, las versiones históricas y los laboratorios anteriores intactos. Resultados temporales siempre según `AGENTS.md`.

## Entregables y salida solicitada

A. Código C++ de vínculo H03 integrado en TrekHost, sin nuevo dueño de sesión.  
B. Pruebas de vínculo, conflictos, concurrencia y scope/generación, CI y regresiones documentadas.  
C. Informe de trazabilidad caso HI → test → resultado con evidencias concretas.  
D. Inventario de ficheros tocados, riesgos residuales, casos diferidos y decisiones que necesita el usuario.  
E. URL de PR Draft, sin merge.  

**Cierre H03:** ChatGPT audita la PR y los resultados; el usuario autoriza o deniega su fusión. Un merge no equivale a certificación de carga persistente ni de integración UE.
