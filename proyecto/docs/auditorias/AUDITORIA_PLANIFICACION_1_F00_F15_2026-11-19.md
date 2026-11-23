# AUDITORÍA INDEPENDIENTE — PLANIFICACIÓN 1 (F00–F15)
## Videojuego Star Trek RPG · 19 de noviembre de 2026 · Informe 1.0

**Dictamen:** PLANIFICACIÓN 1 NO ESTÁ TERMINADA. Hay una base documental y nativa considerable, pero no un circuito integral de juego certificado. El principal riesgo no es la falta de ideas: es la divergencia entre la foto administrativa, los incrementos realmente fusionados, las PR abiertas, el diseño actualizado y las puertas que siguen sin demostrar funcionamiento en el videojuego.

**Repositorio:** https://github.com/robdor80/Videojuego_StarTrek  
**Referencia de lectura:** rama main, commit bb7fcd5f60c628de4812704b7a7c5d1c35369877, 19-11-2026.  
**Archivo maestro contrastado:** proyecto/docs/roadmap/master/ESTADO_GLOBAL.json (fecha interna 03-11-2026).  
**Objeto:** F00–F15, cinco pasos P01–P05 por fase (16 fases y 80 pasos), fuentes de roadmap, decisiones, PR, pruebas declaradas, workflows, integración nativa, HOST/Unreal y dependencias pertinentes.  
**Tipo de trabajo:** auditoría independiente por lectura del repositorio remoto y metadatos de GitHub. **NO** se han ejecutado CoreRPG, compilaciones, tests, Unreal 5.8.2 ni una partida en el MSI durante esta auditoría. Los PASS que se citan proceden de actas, registros o PR históricas, no de una nueva certificación. Tampoco se han auditado exhaustivamente los otros proyectos CoreRPG, HOST autónomo, NAP, Academia web, Lore y Planificación 2: se registran exclusivamente sus fronteras con Planificación 1.

**No se modifican ni se aprueban decisiones creativas, código, tests, esquemas, assets, estados o PR de las fases.** Este documento propone correcciones que debe tramitar la conversación responsable de Planificación 1; cuando dependan de otro ámbito, remitirlas a su propia auditoría.

---

## 1. Resultado ejecutivo y significado de las cifras

- **Estado administrativo registrado:** F00, F01, F02, F03 y F04 aparecen CERRADAS en sus **alcances explícitos**; F05 EN_CURSO; F06 y F07 EN_REVISION; F08–F15 PLANIFICADAS. **Ninguna de las fases F08–F15 está declarada jugable y aceptada** en el registro maestro.
- **Estado del registro:** la fotografía maestra sigue fechada el 03-11 y fija F05 como fase principal y F04 como última cerrada. No incorpora debidamente la PR #89 de F05 ya fusionada, el trabajo F06 de noviembre, la progresión nativa F11, el desarrollo de HOST/F10 ni la finalización **de referencia** de Planificación 2 B01–B10.
- **Recuento mecánico, NO porcentaje de juego:** del total de 80 pasos, el JSON de 03-11 marca 29 como CERRADA y **51 como no CERRADA**. Entre los 29 hay cierres de diseño o referencia, no capacidades jugables; entre los 51 hay avances posteriores importantes todavía no conciliados. No convertir 29/80 en un progreso porcentual real.
- **Restante en términos de fases:** al menos **11 fases todavía sin cierre global** (F05–F15). F05 necesita auditoría/acta y reconciliación, F06/F07 tienen integración técnica parcial y PR pendientes, F08 necesita su primera aceptación E2E, F09–F15 tienen principalmente contratos/referencias y desarrollos puntuales. No hay evidencia para calcular horas o un porcentaje fiable de finalización.
- **Hitos genuinos:** F02 unión técnica Core/UE; F03 estado y persistencia en corte vertical; F04 dotaciones/guardias y campañas; F05 órdenes, delegación, iniciativa y dos repeticiones técnicas MSI; F06 sensores de referencia, ASTRO/Aster y propuestas nativas en borrador; F11 **un** ascenso autoritativo y lector nativo de expediente; P2 diez bloques de referencia; HOST proyectos nativos y mapa diagnóstico. Todo esto debe preservarse.
- **Ausencias decisivas:** no se ha certificado una guardia F08 completa dentro de una nave 3D conectada a Core/HOST, ni la carrera F11 hasta capitán, ni la Academia F10 jugable, ni las otras consolas F09, ni el universo F13 ejecutado, ni las pruebas integrales finales F15. **El proyecto principal Unreal disponible es un diagnóstico HOST, no un juego completo.**

**Conclusión de prioridad:** actualizar el gobierno sin mentir, cerrar realmente F05 si procede, estabilizar las PR encadenadas de F06, conectar Sensores con LCARS/UE5, y demostrar F08 en una única ruta vertical repetible. Evitar fabricar nuevas referencias cuando el bloqueo real es la integración.

### 1.1 Semántica obligatoria de estado

Aplicar las reglas de proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md: diferenciar estado de planificación (PLANIFICADA/EN_CURSO/EN_REVISION/BLOQUEADA/CERRADA) y nivel demostrado (DISEÑO, CONTRATO, REFERENCIA, CORE, UE5, ACEPTACIÓN). CERRADA en F01 significa diseño validado; en F04 significa su corte administrativo de referencia; en F03 corresponde a su alcance concreto Core integrado; no significa que la campaña completa funcione. PR fusionada ≠ fase certificada. Test Python ≠ simulación nativa. Automatización UE5 de laboratorio ≠ experiencia UE5 jugable. Una PR Draft ≠ código incorporado en main.

---

## 2. Matriz completa de F00 a F15

