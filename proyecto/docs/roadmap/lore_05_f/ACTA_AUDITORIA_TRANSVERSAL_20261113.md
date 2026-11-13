# LORE-05F — Acta de auditoría transversal y propuesta de cierre global
**Fecha:** 13 de noviembre de 2026.  
**Repositorio:** `robdor80/Videojuego_StarTrek`.  
**Estado de este documento:** AUDITORÍA PREPARADA / CIERRE GLOBAL PROPUESTO. **La fusión de la PR de LORE-05F exige autorización expresa del autor.**  
**Alcance certificado:** documentación, identificadores y coherencia verificables; **no implementación jugable**.

## 1. Inventario de entradas y situación en GitHub

| Bloque | Entregable central | Fusión observada | Alcance |
|---|---|---|---|
| 05A | DEC-0020, Enterprise-D, Proyecto Valhalla, cronología | PR #124 + acta #125 | Reconciliación documental |
| 05B | 12 fichas de NPC y elenco cerrado | PR #126 | Personajes y continuidad propia |
| 05C | 16 lugares; 12 escenarios | PR #127 | Localizaciones de 2383 y límites de acceso |
| 05D | 8 buques, 12 instalaciones, 8 facciones + 2 instituciones; 18 escenarios | PR #128 | Identidades y gobierno |
| 05E | 8 lenguas, 18 reglas, 24 casos | PR #129 + regularización #130 | Traducción, comunicaciones, exploración |

Todas esas PR constan fusionadas en GitHub cuando se redacta esta auditoría. La evidencia de CI propia de A–E está en sus actas; **no se reutiliza el éxito de un HEAD anterior como certificación de esta PR**. La documentación histórica puede reflejar un estado anterior a la fusión y debe interpretarse con fecha y PR.

## 2. Cruces comprobados

### A × B × D — Una nave, una identidad, varios estados
- **Enterprise NCC-1701-D** = `uss_enterprise_ncc_1701_d`, matrícula `NCC-1701-D`, `class_id=galaxy`.
- **Proyecto Valhalla** = programa dirigido por Geordi La Forge para recuperar/reconstruir el mismo buque. No es una clase ni una segunda nave.
- Antecedentes: pérdida en Veridian III (2371); gestación de programa en 2379; obras desde 2380; todavía en obras al empezar la Academia en 2383; **2387 = objetivo condicional**, no alta cumplida.
- `class_id=valhalla` y sus 16 opciones VAL-TEC son legados históricos: no se migran ni instalan automáticamente. Tampoco 1.800+400 ocupantes, casco secundario Syracuse, Defiant auxiliar, motor de flujo cuántico, plaza del jugador o mando.
- Geordi figura capitán al comienzo de 2383 y contraalmirante como promoción futura dentro de 2383–2387. Su cargo técnico no equivale a mando de la nave.
- La USS Defiant original `NX-74205` destruida en 2375 NO es la posterior São Paulo rebautizada. Odyssey es una clase/conjunto de unidades, no un individuo Enterprise-F nacido automáticamente del catálogo.

### B × A × E — Personajes y calendario de campaña
- El elenco televisivo legendario de LORE-05B queda cerrado en **12**. No incorporar extras disfrazados de extensiones de 05F.
- Picard entrega **personalmente** los galones al jugador cuando obtenga legítimamente el grado de capitán. F11 determina ascenso y acto; la ceremonia es hito narrativo, nunca atajo en la carrera.
- Data falleció en 2379. Su recuperación investigada por Geordi, con B-4 y archivos positrónicos, está condicionada al arco 2390–2395; memoria copiada no garantiza identidad/conciencia.
- Sisko permanece entre los Profetas en 2383; su eventual vuelta 2388–2392 requiere evento efectivo antes de conceder cargo posterior.
- La edad de Siete (~35 años al encuentro significativo) y el ancla 2358/2393 **no son fechas irrevocables**; se deben reconciliar con la fecha de los encuentros y la continuidad alternativa.
- Guinan es civil; el nuevo Ten Forward solo puede existir/funcionar a bordo **después del alta efectiva de la Enterprise-D** y con servicio y dependencias disponibles. Su emplazamiento físico en cubierta E sigue pendiente de validación.

