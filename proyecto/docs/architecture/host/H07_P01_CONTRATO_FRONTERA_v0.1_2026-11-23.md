# H07-P01 — Contrato de frontera HOST ↔ F11 v0.1 (preparatorio)

**Fecha:** 23-11-2026. **Estado:** DISEÑADO para revisión; NO es una API ya implementada.
**Titular del dominio:** F11/Star Trek sobre CoreRPG. **Titular del transporte/admisión:** HOST.
**Ámbito inicial:** un jugador, ejecución local, lectura de hechos F11 confirmados y rechazo seguro de emisión no disponible.
**No altera:** f11_promotions.h, ABI H06, F11TrialHost, CoreRPG, pins o histórica A02-02.

## 1. Contratos de código inspeccionados (existentes, no propuestas)

- F11 producto: f11_personnel(F04Session*, F04Ref, F11PersonnelView*), f11_promotion(F04Session*, F04Ref, uint64_t event, F11PromotionView*), f11_commit_promotion(F04Session*, const F11PromotionRequest*, F11PromotionReceipt*).
- Lector privado: trek::f11_host::career(F04Session*, F04Ref, Career*) y trek::f11_host::promotion(F04Session*, F04Ref, uint64_t, Promotion*). Limpia salida inicial y exige coincidencia de identidad y visibilidad en la proyección; presupone que un HOST externo ya autorizó sujeto y divulgación.
- HOST: SessionOwner (Generation opaca y current_player); SessionOwner::institutional_command(Generation, correlation) **devuelve SERVICE_UNAVAILABLE en NativeSession** si supera admisión y vinculación, sin llamar al puente. La Academy no pasa el control Dispatch naval.
- C ABI HOST: operaciones OPEN, CLOSE, QUERY_VIEW, SUBMIT_SCAN, QUERY_ORDER, CANCEL_ORDER, SAVE y RESTORE; **no existe operación C ABI de emitir F11**.
- F11 productiva actual solo confirma el ascenso 1101→1102 con antecedentes ya emitidos. TrekF11TrialHost y f11_bootstrap_authorized_trial son solo de ensayo.
- Lectura de hechos F11 exige un F04Session con esquema F11 activado. AcademyCampaign H06 no es, por ahora, ese F04Session de oficial comisionado.

## 2. Modelo lógico propuesto (NO una firma C ni un nuevo endpoint)

Petición de lectura: {generation, correlation, kind=PERSONNEL|PROMOTION, event_id?} ingresada en el HOST, **sin F04Ref, grant, subject, character_id ni bandera verified seleccionables por cliente**. HOST resuelve en sesión propia: origen, campaña, principal vinculado, objeto Core, tipo de campaña, generación, hilo y perspectiva. La salida contiene únicamente proyección permitida y revisión Core, no un recibo de emisión.

| Precondición / fallo | Resultado lógico previsto | Efecto |
|---|---|---|
| Sin sesión | SESSION_CLOSED | Salida vacía, cero Core |
| Generación distinta / callback tardío tras restore | GENERATION_EXPIRED | Salida vacía, descartar |
| Guardando/cargando/cerrando | BUSY_STATE o expiración según H02/H04 | No acceder a sesión retirada |
| Sin principal vinculado | PRINCIPAL_UNBOUND | No consultar F11 |
| Academy sin comisión F11 | Sin expediente de oficial / denegación o no disponible según API real | No sintetizar rango ni convertir cadete en oficial |
| Sujeto ajeno o visibilidad no autorizada | ACCESS_DENIED o error de dominio correspondiente | Borrar salida |
| F04Session no preparada con F11 | SERVICE_UNAVAILABLE (capacidad) | No saltar a lector de ensayo |
| Persona legacy o no comisionada | F11_UNCOMMISSIONED (si F11 lo devuelve) | Sin expediente falso |
| Scope/observador caducado | Error F04/F11 preservado internamente; error HOST adecuado | No recuperar con ID de cliente |
| Evento ajeno / identidad discrepante | Denegación con buffer vacío | No filtrar otros expedientes |
| Consulta permitida | Vista del Core; misma revisión, RNG y tick | Cero mutación |
| Emisión institucional sin emisor producto autorizado | SERVICE_UNAVAILABLE | Cero mutación y ningún fallback |
| Error de buffer, excepción o fallo posterior a proyección | Error y salida limpiada | No entregar objeto parcial |

Los nombres de resultado son **semánticos** de diseño: verificar y codificar los mapeos exactos en P02/P03. No inventar valores ABI ni agregar un indicador de permiso sobre la base de la lectura.

## 3. Propiedad y exposición

