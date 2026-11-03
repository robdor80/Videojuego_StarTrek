# USS Enterprise NCC-1701-D — V07, cierre práctico

**3 de noviembre de 2026. Proyecto Galaxia. Recomendación: B — V07 funcional, con limitaciones documentadas.**

Esta intervención conserva D01–D04 y resuelve los pendientes mediante la alternativa práctica autorizada: los seis puntos señalizados de memoria permanecen cerrados con la geometría estática original, y dos huecos bajo escaleras reciben cierres provisionales. Se reproduce y corrige una caída real de Quinn en el hueco sur. No se añaden suelos, salas ni mecanismos; no se inicia V08. La auditoría independiente y la autorización de cierre formal siguen pendientes.

## Estado recuperado y alcance

Repositorio local verificado: `robdor80/Videojuego_StarTrek`. Inicio limpio sobre `codex/valhalla-v07-puertas`, commit `a92f411c459759e84890b5e07a6a1c4e88458023`. La PR #80 estaba abierta en Draft, con esa misma cabecera y base V06 `fd2d40785f1c06cd43763585d2a769721994474b`, rama `codex/valhalla-supercomputadora`. No había cambios locales posteriores que proteger. No se cambió de rama ni se actuó sobre otros worktrees.

Se reutilizaron el informe, las evidencias, los planes y el proyecto existentes. La inspección nueva se limita a las seis candidatas de memoria y a las bocas de escalera; las pruebas posteriores son de regresión y del defecto corregido. Las mediciones históricas V06/V07 no se presentan como pruebas nuevas.

## Inventario final práctico

El [inventario de máquina](../../integration/valhalla_supercomputadora/unreal/Scripts/v07_door_inventory.json) delimita **22 puntos de control de la sala**, no 22 puertas físicas ni un inventario de toda la nave.

| Grupo | Puntos | Paso habilitado | Cerrados intencionadamente |
| --- | ---: | ---: | ---: |
| D01–D04, mecanismos existentes | 4 | 1, automático D01 | 3, D02–D04 |
| MEM_C01–MEM_C06, candidatas señalizadas | 6 | 0 | 6, geometría estática original |
| Bocas de escalera | 8 | 3, sin hojas | 5, B05–B09 |
| Extremos de corredor | 4 | 0 | 4, B01–B04 |
| **Total** | **22** | **4: una automática y tres abiertas** | **18** |

Hay **cuatro mecanismos automáticos funcionales**: uno habilitado en el mapa principal y tres bloqueados por destinos sin construir. No se ha demostrado ni se necesita resolver ahora el número artístico de posibles hojas integradas en otros paños; `total_real_doors` permanece desconocido y la exhaustividad del inventario se limita expresamente a estos puntos de control. Cero accesos quedan sin una decisión práctica. Esto sustituye el criterio anterior de automatización total.

### Puertas D01–D04 conservadas

| ID | Posición UE X / Y / Z, cm | Estado en la sala |
| --- | --- | --- |
| D01 | 3121,58 / 248,13 / 37,00 | Automática habilitada, mecanismo V06 sin cambios |
| D02 | 1545,50 / 249,28 / 37,00 | Seguridad activa, destino no construido |
| D03 | 5219,76 / 121,66 / 37,00 | Seguridad activa, destino no construido |
| D04 | 5219,76 / 374,28 / 37,00 | Seguridad activa, destino no construido |

Se conservan `AVHAutomaticDoor`, retracción, deslizamiento, barridos, ocupación, reapertura y políticas de emergencia. No se editan código nativo, hojas, convexos ni materiales. D02 mantiene el margen de colisión privado de 1 cm; D03/D04, 3,2 cm. El mapa auxiliar permanente permite verificar D02–D04 con Quinn sin habilitar salidas al vacío.

### Seis candidatas de memoria: opción D

Los rótulos `DECK 00 DOOR 00.001` a `.006` están asociados a controles exteriores de servicio (`Component#190/#191/#192`). Su posición no constituye un umbral. La inspección focalizada confirma la separación respecto al paño perimetral `Component#197` y a los apoyos V04E; no identifica una pareja independiente de hojas reutilizable mediante una adaptación sencilla. No se recorta la arquitectura ni se mueven los bancos para crear una puerta.