### C × D × E — Lugares, autoridades y descubrimiento
- Las 16 entradas de 05C incluyen anclajes preexistentes, contexto Sol/Marte y colonias únicamente históricas. **Nueva Bajor no se repuebla automáticamente**; Dorvan V no adquiere un estado actual inventado.
- DS9 conserva una identidad `canon:facility:deep_space_9` y jurisdicciones que no se deducen del diseño Terok Nor; Bajor sigue siendo soberano.
- Una instalación reservada no implica personal, muelles operativos, combustible infinito ni derecho de entrada. Que el jugador viaje a una ubicación no materializa población o estaciones.
- Federación civil, Flota Estelar, gobierno bajorano y demás poderes conservan atribuciones distintas. La traducción de un mensaje nunca valida por sí misma una orden o un tratado.
- Existencia física ≠ observación ≠ conocimiento ≠ autorización ≠ descubrimiento publicado. Los datos de sensores solo pueden proceder del universo causal; IA y PADD no revelan datos ocultos.
- Primer contacto exige autoridad, respeto cultural, consentimiento, Primera Directriz y evaluación de soberanía. La comunicación puede fallar, retrasarse, ser parcial o ser rechazada.

### E × contratos propietarios — Conteos correctos
- El catálogo de idiomas contiene **8 registros**, entre ellos kazon y talaxiano bajo `DLC_DELTA_FUTURE`.
- El contrato propietario del traductor contiene **6 estados** y su overlay conserva exactamente los seis.
- `subspace_communication_contract.json` contiene **10 estados de enlace** y **11 campos de entrada** (`link_inputs`). El acta histórica E04 decía por error «once estados de enlace». Esta auditoría exige aclarar el texto, **sin modificar el contrato técnico ni inventar un estado 11**.
- Los 18 enunciados narrativos y 24 casos de 05E son **documentales**; no son 24 encuentros simulados ni 24 diálogos jugables.

## 3. Hallazgos administrativos y correcciones
| ID | Severidad | Hallazgo | Tratamiento |
|---|---|---|---|
| F-01 | Editorial | El acta de 05B conserva la cabecera histórica «NO FUSIONADO / Draft», posterior a la cual GitHub fusionó PR #126. | Mantenerla como evidencia de precierre, aclarar en 05F y en índices que la PR está realmente fusionada. No adulterar el informe original. |
| F-02 | Enlace | `proyecto/docs/roadmap/README.md` enlaza el elenco 05B con `../../mundo/...`, que desde esa carpeta resuelve a `proyecto/mundo`. | Corregir a `../../../mundo/...` y validar la existencia de destino. |
| F-03 | Conteo | Acta 05E menciona 11 estados de enlace; fuente y overlay tienen 10 estados, 11 entradas de configuración. | Fe de erratas explícita en el acta; no tocar JSON propietario. |
| F-04 | Redacción | El estado global sigue llamando «propuesta» al arranque 2383 en una tabla histórica pese a DEC-0020. | Precisar que **el año 2383 está aprobado**, permaneciendo abiertos día y mes. |
| F-05 | Certificación | Las actas de 05B/C/D consignaron precierre o verificaciones de un HEAD previo. | **Resuelto por esta auditoría:** el HEAD definitivo de cada una registra 20/20 workflows de PR en SUCCESS y todas las PR están fusionadas. No se confunde CI de PR con CI posfusión. |
| F-06 | Técnico diferido | Migraciones Valhalla, implementación/activos de NPC, estado vivo de instalaciones, sensores, primera directriz y PADD no son runtime. | Matriz de responsables y puertas de integración por fases. |

**Resultado editorial:** ningún conflicto irresuelto en los IDs de los cinco bloques que invalide el cierre de su biblioteca documental tras aplicar F-01 a F-04. Los huecos narrativos individuales y dependencias de runtime siguen abiertos **sin convertirlos en ficción ya materializada**.

