# USS Sutherland — Parte A: estado recuperable con bloqueo D04

Fecha: 27/10/2026, Europe/Madrid. **PARTE A INCOMPLETA: D04 no supera la apertura jugable.**
Se detiene la integración funcional en este punto. No se ha eliminado, movido ni rebajado ninguna silla lateral para resolver problemas.

## Base elegida y proyecto

- Base: **SUTHERLAND_VISUAL_02**. Recuperación física: `C:\Users\andro\ST_ORG_01_FASE_3C_09\2026-10-25_02-17-38\RECUPERACION\P-e4252915fcf5`.
- Proyecto de trabajo único: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Unreal\SutherlandPlayable01.uproject`.
- Nivel: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`.
- UE5.8.2 CL56702186 y Blender 5.2.2 LTS comprobados en los logs.
- Las antiguas rutas Documents/StarTrek_3D/PLAYABLE_01 y VISUAL_02 ya no existen. Se localizaron respaldos de reorganización y se leyó su documentación.
- El mapa de VISUAL_02 recuperado coincide con su hash histórico verificado `935938535e566b9187cd58fe8aa86a16be97a53a4d978a5be53e85a64ad7b417`.
- PLAYABLE_01 es el antecesor funcional. VISUAL_02 conserva sus sistemas y su mejora visual. INTEGRACION_FINAL_01 fue contrastada en el rescate TABULA RASA: había retirado las seis sillas y 84 actores visuales; no se adoptó esa retirada. Los laboratorios experimentales no se incorporaron.
- Copia física: 2821 archivos, 3,811,562,912 bytes, verificados por SHA-256 antes de intervenir. Los originales permanecen separados y no se guardó sobre ellos.

## Etapas

| Etapa | Estado |
|---|---|
| A.1 Recuperar base | Verificada |
| A.2 Copia protegida | Verificada |
| A.3 Integrar geometría | Guardada y reabierta; 39 mallas visuales comprobadas |
| A.4 Conservar funcionamiento | Seis sillas y Quinn superan comprobaciones limitadas; D04 bloquea el cierre |
| A.5 Recuperación/documentación | Guardada, con estado anterior y estado integrado disponibles |

## Geometría, referencias y materiales

Se han actualizado **31 mallas visuales**, **ocho hojas móviles** y **51 grupos de colisión dependientes**, conservando los actores originales y sus nombres/referencias. Se importaron 90 assets derivados en `/Game/F07COLL01/Ergonomia03`; las mallas anteriores permanecen disponibles dentro de la misma copia. No hay otro proyecto ni nivel sustitutivo.

Las dos consolas centrales, agrupadas en Ergonomia_03, se exportaron en las 18 partes que espera VISUAL_02. Se comprobó la correspondencia de la topología antes de repartirlas. Las demás piezas actualizadas son los cinco objetos del capitán, paneles/carcasa/pantallas laterales, marcos y paneles interiores del turbo. Lista exacta de actores, assets anteriores y nuevos: `Data/mallas_actualizadas.csv`, `export_meshes.json` e `integration.json`.

Se mantuvieron los pivotes y transformaciones de los actores; la adaptación se exportó desde las coordenadas de Ergonomia_03. No se aplicó escala global. Los vértices guardados de las 31 visuales y ocho hojas se cotejaron en ambos sentidos con tolerancia 0,005 cm. Las ocho colisiones de hoja fueron extraídas del motor al reabrir: sus límites verticales coinciden con la geometría nueva dentro de 0,05 cm; no conservan los antiguos 391 cm.

Los materiales PBR originales se reasignaron por nombre importado y por correspondencia de cara con el Blender de VISUAL_02. Los nombres básicos del Blender Ergonomia_03 no sustituyeron esos grafos. UV de la geometría exportada conservados. No se regeneraron texturas ni se simplificaron materiales. Luces, cámara, TSR, Lumen y VSM permanecen heredados. La inspección GPU mostró el puente texturizado; no certifica aprobación artística ni equivalencia con Blender.

## Condición obligatoria: seis sillas laterales y capitán

Hay exactamente **Chair01–Chair06**, cada una con base fija, MovingRig y **15 componentes móviles**, además de la silla del capitán. Sus propiedades, mallas, materiales, transformaciones y actores visuales adjuntos coinciden con la línea base guardada. Ninguna silla lateral se importó de nuevo, se duplicó, se eliminó, se trasladó o cambió de altura.

Las seis completaron un ciclo nativo Toggle/AdvanceChair con barridos reales: recorrido 57 cm, retorno 0 cm de error, bases fijas y ninguna obstrucción. Detalles individuales en `Data/integration.json/ chair_checks`. La reapertura confirmó las conexiones y posiciones guardadas.

**Límite heredado comprobado:** VISUAL_02 contiene un solo STSeatAnchor con clips Sit/Seated/Stand, correspondiente al capitán. Los seis laterales tienen desplazamiento, ocupación y detección de obstrucción mediante STSlidingChair. No se encontraron seis sistemas de animación de sentarse/levantarse laterales que pudieran recuperarse; no se inventaron ni reconstruyeron en esta Parte A.

## Quinn y comprobación jugable limitada

Se conserva STPlayableQuinn, SKM_Quinn_Simple, ABP_Unarmed, controlador, controles y cámara. Escala de malla 1, cápsula radio 35 / semialtura 90 cm. Se preserva la referencia corporal histórica de **177,3 cm**; no se redimensionó a Quinn.

