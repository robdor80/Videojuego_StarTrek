# Interacción potencial: evaluación, sin implementación

## Puertas y accesos

En el **OBJ original separado** hay geometría de puertas y paneles en grupos propios. La importación devuelve 630 objetos sin parentesco funcional y todos con el origen en cero. Deben identificarse las piezas que forman cada hoja, separar el marco fijo, establecer ejes/pivotes y medir volumen de retirada. Los controles pequeños `Doorpanel_*` no son las hojas. No se ejecutó animación, no hay un mecanismo de puertas entregado en esta auditoría y no se certifica que cada vano admita dos hojas correderas sin intervenir.

En **Recovery MAX** existen grupos `door3`, `door4`, `door04`–`door07` y piezas como `door01`, `Mesh1310`–`Mesh1321`, además de otras. La jerarquía ayuda a localizar piezas, pero su ensamblaje y escala tienen incidencias; no se recomienda copiar una animación de Sutherland sin medir cada caso. En la **colección**, las puertas/recesos se integran mayoritariamente en una malla por módulo (en GLB se separan por material, no por hoja). Un marco independiente sí existe como módulo; eso no implica hojas animables separadas.

Grado: **B/C** en geometría detallada, **C** en puertas fusionadas de colección, funcionamiento **E**. Primera comprobación futura: vano real, suelo/umbral, normal del plano, longitud de cada hoja, profundidad de bolsillo y colisión continua en ida/vuelta. La cabina representada no equivale a un turbolift que transporte personajes.

## Sillas y puestos humanos

El puente detallado contiene dos sillones centrales y tres asientos de estaciones reconocibles en las vistas. El OBJ permite recuperar piezas como `Box_6`–`Box_9`, `Armrest_5`–`Armrest_8`, `Layer__3`–`Layer__5` y componentes ChamferBox/MSB/Object. Los apoyabrazos y respaldos son geometría; el cuero es textura/material. No hay esqueleto, posición de sentarse, espacio de piernas certificado ni animación de ocupante.

Todos los orígenes cero impiden usar directamente las rotaciones locales como giros de asiento. La conversión MAX conserva algo de jerarquía de tres estaciones (`Group009`, `Group008`, `Group003`), pero también transformaciones no uniformes. Debe comprobarse la relación asiento–suelo/plataforma, orientación de rodillas, alcance de consola y paso detrás del respaldo con un personaje real. No reducir la cápsula para que parezca transitable. La colección no incluye sillas reconocibles en su subárbol del puente; habría que incorporarlas desde otra fuente o crearlas.

Grado: **B/C** para piezas del OBJ; **D** para sillas ausentes de la colección; ergonomía **E**.

## Consolas y pantalla principal

Hay carcasas, superficies de pantalla y remates recuperables como objetos OBJ. El GLB fusionado conserva materiales/primitivas pero necesitaría recuperar esa separación desde el original para editar por estación. Las imágenes LCARS prueban contenido visual estático; etiquetas Science, Security, Operations, etc., no prueban una función implementada ni la correspondencia canónica de cada ubicación.

La pantalla principal es una superficie representada, actualmente sin imagen operativa de vistas de nave. Los controles mostrados en LCARS están pintados, no modelados como botones. Para una vista ampliada harían falta superficies/rangos UV bien identificados, zona de activación, cámara/entrada/salida de interacción y contenido dinámico. Si la consola conserva marco y tablero juntos, podría mantenerse agrupada como estática y separar solo la salida de pantalla. No se creó ningún Widget, Render Target ni código.

Grado: **B** como formas editables, **C** para arte y comportamiento final.

## Circulación y NPC

Los rayos de pasillos rectos dan una sección holgada a escala interpretada, pero son mediciones sin radio. No certifican curvas, umbrales, escalones o el recorrido completo del puente. En la conversión MAX está probado un problema real de superficie de suelo; una colisión invisible que lo tape no restauraría el render ni justificaría elegir esa fuente.

Para el puente OBJ no se certifica todavía una ruta acceso→consola→silla→salida. Hacen falta suelo continuo, escalones adecuados, espacio de giro, cápsula del proyecto, barridos de altura y radio y verificación en CharacterMovement. Para NPC habría que definir puntos de aproximación, postura sentada, ocupación de estación, espera ante puerta y navegación/solicitud de apertura; nada de ello está incluido en el modelo.

## Lecciones de Sutherland con evidencia local

| Documento leído | Evidencia documentada | Aplicación conceptual en Voyager |
|---|---|---|
| `INFORME_FINAL_F07_P03G.md` (fuente local: `LABORATORIOS_3D/F07_P03FG_DoorLab/Reports/INFORME_FINAL_F07_P03G.md`) | Cuatro puertas, ocho hojas; recorridos, alojamientos físicos, pruebas Chaos y ruta D04 a cabina; otros destinos bloqueados | Reutilizar enfoque de raíz local, permisos/intención, ocupación de umbral y pruebas por puerta; recalcular medidas y bolsillos |
| `INFORME_FINAL_F07_CHAIR_01.md` (fuente local: `LABORATORIOS_3D/F07_Chair_AutoLab/Reports/INFORME_FINAL_F07_CHAIR_01.md`) | Seis sillas, 15 piezas móviles + base; avance 30 cm y pruebas de ida/vuelta | Separar base y partes móviles; no copiar 30 cm ni número de piezas al diseño Voyager |
| `INFORME_FINAL_F07_COLL_01.md` (fuente local: `LABORATORIOS_3D/F07_COLL_01_Lab/Reports/INFORME_FINAL_F07_COLL_01.md`) | 330 piezas fijas; colisión simple ajustada, revisión de falsos bloqueos; postura sentada todavía pendiente | Medir pasos con cápsula; las líneas no garantizan paso. Movimiento de silla correcto no certifica que un humano se siente |
| [P02_PIPELINE_PBR_BLINDAJE.md](../../roadmap/master/fases/F07/P02_PIPELINE_PBR_BLINDAJE.md) | Especificación de canales/espacios de color y laboratorio PBR procedural; no certifica conversión visual completa de Sutherland | Conservar albedo, definir PBR y emisión selectivamente; verificar materiales del recurso concreto |

Estos son **resultados comunicados por informes locales leídos**, no pruebas repetidas ahora ni garantías transferibles. Las medidas Sutherland, sus recorridos de 86,8 cm, el avance de silla de 30 cm, sus convexos y las rutas Recast **no se adoptan como medidas Voyager**. La carpeta `Sutherland_PBR_Lab` consultada solo aportó texturas; el BLEND PBR existente en la biblioteca fue inventariado, no abierto ni validado artísticamente en esta misión. No se cambió ningún recurso Sutherland.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
