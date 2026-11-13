# H06-P06 — Matriz de aceptación del bootstrap productivo del cadete

**Fecha:** 13-11-2026. **Responsable matriz:** ChatGPT.  
**Estado global:** PLANIFICADA / todos los casos NOT_RUN. No interpretar pruebas Python F10, H05 fixture o H06 diagnóstico como un PASS productivo.  
**Contrato:** H06_P06_CONTRATO_BOOTSTRAP_CADETE_2026-11-13.md.  
**Fuentes:** H03/H04/H05/H06 fusionados, F10 de referencia, contrato de personaje y Academia, pin CoreRPG 76a7b7b485616d8c4994f384a90f123bf333591d.

## 1. Puertas

| Puerta | Propósito | Estado de partida |
|---|---|---|
| P06-G0 | F10 aprueba responsabilidad de admisión, fuente de perfil, condiciones y contexto de campaña | PENDIENTE DE COORDINACIÓN |
| P06-G1 | Alta autoritativa Core de candidato/cadete real, identidad y plaza únicas, sin fixture | NOT_RUN |
| P06-G2 | H03 enlaza único sujeto correcto por flujo interno sin autoridad F05 inventada | NOT_RUN |
| P06-G3 | H04 guarda/carga y resuelve el mismo sujeto/estado entre procesos, revocando generaciones | NOT_RUN |
| P06-G4 | ABI C/Unreal usa intents y proyecciones limitadas; no receptor/ejecutor ni setter de identidad | NOT_RUN |
| P06-G5 | Regresiones y pruebas UE MSI documentadas con revisión exacta | NOT_RUN |

## 2. Matriz de pruebas

| ID | Caso y oráculo esperado | Capa mínima | Estado |
|---|---|---|---|
| CB-01 | Nueva campaña de Academia con contexto, cohorte y población definidos por F10, **no** por miranda/f04_create sintético | F10/Core, nativo | NOT_RUN |
| CB-02 | Perfil campaign_created válido genera un sujeto PERSON real, estable y un único registro de creación en Core | F10/Core, nativo | NOT_RUN |
| CB-03 | Candidato no admitido permanece CANDIDATE; la UI no puede marcarlo admitido mediante flag/campo | F10/Core, UE | NOT_RUN |
| CB-04 | Admisión legítima deja cadet_year_1 y ocupa una plaza real con conservación total/latent; sin duplicados | F10/Core, nativo | NOT_RUN |
| CB-05 | Repetir misma petición y misma intención de alta devuelve la misma persona/resultado; no duplica identidad, plaza o historia | F10/Core, nativo | NOT_RUN |
| CB-06 | Clave repetida con perfil diferente → conflicto sin cambios; no recicla un ID | F10/Core, nativo | NOT_RUN |
| CB-07 | Recursos/plazas agotadas, conflicto canónico o biografía inválida → rechazo íntegro sin restos visibles | F10/Core, nativo | NOT_RUN |
| CB-08 | Fault injection antes de publicación de creación/matrícula → no hay PERSON/slot/registro parcial ni consumos de RNG indebidos | F10/Core, fallo | NOT_RUN |
| CB-09 | F04Ref y revision provienen del Core del mismo owner; no se admiten ID arbitrario ni scope de otra campaña | HOST/H03, nativo | NOT_RUN |
| CB-10 | Dos GameInstances/intentos concurrentes → un único vínculo ganador y una única campaña activa según H02 | HOST/H03, C ABI | NOT_RUN |
| CB-11 | Cadete vinculado puede consultar su proyección propia, sin visualizar información oculta de compañeros | HOST/H03, UE | NOT_RUN |
| CB-12 | Cadete sin rol F05 legítimo no puede emitir órdenes de nave, con rechazo y sin mutación/RNG | F05/HOST, UE | NOT_RUN |
| CB-13 | No existe API de producto para mutar PERSON/issuer/receptor, autoridad F11 ni vínculo arbitrario desde Blueprint, IA o cliente C | ABI/UBT, estática+nativa | NOT_RUN |
| CB-14 | CLOSE durante creación o bind invalida resultado, ticket, generación y proyección tardíos, sin nueva sesión fantasma | HOST/H03/H06, nativo+UE | NOT_RUN |
| CB-15 | LOAD durante una operación revoca ticket anterior y la respuesta no se aplica a un UWorld viejo | HOST/H04/H06, UE | NOT_RUN |
| CB-16 | SAVE confirma COMMITTED y contiene identidad real de jugador, slot/cadete e historia; no duplicados en almacenamiento lateral | H04, nativo+UE | NOT_RUN |
| CB-17 | RESTORE en proceso nuevo reabre misma campaña y mismo PERSON/slot/expediente con scope y generación nuevos | H04/Core, nativo+UE | NOT_RUN |
| CB-18 | Guardado extranjero, alterado, corrupto o identidad distinta → denegación sin publicar acceso ni sustituir partida válida | H04/H03, nativo | NOT_RUN |
| CB-19 | Legacy H04 Miranda/F05 sigue cargando sin reinterpretar tripulante como cadete ni migrarlo en silencio | H04/H05, nativo | NOT_RUN |
| CB-20 | Vínculo de cadete no equivale a rango F11, comisión, acceso de Personal ni orden institucional; SERVICE_UNAVAILABLE si aplica | F11/H07/HOST, nativo+UE | NOT_RUN |
| CB-21 | UE Win64 Editor+Game UBT/UHT, NullRHI y D3D12 verifican alta/denegación/consulta; dos UWorld y map travel preservan identidad | Unreal MSI | NOT_RUN |
| CB-22 | Pruebas nativas nuevas Windows/Linux, ASan/UBSan y Release OFF; no regresión de 238/238 y 83/83 previas | CI | NOT_RUN |
| CB-23 | Limpieza de laboratorio propio no rompe reconstrucción nativa/UE desde Git y Core fijado | MSI+fuentes | NOT_RUN |
| CB-24 | Identidad genérica precomisión y profesional F11 reconciliadas documentalmente: no inventar comisión durante matrícula | Contrato F10/F11 | NOT_RUN |

