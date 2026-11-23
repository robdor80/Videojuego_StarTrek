# Sutherland Bridge — estado recuperado para continuidad

21 de octubre de 2026. Documento de conservación, no nueva entrega de implementación. Sutherland no se modifica durante el trabajo Voyager ni durante este traspaso. Leer [entorno compartido](UE5_ENTORNO_COMPARTIDO.md).

## Qué está acreditado y de dónde procede

El estado técnico más reciente encontrado es **F07-COLL-01, entrega del 19/10/2026**: laboratorio implementado y probado técnicamente, detenido para revisión humana. No significa puente final aprobado, materiales definitivos ni integración en producción.

Se releen informes y documentos de continuidad locales de F07-P03F/G, F07-CHAIR-01 y F07-COLL-01. No se abre Unreal ni Blender y no se repiten sus suites en esta parada. Los recuentos siguientes son resultados históricos documentados. Las respuestas recientes recuperadas del chat «Sutherland» incluyen referencias de contenido que la herramienta no resuelve; por eso se priorizan los informes locales verificables.

## Proyecto principal y laboratorios

El principal identificado en los informes es `C:\Users\andro\Documents\StarTrek_3D\f07sutherland\f07sutherland.uproject`, con mapa histórico `/Game/maps/L_F07_Sutherland_Test`.

Existe también `C:\Users\andro\Documents\StarTrek_3D\F07_sutherland\F07_sutherland.uproject`. No se debe confundir con el anterior. No se determina aquí que esa segunda carpeta sea el principal autorizado.

| Entrega | Archivo y mapa de revisión |
|---|---|
| Puertas P03F/G | `C:\Users\andro\Documents\StarTrek_3D\F07_P03FG_DoorLab\Prototype\F07P02.uproject`; `/Game/F07P03FG/Maps/L_P03FG_FourDoors_BridgeReview` |
| Celda técnica D01 | Mismo proyecto; `/Game/F07P03FG/Maps/L_P03FG_D01_FinalRig` |
| Sillas CHAIR-01 | `C:\Users\andro\Documents\StarTrek_3D\F07_Chair_AutoLab\Prototype\Sutherland_ChairLab.uproject`; `/Game/ChairAutoLab/L_Sutherland_SixChairs_Test` |
| Colisiones COLL-01 | `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab\Prototype\F07P02.uproject`; `/Game/F07COLL01/Maps/L_F07_Sutherland_CollisionReview` |

Blender de puertas: `C:\Users\andro\Documents\StarTrek_3D\F07_P03FG_DoorLab\Blender\Sutherland_FourDoors_Finished_P03FG.blend`.

Blender de seis sillas: `C:\Users\andro\Documents\StarTrek_3D\F07_Chair_AutoLab\Blender\Sutherland_Six_SlidingChairs.blend`.

Blender de colisiones: `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab\Blender\Sutherland_Independent_CollisionReview.blend`.

El laboratorio humano anterior `C:\Users\andro\Documents\StarTrek_3D\Sutherland_ChairLab` es una referencia distinta de `F07_Chair_AutoLab\Prototype`. No guardar resultados nuevos sobre el primero por confundir nombres.

## Trabajo terminado y comprobado en los informes históricos

### Puertas F07-P03F/G

Cuatro puertas, ocho hojas reales, alojamientos huecos sólidos, guías, retornos y marcos; un BP compartido `/Game/F07P03FG/Blueprints/BP_ST_AutomaticDoor_Sutherland`. D04 comunica con cabina construida. D01–D03 no tienen destino construido y conservan permisos denegados y barreras físicas. No habilitarlas para demostrar visualmente una salida.

| Puerta | Carrera por hoja | Estado funcional del laboratorio |
|---|---:|---|
| D01 | 86,81980 cm | Bloqueada en puente; habilitada solo en celda técnica existente |
| D02 | 86,75941 cm | Bloqueada sin destino |
| D03 | 86,87153 cm | Bloqueada sin destino |
| D04 | 86,75933 cm | Paso a cabina; pendiente revisión humana |

Ejes locales: X normal al vano, Y deslizamiento, Z vertical. Left se mueve −Y, Right +Y. Animación Blender 1 cerrado / 49 abierto / 97 retorno. Pivotes, orientaciones y cotas son particulares de cada puerta.

