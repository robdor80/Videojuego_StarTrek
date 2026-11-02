# Enterprise-G â€” V07: estado tÃ©cnico parcial

**2 de noviembre de 2026. V07 NO COMPLETADA. No se acredita cobertura del 100 %.**

La entrega implementa cuatro mecanismos sobre hojas originales identificadas. El nÃºmero total de puertas reales sigue sin cerrarse: quedan seis accesos seÃ±alizados de memoria y la atribuciÃ³n de hojas en los huecos junto a las escaleras. Automatizar paneles sin resolver esa correspondencia podrÃ­a convertir mamparos o revestimientos en puertas. No se ha hecho esa intervenciÃ³n ni se han inventado hojas originales ausentes.

## Estado de cobertura

| Indicador | Resultado |
| --- | --- |
| Total real de puertas de la arquitectura | **No determinado; inventario abierto** |
| Puertas con hojas originales identificadas | 4 |
| Mecanismos implementados | 4 |
| Puertas validadas en el alcance identificado | 4 |
| Puertas bloqueadas por destino no construido | D02, D03 y D04 |
| Accesos seÃ±alizados de memoria pendientes | 6 |
| Marcos de escalera revisados sin atribuciÃ³n completa de hojas | 12 colocaciones de `Component#10` |

Estos contadores no significan Â«4 de 4 puertas totalesÂ». El [inventario legible por mÃ¡quina](../../integration/valhalla_supercomputadora/unreal/Scripts/v07_door_inventory.json) declara `total_real_doors: null`, `inventory_exhaustive: false` y los campos desconocidos de las candidatas como tales. No se han omitido del informe por estar incompletos.

## Puertas implementadas

Coordenadas UE en centÃ­metros; yaw alrededor de Z. Todas tienen dos hojas.

| ID | PosiciÃ³n X / Y / Z | Yaw | ConexiÃ³n y estado final | Componentes originales |
| --- | --- | ---: | --- | --- |
| D01 | 3121.58 / 248.13 / 37.00 | 0Â° | vestibulo principal / corredor exterior construido; automatica habilitada | Component#130 / Component_435035; Component#131 / Component_435936 |
| D02 | 1545.50 / 249.28 / 37.00 | 0Â° | vestibulo occidental / destino no construido; mecanismo preparado; bloqueo de seguridad conservado | #118 / Component_437343 |
| D03 | 5219.76 / 121.66 / 37.00 | 90Â° | corredor este, lateral Y menor / destino no construido; mecanismo preparado; bloqueo de seguridad conservado | #58 / Component_381616 |
| D04 | 5219.76 / 374.28 / 37.00 | 90Â° | corredor este, lateral Y mayor / destino no construido; mecanismo preparado; bloqueo de seguridad conservado | #58 / Component_381616.001 |

D01 conserva el mecanismo y las dimensiones V06. D02 procede de las hojas integradas en `Component#118`; su marco queda en una malla privada separada. D03/D04 proceden de las dos colocaciones de `Component#58` de la sala completa; se conservan sus marcos `#51`. No se confunden nombres iguales de componentes pertenecientes a fuentes diferentes.

| ID | Anchura / altura | Desplazamiento lateral por hoja | RetracciÃ³n normal | Margen de colisiÃ³n privado |
| --- | --- | --- | --- | --- |
| D01 | 181.92 / 203.54 cm | 90.76 cm | original V06 | 0,2 cm de suelo heredado V06 |
| D02 | 86.40 / 186.64 cm | 47.20 cm | -20 cm local X | 1 cm |
| D03 | 184.00 / 203.54 cm | 96.00 cm | -20 cm local X | 3.2 cm |
| D04 | 184.00 / 203.54 cm | 96.00 cm | 20 cm local X | 3.2 cm |

D02â€“D04 separan las hojas del marco y despuÃ©s deslizan; el cierre recorre los mismos segmentos en orden inverso. Cada segmento usa barrido de colisiÃ³n. La cÃ¡psula de Quinn mantiene 35 cm de radio y 90 cm de semialtura. No se desactivan colisiones ni se ignoran marcos para forzar el movimiento.

