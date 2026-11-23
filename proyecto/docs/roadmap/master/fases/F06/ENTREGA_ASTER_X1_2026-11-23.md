# Entrega técnica F06 / ASTER_X1 — 23-11-2026

**Estado:** implementación para revisión en Draft #206. Aceptación visual MSI y cierre F06 pendientes. Fuente contractual: [especificación aprobada](ESPECIFICACION_REMATE_ASTER_X1_2026-11-23.md). [Arranque y recorrido sencillo](../../../../../../desarrollo/integration/f06/qa/GUIA_PRUEBA_ASTER.md).

## Integración y procedencia

Se conserva `2a6b5741` de preparación, la historia #91→#96→#97 y sus ramas originales. Un merge local incorpora el HEAD #91 `0f67affe`: la divergencia respecto a la pila solo añadía dos registros de ensayo. Otro merge incorpora `main@7adaf964`; la revisión de main posterior `8edce7bd` solo cambia H08-P04, sin diferencias F04/F05/F06. No se han fusionado PR productivas ni reescrito ramas anteriores.

La transición F04 ya auditada en main cambió los anclajes de ensamblado. El overlay F06 verifica ahora `history_reference_v2.json`, conserva intactos los archivos originales F04/F05 y sus oráculos v1/v2, reserva las extensiones nuevas desde el campo 512 y conserva los ID anteriores F06 y F11 (256). Core permanece fijado a `76a7b7b485616d8c4994f384a90f123bf333591d`. Se consultaron las cuatro PR, la auditoría de Planificación 1 y R2 en `#179@1fb5b0dc`.

## Implementado

- Puerto privilegiado `f06_host_physical`, versión 1, que materializa equipamiento instalado, estado energético/operativo, longitud y firmas de observabilidad antes de publicar el estado espacial visible. Una máscara efectiva de camuflaje QA impide detección incluso con emisiones. No se expone este puerto al protocolo de la GUI.
- Inventario por unidad en WorldState; observaciones públicas inmutables `f06_equipment`, histórico solo cuando cambia la medición, procedencia de instrumento F06, reloj, confianza, máscara de cobertura y versión del catálogo. Categorías: emisores ofensivos, lanzadores, escudos, blindaje, motores warp e impulso. Recuentos agrupados por categoría; no se inventan tipos de proyectil, posiciones de montaje ni detalles internos que este modelo no mide.
- Referencia técnica independiente `equipment_catalog_qa_v1.json`. Sus cifras se etiquetan **QA ficticia/no canónica**. La D'deridex realmente instalada difiere del catálogo; no existe una condición por ID de contacto en Tk que fabrique la modificación.
- Adquisición naval nominal determinista para la extensión física: firma emitida positiva, alcance operativo, sin camuflaje ni interferencia real, sensores/configuración nominales. Las firmas legacy conservan sus umbrales. Daño, falta de potencia, interferencias, distancia y cobertura oculta siguen afectando al modelo físico. Clase cero sigue siendo desconocida y no bloquea medir equipos.
- Ficha automática central y resumen operativo siempre visible; detalle y scroll, tres zonas, selección preservada ante llegadas rutinarias. Comparaciones verde/ámbar/rojo/gris producidas por F06; ningún diccionario de armas en Tk. El rojo requiere emisión ofensiva real.
- Entregas voluntarias `f06_deliver`: actor F04 autenticado, cualificación/guardia/ubicación sensorial, revisión, clave idempotente y recibo persistente vinculado a una observación inmutable. Destinos: superior, Táctica QA y Ciencia QA. El acuse demuestra entrega al registro/cola Core QA; no acredita lectura de un NPC ni procesamiento científico definitivo. La cola científica existente de estudios profundos sigue disponible.
- Guardia separada de 540 segundos, semilla reproducible, entradas a 60/150/240, modificación a 210, emisión activa a 300, negativo camuflado a 360 y descamuflaje a 390, avería a 450 y recuperación a 465. Hay además una unidad fuera de alcance. El fixture JSON histórico de ocho horas no se modifica.
- Tiempo interactivo basado en reloj monotónico, no en contar callbacks de Tk. ×1 usa un segundo Core por segundo real y compensa el coste del callback en el siguiente ciclo. Telemetría de fuente/recepción/publicación/refresco y origen real de la aparición, sin presentar ticks como latencia MSI.
- SAVE/LOAD en memoria y archivo QA para otro proceso. Se conservan contactos, equipo, observaciones, identificadores, recibos y cursor de avisos sin reenviar entregas. Se rechazan números con sufijos, versiones, revisiones y solicitudes inválidas; las preferencias de navegación de Tk son locales.

