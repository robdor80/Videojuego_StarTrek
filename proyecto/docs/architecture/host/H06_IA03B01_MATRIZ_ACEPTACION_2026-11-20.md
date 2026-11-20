# HOST H06 / IA-03B01 — Matriz de aceptación futura IA-03B02/B03 y M1

**Fecha:** 20-11-2026. **Propietario de diseño:** ChatGPT. **Estado de todos los casos B y C:** PROPUESTOS / **NO EJECUTADOS**. La publicación de esta matriz **no significa PASS**. Las pruebas de IA-03A y del ensayo CoreRPG tienen evidencias propias previas y NO acreditan estos recorridos productivos.

**Fuentes:** DEC-0022 y S04 v2; contrato conceptual H06_IA03B01_CONTRATO_INTEGRACION_v0.1.json; f10_host_candidate_factory_contract_v0.1.json; F10_H06_P06_FACTIBILIDAD_NATIVA; H03, H04, IA-03A y H06. Pin CoreRPG 76a7b7b485616d8c4994f384a90f123bf333591d.

## 1. IA-03B02 — fuente autoral, F10, factory Core

| ID | Entrada / acción | Resultado obligatorio | Observabilidad mínima |
| --- | --- | --- | --- |
| **B02-01** | Nueva partida sin elegir especie/sexo/edad/biografía; nombre válido | F10 selecciona fuente S04 v2 **interna**, híbrido varón 45 en 2383; sin una sola alternativa | Datos emitidos desde fuente autorizada; no de UI |
| **B02-02** | Repetir con nombre diferente en **otra campaña nueva** | Mismo arquetipo y hechos base, nueva PERSON/identidad de campaña | Identidad Core distinta, contenido canónico equivalente |
| **B02-03** | Mismo intento y mismo nombre repetido tras timeout o doble clic | Una PERSON y un hecho de candidatura, mismo resultado | Recuento de entidades/hechos; clave de idempotencia interna |
| **B02-04** | Misma clave de intento con nombre o payload distinto | CONFLICT sin nueva PERSON ni efectos parciales | Revisión/entidades/historia sin cambios |
| **B02-05** | Cliente envía species_id human o vulcan, edad 20, sexo distinto, ascendencia alternativa | Rechazo de campos inmutables, cero PERSON | Rechazo objetivo previo a mutación |
| **B02-06** | Cliente intenta person_id, campaign_id, generation, source_digest, emisor o approval=true | Rechazo; ningún ID/permiso obtiene autoridad desde cliente | Cero cambios de WorldState |
| **B02-07** | Fuente autoral F10 versión desconocida, digest incorrecto o alterada | Rechazo cerrado sin PERSON | Identidad y hash de fuente verificados |
| **B02-08** | Lugar natal/padres/títulos/música exactos sin definir en S04 | Siguen desconocidos; no aparecen hechos planetarios o diplomas inventados | Ningún origen/lugar literal o entidad no autorizada |
| **B02-09** | Fuente fija íntegra y nombre permitido, catálogo válido, policy v2 aprobada | Una PERSON de Academia + hecho candidate_created + antecedente conocido persistible, sin cadet slot | WorldState/catálogo/historial y recibo privado coherentes |
| **B02-10** | Crear candidato con IA no configurada | El contrato fijo v2 no debe producir **respuesta IA simulada**. Se permite sin API solo si F10 v2 autoriza expresamente verificación determinista de fuente canónica | Ningún fake COHERENT; comprobar que v1 sigue exigiendo IA |
| **B02-11** | Intento de reutilizar recibo IA-03A v1, scope H03 caducado o perfil de otra sesión | Rechazo sin PERSON | Generación, regla, fuente y perfil revalidados |
| **B02-12** | Inyectar fallo en preparación/publicación de catálogo, historia, PERSON o hecho | No hay campaña activa parcialmente publicada, ni PERSON huérfana en sesión | Snapshots antes/después y ausencia de efectos |
| **B02-13** | Candidato intenta acceder a órdenes F05, grado F11 o plaza por su mera creación | Sin permisos navales, rango, plaza o admisión | Negativas explícitas de sus propietarios |
| **B02-14** | Comparar fondo autoral nuevo con validación libre IA-03A histórica | Regresiones v1 intactas; no se crean hero alternativos en ruta v2 | Suites F10/IA-02/IA-03A |
| **B02-15** | Resolver PERSON por identidad ajena al intento o por campo UE no validado | Rechazo; no se vincula un tercero | Ref privado con Core revision/contexto |

**Puerta B02:** B02-01, 03–13 y 15, junto a regresiones antiguas, con pruebas nativas de producto sobre Core fijado. **No alcanza** con ejecutar academy_core_feasibility.cpp ni con que un mock cree EntityId=4.

## 2. IA-03B03 — identidad durable y H04 Academy