## 3. Evidencia exigida antes de aprobar

Registrar por caso: commit SHA exacto, comando, entorno, estado PASS / FAIL / BLOCKED / NOT_RUN, evidencia enlazada, función propietaria, hechos antes/después (revisión, entidades, plaza, idempotencia, historial y RNG cuando proceda), y comprobación de no filtración.

El bootstrap es **una mutación crítica**: los tests deben inspeccionar el estado Core y H04, no limitarse a contar botones o a confirmar un mensaje de éxito en Slate. El usuario del cliente no elige person_id, F04Ref, trusted_origin, F11CharacterId, permisos ni la revisión actual del servidor.

Las suites antiguas H06 (238/238 nativo, 83/83 sanitizers) son referencia de regresión, NO pruebas P06 ejecutadas. La matriz solo cambia a PASS cuando exista evidencia nueva verificable.

## 4. Independencia de laboratorios

Los informes de resultados, la matriz consolidada y los scripts de prueba que pasen a producto deberán ser pequeños y quedar versionados bajo desarrollo/ o proyecto/docs. Compilaciones, logs, saves de ensayo y capturas: exclusivamente en la zona temporal ignorada indicada por AGENTS.md, sin dependencias desde los archivos definitivos. La limpieza concurrente no borrará subcarpetas mientras haya herramientas activas. No realizar ningún borrado con esta fase.

## 5. Criterio de cierre P06

Se permite un resultado parcial honesto si F10/Core no ofrece todavía un factory productivo de campaña Academy o si el contrato H03/F05 necesita una extensión aprobada. En ese caso: documentar el bloqueador con pruebas de inspección; no marcar CB-01..CB-24 PASS; no activar una identidad de ensayo, ni forzar P07, ni afirmar M1. P07/P08 solo continúan cuando las puertas relevantes quedan realmente satisfechas.
