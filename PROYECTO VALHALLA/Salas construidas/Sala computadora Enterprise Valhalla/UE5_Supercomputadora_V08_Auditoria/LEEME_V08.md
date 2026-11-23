# V08 — copia independiente para auditoría de rendimiento

Abrir `ValhallaComputer.uproject` con Unreal Engine 5.8.2 y pulsar Play.
Controles de Quinn: WASD, ratón y Espacio.

Base: V07 Cerramientos R01. Se conserva el identificador del mapa:
`/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Cerramientos_R01_Corregida`.
Los mapas, geometrías, materiales, colisiones y mecanismos de puertas proceden
sin cambios de esa entrega. Los README V07 incluidos son documentación heredada.

La configuración V08 habilita DirectX 12 / SM6, Lumen GI y reflejos, soporte
para trazado hardware y campos de distancia. La configuración inicial selecciona
DLSS Super Resolution Quality (66,666667 % por dimensión), con salida según la
resolución de la ventana. Para 2560 × 1600, usar esa resolución al iniciar el juego.
El plugin NVIDIA DLSS 8.9.0 / NGX 310.9.16 para UE 5.8 y su dependencia
StreamlineNGXCommon están incluidos localmente en Plugins.
Frame Generation no forma parte de esta copia.

Esta carpeta contiene el proyecto recuperable. La instrumentación experimental,
los planes de medición y las evidencias de la auditoría se entregan por separado.
No es necesario ejecutar herramientas de auditoría para abrir o recorrer el mapa.
Esta preparación de V08 no constituye una optimización ni una certificación de
rendimiento o estabilidad. Las entregas anteriores se conservan independientes.