| ID | Posición del rótulo X / Y / Z, cm | Colisión que detiene la aproximación interior |
| --- | --- | --- |
| MEM_C01 | 3226,2 / -773,6 / 152,1 | `InstancedStaticMeshComponent_182`, instancia 24 |
| MEM_C02 | 1122,7 / -1631,4 / 152,1 | `InstancedStaticMeshComponent_191`, instancia 1322 |
| MEM_C03 | 3414,3 / -1631,4 / 152,1 | `InstancedStaticMeshComponent_184`, instancia 114 |
| MEM_C04 | 3226,2 / 1268,4 / 152,1 | `InstancedStaticMeshComponent_224`, instancia 24 |
| MEM_C05 | 1122,7 / 2126,1 / 152,1 | `InstancedStaticMeshComponent_233`, instancia 1322 |
| MEM_C06 | 3414,3 / 2126,1 / 152,1 | `InstancedStaticMeshComponent_226`, instancia 114 |

**Los seis conservan el cierre estático original y quedan fuera del recorrido habilitado.** No se necesitan para conectar las zonas interiores terminadas. Las colisiones registradas pertenecen al conjunto original de bancos/arquitectura; no se presentan como seis nuevas hojas de puerta. No se afirma que toda la superficie integrada carezca de intención artística de puerta.

Desde el interior, Quinn se detiene con suelo estable en los seis casos, también saltando. Los barridos independientes detectan bloqueo sin penetración inicial. Cuatro de los seis puntos exteriores muestreados carecen incluso de impacto inferior; los otros dos detectan alguna superficie, lo que no acredita continuidad ni una sala terminada. No se habilita ninguno de esos destinos. La atribución artística de hojas puede aplazarse hasta que exista una necesidad real de abrirlos.

### Escaleras: ocho bocas, tres entradas abiertas y cinco cierres

Las doce colocaciones de `Component#10` son mitades emparejadas en seis marcos. Se distinguen además las dos salidas superiores, a Z=379,635 cm. No se suman las mitades como doce puertas ni se les inventan hojas.

| ID | Boca, posición aproximada X / Y / Z, cm | Decisión |
| --- | --- | --- |
| S01 | Sur, entrada 3204 / -62,76 / 37 | Abierta a escalera construida |
| S02 | Sur, bajo tramo 3353 / -62,76 / 37 | **Nuevo B08** |
| S03 | Norte, subida 3204 / 557,48 / 37 | Abierta a escalera construida |
| S04 | Norte, bajada 3353 / 557,48 / 37 | Abierta a escalera construida |
| S05 | Norte, salida inferior 3204 / 557,48 / -305,635 | B07 conservado |
| S06 | Norte, bajo tramo 3353 / 557,48 / -305,635 | **Nuevo B09 preventivo** |
| S07 | Sur, salida superior 3353 / -66,44 / 379,635 | B05 conservado |
| S08 | Norte, salida superior 3353 / 561,16 / 379,635 | B06 conservado |

**Defecto reproducido:** en la copia inicial, partir de `[3353,10,37]` hacia `[3353,-200,37]` permite cruzar el marco bajo la escalera sur y caer. La sonda termina con `unsupported_drop`, pies en Z=-66,23 cm y sin suelo transitable. No era la entrada válida de la escalera, situada en X=3204.

**Corrección B08:** panel azul de 130 × 250 × 12 cm, en X=3353,18 / Y=-60, desde Z=37 hasta 287 cm, con remate claro y colisión `BlockAll`. Queda bajo el recorrido superior y cierra antes del borde de caída. La entrada contigua, los peldaños y el retorno por la escalera se conservan.

**B09:** panel de 130 × 226,815 × 12 cm en la boca bajo la rampa norte, X=3353,18 / Y=561,15857, desde Z=-305,635. Es un cierre preventivo hacia una cubierta inexistente. No se afirma una caída reproducida en B09 ni una travesía satisfactoria de Quinn por ese destino: el intento diagnóstico sigue la rampa existente y no alcanza el punto inferior solicitado. Su bloqueo se valida con cápsulas físicas desde ambos lados.

B08/B09 y sus dos remates son los únicos cuatro actores añadidos al mapa. Usan `Cube` del motor y materiales existentes M_061/M_099. Los siete cierres V06 y sus siete remates permanecen intactos.

## Validación nueva en UE 5.8.2

