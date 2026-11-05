# Enterprise-D — V07 funcional para inspección con Quinn

**5 de noviembre de 2026.** Esta entrega sustituye el cierre estático de los seis accesos de memoria por puertas practicables. Continúa V07 sobre `fac51a0`, en la rama `codex/valhalla-v07-puertas` y la [PR Draft #80](https://github.com/robdor80/Videojuego_StarTrek/pull/80). No se inicia V08 ni se fusiona con main.

## Entrega local y alcance

Proyecto nuevo: `PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V07_Funcional/ValhallaComputer.uproject`.

Mapa inicial: `/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional`.

Blender nuevo: `PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/Sala_Supercomputadora_V07_Funcional.blend`.

El Blender incluye la geometría final de Unreal, materiales originales, dos imágenes empaquetadas y doce hojas animadas en 1/60/120. Es una copia de trabajo: Unreal conserva la implementación física y jugable. Los 596 archivos del V07 anterior y el Blender V04E original mantienen sus hashes. La entrega nueva contiene sus propios recursos; no necesita los directorios de pruebas para funcionar.

## Puertas, suelos y cubiertas

| Accesos | Resultado |
| --- | --- |
| MEM_C01, C02, C04, C05 | Puertas dobles automáticas hacia cuatro recintos de servicio cerrados, 180 cm de ancho y hasta 400 cm desde el paño original |
| MEM_C03, C06 | Puertas dobles automáticas y conexiones de 180 cm hacia el corredor exterior construido; recorrido curvo conservado |
| D01 | Automática habilitada, mecanismo y propiedades conservados |
| D02–D04 | Mecanismos conservados; siguen bloqueadas por destinos sin construir |

Las seis nuevas reutilizan `AVHAutomaticDoor`: retirada de 35 cm, deslizamiento de 100 cm, barrido, ocupación, reapertura y política de seguridad. Paso de 180 × 230 cm. Quinn cruza los seis en ambos sentidos; las hojas se mueven y vuelven a cerrar durante el juego. Los cuatro recintos cerrados reciben una luz técnica de 600 lm sin sombras, con radio de 400 cm.

Se añaden **30,7266 m² de suelo complementario** y **42,84 m² de techo** en los accesos, descontando cobertura existente. Se conservan los suelos restantes y las conexiones verticales. Dos cubiertas de escalera, de unos **19,982 m²** en conjunto, se sitúan a Z=610 cm con cerramientos superiores. No se tapan peldaños ni se habilitan salidas a cubiertas inexistentes.

B01–B09 permanecen. B08 conserva la protección de la caída sur; B09 conserva la protección preventiva inferior norte. Las tres escaleras y sus retornos pasan la regresión. La firma de propiedades de D01–D04 y límites originales coincide antes y después de la construcción.

Se sustituyen 665 colocaciones de detalle por sus restos recortados agrupados. Permanecen 15.634 instancias originales. Son 24 mallas nuevas, diez piezas de cubierta, seis actores de puerta y cuatro luces: **44 actores añadidos**, sin miles de objetos nuevos. Posiciones, materiales, UV y normales fuera de los volúmenes de paso se conservan; los activos fuente no se sobrescriben.

## Validación ejecutada

Windows local, Unreal 5.8.2 y Blender 5.2.2. Juego real con D3D12 fuera de pantalla, Quinn oficial poseído, Enhanced Input, CharacterMovement y gravedad. Cápsula de 35/90 cm. Sólo se teletransporta al inicio de cada caso.

| Prueba final | Resultado |
| --- | --- |
| Casos nuevos de memoria y regresión B08 | **54/54** en una ejecución completa |
| Plan heredado del mapa, sin cambiar | **49/49** en una ejecución completa |
| Mecanismos de las diez puertas | **220/220** comprobaciones físicas |
| B08/B09, ambas caras y tres posiciones | **12/12** barridos bloqueados, sin penetración inicial |
| Suelo y techo de los accesos | **108/108** posiciones, 216 consultas |
| Cubiertas en puntos de recorrido | **47/47** puntos |
| Pasos abiertos con cápsula | **6/6** barridos libres |
| Recorte, superficies y orientación | **4/4** pruebas de geometría |
| Reapertura de copia de la entrega | **475 paquetes**, ninguno ausente; Map Check **0 errores / 0 advertencias** |
| Inspección automatizada tras iluminar | **12/12** entradas/salidas con nuevas capturas |

Se observan **36 ciclos completos de cierre**, seis por acceso. El verificador adicional exige cruces de umbral, ocupación y posición segura ante puertas bloqueadas. Los 2.550 muestreos de los casos nuevos no detectan solapes bloqueantes de cámara; el brazo mínimo observado allí es de 94,90 cm. Esto no sustituye la valoración personal de cámara en escaleras. Se realizó además una prueba interactiva breve de teclado, salto y cámara mediante control de ventana por Codex. No sustituye la inspección manual exhaustiva del usuario. Se resolvió el aviso heredado de empate entre luces direccionales seleccionando explícitamente la misma luz de mayor intensidad.

La primera geometría invadía el corredor con C03/C06; la regresión lo detectó y se corrigió conectando esos dos pasos al corredor existente. La repetición crítica dio 8/8 y la regresión final completa 49/49. La primera suite nueva dio 45/54: seis casos colocaban a Quinn dentro de hojas cerradas al iniciar y tres exigían un impacto final nominal que podía estar ausente aunque la cápsula seguía bloqueada. Se corrigieron las condiciones iniciales y se verificó explícitamente la posición ante el plano de la hoja. No se presentan esos intentos como pruebas superadas. También se corrigió la orientación de las superficies nuevas, incluida su conversión a precisión de Unreal.

## Código, conservación y revisión pendiente

[Uso y reconstrucción](../../integration/valhalla_supercomputadora/unreal/README_V07_FUNCIONAL.md), [inventario](../../integration/valhalla_supercomputadora/unreal/Scripts/v07_door_inventory.json) y [resultados verificables](V07_FUNCIONAL_RESULTADOS.json).

Git publica código de importación, generación de geometría, reconstrucción del Blender de trabajo, autoría, preparación de copias, planes y verificadores. Los modelos, recursos UE y binarios siguen locales y excluidos por las reglas existentes; no se fuerza su inclusión ni se cambia la protección del repositorio. La generación parte del V07 anterior y del V04E conservado. La receta se repitió desde la exportación completa de todos los componentes: geometría generada, identidades de las 665 sustituciones, puertas y métricas coinciden exactamente con el manifiesto validado; no se elimina ningún actor estático directo.

Las pruebas y sus intentos previos permanecen en un directorio temporal autorizado y autocontenido, sin dependencias desde la entrega. No se borra ningún laboratorio. Unreal/UBA conservan sus cachés y trazas nativas del perfil; no son ubicaciones de entrega ni dependencias del juego.

**Preparado para inspección manual.** Quedan la aceptación personal de recorrido/cámara, especialmente en escaleras, y la valoración visual de los recintos de servicio. La iluminación y los materiales conservan carácter técnico. No se ha realizado un benchmark nuevo de toda la sala ni se declara acabado artístico, auditoría independiente o cierre formal de V07. Las salidas a cubiertas sin construir siguen protegidas.