| Fase | Evidencia disponible en main / PR | Estado real contrastable | Trabajo imprescindible siguiente |
|---|---|---|---|
| **F00 — gobierno** | PR #1; baseline, inventario, normas y 16 fases | CERRADA **documental**; gobierno actual desfasado | Rectificar estado/validador, mantener historial y trazabilidad actual |
| **F01 — visión y canon** | PR #2 y actas; DEC-0020/0021/0022 posteriores | CERRADA **en diseño histórico**; decisión final de nave cambió | Reconciliar referencias actuales a Enterprise-D / Proyecto Valhalla y protagonista fijo sin borrar actas |
| **F02 — Core↔UE** | PR #60, laboratorio de puente real | CERRADA al corte CONTRATO_VALIDADO; no partida jugable | Revalidar compatibilidad del puente con HOST/proyecto principal, interfaces y versiones |
| **F03 — WorldState** | CoreRPG #12 + Trek #62; identidad, tiempo, visibilidad, eventos y save/load | CERRADA en corte CORE_INTEGRADO, no universo galáctico total | Ensayo de los consumidores nuevos y recuperación E2E/actualización de versiones |
| **F04 — naves y dotaciones** | PR #64, #66–#76, campañas 365/730, tres guardias, cinco perfiles | CERRADA **corte administrativo REFERENCIA_PROBADA**; deuda F04-INTEGRACION-04 | Perfiles Enterprise-D Galaxy, independencia por secciones, dotación válida, escalado y actores reales |
| **F05 — órdenes/NPC** | PR #81/#82/#84/#85/#87/#89; #89 fusionada; MSI 2/2 | Fuerte evidencia nativa y UE de laboratorio; **cierre formal no reconciliado** | Auditoría independiente, criterios de incidencias UE, acta y puerta F06; actualizar estado sin sobrecertificar |
| **F06 — sensores** | #7, #92/#93/#94 fusionadas; #91→#96→#97 Draft encadenadas | Referencia y banco de pruebas; integración ampliada **no en main** | Resolver fuente espacial autoritativa, PR stack, manual, Core/HOST, Ciencia, save/load y MSI |
| **F07 — 3D y puente** | #11/#12/#40; Sutherland; pipeline PBR; #95 LCARS Draft | PBR de referencia; recorrido/sillas reportados; falta aceptación UE5 | Evidencia primaria, corregir asiento, LCARS→F06→UE5, controles, rendimiento, build |
| **F08 — guardia v0.0.1** | #13, fixture y validador deliberadamente bloqueado | PLANIFICADA/PAUSADA para runtime | P01–P05 E2E: orden, consola, observación, informe, consecuencias, guardar/cargar y reanudar |
| **F09 — consolas** | #14, catálogo de 16 familias, pruebas de contrato | Preparación offline, **sin conjunto jugable** | Priorizar subconjunto funcional, permisos/acciones, casos multi-consola y UE5 |
| **F10 — Academia** | #15, cuatro cursos offline; F10/H06 PR #149–#169 relevantes | Referencia + piezas nativas de admisión; **protagonista fijo v2 sin migración runtime** | Sustituir editor libre sin romper contratos; ingreso/Academia 4 años, social, clases y graduación reales |
| **F11 — carrera** | #17, #98–#109, #136; #110 Draft; issue #104 abierta | P01–P04 diseñados/probados offline; primer ascenso 1101→1102 nativo; lector Host | Emisor institucional de producto, rangos siguientes, plazas/ofertas/sucesión, presentaciones P05-C/D/E y campaña |
| **F12 — vida social** | #18, contratos y 45 casos offline; IDEA-0017 LIFE | Preparada en referencia; no continuidad social real completa | NPC, agendas y vínculos autoritativos; LOD, privacidad, familia acotada y persistencia |
| **F13 — universo dinámico** | #19 y P2-B01–B10, #122 de B10 | B01–B10 **REFERENCE_COMPLETE**; F13 runtime NO implementado | Diseñar incremento Core/HOST con scheduler, registro causal, LOD, límites y pruebas largas |
| **F14 — arte y NAP** | #20, biblias, manifests, pipeline y materiales separados | Preparación/documentos; arte parcial externo/varios laboratorios | Inventario de assets utilizables, importación UE5, identidad, audio/LCARS, LOD, presupuesto VRAM |
| **F15 — QA final** | #21/#22, gate offline que rechaza plantilla NO_EJECUTADO | PLANIFICADA; no aceptación E2E | QA de campaña real, rendimiento MSI, fallos, migraciones, paquete privado local y acta |

### 2.1 Evidencias significativas por tramo

**F00–F03.** El cierre administrativo F00/F01 no prueba gameplay. F02 #60 integró CoreRPG/UE 5.8.2 en un laboratorio; F03 #62 y Core #12 integraron estado y persistencia para un corte técnico. Exigir regresión a nuevos consumidores HOST, F05, F06 y F11, no reimplementar esos cimientos.

**F04–F05.** F04 #76 acredita campañas históricas y operaciones sobre Core, pero reconoce una integración avanzada pendiente; no confundir plantilla de hasta 2.200 personas con censo aprobado de la nueva Enterprise-D. En F05 la PR [#89](https://github.com/robdor80/Videojuego_StarTrek/pull/89) **está fusionada desde 05-11**, a diferencia de lo escrito en el README/certificado de esa fecha: dos pasadas oficiales, Core 482 PASS + 1 SKIP POSIX, F04/F05 395/395, symlinks 3/3, automatizaciones 12/12 NullRHI y 12/12 D3D12 por repetición. **Persisten 14 mensajes de error globales por arranque** reproducidos en controles UE ajenos al módulo; la aserción concreta no se identificó. No ocultarlos ni proclamar Unreal libre de errores.

