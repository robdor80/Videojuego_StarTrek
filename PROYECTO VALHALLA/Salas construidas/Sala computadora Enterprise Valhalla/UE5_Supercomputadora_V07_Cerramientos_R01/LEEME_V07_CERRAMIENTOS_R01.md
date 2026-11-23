# V07 — Cerramientos R01

Abrir `ValhallaComputer.uproject` con Unreal 5.8. El mapa de inicio es
`/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Cerramientos_R01_Corregida`.
Pulsar Play para recorrerlo con Quinn: WASD, ratón y espacio para saltar.

Esta revisión conserva las entregas anteriores y añade ocho puertas originales
de servidores funcionales, seis MEM corregidas, techo general con espesor,
rellenos de juntas de suelo y tres paredes terminales visibles de 12 cm.
Las paredes usan su propia geometría para la colisión. Los materiales existentes
y los recorridos de escaleras se conservan.

El modelo hermano `Sala_Supercomputadora_V07_Cerramientos_R01.blend` contiene
la misma geometría, materiales empaquetados y colecciones separadas para techo,
suelos y cierres. Los fotogramas 1, 60 y 120 muestran puertas cerradas, abiertas
y cerradas. Esta animación es una previsualización geométrica.

D02 (vestíbulo), D03 y D04 (pasillo este) conservan mecanismos completos.
Actualmente `DestinationConstructed=false` y `SecurityLocked=true`, porque
faltan sus destinos. No se han convertido en paredes. Tras modelar e integrar
suelo, paredes y techo detrás, validar el recorrido y establecer
`DestinationConstructed=true`, `SecurityLocked=false`. Blender por sí solo
no cambia estos permisos de Unreal.

Pendiente de diseño: dos grandes vacíos entre los volúmenes circulares y el
corredor curvo, aproximadamente centrados en UE (3363,1231,37) y
(3361,-741,37), de 72,57 y 78,01 m². Se conservan sin extender el suelo ni
inventar conexiones. Las salidas superior e inferior de escaleras sin destino
construido mantienen sus cierres visibles intencionados. No equivalen a techos
pendientes ni a puertas de servidores rotas.

Esta es una revisión recuperable para recorrer y revisar, no una declaración de
terminación de los destinos arquitectónicos pendientes. No inicia V08 ni cambios
de rendimiento. No necesita herramientas ni archivos de diagnóstico externos.