La mediciÃ³n del hueco de las puertas naranjas da aproximadamente 178,5 cm, frente a 184 cm de sus hojas visibles. La colisiÃ³n se retrae 3,2 cm dentro de cada hoja en Y/Z para retirar regiones ocultas por el marco. En D02 el margen es 1 cm. Solo cambian los convexos de recursos privados V07; las firmas de sus superficies antes/despuÃ©s del ajuste son iguales. Se conservan todas las caras, UV, normales y materiales al separar las hojas. La moldura que cruzaba la junta de `#58` se divide interpolando atributos; la diferencia de Ã¡rea superficial de la particiÃ³n es inferior a 0,000001 cmÂ².

En el mapa principal las tres puertas nuevas quedan con destino no construido y bloqueo de seguridad. TambiÃ©n deniegan la emergencia hacia ese destino. Para habilitarlas en otra fase es necesario construir y validar primero la continuidad; despuÃ©s se podrÃ¡ establecer `DestinationConstructed=true` y `SecurityLocked=false`. Los siete cierres V06 y sus siete remates permanecen intactos. No se reparan suelos ni se aÃ±aden cubiertas.

## Inventario y dificultad pendiente

Se leen de nuevo los Blender y SketchUp originales de la sala y del semicÃ­rculo, sus jerarquÃ­as y la V04E. Resultados: sala original, 1.407 objetos Blender, 920 colocaciones de malla y 1.086 nodos SKP; semicÃ­rculo original, 4.139 objetos, 3.855 colocaciones y 4.179 nodos SKP. La V04E examinada contiene 16.840 objetos y 16.304 colocaciones evaluadas de malla. En V06 estas corresponden a 16.302 colocaciones estÃ¡ticas mÃ¡s las dos hojas de D01.

La revisiÃ³n incluye alzados, secciones a altura de paso, partes conexas con soldadura espacial, colecciones sustituidas `V04E_APOYO_*`, componentes anidados y vistas con Quinn en Unreal. Los 169 componentes geomÃ©tricos del filtro de piezas delgadas son candidatas de diagnÃ³stico, no 169 puertas. No se ha cerrado el inventario por el mero resultado de un filtro.

Se localizan seis rÃ³tulos `DECK 00 DOOR 00` y controles en los recintos de memoria. La posiciÃ³n siguiente identifica el **rÃ³tulo**, no un umbral demostrado.

| Candidata | Instancia del rÃ³tulo | PosiciÃ³n UE del rÃ³tulo, cm | Estado |
| --- | --- | --- | --- |
| MEM_C01 | `DECK 00 DOOR 00.001` | 3226.2 / -773.6 / 152.1 | Hojas, orientaciÃ³n y mecanismo sin atribuir; sin automatizar ni validar |
| MEM_C02 | `DECK 00 DOOR 00.002` | 1122.7 / -1631.4 / 152.1 | Hojas, orientaciÃ³n y mecanismo sin atribuir; sin automatizar ni validar |
| MEM_C03 | `DECK 00 DOOR 00.003` | 3414.3 / -1631.4 / 152.1 | Hojas, orientaciÃ³n y mecanismo sin atribuir; sin automatizar ni validar |
| MEM_C04 | `DECK 00 DOOR 00.004` | 3226.2 / 1268.4 / 152.1 | Hojas, orientaciÃ³n y mecanismo sin atribuir; sin automatizar ni validar |
| MEM_C05 | `DECK 00 DOOR 00.005` | 1122.7 / 2126.1 / 152.1 | Hojas, orientaciÃ³n y mecanismo sin atribuir; sin automatizar ni validar |
| MEM_C06 | `DECK 00 DOOR 00.006` | 3414.3 / 2126.1 / 152.1 | Hojas, orientaciÃ³n y mecanismo sin atribuir; sin automatizar ni validar |