Intención y seguridad documentadas: horizonte 1,2 s; anticipación lenta 120 cm; umbral de movimiento 15 cm/s; gracia 0,22 s; sensor normal 220 cm; retardo 1,5 s; movimiento 0,7 s. La ocupación tiene prioridad sobre cierre. D01 margen 5 cm; D04 `PathClearance=18 cm`. No extrapolar los valores a Voyager.

Resultados documentados: 50/50 comprobaciones Unreal por recarga, 242 movimientos barridos por hoja y 576/576 rayos de ocultación por puerta; D01 Play 29/29 más 6/6 heredadas; caminata/concurrencia 22/22. Recast transitorio con D04 abierta devuelve ruta completa de 3,40 m para agente radio 35 / alto 180 cm. Las recargas no se suman como casos nuevos. No hay navegación dinámica con puertas cerradas, SmartLinks, CoreRPG o NPC.

Incidencias ya resueltas que no se deben reintroducir: D04 usó dos assets nuevos `SM_D04_Left_ExactSlices1`/Right tras discrepancia Chaos frente a geometría real; el volumen Recast se colocó **después** de crear el brush porque CubeBuilder reiniciaba su posición. El jamb de P004 sigue bloqueando el carril Y=−35 cm; se validan centros dentro de ±28,7593 cm y no todo un rectángulo supuesto de vano.

### Sillas F07-CHAIR-01

Seis sillas, 15 piezas móviles por silla y una plataforma fija, carrera aprobada de 30 cm hacia sus consolas y retorno; Chair01–03 avanzan +X, Chair04–06 −X, con giro Z de 180°. Ensayos individuales y simultáneos, rechazo de órdenes opuestas, obstáculo de control y base fija. No se ha demostrado aquí sentarse ni transportar un ocupante.

Resultados históricos: 59/59 antes y después de recarga; 96/96 mallas importadas con geometría y UV verificadas; 30 poses geométricas sin contactos externos en el contexto ensayado. Se conserva un contacto interno mástil/plataforma ya existente, excluido únicamente como interfaz mecánica del mismo actor. No se desactivó la colisión externa general.

En Unreal se corrigió una rotación aplicada al eje erróneo usando argumentos de eje explícitos. Se eliminaron duplicados del fixture mediante un mundo vacío; la escena humana protegida no fue modificada. No repetir versiones rechazadas. Existe desplazamiento global histórico de plataforma humana (−1,95701,+1,67894,0) cm frente al Blender aprobado; revisar apariencia humana antes de promover.

### Colisiones F07-COLL-01

330 piezas fijas independientes, seis consolas laterales agrupadas, todos los canales UV verificados en Unreal y geometría conservada. Configuración final: 623 cajas + 502 convexos = 1125 formas simples, más seis raíles con caja = 1131 formas fijas nuevas. No `ComplexAsSimple` en las 330 piezas fijas nuevas; partes móviles conservan su colisión aprobada.

Los dos arcos superiores son extrusiones exactas de 24,320062 cm. La aproximación Auto Convex que producía falsos bloqueos se descartó y sustituyó por diez convexos completos por arco, UCX estándar, sin modificar el vano visible ni reducir la cápsula. Cero falsos bloqueos en las 30 secciones comparativas finales. La receta final de Unreal y `import_incremental.json` tienen autoridad sobre las primitivas de fabricación iniciales Blender/FBX.

Resultados finales documentados: puertas 50/50, sillas 59/59, CharacterMovement/intención 22/22; circulación diez aserciones y seis observaciones separadas; soporte 13/13; subida real por **ruta curva en ambos lados 2/2**, cápsula de 70 × 180 cm, sin teletransporte durante el recorrido. Caminar 9,9 m arriba mediante colocación inicial no demuestra por sí solo subir: la subida se acredita en la prueba curva posterior.

342/345 sondas lineales localizaron bloqueo. Las tres diferencias puntuales tienen bloqueo dirigido de cápsula confirmado en ambos sentidos. No llamar a ello coincidencia exacta de todas las superficies. Las rutas rectas superiores siguen chocando con arquitectura visible; no se autoriza desactivar colisiones para hacerlas pasar.

## Terminado pero pendiente de validación humana

