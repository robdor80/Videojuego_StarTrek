# P2-B07 — Acta de cierre de referencia (12/11/2026)

**Objeto:** Bloque 7 de 10 — Fenómenos, anomalías y arqueología procedural.
**Propietario:** reglas específicas Star Trek; CoreRPG conserva autoridad, estado, reloj, guardado, posesión y cambios reales.
**Cierre técnico propuesto:** `REFERENCE_COMPLETE` de contratos, simulador offline, fixture y pruebas. Cierre administrativo sólo tras último CI verde y fusión de la PR [#116](https://github.com/robdor80/Videojuego_StarTrek/pull/116). **No** se declara F13 completada ni UE5 jugable.

## Auditoría inicial

- PR #115 de B06 fusionada en main (12/11/2026); respetada la secuencia B1–B6.
- Se reutilizan sin reescribir `anomaly_temporal_state_contract`, `observable_entity_model`, `detectable_signature_model`, `persistent_entity_identity_contract`, atlas científico LORE-02 D, F06, B05, B06, los límites LORE-02 D y F13.
- No se introduce otro escritor del WorldState ni un detector alternativo a los sensores. Sin nuevos assets/binarios/cachés en Git. `laboratorios/` sigue excluido.

## Contenido aprobado como diseño autónomo

1. PA001–PA018: tipologías ordinarias y excepcionales; canon y lugares protegidos; ID por campaña y slot; formación causal tanto antigua como durante campaña; rareza reproducible; persistencia de slots vacíos; señales físicas separadas de percepción; vida temporal, custodias y arqueología.
2. Ruinas con procedencia cultural/estrato, permitidas sólo si hubo origen causal aceptado y permiso del custodio; el artefacto no cambia de propietario por ser excavado.
3. Dos observadores e instrumentos independientes para una **interpretación apoyada, no certeza**; contradicción no resuelta bloquea conclusión; no se concede tecnología, mapa o conocimiento universal.
4. Mensajes con tiempo de entrega y clasificación, proyección individual para NPC/ordenador/PADD; sin revelación global ni necesidad de que el jugador visite el lugar.
5. Sujeto extraordinario temporal/dimensional, Omega o nuevo agujero de gusano excluidos de generación automática; sin viaje temporal jugable. Una anomalía tampoco crea una crisis, misión o ruta.
6. Física y arqueología pueden evolucionar por hechos posteriores **aceptados**. B08 reaccionará si procede al riesgo existente, nunca a un peligro improvisado por el bloque.

## Diseño y fixture verificable

- `sistemas/universe/generation/phenomena_anomalies_archaeology_reference_contract_v0.1.json`.
- `desarrollo/tools/generation/simulate_phenomena_archaeology.py`.
- `desarrollo/tools/generation/test_simulate_phenomena_archaeology.py`.
- `desarrollo/validation/fixtures/phenomena_archaeology/phenomena_archaeology_exploration_v0.1.json`.
- `.github/workflows/p2-b07-phenomena-archaeology.yml`.
- `proyecto/docs/roadmap/procedural_phenomena_archaeology_status_v0.1.json`.

Dos ubicaciones **sintéticas, no canónicas**: perturbación en un sector y ruinas lunares protegidas. Se materializan dos entidades persistentes, se obtienen cuatro evidencias de observación, se interpretan prudentemente, se modifica una fase física por causa aceptada, una arqueóloga registra un hallazgo de estrato bajo permiso y otro NPC recibe un mensaje con retraso. **Ningún inventario, clase de nave, misión, crisis, ruta, tecnología o entidad canónica resulta modificado.**

## Evidencia técnica

**Primera ejecución controlada:** [Actions P2-B07 #43206224117](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43206224117) **SUCCESS** sobre el commit `5ef16d4eb1ca8c7d099a8e2f56c6a0392ab1ac99`. Logs: 54/54 pruebas del primer borrador B07, 206/206 regresiones B1–B7 y 29/29 F13, sintaxis, contrato/fixture JSON y CLI sin error.

**Certificación ampliada de código y roadmap:** [Actions P2-B07 #43207092271](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43207092271) **SUCCESS** sobre el commit `ba881f723f1a2bc8180402081a42889d8388a639`: **56/56** pruebas B07, **208/208** B01–B07, **30/30** F13, validación de JSON, sintaxis y CLI determinista. La revisión añadió generación por causa física posterior al corte, prohibición de reintentar un slot vacío y puerta estricta B07→B08. El mismo commit obtuvo **19/19 workflows SUCCESS**, incluidos F13, B06, LORE-02, auditoría y gobierno del roadmap. Ninguna de esas pruebas prueba integración de producción.

La sincronización documental final se hará en un commit posterior: **verificar el CI de ese HEAD antes de fusionar**; la ejecución indicada arriba es evidencia del código y su frontera, no certificación automática de cualquier edición futura.

## Límites verificados y pendientes de ejecución real

- Las fuentes con `status=accepted` son afirmaciones de un fixture local; jamás se han contrastado con firmas, WorldState de CoreRPG, sensor F06 físico, servidor HOST o datos de una partida.
- No se simula geología/astronomía físicamente, riesgo radiológico real, permisos de una facción viva, propiedades del inventario, ni autonomía de investigación NPC de producción.
- No hay scheduler B10, save/load Core, registro de eventos histórico B05 real, interacción de cubiertas, escenas 3D UE5 o PADD operativo.
- Las reglas de Primera Directriz y soberanía siguen requiriendo autoridad contextual. Una excavación en zona no autorizada se rechaza.
- Sin conflictos con Omega (misión especial narrativa pendiente), con la reserva canónica del agujero de gusano bajorano o con la prohibición de viajes en el tiempo jugables.

## Puerta B08 y estado global

**Bloque 8 — Crisis sistémicas** será el siguiente a partir de la fusión de esta PR y del éxito final de CI. B09 misiones y B10 motor galáctico permanecen cerrados. Las 120 capas siguen 118 completas de referencia, 119 parcial y 120 bloqueada por runtime. F13 global permanece **PLANIFICADA**.

**Administración:** contenido y CI de código certificados en PR #116; fusión condicionada a CI verde del último commit documental. El cierre administrativo de esta acta se hace efectivo con la fusión, sin elevar F13 ni CoreRPG/UE5 de estado.
