# F04-PERSISTENCIA-03 — Persistencia histórica autoritativa

31-10-2026. **Implementación y aceptación de PERSISTENCIA-03 completadas: 365 días en las cinco clases y 730 días en Valhalla, con guardias reales y auditoría íntegra. Pendiente auditoría independiente de ambas PR Draft.** F04 sigue EN_CURSO. No se inicia INTEGRACION-04 ni CIERRE-05. Ninguna PR se fusiona aquí.

Base Star Trek: `45f7816c9aa996bfd678b11b4f9fa1a4b9632021`.
Rama existente: `codex/f04-persistencia-03-campanas-largas`, PR #76.
Core propuesto: [PR Draft #13](https://github.com/robdor80/CoreRPG/pull/13), rama
`codex/core-history-segments-authoritative`, revisión exacta
`89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`, desde
`c147d81ed069da2e09149613ab02cbc3ebe95a4a`.

La [autorización expresa](https://github.com/robdor80/Videojuego_StarTrek/pull/76#issuecomment-6536894218)
aprueba la ampliación genérica antes propuesta en el apartado 5. El
[diagnóstico previo](F04-PERSISTENCIA-03_DIAGNOSTICO_PREVIO.md) se conserva como
registro de la entrega anterior; sus resultados de saturación no son la aceptación
actual. No se han cambiado recursos 3D, Blender, texturas ni otros proyectos.

## 1. Separación de responsabilidades y compatibilidad

CoreRPG administra `HistoryArchive`/`HistoryPersistence`: identidades emitidas,
localización residente/archivada, payload original inmutable, índices comprobados,
SHA-256, cadena de segmentos, manifiesto, checkpoint, reducciones, publicación y
recuperación. No conoce naves, guardias, Marines, civiles ni reglas de Star Trek.

Las firmas, disposición y semántica monolítica de WorldState, Persistence,
CampaignPersistence y Timeline se conservan. SAVE v1/v2/v3 y CRPGTIME v1 siguen
vigentes. Las clases anteriores solo reciben declaraciones friend sin cambio de
layout. El contenedor histórico tiene magic y versión propios, optativos.
`contains` y `entity_count` conservan el significado de IDs emitidos; la residencia
se consulta expresamente con APIs nuevas. Archivar no borra una identidad ni
permite volver a emitirla. No ha sido necesario un cambio incompatible de ABI.

F04 adopta esa proyección activa mediante APIs adicionales ABI 1. La política de
retención y autorización sigue en F04. El presupuesto productivo permanece en
65.536 entidades **residentes**. No se eleva el techo, no se renumeran IDs, no se
regeneran hechos desde semillas y no existe un almacén autoritativo alternativo.

El pin estable `desarrollo/integration/f04/core-revision.txt` permanece en
`c147d81ed069da2e09149613ab02cbc3ebe95a4a`. La integración propuesta exige
`F04_ENABLE_HISTORY=ON` y verifica el SHA independiente de
`core-history-revision.txt`. El modo predeterminado conserva el pin estable.

## 2. Consolidación y determinismo

F04 conserva presente, futuro, siete días operativos anteriores, REST con deuda,
ABSENCE que cruza la frontera, tareas pendientes y las dependencias transitivas
de todos los registros retenidos. No basta la antigüedad para cerrar un hecho.
Se mantienen personas, plazas, competencias, censo, residencia y grupos.
Los hechos cerrados conservan exactamente definición, relaciones, contención,
emisor, persona, plaza, causa, PLAN/ACTIVITY/origen, STOP, suplencias y revocaciones.

Core deriva el acumulador de equidad por persona de los hechos originales:
DUTY con `(STATE==ACTIVE || STOP existe)` y
`START < min(END, STOP si existe)`. F04 puntúa el número archivado más
`p.work.size()` residente. Las ventanas recientes de 168 h, la restricción diaria,
las 12 h de descanso y las ausencias siguen usando los intervalos reales.
Core vuelve a calcular el acumulador durante recuperación y exige igualdad con
el manifiesto. No se sustituyen los hechos consultables por un resumen.
No se añade SCHEMA 5: la reducción pertenece al manifiesto Core versionado.

La selección F04 retiene los objetivos de referencias de cualquier registro vivo,
incluidos planes y actividades origen. La validación semántica F04 de la proyección
resultante se ejecuta antes de la publicación Core. Consolidar aumenta una revisión
técnica, conserva el high-water mark y no consume RNG ni avanza el reloj.

## 3. Publicación, fallo y recuperación

Core prepara segmento/checkpoint/manifiesto, comprueba los objetos y sincroniza
sus escrituras. Publica una generación mediante reemplazo atómico de CURRENT.
Windows usa FlushFileBuffers y MoveFileExW con WRITE_THROUGH; Linux usa fsync,
rename y sincronización del directorio. Un bloqueo de proceso y la comparación
del root/generación impiden que un escritor obsoleto reemplace otro commit.
Se conservan las generaciones anteriores y los originales de migración.

La recuperación valida la generación completa, cada segmento, sus índices,
propiedad de IDs, referencias, reducciones, reloj y RNG antes del intercambio.
No mezcla generaciones ni hace rollback silencioso ante una raíz confirmada
corrupta. Los objetos incompletos no referenciados no adquieren autoridad.
Un resultado de commit incierto bloquea el uso de la sesión F04 hasta recuperar.
Los hashes comprueban integridad; no autentican a quien sustituya la raíz confiable.

Las pruebas incluyen las seis fronteras de publicación entre procesos,
lectura fallida, objetos ausentes/truncados/modificados, manifiestos desconocidos,
cadena y acumulador falsificados con hash válido, rechazo de payload histórico
reintroducido y de escritores obsoletos. La integración F04 añade un fallo real de
reemplazo de CURRENT por bloqueo de almacenamiento Win32, un segmento preparado
parcial, raíz truncada, cursor obsoleto y conservación de REST/deuda más ABSENCE
abierta a través de consolidación y recuperación.

## 4. Consultas y migración

`f04_history_page` devuelve páginas de hechos originales por ID y generación.
`f04_history_relations` devuelve sus relaciones originales. Un error de integridad
se comunica como F04_SAVE, nunca como historial vacío. No se reactivan actividades
ni se crean Actors históricos. Una generación incorrecta devuelve F04_STALE.

La migración es explícita: cargar el guardado anterior, validar y producir un
**directorio nuevo**. El original no se modifica. Se verifica igualdad de bytes
activos, identidad, reloj/RNG y continuación en un proceso nuevo para las cinco
clases. Los lectores anteriores rechazan el nuevo contenedor claramente.

Tras optar por segmentos, `f04_save`/`f04_load` y las antiguas consultas de historial completo
DUTY/gaps/functions devuelven F04_SAVE para impedir exportaciones incompletas.
Se usan las nuevas APIs de persistencia y consulta. El comportamiento monolítico
anterior permanece intacto. La cobertura previa a la frontera no se infiere de
registros ausentes. La exportación activa es solo un diagnóstico explícito.
Las interfaces de personas, puestos, especialistas y residentes siguen disponibles.

## 5. Campañas reales y auditoría de hechos

Cada campaña genera guardias reales en bloques de siete días, procesa fronteras
de autoridad y combina ausencias, descansos, cancelaciones y suplencias. La
planificación siguiente debe coincidir con un proceso de referencia que conserva
todo el historial original. El proceso consolidado utiliza siempre la biblioteca
productiva con el presupuesto fijo. Un rechazo por capacidad es un fallo.

Se comparan todos los nuevos hechos, IDs, estados RNG/reloj y asignaciones de
cada bloque. Se verifica en cada bloque el grafo estático de personas, puestos,
competencias, grupos y censo. Un proceso nuevo abre la última generación y debe
producir exactamente el mismo futuro. Después, otro auditor reconstruye **todos**
los bloques desde segmentos más checkpoint y compara sus bytes canónicos contra
los hashes originales de referencia. No se limita a consultar una muestra.

| Clase | Días completos | Máximo residente | IDs finales | Hechos archivados finales | Pico working set del proceso |
| --- | ---: | ---: | ---: | ---: | ---: |
| Miranda | 365 | 1.926 | 41.438 | 40.309 | 12.091.392 B |
| Intrepid | 365 | 2.234 | 47.877 | 46.556 | 13.012.992 B |
| Sovereign | 365 | 8.492 | 179.181 | 174.137 | 30.961.664 B |
| Odyssey | 365 | 18.348 | 385.384 | 374.435 | 56.401.920 B |
| Valhalla | 365 | 21.218 | 437.731 | 424.908 | 64.196.608 B |
| Valhalla | 730 | 21.218 | 870.964 | 858.295 | 65.495.040 B |

Los seis recorridos verifican 1.948.872 hechos posteriores al bootstrap; 866.849 pertenecen al recorrido de 730 días.
El máximo residente incluye el estado previo a consolidar; el pico de memoria
incluye el ejecutable, copias transaccionales y buffers del laboratorio. El
historial total en disco crece y conserva checkpoints anteriores. No se promete
espacio histórico constante ni latencias independientes de la duración: publicar
y recuperar validan los segmentos del conjunto. Métricas por bloque, tamaños,
consultas, recuperación e inventarios SHA-256 están en las evidencias.

La DLL de referencia es un objetivo exclusivo de pruebas y no se distribuye a
Unreal. Solo ella omite el presupuesto residente para retener toda la historia.
Las cinco comparaciones de 365 días usaron el cálculo histórico original íntegro.
Para 730 días, una opción de prueba conserva todos los originales y recalcula la
carga completa, pero excluye de la ventana temporal de cálculo los intervalos
terminados al menos siete días antes. No pueden afectar una ventana futura ni
sus descansos. El validador sigue comprobando todo el historial original. La
identidad de hashes original/optimizado se verificó también en Miranda 365 días.
La referencia optimizada difiere las comprobaciones globales de tipos/referencias a validaciones completas al final de ambos horizontes; el validador histórico de guardias sigue comprobándose en cada plan. El producto valida cada transacción completa como antes. Esta optimización no se compila en el comportamiento productivo.

## 6. Validación y entrega

- Core completo + Content JSON: **479 PASS**, cuatro omisiones de plataforma,
  cero fallos, 483 entradas. CI del mismo SHA: Windows, Linux y sanitizadores,
  seis jobs satisfactorios.
- F04 con Core propuesto: **271/271** (270 anteriores más fallos históricos).
- F02/F03 contra el Core propuesto: **15/15 y 25/25**. Se usaron copias de laboratorio
  con solo las comprobaciones literales del SHA ajustadas; sus pins estables y
  fuentes del repositorio permanecen intactos.
- Compatibilidad monolítica de DLL anterior y migración histórica no destructiva:
  cinco clases, mismo futuro, incluidos procesos nuevos.
- Unreal **5.8.2**, changelist 56702186, Win64 **NullRHI: 26/26**, cero warnings de test.
  Incluye recuperación, consulta paginada y futuro determinista sin Actors históricos.
- Documentales F02/F03/F04, LORE-03 A, autoridad y gobierno del roadmap: PASS.

[Contratos y reproducción](../../../../../../desarrollo/integration/f04/HISTORY.md).
[Evidencia de aceptación](evidence/F04-PERSISTENCIA-03-HISTORY/acceptance.json).
[Resultados y métricas](evidence/F04-PERSISTENCIA-03-HISTORY/RESULTADOS.md).
[Inventario de fuentes](evidence/F04-PERSISTENCIA-03-HISTORY/source-files.json).
[Hashes de evidencias](evidence/F04-PERSISTENCIA-03-HISTORY/evidence-sha256.json).
[CI Core del SHA propuesto](https://github.com/robdor80/CoreRPG/actions/runs/41195928200).

**Aceptación completa de PERSISTENCIA-03 demostrada.** Ambas PR permanecen Draft para auditoría independiente. No se fusionan, no se actualiza el pin estable y no se inicia INTEGRACION-04 ni CIERRE-05.

Los oráculos completos se generaron con Core `63d2401`. La validación final vuelve a ejecutar las seis campañas consolidadas sobre `89a0e4f` contra esos fixtures de hashes congelados: ningún estado de campaña se carga desde ellos. Cada aceptación registra la revisión ejecutada y el SHA-256 de la referencia. La CI puede regenerar los oráculos omitiendo la opción de fixtures.