Las superficies vecinas de `#197/#198/#200/#202` incluyen revestimientos, marcos y paneles. Su proximidad a un control no demuestra quÃ© superficie debe moverse. Los mÃ³dulos acristalados `#206` y las ocho variantes P01â€“P08 de los bancos tampoco se convierten en hojas de paso por su apariencia. Los marcos `#10` junto a escaleras siguen documentados sin atribuirles hojas ficticias; los lÃ­mites B05â€“B07 continÃºan protegiendo sus destinos.

**Impedimento para cerrar V07:** resolver y contrastar la relaciÃ³n entre cada acceso/umbral y sus hojas mÃ³viles dentro de esa geometrÃ­a integrada, distinguir los huecos sin hojas y cerrar todas las candidatas. DespuÃ©s deberÃ¡n implementarse los mecanismos restantes y repetirse los recorridos con Quinn. Las inspecciones exteriores de diagnÃ³stico detectan falta de suelo; no se usan como pruebas aprobadas ni se abren accesos al vacÃ­o. No es correcto publicar que todas las puertas estÃ¡n automatizadas.

## ValidaciÃ³n ejecutada

| Grupo | Resultado | Alcance |
| --- | --- | --- |
| Mapa principal | 49/49 | 43 casos V06 mÃ¡s seis bloqueos/seguridad D02â€“D04; Quinn real |
| D02 y D03 en recinto con marcos | 18/18 | AproximaciÃ³n bilateral, paso, ocupaciÃ³n, emergencia, cierre y doce ciclos completos por puerta |
| D04 con retracciÃ³n exterior definitiva | 9/9 | Repetida con RHI real; doce ciclos completos observados |
| ComprobaciÃ³n fÃ­sica en toda la sala | 88/88 | 22 consultas/barridos por puerta; sonda de editor separada del juego |
| Copia reconstruida, recorridos de reproducciÃ³n | 10/10 | D01, entrada, ratÃ³n y las tres salidas bloqueadas |
| Recinto auxiliar permanente, RHI real | 13/13 | Cierres, vistas abiertas/cerradas y cuatro lÃ­mites fÃ­sicos |
| Vistas del mapa principal, RHI real | 3/3 | Bloqueo visible D02â€“D04 |
| Identificador de puerta inexistente | Rechazado como se esperaba | El caso registra `passed=false`; no se cuenta como fallo del mecanismo |

Las sondas de juego poseen a Quinn oficial con Enhanced Input, CharacterMovement, gravedad y colisiones; solo teletransportan al inicio de cada caso. Cada puerta acredita doce transiciones completas de abierta a cerrada. No se acepta Ãºnicamente haber alcanzado los puntos del recorrido. Se revisan las capturas de apertura/cierre y de las salidas bloqueadas. La iluminaciÃ³n continÃºa siendo tÃ©cnica, con sobreexposiciÃ³n visible; no supone aprobaciÃ³n artÃ­stica ni de comodidad de cÃ¡mara.

La sonda heredada se corrige para seleccionar `door_id`, restaurar las polÃ­ticas autoradas y aplicar comandos Ãºnicamente a la puerta examinada. Se evita que una prueba de D01 desbloquee las demÃ¡s. La validaciÃ³n de geometrÃ­a en editor no sustituye los casos de juego con Quinn. NullRHI solo se usa en parte de las pruebas fÃ­sicas, nunca para justificar FPS o apariencia.

**Fallos finales en el alcance ejecutado: ninguno. ValidaciÃ³n integral solicitada: NO SUPERADA, porque el inventario sigue abierto y las candidatas no estÃ¡n implementadas/verificadas.**

## Rendimiento frente a V06

ComparaciÃ³n nueva y secuencial sobre copias aisladas, i9-14900HX y RTX 4070 Laptop, UE 5.8.2 Development, D3D12 real y 1920Ã—1080. Se conservan seis segundos de espera y ocho de medida por vista, porcentaje 100, VSync desactivado y sin lÃ­mite de FPS. FPS = 1.000 / intervalo medio; P95 se refiere al intervalo de fotograma.