**F06–F08.** F06 #92/#93/#94 añaden generador y banco de ensayos; #91, #96 y #97 siguen **Draft**, con bases respectivamente main, #91 y #96. Hay trabajo genuino, pero no una pila fusionada y no consta proveedor runtime espacial universal. F07 #95 es HTML/JS LCARS con contrato, no interfaz real conectada a Unreal. F08 mantiene una puerta de aceptación preparada e intencionadamente sin evidencias de ejecución.

**F09–F11.** F09 referencia de 16 consolas ≠ estaciones funcionales. F10 dispone de backend de validación y un proyecto UE HOST de diagnóstico, pero la decisión DEC-0022 de **protagonista único** posterior a IA-03A obliga a migrar selector de especies/edad/sexo/biografía: no borrar validadores históricos ni permitir que HOST se convierta en segundo dueño de reglas F10. F11 #106 confirma únicamente 1101→1102 con expediente y guardado, #107 certifica ese corte y #109 aporta lector HOST **solo lectura**; la PR #110 de emisor institucional sigue Draft, no habilita emisión ni carrera completa.

**F12–F15.** F12 tiene simuladores offline, no una sociedad real en juego. F13 debe aprovechar P2 B01–B10 completada **solo en referencia**, sin duplicar la auditoría de P2. F14 ha producido biblias y preparativos, pero necesita assets y escenas certificados. F15 tiene un validador diseñado para **NO aprobar** una plantilla sin ejecución: comportamiento correcto, no evidencia de beta acabada.

---

## 3. Hallazgos priorizados, fallo, causa, corrección y prueba

Convención: **P0** = impide gobernar o entregar el corte siguiente de manera segura; **P1** = riesgo sustancial de integración o coherencia; **P2** = deuda de calidad, evidencia o planificación. Una propuesta no cambia de por sí el estado del proyecto.

### P0-01 — Validador de roadmap que prohíbe actualizar el roadmap [CONFIRMADO]

**Prueba por lectura:** desarrollo/tools/validation/validate_roadmap_state.py contiene EXPECTED_STATUS con F05=EN_CURSO y F06=EN_REVISION, EXPECTED_MATURITY congelado, completed_management_phase obligatorio F04, lista fija de PR #2–#7 y regla de **una** fase EN_CURSO igual a current_global_phase. El workflow roadmap-governance.yml ejecuta ese script. Esto puede bloquear una corrección honesta o incentivar a mantener datos viejos para lograr un PASS.

**Corrección:** versión nueva del esquema/gobierno: estados y madurez derivables de evidencias y decisiones versionadas, matriz de hitos cerrados, foco principal separado de workstreams paralelos; revisión explícita del contador y PR fusionadas; migración del validador y pruebas positivas/negativas. No desactivar la CI ni eliminar el control: sustituir las constantes históricas por invariantes permanentes y certificaciones fechadas. **Gate:** cambiar F05 con evidencia suficiente sin editar constantes arbitrarias; detectar CERRADA falsa, PR Draft presentada como fusionada y fase jugable sin evidencia.

### P0-02 — No existe primera experiencia jugable E2E certificada [CONFIRMADO DOCUMENTALMENTE]

**Prueba:** F08-P01–P05 siguen sin marcar; su validador y plantilla no acreditan ejecución. juego/UE5/StarTrekRPG/README.md describe mapa/panel HOST de diagnóstico con F11 SERVICE_UNAVAILABLE, no puente 3D/sensores/campaña completa. F06/F07 admiten sus propias faltas de integración.

**Corrección:** fijar un **vertical slice mínimo F08**, con nave/puente piloto Sutherland ya aprobado para la prueba técnica salvo nueva decisión autoral explícita: sesión Core-HOST, capitán NPC y orden, consola, contacto observado y respuesta científica, persistencia entre procesos, consecuencias y un ciclo jugable estable; fallback sin IA. **Gate:** prueba real en el MSI a partir de build/proyecto identificado, comandos, capturas/logs, temporización, hashes y aceptación del autor; no basta el harness.

### P0-03 — Identidad de nave y fichas antiguas incompatibles [CONFIRMADO]

**Prueba:** DEC-0020 (13-11) define USS Enterprise NCC-1701-D, class_id galaxy, Proyecto Valhalla como programa, **no** clase. PLAN_MAESTRO.md, ESTADO_GLOBAL.json, textos antiguos F01/F04/F06/F07/F11 y contratos de clase histórica todavía hablan de una nueva clase Valhalla, capacidad 1.800 Flota + 400 civiles, primera unidad 2387 o futuro buque genérico. DEC-0021 añade doctrina de sensores; DEC-0022 afecta protagonista/F10.

**Corrección:** matriz de consumidores, alias y migración de datos por fase, sin eliminar identificadores ni alterar guardados históricos a ciegas. Mantener cronología aprobada 2383 Academia, 2387 graduación/objetivo de reconstrucción sujeto a hechos del mundo; clase Galaxy, identidad individual Enterprise-D; revisar dotación, separaciones, blindaje, tecnología y recursos. **NO** asignar automáticamente los 2.200 del prototipo a Enterprise-D. **Gate:** pruebas de identidad, serialización, carga legacy, capacidades según estado real del refit y conocimiento del jugador; no reaparecer una clase Valhalla como nave final.

### P0-04 — F06 fragmentada entre PR encadenadas y sin alimentación espacial de producción [CONFIRMADO]

