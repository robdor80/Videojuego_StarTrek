# F05-P05A — auditoría integral Cloud

**Resultado P05A: LISTA PARA VALIDACIÓN MSI**, sin defectos bloqueantes conocidos
tras las ejecuciones Cloud. La entrega exige además CI favorable del HEAD final
y queda en [PR Draft #87](https://github.com/robdor80/Videojuego_StarTrek/pull/87)
para auditoría independiente; el estado de cada ejecución final se publica en
la PR y sus [checks](https://github.com/robdor80/Videojuego_StarTrek/pull/87/checks).
F05 sigue EN_CURSO, P01–P04 EN_REVISION, F06 bloqueada. No certifica MSI ni UE.

## Base y fuentes contrastadas

Star Trek main comprobado:
`1ff057456a135f00b5c665f753fd7577f866c155`; Core main y pin compatible:
`76a7b7b485616d8c4994f384a90f123bf333591d`.
Rama `codex/f05-p05a-integration-audit`, contra main, entrega exclusivamente Draft.
PR #81/#82/#84/#85/#86 fusionadas en la base; ninguna se modifica ni se fusiona
como parte de esta auditoría. Core no requiere modificaciones ni PR dependiente.

Se contrastaron las fuentes ejecutables `desarrollo/integration/f04/` y `f05/`,
sus headers, validadores de esquema, retención histórica, fixtures y runners;
la documentación F05, ESTADO_GLOBAL, CRITERIOS_DE_CIERRE y REGISTRO_VALIDACIONES_MSI;
las integraciones F02/F03 de identidad, conocimiento, scopes y recuperación;
los contratos de `sistemas/gameplay/orders/`, `chain_of_command/` y el registro
`service_scan_obligation`; y las interfaces/documentos reales Core de Actions,
Simulation, Knowledge, Visibility, ContextBuilder, Timeline, CampaignPersistence
e HistoryPersistence. El RFC Core `npc-initiative-authority-delegation.md` es
histórico y **no implementa** un planificador genérico ni una jerarquía universal.
`npc_behavior/README.md` sigue reservado: no acredita personalidad o memoria social.

Las referencias históricas de F04/F05 anteriores a sus integraciones no se
reescriben como capacidades actuales. `P05=CERRADA` en ESTADO_GLOBAL se conserva
solo para la suite documental histórica. P05A y P05B son controles adicionales.

## Defectos reproducidos y correcciones

| ID / gravedad | Reproducción y origen | Corrección / regresión |
|---|---|---|
| P05A-01 / media, control operativo | XO emite con mandato P02, acepta operador; se revoca el nombramiento del capitán y XO pasa a mando efectivo. `f05_cancel(XO)` devolvía F04_REVOKED porque la rama por identidad del emisor comprobaba primero el mandato anterior. Contradecía la facultad vigente de cancelar del mando. | Priorizar mando efectivo en cancelación; no ejecuta ni rescata el mandato. `B_cancel_successor` y negativa `cancel_revoked_issuer`. |
| P05A-02 / media, integridad de persistencia y presupuesto | Crear petición P04 con plazo válido, editar END a 301 ticks y recalcular mediante CampaignPersistence. Core acepta el archivo estructural; Trek lo cargaba porque solo verificaba END>TICK. La API exige <=300. | Aplicar el mismo máximo al restaurar, con resta protegida por la comprobación de intervalo. `archive_ttl`, `limits`, carga fallida conserva bytes y scopes. |

Las dos pruebas aisladas fallaron **2/2 antes** de corregir y pasaron después.
El XML/log de reproducción se conserva separado del resultado final; nunca se
cuenta como PASS. No se cambian contratos aprobados, formato Core, pins u oráculos.
La revisión inicial de los nuevos fixtures también detectó errores del harness:
consulta por antiguo capitán sin acceso, usar al personaje jugador como NPC
desconocido y una colisión que ya estaba rechazada en finish. Se corrigieron los
actores/precondiciones del fixture conforme al contrato; no eran defectos del
producto. Se conserva la salida exploratoria en el laboratorio.

Endurecimiento del procedimiento MSI: la aceptación anterior del runner Unreal
solo comprobaba el total. Ahora exige además los **12 nombres únicos esperados**
y estado Success. No se afirma haber reproducido un falso PASS dentro de Unreal.
Se corrige también la selección Native/P01 para excluir los nuevos tests P05A.

Incidencia de infraestructura durante P05A: el primer job Windows de Core
terminó CTest con código 0 y el recolector nuevo rechazó un JUnit con SKIP. Se
conserva el job [126184946166](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41712799571/job/126184946166).
Core declara condicional la prueba
`ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt`: las
permisiones POSIX no equivalen a ACL Windows. El runner conserva el test y el
JUnit, permite únicamente ese SKIP en Core/Windows, lo separa de PASS y exige
483 casos descubiertos. La nueva CI debe confirmar el resultado exacto; no se
modifican pruebas ni fuentes Core para obtener PASS. Linux ejecutó los 483.
Cualquier otra omisión sigue siendo fallo, incluidos todos los casos F04/F05.

## Matriz de trazabilidad y aceptación

Todos los escenarios usan una única sesión y un único hilo propietario. El
proveedor simulado carece de capacidad de juego. Los IDs de Actor/UWorld no se
introducen en el estado lógico. Las pruebas nuevas viven en
`desarrollo/integration/f05/tests/f05_integration_audit_tests.cpp` y se registran
como `f05.p05a_*` en CTest.

| Requisito | Pruebas nuevas | Oráculo y evidencia exigida |
|---|---|---|
| A, capitán NPC | A_captain | Obligación DUTY auténtica y comunicada, petición/orden/tarea/intento/resultado distintos; cadena issued/accepted/executing/completed; ActionEngine accepted, stream 0xF0401, consumo real 1..100 |
| B, cambios de mando | B_command, B_cancel_successor, cancel_revoked_issuer | Revocación F04 causal, sucesión efectiva, antigua autoridad denegada, nuevo mando puede cancelar; mandato anterior no ejecutable |
| C, revocación y modos | C_revoked, C_suspended, C_expired, C_mode | Sin efecto tras cambio entre aceptación y ejecución, resultado fallido auténtico, hechos anteriores conservados, RNG intacto |
| Aptitud/disponibilidad | availability | Cambio médico del ejecutor invalida P04; P03 no actúa y P01 revalida también; no altera conocimiento ni delegación |
| D, jugador subordinado | D_player | WAIT_PLAYER repetido y P04 APPROVAL no crean tarea; solo recepción/ejecución explícitas producen efecto |
| E, capitán jugador | E_player_captain | XO propone bajo mandato con aprobación; autoaprobación denegada, capitán decide, modo conservado |
| F, varios NPC | F_officers, F_contradictions | Orden única por necesidad, snapshots incompatibles descartados, ningún segundo efecto, atribuciones conservadas, personaje no informado sigue CLARIFY |
| G, IA fallida | G_timeout, G_quota, G_corrupt, G_injection, G_exception | Fallback/rechazo sin efecto, sin RNG, P03/P02/P01 completan escaneo; respuesta tardía también cubierta en B/C/availability y P04 late/out_of_order |
| H, fuera de escena | H_offscreen | Mismo futuro serializado byte a byte en dos sesiones sin representación, incluyendo mundo/conocimiento/reloj/streams/historia |
| I, guardar/otro proceso | I_process_save, I_process_load | Emitida/aprobación/aceptada, petición IA pendiente retirada, propuesta aplicada, refs caducadas rechazadas, monolítico e historial, futuro y replay exactos |
| J, tiempo autoritativo | J_time | Espera real y 60.000 ms de transporte no avanzan juego, save/load conserva tick, avance explícito no autoejecuta F05, retroceso denegado |
| Presupuestos/degradación | limits, capacity_ai, capacity_orders, capacity_delegations, capacity_decisions | 6/7 hechos insuficientes; 300/301 ticks; 512 peticiones IA, 512 órdenes, 256 mandatos, 2048 decisiones; rechazo atómico y sin bypass desde P04 |
| Colisión/reintentos | key_collision y todas las process_* | Espacios P04/P03 distintos no habilitan handoff con key ocupada; rollback completo. El Host reserva keys P03/P01 y P04/P03 no usadas por otras entradas |
| Archivo manipulado | archive_ttl, archive_causality | Core estructuralmente válido pero Trek incoherente rechazado; no sustituye estado vivo ni scopes |

Total nuevo: **30 casos CTest**. Abarcan interacciones nuevas y no sustituyen
P01–P04. Los presupuestos no equivalen a latencia constante ni autonomía ilimitada.

## Revisión sistemática y límites de las garantías

| Área inspeccionada | Conclusión comprobable / límite |
|---|---|
| Validación y efecto | P01 revalida origen, mando, mandato, modo/aprobación, plazo, cualificación, disponibilidad, servicio, estación y presencia antes de llamar a perform. P03/P04 no conceden permiso por un resultado previo. |
| Transacciones y RNG | Campaña por copia, incluyendo Timeline/RandomStreams, y rollback de las llamadas P03/P01 anidadas; rechazo por capacidad/colisión no deja detección/orden parcial. Estado executing no se publica sin terminal. |
| Revisiones | Cambios de revisión invalidan snapshots P04 conservadoramente; el reloj puede cambiar sin revisión y se comprueba además plazo/plan actual. Scope nuevo tras carga impide reutilizar bindings de otra sesión. Revisión no autentica actor. |
| Privacidad | Visibility sin grants y ContextBuilder sujeto acotado. Necesidad oculta/ausente indistinguibles; informes explícitos por receptor. Datos diagnósticos privilegiados no son contexto NPC/UI. Prosa/trace externos no se aprenden ni persisten. |
| Persistencia/historia | Se conservan tombstones y dependencias F05; publicación durable explícita y bloqueo F04 ante resultado de publicación incierto. Se verifican formas/referencias/transiciones/causalidad al restaurar antes del swap. |
| Archivos hostiles | Se corrige el hueco de plazo. Los checksums detectan corrupción y los esquemas incoherencias, **no autentican** una campaña manipulada coherentemente por un Host privilegiado. No se promete firma criptográfica ni aislamiento frente a C++ hostil. |
| Reintentos | Una key/payload recupera el registro, otra carga renueva scopes; terminal no se ejecuta dos veces. Colisión entre namespaces operativos falla, no se autorepara ni reintenta remotamente. |
| P04 sobre P03 | finish es propuesta sin efectos; apply replanifica vía P03. Timeouts/red/cuota/JSON no son acciones. Capacidad IA llena deja P03 operativo; capacidad P03 llena no se elude con IA. |
| Tiempo/simulación | Solo avanza por Host/Timeline; no existe catch-up por reloj real, pausa UE nueva, daemon o progreso offline. Una evaluación ejecuta como máximo una transición P01. |
| Hilos | ABI de confianza, único propietario, workers externos no pueden llamar al Core; los tests previos de rechazo F04_THREAD siguen incluidos. No se ofrece soporte multihilo. |

## Resultados y reproducción Cloud

Evidencia local publicada en [evidence/F05-P05A/summary.json](evidence/F05-P05A/summary.json),
con comandos completos en `*-run.json`, versión real del compilador en
`*-compiler.cmake`, logs de configuración/compilación/ejecución, XML/JUnit,
aceptaciones de campañas, fuentes SHA256 y manifiesto `SHA256.json`.
Entorno real: Linux x86_64, GCC **14.2.0**, CMake **4.4.4**, Python **3.12.14**.

| Suite local ejecutada | PASS | Fallos / omitidas |
|---|---:|---|
| F04/F05 integrada | **395/395** | 0 / 0; F04=261, P01=20, P02=20, P03=26, P04=38, P05A=30 |
| Core compatible completo, JSON ON | **483/483** | 0 / 0 |
| F02 con pin original | **15/15** | 0 / 0 |
| F03 con pin original | **25/25** | 0 / 0 |
| F04 original estable | **259/259** | 0 / 0; selección compatible, sin los 11 diagnósticos largos excluidos |
| Campañas históricas | **6/6** | 0 / 0; ejecución, reanudación y auditoría separadas |
| Documentación F05 unittest | **22/22** | 0 / 0 |
| Fixtures documentales F05 | **48/48** | Referencia, no acciones Core |
| Referencia transversal F04/F05/F06 | **3/3** | No implementa F06 |
| Gobierno roadmap | **PASS** | 16 fases / 80 pasos; no certifica runtime |
| Preparación Unreal estática | **PASS_STATIC_ONLY** | 12 nombres únicos / 25 llamadas ABI declaradas; UE/UBT/UHT/RHI NO EJECUTADOS |
| Repeticiones con red bloqueada | **8/8** | 0 intentos socket/connect IPv4/IPv6 del producto; no se suman como casos únicos nuevos |

| Campaña congelada | Días completados | Resultado | Máximo de entidades residentes |
|---|---:|---|---:|
| Miranda, perfil 1 | 365/365 | PASS, oracle_equal + resume + audit | 1926 |
| Intrepid, perfil 2 | 365/365 | PASS, oracle_equal + resume + audit | 2234 |
| Sovereign, perfil 3 | 365/365 | PASS, oracle_equal + resume + audit | 8492 |
| Odyssey, perfil 4 | 365/365 | PASS, oracle_equal + resume + audit | 18348 |
| Valhalla, perfil 5 | 365/365 | PASS, oracle_equal + resume + audit | 21218 |
| Valhalla, perfil 5 | 730/730 | PASS, oracle_equal + resume + audit | 21218 |

Los metadatos locales conservan honestamente el SHA base y `trek_dirty=true`
porque las ejecuciones comenzaron durante el trabajo de auditoría, antes del
commit. El inventario de fuentes recoge el snapshot publicado antes de exportar
la evidencia; no se reescriben los SHAs de los runs. La CI definitiva compila
explícitamente el HEAD de la rama (no el merge sintético), conserva su SHA real
en cada `run.json`, y sus enlaces/resultados se publican en la descripción de
PR #87. No atribuir CI de un commit anterior al HEAD definitivo.

El workflow `f05-native-orders.yml` exige diez jobs: nativo/Core en Linux y
Windows, F02/F03/F04 originales en ambos sistemas y seis campañas congeladas en
cada sistema. Los artefactos `f05-p05a-native-*`, `f05-p05a-regression-*` y
`f05-p05a-historical-*` contienen JUnit, comandos, compilador y logs originales.
En Core/Windows se debe distinguir el posible SKIP POSIX nominal del PASS;
Linux acredita la suite completa sin omisiones. Las pruebas F04/F05 y campañas
no admiten SKIP. Los workflows de referencia F05, gobierno y release documental
se comprueban también, sin atribuirles certificación runtime.

Runner reproducible (Python, Linux/Windows):

```text
python desarrollo/integration/f05/run_integration_audit.py --suite f05 --core-source <Core-compatible> --output <salida-nueva>
python desarrollo/integration/f05/run_integration_audit.py --suite core --core-source <Core-compatible> --output <salida-nueva>
python desarrollo/integration/f05/run_integration_audit.py --suite f02 --core-source <Core-F02> --output <salida-nueva>
python desarrollo/integration/f05/run_integration_audit.py --suite f03 --core-source <Core-F03> --output <salida-nueva>
python desarrollo/integration/f05/run_integration_audit.py --suite f04 --core-source <Core-F04-estable> --output <salida-nueva>
python desarrollo/integration/f05/run_integration_audit.py --suite history --core-source <Core-historico> --output <salida-nueva> --parallel 2
```

Cada salida debe ser nueva y autorizada bajo los laboratorios del repositorio.
No hay dependencia del producto hacia esas salidas. Durante P05A todos los
temporales permanecen en `laboratorios/f05/p05a/`, excluidos de Git, eliminables
solo con autorización y sin afectar al producto ni a laboratorios anteriores.

Pins preservados: F02 `4f282863737bcd8f5add401202a9e1064c133672`;
F03 `9c53a33787de13d91eb2abe4da07033ee0fa1dc1`;
F04 estable `c147d81ed069da2e09149613ab02cbc3ebe95a4a`;
F04 histórico `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`.
Los seis oráculos congelados proceden de Core
`63d2401edaf85960b4baaf6b537ae571ba52a439` y conservan sus hashes y procedencia.
No se recalculan expectativas para conseguir PASS. Se repitieron además ocho escenarios en Linux con socket/connect IPv4/IPv6 bloqueados mediante LD_PRELOAD y una autocomprobación del bloqueo: ocho PASS y cero intentos de conexión del producto. Es una comprobación de ese binario y llamadas libc, no una garantía universal contra syscalls directas; no añade dependencias de ejecución al producto. Código del bloqueo y logs se conservan en la evidencia, sin versionar el laboratorio. Los 11 diagnósticos
monolíticos históricos de 365/730 días y recuperación asociada permanecen
**EXCLUIDOS / NO EJECUTADOS**, no se suman a las pruebas superadas.

## Riesgos residuales y continuación

- Ningún defecto grave sin corregir está identificado tras las pruebas Cloud.
  P05A-01/02 requieren validación MSI posterior; CI final y auditoría independiente
  son condiciones de entrega, no equivalen a certificación local.
- MSVC local, carga DLL, UBT/UHT, las 12 automatizaciones, RHI real, continuidad
  y repetición limpia en MSI siguen pendientes. Ver
  [plan P05B](P05B_PLAN_CERTIFICACION_MSI.md) y
  [registro acumulativo](REGISTRO_VALIDACIONES_MSI.md).
- Host debe autenticar entradas, reservar keys y decidir evaluaciones/avance.
  No hay memoria social, personalidad, reparación, planeación general de
  tripulación o cliente comercial Luna/Sol acreditados. Único efecto operativo:
  F04_SCAN, sin descubrir contactos ni iniciar F06/F12/F13.
- Límites persistentes finitos, historial de F05 retenido residente y sin
  recolección/rotación automática. Llegar al tope exige intervención de Host y
  una futura decisión de retención, no ampliar límites silenciosamente.
- No se modifican Core, proyectos artísticos, modelos, interiores, materiales,
  naves, copias de seguridad o laboratorios anteriores. Ninguna PR se fusiona.

Bloquean el cierre de F05: auditoría independiente desfavorable, cualquier fallo
grave abierto, CI final incompleta, cualquiera de las verificaciones MSI
obligatorias sin evidencia, o ausencia de acta de aceptación P05B posterior.