### Certificación independiente de HEAD finales A–E
- **05B — PR #126:** último HEAD `67b1eaa6f6fa1427f22400bae0dac40fabb95564` con **20/20 workflows de pull_request SUCCESS**; squash `4df4d23f2e050bba830f6696a27bb6d4c004fd2f`. No hay workflow específico B: 84/84 son controles de la auditoría editorial de sus fichas.
- **05C — PR #127:** último HEAD `4ea1c0871c99dcc88fba396bc2f9725232e1bf72`, **20/20 workflows de pull_request SUCCESS**; [workflow LORE-05C #43353283486](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43353283486) y squash `5cecf75fa647e60c050b40c7c6d2ce87ec6e2e95`.
- **05D — PR #128:** último HEAD `6b265245a6dbe706b71e45bbc27e04c09191a54b`, **20/20 workflows de pull_request SUCCESS**; [workflow LORE-05D #43354607817](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43354607817) y squash `54de78c2240e7876d4ef3d2b1c96bbe1f55e8f29`.
- **05A:** fusión PR #124 y regularización #125 con resultado descrito en su acta. **05E:** fusión PR #129 y regularización #130 con 7/7 workflows del HEAD final según su acta.
- El control de **05F** (29 tests de documento y workflow propio) debe volver a verificarse tras la última edición de esta PR. Estos resultados no prueban implementación CoreRPG/HOST/UE5.

## 4. Límites y trazabilidad del cierre
- **CoreRPG:** autoridad única sobre WorldState, fechas, identidad vigente, permisos, conocimientos, agendas, recursos, eventos, ascensos y guardado.
- **F04/F05:** entidades, naves y contratos; sin actualizaciones automáticas ni migración silenciosa de clases, IDs o partidas.
- **F06:** sensores, observables, interpretación de lecturas y consolas según contratos de cada fase.
- **F11:** rangos, cargos, cadena de mando y emisor institucional. **HOST no duplica ni reimplementa F11**.
- **HOST:** coordina sesiones/servicios y consulta datos autorizados. No es autor institucional ni fuente de hechos.
- **P2:** economía, progreso y evolución offscreen causal; sus documentos no equivalen a simulación viva.
- **UE5/Blender:** presentación, naves, cubiertas, colisiones, PNJ, audio y LCARS; validar derechos y activos antes de uso.
- **PADD externo:** conocimiento adquirido **y** permiso efectivo; excluir secretos de la exportación.
- **Lore y canon:** clasificar `SCREEN_CANON`, `OFFICIAL_REFERENCE`, `INFERRED`, `GAME_ADDITION` y propuestas futuras. El futuro mostrado en *Picard* no obliga a la campaña que arranca en 2383.

## 5. Evidencia automatizada de esta subfase
- `desarrollo/tools/validation/validate_lore05_f.py`: cruza bibliotecas 05A–E con catálogos originales, comprueba IDs y barreras de autoridad.
- `desarrollo/tools/validation/test_lore05_f.py`: casos positivos y mutaciones negativas que deberán ejecutarse en GitHub Actions.
- `.github/workflows/lore05-f-documentary.yml`: ejecución independiente de validación transversal.

**Importante:** esta acta no presupone que los tests ni el workflow hayan finalizado correctamente en el HEAD definitivo. La conclusión del CI debe incorporarse a la revisión de PR antes de cualquier fusión.

## 6. Puerta de cierre global
LORE-05 quedará `COMPLETE_DOCUMENTARY` **solamente cuando**:
1. Los ajustes F-01–F-04 consten en la PR y se valide la coherencia transversal del HEAD definitivo.
2. El workflow LORE-05F y las comprobaciones obligatorias resulten satisfactorios.
3. El usuario autorice **expresamente** la fusión y esta se complete en `main`.
4. Se actualicen `CONTENT_STATUS.md`, índices y acta posfusión con el commit real, sin dar por completados CoreRPG/HOST/UE5.

**Dictamen actual:** PRECIERRE DOCUMENTAL **FAVORABLE CON CONDICIONES**. Cinco subfases A–E fusionadas; LORE-05F queda preparada para revisión y fusión autorizada. Ninguna deuda técnica diferida obliga a reabrir LORE-05 si se mantiene claramente asignada.