## Matriz de comprobación

Los resultados precisos y los SHA se registran en CI del HEAD publicado. Cloud Linux usa compilación Release, Core real, Tk real en Xorg; no mocks de observación ni pruebas MSI.

| Prueba | Verificación automatizada / evidencia | Alcance |
|---|---|---|
| T01 | `aster_x1_acceptance`, inicio Core t=0, automático ON, carguero inicial con equipo | Core |
| T02 | Paso 59→60; transpondedor, clase, ficha y observación en el primer ciclo | Core + Tk |
| T03 | D'deridex 150, transpondedor 0, 8/3 observados frente a 6/2; ámbar | Core + Tk |
| T04 | Clase 0, inventario medido, sin catálogo prestado; blindaje interno redaccionado | Core + Tk |
| T05 | Carguero nominal: conteos cruzados y verde | Core |
| T06 | Cambio real 210 y emisión 300; nueva observación, sin duplicarla en STATUS | Core + Tk |
| T07 | Camuflado/fuera de alcance sin contacto, inventario ni aviso; descamuflaje 390 | Core |
| T08 | Plumbing nativo monotónico + recorrido completo `--realtime` de nueve minutos en Cloud, SLA de apariciones ≤3 s | Cloud; MSI pendiente |
| T09 | Archivo Core en un proceso, restauración en otro, fichas/recibos idénticos y reintento deduplicado | Core real multiproceso |
| T10 | `equipment_contract`, protocolo y regresiones: rol, actor falso, revisión, ID, formato, replay y no mutación | Core/F04/F05/F06 |
| T11 | Dos recorridos Tk reales, colores, órdenes, scroll y geometrías 1460×825 / 1150×700 | Linux Cloud; MSI pendiente |
| T12 | Dos repeticiones misma semilla/cadencia y semillas 7/11 diferentes; generador de catálogo valida tipos/rangos/duplicados | QA determinista |
| T13 | Superior/Táctica/Ciencia: tres recibos Core, observación capturada, persistencia y reintentos | Colas QA |
| T14 | Matriz sin potencia no mide; recuperación autónoma. Suite previa cubre degradación/interferencia | Core |
| T15 | Suite separada de ocho horas Core con cadencias ×15/×30/×60, inventario y vigilancia sin envíos | Acelerada; no prueba de SLA ×1 |

Los logs brutos, compilaciones y capturas permanecen en el laboratorio local ignorado; no se fuerza su inclusión en Git. Los resultados JUnit, resumen de comandos, telemetría ×1 y resumen de ocho horas se publican como artefactos de Actions. El workflow nativo comprueba Linux y Windows, más Tk/reloj real en Linux. No atribuir PASS a un check todavía pendiente o fallido.

## Límites y puertas que siguen abiertas

1. Aceptación visual real del propietario en el MSI: **NO EJECUTADA por Codex**. Validar fluidez, legibilidad, tiempos y recorrido de [la guía](../../../../../../desarrollo/integration/f06/qa/GUIA_PRUEBA_ASTER.md).
2. F05: conciliación administrativa/acta y tratamiento de los 14 mensajes globales de arranque UE de su certificación previa; no declarar Unreal libre de errores por esta entrega.
3. F06/P01: revisión íntegra visual del PDF/manual y de su árbol de diez ramas frente a versión/hash; pendiente según R2. Esta entrega no emite conformidad visual de ese manual.
4. F07: LCARS/UE5 5.8.2 y modelos/visor 3D no se implementan aquí. F08: guardia integral en Unreal no certificada. F13: productor espacial persistente de producción no implementado; el productor de este ensayo es QA controlado y determinista.
5. El casco de prueba F04 es Miranda sintética con perfil sensorial individual Enterprise-D modernizada; no se afirma un casco Galaxy físico. Los valores físicos y catálogos QA no son canon.
6. Camuflaje efectivo y observabilidad son abstracciones físicas explícitas QA; no un modelo espectral exhaustivo. Equipamiento agrupado en seis categorías, sin munición, arcos de tiro ni localización individual de cada montaje. Estado interno sin señal no se publica.
7. Los archivos QA locales no son un formato seguro para recibir mundos de un emisor externo. Los puertos Host permanecen privilegiados y no deben exponerse a IA, red o scripts no confiables. No hay dependencia obligatoria de red/IA durante la guardia.
8. No hay consumidor NPC/UE final para las colas de entrega. Un recibo afirma almacenamiento en la cola QA autenticada del Core, no una conversación ni una investigación finalizada.

**F06 permanece abierta y la PR permanece Draft.** El propietario conserva la decisión de aceptación y las puertas del roadmap no se rebajan.