| Vista | FPS V06 | FPS V07 | Cambio | P95 V07 | Draw calls V06 / V07 |
| --- | ---: | ---: | ---: | ---: | ---: |
| entrada | 185.1 | 186.4 | +0.7 % | 5.89 ms | 732 / 716 |
| circulo_01 | 165.3 | 165.7 | +0.2 % | 6.55 ms | 709 / 713 |
| circulo_02 | 164.7 | 165.0 | +0.2 % | 6.56 ms | 719 / 723 |
| pasillo_exterior | 200.0 | 199.1 | -0.4 % | 5.48 ms | 148 / 189 |
| escalera_sur | 186.4 | 186.3 | -0.1 % | 5.85 ms | 387 / 387 |
| escalera_inferior | 184.1 | 183.9 | -0.1 % | 5.88 ms | 241 / 243 |

Se registran 8.689 fotogramas V06 y 8.696 V07. VariaciÃ³n de FPS entre âˆ’0,4 % y +0,7 %; no se observa degradaciÃ³n importante en estas muestras. El hilo de juego V07 mide 1,21â€“1,35 ms y la memoria local GPU alcanza unos 931,8 MiB. El incremento de llamadas de dibujo en alguna vista refleja las hojas independientes; no se elimina geometrÃ­a para compensarlo. Esta mediciÃ³n cubre cuatro mecanismos y la iluminaciÃ³n provisional, no todas las puertas aÃºn desconocidas ni el acabado artÃ­stico o una distribuciÃ³n empaquetada.

## ConservaciÃ³n e independencia

- 1.573/1.573 archivos de fuentes, entregas y evidencia previa capturados al inicio permanecen idÃ©nticos en tamaÃ±o y SHA-256. No se borran laboratorios anteriores.
- Los 534 archivos de contenido heredados de la entrega V06 permanecen idÃ©nticos; los recursos V07 son privados y nuevos.
- La entrega contiene 592 archivos; su manifiesto registra tamaÃ±o y SHA-256. No contiene enlaces de sistema de archivos ni referencias textuales a las rutas temporales.
- Una copia nueva de la entrega, sin Saved, Intermediate ni cachÃ©s, se reabre con cachÃ© nueva y RHI real. `audit_v07.json` declara `ok=true`: 16.299 instancias estÃ¡ticas, cuatro puertas, catorce elementos de cierre V06 y cero errores/advertencias de Map Check.
- 452 paquetes `/Game/` en las dependencias de los dos mapas, ninguno ausente y ninguna dependencia de `/Game/VH07Test/`. Los recursos normales `/Engine/` y UE 5.8.2 siguen siendo necesarios.
- El diff permitido se limita a la integraciÃ³n Valhalla y este informe. No se ejecutan ni editan CoreRPG, Sutherland o los proyectos de control/hangar. La verificaciÃ³n de 1.573 firmas no se presenta como un inventario de todos los recursos locales de esos otros proyectos.

El mapa auxiliar es un resultado permanente aprobado dentro de la entrega V07, con suelo y lÃ­mites propios. Los mapas de diagnÃ³stico, registros, capturas, exportaciones y copias de trabajo no se incorporan a la entrega. El proyecto puede jugarse sin ellos. Algunas cachÃ©s compartidas y trazas nativas UBA/Zen del motor permanecen en el perfil/ProgramData por comportamiento de Unreal; no se usan para entregar el proyecto ni se limpian retrospectivamente.

## Incidencias y lÃ­mites conservados

Los intentos iniciales revelaron cuerpos de colisiÃ³n aÃºn no listos en la misma autorÃ­a, interferencias de marcos durante apertura/cierre y un panel del corredor en la retracciÃ³n de D04. Se conservaron los registros fallidos y se repitieron las pruebas tras reabrir y con Quinn real. La colisiÃ³n ajustada y la direcciÃ³n exterior de D04 superan la repeticiÃ³n final. No se suman los primeros recorridos de doce puntos como doce ciclos: el contador nuevo verifica el cierre completo.

