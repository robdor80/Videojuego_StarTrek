# F11-P05-A02-03 — Preimplementación segura del emisor institucional

**Fecha:** 2026-11-11
**Estado:** revisión de código y plan de ejecución, **sin emisor implementado**.
**Naturaleza:** handoff para revisión e implementación nativa; no certificado de producto, Core o Unreal.
**Referencia base verificada:** `main` `816e72b2b6e2057c47b84473e616a6feda096016` (PR #108 y #109 fusionadas).
**Alcance de esta entrega:** únicamente nuevos documentos y matriz de aceptación. NO toca módulos, cabeceras, CMake, CI, guardados, pins, históricos ni `ESTADO_GLOBAL.json`.

## 1. Estado observado en código real

| Archivo/área | Constatación |
|---|---|
| `desarrollo/integration/f11/src/f11_trial_host.inc` | Solo el binario `TrekF11TrialHost` emite graduación, comisión, grant, evaluación y orden del escenario. Compila bajo `F11_NATIVE_TEST_HOST`; NO se debe trasladar al producto. |
| `desarrollo/integration/f11/src/f11_promotions.inc` | `f11_commit_promotion` comprueba hechos, autoridad, rango exacto 1101→1102, revocaciones y revisión; publica una copia completa de `Campaign` de forma atómica. NO crea antecedentes institucionales. |
| `desarrollo/integration/f11/src/f11_schema.inc` | `f11_root` exige `CAUSE=110501`, marcador del ensayo y **no autenticación**; compatibilidad histórica no equivale a confianza de entrada. |
| `desarrollo/integration/f04/src/f04_bridge.cpp` | `f04_save/f04_load` usan la serialización/deserialización Core y el validador relacional `schema`. No existe autenticación criptográfica de procedencia del archivo en esta API. Carga cambia `scope`; un `F04Ref` no es credencial. |
| `desarrollo/integration/f04/unreal/F04CampaignSubsystem.cpp` | `UF04CampaignSubsystem::Load` permite cargar bytes aportados por un llamador del laboratorio. Tampoco representa al Host institucional real. |
| `juego/UE5/StarTrekRPG/README.md` | La carpeta del juego principal declara que aún no existe `StarTrekRPG.uproject`; cualquier UE5 final debe esperar a un proyecto auténtico verificable. |
| `desarrollo/integration/f11_host/` | La PR #109 ya proporcionó lector C++20 de producto, aislado, sin emisor. Pruebas 17/17 GNU y 17/17 MSVC en CI de PR. |
| Pins históricos | Core F05 `76a7b7b485616d8c4994f384a90f123bf333591d`; F04 historia `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`. Inmutables para esta tarea. |

### Distinción esencial

- **Consistencia del grafo**: Core puede comprobar que los hechos se relacionan coherentemente.
- **Autenticidad institucional**: el Host debe establecer *antes* de emitir/aceptar hechos quién autoriza, con qué competencia, respecto de quién y bajo qué origen de partida. **Ninguna referencia numérica, campo `verified`, checksum, contraseña incrustada o `CAUSE=110501` acredita eso.**
- **Seguridad de juego local**: un programa completamente controlado por el propietario de su ordenador no es resistente a un adversario que modifique el ejecutable/memoria. Antes de prometer antifalsificación fuerte, decidir si buscamos **integridad interna del gameplay local** o **autoridad verificable externamente**; la segunda necesita una raíz de confianza fuera del control del cliente (p. ej., servicio remoto o una plataforma segura adecuada). No agregar infraestructura externa de improviso.

## 2. Arquitectura mínima a revisar, NO realizada

Flujo objetivo: `fuente de identidad/procedencia del Host` → `servicio privado de Personal de Flota` → `transacción CoreRPG WorldState de hechos` → `f11_commit_promotion` → `f11_host_reader` → futura presentación UE.

### Frontera de lectura/entrada

1. El **Host dueño de la sesión** acepta únicamente su principal autenticado e identifica su partida. No acepta actores/autorizaciones/derechos fabricados por diálogo, Blueprint, LLM, consola o archivo JSON.
2. El subsistema de guardado debe clasificar expresamente los archivos por **origen confiable**; `f04_load` prueba forma y consistencia, no autenticidad. Un archivo externo puede importarse en modo histórico/diagnóstico, pero **no puede mintar competencias institucionales**.
3. No publicar `f11_test_create`, `f11_test_revoke` o `f11_test_fault` en producto. No introducir API genérica `f11_issue_grant(verified=true)`; la decisión de Personal debe construirse desde una dependencia que el cliente no pueda suplir con un parámetro.

### Servicio institucional

1. Operación **privada**, no consumible desde UI/AI/Blueprint/registro editable del jugador. Modelo de datos: sujeto (identidad 128b), oficio/autorizador, competencia para la transición 1101→1102, ventana de validez, graduación certificada, comisión, evaluación, orden, causa y revocación.
2. Crear `f11_root`, `f11_office`, `f11_grant`, `f11_graduation`, `f11_commission_order`, `f11_commission`, `f11_evaluation`, `f11_cause`, `f11_personnel_order` y referencias en el **mismo** `WorldState`; no mantener un expediente lateral de autoridad.
3. Preparar el conjunto de hechos sobre copia temporal `Campaign`; `schema(next)`, comprobar revisión, fuente de autorización y condiciones vigentes justo antes de publicar; `swap` único. Si falla, bytes Core, reloj, RNG, revisión y asignaciones permanecen intactos.
4. **No** reetiquetar ni reutilizar el marcador de ensayo `CAUSE=110501` para producto. Versionar nueva procedencia de raíz y definir migración o convivencia con los históricos, sin alterar el contrato ya certificado de A02-02.
5. Emisión y revocación deben respetar la semántica histórica: revocación antes de un commit, incluso en su mismo tick, bloquea; revocación posterior al commit no elimina el evento histórico válido. Nunca reinterpretar replay idempotente como autorización nueva.
6. El grado es **diferente** del puesto y del mando: el ascenso no traslada nave, no asigna camarote/puesto, no asciende al mando ni modifica funciones de servicio.
7. Aunque exista un primer ascenso, los criterios completos de mérito y evaluación futura corresponden a P05-B1; no fabricar un expediente académico ni conceder el ascenso simplemente por pasar tiempo. Para ensayo de integración se exige **fuente de graduación institucional verificable**, no un botón o un NPC que diga «aprobado».

## 3. Plan de Codex en pequeños cortes auditables

**Corte A — arquitectura y amenazas (obligatorio antes de editar producción).** Localizar en el repositorio/ordenador el Host realmente propietario de sesiones; diferenciar `F02CoreLab`, `F04CampaignSubsystem`, `F05OrdersLab` de juego principal. Proponer modelo de confianza y guardados. Resolver si hay una fuente de autoridad externa o si la garantía buscada es coherencia interna en un juego local. Entregar diseño exacto y riesgos. **No introducir emisión si la fuente de autoridad sigue sin identificarse.**

**Corte B — emisor privado + pruebas de integridad.** Crear una rama y PR Draft de implementación aislada desde `main`, con un único sujeto de test autorizado, sin exports de ensayo ni API libre de concesiones. Pruebas de procedencia, competencia, identidad, ventanas, revocación, conflictos, simultaneidad, idempotencia y rollback. NO alterar fuentes/auditorías históricas para colorear de verde las pruebas.

**Corte C — persistencia/autenticidad.** Guardar y recuperar en **otro proceso**; importar guardado manipulado o de origen desconocido debe negarse para *nueva emisión*. Un archivo con checksum correcto y grafo coherente no constituye autoridad. Sin una política de confianza real, mantener emisor desactivado.

**Corte D — regresión y Unreal.** Ejecutar GNU + MSVC, nuevas pruebas y los 17 casos del lector, F04/F05, seis campañas históricas, y solamente si existe un proyecto UE real, NullRHI/D3D12 y prueba interactiva en MSI. No declarar `UE5_JUGABLE` si `.uproject` no existe.

## 4. Matriz verificable y criterios de cierre

Archivo adjunto en control de versiones:
`proyecto/docs/decisions/F11-P05-A02-03_MATRIZ_PRUEBAS_EMISOR_v0.1.json`.

Cada escenario tiene identificador estable, expectativa, evidencia requerida y estado inicial **NOT_RUN**. Un documento no cuenta como test ejecutado; Codex deberá enlazar cada caso con una prueba C++/CI real. Para aceptar el punto 2, deben estar verdes los casos críticos y debe existir evidencia de qué se ejecutó y dónde. No se puede dar por certificado HOST_07 sin UE5 real.

## 5. Protección de originales

- Sin modificaciones en `desarrollo/integration/f04`, `f05`, `f11` ni `f11_host`.
- Sin actualizaciones de CoreRPG, pins, oráculos, seis campañas históricas, certificados A02-02 o `ESTADO_GLOBAL.json`.
- Sin infraestructura de backend añadida, credenciales embebidas, cambios de acceso ni alteraciones de modelos Unreal/Blender.
- Sin commits de resultados temporales, binarios, `.f04`, logs o directorios de laboratorio.
- Esta entrega es **preparación documentada únicamente**. No ejecuta pruebas de producto ni certifica seguridad absoluta.

## 6. Estado para continuidad

**Pendiente:** diseño firmado de la frontera de confianza (corte A), implementación de emisor privado (B), política de autenticidad y recuperación (C), CI y Unreal final (D). F11-P05-A02-03 sigue **ABIERTA**, y la F11 general no se declara terminada.