- **Unreal / PADD / NPC / LLM:** consumen solo vista autorizada que el HOST proyecta. No reciben F04Session*, concesión ni acceso a f11_commit_promotion; tampoco se les permite seleccionar observador profesional para leer a terceros.
- **HOST:** verifica sesión/generación/binding/ruta/canal, mantiene correlation_id, solicita a F11 consultas o operaciones aprobadas. No crea ni almacena RANK, GRANT, destino, competencia, evaluación o expediente en sidecar.
- **F11:** define visibilidad profesional, validez de cada objeto institucional, autoridad, revocación, idempotencia de promociones y semántica del evento. Incluso cuando HOST admite una intención, F11 debe revalidar todo.
- **CoreRPG:** persiste persona, comisión, rango, evento y decisiones confirmadas. La vista UI se reconstruye de Core. Una presentación cinematográfica o un futuro presented_at no modifica retroactivamente effective_at.

## 4. Acuerdo de composición y compatibilidad

El archivo desarrollo/integration/host/CMakeLists.txt excluye F11_ENABLE_PROMOTIONS e incorpora src/f04_host_bridge.cpp como única unidad del puente. El lector standalone desarrollo/integration/f11_host/CMakeLists.txt incluye ../f11 como subproyecto y ese subproyecto define la biblioteca TrekF11TrialHost. Por tanto:

1. **No** usar add_subdirectory(f11_host) a ciegas en producto ni forzar compilación/enlace del trial.
2. **No** eliminar el guard H02 sin justificar y probar una nueva composición opt-in con la misma unidad de traducción y ABI.
3. Si se necesita una composición de producto F11-enabled, diseñar un target separado o un cambio de feature flag trazable en Codex, con inspección de exports/defines para demostrar que el emisor de ensayo no entra en el binario.
4. Reutilizar la implementación del lector; no copiar reglas de f11_schema.inc/f11_promotions.inc a HOST.
5. Mantener el pin Core fijado y las pruebas históricas intactas. Si cambia un contrato histórico, realizar su reauditoría propia, no editar checksums para silenciarlo.
6. Preservar tamaño/layout de la ABI C de H06; las futuras capacidades institucionales públicas requieren revisión explícita y negativa por defecto.
7. Guardados H04 preexistentes deben seguir abriéndose y preservando bytes de hechos no relacionados; una campaña legacy no gana comisión por migration implícita.

## 5. Procedencia y límites de confianza

- CREATED_LOCALLY y KNOWN_LOCAL son estados de persistencia HOST, **no acreditaciones de Flota**. Una campaña local creada sin antecedentes F11 aprobados no contiene autorización institucional.
- IMPORTED_UNVERIFIED no habilita un canal de mutación profesional, aunque su checksum Core sea correcto; no elevarlo silenciosamente.
- CAUSE=110501 indica raíz histórica del ensayo; **no es autenticación**. No usarlo para crear autorizaciones de producto ni admitir solicitudes de cliente.
- Control local proporcional: evitar errores accidentales y superficies indirectas de autoridad. No prometer defensa frente al dueño que modifica ejecutable y archivos de forma arbitraria.

## 6. Casos clave de ejemplo (conceptuales)

**Caso A — cadete:** el protagonista creado por la Academia pulsa «Expediente de oficial» antes de graduarse. HOST no le inventa insignia, comisión ni número profesional; indica que el expediente de oficial aún no existe, según la respuesta real disponible.

**Caso B — oficial real:** una campaña F04 con expediente F11 confirmado se restaura por H04; HOST verifica binding y scope en el hilo propietario, invoca lector F11, muestra al propio oficial datos de Core y deja idéntica la revisión antes/después.

**Caso C — falsa orden:** una conversación con NPC solicita subir al teniente a capitán. HOST no convierte texto en concesión; responde SERVICE_UNAVAILABLE si no hay API institucional productiva. Aunque existiera, la competencia final sigue siendo de F11.

**Caso D — restauración:** una consulta encolada con generación antigua termina después de un LOAD. Su salida se descarta; nunca se asocia al nuevo principal solo porque el ID numérico coincide.

## 7. Condiciones de aprobación del contrato

- Se verifican CMake, firmas, tipos, prohibición de emisión y diferencias entre Academy/F04 productivo.
- P02/P03 concretarán estructura, error mapping, threading y ABI sin exceder este sobre. Cualquier conflicto con cabeceras reales se resuelve actualizando la versión documental antes de programar.
- P04 matrizará pruebas HOST locales y los 33 escenarios de F11 Draft por separado.
- P05 solo podrá certificar el comportamiento realmente probado; la ausencia de emisor impide certificar mutaciones y progresión institucional.

**Estado:** DISEÑO. No se ha implementado aquí ningún endpoint, conexión UE, test C++ ni cambio Core.