| Grupo | Resultado nuevo | Alcance |
| --- | --- | --- |
| Mapa principal | **49/49** | Plan V07 heredado sin alterar; recorridos, tres escaleras, D01, D02–D04 bloqueadas, teclado y ratón |
| Recinto auxiliar permanente | **27/27** | D02–D04, bilateralidad, paso, ocupación, reapertura, seguridad, emergencia y **12 ciclos completos por puerta** |
| Memoria y B08 | **18/18** | Seis aproximaciones de memoria, seis saltos y seis aproximaciones/saltos en B08 |
| Física de puertas | **88/88** | 22 comprobaciones por mecanismo, sala completa; políticas restauradas sin guardar cambios de prueba |
| Física B08/B09 | **12/12** | Cápsula 35/90 cm, tres posiciones válidas y ambos lados por cierre; sin penetración inicial |
| Reapertura RHI real | **Correcta** | Cero errores/advertencias, recursos de materiales válidos, cierres y dependencias presentes |

**Resultado final: 94/94 casos de ejecución y 100/100 comprobaciones físicas; ninguna regresión en el alcance probado.** El mapa registra 1.301 muestras y los casos nuevos 468, sin solape bloqueante de cámara en esas consultas. La distancia mínima observada de cámara en escaleras es de unos 34,97 cm: conserva la limitación de comodidad ya señalada en V06.

Las ejecuciones de juego poseen al Quinn oficial y usan Enhanced Input, CharacterMovement, gravedad y colisión reales. Se teletransporta únicamente al comienzo de cada caso. Se ha ejecutado el juego en este MSI con D3D12 y renderizado fuera de pantalla; no es solo una comprobación geométrica. **No se ha realizado una sesión manual personal con teclado y ratón por parte del usuario.**

La primera prueba nueva dio 17/18: tras un salto lateral, la consulta final apuntó a la jamba, aunque Quinn siguió ante B08 y con suelo estable. Se corrigió la condición de la prueba: exige contacto observado con B08 y que ninguna muestra de pies cruce Y=-25 ni baje de Z=36 cm, además del bloqueo y suelo final. La repetición completa da 18/18. No se modificó la geometría para forzar ese resultado. El primer muestreo físico de bordes empezaba dentro de marcos originales; se conservó como diagnóstico y se repitió con posiciones iniciales válidas. Los 88 casos de puertas habían pasado también en aquel intento.

Se revisaron las siete capturas nuevas de los seis cierres de memoria y B08: Quinn, bancos y materiales presentes; panel azul claramente visible, entrada válida contigua abierta. La iluminación mantiene la sobreexposición técnica previa. Las muestras de cámara no sustituyen la aceptación de encuadre o comodidad.

## Rendimiento localizado

Comparación secuencial de copias V07 antes/después de B08/B09, en el mismo MSI (i9-14900HX y RTX 4070 Laptop), D3D12 real, 1920 × 1080, seis segundos de espera y ocho de medida por vista, sin VSync ni límite de FPS. Se revisan únicamente entrada y las dos vistas de escaleras afectadas; no se repite la auditoría general V06.

| Vista | FPS antes | FPS después | Cambio | P95 después | Draw calls antes/después |
| --- | ---: | ---: | ---: | ---: | ---: |
| entrada | 188.5 | 186.8 | -0.9 % | 5.81 ms | 716 / 716 |
| escalera_sur | 188.3 | 186.7 | -0.8 % | 5.78 ms | 387 / 387 |
| escalera_inferior | 185.9 | 184.2 | -0.9 % | 5.85 ms | 243 / 243 |

Variación entre -0.9 % y -0.8 %. No se observa una degradación evidente en estas muestras. Un intento previo quedó limitado a 888 × 500; se conserva como diagnóstico y no se usa en esta comparación. Se repitió con ForceRes y r.SetRes, verificando 1920 × 1080 en cada resultado. Esta comprobación localizada no equivale a un benchmark de toda la nave ni del acabado artístico final.

## Conservación, independencia y entrega

La autoría compara puertas, colocaciones de arquitectura y cierres V06 antes y después: misma firma SHA-256 `2d1ad894eb94d188a954ba053f36fae1592ffbb39d5c8a4b7086676cbe84e5e5`. Se conservan 16.299 instancias estáticas, cuatro puertas y los catorce actores de límites V06; se añaden solo cuatro actores B08/B09. Map Check: cero errores y advertencias. La reapertura con RHI real verifica materiales y los 452 paquetes `/Game/` de ambos mapas: ninguno ausente ni procedente de `/Game/VH07Test/`.

Se comparan los 592 archivos iniciales de la entrega: **586 permanecen idénticos**. Los seis reemplazados son el mapa V07, descripción del proyecto, README y tres scripts/inventario; se añaden cuatro archivos de autoría, comprobación y planes. La entrega final contiene **596 archivos**. Bajo `Content` solo cambia el mapa; las mallas, hojas de puertas, materiales, texturas, contenido V06 y mapa auxiliar conservan sus hashes. El Blender V04E conserva SHA-256 `e55df3cf537365ac8e145b9a7cd96605f5b0edaa5537473a734f090f931a8670`. Se guarda copia de los archivos reemplazados y se comprueba la igualdad de la entrega integrada con los archivos validados. No hay cambios en código nativo ni recompilación requerida.