| ID | Entrada / acción | Resultado obligatorio | Observabilidad mínima |
| --- | --- | --- | --- |
| **B03-01** | Alta válida B02 seguida de vínculo H03 Academy | Exactly-one binding a la misma PERSON, sin f05_bind_player ni rango F11 | Identidad de campaña + PERSON comprobada |
| **B03-02** | Candidato intenta SUBMIT_SCAN/orden de puente sin competencia | Denegación sin órdenes y sin mutación de nave | Error controlado, cero efectos |
| **B03-03** | Guardar Academy y cerrar, iniciar otro proceso y restaurar slot | Misma PERSON, mismo nombre, mismos antecedentes, mismo estado candidate, misma campaña y hechos, nueva generación | Comparación de IDs Core persistentes e historia |
| **B03-04** | Guardar y cargar con estado admitted solo si hay decisión F10 real | No repetir acto F10, no consumir plaza por restore | Mismo hecho/ref/plaza, sin duplicados |
| **B03-05** | Abrir slot naval TREKHOST4 1 con lector Academy | Rechazo explícito sin reinterpretar el barco | Ninguna sesión publicada |
| **B03-06** | Abrir slot Academy con lector naval | Rechazo explícito sin pérdida de partida | Igual slot naval previo |
| **B03-07** | Archivo adulterado, versión extraña, catalogo incompatible o PERSON ausente | Rechazo sin sustituir campaña activa | Restore staged, rollback y estado anterior |
| **B03-08** | Cerrar/restaurar cambia generación, persistiendo PERSON | Los tickets, capturas y vistas UWorld viejas caducan | Generation renew y denegación de handles antiguos |
| **B03-09** | Interrupción antes de COMMITTED / fallo de sync/manifest | El último slot duradero sigue válido o no hay slot nuevo, sin publicación parcial | Marcadores H04 y recuperación |
| **B03-10** | Repetir guardado o reanudar dos veces el mismo slot | No duplica PERSON, candidatura, slot de cadete ni campaña | Recuento estable y misma identidad |
| **B03-11** | Migración silenciosa de viejo borrador de 3 especies a Khan fijo | Prohibida; no convertir saves legacy de oficio | Slot permanece intacto; rechazo/compatibilidad explícita |
| **B03-12** | Guardar biografía y fuentes una sola vez y referenciar historia | Sin 20 copias de texto, ni imágenes/audio/modelos 3D en slot | Archivo con referencias tipadas y Core autoritativo |

**Puerta B03:** identidad restaurada realmente **entre procesos** y regresión naval íntegra; no declarar compatible H04 por haber compilado F05. Tests Linux/Windows, sanitizadores, prueba de fallo de publicación y producto tests-OFF.

## 3. Futuro IA-03C / H06 M1 — no confundir con B02/B03

| ID | Entrada / acción | Resultado esperado | Situación |
| --- | --- | --- | --- |
| **C-01** | Abrir UE 5.8.4 → Nueva partida | No selector de especie/sexo/edad, nombre y cosmética permitida | Pendiente IA-03C |
| **C-02** | Ver nombre y ficha autorizada tras alta | Misma PERSON/identidad Core, sin datos privados de emisor | Pendiente IA-03C |
| **C-03** | Cerrar/reabrir desde Unreal, cambio de UWorld | Recuperación correcta y proyecciones antiguas inválidas | Pendiente IA-03C |
| **C-04** | Ver/saltar/repetir intro | Sin segunda PERSON, admisión, plaza, reputación, relación o bonificación | Pendiente IA-03C + F10 |
| **C-05** | Consejo de Janeway/Picard | No emite admisión: solo acto F10 auténtico; Sisko no participa en 2383 | Pendiente narrativa/F10 |
| **C-06** | Llegada como cadete tras prólogo | Solo si F10 ya produjo ADMITTED y matrícula; de lo contrario mostrar candidate | Pendiente aceptación M1 |
| **C-07** | UE NullRHI y D3D12 en MSI | Build y flujo real, no solo fixture M0 | Pendiente IA-03C |
| **C-08** | Consulta OpenAI LIVE real cuando exista consumidor libre que la requiera | Sin falsificar ejecución; gasto acotado y consentimiento | Pendiente hito IA global, no bloqueo para fuente fija v2 |

## 4. Instrumentación y paquetes de prueba exigibles

- F10/IA-03A: validación de fuente/edad/identidad; v1 legacy con transporte simulado y nuevas negativas v2.
- CoreRPG: publicar PERSON/candidate_created y recuperación de historia **con catálogo productivo y pin intacto**; inyección de fallo antes de publicación.
- H03/H04: persistencia y vínculo académico sin dependencia F05, compatibilidad con SAVE/RESTORE naval, invalidación de generación, slots adulterados.
- F11 aislado y F04/F05 nativos históricos sin cambiar las reglas; no usar resultados de tests de fixture como prueba Academy.
- Compilaciones producto Release con tests deshabilitados, CI Windows/Linux y ASan/UBSan cuando se implemente código; para Unreal UBT/UHT y ejecución en el MSI solo en IA-03C.

**Evidencia de B01:** exclusivamente inspección documental del repositorio y estructura contractual JSON; no se han ejecutado oráculos B02/B03/C. El responsable de cada subfase deberá anotar el HEAD real, comando, plataforma, resultados y limitaciones. Ningún PASS por inferencia.