**Prueba:** [#91](https://github.com/robdor80/Videojuego_StarTrek/pull/91), [#96](https://github.com/robdor80/Videojuego_StarTrek/pull/96), [#97](https://github.com/robdor80/Videojuego_StarTrek/pull/97) abiertas en Draft y dependencia sucesiva de sus bases. #91 declara explícitamente que falta el runtime espacial Core/HOST que aporte todas las naves reales. F06 P01 mantiene revisión completa del manual, y F06-P03/P04 no están certificadas E2E.

**Corrección:** auditar diferencias, bases, conflictos y contratos de las tres; decidir integrar cada incremento en orden y probar tras cada merge, o reestructurar sin perder historia. Habilitar origen espacial autoritativo versionado, observador/permiso, pérdida de contacto, transpondedores, filtrado de conocimiento, informe a Ciencia, actuación en órbita y recuperación. Separar Aster **QA** de ordenador de nave del juego. **Gate:** contactos reales y no omniscientes con guardado/carga en HOST/UE, resultados repetibles, negativas y medición de coste.

### P0-05 — F11 carece de circuito institucional de producto y progresión completa [CONFIRMADO]

**Prueba:** #106 implementa solo primer ascenso 1101→1102; #109 lector F11 HOST solo lectura; #110 PR Draft prepara **documentos** y 33 casos NOT_RUN del emisor, sin código de emisión; issue #104 mantiene P05-C/D/E. Plan F11 11-11 garantiza oportunidades creíbles, no niveles gratuitos.

**Corrección:** cerrar frontera de emisión institucional **dentro del gobierno HOST sin reimplementar reglas F11**; identidad, procedencia, autenticidad de guardado, comisión, evaluación, concesión, orden, aceptación y efectos firmes en Core. Extender rango y destinos mediante sucesiones reales y reintentos causales; comunicar ascensos de forma diegética con historial y acuse persistentes. No usar el emisor de ensayo como producto ni permitir autoridad por JSON/LLM. **Gate:** campaña reproducible Academia→alférez→diversos destinos/rangos→capitán Enterprise-D **sin salto automático**, ramas de rechazo/espera y guardado en cada paso.

### P1-06 — F05 certificada técnicamente pero sin acta actualizada [CONFIRMADO]

**Prueba:** #89 está fusionada, README/actas mantienen Draft y F06 BLOQUEADA. La certificación deja final_certification=PENDIENTE_ACTA y reconoce errores globales de arranque UE reproducibles en control sin identificar la aserción.

**Corrección:** auditoría de cierre acotada a evidencias del árbol final fusionado, alcance y políticas sobre incidencia de motor; acta del propietario si procede; marcar P01–P05 según nivel alcanzado; desbloquear **solo** dependencias que el corte cubra, no certificar juego. No inventar nueva repetición MSI. **Gate:** matriz de aceptación P05B con explicación escrita de excepciones y SHA exactos; estado maestro/README sincronizados.

### P1-07 — F07 no dispone de paquete visual/rendimiento aceptado [CONFIRMADO]

**Prueba:** F07/README.md registra ensayos Sutherland reportados sin evidencias primarias completas, asiento F07-SEAT-01 **no aprobado** por intersección de poses, y P05 bloqueada. #95 es consola demo aislada.

**Corrección:** repositorio/manifiesto de derivados con hashes, escala, materiales, colisiones, puntos de interacción, silla correcta, navegación segura, importación UE y presupuesto en GPU objetivo. Integrar LCARS con datos observados del F06 ya fusionado, no con fixture que parezca real. **Gate:** vídeo/capturas, automatización funcional, perfil VRAM/RAM/CPU/FPS y build real en MSI con rechazo de recursos placeholder no declarados.

### P1-08 — F10 sigue aceptando la UX vieja mientras la decisión autoral es protagonista fijo [CONFIRMADO]

**Prueba:** DEC-0022 y H06_S04_TRANSICION_PROTAGONISTA_FIJO_2026-11-17.md especifican un protagonista único varón híbrido humano-vulcano de 45 años en 2383; IA-03A y formularios anteriores admitían varios arquetipos/edad/biografía. S04_MIGRACION_F10_HOST_v2.md se declara NO IMPLEMENTADO.

**Corrección:** fuente autoral inmutable/versionada para antecedentes, nombre y aspecto acotados, sin selector libre de identidad; respetar ACC-01–05, institucionalidad de admisión, registros y cuatro años. Regresión de biografía, habilidades, edad, nuevas partidas/legacy, intro 2D e idempotencia. **Gate:** mismo arquetipo en todas las partidas nuevas, variación solo permitida, sin credenciales fabricadas y progreso real persistido.

### P1-09 — F13 continúa sin simulador galáctico autoritativo [CONFIRMADO]

**Prueba:** F13/README.md certifica B01–B10 a nivel REFERENCE_COMPLETE con #122; declara explícitamente que no ejecuta universo offscreen Core/HOST/UE. El maestro 03-11 sigue afirmando bloque 4 pendiente.

**Corrección:** en Planificación 1, definir **solamente** el primer adaptador runtime de F13 y sus contratos de concurrencia con F03/F04/F05/F06/F09/F11/F12, reutilizando P2; no rediseñar los diez bloques. Tres escalas (visible, región activa, fondo agregado), tiempos virtuales acotados, eventos causales, control de saturación, reversión, semilla, visibilidad y persistencia. **Gate:** campañas cortas/largas offline sobre Core y ensayo UE5 limitado con telemetría; no confundir 383 tests de referencia con una galaxia viva.

### P1-10 — F15 presupone publicación/distribución que no pertenece al objetivo [CONFIRMADO]

**Prueba:** F15-P05 y PLAN_MAESTRO.md incluyen distribución, beta, build distribuible y publicación. **Decisión autoral firme vigente: videojuego solo para uso privado, no distribuir a terceros.**

**Corrección:** reinterpretar F15-P05 como **build privado recuperable**, instalación local, actualización propia, backups, migraciones, rollback e inventario/reproducibilidad. Puede conservar nombres históricos y pruebas técnicas de empaquetado, pero eliminar la distribución pública como puerta obligatoria. Derechos/procedencia de assets siguen siendo relevantes para seguridad y mantenimiento, sin crear burocracia de lanzamiento comercial. **Gate:** instalación/reanudación en el MSI personal y restauración tras fallo, sin servidor de distribución ni testers externos como requisito.

### P1-11 — Cobertura de CI desigual y estados congelados [CONFIRMADO POR WORKFLOWS]

**Prueba:** f06-sensors-reference.yml solo hace push a la rama histórica feat/f06-sensors-functional-reference, no a main; f11-native-promotions.yml, f11-a02-03-native-host-reader.yml y f05-native-orders.yml declaran pull_request y workflow_dispatch, no push main. Otros workflows F10/F15 sí observan main. El validador de gobernanza exige estados obsoletos.

**Corrección:** matriz de PR, push main, integración nocturna/manual pesada MSI y regresiones cruzadas, con path filters que cubran todos los consumidores. Conservar certificaciones históricas congeladas como reproducibles manualmente; añadir **gates vigentes** para nueva ejecución sin romper oráculos. No ejecutar Unreal/Windows en cada edición documental, pero sí cuando se modifica una ABI, regla, puente o asset crítico. **Gate:** cambio adversarial en contrato que detecta regresión en main; reporte de checks requerido/omitido con justificación; no asumir que ausencia de checks significa PASS.

### P1-12 — F04/F12/F11: guardias, autoridad, relaciones y ocupación real no completamente conectadas [RIESGO DOCUMENTADO]

Los patrones de dotación y guardia no garantizan descanso, enfermedad, reemplazos, vacantes profesionales y NPC que habitan/recorren la nave al mismo tiempo. F12 offline y F11 director de sucesiones offline no demuestran un mismo WorldState. **Corrección:** establecer operación temporal única, LOD y reconciliación de horarios/rangos/personas; casos de cambio de turno, promoción sin cambio de plaza, baja simultánea y salida del barco. Incluir privacidad del expediente y memoria social. **Gate:** campaña persistente sin duplicar personas, cargos, NPC o eventos.

### P1-13 — Falta contrato de integración de extremo a extremo por operación, no solo por fase [RIESGO ARQUITECTÓNICO]

El roadmap divide por temas F05/F06/F09/F10/F11/F12/F13, HOST aporta sesiones e IA y sistemas S01–S19 describen funciones. Una función puede estar aprobada en tres lugares sin un flujo probado. **Corrección:** para cada operación prioritaria definir: intención jugador/NPC → autenticación HOST → autorización y reglas Trek Fxx → confirmación WorldState Core → proyección autorizada → UX UE5 → journal/guardado → recuperación → efectos fuera de escena. **Gate:** identificador de caso E2E y propietario por frontera; prohibir mutaciones laterales de HTML, voz, IA o UE.

### P1-14 — Rendimiento y degradación todavía no presupuestados para el juego completo [RIESGO ALTO]

Objetivo MSI i9-14900HX, RTX 4070 Laptop 8 GB y 32 GB. IA central, TTS local CPU, LOD NPC, mundo simulado, interiores, LCARS y arte conviven. Las pruebas nativas aisladas y el NullRHI no validan FPS. **Corrección:** presupuestos medibles de frame time, memoria, GPU/VRAM, latencia de respuesta y actualización offscreen, prioridades/cancelación, caché y degradación segura. IA remota opcional nunca autoriza hechos; TTS sin consumir VRAM si compromete FPS. **Gate:** telemetría del MSI en guardia, interiores densos, cambio de sección, save/load, diálogos y sesión larga.

### P2-15 — Manual PDF F06-P01 todavía sin inspección gráfica integral [CONFIRMADO]

La auditoría de 13-10 contrastó texto y páginas puntuales, no el documento gráfico completo y su hash. **Corrección:** cotejo humano/visual integral del manual, revisión del árbol de diez ramas, trazabilidad de versión y acta. No bloquear por ello otras pruebas Core independientes, pero sí cerrar P01 con evidencia propia.

### P2-16 — Contratos de referencia históricos y notas contradictorias [CONFIRMADO]

README F05, F08, F11, F13 y documentos maestros mezclan párrafos de octubre con novedades de noviembre y expresiones como «F02 única fase principal» pese al avance posterior. **Corrección:** una foto de estado actual breve, fechada y referenciada; histórico inmutable en actas; enlaces de precedencia DEC-0020/0021/0022; marca OBSOLETO en fragmentos incompatibles, nunca borrar evidencia ni fingir que era verdad entonces. **Gate:** revisión automatizada de vocabulario de nave, estado/PR y fechas relevantes con lista de excepciones históricas.

### P2-17 — F08 necesita fixture de campaña actual además del laboratorio 2372 [RIESGO]

El fixture F03 de 2372 y el prototipo Sutherland siguen siendo útiles para regresión técnica. No equivalen a campaña del personaje desde Academia 2383. **Corrección:** conservar fixture 2372 y añadir escenario narrativo 2383→2387 con tripulación, edad, carrera, estado de Enterprise-D y descubrimientos coherentes; separar «ensayo técnico» de «historia de campaña». **Gate:** ambos fixtures se ejecutan sin contaminar temporalidad/canon.

### P2-18 — Seguridad de guardados, identidad y autoridad de F11 deben diferenciar corrupción de autenticidad [CONFIRMADO EN DOCUMENTACIÓN]

F11/README.md reconoce que checksum Core no autentica un guardado entero manipulado y que refs numéricas no son credenciales. **Corrección:** gobierno HOST de procedencia de partida, acceso a expedientes, certificados/recibos institucionales y no exposición de emisores de prueba; diseño proporcional al videojuego local, sin prometer criptografía ficticia. **Gate:** guardado ajeno/falsificado, expediente no visible, clave idempotente y solicitud sin principal fallan cerrados.

### P2-19 — F14 debe registrar qué assets están listos *para jugar*, no solo archivados [RIESGO]

NAP, biblias, GLB, pruebas de sala y pantalla demo existen pero no están homogeneizados como escenas y personajes listos. **Corrección:** manifiesto de procedencia, versión de origen y derivado, validación UE, escala/UV/PBR/LOD/colisión/animación, estado READY, PLACEHOLDER o BLOCKED, estimación VRAM y dependencia de F07/F08/F10/F11. Priorizar la ruta de la primera guardia y protagonista único sobre completar todo el catálogo galáctico. **Gate:** una escena/asset importable y reproducible desde fuente trazable con captura de prueba, no un nombre en inventario.

### P2-20 — Falta aceptación de «no hacer» y presupuesto de alcance [PROPUESTA]

Conservar las 16 fases y 80 pasos salvo revisión autoral formal: no crear una nueva fase para cada sistema S01–S19, ni hacer que F15 espere absolutamente todas las ideas opcionales para una primera versión interna. Introducir **alcance mínimo de validación** por fase, capacidades ampliables y criterio «aplazado con dueño y motivo», sin reinterpretar CERRADA como certificación total. **Gate:** backlog clasificado imprescindible / posterior / experimental y ausencia de puertas imposibles para el corte escogido.

---

## 4. Contradicciones concretas a reconciliar (sin borrar historia)

1. **F05:** PR #89 fusionada 05-11 versus texto «Draft #89, sin fusionar», «F06 BLOQUEADA» y maestro F05 EN_CURSO; verificar acta, no pasar directamente a CERRADA por una URL.
2. **F11:** maestro 03-11 PLANIFICADA como si solo existiera referencia; la PR #106 y #109 aportan código real y #110 continúa abierta. Mantener F11 global no cerrada pero registrar **subhitos**.
3. **F13:** maestro dice bloque 4 pendiente; P2 B10 #122 culminó referencia. No reabrir P2 ni decir que F13 runtime terminó.
4. **Nave final:** clase histórica Valhalla ≠ **USS Enterprise-D, clase Galaxy**, Proyecto Valhalla de reconstrucción. Capacidad 2200 es plantilla heredada no censo ratificado.
5. **Protagonista:** editor libre/humano-vulcano-híbrido por elección ≠ protagonista fijo aprobado 17-11 (DEC-0022).
6. **P05 F15:** distribución beta/publicación para terceros ≠ empaquetado privado instalable, recuperable y actualizable.
7. **F06/F07:** pruebas Aster o LCARS HTML ≠ consola renderizada interactiva del proyecto Unreal final.
8. **Repetición de términos:** «cerrado en referencia» o «CI verde» no se redactará como «completado en el juego».
9. **Normativa CI:** para promover F05/F06/F11, actualizar conjuntamente validador fijo y política de evidencias, no forzar la nueva fotografía a encajar en EXPECTED_STATUS de 13-10.
10. **HOST y F11:** lector institucional #109 no genera hechos de rango; emisor de ensayo no es credencial de producto. HOST ofrece servicios, F11 fija el dominio.

---

## 5. Dependencias y orden recomendado de remediación

### Corte R0 — Gobierno y diagnóstico fiel
Responsable: conversación Planificación 1 (documentación/decisiones), Codex solo si debe cambiar código del validador. Inventariar PR actuales, registrar estados por paso con enlace/SHA/fecha/entorno, actualizar Plan Maestro, ESTADO_GLOBAL, README, validador y su CI en **un único cambio coherente**. No cambiar las 80 denominaciones sin decisión. Resolver clasificación histórica sin destruir evidencia; matriz de cierre por nivel. **Salida:** ningún documento presenta una PR abierta como fusionada, una prueba de referencia como jugabilidad o una clase histórica como nave protagonista.

### Corte R1 — F05: decidir formalmente si el gate queda cerrado
Reauditar #89 y sus dos pasadas, la excepción POSIX, 14 errores UE y limitaciones de laboratorio; documentar aceptación o incidencias exigibles. Solo después emitir acta de F05 al nivel CORE_INTEGRADO **si la evidencia y criterios de fase realmente lo permiten**. No certificar escenario jugable ni retirar deudas F04. **Salida:** F05 con estado real y F06 desbloqueada solo donde corresponda.

### Corte R2 — F06: estabilizar la cadena nativa
Auditar/actualizar #91 → #96 → #97 en orden, fuente de snapshots espaciales autoritativos y contratos de observación; rebase y regresión Core/F04/F05/HOST, pruebas Ciencia, información filtrada, guardado, permisos y rendimiento; integrar en main solo tras la revisión técnica. Cerrar revisión del manual. Coordinar con la **arquitectura HOST** sin trasladar allí reglas de Sensores. **Salida:** una operación F06 desde WorldState real con recibo y proyección.

### Corte R3 — F07: interfaz y nave piloto
Resolver asiento/navegación/materiales, evidencias primarias Sutherland, LCARS #95 y adaptador a F06. Medir en MSI. Distinguir laboratorio técnico Sutherland de la futura Enterprise-D; no sustituir el piloto sin una decisión nueva. **Salida:** consola interactiva en escena UE, con actor/estado y botones conectados, no mock.

### Corte R4 — F08: primera guardia completa
Correr P01–P05 en secuencia con criterios positivos/negativos: orden legítima, contacto espacial, filtrado de conocimiento, barrido, análisis/parte, reacción NPC, reloj, guardado/carga en otro proceso y rendimiento aceptable. **Salida:** primera experiencia realmente jugable y acta reproducible; este es el gate principal para ampliar el resto.

### Corte R5 — F10/F11 y camino largo
Migrar protagonista fijo S04/F10 mediante sus dueños; integrar la Academia 2383–2387, decisiones y guardado. Para F11, coordinar con HOST el emisor institucional de producto, recorrer rangos, plazas, sucesiones, competencia, periodos de servicio, narrativa y acuse de ceremonias. **Salida:** trayectoria reproducible con rechazos/esperas, sin conceder rangos por diálogos, y acceso condicionado a Enterprise-D.

### Corte R6 — F09/F12/F13/F14: amplitud controlada
Después de la primera guardia, priorizar consolas necesarias, vida NPC mínima, un subsistema del universo offscreen y assets reales. Mantener dependencia temporal; no bloquear todo hasta modelar una galaxia exhaustiva. **Salida:** una pequeña nave/situación más rica con rendimiento y persistencia, con expansiones graduales.

### Corte R7 — F15: aceptación privada global
QA de campaña, rendimiento y estabilidad, localización española, errores de red/IA/TTS, backups/migraciones y build privado reproducible. **Salida:** aceptación del usuario en su equipo, sin distribución a terceros.

**Secuencia recomendada:** R0 → R1 → R2/R3 → R4 → R5 y R6 en subproyectos coordinados → R7. Los cortes no requieren una nueva «Planificación 3»: son prioridades dentro de F00–F15. No iniciar automáticamente modificaciones de otros proyectos al aplicar esta auditoría.

---

## 6. Reglas de coordinación y propiedad (anti-duplicación)

| Competencia | Dueño de la decisión/verdad | Consumidores |
|---|---|---|
| Identidad, eventos, tiempo, persistencia genérica | CoreRPG | Todas las fases |
| Reglas de mando, órdenes, sensores, Academia, carrera, misión | F04/F05/F06/F10/F11/F13 de Star Trek según dominio | HOST y Unreal |
| Sesión, autenticación/origen, enrutado institucional, proveedor IA central y composición | HOST | Fxx, UE5, NPC/diálogos |
| Pantalla LCARS, interacción 3D, cámaras, colisión, rendimiento | Unreal 5.8.2 / F07-F09-F14 | Jugador, HOST |
| Lore, cronología, biografías de personajes legendarios, identidad Enterprise-D | Decisiones/Lore vigentes | F01/F04/F10/F11/F13 |
| P2 B01–B10 | Planificación 2: contratos y propuestas offscreen | F13 implementa runtime cuando corresponda |
| Sistemas S01–S19 | Catálogo de necesidades/contratos funcionales (PR #173) | Fases propietarias, sin un segundo motor |
| Validación real de producto | F08/F15 y dueño de cada gate | Evidencias del MSI, CI, usuario |

**No adjudicar cambios transversales por esta auditoría:** las futuras auditorías de HOST, Lore, Planificación 2 y Sistemas resolverán sus propios defectos. Planificación 1 mantiene un **registro de dependencias y solicitudes** hacia esos ámbitos, sin reescribir su código o decisiones por inferencia.

---

## 7. Propuesta de matriz de aceptación que faltaba

Cada operación jugable seleccionada debe disponer de ficha con: ID de operación y fase, intención, actor y autenticidad, hechos/permiso de origen, propietario de reglas, precondiciones, revisión y tiempo Core, datos observables y prohibidos, comando/resultado/recibo, efectos confirmados, journal y persistencia, UI, mensajes y error/fallback, pruebas negativas, latencia/coste de CPU/GPU/VRAM, SHA del código y del asset, versión de UE, captura/log de MSI, repetición tras SAVE/LOAD, responsable y decisión de aceptación.

**Casos transversales mínimos recomendados:**
- Orden F05 de capitán NPC → F06 Sensores → informe de Ciencia → consecuencia persistida.
- Cambio de guardia con NPC ausente/enfermo, sustitución autorizada, orden diferida y relevo sin duplicidad.
- Contacto desconocido o perdido que no aparece como conocimiento identificado por la IA/LCARS.
- Retorno LOAD tras haber autorizado una promoción F11 pero antes de su comunicación, sin reemitir ni duplicar ceremonia.
- Academia F10: intro repetida/saltada, cuatro cursos, graduación y primer destino, mismo perfil autoral.
- Transferencia interconsola F09 con credenciales insuficientes, caducadas o revocadas.
- Salto temporal: F13 agrega acontecimientos fuera de pantalla, sin contradicción en posición/identidad de NPC presentes.
- Fallo/ausencia de OpenAI o TTS no bloquea órdenes, save/load ni el mundo.
- Sesión prolongada en RTX 4070 8 GB: VRAM, CPU, RAM, FPS/frametime y ausencia de crecimiento irrecuperable.
- Guardado legacy/corrupto/no confiable sin cambio silencioso de rango, identidad, nave o WorldState.

---

## 8. Cuánto falta: indicador de avance sin falsa precisión

**Diferenciar cuatro métricas:**
1. **Fases administrativas cerradas en registro de 03-11:** 5/16 (F00–F04), con madurez distinta y SIN equivalencia a 31 % jugable.
2. **Pasos sin marca CERRADA en registro de 03-11:** **51/80**. Este valor identifica **deuda de actualización + trabajo**, no 51 pasos inexistentes: F05/F06/F07/F11 ya evolucionaron en noviembre.
3. **Puertas jugables principales pendientes:** F07 UE5 completo, F08 aceptación de guardia, F09 estaciones, F10 Academia, F11 carrera, F12 vida social, F13 mundo vivo, F14 recursos integrados y F15 aceptación. Se añaden cierres formales/operativos F05 y F06.
4. **Avance cualitativo:** cimientos/contratos sólidos en F02–F05 y numerosas referencias probadas; **la mayoría del esfuerzo de producto jugable sigue por delante**, especialmente la integración transversal y contenido Unreal.

**No dar** porcentaje de horas, semanas o meses sin un WBS actualizado, dependencias resueltas y mediciones reales. Es legítimo indicar un mínimo de **11 fases globales por cerrar** y un primer hito verificable inmediato, F08. No considerar «todo planificado» sinónimo de «todo realizado» ni desmerecer los componentes ya certificados.

---

## 9. Lista de correcciones que debe procesar la conversación de Planificación 1

1. Ratificar esta auditoría como **diagnóstico**, no como permiso de cambiar otros proyectos.
2. Definir nuevo estado maestro actual con dos ejes (planificación/madurez), fotografía 19-11, PR y SHA; conservar trazabilidad de la fotografía 03-11.
3. Reparar el script de gobernanza, sus tests y workflow antes o conjuntamente con el registro nuevo.
4. Verificar cierre F05 #89, 14 errores globales UE, límites, acta y desbloqueo acotado de F06.
5. Reconciliar F06 #91/#96/#97, F07 #95 y F11 #110 sin asumir que una PR abierta forma parte de main.
6. Establecer el primer **camino vertical jugable F08**; usar el piloto Sutherland existente salvo decisión contraria explícita.
7. Reconciliar F01/F04/F06/F07/F11 con DEC-0020/0021 y F10 con DEC-0022, sin romper identidades antiguas/guardados.
8. Registrar P2 B01–B10 como referencia completada en la dependencia de F13, manteniendo el runtime F13 pendiente.
9. Reescribir puerta F15 de distribución pública por instalación y mantenimiento **privados**.
10. Añadir matriz anti-duplicación CoreRPG/Fxx/HOST/UE5/IA, CI para main y criterios E2E/telemetría; priorizar mínimo jugable y no más documentos por inercia.
11. Solo después, dividir correcciones en PR pequeñas, con pruebas, actas y auditoría de cierre. El autor conserva las decisiones creativas.

**Importante:** no declarar CERRADA ninguna nueva fase por leer este informe; la conversación responsable debe inspeccionar el estado vigente al aplicar cada cambio y citar evidencia actual del HEAD.

---

## 10. Índice de evidencia reproducible

**Gobierno y actas:**
- [ESTADO_GLOBAL.json](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/ESTADO_GLOBAL.json)
- [PLAN_MAESTRO.md](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/PLAN_MAESTRO.md)
- [CRITERIOS_DE_CIERRE.md](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md)
- [validate_roadmap_state.py](https://github.com/robdor80/Videojuego_StarTrek/blob/main/desarrollo/tools/validation/validate_roadmap_state.py)
- [Workflow de gobierno](https://github.com/robdor80/Videojuego_StarTrek/blob/main/.github/workflows/roadmap-governance.yml)
- [Auditoría histórica F07–F15](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/AUDITORIA_F07_F15_2026-10-15.md)
- [Auditoría Sistemas S01–S19](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md)

**Resultados y PR técnicos:**
- [F02 #60](https://github.com/robdor80/Videojuego_StarTrek/pull/60), [F03 #62](https://github.com/robdor80/Videojuego_StarTrek/pull/62), [F04 #76](https://github.com/robdor80/Videojuego_StarTrek/pull/76)
- [F05 #89](https://github.com/robdor80/Videojuego_StarTrek/pull/89) y [certificación MSI](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/fases/F05/F05-P05B_CERTIFICACION_INTEGRAL_MSI_20261105.md)
- [F06 #91](https://github.com/robdor80/Videojuego_StarTrek/pull/91), [#96](https://github.com/robdor80/Videojuego_StarTrek/pull/96), [#97](https://github.com/robdor80/Videojuego_StarTrek/pull/97); [F07 LCARS #95](https://github.com/robdor80/Videojuego_StarTrek/pull/95)
- [F11 #106](https://github.com/robdor80/Videojuego_StarTrek/pull/106), [#107](https://github.com/robdor80/Videojuego_StarTrek/pull/107), [#109](https://github.com/robdor80/Videojuego_StarTrek/pull/109), [#110](https://github.com/robdor80/Videojuego_StarTrek/pull/110), [issue #104](https://github.com/robdor80/Videojuego_StarTrek/issues/104)
- [F13/P2 B10 #122](https://github.com/robdor80/Videojuego_StarTrek/pull/122)
- [Proyecto UE principal](https://github.com/robdor80/Videojuego_StarTrek/blob/main/juego/UE5/StarTrekRPG/README.md)

**Precedencias autorales:**
- [DEC-0020 Enterprise-D](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md)
- [Transición F10/S04 de protagonista fijo](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/architecture/host/H06_S04_TRANSICION_PROTAGONISTA_FIJO_2026-11-17.md)
- [Plan F11 actualizado](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/fases/F11/PLAN_F11_ACTUALIZADO_2026-11-11.md)
- [F13 estado posterior a B10](https://github.com/robdor80/Videojuego_StarTrek/blob/main/proyecto/docs/roadmap/master/fases/F13/README.md)

**Límites de auditoría:** lectura de contenido textual y metadatos remotos; sin checkout local completo de todos los repositorios, sin inspección integral de archivos binarios/3D ni reproducción de builds/suites. Riesgos indicados como propuesta o no verificados no son bugs runtime demostrados. Las evidencias y estados pueden evolucionar tras el commit de referencia: recotejar HEAD antes de corregir.

---

**Dictamen final:** no reiniciar Planificación 1, no abrir más familias genéricas por reflejo y **no darla por terminada**. Reconciliar gobernanza, certificar los cortes pendientes, conservar lo ya probado y alcanzar primero la guardia F08 realmente jugable. Ese hito cambiará el valor del resto de fases de «preparación dispersa» a «sistemas integrados en una partida».