Proyecto actualizado, en la misma ruta histórica:

`C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\PROYECTO VALHALLA\Salas construidas\Sala computadora Enterprise Valhalla\UE5_Supercomputadora_V07\ValhallaComputer.uproject`

Mapa principal: `/Game/ValhallaV07/Maps/L_Supercomputadora_V07`.
Mapa auxiliar: `/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion`.
[Uso, reconstrucción y repetición de pruebas](../../integration/valhalla_supercomputadora/unreal/README_V07.md).

Las evidencias y copias de esta intervención quedan únicamente en `laboratorios/valhalla/v07_cierre_20261103/`. La entrega usa sus propios recursos y código; no contiene dependencias de ejecución hacia ese directorio. La carpeta completa es eliminable una vez que el usuario decida prescindir de las evidencias; **no se ha borrado ningún laboratorio ni archivo anterior**. La DDC se redirige al laboratorio tras la primera apertura. Unreal conserva algunas cachés y trazas nativas del perfil; no se usan para entregar el proyecto ni se limpian retrospectivamente.

## Publicación y limitaciones

Rama: `codex/valhalla-v07-puertas`. [PR #80](https://github.com/robdor80/Videojuego_StarTrek/pull/80), abierta en Draft, base V06. Git publica scripts, planes, inventario e informe; los recursos UE y binarios permanecen locales conforme a la política del repositorio. PR #79 y `main` no se modifican; no hay fusiones ni borrado de ramas.

**Necesario antes del cierre formal:** auditoría independiente y aceptación personal del recorrido/cámara, especialmente en escaleras. No se declara cerrada formalmente V07.

**Aplazable sin bloquear el recorrido terminado:** atribución y separación artística de las posibles hojas integradas de memoria, futuras salas exteriores y cubiertas, sustitución de cierres provisionales, PBR e iluminación artística. Los destinos incompletos deben seguir cerrados; abrirlos exigiría construir y validar su continuidad en otra intervención autorizada.

**B. V07 FUNCIONAL, CON LIMITACIONES DOCUMENTADAS.** No queda una reconstrucción de seis puertas exigida para este cierre práctico. No se inicia V08 ni se apaga el MSI.

## Evidencia de esta intervención

| Evidencia local | Archivo relativo a la carpeta de esta intervención | SHA-256 |
| --- | --- | --- |
| Diagnóstico inicial con caída sur | `focused_before_runtime.json` | `cd1f1661b157e9fcd26c2e6c175bb8e0a13fd24b39ae36c13daa7ea6634d33df` |
| Autoría y preservación | `author/author_v07_closure.json` | `3ffaa8ebf460770c6f20beeb499ab792957a9682b79319819f8265750d191113` |
| 18 casos nuevos definitivos | `closure_runtime_v2.json` | `5371ed17c40e1f76308721fafc48116425e0f463be7931a6ef8ff9d8811a380e` |
| 49 casos del mapa | `regression_map.json` | `f51bd7fefcc34df2049524741f4049dacac830d42f28396a10ee35a042e33960` |
| 27 casos del recinto | `regression_rig.json` | `266972299f69733c165d21c91062d7d4e3218c2277c24e8327b4205952e97fb5` |
| 88 + 12 comprobaciones físicas | `physics_after_v2.json` | `127b648281baf46c19b8724519c49c81e89f9bcb49a829a4f1e259e712def0d2` |
| Reapertura | `reopen/audit_v07.json` | `4450aad0ac460dcf9f3fd86493bbcc8d02e5e957ef8db77758c1dc20eff7f0b7` |
| Rendimiento localizado | `performance_comparison.json` | `a757e2fafe8393a57cc755e7a40b9a2f7a5abbec91d14f6d154fb84aa26f587a` |
| Preservación de archivos | `preservation.json` | `039c21d0a357bd3cc6b6c2dc641b96afa247860aba67840560f558c8451fecbb` |
| Integración | `integration.json` | `92746538bfe2a54353215c778a315c82d1cb8955deb4ebb2c7152cea1736647a` |
| Manifiesto de entrega | `delivery_manifest.json` | `e638a29077d4783181d537794c4dc7b3eaff58e7d45c9cec0d76a420e984ef24` |
