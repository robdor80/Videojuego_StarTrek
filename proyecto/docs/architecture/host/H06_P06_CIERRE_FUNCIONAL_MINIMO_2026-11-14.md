# HOST H06-P06 — Cierre funcional mínimo: del personaje nuevo a una partida recuperable

**Fecha:** 14-11-2026. **Responsable de esta preparación:** ChatGPT. **Estado:** DOCUMENTADO, no implementado como flujo productivo. **Objetivo:** terminar el trabajo útil de H06, no abrir otra fase ni añadir un subsistema. **Seguimiento:** issues #144 y #148. **Base examinada:** `main` en `4ce7dfb5a1c62591046a50fef64379d879d3df64`.

## 1. Resultado que queremos ver

Un jugador crea a **Daniel Torres**, humano de **20 años**, declara un pasado personal normal, confirma el personaje y comienza una campaña de Academia. Al guardar, salir y cargar de nuevo, reaparecen **el mismo personaje, la misma campaña y su estado**, sin duplicados ni cambios de identidad.

La edad se **acepta como dato ficticio declarado** y solo se contrasta contra el mínimo de especie vigente (PR #160, ruleset `f10-biography/5`). No se solicita prueba biológica individual, expediente inexistente ni IA para verificar la edad. En una biografía, «me gusta la astronomía» no genera una habilitación profesional; «soy capitán» no concede un rango.

**Candidato y cadete no son lo mismo:** crear `PERSON` como `candidate` **no** lo matricula automáticamente ni consume una plaza. Pasar a `admitted` o `cadet_year_1` requiere la decisión real del dominio F10 y una plaza cuando corresponda. No llamaremos «inicio jugable de primer curso» a una simple ficha candidata.

## 2. Inventario contrastado: no hay que reconstruirlo

| Existe ya y se reutiliza | Falta conectar de forma productiva |
|---|---|
| Proyecto UE5 principal `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`, módulo HOST, ABI C v1, GameInstance y vista diagnóstica; integración H06 PR #142 fusionada | Operación real de «Nueva partida Academia» en la ABI/Unreal |
| `SessionOwner`, un único hilo propietario de Core y cierre/cancelación por generación | Constructor de campaña Academia en el mismo dueño, sin escenario Miranda camuflado |
| Ensayo `academy_core_feasibility.cpp`: materialización de PERSON/candidato con catálogo de prueba, historial y recuperación, sin autorizar producto | Validación de perfil, catálogo y publicación F10 reales, con reintentos seguros |
| H03 `PlayerBootstrap` y comprobación de alcance/revisión para campaña de nave | Vínculo del jugador a PERSON Academia, independiente de `f05_bind_player` |
| H04 slot durable y lectura/restauración de partida naval | Guardado y restauración con discriminador/catálogo Academia y misma identidad |
| PR #160: edad mínima por especie sin «madurez individual demostrada»; A6: comprobación parcial de antecedentes personales | Resolver **solo** las fuentes o decisiones F10 que verdaderamente impidan confirmar un personaje nuevo |

Fuentes comprobadas: `AGENTS.md`, `H06_ACTA_AUDITORIA_FUSION_PARCIAL_2026-11-13.md`, `H06_P06_CONTRATO_BOOTSTRAP_CADETE_2026-11-13.md`, `F10_H06_P06_CONTRATO_INTERFAZ_ACADEMIA_2026-11-14.md`, `F10_H06_P06_FACTIBILIDAD_NATIVA_2026-11-14.md`, `f10_host_candidate_factory_contract_v0.1.json`, `biography_validation.cpp`, `native_session.h`, `player_bootstrap.h`, `host_abi.h` y el ensayo Core.

## 3. Decisiones técnicas, explicadas sin complicaciones

| Decisión | Para qué es necesaria | Qué ocurriría si no |
|---|---|---|
| **D1. Reutilizar el Core fijado, SessionOwner y el proyecto UE existente.** Nada de otro motor, worker o servidor. | Mantiene una sola partida y una sola fuente de verdad; reduce fallos y trabajo. | Podríamos acabar con dos personajes distintos o dos estados de partida incompatibles. |
| **D2. Primero crear PERSON como candidato, sin inventar admisión.** F10 conserva las reglas de Academia. | Una identidad puede existir antes de ser admitida y sin rango profesional. | «Crear personaje» concedería automáticamente plaza o galones sin haberlos obtenido. |
| **D3. Vincular el jugador a esa PERSON sin darla de alta como tripulante F05.** | H03 debe saber quién controlas; no hace falta asignarle un puesto naval. | Fingir una categoría de nave desbloquearía permisos que un candidato no tiene. |
| **D4. Guardar/cargar la campaña con su tipo y vínculo exactos.** No reinterpretar partidas de nave como Academia. | Es la única manera de continuar con el mismo personaje sin corromper saves existentes. | Podríamos abrir la partida equivocada o perder su identidad. |
| **D5. Usar una vista diagnóstica mínima ya existente antes de diseñar una UI artística.** | Probar creación, identidad y persistencia sin mezclar tareas gráficas. | Gastaríamos tiempo en pantallas bonitas sin saber si el personaje se guarda. |

**Coste:** mi parte es documental y de revisión, **cero cuota Codex**. La creación, vínculo, persistencia y Unreal de producto son integración C++/UE de riesgo real, para Codex **GPT-6, razonamiento Alto**. No más trabajos de acreditación de madurez.

## 4. Orden concreto para ejecutar, sin más subfases artificiales

1. **F10/Core — alta de candidato:** recibir un borrador válido, verificar sus reglas realmente exigibles y crear **una única PERSON** e historia en una campaña Academia. Una solicitud repetida no duplica PERSON. Si falla, no publica una partida incompleta.
2. **H03 — identidad:** vincular a ese sujeto con el jugador local; ningún ID de personaje enviado por Unreal se convierte en autoridad. Mantener el flujo naval F05 y denegar órdenes navales sin competencia.
3. **H04 — continuidad:** guardar esa campaña y el vínculo, recuperar la **misma PERSON en otro proceso** y rechazar versiones/procedencias incompatibles sin sustituir la sesión activa.
4. **H06/Unreal — extremo a extremo:** desde el proyecto real, crear, abrir vista autorizada, guardar, cerrar y recuperar. Probar además rechazo de órdenes de nave, cambio de UWorld, NullRHI y D3D12.

**Dependencia real:** el paso 2 necesita una PERSON real del 1; el 3 necesita 1 y 2; el 4 necesita los tres. El propietario de F10 mantiene la admisión; la identidad profesional F11 aparece solo al comisionar, no al crear candidato.

## 5. Único bloqueo de diseño que no hay que ocultar

La composición F10 de producto todavía devuelve `REVIEW_UNAVAILABLE` porque la revisión semántica está exigida por el contrato vigente y no existe un proveedor/verificador productivo conectado; además algunas evidencias biográficas iniciales siguen pendientes. **No se puede declarar creado un candidato real usando un evaluador falso o un recibo de test.**

Antes de modificar esta puerta, Codex debe identificar el caso mínimo exacto que hoy no supera el validador (por ejemplo, un humano de 20 años con biografía corriente), enumerar **qué dato concreto lo bloquea** y proponer la alternativa más simple. Si el cambio exige relajar el contrato de validación F10 actualmente bloqueado, **presentar esa decisión al usuario**, sin alterarlo por su cuenta. La decisión sobre si la IA debe ser obligatoria para crear un personaje no queda tomada por este documento.

No introducir un registro adicional de etapas vitales, nuevos certificados ficticios ni múltiples proveedores IA para resolver el ejemplo. A7 es histórico, sustituido por la PR #160.

## 6. Prueba de aceptación: un único recorrido real

**Caso positivo:** crear a Daniel Torres (humano, 20 años) con un perfil ordinario; obtener exactamente una PERSON F10 en la campaña Academia; identidad H03 `BOUND` a esa PERSON; guardar; cerrar el proceso; cargar en proceso nuevo; verificar misma identidad, biografía, campaña, revisión y estado académico; sin rangos F11. Si hay admisión real, comprobar la plaza una sola vez; de lo contrario mostrar claramente **CANDIDATE**, no fingir matriculación.

**Casos negativos indispensables:** menor que el mínimo; especie Delta fuera de campaña; reintento de alta; misma clave con diferente biografía; falla la publicación sin PERSON parcial; ID falso elegido desde UI; candidato que intenta `SUBMIT_SCAN`; slot adulterado; carga que no debe sobrescribir una sesión válida.

**Evidencia requerida:** regresiones nativas y F10 en Windows/Linux, ASan/UBSan, producto Release con tests OFF, F11 aislado; y, cuando corresponda, ejecución UE5 5.8.2 sobre el MSI con UBT/UHT, NullRHI y D3D12. La batería CB-01..CB-24 previa permanece como referencia, pero no se añadirán barreras nuevas por formalismo.

## 7. Estados y cierre

Este documento y el siguiente encargo pueden considerarse **PREPARADOS**, no código productivo. **H06-P01–P05**: integración técnica diagnóstica fusionada y probada en su alcance. **H06-P06 / HU-08 / M1**: **PARCIALES, NO CERTIFICADOS** hasta tener candidato real, vínculo, guardado y prueba UE. El cierre de toda H06 no significa certificar H13.

**Prohibido** modificar el pin CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d`, contratos bloqueados, reglas F11 o laboratorios ajenos. Temporales únicamente en `laboratorios/` y nunca borrar los existentes sin permiso. Ramas y PR Draft; la implementación real se audita antes de fusionar.