Los cinco marcadores de pose sentada del capitán se bajaron 14,8 cm para acompañar el sillón aceptado; Approach y Exit quedaron sobre el suelo original. Los tres clips y la lista de actores de colisión del asiento permanecen iguales.

Prueba GPU limitada, reutilizada del guion de VISUAL_02: **12/13 comprobaciones superadas**. Se verificaron posesión real, caminar con W y animación, interacción E, sentado con bloqueo de caminar, protección frente a salida ocupada, levantarse, cápsula y locomoción recuperadas. No se afirma circulación completa del puente ni prueba exhaustiva.

## Bloqueo D04 — no declarar completada la Parte A

Resultado fallido literal: `[{'name': 'D04 reaches full open through real Tick', 'passed': False, 'fraction': 6.165355443954468e-07}]`.

D04 acepta la solicitud de Quinn y conserva los permisos/destino construidos, pero su fracción de apertura no alcanza 1 durante Tick. El mecanismo no queda validado como funcional con las mallas/colisiones nuevas. No se ha diagnosticado qué componente impide el movimiento; no se atribuye una causa exacta sin un barrido de contacto.

Se conserva el código, Blueprint, configuración, geometría y mapa anterior de VISUAL_02. No se ha forzado la apertura, desactivado colisiones, inventado una habitación ni cambiado destinos/permisos. D01–D03 siguen bloqueadas por destino no construido; D04 sigue siendo la única que tiene cabina. No hay viaje entre cubiertas.

**Siguiente intervención necesaria para cerrar A.4:** diagnosticar únicamente los contactos de las hojas D04 con las mallas y colisiones nuevas y contrastar con el estado anterior conservado. Si no se puede conciliar sin cambiar la geometría aprobada o los mecanismos de forma segura, conservar ambos y consultar la decisión concreta. No modificar sillas laterales ni emprender la Parte B para ocultar este bloqueo.

## Inventario de colisiones

- 628 componentes primitivos inventariados: perfiles, canales Pawn/Camera, transformaciones, cajas, sensores y mallas; `Data/primitive_collision_inventory.json`.
- 330 actores técnicos SM_COLL presentes en la base y en la copia integrada.
- **279** permanecen idénticos al reabrir.
- **51** grupos afectados se adaptaron reutilizando cada hull anterior y su correspondencia con la superficie fuente. No se reemplazó la arquitectura general. Se conserva el número de formas por grupo; las cajas afectadas pueden quedar representadas como hulls UCX tras deformarlas. Esta representación y el ajuste superficial requieren revisión dirigida en B; no equivalen a certificar todas las paredes/objetos.
- Las tres barreras de destinos no construidos se conservaron y redujeron en altura; no mantienen el antiguo límite superior. Los sensores de puerta acompañan la nueva altura de paso. Las ocho hojas conservan un hull convexo cada una.
- La incidencia **pies suspendidos** permanece abierta hasta verificar expresamente apoyo y ergonomía. Completar la animación no demuestra su resolución.

## Incidencias técnicas conservadas

Los primeros intentos de guion encontraron una propiedad FBX inexistente y una suposición incorrecta sobre el perfil Custom de las visuales; se corrigió el guion sin guardar el nivel de esos intentos. Se conservan JSON/logs. El comprobador histórico de sillas se quedó esperando FinishAllCompilation; no se declaró aprobado. Se sustituyó por seis ciclos reales limitados, que sí produjeron resultados explícitos. Los procesos detenidos no tenían una escritura de mapa activa; se comprobó el hash original antes del guardado válido.

Los intentos de juego con NullRHI no completaron una prueba válida. El lanzamiento ExecCmds inicial tampoco transmitió el nombre de guion por las comillas de la ruta; se ejecutó desde la consola de la ventana real y se obtuvo el resultado GPU de 13 comprobaciones. Los datos incompletos se conservan separados y no se presentan como éxitos.

VSM Non-Nanite Marking Job Queue overflow, diferencias visuales heredadas y ergonomía de pies siguen documentados. No se hizo benchmark nuevo ni conversión Nanite.

## Integridad y recuperación

Hash del mapa integrado guardado: `cff10a2af8d8926d85951834d63b31117d0fe3420bb50007ae24ed8be9792d29`.

Rehash final: **2821/2821 archivos del proyecto fuente y 7 Blender originales sin diferencias**. `Data/final_integrity.json` conserva resultados y SHA-256 de todos los assets derivados. Cambios en archivos previos de la copia fuera de cachés: `['Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap']`. No hubo commit, push, pull request ni modificación de los originales.

- Estado original funcional: `Backups/BeforeIntegration/L_Sutherland_Playable01.umap`, con las mallas antiguas todavía disponibles en sus rutas /Game originales.
- Estado integrado con bloqueo D04: `Backups/L_Sutherland_Ergonomia03_Bloqueo_D04.umap`, idéntico por SHA-256 al mapa activo.
- Estado intermedio anterior al ajuste de barreras: `Backups/L_Sutherland_Playable01_BeforeGuardAdaptation.umap`.
- Instrucciones operativas: `CONTINUAR_AQUI.md`. No repetir 01_prepare ni 07_integrate sobre este estado; 07 se protege frente a un segundo ajuste de marcadores.

## Pendientes posteriores

Antes de cerrar Parte A: resolver/verificar D04 conservando ambos estados y las seis sillas.

Parte B: revisión sistemática de paredes/objetos, superficies adaptadas, circulación y colisiones. Parte C: revisión visual/ergonómica completa, apoyo de pies, cámaras y ajuste futuro de alturas de seis sillas únicamente cuando se autorice. No se ejecutaron esas fases.