Un intento de duplicar/cargar el mapa en un mismo proceso terminÃ³ con una incidencia de recolecciÃ³n de mundos del editor. La receta definitiva guarda la copia y autoriza en dos procesos separados; la reconstrucciÃ³n y la Ãºltima reapertura terminan con cÃ³digo cero. Permanecen pendientes el inventario integral, mecanismos restantes, prueba personal, cÃ¡mara en pasos estrechos, PBR e iluminaciÃ³n artÃ­stica.

## Entrega y publicaciÃ³n

Proyecto local exacto:

`C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\PROYECTO VALHALLA\Salas construidas\Sala computadora Enterprise Valhalla\UE5_Supercomputadora_V07\ValhallaComputer.uproject`

Mapa principal: `/Game/ValhallaV07/Maps/L_Supercomputadora_V07`. Mapa auxiliar: `/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion`. [Instrucciones y reconstrucciÃ³n](../../integration/valhalla_supercomputadora/unreal/README_V07.md).

Rama: `codex/valhalla-v07-puertas`. Base verificada: `fd2d40785f1c06cd43763585d2a769721994474b`, rama V06 `codex/valhalla-supercomputadora`. La PR Draft V07 se revisa contra esa rama, sin volver a presentar V06 como trabajo nuevo. PR #79 y `main` se conservan intactas; no se fusiona ni se elimina ninguna rama. El SHA publicado se confirma en la PR y en el mensaje de entrega.

[PR #80 — V07 parcial, Draft y dependiente de V06](https://github.com/robdor80/Videojuego_StarTrek/pull/80). Implementación y pruebas: `2a4d38803312452b1d384bb3fbc563612210d156`.

Git publica cÃ³digo, planes, inventario e informe; los recursos UE, modelos, imÃ¡genes y binarios permanecen locales conforme a la polÃ­tica existente. **No se ejecuta el apagado del MSI:** la condiciÃ³n del encargo exige V07 integral terminada, validada y publicada, y no se ha alcanzado.

## Evidencia identificada

Los nombres y firmas siguientes identifican resultados locales; no son dependencias de ejecuciÃ³n ni se publican los datos brutos.

| Evidencia | SHA-256 |
| --- | --- |
| inventario de fuentes originales (`original_graphs.json`) | `410e140609079c0d8ba7379aeb7c105282571a88d6d761cc159e7679ae54bce0` |
| manifiesto geomÃ©trico V07 (`source_v07_delivery.json`) | `728af2c37bc6903f4157b536e93d9da04810bfde4241e9ec0947bb1ba6a116eb` |
| 49 casos del mapa (`final_map_report.json`) | `25a29739e73becea66214ced99c187b6165bcee8ebab0597873e7239ceccb06f` |
| D02/D03 y ciclos del recinto (`final_rig_report.json`) | `8c5429adb487f98ba774abe5d435ea8e201ae876e71731a4c264dfc5f225d798` |
| D04 definitivo y vistas (`delivery_rig_report.json`) | `f68af5109b71bf60142bb003f19d4f7dc063e85e4a95cca126b5b444e21e88a0` |
| 88 comprobaciones fÃ­sicas finales (`all_doors_physics_final.json`) | `7aefb7e13e30d0dbcb1856ebe314f37722d405aa9304821159de1d04a306f609` |
| recinto permanente (`portable_validation_report.json`) | `56883d6acb880a5f2dbf445e2c094a877ec6a948a15692480bcfcc0d5e2cc3c3` |
| comparaciÃ³n de rendimiento (`performance_comparison.json`) | `b97d54ba963e3008607cb204948f764830d7420f6b6b1142f48dd3b93aa97e79` |
| reapertura limpia final (`audit_v07.json`) | `333683a91bc7dcd5ac5a946aa243f3c76e0d03e48e6dfa133af15942aad70720` |
| manifiesto de entrega (`delivery_manifest.json`) | `74ddf7ff36bbd9cf0203ea280c1f88c7e5053f1de91c0212489086d374267169` |
| conservaciÃ³n de firmas (`protected_verification.json`) | `ab75f5d6e2cee1b9061fcbc9b6a20998e334c5b07129983be386e0834ff40d62` |