- Revisión visual de las cuatro puertas, proporciones, encuentro con mamparos, comportamiento con teclado/mando y sensación de anticipación.
- Comodidad de los accesos superiores y de las rutas curvas efectivamente ensayadas.
- Aproximación a las seis sillas, posición de las plataformas, espacio de piernas y posibilidad real de sentarse, trabajar y levantarse.
- Huecos medidos entre impactos a Z=75 cm: aproximadamente 93–94 cm en una posición y 63–64 cm con silla adelantada, según estación. Son secciones concretas, no anchuras globales ni pruebas de postura; la cápsula de pie de diámetro 70 cm se detiene en algunas aproximaciones entre silla y consola.
- Aprobación humana del conjunto técnico y cualquier cambio de carrera o redistribución. No hay constancia aquí de que esa aprobación ya se haya dado.

## Iniciado o previsto, sin cierre demostrado

Se ha hablado de integrar la versión visual con PBR del usuario y los sistemas de puertas/sillas en un laboratorio independiente más agradable visualmente. El chat recuperado propone F07-INTEGRATION-01, pero **una propuesta no acredita implementación**. No se encontró una entrega con ese nombre en las carpetas consultadas.

COLL-01 sí reúne puertas/sillas/colisiones técnicas en un laboratorio, pero su informe dice expresamente que no aplica el PBR del usuario. No confundirlo con integración artística definitiva. `Sutherland_PBR_Lab` existe y contiene recursos de materiales; no se ha identificado o abierto en esta parada el `.blend` maestro exacto con los últimos acabados del usuario. Los cambios externos históricos de PBR/CoreRPG no se revierten ni se atribuyen al trabajo de Voyager.

## Trabajo todavía no demostrado o no iniciado en estas entregas

Integración en el principal; acabado PBR definitivo combinado; animación/postura de sentado y ocupante transportado; NPC/IA; enlace CoreRPG; navegación dinámica de puertas; empaquetado de juego y perfilado final. La autorización de laboratorio Voyager no permite iniciar ninguno de estos trabajos sobre Sutherland.

## Documentos autoritativos para recuperar Sutherland

| Referencia | Ruta |
|---|---|
| Último cierre y continuidad | `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab\Reports\CONTINUAR_F07_COLL_01.md` |
| Informe COLL-01 | `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab\Reports\INFORME_FINAL_F07_COLL_01.md` |
| Guía humana COLL-01 | `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab\Reports\GUIA_REVISION_HUMANA.md` |
| Manifiesto final COLL-01 | `C:\Users\andro\Documents\StarTrek_3D\F07_COLL_01_Lab\Backups\final_delivery_manifest.json` |
| Geometría arcos final | `Reports\exact_arch_inputs.json`, `Reports\exact_arch_validation.json`, `Reports\upper_curved_walk.json`, dentro de COLL-01 |
| Informe de puertas | `C:\Users\andro\Documents\StarTrek_3D\F07_P03FG_DoorLab\Reports\INFORME_FINAL_F07_P03G.md` y `INFORME_FINAL_F07_P03F.md` |
| Guía humana de puertas | `C:\Users\andro\Documents\StarTrek_3D\F07_P03FG_DoorLab\GUIA_PRUEBAS_HUMANAS.md` |
| Informe de sillas | `C:\Users\andro\Documents\StarTrek_3D\F07_Chair_AutoLab\Reports\INFORME_FINAL_F07_CHAIR_01.md` |
| Guía humana de sillas | `C:\Users\andro\Documents\StarTrek_3D\F07_Chair_AutoLab\Reports\GUIA_PRUEBA_UNREAL.md` |
| Auditoría antigua del principal | `C:\Users\andro\Documents\StarTrek_3D\f07sutherland\Saved\F07_Sutherland_Audit\Codex_Full_Bridge` |

Los pendientes antiguos del principal sobre falta de puertas separadas o ausencia de Blueprints describen aquel estado del principal; las entregas posteriores los resolvieron **en laboratorios**, no en producción. No tratarlos como fallos de P03FG ni borrar su historia.

No ejecutar `00_isolate.py`, `02_scaffold.py` ni la aproximación descartada `21_refine_arch_collision.py` de COLL-01. `22_exact_arch_inputs.py` protege contra repetición; no borrar su informe para forzarla. Antes de una fase futura, leer la continuidad, comprobar manifiestos y revisar las observaciones humanas. La siguiente actuación propia de Sutherland sigue siendo revisión humana, cuando el usuario la solicite.
