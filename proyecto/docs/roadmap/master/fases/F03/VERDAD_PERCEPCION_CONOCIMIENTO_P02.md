# F03-P02 — Verdad autoritativa, percepción, conocimiento y privacidad

**Fecha:** 2026-10-11. **Estado:** DISEÑO CON REGLAS DE ACEPTACIÓN; integración Core Knowledge 4.9 **BLOQUEADA**. **Entrada:** [P01](CONTRATO_IDENTIDAD_MATERIALIZACION_P01.md).

## Frontera de datos (no se crea implementación Core)

| Capa | Propietario | Contiene | Acceso |
|---|---|---|---|
| Verdad del mundo | CoreRPG World State | `entity_id`, `ground_truth`, posiciones, firmas, datos ocultos, estados reales | Solo procesos autorizados de resolución; **jamás** payload bruto a UI/IA |
| Fenómeno captado | Sensores Trek contra verdad existente | Firma detectable, señal/ruido, filtros, integridad/energía, efectos ambientales | Calculado por resolución autorizada; no muta la entidad objetivo |
| Observación | Resultado del operador/nave | `contact_id`, intervalo, confianza, resolución y datos realmente detectados | Solo observador/contexto legítimo |
| Conocimiento de nave | Core Knowledge futuro + contrato Trek | Contactos, informes, permisos de acceso, evidencias y vigencia | Proyección según rol, autorizaciones y registros compartidos |
| Conocimiento de individuo | Core Knowledge futuro + memoria actor | Qué vio/oyó/leyó, por qué canal y cuándo; incertidumbre | No hereda conocimientos de otro NPC por pertenecer a misma nave |
| Consola/IA/UE5 | Proyección de lectura, efímera | Campos ya autorizados, nunca verdad completa por conveniencia | Sólo datos explícitamente concedidos; propuesta IA no es mutación |

Fuentes originales: `sistemas/universe/generation/observable_entity_model.json`, `sistemas/gameplay/ship_operations/sensor_resolution/sensor_result_contract.json`, `sensor_detection_rules.json`, `sistemas/gameplay/ship_operations/operational_event_log/visibility_projection_rules.json`, `sistemas/gameplay/ship_operations/ship_memory/contact_dossier_model.json`, `sistemas/ai/memory/character_memory_lifecycle_contract.json`. Paquete INT-03 / adaptadores ADP-05 y ADP-07 de F02 PR #3.

## Invariantes obligatorias

1. `observación != realidad`: sensores imperfectos devuelven incertidumbre, falsas hipótesis con procedencia o contactos parcialmente resueltos, **no** cambian la realidad para hacer coincidir la hipótesis.
2. Contacto es clave **relativa al observador**: para el mismo `entity_id` dos naves pueden mantener `contact_id` y estados distintos. Asociarlos internamente no autoriza revelar su equivalencia.
3. Según `sensor_result_contract.json`, niveles de resolución: `trace_detected`, `detected_unclassified`, `partially_resolved`, `resolved`. Clasificación sólo con `resolved`; propiedades ocultas sólo si se acreditó su desbloqueo.
4. **Prohibido** exportar `authoritative_entity_id`, `ground_truth` o `unrevealed_hidden_properties` a payload de usuario. Es una lista mínima, no exhaustiva: prevenir también secretos dentro de `payload`, texto de narración, logs de depuración y claves dinámicas.
5. Un evento append-only no da omnisciencia: filtrado por `visibility` + canal plausible (participación, testigo presente, informe autorizado, transferencia entre consolas o briefing). Archivo médico/privado requiere autorización adicional.
6. Un informe a Ciencia transmite **sólo** los datos explicitamente seleccionados y autorizados. Una bitácora operativa contiene evidencia, pero no conocimientos universales.
7. Memoria personal = reconstrucción derivada de sucesos realmente conocidos; puede ser incierta y reinterpretarse sin mutar el evento original. LOD y Save/Load no resetean conocimientos.
8. IA remota recibe sólo el paquete filtrado; pérdida de IA ⇒ interfaz local degradada, nunca bypass de permisos. Respuesta antigua ⇒ revalidar antes de mostrar o ejecutar acciones.
9. La consulta de datos no puede aumentar el nivel de observación en silencio, ni desencadenar «generación de verdad» al pulsar Escanear.
10. La revocación de permiso impide las nuevas lecturas; no borra retroactivamente recuerdos legítimos sin un mecanismo de seguridad explícito.

## Algoritmo conceptual de proyección (no implementación ni API)

`validar actor/contexto → consultar solo mundo existente → resolver sensores con recursos/obstáculos → redactar visión permitida por conocimiento+rol → emitir registro de observación con sello de tiempo y procedencia → entregar payload autorizado`.

**Regla de denegación:** sin observador validado, permiso, estación o evidencia de adquisición, resultado es denegación segura; nunca fallback a `ground_truth`. Incluso como capitán, los permisos de una consola no convierten la biografía privada de todos en información automática.

## Ejemplo de referencia falsable

La nave `ship_alpha` detecta a `ship_beta` como contacto `contact_s_alpha_04` e interpreta «emisión subespacial, origen no identificado» con `confidence=0.62`. `ship_gamma` puede detectar el mismo objeto como `contact_s_gamma_02`, sin firma suficiente para clasificarlo. El `entity_id` interno no figura en ninguno de los dos payloads. Ciencia sólo recibe la observación de Alpha cuando existe transferencia permitida. Esta ilustración **no** constituye una exploración realmente ejecutada.

## Casos obligatorios F03

- `F03-T06`: dos observadores, diferentes contactos y evidencias, sin correlación gratuita.
- `F03-T07`: recepción con nivel inferior no revela clasificación ni hidden props.
- `F03-T08`: evento con visibilidad restringida no aparece en log público ni memoria de ausentes.
- `F03-T09`: informe/transferencia autorizado entrega un subconjunto preciso y no el objeto bruto.
- `F03-T10`: IA simulada inyecta secreto no disponible ⇒ revalidación y rechazo.
- `F03-T11`: observar sin permisos/credenciales ⇒ denegación, sin modificar verdad.

**Alcance de pruebas de esta PR:** fixture y validador local para límites de datos estructurados; **NO** interfaz Knowledge del Core, ejecución de consola ni E2E. Los tests efectivos del Core quedan pendientes hasta 4.9.
