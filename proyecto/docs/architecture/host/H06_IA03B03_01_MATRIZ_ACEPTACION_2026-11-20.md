# HOST IA-03B03-01 — Matriz de aceptación del vínculo y SAVE/RESTORE Academia

**Fecha:** 20-11-2026 · **Estado:** ORÁCULOS DE DISEÑO / **NO EJECUTADOS**.  
**Responsables:** ChatGPT prepara y audita; Codex implementa/prueba IA-03B03-02/03.  
**Contexto:** #188/#189 fusionadas; \`AcademyCandidateFactory\` B02 crea una sola PERSON real como \`CANDIDATE\` sin vínculo/guardado. La matriz B01 B03-01…B03-12 permanece vigente; esta tabla la precisa y añade casos de riesgo localizados en código.

## 1. Vínculo H03 y bloqueo de operaciones navales

| ID | Ensayo reproducible | Oráculo mínimo |
| --- | --- | --- |
| **B03-01** | Crear PERSON con B02, pasar recibo **privado** al vínculo H03 Academy | \`current_player\` reconoce mismo \`person_id\` y \`generation\`; una sola identidad; no \`f05_bind_player\` |
| **B03-02** | Vincular Academy y pedir \`query_view\`, \`submit_order\`, \`query_order\`, \`cancel_order\` e \`institutional_command\` | Todas denegadas **antes** de \`bridge::dispatch\`; cero llamadas a F05 con \`session_==nullptr\`; sin hechos, rango o plaza nuevos |
| **B03-03a** | Solicitar vínculo dos veces con el mismo recibo en la generación vigente | Idempotencia: mismo sujeto, mismo vínculo, revisión Core no se altera por repetición |
| **B03-03b** | Seleccionar ID numérico ajeno, recibo de otro owner, perfil o intento | Rechazo de ámbito/identidad, nunca vincula otra PERSON; no aceptar ID cliente |
| **B03-03c** | \`close()\` durante petición de vínculo y consultar desde generación antigua | Revocación inmediata de generación y recibos; no reactivar identidad al terminar callback |
| **B03-03d** | Una llamada \`current_player\` con vínculo Academy y luego una llamada naval desde esa identidad | Proyección del mismo sujeto; comprobación de competencia por tipo *en cada operación*, no por estar BOUND |
| **B03-03e** | En paralelo intentar segunda creación B02, sustitución de perfil y vínculo | Un solo principal/persona y campaña; no duplicado, rechazo ordenado sin estado intermedio público |

## 2. Guardado y recuperación H04

| ID | Ensayo reproducible | Oráculo mínimo |
| --- | --- | --- |
| **B03-04** | Vincular Academy, \`SAVE\`, cerrar proceso 1; lanzar proceso 2 con misma raíz H04 y \`RESTORE\` | Misma campaña UUID, PERSON, nombre, fuente S04, antecedentes, hecho de candidatura, estado \`candidate\`, RNG y reloj; nueva generación H02, identidad H03 BOUND |
| **B03-05** | Guardar Academy y navegar slots antiguos navales \`TREKHOST4 1\` | Todos los slots navales previos conservan lectura/restauración intactas; no transformación de perfiles |
| **B03-06** | Pedir LOAD naval de un slot Academy y LOAD Academy de un slot naval | Rechazo explícito por tipo, sin abrir Miranda como Academia ni dañar sesión activa |
| **B03-07** | Alterar nombre/persona/hecho/S04 source digest/catálogo en sobre o en Core | No se confía en metadatos solos; rechazo al comparar estado Core, sin swap |
| **B03-08** | Cargar desde otro proceso con ID Core ordinal coincidente pero **otro UUID** de campaña | Rechazo de identidad; no basta \`person_id=2\` u otro ordinal |
| **B03-09** | \`SAVE\` con fallo inyectado en snapshot, copia, manifiesto, sync, rename COMMITTED, confirmación | Antes de COMMITTED no hay éxito parcial; anterior sigue recuperable; incertidumbre publicada se informa como \`PUBLICATION_UNCERTAIN\` sin auto-sobrescribir |
| **B03-10** | Dos SAVE consecutivos y LOAD repetidos del mismo slot | Misma PERSON/hecho; nuevas versiones de ranura, sin nueva candidatura; no reingreso automático |
| **B03-11** | Versión más reciente confirmada corrupta pero versión anterior íntegra | \`version=0\` no retrocede silenciosamente; selector explícito puede recuperar anterior si procede |
| **B03-12** | Slot antiguo de personaje libre, humano/vulcano/mixto, o biografía incompatible | No reescritura oculta al héroe Khan; no cambia contratos v1 |
| **B03-13** | Reanudar con source S04 v2 desconocida/modificada o pin Core distinto | \`SAVE_INCOMPATIBLE\`/rechazo controlado; no fabricar nueva fuente ni actualizar pin |
| **B03-14** | Guardar sin vínculo H03 válido, con permiso inválido, slot mal formado o registry desconocido | Rechazo previo a publicación; importado no recibe \`KNOWN_LOCAL\` sin constancia de registro |
| **B03-15** | Restaurar archivo con PERSON ausente, hecho \`candidate_created\` sin sujeto, dos PERSON jugables o historia truncada | Rechazo antes de publicar; sesión válida existente permanece intacta si la política admite swap |
| **B03-16** | Restaurar desde CLOSED y repetir después de otro cierre, solicitando recibo de B02 anterior | No se recrea PERSON, se reconstruye el vínculo desde Core; puntero/recibo anterior inválido |
| **B03-17** | Restaurar una Academy \`ACTIVE\` (si se admite) y simular fallo a mitad | Sesión anterior intacta; si esta operación no se admite, denegación previa explícita y documentada |
| **B03-18** | Cambio de mundo/generación lógico o \`CLOSE\` concurrente con LOAD | Cierre prevalece; sin \`ACTIVE\` resucitada; solicitudes y proyecciones viejas denegadas |
| **B03-19** | Inspeccionar raíz con slots Academy, naval, importado y corrupto | Tipo, versión y recuperabilidad correctos; sin marca \`KNOWN_LOCAL\` injustificada |
| **B03-20** | Snapshot con revisión/tick nuevo tras evolución legal de campaña simulada | El ancla inmutable sigue siendo válida; versión nueva no queda bloqueada por revisión/tick original |
| **B03-21** | Repetir/ver/saltar intro tras restore, sin evento de F10 de admisión | No crea segunda PERSON, hecho, plaza ni ingreso; sigue \`candidate\` |
| **B03-22** | Intentar restaurar un \`admitted\` sin hecho F10 autorizado o con plaza declarada por UI | Rechazo; no se admite a nadie en B03 ni se crea cohorte ficticia |

## 3. Regresiones, evidencias y niveles de cierre

| Puerta | Evidencia requerida | Estado hoy |
| --- | --- | --- |
| **G1 — vínculo Academy** | B03-01, B03-02, B03-03a…e y regresiones H03 navales | **NOT_RUN** |
| **G2 — durabilidad real** | B03-04/06/07/09/10/13/14/15/16 y proceso nuevo, verificación Core genuina | **NOT_RUN** |
| **G3 — convivencia legacy** | B03-05/08/11/12/17/18/19/20/21/22, antigua suite H04 y F05 | **NOT_RUN** |
| **G4 — integración nativa** | CTest relevante Windows/Linux, ASan/UBSan, \`TREK_HOST_TESTS=OFF\` Release con DLL ABI y producto sin símbolos de test; F11 aislado | **NOT_RUN** |
| **G5 — UE5 y hito M1** | Prueba manual MSI/Unreal 5.8.4 y NullRHI/D3D12, onboarding y reanudación | **FUERA DE B03 — IA-03C** |

**Importante:** G2 requiere recuperación verificable **entre dos procesos distintos**, no serializar/deserializar en memoria y declarar SAVE/RESTORE completado.

### Casos históricos B01 conservados

La matriz \`H06_IA03B01_MATRIZ_ACEPTACION_2026-11-20.md\` ya establece B03-01…B03-12. Esta matriz B03-01 **amplía la cobertura técnica**, y los identificadores con sufijo (B03-03a…e) o el criterio equivalente B03-04 de la presente son subensayos. Codex mantendrá trazabilidad cruzada en su informe en vez de afirmar que renumerar pruebas equivale a ejecutarlas.

## 4. Oráculos de no duplicación, autoridad y rendimiento razonable

- **No duplicación de PERSON:** una por campaña, la misma tras LOAD; el sujeto de otra campaña es una identidad distinta aun con mismo ordinal.
- **No duplicación de Core:** una sesión Academy activa, un WorldState, un catálogo aprobado; staging no genera una segunda campaña publicada.
- **No duplicación de historia lógica:** cada hecho canónico representa su fuente/antecedente una vez y puede referenciarse. Los snapshots/versiones físicos pueden repetir bytes legítimamente para recuperación, sin requisito de deduplicación física prematura.
- **No duplicación de permisos:** \`BOUND\` expresa control del sujeto, **no** acceso al puente naval, F11 o acto institucional.
- **Sin exceso de seguridad:** juego privado/local; verificar integridad, procedencia, estructura y límites existentes H04 sin DRM, servidores ni firmas obligatorias.
- **Límites operativos:** respetar cotas H04 existentes, no cargar indefinidamente una campaña por repetir SAVE/RESTORE y no bloquear el hilo de Unreal (integración UE posterior).

## 5. Evidencia que deberá entregar Codex

Informe permanente en \`proyecto/docs/architecture/host/\`: PR y HEAD, commit base, nuevas interfaces, formato de sobre (magic real), migración/registro, comandos de compilación, pruebas con números concretos por plataforma, CI URLs/SHA, salida de test multiproceso, inyección y preservación de slots navales. Evidencia temporal únicamente en \`laboratorios/host/ia03b03/\`, excluida de Git, sin borrar nada preexistente.

**Ninguna prueba de esta matriz se ha ejecutado por elaborar B03-01.**
